from __future__ import annotations

from videos.stats.stats6.common import *  # noqa: F403

PROBLEMS = [
    r"$X \ge 0$ with $E X = 1$. \ Show $P(X \ge 3) \le 1/3$, \ and find a distribution for which equality holds.",
    r"A poll of $n$ voters estimates a share $p$. \ How large must $n$ be for $P(|\hat p - p| \ge 0.03) \le 0.05$, \ by Chebyshev "
    r"(use $p(1-p) \le 1/4$), \ by Hoeffding, \ and by the normal approximation?",
    r"Use moment generating functions to show that $\mathrm{Binomial}(n, \lambda/n) \to \mathrm{Poisson}(\lambda)$ in distribution.",
    r"$X_1, \dots, X_n$ are i.i.d.\ exponential with rate $\lambda$. \ Find the limiting distribution of $\sqrt n\,(1/\bar X_n - \lambda)$.",
    r"$U_1, \dots, U_n$ are i.i.d.\ uniform on $(0, 1)$. \ Show $n\,(1 - \max_i U_i) \to \mathrm{Exp}(1)$ in distribution.",
    r"Show that $\sqrt n(\bar X_n - \mu)/S_n \to N(0, 1)$ needs only a finite variance, \ naming each theorem you use.",
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
            (r"Galton's ox: \ the crowd within 1\%", DATA),
            (r"Markov, \ Chebyshev (tight), \ Jensen", BOUND),
            (r"the weak law: \ the funnel narrows like $1/\sqrt n$", SIM),
            (r"in probability, \ in distribution, \ almost surely", S.PRIOR),
            (r"the CLT, seen: \ cumulants die away", EXACT),
            (r"the CLT, proved: \ $n \log M(t/\sqrt n) \to t^2/2$", EXACT),
            (r"de Moivre--Laplace; \ the continuity correction", S.MUSEUM),
            (r"thirty is not enough for skewed data", WORLD),
            (r"the delta method; \ variance stabilizing", S.POST),
            (r"Slutsky: \ the $t$ statistic without normality", S.ACCENT),
            (r"Cauchy and stable laws: \ averaging can fail", BOUND),
            (r"Hoeffding: \ exponential, \ for every $n$", S.PRIOR),
            (r"maxima: \ Gumbel, \ Fr\'echet, \ Weibull; \ return levels", S.LIK),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=30, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.44),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.44)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 6, \ in thirteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part six in thirteen lines. <bookmark mark='a'/> Galton's crowd guessed the ox within one percent. "
            "Markov's inequality needs only a mean, Chebyshev's a variance, and Chebyshev's can't be improved; "
            "Jensen's says the mean of a convex function exceeds the function of the mean. The weak law follows in "
            "three lines, and the funnel narrows like one over root n. Random things converge in probability, in "
            "distribution, or almost surely, and the differences matter. The central limit theorem appears as the "
            "higher cumulants die away, and it's proved by expanding the log-MGF. De Moivre found it for coins, and "
            "the continuity correction makes it accurate. For skewed data, thirty observations are not enough. The "
            "delta method pushes the theorem through smooth functions, and Slutsky's theorem frees the t statistic "
            "from normality. Cauchy averages never settle, and stable laws take over when variances are infinite. "
            "Hoeffding's inequality gives exponential guarantees at every sample size. And maxima have their own "
            "three laws, which predict floods."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=26.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the weak law, consistency", [9, 22, 47]),
            (r"the central limit theorem", [8, 10, 11, 43]),
            (r"Berry--Esseen, the speed of the CLT", [16, 47]),
            (r"the delta method", [9, 14, 18, 22]),
            (r"Slutsky and continuous mapping", [9, 10, 47]),
            (r"Hoeffding and concentration", [51, 54, 58]),
            (r"heavy tails, stable laws", [30, 60]),
            (r"extreme values, return levels", [22, 39, 40]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Consistency is the first property we ask of every estimator, "
            "from Part 9 on. The central limit theorem stands behind every interval and test in the next fifteen "
            "parts, and Part 43 proves it in full. Its speed returns with the bootstrap. The delta method gives the "
            "standard errors of almost every estimator you'll meet. Slutsky's theorem is used every time a nuisance "
            "parameter is estimated. Concentration inequalities are the language of high-dimensional statistics and "
            "learning theory. And heavy tails and extremes return with robust statistics and with spatial and "
            "survival models."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3),
                      run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Markov's inequality, made tight; "
            "a poll's sample size three ways; the Poisson limit by moment generating functions; the delta method for "
            "an exponential rate; the maximum of uniforms; and the t statistic, theorem by theorem. Pause here if "
            "you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"J. Blitzstein \& J. Hwang, \emph{Introduction to Probability} (2nd ed., 2019), chs.~10--11",
             r"G. Grimmett \& D. Stirzaker, \emph{Probability and Random Processes} (4th ed., 2020), ch.~7",
             r"A. W. van der Vaart, \emph{Asymptotic Statistics} (1998), chs.~2--3; \ R. Vershynin, \emph{High-Dimensional Probability} (2018)",
             r"S. Coles, \emph{An Introduction to Statistical Modeling of Extreme Values} (2001); \ E. J. Gumbel (1958)"],
            [r"J. Bernoulli (1713); \ A. de Moivre (1733); \ P.-S. Laplace (1810, 1812); \ P. Chebyshev (1867)",
             r"A. Lyapunov (1901); \ J. W. Lindeberg (1922); \ W. Feller (1935); \ G. P\'olya (1920); \ J. Curtiss (1942)",
             r"A. Berry (1941); \ C.-G. Esseen (1942); \ I. Shevtsova (2011); \ E. Slutsky (1925); \ H. Mann \& A. Wald (1943)",
             r"H. Chernoff (1952); \ W. Hoeffding (1963); \ H. Cram\'er (1938); \ P. L\'evy (1925); \ B. Mandelbrot (1963)",
             r"F. Galton (1907); \ R. A. Fisher \& L. Tippett (1928); \ B. Gnedenko (1943); \ D. van Dantzig (1956)"])
        with self.voiceover(
            "The books and papers this part follows: Blitzstein and Hwang, Grimmett and Stirzaker, van der Vaart's "
            "Asymptotic Statistics, Vershynin on concentration, and Coles on extremes, along with the original "
            "papers from Bernoulli to van Dantzig."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=6, current=None)
        nxt = VGroup(label(r"Part 7", font_size=30, color=GREY_B), label(r"Randomness on Demand", font_size=48),
                     label(r"where do the random numbers in every simulation come from?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Six parts of sixty-five. <bookmark mark='a'/> We now know why averages work, how fast, and when they "
            "don't. But every check in this part leaned on simulation: millions of random draws, from coins, normals, "
            "Cauchys and Paretos. <bookmark mark='b'/> Where do those random numbers come from, on a machine that "
            "can only follow instructions? John von Neumann said that anyone who considers arithmetical methods of "
            "producing random digits is in a state of sin. Part 7 commits that sin, carefully."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(6)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
