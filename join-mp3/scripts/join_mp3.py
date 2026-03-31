#!/usr/bin/env python3
"""
join_mp3.py — Join all mp3 files in a subfolder into one combined mp3 file.
Files are joined in alphabetical order. Output saved in current directory.

Limits:
  - Per file: max 10 MB
  - Total: max 50 MB
  - File count: max 50 files

Usage:
    python join_mp3.py {subfolder}

Examples:
    python join_mp3.py speeches
    python join_mp3.py cantonese_audio
"""

import sys
import os
import subprocess
from datetime import datetime


MAX_FILE_MB  = 10
MAX_TOTAL_MB = 50
MAX_FILES    = 50
MB           = 1024 * 1024


def join_mp3(subfolder: str) -> str:
    if not os.path.isdir(subfolder):
        return f"❌ Folder not found: {subfolder}"

    # Collect mp3 files sorted alphabetically
    all_files = sorted([
        f for f in os.listdir(subfolder)
        if f.lower().endswith('.mp3')
    ])

    if not all_files:
        return f"❌ No mp3 files found in: {subfolder}"

    # Apply limits
    accepted = []
    skipped  = []
    total_size = 0

    for f in all_files:
        if len(accepted) >= MAX_FILES:
            skipped.append(f"{f} (file count limit {MAX_FILES} reached)")
            continue
        filepath = os.path.join(subfolder, f)
        size = os.path.getsize(filepath)
        if size > MAX_FILE_MB * MB:
            skipped.append(f"{f} ({size // MB}MB > {MAX_FILE_MB}MB limit)")
            continue
        if total_size + size > MAX_TOTAL_MB * MB:
            skipped.append(f"{f} (total size limit {MAX_TOTAL_MB}MB reached)")
            continue
        accepted.append(filepath)
        total_size += size

    if not accepted:
        return f"❌ No files within limits in: {subfolder}"

    # Check ffmpeg available
    check = subprocess.run(['ffmpeg', '-version'], capture_output=True)
    if check.returncode != 0:
        return "❌ ffmpeg not found. Install with: brew install ffmpeg"

    # Write concat list file
    timestamp   = datetime.now().strftime('%Y%m%d_%H%M%S')
    list_file   = f"join_mp3_{timestamp}_list.txt"
    output_file = f"joined_{timestamp}.mp3"

    with open(list_file, 'w') as f:
        for fp in accepted:
            f.write(f"file '{os.path.abspath(fp)}'\n")

    try:
        result = subprocess.run(
            ['ffmpeg', '-y', '-f', 'concat', '-safe', '0',
             '-i', list_file, '-c', 'copy', output_file],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            return f"❌ ffmpeg failed: {result.stderr[-300:]}"

        output_path = os.path.abspath(output_file)
        msg = f"✅ Joined {len(accepted)} files from {subfolder}/\n[Saved to {output_path}]"
        if skipped:
            msg += f"\n⚠️ Skipped {len(skipped)} files:\n" + "\n".join(f"  - {s}" for s in skipped)
        return msg
    finally:
        if os.path.exists(list_file):
            os.remove(list_file)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: join_mp3.py {subfolder}")
        sys.exit(1)
    subfolder = ' '.join(sys.argv[1:])
    print(join_mp3(subfolder))
