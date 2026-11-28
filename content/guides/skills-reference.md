---
title: "Skills reference: every Ghost Writer command explained"
description: One entry per skill — what it does, which project files it reads and writes, when to use it, and practical examples.
date: 2026-11-28
weight: 7
level: Reference
---
Ghost Writer has 38 skills. This page lists every one of them with **what it does**, **which files it touches**, **when to use it** and a few **examples**.

How to read the entries:

- **Reads** lists the files the skill only looks at. **Writes** lists the files it creates or changes.
- Almost every skill reads `book.config.json → language` to answer in the book's language. It isn't repeated each time.
- **Graph sync**: skills marked *(syncs the graph)* run the Sync procedure of `/ghost-writer:graph` at the end, when a chapter becomes `status: complete` or changes `version`. That updates `graph/` and, if `site.yaml` exists, rebuilds `docs/index.html`.

If you are just starting, read [How to install Claude Ghost Writer](../install-claude-ghost-writer/) and [How to start your book](../how-to-start-your-book/) first.

## Quick map: which skill writes which file

| File | Written by |
|---|---|
| `book.config.json` | wizard, setup-author, setup-book, setup-voice, retune, longform-upgrade, podcast, gallery, site (`podcast.base_url`) |
| `outline.md` | wizard, setup-book, write, longform-upgrade |
| `chapters/*.md` | write, freeflow, integrate, retune, revise, proofread (only after confirmation), corrections, write-opening, write-closing, demolish and demolish-persona (Demolition Log) |
| `book-memory.md` | write, integrate, revise, corrections, consistency-check, character-interview, session-start (Session Log), write-closing, longform-upgrade |
| `memory/part-N.md` | longform-upgrade, then write and revise in long-form mode |
| `demolition-history.md` | demolish, demolish-persona |
| `voice-sample.md` | write, integrate (silently) |
| `style-rules.md` | rules, revise, corrections |
| `characters/*.md` | character-interview, character-check |
| `personas/*.md` | demolish-persona (custom personas) |
| `sessions/*.md` | start, chapter, review, finish |
| `project-state.md` | session-start |
| `corrections.md`, `manuscript/review-map.json` | corrections |
| `manuscript/*-final.md` / `.pdf` / `.epub` / `.docx` | manuscript-final, export-pdf, export-epub, export-docx |
| `podcast/**` | podcast |
| `graph/**` | graph (Sync) |
| `site.yaml`, `docs/index.html` | site |

## Setup

### check

**What it does:** verifies in about 60 seconds that the plugin and the project are set up correctly, and generates one test sentence in the author's voice. Read-only.

**Reads:** `.claude-plugin/plugin.json`, `presets/*.md`, `book.config.json`, `outline.md`, `book-memory.md`, `demolition-history.md`, `site.yaml` (via `build_site.py --check`), `graph/` (via `graph.py validate` and `check`). **Writes:** nothing.

**When:** right after installing, or whenever something feels broken.

**Examples:**

- Plugin just installed: `/ghost-writer:check` confirms the presets are readable.
- The site doesn't update: `/ghost-writer:check` reports a missing cover or an empty `podcast.base_url`.

### wizard

**What it does:** conversational setup for authors who don't know where to start. You describe the idea in your own words; the wizard works out genre, voice, premise and reader without ever mentioning presets or files.

**Writes:** `book.config.json` (created), `outline.md` (first draft with 3–5 chapters).

**When:** a new book, a non-technical author, or an idea that is still vague.

**Examples:**

- "I want to write about my years in sales, but I don't know if it's an essay or a memoir": `/ghost-writer:wizard`.
- A client describes the idea on a call: paste the transcript into the wizard.

### start

**What it does:** full onboarding macro — setup-author, then setup-book, then setup-voice. Resumes if interrupted.

**Writes:** `sessions/start.md` (onboarding state), plus everything the three setup skills write.

**When:** a new book, with an author willing to go through a structured onboarding (the more rigorous alternative to the wizard).

**Examples:**

- First session on a technical manual: `/ghost-writer:start`.
- Interrupted after setup-book: run `/ghost-writer:start` again and it picks up at setup-voice.

### setup-author

**What it does:** interviews the author about background, expertise, worldview and relationship with the reader.

