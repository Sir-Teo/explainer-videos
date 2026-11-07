from __future__ import annotations

import numpy as np

from videos.stats.stats48.common import *  # noqa: F403


class Learning(VoiceoverScene):
    def construct(self):
        self.card()
        self.erm()
        self.chart()
        self.bounds()

    def card(self):
        card = chapter_card(10, r"Uniform laws at work: \ learning", r"Why minimizing training error works", lit=(1971,), part=PART)
        with self.voiceover("Chapter ten. Uniform laws at work, in learning: why minimizing training error works."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def erm(self):
        rows = [
            cmath(r"R(h) = P(h(X) \ne Y), \ \ R_n(h)", r"=", r"\tfrac1n \textstyle\sum_i \mathbf 1\{h(X_i) \ne Y_i\}", font_size=32),
            cmath(r"\hat h", r"=", r"\operatorname*{argmin}_{h \in \mathcal H} R_n(h): \ \text{empirical risk minimization}", font_size=34),
            cmath(r"R(\hat h) - \inf_{\mathcal H} R", r"\le", r"2 \sup_{h \in \mathcal H} |R_n(h) - R(h)|", font_size=34),
            cmath(r"\mathcal H \text{ of VC dimension } V", r":", r"E\,[R(\hat h)] - \inf R \lesssim \sqrt{V \log n / n}", font_size=32),
        ]
        rows[2][-1].set_color(CLASSC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"true and training error"), why(r"Part 19's recipe"), why(r"add and subtract: \ one line"), why(r"chapters 1--2 \ (Vapnik 1998)")]
        with self.voiceover(
            "<bookmark mark='a'/> The theory was invented, in part, for learning. A classifier h has a true error rate R of "
            "h and a training error rate R n of h. <bookmark mark='b'/> Empirical risk minimization picks the classifier in "
            "the class with the smallest training error, Part nineteen's recipe. <bookmark mark='c'/> Adding and "
            "subtracting, the chosen classifier's excess true error is at most twice the largest gap between training and "
            "true error over the class: a uniform law of large numbers, exactly chapter one's quantity. <bookmark "
            "mark='d'/> So for a class of VC dimension V, the excess risk is of order the root of V log n over n, whatever "
            "the distribution of the data. This is Vapnik and Chervonenkis's original motivation."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("erm")
        ln = np.log10(np.asarray(d["ns"], float))
        A = axes([1.2, 3.4], [-3.4, 0.6], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"$\log_{10}$",
                 xticks=[np.log10(20), 2, np.log10(500), 3], xfmt=lambda v: f"{10 ** v:,.0f}", yticks=[-3, -2, -1, 0], center=[-2.5, 0.2, 0])
        ax = A.ax

        def line(v, c):
            y = np.log10(np.asarray(v, float))
            return VGroup(polyline(ax, ln, y, c, 4), *[Dot(ax.c2p(a, b), radius=0.07, color=c) for a, b in zip(ln, y)])

        cb, cs, ce = line(d["bound"], BOUNDC), line(d["two_sup"], EMPC), line(d["exc"], GOODC)
        side = fit_rows(VGroup(
            label(r"thresholds $\mathbf 1\{x > t\}$; \ $X \sim U(0,1)$, \ $t_0 = 0.3$, \ 20\% label noise", font_size=22),
            label(r"purple: \ the VC bound \ $4\sqrt{2\log(2(n+1))/n}$", font_size=22, color=BOUNDC),
            label(r"blue: \ $2\,E\sup_h |R_n - R|$, \ simulated", font_size=22, color=EMPC),
            label(r"green: \ ERM's actual excess risk", font_size=22, color=GOODC),
            label(r"slopes $-1/2$ \ and \ $-1$: \ the bound is loose here", font_size=22, color=CLASSC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A toy problem. Threshold classifiers on the unit interval, a true threshold at point "
            f"three, and twenty percent of the labels flipped at random, so the best possible error is point two. <bookmark "
            f"mark='b'/> In purple, the distribution-free VC bound. <bookmark mark='c'/> In blue, twice the expected uniform "
            f"deviation, simulated: below the bound, with the same slope of minus a half. <bookmark mark='d'/> In green, "
            f"the excess risk that empirical risk minimization actually incurs: at a thousand observations, "
            f"{d['exc'][5]:.4f}. <bookmark mark='e'/> It falls like one over n, not one over root n, because near the best "
            f"threshold the excess risk is linear in the distance, and the variance there is small: chapter six's "
            f"small-variance classes, and chapter nine's localization, explain the faster rate."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated: \ 600--2,000 samples per $n$")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cs), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ce), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def bounds(self):
        rows = fit_rows(VGroup(
            label(r"from this part to machine learning:", font_size=28, color=GREY_A),
            label(r"Rademacher complexity bounds: \ data-dependent, \ often much tighter than VC", font_size=26, color=CLASSC),
            label(r"margin bounds for SVMs and boosting: \ the scale-sensitive dimension, \ not the parameter count", font_size=26, color=EMPC),
            label(r"localized complexities: \ fast rates $1/n$ \ (Bartlett, \ Bousquet \& Mendelson 2005)", font_size=26, color=GOODC),
            label(r"but deep nets interpolate noise: \ uniform bounds are vacuous there, \ an open problem", font_size=26, color=BADC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> From here the road leads into machine learning theory. <bookmark mark='b'/> Rademacher complexities, computed on the data at hand, give bounds that are often much tighter than the VC bound. <bookmark mark='c'/> Margin bounds explain support vector machines and boosting through a scale-sensitive dimension, not the number of parameters. <bookmark mark='d'/> Localized complexities, due to Peter Bartlett, Olivier Bousquet and Shahar Mendelson, can give fast rates under additional margin or low-variance conditions, such as the constant-noise threshold model shown here. <bookmark mark='e'/> But modern deep networks can fit pure noise perfectly, so unrestricted worst-case VC bounds can be vacuous at the available sample size. Norm constraints, margins, data-dependent complexity and algorithmic stability can still yield useful guarantees. Understanding the full range of deep-network generalization remains an active research problem, and the companion series AI, Built takes up the practice."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
