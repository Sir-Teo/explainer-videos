from __future__ import annotations

from videos.industry.industry23.common import *  # noqa: F403

MC_NAME = {"fashion": "Fashion & Leather Goods", "watches": "Watches & Jewelry", "wines": "Wines & Spirits",
           "retail": "Selective Retailing (Sephora)", "perfume": "Perfumes & Cosmetics"}


class Luxury(VoiceoverScene):
    def construct(self):
        card(self, 7, "Luxury: selling the wait", "How does a house keep 41 cents of every euro?",
             "Chapter seven. Luxury. The third answer to the buyer's problem: make fewer than people want, so there is "
             "nothing left over, and never sell anything off.", lit=("moat", "dollar"))
        self.dollar()
        self.growth()
        self.workshops()
        self.leather()
        self.coach()

    def dollar(self):
        L = R["luxury"]
        rev = L["rms"][2025][0] / 1e3
        gm = L["gross"] / rev
        roi = L["rms"][2025][1] / 1e3 / rev
        parts = [("making it", 1 - gm, DEPT), ("shops, staff, marketing, the rest", gm - roi, FAST), ("operating profit", roi, LUX)]
        bar = viz.bar_split(parts, 1.0, width=12.0, height=0.9).move_to([0, 0.4, 0])
        labs = VGroup()
        for i, (n, v, c) in enumerate(parts):
            labs.add(VGroup(tx(f"{100 * v:.0f}c", 24, c, bold=True), tx(n, 14, GREY_A)).arrange(DOWN, buff=0.06).next_to(bar[i], DOWN, buff=0.2))
        bag = draw.handbag(1.8, color=LEATHER).move_to([0, 2.4, 0])
        nk = tx(f"NIKE: {100 * R['dollar']['make']:.0f}c of each dollar on making the product", 16, SPORT).move_to([0, -2.1, 0])
        src = source("Hermès International, 2025 full-year results: revenue, cost of sales, recurring operating income", size=12)
        beat(self,
             f"Take a euro of Hermès's revenue in 2025. <bookmark mark='a'/> About {100 * (1 - gm):.0f} cents paid for making "
             f"what it sold. <bookmark mark='b'/> About {100 * (gm - roi):.0f} cents ran its shops, paid its staff and its "
             f"marketing. <bookmark mark='c'/> And {100 * roi:.0f} cents was left as operating profit. <bookmark mark='d'/> "
             f"Compare NIKE, where making the product took {100 * R['dollar']['make']:.0f} cents of each dollar. Hermès "
             f"sells what it makes for about {1 / (1 - gm):.1f} times what it cost to make.",
             base=[bag, src], steps=[[bar[0], labs[0]], [bar[1], labs[1]], [bar[2], labs[2]], nk])

    def growth(self):
        L = R["luxury"]["rms"]
        items = [(str(y), v / 1e3, LUX, f"€{v / 1e3:.1f}bn") for y, (v, o) in L.items()]
        bars_ = vbars(items, base_y=-2.4, height=3.8, width=1.2, gap=0.7, size=18, max_value=17)
        margins = VGroup(*[tx(f"{100 * o / v:.1f}% kept", 14, PRICE).next_to(b[0], UP, buff=0.45) for b, (y, (v, o)) in zip(bars_, L.items())])
        lab = tx("Hermès's revenue, and the share kept as recurring operating profit", 16, GREY_A).to_edge(UP, buff=0.6)
        src = source("Hermès International, full-year results releases for 2023, 2024 and 2025", size=12)
        beat(self,
             f"And it has been growing. <bookmark mark='a'/> Hermès's revenue was {L[2022][0] / 1e3:.1f} billion euros in 2022, "
             f"<bookmark mark='b'/> {L[2023][0] / 1e3:.1f} billion in 2023, <bookmark mark='c'/> {L[2024][0] / 1e3:.1f} in "
             f"2024 <bookmark mark='d'/> and {L[2025][0] / 1e3:.1f} in 2025, and in every one of those years it kept "
             "between forty and forty-two cents of each euro as operating profit. In 2025 LVMH's revenue fell five per cent "
             f"and Kering's {100 * (1 - get('ker.rev') / get('ker.rev.2024')):.0f}; Hermès's went on rising.",
             base=[lab, src], steps=[[bars_[i], margins[i]] for i in range(4)])

    def workshops(self):
        L = R["luxury"]
        row = VGroup(*[draw.handbag(0.42, color=LEATHER if i < L["workshops"] else GREY_B) for i in range(L["workshops"])]
                     ).arrange_in_grid(rows=3, buff=0.18).move_to([0, 1.3, 0])
        c = stat_cards([(f"{L['workshops']:.0f}th", "leather goods workshop, opened September 2025", LUX),
                        (f"{L['inhouse']:.0f}%", "of objects made in its own or exclusive workshops", LUX),
                        (f"{L['france']:.0f}%", "of objects made in France", LUX)], y=-1.2, size=38, span=12)
        src = source("Hermès International, 2025 full-year results", size=12)
        beat(self,
             "How does it decide how many to make? Hermès does not publish that, but it does say what limits it. "
             f"<bookmark mark='a'/> Its {L['workshops']:.0f}th leather goods workshop opened in Charente in September 2025, "
             "and more are planned for 2026, 2027 and 2028. <bookmark mark='b'/> "
             f"{L['inhouse']:.0f} per cent of what it sells is made in its own or exclusive workshops, <bookmark mark='c'/> "
             f"and {L['france']:.0f} per cent is made in France. <bookmark mark='d'/> It says its leather goods grew "
             f"{L['leather_g']} per cent in 2025, 'driven by the strong desirability of the collections and the increase "
             "in production capacities'. Our reading: the sales grow about as fast as the workshops can be built and "
             "staffed. The house sells what it can make, not everything it could sell.",
             base=[src], steps=[row, c[0], c[1], c[2]])

    def leather(self):
        M = R["luxury"]["mc"]
        items = [(MC_NAME[k], p / v, LUX if k == "fashion" else GREY_B, f"{100 * p / v:.0f}% of €{v / 1e3:.1f}bn")
                 for k, (v, p) in sorted(M.items(), key=lambda kv: -kv[1][1] / kv[1][0])]
        rows = hbars(items, max_value=0.4, x0=-0.4, top=1.8, row=0.75, length=6.0, size=17, bar_h=0.42)
        lab = tx("LVMH, 2025: profit from recurring operations as a share of each business's revenue", 15, GREY_A).to_edge(UP, buff=0.7)
        src = source("LVMH, 2025 results (27 January 2026): revenue and profit from recurring operations by business group", size=12)
        f = M["fashion"]
        beat(self,
             f"LVMH, the largest luxury group, with more than {R['luxury']['mc_brands']:.0f} brands, shows where the money "
             "is inside luxury. <bookmark mark='a'/> Its fashion and leather goods, Louis Vuitton, Dior and the rest, sold "
             f"{f[0] / 1e3:.1f} billion euros in 2025 and kept {100 * f[1] / f[0]:.0f} per cent as operating profit. "
             "<bookmark mark='b'/> Wines and spirits, watches and jewellery, Sephora's shops and the perfumes kept between "
             "nine and nineteen per cent. Our reading: perfume and make-up carry luxury names but are made in large numbers "
             "and sold in many other people's shops; a bag from the house's own workshop, sold in the house's own shop, is "
             "where luxury's margins are.",
             base=[rows.axis, lab, src], steps=[rows[:1], rows[1:]])

    def coach(self):
        L = R["luxury"]
        items = [("Coach", L["coach_gm"], LUX, f"{L['coach_gm']}%"), ("Kate Spade", L["kate_gm"], BRANDC, f"{L['kate_gm']}%"),
                 ("NIKE", get("nke.gm.2026"), SPORT, f"{get('nke.gm.2026')}%"), ("Inditex", R["hook"]["gm"], FAST, f"{R['hook']['gm']}%")]
        rows = hbars(items, max_value=85, x0=-0.4, top=1.6, row=0.8, length=6.0, size=18, bar_h=0.44)
        lab = tx("gross margin, latest fiscal year", 16, GREY_A).to_edge(UP, buff=0.8)
        bag = draw.handbag(1.4, color="#8E5A3A").move_to([-5.2, 2.2, 0])
        src = source("Tapestry, Inc., Form 10-K for fiscal 2026 (excluding items affecting comparability); NIKE, Inc., Form "
                     "10-K for fiscal 2026; Inditex, FY2025 results", size=12)
        beat(self,
             "Further down the price ladder, the same rule. <bookmark mark='a'/> Coach, an American leather brand sold at "
             f"a fraction of Hermès's prices, kept {L['coach_gm']} per cent of its sales after the cost of its goods in "
             f"the year to June 2026. Its handbags alone sold {L['coach_bags'] / 1e3:.1f} billion dollars. "
             f"<bookmark mark='b'/> Kate Spade, its sister brand, {L['kate_gm']}. <bookmark mark='c'/> NIKE, "
             f"{get('nke.gm.2026')}. <bookmark mark='d'/> Inditex, {R['hook']['gm']}. The more a product is a name, and "
             "the less it is a piece of cloth, the more of its price is margin.",
             base=[rows.axis, lab, bag, src], steps=[rows[0], rows[1], rows[2], rows[3]])