**Writes:** `book.config.json → author_profile`.

**When:** first onboarding step, or to redo only the author profile.

**Example:** the author changed role and wants the new authority reflected: `/ghost-writer:setup-author`.

### setup-book

**What it does:** defines the book — central claim, structure, target reader, purpose and **genre preset** (essay, biography, fiction, fable, manual, childrens-book).

**Reads:** `presets/[preset].md`. **Writes:** `book.config.json → preset`, `preset_digest`, `book_profile`; `outline.md` (first draft).

**When:** after setup-author, or to rethink structure or genre.

**Examples:**

- A how-to book on LinkedIn lead generation: preset `manual`.
- A collection of company stories with a moral: preset `fable`.

### setup-voice

**What it does:** builds the author's *Voice Fingerprint* from an interview plus analysis of writing samples.

**Writes:** `book.config.json → author_voice`.

**When:** after setup-book. From here on the plugin can write.

**Example:** paste three of the author's posts and a newsletter, then run `/ghost-writer:setup-voice`.

## Writing

### chapter

**What it does:** macro for the full chapter cycle — ask-before-writing, write, demolish, integrate. Supports resume. *(Syncs the graph.)*

**Reads:** `book.config.json`, `book-memory.md`, `outline.md`. **Writes:** `sessions/chapter-[NN]-[slug].md`, plus everything the inner skills write.

**When:** the standard way to write a chapter.

**Examples:**

- "Let's write chapter 3": `/ghost-writer:chapter`.
- You stopped after the draft: `/ghost-writer:chapter` offers "Resume 3" at the demolish step.

### ask-before-writing

**What it does:** structured dialogue to clarify what the author wants to say before anything is written. The questions change with the genre.

**Reads:** `book.config.json`, `presets/[preset]-dialogue.md`, `book-memory.md` (defined terms, open promises, chapter summaries). **Writes:** nothing — the confirmed summary is handed to write.

**When:** before every write, if you're not using chapter.

**Example:** you only have a chapter title, "The funnel is dead": `/ghost-writer:ask-before-writing` pulls out the claim.

### freeflow

**What it does:** the author dumps everything in no order (text, transcribed voice notes); the skill extracts structure, claims and usable material. It can produce a draft with `[FROM DUMP]` sections.

**Reads:** `book.config.json`. **Writes:** `chapters/[NN]-[section].md` with `status: freeflow-draft` (only if you choose to generate the draft).

**When:** writer's block, unorganized ideas.

**Examples:**

- A ten-minute transcribed voice note: `/ghost-writer:freeflow`.
- Scattered notes on a chapter: freeflow, then demolish.

### write

**What it does:** generates a section of the book from the outline, in the author's voice.

**Reads:** `book.config.json`, `outline.md`, `book-memory.md`, `voice-sample.md`, `style-rules.md`. **Writes:** `chapters/[NN]-[slug].md`, `outline.md` (status set to `draft`), `book-memory.md` (or `memory/part-N.md` in long-form mode), `voice-sample.md` (silently).

**When:** after ask-before-writing has been confirmed.

**Example:** `/ghost-writer:write 04-pricing` once the content of chapter 4 is clear.

### demolish

**What it does:** hostile critique of the draft. Finds structural weaknesses, logical flaws, undefined concepts and contradictions — one issue at a time.

**Reads:** the chapter, `outline.md`, `demolition-history.md` (active sections). **Writes:** the *Demolition Log* at the bottom of the chapter, `demolition-history.md` (log, counters, archive of completed chapters).

**When:** as soon as a draft exists. See [The Constructive Demolition Protocol](../constructive-demolition-protocol/) for the method.

**Example:** `/ghost-writer:demolish chapters/02-attribution.md` before sending the chapter to a client.

### demolish-persona

**What it does:** demolition from a specific reader's point of view: `target-reader`, `hostile-reader`, `domain-expert`, `editor`, `out-of-target`, or a custom persona.

**Reads:** `personas/[persona].md` (by default only the *Quick Summary*), `book.config.json → target_reader` / `book_profile`. **Writes:** the chapter's Demolition Log, `demolition-history.md`, optionally `personas/[name].md` (custom persona).

**When:** after demolish, or for a targeted test.

**Examples:**

