from __future__ import annotations

import numpy as np

from videos.stats.stats27.common import *  # noqa: F403


class HMC(VoiceoverScene):
    def construct(self):
        self.card()
        self.physics()
        self.leapfrog()
        self.phase()
        self.puck()
        self.dimension()
        self.metric()
        self.tuning()

    def card(self):
        card = chapter_card(5, r"Hamiltonian Monte Carlo", r"Slide, \ don't stumble", lit=(1987,), part=PART)
        with self.voiceover("Chapter five. Hamiltonian Monte Carlo."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def physics(self):
        rows = [
            cmath(r"U(q)", r"=", r"-\log \pi(q): \ \text{a landscape}", font_size=30),
            cmath(r"H(q, p)", r"=", r"U(q) + \tfrac12 p^\top M^{-1} p", font_size=32),
            cmath(r"\dot q = M^{-1} p", r",", r"\ \ \dot p = -\nabla U(q)", font_size=32),
            cmath(r"\text{flow}", r":", r"\text{keeps } H, \ \text{keeps volume, \ is reversible}", font_size=30),
        ]
        rows[2][-1].set_color(SAMPLER)
        whys = [why(r"low where the posterior is high"), why(r"potential plus kinetic energy"),
                why(r"Hamilton's equations: \ the gradient pushes"), why(r"exactly what detailed balance needs")]
        with self.voiceover(
            "<bookmark mark='a'/> Hamiltonian Monte Carlo, invented by Simon Duane and colleagues in 1987 for lattice "
            "physics and brought to statistics by Radford Neal, turns the posterior into a landscape: the potential energy "
            "is minus the log density, low where the posterior is high. <bookmark mark='b'/> Give the position a random "
            "momentum, and add its kinetic energy. <bookmark mark='c'/> Then let physics run: Hamilton's equations, the "
            "position moving with the momentum and the momentum pushed by the slope. <bookmark mark='d'/> The exact flow "
            "conserves energy, preserves volume and runs backwards as well as forwards, exactly the properties a valid "
            "proposal needs, so a puck sent sliding across the landscape lands somewhere far away that is still probable."
        ) as vo:
            intro = label('Hamiltonian dynamics combine a target landscape and momentum', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def leapfrog(self):
        rows = [
            cmath(r"p", r"\leftarrow", r"p - \tfrac{\epsilon}{2}\nabla U(q)", font_size=32),
            cmath(r"q", r"\leftarrow", r"q + \epsilon M^{-1} p", font_size=32),
            cmath(r"p", r"\leftarrow", r"p - \tfrac{\epsilon}{2}\nabla U(q)", font_size=32),
            cmath(r"\text{then}", r":", r"\text{accept with } \min\{1, e^{-H(q', p') + H(q, p)}\}", font_size=30),
        ]
        rows[3][2].set_color(HIT)
        whys = [why(r"half a kick"), why(r"a full drift"), why(r"half a kick"), why(r"corrects the small energy error")]
        with self.voiceover(
            "<bookmark mark='a'/> The computer can't follow the exact flow, so it takes leapfrog steps: half a kick to the "
            "momentum from the gradient, <bookmark mark='b'/> a full step of the position, <bookmark mark='c'/> and another "
            "half kick. <bookmark mark='d'/> After L steps, accept the end point with the Metropolis probability of the "
            "change in total energy. The integrator is volume-preserving and reversible, so this correction is exact, and "
            "because its energy error stays small the acceptance rate stays high."
        ) as vo:
            intro = label('A reversible, volume-preserving step with a Metropolis correction', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def phase(self):
        d = load("hmc")
        A = axes([-3, 3], [-3, 3], x_length=4.8, y_length=4.8, xlabel=r"position $q$", ylabel=r"momentum $p$",
                 xticks=[-2, 0, 2], yticks=[-2, 0, 2], center=[-3.0, 0.1, 0])
        ax = A.ax
        circ = ParametricFunction(lambda t: ax.c2p(np.cos(t), np.sin(t)), t_range=[0, TAU], color=EXACTC, stroke_width=2)
        eu = np.asarray(d["euler"])
        out = np.flatnonzero(np.any(np.abs(eu) >= 3, axis=1))
        stop = int(out[0]) if len(out) else len(eu)
        e_line = polyline(ax, eu[:stop, 0], eu[:stop, 1], RES, 2.2)
        lf = np.asarray(d["leapfrog"])
        l_line = polyline(ax, lf[:, 0], lf[:, 1], HIT, 2.6)
        rows = fit_rows(VGroup(
            label(r"a spring: \ $H = (q^2 + p^2)/2$, \ the exact orbit in gold", font_size=22, color=EXACTC),
            label(rf"red: \ Euler's method, \ $\epsilon = {d['eps']}$: \ spirals out", font_size=22, color=RES),
            label(rf"energy after 60 steps: \ 0.5 $\to$ {d['H_euler'][-1]:.0f}", font_size=22, color=RES),
            label(r"green: \ leapfrog: \ stays on a nearby orbit", font_size=22, color=HIT),
            label(rf"its energy error: \ never above {max(abs(np.asarray(d['H_lf']) - 0.5)):.3f}", font_size=22, color=HIT),
        ), 5.8, 0.42, [3.6, 0.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why leapfrog, and not the obvious method? A spring, whose exact orbits in position "
            "and momentum are circles. <bookmark mark='b'/> Euler's method, update both from the old values, spirals "
            "outwards: <bookmark mark='c'/> after sixty steps its energy has grown from a half to eighty-eight. "
            "<bookmark mark='d'/> For this stable harmonic oscillator, leapfrog stays on a slightly squashed orbit, "
            "<bookmark mark='e'/> its absolute energy error staying below about point oh one one over these sixty "
            "steps. Symplectic methods often keep energy error controlled for long times under suitable stability "
            "conditions; they do not exactly conserve a nearby energy for every nonlinear model."
        ) as vo:
            self.play(FadeIn(A), Create(circ))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(e_line), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(l_line), FadeIn(rows[3]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def puck(self):
        d = load("hmc")
        rho = d["rho"]
        Si = np.linalg.inv(np.array([[1, rho], [rho, 1]]))
        U = lambda x, y: 0.5 * (Si[0, 0] * x * x + 2 * Si[0, 1] * x * y + Si[1, 1] * y * y)  # noqa: E731
        Ps = PuckSurface(U, (-2.6, 2.6), (-2.6, 2.6), n=16, width=7.6, height=4.6, z_cap=6.0, center=[-1.6, -0.1, 0],
                         color=GREY_B)
        paths = [np.asarray(p) for p in d["paths"]]
        trails = VGroup(*[Ps.path(p, color=PATH if k % 2 == 0 else SAMPLER, stroke_width=3) for k, p in enumerate(paths[:5])])
        pucks = VGroup(*[Ps.puck(*p[-1], color=HIT) for p in paths[:5]])
        rows = fit_rows(VGroup(
            label(r"the bowl: \ $U = -\log\pi$ for a correlation-0.9 normal", font_size=22, color=GREY_A),
            label(r"each trajectory: \ 25 leapfrog steps from a random kick", font_size=22, color=PATH),
            label(r"the puck slides along the valley floor", font_size=22, color=SAMPLER),
            label(rf"accepted {100 * d['accept2']:.0f}\% of the trajectories", font_size=22, color=HIT),
        ), 4.0, 0.42, [5.0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is the picture to keep in mind. The surface is the potential energy of a strongly "
            "correlated normal posterior: a long, narrow valley. <bookmark mark='b'/> Each iteration flicks the puck in a "
            "random direction and lets it slide for twenty-five leapfrog steps. <bookmark mark='c'/> It climbs the valley "
            "walls, falls back, and travels along the floor, covering in one iteration a distance a random walk would need "
            "hundreds of steps to cover. <bookmark mark='d'/> Every trajectory here was accepted."
        ) as vo:
            self.play(Create(Ps.wire), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(trails[0]), FadeIn(pucks[0]), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(t) for t in trails[1:]], lag_ratio=0.4), LaggedStart(*[FadeIn(p) for p in pucks[1:]], lag_ratio=0.4),
                      FadeIn(rows[2]), run_time=4.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def dimension(self):
        d = load("hmc")
        th, tr = np.asarray(d["trace_hmc"]), np.asarray(d["trace_rwm"])
        group = VGroup()
        lines = []
        for k, (v, name, col) in enumerate(((tr, r"random walk", RES), (th, r"HMC", HIT))):
            A = axes([0, len(v)], [-3.5, 3.5], x_length=6.6, y_length=1.8, xlabel=r"", ylabel=r"", xticks=[], yticks=[],
                     center=[-2.6, 1.3 - 2.6 * k, 0])
            lines.append(polyline(A.ax, np.arange(len(v)), v, col, 1.6))
            group.add(A, label(name, font_size=22, color=col).next_to(A, UP, buff=0.1).align_to(A, LEFT))
        rows = fit_rows(VGroup(
            label(r"100 dimensions, \ scales from 0.01 to 1", font_size=22),
            label(r"widest coordinate; \ illustrative traces at different subsampling", font_size=22, color=GREY_A),
            label(rf"random walk: \ {d['ess_rwm_per_1000']:.2f} effective draws per 1,000 evaluations", font_size=22, color=RES),
            label(rf"HMC: \ {d['ess_hmc_per_1000']:.1f} per 1,000 gradient evaluations", font_size=22, color=HIT),
            label(r"about 140 times by this retained-run count; \ excludes warmup", font_size=22, color=HIT),
        ), 4.6, 0.42, [4.3, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Radford Neal's demonstration: a hundred-dimensional normal whose coordinates have "
            "scales from point oh one to one. <bookmark mark='b'/> The traces show the widest coordinate, The "
            "displayed traces have different subsampling and are illustrative. The efficiency figures below count "
            "retained-run work, excluding warmup, and distinguish density evaluations from gradients. <bookmark "
            "mark='c'/> The random walk, its step held small by the narrowest coordinate, crawls: about point oh five"
            " effective draws per thousand evaluations. <bookmark mark='d'/> HMC gives six point three. <bookmark "
            "mark='e'/> Counting a gradient as one evaluation, that's about a hundred and forty times the efficiency,"
            " for this coordinate in these runs. Short-run ESS estimates are uncertain, and the ratio is not a "
            "universal dimension-dependent speedup."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(group))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(lines[0]), Create(lines[1]), FadeIn(rows[1]), run_time=2.5)
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def tuning(self):
        rows = [
            cmath(r"\epsilon \text{ too large}", r":", r"\text{energy errors, \ rejections}", font_size=30),
            cmath(r"L \text{ too small}", r":", r"\text{a random walk again}", font_size=30),
            cmath(r"L \text{ too large}", r":", r"\text{the puck comes back: \ wasted work}", font_size=30),
            cmath(r"M", r":", r"\text{mass matrix: \ } M^{-1}\approx\mathrm{Cov}(\theta\mid y)", font_size=30),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"the step size"), why(r"the number of steps"), why(r"near-return can waste work; \ not every orbit is periodic"),
                why(r"rescales the landscape to round")]
        with self.voiceover(
            "<bookmark mark='a'/> The catch is tuning. Too large a step size, and the energy errors cause rejections."
            " <bookmark mark='b'/> Too few steps, and HMC degenerates into a random walk. <bookmark mark='c'/> Too "
            "many, and the puck, on its periodic orbit, comes back to where it started, wasting every gradient in "
            "between. <bookmark mark='d'/> With the kinetic-energy convention used here, the inverse mass matrix "
            "should approximate the posterior covariance, so that Gaussian dynamics have similar frequencies. "
            "Choosing all three automatically is what NUTS does."
        ) as vo:
            intro = label('Step size, path length and inverse mass control dynamics', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def metric(self):
        rows = [
            cmath(r"M^{-1}", r"\approx", r"\mathrm{Cov}(\theta \mid y): \ \text{a round landscape}", font_size=30),
            cmath(r"\text{diagonal}", r":", r"\text{rescales each parameter: \ Stan's default}", font_size=30),
            cmath(r"\text{dense}", r":", r"\text{also undoes linear correlations}", font_size=30),
            cmath(r"\text{Riemannian}", r":", r"M(\theta) \text{ changes with position: \ funnels too}", font_size=30),
        ]
        rows[0][-1].set_color(HIT)
        whys = [why(r"precondition the dynamics"), why(r"learned in warmup"), why(r"costs $d^2$"), why(r"Girolami \& Calderhead (2011)")]
        with self.voiceover(
            "<bookmark mark='a'/> The mass matrix is HMC's preconditioner. Set its inverse to the posterior covariance, and "
            "the landscape the puck sees becomes round. <bookmark mark='b'/> A diagonal one, Stan's default, rescales each "
            "parameter to unit spread. <bookmark mark='c'/> A dense one also removes linear correlations, at a cost of d "
            "squared. <bookmark mark='d'/> Mark Girolami and Ben Calderhead's Riemannian HMC lets it vary with position, "
            "adapting to curvature that changes from place to place, as in a funnel, at a higher cost per step."
        ) as vo:
            intro = label('Inverse mass approximates covariance in this convention', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
