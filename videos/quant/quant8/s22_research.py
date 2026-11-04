from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, BAD, GOOD, KELLY, OVER, PART, UNDER, VALUE, load

PLUG, HALF, STAR, HAT = OVER, UNDER, KELLY, ALT


class Research(VoiceoverScene):
    def construct(self):
        t = load("estrisk_theory")
        self.card()
        self.plug_in()
        self.shrink()
        self.curves(t)
        self.sims(t)
        self.us(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Estimation risk in Merton's rule", r"If the edge must be estimated, how much of the plug-in "
                          r"bet should you place?", part=PART)
        with self.voiceover("For the researcher: Chapter 9 asked what happens if you overestimate your edge by a fixed "
                            "factor. But the error in an estimated edge is random, and it has a law. Here is the exact "
                            "cost of betting on an estimate, and the fraction that minimizes it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def plug_in(self):
        rows = [cmath(r"\hat\pi", r"=", r"\frac{\hat\mu}{\gamma\sigma^2},\qquad \hat\mu \sim N\big(\mu, \sigma^2/T\big)",
                      font_size=32, colors={r"\hat\pi": PLUG}),
                cmath(r"\operatorname{CE}(\pi)", r"=", r"\pi\mu - \tfrac{\gamma}{2}\pi^2\sigma^2", font_size=32,
                      colors={r"\operatorname{CE}(\pi)": VALUE}),
                cmath(r"\mathbb E\,\operatorname{CE}(\hat\pi)", r"=", r"\frac{1}{\gamma}\Big[\theta^2 - \tfrac12\big(\theta^2 "
                      r"+ \tfrac1T\big)\Big] = \frac{\theta^2 - 1/T}{2\gamma}", font_size=32,
                      colors={r"\mathbb E\,\operatorname{CE}(\hat\pi)": PLUG}),
                cmath(r"\mathbb E\,\operatorname{CE}(\hat\pi)", r"<", r"0\quad\Longleftrightarrow\quad T < 1/\theta^2",
                      font_size=32, colors={r"\mathbb E\,\operatorname{CE}(\hat\pi)": BAD})]
        whys = [why(r"Merton's fraction with the mean excess return replaced by its sample average over $T$ years; take "
                    r"$\sigma$ as known for now"),
                why(r"the certainty equivalent per year of holding the fraction $\pi$ for ever, under the true $\mu$: "
                    r"Chapter 1's mean-variance form"),
                why(r"substitute $\hat\pi$, write $\theta = \mu/\sigma$ for the Sharpe ratio, and use $\mathbb E\,\hat\mu^2 = "
                    r"\mu^2 + \sigma^2/T$: the noise enters squared, so it never averages out"),
                why(r"the best possible is $\theta^2/(2\gamma)$; estimation costs exactly $1/(2\gamma T)$ a year, and with a "
                    r"Sharpe ratio of 0.4 the plug-in loses money in expectation on fewer than six years")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.46, edge=6.9)
        with self.voiceover(
            "Start with one risky asset. <bookmark mark='a'/> The plug-in rule is Merton's fraction with the true mean "
            "excess return replaced by its sample average over T years. Keep the volatility known for now. "
            "<bookmark mark='b'/> Score any fraction by its certainty equivalent under the truth: the mean it earns, "
            "less half gamma times its variance. <bookmark mark='c'/> Substitute the estimate. Write theta for the "
            "Sharpe ratio. The expected square of the estimated mean is the true mean squared plus the sampling "
            "variance, and that is the whole story: the noise enters squared, so it never averages away. The expected "
            "certainty equivalent is theta squared minus one over T, over two gamma. <bookmark mark='d'/> The best "
            "possible is theta squared over two gamma. Estimation costs exactly one over two gamma T a year. With a "
            "Sharpe ratio of point four, one over theta squared is six and a quarter years: on less history than that, "
            "the plug-in rule loses money, in expectation, against cash."
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

    def shrink(self):
        rows = [cmath(r"\mathbb E\,\operatorname{CE}(c\,\hat\pi)", r"=", r"\frac{1}{\gamma}\Big[c\,\theta^2 - \tfrac{c^2}{2}"
                      r"\big(\theta^2 + \tfrac1T\big)\Big]", font_size=32,
                      colors={r"\mathbb E\,\operatorname{CE}(c\,\hat\pi)": VALUE}),
                cmath(r"c^*", r"=", r"\frac{T\theta^2}{T\theta^2 + 1}", font_size=34, colors={r"c^*": STAR}),
                cmath(r"\mathbb E\,\operatorname{CE}(c^*\hat\pi)", r"=", r"\frac{\theta^2}{2\gamma}\cdot\frac{T\theta^2}{T\theta^2 "
                      r"+ 1}\ >\ 0", font_size=32, colors={r"\mathbb E\,\operatorname{CE}(c^*\hat\pi)": STAR})]
        whys = [why(r"bet a fixed multiple $c$ of the plug-in: a parabola in $c$"),
                why(r"its vertex: the signal's share of $\mathbb E\,\hat\mu^2$. At $\theta = 0.4$ and $T = 20$ years, $c^* = 0.76$; "
                    r"at $T = 5$, $0.44$. Fractional Kelly is the optimal shrinkage of a noisy estimate"),
                why(r"always positive: a shrunk bet never loses in expectation, at any sample size")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        thm = theorem_card(r"Optimal scaling under parameter uncertainty", wrapped_label(
            r"the expected-utility-maximizing multiple of the plug-in rule is $c^* = T\theta^2/(T\theta^2 + 1)$ for one "
            r"asset; with $N$ assets and an estimated covariance it is smaller still, and mixing in the minimum-variance "
            r"portfolio, a third fund, helps", 10.6, 20, GREY_A),
            who=r"Kan and Zhou (2007), \textit{JFQA} 42; earlier Brown (1976), Klein and Bawa (1976)", width=11.6,
            font_size=22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "So bet less. <bookmark mark='a'/> Scale the plug-in by a constant c, and the expected certainty "
            "equivalent is a parabola in c. <bookmark mark='b'/> Its vertex is T theta squared over T theta squared "
            "plus one: the share of the estimated edge's mean square that is signal rather than noise. At a Sharpe "
            "ratio of point four and twenty years of data, bet seventy-six percent of the plug-in; at five years, forty-"
            "four percent. Fractional Kelly is not timidity: it is the optimal shrinkage of a noisy estimate. "
            "<bookmark mark='c'/> And the shrunk bet's expected certainty equivalent is positive at every sample size. "
            "<bookmark mark='d'/> This is Raymond Kan and Guofu Zhou's result of 2007, which also handles many assets, "
            "where the shrinkage is stronger; that is Part 30."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(thm))
        self.wait(0.5)
        self.clear_scene()

    def curves(self, t):
        T = np.asarray(t["T"], float)
        th = t["theory"]
        g = axes([0, 100], [-0.06, 0.09], x_length=8.4, y_length=4.2, xlabel=r"years of data, $T$",
                 ylabel=r"expected certainty equivalent, \% a year ($\gamma = 1$, $\theta = 0.4$)",
                 xticks=[0, 25, 50, 75, 100], yticks=[-0.04, 0, 0.04, 0.08], yfmt=lambda v: f"{100 * v:.0f}",
                 font_size=15).move_to(LEFT * 1.5 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(100, 0), color=GREY_C, stroke_width=1.2)
        top = DashedLine(ax.c2p(0, t["ce_max"]), ax.c2p(100, t["ce_max"]), color=GREY_B, stroke_width=1.5)
        m = T >= 4
        lines = VGroup(curve(ax, T[m], np.asarray(th["plug"])[m], PLUG, stroke_width=3),
                       curve(ax, T[m], np.asarray(th["half"])[m], HALF, stroke_width=3),
                       curve(ax, T[m], np.asarray(th["star"])[m], STAR, stroke_width=3))
        dots = VGroup(*[Dot(ax.c2p(int(k), v["plug"]), radius=0.07, color=WHITE) for k, v in t["sims"].items()])
        leg = legend([(GREY_B, r"best possible, $\theta^2/2$"), (PLUG, r"plug-in, $c = 1$"), (HALF, r"half, $c = 1/2$"),
                      (STAR, r"$c^*$, if $\theta$ were known"), (WHITE, r"simulated plug-in, $\sigma$ estimated too")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.3)
        fit_right(leg)
        cross = Dot(ax.c2p(1 / t["theta"] ** 2, 0), radius=0.08, color=BAD)
        cl = MathTex(r"T = 1/\theta^2", font_size=20, color=BAD).next_to(cross, DOWN + RIGHT, buff=0.08)
        side = wrapped_label(r"20{,}000 simulated histories per dot, monthly returns, both moments estimated; the dot at "
                             r"five years sits 1.5 points lower because $\mathbb E[\sigma^4/s^4] = 1.11$ on 60 months",
                             3.4, 14, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here are the three rules against the length of the history. <bookmark mark='a'/> The plug-in, in red, "
            "starts deep below zero, crosses it at six and a quarter years, and creeps towards the best possible from "
            "below. <bookmark mark='b'/> Half the plug-in wins until about twenty years, then loses, because once the "
            "estimate is good it bets too little. <bookmark mark='c'/> The optimal multiple, if we knew theta, beats "
            "both everywhere. <bookmark mark='d'/> And the white dots are simulations, estimating the volatility as "
            "well. They sit on the formula, except at five years, where the noise in the estimated variance costs "
            "another point and a half; the exact correction uses the inverse moments of a chi-squared, and it is "
            "the second qualifying problem."
        ) as vo:
            self.play(FadeIn(g), Create(zero), Create(top), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(leg[1]), FadeIn(cross), FadeIn(cl), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines[1]), FadeIn(leg[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lines[2]), FadeIn(leg[3]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(dots), FadeIn(leg[4]), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def sims(self, t):
        Ts = ["5", "10", "20", "50"]
        hx = [-5.0, -2.6, -0.6, 1.4, 3.4, 5.5]
        head = VGroup(label(r"years", font_size=18, color=GREY_B), label(r"plug-in", font_size=20, color=PLUG),
                      label(r"half", font_size=20, color=HALF), label(r"$\hat c\,\hat\pi$", font_size=20, color=HAT),
                      label(r"$c^*$ known", font_size=20, color=STAR), label(r"P(CE $<$ 0)", font_size=18, color=BAD))
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(MathTex(k, font_size=26),
                                                 *[MathTex(rf"{100 * t['sims'][k][f]:.1f}", font_size=26)
                                                   for f in ("plug", "half", "chat", "star_theory")],
                                                 MathTex(rf"{100 * t['sims'][k]['p_negative_ce']:.0f}\%", font_size=26))
                                          for k in Ts]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.9 - 0.68 * j, 0])
            tab.add(row)
        foot = wrapped_label(r"certainty equivalents in \% a year at $\gamma = 1$, true Sharpe ratio 0.4 and volatility 18\%; "
                             r"$\hat c = \max(0, 1 - 1/(T\hat\theta^2))$ estimates the optimal multiple from the same data; "
                             r"the last column: the share of histories whose plug-in bet loses against cash", 12.0, 16,
                             GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The simulations in a table. <bookmark mark='a'/> At five years, the plug-in loses almost four percent a "
            "year in expectation, and in thirty-nine percent of histories it does worse than cash. Half the plug-in "
            "earns over three percent. <bookmark mark='b'/> By fifty years the plug-in is nearly level with the optimal "
            "multiple, within a point of the best possible, and half has fallen behind. <bookmark mark='c'/> The tempting fix is to estimate the "
            "optimal multiple from the same data. Look at the purple column: at five years it is better than the "
            "plug-in, but it loses to plain half at every horizon up to twenty years. The estimated multiple is "
            "itself noisy, and it is largest exactly when the edge has been overestimated. Shrinkage that must be "
            "estimated is a much weaker tool than shrinkage you know."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
            vo.wait_until("b")
            self.play(FadeIn(tab[4]))
            vo.wait_until("c")
            self.play(*[Indicate(r_[3], color=HAT) for r_ in tab[1:]])
        self.wait(0.4)
        self.clear_scene()

    def us(self, t):
        u = t["us"]
        f, l_ = str(t["us_first"]), str(t["us_last"])
        names = [("plug", r"plug-in, expanding window", PLUG), ("half", r"half the plug-in", HALF),
                 ("chat", r"estimated multiple $\hat c$", HAT), ("market", r"100\% in the market", GREY_A),
                 ("hindsight", r"Merton on the full sample (hindsight)", GREY_B)]
        hx = [-4.2, 1.4, 3.4, 5.3]
        head = VGroup(label(r"US market, $\gamma = 2$", font_size=18, color=GREY_B), label(r"CE", font_size=20),
                      label(r"mean", font_size=20), label(r"vol", font_size=20))
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(label(n, font_size=18, color=c),
                                                 *[MathTex(rf"{100 * u[k][f_]:.1f}\%", font_size=24)
                                                   for f_ in ("ce", "mean", "vol")]) for k, n, c in names]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.0 - 0.62 * j, 0])
            row[0].align_to(np.array([hx[0] - 2.6, 0, 0]), LEFT)
            tab.add(row)
        foot = wrapped_label(rf"Kenneth French's market excess return, monthly; each month's weight uses only earlier data, "
                             rf"starting with 1926--35 and scored {f[:4]}-{f[4:]} to {l_[:4]}-{l_[4:]}; CE: mean less "
                             rf"$\gamma/2$ times variance, annualized. The realized Sharpe ratio after 1936 was "
                             rf"{t['us_theta']:.2f}", 11.8, 16, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Now the one history we have: the US market from 1936, each month's bet using only the data before it, "
            "at gamma two. <bookmark mark='a'/> The plug-in earned a certainty equivalent of "
            f"{100 * u['plug']['ce']:.1f} percent; half of it, {100 * u['half']['ce']:.1f}; the estimated multiple, "
            f"{100 * u['chat']['ce']:.1f}. <bookmark mark='b'/> Here the plug-in won. Is the theory wrong? No. The "
            "window started at ten years and grew to ninety-five, so most of the bets were made on long histories, "
            "where the cost of estimation is small. And the Sharpe ratio after 1936 was "
            f"{t['us_theta']:.2f}, above the whole century's {t['us_theta_all']:.2f}: a good draw. An expectation is "
            "not refuted by one path. <bookmark mark='c'/> The path does show two more things. Simply holding the "
            "market, a rule with nothing to estimate, beat all three, because the estimates made just after the crash "
            "of 1929 were small. And hindsight was worth another point and a quarter a year over the plug-in."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:4]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Indicate(tab[1], color=PLUG))
            vo.wait_until("c")
            self.play(FadeIn(tab[4]), FadeIn(tab[5]))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: the best rule you can actually compute", r"$c^*$ needs the true $\theta$; plug-in "
                          r"estimates of it are noisy, and no feasible scaling rule is known to dominate across all "
                          r"$\theta$ and $T$", width=12.4, font_size=18),
            desk_question(r"open: learning, and a moving edge", r"with a Bayesian prior the investor learns while "
                          r"investing, and the horizon matters (Barberis 2000); if the edge itself drifts, how much old "
                          r"data to use and how far to shrink must be chosen together", width=12.4, font_size=18),
            desk_question(r"open: beyond the normal", r"with fat tails, volatility clustering and a long horizon, the "
                          r"exact cost of estimation in Kelly growth, rather than a certainty equivalent, has no closed "
                          r"form", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> The optimal multiple needs the true Sharpe ratio. Estimating it "
            "is noisy, as we saw, and no feasible scaling rule is known to beat all others for every Sharpe ratio and "
            "sample size. <bookmark mark='b'/> A Bayesian investor learns while investing, and Nicholas Barberis showed "
            "in 2000 that parameter uncertainty makes the horizon matter. If the edge itself drifts, how much history "
            "to use and how far to shrink must be chosen together. <bookmark mark='c'/> And with fat tails and "
            "clustered volatility, the exact cost of estimation to Kelly's growth rate has no closed form."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a strategy's Sharpe ratio is estimated at 0.3 from 25 years of data. What multiple of the plug-in "
                       r"bet does Kan and Zhou's rule suggest, if 0.3 were the truth?")
        with self.voiceover(
            "Pause and predict. A Sharpe ratio of point three, estimated from twenty-five years. If that were the truth, "
            "what multiple of the plug-in bet should you place?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
