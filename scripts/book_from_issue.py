#!/usr/bin/env python3
"""Turn an 'Add my book' issue form into content/books/<slug>/.

Reads the issue body from the ISSUE_BODY environment variable. Prints the
created folder name. Exit 1 with a readable message on bad input.
Requires PyYAML. Standard library otherwise.
"""
import os
import re
import sys
import unicodedata
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ROOT / "content" / "books"
MAX_COVER = 2 * 1024 * 1024
COVER_HOSTS = {"github.com", "user-images.githubusercontent.com",
               "private-user-images.githubusercontent.com"}
NO_RESPONSE = "_No response_"


def fail(msg):
    print(msg)
    sys.exit(1)


def parse_form(body):
    """Issue forms render as '### Label\\n\\nvalue' blocks."""
    fields, current = {}, None
    for line in body.replace("\r\n", "\n").split("\n"):
        m = re.match(r"^### (.+?)\s*$", line)
        if m:
            current = m.group(1).strip()
            fields[current] = []
        elif current:
            fields[current].append(line)
    out = {}
    for k, v in fields.items():
        text = "\n".join(v).strip()
        out[k] = "" if text == NO_RESPONSE else text
    return out


def slugify(text):
    text = re.sub(r"['’]", "-", text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text[:60].strip("-") or "book"


def parse_links(text):
    links = []
    for line in text.splitlines():
        line = line.strip().lstrip("-* ").strip()
        if not line:
            continue
        if "|" in line:
            label, url = (p.strip() for p in line.split("|", 1))
        else:
            label, url = "Link", line
        url = url.strip("<>")
        links.append({"label": label, "url": url})
    return links


def find_cover_url(text):
    for url in re.findall(r"https://[^\s)\"'>]+", text or ""):
        host = urlparse(url).netloc
        if host in COVER_HOSTS and ("/user-attachments/" in url or "githubusercontent" in host):
            return url
    return None


def sniff_ext(data):
    if data[:3] == b"\xff\xd8\xff":
        return ".jpg"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    return None


def download_cover(url):
    req = urllib.request.Request(url, headers={"User-Agent": "claudeghostwriter-site-bot"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read(MAX_COVER + 1)
    if len(data) > MAX_COVER:
        fail("The cover image is larger than 2 MB.")
    ext = sniff_ext(data)
    if not ext:
        fail("The cover must be a JPG, PNG or WebP image.")
    return data, ext


def main():
    form = parse_form(os.environ.get("ISSUE_BODY", ""))
    title = form.get("Title", "")
    if not title:
        fail("The issue does not look like an 'Add my book' form (no Title field).")

    genres = [g.strip() for g in form.get("Genre", "").split(",") if g.strip()]
    fm = {
        "title": title,
        "author": form.get("Author", ""),
        "genres": genres,
    }
    if form.get("Language"):
        fm["language"] = form["Language"].lower()
    if form.get("Year", "").isdigit():
        fm["year"] = int(form["Year"])
    fm["date"] = os.environ.get("ISSUE_DATE", "")[:10] or None
    fm["description"] = " ".join(form.get("Short description", "").split())
    fm["links"] = parse_links(form.get("Links", ""))
    if os.environ.get("ISSUE_URL"):
        fm["submission"] = os.environ["ISSUE_URL"]
    fm = {k: v for k, v in fm.items() if v not in (None, "")}

    slug = slugify(title)
    folder, n = BOOKS / slug, 2
    while folder.exists():
        folder, n = BOOKS / f"{slug}-{n}", n + 1
    folder.mkdir(parents=True)

    cover_url = find_cover_url(form.get("Cover image", ""))
    if form.get("Cover image") and not cover_url:
        fail("Could not find an uploaded image in the Cover image field. Drag and drop the file into the field.")
    if cover_url:
        data, ext = download_cover(cover_url)
        (folder / f"cover{ext}").write_bytes(data)

    about = form.get("About the book", "")
    front = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000)
    (folder / "index.md").write_text(f"---\n{front}---\n{about}\n", encoding="utf-8")
    print(folder.name)


if __name__ == "__main__":
    main()
