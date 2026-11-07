from __future__ import annotations

import numpy as np

from videos.stats.stats51.common import *  # noqa: F403


class StatisticalDimension(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.formula()
        self.grid()
        self.table()
        self.beyond()
        self.universal()

    def universal(self):
        rows = fit_rows(VGroup(
            label(r"is it only Gaussian?", font_size=28, color=GREY_A),
            label(r"Donoho \& Tanner (2009): \ the same curve for Bernoulli, \ Fourier and many other ensembles", font_size=26, color=SPHC),
            label(r"Oymak \& Tropp (2018): \ universality, \ proved for i.i.d. designs with enough moments", font_size=26, color=GOODC),
            label(r"structured matrices (partial Fourier, \ sparse) \ follow it closely in practice", font_size=26, color=MATC),
            label(r"but adversarial or highly coherent designs can fail far from it", font_size=26, color=BADC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Is the phase transition a Gaussian accident? <bookmark mark='b'/> David Donoho and Jared Tanner tested it in 2009 on matrices of random signs, random Fourier rows and many other ensembles, and found closely related transitions in the tested regimes; structured matrices require separate arguments. <bookmark mark='c'/> Samet Oymak and Joel Tropp proved in 2018 that the location of universality holds under symmetry, normalization, moment and nondegeneracy assumptions in the theorem, in an asymptotic regime. <bookmark mark='d'/> Structured measurement matrices, like the partial Fourier matrices of MRI scanners, follow it closely in practice. <bookmark mark='e'/> But the guarantee is for random designs: a coherent or adversarial matrix can need far more measurements."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def card(self):
        card = chapter_card(9, r"The statistical dimension", r"The Donoho--Tanner curve, \ explained", lit=(2014,), part=PART)
        with self.voiceover("Chapter nine. The statistical dimension: the Donoho–Tanner curve, explained."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"\delta(C)", r"=", r"E\,\|\Pi_C(g)\|^2: \ \text{closed convex cone }C;\ \Pi_C\text{ is Euclidean projection}", font_size=32),
            cmath(r"\text{a subspace of dimension } k", r":", r"\delta = k: \ \text{it extends dimension to cones}", font_size=32),
            cmath(r"w(C \cap S^{p-1})^2", r"\le", r"\delta(C) \le w(C \cap S^{p-1})^2 + 1", font_size=34),
            cmath(r"\text{the kinematic formula}", r":", r"m \ge \delta + O(\sqrt p) \Rightarrow \text{success}; \ \ m \le \delta - O(\sqrt p) \Rightarrow \text{failure}", font_size=28),
        ]
        rows[0][-1].set_color(SPHC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Amelunxen, \ Lotz, \ McCoy \& Tropp (2014)"), why(r"the right generalization"), why(r"the width, \ squared"), why(r"a sharp transition")]
        heading = label('Statistical dimension is an expected squared cone projection', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> In 2014, Dennis Amelunxen, Martin Lotz, Michael McCoy and Joel Tropp defined the statistical dimension of a convex cone: the expected squared length of a Gaussian vector's projection onto it. <bookmark mark='b'/> For a subspace of dimension k it is exactly k, so it extends the notion of dimension to cones. <bookmark mark='c'/> It is within one of the squared Gaussian width of the cone's intersection with the sphere. <bookmark mark='d'/> Their approximate kinematic formula says that a random subspace of codimension m misses the cone with high probability when m exceeds the statistical dimension by a multiple of root p, and hits it when m falls short by as much. A transition of width root p, controlled around the statistical dimension. This does not assert an exact fifty-percent crossing at finite p."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def formula(self):
        rows = [
            cmath(r"\delta\big(D(x_0)\big)", r"\le", r"\inf_{\tau \ge 0}\, E\,\mathrm{dist}^2\big(g, \tau\,\partial\|x_0\|_1\big)", font_size=34),
            cmath(r"\partial\|x_0\|_1", r"=", r"\{z: z_i = \mathrm{sign}(x_{0i}) \text{ on the support}, \ |z_i| \le 1 \text{ off it}\}", font_size=30),
            cmath(r"\delta", r"\le", r"\inf_\tau \big\{ s(1 + \tau^2) + (p - s)\, E(|g| - \tau)_+^2 \big\}", font_size=34),
            cmath(r"\text{one-dimensional}", r":", r"\text{minimize over } \tau \text{ numerically; \ depends only on } s \text{ and } p", font_size=30),
        ]
        rows[2][-1].set_color(SPHC)
        whys = [why(r"the polar cone"), why(r"the subdifferential"), why(r"soft thresholding at $\tau$"), why(r"statkit.hdp's \texttt{stat\_dim\_l1}")]
        heading = label('The infimum of expectations is an upper bound on the exact dimension', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> For the l-one descent cone, the statistical dimension has a formula, accurate up to a small error term: the smallest expected squared distance from a Gaussian vector to a scaled copy of the subdifferential of the l-one norm at the truth. <bookmark mark='b'/> The subdifferential is the set of vectors equal to the signs on the support and between minus one and one elsewhere. <bookmark mark='c'/> The distance splits by coordinate: on the support, the distance from g to plus or minus tau; off it, the amount by which g exceeds tau in absolute value, which is soft thresholding. <bookmark mark='d'/> Minimizing the expectation gives a computable upper bound on the statistical dimension. The exact dimension instead averages the per-draw minimum; interchanging minimum and expectation creates a gap."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def grid(self):
        d = load("statdim")
        A = axes([0, 44], [0, 100], x_length=7.4, y_length=4.4, xlabel=rf"sparsity $s$, \ $p = {d['p']}$", ylabel=r"measurements $m$",
                 xticks=[0, 10, 20, 30, 40], yticks=[0, 25, 50, 75, 100], center=[-2.5, 0.2, 0])
        ax = A.ax
        dots = VGroup()
        for g in d["grid"]:
            col = interpolate_color(ManimColor(BADC), ManimColor(GOODC), g["success"])
            dots.add(Square(side_length=0.2, fill_color=col, fill_opacity=0.9, stroke_width=0).move_to(ax.c2p(g["s"], g["m"])))
        cs = np.asarray(d["curve_s"])
        cv = np.asarray(d["curve"])
        ok = cs <= 44
        curve = clip_curve(ax, cs[ok], cv[ok], SPHC, 5, ymin=0, ymax=100)
        half = {}
        for s in d["ss"]:
            col = [g for g in d["grid"] if g["s"] == s]
            m50 = next((g["m"] for g in col if g["success"] >= 0.5), None)
            half[s] = m50
        i10 = list(d["curve_s"]).index(10)
        side = fit_rows(VGroup(
            label(r"basis pursuit on $m \times 100$ Gaussian $A$, \ 20 trials a square", font_size=22),
            label(r"green: \ always recovered; \ red: \ never", font_size=22, color=GOODC),
            label(r"gold: \ deterministic upper proxy $\inf_\tau E\,\mathrm{dist}^2$", font_size=22, color=SPHC),
            label(rf"$s = 10$: \ upper proxy ${d['curve'][i10]:.1f}$; \ half-success at $m = {half[10]}$", font_size=22, color=SPHC),
            label(r"no simulation was used to draw the curve", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The test, in a hundred dimensions. For each sparsity and each number of measurements, twenty random problems solved by basis pursuit. <bookmark mark='b'/> Green squares were always recovered exactly; red ones never. Part thirty-two drew this picture as an experiment. <bookmark mark='c'/> The gold curve is the deterministic infimum-of-expectations upper proxy, computed without simulation. <bookmark mark='d'/> At ten non-zero entries it is {say(d['curve'][i10], 1)}, and the empirical success rate first passes one half at {half[10]} measurements. <bookmark mark='e'/> With only twenty trials per square, the empirical crossing is coarse and uncertain. The upper proxy tracks the transition; it is not an exact finite-p fifty-percent threshold."     ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ deterministic upper proxy")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(q) for q in dots], lag_ratio=0.01), FadeIn(side[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(Create(curve), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def table(self):
        d = load("widths")
        rows = [[r"sparsity $s$ \ ($p = 100$)"] + [str(r["s"]) for r in d["cone"]],
                [r"$\inf_\tau E\,\mathrm{dist}^2$, \ upper bound"] + [f"{r['delta']:.1f}" for r in d["cone"]],
                [r"$E\min_\tau \mathrm{dist}^2$, \ simulated"] + [f"{r['dist2']:.1f}" for r in d["cone"]],
                [r"MC standard error"] + [f"{r['mcse']:.2f}" for r in d["cone"]],
                [r"$2s\log(p/s)$"] + [f"{2 * r['s'] * np.log(100 / r['s']):.1f}" for r in d["cone"]]]
        tab = table_rows(rows, font_size=26, col_buff=0.55, row_buff=0.4, colors=[GREY_B, SPHC, GAUSSC, GREY_B, GREY_A])
        if tab.width > 12.8:
            tab.width = 12.8
        tab.move_to([0, 0.9, 0])
        foot = label(r"$E\min_\tau\mathrm{dist}^2=\delta$; \ 10,000 draws; \ per-draw minimum solved exactly", font_size=24, color=GREY_A).move_to([0, -1.2, 0])
        foot2 = label(r"$2s\log(p/s)$, \ the textbook rate, \ overshoots most for the sparsest problems", font_size=24, color=BADC).move_to([0, -2.0, 0])
        c = d["cone"]
        with self.voiceover(
            f"<bookmark mark='a'/> A check of the formula. For each sparsity, the deterministic upper bound from the formula, and the simulated expected squared distance with the best threshold chosen for each draw: {say(c[3]['delta'], 1)} against {say(c[3]['dist2'], 1)} at ten. <bookmark mark='b'/> The per-draw minimization estimates the actual statistical dimension, with a reported Monte Carlo standard error; the deterministic formula is an upper bound. <bookmark mark='c'/> The familiar rate of two s log of p over s has the right shape, but it overshoots most for the sparsest problems: at ten, it is {say(2 * 10 * np.log(10), 1)}, against an upper proxy of {say(c[3]['delta'], 1)}. Only when s is a large fraction of p does it fall below, where its approximations no longer apply."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"simulated; \ deterministic upper proxy")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def beyond(self):
        rows = fit_rows(VGroup(
            label(r"the same recipe, \ any convex regularizer:", font_size=28, color=GREY_A),
            label(r"low-rank matrices by the nuclear norm: \ $\delta \le 3r(p_1 + p_2 - r)$ for rank $r$", font_size=26, color=MATC),
            label(r"sign vectors by the $\ell_\infty$ norm: \ $\delta = p/2$", font_size=26, color=MATC),
            label(r"demixing two signals: \ randomly oriented cones: \ transition near $\delta_1+\delta_2=p$", font_size=26, color=MATC),
            label(r"the price of a regularizer \ = \ the statistical dimension of its descent cone", font_size=26, color=SPHC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The recipe works for any convex regularizer. <bookmark mark='b'/> For a low-rank matrix recovered by minimizing the nuclear norm, the statistical dimension is at most three r times the sum of the dimensions minus r, a small multiple of the number of free parameters in a rank-r matrix. <bookmark mark='c'/> For a vector of signs recovered by the l-infinity norm, it is exactly half the dimension. <bookmark mark='d'/> For separating two superposed signals, each with its own regularizer, randomly oriented demixing succeeds with high probability when the sum of the statistical dimensions is below the ambient dimension by a sufficient finite-dimensional margin. <bookmark mark='e'/> The number of measurements a convex method needs is the statistical dimension of its descent cone, a single geometric number that can be computed before any data are collected."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
