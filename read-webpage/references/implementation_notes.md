# read_webpage.py — What We Did vs. Basic BeautifulSoup

A basic BeautifulSoup developer would typically do:

```python
soup = BeautifulSoup(resp.text, 'html.parser')
print(soup.get_text())
```

Here's what we added on top of that:

1. **Custom User-Agent header** — a bare `requests.get(url)` often gets blocked or returns bot-detection pages. We send a browser-like User-Agent so the server treats us as a real browser.

2. **Noise tag removal** — we explicitly decompose `script`, `style`, `noscript`, `nav`, and `footer` before extracting text. Without this, you get JavaScript code, CSS rules, and navigation menus mixed into the output.

3. **Line-by-line cleaning** — we split on newlines, strip each line, and filter out blank lines. A basic `get_text()` call returns a wall of text with lots of empty lines and leading/trailing whitespace.

4. **Preview cap** — we truncate to 800 characters. Without this, a large page like Wikipedia dumps tens of thousands of characters, which is unusable in a chat context.

5. **Formatted output** — we wrap the result with a `📄 Preview of {url}` header and a `[Fetched N lines]` footer. A basic script just prints raw text with no context:

   ```
   Artificial intelligence
   From Wikipedia, the free encyclopedia
   AI redirects here...
   ```

   Our script returns this instead:

   ```
   📄 Preview of https://en.wikipedia.org/wiki/Artificial_intelligence

   Artificial intelligence
   From Wikipedia, the free encyclopedia
   AI redirects here...

   [Fetched 342 lines of text]
   ```

   Three things added:
   - `📄 Preview of {url}` at the top — confirms which page was actually fetched, useful when the URL redirects or the user sent multiple requests
   - the 800-char preview in the middle — the actual content
   - `[Fetched 342 lines of text]` at the bottom — tells the user the page had 342 lines total, but only the first 800 characters are shown, signalling there's more content available if needed

   It's the difference between a script that dumps data and one that communicates clearly with the user.

6. **`raise_for_status()`** — we explicitly raise an exception on HTTP errors (404, 403, etc.) rather than silently returning empty or error HTML as if it were content.
