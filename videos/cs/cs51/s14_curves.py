from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs51.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load

ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def spoken(n: int) -> str:
    """A whole number below a thousand, as a speaker says it (British: 'one hundred and six')."""
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("" if n % 10 == 0 else "-" + ONES[n % 10])
    rest = n % 100
    return ONES[n // 100] + " hundred" + ("" if rest == 0 else " and " + spoken(rest))


def lerp(a, b, t):
    return (1 - t) * np.asarray(a, float) + t * np.asarray(b, float)


def bspline_span(P, i, ts):
    """Points of span i of a uniform cubic B-spline (control points P[i..i+3]) at local parameters ts."""
    out = []
    for t in ts:
        b = [(1 - t) ** 3 / 6, (3 * t ** 3 - 6 * t ** 2 + 4) / 6, (-3 * t ** 3 + 3 * t ** 2 + 3 * t + 1) / 6,
             t ** 3 / 6]
        out.append(sum(w * np.asarray(P[i + k], float) for k, w in enumerate(b)))
    return out


def rot(yaw, pitch):
    a, b = math.radians(yaw), math.radians(pitch)
    Ry = np.array([[math.cos(a), 0, math.sin(a)], [0, 1, 0], [-math.sin(a), 0, math.cos(a)]])
    Rx = np.array([[1, 0, 0], [0, math.cos(b), -math.sin(b)], [0, math.sin(b), math.cos(b)]])
    return Rx @ Ry


def mesh_mob(V, F, center, scale=0.72, yaw=35, pitch=24, stroke=0.6):
    """A quad mesh drawn with the painter's algorithm and Lambert shading (chapters 3 and 4)."""
    R = rot(yaw, pitch)
    W = np.asarray(V, float) @ R.T
    L = np.array([-0.4, 0.6, 0.7])
    L /= np.linalg.norm(L)
    faces = []
    for f in F:
        q = W[f]
        n = np.cross(q[2] - q[0], q[3] - q[1])
        n /= np.linalg.norm(n) + 1e-12
        if n[2] <= 0:
            continue
        faces.append((q[:, 2].mean(), q, max(0.0, float(n @ L))))
    faces.sort(key=lambda x: x[0])
    g = VGroup()
    for _, q, s in faces:
        pts = [np.array([center[0] + scale * p[0], center[1] + scale * p[1], 0]) for p in q]
        g.add(Polygon(*pts, stroke_color=GREY_E, stroke_width=stroke, fill_color=interpolate_color(
            ManimColor(BG), ManimColor(DATA), 0.25 + 0.7 * s), fill_opacity=1))
    return g


class Curves(VoiceoverScene):
    def construct(self):
        self.card()
        self.casteljau()
        self.bernstein()
        self.bspline()
        self.subdivision()
        self.fonts()

    def card(self):
        card = chapter_card(13, r"Curves, \ surfaces and fonts", r"How do a few numbers draw a smooth shape?",
                            lit=(1959, 1978, 1997), extra=((1959, r"de Casteljau at Citro\"en"),
                                                           (1978, r"Catmull and Clark"),
                                                           (1997, r"\textit{Geri's Game}")), part=PART)
        with self.voiceover("Chapter thirteen. Curves, surfaces and fonts."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ de Casteljau
    def casteljau(self):
        cj = load("casteljau")
        Pts = cj["points"]
        M = lambda p: np.array([-6.2 + 1.3 * p[0], -2.4 + 1.7 * p[1], 0])
        head = label(r"de Casteljau: \ lerp, \ lerp, \ lerp", font_size=36).to_edge(UP, buff=0.3)
        poly = VMobject(color=GREY_B, stroke_width=2.5).set_points_as_corners([M(p) for p in Pts])
        cdots = VGroup(*[Dot(M(p), radius=0.08, color=WHITE) for p in Pts])
        clabs = VGroup(*[MathTex(rf"P_{k}", font_size=28, color=GREY_A).next_to(
            M(p), UP if p[1] > 1 else DOWN, buff=0.12) for k, p in enumerate(Pts)])
        t = ValueTracker(0.3)
        cols = [DATA, YES, HEAD]

        def build():
            tt = t.get_value()
            g = VGroup()
            lvl = [np.asarray(p, float) for p in Pts]
            for c in cols:
                lvl = [lerp(a, b, tt) for a, b in zip(lvl, lvl[1:])]
                if len(lvl) > 1:
                    g.add(VMobject(color=c, stroke_width=2.5).set_points_as_corners([M(p) for p in lvl]))
                g.add(*[Dot(M(p), radius=0.07 if len(lvl) > 1 else 0.11, color=c) for p in lvl])
            return g
        con = always_redraw(build)
        curve_pts = [M(p) for p in cj["curve"]]

        def traced():
            k = max(1, int(round(t.get_value() * (len(curve_pts) - 1))))
            return VMobject(color=HEAD, stroke_width=4).set_points_smoothly(curve_pts[:k + 1])
        tr = always_redraw(traced)
        full = VMobject(color=HEAD, stroke_width=3, stroke_opacity=0.45).set_points_smoothly(curve_pts)
        rd = VGroup(MathTex(r"t =", font_size=32, color=HEAD), DecimalNumber(0.3, num_decimal_places=2,
                                                                             font_size=32, color=HEAD))
        rd.arrange(RIGHT, buff=0.12).move_to([-3.6, 2.3, 0])
        rd[1].add_updater(lambda m: m.set_value(t.get_value()).next_to(rd[0], RIGHT, buff=0.12))
        tab = grid_table([r"$t$", r"$B(t)$, \ from our instrument"],
                         [[f"{s['t']:.2f}", rf"({s['point'][0]:.4g}, \ {s['point'][1]:.4g})"] for s in cj["steps"]],
                         widths=[1.0, 3.6], row_h=0.42, font_size=19, mono_cols=())
        tab.move_to([3.9, 1.7, 0])
        mid = next(s for s in cj["steps"] if s["t"] == 0.5)
        lv = mid["levels"]
        left = [lv_[0] for lv_ in lv]
        right = [lv_[-1] for lv_ in lv][::-1]
        lpoly = VMobject(color=YES, stroke_width=4).set_points_as_corners([M(p) for p in left])
        rpoly = VMobject(color=LAM, stroke_width=4).set_points_as_corners([M(p) for p in right])
        ldots = VGroup(*[Dot(M(p), radius=0.08, color=YES) for p in left])
        rdots = VGroup(*[Dot(M(p), radius=0.08, color=LAM) for p in right])
        notes = VGroup(
            wrapped_label(r"go a fraction $t$ along each leg; \ join the new points; \ repeat until one point is "
                          r"left: \ that point is $B(t)$", 5.0, font_size=19, color=WHITE),
            wrapped_label(r"frozen at $t = \tfrac12$: \ the first points of the levels are the control points of "
                          r"the left half \ (green), \ the last points those of the right half \ (purple)", 5.0,
                          font_size=19, color=WHITE),
            wrapped_label(r"subdivide until each piece is flat, \ then draw lines: \ how renderers draw curves", 5.0,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, DOWN, buff=0.45).align_to(tab, LEFT)
        with self.voiceover(
            "Smooth shapes need curves, and the standard one was found twice, at two car makers: by Paul de "
            "Casteljau at Citroën in 1959, and by Pierre Bézier at Renault, who published it in the 1960s. <bookmark"
            " mark='a'/> Start with four control points. <bookmark mark='b'/> Pick a fraction t. Go that fraction "
            "along each leg of the polygon, and join the new points. Repeat until one point is left: that is the "
            "curve at t. <bookmark mark='c'/> Sweep t from nought to one, and the point draws the whole curve. At "
            "one half, our instrument gives the point two, one point six. <bookmark mark='d'/> The construction "
            "gives more. Frozen at one half, the first points of each level are the control points of the curve's "
            "left half, and the last points those of its right half. <bookmark mark='e'/> Split until every piece is"
            " nearly straight, then draw lines: that is how a renderer draws a curve."
        ) as vo:
            self.play(FadeIn(head), Create(poly), FadeIn(cdots))
            vo.wait_until("a")
            self.play(FadeIn(clabs), Indicate(cdots, color=HEAD))
            vo.wait_until("b")
            self.play(FadeIn(con), FadeIn(rd), FadeIn(notes[0]))
            vo.wait_until("c")
            self.add(tr)
            self.play(t.animate.set_value(0.0), run_time=1)
            self.play(t.animate.set_value(1.0), run_time=4, rate_func=linear)
            self.add(full)
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(t.animate.set_value(0.5), run_time=1.5)
            self.play(Create(lpoly), Create(rpoly), FadeIn(ldots), FadeIn(rdots), FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(FadeIn(notes[2]))
        rd[1].clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Bernstein form
    def bernstein(self):
        head = label(r"The polynomial inside: \ Bernstein", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 1, 0.25], x_length=4.6, y_length=3.4, tips=False,
                  axis_config={"color": GREY_D, "include_ticks": True}).move_to([-4.0, -0.2, 0])
        xt = VGroup(*[label(t, font_size=17, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v, t in ((0, "0"), (0.5, r"$\tfrac12$"), (1, "1"))])
        yt = VGroup(*[label(t, font_size=17, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v, t in ((0, "0"), (1, "1"))])
        xl = label(r"$t$", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.05)
        fns = [(lambda s: (1 - s) ** 3, DATA, r"(1-t)^3"), (lambda s: 3 * (1 - s) ** 2 * s, YES, r"3(1-t)^2t"),
               (lambda s: 3 * (1 - s) * s * s, LAM, r"3(1-t)t^2"), (lambda s: s ** 3, HEAD, r"t^3")]
        curves = VGroup(*[ax.plot(f, x_range=[0, 1, 0.01], color=c, stroke_width=3) for f, c, _ in fns])
        tags = VGroup(*[MathTex(tx, font_size=24, color=c) for _, c, tx in fns]).arrange(RIGHT, buff=0.3).next_to(
            ax, UP, buff=0.3)
        sum1 = DashedLine(ax.c2p(0, 1), ax.c2p(1, 1), color=GREY_A, stroke_width=1.5)
        s1l = label(r"their sum: \ 1", font_size=17, color=GREY_A).next_to(sum1, UP, buff=0.05)
        r0 = MathTex(r"P_{01}", r"=", r"(1-t)\,P_0 + t\,P_1", font_size=32)
        r1 = MathTex(r"B_2(t)", r"=", r"(1-t)\,[(1-t)P_0 + tP_1]", r"+", r"t\,[(1-t)P_1 + tP_2]", font_size=32)
        r2 = MathTex(r"B_2(t)", r"=", r"(1-t)^2P_0", r"+", r"2(1-t)t\,P_1", r"+", r"t^2P_2", font_size=32)
        r3 = MathTex(r"B_3(t)", r"=", r"(1-t)^3P_0 + 3(1-t)^2t\,P_1 + 3(1-t)t^2P_2 + t^3P_3", font_size=32,
                     color=YES)
        nts = [r"one level: \ a linear interpolation", r"two levels: \ lerps of lerps", r"multiply out",
               r"three levels: \ the cubic, \ weights $b_{k,3}(t) = \binom{3}{k}(1-t)^{3-k}t^k$"]
        notes = VGroup(*[note(n, font_size=17, color=YES if i == 3 else GREY_B) for i, n in enumerate(nts)])
        blk = VGroup(*[VGroup(r, n).arrange(DOWN, aligned_edge=LEFT, buff=0.07) for r, n in
                       zip((r0, r1, r2, r3), notes)])
        blk.arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.35).set_y(0.55)
        r2.move_to(r1, aligned_edge=LEFT)
        props = wrapped_label(r"never negative, \ sum to one: \ the curve stays in the convex hull of its points, "
                              r"\ starts and ends on $P_0$ and $P_3$ tangent to the end legs, \ and moving the four "
                              r"points by a matrix moves the curve \ (chapter 1)", 6.4, font_size=19,
                              color=HEAD).to_edge(DOWN, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "What polynomial is the construction computing? <bookmark mark='a'/> One level is a linear "
            "interpolation between two points. <bookmark mark='b'/> Two levels nest them, a lerp of lerps. "
            "<bookmark mark='c'/> Multiply out, and the quadratic weights are one minus t squared, two t times one "
            "minus t, and t squared. <bookmark mark='d'/> Three levels give the cubic, and its four weights are "
            "the Bernstein polynomials. <bookmark mark='e'/> They are never negative and always sum to one. So the "
            "curve stays inside the convex hull of its control points; it starts and ends on the end points, "
            "tangent to the first and last legs; and moving the four points by a matrix moves the curve, so chapter "
            "one's transforms act on control points alone."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl))
            vo.wait_until("a")
            self.play(Write(r0), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Write(r1), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(r1, r2), FadeTransform(notes[1], notes[2].move_to(notes[1],
                                                                                             aligned_edge=LEFT)))
            vo.wait_until("d")
            self.play(Write(r3), FadeIn(notes[3]), LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3),
                      FadeIn(tags), run_time=2.5)
            vo.wait_until("e")
            self.play(Create(sum1), FadeIn(s1l), FadeIn(props))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ B-splines
    def bspline(self):
        rows = load("bspline")["rows"]
        head = label(r"B-splines: \ smooth joins, \ local control", font_size=36).to_edge(UP, buff=0.3)
        ctrl = [(0, 0), (1, 2), (3, 3), (4, 0), (6, -1), (7, 2), (9, 3)]   # the instrument's default control points
        M = lambda p: np.array([-6.3 + 0.6 * p[0], -0.6 + 0.75 * p[1], 0])
        dy = ValueTracker(0.0)
        cols = [DATA, YES, LAM, HEAD]

        def control():
            P = [np.array(p, float) for p in ctrl]
            P[1] = P[1] + np.array([0, dy.get_value()])
            return P

        def drawing():
            P = control()
            g = VGroup(VMobject(color=GREY_C, stroke_width=1.5).set_points_as_corners([M(p) for p in P]),
                       *[Dot(M(p), radius=0.07, color=NO if k == 1 else WHITE) for k, p in enumerate(P)])
            ts = np.linspace(0, 1, 30)
            for i in range(4):
                g.add(VMobject(color=cols[i], stroke_width=5).set_points_smoothly(
                    [M(p) for p in bspline_span(P, i, ts)]))
            for i in range(1, 4):
                g.add(Dot(M(bspline_span(P, i, [0.0])[0]), radius=0.06, color=WHITE))
            return g
        dr = always_redraw(drawing)
        p1l = MathTex(r"P_1", font_size=26, color=NO).add_updater(
            lambda m: m.next_to(M(control()[1]), LEFT, buff=0.12))
        r0 = MathTex(r"C(t) = \sum_i N_{i,3}(t)\,P_i", font_size=32)
        r0n = note(r"Cox and de Boor \ (1972): \ each piece blends four neighbouring points", font_size=17)
        VGroup(r0, r0n).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_edge(RIGHT, buff=0.35).set_y(2.25)

        def sci(v):
            e = int(math.floor(math.log10(abs(v))))
            return rf"$10^{{{e}}}$"
        tab = grid_table([r"knot", r"position", r"slope", r"curvature", r"3rd deriv."],
                         [[f"{r['knot']:.0f}", sci(r["jump_c0"]), sci(r["jump_c1"]), sci(r["jump_c2"]),
                           f"{r['jump_c3']:.2f}"] for r in rows], widths=[0.8, 1.3, 1.3, 1.4, 1.5], row_h=0.42,
                         font_size=19, mono_cols=(), colors=[[WHITE, YES, YES, YES, NO]] * len(rows))
        tcap = label(r"jump across each knot, \ measured by our instrument", font_size=17, color=GREY_A)
        tblk = VGroup(tcap, tab).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.45).set_x(-2.6)
        notes = VGroup(
            wrapped_label(r"$C^2$: \ position, \ slope and curvature continuous at every knot \ (jumps at "
                          r"rounding level); \ only the third derivative jumps", 4.2, font_size=19, color=YES),
            wrapped_label(r"local: \ moving $P_1$ changes only the two pieces that use it", 4.2, font_size=19,
                          color=NO),
            wrapped_label(r"with weights and uneven knots: \ NURBS, \ the curves of CAD", 4.2, font_size=19,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).set_y(-1.6)
        with self.voiceover(
            "Long curves are made of many pieces, and joining Bézier pieces smoothly takes care at every joint. "
            "B-splines build the smoothness in. <bookmark mark='a'/> A cubic B-spline makes each piece from four "
            "neighbouring control points, with weights from the recursion that Maurice Cox and Carl de Boor "
            "published in 1972. Here, seven points make four pieces. <bookmark mark='b'/> Our instrument measures "
            "the joins. At each knot the position, the slope and the curvature agree to rounding error, about ten to the "
            "minus ten; only the third derivative jumps. The curve is C two. <bookmark mark='c'/> And "
            "control is local: move one point, and only the pieces that use it change. <bookmark mark='d'/> Add "
            "weights and uneven knots, and these become NURBS, the curves of computer-aided design."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(dr), FadeIn(p1l), Write(r0), FadeIn(r0n))
            vo.wait_until("b")
            self.play(FadeIn(tblk), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            self.play(dy.animate.set_value(-1.6), run_time=2)
            self.play(dy.animate.set_value(0.8), run_time=2)
            self.play(dy.animate.set_value(0.0), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        p1l.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Catmull-Clark
    def subdivision(self):
        sd = load("subdiv")
        levels = sd["levels"]
        head = label(r"Catmull--Clark: \ surfaces by subdivision", font_size=36).to_edge(UP, buff=0.3)
        xs = [-5.2, -1.75, 1.75, 5.2]
        meshes = VGroup(*[mesh_mob(levels[k]["vertices"], levels[k]["faces"], (xs[k], 1.0),
                                   stroke=0.8 if k < 3 else 0.4) for k in range(4)])
        caps = VGroup(*[label(rf"level {k}: \ {levels[k]['F']} faces", font_size=18, color=GREY_A).next_to(
            meshes[k], DOWN, buff=0.15) for k in range(4)])
        caps.set_y(min(c.get_y() for c in caps))
        tab = grid_table([r"level", r"$V$", r"$E$", r"$F$", r"$V - E + F$", r"corner distance"],
                         [[f"{l['level']}", f"{l['V']:,}".replace(",", "{,}"), f"{l['E']:,}".replace(",", "{,}"),
                           f"{l['F']:,}".replace(",", "{,}"), f"{l['euler']}", f"{l['corner_radius']:.4f}"]
                          for l in levels], widths=[0.8, 0.8, 0.8, 0.8, 1.3, 1.7], row_h=0.36, font_size=18,
                         mono_cols=())
        lim = label(rf"limit \ (Halstead et al. 1993): \ {sd['limit_radius']:.4f}", font_size=18, color=YES)
        VGroup(tab, lim).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DL, buff=0.4)
        rules = VGroup(
            MathTex(r"\text{face point} = \text{mean of the face's vertices}", font_size=26),
            MathTex(r"\text{edge point} = \tfrac14\,(V_a + V_b + F_1 + F_2)", font_size=26),
            MathTex(r"P' = \frac{F + 2R + (n-3)\,P}{n}", font_size=28, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        rn = note(r"$F$, $R$: \ means of the adjacent face points and edge midpoints; \ $n$: \ the valence",
                  font_size=16)
        VGroup(rules, rn).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DR, buff=0.4)
        with self.voiceover(
            "Surfaces follow the same idea. In 1978 Edwin Catmull and Jim Clark gave rules that refine any mesh of "
            "polygons. <bookmark mark='a'/> Each face gets a point at its centre; each edge gets a point averaged "
            "from its two ends and its two faces; <bookmark mark='b'/> and each old vertex moves towards a weighted "
            "average of its neighbours. Every face becomes quadrilaterals. <bookmark mark='c'/> Applied to a cube, "
            "each step multiplies the faces by four, while vertices minus edges plus faces stays two: the surface "
            "keeps a sphere's topology. <bookmark mark='d'/> The corners pull in, from one point seven three "
            "towards nought point eight six six, the limit an exact formula predicts. <bookmark mark='e'/> The "
            "limit surface is smooth almost everywhere, and Pixar first animated a character with such surfaces "
            "in its short film Geri's Game, in 1997."
        ) as vo:
            self.play(FadeIn(head), FadeIn(meshes[0]), FadeIn(caps[0]))
            vo.wait_until("a")
            self.play(FadeIn(rules[0]), FadeIn(rules[1]))
            vo.wait_until("b")
            self.play(FadeIn(rules[2]), FadeIn(rn))
            self.play(FadeIn(meshes[1]), FadeIn(caps[1]))
            vo.wait_until("c")
            self.play(FadeIn(meshes[2]), FadeIn(caps[2]))
            self.play(FadeIn(meshes[3]), FadeIn(caps[3]), FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(lim), Indicate(VGroup(*[r[-1] for r in tab.cells[1:]]), color=HEAD))
            vo.wait_until("e")
            self.play(Indicate(meshes[3], scale_factor=1.05, color=HEAD))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the letters on this screen
    def fonts(self):
        head = label(r"Every letter here is B\'ezier curves", font_size=36).to_edge(UP, buff=0.3)
        from explainer.zh_text import verbatim
        with verbatim():  # the word is the specimen whose curves are counted: it stays as written
            word = Tex(r"Light", font_size=210, color=WHITE).move_to([-3.0, -0.2, 0])
        outline = word.copy().set_fill(opacity=0).set_stroke(color=WHITE, width=2)
        anchors, handles, legs = VGroup(), VGroup(), VGroup()
        n_word = 0
        for m in word.get_family():
            pts = m.points
            if len(pts) < 4:
                continue
            n_word += len(pts) // 4
            for k in range(0, len(pts) - 3, 4):
                a0, h0, h1, a1 = pts[k], pts[k + 1], pts[k + 2], pts[k + 3]
                anchors.add(Dot(a0, radius=0.045, color=HEAD))
                straight = np.linalg.norm(np.cross(a1 - a0, h0 - a0)) < 1e-6 and np.linalg.norm(
                    np.cross(a1 - a0, h1 - a0)) < 1e-6
                if not straight:
                    for a, h in ((a0, h0), (a1, h1)):
                        legs.add(Line(a, h, color=DATA, stroke_width=1.2))
                        handles.add(Square(side_length=0.07, color=DATA, stroke_width=1.5).move_to(h))
        n_head = sum(len(m.points) // 4 for m in head.get_family() if len(m.points) >= 4)
        notes = VGroup(
            wrapped_label(r"dots: \ anchor points; \ squares: \ control handles; \ a straight stroke is a curve "
                          r"with its handles on the line", 4.6, font_size=19, color=WHITE),
            wrapped_label(rf"this word: \ {n_word} cubic curves; \ the heading above: \ {n_head}, \ counted "
                          r"from the shapes on screen", 4.6, font_size=19, color=HEAD),
            wrapped_label(r"PostScript and TeX's Type 1 fonts store cubics; \ TrueType stores quadratics", 4.6,
                          font_size=19, color=DATA),
            wrapped_label(r"to draw a letter: \ fill the outline by its winding number, \ and average coverage "
                          r"within each pixel \ (chapter 5's anti-aliasing)", 4.6, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).set_y(-0.2)
        with self.voiceover(
            "And curves are in front of you now. <bookmark mark='a'/> Every letter in this series is an outline "
            "made of Bézier curves. Here is the word Light, as Manim draws it from TeX's fonts. "
            "<bookmark mark='b'/> The dots are the anchor points where curves meet, and the squares are the "
            "control handles; a straight stroke is simply a curve whose handles lie on the line. "
            f"<bookmark mark='c'/> This word is {spoken(n_word)} cubic curves, and the heading above it is "
            f"{spoken(n_head)}. <bookmark mark='d'/> PostScript, and the fonts TeX uses, store cubic curves; "
            "TrueType stores quadratics. <bookmark mark='e'/> To draw a letter, a rasterizer fills the outline by "
            "its winding number, and averages the coverage within each pixel: chapter five's anti-aliasing, so "
            "that curves look smooth on a grid of samples."
        ) as vo:
            self.play(FadeIn(head), FadeIn(word))
            vo.wait_until("a")
            self.play(word.animate.set_fill(opacity=0.12), Create(outline), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(anchors), FadeIn(legs), FadeIn(handles), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]), Indicate(head, color=HEAD, scale_factor=1.05))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(FadeIn(notes[3]), word.animate.set_fill(opacity=1))
        self.wait(0.6)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
