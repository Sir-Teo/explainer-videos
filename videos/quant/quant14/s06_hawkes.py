from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import BAD, IV, OPT, PART, ROUGH, RV, VAR, illustration, load


class Hawkes(VoiceoverScene):
    def construct(self):
        h = load("hawkes")
        self.card()
        self.flows(h)
        self.theory()

    def card(self):
        c = chapter_card(5, r"Where roughness comes from", r"Why would volatility be rough?", part=PART)
        with self.voiceover("Chapter five. Where roughness comes from."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def flows(self, h):
        grid = np.asarray(h["grid"])
        mid = 0.5 * (grid[1:] + grid[:-1])
        keys = ("0.5", "0.9", "0.99")
        cols = (VAR, IV, ROUGH)
        panels = VGroup()
        for k, c in zip(keys, cols):
            y = np.asarray(h[k]["counts"], float)
            y = y / y.mean()
            g = axes([0, grid[-1]], [0, 12], x_length=10.4, y_length=1.5, xticks=[], yticks=[0, 6, 12], font_size=13)
            bars = VMobject(stroke_color=c, stroke_width=1.6).set_points_as_corners(
                [g.ax.c2p(t, min(v, 12)) for t, v in zip(mid, y)])
            t = label(rf"branching ratio {k}: each trade triggers {float(k):g} more on average"
                      + (r" (nearly unstable)" if k == "0.99" else ""), font_size=19, color=c).next_to(g, UP, buff=0.05).align_to(g, LEFT)
            panels.add(VGroup(g, bars, t))
        panels.arrange(DOWN, buff=0.35).move_to(UP * 0.2)
        foot = label(r"trading activity in equal time bins, relative to its average; every process has the same mean rate",
                     font_size=18, color=GREY_A).to_edge(DOWN, buff=0.7)
        src = illustration(r"Hawkes processes with exponential kernels (Part 5's simulator)")
        with self.voiceover(
            "Why would volatility be rough? Look at where it comes from: orders. Part five modelled order arrivals as "
            "a Hawkes process, in which every trade raises the chance of another. Each panel has the same average "
            "rate of trading. When each trade triggers half a trade on average, activity is steady. "
            "<bookmark mark='a'/> At nine-tenths, it starts to cluster. <bookmark mark='b'/> At ninety-nine "
            "hundredths, the edge of instability, almost all activity is triggered by other activity: long calms, "
            "sudden storms, clusters inside clusters. Real markets sit right there. Fitted to order flow, the "
            "branching ratio comes out close to one, because most orders are reactions to other orders: splitting, "
            "hedging, market making."
        ) as vo:
            self.play(FadeIn(panels[0]), FadeIn(src), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(panels[1]))
            vo.wait_until("b")
            self.play(FadeIn(panels[2]))
        self.wait(0.4)
        self.clear_scene()

    def theory(self):
        rows = [cmath(r"\lambda_t", r"=", r"\mu + \int_0^t \phi(t - s)\,dN_s,\qquad \|\phi\|_1 \to 1,\quad \phi(t) \sim "
                      r"t^{-(1 + \alpha)}", font_size=34, colors={r"\lambda_t": IV}),
                cmath(r"\text{scaling limit}", r"=", r"\text{rough Heston},\quad H = \alpha - \tfrac12", font_size=36,
                      colors={r"\text{scaling limit}": ROUGH})]
        whys = [why(r"nearly unstable (branching ratio near one) with heavy-tailed memory, as order flow is measured to be "
                    r"(Hardiman, Bercot and Bouchaud 2013)"),
                why(r"Jaisson and Rosenbaum (2016); El Euch, Fukasawa and Rosenbaum (2018): zoom out, and the intensity "
                    r"becomes a rough Heston variance; no-arbitrage at high frequency also forces a leverage effect")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-1.4, buff=1.0, edge=6.9)
        with self.voiceover(
            "Thibault Jaisson and Mathieu Rosenbaum made this precise in 2016. Take a Hawkes process whose branching "
            "ratio approaches one, and whose memory decays slowly, like a power law, as measured in real order flow. "
            "<bookmark mark='a'/> Zoom out, and its intensity converges to the variance of a rough Heston model, with "
            "H set by the memory's tail. With Omar El Euch and Masaaki Fukasawa they showed that ruling out arbitrage "
            "at high frequency also forces the leverage effect. Roughness, on this account, is not a modelling "
            "choice. It is what reactive order flow looks like from a distance."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()
