from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant37.common import (BUY_C, IMPACT_C, KERNEL_C, PART, SCHED_C, TWAP_C, fit_right,
                                         load)


class OW(VoiceoverScene):
    def construct(self):
        o = load("ow")
        k = load("kernels")
        self.card()
        self.book()
        self.answer(o)
        self.schedule(o)
        self.by_rho(o)
        self.powerlaw(k)
        self.signals()
        self.crowd()
        self.question()

    def card(self):
        c = chapter_card(6, r"A book that recovers", r"When impact decays, how should one trade?", part=PART)
        with self.voiceover("Chapter six. Almgren and Chriss's temporary impact vanishes the instant after each trade. "
                            "Real books recover over time: liquidity taken is replaced at some rate. Anna Obizhaeva and "
                            "Jiang Wang built the schedule for that world, and its answer surprises."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def book(self):
        rows = [cmath(r"\text{depth}", r":", r"q\ \text{per unit of price}", font_size=38),
                cmath(r"D_t", r"=", r"\int_0^t e^{-\rho (t - s)}\,\frac{dX_s}{q}", font_size=40,
                      colors={r"D_t": IMPACT_C}),
                cmath(r"G(t)", r"=", r"\frac{1}{q}\,e^{-\rho t}", font_size=40, colors={r"G(t)": KERNEL_C})]
        whys = [why(r"a block book: a buy of size $x$ eats the offers and moves the ask by $x/q$"),
                why(r"the displacement of the ask from its undisturbed level; new offers fill the gap at rate $\rho$, the "
                    r"resilience"),
                why(r"so this is Chapter 4's transient impact with an exponential kernel: convex, decreasing, and "
                    r"allowed")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The model. <bookmark mark='a'/> A book with depth q: a buy of size x eats the offers and lifts the ask by x "
            "over q. <bookmark mark='b'/> The displacement then heals: new offers arrive and close the gap at a rate "
            "rho, the resilience. <bookmark mark='c'/> That is Chapter four's transient impact with an exponential "
            "kernel: convex, decreasing, and allowed."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def answer(self, o):
        cf = o["closed"]
        rows = [cmath(r"\text{block at } 0", r":", r"\frac{X}{2 + \rho T}", font_size=40, colors={r"\text{block at } 0": BUY_C}),
                cmath(r"\text{rate between}", r":", r"\frac{\rho X}{2 + \rho T}", font_size=40),
                cmath(r"\text{block at } T", r":", r"\frac{X}{2 + \rho T}", font_size=40, colors={r"\text{block at } T": BUY_C}),
                cmath(r"\text{cost}", r"=", r"\frac{X^2}{q\,(2 + \rho T)}", font_size=40, colors={r"\text{cost}": IMPACT_C})]
        whys = [why(r"open with a block: the book is undisturbed, and the impact will heal while you continue"),
                why(r"then trade at exactly the rate at which the book recovers, keeping the displacement constant"),
                why(r"and close with a block: there is no future left for its impact to cost you"),
                why(r"the research chapter proves this; on a fine grid the discrete optimum matches it")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The answer to the pause: blocks. <bookmark mark='a'/> Open with a block, while the book is undisturbed. "
            "<bookmark mark='b'/> Then trade at exactly the rate at which the book recovers, so the displacement stays "
            "constant. <bookmark mark='c'/> And close with another block of the same size: after the last trade there is "
            "no future left for its impact to cost you. <bookmark mark='d'/> The cost is X squared over the depth times "
            "two plus rho T. With rho T of ten, each block is "
            f"{100 * cf['block']:.1f} percent of the order."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def schedule(self, o):
        t = np.asarray(o["t"], float)
        v = np.asarray(o["v"], float)
        dt = t[1] - t[0]
        rate = v / dt
        top = float(o["closed"]["rate"]) * 3
        g = axes([-0.02, 1.02], [0, top], x_length=8.4, y_length=4.0, xlabel=r"time",
                 ylabel=r"trading rate", xticks=[0, 0.5, 1], yticks=[0], font_size=15).move_to(DOWN * 0.3)
        ax = g.ax
        mid = curve(ax, t[1:-1], rate[1:-1], SCHED_C, stroke_width=3.5)
        b0 = Arrow(ax.c2p(0, 0), ax.c2p(0, top * 0.95), buff=0, color=BUY_C, stroke_width=6)
        b1 = Arrow(ax.c2p(1, 0), ax.c2p(1, top * 0.95), buff=0, color=BUY_C, stroke_width=6)
        tw = DashedLine(ax.c2p(0, 1.0), ax.c2p(1, 1.0), color=TWAP_C, stroke_width=1.8)
        labs = VGroup(label(rf"block {100 * v[0]:.1f}\%", font_size=18, color=BUY_C).next_to(b0, RIGHT, buff=0.15),
                      label(rf"block {100 * v[-1]:.1f}\%", font_size=18, color=BUY_C).next_to(b1, LEFT, buff=0.15),
                      label(r"TWAP", font_size=16, color=TWAP_C).next_to(ax.c2p(0.5, 1.0), UP, buff=0.1))
        rows = o["rows"]
        err = abs(rows[-1]["cost"] / o["closed"]["cost"] - 1)
        with self.voiceover(
            "On a grid of two hundred dates, the numerical optimum. <bookmark mark='a'/> Two spikes, at the ends, and a "
            "flat rate between, below the steady TWAP rate. <bookmark mark='b'/> As the grid refines, the blocks and "
            f"the cost converge to the formula: on a thousand dates the cost differs from it by {100 * err:.3f} percent."
        ) as vo:
            self.play(FadeIn(g), Create(tw), FadeIn(labs[2]))
            vo.wait_until("a")
            self.play(GrowArrow(b0), GrowArrow(b1), Create(mid), FadeIn(labs[:2]))
            vo.wait_until("b")
            self.wait(0.2)
        self.wait(0.4)
        self.clear_scene()

    def by_rho(self, o):
        hx = [-3.4, 0.0, 3.4]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"resilience $\rho T$", r"each block",
                                                                         r"cost $\times\, q/X^2$")])
        tab = VGroup(head)
        for r in o["by_rho"]:
            tab.add(VGroup(MathTex(f"{r['rho']:g}", font_size=26), MathTex(f"{100 * r['block']:.1f}\\%", font_size=26),
                           MathTex(f"{r['cost']:.3f}", font_size=26, color=IMPACT_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.0 - 0.75 * j, 0])
        foot = wrapped_label(r"no resilience: impact is permanent, cost $X^2/2q$ whatever the schedule; fast resilience: "
                             r"the cost falls like $1/(\rho T)$, Almgren--Chriss's temporary impact", 11.0, 16,
                             GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "By resilience. <bookmark mark='a'/> With none, impact is permanent: each block is half the order, and the "
            "cost is the same for every schedule, Huberman and Stanzl's linear permanent impact. As the book recovers "
            "faster, the blocks shrink and the cost falls like one over rho T: in the limit, Almgren and Chriss's "
            "temporary impact. Two models, one family."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def powerlaw(self, k):
        t = np.asarray(k["t"], float)
        ex = k["kernels"]["exponential"]
        pl = k["kernels"]["power law"]
        dt = t[1] - t[0]
        ve = np.asarray(ex["v"], float) / dt
        vp = np.asarray(pl["v"], float) / dt
        top = float(np.ceil(max(ve[1:-1].max(), vp[1:-1].max()) * 1.6))
        g = axes([0, 1], [0, top], x_length=6.4, y_length=4.4, xlabel=r"time", ylabel=r"trading rate, between the blocks",
                 xticks=[0, 0.5, 1], yticks=[0, top], yfmt=lambda v: f"{v:.1f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        ce = curve(ax, t[1:-1], ve[1:-1], KERNEL_C, stroke_width=3)
        cp = curve(ax, t[1:-1], vp[1:-1], SCHED_C, stroke_width=3)
        leg = legend([(KERNEL_C, rf"exponential: blocks {100 * ex['block0']:.0f}\%"),
                      (SCHED_C, rf"power law: blocks {100 * pl['block0']:.0f}\%")], font_size=16)
        leg.to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        gain_e = 100 * (1 - ex["cost"] / ex["twap"])
        gain_p = 100 * (1 - pl["cost"] / pl["twap"])
        with self.voiceover(
            "And with Bouchaud's power-law propagator instead of an exponential. <bookmark mark='a'/> The exponential "
            "keeps a flat rate between its blocks. <bookmark mark='b'/> The power law trades in a U: blocks at both "
            "ends, and a rate that dips in the middle, because old impact lingers longer. Against TWAP, the optimal "
            f"schedule saves {gain_e:.0f} percent of the cost under the exponential and {gain_p:.0f} percent under the "
            "power law."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(ce))
            vo.wait_until("b")
            self.play(Create(cp))
        self.wait(0.4)
        self.clear_scene()

    def signals(self):
        rows = [cmath(r"dS_t", r"=", r"\alpha_t\,dt + \sigma\,dW_t", font_size=40),
                cmath(r"v^*_t", r"=", r"v^{\text{AC}}_t + \text{(a term in } \alpha)", font_size=38,
                      colors={r"v^*_t": SCHED_C}),
                cmath(r"\text{order flow}", r"\Rightarrow", r"\alpha", font_size=40)]
        whys = [why(r"add a short-term forecast of the price's drift, from the book or from the desk's own signal"),
                why(r"Cartea and Jaimungal; Lehalle and Neuman (2019): the optimal rate is the risk-adjusted schedule plus "
                    r"a tilt toward trading ahead of predicted moves"),
                why(r"Part 36's order-flow imbalance and microprice are exactly such short-horizon forecasts")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Signals. <bookmark mark='a'/> Give the executor a short-term forecast of the price's drift. "
            "<bookmark mark='b'/> Álvaro Cartea and Sebastian Jaimungal, and Charles-Albert Lehalle and Eyal Neuman, "
            "showed the optimal rate is the risk-adjusted schedule plus a tilt: trade ahead of predicted moves, wait "
            "through predicted reversals. <bookmark mark='c'/> And Part thirty-six's imbalance and microprice are "
            "exactly such short-horizon forecasts."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def crowd(self):
        cards = VGroup(
            desk_question(r"many executors at once", r"Cardaliaguet and Lehalle (2018): when many funds trade the same "
                          r"way, each one's impact is everyone's cost; a mean-field game of controls (Part 8) gives the "
                          r"equilibrium schedules", width=12.4, font_size=19),
            desk_question(r"predatory trading", r"Brunnermeier and Pedersen (2005): traders who learn of a forced seller "
                          r"sell first and buy back later; secrecy is part of execution", width=12.4, font_size=19),
            desk_question(r"crowded rebalances", r"index changes and month-end flows are public; the cost of trading with "
                          r"the crowd is a measured, recurring tax", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And other executors. <bookmark mark='a'/> When many funds trade the same way, each one's impact is "
            "everyone's cost: Pierre Cardaliaguet and Lehalle solved the equilibrium as a mean-field game, the tool of "
            "Part eight. <bookmark mark='b'/> Markus Brunnermeier and Lasse Pedersen showed how traders who learn of a "
            "forced seller sell first and buy back later: secrecy is part of execution. <bookmark mark='c'/> And public, "
            "crowded flows, like index changes, pay a recurring tax for trading with the crowd."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a reinforcement learner trains for 60{,}000 episodes in the House's order-book simulator to sell "
                       r"20 units in 20 steps. Will it beat a steady TWAP?")
        with self.voiceover(
            "Pause and predict. A reinforcement learner trains for sixty thousand episodes in the House's order-book "
            "simulator, selling twenty units in twenty steps. Will it beat a steady, plain TWAP?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
