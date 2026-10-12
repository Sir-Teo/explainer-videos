from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis3.common import load, plain_axes, polyline, saw, saw_partial


class Parseval(VoiceoverScene):
    def construct(self):
        self.card()
        self.density()
        self.parseval()
        self.basel()
        self.dashboard()
        self.gibbs()
        self.gamma()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(15, r"Parseval, Gibbs, and $\pi^2/6$",
                            r"Do the Fourier partial sums converge to $f$, and in what sense?", lit=(), part=3)
        with self.voiceover(
            "Chapter fifteen, the payoff: in what sense does a Fourier series converge to its function?"
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def density(self):
        d = load("parseval")
        xf, ff, FN, sig, ferr = d["xf"], d["ff"], d["FN"], d["sig"], d["ferr"]
        ax = plain_axes([-np.pi, np.pi, np.pi / 2], [-0.2, 1.1, 0.5], 7.2, 4.2).move_to([-2.9, -0.8, 0])
        fg = polyline(ax, xf, ff, color=WHITE, stroke_width=3.5)
        shown = [0, 2, 4, 6]
        curves = [polyline(ax, xf, sig[i], color=C.APPROX, stroke_width=3) for i in shown]
        head = VGroup(label(r"\textbf{Rudin 8.15} \ trigonometric polynomials are dense in $C(\mathbb T)$", font_size=30),
                      label(r"Stone--Weierstrass: \ the algebra of $\sum c_n e^{inx}$ is self-adjoint, separates points "
                            r"of the circle, \ and contains $1$", font_size=24, color=GREY_A)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        tab = VGroup(MathTex(r"N", r"\quad \sup|\sigma_N - f|", font_size=26, color=GREY_A))
        for N, e in zip(FN, ferr):
            tab.add(MathTex(rf"{int(N)}", rf"\quad {e:.4f}", font_size=26))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.3, -0.2, 0])
        sl = VGroup(label(r"one explicit choice: \ Fej\'er's averages (1900)", font_size=24, color=C.APPROX),
                    MathTex(r"\sigma_N = \sum_{|n| \le N} \Big(1 - \frac{|n|}{N + 1}\Big) c_n e^{inx}", font_size=28,
                            color=C.APPROX),
                    label(r"a positive kernel, \ like Landau's \ (Parts 6 and 7)", font_size=22, color=GREY_A)
                    ).arrange(DOWN, buff=0.12).next_to(ax, DOWN, buff=0.15)
        for k in range(len(sl)):
            if sl[k].width > 7.2:
                sl[k].width = 7.2
        with self.voiceover(
            "<bookmark mark='a'/> First, density. The trigonometric polynomials, sums of c n e to the i n x, form an "
            "algebra of functions on the circle that contains the constants, separates points, and is closed under "
            "complex conjugation. So by Stone's theorem, every continuous periodic function is a uniform limit of "
            "trigonometric polynomials. <bookmark mark='b'/> One explicit choice, found by Fejér in 1900, averages the "
            "partial sums, which damps the high frequencies. Its kernel is positive, like Landau's, and the averages "
            "converge uniformly. <bookmark mark='c'/> Here they are for a continuous function with three corners."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(fg))
            vo.wait_until("b")
            self.play(FadeIn(sl))
            vo.wait_until("c")
            self.play(Create(curves[0]), FadeIn(tab[0]), FadeIn(tab[1]))
            cur = curves[0]
            for k in range(1, len(shown)):
                self.play(ReplacementTransform(cur, curves[k]),
                          LaggedStart(*[FadeIn(tab[j + 1]) for j in range(shown[k - 1] + 1, shown[k] + 1)],
                                      lag_ratio=0.3), run_time=1.3)
                cur = curves[k]
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def parseval(self):
        d = load("parseval")
        Ns, mse, tail = d["Ns"], d["mse"], d["tail"]
        tot = math.pi**2 / 12
        W = 10.0
        x0 = -W / 2
        y = -0.2
        outline = Rectangle(width=W, height=0.7, stroke_color=WHITE, stroke_width=2).move_to([0, y, 0])
        tl = MathTex(r"\frac{1}{2\pi}\int |f|^2 = \frac{\pi^2}{12}", font_size=30).next_to(outline, UP, buff=0.15)
        tl.align_to(outline, RIGHT)
        cols = [C.FREQ, C.CLOSED_SET, C.EPS, C.CONNECTED_SET, C.SEQ, C.INNER]

        def filled(N):
            acc = 0.5 * sum(1.0 / k**2 for k in range(1, N + 1))
            segs = VGroup()
            a = 0.0
            for k in range(1, min(N, 60) + 1):
                w = 0.5 / k**2
                segs.add(Rectangle(width=W * w / tot, height=0.7, stroke_width=0.5 if k < 12 else 0, stroke_color=BLACK,
                                   fill_color=cols[(k - 1) % len(cols)], fill_opacity=0.85)
                         .move_to([x0 + W * (a + w / 2) / tot, y, 0]))
                a += w
            if N > 60:
                segs.add(Rectangle(width=W * (acc - a) / tot, height=0.7, stroke_width=0, fill_color=GREY_B,
                                   fill_opacity=0.85).move_to([x0 + W * (a + (acc - a) / 2) / tot, y, 0]))
            gap = Rectangle(width=max(W * (tot - acc) / tot, 0.01), height=0.7, stroke_color=C.PATHOLOGY,
                            stroke_width=2, fill_color=C.PATHOLOGY, fill_opacity=0.25)
            gap.move_to([x0 + W * (acc + (tot - acc) / 2) / tot, y, 0])
            return VGroup(segs, gap)

        frames = {N: filled(N) for N in (1, 2, 5, 10, 20, 100)}
        lab = {N: MathTex(rf"N = {N}: \ \text{{missing}} = \frac{{1}}{{2\pi}}\int |f - s_N|^2 = "
                          rf"{float(mse[list(Ns).index(N)]):.5f}", font_size=28, color=C.PATHOLOGY).next_to(
            outline, DOWN, buff=0.3) for N in (1, 2, 5, 10, 20, 100)}
        head = VGroup(label(r"\textbf{Rudin 8.16} \ (Parseval) \ for every Riemann-integrable $f$:", font_size=30),
                      MathTex(r"\frac{1}{2\pi}\int_{-\pi}^{\pi} |f - s_N|^2 \to 0, \qquad "
                              r"\sum_{n} |c_n|^2 = \frac{1}{2\pi}\int_{-\pi}^{\pi} |f|^2", font_size=34, color=C.EPS)
                      ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        proof = VGroup(
            label(r"why: \ $f$ is close in mean square to a continuous $h$; \ $h$ is uniformly close to a "
                  r"trigonometric $P$ (8.15);", font_size=22, color=GREY_A),
            label(r"and $s_N$ is at least as close as $P$ once $N \ge \deg P$ (8.11): \ "
                  r"$\|f - s_N\|_2 \le \|f - h\|_2 + \|h - P\|_2$", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.08).next_to(head, DOWN, buff=0.25)
        for r_ in proof:
            if r_.width > 13.0:
                r_.width = 13.0
        note_ = label(r"the missing energy is exactly the tail $\frac12 \sum_{n > N} \frac{1}{n^2}$ \ (computed both ways)",
                      font_size=24, color=GREY_A).to_edge(DOWN, buff=0.35)
        assert np.allclose(mse, tail, rtol=2e-3)
        with self.voiceover(
            "<bookmark mark='a'/> Now Parseval's theorem, Rudin 8.16. For every Riemann-integrable function, the mean "
            "square error of the partial sums goes to zero, and Bessel's inequality becomes an equality. "
            "<bookmark mark='b'/> The proof chains three approximations. f is close in mean square to a continuous "
            "function; that is uniformly close to a trigonometric polynomial; and the Fourier partial sum is at least "
            "as close as any polynomial of its degree. <bookmark mark='c'/> In the picture from last chapter, the bar "
            "now fills completely. The red gap is the energy the partial sum is still missing, which is exactly its "
            "mean square error, and it shrinks to zero."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(FadeIn(proof[0]))
            self.play(FadeIn(proof[1]))
            vo.wait_until("c")
            cur = frames[1]
            self.play(Create(outline), FadeIn(tl), FadeIn(cur), FadeIn(lab[1]))
            cl = lab[1]
            for N in (2, 5, 10, 20, 100):
                self.play(ReplacementTransform(cur, frames[N]), FadeTransform(cl, lab[N]), run_time=1.1)
                cur, cl = frames[N], lab[N]
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def basel(self):
        d = load("parseval")
        lhs, rhs = float(d["lhs"]), float(d["rhs"])
        rows = [
            MathTex(r"\frac{1}{2\pi}\int_0^{2\pi} \Big(\frac{\pi - x}{2}\Big)^2 dx", r"=", r"\sum_{n \ne 0} |c_n|^2",
                    font_size=36),
            MathTex(r"\frac{\pi^2}{12}", r"=", r"\sum_{n \ne 0} |c_n|^2", font_size=36),
            MathTex(r"\frac{\pi^2}{12}", r"=", r"\sum_{n \ge 1} 2 \cdot \frac{1}{4n^2}", font_size=36),
            MathTex(r"\frac{\pi^2}{6}", r"=", r"\sum_{n \ge 1} \frac{1}{n^2}", font_size=40),
        ]
        whys = [why(r"Parseval for the sawtooth"), why(r"$\frac{1}{2\pi}\int_0^{2\pi} \frac{(\pi - x)^2}{4} = "
                                                      r"\frac{1}{8\pi}\cdot\frac{2\pi^3}{3}$"),
                why(r"$\frac{\pi - x}{2} = \sum \frac{\sin nx}{n}$: \ $c_{\pm n} = \mp\frac{i}{2n}$"),
                why(r"multiply by $2$")]
        head = label(r"The payoff: \ $\sum 1/n^2$, \ from Parseval \ (Rudin, Exercise 8.13)", font_size=32).to_edge(
            UP, buff=0.35)
        step = ladder(self, rows, whys, keep=4, top=2.4, buff=0.42, x=-1.6)
        n = np.arange(1, 10**6 + 1)
        ps = np.cumsum(1.0 / n**2)
        nums = VGroup(*[MathTex(rf"\sum_{{n \le {k}}} \tfrac{{1}}{{n^2}} = {ps[k - 1]:.8f}", font_size=26)
                        for k in (10, 1000, 10**6)],
                      MathTex(rf"\tfrac{{\pi^2}}{{6}} = {math.pi**2 / 6:.8f}", font_size=26, color=C.EPS)
                      ).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.9)
        if nums.width > 13.4:
            nums.width = 13.4
        nod = label(r"Euler, 1734 (the Basel problem); \ 3Blue1Brown proved it with lighthouses: \ this is "
                    r"another way in", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.3)
        assert abs(lhs - math.pi**2 / 12) < 1e-6 and abs(2 * rhs - math.pi**2 / 6) < 2e-6
        with self.voiceover(
            "<bookmark mark='a'/> Parseval's equation, applied to the sawtooth, sums a famous series. On one side, the "
            "average of the square of pi minus x over two. <bookmark mark='b'/> That integral is pi squared over "
            "twelve. <bookmark mark='c'/> On the other side, the coefficients: from the sawtooth's series, each pair "
            "plus and minus n contributes one over two n squared. <bookmark mark='d'/> Multiply by two: the sum of one "
            "over n squared is pi squared over six. <bookmark mark='e'/> Euler found this in 1734; a 3Blue1Brown video "
            "proves it with lighthouses. Here it falls out of the geometry of Fourier series."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(Circumscribe(rows[3], color=C.EPS))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(m_) for m_ in nums], lag_ratio=0.3), FadeIn(nod), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dashboard(self):
        ax = plain_axes([0, 2 * np.pi, np.pi / 2], [-2.0, 2.0, 1], 6.8, 4.2).move_to([-3.0, -0.6, 0])

        def seq(n, x):
            return saw_partial(x, max(1, round(n)))

        def lim(x):
            return saw(x)

        dash = Dashboard(ax, seq, lim, n=1.0, x0=1.0, lenses=("point", "sup", "L2"), domain=(0.002, 2 * np.pi - 0.002),
                         samples=1400, exact={"sup": lambda n: math.pi / 2,
                                              "L2": lambda n: math.sqrt(math.pi * (math.pi**2 / 6 - sum(
                                                  1.0 / k**2 for k in range(1, max(1, round(n)) + 1))))})
        g = dash.graph(color=C.APPROX, stroke_width=3)
        lg = VGroup(Line(ax.c2p(0.003, saw(np.array([0.003]))[0]), ax.c2p(2 * np.pi - 0.003,
                                                                         saw(np.array([2 * np.pi - 0.003]))[0]),
                         color=WHITE, stroke_width=3))
        probe = dash.probe()
        panel = dash.panel(font_size=26, width=4.6).move_to([3.9, 0.0, 0])
        nl = always_redraw(lambda: MathTex(rf"s_N, \ N = {max(1, round(dash.n.get_value()))}", font_size=30,
                                           color=C.APPROX).next_to(ax, UP, buff=0.1))
        head = label(r"The sawtooth on the dashboard", font_size=32).to_edge(UP, buff=0.3)
        verdict = VGroup(label(r"in energy: \ yes \ (Parseval)", font_size=24, color=C.CONNECTED_SET),
                         label(r"at each point: \ yes \ (Dini; \ $0$ at the jumps, the midpoint)", font_size=24,
                               color=C.CONNECTED_SET),
                         label(r"uniformly: \ never \ (a uniform limit would be continuous)", font_size=24,
                               color=C.PATHOLOGY)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(panel, DOWN,
                                                                                                     buff=0.45)
        for r_ in verdict:
            if r_.width > 6.0:
                r_.width = 6.0
        verdict.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(panel, DOWN, buff=0.45)
        with self.voiceover(
            "<bookmark mark='a'/> Put the sawtooth's partial sums on the dashboard. <bookmark mark='b'/> The probe at "
            "one closes in, as Dini's test promised. The energy of the error goes to zero, as Parseval promised. "
            "<bookmark mark='c'/> But the uniform lens is stuck: just to the right of the jump the partial sums are near "
            "zero while the sawtooth is near pi over two. A uniform limit of continuous functions is continuous, so "
            "this convergence can never be uniform."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(lg), Create(g), FadeIn(nl))
            vo.wait_until("a")
            self.play(FadeIn(probe), FadeIn(panel))
            vo.wait_until("b")
            self.play(dash.n.animate.set_value(40), run_time=5.0, rate_func=linear)
            vo.wait_until("c")
            self.play(*dash.light({"point": True, "sup": False, "L2": True}))
            self.play(FadeIn(verdict))
        dash.freeze()
        for m in (g, probe, nl):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gibbs(self):
        d = load("parseval")
        GNs, gibbs, limit = d["GNs"], d["gibbs"], float(d["limit"])
        ax = plain_axes([-0.3, 1.5, 0.5], [-0.2, 2.0, 0.5], 7.4, 4.6).move_to([-2.6, -0.8, 0])
        x = np.concatenate([np.linspace(-0.3, -1e-4, 1200), np.linspace(1e-4, 1.5, 7000)])
        fpos = Line(ax.c2p(1e-3, math.pi / 2), ax.c2p(1.5, (math.pi - 1.5) / 2), color=WHITE, stroke_width=3)
        fneg = Line(ax.c2p(-0.3, (-math.pi + 0.3) / 2), ax.c2p(-1e-3, -math.pi / 2), color=WHITE, stroke_width=3)
        top = math.pi / 2 + limit * math.pi
        lvl = DashedLine(ax.c2p(-0.3, top), ax.c2p(1.5, top), color=C.PATHOLOGY, stroke_width=2)
        lvl_l = MathTex(r"\tfrac{\pi}{2} + 0.0895\,\pi", font_size=24, color=C.PATHOLOGY).next_to(lvl, UP, buff=0.05)
        lvl_l.align_to(lvl, RIGHT)
        half = DashedLine(ax.c2p(-0.3, math.pi / 2), ax.c2p(1.5, math.pi / 2), color=GREY_B, stroke_width=1.5)
        half_l = MathTex(r"\tfrac{\pi}{2}", font_size=24, color=GREY_B).next_to(half, LEFT, buff=0.1)
        shown = [10, 30, 100, 300]
        curves = [runs(ax, x, saw_partial(x, N), C.APPROX, 2.5) for N in shown]
        nls = [MathTex(rf"s_{{{N}}}", font_size=30, color=C.APPROX).next_to(ax, UP, buff=0.1) for N in shown]
        head = VGroup(label(r"Gibbs' phenomenon \ (Wilbraham 1848, \ Gibbs 1899)", font_size=30),
                      MathTex(r"\frac{\max s_N - \frac{\pi}{2}}{\text{jump } \pi} \;\to\; "
                              r"\frac{1}{\pi}\int_0^{\pi} \frac{\sin t}{t}\,dt - \frac12 = " + f"{limit:.5f}",
                              font_size=30)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        tab = VGroup(MathTex(r"N", r"\quad \text{overshoot / jump}", font_size=26, color=GREY_A))
        for N, gv in zip(GNs, gibbs):
            tab.add(MathTex(rf"{int(N)}", rf"\quad {gv:.4f}", font_size=26))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.4, -0.3, 0])
        note_ = VGroup(label(r"the overshoot gets narrower, \ never lower:", font_size=24),
                       label(r"about $9\%$ of the jump, \ for every $N$", font_size=24, color=C.PATHOLOGY)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(tab, DOWN, buff=0.35)
        assert abs(gibbs[-1] - limit) < 1e-3 and np.all(np.diff(gibbs) > 0)
        with self.voiceover(
            "<bookmark mark='a'/> Zoom in on the jump. Next to it, every partial sum overshoots. "
            "<bookmark mark='b'/> As N grows, the overshoot moves closer to the jump and gets narrower, but not lower: "
            "its height tends to about nine percent of the jump, precisely the integral of sine t over t from zero to "
            "pi, over pi, minus a half. <bookmark mark='c'/> Wilbraham noticed it in 1848 and Gibbs explained it in "
            "1899. It's the visible face of non-uniform convergence, and it's why sharp edges in compressed images "
            "and audio come with ringing."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), Create(fpos), Create(fneg), Create(half), FadeIn(half_l))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(nls[0]), FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(Create(lvl), FadeIn(lvl_l), FadeIn(head[1]))
            cur, cl = curves[0], nls[0]
            for k in range(1, len(shown)):
                self.play(ReplacementTransform(cur, curves[k]), FadeTransform(cl, nls[k]), FadeIn(tab[k + 1]),
                          run_time=1.3)
                cur, cl = curves[k], nls[k]
            self.play(FadeIn(tab[len(shown) + 1:]), FadeIn(note_))
            vo.wait_until("c")
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gamma(self):
        from scipy.special import gamma as G
        d = load("parseval")
        sn, st = d["sn"], d["stirling"]
        ax = plain_axes([0, 5, 1], [0, 26, 5], 6.4, 4.2, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.3, -0.9, 0])
        x = np.linspace(0.04, 5, 1200)
        gg = runs(ax, x, G(x), C.FUNC, 3.5)
        facts = VGroup(*[Dot(ax.c2p(k + 1, math.factorial(k)), radius=0.07, color=WHITE) for k in range(5)])
        fl = VGroup(*[MathTex(rf"{k}! = {math.factorial(k)}", font_size=22, color=GREY_A).next_to(facts[k], UL, buff=0.05)
                      for k in (2, 3, 4)])
        head = VGroup(label(r"A card for chapter 8's last topic: \ the gamma function \ (Rudin 8.17--8.22)",
                            font_size=28),
                      MathTex(r"\Gamma(x) = \int_0^\infty t^{x-1} e^{-t}\,dt, \qquad \Gamma(n + 1) = n!", font_size=34,
                              color=C.FUNC)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        side = VGroup(
            label(r"\textbf{Bohr--Mollerup} (8.19): \ the only", font_size=24),
            label(r"$\log$-convex $f$ with $f(x + 1) = x f(x)$, $f(1) = 1$", font_size=24),
            label(r"\textbf{Stirling} (8.22): \ $n! \approx (n/e)^n \sqrt{2\pi n}$", font_size=24, color=C.EPS),
            VGroup(*[MathTex(rf"n = {int(n)}: \ \text{{ratio}} \ {r:.5f}", font_size=24) for n, r in zip(sn, st)]
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.06),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.6, -0.7, 0])
        assert all(abs(G(k + 1) - math.factorial(k)) < 1e-9 for k in range(5))
        with self.voiceover(
            "<bookmark mark='a'/> Rudin's chapter ends with the gamma function, which we'll keep to one card. It "
            "interpolates the factorials, <bookmark mark='b'/> and it's the only interpolation whose logarithm is "
            "convex and which obeys the factorial's recursion: that's the Bohr–Mollerup theorem. <bookmark mark='c'/> "
            "Stirling's formula estimates it: the ratio of n factorial to the formula goes to one, already within a "
            "tenth of a percent at a thousand."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), Create(gg), LaggedStart(*[FadeIn(f_, scale=1.5) for f_ in facts], lag_ratio=0.2),
                      FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(side[:2]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), LaggedStart(*[FadeIn(r_) for r_ in side[3]], lag_ratio=0.3), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()
