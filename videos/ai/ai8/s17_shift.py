from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import HIST, MEAS, TEST, TRAIN, chapter, curve, load

PTR, PTE = C.TRUE_P, C.MODEL_Q  # where the training inputs fall, where the test inputs fall
OLS, IW = GREY_B, C.INTERVAL


class Shift(VoiceoverScene):
    def construct(self):
        chapter(self, 16, r"Distribution shift", r"What if the test data comes from somewhere else?",
                "Chapter sixteen. Distribution shift.")
        self.picture()
        self.derive()
        self.results()

    # ------------------------------------------------------------------
    def setup_axes(self, center=(-2.4, -0.6, 0), x_length=7.6, y_length=5.0):
        ax = Axes(x_range=[-1.2, 2.0, 0.5], y_range=[-1.2, 2.2, 1], x_length=x_length, y_length=y_length, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to(center)
        return ax

    def picture(self):
        s = load("shift")
        ax = self.setup_axes()
        from scipy.stats import norm

        f = lambda x: -x + x ** 3  # noqa: E731
        truth = ax.plot(f, x_range=[-1.15, 1.75], color=WHITE, stroke_width=2.5)
        dtr = ax.plot(lambda x: -1.2 + 0.55 * norm.pdf(x, s["mu_tr"], s["sd_tr"]), x_range=[-1.2, 2.0], color=PTR,
                      stroke_width=3)
        dte = ax.plot(lambda x: -1.2 + 0.55 * norm.pdf(x, s["mu_te"], s["sd_te"]) * 0.6, x_range=[-1.2, 2.0], color=PTE,
                      stroke_width=3)
        x0, y0 = np.asarray(s["x0"]), np.asarray(s["y0"])
        dots = VGroup(*[Dot(ax.c2p(a, np.clip(b, -1.15, 2.15)), radius=0.045, color=PTR) for a, b in zip(x0, y0)
                        if -1.2 < a < 2.0])
        co, ci = np.asarray(s["ols_coef"]), np.asarray(s["iw_coef"])
        lo = ax.plot(lambda x: co[0] + co[1] * x, x_range=[-1.2, 2.0], color=OLS, stroke_width=4)
        li = ax.plot(lambda x: ci[0] + ci[1] * x, x_range=[-1.2, 2.0], color=IW, stroke_width=4)
        key = legend([(WHITE, r"truth: \ $y = -x + x^3$ \ (+ noise)"), (PTR, r"training inputs: \ $x \sim p$"),
                      (PTE, r"test inputs: \ $x \sim q$"), (OLS, r"least squares"),
                      (IW, r"least squares weighted by $q/p$")], font_size=20).to_corner(UR, buff=0.35)
        dfn = definition_card(r"covariate shift", r"the inputs' distribution changes, \ $p(x) \to q(x)$, \ while the "
                              r"rule from $x$ to $y$, \ $p(y \mid x)$, \ stays the same.", width=5.0, font_size=20)
        dfn.next_to(key, DOWN, buff=0.35).align_to(key, LEFT)
        tag = note(r"after Shimodaira (2000); \ illustrative").to_corner(DL, buff=0.25)
        with self.voiceover(
            "Everything so far assumed the test data comes from the same distribution as the training data. Often "
            "it doesn't. Here the true relationship is a cubic, <bookmark mark='a'/> the training inputs cluster "
            "around a half, <bookmark mark='b'/> and the inputs we'll be tested on cluster around zero. The rule "
            "from x to y hasn't changed, only where the inputs fall: covariate shift. <bookmark mark='c'/> Fit a "
            "straight line by least squares, and it serves the training region, where most of the points are. "
            "<bookmark mark='d'/> Weight each training point by how much more likely its x is under the test "
            "distribution, and the line turns to serve where the test inputs will be."
        ) as vo:
            self.play(Create(ax), Create(truth), FadeIn(key[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(dtr), FadeIn(dots), FadeIn(key[1]))
            vo.wait_until("b")
            self.play(Create(dte), FadeIn(key[2]), FadeIn(dfn))
            vo.wait_until("c")
            self.play(Create(lo), FadeIn(key[3]))
            vo.wait_until("d")
            self.play(Create(li), FadeIn(key[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"R_q(h)", r"=", r"\int q(x)\, \ell(h, x)\, dx", font_size=36),
            cmath(r"R_q(h)", r"=", r"\int p(x)\, \frac{q(x)}{p(x)}\, \ell(h, x)\, dx", font_size=36),
            cmath(r"R_q(h)", r"=", r"\mathbb{E}_{x \sim p}\big[\, w(x)\, \ell(h, x) \,\big], \quad w = q/p", font_size=36),
            cmath(r"\hat R_w(h)", r"=", r"\frac1n \sum_i w(x_i)\, \ell(h, x_i)", font_size=36,
                  colors={r"\frac1n \sum_i w(x_i)\, \ell(h, x_i)": IW}),
        ]
        whys = [why(r"the risk we care about: \ under the test distribution"),
                why(r"multiply and divide by $p$"),
                why(r"an average over the training distribution"),
                why(r"unbiased, \ from the training sample: \ importance weighting")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-2.6, buff=0.5, edge=6.9)
        hist = history_card(2000, r"H.~Shimodaira", r"\textit{Improving predictive inference under covariate shift by "
                            r"weighting the log-likelihood function}", width=6.0, font_size=17, color=HIST)
        hist.to_corner(DL, buff=0.25)
        ess = label(r"the price: \ variance. \ Effective sample size \ $\dfrac{(\sum w_i)^2}{\sum w_i^2}$ \ (Part 5)",
                    font_size=24, color=GREY_A).to_corner(DR, buff=0.4)
        with self.voiceover(
            "Why weights? <bookmark mark='a'/> The risk we care about averages the loss over the test "
            "distribution q. <bookmark mark='b'/> Multiply and divide by the training distribution p. "
            "<bookmark mark='c'/> Now it's an average over training inputs, of the loss times the ratio q over p. "
            "<bookmark mark='d'/> So the weighted training error is an unbiased estimate of the test error. "
            "Hidetoshi Shimodaira proposed it in 2000. <bookmark mark='e'/> The price is the one part five met in "
            "importance sampling: a few points with huge weights dominate, and the effective sample size shrinks."
        ) as vo:
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(k)
            self.play(FadeIn(hist, shift=UP * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(ess))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        s = load("shift")
        names = [("ols", r"least squares", OLS), ("iw", r"weighted, \ exact $q/p$", IW),
                 ("flat", r"weighted, \ $(q/p)^{1/2}$", C.TRUE_P), ("est", r"weighted, \ $q/p$ estimated", C.BITS)]
        top = max(s["ols_mean"], s["best_risk"]) * 1.15
        G = axes([-0.5, 4.5], [0, top], x_length=7.4, y_length=4.4, xticks=[], yticks=[0, round(top / 2, 2), round(top, 2)],
                 ylabel=r"squared error on test inputs \ (mean of $1{,}000$ runs, $\pm 2$ s.e.)", center=(-2.0, -0.6, 0))
        ax = G.ax
        bs, labs, errs = VGroup(), VGroup(), VGroup()
        for i, (k, nm, col) in enumerate(names):
            v, se = float(s[f"{k}_mean"]), float(s[f"{k}_se"])
            a, b = ax.c2p(i - 0.3, 0), ax.c2p(i + 0.3, v)
            bs.add(Rectangle(width=b[0] - a[0], height=b[1] - a[1], stroke_width=0, fill_color=col,
                             fill_opacity=0.85).move_to([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0]))
            errs.add(Line(ax.c2p(i, v - 2 * se), ax.c2p(i, v + 2 * se), color=WHITE, stroke_width=2))
            labs.add(VGroup(label(nm, font_size=19, color=col), MathTex(f"{v:.3f}", font_size=24, color=col))
                     .arrange(DOWN, buff=0.06).next_to(ax.c2p(i, 0), DOWN, buff=0.12))
        bl = DashedLine(ax.c2p(-0.5, s["best_risk"]), ax.c2p(4.4, s["best_risk"]), color=WHITE, stroke_width=1.5)
        bll = label(rf"the best straight line for $q$: \ ${s['best_risk']:.3f}$", font_size=20).next_to(bl, UP, buff=0.05)
        bll.align_to(bl, RIGHT)
        n = int(s["n"])
        side = VGroup(
            label(rf"effective sample size \\ of the exact weights: \\ ${s['ess_mean']:.0f}$ of ${n}$", font_size=24,
                  color=IW),
            label(r"other shifts: \ labels' frequencies change \\ (label shift); \ or the rule itself changes \\ "
                  r"(concept drift: \ no weighting helps)", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_corner(UR, buff=0.4).shift(DOWN * 0.6)
        r_ols, r_iw, r_est = s["ols_mean"], s["iw_mean"], s["est_mean"]
        helps = r_iw < r_ols - 2 * (s["iw_se"] + s["ols_se"])
        exact = (f"Weighting by the exact ratio brings it to {r_iw:.3f}, close to the best any straight line could "
                 f"do for the test inputs, {s['best_risk']:.3f}. " if helps else
                 f"Weighting by the exact ratio gives {r_iw:.3f}: no clear gain here. ")
        flat_pays = s["flat_mean"] < r_iw
        flat = ("here that pays" if flat_pays else "here it doesn't quite pay")
        with self.voiceover(
            f"Over a thousand runs of {n} training points: plain least squares has a test error of {r_ols:.3f}. "
            "<bookmark mark='a'/> " + exact
            + f"<bookmark mark='b'/> Flattening the weights, the square root of the ratio, trades a little bias for "
            f"less variance; {flat}: {s['flat_mean']:.3f}. <bookmark mark='c'/> In practice nobody knows q over p. But a "
            "classifier trained to tell training inputs from unlabelled test inputs estimates it, from the odds it "
            f"assigns: {r_est:.3f}. <bookmark mark='d'/> The exact weights leave an effective sample of only "
            f"{s['ess_mean']:.0f} points out of {n}. And covariate shift is the easy case: when the label "
            "frequencies change, or the rule itself drifts, the fixes are different, and sometimes there are "
            "none. Part thirty-one returns to this, as the problem of evaluating models on data like the world's."
        ) as vo:
            self.play(FadeIn(G), FadeIn(bs[0]), FadeIn(labs[0]), Create(errs[0]), Create(bl), FadeIn(bll))
            vo.wait_until("a")
            self.play(FadeIn(bs[1]), FadeIn(labs[1]), Create(errs[1]))
            vo.wait_until("b")
            self.play(FadeIn(bs[2]), FadeIn(labs[2]), Create(errs[2]))
            vo.wait_until("c")
            self.play(FadeIn(bs[3]), FadeIn(labs[3]), Create(errs[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[0]))
            self.play(FadeIn(side[1]))
        self.wait(0.3)
        self.clear_scene()
