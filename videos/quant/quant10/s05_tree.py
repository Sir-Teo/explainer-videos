from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant10.common import CASH, DEL, OPT, PART, QQ, SPOT, load


class Tree(VoiceoverScene):
    def construct(self):
        d = load("tree")
        self.card()
        self.one_step()
        self.many_steps(d)
        self.limit(d)

    def card(self):
        c = chapter_card(4, r"The tree and its limit", r"Can a coin flip price an option?", lit=(1979,), part=PART)
        with self.voiceover("Chapter four. The tree and its limit."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def one_step(self):
        # one period: the stock goes from 100 to 120 or 90; a call with strike 100; no interest
        S0, Su, Sd, K = 100, 120, 90, 100
        Cu, Cd = Su - K, 0
        delta = (Cu - Cd) / (Su - Sd)
        bond = Cu - delta * Su
        c0 = delta * S0 + bond
        root = np.array([-5.6, 0.2, 0])
        up, dn = root + np.array([3.2, 1.7, 0]), root + np.array([3.2, -1.7, 0])

        def node(p, tex, col):
            return VGroup(Circle(radius=0.48, color=col, stroke_width=2.5, fill_color=BACKGROUND, fill_opacity=1)
                          .move_to(p), MathTex(tex, font_size=34, color=col).move_to(p))

        n0, nu, nd = node(root, "100", SPOT), node(up, "120", SPOT), node(dn, "90", SPOT)
        e1 = Line(n0.get_center(), nu.get_center(), buff=0.5, color=GREY_C)
        e2 = Line(n0.get_center(), nd.get_center(), buff=0.5, color=GREY_C)
        cu = MathTex(r"C_u = 20", font_size=32, color=OPT).next_to(nu, RIGHT, buff=0.3)
        cd = MathTex(r"C_d = 0", font_size=32, color=OPT).next_to(nd, RIGHT, buff=0.3)
        tree = VGroup(e1, e2, n0, nu, nd, cu, cd)
        rows = VGroup(
            MathTex(r"\Delta = \frac{C_u - C_d}{S_u - S_d} = \frac{20}{30} = \tfrac23", font_size=34, color=DEL),
            MathTex(rf"\text{{bond}} = C_u - \Delta S_u = 20 - 80 = {bond:.0f}", font_size=34, color=CASH),
            MathTex(rf"C_0 = \Delta S_0 + \text{{bond}} = 66.67 - 60 = {c0:.2f}", font_size=36, color=OPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.5).shift(UP * 1.4)
        prob = VGroup(
            MathTex(r"C_0 = q\,C_u + (1 - q)\,C_d", font_size=34, color=OPT),
            MathTex(r"q = \frac{S_0 - S_d}{S_u - S_d} = \tfrac13", font_size=34, color=QQ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(rows, DOWN, buff=0.6).align_to(rows, LEFT)
        pnote = label(r"whatever the real chance of going up", font_size=24, color=GREY_A)
        pnote.next_to(prob, DOWN, buff=0.25).align_to(prob, LEFT)
        ill = note(r"illustrative: zero interest, one period", font_size=18).to_corner(DL, buff=0.3)
        with self.voiceover(
            "There is a third road, the one that is easiest to see. Cox, Ross and Rubinstein in 1979: let time "
            "move in one step, and let the stock do one of two things. From one hundred it goes to one hundred and "
            "twenty, or to ninety. A call with strike one hundred is then worth twenty, or nothing. "
            "<bookmark mark='a'/> Two outcomes, two instruments: we can copy the call exactly. Hold delta shares, "
            "with delta the change in the call over the change in the stock, twenty over thirty: two thirds of a "
            "share. <bookmark mark='b'/> Borrow sixty, so that in the up state the shares are worth eighty, minus "
            "sixty, twenty; in the down state, sixty minus sixty, zero. The copy matches the call in both "
            f"states, so it must cost the same: two thirds of a hundred minus sixty, {c0:.2f}. "
            "<bookmark mark='c'/> Write that price as a weighted average of the two payoffs, and the weight on the "
            "up state comes out to one third. That is a probability, but not anyone's belief: it is the one "
            "probability under which the stock is a fair game, expected to stay at a hundred. Whether the real "
            "chance of going up is ten percent or ninety, the price is the same. The risk-neutral measure, in "
            "its simplest form."
        ) as vo:
            self.play(FadeIn(n0), FadeIn(ill))
            self.play(Create(e1), Create(e2), FadeIn(nu), FadeIn(nd))
            self.play(FadeIn(cu), FadeIn(cd))
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]))
            self.play(Write(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(prob, shift=UP * 0.2))
            self.play(FadeIn(pnote))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def many_steps(self, d):
        small = d["small"]
        layers = {int(k): v for k, v in small["layers"].items()}
        g = binomial_tree(layers, dx=2.45, dy=0.78, node_r=0.38, font_size=22, show=("values",))
        gs = binomial_tree(layers, dx=2.45, dy=0.78, node_r=0.38, font_size=22, show=("spots",))
        gd = binomial_tree({k: v for k, v in layers.items() if v.get("delta") is not None}, dx=2.45, dy=0.78,
                           node_r=0.38, font_size=22, show=("delta",))
        for m in (g, gs, gd):
            m.move_to(LEFT * 1.2 + DOWN * 0.3)
        gd.align_to(g, LEFT).align_to(g, UP).shift(DOWN * (g.height - gd.height) / 2)
        info = VGroup(
            MathTex(rf"u = e^{{\sigma\sqrt{{\Delta t}}}} = {small['u']:.4f}", font_size=28, color=SPOT),
            MathTex(rf"q = \frac{{e^{{r\Delta t}} - d}}{{u - d}} = {small['p']:.4f}", font_size=28, color=QQ),
            MathTex(rf"C_0 = {small['price']:.3f}", font_size=34, color=OPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4).shift(UP * 0.8)
        params = note(rf"$S_0 = K = 100$, $T = 1$, $\sigma = 20\%$, $r = 5\%$, four steps", font_size=20)
        params.to_corner(DR, buff=0.3)
        heads = VGroup(label(r"stock prices", font_size=28, color=SPOT), label(r"call values", font_size=28, color=OPT),
                       label(r"the hedge, $\Delta$", font_size=28, color=DEL))
        for h in heads:
            h.to_edge(UP, buff=0.35).set_x(g.get_x())
        with self.voiceover(
            "Now chop a year into four steps and let the stock move up or down by e to the plus or minus sigma "
            "root delta t at each. The prices recombine into a tree. <bookmark mark='a'/> At the last layer the "
            "call is worth its payoff. Work backwards: each node is the discounted risk-neutral average of the two "
            "nodes after it. That is the replication argument applied once per node, and it lands on a price "
            f"today of {small['price']:.3f}. <bookmark mark='b'/> And at every node the tree also tells you the "
            "hedge: how many shares make the copy work over the next step. Near the top, almost a full share; "
            "near the bottom, almost none. A hedger walking down this tree rebalances at every step."
        ) as vo:
            self.play(FadeIn(heads[0]), FadeIn(gs.edges))
            self.play(LaggedStart(*[FadeIn(gs.nodes[n]) for n in sorted(gs.nodes)], lag_ratio=0.3, run_time=2.5))
            self.play(FadeIn(params), FadeIn(info[0]), FadeIn(info[1]))
            vo.wait_until("a")
            self.play(ReplacementTransform(heads[0], heads[1]), FadeOut(VGroup(*[gs.nodes[n] for n in gs.nodes])))
            for n in sorted(g.nodes, reverse=True):
                self.play(FadeIn(g.nodes[n], shift=LEFT * 0.2), run_time=0.7)
            self.play(FadeIn(info[2]), Indicate(g.nodes[0], color=OPT))
            vo.wait_until("b")
            self.play(ReplacementTransform(heads[1], heads[2]),
                      FadeOut(VGroup(*[g.nodes[n] for n in g.nodes])),
                      LaggedStart(*[FadeIn(gd.nodes[n]) for n in sorted(gd.nodes)], lag_ratio=0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limit(self, d):
        N = np.asarray(d["N"], float)
        px = np.asarray(d["price"], float)
        exact = d["exact"]
        g = axes([0, np.log10(400)], [9.4, 12.4], x_length=7.4, y_length=4.4, xlabel=r"number of steps $N$",
                 ylabel=r"the tree's price", xticks=[0, 1, 2], yticks=[9.5, 10.5, 11.5],
                 xfmt=lambda v: f"10^{{{int(v)}}}", font_size=20)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        lx = np.log10(N)
        line = DashedLine(ax.c2p(0, exact), ax.c2p(np.log10(400), exact), color=OPT, stroke_width=2)
        line_lab = MathTex(rf"\text{{formula}}\ {exact:.4f}", font_size=26, color=OPT)
        line_lab.next_to(ax.c2p(np.log10(400), exact), UP, buff=0.12).shift(LEFT * 0.9)
        odd = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=SPOT) for a, b, n in zip(lx, px, N) if int(n) % 2])
        even = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=QQ) for a, b, n in zip(lx, px, N) if not int(n) % 2])
        leg = VGroup(VGroup(Dot(color=SPOT, radius=0.06), label(r"odd $N$", font_size=22, color=SPOT))
                     .arrange(RIGHT, buff=0.12),
                     VGroup(Dot(color=QQ, radius=0.06), label(r"even $N$", font_size=22, color=QQ))
                     .arrange(RIGHT, buff=0.12)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        leg.move_to(ax.c2p(1.9, 12.0))
        right = VGroup(
            label(r"$N = 400$ steps:", font_size=28, color=GREY_A),
            MathTex(rf"{d['big_N_price']:.4f}", font_size=42, color=OPT),
            label(r"the formula:", font_size=28, color=GREY_A),
            MathTex(rf"{exact:.4f}", font_size=42, color=OPT),
            label(r"error $\propto 1/N$, alternating in sign", font_size=24, color=GREY_A),
            label(r"central limit theorem: the coin flips", font_size=24, color=GREY_A),
            label(r"become a lognormal", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.55)
        with self.voiceover(
            "Add steps and the tree's price converges to the Black-Scholes price. Here is the tree's price for "
            "every number of steps from one to four hundred, on a log scale. It zigzags: trees with an even "
            "number of steps put a node exactly at the strike, odd ones straddle it, and the two families err on "
            "opposite sides, closing in on the formula like one over N. "
            f"<bookmark mark='a'/> With four hundred steps the tree gives {d['big_N_price']:.4f}; the formula, "
            f"{exact:.4f}. The reason is the central limit theorem: the log of the price is a sum of many small "
            "up and down steps, so it becomes normal, the price lognormal, and the tree's backward induction "
            "becomes the equation's. Three derivations, one formula: a riskless portfolio, an expectation under "
            "the risk-neutral measure, and the limit of a coin-flipping tree. Desks use all three, and trees "
            "especially for options that can be exercised early, which is chapter ten."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(line_lab))
            self.play(LaggedStart(*[FadeIn(x) for x in odd], lag_ratio=0.01, run_time=2.5),
                      LaggedStart(*[FadeIn(x) for x in even], lag_ratio=0.01, run_time=2.5), FadeIn(leg))
            vo.wait_until("a")
            self.play(FadeIn(right, shift=LEFT * 0.2))
        self.wait(0.4)
        self.clear_scene()
