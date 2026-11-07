from __future__ import annotations

import numpy as np

from videos.stats.stats61.common import *  # noqa: F403


class GradientFlows(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter eight. Gradient flows: sampling as optimization over distributions.", 8,
                            r"Gradient flows", r"Langevin, \ seen from Wasserstein space", lit=(1998,))
        self.jko()
        self.particles()
        self.kl_chart()
        self.rates()
        self.others()
        self.discretize()
        self.svgd()

    def jko(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Part twenty-seven's Langevin dynamics moves a particle along the gradient of the log "
            "density, plus noise. <bookmark mark='b'/> Richard Jordan, David Kinderlehrer and Felix Otto showed in 1998 what "
            "the law of the particle is doing: steepest descent of the Kullback–Leibler divergence to the target, in the "
            "Wasserstein geometry. <bookmark mark='c'/> Their scheme makes it a sequence of optimization problems: each step "
            "minimizes the divergence plus a Wasserstein penalty for moving far, the proximal step of Part twenty-one in a "
            "space of measures. <bookmark mark='d'/> The Fokker–Planck equation is the limit as the step size goes to zero.",
            [(r"\text{Langevin}", r":", r"dX_t = \nabla\log\pi(X_t)\,dt + \sqrt2\,dW_t", 40),
             (r"\text{its law}", r":", r"\partial_t\rho = \nabla\cdot\big(\rho\nabla\log(\rho/\pi)\big)", 40),
             (r"\text{JKO}", r":", r"\rho_{k+1} = \arg\min_\rho \mathrm{KL}(\rho\,\|\,\pi) + \tfrac{1}{2h}W_2^2(\rho, \rho_k)", 38),
             (r"h \to 0", r":", r"\text{the Fokker--Planck equation}", 40)],
            [r"Part 27", r"a Wasserstein gradient flow", r"Jordan, \ Kinderlehrer \& Otto (1998)", r"Part 21's proximal step"],
            colors=[(2, FLOWC)])

    def particles(self):
        d = load("langevin")
        snaps = [np.asarray(s) for s in d["snaps"]]
        Sig = np.asarray(d["Sig"])
        A = axes([-3.5, 5.5], [-4.5, 3.5], x_length=6.2, y_length=5.4, xlabel=r"", ylabel=r"", center=[-2.7, -0.1, 0])
        ax = A.ax
        w, V = np.linalg.eigh(Sig)
        th = np.linspace(0, 2 * np.pi, 120)
        E = (np.column_stack([np.cos(th), np.sin(th)]) * (2 * np.sqrt(w))) @ V.T
        ell = Polygon(*[ax.c2p(*p) for p in E], color=TGT, stroke_width=2.5).set_fill(TGT, opacity=0.08)
        cloud = VGroup(*[Dot(ax.c2p(*p), radius=0.035, color=FLOWC, fill_opacity=0.8) for p in snaps[0]])
        side = side_groups([
            [(r"gold: \ the target $N(0, \Sigma)$, \ $\rho = 0.8$", TGT), (r"(its 2-sd ellipse)", GREY_A)],
            [(r"teal: \ 300 of 600 particles from $N((4, -3), 0.2I)$", FLOWC), (rf"Euler--Maruyama, \ $h = {d['h']}$", GREY_A)],
            [(r"the cloud's law follows the flow", WHITE), (r"of KL in Wasserstein space", WHITE)],
        ], width=4.6, pos=(4.1, 0.2, 0))
        with self.voiceover(
            "<bookmark mark='a'/> A Gaussian target with correlation eight tenths, its two-standard-deviation ellipse in "
            "gold. <bookmark mark='b'/> Six hundred particles start far away, in a tight cloud, and each runs Langevin "
            "dynamics independently. <bookmark mark='c'/> Watch the cloud: it slides toward the target and spreads to fill "
            "it. No particle knows about the others; the deterministic gradient flow lives in the law of the cloud."
        ) as vo:
            self.play(FadeIn(A), FadeIn(ell), FadeIn(cloud), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            for S_ in snaps[1:12]:
                self.play(Transform(cloud, VGroup(*[Dot(ax.c2p(*p), radius=0.035, color=FLOWC, fill_opacity=0.8) for p in S_])), run_time=0.7, rate_func=linear)
        self.wait(1.0)
        self.clear_scene()

    def kl_chart(self):
        d = load("langevin")
        ts = np.asarray(d["ts"])
        ke, kp = np.asarray(d["kl_exact"]), np.asarray(d["kl_emp"])
        keep = ke > 1e-4
        A = axes([0, 6.2], [-4.2, 2.0], x_length=7.4, y_length=4.4, xlabel=r"time $t$", ylabel=r"$\mathrm{KL}(\rho_t \,\|\, \pi)$ (log scale)",
                 xticks=[0, 2, 4, 6], yticks=[2, 0, -2, -4], yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.5, 0.2, 0])
        ax = A.ax
        le = polyline(ax, ts[keep], np.log10(ke[keep]), FLOWC, 3.5)
        dots = VGroup(*[Dot(ax.c2p(t, np.log10(max(k, 1e-4))), radius=0.06, color=WHITE) for t, k in zip(ts, kp) if k > 6e-4])
        bound = polyline(ax, ts, np.log10(ke[0] * np.exp(-2 * d["rate"] * ts)), GREY_B, 2)
        side = side_groups([
            [(r"teal: \ the exact flow, \ Gaussian", FLOWC), (r"at every $t$", FLOWC)],
            [(r"white: \ the particles' fitted Gaussian", WHITE)],
            [(r"grey: \ the guarantee $e^{-2t/C_{\mathrm{LS}}}$", GREY_B), (rf"$C_{{\mathrm{{LS}}}} = \lambda_{{\max}}(\Sigma) = {1 / d['rate']:.1f}$", GREY_B)],
            [(r"the floor: \ sampling noise and Euler bias", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> For a Gaussian target and a Gaussian start, the flow stays Gaussian, with mean and covariance solving linear equations, so its Kullback–Leibler divergence is known exactly: the teal curve, from {say(ke[0], 0)} at the start. <bookmark mark='b'/> The particles' fitted Gaussian, in white, tracks it with discrepancies from both finite-particle noise and Euler bias. The exact discrete Gaussian law is also recorded; a finite atomic empirical measure itself has infinite KL to a continuous target. <bookmark mark='c'/> The grey line is the general guarantee: for a target with log-Sobolev constant C, the divergence falls at least like e to the minus two t over C. Here C is the largest variance, {say(1 / d['rate'], 1)}. <bookmark mark='d'/> The actual decay is faster at first, because the start is offset along the target's narrow direction, which contracts quickly."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"exact flow; \ particles simulated")))
            vo.wait_until("a")
            self.play(Create(le), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(dots, lag_ratio=0.1), FadeIn(side[1]), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(bound), FadeIn(side[2]))
            vo.wait_until("d")
        self.clear_scene()

    def rates(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The geometry gives the rates. <bookmark mark='b'/> If the target is strongly log-concave, "
            "the divergence is displacement convex, and the flow contracts in Wasserstein distance exponentially: the "
            "Bakry–Émery criterion. <bookmark mark='c'/> More generally, a log-Sobolev inequality is the Polyak–Łojasiewicz "
            "inequality of this space, and gives exponential decay of KL without convexity. <bookmark mark='d'/> Andre "
            "Wibisono, in 2018, made the dictionary explicit: Langevin is gradient descent, and its discretizations are "
            "familiar optimization schemes.",
            [(r"\pi \propto e^{-V}, \ \nabla^2 V \succeq \alpha I", r"\Rightarrow", r"W_2(\rho_t, \pi) \le e^{-\alpha t}W_2(\rho_0, \pi)", 36),
             (r"\text{LSI}", r":", r"\mathrm{KL}(\rho\,\|\,\pi) \le \tfrac{C}{2}\,I(\rho\,\|\,\pi)", 40),
             (r"\text{so}", r":", r"\mathrm{KL}(\rho_t\,\|\,\pi) \le e^{-2t/C}\,\mathrm{KL}(\rho_0\,\|\,\pi)", 40),
             (r"\text{dictionary}", r":", r"\text{sampling} \leftrightarrow \text{optimization}", 40)],
            [r"Bakry \& \'Emery (1985)", r"Fisher information $I$", r"the PL inequality's twin", r"Wibisono (2018)"],
            colors=[(2, FLOWC)])

    def discretize(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Euler discretization changes the continuous Langevin law. <bookmark mark='b'/> For a Gaussian target we can compute that discrete law exactly and separate its stationary bias from finite-particle noise. Under suitable strong convexity and smoothness, general Wasserstein discretization bounds have order root h with dimension-dependent constants; Gaussian bias can have a sharper order. <bookmark mark='c'/> Step-complexity bounds such as dimension over accuracy squared suppress condition numbers, initialization and logarithmic terms, and need stable step sizes and smoothness. <bookmark mark='d'/> A Metropolis correction restores the target invariant law under the usual conditions, rather than exact independent draws after finitely many steps. Hamiltonian methods offer different dynamics; calling all of them accelerated Wasserstein gradient descent would be too literal.",
            [(r"\text{ULA}", r":", r"X_{k+1} = X_k + h\nabla\log\pi(X_k) + \sqrt{2h}\,Z_k", 40),
             (r"\text{bias}", r":", r"W_2(\pi_h, \pi) = O(\sqrt h)", 40),
             (r"\text{steps}", r":", r"O(d/\varepsilon^2) \ \text{for strongly log-concave } \pi", 40),
             (r"\text{fixes}", r":", r"\text{MALA corrects invariant bias; \ HMC uses momentum}", 40)],
            [r"Euler--Maruyama", r"discretization", r"Dalalyan; \ Durmus \& Moulines", r"Part 27"],
            colors=[(1, NAIVEC2), (3, FLOWC)])

    def svgd(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Related variational particle methods use different geometries. <bookmark mark='b'/> Stein variational gradient descent uses a kernel-restricted transport direction, including attraction and repulsion; it is not simply the ordinary Wasserstein flow with the Brownian term removed. <bookmark mark='c'/> Product-law variational inference restricts the family of distributions and introduces approximation error. <bookmark mark='d'/> Mean-field limits of suitable wide two-layer networks describe training as a Wasserstein gradient flow over neuron-parameter laws under the model's scaling and assumptions.",
            [('Related variational and mean-field methods', GREY_A),
             (r"SVGD: \ kernel repulsion instead of noise \ (Liu \& Wang 2016)", FLOWC),
             (r"mean-field variational inference \ (Part 27)", ENTC),
             (r"wide two-layer networks \ (Mei et al.; \ Chizat \& Bach 2018)", TGT)], head_size=36)

    def others(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The same calculus covers more than one equation. <bookmark mark='b'/> The heat equation is "
            "the Wasserstein gradient flow of the entropy alone. <bookmark mark='c'/> Felix Otto showed in 2001 that the "
            "porous medium equation is the flow of a power of the density, and its rate of spreading follows from the "
            "geometry. <bookmark mark='d'/> Particles that attract or repel each other, McKean–Vlasov dynamics, follow the "
            "flow of an interaction energy: the same mathematics as the mean-field limits of neural networks below.",
            [(r"\int\rho\log\rho", r"\Rightarrow", r"\text{the heat equation}", 40),
             (r"\int\rho^m", r"\Rightarrow", r"\text{the porous medium equation}", 40),
             (r"\iint W(x - y)\,d\rho\,d\rho", r"\Rightarrow", r"\text{McKean--Vlasov dynamics}", 40),
             (r"\text{one calculus}", r":", r"\text{many equations}", 40)],
            [r"Jordan, \ Kinderlehrer \& Otto", r"Otto (2001)", r"mean-field particles", r"Otto's calculus"],
            colors=[(3, FLOWC)])
