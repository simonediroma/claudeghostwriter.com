---
title: How to add your book to the gallery
description: Finished a book with Ghost Writer? One command drafts its gallery entry with you and submits it to claudeghostwriter.com.
date: 2026-11-24
weight: 5
level: Publishing
---
The [gallery](/books/) collects books and long-form projects written with Ghost Writer. Adding yours takes one command and a few minutes, and every entry gets its own page with cover, description and links.

## Before you start

- **Ghost Writer 1.8.0 or later.** The command is `/ghost-writer:gallery`.
- **At least one public link to the book.** The gallery points readers somewhere: a store page, a website, a repository, a podcast. If the book isn't online yet, `/ghost-writer:site` builds a free website for it on GitHub Pages: see [Build your book website](/guides/build-your-book-website/).
- **A cover (optional).** JPG, PNG or WebP, up to 2 MB. 2:3 fills the card; a square cover (like a podcast cover) works too and is shown whole, never cropped. Without one, the site draws a typographic cover from the title.

## Run the command

Open Claude Code in the book's folder and type:

```
/ghost-writer:gallery
```

It reads what the project already has (title, genre, language, your book website and cover) and tells you what's missing. Then it drafts the entry **one field at a time**, waiting for your yes on each:

1. **Title, author, year, language.** Author is the name you want public.
2. **Genre**, from the book's preset.
3. **Short description**: one or two sentences, in your voice, up to 300 characters, no spoilers.
4. **Links**: only full `https://` addresses. Tracking parameters (`utm_*`, `ref`, `fbclid`…) are stripped, and affiliate links are not allowed.
5. **About the book** (optional): a few lines for the book page, including how you used Ghost Writer.
6. **Cover** (optional): if it's over 2 MB, the command offers to shrink it and shows you the result first. Any ratio is fine.

Then it asks for three confirmations, all required:

- the book was written, fully or in part, with Ghost Writer;
- you are the author, or have the author's permission to list it;
- you have the rights to publish the cover.

## Check and send

The entry is saved in your project, in `gallery/<your-book>/`, and checked against the site's rules: required fields, genres, description length, links and cover size. You see the final text before anything leaves your computer.

Nothing is sent until you say so. Then:

- **With the GitHub CLI** (`gh`) installed and logged in, the command opens a pull request on the [website repository]({{< param "siteRepo" >}}) directly.
- **Without it**, you get a link to the **Add my book** form, already filled in. Check the fields (title and genre may need to be set by hand), drag the cover into the form and submit.

## What happens next

Every submission is checked automatically and reviewed by the maintainer. Once it's merged, your book appears in the gallery within a few minutes. The command saves the link to your pull request or request in the project. Run `/ghost-writer:gallery` again to update the entry later, for example with a new store link.

## Without the plugin

You can also add a book by hand: open the [Add my book form]({{< param "siteRepo" >}}/issues/new?template=add-book.yml), or follow the [contributing guide]({{< param "siteRepo" >}}/blob/main/CONTRIBUTING.md) to open a pull request yourself.
