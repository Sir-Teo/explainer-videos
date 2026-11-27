from __future__ import annotations

from videos.industry.industry24.common import *  # noqa: F403


class Dollar(VoiceoverScene):
    def construct(self):
        card(self, 2, "Where a building's dollar goes", "Who in the chain keeps the money?",
             "Chapter two. Where a building's dollar goes. From the owner who pays for a building to the quarry that "
             "supplies its gravel, who keeps what?", lit=("dollar", "unit"))
        self.spend()
        self.pay()
        self.chain()
        self.quarry()
        self.rental()

    def spend(self):
        S = R["spending"]
        D = R["dollar"]
        y = 2025
        parts = [("homes", S["residential"][y], "#F2A65A"), ("everything else: factories, offices, roads, power", S["nonresidential"][y], BUILD)]
        tot = sum(v for _, v, _ in parts)
        bar = viz.bar_split(parts, tot, width=11.0, height=0.9).move_to([0, 0.8, 0])
        labs = VGroup(*[VGroup(tx(f"${v:,.0f}bn", 22, c, bold=True), tx(n, 14, GREY_A)).arrange(DOWN, buff=0.06).next_to(bar[i], DOWN, buff=0.2)
                        for i, (n, v, c) in enumerate(parts)])
        pub = tx(f"of which paid for by governments: ${S['public'][y]:,.0f}bn", 18, MAKE, bold=True).move_to([0, -1.8, 0])
        crane = draw.tower_crane(1.6).move_to([-5.2, 2.4, 0]).scale(0.7)
        src = source("Census Bureau, value of construction put in place, annual average of seasonally adjusted rates, via FRED", size=12)
        beat(self,
             f"Start with the size of it. <bookmark mark='a'/> In 2025 America spent about {D['spend']:.2f} trillion "
             f"dollars on construction. About {S['residential'][y]:,.0f} billion went on homes, new ones and improvements "
             f"to old ones, <bookmark mark='b'/> and {S['nonresidential'][y]:,.0f} billion on everything else: factories, "
             f"offices, warehouses, schools, roads and power lines. <bookmark mark='c'/> Governments paid for about "
             f"{S['public'][y]:,.0f} billion of it: most roads, schools and water works are public jobs.",
             base=[crane, src], steps=[[bar[0], labs[0]], [bar[1], labs[1]], pub])

    def pay(self):
        D = R["dollar"]
        items = [("construction", D["comp"], BUILD, f"{D['comp']}%"), ("the whole economy", D["all_comp"], ALL, f"{D['all_comp']}%")]
        rows = hbars(items, max_value=80, x0=-0.4, top=1.0, row=1.0, length=6.0, size=18, bar_h=0.5)
        lab = tx("share of value added paid to employees, 2025", 16, GREY_A).move_to([0, 2.0, 0])
        hats = VGroup(*[draw.hardhat(0.5) for _ in range(6)]).arrange(RIGHT, buff=0.2).move_to([0, -1.8, 0])
        src = source("BEA, value added by industry and its components, 2025", size=12)
        beat(self,
             "Construction is still mostly people's time. <bookmark mark='a'/> Of the value construction added to the "
             f"American economy in 2025, {D['va']:.2f} trillion dollars, {D['comp']} per cent was paid to the people who "
             f"work in it. <bookmark mark='b'/> Across the whole economy the share is {D['all_comp']} per cent. A factory "
             "spreads its people over many identical products; a building site starts again, by hand, every time.",
             base=[rows.axis, lab, src], steps=[rows[0], [rows[1], hats]])

    def chain(self):
        G = R["chain"]
        order = ["general", "trade", "engineer", "concession", "rental", "materials"]
        items = [(GROUP_NAME[k], G[k], GROUP_COL[k], f"{100 * G[k]:.1f}%") for k in order]
        rows = hbars(items, max_value=0.18, x0=-0.2, top=1.8, row=0.72, length=6.0, size=17, bar_h=0.42)
        lab = tx("net income per dollar of revenue: the median company in each group, last five years", 15, GREY_A).to_edge(UP, buff=0.7)
        src = source("Forms 10-K and 20-F via SEC company facts; groups as in the landscape (chapter nine)", size=12)
        beat(self,
             "Now follow a dollar down the chain. <bookmark mark='a'/> The general contractors, who take on the whole "
             f"job and hire everyone else, have kept about {100 * G['general']:.0f} cents of each dollar as profit. The "
             f"specialty contractors, the electricians, mechanical and pipeline firms, about {100 * G['trade']:.0f}. "
             f"<bookmark mark='b'/> The engineers, who sell hours of design rather than buildings, about "
             f"{100 * G['engineer']:.0f}. <bookmark mark='c'/> The companies that rent out the cranes, lifts and "
             f"diggers, about {100 * G['rental']:.0f}, and the makers of cement, concrete and crushed stone, about "
             f"{100 * G['materials']:.0f}. The money is not with the builder; it is with whoever owns something the "
             "builder cannot do without.",
             base=[rows.axis, lab, src], steps=[rows[:2], rows[2:4], rows[4:]])

    def quarry(self):
        comp = {c["name"]: c for c in R["landscape"]["companies"]}
        items = [(n, comp[n]["margin"], GROUP_COL["materials"], f"{100 * comp[n]['margin']:.1f}%") for n in
                 ("Eagle Materials", "Martin Marietta", "Vulcan Materials", "CRH")]
        rows = hbars(items, max_value=0.25, x0=-0.4, top=1.4, row=0.8, length=6.0, size=18, bar_h=0.45)
        pile = draw.pile(1.6, color="#9AA3B2", shape="jagged")
        pile.move_to([-5.4, -1.8, 0])
        truck = draw.mixer_truck(1.8).move_to([4.8, -2.0, 0])
        lab = tx("net margin, median of the last five years", 15, GREY_A).to_edge(UP, buff=0.8)
        src = source("Forms 10-K via SEC company facts", size=12)
        beat(self,
             "Why do the materials companies keep so much? <bookmark mark='a'/> Martin Marietta and Vulcan sell crushed "
             f"stone, sand and gravel, and kept {100 * comp['Martin Marietta']['margin']:.0f} and "
             f"{100 * comp['Vulcan Materials']['margin']:.0f} cents of each dollar; Eagle, a cement maker, "
             f"{100 * comp['Eagle Materials']['margin']:.0f}. Martin Marietta's own report gives the reason: how far stone "
             "travels by truck is limited, 'because the cost of transporting processed aggregates to customers is high "
             "relative to the price of the product itself'. A quarry close to a growing city has few rivals within "
             "reach, the kind of local moat Part 5 described. <bookmark mark='b'/> CRH, the largest, about "
             f"{100 * comp['CRH']['margin']:.0f}.",
             base=[rows.axis, lab, pile, truck, src], steps=[rows[:3], rows[3:]])

    def rental(self):
        comp = {c["name"]: c for c in R["landscape"]["companies"]}
        u, h = comp["United Rentals"], comp["Herc"]
        exc = draw.excavator(2.6).move_to([-3.6, 0.6, 0])
        crane = draw.tower_crane(1.4).move_to([3.8, 0.2, 0])
        c = stat_cards([(f"${u['rev']:.1f}bn", "United Rentals' revenue, 2025", GROUP_COL["rental"]),
                        (f"{100 * u['margin']:.0f}%", "of it kept as net income (median, five years)", GOOD),
                        (f"{100 * h['margin']:.0f}%", "Herc, a smaller rival", GROUP_COL["rental"])], y=-1.8, size=34, span=12)
        src = source("Forms 10-K via SEC company facts", size=12)
        beat(self,
             "And the machines. <bookmark mark='a'/> Many builders rent their diggers, lifts and cranes rather than own "
             f"them, for the weeks a site needs them. The largest renter, United Rentals, took in {u['rev']:.1f} billion "
             f"dollars in 2025, <bookmark mark='b'/> and has kept about {100 * u['margin']:.0f} cents of each dollar as "
             f"profit, five times what a general contractor keeps. <bookmark mark='c'/> Herc, a smaller rival, about "
             f"{100 * h['margin']:.0f}. The renter owns the fleet and keeps it busy across hundreds of sites; the builder "
             "pays for each machine only while it works.",
             base=[exc, crane, src], steps=[c[0], c[1], c[2]])

