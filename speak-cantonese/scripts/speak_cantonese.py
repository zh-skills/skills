#!/usr/bin/env python3
"""
speak_cantonese.py — Convert a Cantonese sentence to speech and save as mp3.

Modes:
  online (default) — uses edge-tts (Microsoft, free, requires internet)
  local            — uses system TTS (macOS 'say' Sinji voice or Windows pyttsx3)
  Falls back to the other mode if the chosen one fails.

Setup:
    pip install edge-tts pygame        # for online mode
    pip install pyttsx3                # for local mode on Windows

Usage:
    python speak_cantonese.py {sentence}
    python speak_cantonese.py online {sentence}
    python speak_cantonese.py local {sentence}

Examples:
    python speak_cantonese.py 各個國家有各個國家嘅國歌
    python speak_cantonese.py local 各個國家有各個國家嘅國歌
    python speak_cantonese.py online 香港係一個國際城市
"""

import sys
import os
import asyncio
import platform
import subprocess
from datetime import datetime


VOICE    = 'zh-HK-HiuMaanNeural'   # edge-tts Cantonese HK voice
SPEECHES = 'speeches'


# ── Dependency check ──────────────────────────────────────────────────────────

def ensure_online_deps():
    """Check edge-tts. Auto-install into the current Python environment."""
    try:
        import edge_tts  # noqa
        return True
    except ImportError:
        pass
    print("⚠️ edge-tts not found. Installing automatically...")
    # Install into the exact Python running this script (not --user which may go elsewhere)
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', 'edge-tts'],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("   ✅ edge-tts installed. Continuing...")
        # Force reimport
        import importlib
        try:
            import edge_tts  # noqa
            return True
        except ImportError:
            pass
    print(f"   ❌ Installation failed: {result.stderr.strip()[:200]}")
    return False


# ── System TTS (local) ────────────────────────────────────────────────────────

