"""Build Farangis and Ghorbanali font files (TTF + WOFF2 + WOFF)."""
import os
import sys
from shapely.geometry import box
from shapely.geometry.polygon import orient
from shapely import affinity
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.ttLib import TTFont

sys.path.insert(0, os.path.dirname(__file__))
from letters import Style, build_forms  # noqa: E402
from geom import to_polys  # noqa: E402

VERSION = '1.000'
AUTHOR = 'Alireza Rahimi'
AUTHOR_FA = 'علیرضا رحیمی'
YEAR = 2026
OV = 8  # overlap at joins, hides anti-aliasing seams


def style(name, **kw):
    return Style(name=name, **kw)


STYLES = {
    # ---- Ghorbanali: calm, rounded, open text face for websites
    'Ghorbanali-Regular': style('Ghorbanali-Regular', family='Ghorbanali', family_fa='قربانعلی', sub='Regular',
                                weight=400, sw=80, G=104, A=640, Ak=590, T=210, D=-290, H=330, C=150,
                                R=110, RL=150, cap='round', join='round', dot=104, dotshape='diamond', dg=56,
                                sb=50, kafstyle='curve', Hn=520, dw=300, space=240),
    'Ghorbanali-Bold': style('Ghorbanali-Bold', family='Ghorbanali', family_fa='قربانعلی', sub='Bold',
                             weight=700, sw=124, G=112, A=650, Ak=600, T=225, D=-290, H=340, C=150,
                             R=110, RL=150, cap='round', join='round', dot=140, dotshape='diamond', dg=56,
                             sb=46, kafstyle='curve', Hn=530, dw=330, space=240),
    # ---- Farangis: heavy geometric display face for posters and billboards
    'Farangis-Bold': style('Farangis-Bold', family='Farangis', family_fa='فرنگیس', sub='Bold',
                           weight=700, sw=130, G=118, A=620, Ak=640, T=245, D=-270, H=340, C=150,
                           R=14, RL=36, cap='flat', join='mitre', dot=140, dotshape='square', dg=50,
                           sb=44, kafstyle='kufi', Hn=540, dw=350, space=230),
    'Farangis-Black': style('Farangis-Black', family='Farangis', family_fa='فرنگیس', sub='Black',
                            weight=900, sw=176, G=134, A=640, Ak=665, T=270, D=-270, H=360, C=150,
                            R=16, RL=40, cap='flat', join='mitre', dot=180, dotshape='square', dg=54,
                            sb=46, kafstyle='kufi', Hn=560, dw=400, space=230),
}

CMAP = {
    'alef': [0x627], 'alefmadda': [0x622], 'alefhamza': [0x623], 'alefhamzabelow': [0x625], 'hamza': [0x621],
    'beh': [0x628], 'peh': [0x67E], 'teh': [0x62A], 'theh': [0x62B], 'jeem': [0x62C], 'tcheh': [0x686],
    'hah': [0x62D], 'khah': [0x62E], 'dal': [0x62F], 'thal': [0x630], 'reh': [0x631], 'zain': [0x632],
    'jeh': [0x698], 'seen': [0x633], 'sheen': [0x634], 'sad': [0x635], 'dad': [0x636], 'tah': [0x637],
    'zah': [0x638], 'ain': [0x639], 'ghain': [0x63A], 'feh': [0x641], 'qaf': [0x642], 'keheh': [0x6A9, 0x643],
    'gaf': [0x6AF], 'lam': [0x644], 'meem': [0x645], 'noon': [0x646], 'waw': [0x648], 'wawhamza': [0x624],
    'heh': [0x647], 'tehmarbuta': [0x629], 'yeh': [0x6CC], 'yehar': [0x64A], 'alefmaksura': [0x649],
    'yehhamza': [0x626], 'hehyeh': [0x6C0], 'tatweel': [0x640],
    'period': [0x2E, 0x6D4], 'colon': [0x3A], 'exclam': [0x21], 'questionar': [0x61F], 'commaar': [0x60C],
    'semicolonar': [0x61B], 'guillemetleft': [0xAB], 'guillemetright': [0xBB], 'parenleft': [0x28],
    'parenright': [0x29], 'hyphen': [0x2D], 'slash': [0x2F], 'percentar': [0x66A, 0x25], 'plus': [0x2B],
    'equal': [0x3D], 'endash': [0x2013], 'emdash': [0x2014], 'comma': [0x2C], 'semicolon': [0x3B],
    'thousandsar': [0x66C], 'decimalar': [0x66B], 'quotedbl': [0x22], 'quotesingle': [0x27],
    'fatha': [0x64E], 'kasra': [0x650], 'damma': [0x64F], 'fathatan': [0x64B], 'dammatan': [0x64C],
    'kasratan': [0x64D], 'shadda': [0x651], 'sukun': [0x652], 'superalef': [0x670], 'hamzaabove': [0x654],
    'hamzabelow': [0x655],
}
for i in range(10):
    CMAP['digit%d' % i] = [0x6F0 + i, 0x660 + i]

