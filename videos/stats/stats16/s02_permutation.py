from __future__ import annotations

import numpy as np

from videos.stats.stats16.common import *  # noqa: F403


class Permutation(VoiceoverScene):
    def construct(self):
        self.card()
        self.exchangeable()
        self.machine()
        self.exact()
        self.any_stat()
        self.correlation()
        self.limits()

    def card(self):
        card = chapter_card(1, r"Permutation tests", r"Exact $p$-values from exchangeability", lit=(1935,), part=PART)
        with self.voiceover("Chapter one. Permutation tests."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def exchangeable(self):
        rows = [
            cmath(r"H_0", r":", r"F_X = F_Y\ \text{(the same distribution, \ whatever it is)}", font_size=30),
            cmath(r"\Rightarrow", r"\ ", r"(Z_1, \ldots, Z_{m+n})\ \text{exchangeable}", font_size=32),
            cmath(r"P(\text{any labelling})", r"=", r"1 \Big/ \binom{m + n}{m}", font_size=34),
            cmath(r"p", r"=", r"\frac{\#\{\text{labellings with } |T| \ge |T_{\text{obs}}|\}}{\binom{m+n}{m}}", font_size=32),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"no shape assumed: \ not normal, \ not anything"), why(r"Part 5: \ the joint law ignores the order"),
                why(r"every split into groups equally likely"), why(r"exact for any statistic $T$, \ any distribution")]
        intro = label('Exchangeability justifies relabelling under the null', font_size=36)
        with self.voiceover(
            "Part 10's permutation machine and Part 13's randomization test return, now as a general principle. "
            "<bookmark mark='a'/> Suppose the null hypothesis is that two samples come from the same distribution, whatever it "
            "is: not normal, not anything in particular. <bookmark mark='b'/> Then the pooled observations are exchangeable, "
            "Part 5's idea: their joint distribution doesn't care about the order. <bookmark mark='c'/> So every way of "
            "splitting them into a group of m and a group of n is equally likely. <bookmark mark='d'/> The p-value is the "
            "share of splits whose statistic is at least as extreme as the observed one. It's exact, for any statistic and any "
            "distribution. In an experiment the justification is the randomization, as in Part 13; in observational data, "
            "it's exchangeability under the null."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def machine(self):
        d = load("perm")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        vals = np.r_[x, y]
        in_a = np.r_[np.ones(12, bool), np.zeros(12, bool)]
        pm = PermutationMachine(vals, in_a, colors=(S.CTRL, S.TREAT), center=[0, 1.6, 0], width=11.4, radius=0.24, font_size=14,
                                fmt="{:.0f}", row_gap=1.0)
        la = label(r"men", font_size=22, color=S.CTRL).next_to(pm.slots_a[0], LEFT, buff=0.35)
        lb = label(r"women", font_size=22, color=S.TREAT).next_to(pm.slots_b[0], LEFT, buff=0.35)
        rows = fit_rows(VGroup(
            label(r"12 men's and 12 women's incomes from the World, \ thousands: \ skewed, \ with outliers", font_size=24),
            MathTex(rf"\bar x_{{\text{{men}}}} - \bar x_{{\text{{women}}}} = {d['obs']:.1f}", font_size=32, color=OBS),
            label(r"is that more than shuffling could produce?", font_size=24),
        ), 12.4, 0.3, [0, -1.8, 0])
        tag = simulated_tag(r"the World: \ 24 adults", corner=DR)
        g = np.random.Generator(np.random.PCG64(16))
        with self.voiceover(
            "<bookmark mark='a'/> Here are twelve men's and twelve women's incomes from the World, in thousands: skewed, as "
            "incomes are, with a few large values. A t-test's normal theory is shaky with samples this small and this skewed. "
            "<bookmark mark='b'/> The women's mean is twenty thousand higher. <bookmark mark='c'/> Shuffle the labels: each "
            "shuffle is a split the null hypothesis says was just as likely. Again, and again."
        ) as vo:
            self.play(FadeIn(pm), FadeIn(la), FadeIn(lb), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            for _ in range(4):
                self.play(pm.shuffle(g.permutation(24), run_time=0.7))
            self.play(pm.reset(run_time=0.6))
        self.clear_scene()

    def exact(self):
        d = load("perm")
        edges = np.asarray(d["edges"])
        hist = np.asarray(d["hist"], float)
        A = axes([-70, 70], [0, 145000], x_length=8.4, y_length=3.8, xlabel=r"difference in means under a relabelling, \ thousands",
                 ylabel=r"labellings", xticks=[-60, -30, 0, 30, 60], yticks=[0, 50000, 100000], center=[-1.2, 0.4, 0],
                 yfmt=lambda v: f"{int(v):,}")
        ax = A.ax
        w = edges[1] - edges[0]
        bars = VGroup()
        for e, h in zip(edges[:-1], hist):
            c = OBS if abs(e + w / 2) >= abs(d["obs"]) else NULLC
            bars.add(*hist_bars(ax, [e, e + w], [h], color=c, opacity=0.85))
        mk = DashedLine(ax.c2p(d["obs"], 0), ax.c2p(d["obs"], 140000), color=OBS, stroke_width=3)
        rows = fit_rows(VGroup(
            MathTex(rf"\binom{{24}}{{12}} = {d['n_alloc']:,}\ \text{{splits}}", font_size=26),
            MathTex(rf"\text{{exact}}\ p = {d['p']:.3f}", font_size=30, color=OBS),
            MathTex(rf"\text{{Welch}}\ p = {d['welch_p']:.3f}", font_size=26, color=S.ALT),
            label(rf"World population mean difference: \ {d['truth']:.2f} thousand", font_size=22, color=S.TRUTH),
        ), 3.8, 0.34, [5.0, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> There are two million seven hundred thousand ways to split twenty-four incomes into two groups "
            "of twelve, few enough for a computer to try every one. Here is the exact distribution of the difference in means "
            "under the null. <bookmark mark='b'/> A difference as large as twenty thousand, either way, happens in twenty-three "
            "percent of the splits: p equals point two three. <bookmark mark='c'/> Welch's test, Part 10's, gives point two four: "
            "the normal approximation is decent even here. <bookmark mark='d'/> The World generates income without a direct sex effect, but its finite population has a small realized difference. "
            "The permutation null requires exchangeable groups, not merely equal means."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.02), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(mk), FadeIn(rows[1]))
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def any_stat(self):
        rows = [
            cmath(r"T", r"=", r"\bar x - \bar y,\ \ \text{median}(x) - \text{median}(y),\ \ \text{a trimmed mean}, \ldots", font_size=30),
            cmath(r"\text{choose } T", r":", r"\text{before seeing the data}", font_size=32),
            cmath(r"\text{too many splits}", r":", r"\text{sample } 10{,}000;\ \ p = \frac{1 + \#\{|T^*| \ge |T|\}}{1 + 10{,}000}", font_size=30),
            cmath(r"\text{the test is exact}", r";", r"\text{the choice of } T \text{ decides its power}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"any statistic that measures the difference"), why(r"or the $p$-value is no longer exact"),
                why(r"the $+1$s keep it valid (Part 10)"), why(r"a robust $T$ for heavy tails")]
        with self.voiceover(
            "<bookmark mark='a'/> The statistic can be anything that measures a difference: the difference in means, in "
            "medians, in trimmed means. <bookmark mark='b'/> It must be chosen before looking, or the exactness is lost. "
            "<bookmark mark='c'/> When there are too many splits to count, sample ten thousand at random; adding one to the "
            "count and to the total keeps the test valid, as in Part 10. <bookmark mark='d'/> Every choice gives an exact test. "
            "What the choice changes is the power: a statistic that resists outliers detects shifts in heavy-tailed data far "
            "better, which is where ranks come in."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def correlation(self):
        d = load("association")
        r, c, p = d["r"], np.asarray(d["null"]), d["p"]
        A = axes([-1, 1], [0, 1700], x_length=8.4, y_length=3.6, xlabel=r"correlation after shuffling the GPAs", ylabel=r"shuffles",
                 xticks=[-1, -0.5, 0, 0.5, 1], yticks=[0, 500, 1000, 1500], center=[-1.2, 0.5, 0])
        ax = A.ax
        e = np.linspace(-1, 1, 51)
        bars = hist_bars(ax, e, np.histogram(c, e)[0], color=NULLC, opacity=0.8)
        mk = DashedLine(ax.c2p(r, 0), ax.c2p(r, 1600), color=OBS, stroke_width=3)
        rows = fit_rows(VGroup(
            label(r"$H_0$: \ LSAT and GPA independent", font_size=24),
            label(r"shuffle one column against the other", font_size=24),
            MathTex(rf"20{{,}}000\ \text{{shuffles:}}\ p = {p:.4f}", font_size=30, color=OBS),
            label(r"evidence against independence", font_size=24, color=OBS),
        ), 3.8, 0.36, [5.0, 0.5, 0])
        with self.voiceover(
            "Permutations test association too. <bookmark mark='a'/> If LSAT and GPA were independent across law schools, "
            "<bookmark mark='b'/> pairing each school's LSAT with a random school's GPA would be as likely as the real pairing. "
            "Shuffle the GPA column twenty thousand times and recompute the correlation each time. <bookmark mark='c'/> A "
            "correlation as large as point seven seven six turns up in fewer than two shuffles in a thousand. "
            "<bookmark mark='d'/> This is evidence against independence under IID sampling, without a normality assumption. The Monte Carlo p-value includes the observed pairing."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.02), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(mk), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def limits(self):
        rows = fit_rows(VGroup(
            label(r"the null must make the data exchangeable", font_size=26),
            label(r"``same mean, \ different spreads'' does not: \ the test then answers a different question", font_size=24, color=RES),
            label(r"time and cluster dependence may require restricted permutations: \ Part 17", font_size=24, color=RES),
            label(r"invert permutation tests for intervals; \ bootstrap also estimates SEs", font_size=24, color=BOOT),
        ), 12.4, 0.5, [0, 0, 0])
        intro = label('Exact calibration depends on the null symmetry', font_size=36)
        with self.voiceover(
            "The limits. <bookmark mark='a'/> The null hypothesis must make the observations exchangeable. "
            "<bookmark mark='b'/> \"Same mean, but perhaps different spreads\" doesn't: shuffling then tests whether the "
            "distributions are identical, a different question. <bookmark mark='c'/> Data that depend on each other, in time or in "
            "clusters, generally need permutations that respect their dependence: Part 17. Some dependent laws are exchangeable. <bookmark mark='d'/> Permutation tests can also be inverted for confidence sets. "
            "For standard errors and another approach to intervals, we turn to the bootstrap."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
