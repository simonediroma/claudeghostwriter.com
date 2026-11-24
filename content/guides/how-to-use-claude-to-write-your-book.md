---
title: How to use Claude properly to write your book
description: One session, one chapter. How the context window works, why long conversations hurt your book and the routine that keeps Claude sharp from the first chapter to the last.
date: 2026-11-24
weight: 3
level: Essentials · 3 of 3
---
The most common mistake when writing a book with Claude isn't a bad prompt. It's a conversation that goes on too long.

## The context window, in one paragraph

Everything Claude can "see" while working with you — your messages, its answers, the files it has read — lives in its **context window**: a working memory that is large, but limited. As a conversation grows, it fills up. When it gets close to full, Claude Code compresses older parts of the conversation into a summary. Details get lost along the way: a term you defined two hours ago, a decision about a character, the exact rhythm of your voice.

For a book, those details are the whole game.

## The rule: one session, one chapter

**Open a fresh session, work on one chapter, close the session.**

A chapter's full cycle — dialogue, draft, demolition, integration — already fills a good part of the context: the chapter text is read and rewritten several times, objections and answers pile up. Starting the next chapter in the same conversation means writing it with a memory that is already crowded with the previous one.

## You don't lose anything by closing

Ghost Writer doesn't rely on the conversation to remember your book. Everything that matters is written to files in the project folder:

| What | Where |
|---|---|
| Terms, promises, claims, chapter log | `book-memory.md` |
| Where you left off and what's pending | `project-state.md` |
| The step a chapter has reached | `sessions/` |
| Objections already raised and how they were handled | `demolition-history.md` |
| Your voice and the book's profile | `book.config.json` |

That's why every session can start from zero without losing anything: `/ghost-writer:session-start` reads a compact digest of the project instead of the whole book.

## The routine

1. **Fresh session.** Open a new conversation, or type `/clear` in Claude Code to empty the current one.
2. **Briefing.** `/ghost-writer:session-start` — where you left off, what's pending, what to do today.
3. **One chapter.** `/ghost-writer:chapter` — the full cycle on one chapter, with resume.
4. **Close.** When the chapter is integrated, stop. The next chapter gets the next session.

## When a chapter takes more than one session

That's normal for long or difficult chapters. `/ghost-writer:chapter` saves the step it has reached after each phase — after the draft, for example, it offers to stop before the demolition. Close, open a fresh session and run `/ghost-writer:chapter` again: it resumes exactly where you stopped.

The best places to stop are **between phases**: after the draft, after the demolition, after the integration. Avoid stopping in the middle of a demolition: the open objections are part of the conversation.

## Keep an eye on the context

- **`/context`** in Claude Code shows how full the context window is.
- **`/compact`** summarizes the conversation to free up space. It's a fallback: a summary keeps the gist, not your exact words. Between phases, a fresh session and a resume are better.
- **Warning signs** that it's time to stop: Claude asks again something you already answered, forgets a term defined earlier, or the voice of the draft starts drifting toward a generic tone.

## Heavy tasks get their own session

Some commands read a lot of text. Run each one in a fresh session, never at the end of a writing session:

- `/ghost-writer:review` — five reader personas, one after another, on the same chapter.
- `/ghost-writer:consistency-check` — every 3–4 chapters, across the book.
- `/ghost-writer:revise --all` — the full editorial pass before the manuscript.
- `/ghost-writer:finish` — introduction, conclusion and final manuscript.

## Don't feed it the whole book

Resist the temptation to paste all your chapters into the chat "for context". The commands already read what they need, and in the most economical form: chapter summaries, the memory files, only the relevant cards of the book graph. Pasting everything just fills the context — and makes the following work worse.

## Long books: long-form mode

When you reach about ten complete chapters, the plugin suggests `/ghost-writer:longform-upgrade`. It splits the book into parts and the memory into one file per part, and adds a summary to each chapter. From then on Claude reads the global index plus the current part instead of everything. Your chapters are not changed.

## Checklist

- [ ] One fresh session per chapter
- [ ] Always start with `/ghost-writer:session-start`
- [ ] Stop between phases, not in the middle of a demolition
- [ ] Review, consistency check and final revision in their own sessions
- [ ] Never paste the whole manuscript into the chat
- [ ] Long-form mode at about ten chapters
