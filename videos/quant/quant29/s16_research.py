from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import BAD, COMB, GOOD, HURDLE, PART, TRAIN_C, VALID_C, fit_right, load

T_COL = {"250": QC.LOSS, "500": QC.DELTA, "1000": QC.GAIN}


class Research(VoiceoverScene):
    def construct(self):
        t = load("theory")
        self.card()
        self.setup_()
        self.derive()
        self.mirror()
        self.theorem()
        self.sims(t)
        self.wishart(t)
        self.marginal(t)
        self.data(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"How many alphas can you combine?", r"When does one more weak signal make an estimated "
                          r"combination worse?", part=PART)
        with self.voiceover("For the researcher: Chapter seven combined mined alphas with weights estimated from the "
                            "data. Every extra signal brings some edge and some estimation error. Exactly how do they "
                            "trade off, and when does one more alpha make the combination worse?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"r_t", r"\sim", r"N(\mu, \Sigma),\quad t = 1, \dots, T,\quad r_t \in \mathbb R^K", font_size=32,
                      colors={r"r_t": COMB}),
                cmath(r"w^*", r"=", r"\Sigma^{-1}\mu,\qquad SR_*^2 = \mu^\top\Sigma^{-1}\mu = \|\theta\|^2,\quad \theta = "
                      r"\Sigma^{-1/2}\mu", font_size=30, colors={r"w^*": GOOD}),
                cmath(r"\hat w", r"=", r"\Sigma^{-1}\hat\mu,\qquad \hat\mu = \tfrac1T\textstyle\sum_t r_t", font_size=32,
                      colors={r"\hat w": HURDLE})]
        whys = [why(r"$K$ alphas' daily long-short returns, jointly normal and independent through time"),
                why(r"the best combination and its Sharpe ratio: the length of the vector of standardised means"),
                why(r"the plug-in rule with the covariance known (the estimated case is worse; we return to it): only the "
                    r"means are estimated, from $T$ days")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Set it up. <bookmark mark='a'/> K alphas, each a daily long-short return; jointly normal, independent from "
            "day to day. <bookmark mark='b'/> The best combination weights them by the inverse covariance times their "
            "means, and its Sharpe ratio is the length of the vector of standardised means, theta. <bookmark mark='c'/> "
            "In practice the means are estimated from T days. Give the rule the true covariance for now, so only the "
            "means are noisy."
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

    def derive(self):
        rows = [cmath(r"z", r"=", r"\Sigma^{1/2}\hat w = \Sigma^{-1/2}\hat\mu = \theta + \tfrac{1}{\sqrt T}\,\varepsilon,\quad "
                      r"\varepsilon \sim N(0, I_K)", font_size=30, colors={r"z": HURDLE}),
                cmath(r"SR(\hat w)", r"=", r"\frac{\hat w^\top\mu}{\sqrt{\hat w^\top\Sigma\hat w}} = \frac{z^\top\theta}{\|z\|}",
                      font_size=32, colors={r"SR(\hat w)": GOOD}),
                cmath(r"\mathbb E\,z^\top\theta", r"=", r"\|\theta\|^2,\qquad \mathbb E\,\|z\|^2 = \|\theta\|^2 + \frac KT",
                      font_size=32),
                cmath(r"SR(\hat w)", r"\approx", r"\frac{SR_*^2}{\sqrt{SR_*^2 + K/T}} = \frac{SR_*}{\sqrt{1 + K/(T\,SR_*^2)}}",
                      font_size=32, colors={r"SR(\hat w)": GOOD})]
        whys = [why(r"whiten: in the coordinates where the alphas are independent with unit variance, the estimated weights "
                    r"are the true direction plus noise of size $1/\sqrt T$ in each of $K$ directions"),
                why(r"the out-of-sample Sharpe ratio of any weights is the cosine of their angle to $\theta$, times $\|\theta\|$"),
                why(r"the signal adds $\|\theta\|^2$; the noise adds $1/T$ in every one of the $K$ directions"),
                why(r"replacing the ratio's parts by their means (exact as $T \to \infty$ with $K/T$ fixed): the edge is "
                    r"diluted by the dimension")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Now the calculation. <bookmark mark='a'/> Rotate into coordinates where the alphas are independent with unit "
            "variance. There, the estimated weights are the true direction theta plus noise of size one over root T in "
            "each of the K directions. <bookmark mark='b'/> The out-of-sample Sharpe ratio of any weights is the length of "
            "theta times the cosine of the angle between the weights and theta. <bookmark mark='c'/> On average the "
            "numerator is the squared length of theta, and the squared length of the weights is that plus K over T: the "
            "noise contributes one over T in every direction. <bookmark mark='d'/> So the out-of-sample Sharpe ratio is "
            "about the true one divided by the square root of one plus K over T times the true squared Sharpe ratio. The "
            "edge is diluted by the dimension."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def mirror(self):
        rows = [cmath(r"SR_{\text{in}}(\hat w)", r"=", r"\frac{\hat w^\top\hat\mu}{\sqrt{\hat w^\top\Sigma\hat w}} = \|z\|",
                      font_size=32, colors={r"SR_{\text{in}}(\hat w)": TRAIN_C}),
                cmath(r"\|z\|", r"\approx", r"\sqrt{SR_*^2 + K/T}", font_size=32, colors={r"\|z\|": TRAIN_C}),
                cmath(r"SR_{\text{in}} \cdot SR_{\text{out}}", r"\approx", r"SR_*^2", font_size=34,
                      colors={r"SR_{\text{in}} \cdot SR_{\text{out}}": HURDLE})]
        whys = [why(r"measured on the same days that estimated the weights, the Sharpe ratio is the length of $z$ itself"),
                why(r"it grows with $K$ even when the alphas are worthless: $\sqrt{K/T}$ of pure fit"),
                why(r"in-sample optimism and out-of-sample loss are two faces of one quantity: the more one rises, the more "
                    r"the other falls")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The same calculation explains the training years. <bookmark mark='a'/> Measured on the days that estimated "
            "the weights, the Sharpe ratio is simply the length of z. <bookmark mark='b'/> That is about the square root "
            "of the true squared Sharpe ratio plus K over T: it grows with every alpha added, even worthless ones. "
            "<bookmark mark='c'/> Multiply the two: the in-sample and out-of-sample Sharpe ratios multiply to about the "
            "true squared Sharpe ratio. Optimism in sample and disappointment out of sample are one quantity seen from "
            "two sides, which is exactly what Chapter seven's training and 2020 lines showed."
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

    def theorem(self):
        st = VGroup(MathTex(r"SR(\hat w) \xrightarrow{\ p\ } \frac{SR_*}{\sqrt{1 + \gamma/SR_*^2}},\qquad K, T \to \infty,\ "
                            r"K/T \to \gamma", font_size=32),
                    wrapped_label(r"with the covariance estimated as well, the loss is larger: the estimated inverse "
                                  r"covariance is biased up by $(T - 1)/(T - K - 2)$ and noisy, as Kan and Zhou (2007) work out "
                                  r"exactly for the plug-in portfolio; shrinkage recovers part of it", 9.6, 20)
                    ).arrange(DOWN, buff=0.35)
        card = theorem_card(r"Estimation risk in combinations", st, r"after Brown (1976); Kan and Zhou (2007), "
                            r"\textit{JFQA} 42", width=11.4, font_size=22)
        with self.voiceover(
            "Stated as a limit. <bookmark mark='a'/> As the number of alphas and the number of days both grow, with their "
            "ratio fixed at gamma, the plug-in combination's Sharpe ratio converges to the true one over the square root "
            "of one plus gamma over the true squared Sharpe ratio. <bookmark mark='b'/> Estimating the covariance too "
            "makes things worse: its inverse is biased upward and noisy, as Raymond Kan and Guofu Zhou worked out exactly "
            "in 2007 for the plug-in portfolio, and shrinkage recovers part of the loss."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.5)
        self.clear_scene()

    def sims(self, t):
        Ks = np.asarray(t["Ks"], float)
        g = axes([0, np.log10(Ks[-1]) + 0.05], [0, 0.3], x_length=7.2, y_length=4.4, xlabel=r"number of alphas combined, $K$ "
                 r"(log scale)", ylabel=r"out-of-sample Sharpe ratio, per day", xticks=[0, 1, np.log10(Ks[-1])],
                 yticks=[0, 0.1, 0.2, 0.3], xfmt=lambda v: f"{10 ** v:.0f}", font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        x = np.log10(Ks)
        star = [r["star"] for r in t["sims"]["500"]]
        top = curve(ax, x, star, GREY_B, stroke_width=2)
        lines, dots, est = VGroup(), VGroup(), VGroup()
        for T in ("250", "500", "1000"):
            rows = t["sims"][T]
            lines.add(curve(ax, x, [r["theory"] for r in rows], T_COL[T], stroke_width=3))
            dots.add(VGroup(*[Dot(ax.c2p(a, r["known"]), radius=0.05, color=T_COL[T]) for a, r in zip(x, rows)]))
            est.add(VGroup(*[Triangle(color=T_COL[T], fill_opacity=0.9).scale(0.06).move_to(ax.c2p(a, r["estimated"]))
                             for a, r in zip(x, rows) if np.isfinite(r["estimated"]) and r["estimated"] > 0]))
        leg = legend([(GREY_B, r"$SR_*$: what the true weights earn"), (T_COL["250"], r"$T = 250$ days"),
                      (T_COL["500"], r"$T = 500$"), (T_COL["1000"], r"$T = 1{,}000$")], font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"every alpha has a Sharpe ratio of {t['sr_each']:.2f} a day (about "
                             rf"{t['sr_each'] * math.sqrt(365):.1f} a year) and is independent of the others. Lines: the formula; "
                             r"dots: simulation with the covariance known; triangles: estimated too (300 draws each)", 3.4, 14,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        r250 = t["sims"]["250"]
        sr_year = t["sr_each"] * math.sqrt(365)
        with self.voiceover(
            f"Check it. Give every alpha the same small edge, a Sharpe ratio of {sr_year:.2f} a year, "
            "and make them independent. <bookmark mark='a'/> The grey line is what the true weights would earn: it grows like the square "
            "root of K. <bookmark mark='b'/> The coloured lines are the formula for one, two and four years of data, and "
            "the dots are simulations: they sit on the lines. With a year of data, forty alphas earn "
            f"{r250[5]['known']:.3f} a day out of sample against a possible {r250[5]['star']:.3f}. <bookmark mark='c'/> "
            "The triangles estimate the covariance too, and lose more again, especially when K approaches T."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(top))
            vo.wait_until("b")
            self.play(*[Create(l_) for l_ in lines], *[FadeIn(d_) for d_ in dots], run_time=2)
            vo.wait_until("c")
            self.play(*[FadeIn(e_) for e_ in est])
        self.wait(0.4)
        self.clear_scene()

    def wishart(self, t):
        rows = [cmath(r"(T - 1)\hat\Sigma", r"\sim", r"W_K(T - 1, \Sigma)", font_size=32, colors={r"(T - 1)\hat\Sigma": HURDLE}),
                cmath(r"\mathbb E\big[\hat\Sigma^{-1}\big]", r"=", r"\frac{T - 1}{T - K - 2}\,\Sigma^{-1}", font_size=32,
                      colors={r"\mathbb E\big[\hat\Sigma^{-1}\big]": BAD}),
                cmath(r"\hat w", r"=", r"\hat\Sigma^{-1}\hat\mu:\ \text{two noises, and the second is not averaged away}",
                      font_size=30, colors={r"\hat w": HURDLE})]
        whys = [why(r"the sample covariance of normal returns is a Wishart matrix with $T - 1$ degrees of freedom, "
                    r"independent of $\hat\mu$"),
                why(r"its inverse is biased upward, without bound as $K$ approaches $T$; the bias inflates every weight "
                    r"alike, but the noise around it tilts the weights in random directions"),
                why(rf"in the simulation: with $T = 250$ and $K = 80$, "
                    rf"{t['sims']['250'][-1]['known']:.3f} a day with $\Sigma$ known, "
                    rf"{t['sims']['250'][-1]['estimated']:.3f} with $\Sigma$ estimated")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        r80 = t["sims"]["250"][-1]
        with self.voiceover(
            "Why does estimating the covariance cost more? <bookmark mark='a'/> The sample covariance of normal returns is "
            "a Wishart matrix with T minus one degrees of freedom, independent of the estimated means. "
            "<bookmark mark='b'/> Its inverse is biased upward by T minus one over T minus K minus two, which explodes as "
            "the number of alphas approaches the number of days. A pure scale would not change the Sharpe ratio, but the "
            "noise around it tilts the weights in random directions. <bookmark mark='c'/> So the plug-in rule carries two "
            "noises, and the second does not average away. In the simulation with one year of data and eighty alphas: "
            f"{r80['known']:.3f} a day with the covariance known, {r80['estimated']:.3f} with it estimated."
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

    def marginal(self, t):
        rows = [cmath(r"f(S, K)", r"=", r"\frac{S}{\sqrt{S + K/T}},\qquad S = SR_*^2", font_size=32, colors={r"f(S, K)": GOOD}),
                cmath(r"\Delta f > 0", r"\iff", r"s^2\big(\tfrac S2 + \tfrac KT\big) > \frac{S}{2T}", font_size=32),
                cmath(r"s^2", r">", r"\frac{S}{T S + 2K}", font_size=34, colors={r"s^2": HURDLE})]
        whys = [why(r"the out-of-sample Sharpe ratio as a function of the total squared edge and the number of alphas"),
                why(r"add one alpha with squared Sharpe ratio $s^2$ (independent of the rest): $S$ grows by $s^2$, $K$ by one; "
                    r"to first order the change is positive exactly when"),
                why(r"a new alpha helps only if its own squared Sharpe ratio exceeds this bar, which shrinks with $T$ but not "
                    r"to zero: with many weak alphas, the weakest ones hurt")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        dim = t["diminishing"]
        best = t["best_K_dim"]
        with self.voiceover(
            "So when does one more alpha help? <bookmark mark='a'/> Write the out-of-sample Sharpe ratio as a function of "
            "the total squared edge S and the count K. <bookmark mark='b'/> Add one independent alpha with squared Sharpe "
            "ratio s squared: S grows by s squared and K by one. <bookmark mark='c'/> To first order it helps only if s "
            "squared exceeds S over T S plus two K. When alphas get weaker as you go down the list, there is a best number "
            f"to combine: with two years of data and the k-th alpha's edge falling like one over root k, the formula peaks "
            f"at about {best}, and adding more makes the combination worse."
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

    def data(self, t):
        rows = t["data"]
        hx = [-4.2, -1.6, 1.0, 3.6]
        head = VGroup(label(r"alphas combined, $K$", font_size=18, color=GREY_B),
                      label(r"estimated weights, 2018--19", font_size=18, color=TRAIN_C),
                      label(r"estimated weights, 2020", font_size=18, color=VALID_C),
                      label(r"equal weights, 2020", font_size=18, color=COMB))
        tab = VGroup(head)
        for r in rows:
            tab.add(VGroup(MathTex(f"{r['K']}", font_size=26), MathTex(f"{r['mv_train']:.2f}", font_size=26),
                           MathTex(f"{r['mv_valid']:.2f}", font_size=26), MathTex(f"{r['ew_valid']:.2f}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.2 - 0.62 * j, 0])
        foot = wrapped_label(r"annualised Sharpe ratios before costs; the $K$ best random formulas by training IC, "
                             r"de-duplicated; weights fitted on 2018--19 daily long-short returns", 11.4, 16,
                             GREY_A).to_edge(DOWN, buff=0.5)
        k_best = max(rows, key=lambda r: r["mv_valid"])["K"]
        r40 = rows[-1]
        with self.voiceover(
            "On the mined alphas. <bookmark mark='a'/> In sample, estimated weights look better the more alphas you give "
            "them: they fit noise in every new direction. <bookmark mark='b'/> On 2020, the estimated combination does "
            f"best with {k_best} alphas; with forty its Sharpe ratio is {r40['mv_valid']:+.2f}. Equal weights, which "
            "estimate nothing, do better at every size above one, and with forty they still earn "
            f"{r40['ew_valid']:.2f}. These alphas are far from independent, so the formula's numbers do not apply as they "
            "stand, but its message does: with many noisy, correlated alphas, estimating weights costs more than it "
            "brings."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1])) for r_ in tab[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[2], r_[3])) for r_ in tab[1:]], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: alphas chosen by the same data", r"the formula assumes the $K$ alphas were fixed in advance; "
                          r"when they are the winners of a search on the same days, their means are biased up as well, and "
                          r"the joint correction is not settled", width=12.4, font_size=18),
            desk_question(r"open: time-varying edges", r"if each alpha's mean decays, $T$ is not a sample size but a trade-off "
                          r"between noise and staleness", width=12.4, font_size=18),
            desk_question(r"open: the best shrinkage for many weak alphas", r"nonlinear covariance shrinkage and shrinking the "
                          r"means toward equal weights both help; the optimal joint rule in high dimension is an active topic",
                          width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> The formula assumes the alphas were fixed in advance; when they "
            "are the winners of a search on the same days, their means are biased too, and the joint correction is not "
            "settled. <bookmark mark='b'/> If each alpha's edge decays, more days is not simply better: it trades noise "
            "against staleness. <bookmark mark='c'/> And the best way to shrink both the means and the covariance of many "
            "weak alphas at once is still an active topic."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"20 independent alphas, each with a daily Sharpe ratio of 0.02, and one year (365 days) of data. "
                       r"Compute $SR_*$ and the formula's out-of-sample Sharpe ratio.")
        with self.voiceover(
            "Pause and predict. Twenty independent alphas, each with a daily Sharpe ratio of point zero two, and a year of "
            "data. What is the best possible Sharpe ratio, and what does the formula say you will get out of sample?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
