---
name: read-webpage-advanced
description: Fetch and display the plain-text content of any webpage URL, including JavaScript-rendered pages. Use ONLY when the user explicitly says "use skill read-webpage-advanced" followed by a URL. Handles both static HTML and dynamic JS-rendered pages using a headless browser (Playwright). Saves full text to a .txt file named after the URL and date/time.
---

# Read Webpage Advanced

Fetch any webpage — including JavaScript-rendered pages — and return clean plain-text content. Uses Playwright headless browser to handle dynamic content that basic HTTP requests cannot access.

## When to Use This Skill vs read-webpage

- Use `read-webpage` for static HTML pages (Wikipedia, news articles, university programme pages)
- Use `read-webpage-advanced` when `read-webpage` returns 0 lines or very little content — this means the page is JS-rendered

## Workflow

1. Extract the URL from the user's message
2. Run `scripts/read_webpage_advanced.py {url}` to fetch using headless browser
3. The script saves the full text to a `.txt` file named after the URL and current date/time
4. Present the preview output and the saved filename to the user

## Important

Run `scripts/read_webpage_advanced.py` only once per request. Each run saves exactly one `.txt` file. Before retrying, check whether a `.txt` file was already saved — if it was, the run succeeded and no retry is needed.

## Trigger Examples

- `use skill read-webpage-advanced https://www.cityu.edu.hk/fo/htm/tpg_fees.htm`
- `use skill read-webpage-advanced https://en.wikipedia.org/wiki/Artificial_intelligence`
- `use skill read-webpage-advanced https://zh.wikipedia.org/wiki/人工智能?variant=zh-hans`
- `use skill read-webpage-advanced https://zh.wikipedia.org/wiki/人工智能?variant=zh-hant`

## Output Format

```
📄 Preview of {url}

{first ~800 characters of clean text}

[Fetched {N} lines of text • Saved to {filename}_{YYYYMMDD_HHMMSS}.txt]
```

If the page cannot be reached, report the HTTP error clearly.

## Setup

Install Playwright and its browser on first use:
```bash
pip install playwright
playwright install chromium
```

## Reference

For implementation details see [references/implementation_notes.md](references/implementation_notes.md) and [references/api_reference.md](references/api_reference.md).
