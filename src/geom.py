"""Geometry helpers: centre-line skeletons -> filled outlines."""
import math
from shapely.geometry import LineString, LinearRing, Polygon, Point, box, MultiPolygon, GeometryCollection
from shapely.ops import unary_union
from shapely import affinity


def _qbez(a, c, b, n=10):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t ** 2 * b[0]
        y = (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t ** 2 * b[1]
        pts.append((x, y))
    return pts


def fillet(pts, closed, R):
    """Round every corner of a polyline with a quadratic curve.
    Each point may carry a third value: radius multiplier."""
    P = [(p[0], p[1], (p[2] if len(p) > 2 else 1.0)) for p in pts]
    n = len(P)
    out = []
    for i in range(n):
        x, y, rm = P[i]
        if not closed and (i == 0 or i == n - 1):
            out.append((x, y))
            continue
        px, py, _ = P[i - 1]
        nx, ny, _ = P[(i + 1) % n]
        r = R * rm
        d1 = math.hypot(x - px, y - py)
        d2 = math.hypot(nx - x, ny - y)
        if r <= 0 or d1 == 0 or d2 == 0:
            out.append((x, y))
            continue
        lim1 = d1 * (0.95 if (not closed and i - 1 == 0) else 0.5)
        lim2 = d2 * (0.95 if (not closed and i + 1 == n - 1) else 0.5)
        t = min(r, lim1, lim2)
        a = (x + (px - x) * t / d1, y + (py - y) * t / d1)
        b = (x + (nx - x) * t / d2, y + (ny - y) * t / d2)
        out.extend(_qbez(a, (x, y), b, 12))
    return out


class Pen:
    """Collects strokes for one glyph in a given style."""

    def __init__(self, S):
        self.S = S
        self.shapes = []

    def path(self, pts, closed=False, sw=None, R=None, cap=None):
        S = self.S
        sw = sw or S.sw
        R = S.R if R is None else R
        cap = cap or S.cap
        c = fillet(pts, closed, R)
        if closed:
            g = LinearRing(c).buffer(sw / 2, join_style=S.join, mitre_limit=4, quad_segs=16)
        else:
            g = LineString(c).buffer(sw / 2, cap_style=cap, join_style=S.join, mitre_limit=4, quad_segs=16)
        self.shapes.append(g)
        return self

    def poly(self, geom):
        self.shapes.append(geom)
        return self

    def dot(self, x, y, size=None):
        S = self.S
        d = size or S.dot
        if S.dotshape == 'square':
            g = box(x - d / 2, y - d / 2, x + d / 2, y + d / 2)
            r = d * 0.12
            g = g.buffer(-r).buffer(r, quad_segs=6)
        elif S.dotshape == 'diamond':
            s = d * 0.62
            g = Polygon([(x, y - s), (x + s, y), (x, y + s), (x - s, y)])
            r = d * 0.10
            g = g.buffer(-r).buffer(r, quad_segs=6)
        else:
            g = Point(x, y).buffer(d / 2, quad_segs=16)
        self.shapes.append(g)
        return self

    def dots(self, x, y, n, where):
        """y = edge of the dot group nearest the letter body."""
        S = self.S
        d = S.dot
        g = d * 0.28  # gap between dots
        if S.dotshape == 'diamond':
            g = d * 0.12
        sgn = 1 if where == 'above' else -1
        c1 = y + sgn * d / 2
        c2 = y + sgn * (d * 1.5 + g)
        if n == 1:
            self.dot(x, c1)
        elif n == 2:
            self.dot(x - (d + g) / 2, c1)
            self.dot(x + (d + g) / 2, c1)
        elif n == 3:
            if where == 'above':  # two below, one on top
                self.dot(x - (d + g) / 2, c1)
                self.dot(x + (d + g) / 2, c1)
                self.dot(x, c2)
            else:  # two on top (near letter), one under
                self.dot(x - (d + g) / 2, c1)
                self.dot(x + (d + g) / 2, c1)
                self.dot(x, c2)
        return self

    def geometry(self):
        g = unary_union(self.shapes)
        return g


def to_polys(g):
    if g.is_empty:
        return []
    if isinstance(g, Polygon):
        return [g]
    if isinstance(g, (MultiPolygon, GeometryCollection)):
        out = []
        for p in g.geoms:
            out += to_polys(p)
        return out
    return []
