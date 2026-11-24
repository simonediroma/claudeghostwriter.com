# Add your book to the gallery

Books are added with a pull request. Each book is one folder:

```
content/books/my-book/
  index.md      required
  cover.jpg     optional — 2:3 ratio, max 2 MB (.jpg, .png or .webp)
```

## From the browser (no tools needed)

1. Click **Submit your project** on [claudeghostwriter.com/books](https://claudeghostwriter.com/books/) — GitHub opens a new `index.md` prefilled with the template, in your fork.
2. Rename the path to `content/books/<your-book-slug>/index.md`, fill in the fields, then **Propose changes**.
3. Optional cover: in your fork, open the same folder, **Add file → Upload files**, upload `cover.jpg` on the same branch.
4. **Create pull request** and fill in the checklist.

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
