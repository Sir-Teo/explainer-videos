from __future__ import annotations

import numpy as np

from videos.stats.stats44.common import *  # noqa: F403


class Convergence(VoiceoverScene):
    def construct(self):
        self.card()
        self.upcrossings()
        self.theorem()
        self.two_cases()
        self.levy()
        self.reverse()

    def card(self):
        card = chapter_card(5, r"Martingale convergence", r"Why a fair game must settle down", lit=(1953,), part=PART)
        with self.voiceover("Chapter five. Martingale convergence: why a bounded fair game must settle down."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def upcrossings(self):
        g = np.random.default_rng(9)
        n = 400
        x = np.r_[2.0, 2.0 + np.cumsum(g.standard_normal(n)) * 0.35]
        # Fixed initial value and increments; show the entire seeded path.
        lo = min(-2.0, float(np.floor(x.min() / 2) * 2))
        hi = max(4.0, float(np.ceil(x.max() / 2) * 2))
        A = axes([0, n], [lo, hi], x_length=7.4, y_length=4.2, xlabel=r"$n$", ylabel=r"$M_n$", xticks=[0, 200, 400], yticks=np.arange(lo, hi + 1, 2),
                 center=[-2.5, 0.3, 0])
        ax = A.ax
        a, b = 1.0, 3.0
        la = DashedLine(ax.c2p(0, a), ax.c2p(n, a), color=GREY_B, stroke_width=2)
        lb = DashedLine(ax.c2p(0, b), ax.c2p(n, b), color=GREY_B, stroke_width=2)
        path = polyline(ax, np.arange(n + 1), x, CHAINC, 2)
        ups = VGroup()
        below, start = x[0] < a, None
        for i, v in enumerate(x):
            if below and v > a and start is None:
                start = i
            if v <= a:
                below, start = True, None
            if start is not None and v >= b:
                ups.add(polyline(ax, np.arange(start, i + 1), x[start:i + 1], MARTC, 4))
                below, start = False, None
        side = fit_rows(VGroup(
            label(rf"an upcrossing of $[a, b]$: \ a climb from below $a$ to above $b$", font_size=22),
            label(rf"this path: \ {len(ups)} upcrossings", font_size=22, color=MARTC),
            label(r"Doob: \ $E\, U_n(a, b) \le \frac{E(M_n - a)^+}{b - a}$", font_size=24, color=S.ACCENT),
            label(r"bet only while climbing: \ a fair game can't pay for many climbs", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The convergence theorem rests on counting upcrossings: climbs of the path from below a "
            "level a to above a level b. <bookmark mark='b'/> This seeded illustration makes three completed upcrossings. The seed was chosen for visibility, not for estimating how often crossings occur. <bookmark mark='c'/> Doob's "
            "upcrossing inequality: the expected number of upcrossings is at most the expected positive part of M n minus a, "
            "over b minus a. <bookmark mark='d'/> The proof is a betting system: buy when the path falls below a, sell when it "
            "rises above b. Each completed climb earns at least b minus a, and a fair game cannot pay for unboundedly many."
        ) as vo:
            self.play(FadeIn(A), FadeIn(la), FadeIn(lb))
            vo.wait_until("a")
            self.play(Create(path), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(ups), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def theorem(self):
        rows = [
            cmath(r"\sup_n E|M_n| < \infty", r"\Rightarrow", r"M_n \to M_\infty \ \text{almost surely}, \ E|M_\infty| < \infty", font_size=30),
            cmath(r"\text{proof}", r":", r"\text{if } \liminf < a < b < \limsup, \ \text{infinitely many upcrossings: \ probability } 0", font_size=28),
            cmath(r"\text{UI}", r"\iff", r"M_n \to M_\infty \text{ in } L^1 \iff M_n = E[M_\infty \mid \mathcal F_n]", font_size=30),
            cmath(r"\text{e.g.}", r":", r"M_n \ge 0 \text{ always converges; \ bounded martingales converge in } L^1", font_size=28),
        ]
        rows[0][-1].set_color(MARTC)
        whys = [why(r"Doob's convergence theorem"), why(r"rationals $a < b$: \ countably many"), why(r"closable martingales"), why(r"two cases")]
        with self.voiceover(
            "<bookmark mark='a'/> Doob's convergence theorem: a martingale bounded in absolute first moment converges"
            " almost surely, to a finite limit. <bookmark mark='b'/> If it did not, for some rational pair a below b "
            "it would oscillate across them infinitely often, and the upcrossing inequality makes that a null event; "
            "there are only countably many rational pairs. <bookmark mark='c'/> Convergence in mean needs more: "
            "uniform integrability, which is equivalent to the martingale being the successive predictions of its own"
            " limit. <bookmark mark='d'/> So every non-negative martingale converges, and every uniformly bounded "
            "one, or one dominated by an integrable envelope, converges in mean too. Merely being bounded separately "
            "on each sample path is insufficient."
        ) as vo:
            heading=label('An absolute first-moment bound gives almost-sure convergence',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def two_cases(self):
        rows = fit_rows(VGroup(
            label(r"P\'olya's urn: \ bounded, \ so UI: \ the limit's mean is the start's, \ $\tfrac12$", font_size=26, color=GOODC),
            label(r"the likelihood ratio under $H_0$: \ $\ge 0$, \ so it converges, \ to 0", font_size=26, color=BADC),
            label(r"$E L_n = 1$ for every $n$, \ but $E L_\infty = 0$: \ not UI", font_size=26, color=BADC),
            label(r"the mass escapes on rare paths: \ the escaping bump of Part 43, \ as a martingale", font_size=24, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two martingales from chapter two show the difference. Pólya's urn is bounded, hence "
            "uniformly integrable: its random limit has mean one half, the starting share. <bookmark mark='b'/> The likelihood "
            "ratio under the null is non-negative, so it converges too, and its limit is zero. <bookmark mark='c'/> Its mean "
            "is one at every n, but the mean of its limit is zero: it is not uniformly integrable. <bookmark mark='d'/> Its "
            "mass escapes along ever rarer paths of ever larger wealth, Part forty-three's escaping bump in the form of a "
            "martingale."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def levy(self):
        rows = [
            cmath(r"\text{L\'evy}", r":", r"E[X \mid \mathcal F_n] \to E[X \mid \mathcal F_\infty] \ \text{a.s. and in } L^1", font_size=32),
            cmath(r"A \in \mathcal F_\infty", r":", r"P(A \mid \mathcal F_n) \to 1_A: \ \text{L\'evy's 0--1 law}", font_size=32),
            cmath(r"\text{Bayes}", r":", r"E[\theta \mid X_1, \ldots, X_n] \to \theta \ \text{a.s.} \ \text{if } \theta \text{ is a function of the data}", font_size=30),
            cmath(r"\text{Doob (1949)}", r":", r"\text{posterior consistency for almost every } \theta \text{ under the prior}", font_size=30),
        ]
        rows[3][-1].set_color(S.ACCENT)
        whys = [why(r"the upward theorem"), why(r"you eventually learn every event"), why(r"posterior means are Doob martingales"), why(r"Part 53")]
        with self.voiceover(
            "<bookmark mark='a'/> Paul Lévy's upward theorem: the predictions of any integrable X, as information "
            "grows, converge to its prediction given the sigma-algebra generated by the union of these information "
            "sets. <bookmark mark='b'/> In particular the conditional probability of any event decided in the limit "
            "tends to one or zero: you eventually learn whether it happens. <bookmark mark='c'/> A Bayesian posterior"
            " mean is such a sequence of predictions: a Doob martingale. If the parameter is integrable, the model "
            "satisfies the standard measurability conditions, and the parameter is measurable from the infinite data,"
            " the posterior mean converges to it. <bookmark mark='d'/> That is Doob's 1949 theorem: posterior "
            "consistency, for almost every parameter value under the prior. Part fifty-three asks the harder "
            "question, for every parameter value."
        ) as vo:
            heading=label('Increasing information reveals the terminal conditional expectation',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def reverse(self):
        rows = [
            cmath(r"\mathcal E_n", r"=", r"\sigma(S_n, X_{n+1}, X_{n+2}, \ldots): \ \text{shrinking information}", font_size=32),
            cmath(r"\bar X_n", r"=", r"E[X_1 \mid \mathcal E_n]: \ \text{a reverse martingale}", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"\bar X_n \to E[X_1 \mid \mathcal E_\infty] = E X_1 \ \ \text{(Hewitt--Savage)}: \ \text{the SLLN}", font_size=30),
            cmath(r"\text{exchangeable}", r":", r"\text{the same argument: \ i.i.d.\ given } \mathcal E_\infty: \ \text{de Finetti (Part 5)}", font_size=30),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"exchangeable information"), why(r"symmetry: \ each $X_i$ alike"), why(r"reverse convergence"), why(r"a promise kept")]
        with self.voiceover(
            "<bookmark mark='a'/> Martingales also run backwards. For independent identically distributed integrable "
            "variables, let E n be the information in the n-th partial sum and everything after it, which shrinks as "
            "n grows. <bookmark mark='b'/> By symmetry, each of the first n variables has the same conditional "
            "expectation given it, so the sample mean is the conditional expectation of the first variable: a reverse"
            " martingale. <bookmark mark='c'/> Reverse martingales always converge, here to the expectation given the"
            " exchangeable sigma-algebra, which by Hewitt and Savage is trivial: the strong law of large numbers "
            "again, in four lines. <bookmark mark='d'/> For an exchangeable sequence extending the argument to "
            "bounded indicator functions and their products establishes conditional factorization given the limiting "
            "empirical law. The sample-mean convergence alone does not prove conditional independence. This outlines "
            "de Finetti's theorem, promised in Part five."
        ) as vo:
            heading=label('Reverse martingales prove the iid integrable strong law',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