TOP_MARKS = ['fatha', 'fathatan', 'damma', 'dammatan', 'shadda', 'sukun', 'superalef', 'hamzaabove']
BOT_MARKS = ['kasra', 'kasratan', 'hamzabelow']
LIGS = ['lamalef', 'lamalefmadda', 'lamalefhamza', 'lamalefhamzabelow']


def geom_to_glyph(g):
    pen = TTGlyphPen(None)
    for poly in to_polys(g):
        poly = orient(poly, sign=-1.0)  # exterior clockwise (TrueType)
        rings = [poly.exterior] + list(poly.interiors)
        for ring in rings:
            pts = [(round(x), round(y)) for x, y in ring.coords[:-1]]
            # drop consecutive duplicates after rounding
            clean = []
            for pt in pts:
                if not clean or clean[-1] != pt:
                    clean.append(pt)
            if len(clean) > 1 and clean[0] == clean[-1]:
                clean.pop()
            if len(clean) < 3:
                continue
            pen.moveTo(clean[0])
            for pt in clean[1:]:
                pen.lineTo(pt)
            pen.closePath()
    return pen.glyph()


def realise(S, F):
    """Turn skeleton forms into positioned geometry + advance widths."""
    out = {}
    hs = S.sw / 2
    for name, f in F.items():
        g = f.pen.geometry().simplify(0.6, preserve_topology=True)
        if f.jl:
            g = g.difference(box(-1e4, -hs - 4, -OV, hs + 4))
        if f.jr:
            g = g.difference(box(f.W + OV, -hs - 4, 1e4, hs + 4))
        minx, miny, maxx, maxy = g.bounds
        if f.kind in ('mark_above', 'mark_below'):
            cx = (minx + maxx) / 2
            dy = -miny if f.kind == 'mark_above' else -maxy
            g = affinity.translate(g, -cx, dy)
            out[name] = (g, 0, f.kind)
            continue
        if f.kind == 'digit':
            adv = S.dw + 2 * S.sb + S.sw * 0.6
            cx = (minx + maxx) / 2
            g = affinity.translate(g, adv / 2 - cx, 0)
            out[name] = (g, round(adv), 'base')
            continue
        left = 0 if f.jl else minx - S.sb
        right = f.W if f.jr else maxx + S.sb
        g = affinity.translate(g, -left, 0)
        out[name] = (g, round(right - left), 'lig' if name.split('.')[0] in LIGS else 'base')
    return out


def feature_code(names):
    dual, right = [], []
    for n in names:
        if '.' in n:
            continue
        if n + '.init' in names and n + '.medi' in names and n + '.fina' in names:
            dual.append(n)
        elif n + '.fina' in names and n not in LIGS:
            right.append(n)
    fea = ['languagesystem DFLT dflt;', 'languagesystem arab dflt;', 'languagesystem arab FAR;',
           'languagesystem arab URD;']
    fea.append('feature init { sub [%s] by [%s]; } init;' % (' '.join(dual), ' '.join(d + '.init' for d in dual)))
    fea.append('feature medi { sub [%s] by [%s]; } medi;' % (' '.join(dual), ' '.join(d + '.medi' for d in dual)))
    fina = dual + right
    fea.append('feature fina { sub [%s] by [%s]; } fina;' % (' '.join(fina), ' '.join(d + '.fina' for d in fina)))
    rl = ['feature rlig {']
    for a, l in [('alef', 'lamalef'), ('alefmadda', 'lamalefmadda'), ('alefhamza', 'lamalefhamza'),
                 ('alefhamzabelow', 'lamalefhamzabelow')]:
        rl.append('  sub lam.init %s.fina by %s;' % (a, l))
        rl.append('  sub lam.medi %s.fina by %s.fina;' % (a, l))
    rl.append('} rlig;')
    fea += rl
    return '\n'.join(fea)


