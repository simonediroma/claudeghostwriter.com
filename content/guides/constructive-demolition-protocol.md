---
title: "The Constructive Demolition Protocol: why every chapter gets demolished"
description: The method behind Ghost Writer's demolition cycles. Draft first, attack second, one question at a time, and nothing resolved without the author.
date: 2026-11-24
weight: 4
level: The method
---
Every chapter you write with Ghost Writer goes through a **demolition**: Claude attacks the draft, you defend it or rewrite it, and the answers go back into the text. That cycle isn't improvised. It comes from the **Constructive Demolition Protocol (CDP)**, a method for hardening any written artifact, from a product spec to an essay. It was developed by the same author as the plugin.

> *Every specification has blind spots. The CDP finds them before reality does.*

For a book, read "readers" where the CDP says "reality".

## Generative first, adversarial second

The CDP starts by building, not by attacking. It has two phases:

1. **Generative.** Raw material becomes a complete first draft, coherent enough to be attacked. The AI asks one question at a time, and only about the gaps. What the author hasn't said stays explicitly marked as open: *inventing content to fill gaps is forbidden*.
2. **Adversarial.** The draft is demolished in rounds. Each round brings one perspective and one angle of attack, and is followed by integration.

In Ghost Writer the first phase is the setup and the dialogue before each chapter (`setup-*`, `ask-before-writing`, `write`). It's where the first principle of the plugin comes from: **Claude formalizes, it doesn't invent.** The second phase is `demolish`, `demolish-persona` and `integrate`.

## Three roles, never mixed

- **The persona attacks.** It is a reader with a specific angle, looking for what doesn't hold.
- **The facilitator orchestrates.** It keeps the state of the round: it counts the issues, keeps the attacks short and records every decision. In Ghost Writer, Claude running the command plays this role.
- **The author judges.** Only you decide whether an objection is answered, parked or accepted as a limit.

## Two rules for every round

**R1 — Few issues, sharp ones.** The CDP sets a soft cap of about five vulnerabilities per cycle. Five precise issues demolish more than ten diluted ones. Anything beyond the cap isn't lost: it moves to the next cycle. Ghost Writer applies the same idea: `demolish` maps the weaknesses and attacks them **in order of severity**, and `demolish --light` keeps only the **three most critical**.

**R2 — Short critique, sharp question.** Each attack is a sentence or two on the problem, a little context, and **one direct question** about what you have to defend, justify or rewrite. The question is the payload. That's why Ghost Writer asks **one objection at a time** and doesn't move on until the current one is resolved or consciously parked.

## Nothing is resolved without you

In the CDP an issue changes state only through an exchange. The persona attacks, the author answers, the facilitator judges whether the answer is enough, and the author confirms. Silence doesn't resolve anything. The protocol never closes an issue on its own.

In Ghost Writer every objection ends in one of three states, written to `demolition-history.md`:

| State | Meaning | What happens next |
|---|---|---|
| **resolved** | You answered and the answer holds | `integrate` brings it into the text, one change at a time, with your confirmation. It is never raised again. |
| **deferred** | Not now: maybe the answer will appear later in the book | It is raised **first** in the next demolition cycle |
| **accepted-limitation** | A conscious limit, declared out of scope | It is not raised again unless new context makes it critical |

The CDP classifies vulnerabilities by severity: **critical** blocks progress, **major** requires a written decision, **minor** goes to the backlog. The ghost-writing version of the same discipline: don't move on while a critical objection is open, and don't let a major one die in silence. Park it or accept it explicitly.

## Rounds are never batched

One round, one perspective, then integration, and only then the next round. The CDP insists on this: tight feedback loops keep the author **writing**, instead of supervising a pile of criticism at the end. In Ghost Writer every `demolish` is followed by `integrate`, and `/ghost-writer:chapter` chains them for you.

Different perspectives get different rounds. The CDP's reference personas are built for specifications (the skeptical user, the developer, the business owner…). Ghost Writer adapts them to books:

| Persona | Looks for |
|---|---|
| `target-reader` | accessibility, relevance, engagement for the reader the book is for |
| `hostile-reader` | unsupported claims, avoided objections |
| `domain-expert` | technical gaps, overclaims |
| `editor` | structure, pacing, prose |
| `out-of-target` | unexplained jargon, invisible assumptions |

Run them with `/ghost-writer:demolish-persona [persona]`, or all five in sequence with `/ghost-writer:review`.

## When is a chapter done?

The CDP declares an artifact *hardened* when it has gone through at least three rounds (a default the author can change), has no open critical issues, has every major issue accepted in writing, and has a complete demolition history. The final declaration is always the author's.

It also offers a practical signal: **convergence**. When each new round finds fewer issues, and each new persona finds less than the previous one, you're close.

For a chapter, a good routine is:

1. `demolish`: the full stress test on logic and structure, then `integrate`.
2. One or two `demolish-persona` rounds with the readers who matter most for this book, each followed by `integrate`.
3. `demolish --light` on late revisions: if the three most critical issues are minor, the chapter has converged.

Keep each round in a manageable context: see [how to use Claude properly to write your book](../how-to-use-claude-to-write-your-book/).

## The history is part of the book

Every round, every objection and every decision stays in `demolition-history.md`. Deferred issues come back at the right time, resolved ones never return, and recurring patterns emerge across chapters. At the end you have a book plus a transparent record of every challenge it survived.

## Learn more

The full protocol (procedure, personas, severity scale, exit criteria and the rules for running it on any LLM) is in the [Constructive Demolition Protocol documentation](https://simonediroma.github.io/cdp/).
