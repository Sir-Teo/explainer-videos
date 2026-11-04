from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, load

DESK = [
    (r"A strategy has a Sharpe ratio of 1 over 4 years. What is the standard error?",
     r"about 0.6: $\sqrt{(1 + SR^2/2)/T} = \sqrt{1.5/4} \approx 0.61$; the 95\% interval runs from about $-0.2$ to $2.2$"),
    (r"You tested 20 strategies and the best has $p = 0.03$. Is it significant?",
     r"no: Bonferroni needs $p < 0.0025$; the chance that one of 20 null strategies reaches $p < 0.03$ is "
     r"$1 - 0.97^{20} \approx 46\%$"),
    (r"Annual returns sampled monthly over 40 years: how many observations?",
     r"about 40, not 480; use Newey--West with fixed-$b$ critical values, or EWC, and still distrust $t \approx 2$"),
    (r"Five-year returns on a persistent yield give $t = 2.5$ with Newey--West. Do you trade it?",
     r"probably not: such tests reject a true null far more than 5\%, the slope carries Stambaugh's bias, and the "
     r"out-of-sample $R^2$ is likely negative"),
    (r"Pooled slope 0.002, Fama--MacBeth slope 0.017: which is wrong?",
     r"neither: Fama--MacBeth averages within-month slopes; pooled OLS mixes the within slope with the between-month "
     r"(market timing) slope"),
]