def mark_code(G, S):
    bases = [n for n, v in G.items() if v[2] in ('base', 'lig') and v[0] is not None and not v[0].is_empty]
    lines = []
    lines.append('markClass [%s] <anchor 0 0> @TOP;' % ' '.join(TOP_MARKS))
    lines.append('markClass [%s] <anchor 0 0> @BOT;' % ' '.join(BOT_MARKS))
    lines.append('feature mark {')
    gap = S.dg * 0.9
    for n in bases:
        g = G[n][0]
        minx, miny, maxx, maxy = g.bounds
        cx = round((minx + maxx) / 2)
        lines.append('  pos base %s <anchor %d %d> mark @TOP <anchor %d %d> mark @BOT;' % (
            n, cx, round(maxy + gap), cx, round(min(miny, -S.sw / 2) - gap)))
    lines.append('} mark;')
    lines.append('feature mkmk {')
    for n in TOP_MARKS:
        g = G[n][0]
        lines.append('  pos mark %s <anchor 0 %d> mark @TOP;' % (n, round(g.bounds[3] + gap * 0.7)))
    for n in BOT_MARKS:
        g = G[n][0]
        lines.append('  pos mark %s <anchor 0 %d> mark @BOT;' % (n, round(g.bounds[1] - gap * 0.7)))
    lines.append('} mkmk;')
    marks = TOP_MARKS + BOT_MARKS
    ligs = [n for n, v in G.items() if v[2] == 'lig']
    others = [n for n in bases if n not in ligs and n != '.notdef']
    lines.append('table GDEF { GlyphClassDef [%s], [%s], [%s], ; } GDEF;' % (
        ' '.join(others), ' '.join(ligs), ' '.join(marks)))
    return '\n'.join(lines)


