from __future__ import annotations

import numpy as np

from videos.stats.stats16.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.efron()
        self.scatter()
        self.formula()
        self.name()
        self.objectives()

    def efron(self):
        tl = timeline(lit=(1979,)).to_edge(UP, buff=0.35)
        hc = history_card(1979, r"Bradley Efron, \ Stanford, \ \emph{Annals of Statistics}",
                          r"``Bootstrap methods: \ another look at the jackknife'': \ estimate the sampling distribution of almost any "
                          r"statistic by resampling the data themselves", color=BOOT, width=10.4, font_size=24).move_to([0, 1.1, 0])
        rows = fit_rows(VGroup(
            label(r"every interval since Part 8 leaned on a model: \ normal, \ binomial, \ Poisson", font_size=24),
            label(r"what if the statistic has no formula, \ or the model is doubtful?", font_size=24, color=RES),
            label(r"let the data stand in for the population", font_size=26, color=BOOT),
        ), 12.4, 0.3, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1979 Bradley Efron, at Stanford, published a paper with a modest title: Bootstrap methods, "
            "another look at the jackknife. It became one of the most influential papers in statistics. <bookmark mark='b'/> "
            "Every interval since Part 8 leaned on a model for the data: normal, binomial or Poisson, with a formula for the "
            "standard error. <bookmark mark='c'/> But what if the statistic has no formula, or the model is doubtful? "
            "<bookmark mark='d'/> Efron's idea was to let the data stand in for the population, and simulate."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def scatter(self):
        d = load("law")
        L, G = np.asarray(museum.LAW_LSAT), np.asarray(museum.LAW_GPA)
        A = axes([530, 680], [2.6, 3.6], x_length=6.6, y_length=4.4, xlabel=r"average LSAT", ylabel=r"average GPA", xticks=[550, 600, 650],
                 yticks=[2.8, 3.0, 3.2, 3.4], center=[-2.4, 0.2, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.09, color=DATA) for a, b in zip(L, G)])
        rows = fit_rows(VGroup(
            label(r"15 American law schools, \ 1973", font_size=24),
            label(r"each point: \ an entering class's average LSAT and GPA", font_size=22),
            MathTex(rf"r = {d['r']:.3f}", font_size=36, color=OBS),
            label(r"how accurate is that number?", font_size=26, color=RES),
            label(r"what is its standard error?", font_size=24),
        ), 4.6, 0.38, [4.5, 0.2, 0])
        tag = historical_tag(r"Efron \& Tibshirani (1993), \ Table 3.1", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> His running example was fifteen American law schools. <bookmark mark='b'/> For each, the "
            "average score of its entering class on the law school admission test, and their average undergraduate grade. "
            "<bookmark mark='c'/> The correlation is point seven seven six. <bookmark mark='d'/> How accurate is that, from "
            "fifteen schools? <bookmark mark='e'/> What is its standard error?"
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots], lag_ratio=0.08), FadeIn(rows[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def formula(self):
        d = load("law")
        rows = [
            cmath(r"\mathrm{SE}(r)", r"\approx", rf"\frac{{1 - r^2}}{{\sqrt{{n - 3}}}} = {d['se_normal']:.3f}", font_size=34),
            cmath(r"\text{assumes}", r":", r"\text{(LSAT, GPA) bivariate normal}", font_size=32),
            cmath(r"\text{the bootstrap}", r":", rf"\mathrm{{SE}}(r) \approx {d['se_boot']:.3f}", font_size=34),
            cmath(r"\text{assumes}", r":", r"\text{IID schools; regularity and finite moments}", font_size=32),
        ]
        rows[2][2].set_color(BOOT)
        whys = [why(r"Fisher's $z$ (1915), \ by the delta method"), why(r"a model for the population"),
                why(r"2,000 resamples: \ chapter seven"), why(r"no model at all")]
        with self.voiceover(
            "<bookmark mark='a'/> There is a classical answer: the standard error of a correlation is roughly one minus r squared "
            "over the square root of n minus three, point one one five. <bookmark mark='b'/> But that formula assumes the "
            "two scores are bivariate normal, which nobody has checked and fifteen points can't confirm. "
            "<bookmark mark='c'/> Efron's bootstrap, which we'll build in chapter seven, gives point one three five, "
            "<bookmark mark='d'/> assuming independent, identically distributed schools, nonzero variances and suitable finite moments. This part is "
            "about methods like that: answers that lean on the data rather than on a model."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def name(self):
        rows = fit_rows(VGroup(
            label(r"``to pull oneself up by one's bootstraps'': \ an impossible feat, \ as of Baron Munchausen", font_size=24, color=GREY_A),
            label(r"the bootstrap seems to get something from nothing: \ a sampling distribution from one sample", font_size=24, color=BOOT),
            label(r"and ranks, \ older still: \ exact tests with no distribution at all \ (Wilcoxon 1945, \ Mann \& Whitney 1947)", font_size=24, color=RANK),
            label(r"two families of methods, \ one idea: \ use the data's own symmetries", font_size=26, color=OBS),
        ), 12.4, 0.46, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The name is a joke: to pull oneself up by one's own bootstraps, an impossible feat attributed to "
            "Baron Munchausen. <bookmark mark='b'/> The bootstrap seems to get something from nothing: a whole sampling "
            "distribution from a single sample. We'll see why it works, and when it doesn't. <bookmark mark='c'/> The part also "
            "covers an older family of methods built on ranks, which give exact tests under exchangeability or symmetry, without a normal model: "
            "Frank Wilcoxon's of 1945, Henry Mann and Donald Whitney's of 1947. <bookmark mark='d'/> Both families rest on the "
            "same idea: use the symmetries the data themselves possess."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 16", font_size=34, color=GREY_B), label(r"Without Assumptions", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"permutation tests: \ exact $p$-values from exchangeability",
            r"ranks: \ the sign test, \ Wilcoxon, \ Mann--Whitney, \ Kruskal--Wallis, \ Spearman, \ Kendall; \ their efficiency",
            r"the jackknife, \ and the bootstrap principle",
            r"bootstrap intervals: \ percentile, \ basic, \ $t$, \ BCa; \ and where the bootstrap fails",
            r"cross-validation, \ and kernel density estimates, \ a first look",
        ], color=BOOT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 8, \ 10 and 11").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.bootstrap}, \ \texttt{statkit.ranks}; \ the resampler").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part sixteen: without assumptions is the title, but weaker assumptions is the promise. <bookmark mark='b'/> We'll build permutation tests from "
            "exchangeability; the rank tests, from the sign test to Kendall's tau, and see how little they cost; the jackknife "
            "and the bootstrap principle; four kinds of bootstrap interval, tested on the Coverage Board, and a case where the "
            "bootstrap fails; and two methods we'll meet again: cross-validation and kernel density estimation."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
