from __future__ import annotations

from videos.economics.econ2.common import *  # noqa: F403

DESIGN_NAME = {"symmetric": r"Part 1's pit: \ balanced", "lopsided": r"sellers' surplus large",
               "flat_supply": r"supply flat at \$2.00", "flat_demand": r"demand flat at \$2.60"}


class Converge(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Why it converges", r"What pushes a price into the band, and is the push intelligence or the "
             r"rules?", "Chapter five. Why it converges.", lit={1993: r"zero-intelligence traders"},
             scale=("person", "market"), horizon=("a day",))
        self.push()
        self.zero()
        self.why()
        self.called()
        self.fact()

    # ------------------------------------------------------------------
    def push(self):
        sup = load("supply")
        m = Market(tuple(sup["values"]), tuple(sup["costs"]))
        ax = price_axes(10, (1, 3.5), x_length=6.0, y_length=4.6, qticks=list(range(0, 11, 2)),
                        pticks=[1, 1.5, 2, 2.5, 3, 3.5], qlabel=r"units", plabel=r"price", center=LEFT * 3.5 + DOWN * 0.4)
        a = ax.ax
        st = market_steps(a, m.steps())
        lo, hi = sup["lo"], sup["hi"]
        band = Rectangle(width=a.c2p(10, 0)[0] - a.c2p(0, 0)[0], height=a.c2p(0, hi)[1] - a.c2p(0, lo)[1],
                         stroke_width=0, fill_color=E.ACCENT, fill_opacity=0.22).move_to((a.c2p(0, lo) + a.c2p(10, hi)) / 2)
        high, low = 2.75, 1.85
        dh, sh = m.demand(high), m.supply(high)
        dl, sl = m.demand(low), m.supply(low)
        ph = DashedLine(a.c2p(0, high), a.c2p(10, high), color=E.SUPPLY, stroke_width=2.5)
        pl = DashedLine(a.c2p(0, low), a.c2p(10, low), color=E.DEMAND, stroke_width=2.5)
        extra_s = Line(a.c2p(dh, high), a.c2p(sh, high), color=E.SUPPLY, stroke_width=9)
        extra_d = Line(a.c2p(sl, low), a.c2p(dl, low), color=E.DEMAND, stroke_width=9)
        down = Arrow(a.c2p(9.3, high + 0.05), a.c2p(9.3, hi + 0.08), buff=0, color=E.SUPPLY, stroke_width=4)
        up = Arrow(a.c2p(9.3, low - 0.05), a.c2p(9.3, lo - 0.08), buff=0, color=E.DEMAND, stroke_width=4)
        def two(a_, b_, col, size=22):
            return VGroup(label(a_, font_size=size, color=col), label(b_, font_size=size, color=col)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08)

        rt = VGroup(
            two(rf"at {dollars(high)}: \ {sh} sellers want to sell,", rf"but only {dh} buyers want to buy", E.SUPPLY),
            two(r"an idle seller offers a little less,", r"and still gains", GREY_A),
            two(rf"at {dollars(low)}: \ {dl} buyers want to buy,", rf"but only {sl} sellers will sell", E.DEMAND),
            two(r"an unserved buyer bids a little more,", r"and still gains", GREY_A),
            two(r"only inside the band", r"can nobody gain by changing a call", E.ACCENT, 24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4).shift(UP * 0.1)
        with self.voiceover(
            "Why does a market find the band at all? Go back to Part one's balanced pit. "
            f"<bookmark mark='a'/> Suppose deals were being struck at {money_words(high)}. At that price "
            f"{sh} sellers would like to sell, but only {dh} buyers want to buy. <bookmark mark='b'/> Some seller "
            "is left holding a unit, and the price is well above her cost. If she offers a little less, she makes a "
            "sale and still gains. So the offers come down. <bookmark mark='c'/> Now suppose deals were at "
            f"{money_words(low)}. Then {dl} buyers want to buy and only {sl} sellers will sell, and an unserved "
            "buyer can bid a little more and still gain. So the bids go up. <bookmark mark='d'/> Only inside the "
            "band can nobody gain by changing what they call out. Economists call that an equilibrium: a state in "
            "which no one has a reason to move."
        ) as vo:
            self.play(FadeIn(ax), Create(st.demand), Create(st.supply), FadeIn(band), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(ph), FadeIn(extra_s), FadeIn(rt[0]))
            vo.wait_until("b")
            self.play(GrowArrow(down), FadeIn(rt[1]))
            vo.wait_until("c")
            self.play(Create(pl), FadeIn(extra_d), FadeIn(rt[2]))
            self.play(GrowArrow(up), FadeIn(rt[3]))
            vo.wait_until("d")
            self.play(FadeIn(rt[4], shift=UP * 0.1), Indicate(band, color=E.ACCENT, scale_factor=1.02))
        self.clear_scene()

    def zero(self):
        d = load("asym")
        order = ("symmetric", "lopsided", "flat_supply", "flat_demand")
        ax = price_axes(4, (1.8, 2.9), x_length=10.4, y_length=4.4, qticks=None, pticks=[1.8, 2.0, 2.2, 2.4, 2.6, 2.8],
                        qlabel="", plabel=r"final-period price", center=DOWN * 0.45)
        a = ax.ax
        items = VGroup()
        for k, name in enumerate(order):
            z = d[name]
            x = k + 0.5
            band = Rectangle(width=1.4, height=max(a.c2p(0, z["hi"])[1] - a.c2p(0, z["lo"])[1], 0.05), stroke_width=0,
                             fill_color=E.ACCENT, fill_opacity=0.45).move_to((a.c2p(x, z["lo"]) + a.c2p(x, z["hi"])) / 2)
            zi = Dot(a.c2p(x - 0.12, z["zi"]["price"]), radius=0.1, color=GREY_B)
            zp = Dot(a.c2p(x + 0.12, z["zip"]["price"]), radius=0.1, color=E.AGORA)
            name_l = label(DESIGN_NAME[name], font_size=19, color=GREY_A).next_to(a.c2p(x, 1.8), DOWN, buff=0.2)
            miss = label(rf"{z['zi_miss']:+.2f}".replace("-", "$-$"), font_size=19, color=GREY_B).next_to(zi, LEFT,
                                                                                                         buff=0.12)
            items.add(VGroup(band, zi, zp, name_l, miss))
        leg = VGroup(
            VGroup(Square(0.22, stroke_width=0, fill_color=E.ACCENT, fill_opacity=0.6),
                   label(r"the competitive band", font_size=20, color=E.ACCENT)).arrange(RIGHT, buff=0.12),
            VGroup(Dot(radius=0.09, color=GREY_B), label(r"zero intelligence", font_size=20, color=GREY_B)).arrange(RIGHT, buff=0.12),
            VGroup(Dot(radius=0.09, color=E.AGORA), label(r"traders who learn", font_size=20, color=E.AGORA)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.5)
        cite = published_tag(r"Gode and Sunder (1993), \emph{JPE} 101; \ Cliff and Bruten (1997), HP Labs", corner=DL,
                             font_size=16)
        tag = agora_tag(r"computed: Agora; medians of 41 runs, sixth period", corner=DR, font_size=16)
        sym = d["symmetric"]
        with self.voiceover(
            "In Part one we met traders with no intelligence at all, the creation of Dhananjay Gode and Shyam "
            "Sunder in 1993. Each one calls out a random price that can't lose it money, and none of them learns "
            "anything. <bookmark mark='a'/> In the balanced pit, their prices settled close to the band, and they "
            "made almost all of the possible gains. It looked as if the rules of the market did nearly all the "
            "work. <bookmark mark='b'/> In 1997 Dave Cliff and Janet Bruten, at Hewlett-Packard's laboratories, "
            "asked Smith's question about them: was that an accident of symmetry? Here is the test, run in Agora "
            "on four markets. <bookmark mark='c'/> In the three lopsided ones, the random traders miss: by "
            f"{abs(d['lopsided']['zi_miss']) * 100:.0f} cents when the sellers' surplus is large, by "
            f"{abs(d['flat_supply']['zi_miss']) * 100:.0f} cents when supply is flat, by "
            f"{abs(d['flat_demand']['zi_miss']) * 100:.0f} cents when demand is. <bookmark mark='d'/> The traders who "
            f"learn are within {max(abs(d[n]['zip_miss']) for n in order) * 100:.0f} cents of the band in every one. "
            "Cliff and Bruten's title said it: zero is not enough."
        ) as vo:
            self.play(FadeIn(leg), FadeIn(cite), FadeIn(tag), FadeIn(ax), *[FadeIn(it[3]) for it in items])
            vo.wait_until("a")
            self.play(FadeIn(items[0][0]), FadeIn(items[0][1], scale=0.5), FadeIn(items[0][4]))
            self.play(FadeIn(items[0][2], scale=0.5))
            vo.wait_until("b")
            for it in items[1:]:
                self.play(FadeIn(it[0]), run_time=0.6)
            vo.wait_until("c")
            for it in items[1:]:
                self.play(FadeIn(it[1], scale=0.5), FadeIn(it[4]), run_time=0.7)
            vo.wait_until("d")
            self.play(*[FadeIn(it[2], scale=0.5) for it in items[1:]])
        self.clear_scene()

    def why(self):
        d = load("asym")["flat_supply"]
        ax = price_axes(10, (0, 5), x_length=6.6, y_length=4.4, qticks=list(range(0, 11, 2)), pticks=[0, 1, 2, 3, 4, 5],
                        qlabel=r"units", plabel=r"price", center=LEFT * 2.7 + DOWN * 0.4)
        a = ax.ax
        m = Market(tuple(d["values"]), tuple(d["costs"]))
        st = market_steps(a, m.steps())
        rng = np.random.default_rng(7)
        asks = VGroup(*[Dot(a.c2p(rng.uniform(0.2, 9.8), rng.uniform(2.0, 5.0)), radius=0.045, color=E.SUPPLY)
                        for _ in range(40)])
        bids = VGroup()
        for k, v in enumerate(sorted(d["values"], reverse=True)):
            for _ in range(4):
                bids.add(Dot(a.c2p(k + rng.uniform(0.1, 0.9), rng.uniform(0, v)), radius=0.045, color=E.DEMAND))
        rt = VGroup(
            label(r"zero intelligence:", font_size=26, color=GREY_B),
            label(r"sellers ask anything from \$2 to \$5", font_size=22, color=E.SUPPLY),
            label(r"buyers bid anything below their cards", font_size=22, color=E.DEMAND),
            label(rf"deals average {dollars(d['zi']['price'])}: \ set by the spread of the cards", font_size=22,
                  color=GREY_A),
            label(r"traders who learn:", font_size=26, color=E.AGORA),
            label(r"an offer that goes unanswered comes down", font_size=22, color=GREY_A),
            label(rf"deals settle at {dollars(d['zip']['price'])}: \ the sellers' cost", font_size=22, color=E.AGORA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP * 0.3)
        take = label(r"the rules give the efficiency; \ the learning gives the price", font_size=28, color=E.ACCENT)
        take.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Why do random traders miss? Look at the market where every seller's cost is two dollars. "
            "<bookmark mark='a'/> A random seller asks for any price between two dollars and the top of the "
            "range, five. <bookmark mark='b'/> A random buyer bids anything below her card. "
            f"<bookmark mark='c'/> Deals happen when a high bid meets a low ask, and they average about "
            f"{money_words(d['zi']['price'])}. That number comes from how widely the cards are spread, not from "
            "where the curves cross. <bookmark mark='d'/> A trader who learns does what the random one can't: when "
            "her offer goes unanswered, she lowers it. With ten sellers all able to sell at two dollars, the price "
            f"falls to {money_words(d['zip']['price'])}, their cost, where the theory says it must. "
            "<bookmark mark='e'/> So the rules of the double auction give a market most of its efficiency, as Gode "
            "and Sunder said. The price itself needs traders who respond to what they see."
        ) as vo:
            self.play(FadeIn(ax), Create(st.demand), Create(st.supply), run_time=1.5)
            self.play(FadeIn(rt[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in asks], lag_ratio=0.03), FadeIn(rt[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in bids], lag_ratio=0.03), FadeIn(rt[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rt[3]))
            vo.wait_until("d")
            self.play(FadeOut(asks), FadeOut(bids), FadeIn(rt[4]), FadeIn(rt[5]))
            self.play(FadeIn(rt[6]))
            vo.wait_until("e")
            self.play(FadeIn(take, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["smith_1956"]
        cc = call_card(r"Vernon Smith", c.when, r"the competitive model will fail to predict the outcome",
                       r"the market converged to near the predicted price and quantity, \ and lopsided markets "
                       r"converged too", c.verdict, width=11.4, font_size=26).move_to(UP * 0.5)
        after = label(r"the start of experimental economics: \ Nobel prize, 2002", font_size=26, color=GREY_A)
        after.next_to(cc, DOWN, buff=0.5)
        src = published_tag(r"Smith (1962), \emph{JPE} 70: 111--137; \ Smith, Nobel autobiography (2002)", corner=DR,
                            font_size=17)
        with self.voiceover(
            "So we can score the prediction from the start of the part. <bookmark mark='a'/> In January 1956 "
            "Vernon Smith expected the competitive model to fail. It predicted the price and the quantity of his "
            "first market, and of the lopsided one he ran to check. <bookmark mark='b'/> The verdict is wrong, and "
            "it's the most productive wrong prediction in this series. It started experimental economics, and won "
            "Smith a Nobel prize in 2002."
        ) as vo:
            self.play(FadeIn(src), FadeIn(cc.card), FadeIn(cc[1]))
            vo.wait_until("b")
            self.play(FadeIn(cc.stamp, scale=1.4))
            self.play(FadeIn(after))
        self.clear_scene()

    def fact(self):
        d = load("asym")
        fc = fact_card(r"double auctions converge to the competitive price within a few rounds",
                       columns=((r"your guess", label(r"chapter 4", font_size=24, color=E.ACCENT)),
                                (r"the data", label(r"Smith (1962): \ yes, \ in his designs", font_size=24)),
                                (r"Agora", VGroup(label(r"learners: \ yes, by period 3", font_size=22, color=E.AGORA),
                                                  label(r"zero intelligence: \ only if balanced", font_size=22,
                                                        color=GREY_B)).arrange(DOWN, buff=0.12))),
                       width=12.4, font_size=24)
        with self.voiceover(
            "And the first of the Facts gets its columns. Double auctions converge to the "
            "competitive price within a few rounds. Smith's students did it. Agora's learning traders do it by the "
            "third period, in every market we tried. Traders with no intelligence do it only when the market is "
            "balanced. So Agora agrees with the Fact, and we know which part of Agora is doing the agreeing."
        ):
            self.play(FadeIn(fc, shift=UP * 0.2))
        self.clear_scene()
