from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, DELTA, GOOD, NET, OPT, PART, REF, ask, illustration, load


def trade_map(ax, S, P, Z, vmax=0.3, stride=2):
    """Cells coloured by the trade the network makes: buying (green), selling (red), nothing (dark); every
    ``stride``-th grid point, so a map is a few hundred cells."""
    S, P, Z = S[::stride], P[::stride], np.asarray(Z)[::stride, ::stride]
    dS, dP = S[1] - S[0], P[1] - P[0]
    cells = VGroup()
    for i in range(len(P)):
        for j in range(len(S)):
            z = float(np.clip(Z[i][j] / vmax, -1, 1))
            col = interpolate_color(ManimColor("#0E1117"), ManimColor(GOOD if z > 0 else BAD), abs(z) ** 0.7)
            p0 = ax.c2p(S[j] - dS / 2, P[i] - dP / 2)
            p1 = ax.c2p(S[j] + dS / 2, P[i] + dP / 2)
            cells.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                                fill_opacity=1).move_to((p0 + p1) / 2))
    return cells


class Band(VoiceoverScene):
    def construct(self):
        h = load("hedge")
        self.card()
        self.emerge(h, load("hedge_replay"))
        self.leland()
        self.ww()
        self.bars(load("leland"))

    def card(self):
        c = chapter_card(13, r"Where not to trade", r"Your hedger has costs. Why does the optimal hedge have a band?",
                         lit=(1985,), part=PART)
        with self.voiceover("Chapter thirteen. Where not to trade, part one: the band emerges."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def emerge(self, h, r):
        m = h["mlp_cost"]
        S, P = np.asarray(r["S"]), np.asarray(r["prev"])
        wl, wh = np.asarray(m["ww_lo"]), np.asarray(m["ww_hi"])
        maps = r["cost_0"]["maps"]
        ck = [0, 100, 200, 300, 500, 800, 1100, 1500]
        runs = np.array([r[f"cost_{s_}"]["curve"] for s_ in range(3)])
        steps = np.arange(runs.shape[1], dtype=float)

        def frame(i):
            g = axes([S[0], S[-1]], [0, 1], x_length=4.6, y_length=3.7, xlabel=r"price, 15 days to expiry",
                     ylabel=r"shares already held", xticks=[90, 100, 110], yticks=[0, 0.5, 1], font_size=12)
            cells = trade_map(g.ax, S, P, maps[str(ck[i])], stride=3)
            ww = VGroup(DashedVMobject(curve(g.ax, S, np.clip(wl, 0, 1), WHITE, stroke_width=2), num_dashes=24),
                        DashedVMobject(curve(g.ax, S, np.clip(wh, 0, 1), WHITE, stroke_width=2), num_dashes=24))
            fl = r["cost_0"]["flat"].get(str(ck[i]))
            txt = (rf"step {ck[i]}: at the money it leaves {fl[0]:.2f}--{fl[1]:.2f} shares alone" if fl else
                   rf"step {ck[i]}: it trades almost everywhere")
            return VGroup(g, cells, ww, label(txt, font_size=16, color=GREY_A).next_to(g, DOWN, buff=0.12))
        rp = TrainingReplay(steps, np.clip(runs, None, np.percentile(runs, 99)), frame, checkpoints=ck,
                            ylabel=r"entropic risk, 0.5\% costs")
        leg = legend([(GOOD, r"buys"), (BAD, r"sells"), (GREY_D, r"dark: does nothing"),
                      (WHITE, r"Whalley--Wilmott's band")], font_size=16).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.35)
        fl = [r[f"cost_{s_}"]["flat"].get("1500") for s_ in range(3)]
        ws = [f_[1] - f_[0] for f_ in fl if f_]
        with self.voiceover(
            "Now the whole map, replayed from the first step of a second training run. Each cell is a price and a "
            "holding; green means the network buys, red means it sells, dark means it does nothing. The dashed lines "
            "are Whalley and Wilmott's band. <bookmark mark='a'/> At first it trades almost everywhere. Then a dark "
            "diagonal stripe opens, running along the delta: the do-nothing zone, growing step by step, with the "
            f"buying below it and the selling above it. Three seeds end with a stripe {min(ws):.2f} to {max(ws):.2f} "
            "shares wide at the money. Nobody drew it; the costs did."
        ) as vo:
            self.play(FadeIn(rp), FadeIn(leg))
            vo.wait_until("a")
            rp.play(self, run_time=max(vo.remaining(0.5), 6))
        self.wait(0.4)
        self.clear_scene()

    def leland(self):
        rows = [cmath(r"\mathbb{E}|\Delta\Delta|\,S", r"\approx", r"\Gamma S^2 \sigma \sqrt{\Delta t}\,\sqrt{2/\pi}",
                      font_size=40, colors={r"\mathbb{E}|\Delta\Delta|\,S": OPT}),
                cmath(r"\text{cost rate}", r"=", r"\tfrac{k}{2}\,\Gamma S^2 \sigma \sqrt{2/\pi} / \sqrt{\Delta t},\quad k = 2c",
                      font_size=38, colors={r"\text{cost rate}": BAD}),
                cmath(r"\hat\sigma^2", r"=", r"\sigma^2\Big(1 + \sqrt{2/\pi}\,\frac{k}{\sigma\sqrt{\Delta t}}\Big)",
                      font_size=40, colors={r"\hat\sigma^2": GOOD}),
                cmath(r"\sigma\sqrt{\Delta t} = 0.0105", r"\Rightarrow",
                      r"\text{Le} = 0.76,\ \ \hat\sigma = 26.6\%\ \text{at}\ c = 0.5\%", font_size=38,
                      colors={r"\Rightarrow": WHITE})]
        whys = [why(r"between rebalances the delta moves by about $\Gamma\,\Delta S$, and $|N(0,1)|$ has mean "
                    r"$\sqrt{2/\pi}$: the shares traded each time, in money"),
                why(r"per unit of time, times the cost per share traded ($c$ per side, round trip $k$)"),
                why(r"Leland (1985): that cost enters the Black--Scholes equation exactly where $\tfrac12\sigma^2 S^2\Gamma$ "
                    r"does, so a short option is priced and hedged as if volatility were higher"),
                why(r"this part's setting: daily rebalancing at 20\% volatility. Leland's number is large, so the "
                    r"correction is large")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.62, edge=6.9)
        with self.voiceover(
            "What would theory have said? Two classical answers. The first is Hayne Leland's, from 1985. Between "
            "rebalances the delta moves by about gamma times the price move, so the money traded each time is gamma "
            "times S squared times sigma root delta t, times the mean of a standard normal's absolute value. "
            "<bookmark mark='a'/> Divide by the time step and multiply by the cost: a cost rate that grows as "
            "rebalancing gets more frequent. <bookmark mark='b'/> It sits in the pricing equation exactly where the "
            "volatility term does, so a seller hedges and prices as if volatility were higher. <bookmark mark='c'/> "
            "Here, rebalancing daily at twenty percent volatility with half-percent costs, the volatility jumps from "
            "twenty to about twenty-six and a half percent. Leland still trades every day; he only changes how much."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def ww(self):
        rows = [cmath(r"\text{risk of a gap } \epsilon", r"\approx", r"\tfrac{\gamma}{2}\,\epsilon^2 \sigma^2 S^2\,dt",
                      font_size=38, colors={r"\text{risk of a gap } \epsilon": BAD}),
                cmath(r"|\epsilon| \le h", r"\Rightarrow", r"\text{turnover} \approx \sigma^2 S^2 \Gamma^2 / h,\quad "
                      r"\mathbb{E}\epsilon^2 = h^2 / 3", font_size=36, colors={r"\Rightarrow": WHITE}),
                cmath(r"\min_h", r"\ ", r"\tfrac{\gamma}{6}\,h^2 \sigma^2 S^2 + c\,S\,\frac{\sigma^2 S^2 \Gamma^2}{h}",
                      font_size=38, colors={r"\min_h": GOOD}),
                cmath(r"h", r"=", r"\Big(\frac{3\,c\,S\,\Gamma^2}{2\gamma}\Big)^{1/3}", font_size=44, colors={r"h": NET})]
        whys = [why(r"Whalley and Wilmott (1997): holding $\delta = \Delta + \epsilon$ instead of the delta leaves "
                    r"risk; exponential utility charges $\tfrac\gamma2$ times its variance"),
                why(r"keep the gap inside $\pm h$ by trading only at the edges: the gap is a reflected diffusion whose "
                    r"variance rate is $\sigma^2 S^2 \Gamma^2$, so the shares traded per unit time are about that over "
                    r"$h$; inside, the gap is spread about evenly, with mean square $h^2/3$"),
                why(r"risk grows like $h^2$, cost falls like $1/h$: balance them"),
                why(r"the band. A cube root: double the cost and it widens by $2^{1/3} \approx 1.26$, not 2. Widest where "
                    r"gamma is largest; it is the House's \texttt{quoting.ww\_band}")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.62, edge=6.9)
        with self.voiceover(
            "The second answer is Whalley and Wilmott's. A gap epsilon between holding and delta costs, under "
            "exponential utility, half the risk aversion times its variance. <bookmark mark='a'/> Keep the gap inside "
            "plus or minus h, trading only at the edges: it wanders like a reflected diffusion, so the trading per unit "
            "time is about sigma squared S squared gamma squared over h, and the gap's mean square is h squared over "
            "three. "
            "<bookmark mark='b'/> Risk grows like h squared; trading cost falls like one over h. Balance them. "
            "<bookmark mark='c'/> The optimal half-width is a cube root: three times the cost times S times gamma "
            "squared, over twice the risk aversion. That answers the hook's question: double the costs, and the band "
            "widens by the cube root of two, about twenty-six percent, not double."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def bars(self, L):
        rows = L["rows"]
        costs = [r["cost"] for r in rows]
        kinds = [("delta", REF, r"delta, every day"), ("leland", OPT, r"Leland's delta"), ("ww", DELTA, r"Whalley--Wilmott"),
                 ("deep", NET, r"band network")]
        mx = max(r["delta"]["price"] for r in rows) * 1.15
        g = axes([-0.5, len(rows) - 0.5], [0, mx], x_length=7.6, y_length=4.2, xlabel=r"trading cost, per cent of each trade",
                 ylabel=r"price the seller must charge", xticks=list(range(len(rows))),
                 xfmt=lambda v: f"{100 * costs[int(round(v))]:g}", yticks=[0, 1, 2, 3, 4, 5][:int(mx) + 1],
                 font_size=15).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        bars = VGroup()
        for i, r in enumerate(rows):
            for j, (key, col, _) in enumerate(kinds):
                v = r[key]["price"]
                p0, p1 = ax.c2p(i - 0.36 + 0.18 * j, 0), ax.c2p(i - 0.2 + 0.18 * j, v)
                bars.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.01), stroke_width=0, fill_color=col,
                                   fill_opacity=0.85).move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0]))
        leg = legend([(c, t) for _, c, t in kinds], font_size=16).arrange(RIGHT, buff=0.35).next_to(g, UP, buff=0.1)
        r5 = next(r for r in rows if abs(r["cost"] - 0.005) < 1e-9)
        order = sorted(kinds, key=lambda k: r5[k[0]]["price"])
        names = {"delta": "daily delta", "leland": "Leland", "ww": "Whalley and Wilmott", "deep": "the band network"}
        side = VGroup(
            label(r"at 0.5\%: price, mean cost, shares traded", font_size=19),
            *[MathTex(rf"\text{{{t.replace('--', '-')}}}\ \ {r5[k]['price']:.2f},\ {r5[k]['mean_cost']:.2f},\ "
                      rf"{r5[k]['turnover']:.2f}", font_size=24, color=c) for k, c, t in kinds],
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "All four, on the same paths, at five cost levels. "
            "<bookmark mark='a'/> At half a percent, the ranking from cheapest to dearest is "
            f"{names[order[0][0]]}, {names[order[1][0]]}, {names[order[2][0]]}, and {names[order[3][0]]}. Leland lowers "
            f"the fees only a little, {r5['leland']['mean_cost']:.2f} against {r5['delta']['mean_cost']:.2f}, because it "
            f"still trades every day; Whalley and Wilmott's band trades {r5['ww']['turnover']:.2f} shares in all, against "
            f"{r5['delta']['turnover']:.2f} for the daily delta. "
            f"<bookmark mark='b'/> A puzzle: Leland's price is {r5['bs_at_leland']:.2f}, yet hedging his way needs "
            f"{r5['leland']['price']:.2f}. Why? Leland covers the expected cost; the entropic price also charges for "
            "the risk that remains."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(side))
            vo.wait_until("b")
            self.play(FadeIn(ask(rf"Leland's price at 0.5\% is Black--Scholes at {100 * r5['sigma_leland']:.1f}\% "
                                 rf"volatility, {r5['bs_at_leland']:.2f}. Why is his hedge's indifference price "
                                 rf"{r5['leland']['price']:.2f}?")))
        self.wait(0.6)
        self.clear_scene()
