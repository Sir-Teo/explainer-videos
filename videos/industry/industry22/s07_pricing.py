from __future__ import annotations

from videos.industry.industry22.common import *  # noqa: F403


class Pricing(VoiceoverScene):
    def construct(self):
        card(self, 6, "Pricing power, tested", "What happens when a brand raises its price nine per cent?",
             "Chapter six. Pricing power, tested. Between 2021 and 2023 prices rose across the economy. The brands raised "
             "theirs too. Did shoppers leave? If a premium is real, the shopper pays more and stays; if not, "
             "the store label wins.", lit=("change", "moat"))
        self.drivers()
        self.cpi()
        self.cocoa()

    def drivers(self):
        Pr = R["pricing"]
        pa = viz.plot_axes([2019.4, 2026.6], [-6, 10], x_length=10.0, y_length=4.4, xticks=list(range(2020, 2027)),
                           yticks=[-5, 0, 5, 10], xfmt=lambda v: f"FY{int(v) % 100:02d}", yfmt=lambda v: f"{int(v):+d}%",
                           ylabel="P&G's sales growth from volume and from price, by fiscal year", size=13).move_to([-0.3, -0.4, 0])
        ax = pa.ax
        zero = DashedLine(ax.c2p(2019.4, 0), ax.c2p(2026.6, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        groups = {}
        for y, d in Pr.items():
            g = VGroup()
            for k, dx, col in (("vol", -0.17, VOL), ("price", 0.17, PRICE)):
                v = d[k]
                h = abs(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]) or 0.02
                b = Rectangle(width=0.3, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9)
                b.move_to([ax.c2p(y + dx, 0)[0], ax.c2p(0, v / 2)[1], 0])
                b.grow = DOWN if v >= 0 else UP
                g.add(b, tx(f"{v:+d}", 13, col, bold=True).next_to(b, UP if v >= 0 else DOWN, buff=0.05))
            groups[y] = g
        key = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=VOL, fill_opacity=0.9), tx("volume", 14, VOL)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.2, stroke_width=0, fill_color=PRICE, fill_opacity=0.9), tx("price", 14, PRICE)).arrange(RIGHT, buff=0.1)
                     ).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.95)
        src = source("The Procter & Gamble Company, Forms 10-K for fiscal 2020 to 2026: net sales change drivers, total company",
                     size=12)
        beat(self,
             "P&G splits each year's sales growth into what it sold more of and what it charged more for. "
             "<bookmark mark='a'/> In fiscal 2020 to 2022, volume did most of the work: "
             f"{Pr[2020]['vol']:+d}, {Pr[2021]['vol']:+d} and {Pr[2022]['vol']:+d} per cent, with prices up "
             f"{Pr[2022]['price']} per cent by 2022. <bookmark mark='b'/> Then, in the year to June 2023, P&G raised its "
             f"prices {Pr[2023]['price']} per cent, and its volume fell only {abs(Pr[2023]['vol'])} per cent. "
             f"<bookmark mark='c'/> Prices rose another {Pr[2024]['price']} per cent the next year, and since then barely "
             "at all, while volume has stayed flat. Nine points of price for three of volume: most shoppers paid the new "
             "price and stayed.",
             base=[pa, zero, key, src], steps=[VGroup(groups[2020], groups[2021], groups[2022]), groups[2023],
                                               VGroup(groups[2024], groups[2025], groups[2026])])

    def cocoa(self):
        E = R["extra"]
        items = [("2024", E["hsy_gm"][0] / 100, FOOD, f"{E['hsy_gm'][0]}%"), ("2025", E["hsy_gm"][1] / 100, BAD, f"{E['hsy_gm'][1]}%")]
        bars_ = vbars(items, base_y=-2.2, height=3.4, width=1.5, gap=1.0, x0=-4.4, max_value=0.5)
        lab = tx("Hershey's gross margin", 16, GREY_A).next_to(bars_, UP, buff=0.5)
        q = quote(["'We may be able to pass some or all raw material, energy, and other input",
                   "cost increases to customers by increasing the selling prices of our products",
                   "or decreasing the size of our products; however, higher product prices or",
                   "decreased product sizes ... may ... result in a reduction in sales volume'"], "The Hershey Company, Form 10-K 2025",
                  size=14, width=7.2).move_to([2.6, 1.0, 0])
        c = tx(f"2025: prices up about {E['hsy_price']}%; General Mills' North America Retail volume {E['gis_vol']}%", 16, PRICE, bold=True).move_to([2.6, -1.4, 0])
        src = source("The Hershey Company, Form 10-K 2025; General Mills, Inc., Form 10-K for fiscal 2026", size=12)
        beat(self,
             "But a brand cannot always pass on everything at once. <bookmark mark='a'/> Hershey's chocolate needs cocoa, "
             f"and in 2025 higher commodity and tariff costs cut its gross margin from {E['hsy_gm'][0]} per cent to "
             f"{E['hsy_gm'][1]}, even though it raised its prices about {E['hsy_price']} per cent. <bookmark mark='b'/> Its "
             "report names the two tools a maker has, raising the price or shrinking the pack, and the cost of both: "
             "fewer sales. <bookmark mark='c'/> General Mills missed its own goal of growing volume again in North American "
             "groceries: it fell one per cent.",
             base=[lab, src], steps=[bars_, q, c])

    def cpi(self):
        Hs = R["history"]["infl"]
        items = [("food at home", Hs["food at home"], FOOD, f"+{100 * Hs['food at home']:.1f}%"),
                 ("all consumer prices", Hs["all"], WHITE, f"+{100 * Hs['all']:.1f}%"),
                 ("personal care", Hs["personal care"], BRAND, f"+{100 * Hs['personal care']:.1f}%")]
        rows = hbars(items, max_value=0.25, x0=-0.4, top=1.2, row=1.0, length=6.2, size=18, bar_h=0.5)
        bask = VGroup(draw.cereal_box(0.9), draw.soap(0.7), draw.detergent(0.8)).arrange(RIGHT, buff=0.3).move_to([-5.0, 2.3, 0])
        lab = tx("rise in US consumer prices, 2020 to 2023 (annual averages)", 16, GREY_A).to_edge(UP, buff=0.9)
        src = source("BLS, CPI-U: food at home, personal care, all items (not seasonally adjusted), annual averages, via FRED", size=12)
        beat(self,
             "Shoppers saw it on the shelf. <bookmark mark='a'/> From 2020 to 2023 the prices of food bought in shops rose "
             f"{100 * Hs['food at home']:.0f} per cent, <bookmark mark='b'/> all consumer prices {100 * Hs['all']:.0f} per "
             f"cent, <bookmark mark='c'/> and personal care products {100 * Hs['personal care']:.0f} per cent. The big makers "
             "raised their prices along with everyone else, and most kept their shoppers: the test a brand's premium has to "
             "pass. A brand that could not raise its price when its costs rose would have had to give up its margin, or its "
             "advertising, and with it the next year's premium.",
             base=[rows.axis, bask, lab, src], steps=[rows[0], rows[1], rows[2]])
