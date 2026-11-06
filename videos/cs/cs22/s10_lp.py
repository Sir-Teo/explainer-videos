from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)

SC = 0.95
ORG = np.array([-2.9, -0.45, 0])
BOX = 6.0
VIEW = 2.8


def S(p):
    return ORG + np.array([p[0] * SC, p[1] * SC, 0])


def clip_poly(poly, h):
    """Sutherland-Hodgman: the part of a convex polygon with a1 x + a2 y <= b."""
    a1, a2, b = h
    out = []
    n = len(poly)
    for k in range(n):
        p, q = poly[k], poly[(k + 1) % n]
        fp, fq = a1 * p[0] + a2 * p[1] - b, a1 * q[0] + a2 * q[1] - b
        if fp <= 0:
            out.append(p)
        if fp * fq < 0:
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def hline(h, color, width=2.0):
    """The boundary line of a half-plane, clipped to the view."""
    a1, a2, b = h
    p0 = np.array([a1 * b, a2 * b])
    d = np.array([-a2, a1])
    pts = [p0 + t * d for t in (-8, 8)]
    sq = [(-VIEW, -VIEW), (VIEW, -VIEW), (VIEW, VIEW), (-VIEW, VIEW)]
    seg = []
    for k in range(4):
        u, v = np.array(sq[k]), np.array(sq[(k + 1) % 4])
        M = np.array([pts[1] - pts[0], u - v]).T
        if abs(np.linalg.det(M)) < 1e-12:
            continue
        t, s = np.linalg.solve(M, u - pts[0])
        if 0 <= s <= 1:
            seg.append(pts[0] + t * (pts[1] - pts[0]))
    if len(seg) < 2:
        return VMobject()
    return Line(S(seg[0]), S(seg[1]), color=color, stroke_width=width)


