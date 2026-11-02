from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.zh_text import verbatim
from videos.quant.quant9.common import (ALT, ARB, CALL, FWD, HEDGE, PART, Q_C, answer_under, load, pause_at, tbar)

S3 = np.array([80.0, 100.0, 125.0])


class Incomplete(VoiceoverScene):
    def construct(self):
        s, inc = load("superlp"), load("incomplete")
        self.card()
        self.lid(s)
        self.duality(s)
        self.lab(s)
        self.states(inc)
        self.predict()

    def card(self):
        c = chapter_card(7, r"Incomplete markets: the interval as a linear program", r"What if the market cannot "
                         r"build the claim?", lit=(1981,), part=PART)
        with self.voiceover("Chapter seven. Incomplete markets: the interval as a linear program."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def lid(self, s):
        X = np.asarray(s["X"])
        B, D = s["B"], s["Delta"]
        g = axes([60, 140], [-12, 40], x_length=5.4, y_length=4.2, xlabel=r"stock price tomorrow",
                 ylabel=r"payoff", xticks=[80, 100, 125], yticks=[0, 11.11, 25], yfmt=lambda v: f"{v:g}",
                 font_size=16)
        g.to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        ax = g.ax
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.09, color=CALL) for a, b in zip(S3, X)])
        hgt = ValueTracker(30.0)

        def lidline():
            off = hgt.get_value()
            return Line(ax.c2p(60, D * 60 + B + off), ax.c2p(140, D * 140 + B + off), color=HEDGE, stroke_width=4)

        L = always_redraw(lidline)
        floor = ValueTracker(-10.0)
        F_ = always_redraw(lambda: Line(ax.c2p(60, floor.get_value()), ax.c2p(140, floor.get_value()), color=ALT,
                                        stroke_width=4))
        top = Dot(ax.c2p(100, s["upper"]), radius=0.1, color=Q_C)
        tl = MathTex(rf"\overline{{p}} = {s['upper']:.2f}", font_size=28, color=Q_C).next_to(top, UL, buff=0.08)
        bl = MathTex(rf"\underline{{p}} = {s['lower']:.0f}", font_size=28, color=ALT).next_to(ax.c2p(100, 0), DR,
                                                                                            buff=0.08)
        # the (B, Delta) plane
        h = axes([-90, 10], [0, 1.4], x_length=5.0, y_length=4.2, xlabel=r"bond $B$", ylabel=r"shares $\Delta$",
                 xticks=[-80, -40, 0], yticks=[0, 0.5, 1.0], font_size=16)
        h.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.2)
        hx = h.ax
        Bs = np.linspace(-90, 10, 2)
        lines = VGroup()
        for sj, xj, col in zip(S3, X, (FWD, GREY_B, CALL)):
            ys = (xj - Bs) / sj
            lines.add(Line(hx.c2p(Bs[0], ys[0]), hx.c2p(Bs[1], ys[1]), color=col, stroke_width=2.5))
        # feasible region: above all three lines (Delta >= (X_j - B) / s_j)
        bb = np.linspace(-90, 10, 101)
        need = np.max([(xj - bb) / sj for sj, xj in zip(S3, X)], axis=0)
        reg = band(hx, bb, np.clip(need, 0, 1.4), np.full_like(bb, 1.4), Q_C, 0.2)
        lvl = ValueTracker(40.0)

        def level():
            c = lvl.get_value()
            b0, b1 = -90, 10
            return Line(hx.c2p(b0, (c - b0) / 100), hx.c2p(b1, (c - b1) / 100), color=HEDGE, stroke_width=3)

        LV = always_redraw(level)
        vert = Dot(hx.c2p(B, D), radius=0.1, color=Q_C)
        vl = MathTex(rf"(B, \Delta) = ({B:.2f},\ {D:.3f})", font_size=24, color=Q_C).next_to(vert, UR, buff=0.1)
        with self.voiceover(
            "Give the stock three outcomes, eighty, a hundred, or a hundred and twenty-five, with "
            "only stock and bond to trade. The call pays nothing, nothing, or twenty-five: no "
            "straight line passes through all three, so it cannot be replicated. <bookmark mark='a'/> "
            "The seller super-replicates: the cheapest line on or above all three points. Lower it "
            f"like a lid; it rests on the worst and best states, at {s['upper']:.2f}. <bookmark "
            "mark='b'/> The buyer pushes a line up from below; it rests at zero. Outside this "
            "interval, one side has an arbitrage. <bookmark mark='c'/> On the right, the same problem "
            "in the plane of bond and shares: each state a half-plane, the cost a sliding line that "
            f"stops at one vertex: borrow {abs(B):.2f}, hold {D:.3f} of a share."
        ) as vo:
            self.play(FadeIn(g), FadeIn(pts))
            vo.wait_until("a")
            self.add(L)
            self.play(hgt.animate.set_value(0.0), run_time=2.5, rate_func=smooth)
            self.play(FadeIn(top), FadeIn(tl))
            vo.wait_until("b")
            self.add(F_)
            self.play(floor.animate.set_value(0.0), run_time=1.5)
            self.play(FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(h), LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), FadeIn(reg))
            self.add(LV)
            self.play(lvl.animate.set_value(s["upper"]), run_time=2.5, rate_func=smooth)
            self.play(FadeIn(vert), FadeIn(vl))
        for m in (L, F_, LV):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def duality(self, s):
        rows = [cmath(r"\overline{p}", r"=", r"\min_{B,\Delta}\ \{B + 100\Delta\ :\ B + \Delta s_j \ge X_j\ \ \forall j\}",
                      font_size=34, colors={r"\overline{p}": Q_C}),
                cmath(r"\overline{p}", r"=", r"\max_{q \ge 0}\ \{\textstyle\sum_j q_j X_j\ :\ \sum_j q_j = 1,\ \sum_j q_j "
                      r"s_j = 100\}", font_size=34, colors={r"\overline{p}": Q_C}),
                cmath(r"q^*", r"=", r"(\tfrac59,\ 0,\ \tfrac49)\ \Rightarrow\ \overline{p} = 25\cdot\tfrac49 = "
                      r"\tfrac{100}{9}", font_size=34, colors={r"q^*": Q_C}),
                cmath(r"(\underline{p},\ \overline{p})", r"=", r"(0,\ 11.11)\quad\text{open}", font_size=34)]
        whys = [why(r"super-replication: the cheapest dominating portfolio", 21),
                why(r"LP duality: the multipliers of the three constraints are a probability (the bond's column) "
                    r"that prices the stock (its column): a martingale measure", 21),
                why(r"the dual optimum sits at an end of chapter 5's segment; the primal is tight in states 1 and 3, "
                    r"where $q^* > 0$ (complementary slackness)", 21),
                why(r"strictly positive $Q$ never reaches the ends: every price strictly inside is consistent with "
                    r"no arbitrage", 21)]
        step = ladder(self, rows, whys, keep=4, top=1.6, x=-0.6, buff=0.55, edge=6.9)
        t = theorem_card(r"The second fundamental theorem", r"An arbitrage-free market is complete, every claim "
                         r"replicable, if and only if the equivalent martingale measure is unique.",
                         who=r"Harrison and Pliska (1981)", color=Q_C, width=8.6, font_size=24).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Linear programs come in pairs. The seller's problem: the cheapest dominating portfolio. "
            "<bookmark mark='a'/> Its dual puts a multiplier on each state: the bond's column makes "
            "them sum to one, the stock's makes them price the stock. The dual maximizes the claim's "
            "expectation over risk-neutral measures. <bookmark mark='b'/> The best one is an end of "
            "chapter five's segment, giving a hundred over nine, the lid's eleven eleven. <bookmark "
            "mark='c'/> The lower bound is the other end, zero, and strictly positive measures never "
            "reach the ends: the interval is open. <bookmark mark='d'/> Harrison and Pliska's second "
            "theorem, of 1981: a market is complete exactly when the martingale measure is unique."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(t, shift=DOWN * 0.2))
        self.wait(0.3)
        self.clear_scene()

    def lab(self, s):
        with verbatim():
            card = lab_card(r"the seller's LP, by the same simplex", [
                "S = [80, 100, 125]; X = [0, 0, 25]",
                "# variables: B+, B-, D+, D-, three surpluses",
                "A = [[1, -1, s, -s] + surplus(j) for j, s in enumerate(S)]",
                "c = [1, -1, 100, -100, 0, 0, 0]   # cost: B + 100 Delta",
                "res = simplex(c, A, X)",
            ], source="videos/quant/quant9/compute.py (superlp)", width=8.2, font_size=18).to_edge(UP, buff=0.5)
        v = s["verts"]
        outs = [f"pivots: {len(v)}   status: optimal",
                f"B = {s['B']:.4f}   Delta = {s['Delta']:.4f}   cost = {s['upper']:.4f}",
                f"HiGHS, same problem: {s['highs_upper']:.4f}"]
        with self.voiceover(
            "The teaching simplex solves the seller's problem too, free variables split in two, a "
            f"surplus per state. <bookmark mark='a'/> {len(v)} pivots to the vertex, cost "
            f"{s['upper']:.4f}; HiGHS agrees to every digit."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            with verbatim():
                lab_run(self, card, outs, run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    def states(self, inc):
        rows = inc["rows"]
        g = axes([0, len(rows)], [0, 0.22], x_length=6.6, y_length=4.2, ylabel=r"no-arbitrage prices of an "
                 r"at-the-money call", xticks=[], yticks=[0, 0.05, 0.1, 0.15, 0.2], font_size=17)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        bars, labs = VGroup(), VGroup()
        for i, r_ in enumerate(rows):
            lo, hi = max(r_["lower"], 0.0), r_["upper"]
            if hi - lo < 1e-6:
                bars.add(Dot(ax.c2p(i + 0.5, lo), radius=0.08, color=CALL))
            else:
                bars.add(tbar(ax, i + 0.5, hi, ALT, width=0.45, lo=lo).set_fill(opacity=0.55))
            labs.add(label(f"{r_['states']}", font_size=19, color=GREY_A).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.1))
        xl = label(r"states tomorrow", font_size=18, color=GREY_B).next_to(labs, DOWN, buff=0.15)
        bsl = DashedLine(ax.c2p(0, inc["bs"]), ax.c2p(len(rows), inc["bs"]), color=CALL, stroke_width=2)
        side = VGroup(
            wrapped_label(r"a stock on a log-normal grid of states, the call struck at today's price: the interval "
                          r"for every number of states", 4.4, 20, GREY_A),
            wrapped_label(rf"two states: a point; three or more: the same interval, whatever the number; dashed: "
                          rf"Black--Scholes at 20\%, {inc['bs']:.3f}, one choice inside it", 4.4, 20, CALL),
            wrapped_label(r"more states never close the gap; more traded assets do (next chapter)", 4.4, 20, Q_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Do more states close the gap? A call at today's price on grids of two to thirty-three "
            "states. <bookmark mark='a'/> Two states: a point. Three or more: the same interval every "
            "time, since only the extremes bind. <bookmark mark='b'/> A model picks one price inside; "
            "adding traded assets, not states, closes the gap."
        ) as vo:
            self.play(FadeIn(g), FadeIn(labs), FadeIn(xl), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.3), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(bsl), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def predict(self):
        card = pause_at(r"Add a fourth state, a stock price of 110. Does the call's interval change?")
        with self.voiceover(
            "Pause and predict. Add a fourth state at a hundred and ten. Does the interval change? "
            "<bookmark mark='a'/> No: its payoff, ten, lies under the lid and above the floor."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"no: the point (110, 10) lies below the lid through (80, 0) and "
                                                r"(125, 25), whose height there is 16.7; the extremes bind")))
        self.wait(0.4)
        self.clear_scene()
