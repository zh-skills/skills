---
name: read-webpage
description: Fetch and display the plain-text content of any publicly accessible webpage URL. Use ONLY when the user explicitly says "use skill read-webpage" followed by a URL. Do not trigger on generic "read webpage" or "fetch page" phrases — those should use the platform's built-in web fetch tool.
---

# Read Webpage

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

## Output Format

```
📄 Preview of {url}

{first ~800 characters of clean text}

[Fetched {N} lines of text • Saved to {filename}_{YYYYMMDD_HHMMSS}.txt]
```

The full text is saved to a `.txt` file named after the full URL and the current date/time (e.g. `zh.wikipedia.org_wiki_人工智能_variant=zh-hans_20260330_143022.txt`).

If the page cannot be reached, report the HTTP error clearly.

## Important

Run `scripts/read_webpage.py` only once per request. Each run saves exactly one `.txt` file. Before retrying, check whether a `.txt` file was already saved — if it was, the run succeeded and no retry is needed.

For full implementation details and API endpoint usage, see [references/api_reference.md](references/api_reference.md).
