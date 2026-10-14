from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis9.common import SQ2PI, load, plain_axes, polyline, trap


def pole_mark(point, size=0.13, color=C.PATHOLOGY) -> VGroup:
    """A cross drawn with two strokes (not a text glyph) marking a zero of the symbol on the real axis."""
    p = np.asarray(point)
    return VGroup(Line(p + size * (LEFT + DOWN), p + size * (RIGHT + UP), color=color, stroke_width=4),
                  Line(p + size * (LEFT + UP), p + size * (RIGHT + DOWN), color=color, stroke_width=4))


class Fundamental(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.examples()
        self.contour()
        self.malgrange()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(11, r"Fundamental solutions", r"Can one convolution solve a whole equation?", lit=(1945,),
                            part=9)
        with self.voiceover("Chapter eleven: fundamental solutions, which solve a differential equation for every right-hand "
                            "side at once."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        d = load("contour")
        x, f, u, uc, res = d["x"], d["f"], d["u"], d["uc"], float(d["res"])
        ax = plain_axes([-8, 8, 2], [-1.0, 1.0, 1], 6.6, 1.4).move_to([-3.1, 1.55, 0])
        bx = plain_axes([-8, 8, 2], [-1.2, 1.2, 1], 6.6, 2.2).move_to([-3.1, -1.1, 0])
        gf = polyline(ax, x, f / 0.37, color=C.FUNC, stroke_width=3)
        gu = polyline(bx, x, u, color=C.APPROX, stroke_width=3.5)
        gc = polyline(bx, x, uc, color=C.EPS, stroke_width=3.5)
        lf = MathTex(r"f \ (\text{two sources})", font_size=24, color=C.FUNC).next_to(ax, UP, buff=0.05)
        lu = MathTex(r"u = \tfrac12\sin|x| * f", font_size=24, color=C.APPROX).next_to(bx.c2p(-8, 1.2), RIGHT, buff=0.1)
        lc = MathTex(r"u = H(x)\sin x * f \ \ (\text{causal})", font_size=24, color=C.EPS).next_to(bx.c2p(-8, -1.2), RIGHT,
                                                                                              buff=0.1)
        assert res < 1e-4 and np.abs(uc[x < -3]).max() < 1e-12
        rows = VGroup(
            MathTex(r"P(D)\,E = \delta", font_size=36, color=C.DISTRIBUTION),
            MathTex(r"\Rightarrow \ P(D)(E * f) = (P(D)E) * f = \delta * f = f", font_size=28),
            label(r"one convolution solves $P(D)u = f$ \ for every $f$", font_size=24, color=C.EPS),
            MathTex(r"u'' + u = f: \ \ E = \tfrac12\sin|x| \ \text{ or } \ H(x)\sin x", font_size=26),
            MathTex(rf"\text{{checked: }} \max|u'' + u - f| = {sci(res, 1)}", font_size=24, color=GREY_A),
            VGroup(label(r"(Part 8's string had its Green's function;", font_size=22, color=GREY_A),
                   label(r"this is the general version)", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.08),
        ).arrange(DOWN, buff=0.16).move_to([3.5, 0.0, 0])
        for r_ in rows:
            if r_.width > 6.0:
                r_.width = 6.0
        rows.arrange(DOWN, buff=0.16).move_to([3.5, 0.0, 0])
        # 'a': the point source and the two responses to it, E = (1/2) sin|x| and E = H(x) sin x; each solves
        # E'' + E = 0 off the source, and its slope jumps by exactly 1 there: E'' + E = delta
        xe = np.linspace(-8, 8, 1601)
        e_sym, e_cau = 0.5 * np.sin(np.abs(xe)), np.where(xe > 0, np.sin(xe), 0.0)
        hh = 1e-6
        for E_ in (lambda t: 0.5 * np.sin(np.abs(t)), lambda t: np.where(t > 0, np.sin(t), 0.0)):
            jump = (E_(2 * hh) - E_(hh)) / hh - (E_(-hh) - E_(-2 * hh)) / hh
            off = np.array([-5.0, -2.0, 1.5, 4.0])
            d2 = (E_(off + 1e-4) - 2 * E_(off) + E_(off - 1e-4)) / 1e-8
            assert abs(jump - 1) < 1e-4 and np.abs(d2 + E_(off)).max() < 1e-4
        src = Arrow(ax.c2p(0, 0), ax.c2p(0, 0.95), buff=0, color=C.DISTRIBUTION, stroke_width=5,
                    max_tip_length_to_length_ratio=0.25)
        srcl = MathTex(r"\delta: \ \text{a point source}", font_size=24, color=C.DISTRIBUTION).next_to(ax, UP, buff=0.05)
        ge1 = polyline(bx, xe, e_sym, color=C.APPROX, stroke_width=3.5)
        ge2 = polyline(bx, xe, e_cau, color=C.EPS, stroke_width=3.5)
        le1 = MathTex(r"E = \tfrac12\sin|x|", font_size=24, color=C.APPROX).next_to(bx.c2p(-8, 1.2), RIGHT, buff=0.1)
        le2 = MathTex(r"E = H(x)\sin x", font_size=24, color=C.EPS).next_to(bx.c2p(-8, -1.2), RIGHT, buff=0.1)
        head = label(r"Solve once, \ for a point source", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> A fundamental solution of a differential operator is a distribution E with P of D "
            "applied to E equal to delta: the response to a single point source. <bookmark mark='b'/> Then E "
            "convolved with f solves the equation with right-hand side f, because derivatives pass through the "
            "convolution, and delta convolved with f is f. <bookmark mark='c'/> For u double prime plus u, the "
            "oscillator, here are two sources of opposite sign, and two responses: the symmetric one, and the causal "
            "one, which is zero before the sources and rings after them. Both satisfy the equation, checked by finite "
            "differences."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[0]), Create(ax), Create(bx))
            self.play(GrowArrow(src), FadeIn(srcl))
            self.play(Create(ge1), FadeIn(le1), Create(ge2), FadeIn(le2), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeOut(VGroup(src, srcl, ge1, ge2, le1, le2)), run_time=0.6)
            self.play(Create(gf), FadeIn(lf), FadeIn(rows[3]))
            self.play(Create(gu), FadeIn(lu))
            self.play(Create(gc), FadeIn(lc), FadeIn(rows[4:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def examples(self):
        d = load("fundamental")
        newton, tests = float(d["newton"]), d["tests"]
        ax = plain_axes([-4, 4, 1], [0, 3, 1], 6.0, 2.6).move_to([-3.4, 1.0, 0])
        tT = ValueTracker(0.01)
        x = np.linspace(-4, 4, 1601)
        xx = np.linspace(-40, 40, 400001)

        def K(t, s):
            return np.exp(-s * s / (4 * t)) / math.sqrt(4 * math.pi * t)

        g = always_redraw(lambda: runs(ax, x, K(tT.get_value(), x), C.MEASURE, 3.5))
        rd = always_redraw(lambda: MathTex(rf"t = {tT.get_value():.3f}: \ \ \int K_t = {trap(K(tT.get_value(), xx), xx):.8f}",
                                           font_size=24).next_to(ax, UP, buff=0.1))
        kl = MathTex(r"K_t(x) = \frac{e^{-x^2/4t}}{\sqrt{4\pi t}}: \ \ (\partial_t - \partial_x^2)\,H(t)K_t = \delta",
                     font_size=26, color=C.MEASURE).next_to(ax, DOWN, buff=0.2)
        for t_ in (0.01, 0.1, 1.0, 2.0):
            assert abs(trap(K(t_, xx), xx) - 1) < 1e-8
        # the table of classics, at a readable size (a dictionary card scaled into half the frame would be ~11 pt)
        pairs = [(r"\frac{d}{dx}", r"H \ \text{(the step)}"),
                 (r"\frac{d^2}{dx^2} + 1", r"\tfrac12\sin|x|"),
                 (r"\Delta \text{ in } \mathbb R^2", r"\tfrac{1}{2\pi}\log|x|"),
                 (r"\Delta \text{ in } \mathbb R^3", r"-\tfrac{1}{4\pi|x|}"),
                 (r"\partial_t - \Delta", r"H(t)\,(4\pi t)^{-n/2} e^{-|x|^2/4t}")]
        trows = VGroup(*[VGroup(MathTex(a_, font_size=26), MathTex(r"\longleftrightarrow", font_size=26, color=GREY_C),
                                MathTex(b_, font_size=26)) for a_, b_ in pairs])
        thead = VGroup(label(r"operator", font_size=24, color=GREY_A), VGroup(),
                       label(r"fundamental solution", font_size=24, color=GREY_A))
        w0 = max(r_[0].width for r_ in trows)
        x0 = 0.6
        xa, xb = x0 + w0 + 0.35, x0 + w0 + 0.35 + trows[0][1].width + 0.35
        for i_, r_ in enumerate(trows):
            y_ = 1.85 - 0.66 * i_
            r_[0].move_to([x0 + r_[0].width / 2, y_, 0])
            r_[1].move_to([xa + r_[1].width / 2, y_, 0])
            r_[2].move_to([xb + r_[2].width / 2, y_, 0])
        thead[0].move_to([x0 + thead[0].width / 2, 2.55, 0])
        thead[2].move_to([xb + thead[2].width / 2, 2.55, 0])
        assert max(r_[2].get_right()[0] for r_ in trows) <= 6.6 and thead[2].get_right()[0] <= 6.6
        checks = VGroup(
            MathTex(rf"\Big\langle -\tfrac{{1}}{{4\pi|x|}}, \Delta\varphi\Big\rangle = {newton:.10f} = \varphi(0)",
                    font_size=24, color=C.EPS),
            MathTex(r"\big\langle \tfrac12\sin|x|, \varphi'' + \varphi\big\rangle: \ " +
                    r",\ ".join(f"{a_:.6f}" for a_, _ in tests) + r" \ = \varphi(0) \text{ for three bumps}",
                    font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        assert abs(newton - 1) < 1e-6 and np.allclose(tests[:, 0], tests[:, 1], atol=1e-5)
        head = label(r"Heat, \ gravity, \ and the oscillator", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The heat equation's fundamental solution is the heat kernel: a point of heat at time "
            "zero spreading into a Gaussian, whose total stays exactly one. <bookmark mark='b'/> Here's the table of "
            "classics: the step for the first derivative, half of sine of the absolute value for the oscillator, the "
            "logarithm in the plane and minus one over four pi r in space for the Laplacian: the potential of a point "
            "charge. <bookmark mark='c'/> Each is checked as a distribution: minus one over four pi r, tested against "
            "the Laplacian of a Gaussian, gives phi of zero to ten digits."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(g), FadeIn(rd), FadeIn(kl))
            self.play(tT.animate.set_value(2.0), run_time=4.0, rate_func=lambda u: u**2)
            vo.wait_until("b")
            self.play(FadeIn(thead[0]), FadeIn(thead[2]))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in trows], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(checks))
        for m in (g, rd):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def contour(self):
        d = load("contour")
        xs, below, above = d["xs"], d["below"], d["above"]
        eb, ea, ec = float(d["eb"]), float(d["ea"]), float(d["ec"])
        cx = plain_axes([-3, 3, 1], [-1.5, 1.5, 0.5], 5.2, 2.6).move_to([-3.6, 0.9, 0])
        poles = VGroup(*[pole_mark(cx.c2p(p, 0)) for p in (-1, 1)])
        pl = MathTex(r"1 - \zeta^2 = 0", font_size=22, color=C.PATHOLOGY).next_to(cx.c2p(1, 0), UR, buff=0.08)
        sT = ValueTracker(-0.5)
        line = always_redraw(lambda: Arrow(cx.c2p(-3, sT.get_value()), cx.c2p(3, sT.get_value()), buff=0,
                                           color=C.EPS if sT.get_value() < 0 else C.APPROX, stroke_width=4,
                                           tip_length=0.15))
        zl = MathTex(r"\zeta \in \mathbb C", font_size=22, color=GREY_B).next_to(cx, UP, buff=0.05).align_to(cx, LEFT)
        # 'a': the trouble, drawn on the real axis: E^(t) = 1 / (sqrt(2 pi) (1 - t^2)) blows up at t = +-1 (cut at the
        # window), and its integral near 1 grows like a logarithm: not integrable
        tr = np.linspace(-3, 3, 6001)
        tr = tr[np.abs(np.abs(tr) - 1) > 1e-6]
        Eh = 1 / (SQ2PI * (1 - tr * tr))
        for k_ in (3, 6):
            u_ = 1 - np.geomspace(1, 10.0**-k_, 200001)  # graded towards the singularity
            assert abs(trap(1 / (SQ2PI * (1 - u_ * u_)), u_) - math.atanh(1 - 10.0**-k_) / SQ2PI) < 1e-3
        assert math.atanh(1 - 1e-6) / SQ2PI - math.atanh(1 - 1e-3) / SQ2PI > 1.3  # +log(10^3)/(2 sqrt(2 pi)): unbounded
        gE = runs(cx, tr, Eh, C.FREQ, 3)
        gEl = MathTex(r"\hat E(t), \ t \in \mathbb R", font_size=22, color=C.FREQ).move_to(cx.c2p(-2.1, 0.55))
        bx = plain_axes([-6, 6, 2], [-1.2, 1.2, 1], 6.0, 2.6).move_to([3.4, 0.9, 0])
        gb = polyline(bx, xs, below, color=C.EPS, stroke_width=3.5)
        ga = polyline(bx, xs, above, color=C.APPROX, stroke_width=3.5)
        gm = DashedVMobject(polyline(bx, xs, (below + above) / 2, color=WHITE, stroke_width=3), num_dashes=60)
        lb = MathTex(r"\text{below: } H(x)\sin x", font_size=22, color=C.EPS).next_to(bx, UP, buff=0.05).align_to(bx, LEFT)
        la = MathTex(r"\text{above: } -H(-x)\sin x", font_size=22, color=C.APPROX).next_to(bx, UP, buff=0.05).align_to(
            bx, RIGHT)
        lm = MathTex(r"\text{average: } \tfrac12\sin|x|", font_size=22).next_to(bx, DOWN, buff=0.05)
        assert max(eb, ea, ec) < 1e-7
        assert np.allclose((below + above) / 2, np.sin(np.abs(xs)) / 2, atol=1e-7)
        rows = VGroup(
            MathTex(r"\widehat{u'' + u} = (1 - t^2)\,\hat u: \quad \hat E = \frac{1}{\sqrt{2\pi}\,(1 - t^2)} \ \text{ is not "
                    r"integrable at } t = \pm 1", font_size=24),
            MathTex(r"E(x) = \frac{1}{2\pi}\int_{\mathrm{Im}\,\zeta = \sigma} \frac{e^{ix\zeta}}{1 - \zeta^2}\,d\zeta", font_size=28,
                    color=C.EPS),
            MathTex(rf"\text{{quadrature vs exact: }} {sci(max(eb, ea), 0)}; \ \ \sigma = -\tfrac12 \text{{ vs }} -1: \ {sci(ec, 0)} "
                    r"\ (\text{Cauchy})", font_size=22, color=GREY_A),
            label(r"crossing the poles adds the residues: \ $\sin x$, \ a solution of $u'' + u = 0$", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        head = label(r"Dodging the zeros of the symbol", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Where do fundamental solutions come from? Transform the equation: one minus t "
            "squared times E hat must be constant. But one minus t squared vanishes at plus and minus one, and one "
            "over it isn't integrable there. <bookmark mark='b'/> So leave the real line. Write the inversion integral "
            "along a line just below the zeros, in the complex plane. Computed numerically, it gives H of x times sine "
            "x, the causal solution, and any lower line gives the same, by Cauchy's theorem. "
            "<bookmark mark='c'/> Move the line above the zeros, and you get a different fundamental solution, minus "
            "H of minus x times sine x. Crossing the poles adds their residues, sine x, which solves the homogeneous "
            "equation. <bookmark mark='d'/> Average the two, and you get the symmetric one, half of sine of the "
            "absolute value."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[0]), Create(cx), FadeIn(poles), FadeIn(pl), FadeIn(zl))
            self.play(Create(gE), FadeIn(gEl), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeOut(VGroup(gE, gEl)), FadeIn(line), FadeIn(rows[1]))
            self.play(Create(bx), Create(gb), FadeIn(lb), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(sT.animate.set_value(0.5), run_time=2.0)
            self.play(gb.animate.set_stroke(opacity=0.35), Create(ga), FadeIn(la), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(Create(gm), FadeIn(lm))
        line.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def malgrange(self):
        pm = ProofMap([
            r"want $\hat E = 1/P$; \ but $P$ has zeros",
            r"move one variable off $\mathbb R^n$, \ onto $\xi + \lambda\eta$, \ $|\lambda| = 1$",
            r"\textbf{8.4} \ $|a f(0)| \le \int |p f|$ on the circle: \ $1/P$ is tamed on average",
            r"Paley--Wiener bounds on $\hat\varphi(\xi + \lambda\eta)$: \ $E$ is a distribution",
            r"Cauchy undoes the shift: \ $P(D)E = \delta$",
        ], font_size=22, width=6.2, buff=0.18, direction=DOWN)
        pm.move_to([-3.4, -0.2, 0])
        thm = label(r"\textbf{FA 8.5} \ (Malgrange--Ehrenpreis, 1954--55) \ every $P(D) \ne 0$ with constant "
                    r"coefficients has a fundamental solution", font_size=24, color=C.EPS).to_edge(UP, buff=1.0)
        # a picture of the averaging: lines Im zeta = sin(theta) sweep the strip; half pass below the zeros, half above
        cx = plain_axes([-2.5, 2.5, 1], [-1.4, 1.4, 0.5], 5.0, 2.8).move_to([3.6, 0.6, 0])
        poles = VGroup(*[pole_mark(cx.c2p(p, 0), size=0.11) for p in (-1, 1)])
        th = np.linspace(0, 2 * np.pi, 25)[:-1] + np.pi / 24
        lines = VGroup(*[Line(cx.c2p(-2.5, math.sin(a)), cx.c2p(2.5, math.sin(a)), stroke_width=2,
                              color=C.EPS if math.sin(a) < 0 else C.APPROX, stroke_opacity=0.6) for a in th])
        circ = Circle(radius=cx.c2p(1, 0)[0] - cx.c2p(0, 0)[0], color=GREY_B, stroke_width=2).move_to(cx.c2p(0, 0))
        cl = MathTex(r"\lambda = e^{i\theta}", font_size=22, color=GREY_B).next_to(cx.c2p(0.05, 1.0), UR, buff=0.05)  # off the axis
        rows = VGroup(
            label(r"shifts by $\lambda = e^{i\theta}$: \ the lines $\mathrm{Im}\,\zeta = \sin\theta$", font_size=22),
            label(r"in the example: \ half below, \ half above, \ average $= \tfrac12\sin|x|$", font_size=22,
                  color=GREY_A),
            label(r"\textbf{FA 8.12} \ elliptic operators are hypoelliptic:", font_size=22, color=C.TEST_FN),
            label(r"$P(D)u \in C^\infty$ $\Rightarrow$ $u \in C^\infty$ \ (harmonic functions are smooth)", font_size=22,
                  color=C.TEST_FN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(cx, DOWN, buff=0.3)
        head = label(r"Every constant-coefficient equation can be solved", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The Malgrange-Ehrenpreis theorem says this always works: every nonzero linear "
            "operator with constant coefficients has a fundamental solution. <bookmark mark='b'/> Rudin's proof is "
            "the same idea in n variables. The symbol has zeros, so move one variable into the complex plane, along "
            "shifts by points of the unit circle, and average. A lemma on polynomials bounds one over P on average, "
            "Paley-Wiener bounds control the test functions, and Cauchy's theorem shows that the averaged functional "
            "really inverts P of D. <bookmark mark='c'/> In our example, the shifted lines sweep a strip; half pass "
            "below the zeros and half above, and the average is the symmetric solution. <bookmark mark='d'/> And for "
            "elliptic operators like the Laplacian, every solution with a smooth right side is smooth itself."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(thm), Create(cx), FadeIn(poles))  # the symbol's zeros from the start
            vo.wait_until("b")
            self.play(FadeIn(pm))
            for i in range(5):
                self.play(*pm.light(i), run_time=0.7)
            vo.wait_until("c")
            self.play(Create(circ), FadeIn(cl))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.1), FadeIn(rows[:2]), run_time=2.5)
            vo.wait_until("d")
            self.play(*pm.done(), FadeIn(rows[2:]))
        self.wait(0.4)
        self.clear_scene()
