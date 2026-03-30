#!/usr/bin/env python3
"""
speak_cantonese.py — Speak a Cantonese sentence aloud.

Modes:
  online (default) — uses edge-tts (Microsoft, free, requires internet)
  local            — uses macOS say command (Sinji voice)

Usage:
    python speak_cantonese.py {sentence}
    python speak_cantonese.py local {sentence}
    python speak_cantonese.py online {sentence}

Examples:
    python speak_cantonese.py 各個國家有各個國家嘅國歌
    python speak_cantonese.py local 各個國家有各個國家嘅國歌
"""

import sys
import os
import asyncio
import subprocess
import tempfile


VOICE = 'zh-HK-HiuMaanNeural'


def speak_online(sentence: str) -> str:
    try:
        import edge_tts
    except ImportError:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'edge-tts'],
                       capture_output=True)
        try:
            import edge_tts
        except ImportError:
            return "❌ edge-tts not installed. Run: pip install edge-tts"

    try:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            tmp = f.name
        asyncio.run(edge_tts.Communicate(sentence, VOICE).save(tmp))
        subprocess.run(['afplay', tmp])
        os.unlink(tmp)
        return f"🔊 Spoke (online): {sentence}"
    except Exception as e:
        return f"❌ edge-tts failed: {e}"


def speak_local(sentence: str) -> str:
    for voice in ['Sinji', 'Sin-ji']:
        check = subprocess.run(['say', '-v', voice, ''], capture_output=True)
        if check.returncode == 0:
            subprocess.run(['say', '-v', voice, sentence])
            return f"🔊 Spoke (local, {voice}): {sentence}"
    return "❌ No Cantonese voice found. Install Sinji in System Settings → Accessibility → Spoken Content."


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: speak_cantonese.py [online|local] {sentence}")
        sys.exit(1)

    args = sys.argv[1:]
    mode_args  = [a for a in args if a.lower() in ('online', 'local')]
    other_args = [a for a in args if a.lower() not in ('online', 'local')]
    mode       = mode_args[0].lower() if mode_args else 'online'
    sentence   = ' '.join(other_args)

    if not sentence:
        print("Please provide a sentence.")
        sys.exit(1)

    if mode == 'local':
        result = speak_local(sentence)
        if result.startswith('❌'):
            result = speak_online(sentence)
    else:
        result = speak_online(sentence)
        if result.startswith('❌'):
            result = speak_local(sentence)

    print(result)
