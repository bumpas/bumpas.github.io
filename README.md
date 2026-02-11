<h1 align="center">Bumpas — Portfolio & Blog</h1>
<p align="center">Personal site of Andrew Bumpas. Built with Astro, tailored for portfolio case studies, photography, and writing.</p>

<p align="center">
  <img src="https://img.shields.io/static/v1?label=Astro&message=5.14&color=000&logo=astro" alt="Astro v5.14" />
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License" />
</p>

---

## Overview

This repo powers <a href="https://bumpas.github.io" target="_blank" rel="nofollow">bumpas.github.io</a>, a static site for:

- Portfolio posts (case studies like Okra Design System)
- Blog articles
- Photography gallery
- Contact and About pages

The site uses Astro 5, Tailwind CSS (v4), MDX, auto-imported shortcodes, and image optimization via `astro:assets`.

## Quick start

Prereqs:

- Node.js (LTS recommended)
- npm

Install and run:

```
npm install
npm run dev
```

Build and preview:

```
npm run build
npm run preview
```

## Content model

Content collections are defined in `src/content.config.ts`:

- `homepage` → `src/content/homepage/-index.md`
- `about` → `src/content/about/-index.md`
- `posts` → `src/content/posts/**` (supports nested folders)
- `pages` → `src/content/pages/**`
- `authors` → `src/content/authors/**`
- `contact` → `src/content/contact/**`
- `photography` → `src/content/photography/-index.md`

### Posts

Frontmatter fields for posts:

- `title` (string)
- `meta_title` (optional)
- `description` (optional)
- `date` (Date)
- `image` (optional, path under `public/images/...`)
- `authors` (string[]; default `admin`) — preferred over single `author`
- `categories` (string[]; default `others`) — use `Portfolio` for case studies
- `tags` (string[]; default `others`)
- `draft` (optional boolean)

Slugs/paths are derived from file location. Nested paths are supported, e.g. `src/content/posts/okra-design-system/okra.mdx` → `/posts/okra-design-system/okra`.

### Photography

Photos are managed in the `photography` collection and displayed via a responsive grid. Images live under `public/images/photography`.

## Homepage highlights

- Banner content from `homepage/-index.md`.
- Portfolio section renders up to the latest 3 posts in the `Portfolio` category in a grid (`PortfolioGrid`).

## Shortcodes (MDX)

Auto-imported components for MD/MDX:

- `Button`, `Accordion`, `Notice`, `Video`, `Youtube`

Use them directly in MDX without import statements.

## Styling

- Tailwind CSS v4 via Vite plugin
- Custom theme utilities in `tailwind-plugin/`
- Global styles under `src/styles/`

## Images

- Put assets under `public/images/...`
- Use `astro:assets` `Image` for optimized output (webp/avif), as done in layouts/partials and components.

## Resume (ATS) PDF generation

This repo includes an ATS-friendly resume generator (plain text + light layout).

Output location: `Andrew-Bumpas-Resume-ATS.pdf`

Generate the PDF:

```
python3 scripts/generate_resume_pdf.py
```

Or via npm:

```
npm run resume
```

Optional (first time): install ReportLab if needed:

```
python3 -m pip install --user reportlab
```

CLI & env controls:

```
# CLI flags
python3 scripts/generate_resume_pdf.py \
  --source /absolute/path/to/-index.md \
  --start-line 14 \
  --header "ANDREW BUMPAS"

# Or environment variables
ATS_SOURCE_MD=/absolute/path/to/-index.md ATS_START_LINE=14 ATS_HEADER="ANDREW BUMPAS" \
  python3 scripts/generate_resume_pdf.py
```

By default, the generator reads from `src/content/about/-index.md` starting at line 14.

## Deployment

This site builds to static HTML in `dist/`.

Typical options:

- GitHub Pages — serve from the `dist` output or use Astro’s guide: https://docs.astro.build/en/guides/deploy/github/
- Any static hosting (Netlify, Vercel, etc.) — upload `dist/` or connect repo and configure build: `npm run build`.

Site metadata (title, base URL, meta image) lives in `src/config/config.json`. A sitemap is generated via `@astrojs/sitemap`.

## License

MIT
