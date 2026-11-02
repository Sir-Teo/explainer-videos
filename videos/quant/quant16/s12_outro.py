from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, DELTA, GOOD, METHOD_COL, OPT, PART, load

DESK = [
    (r"How many paths for a price to one basis point?",
     r"error $\approx \sigma_f/\sqrt n$, so $n \approx (\sigma_f / \varepsilon)^2$: for an at-the-money one-year call "
     r"($\sigma_f \approx 19$, $\varepsilon = 0.01$ on a price of 10.45) about 3.5 million plain paths; a control variate or "
     r"Sobol points cut that by one to three orders of magnitude"),
    (r"Why is AAD's cost independent of the number of Greeks?",
     r"one backward sweep of the recorded computation propagates the price's sensitivity to every input at once, by the "
     r"chain rule in reverse; its cost is a small constant times one pricing, whether there are five inputs or five "
     r"thousand. Bumping needs one extra pricing per input"),
    (r"Crank--Nicolson gives the right price for a digital but the gamma oscillates. Why, and the fix?",
     r"it is second order but only weakly damping: the payoff's jump excites high-frequency modes that decay slowly. "
     r"Start with a few fully implicit (half-)steps, Rannacher's trick, then switch to Crank--Nicolson"),
]

PROBLEMS = [
    r"Show that the control-variate estimator $\bar Y - b(\bar C - \mathbb{E}C)$ has minimal variance at "
    r"$b^* = \text{cov}(Y, C)/\text{var}(C)$, and that the variance falls by the factor $1 - \rho_{YC}^2$.",
    r"For importance sampling with a normal shifted by $\theta$, derive the likelihood ratio, and the $\theta$ that "
    r"centres the shifted normal on the strike.",
    r"Show that for any martingale $M$ with $M_0 = 0$, $\sup_\tau \mathbb{E}[h_\tau] \le \mathbb{E}[\max_t (h_t - M_t)]$.",
    r"Derive the stability condition of the explicit scheme for the heat equation by von Neumann analysis.",
    r"Show that reverse-mode differentiation of $f(g(h(x)))$ for $x \in \mathbb{R}^n$ costs a constant multiple of "
    r"one evaluation, while forward mode costs $n$ times.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("mc"), load("qmc"), load("mlmc"), load("american"), load("greeks"), load("fd"), load("race"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, m, q, ml, a, g, f, r):
        sdq = q["sd"]
        c0, s0 = m["rmse"]["plain"][-1], m["rmse"]["sobol"][-1]
        okc = [x for x in ml["standard"] if np.isfinite(x["cost"])]
        sav = okc[-1]["cost"] / ml["mlmc"][len(okc) - 1]["cost"]
        items = [
            (rf"Monte Carlo converges like $1/\sqrt n$; Sobol points reached {c0 / s0:.0f} times less error", OPT),
            (rf"the Brownian bridge makes quasi-Monte Carlo work on paths: "
             rf"{sdq['pseudo-random'][-1] / sdq['Sobol + bridge'][-1]:.0f} times less spread", METHOD_COL["Sobol + bridge"]),
            (rf"multilevel Monte Carlo: {sav:.0f} times cheaper at the tightest target", GOOD),
            (rf"an American put pinned between {a['lsm']:.3f} and {a['ab'][-1]['upper']:.3f}", DELTA),
            (rf"AAD: every Greek for {g['aad_ratio']:.1f} times one price", DELTA),
            (r"Crank--Nicolson needs Rannacher's start; the explicit scheme can explode", BAD),
            (r"ADI prices Heston on a two-dimensional grid in under a second", METHOD_COL["ADI (Craig-Sneyd)"]),
            (r"for a vanilla, Fourier wins by orders of magnitude; simulation for everything else", METHOD_COL["COS"]),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=28, color=col), label(t, font_size=24)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        title = label(r"Part 16 in eight lines", font_size=38).to_edge(UP, buff=0.4)
        rows.next_to(title, DOWN, buff=0.45)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            "Part sixteen in eight lines. Monte Carlo converges like one over root n, and the constant is where the "
            "craft is. The Brownian bridge makes quasi-Monte Carlo work on paths. Multilevel simulation removes most of "
            "the cost of a fine step. American options can be priced by simulation and bracketed from both sides. "
            "Adjoints deliver every Greek for a few prices. Crank–Nicolson needs a careful start. ADI handles two "
            "dimensions. And for a vanilla, Fourier wins by orders of magnitude."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=24) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Three desk questions. A price to one basis point needs the payoff's standard deviation over the target, "
            "squared: millions of plain paths, far fewer with variance reduction. <bookmark mark='a'/> AAD's cost is "
            "independent of the number of Greeks because one backward sweep sends the sensitivity to every input at "
            "once. <bookmark mark='b'/> And Crank–Nicolson's oscillating gamma comes from weak damping of the payoff's "
            "jump; a few implicit steps at the start remove it. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "And five problems: the optimal control variate, importance sampling's shift, the duality bound, the "
            "explicit scheme's stability, and why reverse mode is cheap. Solutions, in English and Chinese, are in the "
            "notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"neural networks that learn prices and Greeks (differential ML)", [17]),
            (r"term-structure models priced on lattices and by simulation", [19]),
            (r"XVA: the whole book under thousands of scenarios", [21]),
            (r"risk measures by simulation, and importance sampling for tails", [31]),
        ])
        with self.voiceover(
            "Where this comes back. Part seventeen trains networks on prices and Greeks together, which only AAD "
            "makes cheap. Rates models in Part nineteen are priced on lattices and by simulation. Part twenty-one runs "
            "the whole book under thousands of scenarios, and Part thirty-one uses importance sampling for tail risk."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Glasserman, \textit{Monte Carlo Methods in Financial Engineering}; Savine, \textit{Modern Computational "
             r"Finance}", r"Andersen and Piterbarg, \textit{Interest Rate Modeling}, vol.\ I; Duffy, \textit{Finite Difference "
             r"Methods in Financial Engineering}; Seydel, \textit{Tools for Computational Finance}"],
            [r"Crank and Nicolson (1947); Boyle (1977); Rannacher (1984); Craig and Sneyd (1988)",
             r"Broadie and Glasserman (1996); Caflisch, Morokoff and Owen (1997); Carr and Madan (1999)",
             r"Longstaff and Schwartz (2001); Rogers (2002); Andersen and Broadie (2004); Haugh and Kogan (2004)",
             r"Giles and Glasserman (2006); Giles (2008); Fang and Oosterlee (2008); in 't Hout and Foulon (2010)",
             r"Chakrabarti et al.\ (2021)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on. Every number here was computed by the "
            "House's engine on one CPU core."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("data", "vol"))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 17, Deep Pricing and Hedging", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House can now compute any price it can write down, and say how wrong it might be. "
            "<bookmark mark='a'/> Next, Part seventeen: deep pricing and hedging. Networks that learn prices from "
            "this engine, solve equations in a hundred dimensions, and hedge books that no formula describes."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
