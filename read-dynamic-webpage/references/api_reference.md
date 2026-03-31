# API Reference — read-dynamic-webpage

## Python Implementation

```python
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def read_dynamic_webpage(url: str, max_chars: int = 800) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle', timeout=30000)
        page.wait_for_selector('body', timeout=10000)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html.lstrip('\ufeff'), 'html.parser')
    for tag in soup(['script', 'style', 'noscript', 'nav', 'footer']):
        tag.decompose()
    text = soup.get_text(separator='\n')
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    preview = '\n'.join(lines)[:max_chars]
    return f"📄 Preview of {url}\n\n{preview}\n\n[Fetched {len(lines)} lines of text]"
```

## Dependencies

- `playwright` — headless browser for JS-rendered pages
- `beautifulsoup4` — HTML parsing

Install:
```bash
pip install playwright beautifulsoup4
playwright install chromium
```

## Saved Output File

The full page text is saved to a `.txt` file in the current directory:
- Filename format: `{url_as_filename}_{YYYYMMDD_HHMMSS}.txt`
- Example: `www.cityu.edu.hk_fo_htm_tpg_fees.htm_20260330_110515.txt`
- File contains: URL, fetch timestamp, line count, and full plain text

## Limitations

- Slower than `read-webpage` (~5-10s vs ~1s) — launches a full browser
- Some pages block headless browsers (Cloudflare, CAPTCHA-protected sites)
- Login-protected pages cannot be accessed
- Preview capped at 800 characters by default (adjustable via `max_chars`)
