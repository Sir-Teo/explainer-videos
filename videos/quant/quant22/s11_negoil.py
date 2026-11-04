from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant22.common import BAD, BASIS, GOOD, OIL, PART, USD, ask, fit_right, illustration, load


class NegOil(VoiceoverScene):
    def construct(self):
        o = load("oil")
        n = load("negoil")
        self.card()
        self.april(o)
        self.why()
        self.curve20(o)
        self.models()
        self.normal(n)
        self.cme()

    def card(self):
        c = chapter_card(10, r"April 2020: negative oil", r"How can a barrel cost less than nothing?", lit=(2020,),
                         part=PART)
        with self.voiceover("Chapter ten. The twentieth of April 2020, when a barrel of oil cost less than nothing."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def april(self, o):
        d, P = np.asarray(o["april"]["dates"]), np.asarray(o["april"]["P"])
        x = np.arange(len(d))
        g = axes([-0.5, len(d) - 0.5], [-45, 35], x_length=8.2, y_length=4.4, xlabel=r"trading days of April 2020",
                 ylabel=r"\$ a barrel", xticks=[], yticks=[-40, -20, 0, 20], font_size=14).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.3)
        ax = g.ax
        zero = Line(ax.c2p(-0.5, 0), ax.c2p(len(d) - 0.5, 0), color=WHITE, stroke_width=1.2)
        k = int(np.where(d == 20200420)[0][0])
        ca = VGroup(curve(ax, x[:k], P[:k, 0], BAD, stroke_width=3),
                    *[Dot(ax.c2p(a, b), color=BAD, radius=0.05) for a, b in zip(x[:k], P[:k, 0])])
        cb = VGroup(curve(ax, x[k - 1:], P[k - 1:, 0], BAD, stroke_width=3),
                    *[Dot(ax.c2p(a, b), color=BAD, radius=0.05) for a, b in zip(x[k:], P[k:, 0])])
        l2 = curve(ax, x, P[:, 1], OIL, stroke_width=2.5)
        ticks = VGroup(*[label(str(int(dd) % 100), font_size=13).next_to(ax.c2p(i, -45), DOWN, buff=0.08)
                         for i, dd in enumerate(d) if i % 2 == 0])
        side = VGroup(
            legend([(BAD, r"contract 1 (May, until the 21st)"), (OIL, r"contract 2")], font_size=17),
            MathTex(rf"20\ \text{{April}}:\ {P[k, 0]:.2f}", font_size=30, color=BAD),
            MathTex(rf"\text{{the June contract}}:\ {P[k, 1]:.2f}", font_size=26, color=OIL),
            wrapped_label(r"NYMEX settlements (EIA). The May contract's last trading day was the 21st; on the 22nd "
                          r"contract 1 is June", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "April 2020. The world had stopped driving and flying, and oil kept coming out of the ground. "
            "<bookmark mark='a'/> The May crude contract had been falling all month. On Friday the seventeenth it "
            "settled at eighteen dollars. <bookmark mark='b'/> On Monday the twentieth it settled at minus "
            f"{abs(P[k, 0]):.2f}: a seller paid buyers almost thirty-eight dollars to take each barrel. "
            f"<bookmark mark='c'/> The June contract, a month later, closed at {P[k, 1]:.2f}. Only the expiring "
            "contract went below zero."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(ticks), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(ca), run_time=2)
            vo.wait_until("b")
            self.play(Create(cb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(l2), FadeIn(side[2]), FadeIn(side[3]))
        self.add(illustration(r"EIA: RCLC1, RCLC2"))
        self.wait(0.4)
        self.clear_scene()

    def why(self):
        cards = VGroup(
            desk_question(r"physical delivery", r"a WTI future is a promise to take 1,000 barrels at Cushing, Oklahoma, "
                          r"during the delivery month. Holding it past the last trading day means taking the oil", width=12.0,
                          font_size=21),
            desk_question(r"no room", r"storage at Cushing, and on every tanker that could be chartered, was filling "
                          r"fast; a holder without a tank had to sell before the 21st to someone with one", width=12.0,
                          font_size=21),
            desk_question(r"a negative price", r"when the only buyers are those with space, and space has run out, the "
                          r"price of a barrel is minus the price of a tank. The contract was always free to go below "
                          r"zero; nobody had expected it to", width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Why? <bookmark mark='a'/> A crude future is not a bet on a price; it is a promise to take a thousand "
            "barrels at Cushing, Oklahoma, the following month. Anyone still holding the May contract after the "
            "twenty-first would have to take the oil. <bookmark mark='b'/> And the tanks were filling. Holders "
            "without storage, including funds that had never meant to take a barrel, had to sell to the few who "
            "had space. <bookmark mark='c'/> When storage is the scarce thing, the price of a barrel is minus the "
            "price of a place to put it. Chapter seven's cost of carry, with the storage cost gone vertical."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def curve20(self, o):
        sn = o["snaps"]
        g = axes([0.5, 4.5], [-45, 40], x_length=6.8, y_length=4.4, xlabel=r"contract", ylabel=r"\$ a barrel",
                 xticks=[1, 2, 3, 4], yticks=[-40, -20, 0, 20, 40], font_size=14).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        zero = Line(ax.c2p(0.5, 0), ax.c2p(4.5, 0), color=WHITE, stroke_width=1.2)
        out = VGroup()
        for k, c_ in (("2020-04-17", OIL), ("2020-04-20", BAD), ("2020-04-21", USD)):
            P = np.asarray(sn[k]["P"])
            out.add(VGroup(curve(ax, np.arange(1, 5), P, c_, stroke_width=3),
                           *[Dot(ax.c2p(i + 1, p), color=c_, radius=0.06) for i, p in enumerate(P)]))
        P20 = np.asarray(sn["2020-04-20"]["P"])
        side = VGroup(
            legend([(OIL, r"17 April"), (BAD, r"20 April"), (USD, r"21 April")], font_size=17),
            MathTex(rf"F_2 - F_1 = \${P20[1] - P20[0]:.2f}", font_size=28, color=BAD),
            wrapped_label(r"a one-month spread of 58 dollars: what it was worth on the 20th to hold oil for one more "
                          r"month. On the 21st the front contract, now the last day's, was back above zero", 3.6, 17,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The curve on three days. <bookmark mark='a'/> On the seventeenth, a steep contango. "
            "<bookmark mark='b'/> On the twentieth, the front fell off a cliff: fifty-eight dollars between May and "
            "June, the value of one month of storage. <bookmark mark='c'/> The next day, the contract's last, it "
            "settled at ten dollars. Nothing about the world's oil changed between those days; only who had to sell, "
            "and how much room was left."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side[0]))
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(Create(out[i]))
                if i == 1:
                    self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def models(self):
        rows = [cmath(r"\text{Black-76}:\ dF", r"=", r"\sigma F\,dW\ \Rightarrow\ F_T > 0", font_size=38,
                      colors={r"\text{Black-76}:\ dF": BAD}),
                cmath(r"\text{Bachelier}:\ dF", r"=", r"\sigma_N\,dW\ \Rightarrow\ F_T \sim \mathcal{N}(F, \sigma_N^2 T)",
                      font_size=38, colors={r"\text{Bachelier}:\ dF": GOOD}),
                cmath(r"P_N(K)", r"=", r"(K - F)\,N\Big(\frac{K - F}{\sigma_N\sqrt T}\Big) + \sigma_N\sqrt T\,"
                      r"\varphi\Big(\frac{K - F}{\sigma_N\sqrt T}\Big)", font_size=32, colors={r"P_N(K)": GOOD})]
        whys = [why(r"the lognormal model every options system used: prices proportional to the price, so it can never "
                    r"reach zero, and cannot even be evaluated at a negative future or strike"),
                why(r"Louis Bachelier's model of 1900: moves of a fixed size in dollars, whatever the level; the future "
                    r"can cross zero"),
                why(r"the normal-model put, defined for any $F$ and $K$, negative included (Part 19, chapter 7, used it "
                    r"for negative interest rates)")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "The options on those futures broke the industry's models. Black's model, the lognormal standard, makes "
            "every move proportional to the price, so the price can approach zero but never cross it; with a "
            "negative future it cannot even be evaluated. <bookmark mark='a'/> Louis Bachelier's model of 1900 makes "
            "moves a fixed size in dollars, whatever the level, so the future can go below zero. "
            "<bookmark mark='b'/> Its put formula works for any future and any strike, negative or not. Part "
            "nineteen used it for negative interest rates; in April 2020 oil needed it too."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def normal(self, n):
        Fs, put0 = np.asarray(n["Fs"]), np.asarray(n["put0"])
        g = axes([-10, 20], [0, 16], x_length=7.2, y_length=4.4, xlabel=r"the future, \$", ylabel=r"put struck at \$0",
                 xticks=[-10, -5, 0, 5, 10, 15, 20], yticks=[0, 5, 10, 15], font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        line = curve(ax, Fs, put0, GOOD, stroke_width=3.5)
        intr = curve(ax, Fs, np.maximum(-Fs, 0), GREY_B, stroke_width=2)
        side = VGroup(
            MathTex(rf"\sigma_N = \${n['sn_atm']:.1f}\ \text{{a year}}", font_size=26, color=GOOD),
            wrapped_label(rf"a one-month option. A Black volatility of {100 * n['black_vol']:.0f}\% on a \$10 future is "
                          rf"a normal volatility of about \${n['sn_atm']:.0f}: the same option, quoted in dollars instead "
                          r"of percent. Under Black, a put struck at zero is worth nothing at any positive future; "
                          r"under Bachelier it is worth something everywhere", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The difference matters most exactly where Black said nothing could happen. <bookmark mark='a'/> A put "
            "struck at zero, priced in Bachelier's model with a normal volatility of about fifteen dollars a year, "
            "the equivalent of a hundred and fifty percent lognormal on a ten-dollar future. In Black's model that "
            "put is worthless at any positive future. In Bachelier's it is worth "
            "a cent or two with the future at ten, about "
            f"{np.interp(0.0, Fs, put0):.2f} dollars with the future at zero, and its intrinsic value and more once the "
            "future goes below. Traders who sold such puts as "
            "free money learned the difference in one afternoon."
        ) as vo:
            self.play(FadeIn(g), Create(intr))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def cme(self):
        cc = crisis_card(r"April 2020", r"CME switches to Bachelier",
                         r"on 8 April CME Clearing told members it would move options on crude oil to the Bachelier "
                         r"model if futures fell toward zero, and that its systems could handle negative prices; on 21 "
                         r"April it announced the switch, effective the 22nd, for WTI, Brent and related options; it "
                         r"reverted later that year once prices recovered",
                         stats=[(r"-\$37.63", r"May WTI, 20 April 2020"), (r"\text{22 April}", r"Bachelier in production")],
                         width=8.8, font_size=19).move_to(UP * 0.3)
        foot = wrapped_label(r"the lesson for the House: every model's domain must include every price the contract "
                             r"allows, not only those that have happened", 11.0, 19, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The exchange had seen it coming, just. On the eighth of April CME told its members that if crude futures "
            "fell toward zero it would move their options to Bachelier's model, and that its systems could take "
            "negative prices. <bookmark mark='a'/> On the twenty-second it did, for crude oil options, and switched "
            "back later that year when prices recovered. The lesson goes beyond oil: a model's domain must include "
            "every price the contract allows, not only those that have happened."
        ) as vo:
            self.play(FadeIn(cc))
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.add(illustration(r"CME Clearing advisories 20-152 (8 April 2020) and 20-171 (21 April 2020)"))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a fund is long the front-month oil future with no storage, a week before its last trading day, and the "
                r"curve is in steep contango. What are its choices, and which one sets the price?")
        with self.voiceover("A fund is long the front-month oil future, with no storage, a week before the last trading "
                            "day, in a steep contango. What are its choices, and which one sets the price?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
