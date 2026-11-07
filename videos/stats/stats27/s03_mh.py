from __future__ import annotations

import numpy as np

from videos.stats.stats27.common import *  # noqa: F403


class MH(VoiceoverScene):
    def construct(self):
        self.card()
        self.algorithm()
        self.balance()
        self.traces()
        self.tuning()
        self.dimension()
        self.mala()

    def card(self):
        card = chapter_card(2, r"Metropolis--Hastings", r"A Markov chain with the posterior as its limit", lit=(1953, 1970), part=PART)
        with self.voiceover("Chapter two. Metropolis–Hastings."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def algorithm(self):
        rows = [
            cmath(r"x' \sim q(x' \mid x)", r":", r"\text{propose}", font_size=30),
            cmath(r"\alpha(x, x')", r"=", r"\min\Bigl\{1, \ \dfrac{\pi(x')\, q(x \mid x')}{\pi(x)\, q(x' \mid x)}\Bigr\}", font_size=32),
            cmath(r"\text{accept}", r":", r"x \leftarrow x' \text{ with probability } \alpha; \ \text{else repeat } x", font_size=30),
            cmath(r"\text{symmetric } q", r":", r"\text{Metropolis's ratio } \pi(x')/\pi(x)", font_size=30),
        ]
        rows[1][2].set_color(SAMPLER)
        whys = [why(r"any proposal you can sample"), why(r"Hastings (1970): \ correct for asymmetry"),
                why(r"a rejection repeats the current point"), why(r"the 1953 rule")]
        with self.voiceover(
            "<bookmark mark='a'/> Wilfred Hastings generalized the rule in 1970. Propose a new point from any distribution "
            "q you can sample. <bookmark mark='b'/> Accept with probability the target ratio times the ratio of the "
            "proposal densities in reverse, which corrects for proposals that favour some directions. "
            "<bookmark mark='c'/> On rejection, the chain stays put, and the current point counts again; dropping repeats "
            "would bias the answer. <bookmark mark='d'/> For a symmetric proposal, the correction cancels, leaving the 1953 "
            "rule."
        ) as vo:
            intro = label('The Hastings correction accounts for proposal asymmetry', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def balance(self):
        rows = [
            cmath(r"\pi(x)\, K(x \to x')", r"=", r"\pi(x')\, K(x' \to x)", font_size=32),
            cmath(r"\pi(x)\, q(x' \mid x)\, \alpha(x, x')", r"=", r"\min\{\pi(x) q(x' \mid x), \ \pi(x') q(x \mid x')\}", font_size=28),
            cmath(r"\text{symmetric in } x, x'", r"\Rightarrow", r"\text{detailed balance holds}", font_size=30),
            cmath(r"\textstyle\int \pi(x) K(x \to x')\, dx", r"=", r"\pi(x'): \ \pi \text{ is stationary}", font_size=30),
        ]
        rows[3][2].set_color(HIT)
        whys = [why(r"Part 7's detailed balance"), why(r"multiply out the acceptance"), why(r"the same expression either way"),
                why(r"with recurrence and aperiodicity: \ convergence")]
        with self.voiceover(
            "<bookmark mark='a'/> Why it works is Part 7's detailed balance: the flow of probability from x to x prime equals "
            "the flow back. <bookmark mark='b'/> Multiply out: the flow from x to x prime is the smaller of two products, "
            "<bookmark mark='c'/> and that expression is symmetric, so the flows match. <bookmark mark='d'/> Integrating "
            "shows the target is stationary: a chain started from it stays there. If the chain can reach everywhere and "
            "doesn't cycle, it converges to the target from anywhere, and long-run averages converge to posterior "
            "expectations."
        ) as vo:
            intro = label('Detailed balance gives stationarity; convergence needs more', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def traces(self):
        d = load("rwm")
        tr = d["traces"]
        group = VGroup()
        curves = []
        for k, (key, name, col) in enumerate((("0.3", r"tiny steps: \ accept 88\%", RES), ("2.4", r"just right: \ accept 24\%", HIT),
                                              ("8.0", r"huge steps: \ accept 0.3\%", PATH))):
            v = np.asarray(tr[key])
            A = axes([0, 600], [-3.5, 3.5], x_length=11.0, y_length=1.5, xlabel=r"", ylabel=r"", xticks=[], yticks=[],
                     center=[0.3, 2.0 - 2.05 * k, 0])
            c = polyline(A.ax, np.arange(len(v)), v, col, 1.6)
            nm = label(name, font_size=22, color=col).next_to(A, UP, buff=0.08).align_to(A, LEFT).shift(RIGHT * 0.0)
            group.add(A)
            curves.append((c, nm))
        with self.voiceover(
            "<bookmark mark='a'/> The step size matters enormously. Six hundred iterations of the first coordinate of a "
            "twenty-dimensional normal. <bookmark mark='b'/> Tiny steps are almost always accepted, but the chain creeps, "
            "and neighbouring draws are nearly identical. <bookmark mark='c'/> Steps tuned to accept about a quarter of "
            "proposals explore quickly. <bookmark mark='d'/> Huge steps are almost always rejected, and the chain sits still "
            "for long stretches."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(group))
            for k, m_ in enumerate("bcd"):
                if k == 0:
                    vo.wait_until("a")
                vo.wait_until(m_)
                c, nm = curves[k]
                self.play(Create(c), FadeIn(nm), run_time=1.6)
        self.clear_scene()

    def tuning(self):
        d = load("rwm")
        ells, acc, e1 = np.asarray(d["ells"]), np.asarray(d["accept"]), np.asarray(d["ess_x1"])
        A = axes([0, 1], [0, 0.02], x_length=7.2, y_length=4.4, xlabel=r"acceptance rate", ylabel=r"ESS per iteration, \ $x_1$",
                 xticks=[0, 0.234, 0.5, 1], yticks=[0, 0.01, 0.02], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.2f}",
                 center=[-2.0, 0.3, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, e), radius=0.08, color=SAMPLER) for a, e in zip(acc, e1)])
        order = np.argsort(acc)
        line = polyline(ax, acc[order], e1[order], SAMPLER, 2.5)
        mark = DashedLine(ax.c2p(0.234, 0), ax.c2p(0.234, 0.02), color=PATH, stroke_width=2.5)
        rows = fit_rows(VGroup(
            label(r"20-dimensional normal; \ steps $\ell/\sqrt{d}$", font_size=22),
            label(r"each dot: \ one step size, \ 20,000 iterations", font_size=22, color=SAMPLER),
            label(r"best near 0.23: \ about 1.6 effective draws per 100", font_size=22, color=PATH),
            label(r"Roberts, Gelman \& Gilks (1997): \ 0.234 as $d \to \infty$", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Measure it. For a range of step sizes, the acceptance rate against the effective "
            "sample size per iteration. <bookmark mark='b'/> Efficiency rises and then falls. <bookmark mark='c'/> "
            "The peak is near an acceptance rate of a quarter, where the chain gives about one point six effective "
            "draws per hundred iterations. <bookmark mark='d'/> For a smooth product-target limit and an isotropic "
            "random walk, Gareth Roberts, Andrew Gelman and Wally Gilks proved an optimal acceptance rate tending to "
            "point two three four, with the step shrinking like one over the square root of the dimension."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.1), Create(line), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(mark), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def dimension(self):
        rows = [
            cmath(r"\text{step}", r"\propto", r"d^{-1/2}", font_size=32),
            cmath(r"\text{iterations to move } O(1)", r"\propto", r"d", font_size=32),
            cmath(r"\text{correlated posteriors}", r":", r"\text{the step is set by the narrowest direction}", font_size=28),
            cmath(r"\text{the fix}", r":", r"\text{use the gradient: \ chapter five}", font_size=30),
        ]
        rows[3][2].set_color(HIT)
        whys = [why(r"or almost every proposal is rejected"), why(r"a diffusion: \ distance grows like $\sqrt{\text{steps}}$"),
                why(r"and the chain crawls along the wide one"), why(r"Hamiltonian Monte Carlo")]
        with self.voiceover(
            "<bookmark mark='a'/> The trouble is scaling. In that product-target limit, the proposal SD shrinks like "
            "one over root d, <bookmark mark='b'/> and a random walk's distance grows only like the square root of "
            "the number of steps, so crossing the posterior takes a number of iterations proportional to d. <bookmark"
            " mark='c'/> With correlated parameters it's worse: the step is limited by the narrowest direction, and "
            "the chain crawls along the widest. <bookmark mark='d'/> The way out is to stop guessing directions and "
            "follow the gradient, chapter five's Hamiltonian Monte Carlo."
        ) as vo:
            intro = label('Scaling comparisons require a specified target and work count', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mala(self):
        rows = [
            cmath(r"\text{independence}", r":", r"q(x') \text{ ignores } x: \ \text{good only if } q \approx \pi", font_size=28),
            cmath(r"\text{Langevin (MALA)}", r":", r"x' = x + \tfrac{\epsilon^2}{2}\nabla\log\pi(x) + \epsilon\, \xi", font_size=30),
            cmath(r"\text{optimal}", r":", r"\text{accept } 0.574; \ \epsilon^2\propto d^{-1/3}, \ \epsilon\propto d^{-1/6}", font_size=30),
            cmath(r"\text{HMC}", r":", r"\text{many gradient steps, \ step } \propto d^{-1/4}", font_size=30),
        ]
        rows[1][-1].set_color(SAMPLER)
        whys = [why(r"chapter one's proposal, \ as a chain"), why(r"drift up the gradient, \ plus noise"), why(r"Roberts \& Rosenthal (1998): \ smooth product targets"), why(r"chapter five")]
        with self.voiceover(
            "<bookmark mark='a'/> Other proposals fill the gap. An independence sampler proposes from a fixed "
            "distribution, chapter one's proposal turned into a chain, and works only when that distribution "
            "resembles the target. <bookmark mark='b'/> The Metropolis-adjusted Langevin algorithm drifts each "
            "proposal up the gradient of the log density before adding noise. <bookmark mark='c'/> For smooth product"
            " targets, its limiting optimal acceptance is point five seven four. The squared noise scale shrinks like"
            " d to the minus one third, so the noise SD epsilon shrinks like d to the minus one sixth. <bookmark "
            "mark='d'/> For HMC on suitable product targets at fixed integration time, the leapfrog step scales like "
            "d to the minus one quarter. These rules describe particular asymptotic settings, not every posterior or "
            "a universal cost ranking."
        ) as vo:
            intro = label('MALA noise SD scales differently from its squared step', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
