#!/usr/bin/env python3
"""
play_mp3.py — Play an mp3 file using the system audio player.

Usage:
    python play_mp3.py {filename}

Examples:
    python play_mp3.py voice.mp3
    python play_mp3.py cantonese_20260331_065110.mp3
"""

import sys
import os
import subprocess
import platform


def play_mp3(filepath: str) -> str:
    if not os.path.isfile(filepath):
        return f"❌ File not found: {filepath}"

    system = platform.system()
    try:
        if system == 'Darwin':
            subprocess.run(['afplay', filepath], timeout=120)
        elif system == 'Windows':
            subprocess.run(['start', '', filepath], shell=True, timeout=120)
        else:
            subprocess.run(['aplay', filepath], timeout=120)
        return f"🔊 Playing: {filepath}\n✅ Done"
    except subprocess.TimeoutExpired:
        return f"⚠️ Playback timed out: {filepath}"
    except Exception as e:
        return f"❌ Playback failed: {e}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: play_mp3.py {filename}")
        sys.exit(1)
    filepath = ' '.join(sys.argv[1:])
    print(play_mp3(filepath))
