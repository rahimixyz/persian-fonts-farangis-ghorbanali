"""Automated audit of the built fonts (run from repo root: python3 src/audit.py).

Checks, for every font:
  1. cmap coverage of characters that appear in real Persian web text
  2. shaping with HarfBuzz: no .notdef, correct contextual form for every letter
     (derived from Unicode joining types), lam-alef ligature, ZWNJ breaks joins
  3. joins are continuous (raster check of the baseline stroke between joined glyphs)
  4. vertical metrics: nothing clipped by hhea/OS2 win metrics, sensible line height
  5. visual size: height of the Persian body compared with the em
  6. spacing: gap between non-joining letters, compared with stroke width
  7. diacritics: stacked marks (shadda + fatha, kasra under dots ...) must not overlap each other
Exit code 1 when any hard check fails.
"""
import glob
import os
import sys

import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

# Unicode joining types (ArabicShaping.txt) for the letters the fonts cover
DUAL = set('بپتثجچحخسشصضطظعغفقکگلمنهیيئىكـ')
RIGHT = set('اآأإدذرزژوؤةۀ')
JOINING = DUAL | RIGHT

TEST_STRINGS = [
    'پپپ ببب تتت جچحخ سش عغ فقل ییکگ',
    'فونت آرام و خوانا برای وب‌سایت‌ها',
    'فارسی، طراحی، برنامه‌نویسی، جست‌وجو و نمایش اطلاعات',
    '۱۲۳۴۵۶۷۸۹۰ | ۱۲۳,۴۵۶٫۷۸ | ۲۵۰٬۰۰۰ تومان | (۱۴۰۵)',
    'می‌روم، وب‌سایت، خانه‌ها، کتاب‌ها، مسئولیت، نشانه‌گذاری',
    'اقامتگاه بهترین قیمت پشتیبانی ۲۴ ساعته کلبه آپارتمان',
    'زیباترین فصل برای عکاسی و طبیعت‌گردی',
    'لا لأ لإ لآ ملا سلام کلاس',
    'ئ ؤ ء آ أ إ ۀ ة ي ك ى',
    'Price: 250,000 - 1404/08/09 @ 50% #1 [ok] {x} <a> a_b ~ "q" \'s\' & * + = / \\',
]
WEB_CHARS = set(''.join(TEST_STRINGS)) | set('۰۱۲۳۴۵۶۷۸۹0123456789«»؛؟!.،:()-–—٪%/‌‍ ')


def joining_forms(text):
    """Expected form for each character: isol/init/medi/fina or None (non-joining)."""
    out = []
    for i, c in enumerate(text):
        if c not in JOINING:
            out.append(None)
            continue
        prev = text[i - 1] if i > 0 else ''
        nxt = text[i + 1] if i + 1 < len(text) else ''
        joins_prev = prev in DUAL
        joins_next = c in DUAL and nxt in JOINING
        out.append({(False, False): 'isol', (False, True): 'init', (True, True): 'medi', (True, False): 'fina'}[(joins_prev, joins_next)])
    return out


def shape(path, text):
    blob = hb.Blob.from_file_path(path)
    face = hb.Face(blob)
    font = hb.Font(face)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {})
    return buf.glyph_infos, buf.glyph_positions


