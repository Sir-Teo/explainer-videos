from __future__ import annotations

from videos.stats.stats23.common import *  # noqa: F403

PROBLEMS = [
    r"Show that $F = (\mathrm{RSS}_0 - \mathrm{RSS})/(q s^2)$ equals the Wald form $(C\hat\beta - d)^\top[C(X^\top X)^{-1}C^\top]^{-1}(C\hat\beta - d)/(q s^2)$.",
    r"Equicorrelated errors within clusters of size $m$, \ a cluster-level regressor: \ derive Moulton's factor $1 + (m - 1)\rho$.",
    r"With $w = x + u$, \ show $\hat\beta_w \to \beta\lambda$. \ What happens to the intercept?",
    r"Show $E\,e_i^2 = (1 - h_{ii})\sigma^2$ under homoskedasticity, \ so HC2 is unbiased there.",
    r"Derive $\hat\beta - \hat\beta_{(i)} = (X^\top X)^{-1}x_i e_i/(1 - h_{ii})$ from Sherman--Morrison.",
    r"$x \sim N(0, 1)$, \ $y = x^2$: \ find $\beta^*$, \ and the true and classical variances of the OLS slope.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"Longley: \ 0 digits vs 12", PATH), (r"what Part 12 assumed", GREY_A),
            (r"$C\beta = d$: \ one $F$ for all", OLS_C), (r"GLS: \ whiten, \ then OLS", GLS_C),
            (r"AR(1): \ naive SE covers 48\%", RES), (r"HC0 to HC3; \ the wild bootstrap", OLS_C),
            (r"clusters: \ Moulton's factor 7.9", CLUSTER), (r"few clusters: \ the wild cluster bootstrap", CLUSTER),
            (r"$\beta^*$: \ the best linear predictor", TEAL), (r"attenuation; \ Hubble's three slopes", NOISY),
            (r"quantile regression: \ the fan", PATH), (r"B-splines: \ curves as bases", GLS_C),
            (r"Householder: \ mirrors, \ not $X^\top X$", OLS_C), (r"influence and the jackknife", PATH),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.4),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 23, \ in fourteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part twenty-three in fourteen lines. <bookmark mark='a'/> Longley's data defeated the normal equations: "
            "no correct digits in single precision, against twelve for QR in double. Part 12's guarantees rested on a"
            " true linear mean, equal independent errors, exact predictors and exact arithmetic. Every linear "
            "question is C beta equals d, with one F-test. Generalized least squares whitens and then fits. With "
            "autocorrelated errors, the naive standard error covered forty-eight percent. HC estimators address "
            "uneven noise under regularity conditions; the wild bootstrap performed better in our small-sample "
            "experiment. Clustering greatly inflated uncertainty, approximately as the Moulton heuristic suggested. "
            "The Board assesses eight-school bootstrap inference conditionally on observing both treatment arms. A "
            "wrong line still estimates the best linear predictor, whose value depends on who is sampled. Classical "
            "error in a single regressor attenuates its slope, and Hubble's data give three different answers. "
            "Quantile regression shows the whole fan of a distribution; B-splines make curves into linear models. "
            "Householder's mirrors avoid ever forming X transpose X. And the deletion formula measures influence and "
            "gives the jackknife for free."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=38.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"GLMs, \ GEE and working correlations", [24]), (r"mixed models: \ the clusters, \ modelled", [25]),
            (r"smoothing: \ penalized splines", [29]), (r"robust regression; \ influence functions", [30]),
            (r"the lasso when $p > n$", [32]), (r"difference-in-differences with few clusters", [37]),
            (r"measurement error in full", [41]), (r"interpolation and double descent", [59]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 24's generalized estimating equations put chapter five's "
            "clusters into generalized linear models. Part 25 models the clusters instead of correcting for them. Part 29 "
            "penalizes splines rather than choosing knots. Part 30 builds robust regression and influence functions. Part "
            "32 fits linear models with more predictors than observations. Part 37 runs difference-in-differences with few "
            "clusters. Part 41 treats measurement error in full. And Part 59 returns to the minimum-norm solution, when "
            "least squares interpolates."
        ) as vo:
            self.add(card.head)
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The two forms of the F statistic; "
            "Moulton's factor; attenuation, and what it does to the intercept; why HC two is unbiased under equal "
            "variances; the deletion formula; and the best linear predictor of x squared. Pause here if you want to try "
            "them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"S. Weisberg, \emph{Applied Linear Regression} (4th ed., 2014)",
             r"A. C. Cameron \& P. K. Trivedi, \emph{Microeconometrics} (2005)",
             r"R. Koenker, \emph{Quantile Regression} (2005)",
             r"G. Golub \& C. Van Loan, \emph{Matrix Computations} (4th ed., 2013)"],
            [r"J. Longley (1967); \ A. Aitken (1935); \ U. Grenander \& M. Rosenblatt (1957); \ S. Prais \& C. Winsten (1954)",
             r"F. Eicker (1963); \ H. White (1980); \ J. MacKinnon \& H. White (1985); \ B. Moulton (1986)",
             r"K.-Y. Liang \& S. Zeger (1986); \ A. C. Cameron, \ J. Gelbach \& D. Miller (2008); \ M. Webb (2014)",
             r"A. Buja et al.\ (2019); \ E. Hubble (1929); \ R. Koenker \& G. Bassett (1978); \ A. Householder (1958)"])
        with self.voiceover(
            "The books this part follows: Weisberg's Applied Linear Regression, Cameron and Trivedi's Microeconometrics, "
            "Koenker's Quantile Regression, and Golub and Van Loan's Matrix Computations; with the papers from Aitken and "
            "Hubble to Buja and his colleagues."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=23, current=None)
        nxt = VGroup(label(r"Part 24", font_size=30, color=GREY_B), label(r"Generalized Linear Models", font_size=48),
                     label(r"counts, \ yes-or-no and other outcomes that are not normal", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Twenty-three parts of sixty-five. <bookmark mark='a'/> The linear model now has uncertainty methods for "
            "uneven noise, clustering and approximation error, with explicit conditions and finite-sample checks. "
            "<bookmark mark='b'/> Next, outcomes that are not normal at all: counts, proportions, yes-or-no answers. "
            "In 1972 John Nelder and Robert Wedderburn showed that one algorithm fits them all. Part 24: generalized "
            "linear models."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(23)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
