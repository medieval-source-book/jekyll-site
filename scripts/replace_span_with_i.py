#!/usr/bin/env python3
"""
Replace <span ...>...</span> with <i ...>...</i> in all files under references/.
Creates a timestamped backup directory `references_backups/YYYYmmdd_HHMMSS/`.
Preserves attributes on opening tags (e.g. <span class="foo"> -> <i class="foo">)
"""
from pathlib import Path
import re
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
REF_DIR = ROOT / 'references'
BACKUP_ROOT = ROOT / 'references_backups'

span_open_re = re.compile(r'<span(\s+[^>]*)?>', re.IGNORECASE)
span_close_re = re.compile(r'</span>', re.IGNORECASE)

now = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_dir = BACKUP_ROOT / now

files = list(REF_DIR.rglob('*.html'))
if not files:
    print('No reference files found to process.')
    raise SystemExit(0)

backup_dir.mkdir(parents=True, exist_ok=True)
for p in files:
    rel = p.relative_to(ROOT)
    dest = backup_dir / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(p.read_bytes())

count = 0
for p in files:
    s = p.read_text(encoding='utf-8')
    if '<span' not in s.lower() and '</span>' not in s.lower():
        continue
    new = span_open_re.sub(lambda m: '<i' + (m.group(1) or '') + '>', s)
    new = span_close_re.sub('</i>', new)
    if new != s:
        p.write_text(new, encoding='utf-8')
        count += 1

print(f'Backed up {len(files)} files to {backup_dir}')
print(f'Updated {count} files (replaced <span> with <i>).')
