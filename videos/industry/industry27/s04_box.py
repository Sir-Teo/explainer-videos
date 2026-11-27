from __future__ import annotations

from videos.industry.industry27.common import *  # noqa: F403


class Box(VoiceoverScene):
    def construct(self):
        card(self, 3, "The box", "What did a steel box change?",
             "Chapter three. The box. Almost everything you own that was made abroad crossed the sea in one of the same few "
             "sizes of steel box, lifted by a crane and never opened between the factory and the warehouse.", lit=("unit", "make"))
        self.crane()
        self.world()
        self.countries()
        self.volume()
        self.fleet()

    def crane(self):
        c = draw.quay_crane(3.4).move_to([-3.2, 0.4, 0])
        vessel = draw.ship(4.0).move_to([1.0, -1.9, 0])
        boxes = VGroup(*[draw.container(0.9, color=col, feet=20) for col in (BOX, SEA, GOOD, RATE)]).arrange(RIGHT, buff=0.05).move_to([3.8, 1.9, 0])
        g = VGroup(tx("one size of box", 19, BOX, bold=True), tx("one kind of crane", 19, PORT, bold=True),
                   tx("ships, trains and lorries that all take it", 19, SEA, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.8, 0.0, 0])
        tag = estimate_tag("this series' summary", size=12)
        beat(self,
             "The container's trick is that it is always the same. <bookmark mark='a'/> Twenty or forty feet long, with the "
             "same corner fittings on every one, <bookmark mark='b'/> so one kind of crane can lift any "
             "box, <bookmark mark='c'/> and the same box rides a ship, a train and a lorry without anyone touching what is "
             "inside. The unit of the industry is the TEU, the twenty-foot equivalent unit: one small box.",
             base=[tag], steps=[[boxes, g[0]], [c, g[1]], [vessel, g[2]]])

    def world(self):
        W = R["box"]["world"]
        ch = line_chart({"containers handled by the world's ports": (W, BOX)}, x=(2010, 2024), y=(0, 1000),
                        xticks=[2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024], yticks=[0, 250, 500, 750, 1000],
                        yfmt=lambda v: f"{v:.0f}m", ylabel="container port traffic, million TEU a year (each box counted at every port)",
                        width=9.4, height=4.4, center=(-0.6, -0.45), label_end=False)
        m1 = marker(ch.ax, 2010, W[2010], f"2010: {W[2010]:.0f}m", ALL, side=UP)
        m2 = marker(ch.ax, 2020, W[2020], f"2020: {W[2020]:.0f}m", BAD, side=DOWN)
        m3 = marker(ch.ax, 2024, W[2024], f"2024: {W[2024]:.0f}m", BOX, side=LEFT)
        src = source("World Bank, World Development Indicators: container port traffic (IS.SHP.GOOD.TU)", size=12)
        beat(self,
             "How many boxes? <bookmark mark='a'/> In 2010 the world's ports handled "
             f"{W[2010]:.0f} million TEU, counting each box every time it was lifted on or off a ship. "
             f"<bookmark mark='b'/> The total dipped only once, in 2020, <bookmark mark='c'/> and reached {W[2024]:.0f} "
             "million in 2024.",
             base=[ch.frame, src], steps=[[ch.lines["containers handled by the world's ports"], m1], m2, m3])

    def countries(self):
        P = R["ports"]
        top = P["top"][:10]
        names = {"Korea, Rep.": "South Korea", "Viet Nam": "Vietnam", "United Arab Emirates": "UAE"}
        items = [(names.get(c, c), v, BAD if c == "China" else (SEA if c == "United States" else BOX), f"{v:.0f}m") for c, v in top]
        rows = hbars(items, max_value=310, x0=-0.4, top=2.4, row=0.5, length=6.6, size=15, bar_h=0.32)
        lab = tx(f"container port traffic, million TEU, {P['year']}", 16, GREY_A).to_edge(UP, buff=0.4)
        src = source("World Bank, World Development Indicators: container port traffic", size=12)
        c = dict(top)
        beat(self,
             f"And where. <bookmark mark='a'/> China's ports handled {c['China']:.0f} million TEU in {P['year']}, five times "
             f"America's {c['United States']:.0f} million. <bookmark mark='b'/> Then Singapore, {c['Singapore']:.0f} million, "
             "more than any country but those two, then South Korea, Malaysia, Vietnam and India: a map of where the "
             "world's goods are made and where its ships meet.",
             base=[lab, src], steps=[VGroup(*rows[:2]), VGroup(*rows[2:])])

    def volume(self):
        B = R["box"]
        a, b = B["zim_teu"]
        items = [("2019", a / 1e3, ALL, f"{a / 1e3:.2f}m TEU"), ("2025", b / 1e3, BOX, f"{b / 1e3:.2f}m TEU")]
        rows = hbars(items, max_value=4, x0=-0.4, top=1.0, row=1.2, length=6.4, size=18, bar_h=0.6)
        lab = tx("ZIM: containers carried a year", 17, GREY_A).to_edge(UP, buff=0.8)
        vessel = draw.ship(2.4).move_to([0, -2.1, 0])
        src = source("ZIM Integrated Shipping Services, Forms 20-F for 2020 and 2025", size=12)
        beat(self,
             f"One line's share of it: <bookmark mark='a'/> ZIM carried {a / 1e3:.2f} million TEU in 2019 <bookmark mark='b'/> "
             f"and {b / 1e3:.2f} million in 2025, {100 * (b / a - 1):.0f} per cent more, with {int(R['liner']['ships'])} ships, "
             "most of them rented. Volume grows steadily; it is the price of carrying it that leaps.",
             base=[lab, vessel, src], steps=[rows[0], rows[1]])

    def fleet(self):
        B = R["box"]
        c = stat_cards([(f"{B['fleet21']:.0f}m TEU", "the world's container fleet, end of 2021", ALL),
                        (f"{B['fleet']:.1f}m TEU", "end of 2025, about 6,700 ships", BOX),
                        (f"{B['order']:.1f}m TEU", "still on order at the end of 2025", BAD)], y=0.6, size=36, span=12)
        vessel = draw.ship(3.0, boxes=18).move_to([0, -1.8, 0])
        src = source("Alphaliner, as quoted in ZIM's Forms 20-F for 2021 and 2025", size=12)
        beat(self,
             "And the ships that carry them. <bookmark mark='a'/> At the end of 2021 the world's container ships could carry "
             f"about {B['fleet21']:.0f} million TEU between them. <bookmark mark='b'/> By the end of 2025, "
             f"{B['fleet']:.1f} million, in about {B['ships']:,.0f} ships: a third more in four years. "
             f"<bookmark mark='c'/> And another {B['order']:.1f} million TEU was on order, a third of the fleet again. "
             "Chapter four is why.",
             base=[vessel, src], steps=[c[0], c[1], c[2]])
