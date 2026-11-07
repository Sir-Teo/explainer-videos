from __future__ import annotations

import numpy as np

from videos.stats.stats27.common import *  # noqa: F403


class NUTS(VoiceoverScene):
    def construct(self):
        self.card()
        self.uturn()
        self.trajectory()
        self.adaptation()
        self.depths()
        self.divergences()
        self.discrete()

    def card(self):
        card = chapter_card(6, r"NUTS", r"Stop when the path turns back", lit=(2014,), part=PART)
        with self.voiceover("Chapter six. The No-U-Turn Sampler."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def uturn(self):
        rows = [
            cmath(r"\text{build}", r":", r"\text{a trajectory forwards and backwards in time, \ doubling}", font_size=28),
            cmath(r"\text{stop when}", r":", r"(q^+-q^-)^\top M^{-1}p^-<0 \ \text{or } (q^+-q^-)^\top M^{-1}p^+<0", font_size=30),
            cmath(r"\text{choose}", r":", r"\text{a point from the trajectory, \ preserving detailed balance}", font_size=28),
            cmath(r"\text{cost}", r":", r"\text{adaptive path length, \ limited by maximum depth}", font_size=30),
        ]
        rows[1][2].set_color(SAMPLER)
        whys = [why(r"1, 2, 4, 8, \ldots\ leapfrog steps"), why(r"an end starts moving back towards the other"),
                why(r"Hoffman \& Gelman (2014)"), why(r"$L$ adapts, \ every iteration")]
        with self.voiceover(
            "<bookmark mark='a'/> Matthew Hoffman and Andrew Gelman's No-U-Turn Sampler removes the number of steps. "
            "From the current point it builds a trajectory both forwards and backwards in time, doubling its length "
            "each round: one step, two, four, eight. <bookmark mark='b'/> It stops when the path starts to turn back "
            "on itself, when either end's momentum points back towards the other end. <bookmark mark='c'/> The next "
            "point is then drawn from the trajectory in a way that keeps detailed balance, the subtle part of the "
            "algorithm. <bookmark mark='d'/> The path length responds to local geometry, with a maximum-depth "
            "safeguard. A U-turn is a stopping rule, not proof that an iteration did all the exploration needed."
        ) as vo:
            intro = label('NUTS stops when endpoint velocities turn back', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def trajectory(self):
        d = load("nuts")
        rho = d["rho"]
        A = axes([-3, 3], [-3, 3], x_length=5.0, y_length=5.0, xlabel=r"$x_1$", ylabel=r"$x_2$", xticks=[-2, 0, 2], yticks=[-2, 0, 2],
                 center=[-3.0, 0.1, 0])
        ax = A.ax
        L = Landscape(ax, lambda X, Y: np.exp(-0.5 * (X ** 2 - 2 * rho * X * Y + Y ** 2) / (1 - rho ** 2)), (-3, 3), (-3, 3),
                      levels=[0.6, 0.3, 0.1, 0.02], color=EXACTC, stroke_width=1.5)
        groups = []
        cols = [PATH, SAMPLER, HIT]
        for k, t in enumerate(d["trajs"]):
            pts = np.asarray(t["path"])
            dots = VGroup(*[Dot(ax.c2p(*p), radius=0.045, color=cols[k]) for p in pts])
            line = polyline(ax, pts[:, 0], pts[:, 1], cols[k], 1.8, 0.8)
            end = Dot(ax.c2p(*t["end"]), radius=0.1, color=cols[k]).set_stroke(WHITE, 2)
            groups.append((line, dots, end, t))
        rows = fit_rows(VGroup(
            label(rf"a normal with correlation {rho}", font_size=22, color=EXACTC),
            label(rf"iteration 1: \ depth {d['trajs'][0]['depth']}, \ {d['trajs'][0]['n']} leapfrog steps", font_size=22, color=cols[0]),
            label(rf"iteration 2: \ depth {d['trajs'][1]['depth']}, \ {d['trajs'][1]['n']} steps", font_size=22, color=cols[1]),
            label(rf"iteration 3: \ depth {d['trajs'][2]['depth']}, \ {d['trajs'][2]['n']} steps", font_size=22, color=cols[2]),
            label(r"ringed: \ the point chosen", font_size=22, color=GREY_A),
        ), 5.6, 0.42, [3.6, 0.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Three NUTS iterations on a correlated normal. <bookmark mark='b'/> The first builds a "
            "trajectory of seven leapfrog steps, both ways from the start, until it has swept along the valley and begun to "
            "turn. <bookmark mark='c'/> The second, starting from the chosen point, needs fifteen, <bookmark mark='d'/> the "
            "third seven again. <bookmark mark='e'/> The ringed dots are the points chosen: each far from where its "
            "iteration began."
        ) as vo:
            self.play(FadeIn(A), FadeIn(L.levels))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                line, dots, end, t = groups[k]
                self.play(Create(line), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.05), FadeIn(rows[k + 1]), run_time=1.6)
                self.play(FadeIn(end, scale=1.5))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def adaptation(self):
        rows = [
            cmath(r"\epsilon", r":", r"\text{dual averaging to a target acceptance, \ 0.8}", font_size=30),
            cmath(r"M^{-1}", r":", r"\text{the variance of the draws, \ in doubling windows}", font_size=30),
            cmath(r"\text{warmup}", r":", r"\text{initial buffer, \ expanding windows, \ final step-size buffer}", font_size=28),
            cmath(r"\text{after warmup}", r":", r"\text{freeze them: \ a valid Markov chain}", font_size=30),
        ]
        rows[1][2].set_color(SAMPLER)
        whys = [why(r"Nesterov's dual averaging, \ adapted"), why(r"the posterior's scales"),
                why(r"simplified Stan-inspired schedule"), why(r"ongoing adaptation needs additional conditions")]
        with self.voiceover(
            "<bookmark mark='a'/> The step size and mass matrix are learned during warmup. The step size by dual "
            "averaging, an optimization method that adjusts it until the average acceptance probability is point "
            "eight. <bookmark mark='b'/> The inverse mass matrix is estimated from draw variances in expanding "
            "windows. <bookmark mark='c'/> Statkit uses a simplified schedule inspired by Stan, with initial and "
            "terminal buffers proportional to warmup length; it is not Stan's exact production implementation. "
            "<bookmark mark='d'/> Then both are frozen for ordinary Markov-chain sampling. Continuing adaptation "
            "requires additional adaptive-MCMC conditions; it is not automatically invalid. Warmup draws are "
            "discarded."
        ) as vo:
            intro = label('Adapt step size and inverse mass during warmup', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def depths(self):
        d = load("nuts")
        counts = np.asarray(d["depth_counts"], float)
        A = axes([0.4, 7.6], [0, float(counts.max()) * 1.15], x_length=7.2, y_length=4.2, xlabel=r"tree depth",
                 ylabel=r"iterations", xticks=list(range(1, 8)), yticks=[], center=[-2.0, 0.3, 0])
        ax = A.ax
        bars = bars_at(ax, list(range(1, 8)), counts[1:8], 0.7, SAMPLER, 0.85)
        rows = fit_rows(VGroup(
            label(r"eight schools, \ non-centred; \ $\delta=0.9$, \ 4 chains $\times$ 1,000", font_size=22),
            label(rf"mostly depth 3: \ 7 leapfrog steps; \ mean {d['mean_leapfrog']:.1f}", font_size=22, color=SAMPLER),
            label(rf"adapted step {d['eps_final']:.2f}", font_size=22, color=GREY_A),
            label(rf"$\hat R(\log\tau) = {d['rhat_tau']:.3f}$; \ ESS {d['ess_tau']:,.0f}; \ {d['divergent']} divergences", font_size=22, color=HIT),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the eight schools, written in the non-centred form chapter seven explains, four "
            "chains of a thousand. <bookmark mark='b'/> Most iterations need a tree of depth three, seven leapfrog "
            "steps, about eight on average. <bookmark mark='c'/> The caption reports the average adapted step size of"
            " these four chains. <bookmark mark='d'/> R-hat for log tau is one point oo two, the effective sample "
            "size about eighteen hundred, and there are no divergences: a clean run."
        ) as vo:
            self.add(schools_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def divergences(self):
        rows = [
            cmath(r"\text{divergence}", r":", r"\text{large energy error; \ original slice NUTS uses a slice threshold}", font_size=30),
            cmath(r"\text{cause}", r":", r"\text{curvature the step size cannot follow}", font_size=30),
            cmath(r"\text{symptom}", r":", r"\text{possible under-exploration and biased finite-run estimates}", font_size=30),
            cmath(r"\text{treat}", r":", r"\text{never ignore; \ reparametrize}", font_size=30),
        ]
        rows[2][2].set_color(DIV)
        whys = [why(r"the energy blows up"), why(r"a funnel's neck, \ a sharp ridge"), why(r"a warning, \ with a location"),
                why(r"chapter seven")]
        with self.voiceover(
            "<bookmark mark='a'/> HMC has one more gift: it reports its own failures. If the energy along a "
            "trajectory suddenly explodes, the trajectory has diverged. <bookmark mark='b'/> That happens where the "
            "posterior's curvature changes faster than the step size can follow, in a narrow neck or a sharp ridge. "
            "<bookmark mark='c'/> The sampler then can't enter that region properly, and finite-run estimates may be "
            "biased, sometimes without another obvious warning. <bookmark mark='d'/> So a divergence is never to be "
            "ignored. Usually the fix is to change the parametrization, as the next chapter shows."
        ) as vo:
            intro = label('Large integration errors warn of difficult geometry', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def discrete(self):
        rows = [
            cmath(r"\text{HMC needs}", r":", r"\text{differentiable continuous coordinates; \ transform constraints}", font_size=30),
            cmath(r"\text{discrete parameters}", r":", r"\text{a mixture's labels, \ a change point}", font_size=30),
            cmath(r"\text{marginalize}", r":", r"p(y \mid \theta) = \textstyle\sum_k \pi_k\, p(y \mid \theta_k)", font_size=30),
            cmath(r"\text{then}", r":", r"\text{recover the labels afterwards, \ draw by draw}", font_size=30),
        ]
        rows[2][-1].set_color(HIT)
        whys = [why(r"gradients, \ everywhere"), why(r"no derivative to follow"), why(r"Part 31's mixtures, \ by the sum rule"), why(r"by Bayes's rule, \ per draw")]
        with self.voiceover(
            "<bookmark mark='a'/> One limitation of all gradient-based samplers: standard HMC needs differentiable "
            "continuous coordinates in the region it explores, often after transforming constrained parameters. "
            "<bookmark mark='b'/> Discrete unknowns, like which component of a mixture each observation came from, or"
            " the time of a change point, have no gradient. <bookmark mark='c'/> The standard remedy is to sum them "
            "out of the likelihood, which for a mixture gives the familiar weighted sum of densities. <bookmark "
            "mark='d'/> Their posterior can then be recovered afterwards, one draw at a time."
        ) as vo:
            intro = label('Marginalization can remove discrete latent parameters', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
