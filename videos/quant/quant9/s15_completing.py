from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import (ALT, ARB, CALL, FWD, HEDGE, PART, Q_C, answer_under, illustration, load,
                                        pause_at)


class Completing(VoiceoverScene):
    def construct(self):
        c, st = load("completing"), load("super_tree")
        self.card()
        self.strikes(c)
        self.trinomial()
        self.converge(st)
        self.predict()

    def card(self):
        c = chapter_card(8, r"Completing the market; super-replication through time", r"How do options close the "
                         r"gap, and what does a hedger do without them?", lit=(1976,), part=PART)
        with self.voiceover("Chapter eight. Completing the market, and super-replication through time."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def strikes(self, c):
        S, rows, true = np.asarray(c["S"]), c["rows"], c["true"]
        g = axes([0.5, 1.75], [0, 1.0], x_length=6.4, y_length=1.4, xlabel=r"the 33 states: stock price tomorrow",
                 xticks=[0.6, 0.8, 1.0, 1.2, 1.4, 1.6], yticks=[], font_size=15)
        g.to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.6)
        ax = g.ax
        w = np.asarray(c["w"])
        st = VGroup(*[Line(ax.c2p(s, 0), ax.c2p(s, 0.15 + 0.85 * wi / w.max()), color=Q_C, stroke_width=3)
                      for s, wi in zip(S, w)])
        dig = DashedLine(ax.c2p(1.1, 0), ax.c2p(1.1, 1.0), color=ARB, stroke_width=2)
        dl = label(r"the digital pays 1 above 1.1", font_size=17, color=ARB).next_to(ax.c2p(1.1, 1.0), RIGHT, buff=0.1)
        hinge = VGroup()
        for r_ in rows[1:]:
            k = r_["strike"]
            hinge.add(VGroup(Triangle(color=HEDGE, fill_opacity=1).scale(0.09).move_to(ax.c2p(k, 0) + DOWN * 0.12),
                             MathTex(f"{k:g}", font_size=17, color=HEDGE).move_to(ax.c2p(k, 0) + DOWN * 0.38)))
        h = axes([0, 10], [0, 0.85], x_length=6.4, y_length=3.4, xlabel=r"traded calls added", ylabel=r"the digital's "
                 r"no-arbitrage interval", xticks=list(range(0, 11)), yticks=[0, 0.25, 0.5, 0.75], font_size=15)
        h.to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        hx = h.ax
        bars = VGroup(*[Rectangle(width=0.36, height=max(hx.c2p(0, r_["upper"])[1] - hx.c2p(0, r_["lower"])[1], 0.02),
                                  stroke_width=0, fill_color=ALT, fill_opacity=0.65).move_to(
            hx.c2p(i, (r_["upper"] + r_["lower"]) / 2)) for i, r_ in enumerate(rows)])
        tl = DashedLine(hx.c2p(0, true), hx.c2p(10, true), color=Q_C, stroke_width=2)
        tll = MathTex(rf"\text{{true }} {true:.3f}", font_size=22, color=Q_C).next_to(hx.c2p(10, true), RIGHT, buff=0.1)
        r0, r1, r4, rl = rows[0], rows[1], rows[4], rows[-1]
        side = VGroup(
            history_card(1976, r"Stephen Ross, ``Options and efficiency''", r"with options on enough strikes, any "
                         r"payoff of the underlying can be built: options complete the market", width=4.8,
                         font_size=19),
            MathTex(rf"\text{{stock and bond only: }}[{r0['lower']:.3f},\ {r0['upper']:.3f}]", font_size=24, color=ALT),
            MathTex(rf"\text{{one call: }}[{r1['lower']:.3f},\ {r1['upper']:.3f}]", font_size=24, color=ALT),
            MathTex(rf"\text{{ten calls: }}[{rl['lower']:.3f},\ {rl['upper']:.3f}]", font_size=24, color=ALT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        src = illustration(r"33 states, log-normal weights as the true $Q$; each call priced under it")
        with self.voiceover(
            "Options are how real markets close the gap. A stock with thirty-three possible prices tomorrow, and a "
            "digital option that pays one if the price ends above one point one. With only the stock and the bond, "
            f"no arbitrage says the digital is worth somewhere between {r0['lower']:.2f} and {r0['upper']:.2f}: "
            "almost nothing. <bookmark mark='a'/> Now let calls trade, one strike at a time, each priced by the "
            "same true measure. Every call adds a hinge to the set of payoffs the market can build, and the "
            "super-replication program gets a new tool. <bookmark mark='b'/> The interval shrinks with each strike: "
            f"one call, {r1['lower']:.2f} to {r1['upper']:.2f}; ten calls, {rl['lower']:.2f} to {rl['upper']:.2f}, "
            f"around the true price of {true:.2f}. Stephen Ross proved in 1976 that options on enough strikes "
            "complete the market: every payoff of the stock becomes a portfolio of calls. That is the deepest reason "
            "options exist."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[Create(l_) for l_ in st], lag_ratio=0.03), Create(dig), FadeIn(dl),
                      FadeIn(h), FadeIn(src), run_time=2.5)
            self.play(FadeIn(bars[0]), Create(tl), FadeIn(tll), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            for i in range(1, 4):
                self.play(FadeIn(hinge[i - 1], shift=UP * 0.1), FadeIn(bars[i]), run_time=0.8)
            self.play(FadeIn(side[2]))
            vo.wait_until("b")
            for i in range(4, len(rows)):
                self.play(FadeIn(hinge[i - 1], shift=UP * 0.1), FadeIn(bars[i]), run_time=0.5)
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def trinomial(self):
        dx, dy = 1.5, 0.55
        nodes, edges = {}, VGroup()
        for n in range(4):
            for j in range(-n, n + 1):
                nodes[(n, j)] = Dot([n * dx, j * dy, 0], radius=0.07, color=GREY_B)
        for n in range(3):
            for j in range(-n, n + 1):
                for dj, col in ((1, HEDGE), (0, GREY_D), (-1, HEDGE)):
                    edges.add(Line(nodes[(n, j)].get_center(), nodes[(n + 1, j + dj)].get_center(), stroke_width=2,
                                   color=GREY_C))
        tree = VGroup(edges, *nodes.values()).move_to(LEFT * 3.4 + DOWN * 0.4)
        outer = VGroup(*[e for e in edges if abs(e.get_end()[1] - e.get_start()[1]) > 0.1])
        mid = VGroup(*[e for e in edges if abs(e.get_end()[1] - e.get_start()[1]) <= 0.1])
        rows = [cmath(r"\overline{V}_n", r"=", r"\max_{q:\ \mathbb{E}^q[S_{n+1}] = S_n}\ \mathbb{E}^q[\overline{V}_{n+1}]",
                      font_size=32, colors={r"\overline{V}_n": HEDGE}),
                cmath(r"q", r"\in", r"\big[\,(q_u, 0, q_d),\ (0, 1, 0)\,\big]", font_size=32),
                cmath(r"\overline{V}\ \text{convex}", r"\Rightarrow", r"\text{outer branches: a CRR step}",
                      font_size=32),
                cmath(r"\overline{V}_0", r"\to", r"\mathrm{BS}(\sigma_{\max}),\qquad \underline{V}_0 \to (S_0 - K)^+",
                      font_size=32, colors={r"\overline{V}_0": HEDGE})]
        whys = [why(r"a trinomial step with only the stock and the bond: one step of chapter 7's program", 19),
                why(r"the one-step martingale measures form a segment: its ends are the two-point measures", 19),
                why(r"linear in $q$, so the max is at an end; a convex value prefers the spread-out end (Jensen)", 19),
                why(r"so the super-price is the binomial price at the tree's widest moves: Black--Scholes at the "
                    r"highest volatility (Avellaneda, Levy and Par\'as 1995; Lyons 1995)", 19)]
        step = ladder(self, rows, whys, keep=4, top=3.3, x=2.6, buff=0.6, edge=6.95)
        src = note(r"Kramkov (1996), optional decomposition; F\"ollmer and Schied, ch.\ 7", font_size=17,
                   color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Now remove the options and add time. A trinomial tree: each step the stock goes up, stays, or goes down, "
            "with only the stock and the bond to trade. Three branches, two assets: incomplete at every node. "
            "<bookmark mark='a'/> The seller super-replicates step by step, backward: at each node, the cheapest "
            "cover of tomorrow's super-price, which by the duality of the last chapter is the largest expectation "
            "over the one-step martingale measures. <bookmark mark='b'/> Those measures form a segment, and its ends "
            "are two-point measures: either the outer branches only, or the middle branch only. <bookmark mark='c'/> "
            "For a convex claim, the spread-out end always wins. The outer branches light up at every node, the "
            "middle ones go dark: the super-hedger prices as if every move were the biggest possible. "
            "<bookmark mark='d'/> So the super-price is a binomial price, at the largest volatility the tree allows, "
            "and in the limit it is Black and Scholes at that volatility. Marco Avellaneda, Arnon Levy and Antonio "
            "Parás, and Terry Lyons, called this uncertain volatility, in 1995."
        ) as vo:
            self.play(FadeIn(tree), FadeIn(src))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            vo.wait_until("c")
            self.play(outer.animate.set_color(HEDGE).set_stroke(width=4), mid.animate.set_opacity(0.15), run_time=1.5)
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    def converge(self, st):
        N, up = np.asarray(st["N"]), np.asarray(st["upper"])
        g = axes([0, np.log2(256)], [8.5, 12.8], x_length=7.0, y_length=4.2, xlabel=r"steps (log scale)",
                 ylabel=r"super-replication price of the call", xticks=list(range(0, 9)),
                 xfmt=lambda v: f"{2 ** int(v)}", yticks=[9, 10, 11, 12], font_size=16)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        bsl = DashedLine(ax.c2p(0, st["bs"]), ax.c2p(8, st["bs"]), color=Q_C, stroke_width=2)
        bl = MathTex(rf"\mathrm{{BS}}(25\%) = {st['bs']:.3f}", font_size=24, color=Q_C).next_to(ax.c2p(8, st["bs"]),
                                                                                             DOWN, buff=0.15).shift(LEFT * 0.8)
        pts = VGroup(*[Dot(ax.c2p(np.log2(n), u), radius=0.07, color=HEDGE) for n, u in zip(N, up)])
        ln = curve(ax, np.log2(N), up, HEDGE, stroke_width=3)
        side = VGroup(
            MathTex(rf"N = 256:\ {up[-1]:.3f}", font_size=30, color=HEDGE),
            MathTex(rf"\text{{sub-replication: }} {max(st['lower']):.0f}\ \text{{for every }} N", font_size=28, color=ALT),
            wrapped_label(r"the interval for an at-the-money call with stock and bond alone: from intrinsic value to "
                          r"Black--Scholes at the widest volatility; a model, or traded options, must choose inside",
                          4.6, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Run it. The super-replication price of an at-the-money call on trinomial trees with up to two hundred "
            f"and fifty-six steps, widest volatility twenty-five percent: {up[-1]:.3f} at the finest tree, against "
            f"Black and Scholes at twenty-five percent, {st['bs']:.3f}. <bookmark mark='a'/> The sub-replication "
            "price is the other extreme, all mass on the middle branch: the stock never moves, and the call is "
            "worth its intrinsic value, zero. The no-arbitrage interval is enormous. A real desk narrows it the "
            "way the first half of this chapter did, by trading options, or by choosing a model."
        ) as vo:
            self.play(FadeIn(g), Create(bsl), FadeIn(bl))
            self.play(LaggedStart(*[GrowFromCenter(p_) for p_ in pts], lag_ratio=0.25), Create(ln), run_time=3)
            self.play(FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def predict(self):
        card = pause_at(r"You may add two traded calls. Which pair of strikes closes the digital's interval completely?")
        with self.voiceover(
            "Pause and predict. You may add two traded calls. Which pair of strikes closes the digital's interval "
            "completely? <bookmark mark='a'/> Any two strikes with no state between them, both between the last "
            "state below one point one and the first state above it. Their call spread pays nothing in every state "
            "below the jump and the same amount in every state above: scaled up, it is the digital, replicated "
            "exactly. The House's program agrees: with calls at one point one and one point one two, the interval "
            "has width zero."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"two strikes with no state between them, bracketing the jump (say 1.10 "
                                                r"and 1.12): the scaled call spread is the digital in every state")))
        self.wait(0.4)
        self.clear_scene()
