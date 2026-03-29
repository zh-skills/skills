---
name: read-webpage
description: Fetch and preview the text content of any webpage URL. Use when the user wants to read, summarise, or extract information from a webpage. Trigger when user says "read webpage", "fetch page", "get content from URL", or provides a URL and asks what it says.
---

# Read Webpage Skill

This skill fetches the plain text content of any publicly accessible webpage and presents a readable preview to the user.

## When to Use

**Trigger phrases:**
- `read webpage <url>`
- `fetch page <url>`
- `read <url>`
- `what does <url> say`
- `/read-webpage <url>`

## How It Works

1. Extract the URL from the user's message
2. Fetch the page using an HTTP GET request with a browser-like User-Agent header
3. Strip all HTML tags, scripts, styles, and navigation noise using BeautifulSoup
4. Return the first ~800 characters of clean text as a preview

## Usage Example

**User input:**
```
read webpage https://en.wikipedia.org/wiki/Hong_Kong
```

**Expected output:**
A plain-text preview of the page content, trimmed to a readable length, followed by a note that the full page was fetched.

## Implementation Reference

```python
import requests
from bs4 import BeautifulSoup

def read_webpage(url: str) -> str:
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; SkillBot/1.0)'}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    for tag in soup(['script', 'style', 'noscript', 'nav', 'footer']):
        tag.decompose()
    text = soup.get_text(separator='\n')
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    preview = '\n'.join(lines)[:800]
    return f"📄 Preview of {url}:\n\n{preview}\n\n[Fetched {len(lines)} lines of text]"
```

## API Endpoint (if running ai06_server.py)

```
POST /api/read-webpage
Content-Type: application/json

{ "message": "read webpage https://en.wikipedia.org/wiki/Hong_Kong" }
```

Response:
```json
{ "answer": "📄 Preview of https://...\n\n...", "skill": "read-webpage" }
```

## Dependencies

- `requests` — HTTP fetching
- `beautifulsoup4` — HTML parsing and text extraction

## Notes

- Works on any publicly accessible URL (no login required)
- JavaScript-rendered pages may return limited content
- For asking questions about a page's content, use the `ask-webpage` skill instead
