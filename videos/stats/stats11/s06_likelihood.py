from __future__ import annotations

import numpy as np

from videos.stats.stats11.common import *  # noqa: F403


class Likelihood(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_of_thirty()
        self.curve()
        self.invariance()
        self.large_n()
        self.rule_of_three()

    def card(self):
        card = chapter_card(5, r"Likelihood intervals", r"Where the log-likelihood drops by 1.92", part=PART)
        with self.voiceover("Chapter five. Likelihood intervals."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def two_of_thirty(self):
        d = load("likelihood")
        order = ["wald", "wilson", "agresti_coull", "clopper_pearson", "jeffreys", "lr"]
        A = axes([-0.02, 0.26], [0, 7], x_length=8.4, y_length=4.6, xlabel=r"$p$: \ 95\% intervals from 2 successes in 30",
                 xticks=[0, 0.0667, 0.1, 0.2], xfmt=lambda v: f"{v:g}", center=[-1.4, -0.2, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 7), color=GREY_B, stroke_width=1.5)
        ph = DashedLine(ax.c2p(2 / 30, 0), ax.c2p(2 / 30, 7), color=DATA, stroke_width=2)
        bars = VGroup()
        for i, k in enumerate(order):
            lo, hi = d["ints"][k]
            y = 6.2 - i
            bars.add(VGroup(Line(ax.c2p(lo, y), ax.c2p(hi, y), color=METHOD_COL[k], stroke_width=6),
                            label(METHOD_TEX[k], font_size=22, color=METHOD_COL[k]).next_to(ax.c2p(-0.02, y), LEFT, buff=0.15),
                            MathTex(rf"[{lo:.3f}, {hi:.3f}]", font_size=22, color=METHOD_COL[k]).next_to(ax.c2p(hi, y), RIGHT, buff=0.15)))
        foot = label(r"Wald reaches down to 0, \ as if a rate of zero were plausible after seeing two successes", font_size=24,
                     color=METHOD_COL["wald"]).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here's a concrete case: two successes in thirty trials. <bookmark mark='a'/> The six intervals, each a "
            "line. <bookmark mark='b'/> The Wald interval runs from zero to point one five six. Its lower end is clipped "
            "at zero, because the formula goes negative. But zero is not a plausible rate after seeing two successes. "
            "The others start between point zero zero eight and point zero one eight, and they reach higher, to about "
            "point two, because with a skewed likelihood the uncertainty is mostly upward."
        ) as vo:
            self.play(FadeIn(A), Create(zero), Create(ph))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in bars], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(Indicate(bars[0], color=METHOD_COL["wald"]), FadeIn(foot))
        self.clear_scene()

    def curve(self):
        d = load("likelihood")
        ps = np.asarray(d["ps"])
        lo, hi = d["ints"]["lr"]
        A = axes([0, 0.3], [-6, 0.3], x_length=7.4, y_length=4.4, xlabel=r"$p$", ylabel=r"$\ell(p) - \ell(\hat p)$, \ 2 of 30",
                 xticks=[0, 0.0667, 0.1, 0.2, 0.3], xfmt=lambda v: f"{v:g}", yticks=[-6, -4, -1.92, 0], center=[-2.0, -0.3, 0])
        ax = A.ax
        cv = clip_curve(ax, ps, d["ll"], METHOD_COL["lr"], 3.5, ymin=-6)
        cut = DashedLine(ax.c2p(0, -1.92), ax.c2p(0.3, -1.92), color=OBS, stroke_width=2)
        seg = Line(ax.c2p(lo, -1.92), ax.c2p(hi, -1.92), color=OBS, stroke_width=8)
        par = DashedVMobject(clip_curve(ax, ps, -0.5 * (ps - 2 / 30) ** 2 / ((2 / 30) * (28 / 30) / 30), METHOD_COL["wald"], 2.5, ymin=-6),
                             num_dashes=40)
        rows = fit_rows(VGroup(
            label(r"the likelihood interval: \ $\{p : 2(\ell(\hat p) - \ell(p)) \le 3.84\}$", font_size=24),
            MathTex(rf"[{lo:.3f},\ {hi:.3f}]", font_size=30, color=OBS),
            label(r"the dashed parabola is Wald's: \ symmetric, \ so it must spill below 0", font_size=24, color=METHOD_COL["wald"]),
            label(r"the curve is skewed: \ the interval follows it", font_size=24, color=GREY_A),
        ), 5.2, 0.34, [4.3, -0.3, 0])
        with self.voiceover(
            "Why the difference? Look at the likelihood. <bookmark mark='a'/> For two of thirty, the log-likelihood rises "
            "steeply from zero, peaks at one fifteenth, and falls slowly to the right: it's skewed. "
            "<bookmark mark='b'/> The likelihood interval takes every p where the curve is within one point nine two of "
            "its peak, half of three point eight four, by inverting the likelihood ratio test with Wilks' theorem: "
            "point zero one one to point one nine two. <bookmark mark='c'/> The Wald interval is what you'd get from the "
            "parabola that matches the curve's curvature at the peak, the dashed line. A parabola is symmetric, so it "
            "spills below zero on the left and stops short on the right. The likelihood interval follows the actual shape."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cv))
            vo.wait_until("b")
            self.play(Create(cut), Create(seg), FadeIn(rows[:2]))
            vo.wait_until("c")
            self.play(Create(par), FadeIn(rows[2:]))
        self.clear_scene()

    def invariance(self):
        d = load("likelihood")
        lo, hi = d["ints"]["lr"]
        lg = lambda p: np.log(p / (1 - p))  # noqa: E731
        rows = [
            cmath(r"\eta", r"=", r"\log\frac{p}{1 - p}", r"\quad\text{the log-odds}", font_size=34),
            cmath(r"\text{likelihood interval for } \eta", r"=", rf"[{lg(lo):.2f},\ {lg(hi):.2f}] = \log\text{{-odds of }} [{lo:.3f},\ {hi:.3f}]",
                  font_size=30),
            cmath(r"\text{Wald on the log-odds scale}", r"\ne", r"\text{Wald on the } p \text{ scale}", font_size=30),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"the scale of logistic regression (Part 14)"), why(r"invariant under a one-to-one coordinate change"),
                why(r"Wald intervals depend on the coordinates; \ likelihood intervals do not")]
        intro = label('One-to-one coordinate changes preserve likelihood sets', font_size=36)
        with self.voiceover(
            "Likelihood intervals have the invariance of Part 9's maximum likelihood estimates. <bookmark mark='a'/> Change "
            "coordinates to the log-odds, the scale logistic regression uses. <bookmark mark='b'/> The likelihood "
            "interval for the log-odds is exactly the log-odds of the interval for p: the cut at one point nine two "
            "doesn't care how the parameter is labelled. <bookmark mark='c'/> The Wald interval does care. A Wald "
            "interval on the log-odds scale, transformed back, is a different interval from Wald on the p scale, and "
            "often a better interior approximation. It is undefined at zero or all successes without an additional convention. That's why software reports intervals for odds ratios on the log scale, a point Part "
            "14 returns to on the Coverage Board."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.2, buff=0.9, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def rule_of_three(self):
        d = load("likelihood")["three"]
        rows = [
            cmath(r"P_p(X = 0)", r"=", r"(1 - p)^n", font_size=34),
            cmath(r"(1 - p)^n", r"=", r"0.05\ \Rightarrow\ p_{\mathrm{upper}} = 1 - 0.05^{1/n}", font_size=32),
            cmath(r"1 - 0.05^{1/n}", r"\approx", r"\frac{-\log 0.05}{n} = \frac{3.00}{n}", font_size=34),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"no events in $n$ trials"), why(r"an exact one-sided 95\% upper bound"), why(r"$-\log 0.05 = 2.996$")]
        tab = VGroup(*[MathTex(rf"n = {n}:\ \ {v['exact']:.4f}\ \text{{vs}}\ 3/n = {v['rule']:.4f}", font_size=26) for n, v in d.items()])
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -2.2, 0])
        foot = label(r"Hanley \& Lippman-Hand (1983): \ ``If nothing goes wrong, \ is everything all right?''", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.15)
        intro = label('Zero events still leave uncertainty about the rate', font_size=36)
        with self.voiceover(
            "And the edge case where the Wald interval is most absurd: zero events. A new drug is given to a hundred "
            "patients and nobody has a serious side effect. The Wald interval is zero to zero. <bookmark mark='a'/> But "
            "the chance of zero events in n trials is one minus p to the n. <bookmark mark='b'/> For an exact one-sided ninety-five percent upper bound, set that to five percent "
            "and solve: the largest rate still consistent with seeing nothing. <bookmark mark='c'/> Since minus log point "
            "zero five is almost exactly three, the upper limit is about three over n. This differs from the two-sided Wilks likelihood cutoff. That's the rule of three: after a "
            "hundred clean patients, the side-effect rate could still be as high as three percent. "
            "<bookmark mark='d'/> James Hanley and Abby Lippman-Hand popularized it in 1983, in a paper titled 'If nothing "
            "goes wrong, is everything all right?'"
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.4, buff=0.6, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
                if k == 2:
                    self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def large_n(self):
        from scipy import stats as st
        n, S_ = 200, 122
        lh = S_ / n
        wald = (lh - 1.96 * np.sqrt(lh / n), lh + 1.96 * np.sqrt(lh / n))
        garw = (st.chi2.ppf(0.025, 2 * S_) / 2 / n, st.chi2.ppf(0.975, 2 * S_ + 2) / 2 / n)
        from scipy import optimize
        f = lambda l: 2 * (S_ * np.log(lh / l) - (S_ - n * l)) - 3.8415  # noqa: E731
        lr = (optimize.brentq(f, 0.3, lh), optimize.brentq(f, lh, 1.0))
        rows = fit_rows(VGroup(
            label(r"Bortkiewicz's horse kicks: \ 122 deaths in 200 corps-years", font_size=26, color=DATA),
            MathTex(rf"\text{{Wald: }}[{wald[0]:.3f},\ {wald[1]:.3f}]", font_size=30, color=METHOD_COL["wald"]),
            MathTex(rf"\text{{likelihood ratio: }}[{lr[0]:.3f},\ {lr[1]:.3f}]", font_size=30, color=METHOD_COL["lr"]),
            MathTex(rf"\text{{Garwood (exact): }}[{garw[0]:.3f},\ {garw[1]:.3f}]", font_size=30, color=METHOD_COL["clopper_pearson"]),
            label(r"with 122 events the likelihood is nearly a parabola, \ and all three are close", font_size=24, color=OBS),
            label(r"the methods differ where it matters: \ few events, \ rates near a boundary", font_size=24, color=GREY_A),
        ), 12.6, 0.36, [0, 0.0, 0])
        intro = label('Compare three interval methods with 122 events', font_size=36)
        with self.voiceover(
            "When does the choice of method stop mattering? <bookmark mark='a'/> Take Part 9's horse kicks: a hundred and "
            "twenty-two deaths in two hundred corps-years. <bookmark mark='b'/> The Wald interval for the rate, "
            "<bookmark mark='c'/> the likelihood ratio interval, <bookmark mark='d'/> and Garwood's exact interval agree to "
            "within about a hundredth. <bookmark mark='e'/> With a hundred and twenty-two events the log-likelihood is "
            "almost exactly a parabola, which is the condition under which Wald, likelihood and exact methods agree to first order. "
            "<bookmark mark='f'/> They differ where it matters: few events, or a parameter near the edge of its range."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
