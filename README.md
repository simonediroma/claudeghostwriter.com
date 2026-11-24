# claudeghostwriter.com

Website of [Ghost Writer](https://github.com/simonediroma/claude-ghost-writer), the Claude Code plugin for writing books. Built with [Hugo](https://gohugo.io) (extended), deployed to GitHub Pages on every push to `main`.

## Add a book to the gallery

Books are added by pull request — see [CONTRIBUTING.md](CONTRIBUTING.md). Authors usually submit the **Add my book** issue form; adding the `approved` label runs `.github/workflows/book-from-issue.yml`, which creates the book folder (downloading the cover) and opens the pull request. Every PR is checked by `.github/workflows/check-pr.yml` (`scripts/validate_books.py` + Hugo build); merging to `main` deploys.

### Format

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

## Write a guide

```bash
hugo new guides/my-guide.md
```

Fill in `title`, `description`, `weight` (order) and an optional `level` label, write the guide in Markdown and set `draft: false` (or remove it). The newest three guides appear on the home page; the section is hidden there until the first guide exists.

## Install button

Set `installUrl` in `hugo.toml → [params]` to the plugin page on claude.ai: the main buttons point there. Empty = they point to the install section with the `/plugin` commands.

## Edit the home page

Texts that change often live in `data/`: `features.yaml`, `presets.yaml`, `method.yaml`, `principles.yaml`. Install commands and links are in `hugo.toml → [params]`. Layout: `layouts/index.html`; style: `assets/css/main.css`.

## Run locally

```bash
hugo server
```

## Repository setup (once)

- **Settings → Actions → General → Workflow permissions**: enable *Allow GitHub Actions to create and approve pull requests*.
- Labels `book-submission` and `approved` are created by `.github/workflows/labels.yml` on the first push (or run it manually).

## Domain setup (once)

1. **Settings → Pages → Source: GitHub Actions**. Custom domain `claudeghostwriter.com`, then **Enforce HTTPS**.
2. DNS:
   - `A` records for `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` for `www` → `simonediroma.github.io`
