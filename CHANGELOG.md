# Changelog

## 1.100 — 2026-10-31

Fixes found by an automated audit (`src/audit.py`) and by testing on a live website.

- **Larger Persian bodies.** Letter bodies (س، ب، م…) were only ~0.2 em tall next to a 0.68 em alef, so text looked tiny and loose at 14–16 px. Bodies are now ~0.32 em, in line with common Persian web fonts; letters are wider and side bearings tighter.
- **Final yeh (ـی) redrawn.** It looked like the tail of س/ن, so «عکاسی» read like «عکاس». It now has a diagonal entry and a wide bowl with the tail rising on the left.
- **Latin digits 0–9** at the same height as Persian digits, and missing ASCII punctuation: `| [ ] _ * < > ~ \ # ?` plus `… • ×`. Previously the browser fell back to another font for these.
- **OTF** files added next to TTF, WOFF and WOFF2.
- **CDN**: `fonts.css` loads both families; CSS now also lists the TTF fallback.
- Ghorbanali font files were missing from the GitHub folder; they are now included.
- Audit and build run in CI on every push.

Checked and found correct (no change needed): contextual forms of every letter in real sentences follow Unicode joining types, joins have no gaps, ZWNJ breaks joins. ALEF MAKSURA (U+0649) is dual-joining in Unicode (ArabicShaping.txt, type D), so sharing the dotless-yeh forms is correct.

## 1.000 — 2026-10-27

First release.
