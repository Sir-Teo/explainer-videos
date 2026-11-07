from __future__ import annotations

from videos.stats.stats21.common import *  # noqa: F403

PROBLEMS = [
    r"Show that the logistic log likelihood has Hessian $-X'WX$, \ $W = \operatorname{diag}(p_i(1 - p_i))$, \ so it is concave.",
    r"Maximize the entropy $-\sum_k p_k \log p_k$ subject to $\sum_k p_k = 1$ and $\sum_k k\,p_k = \mu$: \ show $p_k \propto e^{-\lambda k}$.",
    r"Write the dual of the bakery's LP and check that $y = (1, 0, 2)$ is feasible and optimal.",
    r"Newton for an exponential rate: \ show $\lambda_1 - \hat\lambda = -\bar x(\lambda_0 - \hat\lambda)^2$. \ When does it go negative?",
    r"Derive the proximal operator of $\lambda|x|$: \ soft thresholding.",
    r"Robbins--Monro for a median with steps $a/k$: \ why $a > 1/(2f(\theta^*))$? \ The bound for $N(10, 3^2)$.",
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
            (r"Dantzig's homework; \ the simplex", PATH), (r"convexity: \ local is global", FIT),
            (r"Jensen; \ KL $\ge 0$", FIT), (r"Lagrange, \ KKT, \ slackness", NEWT),
            (r"duality: \ shadow prices", NEWT), (r"Neyman--Pearson as an LP", TRUE),
            (r"LAD and quantiles: \ LPs", RES), (r"Newton: \ local quadratic convergence", NEWT),
            (r"MM: \ touching majorizers give descent", PATH), (r"coordinate descent: \ glmnet", PATH),
            (r"ISTA $1/k$, \ FISTA $1/k^2$", FAST), (r"ADMM: \ split and conquer", TEAL),
            (r"SGD; \ Polyak--Ruppert: \ 93\%", GRAD), (r"curvature and uncertainty: \ with assumptions", TRUE),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.4),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 21, \ in fourteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part twenty-one in fourteen lines. <bookmark mark='a'/> Dantzig's homework led to linear programming and"
            " the simplex method. Convex problems have no local traps, and Jensen's inequality shows why likelihood "
            "works. Lagrange multipliers and the KKT conditions handle constraints, with complementary slackness; "
            "duality turns constraints into prices, and the Neyman–Pearson lemma into a linear program whose "
            "multiplier is the critical value. Least absolute deviations and quantile regression are linear programs."
            " Near a regular optimum, Newton can have quadratic convergence; MM algorithms never go uphill; "
            "coordinate descent powers the lasso; FISTA's momentum turns one over k into one over k squared; ADMM "
            "splits hard problems into easy ones. Averaged stochastic gradient has strong asymptotic guarantees under"
            " explicit regularity and step assumptions; the Board illustrates one finite-sample setting. Curvature "
            "supports regular likelihood inference, while misspecification requires more than the Hessian alone."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=34.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"EM, \ and the likelihood in depth", [22]), (r"IRLS for every GLM", [24]),
            (r"mixed models: \ optimizing over variance components", [25]), (r"Bayesian computation: \ optimization's cousin", [27]),
            (r"the lasso's theory", [32]), (r"empirical risk minimization", [54]),
            (r"optimal transport: \ an LP between distributions", [61]), (r"training neural networks", [64]),
        ], font_size=22)
        intro = label("Where optimization returns in the course", font_size=36)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 22 makes the EM algorithm the centre of likelihood computation. "
            "Part 24 uses iteratively reweighted least squares for every generalized linear model. Part 25 optimizes over "
            "variance components. Part 27's Bayesian computation is optimization's cousin. Part 32 proves when the lasso finds "
            "the truth. Part 54 studies empirical risk minimization. Part 61's optimal transport is a linear program between "
            "distributions. And Part 64 trains neural networks with stochastic gradient."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), FadeIn(card.head), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The concavity of the logistic likelihood; "
            "maximum entropy, which produces an exponential family; the bakery's dual; Newton's quadratic convergence for an "
            "exponential rate, and when it fails; the soft-threshold operator; and the step size Robbins–Monro needs. Pause "
            "here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"S. Boyd \& L. Vandenberghe, \emph{Convex Optimization} (2004)",
             r"K. Lange, \emph{Optimization} (2nd ed., 2013); \ \emph{MM Optimization Algorithms} (2016)",
             r"J. Nocedal \& S. Wright, \emph{Numerical Optimization} (2nd ed., 2006)",
             r"R. Koenker, \emph{Quantile Regression} (2005)"],
            [r"G. Dantzig (1940, 1947); \ G. Dantzig \& A. Wald (1951); \ H. Kuhn \& A. Tucker (1951)",
             r"R. Koenker \& G. Bassett (1978); \ D. Hunter \& K. Lange (2000); \ P. Tseng (2001)",
             r"A. Beck \& M. Teboulle (2009); \ Y. Nesterov (1983); \ S. Boyd et al.\ (2011)",
             r"H. Robbins \& S. Monro (1951); \ B. Polyak \& A. Juditsky (1992); \ L. Bottou \& O. Bousquet (2008)"])
        with self.voiceover(
            "The books this part follows: Boyd and Vandenberghe's Convex Optimization, Kenneth Lange's books on optimization and "
            "MM, Nocedal and Wright's Numerical Optimization, and Koenker's Quantile Regression; with the papers from Dantzig "
            "and Wald to Polyak and Juditsky."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=21, current=None)
        nxt = VGroup(label(r"Part 22", font_size=30, color=GREY_B), label(r"Likelihood in Depth", font_size=48),
                     label(r"why maximum likelihood works, \ and what happens when the model is wrong", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Twenty-one parts of sixty-five, the first of the master's. <bookmark mark='a'/> We have a collection of "
            "algorithms for many estimators, and know that interpreting their curvature requires statistical "
            "assumptions. <bookmark mark='b'/> Next, the likelihood itself. In 1894 Karl Pearson tried to split a "
            "thousand crabs from Naples into two species by solving a ninth-degree polynomial. Maximum likelihood and"
            " the EM algorithm do it better, and a wrong model gets a sandwich. Part 22: likelihood in depth."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(21)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
