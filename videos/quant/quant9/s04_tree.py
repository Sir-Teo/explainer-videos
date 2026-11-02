from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.viz import binomial_tree
from explainer.zh_text import verbatim
from videos.quant.quant9.common import (ARB, CALL, FWD, HEDGE, PART, PUT, Q_C, answer_under, illustration, load,
                                        pause_at)


class Tree(VoiceoverScene):
    def construct(self):
        t = load("tree")
        self.card()
        self.one_step(t)
        self.fold(t)
        self.lab(t)
        self.american(t)
        self.predict()

    def card(self):
        c = chapter_card(6, r"The tree: replication, then folding back", r"Where does the risk-neutral probability "
                         r"come from?", lit=(1979,), part=PART)
        with self.voiceover("Chapter six. The tree: replication, then folding back."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def one_step(self, t):
        o = t["one"]
        g = axes([60, 140], [-50, 35], x_length=5.6, y_length=4.4, xlabel=r"stock price $S$",
                 ylabel=r"value $V$", xticks=[80, 100, 120], yticks=[-40, 0, 10, 20], font_size=17)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        up = Dot(ax.c2p(120, 20), radius=0.09, color=CALL)
        dn = Dot(ax.c2p(80, 0), radius=0.09, color=CALL)
        lab = VGroup(label(r"up: stock 120, call pays 20", font_size=18, color=CALL).next_to(up, UP, buff=0.12),
                     label(r"down: stock 80, call pays 0", font_size=18, color=CALL).next_to(dn, DOWN, buff=0.15))
        xs = np.array([60, 140])
        rep = Line(ax.c2p(60, o["Delta"] * 60 + o["B"]), ax.c2p(140, o["Delta"] * 140 + o["B"]), color=HEDGE,
                   stroke_width=4)
        here = DashedLine(ax.c2p(100, -50), ax.c2p(100, o["V"]), color=GREY_B, stroke_width=1.5)
        val = Dot(ax.c2p(100, o["V"]), radius=0.1, color=Q_C)
        vl = MathTex(rf"V_0 = {o['V']:.0f}", font_size=28, color=Q_C).next_to(val, LEFT, buff=0.15)
        bl = label(r"intercept: the bond, $B$", font_size=17, color=HEDGE).next_to(ax.c2p(60, o["Delta"] * 60 + o["B"]),
                                                                                   RIGHT, buff=0.1).shift(DOWN * 0.3)
        rows = [cmath(r"\Delta S_u + B e^{r\Delta t}", r"=", r"V_u,\qquad \Delta S_d + B e^{r\Delta t} = V_d",
                      font_size=30),
                cmath(r"\Delta", r"=", r"\frac{V_u - V_d}{S_u - S_d},\qquad B = e^{-r\Delta t}\frac{S_u V_d - S_d V_u}"
                      r"{S_u - S_d}", font_size=30, colors={r"\Delta": HEDGE}),
                cmath(r"V_0 = \Delta S_0 + B", r"=", r"e^{-r\Delta t}\big[q V_u + (1 - q) V_d\big]", font_size=30,
                      colors={r"V_0 = \Delta S_0 + B": Q_C}),
                cmath(r"q", r"=", r"\frac{S_0 e^{r\Delta t} - S_d}{S_u - S_d}\in(0, 1) \iff S_d < S_0 e^{r\Delta t} "
                      r"< S_u", font_size=30, colors={r"q": Q_C})]
        whys = [why(r"hold $\Delta$ shares and $B$ in bonds; match the claim in both states", 19),
                why(r"subtract the two equations; substitute back", 19),
                why(r"collect the terms in $V_u$ and $V_d$: the weights add to one", 19),
                why(r"no real probability appears anywhere; $q$ is a probability exactly when there is no arbitrage "
                    r"(chapter 4)", 19)]
        step = ladder(self, rows, whys, keep=4, top=3.4, x=3.4, buff=0.62, edge=6.95)
        res = MathTex(rf"\Delta = {o['Delta']:.1f},\ \ B = {o['B']:.0f},\ \ V_0 = {o['V']:.0f},\ \ q = {o['q']:.1f}",
                      font_size=30, color=Q_C).to_corner(DR, buff=0.4)
        with self.voiceover(
            "Cox, Ross and Rubinstein made the theorem computable in 1979. One step: a stock at a "
            "hundred goes to a hundred and twenty or eighty; a call at a hundred pays twenty or "
            "nothing: two points in the plane. <bookmark mark='a'/> Shares plus a bond make a "
            "straight line, and exactly one passes through both points: the replicating portfolio. "
            "<bookmark mark='b'/> Its height at today's price is the call's price, ten: buy half a "
            "share, borrow forty. <bookmark mark='c'/> In symbols: match both states, subtract, "
            "substitute. <bookmark mark='d'/> The price is a weighted average of the payoffs. "
            "<bookmark mark='e'/> The weight q comes from the moves and the rate alone, no one's "
            "probability of an up move, and it lies in zero to one exactly when there is no "
            "arbitrage."
            " Check the hedge: in the up state half a share is worth sixty, minus the forty owed, "
            "twenty; in the down state, forty minus forty, zero. Both payoffs, exactly."
        ) as vo:
            self.play(FadeIn(g), FadeIn(up), FadeIn(dn), FadeIn(lab))
            vo.wait_until("a")
            self.play(Create(rep), FadeIn(bl))
            vo.wait_until("b")
            self.play(Create(here), FadeIn(val), FadeIn(vl), FadeIn(res))
            vo.wait_until("c")
            step(0)
            step(1)
            vo.wait_until("d")
            step(2)
            vo.wait_until("e")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    def fold(self, t):
        layers = t["layers"]
        g = binomial_tree(layers, dx=1.75, dy=0.6, node_r=0.33, font_size=18, show=("values",))
        g.to_edge(LEFT, buff=0.5).shift(DOWN * 0.15)
        deltas = VGroup()
        for n in range(4):
            for j, d in enumerate(layers[str(n)]["delta"]):
                deltas.add(MathTex(rf"\Delta\,{d:.2f}", font_size=15, color=HEDGE).next_to(g.nodes[n][j], DOWN,
                                                                                           buff=0.04))
        for n in g.nodes:
            for nd in g.nodes[n]:
                nd[1].set_opacity(0)
        led = t["ledger"]
        path_nodes = []
        j = 0
        for n in range(5):
            if n > 0:
                j += int(led[n][0] > led[n - 1][0])
            path_nodes.append(g.nodes[n][j])
        lit = VGroup(*[Circle(radius=0.37, color=QC.HOUSE, stroke_width=4).move_to(nd) for nd in path_nodes])
        k = ValueTracker(0)

        def ledger_panel():
            i = int(round(k.get_value()))
            S, V, sh = led[i]
            return VGroup(label(r"the hedger's book on the lit path", font_size=21, color=QC.HOUSE),
                          MathTex(rf"S = {S:.2f}", font_size=28, color=FWD),
                          MathTex(rf"\text{{shares }} = {sh:.3f}", font_size=28, color=HEDGE),
                          MathTex(rf"\text{{book value}} = {V:.4f}", font_size=28, color=Q_C)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.4)

        panel = always_redraw(ledger_panel)
        S_T = led[-1][0]
        fin = wrapped_label(rf"at expiry: book {led[-1][1]:.4f}, payoff $\max(S_T - 100, 0) = {max(S_T - 100, 0):.4f}$; "
                            rf"over {t['rep_paths']:,} random paths the largest miss is {t['rep_max_err']:.0e}".replace(",", "{,}"),
                            4.8, 20, CALL).to_corner(DR, buff=0.4)
        eq = MathTex(rf"q = {t['q']:.4f},\ \ V_0 = {t['four_price']:.4f}", font_size=28, color=Q_C).to_corner(UR, buff=0.4)
        with self.voiceover(
            "Now four steps: a call at a hundred, twenty-five percent volatility, one year. At "
            "expiry, the payoffs. <bookmark mark='a'/> Fold back: each node is the risk-neutral "
            "average of the two after it, and its delta is their slope. The root: "
            f"{t['four_price']:.2f}. <bookmark mark='b'/> Now trade it: start with that much, hold "
            "each node's delta, finance the rest. Follow one path. <bookmark mark='c'/> At expiry the "
            "book equals the payoff exactly, on this path and on every one of a thousand, to within "
            f"{t['rep_max_err']:.0e}. That is replication."
            " Notice the deltas: near one deep in the money, near zero far out of it, just as Part "
            "ten's Black-Scholes delta will be."
        ) as vo:
            self.play(FadeIn(g.edges), *[FadeIn(nd[0]) for n in g.nodes for nd in g.nodes[n]])
            self.play(*[nd[1].animate.set_opacity(1) for nd in g.nodes[4]])
            vo.wait_until("a")
            for n in range(3, -1, -1):
                idx = [i for i, m_ in enumerate(deltas) if m_.get_center()[0] < g.nodes[n][0].get_center()[0] + 0.3
                       and m_.get_center()[0] > g.nodes[n][0].get_center()[0] - 0.3]
                self.play(*[nd[1].animate.set_opacity(1) for nd in g.nodes[n]], *[FadeIn(deltas[i]) for i in idx],
                          run_time=0.9)
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(FadeOut(eq))
            self.add(panel)
            self.play(Create(lit[0]))
            for i in range(1, 5):
                self.play(k.animate.set_value(i), Create(lit[i]), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(fin))
        panel.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def lab(self, t):
        with verbatim():
            card = lab_card(r"the tree, folded back", [
                "def crr(S, K, T, sigma, r=0.0, N=200, cp=1, american=False):",
                "    dt = T / N; u = exp(sigma * sqrt(dt)); d = 1 / u",
                "    p = (exp(r * dt) - d) / (u - d)        # risk-neutral",
                "    spots = S * u ** (2 * arange(N + 1) - N)",
                "    values = maximum(cp * (spots - K), 0)  # payoff",
                "    for n in reversed(range(N)):",
                "        values = exp(-r*dt) * (p*values[1:] + (1-p)*values[:-1])",
                "        if american:                       # exercise?",
                "            values = maximum(values, cp * (spots_n - K))",
                "    return values[0]",
            ], source="explainer/quant/house/trees.py", width=6.9, font_size=16).to_corner(UL, buff=0.3)
        N, P = np.asarray(t["N"]), np.asarray(t["prices"])
        g = axes([0, 200], [8.0, 12.6], x_length=5.6, y_length=3.6, xlabel=r"steps $N$", ylabel=r"call price",
                 xticks=[1, 50, 100, 150, 200], yticks=[8, 9, 10, 11, 12], font_size=15)
        g.to_corner(UR, buff=0.4).shift(DOWN * 0.2)
        ax = g.ax
        bsl = DashedLine(ax.c2p(0, t["bs"]), ax.c2p(200, t["bs"]), color=Q_C, stroke_width=2)
        bsll = MathTex(rf"\text{{Black--Scholes }} {t['bs']:.3f}", font_size=22, color=Q_C).next_to(ax.c2p(200, t["bs"]),
                                                                                               UP, buff=0.1).shift(LEFT * 1.3)
        n = ValueTracker(1)
        live = always_redraw(lambda: VGroup(*[Dot(ax.c2p(a, min(b, 12.6)), radius=0.025, color=CALL)
                                              for a, b in zip(N, P) if a <= n.get_value()]))
        cnt = always_redraw(lambda: MathTex(rf"N = {int(n.get_value())}:\ {P[int(n.get_value()) - 1]:.4f}",
                                            font_size=26, color=CALL).next_to(g, DOWN, buff=0.15))
        outs = [f"[crr(100, 100, 1, 0.25, N=n) for n in (1, 2, 3, 4)]",
                f"[{P[0]:.2f}, {P[1]:.2f}, {P[2]:.2f}, {P[3]:.2f}]",
                f"crr(..., N=200) = {P[199]:.3f}   bs = {t['bs']:.3f}"]
        with self.voiceover(
            "The House's tree in ten lines: up and down factors from volatility, the risk-neutral "
            "probability, payoffs at the leaves, and one line folding back a step at a time. "
            "<bookmark mark='a'/> Run one to four steps, then let N grow. <bookmark mark='b'/> The "
            f"prices zigzag, odd above even, closing in on Black and Scholes' {t['bs']:.3f}; at two "
            f"hundred steps, {P[199]:.3f}."
            " The whole tree costs about N squared over two operations, and the error shrinks roughly "
            "like one over N, with the zigzag on top."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(g), Create(bsl), FadeIn(bsll))
            vo.wait_until("a")
            with verbatim():
                lab_run(self, card, outs, run_time=2.0, font_size=17)
            vo.wait_until("b")
            self.add(live, cnt)
            self.play(n.animate.set_value(200), run_time=max(vo.remaining(1.0) - 1.0, 3.0), rate_func=rate_functions.ease_in_quad)
        live.clear_updaters()
        cnt.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def american(self, t):
        nodes = t["ex_nodes"]
        rows = VGroup(*[MathTex(rf"\text{{step }} {e['n']},\ S = {e['S']:.2f}:\ \ \text{{exercise}}\ {e['exercise']:.2f}"
                                rf"\ >\ \text{{hold}}\ {e['hold']:.2f}", font_size=28, color=PUT) for e in nodes])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"an American put on the same tree, rates at 5\%", font_size=28)
        res = MathTex(rf"\text{{American }} {t['am_put']:.2f}\ \ >\ \ \text{{European }} {t['eu_put']:.2f}",
                      font_size=34, color=Q_C)
        rule = cmath(r"V_n", r"=", r"\max\big(\text{exercise now},\ e^{-r\Delta t}[q V_u + (1 - q) V_d]\big)",
                     font_size=32)
        VGroup(head, rule, rows, res).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        src = note(r"Shreve I, ch.\ 4; the full theory of early exercise: Parts 8 and 10", font_size=18,
                   color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "One more line makes it American: at each node keep the larger of exercising now and "
            "waiting. <bookmark mark='a'/> For a put with five percent rates, exercise wins at "
            f"{len(nodes)} deep in-the-money nodes, and the put is worth {t['am_put']:.2f} against "
            f"{t['eu_put']:.2f} European. Shreve's chapter four does this in full."
            " The line between the nodes where exercise wins and those where waiting wins is the "
            "early-exercise boundary of Parts eight and ten."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rule), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.4), run_time=2)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    def predict(self):
        card = pause_at(r"Why does the tree's price zigzag between odd and even numbers of steps?")
        with self.voiceover(
            "Pause and predict. Why the zigzag between odd and even steps? <bookmark mark='a'/> With "
            "even N a node sits on the strike, at the payoff's kink; with odd N the strike falls "
            "between nodes, and the error changes sign."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"even $N$: a node sits on the strike, at the payoff's kink; odd $N$: the "
                                                r"strike falls between nodes, and the error changes sign")))
        self.wait(0.4)
        self.clear_scene()
