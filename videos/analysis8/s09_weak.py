from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis8.common import load, plain_axes, polyline


class Weak(VoiceoverScene):
    def construct(self):
        self.card()
        self.unit_vectors()
        self.three_ways()
        self.mazur()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(8, r"Weak convergence", r"Can a sequence converge without getting close?", lit=(), part=8)
        with self.voiceover("Chapter eight: weak convergence, convergence as seen by every functional."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def unit_vectors(self):
        d = load("weak")
        ns, inner = d["ns"], d["inner"]
        ax = plain_axes([0.5, 12.5, 1], [0, 1.15, 0.5], 6.4, 2.2).move_to([-3.2, 1.0, 0])
        y = np.array([1 / k for k in range(1, 13)])
        y = y / np.linalg.norm(1 / np.arange(1, 4001))
        ydots = VGroup(*[Dot(ax.c2p(k + 1, v), radius=0.05, color=C.INNER) for k, v in enumerate(y)])
        nT = ValueTracker(1)

        def bar():
            n = int(round(nT.get_value()))
            return VGroup(Rectangle(width=0.32, height=ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=C.EPS,
                                    fill_opacity=0.9).move_to(ax.c2p(n, 0.5)),
                          MathTex(rf"e_{{{n}}}", font_size=24, color=C.EPS).next_to(ax.c2p(n, 1), UP, buff=0.04))

        eb = always_redraw(bar)
        rd = always_redraw(lambda: VGroup(
            MathTex(r"\|e_n\| = 1", font_size=28),
            MathTex(rf"\langle e_n, y\rangle = y_{{{int(round(nT.get_value()))}}} = {y[int(round(nT.get_value())) - 1]:.4f}",
                    font_size=28, color=C.INNER)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.4, 1.2, 0]))
        tab = VGroup(MathTex(r"n", r"\quad \max_{50 \text{ random } y} |\langle e_n, y\rangle|", font_size=24, color=GREY_A))
        for n, v in zip(ns, inner):
            tab.add(MathTex(f"{int(n)}", rf"\quad {v:.4f}", font_size=26, color=C.INNER))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.4, -1.2, 0])
        regrid(tab)
        assert np.all(np.diff(inner) < 0)
        defn = VGroup(
            label(r"$x_n \rightharpoonup x$ \ (weakly) \ if $\Lambda x_n \to \Lambda x$ for every $\Lambda \in X^*$",
                  font_size=26, color=C.EPS),
            label(r"in $\ell^2$: \ every $\Lambda$ is $\langle \cdot, y\rangle$, \ and $y_n \to 0$: \ so $e_n \rightharpoonup 0$",
                  font_size=24),
            label(r"but $\|e_n - 0\| = 1$: \ no convergence in norm", font_size=24, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-3.0, -1.6, 0])
        for r_ in defn:
            if r_.width > 7.0:
                r_.width = 7.0
        y_l = MathTex(r"y = c\,(1, \tfrac12, \tfrac13, \ldots)", font_size=24, color=C.INNER).next_to(ax, UP, buff=0.35)
        head = label(r"Converging weakly: \ every functional's view converges", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> The unit vectors of l two never get close to anything: each is root two from every "
            "other, and one from zero. <bookmark mark='b'/> But look at them through a fixed functional, the inner "
            "product with a vector y. That reading is just the n-th coordinate of y, which goes to zero. "
            "<bookmark mark='c'/> For fifty random y's, the largest reading falls steadily. "
            "<bookmark mark='d'/> So e n converges to zero weakly: every functional sees the sequence converge, even "
            "though its norm never shrinks."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(eb))
            self.play(nT.animate.set_value(4), run_time=1.5, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(ydots), FadeIn(y_l), FadeIn(rd))
            self.play(nT.animate.set_value(12), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(defn))
        for m in (eb, rd):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def three_ways(self):
        panels = VGroup()
        specs = [
            (r"oscillate: \ $\sin nx$", lambda x, n: np.sin(n * x) / math.sqrt(math.pi), (0, 2 * math.pi), (-1.2, 1.2), C.SEQ),
            (r"concentrate: \ $\sqrt n\,\mathbf 1_{[0, 1/n]}$", lambda x, n: math.sqrt(n) * ((x >= 0) & (x <= 1 / n)),
             (0, 1), (0, 3.4), C.APPROX),
            (r"escape: \ $\mathbf 1_{[n, n+1]}$", lambda x, n: ((x >= n) & (x <= n + 1)).astype(float), (0, 10), (0, 1.3),
             C.MEASURE),
        ]
        nT = ValueTracker(1.0)
        for k, (ttl, F, xr, yr, col) in enumerate(specs):
            ax = plain_axes([xr[0], xr[1], (xr[1] - xr[0]) / 4], [yr[0], yr[1], (yr[1] - yr[0]) / 2], 3.8, 2.4).move_to(
                [-4.6 + 4.6 * k, 0.4, 0])
            x = np.linspace(xr[0], xr[1], 2000)
            g = always_redraw(lambda ax=ax, F=F, x=x, col=col: runs(ax, x, F(x, nT.get_value()), col, 3))
            t = label(ttl, font_size=24, color=col).next_to(ax, UP, buff=0.1)
            panels.add(VGroup(ax, g, t))
        # the three are weakly null in L^2, with norm 1
        d = load("weak")
        pair, pns = d["pair"], d["pair_ns"]
        notes = VGroup(
            label(r"all three have $\|f_n\|_2 = 1$ \ and $\langle f_n, g\rangle \to 0$ for every $g \in L^2$", font_size=26,
                  color=C.EPS),
            MathTex(r"\Big|\int_0^{2\pi} \sin(nx)\, g(x)\,dx\Big|,\ n = 1, 4, 16, 64, 256: \ " +
                    r",\ ".join(f"{v:.4f}" for v in pair), font_size=24, color=C.SEQ),
            label(r"(Riemann--Lebesgue, \ for $g = e^{-(x - 2)^2} + 0.3x$)", font_size=20, color=GREY_A),
            label(r"the bump engine's evil twins: \ Part 3's dashboard lights the ``tested'' lens, \ never the norm",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        assert np.all(np.diff(pair) < 0)
        head = label(r"Three ways to go weakly to $0$ without going to $0$", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> In L two there are three ways to converge weakly without converging. "
            "<bookmark mark='b'/> Oscillate: sine n x wiggles faster and faster, and against any fixed function its "
            "integral fades, by the Riemann-Lebesgue lemma. <bookmark mark='c'/> Concentrate: a tall thin spike of "
            "norm one sees less and less of any fixed function. Escape: a bump sliding off to infinity. "
            "<bookmark mark='d'/> All have norm one, all converge weakly to zero. These are the bump's evil twins from "
            "Part 3, back as the standard examples."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), *[FadeIn(p_[0]) for p_ in panels], *[FadeIn(p_[2]) for p_ in panels])
            self.add(*[p_[1] for p_ in panels])
            vo.wait_until("b")
            self.play(nT.animate.set_value(3.0), run_time=2.0)
            vo.wait_until("c")
            self.play(nT.animate.set_value(8.0), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(notes))
        for p_ in panels:
            p_[1].clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mazur(self):
        d = load("weak")
        Ns, avg = d["Ns"], d["avg"]
        ax = plain_axes([0, 2 * math.pi, math.pi / 2], [-1.6, 2.2, 1], 6.4, 3.4).move_to([-3.2, -0.5, 0])
        x = np.linspace(0, 2 * math.pi, 2000)
        cols = [C.SEQ, C.APPROX, C.EPS, C.CONNECTED_SET]
        curves = [polyline(ax, x, np.mean([np.sin(n * x) for n in range(1, N + 1)], axis=0), color=c, stroke_width=2.5)
                  for N, c in zip(Ns, cols)]
        labs = [MathTex(rf"\frac{{1}}{{{N}}}\sum_{{n \le {N}}} \sin nx: \ \|\cdot\|_2 = {a:.4f}", font_size=26, color=c)
                .next_to(ax, UP, buff=0.1) for N, a, c in zip(Ns, avg, cols)]
        assert np.allclose(avg, np.sqrt(np.pi / Ns), rtol=1e-4)
        rows = VGroup(
            label(r"\textbf{FA 3.13} \ (Mazur) \ a weak limit is a \emph{norm} limit", font_size=24),
            label(r"of convex combinations", font_size=24),
            MathTex(r"\Big\|\frac1N\sum_{n \le N} \sin nx\Big\|_2 = \sqrt{\pi/N} \to 0", font_size=28, color=C.EPS),
            label(r"so closed convex sets are weakly closed", font_size=24, color=C.EPS),
            label(r"weakly convergent sequences are bounded", font_size=22, color=GREY_A),
            label(r"(Banach--Steinhaus, \ applied in $X^{**}$)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.7, -0.5, 0])
        for r_ in rows:
            if r_.width > 5.8:
                r_.width = 5.8
        head = label(r"Averaging turns weak convergence into norm convergence", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Weak limits aren't far from norm limits, though. Average the first N sine waves. "
            "<bookmark mark='b'/> The averages really do shrink, in norm, like the square root of pi over N. "
            "<bookmark mark='c'/> Mazur's theorem says this always happens: a weak limit is a norm limit of convex "
            "combinations. So closed convex sets are also weakly closed. And by Banach and Steinhaus, a weakly "
            "convergent sequence is always bounded."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(curves[0]), FadeIn(labs[0]))
            vo.wait_until("b")
            for k in range(1, 4):
                self.play(ReplacementTransform(curves[k - 1], curves[k]), FadeTransform(labs[k - 1], labs[k]),
                          run_time=1.1)
            vo.wait_until("c")
            self.play(FadeIn(rows[:4]))
            self.play(FadeIn(rows[4:]))
        self.wait(0.4)
        self.clear_scene()