- A book for marketing directors: `/ghost-writer:demolish-persona domain-expert chapters/05-measurement.md`.
- A custom persona, "small-business owner, not technical", saved in `personas/` and reused on every chapter.

### integrate

**What it does:** turns the author's answers to the demolition into precise changes to the text. Nothing changes without approval, one change at a time. *(Syncs the graph.)*

**Reads:** `style-rules.md`, `book.config.json`. **Writes:** the chapter (text, `version`, optionally `status: complete`, Demolition Log entries set to `integrated`), `book-memory.md`, `voice-sample.md` (if three or more paragraphs were rewritten).

**When:** right after demolish, demolish-persona or review.

**Examples:**

- You answered six objections: `/ghost-writer:integrate` applies them one by one.
- "This is the final version": integrate sets `status: complete` and syncs the graph.

## Review and quality

### review

**What it does:** macro that runs demolition with all five personas in sequence (editor, target-reader, hostile-reader, domain-expert, out-of-target), then integrates. Supports resume. *(Syncs the graph.)*

**Reads:** the chapter, `demolition-history.md`. **Writes:** `sessions/review-[slug].md`, plus what demolish-persona and integrate write.

**When:** a deep review of a key chapter.

**Example:** the opening chapter before showing it to a publisher: `/ghost-writer:review chapters/01-intro.md`.

### consistency-check

**What it does:** cross-chapter audit — term drift, inconsistent tone, broken promises, contradicted claims, repeated examples. Produces a prioritized list.

**Reads:** all chapters, `book-memory.md`, `demolition-history.md`, `graph/INDEX.md` and cards (if the graph exists). **Writes:** `book-memory.md`, only when you resolve an item.

**When:** every 3–4 chapters.

**Example:** chapter 2 says "customer journey", chapter 6 says "buyer path": consistency-check flags it.

### proofread

**What it does:** grammar and style check — errors, repeated words, rhythm problems, phrases forbidden by the voice profile.

**Reads:** `book.config.json → author_voice`, the chapter. **Writes:** the chapter, only after explicit confirmation.

**When:** before the final integrate or the final draft.

**Example:** `/ghost-writer:proofread chapters/03-the-shift.md`.

### revise

**What it does:** editorial pass — grammar, punctuation and the rules in `style-rules.md`, event timeline, character details, continuity of objects, places, dates and numbers. Proposes every fix, never applies without confirmation. *(Syncs the graph.)*

**Reads:** `style-rules.md`, `book-memory.md` / `memory/part-*.md`, `characters/*.md`, the graph. **Writes:** the chapter, `book-memory.md` (Continuity Ledger), `style-rules.md` (inferred conventions or new rules).

**When:** on one chapter after integrate, or on the whole book before manuscript-final.

**Examples:**

- `/ghost-writer:revise chapters/07-case-study.md`.
- `/ghost-writer:revise --all` before the final assembly.

### rules

**What it does:** manages the book's writing rules (punctuation conventions and custom rules). Enforced by write, integrate and revise.

**Reads:** `book.config.json → language` for the defaults. **Writes:** `style-rules.md` (created from the template if missing).

**When:** whenever you have a convention to apply to the whole book.

**Examples:**

- `/ghost-writer:rules add "always use double quotes for thoughts"`.
- `/ghost-writer:rules infer` to infer the rules from chapters already written; `/ghost-writer:rules remove R3`.

### corrections

**What it does:** collects and applies the corrections you make while re-reading away from the computer: a review PDF with paragraph IDs in the margin (3.12 = chapter 3, paragraph 12), import of PDF annotations, or free-form notes (voice dictation, photos of marked-up pages). *(Syncs the graph.)*

**Writes:** `corrections.md`, `manuscript/review-map.json`, chapters, `book-memory.md` (Continuity Ledger), `style-rules.md` (when a correction becomes a rule). Uses `review_pdf.py` (requires `reportlab` and `pymupdf`).

**When:** re-reading on paper or tablet.

**Examples:**

- `/ghost-writer:corrections print 1-4`: a PDF to read on a tablet.
- `/ghost-writer:corrections import annotated.pdf` once you've highlighted it.
- Paste a voice note — "in 5.8 drop 'basically'" — and run `/ghost-writer:corrections`.

### retune

