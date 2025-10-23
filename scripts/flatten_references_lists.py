#!/usr/bin/env python3
"""
Flatten lists in files under references/: remove <ul> and <li> tags.
- If <li> contains one or more <p>...</p>, keep those <p> elements and drop the <li> wrapper.
- If <li> contains plain text (no <p>), replace it with <p>text</p>.
Writes files in-place and prints a summary.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF_DIR = ROOT / 'references'

li_re = re.compile(r'<li[^>]*>([\s\S]*?)</li>', re.IGNORECASE)
ul_open_re = re.compile(r'<ul[^>]*>', re.IGNORECASE)
ul_close_re = re.compile(r'</ul>', re.IGNORECASE)

files = list(REF_DIR.rglob('*.html'))
count = 0
updated_files = []
for p in files:
    s = p.read_text(encoding='utf-8')
    if '<ul' not in s.lower() and '<li' not in s.lower():
        continue
    def repl_li(m):
        inner = m.group(1).strip()
        # if contains any <p> tag, keep inner as-is
        if re.search(r'<p[^>]*>', inner, re.IGNORECASE):
            return inner
        # otherwise collapse whitespace and wrap in <p>
        text = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', inner)).strip()
        return f'<p>{text}</p>' if text else ''
    new = ul_open_re.sub('', s)
    new = ul_close_re.sub('', new)
    new = li_re.sub(repl_li, new)
    if new != s:
        p.write_text(new, encoding='utf-8')
        count += 1
        updated_files.append(str(p.relative_to(ROOT)))

print(f'Processed {len(files)} files, updated {count} files.')
if updated_files:
    print('Updated files:')
    for fn in updated_files[:200]:
        print(fn)
