# API Reference — read-webpage

## Python Implementation

```python
import requests
from bs4 import BeautifulSoup

def read_webpage(url: str, max_chars: int = 800) -> str:
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; SkillBot/1.0)'}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    for tag in soup(['script', 'style', 'noscript', 'nav', 'footer']):
        tag.decompose()
    text = soup.get_text(separator='\n')
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    preview = '\n'.join(lines)[:max_chars]
    return f"📄 Preview of {url}\n\n{preview}\n\n[Fetched {len(lines)} lines of text]"
```

## Flask API Endpoint

```
POST /api/read-webpage
Content-Type: application/json

{ "message": "use skill read-webpage https://en.wikipedia.org/wiki/Artificial_intelligence" }
```

Response:
```json
{ "answer": "📄 Preview of https://...\n\n...", "skill": "read-webpage" }
```

## Dependencies

- `requests` — HTTP fetching
- `beautifulsoup4` — HTML parsing

Install:
```bash
pip install requests beautifulsoup4
```

## Saved Output File

The full page text is saved to a `.txt` file in the current directory:
- Filename format: `{page_name}_{YYYYMMDD_HHMMSS}.txt`
- Example: `Artificial_intelligence_20260330_143022.txt`
- File contains: URL, fetch timestamp, line count, and full plain text



- JavaScript-rendered pages may return limited content (static HTML only)
- Requires public URL — no login-protected pages
- Preview capped at 800 characters by default (adjustable via `max_chars`)
