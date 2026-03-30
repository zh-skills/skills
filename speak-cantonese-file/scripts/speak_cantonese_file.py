#!/usr/bin/env python3
"""
speak_cantonese_file.py — Read a text file line by line, speak each line in Cantonese,
and save each line as an mp3 file in the current directory.

Usage:
    python speak_cantonese_file.py {filename}

Examples:
    python speak_cantonese_file.py cantonese-challenge-1.txt
    python speak_cantonese_file.py speech-Cantonese.txt
"""

import sys
import asyncio
import subprocess
import os
import re
import platform
from datetime import datetime


VOICE = 'zh-HK-HiuMaanNeural'


def ensure_edge_tts():
    try:
        import edge_tts  # noqa
        return True
    except ImportError:
        print("⚠️ edge-tts not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'edge-tts'],
                       capture_output=True)
        try:
            import edge_tts  # noqa
            return True
        except ImportError:
            print("❌ edge-tts install failed. Run: pip install edge-tts")
            return False


def clean_line(line: str) -> str:
    """Strip markdown formatting."""
    line = re.sub(r'^#{1,6}\s*', '', line)
    line = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', line)
    line = re.sub(r'^\d+\.\s*', '', line)
    line = re.sub(r'^[-*•]\s*', '', line)
    line = re.sub(r'\(.*?\)', '', line)
    return line.strip()


def play(filepath: str):
    system = platform.system()
    if system == 'Darwin':
        subprocess.run(['afplay', filepath])
    elif system == 'Windows':
        subprocess.run(['start', '', filepath], shell=True)
        import time; time.sleep(3)
    else:
        subprocess.run(['aplay', filepath])


def speak_file(filepath: str) -> str:
    if not os.path.isfile(filepath):
        return f"❌ File not found: {filepath}"

    if not ensure_edge_tts():
        return "❌ edge-tts not available."

    import edge_tts

    with open(filepath, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()

    lines = [clean_line(l) for l in raw_lines]
    lines = [l for l in lines if len(l) >= 1 and re.search(r'\w', l)]

    if not lines:
        return f"❌ No speakable content found in: {filepath}"

    timestamp   = datetime.now().strftime('%Y%m%d_%H%M%S')
    saved_files = []

    for i, line in enumerate(lines):
        print(f"[{i+1}/{len(lines)}] {line}")
        filename = f"cantonese_{timestamp}_{i+1:03d}.mp3"
        filepath_out = os.path.join(os.getcwd(), filename)
        try:
            asyncio.run(edge_tts.Communicate(line, VOICE).save(filepath_out))
            play(filepath_out)
            saved_files.append(filename)
        except Exception as e:
            print(f"   ⚠️ Skipped: {e}")

    return (f"🔊 Spoke {len(saved_files)}/{len(lines)} lines from: {filepath}\n"
            f"[Saved {len(saved_files)} mp3 files in current directory]")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: speak_cantonese_file.py {filename}")
        sys.exit(1)

    filename = ' '.join(sys.argv[1:])
    print(speak_file(filename))
