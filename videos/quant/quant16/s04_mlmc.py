from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, illustration, load


class MLMC(VoiceoverScene):
    def construct(self):
        m = load("mlmc")
        self.card()
        self.idea()
        self.cost(m)

    def card(self):
        c = chapter_card(3, r"Multilevel Monte Carlo", r"Why simulate every path at the finest step?", part=PART)
        with self.voiceover("Chapter three. Multilevel Monte Carlo."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def idea(self):
        rows = [cmath(r"\mathbb{E}[P_L]", r"=", r"\mathbb{E}[P_0] + \sum_{l=1}^{L}\mathbb{E}\big[P_l - P_{l-1}\big]", font_size=38,
                      colors={r"\mathbb{E}[P_L]": OPT}),
                cmath(r"N_l", r"\propto", r"\varepsilon^{-2}\sqrt{V_l / C_l}\,\sum_k\sqrt{V_k C_k}", font_size=36,
                      colors={r"N_l": GOOD})]
        whys = [why(r"Giles (2008): the fine-step price is the coarse price plus corrections; each correction uses a fine "
                    r"path and a coarse path driven by the same noise, so it is small and has small variance"),
                why(r"spend many cheap paths on the coarse level and few expensive ones on the fine corrections; "
                    r"total cost $\varepsilon^{-2}(\log\varepsilon)^2$ instead of $\varepsilon^{-3}$ for Euler")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-1.0, buff=1.0, edge=6.9)
        with self.voiceover(
            "Simulating a diffusion has two errors: the noise, which falls with more paths, and the bias of the time "
            "step, which falls with finer steps. Reaching accuracy epsilon with Euler steps costs epsilon to the minus "
            "three: a hundred times the paths and ten times the steps for each extra digit. Mike Giles saw in 2008 "
            "that the fine-step price is a coarse-step price plus a ladder of corrections. <bookmark mark='a'/> Each "
            "correction compares a fine path with a coarse path driven by the same random numbers, so it is small and "
            "barely random, and needs few samples. Put most of the paths on the cheap coarse levels and only a "
            "handful on the expensive fine ones, and the cost falls to roughly epsilon to the minus two."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def cost(self, m):
        eps = np.asarray(m["eps"])
        cm = np.array([r["cost"] for r in m["mlmc"]])
        cs = np.array([r["cost"] for r in m["standard"]])
        g = axes([np.log10(0.008), np.log10(0.05)], [6.3, 9.6], x_length=5.6, y_length=4.0,
                 xlabel=r"target accuracy $\varepsilon$", ylabel=r"cost (Euler steps simulated)",
                 xticks=list(np.log10(eps)), xfmt=lambda u: f"{10 ** u:.2f}", yticks=[7, 8, 9],
                 yfmt=lambda u: f"10^{{{int(round(u))}}}", font_size=15, log_x=True)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        ok = np.isfinite(cs)

        def line(x, y, col):
            pts = [ax.c2p(a, np.clip(b, 6.3, 9.6)) for a, b in zip(np.log10(x), np.log10(y))]
            return VGroup(VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(pts),
                          *[Dot(p_, radius=0.06, color=col) for p_ in pts])

        ls = line(eps[ok], cs[ok], BAD)
        lm = line(eps, cm, GOOD)
        leg = legend([(BAD, r"standard Monte Carlo, finest step"), (GOOD, r"multilevel")], font_size=17).next_to(
            g, UP, buff=0.1).align_to(g, LEFT)
        V = np.asarray(m["mlmc"][-1]["V"])
        g2 = axes([-0.5, len(V) - 0.5], [-3.5, 2.5], x_length=4.4, y_length=3.2, xlabel=r"level $l$ (steps $2^l$)",
                  ylabel=r"$\log_{10}$ variance", xticks=list(range(0, len(V), 2)), yticks=[-3, -1, 1], font_size=14)
        g2.next_to(g, RIGHT, buff=1.0).align_to(g, DOWN)
        bars = VGroup(*[Dot(g2.ax.c2p(i, np.log10(v)), radius=0.06, color=OPT) for i, v in enumerate(V)])
        last = int(np.flatnonzero(ok)[-1])
        side = wrapped_label(rf"at $\varepsilon = {eps[last]}$: {cs[last] / cm[last]:.0f} times cheaper. The corrections' "
                             r"variance falls two- to threefold per level, so the deep levels need only a few thousand paths",
                             4.6, 19, GREY_A).next_to(g2, UP, buff=0.3).align_to(g2, LEFT)
        src = illustration(r"a continuously averaged Asian call under Euler; 20\% volatility, one year")
        with self.voiceover(
            "Here is the cost of hitting a target accuracy, on log scales, for a standard estimator at the finest "
            "step it needs, and for the multilevel one. <bookmark mark='a'/> The gap widens as the target tightens: "
            f"at an accuracy of {eps[last]}, multilevel is {cs[last] / cm[last]:.0f} times cheaper. <bookmark mark='b'/> "
            "On the right, why: the variance of each correction falls level by level, so the finest levels need only a "
            "few thousand paths. The method now runs inside bank risk systems, and it is why a simulation's step size "
            "no longer has to be a compromise."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(ls), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(lm), FadeIn(leg[1]))
            vo.wait_until("b")
            self.play(FadeIn(g2), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.1), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
