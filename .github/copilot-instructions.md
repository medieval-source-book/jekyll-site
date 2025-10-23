Repository: medieval-source-book.github.io

Purpose
- This repository is a Jekyll-based static site for a medieval sources project (derived from the Digital Humanities Literacy Guidebook repo). The site is built and served with Bundler + Jekyll; production builds use `bundle exec jekyll build` and preview with `bundle exec jekyll serve`.

Top-level quick facts for an AI coding agent
- Language/tech: Ruby, Jekyll, Liquid templates, SCSS, YAML, Markdown
- Entry points: `_layouts/` (page templates), `_includes/` (shared partials), `_data/` (site data), `_sass/` (styles), content in root and `_texts`, `_periods`, `_regions`, `_genres` directories.
- Local preview command: `bundle exec jekyll serve --watch --config _config.yml,_config_local.yml`
- Build + link-checking: `bundle exec jekyll build --config _config.yml,_config_local.yml` then `bundle exec htmlproofer ./_site --assume-extension --empty-alt-ignore --timeframe '30d' --allow-hash-href`

What to focus on when making changes
- Respect Jekyll/Liquid conventions used across `_layouts` and `_includes`; many templates rely on specific YAML front-matter fields (e.g., `identifier`, `meta_title`, `title`, `permalink`, `creationdate`, `date_updated`). See README.md for required fields when adding pages.
- Navigation is driven by `_data/navigation.yml` and `_data/disciplines.yml`; when adding new top-level pages or disciplines update these files.
- Content directories (e.g., `_periods/`, `_regions/`, `_genres/`) contain markdown files with front-matter used to populate listing pages—follow existing identifier/permalink conventions.
- Styling lives in `_sass/` with ordered partials (`_01_...` through `_10_...`)—don't reorder unless you know the cascade impact.

Patterns and examples an agent should use
- Page templating: pages typically set `layout: page` or `layout: project` in front-matter and rely on `_layouts/page.html` or `_layouts/project.html`. When editing templates, search `_includes` for helper fragments like `_navigation.html`, `_masthead.html`, and `_text-metadata.html`.
- Adding a new page: copy an existing page in the appropriate directory, update required YAML fields (identifier, meta_title, title, permalink, creationdate, date_updated). Then add a navigation entry in `_data/navigation.yml` so it appears in menus.
- Adding a discipline/topic: update `_data/disciplines.yml` or relevant `_data` files. Disciplines must use a lowercase `identifier` string to match across project pages.

Developer workflows and commands
- Install dependencies:
  - `gem install bundler`
  - `bundle install`
- Local preview (watch mode):
  - `bundle exec jekyll serve --watch --config _config.yml,_config_local.yml`
- One-off build (for link checking):
  - `bundle exec jekyll build --config _config.yml,_config_local.yml`
  - `bundle exec htmlproofer ./_site --assume-extension --empty-alt-ignore --timeframe '30d' --allow-hash-href`
- CI: see `.github/workflows/jekyll.yml` for how GitHub Actions builds the site; mimic those steps locally for parity.

Project-specific conventions and gotchas
- Identifiers: front-matter `identifier` must be lowercase letters only, cannot start with a digit, and contain no spaces. This is enforced by site templates and navigation matching.
- Permalinks: must end with a trailing slash `/` and be lowercase; these affect breadcrumb generation.
- Data-driven lists: many pages and landing lists are populated from `_data` YAML files—changes there can affect many pages site-wide.
- HTML proofer options used in README (allow-hash-href, assume-extension) indicate the site uses in-page anchors and extensionless URLs—avoid changing link formats without running the link-checker.
- Avoid moving Sass partials out of the numeric ordering in `_sass/`—the numbers indicate intended load order.

Integration points and external dependencies
- Bundler-managed Ruby gems as declared in `Gemfile` (run `bundle install` to match CI). Do not hard-upgrade gems without checking CI `.github/workflows/jekyll.yml`.
- `htmlproofer` is used for link checking during local checks and CI.
- Theme: based on Feeling Responsive (see README) — layout/partials may follow that theme's conventions.

When making PRs (code/markup changes)
- Run `bundle exec jekyll build` and `htmlproofer` locally to catch link and build regressions before opening a PR.
- For content changes, include the required front-matter fields and update `_data/navigation.yml` when adding new pages intended for the nav.
- When editing templates or Sass, verify the site renders locally (`jekyll serve`) and visually inspect key pages: frontpage, a genre page (e.g., `_genres/canso.md`), and a text page under `_texts`.

Files to inspect when debugging a layout or content issue
- `_layouts/page.html`, `_layouts/text.html`, `_includes/_navigation.html`, `_includes/_masthead.html`, `_data/navigation.yml`, `_sass/_01_settings_colors.scss`, `_sass/_06_typography.scss`.

If you need more detail
- Ask for specific areas to expand: templates, data files, SCSS, or CI steps. Provide a short reproduction case (file changed + expected vs actual) and I will update the instructions or make a targeted fix.

---
Please review this draft and tell me which sections you want expanded, merged differently, or rewritten. I can also merge it with existing custom instructions if you provide them.