PROBLEMS = [
    r"For $h$-month sums of iid returns regressed on a slowly moving predictor, show that the naive standard "
    r"error understates the true one by roughly $\sqrt{h}$.",
    r"From Kendall's $\mathbb{E}[\hat\rho - \rho] \approx -(1 + 3\rho)/T$, derive Stambaugh's bias; evaluate it for "
    r"$\rho = 0.91$, corr$(u, v) = -0.83$, $T = 149$.",
    r"Derive the standard error of a Sharpe ratio from iid normal returns by the delta method.",
    r"Show that Holm's procedure controls the family-wise error rate and rejects at least as much as Bonferroni.",
    r"For $k \ge 3$ means $x_i \sim N(\mu_i, 1)$, show that $(1 - (k - 2)/\|x\|^2)\,x$ has lower total squared "
    r"error than $x$ (James--Stein).",
    r"Show that pooled OLS with month fixed effects equals the Fama--MacBeth average weighted by each month's "
    r"cross-sectional variance of $x$, and that pooled OLS without them averages the within and between slopes.",
    r"Show that the iid bootstrap variance of $\sqrt n\,\bar x^*$ is $\hat\Gamma_0$, and that moving blocks of "
    r"length $\ell$ give approximately a Bartlett-weighted long-run variance.",
    r"(qual) With $\rho = 1 + c/T$, show $T(\hat\rho - \rho) \Rightarrow \int_0^1 J_c\,dW/\int_0^1 J_c^2$, $dJ_c = cJ_c\,dt + dW$ "
    r"(no intercept), from the FCLT for near-integrated processes.",
    r"(qual) With $\phi = -1$ and $\rho = 1$, show $t_{\hat\beta} = -\tau_{DF}$, and use Chapter 5's simulation tools to "
    r"estimate the size of a nominal 5\% one-sided test.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.env = load("envelope")
        self.o = load("overlap")
        self.fe = load("panel_fe")
        self.g = load("gmm")
        self.f = load("fomc")
        self.b = load("bootstrap")
        self.oos = load("oos")
        self.module()
        self.recap()
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def module(self):
        env = self.env
        chart = house_chart(PART, lit=("data",)).scale(0.55).to_edge(UP, buff=0.15)
        rows = [
            (r"\texttt{ols}, \texttt{lrv}, \texttt{fixed\_b\_cv}, \texttt{hodrick\_se}",
             r"White, Newey--West, Hansen--Hodrick, Hodrick 1B, EWC, fixed-$b$, clustered errors"),
            (r"\texttt{fama\_macbeth}, \texttt{within\_between}, \texttt{two\_pass}, \texttt{grs}",
             r"panels, the within/between split, two-pass with Shanken, GRS"),
            (r"\texttt{mle}, \texttt{gmm}", r"Newton with replayable iterates, sandwich errors; two-step GMM with $J$"),
            (r"\texttt{oos\_r2}, \texttt{augmented\_predictive}, \texttt{ivx}", r"out of sample; Stambaugh-proof tests"),
            (r"\texttt{event\_mean\_test}, \texttt{placebo\_means}", r"event studies with placebos"),
            (r"\texttt{stationary\_bootstrap}, \texttt{stationary\_indices}", r"resampling that keeps dependence"),
            (r"\texttt{gibbs\_hierarchical}, \texttt{shrink\_means}", r"Bayesian and empirical-Bayes shrinkage"),
            (r"\texttt{holm}, \texttt{benjamini\_hochberg}", r"family-wise and false-discovery control"),
            (r"\texttt{iv\_2sls}, \texttt{twfe}, \texttt{did\_cs}, \texttt{rd\_local\_linear}, \texttt{dml\_plr}",
             r"causal designs and double ML"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=18, color=QC.HOUSE), label(b, font_size=17, color=GREY_A)).arrange(
            RIGHT, buff=0.3) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 6.4)
        if tab.width > 13.2:
            tab.scale_to_fit_width(13.2)
        tab.next_to(chart, DOWN, buff=0.25)
        rule = wrapped_label(r"Rule 7: no number leaves the House without a standard error that respects how the data "
                             rf"were sampled, and the count of everything tried. The trial counter reads {env['trials']}.",
                             12.4, 22, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The House's statistics module now holds this part's tools, each tested on a simulated case with a known "
            "answer. <bookmark mark='a'/> Robust standard errors and long-run variances; panels and two passes; "
            "likelihood and GMM; out-of-sample and Stambaugh-proof tests; event studies; bootstraps; Gibbs; multiple "
            "testing; causal designs and double ML. <bookmark mark='b'/> And rule seven: no number leaves the House "
            "without a standard error that respects the sampling, and the count of everything tried. With this part's "
            f"registrations, the trial counter reads {env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=6))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def recap(self):
        o, fe, g, f, b, oos = self.o, self.fe, self.g, self.f, self.b, self.oos
        dp = oos["predictors"]["dividend yield"]
        items = [
            (r"OLS is a projection; every standard error is a sandwich whose meat is how the scores co-move", EST),
            (rf"overlap: the dividend yield's $t$ of {o['est']['naive']['t']:.0f} is {o['est']['nw']['t']:.1f} with "
             r"Newey--West; fixed-$b$ and EWC fix the remaining over-rejection", BAD),
            (r"panels: cluster on the shock both $x$ and $u$ share; returns share the month", ALT),
            (rf"pooled ({fe['pooled']:.4f}) = within ({fe['within']:.4f}) mixed with between ({fe['between']:.4f}); "
             r"Fama--MacBeth answers the within question", GOOD),
            (rf"Stambaugh's bias tilts the cloud; out of sample the dividend yield's $R^2$ is "
             rf"{100 * dp['r2_os']:.2f}\%", BAD),
            (rf"MLE and GMM: curvature is precision; the Euler equation is rejected ($J = {g['J']:.0f}$), "
             rf"$\gamma$ barely identified", EST),
            (rf"FOMC days: {1e4 * f['all']['mean_event']:.0f} bp vs {1e4 * f['all']['mean_other']:.0f} bp; events "
             r"sharing a date do not diversify", DATA_C),
            (rf"block bootstraps: the market's Sharpe ratio has a standard error of {b['se_stationary']:.2f} after 94 "
             r"years", EST),
            (r"shrinkage and Gibbs halve the forecast error of 40 means; BH controls false discoveries", GOOD),
            (r"causal designs and double ML; a Sharpe of 0.5 needs 16 years to prove itself", ALT),
        ]
        rows = VGroup()
        for i, (t, c) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=26, color=c), label(t, font_size=21)).arrange(RIGHT, buff=0.25))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        title = label(r"Part 6 in ten lines", font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(title, DOWN, buff=0.3)
        if rows.width > 13.2:
            rows.scale_to_fit_width(13.2)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        with self.voiceover(
            "Part six in ten lines. Least squares is a projection; every standard error is a claim about how scores "
            "co-move. Overlap and persistence inflate t, and even Newey-West needs fixed-b values or EWC. Cluster on the "
            "shared shock. Pooled least squares mixes within-month and market timing; Fama-MacBeth answers the first. "
            "Persistent predictors carry Stambaugh's bias and lose out of sample. Curvature is precision, and GMM "
            "rejects the Euler equation. FOMC days carried a quarter of the excess return. Block bootstraps keep "
            "dependence. Shrinkage beats forty means; Benjamini-Hochberg controls false discoveries. Causal questions "
            "need designs. And a good strategy needs sixteen years."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=20))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.6, font_size=21) for q, a in DESK]).arrange(DOWN, buff=0.15)
        if cards.height > 7.6:
            cards.scale_to_fit_height(7.6)
        with self.voiceover(
            "Five desk questions. A Sharpe of one over four years: a standard error of about zero point six. "
            "<bookmark mark='a'/> Twenty strategies, the best at three percent: not significant. <bookmark mark='b'/> "
            "Forty years sampled monthly: about forty observations. <bookmark mark='c'/> A t of two and a half on "
            "five-year returns: do not trade it on that alone. <bookmark mark='d'/> Pooled against Fama-MacBeth: "
            "different questions. Solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for i, mk in enumerate("abcd", 1):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And nine problems: the cost of overlap, Stambaugh's bias derived, the Sharpe ratio's standard error, "
            "Holm against Bonferroni, the James-Stein estimator, the within and between decomposition of chapter four, "
            "why the iid bootstrap forgets dependence, and two at the level of a qualifying exam: the local-to-unity limit, "
            "and the predictive t-test at a unit root. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"GMM and the stochastic discount factor", [23]),
            (r"Fama--MacBeth, two-pass, GRS and clustering", [24, 25]),
            (r"multiple testing, the trial counter, inference on winners", [25, 26, 43]),
            (r"shrinkage and estimation error", [27, 30]),
            (r"double ML; look-ahead in language models", [27, 28]),
            (r"persistence, unit roots and volatility", [7]),
        ])
        with self.voiceover(
            "Where this returns: GMM in the discount factor of Part twenty-three; Fama-MacBeth and clustering in the "
            "factor parts; multiple testing in the factor zoo, backtesting and the finale; shrinkage in machine learning "
            "and portfolios; double ML and look-ahead in learning from returns and text; persistence in Part seven."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Campbell, Lo and MacKinlay, \textit{The Econometrics of Financial Markets}, ch.\ 2, 4, 8 and App.\ A",
             r"Cochrane, \textit{Asset Pricing} (rev.\ ed.), ch.\ 10--16, 20--21; Hayashi, \textit{Econometrics}, ch.\ 1--8",
             r"Greene, \textit{Econometric Analysis} (8th ed.), ch.\ 2--6, 8, 11, 13--16, 20; Bali, Engle and Murray, "
             r"\textit{Empirical Asset Pricing}, ch.\ 1--6",
             r"Efron and Tibshirani, \textit{An Introduction to the Bootstrap}; Angrist and Pischke, \textit{Mostly "
             r"Harmless Econometrics}; Gelman et al., \textit{Bayesian Data Analysis}"],
            [r"Cowles (1933); Fama, Fisher, Jensen and Roll (1969); Fama and MacBeth (1973); Hansen and Hodrick (1980); "
             r"Hansen (1982); Hansen and Singleton (1982); Newey and West (1987); K\"unsch (1989); Hodrick (1992); "
             r"Shanken (1992)",
             r"Politis and Romano (1994); Benjamini and Hochberg (1995); MacKinlay (1997); Stambaugh (1999); Kiefer and "
             r"Vogelsang (2005); Goyal and Welch (2008); Campbell and Thompson (2008); Petersen (2009)",
             r"Kostakis, Magdalinos and Stamatogiannis (2015); Lucca and Moench (2015); Chang, Hong and Liskovich "
             r"(2015); Lazarus, Lewis, Stock and Watson (2018); Chernozhukov et al.\ (2018); Baker, Larcker and Wang "
             r"(2022)",
             r"Goyal, Welch and Zafirov (2024); Kelly, Malamud and Zhou (2024); Nagel (2025); Andrews, Kitagawa and "
             r"McCloskey (2024); Menkveld et al.\ (2024); P\'erignon et al.\ (2024); Glasserman and Lin (2023)"])
        if card.height > 7.6:
            card.scale_to_fit_height(7.6)
        with self.voiceover(
            "The books and papers, each with its finding in the notes. Every number came from public data: Shiller, "
            "Kenneth French, the St. Louis Fed, and the Federal Reserve's own calendar."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("data",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 7, Time Series and Volatility", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House can now say how sure it is. <bookmark mark='a'/> Next, Part seven: time series and volatility. "
            "ARMA models, unit roots, GARCH and its many children, and forecasts of volatility from the realized "
            "variance we measured in Part five."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
