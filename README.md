# Sanhita Atlas

An independent research platform for the **Bharatiya Nyaya Sanhita, 2023** — the code that replaced the
Indian Penal Code on 1 July 2024.

- **358 sections, 20 chapters** — the full structure, with exact section ranges
- **Section index** — searchable, filterable by chapter
- **IPC → BNS mapping** — 39 provisions and where they landed
- **What changed** — the 20 new offences, the 19 provisions dropped, the penalties that moved
- **Companion codes** — BNSS (procedure) and BSA (evidence)

## Stack

Static HTML and CSS, no build runtime.

| Layer | Choice |
| --- | --- |
| Styling | Hand-written CSS design system + Tailwind base/utilities |
| Interactivity | [Alpine.js](https://alpinejs.dev) 3 |
| Search | [Fuse.js](https://fusejs.io) over a static JSON index |
| Charts | [Chart.js](https://www.chartjs.org) |
| Type | Sora, Public Sans, JetBrains Mono |

## Structure

```
index.html              platform home
bns/                    the Sanhita — overview, chapters, sections, mapping, changes, punishments
procedure/              BNSS and BSA
research/               methodology and sources
about.html              404.html
assets/css/app.css      compiled stylesheet
assets/js/app.js        Alpine components
assets/data/search.json search index
```

## Local development

```bash
npm install
python3 build.py                       # generate HTML into dist/
npx tailwindcss -i src/app.css -o dist/assets/css/app.css --minify
python3 -m http.server -d dist 8000
```

## Licence

MIT. The statutory text it indexes is published by the Government of India and is not claimed by this project.
Not legal advice.
