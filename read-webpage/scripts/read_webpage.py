#!/usr/bin/env python3
"""
read_webpage.py — Fetch and preview plain text from a webpage URL.
Saves full text to a .txt file named after the webpage + date + time.

Usage:
    python read_webpage.py <url>

Examples:
    python read_webpage.py https://en.wikipedia.org/wiki/Artificial_intelligence
    python read_webpage.py https://zh.wikipedia.org/wiki/人工智能?variant=zh-hant
    python read_webpage.py https://zh.wikipedia.org/wiki/人工智能?variant=zh-hans
"""

import sys
import re
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def make_filename(url: str) -> str:
    """Derive a safe filename from the full URL + current date + time."""
    # Strip scheme (https://)
    name = re.sub(r'^https?://', '', url)
    # Replace invalid filename characters with underscores
    name = re.sub(r'[/:?&]', '_', name)
    # Collapse multiple underscores
    name = re.sub(r'_+', '_', name).strip('_')
    # Limit length
    name = name[:80]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{name}_{timestamp}.txt"


def read_webpage(url: str, max_chars: int = 800, save_dir: str = '.') -> str:
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; SkillBot/1.0)'}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    for tag in soup(['script', 'style', 'noscript', 'nav', 'footer']):
        tag.decompose()
    text = soup.get_text(separator='\n')
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    full_text = '\n'.join(lines)
    preview = full_text[:max_chars]

    # Save full text to file
    filename = make_filename(url)
    filepath = os.path.join(save_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"URL: {url}\n")
        f.write(f"Fetched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Lines: {len(lines)}\n")
        f.write('─' * 60 + '\n\n')
        f.write(full_text)

    return (f"📄 Preview of {url}\n\n{preview}\n\n"
            f"[Fetched {len(lines)} lines of text • Saved to {filename}]")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: read_webpage.py <url>")
        sys.exit(1)
    print(read_webpage(sys.argv[1]))