def speak_local(sentence: str, filepath: str):
    """
    Try system TTS.
    Returns (success, method, error, actual_filepath).
    macOS: uses 'say' with Sinji (zh_HK) voice, saves to aiff then converts to mp3.
    Windows: uses pyttsx3.
    """
    system = platform.system()

    if system == 'Darwin':
        for voice in ['Sinji', 'Sin-ji', 'Meijia']:
            check = subprocess.run(['say', '-v', voice, ''], capture_output=True)
            if check.returncode != 0:
                continue
            aiff_path = filepath.replace('.mp3', '.aiff')
            # Save to file only — no playback (say without -o plays audio)
            result = subprocess.run(
                ['say', '-v', voice, '-o', aiff_path, '--', sentence],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                # Try converting aiff → mp3 via ffmpeg
                conv = subprocess.run(
                    ['ffmpeg', '-y', '-i', aiff_path, filepath],
                    capture_output=True
                )
                if conv.returncode == 0:
                    os.remove(aiff_path)
                    return True, f"macOS system voice ({voice})", "", filepath
                else:
                    # Keep aiff if ffmpeg not available
                    return True, f"macOS system voice ({voice})", "", aiff_path
        return False, "", "No Cantonese voice found. Install Sinji in System Settings → Accessibility → Spoken Content.", filepath

    elif system == 'Windows':
        try:
            import pyttsx3
            engine = pyttsx3.init()
            for v in engine.getProperty('voices'):
                if any(k in v.name.lower() for k in ['cantonese', 'hong kong', 'tracy']):
                    engine.setProperty('voice', v.id)
                    break
            engine.save_to_file(sentence, filepath)
            engine.runAndWait()
            return True, "Windows system voice", "", filepath
        except ImportError:
            return False, "", "pyttsx3 not installed. Run: pip install pyttsx3", filepath
        except Exception as e:
            return False, "", str(e), filepath

    return False, "", f"Local TTS not supported on {system}", filepath


# ── Online TTS (edge-tts) ─────────────────────────────────────────────────────

async def _synthesize_edge(text: str, output: str):
    import edge_tts
    await edge_tts.Communicate(text, VOICE).save(output)


def speak_online(sentence: str, filepath: str):
    """Try edge-tts. Returns (success, method, error, filepath)."""
    try:
        import edge_tts  # noqa
    except ImportError:
        if not ensure_online_deps():
            return False, "", "edge-tts not installed. Re-run after installation.", filepath
    try:
        asyncio.run(_synthesize_edge(sentence, filepath))
        return True, "edge-tts (online, Microsoft zh-HK-HiuMaanNeural)", "", filepath
    except Exception as e:
        return False, "", str(e), filepath


# ── Playback ──────────────────────────────────────────────────────────────────

def play_audio(filepath: str):
    """No-op — audio is saved to file. User opens it to listen."""
    pass


# ── Main ──────────────────────────────────────────────────────────────────────

def speak_cantonese(sentence: str, mode: str = 'online', save_dir: str = '.') -> str:
    os.makedirs(os.path.join(save_dir, SPEECHES), exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename  = f"cantonese_{timestamp}.mp3"
    filepath  = os.path.join(save_dir, SPEECHES, filename)

    if mode == 'local':
        success, method, error, filepath = speak_local(sentence, filepath)
        if not success:
            print(f"⚠️ Local TTS failed: {error}")
            print("   Falling back to edge-tts (online)...")
            success, method, error, filepath = speak_online(sentence, filepath)
    else:
        success, method, error, filepath = speak_online(sentence, filepath)
        if not success:
            print(f"⚠️ edge-tts failed: {error}")
            print("   Falling back to local system TTS...")
            success, method, error, filepath = speak_local(sentence, filepath)

    if not success:
        return f"❌ Both TTS methods failed.\nLast error: {error}\nTry: pip install edge-tts pygame"

    play_audio(filepath)
    saved_name = os.path.basename(filepath)
    return (f"🔊 Cantonese audio ready: {sentence}\n"
            f"   Using: {method}\n\n"
            f"[Saved to {SPEECHES}/{saved_name} — open to listen]")


# ── File mode ─────────────────────────────────────────────────────────────────

def clean_line(line: str) -> str:
    """Strip markdown formatting from a line."""
    import re
    line = re.sub(r'^#{1,6}\s*', '', line)
    line = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', line)
    line = re.sub(r'^\d+\.\s*', '', line)
    line = re.sub(r'^[-*•]\s*', '', line)
    line = re.sub(r'\(.*?\)', '', line)
    return line.strip()


def speak_cantonese_file(filepath: str, mode: str = 'online', save_dir: str = '.') -> str:
    """Read a text file line by line and speak each line."""
    if not os.path.isfile(filepath):
        return f"❌ File not found: {filepath}"

    with open(filepath, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()

    lines = [clean_line(l) for l in raw_lines]
    lines = [l for l in lines if len(l) >= 1 and any('\u4e00' <= c <= '\u9fff' for c in l)]

    if not lines:
        return f"❌ No speakable Cantonese content found in: {filepath}"

    os.makedirs(os.path.join(save_dir, SPEECHES), exist_ok=True)
    timestamp   = datetime.now().strftime('%Y%m%d_%H%M%S')
    saved_files = []
    method_used = ""

    for i, line in enumerate(lines):
        print(f"[{i+1}/{len(lines)}] {line}")
        filename = f"cantonese_{timestamp}_{i+1:03d}.mp3"
        fp       = os.path.join(save_dir, SPEECHES, filename)

        if mode == 'local':
            success, method, error, fp = speak_local(line, fp)
            if not success:
                success, method, error, fp = speak_online(line, fp)
        else:
            success, method, error, fp = speak_online(line, fp)
            if not success:
                success, method, error, fp = speak_local(line, fp)

        if success:
            method_used = method
            # Skip pygame playback if macOS say already played the audio
            if 'macOS' not in method:
                play_audio(fp)
            saved_files.append(os.path.basename(fp))
        else:
            print(f"   ⚠️ Skipped (TTS failed): {error}")

    # Synthesise combined mp3 (only if edge-tts available)
    combined_name = f"cantonese_{timestamp}_combined.mp3"
    combined_path = os.path.join(save_dir, SPEECHES, combined_name)
    try:
        import edge_tts as _edge_tts_check  # noqa
        full_text = "。".join(lines)
        asyncio.run(_synthesize_edge(full_text, combined_path))
        combined_msg = f"Combined: {SPEECHES}/{combined_name}"
    except ImportError:
        combined_msg = "Combined mp3 skipped (edge-tts not installed). Run: pip install edge-tts"
    except Exception as e:
        combined_msg = f"Combined file failed: {e}"

    return (f"🔊 Spoke {len(saved_files)}/{len(lines)} lines from: {filepath}\n"
            f"   Using: {method_used}\n\n"
            f"[{combined_msg}]")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: speak_cantonese.py [online|local] {sentence}")
        print("       speak_cantonese.py [online|local] file {filepath}")
        sys.exit(1)

    args = sys.argv[1:]
    mode = 'online'

    # Extract mode if specified
    if args[0].lower() in ('online', 'local'):
        mode = args[0].lower()
        args = args[1:]

    if not args:
        print("Please provide a sentence or 'file {filepath}'.")
        sys.exit(1)

    # File mode
    if args[0].lower() == 'file':
        if len(args) < 2:
            print("Please provide a filepath after 'file'.")
            sys.exit(1)
        filepath = ' '.join(args[1:])
        print(speak_cantonese_file(filepath, mode=mode))
    else:
        sentence = ' '.join(args)
        print(speak_cantonese(sentence, mode=mode))
