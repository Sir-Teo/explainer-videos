from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant22.common import BAD, BASIS, GOOD, OIL, PART, USD, ask, fit_right, illustration, load


class Storage(VoiceoverScene):
    def construct(self):
        o = load("oil_public_example")
        self.card()
        self.carry()
        self.convenience()
        self.snapshots(o)
        self.slope(o)
        self.working()
        self.theory()

    def card(self):
        c = chapter_card(7, r"Storage, carry and the convenience yield", r"What should oil for delivery next year cost?",
                         lit=(2008, 2020), part=PART)
        with self.voiceover("Chapter seven. Commodities: what a barrel for future delivery should cost, and why it "
                            "often does not."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def carry(self):
        rows = [cmath(r"F_{t,T}", r"\le", r"S_t\,e^{(r + u)(T - t)}", font_size=42, colors={r"F_{t,T}": OIL}),
                cmath(r"F_{t,T}", r"=", r"S_t\,e^{(r + u - y)(T - t)}", font_size=42, colors={r"F_{t,T}": OIL})]
        whys = [why('cash and carry: buy a barrel, store it at cost $u$, finance it at $r$, sell it forward. Upper bound assumes accessible deliverable storage, locked financing and costs, and ability to sell forward; futures margin and stochastic rates need additional treatment'),
                why(r"but the reverse trade needs someone to lend you oil, and those who hold it value having it: a "
                    r"refinery cannot stop. That benefit, the convenience yield $y$, can push the future far below the "
                    r"cost of carry (Kaldor, 1939; Working, 1949)")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Cash and carry gives an upper bound when the commodity is deliverable, storage is accessible at the stated cost, financing is locked, and the forward can be sold. Buying and storing spot then locks a delivery payoff. The displayed exponential assumes proportional deterministic carrying costs. Futures margin and stochastic rates require extra care. <bookmark mark='a'/> Reverse cash and carry also requires borrowing the physical commodity, which can be difficult. Holders may value immediate access: the convenience benefit. Scarcity, location, quality and storage constraints can all affect the curve. The second equality is a model-based effective yield representation for positive prices; it is not a universal replication formula or proof of executable arbitrage."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def convenience(self):
        rows = [cmath(r"y - u", r"=", r"r - \frac{1}{T_2 - T_1}\ln\frac{F_{T_2}}{F_{T_1}}", font_size=42,
                      colors={r"y - u": GOOD})]
        whys = [why(r"two futures one month apart give the convenience yield net of storage: positive when the curve "
                    r"slopes down (backwardation, oil is scarce now), negative in steep contango (storage is full, and "
                    r"holders must be paid to keep it)")]
        step = ladder(self, rows, whys, keep=1, top=2.3, x=-0.4, buff=0.8, edge=6.9)
        names = VGroup(
            desk_question(r"backwardation", r"next month's oil cheaper than today's: inventories are low, and having a "
                          r"barrel now is worth a premium", width=12.0, font_size=21),
            desk_question(r"contango", r"next month's oil dearer: inventories are high, and the spread pays for storage "
                          r"and financing", width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Under a positive-price carry approximation, two nearby futures give an effective convenience yield net of storage, using an assumed interval and financing rate. Storage cost and convenience benefit cannot be separated from this price ratio alone. <bookmark mark='a'/> A downward curve is called backwardation; it is often associated with nearby scarcity. <bookmark mark='b'/> An upward curve is contango. Its sign alone does not prove that tanks are full or identify inventories. Risk premia, seasonality, delivery locations and quality also matter. Here adjacent contract numbers are treated as about one month apart, so the annualization is a proxy rather than an exact dated forward-carry calculation."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(names[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(names[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def snapshots(self, o):
        sn = o["snaps"]
        keys_b = ["2008-07-03", "2014-06-20", "2022-03-08"]
        keys_c = ["2008-12-19", "2016-02-11", "2020-04-17"]
        g1 = axes([0.5, 4.5], [90, 160], x_length=5.4, y_length=3.6, xlabel=r"contract (months ahead)",
                  ylabel=r"\$ a barrel", xticks=[1, 2, 3, 4], yticks=[100, 125, 150], font_size=13)
        g2 = axes([0.5, 4.5], [10, 55], x_length=5.4, y_length=3.6, xlabel=r"contract (months ahead)",
                  ylabel=r"\$ a barrel", xticks=[1, 2, 3, 4], yticks=[20, 35, 50], font_size=13)
        VGroup(g1, g2).arrange(RIGHT, buff=1.0).shift(DOWN * 0.5)
        cols = [OIL, BAD, GOOD]

        def curves(g, keys):
            out = VGroup()
            for k, c_ in zip(keys, cols):
                P = np.asarray(sn[k]["P"])
                out.add(VGroup(curve(g.ax, np.arange(1, 5), P, c_, stroke_width=3),
                               *[Dot(g.ax.c2p(i + 1, p), color=c_, radius=0.05) for i, p in enumerate(P)],
                               label(k, font_size=14, color=c_).next_to(g.ax.c2p(4, P[-1]), RIGHT, buff=0.1)))
            return out
        cb, cc_ = curves(g1, keys_b), curves(g2, keys_c)
        t1 = label('backwardation: dated curve examples', font_size=22, color=GOOD).next_to(g1, UP, buff=0.25)
        t2 = label('contango: dated curve examples', font_size=22, color=BAD).next_to(g2, UP, buff=0.25)
        with self.voiceover(
            "The NYMEX crude curve, first to fourth contract, on six days. <bookmark mark='a'/> On the left, "
            "backwardation: July 2008 at a hundred and forty-five dollars, the summer of 2014 before the fall, and "
            "March 2022 after Russia's invasion, when the front contract stood thirteen dollars above the fourth. "
            "<bookmark mark='b'/> On the right, contango: December 2008, when the front month traded at thirty-four "
            "and the fourth at forty-seven, enough to pay tankers to sit at sea full of oil; February 2016's glut; "
            "and the seventeenth of April 2020, three days before the front contract went below zero."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(t1), FadeIn(t2))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c_) for c_ in cb], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c_) for c_ in cc_], lag_ratio=0.4))
        self.add(illustration(r"EIA: NYMEX WTI futures contracts 1--4 (RCLC1--4), daily settlements"))
        self.wait(0.4)
        self.clear_scene()

    def slope(self, o):
        t, sl, c1 = np.asarray(o["t"]), 100 * np.asarray(o["slope"]), np.asarray(o["c1"])
        ok = np.isfinite(sl) & (c1 > 0)
        t, sl, c1 = t[ok], sl[ok], c1[ok]
        off = (sl < -60) | (sl > 120)
        displayed = np.clip(sl, -60, 120)
        g1 = axes([1986, 2025], [0, 150], x_length=10.4, y_length=2.0, xlabel=r"", ylabel=r"front, \$",
                  xticks=[], yticks=[0, 50, 100, 150], font_size=12).to_edge(UP, buff=0.6)
        g2 = axes([1986, 2025], [-60, 120], x_length=10.4, y_length=2.6, xlabel=r"year",
                  ylabel=r"slope, \% a year", xticks=[1990, 2000, 2010, 2020], yticks=[-50, 0, 50, 100], font_size=12
                  ).next_to(g1, DOWN, buff=0.35)
        l1 = curve(g1.ax, t, c1, OIL, stroke_width=2)
        zero = DashedLine(g2.ax.c2p(1986, 0), g2.ax.c2p(2025, 0), color=GREY_B, stroke_width=1.2)
        l2 = curve(g2.ax, t, displayed, BASIS, stroke_width=1.6)
        extremes = VGroup(*[Triangle(color=BAD, fill_opacity=1).scale(0.045).rotate(PI if value < -60 else 0).move_to(g2.ax.c2p(time, np.clip(value, -60, 120))) for time, value in zip(t[off], sl[off])])
        foot = wrapped_label(f"the annualised slope from the first to the fourth contract (viewport $[-60,120]\\%$; red triangles mark off-scale values); in contango {100 * o['contango_share']:.0f}\\% of days since 1986. The slope spikes upward in gluts (1998, 2008--09, 2015--16, 2020) and is most negative when supply is tight",
                             11.8, 17, GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Over four decades. <bookmark mark='a'/> The front-month price above, the curve's slope below, annualised. "
            "<bookmark mark='b'/> The slope leaps upward in every glut: the Asian crisis of 1998, the winter of 2008, "
            "the price war of 2015 and 2016, and April 2020, when it went off the chart. It is negative when supply "
            f"is tight. Over the whole period the curve was in contango on {100 * o['contango_share']:.0f} percent "
            "of days: oil, on most days, was plentiful enough to need storing."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), Create(zero))
            vo.wait_until("a")
            self.play(Create(l1), run_time=2)
            vo.wait_until("b")
            self.play(Create(l2), FadeIn(extremes), FadeIn(foot), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def working(self):
        inv = np.linspace(0.05, 1.0, 120)
        spread = 0.04 * inv - 0.25 * np.exp(-7 * inv)
        g = axes([0, 1.05], [-0.2, 0.06], x_length=7.2, y_length=4.2, xlabel=r"inventories (relative to normal)",
                 ylabel=r"$(F_2 - F_1)/F_1$, a month", xticks=[], yticks=[-0.15, -0.1, -0.05, 0, 0.05], font_size=14
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(1.05, 0), color=GREY_B, stroke_width=1.2)
        line = curve(ax, inv, spread, OIL, stroke_width=3.5)
        cap = DashedLine(ax.c2p(0, 0.045), ax.c2p(1.05, 0.045), color=BAD, stroke_width=1.5)
        capl = label(r"full carry: storage plus financing", font_size=15, color=BAD).next_to(ax.c2p(0.55, 0.045), UP,
                                                                                         buff=0.06)
        side = wrapped_label(r"a stylised Working curve: when stocks are scarce, the spread falls steeply below zero "
                             r"(backwardation, a high convenience yield); when they are ample, it rises toward full carry "
                             r"and stops there, because cash and carry caps it. Illustrative shape", 3.6, 17,
                             GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Holbrook Working drew the shape in 1949. <bookmark mark='a'/> Plot the spread between next month's future "
            "and this month's against inventories. When stocks are scarce, the spread plunges below zero: people pay "
            "heavily to have oil now. As stocks grow it rises, <bookmark mark='b'/> toward full carry, the cost of "
            "storage and financing, and it cannot go beyond, because cash and carry would cap it. The curve is steep "
            "on the left and flat on the right: scarcity moves prices far more than plenty does."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(Create(line), run_time=2)
            vo.wait_until("b")
            self.play(Create(cap), FadeIn(capl), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def theory(self):
        cards = VGroup(
            desk_question(r"the theory of storage", r"Working's curve: the spread between near and far futures rises "
                          r"with inventories, steeply when they are scarce and flat when they are ample", width=12.0,
                          font_size=21),
            desk_question(r"the evidence", r"Gorton, Hayashi and Rouwenhorst (2013): low inventories predict "
                          r"backwardation, higher volatility and higher futures returns, across 31 commodities",
                          width=12.0, font_size=21),
            desk_question(r"what it means for a future", r"a commodity future is not a forecast of the spot price: it "
                          r"is the spot price, adjusted for what holding the stuff costs and is worth", width=12.0,
                          font_size=21),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "The relationship has been measured many times. <bookmark mark='a'/> The spread between near and far "
            "futures rises with inventories: steeply when stocks are scarce, flat when they are ample. "
            "<bookmark mark='b'/> Gary Gorton, Fumio Hayashi and Geert Rouwenhorst confirmed it on thirty-one "
            "commodities: low inventories predict backwardation, higher volatility, and higher returns to holding "
            "futures. <bookmark mark='c'/> A commodity future is not the market's forecast of the spot price. It is "
            "today's price, adjusted for what holding the stuff costs, and what having it is worth."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"the front WTI contract is \$70 and the next is \$71.50, a month later, with rates at 5\%. What is the "
                r"implied convenience yield net of storage, and what does it say about inventories?")
        with self.voiceover("The front oil contract is seventy dollars and the next is seventy-one fifty, a month later, "
                            "with rates at five percent. What convenience yield, net of storage, does that imply, and "
                            "what does it say about inventories?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
