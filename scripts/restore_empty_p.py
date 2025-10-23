#!/usr/bin/env python3
"""
Restore files from html_backups/ to html/ when the backup contains empty paragraph tags (<p><br/>)
This will only overwrite files that in the backup contain at least one empty paragraph tag.
"""
from pathlib import Path
import shutil
import re

ROOT = Path(__file__).resolve().parent.parent
HTML_DIR = ROOT / 'html'
BACKUP_DIR = ROOT / 'html_backups'

if not BACKUP_DIR.exists():
    print('No backups found at', BACKUP_DIR)
    raise SystemExit(1)

pattern = re.compile(r"<p[^>]*>\s*(?:<br\s*/?>)\s*</p>", re.IGNORECASE)

restored = []
for p in BACKUP_DIR.rglob('*.html'):
    rel = p.relative_to(BACKUP_DIR)
    s = p.read_text(encoding='utf-8')
    if pattern.search(s):
        dest = HTML_DIR / rel
        if dest.exists():
            shutil.copy2(p, dest)
            restored.append(str(rel))

print(f'Restored {len(restored)} files from backups (files that contained empty <p> tags).')
for r in restored[:50]:
    print(r)
