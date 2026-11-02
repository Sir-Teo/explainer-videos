from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import sim
from videos.quant.quant14.common import BAD, IV, PART, ROUGH, RV, VAR, illustration, load


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.zoom()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Rough")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part fourteen. Rough and path-dependent volatility. The newest chapter of volatility modelling, and "
            "the most argued over."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def zoom(self):
        n = 4096
        rough = np.asarray(sim.fbm(0.1, n, 1.0, 1, seed=3)).ravel()[: n + 1]
        smooth = np.asarray(sim.fbm(0.5, n, 1.0, 1, seed=3)).ravel()[: n + 1]
        panels = VGroup()
        anims = []
        for z, col, txt in ((smooth, VAR, r"$H = 0.5$: Brownian"), (rough, ROUGH, r"$H = 0.1$: rough")):
            row = VGroup()
            for span in (n, n // 16, n // 256):
                seg = z[:span + 1]
                seg = (seg - seg.min()) / max(seg.max() - seg.min(), 1e-12)
                g = axes([0, span], [0, 1], x_length=3.8, y_length=1.7, xticks=[], yticks=[], font_size=12)
                row.add(VGroup(g, curve(g.ax, np.arange(span + 1), seg, col, stroke_width=1.6)))
            row.arrange(RIGHT, buff=0.35)
            t = label(txt, font_size=22, color=col).next_to(row, UP, buff=0.1).align_to(row, LEFT)
            panels.add(VGroup(t, row))
        panels.arrange(DOWN, buff=0.5).move_to(UP * 0.1)
        heads = VGroup(*[label(s, font_size=18, color=GREY_A).next_to(panels[1][1][i], DOWN, buff=0.12)
                         for i, s in enumerate((r"the whole path", r"zoomed 16 times", r"zoomed 256 times"))])
        src = illustration(r"fractional Brownian motion, each panel rescaled to fill its box")
        with self.voiceover(
            "Here are two random paths, each shown whole, then zoomed sixteen times, then two hundred and fifty-six "
            "times, every panel rescaled to fill its box. A Brownian path looks smoother and smoother as you zoom: at "
            "small scales it is almost a straight line. <bookmark mark='a'/> This one does not. It looks equally "
            "jagged at every scale. Its Hurst exponent is a tenth, and in 2014 three researchers found that "
            "volatility itself, measured in the market, looks like this one, not the other."
        ) as vo:
            self.play(FadeIn(panels[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(panels[1]), FadeIn(heads))
        self.wait(0.5)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"The fact: the at-the-money skew grows like $T^{H - 1/2}$; the power law and its rival",
            r"Volatility is rough: the Gatheral--Jaisson--Rosenbaum estimator, run on bitcoin",
            r"Rough Bergomi and rough Heston, calibrated to the Surface",
            r"Where roughness comes from: nearly unstable order flow",
            r"Markovian lifts; the debate over whether volatility is rough at all",
            r"Path-dependent volatility, fitted to DVOL out of sample",
            r"The frontier: quadratic rough Heston, signatures, and fast calibration",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan. The fact that started it: how the skew grows as expiry nears. The measurement that named it, "
            "run on Bitcoin. The two rough models desks know, fitted to the Surface. A theory of where roughness comes "
            "from. How to make a rough model Markovian. The case against roughness, taken seriously. A rival view, "
            "that volatility is mostly a function of the past. And the frontier."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=10))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("vol",))
        with self.voiceover(
            "In the House, the volatility desk opens a rough lab. <bookmark mark='a'/> It adds models, and a rule for "
            "when a new model has earned its place."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
