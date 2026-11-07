from __future__ import annotations

from videos.stats.stats11.common import *  # noqa: F403

PROBLEMS = [
    r"Find the 95\% Wilson interval for 0 successes in 20 trials, \ and compare it with Wald's.",
    r"Show that $\lambda\sum X_i \sim \mathrm{Gamma}(n, 1)$ for exponential data, \ and give the 95\% interval for $\lambda$ when $n = 5$, "
    r"\ $\sum x_i = 10$.",
    r"No adverse events in 200 patients: \ give the one-sided 95\% upper limit exactly, \ and by the rule of three.",
    r"Ten men: \ $\bar x = 176$, \ $s = 7$. \ Give the 95\% confidence interval for $\mu$ and the 95\% prediction interval for the next man.",
    r"$\bar x = 4$, \ $\bar y = 8$, \ independent, \ each with SE 1: \ find Fieller's 95\% set for $\mu_y/\mu_x$, \ and the delta-method interval.",
    r"Welch's example: \ for $X_1, X_2 \sim U(\theta - \tfrac12, \theta + \tfrac12)$, \ show $P(|X_1 - X_2| \ge \tfrac12) = \tfrac14$, \ "
    r"and that the coverage given $|X_1 - X_2| < \tfrac12$ is $\tfrac13$.",
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
            (r"the Wald sawtooth: \ 591 vs 592", MISS),
            (r"Neyman: \ $\ge 1 - \alpha$ for every $\theta$", OBS),
            (r"the 95\% belongs to the procedure", OBS),
            (r"pivots: \ $t$, \ $\chi^2$, \ $F$, \ gamma, \ beta", S.LIK),
            (r"invert a test: \ Neyman's belt", S.LIK),
            (r"Wilson, \ Agresti--Coull, \ Clopper--Pearson, \ Jeffreys", METHOD_COL["wilson"]),
            (r"likelihood intervals; \ the rule of three", METHOD_COL["lr"]),
            (r"discreteness: \ guarantee or average", GREY_A),
            (r"Fieller: \ sometimes the whole line", S.POST),
            (r"simultaneous: \ Bonferroni, \ Scheff\'e, \ DKW", S.POST),
            (r"prediction is not confidence", HIT),
            (r"credible vs confidence; \ Welch 1939", METHOD_COL["jeffreys"]),
            (r"the Board's protocol", S.KEPT),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=27, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 11, \ in thirteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part eleven in thirteen lines. <bookmark mark='a'/> The textbook interval for a proportion fails in a "
            "sawtooth, ninety-four and a half percent at one sample size, seventy-nine at the next. Neyman's promise is "
            "coverage of at least one minus alpha for every parameter value, and the ninety-five percent belongs to the "
            "procedure, not to the interval in hand. Pivots give exact intervals; inverting tests gives confidence sets for "
            "almost anything, through Neyman's belt. For proportions, use Wilson, Agresti–Coull, Clopper–Pearson or "
            "Jeffreys; likelihood intervals follow the likelihood's shape, and after zero events the rule of three "
            "applies. Discrete data force a choice between a guarantee and an average. Fieller's ratio sets can be the "
            "whole line, and must be. Several promises at once need Bonferroni, Scheffé or the DKW band. Prediction is not "
            "confidence. Credible and confidence intervals agree under regular large-sample conditions and part company in Welch's example. "
            "And the Coverage Board's protocol is now written down."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=28.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"intervals by inverting tests", [12, 14, 46]),
            (r"likelihood and profile intervals", [14, 22]),
            (r"bootstrap intervals", [16, 47]),
            (r"simultaneous bands", [12, 29, 48]),
            (r"prediction, conformal", [19, 34, 57]),
            (r"credible intervals", [15, 26, 53]),
            (r"Fieller, weak identification", [37, 46]),
            (r"the Coverage Board", [12, 14, 16, 65]),
        ], font_size=22)
        intro = label('Where interval construction returns', font_size=36)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Inverted tests give the intervals of regression in Part 12 and of "
            "generalized linear models in Part 14. Profile likelihood intervals return in Part 22, bootstrap intervals in "
            "Part 16, and simultaneous bands for regression lines and curves in Parts 12 and 29. Wilks' order statistics "
            "grow into conformal prediction in Part 34; credible intervals into Bayesian data analysis; and Fieller's "
            "unbounded sets into the weak-instrument problem of Part 37."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Wilson after zero successes; the "
            "exponential pivot; the rule of three; confidence versus prediction; a Fieller set; and the arithmetic of "
            "Welch's example. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"G. Casella \& R. Berger, \emph{Statistical Inference} (2nd ed., 2002), ch.~9",
             r"E. Lehmann \& J. Romano, \emph{Testing Statistical Hypotheses} (4th ed., 2022), chs.~3, 5",
             r"A. Agresti, \emph{Categorical Data Analysis} (3rd ed., 2013), ch.~1; \ G. Hahn \& W. Meeker, \emph{Statistical Intervals} (2nd ed., 2017)",
             r"L. Wasserman, \emph{All of Statistics} (2004), chs.~6--7"],
            [r"J. Neyman (1937); \ E. B. Wilson (1927); \ C. Clopper \& E. S. Pearson (1934); \ A. Agresti \& B. Coull (1998)",
             r"L. Brown, T. Cai \& A. DasGupta (2001); \ E. Fieller (1954); \ L. Gleser \& J. T. Hwang (1987)",
             r"H. Scheff\'e (1953); \ A. Dvoretzky, J. Kiefer \& J. Wolfowitz (1956); \ P. Massart (1990); \ S. Wilks (1941)",
             r"B. L. Welch (1939); \ W. Stevens (1950); \ H. Lancaster (1961); \ J. Hanley \& A. Lippman-Hand (1983)"])
        with self.voiceover(
            "The books and papers this part follows: Casella and Berger, Lehmann and Romano, Agresti on categorical data, "
            "Hahn and Meeker's Statistical Intervals, and Wasserman, with the papers from Wilson in 1927 to Brown, Cai and "
            "DasGupta in 2001."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=11, current=None)
        nxt = VGroup(label(r"Part 12", font_size=30, color=GREY_B), label(r"Least Squares", font_size=48),
                     label(r"Legendre and Gauss find Ceres; \ a line, \ a plane, \ a projection", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Eleven parts of sixty-five, and the start of Stage II: methods. <bookmark mark='a'/> We can estimate, test "
            "and give honest intervals for one quantity at a time. <bookmark mark='b'/> But most questions are about "
            "relationships: how one variable changes with another. In 1801 a new planet, Ceres, was lost behind the sun, "
            "and the young Gauss found it again with a method he had invented for fitting orbits to noisy observations. "
            "Part 12: least squares."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(11)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
