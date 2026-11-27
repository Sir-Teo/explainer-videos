from __future__ import annotations

from videos.industry.industry13.common import *  # noqa: F403


class Retail(VoiceoverScene):
    def construct(self):
        card(self, 9, "The retailer's squeeze", "What happens to a company that sells at a fixed price and buys at a floating one?",
             "Chapter nine. The retailer's squeeze.", lit=("dollar", "change", "state"))
        self.model()
        self.entry()
        self.squeeze()
        self.bill()

    def model(self):
        mkt = VGroup(draw.gas_plant(1.0), draw.wind_turbine(1.2)).arrange(RIGHT, buff=0.3).move_to([-4.8, 0.4, 0])
        ml = VGroup(tx("the wholesale market", 17, GAS, bold=True), tx("price changes every half hour", 14, GREY_A)).arrange(
            DOWN, buff=0.04).next_to(mkt, DOWN, buff=0.2)
        sup = RoundedRectangle(corner_radius=0.15, width=2.4, height=1.3, stroke_color=UK, stroke_width=3, fill_color=UK,
                               fill_opacity=0.15).move_to([0, 0.4, 0])
        sl = VGroup(tx("the supplier", 18, UK, bold=True), tx("buys, bills, answers the phone", 13, GREY_A)).arrange(DOWN, buff=0.04).move_to(sup)
        homes = VGroup(*[draw.house(0.6) for _ in range(3)]).arrange(RIGHT, buff=0.2).move_to([4.8, 0.4, 0])
        hl = VGroup(tx("households", 17, WHITE, bold=True), tx("pay a tariff, capped by the regulator", 14, GREY_A)).arrange(
            DOWN, buff=0.04).next_to(homes, DOWN, buff=0.2)
        a1 = Arrow(mkt.get_right(), sup.get_left(), buff=0.2, stroke_width=3, color=GAS)
        a2 = Arrow(sup.get_right(), homes.get_left(), buff=0.2, stroke_width=3, color=UK)
        note = VGroup(tx("Britain: since 2019 a price cap on standard tariffs, operated by Ofgem", 16, GREY_A),
                      tx("the supplier's margin = the capped price − what it paid for the energy − its costs", 16, WHITE)).arrange(
            DOWN, buff=0.08).to_edge(DOWN, buff=0.8)
        src = source("National Audit Office, The energy supplier market (June 2022)", size=13)
        with self.voiceover(
            "In many places the business of making electricity is separate from the business of selling it. "
            "<bookmark mark='a'/> In Britain, suppliers buy power and gas on the wholesale market, where the price changes "
            "through the day, <bookmark mark='b'/> and sell it to households, who mostly pay a tariff. <bookmark mark='c'/> "
            "Since 2019, a price cap, operated by the regulator, Ofgem, has limited what the standard tariff can charge. A "
            "supplier's margin is the gap between that capped price and what it paid for the energy: a thin slice, "
            "squeezed from both sides."
        ) as vo:
            self.play(FadeIn(sup), FadeIn(sl), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(mkt), FadeIn(ml), GrowArrow(a1))
            vo.wait_until("b")
            self.play(FadeIn(homes), FadeIn(hl), GrowArrow(a2))
            vo.wait_until("c")
            self.play(FadeIn(note, shift=UP * 0.1))
        self.clear_scene()

    def entry(self):
        T = R["retail"]
        pts = [(2010, T["s2010"], "December 2010"), (2018, T["speak"], "mid-2018"), (2022, T["s2022"], "May 2022")]
        pa = viz.plot_axes([2009, 2023], [0, 80], x_length=7.4, y_length=4.2, xticks=[2010, 2014, 2018, 2022], yticks=[20, 40, 60, 80],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}", ylabel="domestic energy suppliers in Britain",
                           size=14).move_to([-2.4, -0.4, 0])
        bars = VGroup()
        for x, v, lab in pts:
            p0, p1 = pa.ax.c2p(x, 0), pa.ax.c2p(x, v)
            b = Rectangle(width=0.9, height=p1[1] - p0[1], stroke_width=0, fill_color=UK, fill_opacity=0.85).move_to([p0[0], (p0[1] + p1[1]) / 2, 0])
            bars.add(VGroup(b, tx(f"{v:.0f}", 20, UK, bold=True).next_to(b, UP, buff=0.08), tx(lab, 12, GREY_A).next_to(b, DOWN, buff=0.35)))
        notes = VGroup(tx(f"newcomers' share of the market,", 16, GREY_A), tx(f"September 2021: about {T['new_share']:.0f}%", 18, UK, bold=True),
                       tx("many, the auditors found, with", 15, GREY_A), tx("weak finances", 15, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([4.4, 0.6, 0])
        src = source("National Audit Office, The energy supplier market (June 2022)", size=13)
        with self.voiceover(
            "In the 2010s, new suppliers poured in. <bookmark mark='a'/> In December 2010 there "
            f"were {T['s2010']:.0f} suppliers of household energy. <bookmark mark='b'/> By the middle of 2018, "
            f"{T['speak']:.0f}. By September 2021 the newcomers had about {T['new_share']:.0f} per cent of the market. "
            "<bookmark mark='c'/> The National Audit Office later concluded that the regulator let many of them in with "
            "weak finances, and never imagined prices staying high for long. <bookmark mark='d'/> By May 2022 there were "
            f"{T['s2022']:.0f}."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]))
            vo.wait_until("a")
            self.play(Indicate(bars[0], color=UK))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]), FadeIn(notes[:2]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2:]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][1:]))
        self.clear_scene()

    def squeeze(self):
        T = R["retail"]
        ms = T["months"]
        xs = [int(m[:4]) + (int(m[5:7]) - 0.5) / 12 for m in ms]
        pa = viz.plot_axes([xs[0], xs[-1]], [-500, 520], x_length=9.0, y_length=4.6, xticks=[2021, 2022], yticks=[-400, -200, 0, 200, 400],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}", ylabel="$ a MWh", size=14).move_to([-1.6, -0.4, 0])
        zero = Line(pa.ax.c2p(xs[0], 0), pa.ax.c2p(xs[-1], 0), stroke_color=GREY_B, stroke_width=1.2)
        lw = poly(pa, list(zip(xs, T["wholesale"])), GAS, 3.5)
        fx = DashedLine(pa.ax.c2p(xs[0], T["fixed"]), pa.ax.c2p(xs[-1], T["fixed"]), stroke_color=UK, stroke_width=3, dash_length=0.1)
        mu = poly(pa, list(zip(xs, T["unhedged"])), BAD, 3.5)
        mh = poly(pa, list(zip(xs, T["hedged"])), GOOD, 3.5)
        key = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=c, stroke_width=4), tx(t_, 14, c)).arrange(RIGHT, buff=0.1)
                       for c, t_ in ((GAS, "wholesale power (from European gas)"), (UK, "the supplier's fixed selling price"),
                                     (BAD, "margin, buying everything at the day's price"), (GOOD, "margin, 90% bought ahead"))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.6, 2.2, 0])
        note = VGroup(tx("the real thing: the wholesale gas price", 15, GREY_A),
                      tx(f"rose nearly {T['gas_x']:.0f}-fold, February to December 2021", 15, GAS, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.05).move_to([-3.4, 2.85, 0])
        tag = estimate_tag("the Works (power.py): an illustrative supplier; wholesale from the IMF's European gas price", corner=DR, size=11)
        with self.voiceover(
            "Then came 2021. Play it with the Works: a supplier that set its selling price in the summer of 2020. "
            "<bookmark mark='a'/> Here is what wholesale power cost, following the price of gas in Europe. "
            "<bookmark mark='b'/> And here is the supplier's fixed price. <bookmark mark='c'/> A supplier that bought its "
            "energy day by day saw its margin turn negative by the autumn of 2021, and then fall off a cliff: it was "
            "losing hundreds of dollars on every megawatt-hour it sold, and with its price capped, it could not simply "
            "charge more. <bookmark mark='d'/> One that had bought most of its energy ahead, at the old prices, rode it out."
        ) as vo:
            self.play(FadeIn(pa), Create(zero), FadeIn(tag), FadeIn(note))
            vo.wait_until("a")
            self.play(Create(lw), FadeIn(key[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(fx), FadeIn(key[1]))
            vo.wait_until("c")
            self.play(Create(mu), FadeIn(key[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(Create(mh), FadeIn(key[3]), run_time=2.0)
        self.clear_scene()

    def bill(self):
        T = R["retail"]
        tomb = VGroup(*[RoundedRectangle(corner_radius=0.12, width=0.42, height=0.55, stroke_width=0, fill_color=GREY_D, fill_opacity=0.9)
                        for _ in range(int(T["failed"]))]).arrange_in_grid(rows=3, buff=0.12).move_to([-3.6, 1.3, 0])
        tl = tx(f"{T['failed']:.0f} suppliers failed, July 2021 to May 2022", 18, WHITE, bold=True).next_to(tomb, DOWN, buff=0.2)
        tl2 = tx("nearly four million households affected", 15, GREY_A).next_to(tl, DOWN, buff=0.08)
        facts = VGroup(tx("Bulb Energy:", 18, UK, bold=True), tx(f"{T['bulb']:.1f} million customers, in special", 16, GREY_A),
                       tx("administration from November 2021", 16, GREY_A),
                       tx(f"the cost of moving customers: about £{T['cost']:.1f}bn,", 17, BAD, bold=True),
                       tx(f"about £{T['per']:.0f} on every customer's bill", 17, BAD, bold=True),
                       tx(f"the capped bill: £{T['cap18']:,.0f} (winter 2018-19)", 16, GREY_A),
                       tx(f"to £{T['cap22']:,.0f} (summer 2022), +{100 * (T['cap22'] / T['cap18'] - 1):.0f}%", 16, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.07).move_to([3.6, 0.4, 0])
        lesson = tx("A retailer with no plants and no hedges is a bet that wholesale prices stay calm.", 17, GOLD, bold=True).to_edge(DOWN, buff=0.6)
        src = source("National Audit Office, The energy supplier market (June 2022)", size=13)
        with self.voiceover(
            f"And that is what happened. <bookmark mark='a'/> Between July 2021 and May 2022, {T['failed']:.0f} British "
            "energy suppliers failed, affecting nearly four million households. Their customers were moved to other "
            "suppliers, without their lights going out. <bookmark mark='b'/> The largest, Bulb, with about "
            f"{T['bulb']:.1f} million customers, was put into special administration in November 2021 and run at the "
            "government's expense. "
            f"<bookmark mark='c'/> The regulator's best estimate of the cost of moving everyone: about £{T['cost']:.1f} "
            f"billion, roughly £{T['per']:.0f} on every customer's bill, the failed suppliers' and everyone else's. "
            "<bookmark mark='d'/> A retailer with no power plants and no hedges is a bet that wholesale prices stay calm. "
            "In 2021 that bet was lost, and the customers paid."
        ) as vo:
            tomb.set_opacity(0.5)
            self.play(FadeIn(src), FadeIn(tomb), FadeIn(tl))
            vo.wait_until("a")
            self.play(LaggedStart(*[t_.animate.set_opacity(0.9) for t_ in tomb], lag_ratio=0.04), FadeIn(tl2), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(facts[:3]))
            vo.wait_until("c")
            self.play(FadeIn(facts[3:]))
            vo.wait_until("d")
            self.play(FadeIn(lesson, shift=UP * 0.1))
        self.clear_scene()
