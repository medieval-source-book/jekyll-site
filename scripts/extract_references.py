#!/usr/bin/env python3
"""
Extract content between <h2>Further Reading</h2> and the next <h1> for each html file in html/.
Write outputs to references/<originalname>-references.html
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
HTML_DIR = ROOT / 'html'
OUT_DIR = ROOT / 'references'
OUT_DIR.mkdir(exist_ok=True)

hdr_re = re.compile(r'<h2[^>]*>\s*Further Reading\s*</h2>', re.IGNORECASE)
# find from the end of the Further Reading header to the next <h1>
chunk_re = re.compile(r'<h2[^>]*>\s*Further Reading\s*</h2>([\s\S]*?)(?=<h1[^>]*>)', re.IGNORECASE)

count=0
for p in HTML_DIR.rglob('*.html'):
    s = p.read_text(encoding='utf-8')
    m = chunk_re.search(s)
    if m:
        out = m.group(1).strip()
        # wrap in a minimal fragment if needed
        out_path = OUT_DIR / (p.stem + '-references.html')
        out_path.write_text(out, encoding='utf-8')
        count += 1

print(f'Extracted {count} reference sections to {OUT_DIR}')
