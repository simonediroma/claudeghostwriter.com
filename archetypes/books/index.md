---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
author: ""
genres: []          # one or more: essay, fiction, manual, biography, fable, childrens-book
language: en
year: {{ now.Year }}
date: {{ .Date }}
description: ""     # max 300 characters, shown on the card
links:
  - label: ""
    url: ""
---
Write a longer description here (Markdown). Optional: how you used Ghost Writer.
