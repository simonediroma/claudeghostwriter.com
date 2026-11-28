---
title: Build your podcast
description: Turn your finished book into a narrated podcast and publish it on Spotify, Apple Podcasts, YouTube Music and Amazon Music. Free, offline, no API keys.
date: 2026-11-28
weight: 6
level: Publishing
---
Ghost Writer can turn your book into a narrated podcast, one episode per chapter, and give you everything the podcast apps need to list it. It costs nothing: the voice is generated offline with [Piper](https://github.com/OHF-Voice/piper1-gpl), the audio is built with ffmpeg, and the episodes can be hosted for free on GitHub Pages. If you want a more natural voice, or your own cloned voice, you can [render the episodes with ElevenLabs](#premium-voice-with-elevenlabs-optional) instead.

## The path at a glance

| Step | Command | Time |
|---|---|---|
| 1. Install the tools | `pip install piper-tts numpy` + ffmpeg | 5 min |
| 2. Choose the voice | `/ghost-writer:podcast voice` | 10 min |
| 3. Intro jingle (optional) | `/ghost-writer:podcast jingle` | 5–15 min |
| 4. Episode plan | `/ghost-writer:podcast` | 2 min |
| 5. Scripts for the ear | `/ghost-writer:podcast script [chapter]` | 5 min per episode |
| 6. Render the MP3s | `/ghost-writer:podcast build` | a few minutes |
| 7. Hosting and RSS feed | `/ghost-writer:site` + `/ghost-writer:podcast feed` | 15 min |
| 8. Submit to the platforms | by hand, once | 30 min |

`/ghost-writer:podcast` runs the whole flow and picks up where you left off.

## Before you start

- **A finished book.** The podcast is built from `manuscript/[title]-final.md` (from `/ghost-writer:manuscript-final`) or from the chapters in `chapters/`. If a chapter is still a draft, the plugin warns you: the podcast works best from integrated text.
- **Piper and ffmpeg:**

```bash
pip install piper-tts numpy
sudo apt install ffmpeg      # Linux
brew install ffmpeg          # macOS
winget install ffmpeg        # Windows
```

On first use the plugin creates `export_podcast.py` in your project and checks both. **Your chapters are never modified**: the scripts live in `podcast/scripts/`.

## Choose the narrator

```
/ghost-writer:podcast voice
```

1. The plugin lists the Piper voices for your book's language and recommends two or three (for English, `en_US-lessac-medium`).
2. It renders a **sample from a real passage of your book** into `podcast/samples/`, so you hear your own prose. Listen and pick one.
3. Tune it together, with a new sample after each change:
   - **Speed**: `0.9` for narrative, `1.0` natural, `1.1` for manuals.
   - **Pauses** between sentences and paragraphs: longer pauses feel calmer and more literary.

For fiction, fables, children's books and biographies you can also give the main characters their own voice. By default the narrator reads everything, like a classic audiobook.

> **Voice licenses.** Each Piper voice has its own model card with the license of its training data. If you plan to monetize the podcast, check that your voice allows commercial use.

## Add an intro jingle (optional)

```
/ghost-writer:podcast jingle
```

- **Composed offline** (recommended): an original 6–9 second sting, no license issues. The style follows your genre: `warm`, `upbeat`, `mysterious`, `playful` or `grime`. Ask for "another one" to get a new variation.
- **AI music, locally**, with the open-source ACE-Step (needs a GPU with about 8 GB or an Apple Silicon Mac). The plugin writes the prompt for you.
- **Your own file**, or CC0 music (for example Freesound with the CC0 filter).

The voice comes in over the tail of the jingle.

## Plan the episodes

The plugin proposes **one episode per chapter**. It merges chapters under about 800 words and splits those over about 6,000 (roughly 40 minutes) at a scene break.

```
PODCAST PLAN — [title]
  Ep 1  Introduction           ~1,900 words · ~13 min
  Ep 2  Ch. 1 — [title]        ~3,400 words · ~23 min
```

Once you confirm, the plan is saved to `podcast/plan.md` with a status for each episode.

## Scripts written for the ear

```
/ghost-writer:podcast script 1
```

Your voice comes first: sentences, rhythm and vocabulary stay yours. Only what doesn't work when heard changes:

- lists and tables become spoken sentences;
- "see above" or "in the figure" are rewritten or dropped;
- numbers, dates, symbols and abbreviations are spelled out ("$1,500" becomes "fifteen hundred dollars");
- sentences over about 45 words are split at a natural point, never changing their meaning;
- pauses mark scene breaks.

Each episode gets a short opening (book title, episode number, a line recalling the previous episode) and a closing that teases the next one without spoilers.

**You approve every script.** You see the opening, the closing and a compact list of every change. Nothing goes to audio before your OK.

## Render the audio

```
/ghost-writer:podcast build              # all approved scripts
/ghost-writer:podcast build episode-02   # one episode
```

The episodes land in `podcast/episodes/`: mono MP3 at 96 kbps, the standard for spoken word, with title, book and author tags. A 40-minute episode is about 29 MB.

**Listen to the first two minutes of episode 1 before publishing.** If a word is mispronounced, tell the plugin: it fixes the spelling in the script, re-renders only that episode and remembers the fix for the next ones.

## Premium voice with ElevenLabs (optional)

Piper is free and offline. [ElevenLabs](https://elevenlabs.io) is a paid text-to-speech service with more expressive voices, and it can **clone your own voice** so the podcast is read by you. The plugin doesn't call ElevenLabs itself, but everything else stays the same: you still plan the episodes and approve every script with `/ghost-writer:podcast`, then render the audio with the small script below instead of `/ghost-writer:podcast build`.

### What you need

- **An ElevenLabs account and API key**: Profile → API Keys. Check the current plans on the [pricing page](https://elevenlabs.io/pricing): usage is billed in characters, and you need a paid plan to publish commercially without attribution and to clone your voice.
- **A voice ID**: pick a voice in the Voice Library, or create your own with Voice Cloning, then copy its ID from the voice's menu.
- **Python with `requests`** (`pip install requests`) and ffmpeg.

A 3,400-word chapter is roughly 20,000 characters, so you can estimate the cost of the whole book before you start: count the characters in `podcast/scripts/`.

### Render the episodes

Save this as `elevenlabs_podcast.py` in your project folder:

```python
"""Render approved Ghost Writer podcast scripts with ElevenLabs.

Usage:  python3 elevenlabs_podcast.py [episode-02.md]
Needs:  ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID, ffmpeg
"""
import os, re, sys, glob, subprocess, tempfile, requests

KEY = os.environ["ELEVENLABS_API_KEY"]
VOICE = os.environ["ELEVENLABS_VOICE_ID"]
MODEL = os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")
CHUNK = 4000  # characters per request, below every model's limit

def clean(md):
    md = re.sub(r"^---\n.*?\n---\n", "", md, flags=re.S)           # front matter
    md = re.sub(r"\[pause ([\d.]+)\]", lambda m: f'<break time="{min(float(m[1]), 3)}s" />', md)
    md = re.sub(r"\[(voice [^\]]+|narrator)\]", "", md)            # single narrator
    md = re.sub(r"^#+\s*", "", md, flags=re.M)                      # headings
    return re.sub(r"\n{3,}", "\n\n", md).strip()

def chunks(text):
    out, cur = [], ""
    for p in text.split("\n\n"):
        if cur and len(cur) + len(p) > CHUNK:
            out.append(cur); cur = ""
        cur = f"{cur}\n\n{p}" if cur else p
    return out + [cur] if cur else out

def render(path):
    md = open(path, encoding="utf-8").read()
    if not re.search(r"^status:\s*(approved|rendered)", md, re.M):
        print(f"skip {path}: not approved"); return
    parts, prev_ids = [], []
    tmp = tempfile.mkdtemp()
    for i, text in enumerate(chunks(clean(md))):
        r = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128",
            headers={"xi-api-key": KEY},
            json={"text": text, "model_id": MODEL, "previous_request_ids": prev_ids[-3:]},
            timeout=300)
        r.raise_for_status()
        prev_ids.append(r.headers.get("request-id", ""))
        f = os.path.join(tmp, f"{i:03}.mp3"); open(f, "wb").write(r.content); parts.append(f)
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    os.makedirs("podcast/episodes", exist_ok=True)
    out = "podcast/episodes/" + os.path.basename(path).replace(".md", ".mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-ac", "1", "-b:a", "96k", out], check=True)
    print(f"ok {out} ({len(parts)} requests)")

files = [f"podcast/scripts/{a}" for a in sys.argv[1:]] or sorted(glob.glob("podcast/scripts/episode-*.md"))
for f in files:
    render(f)
```

Then run it:

```bash
pip install requests
export ELEVENLABS_API_KEY="your-key"
export ELEVENLABS_VOICE_ID="the-voice-id"
python3 elevenlabs_podcast.py                 # all approved scripts
python3 elevenlabs_podcast.py episode-02.md   # one episode
```

What the script does:

- renders only scripts with `status: approved`, like the plugin;
- turns `[pause 1.5]` into ElevenLabs pauses (up to 3 seconds each);
- reads everything with one voice: character voice tags are ignored;
- splits long chapters into chunks and links them (`previous_request_ids`), so the tone stays consistent across the episode;
- writes `podcast/episodes/episode-NN.mp3`, mono at 96 kbps, the same files and names the plugin uses. The next steps, from the feed to the platforms, don't change.

The default model is `eleven_multilingual_v2`, which reads 29 languages and supports pauses. To try another one, set `ELEVENLABS_MODEL`. The script doesn't add the intro jingle: if you want one, mix it in with ffmpeg or an audio editor.

**Keep the key private.** Don't write it in the script or commit it to the repository: set it as an environment variable, as shown above.

**Disclose the synthetic voice** in the show description, even when it's a clone of yours.

## Host the episodes and create the feed

Podcast platforms don't store your files. They read an **RSS feed** that points to MP3s published online. You need a public place for the MP3s and a `feed.xml`.

### The free way: your book website on GitHub Pages

1. Build the site with `/ghost-writer:site`. It gets a podcast section with a player, the episodes and a link to the feed.
2. On GitHub, open the repository's **Settings → Pages → Deploy from a branch → `main` / `docs`**.
3. In `book.config.json`, set the folder where the episodes will be served:

```json
"podcast": { "base_url": "https://<user>.github.io/<repository>/episodes" }
```

4. Generate the feed and rebuild the site:

```
/ghost-writer:podcast feed
python3 build_site.py
```

5. Commit and push `docs/`.

Your feed address, the one you'll give to every platform, is:

```
https://<user>.github.io/<repository>/feed.xml
```

GitHub Pages allows files up to 100 MB and about 1 GB per site: enough for a whole book at 96 kbps. Other free options: GitHub Releases, the Internet Archive, or your own website.

### Checklist before you submit

- **Cover**: square, JPG or PNG in RGB, **3000 × 3000 px** (1400 × 1400 minimum). Apple and Spotify both require it.
- **Owner email** in the feed (`itunes:owner` / `itunes:email`): Spotify and others send the verification code there.
- **Category, language and the explicit flag** are set.
- **Every MP3 link opens** in the browser.
- **The feed validates** in a free checker such as [Podbase](https://podba.se/validate/) or [Cast Feed Validator](https://www.castfeedvalidator.com/).
- **The show description says the narration uses a synthetic voice.** It's good practice, and some platforms ask you to disclose AI-generated content.

If something is missing, ask the plugin to add it and run `/ghost-writer:podcast feed` again.

## Submit to the platforms

You do this **once**. From then on, every new episode you add to the feed shows up everywhere on its own.

| Platform | Where | What to do | Review |
|---|---|---|---|
| **Apple Podcasts** | [podcastsconnect.apple.com](https://podcastsconnect.apple.com) | Sign in with your Apple ID → **+** → New Show → add the RSS feed URL → submit for review | 1–5 days |
| **Spotify** | [creators.spotify.com](https://creators.spotify.com) | Sign in → choose to add an existing podcast → paste the feed URL → enter the code sent to the feed's email | minutes to hours |
| **YouTube / YouTube Music** | [studio.youtube.com](https://studio.youtube.com) | Create → New podcast → Submit RSS feed → paste the URL and confirm your rights | hours to days |
| **Amazon Music / Audible** | [podcasters.amazon.com](https://podcasters.amazon.com) | Sign in → add your podcast → paste the URL → verify by email | 1–2 days |
| **Deezer** | [podcasters.deezer.com](https://podcasters.deezer.com) | Sign up → add podcast → paste the URL | 1–3 days |
| **Podcast Index** | [podcastindex.org/add](https://podcastindex.org/add) | Paste the URL. It feeds Podcast Addict, Fountain, Podverse and many other apps | minutes |

Overcast, Pocket Casts, Castro and Castbox read Apple's directory and Podcast Index, so your show appears there shortly after approval, with no extra step.

**Suggested order:** Apple first, since its review is the slowest and many apps rely on its directory. Then Spotify. Then YouTube, Amazon, Podcast Index and Deezer on the same day.

The platforms change their dashboards often: if a button has moved, look for "add show" or "submit RSS feed".

## After launch

**A new episode**, for example if you publish the book in installments:

```
/ghost-writer:podcast script 5
/ghost-writer:podcast build episode-05
/ghost-writer:podcast feed
python3 build_site.py
git add docs podcast && git commit -m "Episode 5" && git push
```

The platforms re-read the feed on their own, usually within a few hours.

**Fixing a published episode:** re-render it under the same file name and push. Don't rename files or change URLs: podcast apps use them to identify episodes.

**Stats** live in each platform's dashboard: Spotify for Creators, Apple Podcasts Connect, YouTube Studio, Amazon.

**Share it:** your book website already shows the player and episodes, and you can [add the book to the gallery](/guides/add-your-book-to-the-gallery/) with a link to the podcast.

## Common problems

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: piper` | `pip install piper-tts numpy` |
| `ffmpeg: command not found` | Install ffmpeg (see Before you start) |
| A word sounds wrong | Tell the plugin: it fixes the script and re-renders only that episode |
| Spotify's code never arrives | Check the email is in the feed (`itunes:email`) and look in spam |
| Apple rejects the feed | Almost always the cover: square, 1400–3000 px, RGB, JPG or PNG |
| ElevenLabs returns 401 | The API key is missing or wrong: check `ELEVENLABS_API_KEY` |
| ElevenLabs returns 402 or a quota error | You're out of characters for the month: upgrade the plan or wait for the reset |
| A new episode doesn't appear | Check the updated `feed.xml` is online, then wait a few hours |
| An episode won't play | Open the MP3 link in a browser: it must play or download |
