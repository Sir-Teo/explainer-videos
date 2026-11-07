from __future__ import annotations

from videos.stats.stats37.common import *  # noqa: F403

PROBLEMS = [
    r"With a binary instrument, \ show that 2SLS equals the Wald ratio $\frac{E[Y|Z=1]-E[Y|Z=0]}{E[D|Z=1]-E[D|Z=0]}$.",
    r"Show that under $H_0: \beta = b_0$ the Anderson--Rubin statistic's distribution does not depend on the first stage.",
    r"Local linear RD: \ bias $\approx B h^2$, \ variance $\approx V/(nh)$. \ Find $h_{\text{MSE}}$, \ and show bias/SD $= \frac12$ there.",
    r"Show that with two groups and two periods, \ the TWFE coefficient equals the difference in differences.",
    r"For $y_{it} = \rho y_{i,t-1} + \alpha_i + \varepsilon_{it}$ with two usable periods, \ show FE converges to $\rho - (1+\rho)/2$.",
    r"Derive Manski's bounds on $E[Y(1)] - E[Y(0)]$ for $Y \in [0,1]$ with response rates $r_1, r_0$; \ show the width is $2 - r_1 - r_0$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.upgrade()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"Snow: \ two companies, \ one street, \ 315 vs 37", Y1C), (r"design before regression", TAUC),
            (r"instruments: \ the Wald ratio, \ 2SLS", IVC), (r"weak instruments: \ $F$, \ $tF$, \ Anderson--Rubin", IVC),
            (r"many instruments; \ LIML; \ Mendelian randomization", IVC), (r"RD: \ local fits, \ robust bias correction", CUTC),
            (r"RD checks: \ density, \ covariates; \ fuzzy RD", CUTC), (r"DiD: \ parallel trends; \ Card--Krueger", Y0C),
            (r"DiD inference: \ cluster; \ placebo laws", Y0C), (r"staggered adoption: \ TWFE's sign; \ CS, \ imputation", MISSC),
            (r"honest trends; \ synthetic control; \ SDID", BANDC), (r"fixed effects; \ Nickell; \ Manski and Lee bounds", GREY_A),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.45),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 37, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part thirty-seven in twelve lines. <bookmark mark='a'/> Snow's two water companies ran down the same "
            "streets, and the contaminated-water group had about eight times as many deaths per house. The "
            "credibility revolution put the design before the regression. An instrument identifies an effect by a "
            "Wald ratio, or two-stage least squares, if it reaches the outcome only through the treatment. Weak "
            "instruments make the usual interval unreliable, and the Anderson-Rubin set is valid regardless of "
            "strength under its stated linear-IV and error-distribution assumptions. Many instruments drag two-stage "
            "least squares back to ordinary least squares, while limited-information maximum likelihood resists, and "
            "genes can serve as instruments if they act through one path. Regression discontinuities compare people "
            "at a cutoff, with local fits and robust bias correction, and must be checked for sorting. "
            "Differences-in-differences assume parallel trends, and need standard errors clustered by the unit of "
            "treatment. With staggered adoption, two-way fixed effects can get the sign wrong, and estimators such as"
            " Callaway and Sant'Anna or imputation target explicit effects under their own identification conditions."
            " Honest parallel trends carry doubt about the trends into the interval; synthetic controls and synthetic"
            " DiD build the comparison. Fixed effects remove what is fixed, and dynamic panels need instruments. And "
            "bounds show what the data say before the assumptions speak."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=40.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(37, r"causal effects from natural experiments: \ instruments, \ cutoffs, \ trends",
                            r"that each design's untestable assumption holds, \ and panels with short memories",
                            r"Part 38: \ time series in depth: \ long memory, \ unit roots, \ volatility, \ hidden states")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for later. This part estimated causal effects from natural experiments. "
            "<bookmark mark='b'/> It assumed that each design's key assumption held, and it met serial correlation only as "
            "a nuisance for standard errors. <bookmark mark='c'/> Part thirty-eight takes time seriously: long memory, unit "
            "roots, volatility that moves, and states that can only be inferred."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card[0]), FadeIn(card[1][0]), FadeIn(card[1][1][0]))
            vo.wait_until("b")
            self.play(FadeIn(card[1][1][1]))
            vo.wait_until("c")
            self.play(FadeIn(card[1][1][2]))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"unit roots and persistence", [38]), (r"spillovers across space", [39]),
            (r"selection and measurement error", [41]), (r"weak-instrument asymptotics", [47]),
            (r"influence functions for DiD and IV", [49]), (r"many instruments, \ high dimensions", [52]),
            (r"permutation inference, \ distribution-free", [57]), (r"external validity, \ distribution shift", [60]),
            (r"sensitivity, \ partial identification, \ surrogates", [62]),
        ], font_size=22)
        self.add(card.head)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 38 studies the persistence that made placebo laws so dangerous. "
            "Part 39 handles spillovers across space. Part 41 returns to selection, with Heckman's model, and to "
            "measurement error. Part 47 derives weak-instrument asymptotics. Part 49 finds the influence functions behind "
            "these estimators. Part 52 treats many instruments as a high-dimensional problem. Part 57 makes permutation "
            "inference rigorous. Part 60 asks when an effect found in one place holds in another. And Part 62 takes "
            "partial identification and sensitivity to the frontier."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The Wald ratio as two-stage least "
            "squares; why the Anderson-Rubin test is immune to weak instruments; the optimal bandwidth and its built-in bias; "
            "two-way fixed effects in the two-by-two case; Nickell's bias with two periods; and Manski's bounds. Pause here "
            "if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"J. Angrist \& J.-S. Pischke, \emph{Mostly Harmless Econometrics} (2009)",
             r"S. Cunningham, \emph{Causal Inference: The Mixtape} (2021); \ N. Huntington-Klein, \emph{The Effect} (2022)",
             r"M. Cattaneo, N. Idrobo \& R. Titiunik, \emph{A Practical Introduction to Regression Discontinuity Designs} (2020)",
             r"C. Manski, \emph{Partial Identification of Probability Distributions} (2003)"],
            [r"J. Snow (1855); \ P. Wright (1928); \ T. Anderson \& H. Rubin (1949); \ D. Thistlethwaite \& D. Campbell (1960)",
             r"J. Angrist \& A. Krueger (1991); \ J. Bound, D. Jaeger \& R. Baker (1995); \ D. Lee, J. McCrary, M. Moreira \& J. Porter (2022)",
             r"D. Card \& A. Krueger (1994); \ M. Bertrand, E. Duflo \& S. Mullainathan (2004); \ A. Goodman-Bacon (2021)",
             r"A. Abadie et al. (2010); \ D. Arkhangelsky et al. (2021); \ A. Rambachan \& J. Roth (2023); \ D. Lee (2009)"])
        with self.voiceover(
            "The books this part follows: Angrist and Pischke's Mostly Harmless Econometrics; Scott Cunningham's Mixtape "
            "and Nick Huntington-Klein's The Effect; Cattaneo, Idrobo and Titiunik on regression discontinuity; and Manski "
            "on partial identification; with the papers from Snow to Rambachan and Roth."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=37, current=None)
        nxt = VGroup(label(r"Part 38", font_size=30, color=GREY_B), label(r"Time Series in Depth", font_size=48),
                     label(r"long memory, \ unit roots, \ volatility, \ and the hidden state", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Thirty-seven parts of sixty-five. <bookmark mark='a'/> When the world runs an experiment by accident, we can "
            "read it, if we check the design as carefully as the estimate. <bookmark mark='b'/> Next, Harold Hurst measures "
            "the Nile, and finds a memory that lasts for centuries. Part 38: time series in depth."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(37)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
