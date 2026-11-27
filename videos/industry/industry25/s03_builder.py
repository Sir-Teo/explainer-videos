from __future__ import annotations

from videos.industry.industry25.common import *  # noqa: F403


class Builder(VoiceoverScene):
    def construct(self):
        card(self, 2, "A builder's arithmetic", "What does America's largest builder make on a house?",
             "Chapter two. A builder's arithmetic. The Works' builder was a sketch. Here are the real ones, and the real "
             "squeeze of 2025 and 2026.", lit=("dollar", "unit"))
        self.horton()
        self.margin()
        self.lennar()
        self.incent()
        self.unsold()
        self.subs()

    def horton(self):
        D = R["builder"]["dhi"]
        houses = VGroup(*[draw.house(0.55, color="#F2D0A4") for _ in range(10)]).arrange(RIGHT, buff=0.18).move_to([0, 2.2, 0])
        c = stat_cards([(f"{D['closed']:,.0f}", "homes closed in the year to September 2026", HOUSE),
                        (f"${D['price']:,.0f}k", "average price", PRICE),
                        (f"${D['rev']:.1f}bn", "revenue", GOOD)], y=0.2, size=40, span=12)
        src = source("D.R. Horton, Inc., Form 10-K for fiscal 2026 and Form 8-K of 29 October 2026", size=12)
        beat(self,
             "D.R. Horton, from Fort Worth in Texas, says it has been the largest homebuilder in the United States by "
             "volume every year since 2002. <bookmark mark='a'/> In the "
             f"year to September 2026 it closed {D['closed']:,.0f} homes, more than two hundred and thirty a day, "
             f"<bookmark mark='b'/> at an average price of {D['price']:,.0f} thousand dollars, below the national median for "
             f"a new house, <bookmark mark='c'/> for {D['rev']:.1f} billion dollars of revenue.",
             base=[houses, src], steps=[c[0], c[1], c[2]])

    def margin(self):
        D = R["builder"]["dhi"]
        items = [("home sales gross margin, fiscal 2025", D["gm_prev"], GREY_B, f"{D['gm_prev']}%"),
                 ("home sales gross margin, fiscal 2026", D["gm"], HOUSE, f"{D['gm']}%"),
                 ("homebuilding pre-tax margin, fiscal 2026", D["pretax"], GOOD, f"{D['pretax']}%")]
        rows = hbars(items, max_value=25, x0=0.6, top=1.2, row=1.0, length=5.4, size=17, bar_h=0.5)
        q = tx("'rising mortgage rates, affordability constraints and cautious consumer sentiment'", 16, PRICE).move_to([0, -1.9, 0])
        src = source("D.R. Horton, Inc., Form 10-K for fiscal 2026 and Form 8-K of 29 October 2026", size=12)
        beat(self,
             "What does it keep? <bookmark mark='a'/> After the land, the materials and the trades, "
             f"{D['gm_prev']} cents of each dollar in fiscal 2025, <bookmark mark='b'/> and {D['gm']} cents in fiscal 2026. "
             f"<bookmark mark='c'/> After selling and running the company, {D['pretax']} cents before tax. "
             "<bookmark mark='d'/> The company blamed the slide on 'rising mortgage rates, affordability constraints and "
             "cautious consumer sentiment'. A builder's margin is set less by what it costs to build than by what its "
             "buyers can borrow.",
             base=[rows.axis, src], steps=[rows[0], rows[1], rows[2], q])

    def lennar(self):
        L = R["builder"]["len"]
        items = [(str(y), v, HOUSE if y == 2025 else GREY_B, f"${v:.0f}k") for y, v in L["price"].items()]
        bars_ = vbars(items, base_y=-2.2, height=3.4, width=1.3, gap=0.8, size=18, max_value=470)
        lab = tx("Lennar: average price of a home delivered, fiscal years", 16, GREY_A).to_edge(UP, buff=0.7)
        gm = tx(f"gross margin on home sales: {L['gm'][0]}% to {L['gm'][1]}%", 19, BAD, bold=True).move_to([3.6, 0.6, 0])
        src = source("Lennar Corporation, Form 10-K for fiscal 2025", size=12)
        beat(self,
             "Lennar, the other giant, shows the squeeze in its prices. <bookmark mark='a'/> Its average home sold for "
             f"{L['price'][2023]:.0f} thousand dollars in fiscal 2023, {L['price'][2024]:.0f} thousand in 2024 and "
             f"{L['price'][2025]:.0f} thousand in 2025, while it delivered more homes than the year before: "
             f"{L['deliveries']:,.0f}. <bookmark mark='b'/> Its gross margin fell from {L['gm'][0]} per cent to "
             f"{L['gm'][1]}. It chose to keep building and selling, and let the price give.",
             base=[lab, src], steps=[bars_, gm])

    def incent(self):
        L = R["builder"]["len"]
        items = [("fiscal 2024", L["incent"][0], GREY_B, f"${L['incent'][0]:.1f}k a home"),
                 ("fiscal 2025", L["incent"][1], BAD, f"${L['incent'][1]:.1f}k a home")]
        rows = hbars(items, max_value=70, x0=-0.2, top=1.0, row=1.1, length=6.0, size=18, bar_h=0.55)
        lab = tx("Lennar's sales incentives", 16, GREY_A).move_to([0, 2.1, 0])
        note = tx(f"{L['incent_pct']}% of revenue; D.R. Horton's include 'mortgage rate buydowns'", 18, PRICE, bold=True).move_to([0, -1.6, 0])
        key = draw.house_key(1.2).move_to([-5.2, -1.6, 0])
        src = source("Lennar Corporation, Form 10-K for fiscal 2025", size=12)
        beat(self,
             "How do you cut a price without cutting it? <bookmark mark='a'/> With incentives. In fiscal 2024 Lennar gave "
             f"buyers incentives worth {L['incent'][0]:.1f} thousand dollars a home; <bookmark mark='b'/> in fiscal 2025, "
             f"{L['incent'][1]:.1f} thousand, {L['incent_pct']} per cent of its revenue. <bookmark mark='c'/> D.R. Horton "
             "says its incentives include 'mortgage rate buydowns', and expects them to stay high in fiscal 2027. A "
             "buydown lowers the buyer's monthly payment without lowering the price on the contract: the builder pays to "
             "fix the loan, because the loan is what the buyer can or cannot afford.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1], [note, key]])

    def subs(self):
        frame = draw.house_frame(2.4).move_to([-3.6, 0.4, 0])
        hats = VGroup(*[draw.hardhat(0.6, color=c) for c in ("#F6C453", "#F2A65A", "#7EC8F5", "#7BD88F", "#B58CFF")]).arrange(RIGHT, buff=0.3).move_to([3.2, 1.0, 0])
        q = quote(["'We hire subcontractors for site improvements and virtually all of the work involved",
                   "in the construction of homes.'"], "Lennar Corporation, Form 10-K for fiscal 2025", size=17).move_to([2.6, -0.8, 0])
        src = source("Lennar Corporation, Form 10-K for fiscal 2025", size=12)
        beat(self,
             "And who actually builds the house? <bookmark mark='a'/> Not the builder. Lennar's report says it hires "
             "subcontractors for site work 'and virtually all of the work involved in the construction of homes'. "
             "<bookmark mark='b'/> The framers, roofers, plumbers and electricians of Part 24 are separate firms. The "
             "homebuilder's real jobs are the ones it keeps: finding and controlling land, getting approvals, designing a "
             "few plans, selling, and arranging the buyer's loan.",
             base=[frame, src], steps=[q, hats])

    def unsold(self):
        D = R["builder"]["dhi"]
        houses = VGroup(*[draw.house(0.42, color="#F2D0A4" if i < 18 else "#5C6472") for i in range(28)]).arrange_in_grid(rows=2, buff=0.14).move_to([0, 1.6, 0])
        c = stat_cards([(f"{get('dhi.inventory'):,.0f}", "homes in D.R. Horton's inventory, September 2026", HOUSE),
                        (f"{D['unsold']:,.0f}", "of them not yet sold to anyone", BAD),
                        (f"{get('dhi.finished'):,.0f}", "unsold and already finished", PRICE)], y=-0.9, size=36, span=12)
        src = source("D.R. Horton, Inc., Form 8-K of 29 October 2026", size=12)
        beat(self,
             "And a builder carries houses as well as land. <bookmark mark='a'/> At the end of September 2026 D.R. Horton "
             f"had {get('dhi.inventory'):,.0f} homes under construction or finished, <bookmark mark='b'/> "
             f"{D['unsold']:,.0f} of them not yet sold to anyone, <bookmark mark='c'/> and {get('dhi.finished'):,.0f} of those "
             "already "
             "finished, waiting for a buyer. A finished house nobody has bought is the builder's most expensive kind of "
             "inventory, and the incentives above are how it gets sold.",
             base=[houses, src], steps=[c[0], c[1], c[2]])
