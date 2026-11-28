---
title: "Project files explained: what Ghost Writer creates and where answers come from"
description: How the plugin works, what every file in your book's folder is for and what it holds, and which file answers a question about your plot or characters.
date: 2026-11-28
weight: 9
level: Reference
---
Ghost Writer writes a book with you, not instead of you. You bring the ideas. Claude gives them shape, writes them in your voice, then attacks them. The whole state of the project lives in Markdown, JSON and YAML files in your book's folder, so every session starts from those files rather than from the chat's memory.

This guide explains the cycle, every file the plugin creates, and which file answers the questions you will ask about your story.

## How it works

The cycle has four phases:

1. **Onboarding (once).** `/ghost-writer:start` (or `/ghost-writer:wizard` if your idea is still vague) runs `setup-author`, `setup-book` and `setup-voice`. It covers who you are, what the book is about, which genre preset to use (essay, fiction, manual, biography, fable, childrens-book) and what your voice sounds like. It produces `book.config.json` and a first `outline.md`.
2. **Chapter (repeated).** `/ghost-writer:chapter` runs `ask-before-writing` (a dialogue, one question at a time), `write` (the draft), `demolish` (hostile critique) and `integrate` (changes approved one by one). Optional: `review` (five reader personas), `revise` (grammar, timeline, continuity), `character-interview` and `character-check`.
3. **Periodic check.** `consistency-check` every 3–4 chapters finds drifting terms, broken promises and contradicted claims.
4. **Closing (once).** `/ghost-writer:finish` writes the introduction last, then the conclusion, audits the arc and assembles the manuscript. After that come the exports (PDF, EPUB, DOCX), the [podcast](/guides/build-your-podcast/) and the [website](/guides/build-your-book-website/).

The one command to remember is `/ghost-writer:session-start` (or `/ghost-writer:resume`). It reads `project-state.md` and tells you where you left off and what to do today.

Three rules hold everywhere: one question at a time; no change to the text without your approval; the book graph holds only what the chapters say, with line and quote.

For every command, see the [skills reference](/guides/skills-reference/).

## The project files

The plugin creates and updates these files in your book's folder. The only ones you really edit by hand are `style-rules.md`, the cards in `graph/cards/` and, if needed, the profiles in `characters/`.

