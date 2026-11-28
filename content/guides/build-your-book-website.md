---
title: Build your book website
description: One command turns the book you are writing into a website (cover, download, characters, podcast, explorable graph) that you can publish free on GitHub Pages.
date: 2026-11-28
weight: 6
level: Publishing
---
Your book needs a home online: a link you can share, put in your bio, send to readers and submit to the [gallery](/books/). `/ghost-writer:site` builds it from what your project already has. You get one page, `docs/index.html`, that you can publish for free on GitHub Pages.

The page is built for phones first and loads no fonts, scripts or trackers from other sites. All the text is in the HTML; JavaScript only draws the graph.

## What the site contains

Sections appear only when your project has what they need:

| Section | Appears when | Comes from |
|---|---|---|
| Opening: cover, title, tagline | always | your texts + `cover.jpg` / `cover.png` |
| The book, with a download button | always | your texts + a PDF or EPUB |
| Characters, people or key ideas | you choose some | your texts, linked to the graph |
| Podcast: episodes and RSS feed | MP3s exist | `/ghost-writer:podcast` |
| Explorable graph: search, chapters, open points | the graph exists | `/ghost-writer:graph` |

The title of the featured section follows your book's preset: **characters** for fiction, fables and children's books, **people** for biographies, **key ideas** for essays and manuals.

You can publish early and add sections later: every rebuild picks up what's new.

## Before you start

- **Python 3.9+ and PyYAML**: `pip install pyyaml`.
- **A Ghost Writer project** with some complete chapters.
- **A GitHub account**, to publish.
- **A cover (recommended).** A square image, at least 720×720, saved as `cover.jpg` or `cover.png` in the book's folder. The page works without one, but the opening and link previews (messaging apps, social networks, email) look much better with it. Install Pillow (`pip install pillow`) and it's resized to 720 px for you.

To fill the optional sections, run these first:

- **Download button**: `/ghost-writer:manuscript-final`, then `/ghost-writer:export-pdf` or `/ghost-writer:export-epub`.
- **Graph**: `/ghost-writer:graph`. Complete chapters sync on their own.
- **Podcast**: `/ghost-writer:podcast`. It needs `ffmpeg` and `pip install piper-tts numpy`. See [Build your podcast](/guides/build-your-podcast/).

## Run the command

Open Claude Code in the book's folder and type:

```
/ghost-writer:site
```

First it checks the project and tells you in one line what the site will have and what's missing:

> The site will have: opening, the book, characters, podcast — 12 episodes, graph — 84 cards. Missing: download. Shall we write the texts?

Then it drafts the page texts **one block at a time**, in the book's language and in your voice, and waits for your yes on each:

1. **Opening**: a kicker (genre and format, 3–7 words), the tagline (your hook), subtitle and author.
2. **The book**: two or three short paragraphs. Back-cover copy, not a summary.
3. **Download** (optional): which file, the button label, a short note (format, chapters included).
4. **Featured** (optional): 3–5 main characters or key ideas, each with a short role and two sentences, no spoilers. If the graph exists, each one links to its card.
5. **Podcast** (if you have episodes): a title and a line of text.
6. **Graph** (if it exists): show the whole book, or only up to a chapter, plus the cards it starts from.

Nothing goes on the page beyond what you want public. Your texts are saved in `site.yaml`, in the book's folder.

## Check and build

```bash
python3 build_site.py --check   # validates everything, writes nothing
python3 build_site.py           # writes docs/
```

If a browser is available, Claude shows you a phone and a desktop screenshot. Otherwise open `docs/index.html` in your browser.

## Publish on GitHub Pages

1. Commit the `docs/` folder and push your project to a GitHub repository.
2. On GitHub, open **Settings → Pages → Build and deployment → Deploy from a branch**, choose branch `main` and folder `/docs`, then **Save**.
3. After about a minute your site is live at `https://<user>.github.io/<repository>/`.

Claude never pushes or changes repository settings unless you ask. To use your own domain, set it in **Settings → Pages → Custom domain** and follow GitHub's DNS instructions.

### With a podcast

1. In `book.config.json`, set `podcast.base_url` to `https://<user>.github.io/<repository>/episodes`.
2. Run `python3 export_podcast.py feed`, then `python3 build_site.py`, then commit and push.
3. Submit `https://<user>.github.io/<repository>/feed.xml` to Spotify for Creators, Apple Podcasts and other directories.

GitHub refuses files over 100 MB and Pages sites over 1 GB. At 96 kbps an episode takes about 0.7 MB per minute.

## Publishing a book in installments

Writing in public? Set `graph.up_to_chapter` in `site.yaml` to the last chapter you've released. The graph then shows only cards, facts and events up to that chapter. When the next one goes out, raise the number and rebuild.

## Keeping it updated

The site is generated: never edit `docs/` by hand.

- **A chapter becomes complete**: the graph syncs and the site is rebuilt automatically.
- **New podcast episodes**: the podcast command rebuilds the site.
- **A text on the page**: run `/ghost-writer:site` again and change just that block.

After every rebuild, **commit and push `docs/`** to put it live.

## If something goes wrong

- **`ModuleNotFoundError: yaml`**: run `pip install pyyaml`.
- **The build stops on graph errors**: run `python3 graph.py build` and fix what it reports.
- **A featured entry isn't found in the graph**: `python3 graph.py find <name>` gives you the right id.
- **No download button**: check the file path in `site.yaml` (`book.download.file`, relative to the book's folder).
- **Episodes don't play in podcast apps**: `podcast.base_url` is empty or wrong. Fix it, regenerate the feed and rebuild.
- **404 on GitHub**: Pages must point to `main` / `/docs`. Wait a minute after saving.

## Next: add it to the gallery

Once the site is live, use its address as the book's link and [add your book to the gallery](/guides/add-your-book-to-the-gallery/):

```
/ghost-writer:gallery
```
