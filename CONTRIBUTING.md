# Add your book to the gallery

Books are added with a pull request. Each book is one folder:

```
content/books/my-book/
  index.md      required
  cover.jpg     optional — max 2 MB (.jpg, .png or .webp); 2:3 ideal, square OK
```

## From your book project (recommended)

If you wrote the book with Ghost Writer 1.8.0 or later, open Claude Code in the book's folder and run:

```
/ghost-writer:gallery
```

It drafts the entry with you (title, genres, short description, links, cover), checks it against the rules below and, after your OK, opens the pull request with the GitHub CLI — or, without it, gives you a pre-filled link to the form.

## With the form

1. Click **Submit your project** on [claudeghostwriter.com/books](https://claudeghostwriter.com/books/), or open a new issue with the **Add my book to the gallery** template.
2. Fill in the fields and drag the cover image into the *Cover image* field.
3. The maintainer reviews the request and adds the `approved` label: a pull request with your book is created automatically (`.github/workflows/book-from-issue.yml`).
4. When the pull request is merged, the site updates within a few minutes and the issue is closed.

If something is wrong (missing field, invalid link, cover too large) the bot comments on the issue: edit it and it will be approved again.

## With a pull request

Fork the repository, add the folder `content/books/<your-book-slug>/` and open a pull request; fill in the checklist in the template.

## From the command line

```bash
hugo new books/my-book/index.md
```

Edit the file, add the cover, then check it:

```bash
pip install pyyaml
python3 scripts/validate_books.py
hugo server
```

## Fields

| Field | Required | Notes |
|---|---|---|
| `title` | yes | |
| `author` | yes | |
| `genres` | yes | list: `essay`, `fiction`, `manual`, `biography`, `fable`, `childrens-book` |
| `description` | yes | max 300 characters, shown on the card |
| `links` | yes | list of `{label, url}`, full `https://` URLs |
| `language` | no | e.g. `en`, `it` |
| `year` | no | |
| `date` | no | newest first in the gallery |

The text below the front matter is shown on the book page (Markdown).

Every pull request is checked automatically (fields, links, cover size, site build). The maintainer reviews and merges; the site updates a few minutes later.
