from __future__ import annotations

import numpy as np

from videos.stats.stats59.common import *  # noqa: F403


class AMP(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter five. Approximate message passing and its state evolution: an algorithm whose every "
                            "step can be predicted exactly.", 5, r"AMP and state evolution", r"An algorithm you can predict",
                            lit=(2009, 2011))
        self.algorithm()
        self.onsager()
        self.se()
        self.cobweb()
        self.compare()
        self.cost()
        self.dt()
        self.dt_chart()
        self.proof()

    def algorithm(self):
        heading = label('AMP with a correctly scaled Gaussian matrix', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> David Donoho, Arian Maleki and Andrea Montanari introduced approximate message "
            'passing in 2009, for compressed sensing: recover a sparse x from y equal to A x plus noise, with A an '
            "n by p Gaussian matrix. <bookmark mark='b'/> Each step forms a pseudo-observation, the current "
            "estimate plus A transpose times the residual, <bookmark mark='c'/> and soft-thresholds it, as the "
            "lasso does. <bookmark mark='d'/> The residual carries one extra term, the Onsager correction: the "
            'previous residual, times the fraction of coordinates currently nonzero, divided by delta, the ratio n '
            'over p.'
        ),
            [(r"\text{problem}", r":", r"y = Ax + w, \ \ A_{ij} \sim N(0, 1/n), \ \ \delta = n/p", 38),
             (r"r^t", r"=", r"x^t + A'z^t", 40),
             (r"x^{t+1}", r"=", r"\eta(r^t; \theta\tau_t), \ \ \eta = \text{soft threshold}", 40),
             (r"z^{t+1}", r"=", r"y - Ax^{t+1} + \tfrac1\delta\,z^t\,\langle\eta'(r^t)\rangle", 38)],
            [r"Donoho, \ Maleki \& Montanari (2009)", r"a pseudo-observation", r"Part 32's shrinkage", r"the Onsager term"],
            colors=[(3, AMPC)])

    def onsager(self):
        heading = label('The reaction term cancels leading feedback', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Without the Onsager term, this resembles iterative soft thresholding with a unit "
            'step; ordinary ISTA also needs a suitable step size, and its pseudo-observations are a tangle of '
            "correlated errors. <bookmark mark='b'/> The extra term cancels, to leading order, the correlation "
            "between the current estimate and the noise in A transpose z. <bookmark mark='c'/> The effect is "
            'remarkable: at every iteration, the pseudo-observation behaves like the truth plus independent '
            "Gaussian noise, coordinate by coordinate. <bookmark mark='d'/> The idea comes from statistical "
            'physics, where Thouless, Anderson and Palmer used such a reaction term for spin glasses in 1977.'
        ),
            [(r"\text{without it}", r":", r"\text{ISTA: \ correlated errors}", 40),
             (r"\text{with it}", r":", r"\text{the correlation with the past cancels}", 40),
             (r"r^t", r"\approx", r"x + \tau_t Z \ \ \text{coordinatewise, \ } Z \sim N(0, 1)", 40),
             (r"\text{origin}", r":", r"\text{Thouless, \ Anderson \& Palmer (1977)}", 40)],
            [r"Part 21's ISTA", r"a reaction term", r"the miracle", r"spin glasses"],
            colors=[(2, AMPC)])

    def se(self):
        heading = label('State evolution at each fixed iteration', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Then the noise level obeys a one-dimensional recursion, the state evolution. "
            "<bookmark mark='b'/> The next noise variance is the measurement noise, plus one over delta times the "
            'mean squared error of the soft-threshold denoiser applied to the truth plus noise at the current '
            "level. <bookmark mark='c'/> The expectation is over one scalar: a coordinate of x drawn from its "
            "empirical distribution, and an independent standard normal. <bookmark mark='d'/> Mohsen Bayati and "
            'Montanari proved in 2011 that this holds exactly in the proportional limit, for Gaussian matrices, at '
            'every fixed iteration.'
        ),
            [(r"\tau_{t+1}^2", r"=", r"\sigma^2 + \tfrac1\delta\,E\big[(\eta(X + \tau_t Z; \theta\tau_t) - X)^2\big]", 38),
             (r"\text{the map}", r":", r"\tau^2 \mapsto F(\tau^2)", 40),
             (r"\text{a scalar expectation}", r":", r"X \sim \text{the signal's law}, \ Z \sim N(0, 1)", 38),
             (r"\text{theorem}", r":", r"\text{proportional limit at every fixed } t", 40)],
            [r"state evolution", r"the cobweb's curve", r"one dimension", r"Bayati \& Montanari (2011)"],
            colors=[(0, AMPC), (3, PROPC)])

    def cobweb(self):
        d = load("amp")
        grid = np.asarray(d["grid"])
        A = axes([0, 0.25], [0, 0.25], x_length=5.4, y_length=5.4, xlabel=r"$\tau_t^2$", ylabel=r"$\tau_{t+1}^2$",
                 xticks=[0, 0.1, 0.2], yticks=[0, 0.1, 0.2], center=[-2.6, 0.0, 0])
        ax = A.ax
        se = StateEvolution(ax, grid, d["smap"])
        cw = se.cobweb(d["tau2_se"][:12], AMPC)
        its = se.iterates(d["tau2_amp"][:12], WHITE)
        fp = se.fixed_point(d["tau2_se"][-1], PROPC)
        side = fit_rows(VGroup(
            label(rf"$n = {d['n']:,}$, \ $p = {d['p']:,}$, \ $\delta = {d['delta']:g}$; \ {int(d['eps'] * 100)}\% of $x$ is $\pm 1$", font_size=22),
            label(rf"noise $\sigma^2 = {d['sigma2']:g}$; \ threshold $\theta = {d['theta']:g}$", font_size=22, color=GREY_A),
            label(r"blue: \ the state-evolution map $F$; \ grey: \ the diagonal", font_size=22, color=SIMC),
            label(r"gold: \ the cobweb, \ iterating $F$ from $\tau_0^2$", font_size=22, color=AMPC),
            label(r"white: \ AMP's measured $\|z^t\|^2/n$, \ iteration by iteration", font_size=22, color=WHITE),
            label(rf"green: \ the fixed point, \ $\tau_\infty^2 = {d['tau2_se'][-1]:.4f}$", font_size=22, color=PROPC),
        ), 5.6, 0.34, [3.6, 0.2, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The part's instrument: the state-evolution cobweb. A thousand measurements of a "
            f"two-thousand-dimensional signal, a tenth of it plus or minus one. <bookmark mark='b'/> Small noise, and a "
            f"threshold of one and a half noise levels. <bookmark mark='c'/> The blue curve is the map from one noise "
            f"variance to the next; the grey line is the diagonal. <bookmark mark='d'/> Iterating the map traces the gold "
            f"staircase, step by step down to the crossing. <bookmark mark='e'/> The white dots are the real algorithm's "
            f"measured noise at each iteration: they land on the staircase. <bookmark mark='f'/> Both settle at the fixed "
            f"point, {say(d['tau2_se'][-1], 4)}: the algorithm's whole trajectory was predictable from one scalar map."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"AMP simulated; \ state evolution exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(se.map_curve(SIMC)), Create(se.diagonal()), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(cw), FadeIn(side[3]), run_time=3.0)
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(i, scale=0.5) for i in its], lag_ratio=0.15), FadeIn(side[4]), run_time=2.5)
            vo.wait_until("f")
            self.play(FadeIn(fp, scale=0.5), FadeIn(side[5]))
        self.clear_scene()

    def compare(self):
        d = load("amp")
        t_amp, t_se = d["tau2_amp"], d["tau2_se"]
        heading = label('Measured iterates and limiting predictions', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            f"<bookmark mark='a'/> The numbers, side by side. After one iteration, AMP's noise variance is "
            f"{say(t_amp[1], 4)}, and state evolution predicts {say(t_se[1], 4)}. <bookmark mark='b'/> After three, "
            f"{say(t_amp[3], 4)} against {say(t_se[3], 4)}. <bookmark mark='c'/> After twenty-five, the estimate's mean "
            f"squared error is {say(d['mse_amp'][-1], 4)}. <bookmark mark='d'/> At two thousand dimensions the agreement is "
            f"close in this single simulation; the theorem says it becomes exact as the dimension grows.",
            [(r"t = 1", r":", rf"\text{{AMP }} {t_amp[1]:.4f}, \ \ \text{{SE }} {t_se[1]:.4f}", 40),
             (r"t = 3", r":", rf"{t_amp[3]:.4f}, \ \ {t_se[3]:.4f}", 40),
             (r"t = 25", r":", rf"\text{{MSE}} = {d['mse_amp'][-1]:.4f}", 40),
             (r"\text{agreement}", r":", r"\text{two or three digits at } p = 2{,}000", 40)],
            [r"measured vs predicted", r"still close", r"converged", r"exact as $p \to \infty$"],
            colors=[(3, PROPC)])

    def dt(self):
        heading = label('The noiseless weak recovery boundary', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> State evolution explains Part thirty-two's Donoho–Tanner curve. With no noise, "
            "the fixed point at zero is stable, and the signal is recovered exactly, when the map's slope at zero "
            "is below one. <bookmark mark='b'/> That slope depends on the sparsity rho, the undersampling delta, "
            "and the threshold. <bookmark mark='c'/> Minimizing over the threshold gives the boundary in closed "
            'form: rho of delta is the maximum over z of one minus two over delta times a Gaussian integral, '
            "divided by one plus z squared minus twice that integral. <bookmark mark='d'/> Donoho, Maleki and "
            'Montanari showed it is exactly the curve Donoho and Tanner had found from the geometry of random '
            'polytopes.'
        ),
            [(r"\sigma = 0", r":", r"\text{recovery} \iff F'(0) < 1", 40),
             (r"F'(0)", r"=", r"\text{a function of } \rho, \delta, \theta", 40),
             (r"\rho_{\mathrm{DT}}(\delta)", r"=", r"\max_z \frac{1 - \frac2\delta[(1 + z^2)\Phi(-z) - z\phi(z)]}{1 + z^2 - 2[(1 + z^2)\Phi(-z) - z\phi(z)]}", 32),
             (r"=", r"\;", r"\text{the polytope curve of Part 32}", 40)],
            [r"stability of zero", r"$\rho = k/n$", r"minimax threshold", r"two proofs, \ one curve"],
            colors=[(2, AMPC), (3, PROPC)])

    def dt_chart(self):
        d = load("amp")
        A = axes([0, 1], [0, 1], x_length=5.6, y_length=4.6, xlabel=r"$\delta = n/p$", ylabel=r"$\rho = k/n$",
                 xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], center=[-2.6, 0.2, 0])
        ax = A.ax
        dl = np.asarray(d["deltas"])
        cur = polyline(ax, np.r_[0, dl, 1], np.r_[0, d["dt"], 1], AMPC, 4)
        ok = Polygon(*[ax.c2p(a, b) for a, b in zip(np.r_[0, dl, 1], np.r_[0, d["dt"], 1])], ax.c2p(1, 0), ax.c2p(0, 0),
                     stroke_width=0, fill_color=PROPC, fill_opacity=0.25)
        rho_here = d["eps"] / d["delta"]
        here = Dot(ax.c2p(d["delta"], rho_here), radius=0.1, color=WHITE)
        side = fit_rows(VGroup(
            label(r"gold: \ the Donoho--Tanner curve, \ from state evolution", font_size=22, color=AMPC),
            label(r"green: \ exact recovery by $\ell_1$ \ (and by AMP)", font_size=22, color=PROPC),
            label(rf"white: \ chapter 5's problem, \ $\delta = {d['delta']:g}$, \ $\rho = {rho_here:.2f}$", font_size=22, color=WHITE),
            label(r"same curve as Part 32's polytope count", font_size=22, color=GREY_A),
        ), 5.0, 0.4, [3.9, 0.3, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The curve, computed from state evolution. <bookmark mark='b'/> Below it, l-one "
            f"minimization and AMP recover the sparse signal exactly when there is no noise. <bookmark mark='c'/> Our problem "
            f"sits at delta a half and rho a fifth, comfortably inside. <bookmark mark='d'/> It is the same curve Part "
            f"thirty-two drew from counting the faces of random polytopes: two theories, one answer."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact")))
            vo.wait_until("a")
            self.play(Create(cur), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(ok), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(here, scale=0.5), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def proof(self):
        heading = label('Empirical limits, not exact finite Gaussian errors', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> A proof conditions on the matrix information revealed by earlier iterates. For an "
            'IID Gaussian design the unexplored component retains a controlled Gaussian distribution. <bookmark '
            "mark='b'/> The Onsager correction cancels the leading feedback from reusing the same matrix. <bookmark "
            "mark='c'/> Induction proves an empirical distributional state-evolution limit at every fixed "
            'iteration, under denoiser and moment conditions. It does not say finite-dimensional errors are exactly '
            'independent Gaussians, or justify exchanging iteration and dimension limits without more work. '
            "<bookmark mark='d'/> At a converged fixed point, the soft threshold's KKT conditions match a lasso "
            'with a calibrated positive penalty. Additional convergence analysis connects fixed-iteration AMP '
            "theory to the estimator's limiting risk."
        ),
            [(r"\text{Bolthausen}", r":", r"\text{condition on what the algorithm has used}", 38),
             (r"\text{Onsager}", r":", r"\text{removes the used part's influence}", 40),
             (r"\text{induction}", r":", r"(x_j,r_j^t)\Rightarrow(X,X+\tau_tZ) \text{ empirically; }t\text{ fixed}", 40),
             (r"\text{fixed points}", r":", r"\text{KKT matches lasso at a calibrated positive penalty}", 40)],
            [r"Bolthausen (2014)", r"why the term", r"the theorem", r"Bayati \& Montanari (2012)"],
            colors=[(3, PROPC)])

    def cost(self):
        heading = label('Dense matrix products and convergence limits', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Each dense AMP step multiplies by A and by its transpose. This costs order n "
            "times p operations. <bookmark mark='b'/> At a thousand by two thousand, the two products use about "
            'four million multiply-accumulate pairs, or eight million elementary floating-point operations. The '
            "illustration runs twenty-five iterations. <bookmark mark='c'/> Coordinate descent can have a "
            'comparable order per sweep, but wall-clock speed depends on implementation, conditioning and stopping '
            "accuracy. <bookmark mark='d'/> State evolution predicts AMP's limiting trajectory under its "
            'assumptions. Ordinary AMP can fail for correlated or poorly conditioned designs; damping and vector '
            'variants have their own conditions, rather than a universal repair.'
        ),
            [('\\text{per iteration}', ':', "Ax, \\ A'z: \\ O(np)", 40),
             ('\\text{here}', ':', '\\approx 4 \\times 10^6 \\text{ multiply--accumulate pairs}, \\ 25 \\text{ iterations}', 40),
             ('\\text{compare}', ':', '\\text{coordinate descent: \\ similar; \\ interior point: \\ more}', 38),
             ('\\text{the catch}', ':', '\\text{non-Gaussian } A \\text{ can make it diverge}', 40)],
            ['two products', '$n = 1{,}000$, \\ $p = 2{,}000$', "Part 21's solvers", 'damped and vector AMP'],
            colors=[(3, CLASSC)])
