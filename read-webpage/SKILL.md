---
name: read-webpage
description: Fetch and display the plain-text content of any publicly accessible webpage URL. Use ONLY when the user explicitly says "use skill read-webpage", "用技能读网页" (Simplified Chinese), or "用技能讀網頁" (Traditional Chinese) followed by a URL. Do not trigger on generic "read webpage" or "fetch page" phrases — those should use the platform's built-in web fetch tool.
---

# Read Webpage

> 中文版本：[SKILL.zh.md](SKILL.zh.md)

Fetch a webpage URL and return a clean plain-text preview, stripping all HTML, scripts, and navigation noise.

## Workflow

1. Extract the URL from the user's message
2. Run `scripts/read_webpage.py {url}` to fetch and clean the page
3. The script saves the full text to a `.txt` file named after the URL and current date/time
4. Present the preview output and the saved filename to the user

## Trigger Examples

- `use skill read-webpage https://en.wikipedia.org/wiki/Artificial_intelligence`
- `use skill read-webpage https://zh.wikipedia.org/wiki/人工智能?variant=zh-hans`
- `use skill read-webpage https://zh.wikipedia.org/wiki/人工智能?variant=zh-hant`
- `用技能读网页 https://zh.wikipedia.org/wiki/人工智能?variant=zh-hans`
- `用技能讀網頁 https://zh.wikipedia.org/wiki/人工智能?variant=zh-hant`

If the page returns fewer than 5 lines (e.g. `https://quotes.toscrape.com/js/`), it is JS-rendered — use `read-dynamic-webpage` instead.

## Output Format

```
📄 Preview of {url}

{first ~800 characters of clean text}

[Fetched {N} lines of text • Saved to {filename}_{YYYYMMDD_HHMMSS}.txt]
```

The full text is saved to a `.txt` file named after the full URL and the current date/time (e.g. `zh.wikipedia.org_wiki_人工智能_variant=zh-hans_20260330_143022.txt`).

If the page cannot be reached, report the HTTP error clearly. If fewer than 5 lines are fetched, the page is likely JavaScript-rendered — suggest using `read-dynamic-webpage` instead and do not save a file.

## Language Detection

The script automatically detects the language from the user's input and responds accordingly:

- If the input contains Chinese characters (`\u4e00-\u9fff`), Chinese output is used
- Traditional Chinese is detected by the presence of Traditional-only characters (e.g. `網`, `頁`, `讀`, `儲`)
- Simplified Chinese is used as the default when Chinese is detected but Traditional markers are absent
- English is used when no Chinese characters are found

Output messages (preview header, fetched line count, saved filename) are localised to the detected language. The saved `.txt` file content is always in the original language of the webpage.

## Important

Run `scripts/read_webpage.py` only once per request. Each run saves exactly one `.txt` file. Before retrying, check whether a `.txt` file was already saved — if it was, the run succeeded and no retry is needed.

For full implementation details and API endpoint usage, see [references/api_reference.md](references/api_reference.md).
