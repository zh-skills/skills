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


def detect_lang(text: str) -> str:
    """Detect language from user input: 'zh-hans', 'zh-hant', or 'en'."""
    # Known Simplified-only characters
    simplified = set('简体网页读书学习时间问题')
    # Known Traditional-only characters
    traditional = set('繁體網頁讀書學習時間問題')
    if not re.search(r'[\u4e00-\u9fff]', text):
        return 'en'
    simp_count = sum(1 for c in text if c in simplified)
    trad_count = sum(1 for c in text if c in traditional)
    return 'zh-hant' if trad_count > simp_count else 'zh-hans'


MSGS = {
    'en': {
        'preview':   '📄 Preview of {url}',
        'fetched':   '[Fetched {n} lines of text • {saved}]',
        'saved':     'Saved to {filename}',
        'save_fail': 'File save failed',
        'js_warn':   '⚠️ Only {n} line(s) found — this page is likely JavaScript-rendered.\nTry: use skill read-webpage-advanced {url}\nInstall: git clone https://github.com/zh-skills/skills',
    },
    'zh-hans': {
        'preview':   '📄 网页预览：{url}',
        'fetched':   '【已读取 {n} 行 • {saved}】',
        'saved':     '已保存至 {filename}',
        'save_fail': '文件保存失败',
        'js_warn':   '⚠️ 仅读取到 {n} 行——此网页可能使用 JavaScript 动态加载内容。\n建议改用：use skill read-webpage-advanced {url}\n安装：git clone https://github.com/zh-skills/skills',
    },
    'zh-hant': {
        'preview':   '📄 網頁預覽：{url}',
        'fetched':   '【已讀取 {n} 行 • {saved}】',
        'saved':     '已儲存至 {filename}',
        'save_fail': '檔案儲存失敗',
        'js_warn':   '⚠️ 僅讀取到 {n} 行——此網頁可能使用 JavaScript 動態載入內容。\n建議改用：use skill read-webpage-advanced {url}\n安裝：git clone https://github.com/zh-skills/skills',
    },
}


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


def read_webpage(url: str, max_chars: int = 800, save_dir: str = '.', lang: str = 'en') -> str:
    m = MSGS[lang if lang in MSGS else 'en']
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; SkillBot/1.0)'}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding  # fix garbled text / UTF-8 BOM
    soup = BeautifulSoup(resp.text, 'html.parser')
    for tag in soup(['script', 'style', 'noscript', 'nav', 'footer']):
        tag.decompose()
    text = soup.get_text(separator='\n')
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    full_text = '\n'.join(lines)

    # If very few lines fetched, page is likely JS-rendered — don't save, suggest advanced skill
    if len(lines) < 5:
        return m['js_warn'].format(n=len(lines), url=url)

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
            break  # success — do not retry
        except OSError as e:
            if attempt == 0:
                print(f"⚠️ Write error (attempt 1): {e} — retrying...")
            else:
                print(f"❌ Write failed after retry: {e}")
                filename = None

    saved_msg = m['saved'].format(filename=filename) if filename else m['save_fail']
    return (f"{m['preview'].format(url=url)}\n\n{preview}\n\n"
            f"{m['fetched'].format(n=len(lines), saved=saved_msg)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: read_webpage.py <url>")
        sys.exit(1)
    user_input = ' '.join(sys.argv)
    lang = detect_lang(user_input)
    print(read_webpage(sys.argv[1], lang=lang))
