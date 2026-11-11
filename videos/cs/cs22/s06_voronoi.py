from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.algo import geometry as G
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)

BOX = (-7.4, -4.2, 7.4, 4.2)          # data coordinates of the drawing box
SC = 0.62
ORG = np.array([-2.25, -0.35, 0])


def S(p):
    return ORG + np.array([p[0] * SC, p[1] * SC, 0])


def _clip(a, b, box=BOX):
    """Liang-Barsky: the part of segment ab inside the box, or None."""
    x0, y0, x1, y1 = box
    t0, t1 = 0.0, 1.0
    dx, dy = b[0] - a[0], b[1] - a[1]
    for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
        if p == 0:
            if q < 0:
                return None
            continue
        t = q / p
        if p < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
    if t0 > t1:
        return None
    return (a[0] + t0 * dx, a[1] + t0 * dy), (a[0] + t1 * dx, a[1] + t1 * dy)


def voronoi_edges(sites, tris):
    """Voronoi edges from the Delaunay triangles: between circumcentres of triangles sharing an edge, and rays from
    hull triangles.  Returns [(a, b, (site i, site j))] in data coordinates, clipped to the box."""
    cc = {t: G._circumcircle(sites[t[0]], sites[t[1]], sites[t[2]])[:2] for t in tris}
    by_edge = {}
    for t in tris:
        for i, j in ((t[0], t[1]), (t[1], t[2]), (t[0], t[2])):
            by_edge.setdefault((min(i, j), max(i, j)), []).append(t)
    out = []
    for (i, j), ts in by_edge.items():
        if len(ts) == 2:
            seg = _clip(cc[ts[0]], cc[ts[1]])
        else:
            t = ts[0]
            k = next(x for x in t if x not in (i, j))
            a, b, c = np.array(sites[i]), np.array(sites[j]), np.array(sites[k])
            m = (a + b) / 2
            d = np.array([-(b - a)[1], (b - a)[0]])
            if np.dot(d, c - m) > 0:
                d = -d
            o = np.array(cc[t])
            seg = _clip(tuple(o), tuple(o + d / np.linalg.norm(d) * 40))
        if seg is not None:
            out.append((seg[0], seg[1], (i, j)))
    return out


