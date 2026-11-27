from __future__ import annotations

from videos.industry.industry24.common import *  # noqa: F403

CON, HWY = "#F2A65A", "#F2A7B5"


class Concession(VoiceoverScene):
    def construct(self):
        card(self, 7, "Building the road, or owning it", "Why does the same company earn 5% on one road and 50% on another?",
             "Chapter seven. Building the road, or owning it. Some contractors found a way out of the thin margins of "
             "building: they keep a share of what they build.", lit=("moat", "dollar"))
        self.split()
        self.road()
        self.price()
        self.risk()
        self.book()

    def split(self):
        K = R["concession"]
        (cr, co), (hr, ho) = K["con"], K["hwy"]
        items = [("building: Ferrovial's construction arm", co / cr, CON, f"{100 * co / cr:.1f}% of €{cr / 1e3:.2f}bn"),
                 ("owning: its toll roads", ho / hr, HWY, f"{100 * ho / hr:.0f}% of €{hr / 1e3:.2f}bn")]
        rows = hbars(items, max_value=0.6, x0=0.4, top=1.0, row=1.1, length=5.4, size=17, bar_h=0.55)
        lab = tx("operating profit as a share of revenue, 2025", 16, GREY_A).move_to([0, 2.1, 0])
        hat = draw.hardhat(1.0).move_to([-5.6, 1.0, 0])
        road = draw.toll_road(3.0).scale(0.7).move_to([-4.6, -1.8, 0])
        src = source("Ferrovial SE, Form 20-F for 2025: income statement by business segment", size=12)
        beat(self,
             "Ferrovial, a European infrastructure group that reports to America's securities regulator, does both. "
             "<bookmark mark='a'/> Its construction arm "
             f"had {cr / 1e3:.2f} billion euros of revenue in 2025 and kept {100 * co / cr:.1f} per cent as operating "
             f"profit: a builder's margin. <bookmark mark='b'/> Its toll roads had {hr / 1e3:.2f} billion euros of revenue "
             f"and kept {100 * ho / hr:.0f} per cent. Same company, same engineers. The difference is what each one sells: "
             "the construction arm sells a road once; the motorway company owns the road and sells every trip on it, "
             "for decades.",
             base=[lab, hat, road, src], steps=[rows[0], rows[1]])

    def road(self):
        K = R["concession"]
        rev, net = K["e407"]
        road = draw.toll_road(9.0).move_to([0, 1.6, 0])
        c = stat_cards([(f"C${rev / 1e3:.2f}bn", "the 407 ETR's revenue, 2025", HWY), (f"C${net / 1e3:.2f}bn", "its net profit", GOOD),
                        (f"{K['stake']}%", "Ferrovial's share of it", PRICE)], y=-1.0, size=38, span=12)
        src = source("Ferrovial SE, Form 20-F for 2025", size=12)
        beat(self,
             "Its prize is a road in Toronto: the 407 Express Toll Route. <bookmark mark='a'/> In 2025 it took in "
             f"{rev:,.0f} million Canadian dollars, up eighteen per cent, mostly because tolls were raised in February, "
             f"<bookmark mark='b'/> and made a net profit of {net:,.0f} million: {100 * net / rev:.0f} cents of every "
             f"dollar. <bookmark mark='c'/> Ferrovial owns {K['stake']} per cent of it.",
             base=[road, src], steps=[c[0], c[1], c[2]])

    def price(self):
        K = R["concession"]
        whole = K["buy"] / 0.0506
        c = stat_cards([(f"C${K['buy']:.2f}bn", "paid in June 2025 for 5.06% more of the 407 ETR", PRICE),
                        (f"C${whole:.0f}bn", "what that values the whole road at", HWY)], y=0.8, size=42, span=10)
        note = tx("a builder bids for one job at a time; an owner is paid for the road, every day, for decades", 18, WHITE).move_to([0, -1.4, 0])
        tag = estimate_tag("this series' arithmetic: 1.99 / 0.0506", size=12)
        src = source("Ferrovial SE, Form 20-F for 2025", size=12)
        beat(self,
             "What is such a road worth? <bookmark mark='a'/> In June 2025 Ferrovial paid "
             f"{K['buy']:.2f} billion Canadian dollars for another 5.06 per cent of it. <bookmark mark='b'/> At that price, "
             f"the whole road would be worth about {whole:.0f} billion. <bookmark mark='c'/> That is the logic of the "
             "concession: the contractor takes on the risk of building and of traffic, and in return is paid for the use "
             "of the thing for decades, not for the work of making it once.",
             base=[tag, src], steps=[c[0], c[1], note])

    def risk(self):
        M = R["mega"]
        road = draw.toll_road(8.0).move_to([0, 1.7, 0])
        g = VGroup(tx("the builder's risk: the cost of building, for a few years", 19, "#F2A65A", bold=True),
                   tx("the owner's risk: how many people use the road, for decades", 19, "#F2A7B5", bold=True),
                   tx(f"roads: even odds that traffic forecasts are wrong by more than a fifth (Flyvbjerg)", 17, GREY_A)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -0.9, 0])
        src = source("Flyvbjerg (2014)", size=12)
        beat(self,
             "Owning is not free money. <bookmark mark='a'/> A builder's risk is the cost of building, and it ends when "
             "the road opens. <bookmark mark='b'/> An owner's risk is whether people drive on it, and it lasts for the "
             "length of the concession. <bookmark mark='c'/> Flyvbjerg's figures for roads put even odds on traffic "
             "forecasts being wrong by more than a fifth. A toll road that drivers use earns like the 407; one they avoid "
             "can bankrupt its owner while the builder, paid long ago, has moved on.",
             base=[road, src], steps=[g[0], g[1], g[2]])

    def book(self):
        K = R["concession"]
        c = stat_cards([(f"€{K['book']:.1f}bn", "Ferrovial's construction order book, end of 2025", CON),
                        (f"{K['public']}%", "of it for public-sector clients", MAKE)], y=0.8, size=42, span=10)
        note = tx("the order book is years of work, mostly for governments, at a builder's margin", 18, GREY_A).move_to([0, -1.2, 0])
        src = source("Ferrovial SE, Form 20-F for 2025", size=12)
        beat(self,
             "And the building side? <bookmark mark='a'/> At the end of 2025 Ferrovial's construction arm had "
             f"{K['book']:.1f} billion euros of work signed and not yet done, about two years of its revenue, "
             f"<bookmark mark='b'/> {K['public']} per cent of it for governments and other public bodies. Building is "
             "the work; owning is the return.",
             base=[src], steps=[c[0], [c[1], note]])
