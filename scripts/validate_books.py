#!/usr/bin/env python3
"""Validate every book in content/books/. Exit 1 on errors. Requires PyYAML."""
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import yaml

GENRES = {"essay", "fiction", "manual", "biography", "fable", "childrens-book"}
REQUIRED = ["title", "author", "genres", "description", "links"]
COVER_EXT = {".jpg", ".jpeg", ".png", ".webp"}
MAX_COVER = 2 * 1024 * 1024
MAX_DESC = 300
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ALLOWED_FILES = {"index.md"} | {f"cover{e}" for e in COVER_EXT}

root = Path(__file__).resolve().parent.parent / "content" / "books"
errors = []


def err(book, msg):
    errors.append(f"{book}: {msg}")


for d in sorted(p for p in root.iterdir() if p.is_dir()):
    name = d.name
    if not SLUG.match(name):
        err(name, "folder name must be lowercase-with-dashes")
    for f in d.iterdir():
        if f.name not in ALLOWED_FILES:
            err(name, f"unexpected file '{f.name}' (allowed: index.md, cover.jpg/.png/.webp)")
        elif f.name.startswith("cover") and f.stat().st_size > MAX_COVER:
            err(name, f"{f.name} is larger than 2 MB")
    idx = d / "index.md"
    if not idx.exists():
        err(name, "missing index.md")
        continue
    text = idx.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        err(name, "index.md must start with a --- YAML front matter block")
        continue
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        err(name, f"invalid YAML: {e}")
        continue
    for k in REQUIRED:
        if not fm.get(k):
            err(name, f"'{k}' is required")
    genres = fm.get("genres") or []
    if not isinstance(genres, list):
        err(name, "'genres' must be a list, e.g. [fiction]")
    else:
        for g in genres:
            if g not in GENRES:
                err(name, f"unknown genre '{g}' (use: {', '.join(sorted(GENRES))})")
    if len(str(fm.get("description", ""))) > MAX_DESC:
        err(name, f"'description' is longer than {MAX_DESC} characters")
    for link in fm.get("links") or []:
        if not isinstance(link, dict) or not link.get("label") or not link.get("url"):
            err(name, "each link needs 'label' and 'url'")
            continue
        u = urlparse(str(link["url"]))
        if u.scheme != "https" or not u.netloc:
            err(name, f"link must be a full https:// URL: {link['url']}")

if errors:
    print("Book validation failed:\n" + "\n".join(f"  - {e}" for e in errors))
    sys.exit(1)
print(f"OK: {sum(1 for p in root.iterdir() if p.is_dir())} books valid")
