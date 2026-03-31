#!/usr/bin/env python3
"""
read_dynamic_webpage.py — Fetch plain text from any webpage, including JS-rendered pages.
Uses Playwright headless browser. Saves full text to a .txt file named after the URL + date/time.

Setup (first time only):
    pip install playwright
    playwright install chromium

Usage:
    python read_dynamic_webpage.py <url>

Examples:
    python read_dynamic_webpage.py https://quotes.toscrape.com/js/
    python read_dynamic_webpage.py https://en.wikipedia.org/wiki/Artificial_intelligence
    python read_dynamic_webpage.py https://zh.wikipedia.org/wiki/人工智能?variant=zh-hant
    python read_dynamic_webpage.py https://zh.wikipedia.org/wiki/人工智能?variant=zh-hans
    python read_dynamic_webpage.py https://zh.wikipedia.org/wiki/人工智能?variant=zh-hant
    python read_dynamic_webpage.py https://zh.wikipedia.org/wiki/人工智能?variant=zh-hans
"""

import sys
import re
import os
from datetime import datetime


def make_filename(url: str) -> str:
    """Derive a safe filename from the full URL + current date/time."""
    name = re.sub(r'^https?://', '', url)
    name = re.sub(r'[/:?&]', '_', name)
    name = re.sub(r'_+', '_', name).strip('_')
    name = name[:80]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{name}_{timestamp}.txt"


def ensure_playwright():
    """Check if playwright is installed. If not, offer to install it automatically."""
    try:
        from playwright.sync_api import sync_playwright
        return True
    except ImportError:
        print("⚠️ Playwright is not installed in your current Python environment.")
        print(f"   Python: {sys.executable}")
        answer = input("   Install it now? (yes/no): ").strip().lower()
        if answer in ('yes', 'y'):
            import subprocess
            print("   Installing playwright...")
            # Use --user flag to handle externally-managed Python environments (e.g. Homebrew)
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '--user', 'playwright'],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                # Fallback: try without --user (works in venvs)
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', 'playwright'],
                    capture_output=True, text=True
                )
            if result.returncode != 0:
                print(f"   ❌ Installation failed: {result.stderr.strip()}")
                print("   Try manually: pip install --user playwright && playwright install chromium")
                return False
            print("   Installing Chromium browser...")
            subprocess.check_call([sys.executable, '-m', 'playwright', 'install', 'chromium'])
            print("   ✅ Done. Re-run the script to continue.")
        else:
            print("   Skipped. Run manually: pip install playwright && playwright install chromium")
        return False


def read_dynamic_webpage(url: str, max_chars: int = 800, save_dir: str = '.') -> str:
    if not ensure_playwright():
        return "❌ Playwright not installed. Re-run the script after installation."
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return "❌ Playwright not installed. Run: pip install playwright && playwright install chromium"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle', timeout=30000)
        # Wait for body content to load
        page.wait_for_selector('body', timeout=10000)
        html = page.content()
        browser.close()

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html.lstrip('\ufeff'), 'html.parser')
    for tag in soup(['script', 'style', 'noscript', 'nav', 'footer']):
        tag.decompose()
    text = soup.get_text(separator='\n')
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    full_text = '\n'.join(lines)
    preview = full_text[:max_chars]

    # Save full text to file, retry once on write error
    filename = make_filename(url)
    filepath = os.path.join(save_dir, filename)
    for attempt in range(2):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"URL: {url}\n")
                f.write(f"Fetched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Lines: {len(lines)}\n")
                f.write('─' * 60 + '\n\n')
                f.write(full_text)
            break
        except OSError as e:
            if attempt == 0:
                print(f"⚠️ Write error (attempt 1): {e} — retrying...")
            else:
                print(f"❌ Write failed after retry: {e}")
                filename = None

    saved_msg = f"Saved to {filename}" if filename else "File save failed"
    return (f"📄 Preview of {url}\n\n{preview}\n\n"
            f"[Fetched {len(lines)} lines of text • {saved_msg}]")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: read_dynamic_webpage.py <url>")
        sys.exit(1)
    print(read_dynamic_webpage(sys.argv[1]))
