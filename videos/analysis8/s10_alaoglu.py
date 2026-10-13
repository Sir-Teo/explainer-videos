from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis8.common import load, plain_axes


def histogram(ax, xc, w, color, opacity=0.6, scale=1.0):
    bw = xc[1] - xc[0]
    g = VGroup()
    for x, v in zip(xc, w):
        h = ax.c2p(0, v * scale)[1] - ax.c2p(0, 0)[1]
        g.add(Rectangle(width=ax.c2p(bw, 0)[0] - ax.c2p(0, 0)[0], height=max(h, 0.001), stroke_width=0.5,
                        stroke_color=BACKGROUND, fill_color=color, fill_opacity=opacity).move_to(ax.c2p(x, v * scale / 2)))
    return g


class Alaoglu(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.measures()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(9, r"Banach--Alaoglu", r"Where does compactness come back?", lit=(), part=8)
        with self.voiceover("Chapter nine: the compactness that infinite dimensions take away comes back, in the "
                            "weak-star topology."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def theorem(self):
        thm = VGroup(
            label(r"\textbf{FA 3.15} \ (Banach--Alaoglu) \ the closed unit ball of $X^*$ is weak-$*$ compact", font_size=30,
                  color=C.EPS),
            label(r"weak-$*$: \ $\Lambda_\alpha \to \Lambda$ \ iff \ $\Lambda_\alpha x \to \Lambda x$ for every $x \in X$",
                  font_size=26),
        ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        # the dual ball of l^1: a point is a choice of one value in [-1, 1] for each coordinate
        intervals = VGroup()
        rng = np.random.default_rng(2)
        vals = rng.uniform(-1, 1, 10)
        dots = VGroup()
        for k in range(10):
            x = -6.0 + 0.62 * k
            intervals.add(Line([x, -2.2, 0], [x, 0.2, 0], color=GREY_B, stroke_width=3))
            dots.add(Dot([x, -1.0 + 1.2 * vals[k], 0], radius=0.07, color=C.FUNCTIONAL))
        dl = VGroup(*[MathTex(rf"\Lambda e_{{{k + 1}}}", font_size=18, color=GREY_B).move_to([-6.0 + 0.62 * k, -2.5, 0])
                      for k in range(10)])
        dl.add(MathTex(r"\cdots", font_size=30).move_to([0.5, -1.0, 0]))
        cube = label(r"$X = \ell^1$: \ $\{\|\Lambda\| \le 1\} = [-1, 1]^{\N}$, \ a product of intervals", font_size=24,
                     color=C.FUNCTIONAL).move_to([-3.1, 0.75, 0])
        pm = ProofMap([r"$\Lambda \mapsto (\Lambda x)_{x \in X}$ embeds the ball in $\prod_x [-\|x\|, \|x\|]$",
                       r"Tychonoff: \ a product of compact sets is compact", r"the image is closed \ (linearity is a "
                       r"pointwise condition)"], font_size=20, width=5.0, buff=0.22, direction=DOWN).move_to([3.9, -1.0, 0])
        notes = label(r"for separable $X$, \ every bounded sequence in $X^*$ has a weak-$*$ convergent subsequence "
                      r"\ (FA 3.17)", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Banach-Alaoglu: the closed unit ball of a dual space is compact in the weak-star "
            "topology, where functionals converge when their values at each point converge. "
            "<bookmark mark='b'/> For the dual of l one, a functional of norm at most one is just a choice of a number "
            "between minus one and one for each coordinate: a point of an infinite cube. <bookmark mark='c'/> In "
            "general, each functional is a point in a product of intervals, one interval for each vector. Tychonoff's "
            "theorem says the product is compact, and linearity is a closed condition. <bookmark mark='d'/> For "
            "separable spaces there's a sequential version, proved by Cantor's diagonal argument, which is how it's "
            "used most often."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(FadeIn(cube), LaggedStart(*[Create(i_) for i_ in intervals], lag_ratio=0.1), FadeIn(dl))
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(pm))
            for k in range(3):
                self.play(*pm.light(k), run_time=0.6)
            self.play(*pm.done())
            vo.wait_until("d")
            self.play(FadeIn(notes))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measures(self):
        d = load("alaoglu")
        xc, w_first, w_sub, w_lim, sub, errs, m1 = d["xc"], d["w_first"], d["w_sub"], d["w_lim"], d["sub"], d["errs"], d["m1"]
        bins = len(xc)
        dens = lambda w: w * bins  # noqa: E731  probability -> density
        ax = plain_axes([0, 1, 0.25], [0, 2.2, 1], 5.0, 2.4).move_to([-3.6, 0.6, 0])
        hs = [histogram(ax, xc, dens(w), C.SEQ) for w in w_first]
        hl = [MathTex(rf"\mu_{{{n}}}", font_size=28, color=C.SEQ).next_to(ax, UP, buff=0.05) for n in (1, 2, 3, 4)]
        bx = plain_axes([0, 60, 10], [0.4, 0.6, 0.1], 5.0, 1.6).move_to([-3.6, -2.3, 0])
        mpts = VGroup(*[Dot(bx.c2p(k + 1, v), radius=0.03, color=C.SEQ) for k, v in enumerate(m1)])
        b_l = MathTex(r"\int x\,d\mu_n, \ n = 1, \ldots, 60: \text{ no limit}", font_size=22, color=C.SEQ).next_to(
            bx, UP, buff=0.05)
        cx = plain_axes([0, 1, 0.25], [0, 2.2, 1], 5.0, 2.4).move_to([3.4, 0.6, 0])
        lim = VGroup(*[Line(cx.c2p(x - 0.5 / bins, v), cx.c2p(x + 0.5 / bins, v), color=WHITE, stroke_width=3)
                       for x, v in zip(xc, dens(w_lim))])
        hsub = [histogram(cx, xc, dens(w), C.EPS) for w in w_sub]
        sl = [MathTex(rf"\mu_{{{int(n)}}}", font_size=28, color=C.EPS).next_to(cx, UP, buff=0.05) for n in sub]
        tab = VGroup(MathTex(r"n_k", r"\quad \max_{j \le 4} |\textstyle\int x^j d\mu_{n_k} - \int x^j d\mu|", font_size=22,
                             color=GREY_A))
        for n, e in zip(sub, errs):
            tab.add(MathTex(f"{int(n)}", rf"\quad {sci(float(e), 1)}", font_size=24, color=C.EPS))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.4, -2.2, 0])
        regrid(tab)
        assert np.ptp(m1) > 0.05 and np.all(np.diff(errs) < 0)
        head = label(r"Probability measures on $[0, 1]$: \ a sequence with no limit has a convergent subsequence",
                     font_size=28).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Here's the payoff for measures. Probability measures on the unit interval are "
            "functionals on the continuous functions, all in the dual unit ball. <bookmark mark='b'/> This sequence "
            "keeps changing shape: its mean wanders forever and never settles. <bookmark mark='c'/> But Alaoglu "
            "promises a weak-star convergent subsequence. Take n equal to 6, 44, 710, 103993, nearly multiples of two "
            "pi. Along it, the histograms settle onto a limit measure, and every moment converges: the error drops "
            "to four ten-millionths. This is how analysts produce limits of measures, from Haar measure to "
            "Prokhorov's theorem in probability."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(hs[0]), FadeIn(hl[0]))
            vo.wait_until("b")
            for k in range(1, 4):
                self.play(ReplacementTransform(hs[k - 1], hs[k]), FadeTransform(hl[k - 1], hl[k]), run_time=0.8)
            self.play(Create(bx), FadeIn(b_l), LaggedStart(*[FadeIn(p_) for p_ in mpts], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(cx), FadeIn(lim), FadeIn(hsub[0]), FadeIn(sl[0]), FadeIn(tab[:2]))
            for k in range(1, 4):
                self.play(ReplacementTransform(hsub[k - 1], hsub[k]), FadeTransform(sl[k - 1], sl[k]),
                          FadeIn(tab[k + 1]), run_time=1.0)
        self.wait(0.4)
        self.clear_scene()