**What it does:** realigns a chapter to the author's real voice when they say "this doesn't sound like me", starting from their own rewrite or notes. *(Syncs the graph.)*

**Writes:** the chapter (and its `version`), `book.config.json → author_voice` (new signature phrases and patterns).

**When:** after reading a draft that doesn't feel like yours.

**Example:** the author rewrites the first paragraph their way; `/ghost-writer:retune` uses it to realign the whole chapter and update the voice profile.

### character-interview

**What it does:** deep interview on a character's psychology, behavior, contradictions and voice — real or fictional.

**Writes:** `characters/[name].md` (folder created if missing), `book-memory.md → ## Characters`.

**When:** once per character, before writing scenes that feature them.

**Example:** a founder's biography: `/ghost-writer:character-interview co-founder`.

### character-check

**What it does:** verifies that a character behaves consistently with their profile in a chapter.

**Reads:** `characters/[name].md`, the chapter, the graph. **Writes:** `characters/[name].md` (*Notes* and *Arc Moments* sections).

**When:** after every chapter that features a profiled character.

**Example:** `/ghost-writer:character-check marco chapters/06-crisis.md`.

### graph

**What it does:** the book graph — characters, organizations, places, concepts, terms and events, each linked to the exact line of the chapter it comes from. Fed only by `complete` chapters; other skills call its Sync.

**Writes:** `graph/cards/**/*.yaml`; `graph/INDEX.md`, `graph/graph.json`, `graph/view/`, `graph/snapshots/`, `graph/chapters.yaml` (generated by `graph.py`); `docs/index.html` if `site.yaml` exists. Requires `pyyaml`.

**When:** to look something up, force a sync or migrate an old graph.

**Examples:**

- `/ghost-writer:graph find "attribution model"`: where it is defined and used.
- `/ghost-writer:graph check`: chapters waiting for a sync.

## Finishing

### finish

**What it does:** closing macro — introduction, conclusion, arc audit, manuscript assembly. Skips the steps already done and supports resume.

**Writes:** `sessions/finish.md`, `chapters/00-introduction.md`, `chapters/99-conclusion.md`, `manuscript/[title]-final.md`.

**When:** all chapters are complete.

**Example:** last chapter integrated: `/ghost-writer:finish`.

### write-opening

**What it does:** writes the introduction **last**, because it can only make promises the book has actually kept.

**Reads:** the whole book, `book-memory.md`, `outline.md`, `demolition-history.md`. **Writes:** `chapters/00-introduction.md`.

**When:** after all chapters.

**Example:** `/ghost-writer:write-opening` on a finished lead-magnet ebook.

### write-closing

**What it does:** writes the conclusion that closes the arc opened by the introduction. It doesn't summarize — it lands.

**Reads:** the whole book, `chapters/00-introduction.md`. **Writes:** `chapters/99-conclusion.md`, `book-memory.md → Open Promises` (marked resolved).

**When:** after the introduction.

### manuscript-final

**What it does:** final audit (arc, promises kept, opening–closing correspondence) and assembly of a clean manuscript.

**Reads:** all chapters, `outline.md`, `book-memory.md`, `demolition-history.md`. **Writes:** `manuscript/[title]-final.md`, optionally `manuscript/process-note.md`.

**When:** the last step before exporting.

## Export

### export-pdf

**What it does:** a readable PDF with cover page, table of contents and chapter layout (ReportLab).

**Reads:** `book.config.json`, `manuscript/[title]-final.md`. **Writes:** `manuscript/[title]-final.pdf`, `export_pdf.py` (generated if missing).

**Example:** a PDF for beta readers, or a lead magnet to download from a landing page.

### export-epub

**What it does:** an EPUB that works on Kindle, Kobo and Apple Books.

**Reads:** as above. **Writes:** `manuscript/[title]-final.epub`, `export_epub.py`.

**Example:** self-publishing on Amazon KDP.

### export-docx

**What it does:** a DOCX with clean styles for editors, agents and publishers.

**Reads:** as above. **Writes:** `manuscript/[title]-final.docx`, `export_docx.py`.

**Example:** handing the book to a copy editor who works in Word with tracked changes.

### podcast

