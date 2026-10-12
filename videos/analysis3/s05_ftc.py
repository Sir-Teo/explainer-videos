from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis3.common import load, plain_axes, polyline


def fstep(x):
    """A function with one jump at 1.5: 0.5 + 0.3 sin(2x) before, 1.4 - 0.2 x after."""
    x = np.asarray(x, float)
    return np.where(x < 1.5, 0.5 + 0.3 * np.sin(2 * x), 1.4 - 0.2 * x)


def Fstep(x):
    x = np.asarray(x, float)
    a = 0.5 * np.minimum(x, 1.5) + 0.15 * (1 - np.cos(2 * np.minimum(x, 1.5)))
    b = np.where(x > 1.5, 1.4 * (x - 1.5) - 0.1 * (x * x - 2.25), 0.0)
    return a + b


class FTC(VoiceoverScene):
    def construct(self):
        self.card()
        self.running()
        self.theorem()
        self.length()
        self.koch()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(4, r"The fundamental theorem, and the length of a curve",
                            r"Why do derivatives undo integrals?", lit=(), part=3)
        with self.voiceover(
            "Chapter four: why integration and differentiation undo each other, and what it means for a curve to have "
            "a length."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def running(self):
        ax = plain_axes([0, 3, 1], [0, 1.6, 0.5], 6.2, 2.6).move_to([-3.3, 1.35, 0])
        bx = plain_axes([0, 3, 1], [0, 2.6, 1], 6.2, 2.6).move_to([-3.3, -2.0, 0])
        gf = VGroup(ax.plot(fstep, x_range=[0, 1.499, 0.005], color=C.FUNC, stroke_width=4),
                    ax.plot(fstep, x_range=[1.5, 3, 0.005], color=C.FUNC, stroke_width=4))
        fl = MathTex(r"f", font_size=32, color=C.FUNC).next_to(ax.c2p(0.2, fstep(0.2)), UP, buff=0.15)
        xT = ValueTracker(0.05)
        area = always_redraw(lambda: ax.get_area(gf[0], x_range=[0, min(xT.get_value(), 1.499)], color=C.FUNC,
                                                 opacity=0.35) if xT.get_value() <= 1.5 else
                             VGroup(ax.get_area(gf[0], x_range=[0, 1.499], color=C.FUNC, opacity=0.35),
                                    ax.get_area(gf[1], x_range=[1.5, xT.get_value()], color=C.FUNC, opacity=0.35)))
        xx = np.linspace(0, 3, 600)
        Fg = always_redraw(lambda: polyline(bx, xx[xx <= xT.get_value()], Fstep(xx[xx <= xT.get_value()]),
                                            color=C.EPS, stroke_width=4) if xT.get_value() > 0.02 else VMobject())
        Fdot = always_redraw(lambda: Dot(bx.c2p(xT.get_value(), float(Fstep(np.array([xT.get_value()]))[0])),
                                         radius=0.07, color=C.EPS))

        def tangent():
            x0 = xT.get_value()
            s = float(fstep(np.array([x0]))[0])
            y0 = float(Fstep(np.array([x0]))[0])
            return Line(bx.c2p(x0 - 0.35, y0 - 0.35 * s), bx.c2p(x0 + 0.35, y0 + 0.35 * s), color=WHITE, stroke_width=2.5)

        tan = always_redraw(tangent)
        Fl = MathTex(r"F(x) = \int_a^x f(t)\,dt", font_size=32, color=C.EPS).next_to(bx, UP, buff=0.05).shift(RIGHT * 1.3)
        side = VGroup(
            label(r"\textbf{Rudin 6.20}", font_size=28),
            MathTex(r"|F(y) - F(x)| \le M\,|y - x|", font_size=32),
            label(r"so $F$ is continuous, \ even where $f$ jumps", font_size=24, color=GREY_A),
            MathTex(r"F'(x_0) = f(x_0) \ \text{where } f \text{ is continuous}", font_size=30, color=C.EPS),
            label(r"the slope of $F$ is the height of $f$", font_size=24, color=GREY_A),
            label(r"at the jump, \ $F$ has a corner", font_size=24, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.5, 0.0, 0])
        assert abs(float(Fstep(np.array([3.0]))[0]) - (0.75 + 0.15 * (1 - np.cos(3.0)) + 1.4 * 1.5 - 0.1 * (9 - 2.25))) < 1e-12
        with self.voiceover(
            "Start with an integrable function f, and let capital F of x be the area under f from a up to x. "
            "<bookmark mark='a'/> As x moves right, F grows by the area swept. <bookmark mark='b'/> If f is bounded by "
            "M, a step of h changes the area by at most M times h, so F is continuous, even across a jump of f. "
            "<bookmark mark='c'/> More: wherever f is continuous, the area added over a short step is nearly f times "
            "the step, so the slope of F at that point is the value of f. <bookmark mark='d'/> At the jump, the slope "
            "changes abruptly, and F has a corner."
        ) as vo:
            self.play(Create(ax), Create(gf), FadeIn(fl), Create(bx))
            vo.wait_until("a")
            self.add(area, Fg, Fdot)
            self.play(FadeIn(Fl), xT.animate.set_value(1.2), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(side[:3]))
            vo.wait_until("c")
            self.play(FadeIn(tan), FadeIn(side[3:5]))
            self.play(xT.animate.set_value(1.5), run_time=1.2, rate_func=linear)
            vo.wait_until("d")
            self.play(xT.animate.set_value(2.95), FadeIn(side[5]), run_time=3.0, rate_func=linear)
        for m in (area, Fg, Fdot, tan):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        thm = VGroup(label(r"\textbf{Rudin 6.21} \ (fundamental theorem of calculus)", font_size=30),
                     MathTex(r"F' = f \text{ on } [a, b],\ f \text{ integrable} \;\Rightarrow\; \int_a^b f\,dx = F(b) - F(a)",
                             font_size=34)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        ax = plain_axes([0, 3, 1], [0, 2.4, 1], 6.6, 3.8).move_to([-3.55, -1.2, 0])
        Fn = lambda t: 0.3 + 0.5 * t + 0.25 * np.sin(2.2 * t)  # noqa: E731
        fn = lambda t: 0.5 + 0.55 * np.cos(2.2 * t)  # noqa: E731
        gF = ax.plot(Fn, x_range=[0, 3, 0.01], color=C.EPS, stroke_width=4)
        e = np.linspace(0, 3, 6)
        rises = VGroup()
        mvt = VGroup()
        for a, b in zip(e[:-1], e[1:]):
            rises.add(Line(ax.c2p(b, Fn(a)), ax.c2p(b, Fn(b)), color=C.FUNC, stroke_width=5))
            rises.add(DashedLine(ax.c2p(a, Fn(a)), ax.c2p(b, Fn(a)), color=GREY_B, stroke_width=1.5))
            # a mean-value point t_i with F'(t_i) = (F(b) - F(a)) / (b - a)
            t = np.linspace(a, b, 4001)
            slope = (Fn(b) - Fn(a)) / (b - a)
            ti = t[np.argmin(np.abs(fn(t) - slope))]
            assert abs(fn(ti) - slope) < 2e-3
            mvt.add(Dot(ax.c2p(ti, Fn(ti)), radius=0.06, color=WHITE))
        rows = [
            MathTex(r"F(b) - F(a)", r"=", r"\sum_i \big(F(x_i) - F(x_{i-1})\big)", font_size=32),
            MathTex(r"F(b) - F(a)", r"=", r"\sum_i f(t_i)\,\Delta x_i", font_size=32),
            MathTex(r"L(P, f)", r"\le", r"F(b) - F(a) \le U(P, f)", font_size=32),
        ]
        whys = [why(r"telescoping: \ the rises add up"), why(r"mean value theorem on each piece"),
                why(r"$m_i \le f(t_i) \le M_i$; \ refine")]
        step = ladder(self, rows, whys, keep=3, top=1.95, buff=0.38, x=3.3, edge=6.95)
        extra = label(r"also: integration by parts (6.22), \ change of variables (6.19)", font_size=24, color=GREY_B)
        extra.to_edge(DOWN, buff=0.2).shift(RIGHT * 3.0)
        with self.voiceover(
            "<bookmark mark='t'/> The fundamental theorem goes the other way: if F has derivative f, and f is "
            "integrable, then the integral of f is F of b minus F of a. <bookmark mark='a'/> Take any partition. The "
            "total rise of F is the sum of its rises over the pieces. <bookmark mark='b'/> By the mean value theorem, "
            "each rise is f at some point t i times the width of the piece. <bookmark mark='c'/> That sum lies between "
            "the lower and upper sums, for every partition, so the total rise is the integral. "
            "<bookmark mark='d'/> Integration by parts and the change of variables formula follow from the same "
            "chapter's results."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(thm), Create(ax), Create(gF))
            vo.wait_until("a")
            step(0)
            self.play(LaggedStart(*[Create(r) for r in rises], lag_ratio=0.15))
            vo.wait_until("b")
            step(1)
            self.play(LaggedStart(*[FadeIn(m, scale=2) for m in mvt], lag_ratio=0.15))
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(extra))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def length(self):
        head = VGroup(label(r"\textbf{Rudin 6.26--6.27} \ the length of a curve $\gamma: [a, b] \to \R^k$", font_size=30),
                      MathTex(r"\Lambda(\gamma) = \sup_P \sum |\gamma(t_i) - \gamma(t_{i-1})|, \qquad "
                              r"\Lambda(\gamma) = \int_a^b |\gamma'(t)|\,dt \ \text{ if } \gamma' \text{ is continuous}",
                              font_size=30)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        o = np.array([-3.4, -1.0, 0])
        t = np.linspace(0, 2 * np.pi, 2000)

        def gam(t):
            return np.c_[1.9 * np.cos(t) + 0.45 * np.cos(3 * t), 1.4 * np.sin(t) - 0.3 * np.sin(2 * t)]

        P = gam(t)
        curve = VMobject(color=C.FUNC, stroke_width=4).set_points_as_corners([o + np.array([p[0], p[1], 0]) for p in P])
        curve.set_fill(opacity=0)
        true_len = float(np.sum(np.linalg.norm(np.diff(P, axis=0), axis=1)))
        polys, lens = [], []
        for n in (4, 8, 16, 64):
            tt = np.linspace(0, 2 * np.pi, n + 1)
            Q = gam(tt)
            lens.append(float(np.sum(np.linalg.norm(np.diff(Q, axis=0), axis=1))))
            pm = VMobject(color=C.EPS, stroke_width=3).set_points_as_corners([o + np.array([q[0], q[1], 0]) for q in Q])
            pm.set_fill(opacity=0)
            polys.append(VGroup(pm, *[Dot(o + np.array([q[0], q[1], 0]), radius=0.045, color=C.EPS) for q in Q[:-1]]))
        assert all(a < b for a, b in zip(lens, lens[1:])) and lens[-1] < true_len
        labs = [MathTex(rf"n = {n}: \ {L_:.4f}", font_size=30, color=C.EPS).move_to([3.4, 0.4 - 0.55 * i, 0])
                for i, (n, L_) in enumerate(zip((4, 8, 16, 64), lens))]
        tl = MathTex(rf"\int |\gamma'| = {true_len:.4f}", font_size=32, color=C.FUNC).move_to([3.4, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The same circle of ideas gives curves a length. Inscribe polygons in the curve, with "
            "corners at the points of a partition. <bookmark mark='b'/> Refining the partition can only lengthen the "
            "polygon, by the triangle inequality, and the length of the curve is defined as the supremum. "
            "<bookmark mark='c'/> When the curve has a continuous derivative, that supremum is the integral of the "
            "speed."
        ) as vo:
            self.play(FadeIn(head[0]))
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(head[1]))
            vo.wait_until("b")
            self.play(Create(polys[0]), FadeIn(labs[0]))
            for k in range(1, 4):
                self.play(ReplacementTransform(polys[k - 1], polys[k]), FadeIn(labs[k]), run_time=0.9)
            vo.wait_until("c")
            self.play(FadeIn(tl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def koch(self):
        d = load("koch")
        lengths = d["lengths"]
        sc = 10.0
        o = np.array([-6.3, -1.75, 0])
        curves = []
        for k in range(0, 7):
            P = d[f"p{k}"]
            m = VMobject(color=C.PATHOLOGY if k else C.FUNC, stroke_width=3 if k < 5 else 2)
            m.set_points_as_corners([o + sc * np.array([p[0], p[1], 0]) for p in P])
            curves.append(m)
        head = label(r"The Koch curve: \ continuous, \ but no length", font_size=34).to_edge(UP, buff=0.35)
        tab = VGroup(*[MathTex(rf"\text{{depth }} {k}: \ ({{\tfrac43}})^{{{k}}} = {lengths[k]:.3f}", font_size=26)
                       for k in (1, 2, 3, 6, 9, 12)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.9, 1.7, 0])
        card = museum_card(r"the Koch curve", r"H. von Koch, 1904", r"finite length", r"Rudin 6.26: not rectifiable",
                           width=3.8).scale(0.85).to_corner(DR, buff=0.3)
        # self-similarity: the first quarter of the curve (over [0, 1/3]) is the whole curve shrunk by 3
        src = Axes(x_range=[0, 1, 1], y_range=[0, 0.3, 0.3], x_length=sc, y_length=0.3 * sc, tips=False,
                   axis_config={"stroke_opacity": 0, "include_ticks": False})
        src.shift(o - src.c2p(0, 0))
        inset, decor = magnifier(src, (-0.004, 0.3373), (-0.006, 0.1025), center=[-3.7, 1.45, 0], width=4.2,
                                 height=4.2 * 0.1085 / 0.3413, color=GREY_B, tag=r"\times 3")
        P6 = d["p6"]
        q = P6[: (len(P6) - 1) // 4 + 1]
        assert np.allclose(q * 3, P6[::4]) and np.allclose(q[-1], [1 / 3, 0])
        zoomed = VMobject(color=C.PATHOLOGY, stroke_width=2).set_points_as_corners([inset.c2p(a, b) for a, b in q])
        piece = VMobject(color=C.EPS, stroke_width=3).set_points_as_corners([o + sc * np.array([a, b, 0]) for a, b in q])
        selfsim = VGroup(MathTex(r"\text{length} = 4 \times \tfrac13\,\text{length}", font_size=30, color=C.PATHOLOGY),
                         label(r"so it is $0$ or $\infty$; \ and it is not $0$", font_size=24, color=GREY_A)
                         ).arrange(DOWN, buff=0.1).next_to(decor.frame, RIGHT, buff=0.35).shift(DOWN * 0.1)
        with self.voiceover(
            "And a curve without a length. <bookmark mark='a'/> Start with a segment. Replace its middle third by two "
            "sides of an equilateral triangle, and repeat on every segment, forever. <bookmark mark='b'/> Each step "
            "multiplies the length by four thirds, so the polygons' lengths grow without bound: after twelve steps "
            "they're already thirty-one times the original. <bookmark mark='z'/> Zoom in on the first quarter of the "
            "curve: it is the whole curve, shrunk by a factor of three. The curve is four such copies, so its length "
            "would have to be four thirds of itself, which no finite positive number is. <bookmark mark='c'/> The "
            "polygons converge uniformly to a continuous curve, which by the definition has no finite length. "
            "Uniform convergence will reappear in a moment: it's the theme of the rest of this part."
        ) as vo:
            self.play(FadeIn(head), Create(curves[0]))
            vo.wait_until("a")
            cur = curves[0]
            for k in range(1, 4):
                self.play(ReplacementTransform(cur, curves[k]), run_time=1.0)
                cur = curves[k]
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab], lag_ratio=0.25))
            for k in range(4, 7):
                self.play(ReplacementTransform(cur, curves[k]), run_time=0.8)
                cur = curves[k]
            vo.wait_until("z")
            self.play(FadeIn(decor))
            self.play(ShowPassingFlash(piece.copy(), time_width=0.5), run_time=1.0)
            self.play(TransformFromCopy(piece, zoomed), run_time=1.2)
            self.play(FadeIn(selfsim))
            vo.wait_until("c")
            self.play(FadeIn(card, scale=0.95))
        assert lengths[12] > 31
        self.wait(0.4)
        self.clear_scene()
