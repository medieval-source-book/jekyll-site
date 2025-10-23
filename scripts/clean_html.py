#!/usr/bin/env python3
"""
Clean HTML files in html/:
- remove <head>...</head> sections
- remove <style>...</style> blocks
- remove style="..." and class="..." attributes
- ensure a newline after every closing '>' character
Creates backups under html_backups/ with the same relative paths.
"""
import re
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
HTML_DIR = ROOT / 'html'
BACKUP_DIR = ROOT / 'html_backups'

HEAD_RE = re.compile(r"<head[\s\S]*?</head>", re.IGNORECASE)
STYLE_RE = re.compile(r"<style[\s\S]*?</style>", re.IGNORECASE)
# remove style= or class= with single or double quoted values, and also unquoted (defensive)
ATTR_RE = re.compile(r"\s*(?:style|class)\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s>]+)", re.IGNORECASE)


def clean_html(text: str) -> str:
    # remove head
    text = HEAD_RE.sub('', text)
    # remove style blocks
    text = STYLE_RE.sub('', text)
    # remove style= and class=
    text = ATTR_RE.sub('', text)
    # ensure newline after every closing '>' (but avoid adding too many newlines)
    # replace any '>' followed by optional whitespace then a non-newline with '>' + newline + that char
    text = re.sub(r">\s*(?!\n)(?=[^\n])", ">\n", text)
    # collapse <p> inner content to a single line: remove newlines and collapse whitespace inside tags
    def collapse_p(match):
        opening = match.group(1)
        inner = match.group(2)
        closing = match.group(3) or ''
        # collapse whitespace inside inner while preserving tags
        # we'll collapse any runs of whitespace between > and < or around text
        inner2 = re.sub(r"\s+", " ", inner).strip()
        return f"{opening}{inner2}{closing}"

    # match <p ...> (capture opening tag), inner content, and closing </p>
    text = re.sub(r"(<p[^>]*>)([\s\S]*?)(</p>)", collapse_p, text, flags=re.IGNORECASE)
    # collapse header tags (<h1>..</h1> ... <h6>) so their opening tag, text, and closing tag are on one line
    def collapse_h(match):
        opening = match.group(1)
        inner = match.group(2)
        closing = match.group(3) or ''
        inner2 = re.sub(r"\s+", " ", inner).strip()
        return f"{opening}{inner2}{closing}"

    text = re.sub(r"(<h[1-6][^>]*>)([\s\S]*?)(</h[1-6]>)", collapse_h, text, flags=re.IGNORECASE)
    return text


def main():
    if not HTML_DIR.exists():
        print('html/ directory not found at', HTML_DIR)
        return
    # copy backups
    if BACKUP_DIR.exists():
        print('Backup dir already exists at', BACKUP_DIR)
    else:
        print('Creating backup at', BACKUP_DIR)
        shutil.copytree(HTML_DIR, BACKUP_DIR)

    files = list(HTML_DIR.rglob('*.html'))
    print(f'Found {len(files)} html files')
    for p in files:
        rel = p.relative_to(HTML_DIR)
        print('Processing', rel)
        txt = p.read_text(encoding='utf-8')
        new = clean_html(txt)
        p.write_text(new, encoding='utf-8')

    print('Done')


if __name__ == '__main__':
    main()
