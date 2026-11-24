from __future__ import annotations

from videos.industry.industry9.common import *  # noqa: F403


class Pricing(VoiceoverScene):
    def construct(self):
        card(self, 8, "How metals are priced", "Who sets the price of a tonne of copper, and where?",
             "Chapter eight. How metals are priced.", lit=("dollar", "change"))
        self.chain()
        self.record()
        self.tariff()

    def chain(self):
        mine_ = VGroup(draw.open_pit(1.8, 0.7, benches=3), tx("the mine", 18, WHITE, bold=True)).arrange(DOWN, buff=0.15)
        smelt = VGroup(Rectangle(width=1.3, height=1.0, stroke_color=STONE, stroke_width=2, fill_color="#3E4553",
                                 fill_opacity=1), tx("the smelter and refinery", 18, WHITE, bold=True)).arrange(
            DOWN, buff=0.15)
        buyer = VGroup(VGroup(*[draw.cathode(0.5) for _ in range(3)]).arrange(RIGHT, buff=-0.2),
                       tx("the wire maker", 18, WHITE, bold=True)).arrange(DOWN, buff=0.15)
        row = VGroup(mine_, smelt, buyer).arrange(RIGHT, buff=2.4).move_to([0, 1.2, 0])
        a1 = Arrow(mine_.get_right() + UP * 0.2, smelt.get_left() + UP * 0.2, buff=0.15, stroke_width=3, color=COPPER,
                   tip_length=0.16)
        a2 = Arrow(smelt.get_right() + UP * 0.2, buyer.get_left() + UP * 0.2, buff=0.15, stroke_width=3, color=COPPER,
                   tip_length=0.16)
        l1 = tx("concentrate", 15, COPPER).next_to(a1, UP, buff=0.06)
        l2 = tx("cathode", 15, COPPER).next_to(a2, UP, buff=0.06)
        lme = VGroup(RoundedRectangle(corner_radius=0.12, width=5.0, height=1.0, stroke_color=PRICE, stroke_width=2,
                                      fill_color="#141A24", fill_opacity=1),
                     VGroup(tx("the exchange price", 22, PRICE, bold=True),
                            tx("London (LME), New York (COMEX), Shanghai", 15, GREY_A)).arrange(DOWN, buff=0.05)
                     ).move_to([0, -1.2, 0])
        lme[1].move_to(lme[0])
        d1 = DashedLine(lme.get_corner(UL) + RIGHT * 0.5, a1.get_center() + DOWN * 0.25, stroke_width=2, color=PRICE)
        d2 = DashedLine(lme.get_corner(UR) + LEFT * 0.5, a2.get_center() + DOWN * 0.25, stroke_width=2, color=PRICE)
        f1 = VGroup(tx("the miner is paid:", 15, GREY_A), tx("exchange price x copper content", 16, WHITE),
                    tx("minus the smelter's charges", 16, STATE)).arrange(DOWN, buff=0.04).move_to([-4.3, -2.6, 0])
        f2 = VGroup(tx("the buyer pays:", 15, GREY_A), tx("exchange price", 16, WHITE),
                    tx("plus a premium for delivery", 16, GREEN_C)).arrange(DOWN, buff=0.04).move_to([4.3, -2.6, 0])
        src = source("how copper is sold: the standard terms, simplified", size=13)
        with self.voiceover(
            "Who decides what copper costs? Not the miner, and not the buyer. <bookmark mark='a'/> Follow the metal. "
            "The mine sells concentrate to a smelter, and the smelter and refinery sell cathode to the companies that "
            "make wire, tube and sheet. <bookmark mark='b'/> At both steps, the price comes from an exchange: the London "
            "Metal Exchange above all, and COMEX in New York and the Shanghai Futures Exchange, where traders buy and "
            "sell copper for delivery now and in the months ahead. <bookmark mark='c'/> The miner is paid the exchange "
            "price for the copper in its concentrate, minus charges for smelting and refining it. "
            "<bookmark mark='d'/> The buyer of cathode pays the exchange price plus a premium for delivery where it "
            "wants it. So every mine on Earth takes the same price, set every day by traders who will never see the ore. "
            "A miner cannot charge more because its copper is better: a tonne of cathode is a tonne of cathode. All it "
            "can choose is its cost."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(mine_), run_time=0.8)
            self.play(GrowArrow(a1), FadeIn(l1), FadeIn(smelt))
            self.play(GrowArrow(a2), FadeIn(l2), FadeIn(buyer))
            vo.wait_until("b")
            self.play(FadeIn(lme, shift=UP * 0.1))
            self.play(Create(d1), Create(d2))
            vo.wait_until("c")
            self.play(FadeIn(f1, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(f2, shift=UP * 0.1))
        self.clear_scene()

    def record(self):
        P = R["prices"]
        ms = P["months"]
        nom = P["nominal"]["PCOPPUSDM"]
        real = P["real"]["PCOPPUSDM"]
        xs = [mx(m) for m in ms]
        pa = viz.plot_axes([1992, 2027], [0, 16000], x_length=10.8, y_length=4.6,
                           xticks=[1995, 2000, 2005, 2010, 2015, 2020, 2025], yticks=[4000, 8000, 12000, 16000],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:,.0f}", size=15).move_to([0.2, -0.5, 0])
        ln_n = VMobject(stroke_color=COPPER, stroke_width=3).set_points_as_corners(
            [pa.ax.c2p(x, v) for x, v in zip(xs, nom) if v is not None])
        ln_r = VMobject(stroke_color=WHITE, stroke_width=2.5).set_points_as_corners(
            [pa.ax.c2p(x, v) for x, v in zip(xs, real) if v is not None])
        ln_r.set_stroke(opacity=0.85)
        k11 = int(np.nanargmax([v if v else np.nan for v in real]))
        rec = Dot(pa.ax.c2p(xs[-1], nom[-1]), color=COPPER, radius=0.08)
        rec_l = VGroup(tx(f"{mlabel(ms[-1])}: ${nom[-1]:,.0f} a tonne", 17, COPPER, bold=True),
                       tx("a record, in dollars of the day", 14, GREY_A)).arrange(DOWN, buff=0.03, aligned_edge=RIGHT
                                                                                 ).next_to(rec, LEFT, buff=0.15).shift(
            UP * 0.35)
        pk = Dot(pa.ax.c2p(xs[k11], real[k11]), color=WHITE, radius=0.08)
        pk_l = VGroup(tx(f"{mlabel(ms[k11])}: ${real[k11]:,.0f}", 17, WHITE, bold=True),
                      tx(f"in dollars of {mlabel(P['cpi_month'])}", 14, GREY_A)).arrange(DOWN, buff=0.03,
                                                                                         aligned_edge=RIGHT).next_to(
            pk, LEFT, buff=0.15)
        key = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=COPPER, stroke_width=3), tx("dollars of the day", 15,
                                                                                               COPPER)).arrange(RIGHT, buff=0.1),
                     VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=WHITE, stroke_width=3),
                            tx(f"dollars of {mlabel(P['cpi_month'])}", 15, WHITE)).arrange(RIGHT, buff=0.1)
                     ).arrange(RIGHT, buff=0.5).next_to(pa, UP, buff=0.1).align_to(pa, LEFT).shift(RIGHT * 1.0)
        head = tx("Copper, dollars a tonne, month by month", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("IMF primary commodity prices via FRED (PCOPPUSDM), deflated by the US CPI (BLS)", size=13)
        with self.voiceover(
            "And the price moves a great deal. <bookmark mark='a'/> Here is copper since 1992, in the dollars of each "
            "month. It sat near two thousand dollars a tonne for a decade, rose fourfold in the China boom of the 2000s, "
            "crashed in 2008, and has climbed in waves since. <bookmark mark='b'/> In September 2026 it averaged "
            f"{nom[-1]:,.0f} dollars a tonne, about {say_money(P['copper_last_lb'])} a pound: the highest monthly "
            "average in this record. <bookmark mark='c'/> But a dollar of 1992 is not a dollar of today. Adjust for "
            f"inflation, and the peak was {mlabel(ms[k11])}, at about {real[k11]:,.0f} of today's dollars. Copper is "
            "dear today, but not, after inflation, at its dearest. Always ask which dollars a record is counted in."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(src), FadeIn(key[0]))
            vo.wait_until("a")
            self.play(Create(ln_n), run_time=5.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(rec, scale=2), FadeIn(rec_l))
            vo.wait_until("c")
            self.play(FadeIn(key[1]), TransformFromCopy(ln_n, ln_r), run_time=2.5)
            self.play(FadeIn(pk, scale=2), FadeIn(pk_l))
        self.clear_scene()

    def tariff(self):
        cx24, cx25, lme = get("usgs.cu.comex.2024"), get("usgs.cu.comex"), get("lme.copper.2025")
        imp24, imp25 = 903, get("usgs.cu.imports")
        wm = draw.world_map(6.4, lon=(-125, -35), lat=(-45, 50)).move_to([-3.3, -0.35, 0])
        us = wm.p(-98, 38)
        lanes = [VMobject().set_points_smoothly([wm.p(-73, -27), wm.p(-79, -10), wm.p(-80, 2), wm.p(-79.6, 9),
                                                 wm.p(-82, 17), wm.p(-89, 25), wm.p(-94.5, 29)]),
                 VMobject().set_points_smoothly([wm.p(-78, -12), wm.p(-82, -3), wm.p(-79.8, 7.5), wm.p(-81, 15),
                                                 wm.p(-87, 23), wm.p(-93.5, 28.6)])]
        for l_ in lanes:
            l_.set_stroke(GREY_B, 1.5, opacity=0.5)
        ships = VGroup(*[draw.ship(0.45, boxes=0) for _ in range(6)])
        bars = VGroup()
        vals = [("COMEX 2024", cx24, GREY_B), ("LME 2025", lme, WHITE), ("COMEX 2025", cx25, COPPER)]
        for k, (n, v, c) in enumerate(vals):
            b = Rectangle(width=0.7, height=v / 5 * 2.4, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to(
                [2.7 + 1.05 * k, -2.7, 0], aligned_edge=DOWN)
            bars.add(VGroup(b, tx(f"${v:.2f}", 15, WHITE, bold=True).next_to(b, UP, buff=0.06),
                            tx(n, 13, GREY_A).next_to(b, DOWN, buff=0.08)))
        imp = VGroup(tx("US imports of refined copper", 16, GREY_A),
                     VGroup(tx(f"{imp24:,} kt", 22, GREY_B, bold=True), tx("2024", 13, GREY_B)).arrange(DOWN, buff=0.02),
                     VGroup(tx(f"{imp25:,.0f} kt", 22, COPPER, bold=True), tx("2025", 13, COPPER)).arrange(DOWN,
                                                                                                         buff=0.02))
        imp[1:].arrange(RIGHT, buff=0.6)
        imp.arrange(DOWN, buff=0.1).move_to([3.75, 2.2, 0])
        gap = Brace(VGroup(bars[1][0], bars[2][0]), UP, buff=0.4, color=COPPER)
        gap_l = tx(f"+{100 * (cx25 - lme):.0f} cents", 16, COPPER, bold=True).next_to(gap, UP, buff=0.06)
        head = tx("2025: one metal, two prices", 22, WHITE, bold=True).to_edge(UP, buff=0.35).shift(LEFT * 2.6)
        src = source("US Geological Survey, Mineral Commodity Summaries 2026, 'copper' (COMEX, imports); Freeport-McMoRan "
                     "10-K for 2025 (LME); routes illustrative", size=13)
        with self.voiceover(
            "Normally the exchanges in London, New York and Shanghai quote almost the same price, because if they "
            "drift apart, traders buy in the cheap place and ship to the dear one. In 2025 that broke. "
            "<bookmark mark='a'/> The United States announced it would look into tariffs on imported copper, and "
            f"nobody knew how high they would be, or when. COMEX copper, in New York, averaged {say_money(cx25)} a "
            f"pound, a record, against {say_money(lme)} on the London exchange. <bookmark mark='b'/> A gap of about thirty "
            "cents a pound is a fortune on a shipload, so traders raced to get copper into America before any tariff "
            f"began. <bookmark mark='c'/> American imports of refined copper nearly doubled, from {imp24} thousand "
            f"tonnes to about {imp25:,.0f} thousand, far more than the country used. The price of a metal is set by "
            "traders, but it can still be bent by a single government."
        ) as vo:
            self.play(FadeIn(wm), FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1:])) for b in bars],
                                  lag_ratio=0.3), run_time=2.0)
            self.play(GrowFromCenter(gap), FadeIn(gap_l))
            vo.wait_until("b")
            self.play(Create(lanes[0]), Create(lanes[1]))
            self.play(LaggedStart(*[MoveAlongPath(sh, lanes[k % 2], rate_func=linear) for k, sh in enumerate(ships)],
                                  lag_ratio=0.3), run_time=6.0)
            vo.wait_until("c")
            self.play(FadeIn(imp[0]), FadeIn(imp[1]))
            self.play(TransformFromCopy(imp[1], imp[2]))
            self.play(Flash(us, color=COPPER, line_length=0.3))
        self.clear_scene()
