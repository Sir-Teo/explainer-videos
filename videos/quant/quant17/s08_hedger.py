from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, DELTA, GOOD, NET, OPT, PART, REF, illustration, load


class Hedger(VoiceoverScene):
    def construct(self):
        h = load("hedge")
        self.card()
        self.framework(h)
        self.nocost(h)
        self.prices(h)

    def card(self):
        c = chapter_card(7, r"The deep hedger", r"What if the hedge is learned, not derived?", part=PART)
        with self.voiceover("Chapter seven. The deep hedger."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def framework(self, h):
        rows = [cmath(r"\delta_k", r"=", r"\text{network}\big(\log S_k/K,\ \tau_k,\ \delta_{k-1}\big)", font_size=38,
                      colors={r"\delta_k": NET}),
                cmath(r"X", r"=", r"-(S_T - K)^+ + \sum_k \delta_k\,(S_{k+1} - S_k) - c\sum_k |\delta_k - \delta_{k-1}|\,S_k",
                      font_size=32, colors={r"X": OPT}),
                cmath(r"\min_\theta", r"\ ", r"\rho(X) = \tfrac{1}{\gamma}\log \mathbb{E}\,e^{-\gamma X}", font_size=38,
                      colors={r"\min_\theta": GOOD})]
        whys = [why(r"Buehler, Gonon, Teichmann and Wood (2019): at each rebalancing date a network chooses the holding from "
                    r"the price, the time left and the holding it already has; nothing about Greeks or formulas"),
                why(r"the seller's profit and loss on a short call: the payoff paid, the hedge's gains, and a proportional cost "
                    r"$c$ on every trade"),
                why(r"minimize a risk measure of that profit and loss over simulated paths. Here the entropic one, "
                    r"exponential utility's certainty equivalent; with CVaR the method is the same. The minimum is the "
                    r"price the seller must charge: the indifference price (Hodges and Neuberger 1989)")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.6, buff=0.75, edge=6.9)
        with self.voiceover(
            "Every hedge so far came from a model: differentiate a formula, get a delta. Hans Buehler, Lukas Gonon, Josef "
            "Teichmann and Ben Wood turned it around. At each rebalancing date, a network chooses the holding, looking "
            "only at the price, the time left, and what it already holds. <bookmark mark='a'/> Simulate many paths and "
            "score each one: the payoff the seller owes, the gains of the hedge, and a cost on every trade. "
            "<bookmark mark='b'/> Then train the network to minimize a measure of risk of that profit and loss. The "
            "minimum is more than a number: it is the price the seller has to charge to be no worse off than not "
            "selling at all, an indifference price, an idea of Stewart Hodges and Anthony Neuberger from 1989."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def nocost(self, h):
        n = h["nocost"]
        S = np.asarray(n["S"])
        g = axes([S[0], S[-1]], [0, 1], x_length=7.2, y_length=4.4, xlabel=r"price, 15 days before expiry",
                 ylabel=r"hedge (shares per option)", xticks=[90, 100, 110], yticks=[0, 0.5, 1],
                 font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        ref = DashedVMobject(curve(ax, S, np.asarray(n["bs_delta"]), REF, stroke_width=2.5), num_dashes=40)
        net = curve(ax, S, np.clip(np.asarray(n["learned"]), 0, 1), NET, stroke_width=4)
        leg = legend([(REF, r"Black--Scholes delta"), (NET, r"the deep hedger, no costs")], font_size=17)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        dev = float(np.max(np.abs(np.asarray(n["learned"]) - np.asarray(n["bs_delta"]))))
        ev, bsd = n["eval"], n["bs_eval"]
        side = VGroup(
            wrapped_label(rf"never shown a formula, it rebuilds the delta to within {dev:.2f} shares", 4.2, 20, GREY_A),
            MathTex(rf"\text{{price}}\ {ev['price']:.3f}\ \ \text{{vs}}\ \ {bsd['price']:.3f}", font_size=30, color=NET),
            wrapped_label(rf"its indifference price against delta hedging's, on the same 200{{,}}000 fresh paths; the "
                          rf"Black--Scholes price is {n['bs_price']:.3f}, the rest is the risk of hedging once a day", 4.2,
                          18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = illustration(r"a 30-day at-the-money call, 20\% volatility, daily rebalancing; 2{,}500 steps of 4{,}096 paths")
        with self.voiceover(
            "First, a check. With no trading costs, theory says the answer is the Black–Scholes delta. "
            f"<bookmark mark='a'/> The network was never shown a formula, and it rebuilds the delta to within {dev:.2f} "
            f"shares. Its indifference price is {ev['price']:.2f}, against {bsd['price']:.2f} for delta hedging on the "
            f"same paths, and {n['bs_price']:.2f} for the Black–Scholes formula: the difference is the risk left by "
            "hedging once a day instead of continuously."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(ref), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(net), FadeIn(leg[1]), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def prices(self, h):
        rows = h["band"]["rows"]
        costs = [r["cost"] for r in rows]
        mx = max(max(r["deep"]["price"], r["delta"]["price"]) for r in rows) * 1.15
        g = axes([-0.5, len(rows) - 0.5], [0, mx], x_length=7.4, y_length=4.2, xlabel=r"trading cost, per cent of each trade",
                 ylabel=r"price the seller must charge", xticks=list(range(len(rows))),
                 xfmt=lambda v: f"{100 * costs[int(round(v))]:g}", yticks=[0, 1, 2, 3, 4][:int(mx) + 1],
                 font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        bars = VGroup()
        for i, r in enumerate(rows):
            for j, (key, col) in enumerate((("delta", REF), ("ww", DELTA), ("deep", NET))):
                v = r[key]["price"]
                p0, p1 = ax.c2p(i - 0.3 + 0.2 * j, 0), ax.c2p(i - 0.1 + 0.2 * j, v)
                bars.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.01), stroke_width=0, fill_color=col,
                                   fill_opacity=0.85).move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0]))
        leg = legend([(REF, r"delta hedge every day"), (DELTA, r"Whalley--Wilmott band"), (NET, r"the deep hedger")],
                     font_size=17).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        hi = rows[-1]
        side = wrapped_label(rf"at {100 * hi['cost']:g}\% a trade, delta hedging every day costs {hi['delta']['mean_cost']:.2f} "
                             rf"in fees and needs a price of {hi['delta']['price']:.2f}; the deep hedger trades "
                             rf"{hi['deep']['turnover']:.1f} shares in total instead of {hi['delta']['turnover']:.1f} and "
                             rf"needs {hi['deep']['price']:.2f}. Costs make the market incomplete: the price now depends on "
                             r"the seller's risk aversion, and the hedge on the price", 4.4, 19, GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Now add costs. Here is the price the seller must charge, by cost per trade, for three strategies: the "
            "delta hedge rebalanced every day, Whalley and Wilmott's band from Part eleven, and the deep hedger. "
            f"<bookmark mark='a'/> At {100 * hi['cost']:g} percent a trade, the daily delta hedge pays "
            f"{hi['delta']['mean_cost']:.2f} in fees and needs {hi['delta']['price']:.2f}; the deep hedger trades far "
            f"less and needs {hi['deep']['price']:.2f}. With costs there is no unique price any more: it depends on how "
            "much risk the seller will bear."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(side))
        self.wait(0.5)
        self.clear_scene()
