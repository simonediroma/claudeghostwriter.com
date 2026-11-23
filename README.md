# claudeghostwriter.com

Website of [Ghost Writer](https://github.com/simonediroma/claude-ghost-writer), the Claude Code plugin for writing books. Built with [Hugo](https://gohugo.io) (extended), deployed to GitHub Pages on every push to `main`.

## Add a book to the gallery

Create a folder in `content/books/` with an `index.md` and, optionally, a cover image named `cover.jpg` (or `.png`/`.webp`, ideally 2:3):

```
content/books/my-book/
  index.md
  cover.jpg
```

```markdown
---
title: My Book
author: Author Name
genres: [fiction]        # essay, fiction, manual, biography, fable, childrens-book
language: it
year: 2026
date: 2026-11-23         # newest first in the gallery
description: One or two sentences shown on the card and in search results.
links:
  - label: Buy on Amazon
    url: https://...
  - label: Read online
    url: https://...
---
Longer description shown on the book page (Markdown).
```

Without a cover, a typographic cover is generated from the title.

## Edit the home page

Texts that change often live in `data/`: `features.yaml`, `presets.yaml`, `method.yaml`, `principles.yaml`. Install commands and links are in `hugo.toml → [params]`. Layout: `layouts/index.html`; style: `assets/css/main.css`.

## Run locally

```bash
hugo server
```

## Domain setup (once)

1. **Settings → Pages → Source: GitHub Actions**. Custom domain `claudeghostwriter.com`, then **Enforce HTTPS**.
2. DNS:
   - `A` records for `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` for `www` → `simonediroma.github.io`
