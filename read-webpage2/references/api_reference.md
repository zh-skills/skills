# API Reference — read-webpage2

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

## Flask API Endpoint (ai06_server.py)

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
- `beautifulsoup4` — HTML parsing

Install:
```bash
pip install requests beautifulsoup4
```

## Limitations

- JavaScript-rendered pages may return limited content (static HTML only)
- Requires public URL — no login-protected pages
- Preview capped at 800 characters by default (adjustable via `max_chars`)
