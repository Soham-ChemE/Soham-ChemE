# QA for the live page

Served from docs/ by docs/tools/page-qa.mjs (node) or docs/tools/hero_shapes.py (Python Playwright), loaded in headless Chromium (software WebGL, so frame timing is not representative). Screenshots in both themes: the hero at the top and scrolled to its last project, the first two body scenes, the ALD card thumbnail, the 375 px hero.

## index.html

Lighthouse (desktop preset): performance 98, accessibility 96, best practices 100, SEO 100

| Metric | Value |
|---|---|
| First Contentful Paint | 0.8 s |
| Largest Contentful Paint | 0.9 s |
| Speed Index | 1.2 s |
| Total Blocking Time | 50 ms |
| Cumulative Layout Shift | 0 |
| Total byte weight | Total size was 431 KiB |

| Theme | Console errors | Failed requests | Images loaded | Transfer (bytes) | Body scenes captured |
|---|---|---|---|---|---|
| dark | 0 | 0 | 0/0 | 530,574 | ald, cathodeai |
| light | 0 | 0 | 0/0 | 530,574 | ald, cathodeai |

Hero scrolled to its end (dark): focus panel `14.05 s`, panel in focus true, readout "ALD chamber-to-feature model, OpenFOAM · 7 of 7 · open the live page", scroll progress 1.
Hero scrolled to its end (light): focus panel `14.05 s`, panel in focus true, readout "ALD chamber-to-feature model, OpenFOAM · 7 of 7 · open the live page", scroll progress 1.

Files: `light/` and `dark/` hold `index-hero.png` (hero at the top of the page), `index-hero-end.png` (hero scrolled to the last project), `index-scene1-*.png`, `index-scene2-*.png`, `index-card-ald.png` (the ALD card thumbnail) and `index-mobile-375-hero.png`; `lighthouse.report.html` and `.json` are the Lighthouse run (round 3, not re-run in round 4); `qa.json` is the machine-readable summary.
