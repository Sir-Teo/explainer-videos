from __future__ import annotations

from videos.stats.stats7.common import *  # noqa: F403

PROBLEMS = [
    r"Show that $x \mapsto (5x + 3) \bmod 16$ has full period, \ and find the period of $x \mapsto 5x \bmod 16$ started at 1.",
    r"Derive inverse-CDF samplers for the Pareto ($P(X > x) = (x_m/x)^\alpha$) and the logistic ($F(x) = 1/(1 + e^{-x})$).",
    r"Rejection from a uniform box for $f(x) = 6x(1 - x)$ on $[0, 1]$: \ find $M$, \ the acceptance rate, \ and the mean number "
    r"of darts per draw.",
    r"Estimate $\int_0^1 \sqrt{1 - x^2}\,dx$ by Monte Carlo. \ Find the estimator's variance, \ and the $n$ that gives a "
    r"standard error of $0.001$.",
    r"For $P = \begin{pmatrix} 1 - a & a \\ b & 1 - b \end{pmatrix}$, \ find the stationary law and the second eigenvalue.",
    r"Show that Metropolis with a symmetric proposal satisfies detailed balance for an \emph{unnormalized} $f$.",
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
            (r"a state of sin: \ RANDU's fifteen planes", BAD),
            (r"LCGs, \ periods, \ lattices; \ PCG; \ testing", GOOD),
            (r"the inverse CDF, \ continuous and discrete", EXACT),
            (r"rejection: \ darts under a curve, \ rate $1/M$", ACC),
            (r"Box--Muller, \ Marsaglia--Tsang, \ the alias table", S.POST),
            (r"Monte Carlo: \ $\sigma/\sqrt n$ in any dimension", GOOD),
            (r"Buffon's needle, \ and Lazzarini's", S.MUSEUM),
            (r"ADEMP, \ Monte Carlo SEs, \ seeds and streams", S.ACCENT),
            (r"antithetic, \ control variates, \ importance", S.POST),
            (r"Markov chains: \ mass flowing to $\pi$", CHAIN),
            (r"detailed balance; \ random walks; \ PageRank", CHAIN),
            (r"seven shuffles: \ the cutoff", S.EST),
            (r"Metropolis: \ detailed balance by design", CHAIN),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=30, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.44),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.44)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 7, \ in thirteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part seven in thirteen lines. <bookmark mark='a'/> Arithmetic randomness is a state of sin, and RANDU's "
            "triples fell on fifteen planes. Linear congruential generators have periods and lattices; PCG hides "
            "them, and statistical tests can catch what remains. The inverse CDF turns one uniform into any "
            "distribution with a usable inverse. Rejection keeps the darts under a curve, at a rate of one over M. "
            "Box and Muller make normals from polar coordinates, Marsaglia and Tsang make gammas, and Walker's alias "
            "table makes discrete draws in constant time. Monte Carlo integration has error sigma over root n in any "
            "dimension; Buffon's needle estimates pi, and Lazzarini's needle teaches honesty. Simulation studies need "
            "a protocol, Monte Carlo standard errors and controlled seeds. Antithetic pairs, control variates and "
            "importance sampling make each draw count for more. A Markov chain moves probability like a fluid "
            "toward its stationary law; detailed balance builds chains, random walks favour hubs, and PageRank "
            "ranks the web. Seven riffle shuffles mix a deck, with a cutoff. And Metropolis builds a chain with any "
            "stationary law we like."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=26.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"statkit.random, the simulation harness", [8, 11, 16, 33]),
            (r"Monte Carlo error, simulation studies", [11, 16, 28, 59]),
            (r"importance sampling", [27, 28]),
            (r"Markov chains, stationary laws", [17, 27, 44]),
            (r"mixing, convergence diagnostics", [27, 53]),
            (r"Metropolis, MCMC", [15, 26, 27]),
            (r"random walks on graphs", [39, 44]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> statkit's generator and harness run every simulation from here "
            "on: sampling distributions in Part 8, coverage in Part 11, the bootstrap in Part 16, thousands of tests "
            "in Part 33. Importance sampling returns in Bayesian computation and model comparison. Markov chains "
            "return in time series and, with full rigour, in Part 44. And Metropolis grows into the whole of "
            "Bayesian computation in Part 27."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3),
                      run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Periods of two small generators; "
            "inverse-CDF samplers for the Pareto and the logistic; a rejection sampler's efficiency; the cost of a "
            "Monte Carlo integral; a two-state chain; and the proof that Metropolis works. Pause here if you want to "
            "try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"D. Knuth, \emph{The Art of Computer Programming}, vol.~2: \emph{Seminumerical Algorithms} (3rd ed., 1997), ch.~3",
             r"L. Devroye, \emph{Non-Uniform Random Variate Generation} (1986); \ C. Robert \& G. Casella, \emph{Monte Carlo "
             r"Statistical Methods} (2nd ed., 2004)",
             r"A. Owen, \emph{Monte Carlo Theory, Methods and Examples} (2013--); \ D. Levin \& Y. Peres, \emph{Markov Chains and "
             r"Mixing Times} (2nd ed., 2017)"],
            [r"J. von Neumann (1951); \ D. H. Lehmer (1949); \ T. Hull \& A. Dobell (1962); \ G. Marsaglia (1968); \ M. O'Neill (2014)",
             r"G. Box \& M. Muller (1958); \ G. Marsaglia \& W. W. Tsang (2000); \ A. Walker (1974); \ M. Vose (1991)",
             r"G. Buffon (1777); \ T. Morris, I. White \& M. Crowther (2019); \ P. L'Ecuyer \& R. Simard (2007)",
             r"A. Markov (1906, 1913); \ S. Brin \& L. Page (1998); \ D. Bayer \& P. Diaconis (1992)",
             r"N. Metropolis, A. \& M. Rosenbluth, A. \& E. Teller (1953); \ W. K. Hastings (1970)"])
        with self.voiceover(
            "The books and papers this part follows: Knuth's second volume, Devroye's encyclopedia of samplers, Robert "
            "and Casella, Owen on Monte Carlo, and Levin and Peres on mixing, with the original papers from von "
            "Neumann to Bayer and Diaconis."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=7, current=None)
        nxt = VGroup(label(r"Part 8", font_size=30, color=GREY_B), label(r"From Sample to Population", font_size=48),
                     label(r"how much does a statistic vary from sample to sample, \ and why $n - 1$?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Seven parts of sixty-five. <bookmark mark='a'/> We can now make randomness, shape it into any "
            "distribution, and use it to test methods honestly. <bookmark mark='b'/> Next, we turn the machine on "
            "statistics themselves: draw sample after sample from the World, compute a mean, a variance, a t "
            "statistic each time, and watch how they vary. That variation has exact laws, discovered by a brewer at "
            "Guinness in 1908. Part 8: from sample to population."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(7)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