class Lp(VoiceoverScene):
    def construct(self):
        self.card()
        self.seidel()
        self.analysis()
        self.circle()

    def card(self):
        card = chapter_card(9, r"Linear programming in the plane", r"Where is the best point of a polygon?",
                            lit=(1984, 1991), extra=((1984, r"Megiddo"), (1991, r"Seidel")), part=PART)
        with self.voiceover("Chapter nine. Linear programming in the plane."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def seidel(self):
        d = load("lp")
        H = [tuple(h) for h in d["H"]]
        c = d["c"]
        head = label(r"Seidel's algorithm: \ add the constraints in random order", font_size=30).to_edge(UP, buff=0.3)
        frame = Square(side_length=2 * VIEW * SC, color=GREY_D, stroke_width=1).move_to(S((0, 0)))
        region = [(-VIEW, -VIEW), (VIEW, -VIEW), (VIEW, VIEW), (-VIEW, VIEW)]
        reg = Polygon(*[S(p) for p in region], stroke_width=0).set_fill(DATA, 0.18)
        cvec = Arrow(S((-2.4, -2.4)), S((-2.4 + c[0], -2.4 + c[1])), buff=0, color=HEAD, stroke_width=4)
        clab = MathTex(r"c", font_size=28, color=HEAD).next_to(cvec, RIGHT, buff=0.08)
        opt = Dot(S((VIEW - 0.05, VIEW - 0.05)), radius=0.1, color=HEAD)
        side = VGroup(
            label(r"maximize $c \cdot x$ \ subject to $a_i \cdot x \le b_i$", font_size=22, color=WHITE),
            label(r"keep the optimum of the constraints so far", font_size=22, color=HEAD),
            label(r"a new constraint it satisfies: \ nothing to do", font_size=22, color=YES),
            label(r"one it violates: \ the new optimum lies \textbf{on} its line: \\ a 1D problem over the earlier "
                  r"constraints, \ $O(i)$", font_size=22, color=NO),
            label(r"(Part 23 builds the simplex method, \\ for many dimensions)", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        if side.width > 5.4:
            side.width = 5.4
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "A linear program asks for the point of a convex region that goes furthest in a given direction. "
            "<bookmark mark='a'/> In the plane the region is an intersection of half-planes, and the direction is a "
            "vector c. Part 23 builds the simplex method for thousands of dimensions; in two, Raimund Seidel's "
            "algorithm from 1991 fits in a dozen lines. <bookmark mark='b'/> Add the constraints one at a time, in "
            "random order, keeping the optimum of those seen so far. <bookmark mark='c'/> If the current optimum "
            "satisfies the new constraint, nothing changes. <bookmark mark='d'/> If it violates it, the new optimum "
            "must lie on the new constraint's line, and finding it there is a one-dimensional problem: intersect "
            "the line with the earlier constraints, an interval, and take the better end. Watch: of nine "
            "constraints, only three move the optimum."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(reg))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), GrowArrow(cvec), FadeIn(clab), FadeIn(side[4]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(opt))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            prev = None
            lines = []
            for step in d["trace"]:
                h = H[step["added"]]
                region = clip_poly(region, h)
                ln = hline(h, LAM)
                lines.append(ln)
                x = step["x"]
                moved = prev is None or np.hypot(x[0] - prev[0], x[1] - prev[1]) > 1e-6
                newreg = Polygon(*[S(p) for p in region], stroke_width=0).set_fill(DATA, 0.18)
                self.play(Create(ln), Transform(reg, newreg), run_time=0.6)
                if moved:
                    self.play(ln.animate.set_color(NO), opt.animate.move_to(S(x)), run_time=0.7)
                    self.play(ln.animate.set_color(LAM), run_time=0.2)
                else:
                    self.play(Indicate(ln, color=YES), run_time=0.5)
                prev = x
            self.play(Flash(opt.get_center(), color=HEAD))
        self.wait(0.3)
        self.clear_scene()

    def analysis(self):
        d = load("lp")
        head = label(r"Why random order makes it linear", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"backwards again: \ the optimum of $i$ constraints is fixed by \textbf{two} of them", font_size=22,
                  color=WHITE),
            MathTex(r"\Pr[\text{the $i$-th constraint moved it}] \le \frac{2}{i} \qquad \Rightarrow \qquad "
                    r"\mathbb{E}[\text{work}] \le \sum_{i} \frac{2}{i}\, O(i) = O(n)", font_size=32, color=YES),
            label(r"in $d$ dimensions: \ $O(d!\, n)$; \ Megiddo (1984): \ linear for every fixed $d$, \ deterministically",
                  font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.4)
        rows = [[words(r["n"]), f"{r['recompute']:.1f}", f"{r['bound']:.1f}", f"{r['work_per_n']:.2f}",
                 r"yes" if r["ok"] else (r"---" if r["ok"] is None else r"NO")] for r in d["rows"]]
        tab = grid_table([r"constraints $n$", r"times the optimum moved", r"$2 H_n$", r"1D work per constraint",
                          r"same as scipy"], rows, widths=[2.4, 3.4, 1.6, 3.2, 2.2], row_h=0.44, font_size=21,
                         mono_cols=(), colors=[[WHITE, NO, GREY_A, YES, YES]] * len(rows))
        tab.next_to(lines, DOWN, buff=0.4).set_x(0)
        with self.voiceover(
            "How much does this cost? <bookmark mark='a'/> Backwards analysis once more. After i constraints, the "
            "optimum is a corner where two constraint lines meet. The i-th constraint, a random one of the i, moved "
            "the optimum only if it is one of those two. <bookmark mark='b'/> That happens with probability at most "
            "two over i, and then costs order i. Summed, the expected work is linear. <bookmark mark='c'/> We ran it "
            "on up to a hundred thousand random constraints. The optimum moved about as often as two times the "
            "harmonic number predicts, twenty-three times among a hundred thousand constraints, and the total "
            "one-dimensional work came to fewer than three steps per constraint, falling as n grew. In d dimensions the same algorithm takes "
            "d factorial times n, and Nimrod Megiddo showed in 1984 that linear time is possible deterministically "
            "for any fixed dimension."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def circle(self):
        d = load("welzl")
        P = [tuple(p) for p in d["P"]]
        steps = d["steps"]
        s_ = 1.15
        O = np.array([-3.0, -0.4, 0])

        def T(p):
            return O + np.array([p[0] * s_, p[1] * s_, 0])
        head = label(r"The same idea: \ the smallest enclosing circle", font_size=32).to_edge(UP, buff=0.3)
        dots_ = VGroup(*[Dot(T(p), radius=0.06, color=GREY_B) for p in P])
        circ = Circle(radius=0.01, color=HEAD, stroke_width=2.5).move_to(T(P[0]))
        rows = [[words(r["n"]), words(r["rebuilt"]), f"{3 * r['ln_n']:.0f}", f"{r['seconds'] * 1000:.1f} ms"]
                for r in d["rows"]]
        tab = grid_table([r"points", r"rebuilt", r"$3 \ln n$", r"time"], rows, widths=[1.7, 1.3, 1.3, 1.6],
                         row_h=0.42, font_size=19, mono_cols=(), colors=[[WHITE, NO, GREY_A, YES]] * len(rows))
        side = VGroup(
            label(r"add the points in random order; \\ if a point is outside the circle, \\ the new circle passes "
                  r"\textbf{through} it", font_size=21, color=WHITE),
            label(r"then the same question one level down, \\ with one point fixed, \ then two", font_size=21,
                  color=LAM),
            label(r"a circle is fixed by three points: \\ the $i$-th breaks it with probability $\le 3/i$", font_size=21,
                  color=YES),
            tab,
            label(r"Welzl (1991): \ expected $O(n)$; \\ Megiddo (1983): \ deterministic $O(n)$", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 5.8:
            side.width = 5.8
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "The same trick solves a different problem: the smallest circle that encloses a set of points, where to "
            "put one radio mast to cover a set of houses. <bookmark mark='a'/> Add the points in random order. While "
            "a new point is inside the current circle, nothing changes. When it falls outside, the new smallest "
            "circle must pass through it. <bookmark mark='b'/> Finding that circle is the same problem one level "
            "down, with one point fixed on the boundary, and then two. <bookmark mark='c'/> A circle is fixed by at "
            "most three points, so backwards analysis says the i-th point breaks it with probability at most three "
            "over i. <bookmark mark='d'/> We counted: a hundred thousand points rebuilt the circle only twenty-nine "
            "times, within three times the natural logarithm, and the whole computation took half a second in "
            "Python. <bookmark mark='e'/> Emo Welzl's algorithm runs in expected linear time, and Megiddo had found "
            "a deterministic one in 1983."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dots_))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(circ))
            prev = None
            for k, (cx, cy, r) in enumerate(steps):
                if prev is not None and abs(r - prev) < 1e-9:
                    continue
                new = Circle(radius=max(r * s_, 0.01), color=HEAD, stroke_width=2.5).move_to(T((cx, cy)))
                self.play(Transform(circ, new), Indicate(dots_[k + 1], color=NO, scale_factor=1.8), run_time=0.6)
                prev = r
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()
