from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant25.common import (BAD, FALSE, GOOD, HURDLE, NOISE, PART, SDF, TRUE, era_strip, fit_right,
                                         illustration, load)


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.coins(load("noise"))
        self.zoo(load("zoo"))
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"The Factor Zoo")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part twenty-five. The factor zoo: hundreds of published ways to beat the market, and how to tell the few "
            "that are real from the many that were found by looking."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def coins(self, n):
        t = np.sort(np.asarray(n["example_t"]))
        g = axes([-0.5, 200.5], [-3.5, 3.5], x_length=8.4, y_length=4.4, xlabel=r"200 strategies, sorted",
                 ylabel=r"$t$-statistic of the mean", xticks=[], yticks=[-3, -2, 0, 2, 3], font_size=14).to_edge(
            LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup(*[Line(ax.c2p(i, 0), ax.c2p(i, v), color=TRUE if v > 1.96 else NOISE, stroke_width=2.2)
                        for i, v in enumerate(t)])
        h = DashedLine(ax.c2p(0, 1.96), ax.c2p(200, 1.96), color=HURDLE, stroke_width=2)
        side = VGroup(
            MathTex(rf"\text{{best}}:\ t = {n['example_best']:.2f}", font_size=28, color=TRUE),
            MathTex(rf"\text{{above 1.96}}:\ {int((t > 1.96).sum())}\ \text{{of 200}}", font_size=26, color=TRUE),
            wrapped_label(r"two hundred strategies of pure noise: twenty years of monthly returns, each with a true "
                          r"premium of exactly zero. A few clear the usual hurdle by chance alone, and the best looks "
                          r"like a discovery", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Two hundred trading strategies, each with twenty years of monthly returns, and every one of them pure "
            "noise: the true premium is exactly zero. <bookmark mark='a'/> Sort them by their t-statistic. About one "
            "in forty clears the textbook hurdle of two by chance alone, and the best has a t-statistic near three. "
            "Published as the only strategy its author tried, it would look like a discovery. <bookmark mark='b'/> "
            "Finance has tested far more than two hundred."
        ) as vo:
            self.play(FadeIn(g), Create(h))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b_) for b_ in bars], lag_ratio=0.01), FadeIn(side[0]), FadeIn(side[1]),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.add(illustration(r"simulated: the House's \texttt{zoo.noise\_max\_t}"))
        self.wait(0.4)
        self.clear_scene()

    def zoo(self, z):
        yrs, cnt = np.asarray(z["years"]), np.asarray(z["count"])
        g = axes([1970, 2017], [0, 220], x_length=8.2, y_length=4.4, xlabel=r"year of publication",
                 ylabel=r"predictors published, cumulative", xticks=[1970, 1980, 1990, 2000, 2010],
                 yticks=[0, 50, 100, 150, 200], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, yrs, cnt, SDF, stroke_width=3)
        side = VGroup(
            MathTex(rf"{z['n']}\ \text{{predictors}}", font_size=30, color=SDF),
            wrapped_label(r"Chen and Zimmermann's Open Source Asset Pricing: every predictor of the cross-section of US "
                          r"stock returns they could rebuild from its paper, 1973 to 2016. Harvey, Liu and Zhu (2016) "
                          r"counted 316 published factors; later counts run past 400", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here is how many predictors of stock returns were published, year by year, in one careful open-source "
            "collection. <bookmark mark='a'/> A handful in the 1970s, about fifty by 2000, more than two hundred by "
            "2016. John Cochrane called it a zoo of new factors. Every one was significant in its paper; that is how "
            "it was published. How many would be, if we knew how many had been tried?"
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side), run_time=2.5)
        self.add(illustration(r"Open Source Asset Pricing, release 2024.10 (SignalDoc)"))
        self.wait(0.4)
        self.clear_scene()

    def history(self):
        I, C = QC.IDEA, QC.CRISIS
        entries = [(1979, r"Holm's step-down", I), (1995, r"Benjamini--Hochberg", I), (2000, r"White's reality check", I),
                   (2005, r"Romano--Wolf", I), (2010, r"Lewellen--Nagel--Shanken", I), (2011, r"Cochrane's zoo", I),
                   (2016, r"Harvey--Liu--Zhu: $t > 3$", I), (2018, r"Barillas--Shanken", I), (2020, r"KNS; FGX; HXZ", I),
                   (2021, r"Giglio--Xiu", I), (2022, r"open-source AP", I), (2023, r"Jensen--Kelly--Pedersen", I)]
        strip = era_strip(entries, y0=1975, y1=2026, font_size=14).move_to(DOWN * 0.3)
        head = label(r"How the zoo was tamed", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 4), (4, 8), (8, 12)]
        with self.voiceover(
            "The tools came from statistics first: Sture Holm's step-down procedure in 1979, Yoav Benjamini and Yosef "
            "Hochberg's false discovery rate in 1995, Halbert White's reality check for data snooping in 2000. "
            "<bookmark mark='a'/> Finance caught up as the zoo grew: Cochrane named it in 2011, and Campbell Harvey, "
            "Yan Liu and Heqing Zhu argued in 2016 that a new factor should need a t-statistic above three. "
            "<bookmark mark='b'/> Then came shrinkage and selection methods built for many factors at once, the "
            "replication studies, and open-source data that anyone can check."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), m in zip(groups, [None, "a", "b"]):
                if m:
                    vo.wait_until(m)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"The best of many noisy strategies; the hurdle rising with the count",
            r"Bonferroni, Holm and the false discovery rate, on two hundred predictors",
            r"Replication: Hou--Xue--Zhang against Jensen--Kelly--Pedersen; open-source asset pricing",
            r"Decay, shrinkage, publication bias; mined signals against published ones",
            r"Shrinking the cross-section; taming the zoo; weak factors; PCA, RP-PCA, IPCA",
            r"Comparing models; a shrinkage SDF registered and scored on 2021--2023",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: the best of many noisy strategies, and how the hurdle must rise with the count; three ways of "
            "correcting for many tests; whether the zoo replicates; how much it decays, and why; whether mined signals "
            "do worse than published ones; four modern methods built for hundreds of factors at once; how to compare "
            "models; and a shrinkage discount factor, registered and opened on the sealed years."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=11))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("research",))
        with self.voiceover(
            "In the House, the research desk adds its first statistical model of returns: a discount factor that "
            "loads on the whole zoo at once, shrunk toward caution, and kept honest by counting every trial."
        ):
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
