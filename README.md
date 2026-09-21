# From Pattern to Mind

A single-page essay + interactive concept map on how structure becomes stable, alive, felt, and selected.

- `index.html` — the essay (self-contained; uses `fptm-assets/`).
- `fptm-assets/` — diagram-section background images (WebP).
- `gen_diagram.py` — regenerates the inline SVG concept map.
- `en.json`, `uk.json`, `ru.json` — all page text per language; `diagram.json` — map labels.
- `build_i18n.py` — writes the JSON text into `index.html` and `i18n.js`. Edit the JSON, then run it.
- `test_revision.py` — checks key parity, HTML fragments, sources and build reproducibility.
