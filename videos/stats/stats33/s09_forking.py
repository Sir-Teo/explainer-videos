from __future__ import annotations

import numpy as np

from videos.stats.stats33.common import *  # noqa: F403


class Forking(VoiceoverScene):
    def construct(self):
        self.card()
        self.sixty_four()
        self.garden()
        self.stopping()
        self.simulator()
        self.bars()
        self.multiverse()

    def card(self):
        card = chapter_card(8, r"The garden of forking paths", r"Many analyses of one data set", lit=(2011,), part=PART)
        with self.voiceover("Chapter eight. The garden of forking paths."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def sixty_four(self):
        rows = fit_rows(VGroup(
            label(r"2011: \ Joseph Simmons, \ Leif Nelson \& Uri Simonsohn, \ `False-positive psychology'", font_size=24),
            label(r"a real experiment: \ students listened to the Beatles' `When I'm Sixty-Four'", font_size=24),
            label(r"result: \ they became 1.5 years younger, \ $p = 0.04$", font_size=24, color=FALSEC),
            label(r"obtained by flexible, \ entirely common analysis choices, \ reported as if planned", font_size=24, color=SIGC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 2011 the psychologists Joseph Simmons, Leif Nelson and Uri Simonsohn published a paper "
            "called False-Positive Psychology. <bookmark mark='b'/> In a real experiment, students listened either to the "
            "Beatles' When I'm Sixty-Four or to a control song. <bookmark mark='c'/> Afterwards, those who heard the Beatles "
            "were, by their reported birth dates, a year and a half younger, with a p-value of point oh four. "
            "<bookmark mark='d'/> An impossible result, obtained honestly, by a handful of entirely common choices in the "
            "analysis, each reported as though it had been planned."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def garden(self):
        rows = [
            cmath(r"\text{choices}", r":", r"\text{outcome, \ covariates, \ exclusions, \ subgroups, \ when to stop}", font_size=28),
            cmath(r"\text{each made}", r":", r"\text{after seeing the data, \ often in good faith}", font_size=30),
            cmath(r"\text{effective tests}", r"\gg", r"\text{the one reported}", font_size=32),
            cmath(r"\text{p-hacking}", r"\ne", r"\text{fraud: \ the garden of forking paths}", font_size=30),
        ]
        rows[2][-1].set_color(FALSEC)
        whys = [why(r"researcher degrees of freedom"), why(r"each one reasonable"),
                why(r"a multiple-comparisons problem in disguise"), why(r"Gelman \& Loken (2014)")]
        with self.voiceover(
            "<bookmark mark='a'/> Every analysis involves choices: which outcome to report, which covariates to adjust for, "
            "which observations to exclude, which subgroups to examine, when to stop collecting data. "
            "<bookmark mark='b'/> When those choices are made after seeing the data, each can be perfectly reasonable on "
            "its own. <bookmark mark='c'/> But the effective number of tests is far larger than the one reported. "
            "<bookmark mark='d'/> Andrew Gelman and Eric Loken called this the garden of forking paths, to stress that it "
            "needs no deliberate fishing: a single analysis, chosen in light of the data, has the same problem."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def stopping(self):
        d = load("stopping")
        looks, tr = np.asarray(d["looks"]), np.asarray(d["traj"])
        A = axes([0, 105], [0, 1.0], x_length=7.4, y_length=4.4, xlabel=r"subjects per group so far",
                 ylabel=r"$p$-value at each look", xticks=[10, 40, 70, 100], yticks=[0, 0.05, 0.5, 1], center=[-2.0, 0.3, 0])
        ax = A.ax
        line05 = DashedLine(ax.c2p(0, 0.05), ax.c2p(105, 0.05), color=FALSEC, stroke_width=2.5)
        path = VGroup(polyline(ax, looks, tr, BHC, 3), *[Dot(ax.c2p(a, b), radius=0.07, color=BHC) for a, b in zip(looks, tr)])
        hit = Circle(radius=0.2, color=SIGC, stroke_width=3).move_to(ax.c2p(looks[-1], tr[-1]))
        rows = fit_rows(VGroup(
            label(r"no effect at all; \ test after every 10 per group", font_size=22),
            label(r"stop at the first $p < 0.05$", font_size=22, color=FALSEC),
            label(r"this study `succeeds' at 100", font_size=22, color=SIGC),
            label(rf"chance of ever succeeding: \ {100 * d['p_ever']:.0f}\%, \ not 5\%", font_size=22, color=FALSEC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One fork is when to stop. A study with no effect at all, tested after every ten subjects "
            "per group. <bookmark mark='b'/> The rule: stop as soon as p is below five percent. <bookmark mark='c'/> This "
            "study's p-value wanders, and dips below point oh five at the last look: a publishable result. "
            "<bookmark mark='d'/> With ten looks, the chance of ever succeeding is nineteen percent, almost four times the "
            "nominal five. Part 58 builds tests that can be checked at every look, honestly."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(line05))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(path), FadeIn(rows[2]), run_time=2.5)
            self.play(Create(hit))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def simulator(self):
        rows = [
            cmath(r"\text{A}", r":", r"\text{two correlated outcomes: \ report either, \ or their mean}", font_size=30),
            cmath(r"\text{B}", r":", r"\text{20 per group; \ if } p > 0.05, \ \text{add 10 more}", font_size=30),
            cmath(r"\text{C}", r":", r"\text{adjust for gender, \ or its interaction, \ or not}", font_size=30),
            cmath(r"\text{D}", r":", r"\text{three conditions: \ report any two, \ or the trend}", font_size=30),
        ]
        rows[0][-1].set_color(SIGC)
        whys = [why(r"$r = 0.5$"), why(r"optional stopping"), why(r"a covariate"), why(r"dropping a condition")]
        with self.voiceover(
            "<bookmark mark='a'/> This part's build is a simulator of Simmons, Nelson and Simonsohn's four flexibilities, "
            "with no true effect anywhere. A: two correlated outcome measures, reporting either one or their average. "
            "<bookmark mark='b'/> B: twenty subjects per group, and ten more if the first look fails. "
            "<bookmark mark='c'/> C: adjusting for gender, or its interaction with the condition, or not. "
            "<bookmark mark='d'/> D: three conditions, reporting any two or the linear trend."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bars(self):
        d = load("phack")
        keys = ["none", "A", "B", "C", "D", "ABC", "ABCD"]
        names = [r"none", r"A", r"B", r"C", r"D", r"A+B+C", r"all four"]
        paper = [0.05, 0.095, 0.077, 0.117, 0.126, 0.309, 0.607]
        A = axes([0.3, 7.7], [0, 0.7], x_length=8.0, y_length=4.4, xlabel=r"", ylabel=r"false-positive rate",
                 xticks=[], yticks=[0, 0.05, 0.3, 0.6], yfmt=lambda v: f"{v:g}", center=[-1.6, 0.4, 0])
        ax = A.ax
        bars = bars_at(ax, np.arange(1, 8), [d[k] for k in keys], 0.55, SIGC, 0.85)
        pdots = VGroup(*[Line(ax.c2p(i + 0.7, v), ax.c2p(i + 1.3, v), color=WHITE, stroke_width=3) for i, v in enumerate(paper)])
        labs = VGroup(*[label(n, font_size=20, color=GREY_A).next_to(ax.c2p(i + 1, 0), DOWN, buff=0.15) for i, n in enumerate(names)])
        five = DashedLine(ax.c2p(0.3, 0.05), ax.c2p(7.7, 0.05), color=FALSEC, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"5{,}000 simulated null studies", font_size=22),
            label(r"gold: \ our simulator; \ white: \ the 2011 paper", font_size=22, color=SIGC),
            label(rf"each choice alone: \ {100 * d['A']:.0f}--{100 * d['D']:.0f}\%", font_size=22),
            label(rf"all four: \ {100 * d['ABCD']:.0f}\% \ (paper: 60.7\%)", font_size=22, color=FALSEC),
        ), 3.4, 0.42, [5.3, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Five thousand simulated studies with no effect. <bookmark mark='b'/> Gold bars from our "
            "simulator, white marks from the 2011 paper's table; they agree within simulation error. "
            "<bookmark mark='c'/> Each flexibility alone roughly doubles the false-positive rate, to between eight and "
            "thirteen percent. <bookmark mark='d'/> All four together give sixty-one percent. A researcher with these "
            "four ordinary freedoms will find a significant result in a null world more often than not."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), FadeIn(labs), Create(five))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), FadeIn(pdots), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def multiverse(self):
        rows = fit_rows(VGroup(
            label(r"disclose every choice: \ Simmons et al.'s six rules for authors", font_size=26),
            label(r"the multiverse analysis: \ run every reasonable path and show them all \ (Steegen et al. 2016)", font_size=26, color=BHC),
            label(r"many analysts, \ one data set: \ 29 teams, \ odds ratios from 0.9 to 2.9 \ (Silberzahn et al. 2018)", font_size=26, color=SIGC),
            label(r"or fix the path before seeing the data: \ chapter eleven", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Remedies follow from the diagnosis. Simmons and colleagues proposed simple rules: decide "
            "when to stop in advance, report every measure and condition, and show results with and without covariates and "
            "exclusions. <bookmark mark='b'/> A multiverse analysis runs every reasonable path and shows them all. "
            "<bookmark mark='c'/> And when twenty-nine teams were given the same data and the same question, whether "
            "football referees give more red cards to dark-skinned players, their odds ratios ranged from point nine to "
            "two point nine. <bookmark mark='d'/> Or fix the path before seeing the data, as chapter eleven discusses."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
