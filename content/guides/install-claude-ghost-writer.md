---
title: How to install Claude Ghost Writer
description: Install the plugin from the Claude plugin directory or with two commands in Claude Code, check that it works and add the optional extras.
date: 2026-11-24
weight: 1
level: Essentials · 1 of 3
---
Ghost Writer is a plugin: a set of commands that teach Claude a writing method — ask before writing, draft in your voice, demolish the draft, integrate the answers. Installing it takes a couple of minutes.

## What you need

- A Claude account with access to **Claude Code** (terminal, desktop app or IDE extension).
- A folder on your computer for the book. Ghost Writer keeps everything — chapters, memory, outline — as plain files in that folder.

## Option A — From the Claude plugin directory

The quickest way: open the [Ghost Writer page in the Claude plugin directory](https://claude.ai/customize/plugins/id/4b831b3b-c718-4a20-b786-598ed6566696%40anthropic-plugin-directory) and install it from there.

## Option B — With two commands in Claude Code

Open Claude Code and type:

```
/plugin marketplace add simonediroma/claude-ghost-writer
/plugin install ghost-writer@simonediroma-ghost-writer
```

The first command adds the plugin's repository as a marketplace; the second installs the plugin from it.

## Check that it works

Open Claude Code in your book folder and type `/ghost-writer:` — the list of commands should appear. Then run:

```
/ghost-writer:help
```

It shows every command grouped by phase of the book. If nothing appears, restart Claude Code and try again.

Once your book is set up (see the [next guide](../how-to-start-your-book/)), `/ghost-writer:check` verifies the project in about a minute. It is read-only: it never changes your files.

## Optional extras

The writing method itself needs nothing else. A few advanced features use small Python tools:

| Feature | Command | Requires |
|---|---|---|
| Book graph (map of characters, places, ideas) | `/ghost-writer:graph` | `pip install pyyaml` |
| Re-reading on paper or tablet | `/ghost-writer:corrections` | `pip install reportlab pymupdf` |
| Book to podcast | `/ghost-writer:podcast` | `pip install piper-tts numpy` and `ffmpeg` |

You can install them later, when you need them.
