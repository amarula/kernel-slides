# Kernel development slides

## Purpose

The purpose of these slides is to provide some notes to newcomers to kernel
development. As approaching the Linux kernel development is difficult, we aim to
simplify the procedure.

## Technology

We use [slidev](https://github.com/slidevjs/slidev) for writing our slides. This
allows us to have a common template, to be able to export slides in a very fast
way and to review them as text, allowing us to use git to correct us without
doing it "the old way" (not as old as saving them on ~~floppy disks~~ USB
devices and passing them around).

## Requirements

- Node.js 20 or newer
- npm
- Playwright Chromium for PDF/PNG export (installed once, see below)

## Install

```bash
npm install
```

## Deck layout

The main deck is `kernel/linux-kernel/linux-kernel.md`; the chapters live in
`kernel/linux-kernel/slides/`. The npm scripts already point to the main entry
file, so no path is needed on the command line.

## Preview the slides

```bash
npm run dev
```

Then open <http://localhost:3030>.

## Build the static site

```bash
npm run build
```

The generated site is written to `dist/` and is what the Netlify/Vercel
configurations deploy.

## Export to PDF

PDF export is powered by Playwright. Install the browser once:

```bash
npx playwright install chromium
```

Then export the deck:

```bash
npm run export
```

This creates `linux-kernel-export.pdf` in the repository root. To choose the
output path:

```bash
npm run export -- --output kernel/linux-kernel/linux-kernel.pdf
```

Export only a range of slides, or use another format:

```bash
npm run export -- --range "1-10"
npm run export -- --format png --output /tmp/slides-png
```

Useful export options:

- `--output <path>` — output file (PDF/PPTX) or directory (PNG)
- `--range "1,4-6"` — selected slides
- `--format pdf|png|pptx` — output format (default: `pdf`)
- `--with-clicks` — one page per click animation
- `--dark` — export with the dark theme
- `--per-slide` — render slide by slide (may break cross-slide links and the TOC)

Generated PDFs and the `dist/` directory are build artifacts and are not
committed.
