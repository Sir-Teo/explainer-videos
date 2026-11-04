from __future__ import annotations

import numpy as np

from videos.quant.quant26.common import *  # noqa: F403
from videos.quant.quant26.common import GOOD, HURDLE, IS_C, NOISE, OOS_C, PART, RULE, fit_right, load

NAIVE = QC.LOSS
COND = QC.GAIN
HYB = QC.OPTION


def _pc(s: str) -> str:
    """A rule's label for TeX: its percent signs escaped."""
    return s.replace("%", r"\%")


def _ci(c, digits=2):
    return rf"[{c[0]:.{digits}f},\ {c[1]:.{digits}f}]"


class Research(VoiceoverScene):
    def construct(self):
        t = load("winners")
        self.card(t)
        self.curse()
        self.condition()
        self.invert()
        self.sim(t)
        self.picture(t)
        self.data(t)
        self.reading(t)
        self.open_problems()
        self.question()

    def card(self, t):
        w = t["data"]["1926-86"]
        c = research_card(r"Inference on the winner", rf"The best of 10{{,}}000 rules earned a Sharpe ratio of {w['x']:.2f}. "
                          r"What interval for its true Sharpe ratio is honest, given that it was picked for being best?",
                          part=PART)
        with self.voiceover("For the researcher: Chapters 3 and 8 deflated the best backtest against a hurdle, and asked "
                            "whether it beats noise. A sharper question: given that we picked it for being the best, what "
                            "is an honest estimate of how good it really is, with an interval that covers? Isaiah Andrews, "
                            "Toru Kitagawa and Adam McCloskey answered it exactly."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def curse(self):
        rows = [cmath(r"X", r"\sim", r"N(\mu, \Sigma),\qquad \hat\jmath = \arg\max_j X_j", font_size=34, colors={r"X": RULE}),
                cmath(r"\mathbb E\big[X_{\hat\jmath} - \mu_{\hat\jmath}\big]", r">", r"0", font_size=34,
                      colors={r"\mathbb E\big[X_{\hat\jmath} - \mu_{\hat\jmath}\big]": NAIVE}),
                cmath(r"\Pr\big(\mu_{\hat\jmath} \in X_{\hat\jmath} \pm 1.96\,\sigma_{\hat\jmath}\big)", r"<", r"0.95",
                      font_size=32, colors={r"\Pr\big(\mu_{\hat\jmath} \in X_{\hat\jmath} \pm 1.96\,\sigma_{\hat\jmath}\big)": NAIVE})]
        whys = [why(r"each backtest's Sharpe ratio is an estimate, jointly normal across rules with a covariance we can "
                    r"estimate; we keep the largest"),
                why(r"the winner's curse: the largest estimate is, on average, an overestimate of its own mean"),
                why(r"so the textbook interval undercovers. With 50 independent noise rules it covers $\mu_{\hat\jmath} = 0$ "
                    r"only $0.975^{50} - 0.025^{50} \approx 28\%$ of the time")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Set it up. <bookmark mark='a'/> Each backtest's Sharpe ratio is an estimate; across rules they are jointly "
            "normal, with a covariance we can estimate from the returns. We keep the largest. <bookmark mark='b'/> The "
            "winner's curse: the largest estimate is, on average, an overestimate of its own true value, because it won "
            "partly by luck. <bookmark mark='c'/> So the textbook interval undercovers. With fifty independent noise "
            "rules, it covers the winner's true value of zero only about twenty-eight percent of the time."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def condition(self):
        rows = [cmath(r"Z", r"=", r"X - \frac{\Sigma_{\cdot j}}{\Sigma_{jj}}\,X_j \ \perp\ X_j", font_size=34, colors={r"Z": GREY_A}),
                cmath(r"\{\hat\jmath = j\}", r"=", r"\Big\{X_j \ge \max_{k:\,\Sigma_{jk} < \Sigma_{jj}} \frac{\Sigma_{jj}Z_k}"
                      r"{\Sigma_{jj} - \Sigma_{jk}} = L(Z)\Big\}", font_size=30, colors={r"\{\hat\jmath = j\}": HURDLE}),
                cmath(r"X_j \mid \hat\jmath = j,\ Z", r"\sim", r"N(\mu_j, \Sigma_{jj})\ \text{truncated to } [L(Z), U(Z)]", font_size=30,
                      colors={r"X_j \mid \hat\jmath = j,\ Z": COND})]
        whys = [why(r"regress the other estimates on the winner's: the residual $Z$ is independent of $X_j$ (jointly normal, "
                    r"uncorrelated)"),
                why(r"$X_j \ge X_k$ is $X_j(1 - \Sigma_{jk}/\Sigma_{jj}) \ge Z_k$: a lower bound on $X_j$ for each rival "
                    r"(an upper bound $U$ for any with $\Sigma_{jk} > \Sigma_{jj}$, none here)"),
                why(r"so, given that $j$ won and given $Z$, the winner's estimate is a truncated normal whose only unknown is "
                    r"$\mu_j$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        theorem = theorem_card(r"Inference on winners",
                               wrapped_label(r"the median-unbiased estimate and equal-tailed interval from this truncated "
                                             r"normal have exact coverage conditional on $j$ winning, hence also "
                                             r"unconditionally; a hybrid with a projection interval is never wider "
                                             r"than projection", 9.6, 22),
                               r"Andrews, Kitagawa and McCloskey (2024), \textit{QJE} 139", width=10.4, font_size=22)
        with self.voiceover(
            "The trick is to condition on having won. <bookmark mark='a'/> Regress the other estimates on the winner's. "
            "The residuals are jointly normal and uncorrelated with the winner's estimate, so independent of it. "
            "<bookmark mark='b'/> Rule j beats rule k exactly when its estimate, scaled down by one minus their "
            "relative covariance, beats the residual. Each rival sets a lower bound; the largest is L. "
            "<bookmark mark='c'/> So, given that j won and given the residuals, the winner's estimate is a normal "
            "truncated below at L, and its only unknown is the true value we want. <bookmark mark='d'/> That is Andrews, "
            "Kitagawa and McCloskey's theorem, published in 2024: invert this truncated normal and the interval has "
            "exact coverage, conditional on winning, and therefore unconditionally too."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeOut(Group(*self.mobjects)))
            self.play(FadeIn(theorem, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def invert(self):
        rows = [cmath(r"F(\mu)", r"=", r"\Pr_{\mu}\big(X_j \le x_j \mid L \le X_j \le U\big)\ \ \text{falls as } \mu \text{ rises}",
                      font_size=30, colors={r"F(\mu)": COND}),
                cmath(r"F(\hat\mu_{1/2})", r"=", r"\tfrac12,\qquad F(\mu_{\mathrm{lo}}) = 1 - \tfrac\alpha2,\quad F(\mu_{\mathrm{hi}}) = "
                      r"\tfrac\alpha2", font_size=30, colors={r"F(\hat\mu_{1/2})": COND}),
                cmath(r"\text{hybrid}", r":", r"\text{also truncate to } |X_j - \mu| \le c_\beta\sigma_j,\ \text{level } "
                      r"\tfrac{\alpha - \beta}{1 - \beta}", font_size=30, colors={r"\text{hybrid}": HYB})]
        whys = [why(r"the conditional cdf of the observed estimate, as a function of the unknown mean"),
                why(r"the median-unbiased estimate and the equal-tailed interval: exactly as for an ordinary normal, but on "
                    r"the truncated one. When $x_j$ is close to $L$, the interval becomes very wide"),
                why(r"$c_\beta$: the simultaneous (max-$|t|$) critical value at $\beta = 0.5\%$. The hybrid lies inside "
                    r"the projection interval, and covers at least $1 - \alpha$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Inverting it is mechanical. <bookmark mark='a'/> Write the conditional distribution function of the "
            "observed estimate as a function of the unknown mean. It falls as the mean rises. <bookmark mark='b'/> The "
            "mean that puts the estimate at the median is median-unbiased; the means that put it at the two tails "
            "bound the interval. The catch: when the winner barely won, its estimate sits near the truncation point and "
            "the interval becomes very wide. <bookmark mark='c'/> The hybrid fixes that. First take a simultaneous "
            "interval at a tiny level, half a percent, then condition on the truth lying inside it too. The result is "
            "never wider than the simultaneous interval, and still covers at least ninety-five percent."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def picture(self, t):
        w = t["data"]["1987-2003"]
        inv = t["inv"]
        mu = np.asarray(inv["mu"], float)
        g = axes([-3, 2], [0, 1], x_length=8.0, y_length=4.2, xlabel=r"candidate true Sharpe ratio $\mu$ of the "
                 r"1987--2003 winner", ylabel=r"$F(\mu)$: chance of an estimate at or below the one observed, given it won",
                 xticks=[-3, -2, -1, 0, 1, 2], yticks=[0, 0.5, 1], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        curves = {}
        for key, col in (("naive", NAIVE), ("cond", COND), ("hybrid", HYB)):
            y = np.asarray(inv[key], float)
            ok = np.isfinite(y)
            curves[key] = curve(ax, mu[ok], y[ok], col, stroke_width=3)
        levels = VGroup(*[DashedLine(ax.c2p(-3, v), ax.c2p(2, v), color=GREY_C, stroke_width=1.5) for v in (0.025, 0.5, 0.975)])
        dots = VGroup(Dot(ax.c2p(w["x"], 0.5), color=NAIVE), Dot(ax.c2p(w["med"], 0.5), color=COND),
                      Dot(ax.c2p(w["hyb_med"], 0.5), color=HYB))
        leg = legend([(NAIVE, r"naive: a plain normal"), (COND, r"conditional on winning"),
                      (HYB, r"hybrid: inside the simultaneous interval")], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        side = wrapped_label(rf"{_pc(w['label'])} won by {w['gap']:.2f} standard errors over {_pc(w['binding'])}. Estimates where "
                             rf"each curve crosses $\frac12$: {w['x']:.2f}, {w['med']:.2f}, {w['hyb_med']:.2f}; the "
                             rf"conditional interval runs off the chart to {w['cond'][0]:.1f}", 3.4, 15,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here is the inversion, for the rule chosen on 1987 to 2003. It beat its closest rival by a hair: "
            f"{w['gap']:.2f} standard errors. <bookmark mark='a'/> Red is the naive distribution function, a plain "
            f"normal. It crosses one half at the estimate itself, {w['x']:.2f}. <bookmark mark='b'/> Green is the "
            "conditional one. Because the winner sits right at the point where it would stop winning, the curve stays "
            f"high far to the left: the median-unbiased estimate is {w['med']:.2f}, and the interval runs off the chart, "
            f"to {w['cond'][0]:.0f}. That is the conditional method's weakness. <bookmark mark='c'/> Purple is the "
            "hybrid, defined only inside the simultaneous interval. It crosses one half at "
            f"{w['hyb_med']:.2f}, and its interval runs from {w['hybrid'][0]:.2f} to {w['hybrid'][1]:.2f}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(levels), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(curves["naive"]), FadeIn(dots[0]), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(curves["cond"]), FadeIn(dots[1]), FadeIn(leg[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(curves["hybrid"]), FadeIn(dots[2]), FadeIn(leg[2]))
        self.wait(0.4)
        self.clear_scene()

    def sim(self, t):
        hx = [-4.6, -2.2, -0.6, 1.0, 2.6, 4.6]
        head = VGroup(label(r"true means", font_size=18, color=GREY_B), label(r"naive", font_size=19, color=NAIVE),
                      label(r"conditional", font_size=19, color=COND), label(r"hybrid", font_size=19, color=HYB),
                      label(r"projection", font_size=19, color=GREY_A), label(r"median bias: naive / $\hat\mu_{1/2}$",
                                                                              font_size=17, color=GREY_B))
        tab = VGroup(head)
        for name, s_ in t["sims"].items():
            cv, ln = s_["cover"], s_["length"]
            tab.add(VGroup(label(name, font_size=18),
                           *[MathTex(rf"{100 * cv[k]:.0f}\%\ ({ln[k]:.1f})", font_size=24) for k in ("naive", "cond", "hybrid", "proj")],
                           MathTex(rf"{s_['medbias_naive']:+.2f}\ /\ {s_['medbias_med']:+.2f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.5 - 0.8 * j, 0])
        foot = wrapped_label(rf"{t['J']} estimates with unit standard error, correlation {t['rho']:.1f} between every pair; "
                             rf"{t['reps']:,} draws per row; coverage of the winner's true mean by 95\% intervals, median "
                             r"length in brackets; projection: the simultaneous max-$|t|$ interval", 11.4, 16,
                             GREY_A).to_edge(DOWN, buff=0.6)
        z, c1 = t["sims"]["all zero"], t["sims"]["one clear winner"]
        with self.voiceover(
            f"Check it. Fifty correlated estimates, {t['reps']:,} draws for each world. <bookmark mark='a'/> When every "
            f"true mean is zero, the naive interval covers only {100 * z['cover']['naive']:.0f} percent of the time, and "
            f"its estimate is {z['medbias_naive']:.1f} standard errors too high. When one rule is clearly best, the naive "
            f"interval covers {100 * c1['cover']['naive']:.0f} percent: there is little curse when the winner was never "
            "in doubt. <bookmark mark='b'/> The conditional and hybrid intervals cover ninety-five percent or a little "
            "more in every world, and the median-unbiased estimate has almost no median bias. <bookmark mark='c'/> The "
            "price is length. The conditional interval can be very long; the hybrid is shorter than the simultaneous "
            "interval, and longer than the naive one, which is the honest price of having searched."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot), *[FadeIn(r_[0]) for r_ in tab[1:]])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_[1]) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[2], r_[3], r_[5])) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_[4]) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def data(self, t):
        hx = [-4.9, -2.3, -0.2, 1.9, 4.6]
        head = VGroup(label(r"chosen on", font_size=18, color=GREY_B), label(r"naive", font_size=19, color=NAIVE),
                      label(r"conditional", font_size=19, color=COND), label(r"hybrid", font_size=19, color=HYB),
                      label(r"afterwards ($\pm 1.96$ s.e.)", font_size=18, color=OOS_C))
        tab = VGroup(head)
        for name, w in t["data"].items():
            after = rf"{w['first_out'] // 10000}\text{{--}}{w['last_out'] // 10000 % 100:02d}"
            tab.add(VGroup(VGroup(label(rf"{name}", font_size=20), label(_pc(w["label"]), font_size=15, color=GREY_A)).arrange(DOWN, buff=0.08),
                           VGroup(MathTex(rf"{w['x']:.2f}", font_size=26), MathTex(_ci(w["naive"]), font_size=20)).arrange(DOWN, buff=0.08),
                           VGroup(MathTex(rf"{w['med']:.2f}", font_size=26), MathTex(_ci(w["cond"]), font_size=20)).arrange(DOWN, buff=0.08),
                           VGroup(MathTex(rf"{w['hyb_med']:.2f}", font_size=26), MathTex(_ci(w["hybrid"]), font_size=20)).arrange(DOWN, buff=0.08),
                           VGroup(MathTex(rf"{w['out']:.2f}", font_size=26),
                                  MathTex(rf"\pm {1.96 * w['s_out']:.2f}\ \ ({after})", font_size=20)).arrange(DOWN, buff=0.08)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 1.2 * j, 0])
        foot = wrapped_label(r"annualised Sharpe ratios of the best of the 10{,}000 rules, chosen in each era; standard error "
                             r"$\sqrt{252/T}$; correlations between rules estimated from their daily returns; $c_\beta$ by a "
                             r"multiplier bootstrap of all 10{,}000 rules", 11.4, 16, GREY_A).to_edge(DOWN, buff=0.55)
        a_, b_ = t["data"]["1926-86"], t["data"]["1987-2003"]
        with self.voiceover(
            "Now the ten thousand rules, chosen twice. <bookmark mark='a'/> Chosen on 1926 to 1986, the winner led by "
            f"{a_['gap']:.1f} standard errors, and conditioning changes nothing: {a_['x']:.2f}, with an interval from "
            f"{a_['cond'][0]:.2f} to {a_['cond'][1]:.2f}. Afterwards it earned {a_['out']:.2f}. <bookmark mark='b'/> "
            f"Chosen on 1987 to 2003, the winner's {b_['x']:.2f} becomes about zero under the hybrid, with an interval "
            f"from {b_['hybrid'][0]:.2f} to {b_['hybrid'][1]:.2f}. Afterwards it earned {b_['out']:.2f}, give or take "
            f"{1.96 * b_['s_out']:.2f}."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
        self.wait(0.4)
        self.clear_scene()

    def reading(self, t):
        a_, b_ = t["data"]["1926-86"], t["data"]["1987-2003"]
        cards = VGroup(
            desk_question(r"1926--86: not selection, but the world changing", rf"the winner led by {a_['gap']:.1f} "
                          r"standard errors, so having picked it costs nothing; no interval for the in-sample mean covers "
                          r"what came after. Index autocorrelation, much of it attributed to stale prices, faded after "
                          r"the 1980s", width=12.4, font_size=18),
            desk_question(r"1987--2003: selection, all of it", rf"{b_['n_close']} rules lay within two standard errors of "
                          r"the winner; picked from a crowd, its honest estimate is about zero, as the next seventeen years "
                          r"agreed", width=12.4, font_size=18),
            desk_question(r"what it adds to deflation", r"the deflated Sharpe ratio asks whether the winner beats noise; "
                          r"this asks how good it is, with an interval that covers. Both use the trials, here through the "
                          r"rivals' covariance", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Two different failures. <bookmark mark='a'/> The old winner's collapse was not selection. It led by "
            f"{a_['gap']:.0f} standard errors, so having picked it costs nothing. The market changed: the short-term "
            "autocorrelation of the index, much of it attributed to stale prices, faded after the 1980s. Inference on "
            "winners corrects for selection, not for a world that stops paying. <bookmark mark='b'/> The later winner's "
            f"collapse was selection, all of it. {b_['n_close']} rules lay within two standard errors of it; picked from "
            "a crowd, its honest estimate is about zero, and the next seventeen years agreed. <bookmark mark='c'/> And it "
            "complements deflation. The deflated Sharpe ratio asks whether the winner beats noise; this asks how good it "
            "is. Both use the trials, here through the rivals' covariance."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: non-normal, dependent returns", r"the theorem needs a normal estimate with known "
                          r"covariance; with fat tails and time-varying volatility it holds only asymptotically, and how fast "
                          r"in Sharpe-ratio problems is not well charted", width=12.4, font_size=18),
            desk_question(r"open: adaptive research", r"real searches are sequential: each try depends on the last. "
                          r"Conditioning on a whole research path, not just one argmax, is largely open", width=12.4,
                          font_size=18),
            desk_question(r"open: winners in a changing world", r"combining selection-corrected inference with "
                          r"structural breaks, so that an interval covers next decade's Sharpe ratio, not last decade's", width=12.4,
                          font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> The theorem needs a normal estimate with a known covariance. With "
            "fat tails and changing volatility it holds only in large samples, and how large, for Sharpe ratios, is not "
            "well charted. <bookmark mark='b'/> Real research is sequential: each try depends on the last. Conditioning "
            "on a whole research path, not one maximum, is largely open. <bookmark mark='c'/> And an interval that "
            "covers next decade's Sharpe ratio, not last decade's, needs selection and structural change handled "
            "together."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"two uncorrelated rules, both with standard error 0.2; estimates 1.0 and 0.98. Is the winner's "
                       r"conditional interval wide or narrow? And if the estimates were 1.0 and 0.2?")
        with self.voiceover(
            "Pause and predict. Two uncorrelated rules, each with standard error point two. Their estimates are one "
            "and point nine eight. Is the winner's conditional interval wide or narrow? And if the estimates were one "
            "and point two?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
