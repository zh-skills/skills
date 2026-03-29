---
name: read-webpage2
description: Fetch and display the plain-text content of any publicly accessible webpage URL. Use when the user wants to read, preview, or extract text from a webpage. Triggers on phrases like "read webpage", "fetch page", "what does this URL say", "get content from URL", or "/read-webpage".
---

# Read Webpage

Fetch a webpage URL and return a clean plain-text preview, stripping all HTML, scripts, and navigation noise.

## Workflow

1. Extract the URL from the user's message
2. Run `scripts/read_webpage.py <url>` to fetch and clean the page
3. Present the output to the user

## Trigger Examples

- `read webpage https://en.wikipedia.org/wiki/Hong_Kong`
- `fetch page https://example.com`
- `/read-webpage https://news.ycombinator.com`

## Output Format

```
📄 Preview of <url>

<first ~800 characters of clean text>

[Fetched N lines of text]
```

If the page cannot be reached, report the HTTP error clearly.

## Reference

For full implementation details and API endpoint usage, see [references/api_reference.md](references/api_reference.md).