def build(key, outdir):
    S = STYLES[key]
    F = build_forms(S)
    G = realise(S, F)
    order = ['.notdef', 'space', 'nbspace', 'zwnj', 'zwj', 'lrm', 'rlm'] + sorted(G.keys())
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(order)
    cmap = {0x20: 'space', 0xA0: 'nbspace', 0x200C: 'zwnj', 0x200D: 'zwj', 0x200E: 'lrm', 0x200F: 'rlm'}
    for n, cps in CMAP.items():
        for cp in cps:
            cmap[cp] = n
    fb.setupCharacterMap(cmap)
    glyphs, metrics = {}, {}
    # .notdef box
    nd = box(60, 0, 440, 640).difference(box(60 + S.sw * 0.6, S.sw * 0.6, 440 - S.sw * 0.6, 640 - S.sw * 0.6))
    glyphs['.notdef'] = geom_to_glyph(nd)
    metrics['.notdef'] = (500, 60)
    empty = TTGlyphPen(None).glyph()
    for n, w in [('space', S.space), ('nbspace', S.space), ('zwnj', 0), ('zwj', 0), ('lrm', 0), ('rlm', 0)]:
        glyphs[n] = empty
        metrics[n] = (w, 0)
    ymax, ymin = 0, 0
    for n, (g, adv, kind) in G.items():
        glyphs[n] = geom_to_glyph(g)
        lsb = round(g.bounds[0]) if not g.is_empty else 0
        metrics[n] = (adv, lsb)
        if not g.is_empty:
            ymax = max(ymax, g.bounds[3])
            ymin = min(ymin, g.bounds[1])
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    asc = round(ymax + 60)
    desc = round(ymin - 60)
    fb.setupHorizontalHeader(ascent=asc, descent=desc, lineGap=0)
    fam, sub = S.family, S.sub
    ribbi = sub in ('Regular', 'Bold')
    psname = '%s-%s' % (fam, sub)
    full = '%s %s' % (fam, sub) if sub != 'Regular' else fam
    copyright_ = 'Copyright %d %s. Licensed under the SIL Open Font License, Version 1.1.' % (YEAR, AUTHOR)
    names = {
        'copyright': copyright_,
        'familyName': fam if ribbi else '%s %s' % (fam, sub),
        'styleName': sub if ribbi else 'Regular',
        'uniqueFontIdentifier': '%s;%s;%s' % (VERSION, AUTHOR.replace(' ', ''), psname),
        'fullName': full,
        'version': 'Version %s' % VERSION,
        'psName': psname,
        'manufacturer': AUTHOR,
        'designer': AUTHOR,
        'description': S.desc if hasattr(S, 'desc') else '',
        'licenseDescription': 'This Font Software is licensed under the SIL Open Font License, Version 1.1. '
                              'This license is available with a FAQ at: https://openfontlicense.org',
        'licenseInfoURL': 'https://openfontlicense.org',
    }
    if not ribbi:
        names['typographicFamily'] = fam
        names['typographicSubfamily'] = sub
    fb.setupNameTable(names, mac=False)
    # Persian names (Windows, fa-IR = 0x0429)
    nt = fb.font['name']
    fa_full = S.family_fa if sub == 'Regular' else '%s %s' % (S.family_fa, {'Bold': 'ضخیم', 'Black': 'سیاه'}[sub])
    nt.setName(S.family_fa if ribbi else fa_full, 1, 3, 1, 0x0429)
    nt.setName(fa_full, 4, 3, 1, 0x0429)
    nt.setName(AUTHOR_FA, 9, 3, 1, 0x0429)
    if not ribbi:
        nt.setName(S.family_fa, 16, 3, 1, 0x0429)
    fsSel = 0x40 if sub == 'Regular' else (0x20 if sub == 'Bold' else 0)
    fsSel |= 0x80  # USE_TYPO_METRICS
    fb.setupOS2(usWeightClass=S.weight, sTypoAscender=asc, sTypoDescender=desc, sTypoLineGap=0,
                usWinAscent=asc, usWinDescent=-desc, fsSelection=fsSel, version=4, achVendID='ARRF',
                sxHeight=round(S.H), sCapHeight=round(S.A), fsType=0,
                ulCodePageRange1=(1 << 0) | (1 << 6))
    fb.setupPost()
    fb.setupHead(unitsPerEm=1000, fontRevision=float(VERSION), macStyle=(1 if sub in ('Bold', 'Black') else 0))
    if sub == 'Black':
        fb.font['head'].macStyle = 1
    from fontTools.misc.timeTools import timestampNow
    fb.font['head'].created = fb.font['head'].modified = timestampNow()
    fb.font['OS/2'].recalcUnicodeRanges(fb.font)
    names_set = set(G.keys())
    fea = feature_code(names_set) + '\n' + mark_code(G, S)
    addOpenTypeFeaturesFromString(fb.font, fea)
    os.makedirs(outdir, exist_ok=True)
    ttf = os.path.join(outdir, 'ttf', psname + '.ttf')
    os.makedirs(os.path.dirname(ttf), exist_ok=True)
    fb.font.save(ttf)
    return ttf


def autohint(ttf):
    try:
        from ttfautohint import ttfautohint
    except ImportError:
        print('ttfautohint-py not installed; skipping hinting')
        return
    ttfautohint(in_file=ttf, out_file=ttf + '.tmp', default_script='arab', fallback_script='none', no_info=True)
    os.replace(ttf + '.tmp', ttf)


def webfonts(ttf, outdir):
    for flavor in ('woff2', 'woff'):
        f = TTFont(ttf)
        f.flavor = flavor
        d = os.path.join(outdir, flavor)
        os.makedirs(d, exist_ok=True)
        f.save(os.path.join(d, os.path.basename(ttf).replace('.ttf', '.' + flavor)))


if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv) > 1 else 'out'
    keys = sys.argv[2:] or list(STYLES)
    for k in keys:
        fam = STYLES[k].family
        od = os.path.join(root, fam, 'fonts')
        t = build(k, od)
        autohint(t)
        webfonts(t, od)
        print('built', t)
