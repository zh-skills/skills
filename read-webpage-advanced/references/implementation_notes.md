# Implementation Notes — read-webpage-advanced

## Why Playwright Instead of requests + BeautifulSoup

Basic `requests.get()` only fetches the initial static HTML. Many modern websites load their content via JavaScript after the page loads — so `requests` returns an empty or near-empty page.

Playwright launches a real headless Chromium browser, waits for the JavaScript to finish executing (`wait_until='networkidle'`), then extracts the fully-rendered HTML. This captures content that basic HTTP requests cannot see.

## Key Differences vs read-webpage

| Feature | read-webpage | read-webpage-advanced |
|---------|-------------|----------------------|
| Static HTML pages | ✅ Fast | ✅ Works |
| JS-rendered pages | ❌ Returns 0 lines | ✅ Works |
| Speed | Fast (~1s) | Slower (~5-10s) |
| Dependencies | requests, beautifulsoup4 | playwright, beautifulsoup4 |
| Setup required | None | `playwright install chromium` |

## When to Use Each

- Start with `read-webpage` — it's faster and simpler
- If it returns 0 lines or very little content, switch to `read-webpage-advanced`

## Dependencies

```bash
pip install playwright beautifulsoup4
playwright install chromium
```

## Limitations

- Slower than basic fetch (launches a full browser)
- Some pages block headless browsers (Cloudflare, CAPTCHA-protected sites)
- Login-protected pages still cannot be accessed