class Voronoi(VoiceoverScene):
    def construct(self):
        self.card()
        self.diagram()
        self.fortune()
        self.measured()

    def card(self):
        card = chapter_card(5, r"Voronoi diagrams", r"Which post office is nearest?", lit=(1908, 1986),
                            extra=((1908, r"Vorono\"i"), (1986, r"Fortune's sweep")), part=PART)
        with self.voiceover("Chapter five. Voronoi diagrams."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def diagram(self):
        d = load("voronoi")
        sites = [tuple(s) for s in d["sites"]]
        tris = [tuple(t) for t in d["tris"]]
        head = label(r"The Voronoi diagram", font_size=34).to_edge(UP, buff=0.3)
        frame = Rectangle(width=(BOX[2] - BOX[0]) * SC, height=(BOX[3] - BOX[1]) * SC, color=GREY_D,
                          stroke_width=1).move_to(S(((BOX[0] + BOX[2]) / 2, (BOX[1] + BOX[3]) / 2)))
        sd = VGroup(*[Dot(S(s), radius=0.07, color=HEAD) for s in sites])
        edges = VGroup(*[Line(S(a), S(b), color=DATA, stroke_width=2.2) for a, b, _ in voronoi_edges(sites, tris)])
        verts = VGroup(*[Dot(S((v[0], v[1])), radius=0.045, color=LAM) for v in d["vertices"]
                         if BOX[0] < v[0] < BOX[2] and BOX[1] < v[1] < BOX[3]])
        side = VGroup(
            label(r"$n$ sites; \ each region holds \\ the points nearest to its site", font_size=21, color=WHITE),
            label(r"edges: \ equidistant from two sites", font_size=21, color=DATA),
            label(r"vertices: \ from three, \ the centre \\ of an empty circle", font_size=21, color=LAM),
            label('general position, $n\\ge3$: \\\\ at most $2n-5$ vertices, $3n-6$ edges', font_size=21, color=YES),
            label(r"Dirichlet (1850), \ Vorono\"i (1908); \\ Snow's cholera map (1854)", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        if side.width > 4.0:
            side.width = 4.0
            side.to_edge(RIGHT, buff=0.3)
        q = np.array([1.2, -1.3])
        near = min(range(len(sites)), key=lambda i: np.hypot(*(np.array(sites[i]) - q)))
        qd = Dot(S(q), radius=0.08, color=WHITE)
        ql = DashedLine(S(q), S(sites[near]), color=WHITE, stroke_width=1.5)
        with self.voiceover(
            "Scatter n distinct sites over the plane. Which site is nearest to each point? <bookmark mark='a'/> The Voronoi regions answer that question. <bookmark mark='b'/> A shared edge lies on two sites' perpendicular bisector. <bookmark mark='c'/> In general position, a vertex is the centre of an empty circle through three sites. Cocircular and collinear inputs need separate conventions. <bookmark mark='d'/> For at least three noncollinear sites, Euler gives at most two n minus five finite vertices and three n minus six edges. <bookmark mark='e'/> Dirichlet and Voronoi studied this partition. Nearest-pump regions also offer a geometric interpretation of Snow's cholera investigation; the historical map itself is not a computed Voronoi diagram."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(sd))
            self.play(FadeIn(qd), Create(ql))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.04), FadeIn(side[0]), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(edges, color=WHITE))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(verts))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    def fortune(self):
        d = load("voronoi")
        sites = [tuple(s) for s in d["sites"]]
        tris = [tuple(t) for t in d["tris"]]
        edges = voronoi_edges(sites, tris)
        vev = []
        for v in d["vertices"]:
            a = sites[v[2][0]]
            r = float(np.hypot(a[0] - v[0], a[1] - v[1]))
            vev.append((v[0], v[1], v[1] - r))
        head = label(r"Fortune's sweep: \ a beach line of parabolas", font_size=32).to_edge(UP, buff=0.3)
        frame = Rectangle(width=(BOX[2] - BOX[0]) * SC, height=(BOX[3] - BOX[1]) * SC, color=GREY_D,
                          stroke_width=1).move_to(S(((BOX[0] + BOX[2]) / 2, (BOX[1] + BOX[3]) / 2)))
        sd = VGroup(*[Dot(S(s), radius=0.07, color=HEAD) for s in sites])
        L = ValueTracker(BOX[3] - 0.05)
        xs = np.linspace(BOX[0], BOX[2], 361)

        def sweep_line():
            y = L.get_value()
            return Line(S((BOX[0], y)), S((BOX[2], y)), color=NO, stroke_width=2.5)

        def beach():
            y = L.get_value()
            ys = G.beach_line(sites, y, xs)
            pts = [S((x, min(v, BOX[3]))) for x, v in zip(xs, ys) if np.isfinite(v)]
            if len(pts) < 2:
                return VMobject()
            return VMobject(color=YES, stroke_width=3).set_points_as_corners(pts)

        ts = np.linspace(0, 1, 41)
        samp = np.array([[(a_[0] + t * (b_[0] - a_[0]), a_[1] + t * (b_[1] - a_[1])) for t in ts] for a_, b_, _ in edges])

        def done_edges():
            y = L.get_value()
            by = G.beach_line(sites, y, samp[:, :, 0].ravel()).reshape(samp.shape[:2])
            ok = samp[:, :, 1] >= by - 1e-9
            g = VGroup()
            for k in range(len(samp)):
                run = []
                for t in range(len(ts)):
                    if ok[k, t]:
                        run.append(S(samp[k, t]))
                    else:
                        if len(run) >= 2:
                            g.add(VMobject(color=DATA, stroke_width=2.2).set_points_as_corners(run))
                        run = []
                if len(run) >= 2:
                    g.add(VMobject(color=DATA, stroke_width=2.2).set_points_as_corners(run))
            return g

        def done_verts():
            y = L.get_value()
            return VGroup(*[Dot(S((vx, vy)), radius=0.05, color=LAM) for vx, vy, ey in vev if ey >= y
                            and BOX[0] < vx < BOX[2] and BOX[1] < vy < BOX[3]])
        sl = always_redraw(sweep_line)
        bl = always_redraw(beach)
        de = always_redraw(done_edges)
        dv = always_redraw(done_verts)
        side = VGroup(
            label(r"the sweep line moves down", font_size=21, color=NO),
            label(r"points equally far from a site \\ and the line: \ a \textbf{parabola}", font_size=21, color=WHITE),
            label(r"the \textbf{beach line}: \ their lower envelope; \\ above it, \ the diagram is final", font_size=21,
                  color=YES),
            label(r"breakpoints trace the edges", font_size=21, color=DATA),
            label(r"\textbf{site event}: \ a new arc appears", font_size=21, color=HEAD),
            label(r"\textbf{circle event}: \ an arc shrinks to nothing: \\ a vertex, \ the centre of an empty circle",
                  font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.3)
        if side.width > 4.2:
            side.width = 4.2
            side.to_edge(RIGHT, buff=0.3)
        ymin = min(min(e for _, _, e in vev), min(s[1] for s in sites)) - 0.3
        with self.voiceover(
            "Steven Fortune found, in 1986, a way to build the diagram with a sweep. The difficulty is that a line "
            "sweeping down meets a Voronoi region before it meets the region's site, so it cannot know yet what lies "
            "below. <bookmark mark='a'/> Fortune's answer: consider the points that are as close to a site above the "
            "line as to the line itself. For each site, they form a parabola. <bookmark mark='b'/> The lowest of "
            "these parabolas form the beach line. Any point above it is closer to some site than to the sweep line, "
            "so no site still below the line can claim it: above the beach line, the diagram is final. <bookmark "
            "mark='c'/> As the line moves, the breakpoints where arcs meet slide along Voronoi edges and draw them. "
            "<bookmark mark='d'/> When the line reaches a site, a new arc is born, a thin spike that widens. "
            "<bookmark mark='e'/> When an arc shrinks to nothing between its neighbours, three sites are equally far "
            "from one point and from the line: that point is a Voronoi vertex, and the line touches the bottom of "
            "the empty circle through the three sites. <bookmark mark='f'/> Those are the only two events, so with "
            "a balanced tree for the beach line the sweep takes n log n."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(sd))
            self.add(sl)
            self.play(FadeIn(side[0]))
            vo.wait_until("a")
            self.add(bl, de, dv)
            self.play(FadeIn(side[1]), L.animate.set_value(1.2), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(side[2]), L.animate.set_value(0.2), run_time=3.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(side[3]), L.animate.set_value(-1.0), run_time=4.0, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(side[4]), L.animate.set_value(-2.0), run_time=4.0, rate_func=linear)
            vo.wait_until("e")
            self.play(FadeIn(side[5]), L.animate.set_value(-3.0), run_time=4.0, rate_func=linear)
            vo.wait_until("f")
            self.play(L.animate.set_value(max(ymin, BOX[1] + 0.1)), run_time=5.0, rate_func=linear)
        self.wait(0.3)
        for m in (sl, bl, de, dv):
            m.clear_updaters()
        self.clear_scene()

    def measured(self):
        d = load("voronoi")
        head = label(r"Our sweep, \ against the lifting map", font_size=32).to_edge(UP, buff=0.35)
        rows = [[words(r["n"]), words(r["site"]), words(r["circle"]), words(r["expected"]), words(r["false"]),
                 f"{r['seconds'] * 1000:.0f} ms", r"yes" if r["match"] else r"NO"] for r in d["rows"]]
        tab = grid_table([r"sites $n$", r"site events", r"circle events", r"$2n - 2 - h$", r"false alarms", r"time",
                          r"Delaunay agrees"], rows, widths=[1.6, 1.9, 2.0, 1.9, 1.9, 1.4, 2.4], row_h=0.5,
                         font_size=21, mono_cols=(), colors=[[WHITE, HEAD, LAM, LAM, NO, GREY_A, YES]] * len(rows))
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        notes = VGroup(
            label(r"every vertex is one circle event, \ and there are exactly $2n - 2 - h$ \ ($h$ on the hull)",
                  font_size=22, color=LAM),
            label(r"false alarms: \ circle events cancelled because a new arc arrived first", font_size=22, color=NO),
            label(r"each vertex's three sites form a \textbf{Delaunay} triangle: \ checked against chapter 7's method",
                  font_size=22, color=YES),
            label(r"our beach line is a plain list: \ $O(n^2)$ here, \ $O(n \log n)$ with a balanced tree", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.28).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Our finite-precision sweep keeps the beach line in a plain list. We ran it on seeded random sites up to two thousand. <bookmark mark='a'/> On these nondegenerate inputs, circle events match two n minus two minus h, with h hull sites. <bookmark mark='b'/> Cancelled event predictions count as false alarms. <bookmark mark='c'/> Every output triangle set agrees with a separate Qhull construction after timing. This is full numerical agreement on these inputs, not an exact-arithmetic proof for all inputs. <bookmark mark='d'/> The list implementation can take quadratic time. The balanced-tree Fortune algorithm has the n log n bound under its event and arithmetic assumptions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3))
            for mk, nt in zip("abcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(nt))
        self.wait(0.3)
        self.clear_scene()
