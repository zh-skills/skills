#!/usr/bin/env python3
"""
read_webpage.py — Fetch and preview plain text from a webpage URL.

Usage:
    python read_webpage.py <url>

Examples:
    python read_webpage.py https://en.wikipedia.org/wiki/ai
    python read_webpage.py https://zh.wikipedia.org/wiki/人工智能?variant=zh-hant
    python read_webpage.py https://zh.wikipedia.org/wiki/人工智能?variant=zh-hans
"""

import sys
import requests
from bs4 import BeautifulSoup


def read_webpage(url: str, max_chars: int = 800) -> str:
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; SkillBot/1.0)'}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    for tag in soup(['script', 'style', 'noscript', 'nav', 'footer']):
        tag.decompose()
    text = soup.get_text(separator='\n')
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    preview = '\n'.join(lines)[:max_chars]
    return f"📄 Preview of {url}\n\n{preview}\n\n[Fetched {len(lines)} lines of text]"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: read_webpage.py <url>")
        sys.exit(1)
    print(read_webpage(sys.argv[1]))