| File | What it's for | What it holds | Written by |
|---|---|---|---|
| `book.config.json` | The project's identity card | Title, preset, language, target reader, voice profile (tone, register, point of view, rhythm, signature phrases, things to avoid), preset digest, writing log, podcast settings | setup-book, wizard, setup-voice, retune |
| `outline.md` | Working table of contents | Chapter list with status (to write / draft / complete); in long-form mode, the parts too | setup-book, write, chapter, longform-upgrade |
| `chapters/NN-slug.md` | The book's text | Frontmatter (`title`, `version`, `claim`, `status`, `summary`), the chapter text, a Demolition Log per cycle (issue, category, status, resolution) | write, integrate |
| `book-memory.md` | The book's memory, read by every skill | Defined terms, central claims, open promises to the reader, examples already used, recurring metaphors, character table, **Timeline** of events, **Continuity Ledger** (objects, places, numbers, minor names: the first mention is canonical) | write, integrate, revise, consistency-check, character-interview |
| `characters/<name>.md` | A character's psychological profile | Surface and contradiction, three sample lines of voice, wound, belief, fear, blind spot, behavior under stress and in conflict, the "tell", want vs. need, arc (or the author's stance, for real people), notes | character-interview |
| `graph/cards/<type>/<id>.yaml` | The book graph: what the text actually says | For fiction: characters, organizations, objects, places, concepts, terms, events. Every entry has a `source` (`c3:19` = chapter 3, line 19) and an exact quote. Fields: `traits`, `state` per chapter, `relations`, `not_said` (what the text doesn't say), `open` (doubts and errors). Events add `order`, `when`, `where`, `involved`, `after` | automatic graph sync |
| `graph/view/`, `INDEX.md`, `graph.json`, `snapshots/` | Generated views of the graph | Readable cards, backlinks, event chain per chapter, a copy of the analyzed text for diffs | graph.py (never edit) |
| `project-state.md` | Digest for a fast restart | Chapter counts, last session, next step, chapter in progress and its step, open issues | session-start |
| `demolition-history.md` | The whole book's critique log | Totals of cycles and issues (resolved, deferred, accepted limitations), patterns that recur across chapters | demolish |
| `voice-sample.md` | Style reference | Three paragraphs taken from the last chapter written | write, integrate |
| `style-rules.md` | Writing rules | Punctuation conventions (dialogue, thoughts, dashes, numbers) and your own rules, each with a right and a wrong example | rules, corrections, you |
| `corrections.md` | Queue of corrections from re-reading | Corrections with paragraph IDs (`3.12`) imported from an annotated PDF, notes or photos | corrections |
| `sessions/` | State of the macro commands | How far chapter, review and finish got, so they can resume | chapter, review, finish |
| `memory/part-N.md` | Per-part memory (books with 10+ chapters) | Summary of the part, terms and claims introduced in it | longform-upgrade, write |
| `manuscript/`, `podcast/`, `site.yaml`, `docs/` | Final outputs | Manuscript and exports, podcast scripts and MP3 episodes with RSS feed, website texts and pages | manuscript-final, export-*, podcast, site |

When a chapter reaches `status: complete`, it enters the graph. When its `version` changes, the graph re-syncs only the paragraphs that changed.

## Sample questions and where the answers come from

A rule of thumb:

- **What happened in the text** comes from the graph, with line and quote.
- **What you decided about a character** comes from `characters/`.
- **What the book promised or fixed** comes from `book-memory.md`.

The examples use a novel with Marta, the lighthouse keeper, and Ferro, her cat.

| Question | Where the information comes from | How it answers |
|---|---|---|
| How old is Marta? | `graph/cards/characters/marta.yaml` → `traits` and `not_said` | If a chapter says it, it cites the line (e.g. `c1:8`); if it's in `not_said`, it answers "the text never says" instead of making it up |
| What does Marta know at the end of chapter 4? | Marta's card → `state` filtered by `chapter: 4` (`graph.py find marta`) | Her state chapter by chapter, each with its quote |
| What is the relationship between Marta and Ferro? | Marta's card → `relations` (`to: ferro, type: "lives with"`) | The kind of relationship and the line where the text establishes it |
| How would Marta react if someone accused her of lying? | `characters/marta.md` → *In conflict*, *The tell*, *Under stress* | It answers from the profile you defined, not from the text |
| Does this line sound like Marta? | `characters/marta.md` → *Voice* + her graph card (`character-check`) | It compares the line with the three sample lines and the traits already in the text, and flags any drift citing both lines |
| In what order do the events of chapter 2 happen? | `graph/cards/events/` → `order`, `after`, `when` (`graph.py find --chapter 2`) + `book-memory.md` → Timeline | The sequence of events and which events each one follows from |
| Who wrote the note? | Card → `open` | If it's an open question, it says so: a gap still to resolve, not a fact |
| What color was the lantern the first time it appeared? | `book-memory.md` → Continuity Ledger + the object's card | The first mention is canonical; if a later chapter contradicts it, `revise` flags it |
| Did we promise the reader to explain why the lighthouse is dark? | `book-memory.md` → Open Promises | The chapter where the promise was made and whether it has been resolved |
| What is the book's dramatic question, and what does chapter 3 argue? | `book.config.json` (fiction preset) + the `claim` in the frontmatter of `chapters/03-*.md` | The book's and the chapter's thesis, in the words you already approved |
| What happens in chapter 7, in short? | The chapter's `summary` frontmatter (long-form mode) or `memory/part-N.md` | A 3–5 sentence summary, without re-reading the whole chapter |
| Where did we leave chapter 5? | `project-state.md` + `sessions/` | The current step (write, demolish, integrate) and any deferred issues |

The graph only knows what `complete` chapters say: a draft is not a source yet. If the answer isn't in any file, the plugin says so and asks you.
