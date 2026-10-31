"""Skeleton definitions for Persian letters, digits and punctuation.

Everything is described as centre-lines in font units (UPM 1000); the
style object decides stroke weight, corner rounding, caps and proportions.
The baseline (joining) stroke has its centre-line on y = 0.
Glyph x grows to the right; joining happens on the left (to the next
letter) and on the right (to the previous letter)."""
from geom import Pen


class Form:
    def __init__(self, pen, jl=False, jr=False, W=None, kind='base'):
        self.pen, self.jl, self.jr, self.W, self.kind = pen, jl, jr, W, kind


class Style:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        sw = self.sw
        self.E = sw * 2                      # extension past the joining edge
        self.capx = sw / 2 if self.cap == 'round' else 0
        self.lp = self.C + sw                # loop centre-line size
        self.tw = sw + 1.3 * self.G          # medial tooth width
        self.ts = sw + 0.95 * self.G         # tooth pitch (seen)
        self.Ts = self.T * 0.85              # seen tooth height
        self.P = sw + self.G                 # pitch of parallel strokes


def build_forms(S):
    sw, G, A, T, D, H, E, lp = S.sw, S.G, S.A, S.T, S.D, S.H, S.E, S.lp
    tw, ts, Ts, P, capx, dg = S.tw, S.ts, S.Ts, S.P, S.capx, S.dg
    hs = sw / 2
    F = {}

    def pen():
        return Pen(S)

    above_tooth = T + capx + dg
    below_base = -hs - dg

    # ------------------------------------------------------------------ helpers
    def tooth_forms(name, ndots, where, extra=None):
        # init
        tx = tw * 0.62
        p = pen().path([(tx, T), (tx, 0, 0.5), (-E, 0)])
        if ndots:
            p.dots(tx, above_tooth if where == 'above' else below_base, ndots, where)
        if extra:
            extra(p, tx, T + capx)
        F[name + '.init'] = Form(p, jl=True)
        # medi
        tx = tw / 2
        p = pen().path([(-E, 0), (tw + E, 0)]).path([(tx, 0), (tx, T)])
        if ndots:
            p.dots(tx, above_tooth if where == 'above' else below_base, ndots, where)
        if extra:
            extra(p, tx, T + capx)
        F[name + '.medi'] = Form(p, jl=True, jr=True, W=tw)

    bw = 3.4 * G + sw  # beh bowl width
    bh = T * 0.85

    def beh_bowl(fina):
        p = pen()
        if fina:
            p.path([(0, bh), (0, 0, 1.6), (bw + E, 0)])
        else:
            p.path([(0, bh), (0, 0, 1.6), (bw, 0, 1.6), (bw, bh)])
        return p

    for nm, nd, wh in [('beh', 1, 'below'), ('peh', 3, 'below'), ('teh', 2, 'above'), ('theh', 3, 'above')]:
        for fina in (False, True):
            p = beh_bowl(fina)
            p.dots(bw / 2, (hs + dg) if wh == 'above' else below_base, nd, wh)
            F[nm + ('.fina' if fina else '')] = Form(p, jr=fina, W=bw + G * 0.25 if fina else None)
        tooth_forms(nm, nd, wh)

    # noon
    nw = 2.3 * G + sw
    nd_ = D * 0.72

    def noon_bowl(p, fina, x0=0, top=None, right_top=None):
        top = T * 0.7 if top is None else top
        pts = [(x0, top), (x0, nd_, 2.2), (x0 + nw, nd_, 2.2)]
        if fina:
            pts += [(x0 + nw, 0, 1), (x0 + nw + G * 0.3 + E, 0)]
        else:
            pts += [(x0 + nw, right_top if right_top is not None else T * 0.7)]
        p.path(pts)
        return p

    for fina in (False, True):
        p = noon_bowl(pen(), fina)
        p.dots(nw / 2, nd_ + hs + dg * 1.6 + (T * 0.25), 1, 'above')
        F['noon' + ('.fina' if fina else '')] = Form(p, jr=fina, W=nw + G * 0.3 if fina else None)
    tooth_forms('noon', 1, 'above')

    # yeh (farsi)
    yw = 3.0 * G + sw * 1.3
    yb = D * 0.78

    def yeh_isol(p, x0=0):
        p.path([(x0 + 0.62 * yw, H * 0.72), (x0 + 0.3 * yw, H * 0.72, 1.2), (x0 + 0.3 * yw, 0, 1.0),
                (x0 + yw, 0, 1.3), (x0 + yw, yb, 1.8), (x0, yb, 1.8), (x0, yb * 0.25)])
        return p

    yfw = yw * 1.05  # final form: diagonal entry from the join, wide bowl, tail rising on the left

    def yeh_fina(p):
        p.path([(yfw + E, 0), (yfw * 0.72, 0, 0.9), (yfw * 0.4, yb, 1.2), (0, yb, 1.8), (0, yb * 0.05)])
        return p

    F['yeh'] = Form(yeh_isol(pen()))
    F['yeh.fina'] = Form(yeh_fina(pen()), jr=True, W=yfw)
    tooth_forms('yeh', 2, 'below')
    # arabic yeh (with dots in all forms)
    F['yehar'] = Form(yeh_isol(pen()).dots(0.62 * yw, yb - hs - dg, 2, 'below'))
    F['yehar.fina'] = Form(yeh_fina(pen()).dots(yfw * 0.45, yb - hs - dg, 2, 'below'), jr=True, W=yfw)
    F['yehar.init'] = F['yeh.init']
    F['yehar.medi'] = F['yeh.medi']
    # alef maksura
    F['alefmaksura'] = F['yeh']
    F['alefmaksura.fina'] = F['yeh.fina']
    tooth_forms('alefmaksura', 0, 'below')  # Arabic alef maksura: dotless in every form

    # ------------------------------------------------------------------ jeem family
    jw = 2.5 * G + sw * 1.2
    jh = H

    def jeem_head():
        return [(0.1 * jw, jh * 0.8), (0.22 * jw, jh, 0.5), (jw, jh, 0.5)]

    def jeem(form):
        p = pen()
        head = jeem_head()
        if form in ('init', 'medi'):
            p.path(head + [(0.28 * jw, 0, 0.6), (-E, 0)])
            if form == 'medi':
                p.path([(0.28 * jw, 0), (jw + E, 0)])
            return p, (0.5 * jw, below_base), (0.55 * jw, jh + capx + hs + dg)
        p.path(head + [(0.05 * jw, 0.05 * jh, 1.0), (0, D * 0.85, 1.6), (jw * 1.05, D * 0.85)])
        if form == 'fina':
            p.path([(0.1 * jw, 0), (jw + E, 0)])
        return p, (0.55 * jw, (D * 0.85 + hs + 0) / 2 + 0 + S.dot * 0.5 - 0), (0.55 * jw, jh + capx + hs + dg)

    for nm, nd, wh in [('jeem', 1, 'in'), ('tcheh', 3, 'in'), ('hah', 0, ''), ('khah', 1, 'above')]:
        for form in ('isol', 'init', 'medi', 'fina'):
            p, inpos, abpos = jeem(form)
            if wh == 'above':
                p.dots(abpos[0], abpos[1] - hs - dg + dg, nd, 'above')
            elif wh == 'in':
                if form in ('init', 'medi'):
                    p.dots(inpos[0], inpos[1], nd, 'below')
                else:
                    # inside the bowl
                    cy = (D * 0.85 + hs + (-hs)) / 2
                    if nd == 1:
                        p.dot(0.55 * jw, cy)
                    else:
                        p.dots(0.55 * jw, cy + S.dot * 0.9, 3, 'below')
            name = nm if form == 'isol' else nm + '.' + form
            F[name] = Form(p, jl=form in ('init', 'medi'), jr=form in ('medi', 'fina'),
                           W=jw if form in ('medi', 'fina') else None)

    # ------------------------------------------------------------------ dal / reh / waw
    dw = 1.6 * G + sw
    for nm, nd in [('dal', 0), ('thal', 1)]:
        p = pen().path([(0.25 * dw, H), (dw, 0, 0.9), (0, 0)])
        if nd:
            p.dots(0.25 * dw, H + capx + dg, 1, 'above')
        F[nm] = Form(p)
        p = pen().path([(0.2 * dw, H), (0.8 * dw, 0, 0.9), (0, 0)]).path([(0.8 * dw, 0), (dw + E, 0)])
        if nd:
            p.dots(0.2 * dw, H + capx + dg, 1, 'above')
        F[nm + '.fina'] = Form(p, jr=True, W=dw)

    rw = 1.25 * G + sw
    rtop = H * 0.55

    def reh(p, x0, fina, top=None):
        if fina:
            p.path([(x0, D * 0.85), (x0 + rw * 0.8, D * 0.22, 1.2), (x0 + rw * 0.8, 0, 0.5), (x0 + rw + E, 0)])
        else:
            p.path([(x0 + rw, rtop if top is None else top), (x0 + rw, D * 0.22, 1.2), (x0, D * 0.85)])
        return p

    for nm, nd in [('reh', 0), ('zain', 1), ('jeh', 3)]:
        p = reh(pen(), 0, False)
        if nd:
            p.dots(rw, rtop + capx + dg, nd, 'above')
        F[nm] = Form(p)
        p = reh(pen(), 0, True)
        if nd:
            p.dots(rw * 0.8, hs + dg, nd, 'above')
        F[nm + '.fina'] = Form(p, jr=True, W=rw)

    # waw
    ww = lp * 0.95
    wh_ = lp
    wx = rw * 0.45

    def waw(p, fina):
        p.path([(wx, 0), (wx + ww, 0), (wx + ww, wh_), (wx, wh_)], closed=True, R=S.RL)
        p.path([(wx + ww, wh_ * 0.5), (wx + ww, D * 0.22, 1.2), (0, D * 0.85)])
        if fina:
            p.path([(wx + ww, 0), (wx + ww + G * 0.35 + E, 0)])
        return p

    F['waw'] = Form(waw(pen(), False))
    F['waw.fina'] = Form(waw(pen(), True), jr=True, W=wx + ww + G * 0.35)

    # ------------------------------------------------------------------ seen / sheen
    def seen(form, nd):
        p = pen()
        if form in ('init', 'medi'):
            a = 0.55 * ts
            xs = [a, a + ts, a + 2 * ts]
            if form == 'init':
                p.path([(-E, 0), (xs[2], 0, 0.5), (xs[2], Ts)])
            else:
                W = xs[2] + 0.55 * ts
                p.path([(-E, 0), (W + E, 0)]).path([(xs[2], 0), (xs[2], Ts)])
            for x in xs[:2]:
                p.path([(x, 0), (x, Ts)])
            cx = xs[1]
        else:
            xs = [nw, nw + ts, nw + 2 * ts]
            p.path([(0, T * 0.6), (0, nd_, 2.2), (nw, nd_, 2.2), (nw, Ts)])
            if form == 'isol':
                p.path([(nw, 0), (xs[2], 0, 0.5), (xs[2], Ts)])
            else:
                W = xs[2] + 0.55 * ts
                p.path([(nw, 0), (W + E, 0)]).path([(xs[2], 0), (xs[2], Ts)])
            p.path([(xs[1], 0), (xs[1], Ts)])
            cx = xs[1]
        if nd:
            p.dots(cx, Ts + capx + dg, 3, 'above')
        W = None
        if form in ('medi', 'fina'):
            W = xs[2] + 0.55 * ts
        return Form(p, jl=form in ('init', 'medi'), jr=form in ('medi', 'fina'), W=W)

    for nm, nd in [('seen', 0), ('sheen', 3)]:
        for form in ('isol', 'init', 'medi', 'fina'):
            F[nm if form == 'isol' else nm + '.' + form] = seen(form, nd)

    # ------------------------------------------------------------------ sad / dad
    sl = 2.1 * G + sw * 1.4
    sh = lp * 0.92

    def sad(form, nd):
        p = pen()
        if form in ('init', 'medi'):
            tx = 0.5 * ts
            a = tx + 0.95 * ts
            p.path([(-E, 0), (a, 0)]).path([(tx, 0), (tx, Ts)])
        else:
            p.path([(0, T * 0.6), (0, nd_, 2.2), (nw, nd_, 2.2), (nw, Ts)])
            a = nw + 0.95 * ts
            p.path([(nw, 0), (a, 0)])
        p.path([(a, 0), (a + sl, 0), (a + sl, sh), (a, sh)], closed=True, R=S.RL)
        W = None
        if form in ('medi', 'fina'):
            W = a + sl + 0.45 * G
            p.path([(a + sl, 0), (W + E, 0)])
        if nd:
            p.dots(a + sl / 2, sh + capx + hs + dg - capx, 1, 'above')
        return Form(p, jl=form in ('init', 'medi'), jr=form in ('medi', 'fina'), W=W)

    for nm, nd in [('sad', 0), ('dad', 1)]:
        for form in ('isol', 'init', 'medi', 'fina'):
            F[nm if form == 'isol' else nm + '.' + form] = sad(form, nd)

    # ------------------------------------------------------------------ tah / zah
    def tah(form, nd):
        p = pen()
        a = 0.3 * G + hs if form in ('init', 'medi') else 0
        if form in ('init', 'medi'):
            p.path([(-E, 0), (a, 0)])
        p.path([(a, 0), (a + sl, 0), (a + sl, sh), (a, sh)], closed=True, R=S.RL)
        sx = a + sl * 0.3
        p.path([(sx, sh * 0.5), (sx, A)])
        W = None
        if form in ('medi', 'fina'):
            W = a + sl + 0.45 * G
            p.path([(a + sl, 0), (W + E, 0)])
        if nd:
            p.dots(a + sl * 0.68, sh + hs + dg, 1, 'above')
        return Form(p, jl=form in ('init', 'medi'), jr=form in ('medi', 'fina'), W=W)

    for nm, nd in [('tah', 0), ('zah', 1)]:
        for form in ('isol', 'init', 'medi', 'fina'):
            F[nm if form == 'isol' else nm + '.' + form] = tah(form, nd)

    # ------------------------------------------------------------------ ain / ghain
    aw = 1.6 * G + sw * 1.2
    he = H * 0.92
    mw = lp * 1.3 + 0.3 * G
    mh = max(he * 0.85, lp * 1.15)

    def ain(form, nd):
        p = pen()
        W = None
        if form == 'init':
            p.path([(aw, he), (0.2 * aw, he, 1.2), (0.2 * aw, 0, 1.0), (0.78 * aw, 0)])
            p.path([(0.2 * aw, 0), (-E, 0)])
            dx, dy = 0.6 * aw, he + capx + hs + dg - capx
        elif form == 'isol':
            p.path([(aw, he), (0.2 * aw, he, 1.2), (0.2 * aw, 0, 1.0), (0.75 * aw, 0, 0),
                    (0, D * 0.3, 1.0), (0, D * 0.85, 1.6), (aw * 1.05, D * 0.85)])
            dx, dy = 0.6 * aw, he + hs + dg
        else:
            x0 = 0.35 * G if form == 'fina' else 0
            p.path([(x0, mh), (x0 + mw, mh), (x0 + mw / 2, 0)], closed=True, R=S.RL * 0.6)
            W = x0 + mw + 0.35 * G
            p.path([(x0 + mw / 2, 0), (W + E, 0)])
            if form == 'medi':
                p.path([(-E, 0), (x0 + mw / 2, 0)])
            else:
                p.path([(x0 + mw / 2, 0), (0, D * 0.3, 1.0), (0, D * 0.85, 1.6), (x0 + mw * 1.05, D * 0.85)])
            dx, dy = x0 + mw / 2, mh + hs + dg
        if nd:
            p.dots(dx, dy, 1, 'above')
        return Form(p, jl=form in ('init', 'medi'), jr=form in ('medi', 'fina'), W=W)

    for nm, nd in [('ain', 0), ('ghain', 1)]:
        for form in ('isol', 'init', 'medi', 'fina'):
            F[nm if form == 'isol' else nm + '.' + form] = ain(form, nd)

    # ------------------------------------------------------------------ feh / qaf
    fl = lp * 1.0
    fh = lp * 1.0

    def feh(form, nd, qaf=False):
        p = pen()
        W = None
        if form in ('init', 'medi'):
            a = 0.3 * G + hs
            p.path([(-E, 0), (a, 0)])
        elif not qaf:
            fbw = bw + fl * 0.6
            a = fbw - fl
            p.path([(0, bh), (0, 0, 1.6), (a + fl, 0)])
        else:
            qw = nw + fl * 0.35
            a = qw - fl
            p.path([(0, T * 0.7), (0, nd_, 2.2), (qw, nd_, 2.2), (qw, 0)])
        p.path([(a, 0), (a + fl, 0), (a + fl, fh), (a, fh)], closed=True, R=S.RL)
        if form in ('medi', 'fina'):
            W = a + fl + 0.4 * G
            p.path([(a + fl, 0), (W + E, 0)])
        p.dots(a + fl / 2, fh + hs + dg, nd, 'above')
        return Form(p, jl=form in ('init', 'medi'), jr=form in ('medi', 'fina'), W=W)

    for form in ('isol', 'init', 'medi', 'fina'):
        F['feh' if form == 'isol' else 'feh.' + form] = feh(form, 1)
        F['qaf' if form == 'isol' else 'qaf.' + form] = feh(form, 2, qaf=form in ('isol', 'fina'))

    # ------------------------------------------------------------------ kaf / gaf
    kw = 1.35 * G + sw * 1.1
    Ak = S.Ak

    def kaf(form, gaf):
        p = pen()
        W = None
        if form in ('init', 'medi'):
            x = kw
        else:
            x = bw * 0.95
        if S.kafstyle == 'kufi':
            p.path([(x, Ak), (x, 0, 0.8), ((-E if form in ('init', 'medi') else 0), 0, 1.6)] +
                   ([] if form in ('init', 'medi') else [(0, bh)]))
            slope = 0.25
            fl_ = kw * 0.9
            p.path([(x + hs, Ak + hs), (x - fl_, Ak + hs - fl_ * slope)], cap='flat')
            if gaf:
                y2 = Ak + hs + P * 0.78
                p.path([(x + hs, y2), (x - fl_ * 0.85, y2 - fl_ * 0.85 * slope)], cap='flat')
        else:
            vx = x - kw * 0.92
            vy = Ak * 0.52
            base = [(-E, 0)] if form in ('init', 'medi') else [(0, 0, 1.6), (0, bh)]
            p.path([(x + kw * 0.08, Ak), (vx, vy, 0.9), (x, 0, 0.5)] + base)
            if gaf:
                # parallel stroke above the upper diagonal
                import math
                dx, dy = vx - (x + kw * 0.08), vy - Ak
                L = math.hypot(dx, dy)
                nx_, ny_ = -dy / L, dx / L
                if ny_ < 0:
                    nx_, ny_ = -nx_, -ny_
                off = P * 0.95
                sx, sy = x + kw * 0.08 + nx_ * off, Ak + ny_ * off
                p.path([(sx, sy), (sx + dx * 0.55, sy + dy * 0.55)])
        if form in ('medi', 'fina'):
            W = x + 0.35 * G
            p.path([(x, 0), (W + E, 0)])
        return Form(p, jl=form in ('init', 'medi'), jr=form in ('medi', 'fina'), W=W)

    for form in ('isol', 'init', 'medi', 'fina'):
        F['keheh' if form == 'isol' else 'keheh.' + form] = kaf(form, False)
        F['gaf' if form == 'isol' else 'gaf.' + form] = kaf(form, True)

    # ------------------------------------------------------------------ lam
    lw = nw * 0.95
    lx = 0.62 * G + hs
    F['lam.init'] = Form(pen().path([(lx, A), (lx, 0, 0.6), (-E, 0)]), jl=True)
    F['lam.medi'] = Form(pen().path([(-E, 0), (2 * lx + E, 0)]).path([(lx, 0), (lx, A)]), jl=True, jr=True, W=2 * lx)
    F['lam'] = Form(pen().path([(0, T * 0.7), (0, nd_, 2.2), (lw, nd_, 2.2), (lw, A)]))
    F['lam.fina'] = Form(pen().path([(0, T * 0.7), (0, nd_, 2.2), (lw, nd_, 2.2), (lw, A)])
                         .path([(lw, 0), (lw + 0.7 * G + E, 0)]), jr=True, W=lw + 0.7 * G)

    # lam-alef ligatures
    L2 = 1.9 * G + sw * 1.3
    la = 0.42 * L2

    def lamalef(fina, mark=None):
        p = pen().path([(0, A * 0.97), (la, 0, 0.5), (L2, 0, 0.9), (L2, A)])
        W = None
        if fina:
            W = L2 + 0.8 * G
            p.path([(L2, 0), (W + E, 0)])
        if mark:
            mark(p, 0.0, A * 0.97 + capx)
        return Form(p, jr=fina, W=W)

    # ------------------------------------------------------------------ meem
    mlw = lp * 1.12
    mlh = lp * 0.86

    def meem(form):
        p = pen()
        W = None
        if form in ('init', 'medi'):
            a = 0.3 * G + hs
            p.path([(-E, 0), (a, 0)])
        else:
            a = 0
            p.path([(a, 0), (a, D * 0.9)])
        p.path([(a, 0), (a + mlw, 0), (a + mlw, mlh), (a, mlh)], closed=True, R=S.RL)
        if form in ('medi', 'fina'):
            W = a + mlw + 0.4 * G
            p.path([(a + mlw, 0), (W + E, 0)])
        return Form(p, jl=form in ('init', 'medi'), jr=form in ('medi', 'fina'), W=W)

    for form in ('isol', 'init', 'medi', 'fina'):
        F['meem' if form == 'isol' else 'meem.' + form] = meem(form)

    # ------------------------------------------------------------------ heh
    hw = lp * 1.2
    hh = lp * 1.3

    def heh(form, nd=0, hamza=None):
        p = pen()
        W = None
        top = hh
        if form == 'isol':
            p.path([(0, 0), (hw, 0), (hw, hh), (0, hh)], closed=True, R=S.RL * 1.2)
            cx = hw / 2
        elif form == 'fina':
            a = 0
            p.path([(a, 0), (a + hw * 0.9, 0), (a + hw * 0.9, hh * 0.85), (a, hh * 0.85)], closed=True, R=S.RL * 1.2)
            W = a + hw * 0.9 + 0.4 * G
            p.path([(a + hw * 0.9, 0), (W + E, 0)])
            cx = hw * 0.45
            top = hh * 0.85
        elif form == 'init':
            a = 0.3 * G + hs
            hi = 2 * (S.C * 0.8) + 2 * sw
            p.path([(-E, 0), (a, 0)])
            p.path([(a, 0), (a + lp, 0), (a + lp, hi), (a, hi)], closed=True, R=S.RL * 0.8)
            p.path([(a, hi / 2), (a + lp, hi / 2)])
            cx = a + lp / 2
            top = hi
        else:  # medi
            a = 0.3 * G + hs
            lo = -(S.C * 0.75 + sw)
            hi = S.C * 0.75 + sw
            p.path([(-E, 0), (a + lp + 0.3 * G + E, 0)])
            p.path([(a, lo), (a + lp, lo), (a + lp, hi), (a, hi)], closed=True, R=S.RL * 0.8)
            W = a + lp + 0.3 * G
            cx = a + lp / 2
            top = hi
        if nd:
            p.dots(cx, top + hs + dg, nd, 'above')
        if hamza:
            hamza(p, cx, top + hs + dg)
        return Form(p, jl=form in ('init', 'medi'), jr=form in ('medi', 'fina'), W=W)

    for form in ('isol', 'init', 'medi', 'fina'):
        F['heh' if form == 'isol' else 'heh.' + form] = heh(form)
    F['tehmarbuta'] = heh('isol', 2)
    F['tehmarbuta.fina'] = heh('fina', 2)

    # ------------------------------------------------------------------ hamza & alef
    def hamza_path(p, x, y, s=1.0, sw_=None):
        w = (0.9 * G + sw) * s
        h = H * 0.8 * s
        p.path([(x + w / 2, y + h), (x - w / 2 + w * 0.1, y + h, 1.0), (x - w / 2 + w * 0.1, y + h * 0.45, 1.0),
                (x + w / 2, y + h * 0.12)], sw=sw_, R=S.R * s)
        return w, h

    msw = max(48, sw * 0.62)  # mark stroke

    def hamza_above(p, x, y):
        hamza_path(p, x, y + msw * 0.1, 0.62, msw)

    def hamza_below(p, x, y):
        w, h = hamza_path(p, x, y - H * 0.8 * 0.62 - msw * 0.6, 0.62, msw)

    def madda(p, x, y):
        m = 2.3 * G * 0.75 + msw
        h = H * 0.32
        yy = y + msw * 0.5
        p.path([(x - m / 2, yy), (x - m / 6, yy + h, 0.6), (x + m / 6, yy, 0.6), (x + m / 2, yy + h)], sw=msw, R=S.R * 0.4)

    hp = pen()
    hamza_path(hp, 0, 0)
    F['hamza'] = Form(hp)

    def alef(fina, mark=None, below=None):
        p = pen()
        W = None
        if fina:
            p.path([(0, A), (0, 0, 0.6), (0.5 * G + hs + E, 0)])
            W = 0.5 * G + hs
        else:
            p.path([(0, 0), (0, A)])
        if mark:
            mark(p, 0, A + capx + dg * 0.8)
        if below:
            below(p, 0, -hs - dg * 0.8)
        return Form(p, jr=fina, W=W)

    F['alef'] = alef(False)
    F['alef.fina'] = alef(True)
    for nm, mk, bl in [('alefmadda', madda, None), ('alefhamza', hamza_above, None), ('alefhamzabelow', None, hamza_below)]:
        F[nm] = alef(False, mk, bl)
        F[nm + '.fina'] = alef(True, mk, bl)
    F['lamalef'] = lamalef(False)
    F['lamalef.fina'] = lamalef(True)
    F['lamalefmadda'] = lamalef(False, lambda p, x, y: madda(p, x + G * 0.25, y + dg * 0.8))
    F['lamalefmadda.fina'] = lamalef(True, lambda p, x, y: madda(p, x + G * 0.25, y + dg * 0.8))
    F['lamalefhamza'] = lamalef(False, lambda p, x, y: hamza_above(p, x + G * 0.15, y + dg * 0.8))
    F['lamalefhamza.fina'] = lamalef(True, lambda p, x, y: hamza_above(p, x + G * 0.15, y + dg * 0.8))
    F['lamalefhamzabelow'] = lamalef(False, lambda p, x, y: hamza_below(p, x + la * 0.5, -hs - dg))
    F['lamalefhamzabelow.fina'] = lamalef(True, lambda p, x, y: hamza_below(p, x + la * 0.5, -hs - dg))

    # waw hamza
    p = waw(pen(), False)
    hamza_above(p, wx + ww / 2, wh_ + hs + dg)
    F['wawhamza'] = Form(p)
    p = waw(pen(), True)
    hamza_above(p, wx + ww / 2, wh_ + hs + dg)
    F['wawhamza.fina'] = Form(p, jr=True, W=wx + ww + G * 0.35)
    # yeh hamza
    p = yeh_isol(pen())
    hamza_above(p, 0.45 * yw, H * 0.72 + capx + hs + dg * 0.5)
    F['yehhamza'] = Form(p)
    p = yeh_fina(pen())
    hamza_above(p, 0.3 * yfw, hs + dg)
    F['yehhamza.fina'] = Form(p, jr=True, W=yfw)
    tooth_forms('yehhamza', 0, 'above', extra=lambda p, x, y: hamza_above(p, x, y + dg))
    # heh with yeh above (ۀ)
    F['hehyeh'] = heh('isol', hamza=hamza_above)
    F['hehyeh.fina'] = heh('fina', hamza=hamza_above)

    # tatweel
    tk = tw * 1.2
    F['tatweel'] = Form(pen().path([(-E, 0), (tk + E, 0)]), jl=True, jr=True, W=tk)

    # ------------------------------------------------------------------ digits (tabular)
    Hn = S.Hn
    dwid = S.dw          # inner design width of a digit
    dsw = S.dsw if hasattr(S, 'dsw') else sw

    def dpen():
        return Pen(S)

    digs = {}
    w = dwid
    p = dpen()
    p.dot(w / 2, Hn * 0.45, size=S.dot * 1.05)
    digs[0] = p
    digs[1] = dpen().path([(w * 0.42, Hn), (w * 0.5, Hn * 0.7, 1.5), (w * 0.5, 0)])
    digs[2] = dpen().path([(w * 0.12, Hn), (w * 0.22, Hn * 0.6, 1.2), (w * 0.22, 0)]) \
        .path([(w * 0.22, Hn * 0.62), (w * 0.95, Hn * 0.62, 1.1), (w * 0.95, Hn)])
    digs[3] = dpen().path([(w * 0.08, Hn), (w * 0.18, Hn * 0.6, 1.2), (w * 0.18, 0)]) \
        .path([(w * 0.18, Hn * 0.62), (w * 0.98, Hn * 0.62, 0.8), (w * 0.98, Hn)]) \
        .path([(w * 0.58, Hn * 0.62), (w * 0.58, Hn * 0.92)])
    digs[4] = dpen().path([(w * 0.12, Hn), (w * 0.22, Hn * 0.6, 1.2), (w * 0.22, 0)]) \
        .path([(w * 0.95, Hn), (w * 0.5, Hn, 1.0), (w * 0.5, Hn * 0.6, 1.0), (w * 0.95, Hn * 0.55)]) \
        .path([(w * 0.22, Hn * 0.62), (w * 0.5, Hn * 0.6)])
    digs[5] = dpen().path([(w * 0.05, 0), (w * 0.5, Hn * 0.12), (w * 0.95, 0), (w * 0.95, Hn * 0.55),
                           (w * 0.5, Hn), (w * 0.05, Hn * 0.55)], closed=True, R=S.RL * 1.1)
    digs[6] = dpen().path([(w * 0.95, Hn), (w * 0.12, Hn, 1.0), (w * 0.12, Hn * 0.62, 1.0), (w * 0.95, Hn * 0.6)]) \
        .path([(w * 0.7, Hn * 0.6), (w * 0.05, 0)])
    digs[7] = dpen().path([(w * 0.02, Hn), (w * 0.5, 0, 0.25), (w * 0.98, Hn)], R=S.R * 0.3)
    digs[8] = dpen().path([(w * 0.02, 0), (w * 0.5, Hn, 0.25), (w * 0.98, 0)], R=S.R * 0.3)
    l9 = min(w * 0.85, lp * 1.05)
    digs[9] = dpen().path([(w * 0.92 - l9, Hn - l9 * 0.95), (w * 0.92, Hn - l9 * 0.95), (w * 0.92, Hn), (w * 0.92 - l9, Hn)],
                          closed=True, R=S.RL).path([(w * 0.92, Hn * 0.6), (w * 0.92, 0)])
    for i, p in digs.items():
        F['digit%d' % i] = Form(p, kind='digit', W=dwid)

    # ------------------------------------------------------------------ Latin digits (same height as Persian)
    lat = {}
    rr = S.RL * 1.1
    lat[0] = dpen().path([(w * 0.1, 0), (w * 0.9, 0), (w * 0.9, Hn), (w * 0.1, Hn)], closed=True, R=rr)
    lat[1] = dpen().path([(w * 0.22, Hn * 0.78), (w * 0.58, Hn, 0.3), (w * 0.58, 0)], R=S.R * 0.4)
    lat[2] = dpen().path([(w * 0.1, Hn * 0.7), (w * 0.1, Hn, 0.9), (w * 0.9, Hn, 0.9), (w * 0.9, Hn * 0.58, 0.9),
                          (w * 0.1, 0, 0.2), (w * 0.92, 0)], R=rr)
    lat[3] = dpen().path([(w * 0.1, Hn), (w * 0.88, Hn, 0.4), (w * 0.42, Hn * 0.56, 0.3), (w * 0.9, Hn * 0.5, 0.9),
                          (w * 0.9, 0, 0.9), (w * 0.08, 0)], R=rr)
    lat[4] = dpen().path([(w * 0.7, 0), (w * 0.7, Hn, 0.2), (w * 0.06, Hn * 0.3, 0.2), (w * 0.95, Hn * 0.3)], R=S.R * 0.4)
    lat[5] = dpen().path([(w * 0.88, Hn), (w * 0.14, Hn, 0.3), (w * 0.12, Hn * 0.55, 0.3), (w * 0.9, Hn * 0.55, 0.9),
                          (w * 0.9, 0, 0.9), (w * 0.08, 0)], R=rr)
    lat[6] = dpen().path([(w * 0.82, Hn), (w * 0.1, Hn, 0.9), (w * 0.1, 0, 0.9), (w * 0.9, 0, 0.9),
                          (w * 0.9, Hn * 0.56, 0.9), (w * 0.1, Hn * 0.56)], R=rr)
    lat[7] = dpen().path([(w * 0.08, Hn), (w * 0.92, Hn, 0.2), (w * 0.38, 0)], R=S.R * 0.4)
    lat[8] = dpen().path([(w * 0.16, Hn * 0.55), (w * 0.84, Hn * 0.55), (w * 0.84, Hn), (w * 0.16, Hn)], closed=True, R=rr) \
        .path([(w * 0.08, 0), (w * 0.92, 0), (w * 0.92, Hn * 0.55), (w * 0.08, Hn * 0.55)], closed=True, R=rr)
    lat[9] = dpen().path([(w * 0.18, 0), (w * 0.9, 0, 0.9), (w * 0.9, Hn, 0.9), (w * 0.1, Hn, 0.9),
                          (w * 0.1, Hn * 0.44, 0.9), (w * 0.9, Hn * 0.44)], R=rr)
    for i, p in lat.items():
        F['digitlat%d' % i] = Form(p, kind='digit', W=dwid)

    # ------------------------------------------------------------------ punctuation
    dd = S.dot * 1.15
    F['period'] = Form(pen().dot(0, dd / 2 - hs, size=dd))
    F['colon'] = Form(pen().dot(0, dd / 2 - hs, size=dd).dot(0, H * 0.75, size=dd))
    F['exclam'] = Form(pen().dot(0, dd / 2 - hs, size=dd).path([(0, dd + G * 0.35), (0, A)]))
    qw_ = 1.3 * G + sw
    F['questionar'] = Form(pen().dot(qw_ / 2, dd / 2 - hs, size=dd)
                           .path([(qw_, A * 0.72), (qw_, A, 1.2), (0, A, 1.2), (0, A * 0.55, 1.2),
                                  (qw_ / 2, A * 0.5, 0.8), (qw_ / 2, dd + G * 0.35)]))

    def commaar(p, x, y):
        s = dd
        p.dot(x, y + s / 2, size=s)
        p.path([(x - s * 0.15, y + s * 0.6), (x + s * 0.55, y + s * 1.6)], sw=s * 0.55, cap='round')

    p = pen()
    commaar(p, 0, -hs)
    F['commaar'] = Form(p)
    p = pen()
    commaar(p, 0, -hs)
    p.dot(0, H * 0.8, size=dd)
    F['semicolonar'] = Form(p)
    ch = H * 0.62
    cw = ch * 0.55

    def chev(p, x, d):
        p.path([(x + d * cw, H * 0.05), (x, H * 0.05 + ch / 2, 0.2), (x + d * cw, H * 0.05 + ch)], R=S.R * 0.2,
               sw=sw * 0.8)

    p = pen()
    chev(p, 0, 1)
    chev(p, cw * 0.95 + sw * 0.4, 1)
    F['guillemetleft'] = Form(p)
    p = pen()
    chev(p, cw, -1)
    chev(p, cw * 1.95 + sw * 0.4, -1)
    F['guillemetright'] = Form(p)
    pw = G * 0.9
    F['parenleft'] = Form(pen().path([(pw, A + G * 0.4), (0, A * 0.55, 2.5), (0, A * 0.25), (pw, D * 0.9)], R=S.R * 2.5))
    F['parenright'] = Form(pen().path([(0, A + G * 0.4), (pw, A * 0.55, 2.5), (pw, A * 0.25), (0, D * 0.9)], R=S.R * 2.5))
    hy = G * 1.6
    F['hyphen'] = Form(pen().path([(0, H * 0.5), (hy, H * 0.5)], cap='flat'))
    F['slash'] = Form(pen().path([(0, D * 0.4), (G * 2.2, A)], sw=sw * 0.85))
    pc = G * 2.4
    F['percentar'] = Form(pen().path([(0, D * 0.1), (pc, A * 0.9)], sw=sw * 0.85)
                          .dot(pc * 0.12, A * 0.75, size=dd).dot(pc * 0.88, H * 0.1, size=dd))
    F['plus'] = Form(pen().path([(0, H * 0.55), (G * 2.4, H * 0.55)], cap='flat').path([(G * 1.2, H * 0.55 - G * 1.2), (G * 1.2, H * 0.55 + G * 1.2)], cap='flat'))
    F['equal'] = Form(pen().path([(0, H * 0.55 + G * 0.55), (G * 2.4, H * 0.55 + G * 0.55)], cap='flat').path([(0, H * 0.55 - G * 0.55), (G * 2.4, H * 0.55 - G * 0.55)], cap='flat'))

    F['endash'] = Form(pen().path([(0, H * 0.5), (G * 3.2, H * 0.5)], cap='flat'))
    F['emdash'] = Form(pen().path([(0, H * 0.5), (G * 6.4, H * 0.5)], cap='flat'))

    def tail(p, x, y, s):
        p.dot(x, y + s / 2, size=s)
        p.path([(x + s * 0.15, y + s * 0.4), (x - s * 0.45, y - s * 0.7)], sw=s * 0.55, cap='round')

    p = pen(); tail(p, 0, -hs, dd); F['comma'] = Form(p)
    p = pen(); tail(p, 0, -hs, dd); p.dot(0, H * 0.8, size=dd); F['semicolon'] = Form(p)
    p = pen(); tail(p, 0, -hs + H * 0.15, dd * 0.8); F['thousandsar'] = Form(p)
    p = pen(); p.path([(dd * 0.3, -hs + dd * 1.4), (-dd * 0.3, -hs)], sw=dd * 0.6, cap='round'); F['decimalar'] = Form(p)
    F['quotedbl'] = Form(pen().path([(0, A), (0, A - H * 0.55)], sw=sw * 0.8).path([(G * 1.1, A), (G * 1.1, A - H * 0.55)], sw=sw * 0.8))
    F['quotesingle'] = Form(pen().path([(0, A), (0, A - H * 0.55)], sw=sw * 0.8))

    bh_ = A + G * 0.3
    F['bar'] = Form(pen().path([(0, D * 0.75), (0, bh_)], cap='flat'))
    bw_ = G * 0.75
    F['bracketleft'] = Form(pen().path([(bw_, bh_), (0, bh_, 0.2), (0, D * 0.75, 0.2), (bw_, D * 0.75)], R=S.R * 0.3))
    F['bracketright'] = Form(pen().path([(0, bh_), (bw_, bh_, 0.2), (bw_, D * 0.75, 0.2), (0, D * 0.75)], R=S.R * 0.3))
    F['underscore'] = Form(pen().path([(0, D * 0.55), (G * 3.2, D * 0.55)], cap='flat'))
    ast = G * 0.85
    p = pen()
    for k in range(3):
        import math as _m
        a = _m.pi / 2 + k * _m.pi / 3
        cx, cy = ast, A - ast
        p.path([(cx - _m.cos(a) * ast, cy - _m.sin(a) * ast), (cx + _m.cos(a) * ast, cy + _m.sin(a) * ast)], sw=sw * 0.8)
    F['asterisk'] = Form(p)
    lg = G * 1.6
    F['less'] = Form(pen().path([(lg, H * 0.55 + lg * 0.6), (0, H * 0.55, 0.2), (lg, H * 0.55 - lg * 0.6)], R=S.R * 0.3))
    F['greater'] = Form(pen().path([(0, H * 0.55 + lg * 0.6), (lg, H * 0.55, 0.2), (0, H * 0.55 - lg * 0.6)], R=S.R * 0.3))
    tw_ = G * 2.2
    F['asciitilde'] = Form(pen().path([(0, H * 0.45), (tw_ * 0.3, H * 0.7, 0.8), (tw_ * 0.7, H * 0.4, 0.8), (tw_, H * 0.65)], R=S.R * 0.8))
    F['backslash'] = Form(pen().path([(G * 2.2, D * 0.4), (0, A)], sw=sw * 0.85))
    nw_ = G * 2.4
    F['numbersign'] = Form(pen().path([(nw_ * 0.35, 0), (nw_ * 0.45, A * 0.9)], sw=sw * 0.8).path([(nw_ * 0.65, 0), (nw_ * 0.75, A * 0.9)], sw=sw * 0.8)
                           .path([(0, A * 0.3), (nw_, A * 0.3)], sw=sw * 0.8, cap='flat').path([(nw_ * 0.08, A * 0.62), (nw_ * 1.05, A * 0.62)], sw=sw * 0.8, cap='flat'))
    F['question'] = Form(pen().dot(qw_ / 2, dd / 2 - hs, size=dd)
                         .path([(0, A * 0.72), (0, A, 1.2), (qw_, A, 1.2), (qw_, A * 0.55, 1.2),
                                (qw_ / 2, A * 0.5, 0.8), (qw_ / 2, dd + G * 0.35)]))
    F['bullet'] = Form(pen().dot(0, H * 0.5, size=dd * 1.3))
    F['ellipsis'] = Form(pen().dot(0, dd / 2 - hs, size=dd).dot(dd * 1.9, dd / 2 - hs, size=dd).dot(dd * 3.8, dd / 2 - hs, size=dd))
    mx = G * 1.1
    F['multiply'] = Form(pen().path([(0, H * 0.55 - mx), (2 * mx, H * 0.55 + mx)], cap='flat').path([(0, H * 0.55 + mx), (2 * mx, H * 0.55 - mx)], cap='flat'))

    # ------------------------------------------------------------------ marks (zero width, centred on x=0)
    fw = G * 0.9 + msw

    def mk(f, kind='mark_above'):
        p = pen()
        f(p)
        return Form(p, kind=kind)

    F['fatha'] = mk(lambda p: p.path([(-fw / 2, 0), (fw / 2, fw * 0.45)], sw=msw, cap='flat'))
    F['kasra'] = mk(lambda p: p.path([(-fw / 2, -fw * 0.45), (fw / 2, 0)], sw=msw, cap='flat'), 'mark_below')
    F['fathatan'] = mk(lambda p: p.path([(-fw / 2, 0), (fw / 2, fw * 0.45)], sw=msw, cap='flat')
                       .path([(-fw / 2, msw * 1.9), (fw / 2, fw * 0.45 + msw * 1.9)], sw=msw, cap='flat'))
    F['kasratan'] = mk(lambda p: p.path([(-fw / 2, -fw * 0.45), (fw / 2, 0)], sw=msw, cap='flat')
                       .path([(-fw / 2, -fw * 0.45 - msw * 1.9), (fw / 2, -msw * 1.9)], sw=msw, cap='flat'), 'mark_below')
    dl = lp * 0.55

    def damma(p, x=0):
        p.path([(x - dl * 0.1, msw * 1.0 + dl * 0.2), (x + dl * 0.9, msw * 1.0 + dl * 0.2), (x + dl * 0.9, msw + dl * 1.1),
                (x - dl * 0.1, msw + dl * 1.1)], closed=True, sw=msw, R=S.RL * 0.4)
        p.path([(x + dl * 0.9, msw + dl * 0.6), (x + dl * 0.9, msw * 0.5, 1), (x - dl * 0.5, 0)], sw=msw, R=S.R * 0.5)

    F['damma'] = mk(lambda p: damma(p, -dl * 0.25))
    F['dammatan'] = mk(lambda p: (damma(p, -dl * 0.8), damma(p, dl * 0.3)))
    F['sukun'] = mk(lambda p: p.path([(-dl * 0.45, 0), (dl * 0.45, 0), (dl * 0.45, dl * 0.9), (-dl * 0.45, dl * 0.9)],
                                    closed=True, sw=msw * 0.9, R=S.RL * 0.5))
    shw = G * 1.5 + msw

    def shadda(p):
        p.path([(-shw / 2, fw * 0.55), (-shw / 2, 0, 0.6), (shw / 2, 0, 0.6), (shw / 2, fw * 0.55)], sw=msw, R=S.R * 0.4)
        p.path([(0, 0), (0, fw * 0.45)], sw=msw)

    F['shadda'] = mk(shadda)
    F['superalef'] = mk(lambda p: p.path([(0, 0), (0, H * 0.75)], sw=msw))
    F['hamzaabove'] = mk(lambda p: hamza_above(p, 0, 0))
    F['hamzabelow'] = mk(lambda p: hamza_path(p, 0, -H * 0.8 * 0.62, 0.62, msw), 'mark_below')
    return F
