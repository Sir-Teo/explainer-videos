from __future__ import annotations

import numpy as np

from videos.stats.stats47.common import *  # noqa: F403


class Ranks(VoiceoverScene):
    def construct(self):
        self.card()
        self.signed()
        self.power()
        self.are()
        self.hodges_lehmann()
        self.scores()

    def card(self):
        card = chapter_card(6, r"Rank statistics", r"How much is lost by keeping only the order?", lit=(1945,), part=PART)
        with self.voiceover("Chapter six. Rank statistics: how much is lost by keeping only the order?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def signed(self):
        rows = [
            cmath(r"W", r"=", r"\textstyle\sum_i R_i^+ \mathbf 1\{X_i > 0\}, \ \ R_i^+ = \text{rank of } |X_i|", font_size=32),
            cmath(r"\text{under } H_0 \ (\text{symmetric about } 0)", r":", r"\text{the signs are fair coins, \ independent of the ranks}", font_size=28),
            cmath(r"\hat W", r"=", r"EW+\textstyle\sum_i[\mathbf1\{X_i>0\}-\tfrac12+(n-1)(F(X_i)-\tfrac12)]:\ \text{Hájek's projection}", font_size=30),
            cmath(r"\frac{W - n(n+1)/4}{\sqrt{n(n+1)(2n+1)/24}}", r"\Rightarrow", r"N(0,1)\text{ under }H_0;\ \text{shifted normal under regular local alternatives}", font_size=30),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Wilcoxon (1945)"), why(r"distribution-free"), why(r"$F$: \ continuous null CDF, symmetric about zero"), why(r"Part 16's normal approximation")]
        with self.voiceover(
            "<bookmark mark='a'/> Frank Wilcoxon's signed-rank statistic adds up the ranks of the absolute values of "
            "the positive observations. <bookmark mark='b'/> Under the null of a distribution symmetric about zero, "
            "the signs are fair coins independent of the ranks, so its null distribution is the same for every such "
            "distribution. <bookmark mark='c'/> For a continuous symmetric distribution F, the exact centered "
            "projection is the sum of indicator X positive minus one half, plus n minus one times F of X minus one "
            "half. This follows from the Walsh identity: W counts positive pair sums including diagonal pairs. Each "
            "projected term depends on one observation. <bookmark mark='d'/> So the standardized statistic is "
            "asymptotically standard normal under the symmetric null. Under regular local shifts it has a shifted "
            "normal limit, which determines power."
        ) as vo:
            heading=label('The signed-rank projection follows from positive Walsh sums',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def power(self):
        d = load("ranks")
        rows = [[r"errors", r"test"] + [rf"$h = {h:g}$" for h in d["hs"]]]
        for name in ("normal", "Laplace", "t3"):
            law = d["laws"][name]
            lab = {"normal": "normal", "Laplace": "Laplace", "t3": r"$t_3$"}[name]
            rows.append([lab, r"$t$"] + [f"{v:.3f}" for v in law["t"]])
            rows.append(["", r"Wilcoxon"] + [f"{v:.3f}" for v in law["wilcoxon"]])
        tab = table_rows(rows, font_size=26, col_buff=0.7, row_buff=0.22, colors=[GREY_A, MLEC, GOODC, MLEC, GOODC, MLEC, GOODC]).move_to([0, 0.7, 0])
        note_ = label(rf"one-sided 5\%, \ $n = {d['n']}$, \ shift $h/\sqrt n$, \ unit variance; \ 8,000 samples per cell", font_size=24, color=GREY_A).move_to([0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Power against local shifts h over root n, with thirty observations of unit "
            "variance. <bookmark mark='b'/> For normal errors, the t test is slightly better: at h equal to two, "
            "sixty-two percent against sixty-one. <bookmark mark='c'/> For Laplace errors, Wilcoxon wins clearly: "
            "seventy-three percent against sixty-three. <bookmark mark='d'/> For the heavy-tailed t with three "
            "degrees of freedom, eighty-three against seventy-one. Using the signs and the ranks of magnitudes costs "
            "little at the normal and gains in these other symmetric models."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(note_), FadeIn(exact_tag(r"simulated: 8,000 samples per cell")))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
            vo.wait_until("d")
            self.play(FadeIn(tab[5]), FadeIn(tab[6]))
        self.clear_scene()

    def are(self):
        d = load("ranks")["are"]
        rows = [
            cmath(r"\mathrm{ARE}(W, t)", r"=", r"12\, \sigma^2 \Big(\textstyle\int f^2\Big)^2", font_size=36),
            cmath(r"\text{normal}", r":", rf"3/\pi = {d['normal']:.3f}", font_size=34),
            cmath(r"\text{Laplace}, \ t_3", r":", rf"{d['Laplace']:.2f}, \ \ {d['t3']:.2f}", font_size=34),
            cmath(r"\inf_f", r"=", rf"108/125 = {d['min']:.3f}: \ \text{{never much worse, \ sometimes much better}}", font_size=30),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Pitman efficiency, \ chapter 10"), why(r"a 4.5\% loss"), why(r"gains"), why(r"Hodges \& Lehmann (1956)")]
        with self.voiceover(
            "<bookmark mark='a'/> The asymptotic relative efficiency of Wilcoxon's test to the t test, in Pitman's "
            "sense of chapter ten, is twelve sigma squared times the square of the integral of the density squared. "
            "<bookmark mark='b'/> At the normal, three over pi: ninety-five and a half percent. <bookmark mark='c'/> "
            "At the Laplace, one and a half; at the t with three degrees of freedom, nearly two. <bookmark mark='d'/>"
            " And Joseph Hodges and Erich Lehmann proved in 1956 that it is never below one hundred and eight over "
            "one hundred and twenty-five, eighty-six percent, for the regular symmetric finite-variance location "
            "densities covered by that theorem. The Wilcoxon test is never much worse than the t test, and can be "
            "infinitely better."
        ) as vo:
            heading=label('Local rank efficiency depends on the location density',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def scores(self):
        rows = fit_rows(VGroup(
            label(r"general linear rank statistics: \ $\sum_i a(R_i) c_i$, \ with scores $a(i) = \varphi(i/(n+1))$", font_size=26),
            label(r"locally most powerful for density $f$: \ $\varphi(u) = -f'(F^{-1}(u)) / f(F^{-1}(u))$", font_size=26, color=GOODC),
            label(r"normal scores \ (van der Waerden): \ ARE $\ge1$ against $t$: \ regular continuous finite-variance location models \ (Chernoff \& Savage 1958)", font_size=26, color=S.ACCENT),
            label(r"Hájek \& Šidák, \ \emph{Theory of Rank Tests} (1967): \ efficient tests from ranks alone", font_size=24, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Wilcoxon's is one of a family: sums of scores of the ranks. <bookmark mark='b'/> "
            "For a suitably differentiable location density with finite positive Fisher information there is an "
            "optimal score function, built from the derivative of log f at the quantiles, that makes the rank test "
            "locally most powerful, and asymptotically as efficient as the best test that knows f. <bookmark "
            "mark='c'/> And Herman Chernoff and Richard Savage proved in 1958 that the normal-scores test has "
            "relative efficiency at least one against the t test, under the theorem's continuous finite-variance "
            "location-model regularity conditions. <bookmark mark='d'/> Hájek and Zbyněk Šidák's Theory of Rank Tests"
            " of 1967 is the classic account."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def hodges_lehmann(self):
        rows = [
            cmath(r"\hat\theta_{HL}", r"=", r"\mathrm{median}\{(X_i + X_j)/2 : i \le j\}", font_size=34),
            cmath(r"\text{inverts Wilcoxon}", r":", r"\text{the } \theta \text{ at which } W(X - \theta) \text{ is centred}", font_size=32),
            cmath(r"\text{efficiency vs the mean}", r"=", r"\mathrm{ARE}(W, t): \ 0.955 \text{ at the normal}, \ \ge0.864\text{ under the stated regular symmetric conditions}", font_size=30),
            cmath(r"\text{breakdown point}", r"=", r"1 - 1/\sqrt 2 \approx 29\%", font_size=34),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"the median of Walsh averages"), why(r"a test becomes an estimator"), why(r"the same numbers"), why(r"Part 30")]
        with self.voiceover(
            "<bookmark mark='a'/> Every rank test has an estimator hidden inside it. Hodges and Lehmann's estimator "
            "is the median of all pairwise averages of the observations. <bookmark mark='b'/> It is the value of "
            "theta at which the Wilcoxon statistic of the shifted data crosses its null centre. The statistic is a "
            "step function, so the center may be an interval or require a convention; the Walsh median is the usual "
            "estimate. <bookmark mark='c'/> Its efficiency relative to the mean is the same as the test's relative to"
            " the t test: ninety-five and a half percent at the normal, at least eighty-six percent under the stated "
            "regular symmetric finite-variance conditions. <bookmark mark='d'/> And it tolerates twenty-nine percent "
            "of arbitrary contamination before breaking down, as Part thirty found."
        ) as vo:
            heading=label('Walsh medians invert signed-rank location comparisons',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
