#!/usr/bin/env python3
"""
Zero-dependency web page text extractor.
Fetches a URL using urllib with a realistic User-Agent, strips boilerplate
(<script>, <style>, <nav>, <footer>, <header>), and prints clean text to stdout.
Requires only Python standard library (no bs4, no requests, no trafilatura).
"""

import sys
import urllib.request
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    IGNORE_TAGS = {"script", "style", "nav", "footer", "header", "noscript", "svg"}

    def __init__(self):
        super().__init__()
        self.texts = []
        self.ignore_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.IGNORE_TAGS:
            self.ignore_depth += 1

    def handle_endtag(self, tag):
        if tag.lower() in self.IGNORE_TAGS:
            self.ignore_depth = max(0, self.ignore_depth - 1)

    def handle_data(self, data):
        if self.ignore_depth == 0:
            text = data.strip()
            if text:
                self.texts.append(text)

def extract_text_from_url(url: str, timeout: int = 15) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        html = resp.read().decode("utf-8", errors="replace")

    parser = TextExtractor()
    parser.feed(html)
    return "\n".join(parser.texts)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: extract_url_text.py <URL>")
        sys.exit(1)

    target_url = sys.argv[1]
    try:
        content = extract_text_from_url(target_url)
        print(content)
    except Exception as e:
        print(f"Error extracting {target_url}: {e}", file=sys.stderr)
        sys.exit(1)
