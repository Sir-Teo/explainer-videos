from __future__ import annotations

from videos.economics.econ2.common import *  # noqa: F403


class Controls(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Price controls", r"What happens when the law holds a price still?",
             "Chapter ten. Price controls.", lit={1973: r"queues for petrol", 1994: r"San Francisco's rent control"},
             scale=("market", "city"), horizon=("a year", "a decade"))
        self.cap()
        self.lottery()
        self.waiting()
        self.rent()
        self.floor()
        self.ought()

    # ------------------------------------------------------------------
    def cap(self):
        c_ = load("controls")
        sup = load("supply")
        v, c = sup["values"], sup["costs"]
        cap = c_["cap"]["price"]
        ax = price_axes(10, (1, 3.5), x_length=6.6, y_length=4.6, qticks=list(range(0, 11, 2)),
                        pticks=[1, 1.5, 2, 2.5, 3, 3.5], qlabel=r"units", plabel=r"price", center=LEFT * 3.0 + DOWN * 0.4)
        a = ax.ax
        st = market_steps(a, Market(tuple(v), tuple(c)).steps())
        cl = Line(a.c2p(0, cap), a.c2p(10, cap), color=CAP, stroke_width=4)
        clab = label(rf"the legal maximum: \ {dollars(cap)}", font_size=22, color=CAP).next_to(a.c2p(0.15, cap), UP,
                                                                                              buff=0.12)
        clab.align_to(cl, LEFT).shift(RIGHT * 0.1)
        k, n = c_["cap"]["sellers"], c_["cap"]["wanting"]
        short = BraceBetweenPoints(a.c2p(k, cap), a.c2p(n, cap), direction=DOWN, color=CAP)
        sl = label(rf"shortage: \ {n - k}", font_size=22, color=CAP).next_to(short, DOWN, buff=0.08)
        rows = VGroup(
            label(rf"{k} sellers can sell at {dollars(cap)}", font_size=25, color=E.SUPPLY),
            label(rf"{n} buyers want to buy at {dollars(cap)}", font_size=25, color=E.DEMAND),
            label(r"which of them get the units?", font_size=27, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(UP * 0.6)
        with self.voiceover(
            f"Now let the law set a price. Back in the pit, suppose no unit may sell for more than "
            f"{money_words(cap)}, below the band. <bookmark mark='a'/> At that price only the sellers whose costs are "
            f"{money_words(cap)} or less will sell: {k} of them. <bookmark mark='b'/> But {n} buyers want to buy. "
            f"There's a shortage of {n - k}. <bookmark mark='c'/> The price can't do its job of deciding who gets "
            "the scarce units, so something else has to. The question is what."
        ) as vo:
            self.play(FadeIn(ax), Create(st.demand), Create(st.supply), run_time=1.5)
            self.play(Create(cl), FadeIn(clab))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), GrowFromCenter(short), FadeIn(sl))
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()

    def lottery(self):
        c_ = load("controls")["cap"]
        ax = price_axes(3, (0, 1.18), x_length=7.4, y_length=4.4, qticks=None, pticks=[0, 0.25, 0.5, 0.75, 1],
                        qlabel="", plabel=r"share of the most the market could make", money=False,
                        center=LEFT * 2.2 + DOWN * 0.5)
        a = ax.ax
        vals = [(r"to the keenest buyers", c_["best_share"], E.GAIN),
                (r"by lottery", c_["lottery_share"], GREY_B),
                (r"Agora's traders", c_["zip"]["efficiency"], E.AGORA)]
        bars = VGroup()
        for i, (name, x, col) in enumerate(vals):
            b = Rectangle(width=1.5, height=a.c2p(0, x)[1] - a.c2p(0, 0)[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((a.c2p(i + 0.5, 0) + a.c2p(i + 0.5, x)) / 2)
            t = label(pct(x, 1), font_size=26, color=WHITE).next_to(b, UP, buff=0.1)
            nm = label(name, font_size=21, color=GREY_A).next_to(a.c2p(i + 0.5, 0), DOWN, buff=0.2)
            bars.add(VGroup(b, t, nm))
        rt = VGroup(
            label(r"the triangle alone: \ one unit fewer", font_size=23, color=E.GAIN),
            label(r"the lottery: \ the units go to whoever", font_size=23, color=GREY_B),
            label(r"calls first, \ keen or not", font_size=23, color=GREY_B),
            label(r"learning traders all bid the cap,", font_size=23, color=E.AGORA),
            label(r"so calling first is all that counts", font_size=23, color=E.AGORA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.45).shift(UP * 0.4)
        tag = agora_tag(r"computed: Agora; medians of 41 runs, sixth period", corner=DR, font_size=16)
        with self.voiceover(
            "There are two answers on paper. <bookmark mark='a'/> If the five units went to the five keenest "
            "buyers, the market would lose only the triangle, one unit's worth, and still make "
            f"{100 * c_['best_share']:.1f} percent of what it could. <bookmark mark='b'/> If they went by lottery "
            "among everyone who wants one, some would go to buyers who value them least, and the market would make "
            f"only {100 * c_['lottery_share']:.0f} percent. <bookmark mark='c'/> Run the pit, and Agora's learning "
            f"traders make {100 * c_['zip']['efficiency']:.0f} percent: the lottery, almost exactly. Under the cap "
            "every buyer soon bids the maximum, so a unit goes to whoever calls first, whatever his card. "
            "<bookmark mark='d'/> That's the hidden cost of a price control. The triangle is only part of it; "
            "the rest is that the goods end up with the wrong people. Edward Glaeser and Erzo Luttmer found it in "
            "New York's rent-controlled flats: compared with cities without rent control, a sizeable share of "
            "apartments housed the wrong kinds of households."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]), FadeIn(rt[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]), FadeIn(rt[1]), FadeIn(rt[2]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][1:]), FadeIn(rt[3]), FadeIn(rt[4]))
            vo.wait_until("d")
            self.play(Indicate(bars[2][0], color=E.AGORA, scale_factor=1.03))
        self.clear_scene()

    def waiting(self):
        hc = history_card(r"1973--74 and 1979", r"petrol queues in the United States",
                          r"with the price of petrol held down by law, drivers waited for hours, and states let cars "
                          r"fill up only on odd or even days", color=CAP, width=8.6, font_size=25).to_edge(UP, buff=0.6)
        price = VGroup(
            label(r"a queue is a price", font_size=36, color=E.ACCENT),
            label(r"paid in time, \ which nobody receives", font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(hc, DOWN, buff=0.8)
        who = label(r"it favours those whose time is cheap, \ not those who value the petrol most", font_size=26,
                    color=WHITE).next_to(price, DOWN, buff=0.6)
        src = published_tag(r"Deacon and Sonstelie (1985), \emph{JPE} 93: 627--647: Chevron's stations, "
                            r"California, 1980", corner=DR, font_size=16)
        with self.voiceover(
            "In the real world the commonest answer is a queue. <bookmark mark='a'/> In 1973 and 74, and again in "
            "1979, the United States held the price of petrol below what the market would have set, and drivers "
            "waited at the pumps for hours; some states let cars fill up only on odd or even days. "
            "<bookmark mark='b'/> A queue is a price too, paid in time instead of money, and nobody receives it. "
            "<bookmark mark='c'/> And it hands the goods to whoever's time is cheapest, which is not the same as "
            "whoever values them most. In 1980 a court order held down the price at Chevron's stations in California, "
            "and Robert Deacon and Jon Sonstelie used the queues that formed to measure what drivers' time was worth "
            "to them."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(price, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(who, shift=UP * 0.1))
        self.clear_scene()

    def rent(self):
        sc = study_card(r"Rent control in San Francisco", r"Rebecca Diamond, Tim McQuade and Franklin Qian (2019)",
                        [(r"what", r"in 1994 the city extended rent control to small apartment buildings built before "
                                   r"1980; \ newer ones stayed uncontrolled"),
                         (r"tenants", r"20\% less likely to move; \ fewer displaced from the city"),
                         (r"landlords", r"cut the rental housing they offered by 15\%, \ selling to owner-occupiers "
                                        r"and redeveloping"),
                         (r"so", r"less rental housing, \ which likely pushed up market rents")],
                        design="DiD", width=10.6, font_size=23).move_to(UP * 0.2)
        src = published_tag(r"Diamond, McQuade and Qian (2019), \emph{American Economic Review} 109(9)", corner=DR,
                            font_size=16)
        with self.voiceover(
            "The best evidence on a modern price control comes from San Francisco. <bookmark mark='a'/> In 1994 "
            "the city extended rent control to small apartment buildings built before 1980, and left those built "
            "later uncontrolled, which gave Rebecca Diamond, Tim McQuade and Franklin Qian a comparison. "
            "<bookmark mark='b'/> Rent control did what it was meant to do for sitting tenants: they were about "
            "twenty percent less likely to move, and fewer were pushed out of the city. <bookmark mark='c'/> But "
            "landlords of the controlled buildings cut the rental housing they offered by fifteen percent, by "
            "selling to owner-occupiers and redeveloping. <bookmark mark='d'/> Less rental housing means higher "
            "rents for everyone looking for a flat, and the authors concluded that this probably undid much of what "
            "the law set out to achieve."
        ) as vo:
            self.play(FadeIn(src), FadeIn(sc.card), FadeIn(sc.head), FadeIn(sc[2:] if len(sc) > 2 else VGroup()))
            vo.wait_until("a")
            self.play(FadeIn(sc.body[0]))
            vo.wait_until("b")
            self.play(FadeIn(sc.body[1]))
            vo.wait_until("c")
            self.play(FadeIn(sc.body[2]))
            vo.wait_until("d")
            self.play(FadeIn(sc.body[3]))
        self.clear_scene()

    def floor(self):
        c_ = load("controls")["floor"]
        sup = load("supply")
        v, c = sup["values"], sup["costs"]
        lo = c_["price"]
        ax = price_axes(10, (1, 3.5), x_length=6.6, y_length=4.6, qticks=list(range(0, 11, 2)),
                        pticks=[1, 1.5, 2, 2.5, 3, 3.5], qlabel=r"units", plabel=r"price", center=LEFT * 3.0 + DOWN * 0.4)
        a = ax.ax
        st = market_steps(a, Market(tuple(v), tuple(c)).steps())
        fl = Line(a.c2p(0, lo), a.c2p(10, lo), color=CAP, stroke_width=4)
        flab = label(rf"the legal minimum: \ {dollars(lo)}", font_size=22, color=CAP).next_to(a.c2p(0.15, lo), DOWN,
                                                                                             buff=0.12)
        flab.align_to(fl, LEFT).shift(RIGHT * 0.1)
        rows = VGroup(
            label(rf"{c_['buyers']} buyers will pay {dollars(lo)}", font_size=25, color=E.DEMAND),
            label(rf"{c_['offering']} sellers want to sell at it", font_size=25, color=E.SUPPLY),
            label(rf"the cheapest four selling: \ {pct(c_['best_share'], 0)}", font_size=24, color=E.GAIN),
            label(rf"by lottery: \ {pct(c_['lottery_share'], 0)}", font_size=24, color=GREY_B),
            label(rf"Agora's traders: \ {pct(c_['zip']['efficiency'], 0)}", font_size=24, color=E.AGORA),
            label(r"a minimum wage is a floor on a price: \ Part 38", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.45).shift(UP * 0.2)
        tag = agora_tag(r"computed: Agora; medians of 41 runs, sixth period", corner=DR, font_size=16)
        with self.voiceover(
            f"A floor is the mirror image. Set a minimum price of {money_words(lo)}. <bookmark mark='a'/> Only "
            f"{c_['buyers']} buyers will pay that much, but {c_['offering']} sellers would like to sell at it, so the "
            "sellers are rationed instead. <bookmark mark='b'/> If the four cheapest sold, the market would keep "
            f"{100 * c_['best_share']:.0f} percent of its gains. By lottery, {100 * c_['lottery_share']:.0f} percent; "
            f"and Agora's traders make {100 * c_['zip']['efficiency']:.0f}. <bookmark mark='c'/> The commonest floor "
            "on a price is a minimum wage, and there the evidence is subtler than this pit, because employers may "
            "have power over wages to begin with. That's Part thirty-eight."
        ) as vo:
            self.play(FadeIn(ax), Create(st.demand), Create(st.supply), FadeIn(tag), run_time=1.5)
            self.play(Create(fl), FadeIn(flab))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[2:5]], lag_ratio=0.5), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def ought(self):
        io = is_ought_card(
            r"a binding rent cap lowers rents for sitting tenants, keeps them in place, and shrinks the supply of "
            r"rental housing, which raises rents for newcomers",
            r"whether to cap rents, \ and how",
            r"how much the security of sitting tenants is worth, against higher rents for those still looking, and "
            r"who should bear the cost",
            width=11.8, font_size=25).move_to(UP * 0.1)
        with self.voiceover(
            "Notice what the evidence does and doesn't settle. <bookmark mark='a'/> It tells us what a rent cap "
            "does: sitting tenants pay less and stay put, and newcomers face fewer flats at higher rents. "
            "<bookmark mark='b'/> Whether to have one needs something more: a judgment about how much the security "
            "of the people already housed is worth, against the cost to the people still looking, and who should "
            "pay for it. <bookmark mark='c'/> Economics can measure both sides of that ledger. It can't, by itself, "
            "tell you how to weigh them."
        ) as vo:
            self.play(FadeIn(io.card), FadeIn(io.is_row))
            vo.wait_until("b")
            self.play(FadeIn(io.judgment), FadeIn(io[1][1]))
            vo.wait_until("c")
            self.play(FadeIn(io.ought), FadeIn(io[1][3]))
        self.clear_scene()
