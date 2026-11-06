from __future__ import annotations

from videos.stats.stats59.common import *  # noqa: F403


class CGMT(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter six. Gordon's comparison inequality: replacing a matrix by two vectors.", 6,
                            r"Gordon's comparison", r"A matrix, \ replaced by two vectors", lit=(2015,))
        self.gordon()
        self.convex()
        self.recipe()
        self.ols_worked()
        self.ridge_cgmt()
        self.lasso()
        self.compare_tools()

    def gordon(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Yehoram Gordon proved in 1985 a comparison between two Gaussian processes. The primary "
            "one is a bilinear form, u transpose G w, for a Gaussian matrix G, plus any function psi of u and w. <bookmark "
            "mark='b'/> The auxiliary one replaces the matrix by two independent Gaussian vectors, g and h: the norm of w "
            "times g transpose u, plus the norm of u times h transpose w. <bookmark mark='c'/> Gordon's inequality says the "
            "min-max of the primary is, with high probability, at least that of the auxiliary, minus a little. <bookmark "
            "mark='d'/> The auxiliary problem has only vectors, and its min-max collapses to a few scalars.",
            [(r"\text{primary}", r":", r"\min_w\max_u \ u'Gw + \psi(w, u)", 40),
             (r"\text{auxiliary}", r":", r"\min_w\max_u \ \|w\|g'u + \|u\|h'w + \psi(w, u)", 38),
             (r"\text{Gordon (1985)}", r":", r"P(\text{primary} < c) \le 2P(\text{auxiliary} \le c)", 38),
             (r"\text{the point}", r":", r"\text{the auxiliary problem reduces to scalars}", 40)],
            [r"a bilinear form", r"two vectors, \ not a matrix", r"Slepian's cousin", r"Part 51's comparison"],
            colors=[(1, AMPC)])

    def convex(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Gordon's inequality goes one way. Christos Thrampoulidis, Samet Oymak and Babak Hassibi "
            "showed in 2015 that with convexity it goes both ways: <bookmark mark='b'/> if psi is convex in w and concave in "
            "u, over convex compact sets, the primary and auxiliary optimal values concentrate around the same number. "
            "<bookmark mark='c'/> More: any property of the auxiliary problem's minimizer that holds with high probability "
            "also holds for the primary's. <bookmark mark='d'/> That is the convex Gaussian min-max theorem, and it gives the "
            "exact error of any convex regularized estimator with a Gaussian design.",
            [(r"\text{one way}", r":", r"\text{Gordon: \ a lower bound}", 40),
             (r"\psi \text{ convex-concave}", r":", r"\text{primary} \approx \text{auxiliary}", 40),
             (r"\text{minimizers}", r":", r"\text{properties transfer}", 40),
             (r"\text{CGMT}", r":", r"\text{exact errors of convex estimators}", 40)],
            [r"Gordon's direction", r"Thrampoulidis, \ Oymak \& Hassibi (2015)", r"the key step", r"a general tool"],
            colors=[(1, PROPC), (3, PROPC)])

    def recipe(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The recipe for an estimator minimizing a loss of y minus X beta plus a penalty. <bookmark "
            "mark='b'/> Write the loss through its convex conjugate, which introduces the max over u and the bilinear form "
            "in the Gaussian design. <bookmark mark='c'/> Replace it by the auxiliary problem and optimize over the "
            "directions of u and w: two or three scalar variables remain, the norm of the error among them. <bookmark "
            "mark='d'/> Their saddle point is the answer, and the equations it satisfies are, in every case checked, the "
            "same as state evolution's fixed point.",
            [(r"\min_\beta", r"\;", r"L(y - X\beta) + f(\beta)", 40),
             (r"\text{conjugate}", r":", r"\max_u \ u'(y - X\beta) - L^*(u)", 40),
             (r"\text{auxiliary}", r":", r"\text{scalars: \ } \|\hat\beta - \beta\|, \ \|u\|, \dots", 40),
             (r"\text{saddle point}", r"=", r"\text{AMP's fixed point}", 40)],
            [r"a convex estimator", r"a min-max", r"a few scalars", r"two tools agree"],
            colors=[(3, AMPC)])

    def ols_worked(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A worked case: least squares, with n by p design, kappa less than one, and noise sigma. "
            "<bookmark mark='b'/> The auxiliary problem, after optimizing over directions, is a minimization in one scalar, "
            "the error norm a, of root of a squared plus sigma squared, times root n, minus a times root p. <bookmark "
            "mark='c'/> Setting its derivative to zero gives a squared over a squared plus sigma squared equal to kappa, so a "
            "squared is sigma squared kappa over one minus kappa. <bookmark mark='d'/> That is chapter one's exact formula, "
            "recovered in four lines without inverting a matrix.",
            [(r"\text{least squares}", r":", r"\min_\beta \|y - X\beta\|", 40),
             (r"\text{auxiliary}", r":", r"\min_{a \ge 0} \ \sqrt{a^2 + \sigma^2}\,\sqrt n - a\sqrt p", 40),
             (r"\text{stationary}", r":", r"\frac{a^2}{a^2 + \sigma^2} = \kappa", 40),
             (r"\Rightarrow", r"\;", r"a^2 = \sigma^2\frac{\kappa}{1 - \kappa}", 40)],
            [r"chapter 1's case", r"one scalar", r"calculus", r"chapter 1's formula"],
            colors=[(3, PROPC)])

    def lasso(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> For the lasso, the same recipe gives two scalar equations, in the error level tau and a "
            "scaling of the penalty. <bookmark mark='b'/> They say tau squared equals sigma squared plus one over delta times "
            "the soft-threshold error at noise tau, and that the threshold relates to the penalty through the fraction of "
            "nonzero coordinates. <bookmark mark='c'/> These are state evolution's fixed-point equations, from chapter five, "
            "exactly. <bookmark mark='d'/> So the lasso's exact error is known two ways: as the limit of an algorithm, and as "
            "the saddle point of a Gaussian min-max. The cobweb's fixed point is the lasso's error.",
            [(r"\tau^2", r"=", r"\sigma^2 + \tfrac1\delta E[(\eta(X + \tau Z; \theta\tau) - X)^2]", 38),
             (r"\lambda", r"=", r"\theta\tau\big(1 - \tfrac1\delta P(|X + \tau Z| > \theta\tau)\big)", 38),
             (r"=", r"\;", r"\text{chapter 5's fixed point}", 40),
             (r"\text{so}", r":", r"\text{two derivations, \ one exact error}", 40)],
            [r"Thrampoulidis et al.; \ Bayati \& Montanari", r"the calibration", r"state evolution", r"the cobweb's endpoint"],
            colors=[(0, AMPC), (3, PROPC)])

    def compare_tools(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Two tools compared. <bookmark mark='b'/> AMP gives an algorithm and its whole trajectory, "
            "and handles non-convex and Bayesian problems, but its proofs need the iteration to converge. <bookmark "
            "mark='c'/> CGMT handles any convex estimator directly, with finite-sample high-probability bounds, but needs "
            "convexity and a Gaussian design. <bookmark mark='d'/> Where both apply, they agree. Where neither does, the "
            "physicists' method, next, still makes predictions.",
            [(r"AMP vs CGMT:", GREY_A),
             (r"AMP: \ an algorithm, \ its trajectory; \ non-convex and Bayesian problems", AMPC),
             (r"CGMT: \ any convex estimator, \ high-probability bounds; \ needs convexity", PROPC),
             (r"where both apply, \ they agree; \ beyond both, \ the replica method", THEORYC)])

    def ridge_cgmt(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The same calculation for ridge adds the penalty to the auxiliary problem. <bookmark mark='b'/> The minimization over directions now trades the residual term against the penalty, leaving two scalars: the error norm and the projection of the estimate on the truth. <bookmark mark='c'/> Their optimum reproduces chapter three's Dobriban–Wager formula, which there came from the Marchenko–Pastur Stieltjes transform. <bookmark mark='d'/> Random matrices, Gordon, and AMP: three derivations of one number, which is the strongest evidence that it is right.",
            [('\\text{ridge}', ':', '\\min_\\beta \\tfrac12\\|y - X\\beta\\|^2 + \\tfrac\\lambda2\\|\\beta\\|^2', 40),
             ('\\text{auxiliary}', ':', '\\text{two scalars: \\ error norm, \\ alignment}', 40),
             ('\\text{optimum}', '=', "\\text{chapter 3's formula}", 40),
             ('\\text{three routes}', ':', '\\text{RMT, \\ CGMT, \\ AMP}', 40)],
            ['a penalty', 'one more scalar', 'Dobriban \\& Wager', 'one answer'],
            colors=[(3, PROPC)])
