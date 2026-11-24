---
title: Getting started with Ghost Writer
description: Install the plugin, set up your book in one conversation and write your first chapter with the ask–write–demolish–integrate cycle.
date: 2026-11-24
weight: 1
level: Beginner
---
Ghost Writer is a Claude Code plugin for writing books and long-form projects with Claude — without letting Claude write your book for you. Concepts come from you; Claude asks, formalizes, drafts in your voice and then attacks the draft before your readers do.

This guide takes you from installation to your first finished chapter.

## 1. Install the plugin

The quickest way is the [Ghost Writer page in the Claude plugin directory](https://claude.ai/customize/plugins/id/4b831b3b-c718-4a20-b786-598ed6566696%40anthropic-plugin-directory): open it and install.

Alternatively, in Claude Code, add the repository as a marketplace and install the plugin:

```
/plugin marketplace add simonediroma/claude-ghost-writer
/plugin install ghost-writer@simonediroma-ghost-writer
```

Then open (or create) the folder where your book will live and check that everything is in place:

```
/ghost-writer:check
```

It verifies the installation and the project setup in about a minute.

## 2. Set up the book

If you are starting from scratch, run the wizard:

```
/ghost-writer:wizard
```

It is a conversation, one question at a time. If you prefer the full onboarding, `/ghost-writer:start` runs the three setup steps in sequence:

- **`setup-author`** — who you are, your authority on the subject, your emotional stake.
- **`setup-book`** — premise, reader and structure. Here you pick a **genre preset**: `essay`, `fiction`, `manual`, `biography`, `fable` or `childrens-book`. The preset adapts vocabulary, questions and the way drafts are criticized.
- **`setup-voice`** — your tone of voice, from an interview and samples of your writing.

At the end you have a first outline and a set of project files (`book.config.json`, `outline.md`, `book-memory.md`, `style-rules.md`…). You don't need to edit them by hand.

## 3. Write your first chapter

One command runs the whole cycle:

```
/ghost-writer:chapter
```

Behind it are four steps you can also run one by one:

1. **Ask** — `/ghost-writer:ask-before-writing` opens a structured dialogue about the chapter. Nothing is written until the concept is clear. Feeling blocked? `/ghost-writer:freeflow` lets you dump everything you have and organizes it for you.
2. **Write** — `/ghost-writer:write` generates the section in your voice, following your style rules.
3. **Demolish** — `/ghost-writer:demolish` attacks the draft: unsupported claims, circular arguments, unearned endings — one objection at a time. Short on time? Add `--light` for the three most critical issues only.
4. **Integrate** — `/ghost-writer:integrate` brings your answers back into the text, one change at a time. Nothing changes without your confirmation.

## 4. Come back tomorrow

Every time you open the project, start with:

```
/ghost-writer:session-start
```

It reads the project digest and tells you in seconds where you left off, what is pending and what to do today.

## What's next

- Every 3–4 chapters, run `/ghost-writer:consistency-check` to catch term drift, contradicted claims and broken promises.
- Before re-reading, `/ghost-writer:review` puts the chapter in front of five reader personas — from your target reader to a hostile one.
- When all chapters are done, `/ghost-writer:finish` writes the introduction (always last), the conclusion and assembles the manuscript.

Not sure which command to use? Run `/ghost-writer:help`.
