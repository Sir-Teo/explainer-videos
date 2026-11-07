from __future__ import annotations

import numpy as np

from videos.stats.stats27.common import *  # noqa: F403


def spin_grid(state, cell=0.22, center=ORIGIN):
    s = np.asarray(state)
    L = s.shape[0]
    g = VGroup()
    for i in range(L):
        for j in range(L):
            g.add(Square(side_length=cell, stroke_width=0, fill_opacity=1,
                         fill_color=SAMPLER if s[i, j] > 0 else "#1b2230").move_to([(j - L / 2 + 0.5) * cell, (L / 2 - i - 0.5) * cell, 0]))
    return g.move_to(center)


class CFTP(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.idea()
        self.ising()
        self.coalescence()
        self.coupling_now()
        self.limits()

    def card(self):
        card = chapter_card(13, r"Exact sampling", r"Coupling from the past", lit=(1996,), part=PART)
        with self.voiceover("Chapter thirteen. Exact sampling."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = fit_rows(VGroup(
            label(r"every chain so far is only approximately at its target", font_size=26),
            label(r"how long is long enough? \ diagnostics can only warn", font_size=26, color=RES),
            label(r"Propp \& Wilson (1996): \ sometimes we can know, \ and stop exactly", font_size=26, color=HIT),
        ), 12.4, 0.7, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Every chain in this part reaches its target only in the limit. After any finite run it is "
            "approximately there, and chapter four's diagnostics can only warn when it isn't. <bookmark mark='b'/> How long "
            "is long enough? <bookmark mark='c'/> In 1996 James Propp and David Wilson showed that for some chains the "
            "question has an exact answer, and a sampler can stop knowing its draw is perfect."
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def idea(self):
        rows = [
            cmath(r"\text{run from } t = -T \text{ to } 0", r":", r"\text{from every starting state, \ the same random numbers}", font_size=28),
            cmath(r"\text{all coalesce by } t = 0", r"\Rightarrow", r"\text{the state at } 0 \text{ is an exact draw}", font_size=28),
            cmath(r"\text{else}", r":", r"T \leftarrow 2T, \ \text{reusing the old random numbers}", font_size=30),
            cmath(r"\text{monotone chains}", r":", r"\text{track only the top and bottom states}", font_size=30),
        ]
        rows[1][2].set_color(HIT)
        whys = [why(r"coupling from the past"), why(r"as if run from $-\infty$"), why(r"not from the future: \ that biases it"),
                why(r"everything else is sandwiched between")]
        with self.voiceover(
            "<bookmark mark='a'/> Imagine running the chain from time minus T to zero, from every possible starting state at "
            "once, all driven by the same random numbers. <bookmark mark='b'/> If every copy has merged into one state by "
            "time zero, that state doesn't depend on where the chain began, so it is what a chain started infinitely long "
            "ago would show: an exact draw from the stationary distribution. <bookmark mark='c'/> If they haven't merged, go "
            "further back, doubling T and reusing the same random numbers for the most recent times; running forwards until "
            "coalescence instead would bias the result. <bookmark mark='d'/> For monotone chains we needn't track every state: "
            "only the highest and the lowest, since every other copy is trapped between them."
        ) as vo:
            intro = label('Replay shared randomness from the past until all states coalesce', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ising(self):
        rows = [
            cmath(r"\pi(s)", r"\propto", r"\exp\bigl\{\beta \textstyle\sum_{i \sim j} s_i s_j\bigr\}, \ \ s_i = \pm 1", font_size=30),
            cmath(r"\text{heat bath}", r":", r"P(s_i = +1 \mid \text{neighbours}) = \tfrac{1}{1 + e^{-2\beta h_i}}", font_size=30),
            cmath(r"\text{monotone}", r":", r"\text{more } + \text{ neighbours } \Rightarrow \text{ more likely } +", font_size=30),
            cmath(r"\text{top and bottom}", r":", r"\text{all } +1, \ \text{all } -1", font_size=30),
        ]
        rows[0][2].set_color(SAMPLER)
        whys = [why(r"the Ising model: \ Part 22's pseudo-likelihood"), why(r"Gibbs for one spin"),
                why(r"ferromagnetic $\beta\ge0$: \ order preserved"), why(r"two chains bound every other")]
        with self.voiceover(
            "<bookmark mark='a'/> Propp and Wilson's showcase was the Ising model of Part 22: spins on a grid, plus or minus "
            "one, preferring to agree with their neighbours, more strongly as beta grows. <bookmark mark='b'/> The Gibbs "
            "update sets one spin to plus with a probability that rises with the sum of its neighbours. "
            "<bookmark mark='c'/> Using one shared uniform for every copy, a configuration with more plus spins stays above "
            "one with fewer: the coupling is monotone. <bookmark mark='d'/> So it is enough to run two chains, from all plus "
            "and all minus."
        ) as vo:
            intro = label('Ferromagnetic heat-bath updates preserve the spin order', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def coalescence(self):
        d = load("cftp")
        group = VGroup()
        anims = []
        for k, key in enumerate(("warm", "near")):
            D = d[key]
            mags = np.asarray(D["mags"])
            T = D["T"]
            A = axes([0, T], [-1.05, 1.05], x_length=5.0, y_length=2.6, xlabel=rf"time from $-{T}$ to 0, \ $\beta = {D['beta']}$",
                     ylabel=r"magnetization", xticks=[], yticks=[-1, 0, 1], center=[-3.3 + 6.6 * k, 1.4, 0])
            top = polyline(A.ax, np.arange(1, T + 1), mags[:, 0], HIT, 2.2)
            bot = polyline(A.ax, np.arange(1, T + 1), mags[:, 1], RES, 2.2)
            grid = spin_grid(D["state"], cell=0.13, center=[-3.3 + 6.6 * k, -1.7, 0])
            group.add(A)
            anims.append((top, bot, grid, T))
        rows = fit_rows(VGroup(
            label(r"green: \ from all $+$; \ red: \ from all $-$; \ $16 \times 16$ spins", font_size=22),
            label(rf"$\beta = 0.3$: \ coalesced from $T = {d['warm']['T']}$", font_size=22, color=HIT),
            label(rf"$\beta = 0.42$, \ nearer the critical 0.44: \ $T = {d['near']['T']}$", font_size=22, color=PATH),
        ), 12.0, 0.2, [0, -3.25, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A sixteen-by-sixteen grid. In green, the magnetization of the chain started from "
            "all plus; in red, from all minus. <bookmark mark='b'/> At beta of point three the two meet within "
            "thirty-two sweeps, and the state they share at time zero, shown below, is an exact draw from the Ising "
            "distribution. <bookmark mark='c'/> At point four two, closer to the infinite square lattice's critical "
            "inverse temperature of about point four four. This finite torus has no sharp phase transition; in this "
            "seeded run, they need a hundred and twenty-eight: near criticality the chain mixes slowly, and the "
            "observed coalescence horizon is a random computational cost, not the exact mixing time."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(group), FadeIn(rows[0]))
            vo.wait_until("a")
            for k, m_ in enumerate("bc"):
                vo.wait_until(m_)
                top, bot, grid, T = anims[k]
                self.play(Create(top), Create(bot), run_time=2.0)
                self.play(FadeIn(grid), FadeIn(rows[k + 1]))
        self.clear_scene()

    def limits(self):
        rows = fit_rows(VGroup(
            label(r"needs monotonicity, \ or another way to bound all starting states", font_size=24),
            label(r"the running time is random, \ and can be long", font_size=24, color=RES),
            label(r"most posteriors have no such structure", font_size=24, color=RES),
            label(r"but it shows what `converged' means, \ exactly", font_size=24, color=HIT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The price: the method needs monotonicity, or some other way to bound all starting states. "
            "<bookmark mark='b'/> Its running time is random, and can be long. <bookmark mark='c'/> Most posteriors offer no "
            "such structure, so in practice we rely on the diagnostics. <bookmark mark='d'/> But coupling from the past makes "
            "precise what we mean when we hope a chain has converged."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def coupling_now(self):
        rows = [
            cmath(r"\text{couple two chains}", r":", r"\text{one lagged by } L \text{ steps}", font_size=30),
            cmath(r"\text{when they meet}", r":", r"\text{an unbiased estimate, \ from finite runs}", font_size=30),
            cmath(r"\text{meeting times}", r":", r"\text{bound the distance to stationarity}", font_size=30),
            cmath(r"\text{works for}", r":", r"\text{MH, \ Gibbs, \ HMC: \ no monotonicity needed}", font_size=30),
        ]
        rows[1][-1].set_color(HIT)
        whys = [why(r"Jacob, O'Leary \& Atchad\'e (2020)"), why(r"debiasing the burn-in"), why(r"under coupling and moment conditions"), why(r"coupling, \ revived")]
        with self.voiceover(
            "<bookmark mark='a'/> The coupling idea has recently returned in a practical form. Pierre Jacob, John "
            "O'Leary and Yves Atchadé couple two copies of an ordinary Markov chain, one lagged behind the other. "
            "<bookmark mark='b'/> Once they meet, a simple correction turns finite runs into unbiased estimates of "
            "posterior expectations, under appropriate coupling, meeting-time and moment conditions. The unbiased "
            "object is an expectation estimator, not an exact posterior draw. <bookmark mark='c'/> The distribution "
            "of meeting times bounds how far the chain is from stationarity, under the relevant coupling and "
            "integrability assumptions. <bookmark mark='d'/> And it works for Metropolis–Hastings, Gibbs and HMC, "
            "without needing monotonicity."       ) as vo:
            intro = label('Coupled expectation estimators need meeting-time conditions', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
