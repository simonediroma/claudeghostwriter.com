---
title: How to start your book
description: Turn an idea — even a vague one — into a book project with a genre, a reader, a voice and a first outline. Then pick the chapter to write first.
date: 2026-11-24
weight: 2
level: Essentials · 2 of 3
aliases: [/guides/getting-started/]
---
Before writing a single line, Ghost Writer needs to know three things: **who you are**, **what the book is** and **how it sounds**. You don't fill in forms: you have a conversation, one question at a time.

## 1. One folder per book

Create an empty folder for the book and open Claude Code in it. Every book gets its own folder: the plugin stores the whole project there as plain text files, so you can back it up, version it with git or move it anywhere.

## 2. Choose how to start

### If you only have an idea: the wizard

```
/ghost-writer:wizard
```

Tell it what's in your head — a few sentences, a ramble, a feeling. No technical choices: the wizard reflects back what it heard, asks the one question it most needs, proposes two or three possible shapes for the book (with real books as examples) and builds the project from your answer. If the idea isn't formed yet, it sends you to `/ghost-writer:freeflow` to find the book by talking it through.

### If you know what you want: the full onboarding

```
/ghost-writer:start
```

Three short sessions, which you can interrupt and resume:

1. **Who you are** (`setup-author`) — your experience, your authority on the subject, why this book matters to you.
2. **What the book is** (`setup-book`) — the genre, the premise, the one reader it's for, the structure.
3. **How it sounds** (`setup-voice`) — your voice, from an interview and samples of your writing.

Started with the wizard? Run `/ghost-writer:setup-voice` later with a few pages you've written: it refines the voice profile the wizard extracted from your words.

## 3. Pick the genre

The genre — the plugin calls it a *preset* — changes the questions you're asked, the structure of the chapters and how drafts are attacked.

| Genre | At its center | Drafts are attacked on |
|---|---|---|
| Essay | a thesis | falsifiability, circularity, scope |
| Fiction | a dramatic question | motivation, consequence, earned change |
| Manual / how-to | a transformation | evidence, context, prerequisites |
| Biography | an interpretation | evidence, selection bias, alternative readings |
| Fable | the moral | earned ending, displacement, narrative necessity |
| Children's book | the heart | age, child logic, pacing, read-aloud quality |

## 4. Prepare good answers

The quality of the book depends on the quality of these answers. Three questions are worth thinking about before you start:

- **The premise.** Can you finish this sentence? *"This book exists because most people believe X, but the truth is Y."*
- **The reader.** Not a demographic — one specific person, what they're doing now and what problem the book solves for them.
- **Your voice.** Two or three pages you wrote and like: emails, posts, an old draft. Real text beats any description of your style.

Remember the first principle of the method: **Claude formalizes, it doesn't invent.** Ideas, stories and opinions come from you.

## 5. What you get

At the end of the setup the folder contains the project files: `book.config.json` (book, genre, voice), `outline.md` (a first chapter list in your words), `book-memory.md` (terms, promises, claims) and the folders for chapters and sessions. You never need to edit them by hand — and you can change titles, order and number of chapters as you go.

## 6. Write the first chapter

Start with the chapter you **most want to write**, not necessarily chapter one. The introduction, in any case, is written last.

```
/ghost-writer:chapter
```

How to organize the writing sessions so Claude stays sharp from the first chapter to the last is the subject of the next guide.