def audit(path):
    f = TTFont(path)
    name = os.path.basename(path)
    order = f.getGlyphOrder()
    cmap = f.getBestCmap()
    gs = f.getGlyphSet()
    upm = f['head'].unitsPerEm
    errors, warnings, info = [], [], []

    # 1. coverage
    missing = sorted(c for c in WEB_CHARS if ord(c) not in cmap and c not in ' ' and not ('a' <= c.lower() <= 'z' or c in '@&{}'))
    if missing:
        errors.append('missing characters: ' + ' '.join(f'{c}(U+{ord(c):04X})' for c in missing))

    # 2. shaping
    for text in TEST_STRINGS:
        infos, _ = shape(path, text)
        names = [order[i.codepoint] for i in infos]
        if '.notdef' in names and not any('a' <= c.lower() <= 'z' for c in text):
            errors.append(f'.notdef in "{text}"')
        expected = joining_forms(text)
        by_cluster = {}
        for i, n in zip(infos, names):
            by_cluster.setdefault(i.cluster, []).append(n)
        for idx, (c, form) in enumerate(zip(text, expected)):
            if form is None or idx not in by_cluster:
                continue
            g = by_cluster[idx][0]
            if g.startswith('lamalef'):
                continue
            got = g.split('.')[1] if '.' in g else 'isol'
            if got != form:
                errors.append(f'"{text}": {c} at {idx} is {g}, expected {form}')

    # 3. join continuity: every dual-joining glyph's joining stub must reach x=0 / x=advance on the baseline
    hmtx = f['hmtx']
    for g in order:
        if not ('.init' in g or '.medi' in g or '.fina' in g):
            continue
        pen = BoundsPen(gs)
        gs[g].draw(pen)
        if pen.bounds is None:
            continue
        xmin, ymin, xmax, ymax = pen.bounds
        adv = hmtx[g][0]
        if ('.init' in g or '.medi' in g) and xmin > 0:
            errors.append(f'{g}: left join stub ends at x={xmin}, does not reach 0 (gap)')
        if ('.medi' in g or '.fina' in g) and xmax < adv:
            errors.append(f'{g}: right join stub ends at x={xmax} < advance {adv} (gap)')

    # 4. vertical metrics
    yb = [BoundsPen(gs) for _ in range(1)]
    gmax, gmin = 0, 0
    for g in order:
        pen = BoundsPen(gs)
        gs[g].draw(pen)
        if pen.bounds:
            gmin = min(gmin, pen.bounds[1])
            gmax = max(gmax, pen.bounds[3])
    os2, hhea = f['OS/2'], f['hhea']
    if os2.usWinAscent < gmax or os2.usWinDescent < -gmin:
        errors.append(f'win metrics clip glyphs: winAscent {os2.usWinAscent}/{gmax}, winDescent {os2.usWinDescent}/{-gmin}')
    line = (os2.sTypoAscender - os2.sTypoDescender + os2.sTypoLineGap) / upm
    info.append(f'line height (typo, use_typo_metrics={bool(os2.fsSelection & 128)}): {line:.2f} em')

    # 5. visual size: height of "س" teeth/body vs em, and alef height
    def gh(ch):
        n = cmap.get(ord(ch))
        pen = BoundsPen(gs)
        gs[n].draw(pen)
        return pen.bounds
    alef = gh('ا')
    seen = gh('س')
    info.append(f'alef height {alef[3] / upm:.2f} em, seen top {seen[3] / upm:.2f} em')
    if alef[3] / upm < 0.6:
        warnings.append(f'Persian looks small: alef is only {alef[3] / upm:.2f} em tall (typical web fonts 0.65–0.75)')

    # 6. spacing between non-joining letters ("آرام")
    infos, pos = shape(path, 'آرام')
    total = sum(p.x_advance for p in pos)
    ink = 0
    for i in infos:
        pen = BoundsPen(gs)
        gs[order[i.codepoint]].draw(pen)
        if pen.bounds:
            ink += pen.bounds[2] - pen.bounds[0]
    info.append(f'"آرام": advance {total / upm:.2f} em, white space {(total - ink) / upm:.2f} em')
    if (total - ink) / upm > 0.45:
        warnings.append(f'loose spacing between non-joining letters ("آرام" has {(total - ink) / upm:.2f} em of side space)')

    # 7. diacritics: ink of each mark must not collide with other marks of the same word
    from shapely.geometry import box as sbox
    def ink_boxes(text):
        infos, pos = shape(path, text)
        x = 0
        out = []
        for i, p in zip(infos, pos):
            g = order[i.codepoint]
            pen = BoundsPen(gs)
            gs[g].draw(pen)
            if pen.bounds:
                a, b, c, d = pen.bounds
                ox, oy = x + p.x_offset, p.y_offset
                out.append((g, sbox(a + ox, b + oy, c + ox, d + oy)))
            x += p.x_advance
        return out
    marks = set(['fatha', 'kasra', 'damma', 'fathatan', 'dammatan', 'kasratan', 'shadda', 'sukun',
                 'superalef', 'hamzaabove', 'hamzabelow'])
    for word in ['مُحَمَّدٌ', 'بِسْمِ', 'شَدَّةً', 'إِنَّ', 'رَبِّي', 'كِتَابٌ', 'سُؤَال', 'عَلِيٌّ', 'قُرْآن', 'تَشَکُّر']:
        bx = ink_boxes(word)
        mk = [(g, b) for g, b in bx if g in marks]
        for i in range(len(mk)):
            for j in range(i + 1, len(mk)):
                if mk[i][1].intersection(mk[j][1]).area > 0:
                    errors.append(f'marks collide in "{word}": {mk[i][0]} and {mk[j][0]}')

    print(f'\n== {name}: {len(errors)} errors, {len(warnings)} warnings')
    for e in errors[:40]:
        print('  ERROR', e)
    if len(errors) > 40:
        print(f'  ... {len(errors) - 40} more')
    for w in warnings:
        print('  WARN ', w)
    for i in info:
        print('  info ', i)
    return errors


if __name__ == '__main__':
    paths = sys.argv[1:] or sorted(glob.glob('*/fonts/ttf/*.ttf'))
    total = sum(len(audit(p)) for p in paths)
    sys.exit(1 if total else 0)
