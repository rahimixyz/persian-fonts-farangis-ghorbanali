# Changelog

## 1.200 — 2026-10-31

- **More weights.** Ghorbanali: Light 300, Regular 400, Medium 500, SemiBold 600, Bold 700, ExtraBold 800. Farangis: Medium 500, SemiBold 600, Bold 700, ExtraBold 800, Black 900. New weights are generated from the same skeletons with stroke width, spacing and proportions interpolated between the drawn masters. `ghorbanali.css` and `farangis.css` define every weight.
- **Same line spacing in every weight** of a family: typo/hhea metrics come from the reference weight, win metrics cover the tallest glyph of all weights (no clipping on Windows).
- **Kerning** (`kern` feature): optical kerning for letters that meet without joining («را»، «ورود»، «زن»…), measured from the outlines and pulled towards the alef+alef reference distance. It never makes letters touch.
- **Diacritics:** dammatan is more compact, so it no longer collides with a shadda on the neighbouring letter in the heavy weights. The audit now checks stacked and neighbouring marks for collisions.
- **ALEF MAKSURA (ى) initial and medial forms are now dotless.** In 1.100 they reused the Persian yeh forms, which have two dots. (ARABIC YEH ي keeps its two dots in every form, as it should.)
- **Test page** (`index.html`): live weight, size, line-height and word-spacing controls, side-by-side comparison with Vazirmatn or Tahoma, all weights, character set, and diacritics samples.

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
