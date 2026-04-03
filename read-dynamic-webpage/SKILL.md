---
name: read-dynamic-webpage
description: Fetch and display the plain-text content of any webpage URL, including JavaScript-rendered pages. Use ONLY when the user explicitly says "use skill read-dynamic-webpage", "用技能讀動態網頁" (Traditional Chinese), or "用技能读动态网页" (Simplified Chinese) followed by a URL. Handles dynamic JS-rendered pages using a headless browser (Playwright). Saves full text to a .txt file named after the URL and date/time.
---

# Read Dynamic Webpage

> 中文版本：[SKILL.zh.md](SKILL.zh.md)

Fetch any webpage — including JavaScript-rendered pages — and return clean plain-text content. Uses Playwright headless browser to handle dynamic content that basic HTTP requests cannot access.

## When to Use This Skill vs read-webpage

- Use `read-webpage` for static HTML pages (Wikipedia, news articles, university programme pages)
- Use `read-dynamic-webpage` when `read-webpage` returns 0 lines or very little content — this means the page is JS-rendered

## Workflow

1. Extract the URL from the user's message
2. Run `scripts/read_dynamic_webpage.py {url}` to fetch using headless browser
3. The script saves the full text to a `.txt` file named after the URL and current date/time
4. Present the preview output and the saved filename to the user

## Important

Run `scripts/read_dynamic_webpage.py` only once per request. Each run saves exactly one `.txt` file. Before retrying, check whether a `.txt` file was already saved — if it was, the run succeeded and no retry is needed.

## Trigger Examples

- `use skill read-dynamic-webpage https://quotes.toscrape.com/js/`
- `use skill read-dynamic-webpage https://en.wikipedia.org/wiki/Artificial_intelligence`
- `use skill read-dynamic-webpage https://zh.wikipedia.org/wiki/人工智能?variant=zh-hans`
- `use skill read-dynamic-webpage https://zh.wikipedia.org/wiki/人工智能?variant=zh-hant`
- `用技能讀動態網頁 https://quotes.toscrape.com/js/`
- `用技能读动态网页 https://quotes.toscrape.com/js/`

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
python -m playwright install chromium
```

## Reference

For implementation details see [references/implementation_notes.md](references/implementation_notes.md) and [references/api_reference.md](references/api_reference.md).
