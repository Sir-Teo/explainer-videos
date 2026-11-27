from __future__ import annotations

from videos.industry.industry14.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 13, "Called it?", "Did America run out of places to put its rubbish?", "Chapter thirteen. Called it?", lit=("change",))
        self.theirs()
        self.ours()

    def theirs(self):
        C = R["called"]
        tons = R["landfill"]["tons"]
        ys = sorted(tons)
        pa = viz.plot_axes([1960, 2025], [0, 180], x_length=7.6, y_length=4.2, xticks=[1960, 1970, 1980, 1989, 2000, 2010, 2018],
                           yticks=[50, 100, 150], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}m",
                           ylabel="tons landfilled a year, US municipal waste", size=13).move_to([-2.4, -0.6, 0])
        upto = poly(pa, [(y, tons[y]) for y in ys if y <= 1989], WASTE, 4)
        after = poly(pa, [(y, tons[y]) for y in ys if y >= 1989], WHITE, 4)
        mark = DashedLine(pa.ax.c2p(1989, 0), pa.ax.c2p(1989, 175), stroke_color=PRICE, stroke_width=2, dash_length=0.08)
        quote = VGroup(tx("'One-third of the nation's landfills", 17, WHITE), tx("will be full by 1991'", 17, WHITE),
                       tx("US EPA, The Solid Waste Dilemma, February 1989", 13, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([4.2, 2.1, 0])
        n88, n09 = C["count"]
        facts = VGroup(tx(f"landfills: {n88:,.0f} (1988), {n09:,.0f} (2009)", 15, WHITE, bold=True),
                       tx(f"tons landfilled: {C['tons88']:.0f}m (1988), {C['tons18']:.0f}m (2018)", 15, WHITE, bold=True),
                       tx("EPA, 2009: 'at the national level,", 15, GREY_A), tx("capacity does not appear to be a problem'", 15, GREY_A),
                       tx(f"2025: Waste Management, {C['life']:.0f} years left;", 15, GREY_A),
                       tx(f"Republic, about {C['rsg_years']:.0f}", 15, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.07).move_to([4.1, -0.4, 0])
        verdict = tx("Called it? Half. The small dumps closed; the space did not run out.", 19, PRICE, bold=True).to_edge(DOWN, buff=0.75)
        src = source("US EPA, The Solid Waste Dilemma (1989); MSW in the US: 2009 Facts and Figures; Facts and Figures 1960-2018; "
                     "Forms 10-K 2025", size=13)
        with self.voiceover(
            "The forecast to test is the government's own, from the years of America's 'landfill crisis'. <bookmark mark='a'/> In February "
            "1989 the EPA warned that 'one-third of the nation's landfills will be full by 1991', and that the country was "
            "'running out of space to bury' its rubbish. <bookmark mark='b'/> What happened? The landfills did close: "
            f"from {n88:,.0f} in 1988 to {n09:,.0f} in 2009. <bookmark mark='c'/> But the rubbish kept going into the "
            f"ground, about {C['tons88']:.0f} million tons a year then, about {C['tons18']:.0f} million in 2018, into "
            "fewer, bigger, lined landfills. By 2009 the EPA itself wrote that 'at the national level, capacity does not "
            "appear to be a problem'. Today Waste Management reports about "
            f"{C['life']:.0f} years of permitted room and Republic about {C['rsg_years']:.0f}. <bookmark mark='d'/> Called "
            "it? Half. The prediction about landfills came true; the prediction about space did not, because a scarce "
            "permit is a price signal, and the industry answered it by building bigger holes."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(upto), run_time=2.0)
            self.play(Create(mark), FadeIn(quote))
            vo.wait_until("b")
            self.play(FadeIn(facts[0]))
            vo.wait_until("c")
            self.play(Create(after), run_time=2.5)
            self.play(FadeIn(facts[1:], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(verdict, shift=UP * 0.1))
        self.clear_scene()

    def ours(self):
        C = R["called"]
        g = C["growth"]
        ys = list(range(2016, 2026))
        sc = 0.55
        bars = VGroup()
        for i, y in enumerate(ys):
            v = g[y]
            b = Rectangle(width=0.42, height=v * sc, stroke_width=0, fill_color=WATER if v >= 4 else "#5D6B82", fill_opacity=0.9).move_to(
                [-6.0 + 0.55 * i, -1.9, 0], aligned_edge=DOWN)
            bars.add(VGroup(b, tx(f"{v:.1f}", 12, WHITE).next_to(b, UP, buff=0.05), tx(f"'{str(y)[2:]}", 12, GREY_A).next_to(b, DOWN, buff=0.06)))
        ytd = Rectangle(width=0.42, height=C["ytd"] * sc, stroke_width=0, fill_color=PRICE, fill_opacity=0.9).move_to([-6.0 + 0.55 * 10, -1.9, 0], aligned_edge=DOWN)
        ytd_g = VGroup(ytd, tx(f"{C['ytd']:.1f}", 12, PRICE, bold=True).next_to(ytd, UP, buff=0.05), tx("'26*", 12, PRICE).next_to(ytd, DOWN, buff=0.06))
        four = DashedLine([-6.3, -1.9 + 4 * sc, 0], [-0.1, -1.9 + 4 * sc, 0], stroke_color=PRICE, stroke_width=2, dash_length=0.08)
        four_l = tx("4%", 14, PRICE, bold=True).next_to(four, RIGHT, buff=0.08)
        bl = VGroup(tx("US water and sewerage prices, % rise on the year before", 14, GREY_B),
                    tx("* January-September", 12, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([-3.3, 2.3, 0])
        card_ = VGroup(tx("Our call", 28, PRICE, bold=True),
                       tx("America's price index for water and sewerage", 17, WHITE),
                       tx("will average more than 4.0% higher in 2027 than in 2026.", 17, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 26, PRICE, bold=True),
                       tx("Checked against the BLS's figures in January 2028", 14, GREY_A)).arrange(DOWN, buff=0.12).move_to([3.4, 1.0, 0])
        why = VGroup(tx("For: above 4% every year since 2022; the pipes still to replace", 14, GOOD),
                     tx("Against: lower inflation, as in 2017-2021, when it rose 3.1-3.7%", 14, BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.05).move_to([3.4, -1.6, 0])
        src = source("BLS, CPI-U water and sewerage maintenance (CUUR0000SEHG01), annual averages and January-September 2026", size=13)
        with self.voiceover(
            "Now our own forecast, written down so you can check it. <bookmark mark='a'/> Here is how much America's "
            "price index for water and sewerage rose each year. From 2017 to 2021, when inflation was low, between three "
            f"and four per cent. Since 2022, more than four every year. <bookmark mark='b'/> And in the first nine months "
            f"of 2026, about {C['ytd']:.1f} per cent above the same months of 2025. <bookmark mark='c'/> We think 2027 "
            "will be another year above four per cent: the pipes still have to be replaced, and the bill is how they are "
            "paid for. Against us: if inflation falls back, the water price tends to follow. <bookmark mark='d'/> We give "
            f"it {100 * C['prob']:.0f} per cent, and we will check it against the Bureau of Labor Statistics' figures in "
            "January 2028, right or wrong."
        ) as vo:
            self.play(FadeIn(src), FadeIn(bl), FadeIn(card_[0]), Create(four), FadeIn(four_l))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_[0], DOWN), FadeIn(b_[1]), FadeIn(b_[2])) for b_ in bars], lag_ratio=0.12), run_time=2.5)
            vo.wait_until("b")
            self.play(GrowFromEdge(ytd, DOWN), FadeIn(ytd_g[1:]))
            vo.wait_until("c")
            self.play(FadeIn(card_[1:3]), FadeIn(why))
            vo.wait_until("d")
            self.play(FadeIn(card_[3:], scale=1.1))
        self.clear_scene()
