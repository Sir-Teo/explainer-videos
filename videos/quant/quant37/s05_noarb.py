from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant37.common import (BAD, BUY_C, GOOD, IMPACT_C, KERNEL_C, PART, SELL_C, load)


class NoArb(VoiceoverScene):
    def construct(self):
        k = load("kernels")
        self.card()
        self.cost_formula()
        self.permanent()
        self.hs_example()
        self.box(k)
        self.gatheral()
        self.convex()
        self.gauss(k)
        self.refine(k)
        self.btc_passes(load("propagator"))
        self.lessons()
        self.question()

    def card(self):
        c = chapter_card(4, r"No dynamic arbitrage", r"Which models of impact are allowed?", part=PART)
        with self.voiceover("Chapter four, and the answer to the pause: yes. If impact lasted a fixed time and then "
                            "vanished, a trader could buy, wait, and sell into prices still pushed up by the buying. A "
                            "model of impact must not hand out money machines. Jim Gatheral turned that into "
                            "conditions."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def cost_formula(self):
        rows = [cmath(r"p_t", r"=", r"p_0 + \int_0^t G(t - s)\,dX_s + \text{noise}", font_size=38,
                      colors={r"G(t - s)": KERNEL_C}),
                cmath(r"\mathcal C[X]", r"=", r"\tfrac12 \iint G(|t - s|)\,dX_s\,dX_t", font_size=40,
                      colors={r"\mathcal C[X]": IMPACT_C}),
                cmath(r"\text{round trip}", r":", r"\textstyle\int dX = 0", font_size=36)]
        whys = [why(r"linear transient impact: each unit traded pushes the price by a kernel that decays"),
                why(r"the expected cost of a trading programme $X$: every trade pays the impact of the trades before it, "
                    r"and half its own"),
                why(r"a programme that ends flat; with no information, it should never have negative expected cost")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The setting. <bookmark mark='a'/> Linear transient impact: each unit traded pushes the price by a kernel "
            "G that decays. <bookmark mark='b'/> The expected cost of a trading programme is a double integral: every "
            "trade pays the impact left by the trades before it, and half of its own. <bookmark mark='c'/> A round trip "
            "buys and sells back to zero. A trader with no information should never expect to profit from one."
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

    def permanent(self):
        rows = [cmath(r"\text{permanent}", r":", r"p \mathrel{+}= f(v)\,dt", font_size=38),
                cmath(r"\text{no round-trip profit}", r"\Rightarrow", r"f(v) = \kappa\,v", font_size=36,
                      colors={r"f(v) = \kappa\,v": GOOD}),
                cmath(r"\text{cost}", r"=", r"\tfrac12\,\kappa\,X^2\ \text{whatever the schedule}", font_size=34)]
        whys = [why(r"impact that never decays, as a function of the trading rate"),
                why(r"Huberman and Stanzl (2004): if permanent impact were nonlinear, buying fast and selling slowly, or the "
                    r"reverse, would make money; only a linear function forbids it"),
                why(r"so permanent impact cannot be optimised away; only the transient part depends on how one trades")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "First, permanent impact. <bookmark mark='a'/> Suppose trading at rate v moves the price permanently by f "
            "of v. <bookmark mark='b'/> Gur Huberman and Werner Stanzl showed that unless f is linear, buying fast and "
            "selling slowly, or the reverse, makes money. <bookmark mark='c'/> And with linear permanent impact the "
            "cost is one half kappa X squared whatever the schedule: it cannot be optimised away. Only the transient "
            "part depends on how one trades."
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

    def hs_example(self):
        rows = [cmath(r"f(v)", r"=", r"v^2", font_size=40),
                cmath(r"\text{buy 1 in time 1}", r":", r"\Delta p = \int f(1)\,dt = 1", font_size=34, colors={r"\text{buy 1 in time 1}": BUY_C}),
                cmath(r"\text{sell 1 in time 10}", r":", r"\Delta p = -\int f(0.1)\,dt = -0.1", font_size=34,
                      colors={r"\text{sell 1 in time 10}": SELL_C}),
                cmath(r"\text{net}", r":", r"\text{the price ends } 0.9 \text{ higher, holding nothing}", font_size=32,
                      colors={r"\text{net}": BAD})]
        whys = [why(r"suppose permanent impact grew like the square of the trading rate"),
                why(r"buying one unit fast pushes the price up by one"),
                why(r"selling it back slowly pushes it down by only a tenth"),
                why(r"so the selling happened at prices above the buying's average: repeat, and the trader is a money "
                    r"machine; a linear $f$ makes the two moves cancel exactly")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Why it must be linear, in numbers. <bookmark mark='a'/> Suppose permanent impact grew like the square of "
            "the trading rate. <bookmark mark='b'/> Buy one unit quickly, in one unit of time: the price rises by one. "
            "<bookmark mark='c'/> Sell it back slowly, over ten: it falls by only a tenth. <bookmark mark='d'/> The "
            "position is flat and the price is higher: the sales were made at prices above the purchases. Repeat, and "
            "it is a money machine. Only a linear function makes the two moves cancel."
        ) as vo:
            step(0)
            for k_, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k_:
                    step(k_)
        self.wait(0.5)
        self.clear_scene()

    def box(self, k):
        b = k["kernels"]["box"]
        t = np.asarray(k["t"], float)
        v = np.asarray(b["round_trip"], float)
        top = float(np.abs(v).max()) * 1.15
        g = axes([0, 1], [-top, top], x_length=8.4, y_length=3.8, xlabel=r"time", ylabel=r"trades", xticks=[0, 0.5, 1],
                 yticks=[0], font_size=15).move_to(DOWN * 0.4)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.06, height=max(1e-3, abs(ax.c2p(0, x)[1] - ax.c2p(0, 0)[1])),
                                  fill_color=BUY_C if x > 0 else SELL_C, fill_opacity=0.85, stroke_width=0)
                        .move_to(ax.c2p(a, x / 2)) for a, x in zip(t, v)])
        st = label(rf"expected cost of this round trip: ${b['rt_cost']:.3f}$ per unit traded", font_size=20, color=BAD)
        st.to_edge(UP, buff=0.7)
        with self.voiceover(
            "The kernel of the pause: impact that lasts for three-tenths of the horizon, then vanishes. "
            "<bookmark mark='a'/> Search for the cheapest round trip, and the answer is a pattern of buys and sells "
            "timed against the kernel's edge. <bookmark mark='b'/> Its expected cost is negative: "
            f"{b['rt_cost']:.2f} per unit of trading. A money machine, with no information at all. So this kernel is "
            "not a possible model of impact."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in bars], lag_ratio=0.01))
            vo.wait_until("b")
            self.play(FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def gatheral(self):
        rows = [cmath(r"\mathcal C[X] \ge 0", r"\ \forall\, X", r"\iff G\ \text{positive definite}", font_size=36),
                cmath(r"\hat G(\omega)", r"\ge", r"0", font_size=40, colors={r"0": GOOD}),
                cmath(r"\text{box kernel}", r":", r"\hat G = \text{sinc} < 0\ \text{somewhere}", font_size=36,
                      colors={r"\text{box kernel}": BAD})]
        whys = [why(r"Gatheral (2010): no round trip has negative expected cost exactly when the kernel is positive "
                    r"definite as a function of the time difference"),
                why(r"Bochner's theorem: for a symmetric continuous kernel that means a non-negative Fourier transform"),
                why(r"the box's transform is a sinc, negative in places, which is why the money machine exists; decaying "
                    r"exponentials and power laws pass")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The condition. <bookmark mark='a'/> Gatheral showed that no round trip has negative expected cost exactly "
            "when the kernel is positive definite. <bookmark mark='b'/> By Bochner's theorem, that means its Fourier "
            "transform is never negative. <bookmark mark='c'/> The box's transform is a sinc, negative in places: hence "
            "the machine. Decaying exponentials and power laws pass."
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

    def convex(self):
        rows = [cmath(r"G\ \text{convex, decreasing}", r"\Rightarrow", r"\text{optimal } dX \ge 0", font_size=34,
                      colors={r"\text{optimal } dX \ge 0": GOOD}),
                cmath(r"G\ \text{p.d. but not convex}", r"\Rightarrow", r"\text{buy--sell oscillations}", font_size=34,
                      colors={r"\text{buy--sell oscillations}": BAD}),
                cmath(r"\text{e.g.}", r":", r"G(t) = e^{-t^2}", font_size=38)]
        whys = [why(r"Alfonsi, Schied and Slynko (2012): with a convex decreasing kernel the optimal way to buy never "
                    r"sells"),
                why(r"positive definiteness is not enough: some allowed kernels make the best purchase include sales, "
                    r"transaction-triggered price manipulation"),
                why(r"the Gaussian kernel is positive definite (its transform is Gaussian) but concave near zero")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A stronger condition. <bookmark mark='a'/> Aurélien Alfonsi, Alexander Schied and Alla Slynko proved that "
            "with a convex, decreasing kernel the optimal way to buy never sells. <bookmark mark='b'/> Positive "
            "definiteness alone is not enough: some kernels that forbid money machines still make the best purchase "
            "include sales. <bookmark mark='c'/> The Gaussian kernel is one: positive definite, but concave near zero."
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

    def gauss(self, k):
        gg = [x for x in k["gauss"] if x["n"] == 11][0]
        t = np.asarray(gg["t"], float)
        v = np.asarray(gg["v"], float)
        top = float(np.abs(v).max()) * 1.15
        g = axes([-0.05, 1.05], [-top, top], x_length=8.4, y_length=3.8, xlabel=r"time", ylabel=r"trades",
                 xticks=[0, 0.5, 1], yticks=[0], font_size=15).move_to(DOWN * 0.4)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.25, height=max(1e-3, abs(ax.c2p(0, x)[1] - ax.c2p(0, 0)[1])),
                                  fill_color=BUY_C if x > 0 else SELL_C, fill_opacity=0.85, stroke_width=0)
                        .move_to(ax.c2p(a, x / 2)) for a, x in zip(t, v)])
        st = label(rf"to buy 1: buy {1 + gg['sell']:.2f}, sell {gg['sell']:.2f}; cost {gg['cost']:.3f} against TWAP's "
                   rf"{gg['twap']:.3f}", font_size=20, color=BAD).to_edge(UP, buff=0.7)
        with self.voiceover(
            "The Gaussian kernel, on eleven trading dates. <bookmark mark='a'/> The optimal way to buy one unit "
            f"alternates: it buys {1 + gg['sell']:.2f} in total and sells {gg['sell']:.2f} back. <bookmark mark='b'/> "
            f"And it is cheaper than buying steadily, {gg['cost']:.3f} against {gg['twap']:.3f}. A model that recommends "
            "selling in order to buy is telling you its kernel is wrong."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in bars], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def refine(self, k):
        hx = [-3.6, -0.6, 2.2, 4.8]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"trading dates", r"largest trade",
                                                                         r"total sold", r"cost")])
        tab = VGroup(head)
        for r in k["gauss"]:
            tab.add(VGroup(MathTex(str(r["n"]), font_size=26), MathTex(f"{r['max']:,.2f}".replace(",", "{,}"),
                                                                        font_size=26),
                           MathTex(f"{r['sell']:,.2f}".replace(",", "{,}"), font_size=26, color=BAD),
                           MathTex(f"{r['cost']:.3f}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.8 * j, 0])
        foot = wrapped_label(r"the Gaussian kernel, buying 1 unit over a unit of time: finer grids buy cheaper with ever "
                             r"wilder oscillations, and no optimum exists in the limit", 11.0, 16, GREY_A).to_edge(DOWN,
                                                                                                    buff=0.7)
        last = k["gauss"][-1]
        with self.voiceover(
            "Refine the grid and it gets worse. <bookmark mark='a'/> With six dates the optimum barely sells. With "
            f"twenty-one, the largest single trade is about {last['max']:,.0f} units, to buy one. The cost keeps "
            "falling and the trades blow up: there is no optimal strategy in the limit, only ever more violent "
            "manipulation of one's own impact."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def btc_passes(self, p):
        rows = [cmath(r"G(\ell)", r"=", rf"(1 + \ell/{p['G_peak_lag']})^{{-{p['beta']:.2f}}}", font_size=40,
                      colors={r"G(\ell)": KERNEL_C}),
                cmath(r"\text{decreasing, convex}", r":", r"\text{yes}", font_size=38, colors={r"\text{yes}": GOOD}),
                cmath(r"\text{positive definite}", r":", r"\text{yes (Pólya)}", font_size=38, colors={r"\text{yes (Pólya)}": GOOD})]
        whys = [why(r"Chapter 3's propagator, as a power law beyond its peak"),
                why(r"its derivative is negative and its second derivative positive"),
                why(r"Pólya's criterion: an even function that is convex and decreasing to zero on the half-line is "
                    r"positive definite; so the fitted kernel admits no round-trip profit and no buying by selling")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Does Bitcoin's fitted kernel pass? <bookmark mark='a'/> Beyond its peak, Chapter three's propagator is a "
            f"power law with exponent {p['beta']:.2f}. <bookmark mark='b'/> It is decreasing and convex. "
            "<bookmark mark='c'/> And by Pólya's criterion, an even function that is convex and decreasing to zero is "
            "positive definite. So the measured kernel allows neither round-trip profits nor buying by selling: the "
            "market, as fitted, is free of dynamic arbitrage."
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

    def lessons(self):
        cards = VGroup(
            desk_question(r"test the model, not only the data", r"before an impact model drives a trading algorithm, check "
                          r"it is positive definite and, ideally, convex and decreasing", width=12.4, font_size=19),
            desk_question(r"exponential and power laws pass", r"Obizhaeva--Wang's exponential and Bouchaud's power-law "
                          r"propagator are both convex and decreasing", width=12.4, font_size=19),
            desk_question(r"nonlinear transient impact", r"with a power of the rate inside a decaying kernel, Gatheral "
                          r"showed exponential decay forces linearity, and a power-law decay must satisfy an "
                          r"inequality linking its exponent to the impact's; free choices are rare", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The lessons for a desk. <bookmark mark='a'/> Before an impact model drives an algorithm, test the model "
            "itself: positive definite, and ideally convex and decreasing. <bookmark mark='b'/> The exponential of "
            "Obizhaeva and Wang and Bouchaud's power-law propagator both pass. <bookmark mark='c'/> And once impact is "
            "nonlinear in the trading rate, Gatheral showed that exponential decay is impossible, and that a power-law "
            "decay must satisfy an inequality linking its exponent to the impact's: free choices are rare."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"you must sell 5{,}000 BTC within an hour. Trading faster costs more impact; trading slower leaves "
                       r"you exposed to the price for longer. How should a very risk-averse seller trade?")
        with self.voiceover(
            "Pause and predict. You must sell five thousand bitcoin within an hour. Faster costs more impact; slower "
            "leaves you exposed to the price for longer. How should a very risk-averse seller trade?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
