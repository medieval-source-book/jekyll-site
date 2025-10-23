---
title: Medieval Source Book (11ty port)
layout: layout.njk
---

This is a minimal Eleventy port of the medieval-source-book Jekyll site. It is intended as a starting point for migrating templates and assets.

Key notes:

- Styles are sourced from the repository's `_sass/` directory and compiled with `sass` to `./dist/css`.
- Static assets are copied from the repository `assets/` and `html/` directories.

To run locally, from the `11ty/` directory run:

```bash
npm install
npm start
```
