from __future__ import annotations

import numpy as np

from videos.stats.stats59.common import *  # noqa: F403


class MEstimation(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter four. M-estimation in high dimensions: when the textbook's choice of loss is wrong.", 4,
                            r"M-estimation in high dimensions", r"When the best loss changes")
        self.scaling()
        self.chart()
        self.system()
        self.ols_check()
        self.why()
        self.optimal_loss()
        self.lessons()

    def scaling(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Part thirty's robust regression chose the loss by the error distribution: least absolute "
            "deviations for heavy-tailed errors, because its asymptotic variance is smaller there. <bookmark mark='b'/> For "
            "Laplace errors, fixed-p theory says least absolute deviations has half the variance of least squares. <bookmark "
            "mark='c'/> Noureddine El Karoui, Derek Bean, Peter Bickel, Chinghway Lim and Bin Yu asked in 2013 what happens "
            "when p grows with n. <bookmark mark='d'/> Their answer: the error of any M-estimator solves a system of two "
            "equations, and the ranking of losses can reverse.",
            [(r"\text{Part 30}", r":", r"\text{choose the loss by the error law}", 40),
             (r"\text{Laplace errors}", r":", r"\mathrm{Var}(\mathrm{LAD}) = \tfrac12\mathrm{Var}(\mathrm{OLS}) \text{ at fixed } p", 38),
             (r"\text{El Karoui et al. (2013)}", r":", r"p/n \to \kappa", 40),
             (r"\text{answer}", r":", r"\text{a two-equation system; \ rankings can reverse}", 40)],
            [r"Huber's programme", r"Part 30's ARE", r"\emph{PNAS}", r"chapter 2's method"],
            colors=[(1, CLASSC), (3, PROPC)])

    def chart(self):
        d = load("robust")
        R = d["rows"]
        ks = np.array([r["kappa"] for r in R])
        A = axes([0, 0.52], [0, 1.25], x_length=7.4, y_length=4.4, xlabel=r"$\kappa = p/n$", ylabel=r"$E\|\hat\beta - \beta\|^2$",
                 xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[0, 0.5, 1.0], center=[-2.5, 0.2, 0])
        ax = A.ax
        ols = VGroup(polyline(ax, ks, [r["ols"] for r in R], SIMC, 4), *[Dot(ax.c2p(k, r["ols"]), radius=0.07, color=SIMC) for k, r in zip(ks, R)])
        lad = VGroup(polyline(ax, ks, [r["lad"] for r in R], AMPC, 4), *[Dot(ax.c2p(k, r["lad"]), radius=0.07, color=AMPC) for k, r in zip(ks, R)])
        ex = polyline(ax, ks, [r["ols_exact"] for r in R], GREY_B, 2.5)
        r1 = R[1]
        rl = R[-1]
        side = fit_rows(VGroup(
            label(rf"$n = {d['n']}$, \ Laplace errors of variance 1, \ 12 repetitions", font_size=22),
            label(r"blue: \ least squares; \ grey: \ its exact $\kappa/(1-\kappa)$", font_size=22, color=SIMC),
            label(rf"gold: \ least absolute deviations", font_size=22, color=AMPC),
            label(rf"$\kappa = 0.1$: \ LAD {r1['lad']:.3f} \ vs \ OLS {r1['ols']:.3f}", font_size=22, color=PROPC),
            label(rf"$\kappa = 0.5$: \ LAD {rl['lad']:.2f} \ vs \ OLS {rl['ols']:.2f}: \ reversed", font_size=22, color=CLASSC),
        ), 4.6, 0.38, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A simulation, with Laplace errors of variance one. <bookmark mark='b'/> Least squares follows "
            f"its exact formula, kappa over one minus kappa. <bookmark mark='c'/> Least absolute deviations, in gold, starts "
            f"lower, <bookmark mark='d'/> as fixed-p theory promises: at a tenth, {say(r1['lad'], 3)} against "
            f"{say(r1['ols'], 3)}. <bookmark mark='e'/> But the curves cross between a fifth and three tenths, and at a half "
            f"least squares is better, {say(rl['ols'], 2)} against {say(rl['lad'], 2)}, although the errors are exactly the "
            f"kind least absolute deviations was designed for."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ex), Create(ols), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(lad), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def system(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The theory behind the crossing. For an M-estimator with loss rho, the residual of a "
            "held-out observation is the error plus a Gaussian term whose standard deviation r is the estimator's error, "
            "<bookmark mark='b'/> and the fitted residual is the proximal map of rho, at a scale c, applied to that "
            "held-out residual. <bookmark mark='c'/> Two equations in r and c follow, from leave-one-out arguments: one "
            "matching the proximal map's average slope to one minus kappa, one matching the squared size of the fitted "
            "scores to kappa r squared. <bookmark mark='d'/> David Donoho and Andrea Montanari derived the same system from "
            "approximate message passing, in 2016.",
            [(r"\text{held-out residual}", r":", r"\varepsilon + r Z", 40),
             (r"\text{fitted residual}", r"=", r"\operatorname{prox}_{c\rho}(\varepsilon + rZ)", 40),
             (r"\text{equations}", r":", r"E[\operatorname{prox}'_{c\rho}] = 1 - \kappa, \ \ E[(\varepsilon + rZ - \operatorname{prox})^2] = \kappa r^2", 32),
             (r"\text{also from AMP}", r":", r"\text{Donoho \& Montanari (2016)}", 40)],
            [r"leave one out", r"chapter 1's prox, \ again", r"two unknowns, \ $r$ and $c$", r"chapter 5's method"],
            colors=[(2, PROPC)])

    def why(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Why least absolute deviations loses. In high dimensions the fitted residuals are not the "
            "errors: each is the error plus a Gaussian term from estimating p coefficients. <bookmark mark='b'/> As kappa "
            "grows, that Gaussian term dominates. <bookmark mark='c'/> A loss tuned to the tails of the errors is then tuned "
            "to the wrong distribution: the effective noise is the error convolved with a normal. <bookmark mark='d'/> Squared "
            "loss is the right choice for Gaussian-like effective noise, so it wins once kappa is large.",
            [(r"\text{residual}", r"\approx", r"\varepsilon + rZ, \ \ r^2 = E\|\hat\beta - \beta\|^2", 40),
             (r"\kappa \uparrow", r":", r"rZ \text{ dominates}", 40),
             (r"\text{effective noise}", r":", r"\varepsilon * N(0, r^2): \ \text{more Gaussian}", 40),
             (r"\text{so}", r":", r"\text{squared loss wins at large } \kappa", 40)],
            [r"estimation noise", r"the regime's signature", r"a convolution", r"the crossing, \ explained"],
            colors=[(3, SIMC)])

    def optimal_loss(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> So what is the best loss? Bean, Bickel, El Karoui and Yu found it in 2013: not minus the "
            "log density of the errors, as at fixed p, but minus the log density of the errors convolved with a normal of the "
            "right variance, <bookmark mark='b'/> passed through a proximal transformation. <bookmark mark='c'/> For "
            "log-concave errors the optimal loss is convex, and it becomes more quadratic as kappa grows. <bookmark "
            "mark='d'/> Maximum likelihood is no longer optimal among M-estimators: efficiency has to be re-derived for the "
            "regime.",
            [(r"\text{fixed } p", r":", r"\rho_{\mathrm{opt}} = -\log f_\varepsilon \ \ (\text{the MLE})", 40),
             (r"\kappa > 0", r":", r"\text{based on } -\log(f_\varepsilon * \varphi_{r})", 40),
             (r"\text{log-concave errors}", r":", r"\text{convex, \ more quadratic as } \kappa \uparrow", 38),
             (r"\text{so}", r":", r"\text{the MLE is not optimal}", 40)],
            [r"Part 22's answer", r"Bean et al. (2013)", r"a family of losses", r"Part 45 revisited"],
            colors=[(1, PROPC), (3, CLASSC)])

    def lessons(self):
        self.list_voiceover(
            "<bookmark mark='a'/> The lessons of chapter four. <bookmark mark='b'/> Fixed-p efficiency rankings can reverse "
            "in high dimensions. <bookmark mark='c'/> Residuals are not errors: they carry the estimation noise of all p "
            "coefficients. <bookmark mark='d'/> And every M-estimator's error is computable from a small system of equations, "
            "which also says how to choose the loss.",
            [(r"chapter 4's lessons:", GREY_A),
             (r"efficiency rankings can reverse", CLASSC),
             (r"residuals carry the estimation noise of all $p$ coefficients", SIMC),
             (r"a small system gives every M-estimator's error, \ and the best loss", PROPC)])

    def ols_check(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A check of the system on least squares, where rho is half the square. <bookmark mark='b'/> Its proximal map at scale c is the input divided by one plus c, with constant slope one over one plus c. <bookmark mark='c'/> The first equation gives one over one plus c equal to one minus kappa. <bookmark mark='d'/> The second then gives r squared equal to the error variance times kappa over one minus kappa: chapter one's formula once more, from a third route.",
            [('\\rho(x)', '=', 'x^2/2', 40),
             ('\\operatorname{prox}_{c\\rho}(x)', '=', 'x/(1 + c)', 40),
             ('\\text{first equation}', ':', '1/(1 + c) = 1 - \\kappa', 40),
             ('\\text{second}', ':', 'r^2 = \\sigma^2\\kappa/(1 - \\kappa)', 40)],
            ['least squares', 'linear', 'the slope', 'chapter 1, \\ a third time'],
            colors=[(3, PROPC)])