**What it does:** turns the book into a narrated podcast, one episode per chapter: voice chosen from audio samples, scripts written for the ear (approved by the author), MP3s and an RSS feed. Free and offline (Piper TTS + ffmpeg).

**Reads:** chapters, `style-rules.md`. **Writes:** `book.config.json → podcast`, `podcast/plan.md`, `podcast/scripts/episode-NN.md`, `podcast/episodes/episode-NN.mp3`, `podcast/feed.xml`, `podcast/voices/`, `export_podcast.py`.

**When:** complete chapters you want to reuse as audio content.

**Examples:**

- `/ghost-writer:podcast voice` to pick the voice; `/ghost-writer:podcast script 3` for the chapter 3 script.
- `/ghost-writer:podcast build 3` for the MP3; `/ghost-writer:podcast feed` for the RSS feed for Spotify and Apple Podcasts.
- `/ghost-writer:podcast jingle` for the intro music.

## Publishing

### site

**What it does:** builds the book's website — one mobile-first page for GitHub Pages with cover, download button, featured characters or key ideas, podcast episodes and the explorable graph.

**Reads:** `graph/cards/**/*.yaml`, `podcast/**`, `manuscript/*.pdf` / `.epub`, `cover.jpg` / `cover.png`. **Writes:** `site.yaml`, `docs/index.html` (plus copied assets), `build_site.py`, `book.config.json → podcast.base_url`.

**When:** the book is ready to promote.

**Example:** a free landing page with a downloadable PDF: `/ghost-writer:site`, then push `docs/`.

### gallery

**What it does:** drafts the book's entry for the [gallery](/books/), validates it and opens a pull request (or a pre-filled issue). Nothing is sent without your explicit OK.

**Reads:** `book.config.json`, `site.yaml`. **Writes:** `book.config.json → gallery` (slug, PR or issue URL, date).

**Example:** once the site is live: `/ghost-writer:gallery`. More in [How to add your book to the gallery](../add-your-book-to-the-gallery/).

## Status and utilities

### session-start

**What it does:** opening briefing — where you left off, what's pending, what to work on today. At the end of the day it logs the session.

**Reads:** `project-state.md` (fast path if updated in the last 7 days), `book.config.json`, `book-memory.md`, `outline.md`, `demolition-history.md`. **Writes:** `project-state.md` (regenerated), `book-memory.md → ## Session Log`; runs pending graph syncs.

**Example:** Monday morning, back on the project after a week: `/ghost-writer:session-start`.

### resume

**What it does:** one status line and a single recommendation for the next step. Fast scan, read-only.

**Reads:** `book.config.json`, `outline.md`, `sessions/`, `demolition-history.md`, the most recently modified file in `chapters/`. **Writes:** nothing.

**Example:** you have fifteen minutes and want to know what to do: `/ghost-writer:resume`.

### status

**What it does:** full overview — chapters complete, in draft, not yet written — and the suggested next step.

**Reads:** `book.config.json`, `outline.md`, the graph. **Writes:** nothing.

**Example:** a progress report to share with a client or co-author.

### help

**What it does:** every command grouped by phase, with a suggested next step. Read-only.

**Reads:** `book.config.json` (if it exists). **Writes:** nothing.

### longform-upgrade

**What it does:** activates long-form mode for books with 10+ chapters: splits the book into parts, splits the memory per part, adds chapter summaries, and makes every skill read lazily.

**Writes:** `outline.md` (part headers), `book-memory.md` (becomes a global index), `memory/part-N.md`, `book.config.json` (`longform_mode`), the graph.

**When:** automatically when the 10th chapter is completed, or by hand.

**Example:** a 14-chapter manual where sessions are getting slow: `/ghost-writer:longform-upgrade`.

## Typical workflows

| Goal | Sequence |
|---|---|
| A new book from scratch | `check` → `wizard` (or `start`) → `chapter` × N → `finish` → `export-pdf` |
| A chapter from messy notes | `freeflow` → `ask-before-writing` → `write` → `demolish` → `integrate` |
| Bulletproofing a key chapter | `chapter` → `review` → `character-check` → `proofread` |
| Re-reading on paper | `corrections print` → (annotate) → `corrections import` → `revise --all` |
| One book, many channels | `manuscript-final` → `export-pdf` / `export-epub` → `podcast` → `site` → `gallery` |
