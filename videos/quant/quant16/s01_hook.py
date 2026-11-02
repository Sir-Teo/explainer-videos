from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, METHOD_COL, OPT, PART, illustration, load


class Hook(VoiceoverScene):
    def construct(self):
        r = load("race")
        self.title_card()
        self.spread(r)
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"One price, many machines")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part sixteen. Computing prices. The models of the last six parts are equations; this part is about "
            "turning them into numbers, fast enough and accurately enough for a trading desk."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def spread(self, r):
        pts = r["points"]
        best = {}
        for p_ in pts:
            b = best.get(p_["method"])
            if b is None or p_["err"] < b["err"]:
                best[p_["method"]] = p_
        order = ["Monte Carlo (QE, 50 steps)", "ADI (Craig-Sneyd)", "Carr-Madan FFT", "COS"]
        rows = VGroup()
        for m in order:
            if m not in best:
                continue
            b = best[m]
            rows.add(VGroup(label(m, font_size=24, color=METHOD_COL[m]),
                            MathTex(rf"\text{{error}}\ {b['err']:.0e}", font_size=28),
                            MathTex(rf"{b['time']:.4f}\,\text{{s}}", font_size=28)))
        for row in rows:
            row[0].set_x(-3.6)
            row[1].set_x(1.2)
            row[2].set_x(4.2)
        rows.arrange(DOWN, buff=0.45)
        for row in rows:
            row[0].set_x(-3.6)
            row[1].set_x(1.2)
            row[2].set_x(4.2)
        head = label(rf"one Heston call, four engines (price {r['ref']:.4f})", font_size=28).to_edge(UP, buff=0.9)
        rows.next_to(head, DOWN, buff=0.6)
        foot = label(r"the same answer, at costs that differ by orders of magnitude", font_size=24, color=GOOD).to_edge(DOWN, buff=0.9)
        src = illustration(r"each engine's most accurate run in the race of chapter 8; one CPU core")
        with self.voiceover(
            "Here is one option, a one-year call under the Heston model of Part thirteen, priced four ways by the "
            "House's engine. <bookmark mark='a'/> Simulation, a grid, and two Fourier methods. They agree on the "
            "price. They do not agree on what it costs to get there, or on how much you can trust the last digits. "
            "Choosing the method, and knowing its error, is the craft of this part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.4, run_time=3),
                      FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Monte Carlo at $1/\sqrt n$; antithetics, control variates, importance sampling",
            r"Quasi-Monte Carlo: Sobol points and the Brownian bridge",
            r"Multilevel Monte Carlo: $\varepsilon^{-2}$ instead of $\varepsilon^{-3}$",
            r"American options by regression, bracketed by a duality bound",
            r"Greeks three ways, and all of them at once by adjoint differentiation",
            r"Finite differences: Crank--Nicolson, Rannacher, the American LCP, ADI for Heston",
            r"Fourier pricing, the race, and what hardware buys",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan. Monte Carlo and the tricks that make it converge faster. Quasi-random points, and the bridge "
            "that makes them work on paths. Multilevel simulation. American options by simulation, bracketed from both "
            "sides. Greeks, and adjoint differentiation. Grids for one and two dimensions. Fourier methods, a race "
            "between all of them, and what faster hardware really buys."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=10))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("data", "vol"))
        with self.voiceover(
            "In the House, this part builds the pricing engine that every desk shares. <bookmark mark='a'/> Its rule: "
            "no number leaves it without an estimate of its own error."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
