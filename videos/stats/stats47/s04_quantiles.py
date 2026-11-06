from __future__ import annotations

import numpy as np

from videos.stats.stats47.common import *  # noqa: F403


class Quantiles(VoiceoverScene):
    def construct(self):
        self.card()
        self.limit()
        self.bahadur()
        self.table()
        self.orderci()
        self.uses()

    def card(self):
        card = chapter_card(3, r"Quantiles and the Bahadur representation", r"A sample quantile is an average in disguise", lit=(1966,), part=PART)
        with self.voiceover("Chapter three. Quantiles and the Bahadur representation: a sample quantile is an average in disguise."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def limit(self):
        rows = [
            cmath(r"\hat\xi_p = F_n^{-1}(p)", r",", r"\ \xi_p = F^{-1}(p), \ f(\xi_p) > 0", font_size=34),
            cmath(r"P(\hat\xi_p \le \xi_p + t/\sqrt n)", r"=", r"P\big(\textstyle\sum \mathbf 1\{X_i \le \xi_p + t/\sqrt n\} \ge np\big)", font_size=30),
            cmath(r"\phantom{P}", r"\to", r"\Phi\big(t f(\xi_p) / \sqrt{p(1-p)}\big)", font_size=34),
            cmath(r"\sqrt n(\hat\xi_p - \xi_p)", r"\Rightarrow", r"N\big(0, \ p(1 - p)/f(\xi_p)^2\big)", font_size=34),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"a sample quantile"), why(r"a binomial count"), why(r"the de Moivre--Laplace CLT"), why(r"the median: \ $\pi\sigma^2/2$ at the normal")]
        with self.voiceover(
            "<bookmark mark='a'/> The p-th sample quantile estimates the p-th population quantile, at a point where the "
            "density is positive. <bookmark mark='b'/> The event that it lies below the truth plus t over root n is the "
            "event that enough observations fall below that point: a binomial count. <bookmark mark='c'/> The binomial's "
            "normal limit, with the density converting the shift in the argument into a shift in probability, <bookmark "
            "mark='d'/> gives asymptotic normality with variance p times one minus p over the density squared. For the "
            "median of normal data that is pi over two times sigma squared: an efficiency of sixty-four percent against "
            "the mean, as Part thirty found."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bahadur(self):
        rows = [
            cmath(r"\hat\xi_p", r"=", r"\xi_p + \frac{p - F_n(\xi_p)}{f(\xi_p)} + R_n", font_size=36),
            cmath(r"\frac{p - F_n(\xi_p)}{f(\xi_p)}", r"=", r"\frac1n \textstyle\sum_i \frac{p - \mathbf 1\{X_i \le \xi_p\}}{f(\xi_p)}: \ \text{an average}", font_size=30),
            cmath(r"R_n", r"=", r"O\big(n^{-3/4}(\log n)^{1/2}(\log\log n)^{1/4}\big) \ \text{a.s.}", font_size=32),
            cmath(r"\sqrt n\, R_n", r"=", r"O_P(n^{-1/4}): \ \text{small, \ but slowly}", font_size=34),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(S.ACCENT)
        whys = [why(r"Bahadur (1966)"), why(r"influence terms"), why(r"Kiefer (1967): \ the exact rate"), why(r"compare $n^{-1/2}$ for smooth M-estimators")]
        with self.voiceover(
            "<bookmark mark='a'/> Raghu Raj Bahadur showed in 1966 that the sample quantile is, to first order, an average. "
            "It equals the true quantile, plus p minus the empirical distribution function at the true quantile, over the "
            "density, plus a remainder. <bookmark mark='b'/> The middle term is an average of independent bounded terms, one "
            "per observation: their influence. <bookmark mark='c'/> The remainder is of order n to the minus three quarters, "
            "up to logarithms, as Jack Kiefer later pinned down exactly. <bookmark mark='d'/> So after multiplying by root n "
            "it vanishes, but only like n to the minus one quarter, much more slowly than for smooth M-estimators, because "
            "the indicator function is not differentiable."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("quantile")
        rows = [[r"$n$", r"SD of $\sqrt n(\hat\xi - \xi)$", r"theory $\sqrt{\pi/2}$", r"RMS of $\sqrt n R_n$", r"$\times\, n^{1/4}$"]]
        for r in d["rows"]:
            rows.append([f"{r['n']:,}", f"{r['sd']:.3f}", f"{r['theory']:.3f}", f"{r['rms']:.3f}", f"{r['rms'] * r['n'] ** 0.25:.2f}"])
        tab = table_rows(rows, font_size=28, col_buff=0.8, row_buff=0.3, colors=[GREY_A] + [None] * len(d["rows"])).move_to([0, 0.7, 0])
        note_ = fit_rows(VGroup(
            label(r"the median of $N(0, 1)$ samples; \ 2,000 samples per row \ (800 at $n = 5{,}000$)", font_size=24, color=GREY_A),
            label(r"the remainder shrinks like $n^{-1/4}$: \ the last column is roughly constant", font_size=26, color=S.ACCENT),
        ), 12.4, 0.25, [0, -2.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Simulated, for the median of normal samples. <bookmark mark='b'/> The standard deviation of "
            "root n times the error matches the theory, root of pi over two, at every sample size. <bookmark mark='c'/> The "
            "root-mean-square of the scaled remainder falls from point five seven to point one eight as n grows a hundredfold, "
            "<bookmark mark='d'/> and multiplied by n to the one quarter it stays roughly constant: the slow rate, confirmed."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(note_[0]), FadeIn(exact_tag(r"simulated")))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(VGroup(*[r[3] for r in tab[1:]]), color=S.ACCENT))
            vo.wait_until("d")
            self.play(FadeIn(note_[1]))
        self.clear_scene()

    def uses(self):
        rows = fit_rows(VGroup(
            label(r"what the representation buys:", font_size=28, color=GREY_A),
            label(r"joint limits of several quantiles: \ the interquartile range, \ L-estimators, \ trimmed means", font_size=26),
            label(r"Part 23's quantile-regression SEs, \ Part 40's median survival: \ the same linearization", font_size=26, color=GOODC),
            label(r"the influence function of a quantile: \ $(p - \mathbf 1\{x \le \xi_p\})/f(\xi_p)$, \ bounded: \ robust", font_size=26, color=S.ACCENT),
            label(r"but it needs $f(\xi_p)$: \ hard to estimate; \ hence bootstrap and order-statistic intervals", font_size=26, color=HODC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What does the representation buy? <bookmark mark='b'/> Joint limits of several quantiles at "
            "once, and of statistics built from them: the interquartile range, L-estimators, trimmed means. <bookmark "
            "mark='c'/> The same linearization drives quantile regression and median survival times from earlier parts. "
            "<bookmark mark='d'/> It identifies the quantile's influence function, which is bounded: a quantile is robust. "
            "<bookmark mark='e'/> But the variance involves the density at the quantile, which is hard to estimate, which is "
            "why intervals for quantiles usually come from order statistics or the bootstrap instead."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def orderci(self):
        rows = [
            cmath(r"P\big(X_{(j)} \le \xi_p < X_{(k)}\big)", r"=", r"P(j \le B < k), \ \ B \sim \mathrm{Bin}(n, p)", font_size=32),
            cmath(r"\text{exact for every continuous } F", r":", r"\text{a distribution-free interval for } \xi_p", font_size=32),
            cmath(r"j, k", r"\approx", r"np \mp z\sqrt{np(1 - p)}: \ \text{the order statistics around the target}", font_size=30),
            cmath(r"\text{the median}, \ n = 20", r":", r"[X_{(6)}, \ X_{(15)}] \ \text{covers with probability } 0.959", font_size=32),
        ]
        rows[1][-1].set_color(GOODC)
        whys = [why(r"count the points below $\xi_p$"), why(r"no density needed"), why(r"the normal approximation"), why(r"binomial sums")]
        with self.voiceover(
            "<bookmark mark='a'/> Quantiles also have an exact interval that needs no density at all. The chance that the "
            "true quantile lies between two order statistics is a binomial probability: it depends only on how many "
            "observations fall below the quantile. <bookmark mark='b'/> So the interval is exact for every continuous "
            "distribution. <bookmark mark='c'/> Its indices are roughly n p plus or minus z times the binomial standard "
            "deviation. <bookmark mark='d'/> For the median of twenty observations, the sixth and fifteenth order "
            "statistics cover with probability point nine five nine, whatever the distribution."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
