from __future__ import annotations

from videos.stats.stats26.common import *  # noqa: F403

PROBLEMS = [
    r"Eight schools: \ show $p(\tau \mid y) \propto p(\tau)\, V_\mu^{1/2} \prod_j (\sigma_j^2 + \tau^2)^{-1/2} \exp\{-(y_j - \hat\mu)^2/2(\sigma_j^2 + \tau^2)\}$.",
    r"Show that Jeffreys's prior is invariant: \ if $\eta = g(\theta)$, \ $\sqrt{I(\eta)} = \sqrt{I(\theta)}\,|d\theta/d\eta|$.",
    r"Poisson--gamma: \ show the posterior mean is $\tfrac{b}{b + n}\tfrac{a}{b} + \tfrac{n}{b + n}\bar x$.",
    r"Derive $BF_{01}$ for $\bar y \sim N(\mu, \sigma^2/n)$, \ $H_0: \mu = 0$ vs $\mu \sim N(0, \tau^2)$; \ its limit as $\tau \to \infty$?",
    r"Show that the posterior median minimizes expected absolute loss.",
    r"CRP: \ show $E K_n = \sum_{i=0}^{n-1} \alpha/(\alpha + i)$.",
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
            (r"eight schools: \ neither 28 nor 7.7", PATH), (r"exchangeability motivates sharing; \ normality is a choice", PRIOR),
            (r"$p(\tau \mid y)$ on a grid; \ A: \ 10 [$-2$, 31]", SHRUNK), (r"Jeffreys, \ reference, \ half-Cauchy", PRIOR),
            (r"conjugacy: \ priors as pseudo-data", SHRUNK), (r"BvM: \ TV 0.08 $\to$ 0.008", HIT),
            (r"Bayes factors: \ Bartlett's warning", RES), (r"PEAR: \ $p = 0.0003$, \ BF 12 for $H_0$", RES),
            (r"Occam: \ evidence peaks at the simulated degree here", SHRUNK), (r"decisions; \ EVPI 2.20, \ EVSI 1.23", POST),
            (r"checks: \ Poisson fails, \ NB passes", HIT), (r"workflow; \ SBC catches two bugs", HIT),
            (r"coherence, \ and calibrated Bayes", PATH), (r"the Dirichlet process", SHRUNK),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.4),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 26, \ in fourteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part twenty-six in fourteen lines. <bookmark mark='a'/> The eight schools' coaching effects were neither"
            " each school's own estimate nor one pooled number. Infinite exchangeability motivates a mixture "
            "representation; a normal population and its hyperprior remain additional choices. A checked wide-grid "
            "approximation to tau's posterior gave independent conditional draws, and school A's twenty-eight became "
            "ten, with an interval from minus two to about thirty-two. Jeffreys's rule, reference priors and weakly "
            "informative half-Cauchys replaced priors by habit. Conjugate priors act as pseudo-data. Bernstein–von "
            "Mises made posteriors and sampling distributions agree as data grew. Bayes factors compare predictions, "
            "and depend on the alternative's prior, as Bartlett warned. The PEAR data were significant at three in "
            "ten thousand, and favoured the null twelve to one. The evidence carries Occam's razor. Decisions "
            "maximize expected utility, and information has a price. Checks flagged the Poisson zero fraction; the "
            "negative binomial reproduced that chosen feature. Simulation-based calibration caught two bugs. "
            "Coherence is the Bayesian's case, and calibrated Bayes the working truce. And the Dirichlet process puts"
            " a prior on distributions themselves."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=40.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"computing high-dimensional posteriors: \ MCMC, \ HMC, \ the funnel", [27]), (r"choosing models: \ LOO, \ WAIC, \ BIC", [28]),
            (r"priors for sparsity: \ the horseshoe", [32]), (r"empirical Bayes for many tests", [33]),
            (r"decisions in experiments", [35]), (r"Gaussian processes", [39]),
            (r"decision theory and admissibility", [45]), (r"BvM proved; \ Bayesian nonparametrics", [53]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 27 computes posteriors no grid can reach, with Markov chains and "
            "Hamiltonian dynamics, and returns to the eight schools in the shape of Neal's funnel. Part 28 chooses among "
            "models by cross-validation and information criteria. Part 32's horseshoe is a prior built for sparsity. Part 33 "
            "applies empirical Bayes to thousands of tests at once. Part 35 makes decisions about experiments. Part 39 puts "
            "Gaussian process priors on functions. Part 45 builds decision theory properly. And Part 53 proves "
            "Bernstein–von Mises and develops Bayesian nonparametrics."
        ) as vo:
            self.add(card.head)
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The marginal posterior of tau; the "
            "invariance of Jeffreys's prior; the Poisson–gamma posterior mean as a weighted average; the normal Bayes factor "
            "and its limit; why the median minimizes absolute loss; and the expected number of tables in the Chinese "
            "restaurant. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"A. Gelman, J. Carlin, H. Stern, D. Dunson, A. Vehtari \& D. Rubin, \emph{Bayesian Data Analysis} (3rd ed., 2013)",
             r"R. McElreath, \emph{Statistical Rethinking} (2nd ed., 2020)",
             r"C. Robert, \emph{The Bayesian Choice} (2nd ed., 2007)",
             r"S. B. McGrayne, \emph{The Theory That Would Not Die} (2011)"],
            [r"D. Rubin (1981, 1984); \ B. de Finetti (1931, 1937); \ H. Jeffreys (1939, 1946); \ J. Bernardo (1979)",
             r"A. Gelman (2006); \ P. Diaconis \& D. Ylvisaker (1979); \ R. Kass \& A. Raftery (1995); \ D. Lindley (1957)",
             r"W. Jefferys (1990); \ T. Sellke, M. J. Bayarri \& J. Berger (2001); \ D. MacKay (1992); \ L. Savage (1954)",
             r"A. Gelman, X.-L. Meng \& H. Stern (1996); \ S. Talts et al.\ (2018); \ A. Gelman et al.\ (2020); \ T. Ferguson (1973)"])
        with self.voiceover(
            "The books this part follows: Gelman and colleagues' Bayesian Data Analysis, McElreath's Statistical Rethinking, "
            "Robert's The Bayesian Choice, and McGrayne's history; with the papers from de Finetti to the Bayesian workflow."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=26, current=None)
        nxt = VGroup(label(r"Part 27", font_size=30, color=GREY_B), label(r"Bayesian Computation", font_size=48),
                     label(r"importance sampling, \ Metropolis, \ Gibbs, \ Hamiltonian Monte Carlo", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Twenty-six parts of sixty-five. <bookmark mark='a'/> We can now build, fit on a grid, check and defend a "
            "Bayesian model. <bookmark mark='b'/> But a grid works in one dimension, not a hundred. In 1953, at Los Alamos, "
            "Nicholas Metropolis and colleagues computed the physics of hard disks with a random walk, and that walk became "
            "the engine of Bayesian statistics. Part 27: Bayesian computation."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(26)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
