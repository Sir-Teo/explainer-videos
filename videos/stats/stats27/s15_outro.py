from __future__ import annotations

from videos.stats.stats27.common import *  # noqa: F403

PROBLEMS = [
    r"Show that the Metropolis--Hastings kernel satisfies detailed balance with respect to $\pi$.",
    r"Show that the self-normalized importance estimator is consistent, \ and that $\mathrm{ESS} = n$ when $q = \pi$.",
    r"Gibbs for $N_2(0, [[1, \rho], [\rho, 1]])$: \ show $x_1^{(t+1)}$ is AR(1) with coefficient $\rho^2$; \ find its ESS.",
    r"Show that a leapfrog step preserves volume and is reversible (negate $p$, \ step, \ negate again).",
    r"Show that $\log p(y) = \text{ELBO}(q) + \mathrm{KL}(q \,\|\, p(\theta \mid y))$.",
    r"Show that if $\tau = e^u$ and $\tau \sim p$, \ then $u$ has density $p(e^u)\, e^u$.",
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
            (r"hard disks: \ a random walk integrates", PATH), (r"importance: \ $\hat k$ 0.93 says no", RES),
            (r"Metropolis--Hastings; \ accept 0.234", SAMPLER), (r"Gibbs and data augmentation", SAMPLER),
            (r"$\hat R$ 1.53 for stuck chains", RES), (r"HMC: \ 140 times the random walk", HIT),
            (r"NUTS: \ stop at the U-turn", HIT), (r"the funnel: \ non-centre", HIT),
            (r"a PPL, \ checked against exact answers", SAMPLER), (r"particles; \ SMC evidence within 0.15", SAMPLER),
            (r"VI: \ too narrow, \ fast", VIC), (r"Laplace and INLA", HIT),
            (r"ABC: \ the summary decides", RES), (r"coupling from the past: \ exact", PATH),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.4),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 27, \ in fourteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part twenty-seven in fourteen lines. <bookmark mark='a'/> A random walk over hard disks integrated what no grid "
            "could. Importance sampling reweights a proposal, and Pareto's k-hat says when not to trust it. "
            "Metropolis–Hastings needs only density ratios, and tunes best near a quarter acceptance. Gibbs updates one "
            "coordinate at a time, helped by latent variables. R-hat and effective sample sizes caught stuck chains. "
            "Hamiltonian Monte Carlo follows the gradient, a hundred and forty times more efficient in a hundred dimensions. "
            "NUTS stops each trajectory at its U-turn and tunes itself. Neal's funnel defeats it until the model is "
            "non-centred. Statkit's probabilistic programming language reproduces exact answers. Particle filters track "
            "hidden states, and tempered SMC found the evidence. Variational inference is fast and too narrow. Laplace and "
            "INLA put normals at the mode. ABC needs only a simulator, and lives or dies by its summaries. And coupling from "
            "the past samples exactly."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=40.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"PSIS-LOO and WAIC", [28]), (r"Bayesian lasso and horseshoe by NUTS", [32]),
            (r"state-space models and Kalman", [38]), (r"Gaussian processes, \ INLA", [39]),
            (r"multiple imputation by MCMC", [41]), (r"Markov chains and mixing times", [44]),
            (r"stochastic approximation", [50]), (r"BvM and posterior contraction", [53]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 28 uses Pareto-smoothed importance sampling for leave-one-out "
            "cross-validation. Part 32 fits sparsity priors with NUTS. Part 38 builds the Kalman filter the particles "
            "matched. Part 39 fits Gaussian processes and spatial models with INLA. Part 41 imputes missing data by MCMC. "
            "Part 44 proves when Markov chains converge and how fast. Part 50 studies stochastic approximation, the theory "
            "behind adaptation. And Part 53 proves Bernstein–von Mises."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Detailed balance for Metropolis–Hastings; "
            "consistency of self-normalized importance sampling; the Gibbs sampler on a correlated normal as an "
            "autoregression; why leapfrog preserves volume and reverses; the ELBO identity; and the Jacobian of the log "
            "transform. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"C. Robert \& G. Casella, \emph{Monte Carlo Statistical Methods} (2nd ed., 2004)",
             r"S. Brooks, A. Gelman, G. Jones \& X.-L. Meng (eds.), \emph{Handbook of Markov Chain Monte Carlo} (2011)",
             r"A. Gelman et al., \emph{Bayesian Data Analysis} (3rd ed., 2013), \ Part III",
             r"A. Doucet, N. de Freitas \& N. Gordon (eds.), \emph{Sequential Monte Carlo Methods in Practice} (2001)"],
            [r"N. Metropolis et al.\ (1953); \ W. Hastings (1970); \ S. \& D. Geman (1984); \ A. Gelfand \& A. Smith (1990)",
             r"S. Duane et al.\ (1987); \ R. Neal (2003, 2011); \ M. Hoffman \& A. Gelman (2014); \ A. Vehtari et al.\ (2021, 2024)",
             r"N. Gordon, D. Salmond \& A. Smith (1993); \ M. Jordan et al.\ (1999); \ A. Kucukelbir et al.\ (2017)",
             r"H. Rue, S. Martino \& N. Chopin (2009); \ M. Beaumont et al.\ (2002); \ J. Propp \& D. Wilson (1996)"])
        with self.voiceover(
            "The books this part follows: Robert and Casella's Monte Carlo Statistical Methods, the Handbook of Markov Chain "
            "Monte Carlo, the computational chapters of Bayesian Data Analysis, and Doucet, de Freitas and Gordon on "
            "sequential Monte Carlo; with the papers from Metropolis to Propp and Wilson."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=27, current=None)
        nxt = VGroup(label(r"Part 28", font_size=30, color=GREY_B), label(r"Which Model?", font_size=48),
                     label(r"optimism, \ AIC, \ BIC, \ cross-validation, \ LOO and WAIC", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Twenty-seven parts of sixty-five. <bookmark mark='a'/> Any model we can write down, we can now fit and check. "
            "<bookmark mark='b'/> Which makes the next question unavoidable: which model should we believe? In 1983 David "
            "Freedman regressed pure noise on fifty columns of noise, kept the columns that looked significant, refitted, and "
            "found a highly significant regression. Part 28: which model?"
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(27)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
