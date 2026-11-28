from __future__ import annotations

from videos.industry.industry33.common import *  # noqa: F403


class Trading(VoiceoverScene):
    def construct(self):
        card(self, 7, "The trading house", "What happens to a middleman that starts to own what it trades?",
             "Chapter seven. The trading house. Japan's great trading companies began by buying and selling for others. "
             "Look at where one of them now makes its money.", lit=("dollar", "change"))
        self.income()
        self.cash()
        self.risk()
        self.crops()

    def income(self):
        T = R["trading"]
        items = [("gross profit", T["gp"], TRADE, f"¥{T['gp']:,.0f}bn"),
                 ("share of profit of companies it partly owns", T["equity"], TRADE, f"¥{T['equity']:,.0f}bn"),
                 ("dividends from its holdings", T["div"], TRADE, f"¥{T['div']:,.0f}bn"),
                 ("profit for its owners", T["profit"], GOOD, f"¥{T['profit']:,.0f}bn")]
        rows = hbars(items, max_value=1400, x0=0.4, top=0.9, row=0.95, length=6.0, size=17, bar_h=0.5)
        rev = VGroup(tx(f"revenue: ¥{T['rev'] / 1e3:.1f} trillion", 24, ALL, bold=True),
                     tx("at this scale its bar would run ten screens to the right", 15, GREY_A)).arrange(DOWN, buff=0.08).move_to([0, 2.1, 0])
        hd = tx("Mitsui & Co., year to March 2026", 21, WHITE, bold=True).to_edge(UP, buff=0.4)
        src = source("Mitsui & Co., consolidated financial results for the year ended 31 March 2026 (IFRS)", size=12)
        beat(self,
             f"<bookmark mark='a'/> Mitsui's revenue was {T['rev'] / 1e3:.1f} trillion yen. <bookmark mark='b'/> Its gross "
             f"profit, what it kept after paying for what it sold, {T['gp']:,.0f} billion: under ten yen in a hundred. "
             f"<bookmark mark='c'/> Its share of the profits of companies it partly owns, from Australian iron ore mines to "
             f"gas projects, {T['equity']:,.0f} billion. <bookmark mark='d'/> Dividends from other holdings, "
             f"{T['div']:,.0f} billion. <bookmark mark='e'/> And profit for its owners, {T['profit']:,.0f} billion yen: more "
             "than half of it from being an owner, not a trader.",
             base=[hd, rows.axis, src], steps=[rev, rows[0], rows[1], rows[2], rows[3]])

    def cash(self):
        T = R["trading"]
        cf = T["cf"]
        cols = {"metals and mines": CROP, "energy": BAD, "machinery and infrastructure": IND, "chemicals": TECH,
                "innovation and corporate": DRUG, "iron and steel products": ALL, "lifestyle (food, retail, health)": FOOD}
        items = [(k, v, cols[k], f"¥{v:.0f}bn") for k, v in cf.items()]
        rows = hbars(items, max_value=350, x0=0.0, top=2.0, row=0.62, length=5.8, size=16, bar_h=0.36)
        hd = tx(f"Mitsui's core operating cash flow by business, year to March 2026 (total ¥{T['cf_total']:.0f}bn)", 19, WHITE, bold=True).to_edge(UP, buff=0.5)
        src = source("Mitsui & Co., consolidated financial results for the year ended 31 March 2026", size=12)
        beat(self,
             "Where does the cash come from? <bookmark mark='a'/> Metals and mines: "
             f"{cf['metals and mines']:.0f} billion yen. <bookmark mark='b'/> Energy, mostly oil and gas: "
             f"{cf['energy']:.0f} billion. <bookmark mark='c'/> Machinery and infrastructure, chemicals and the rest, less. "
             f"<bookmark mark='d'/> And lifestyle, the food, retail and health businesses closest to old-fashioned trading: "
             f"{cf['lifestyle (food, retail, health)']:.0f} billion. In this series' reading, the trading house solved the "
             "middleman's problem of thin margins by buying stakes in the things it used to trade, which also means it now "
             "carries the owner's risk: when iron ore or oil prices fall, so do its profits.",
             base=[rows.axis, hd, src], steps=[rows[0], rows[1], VGroup(*rows[2:6]), rows[6]])

    def risk(self):
        T = R["trading"]
        items = [("energy's cash, year to March 2025", get("mi33.cf.en.prev"), BAD, f"¥{get('mi33.cf.en.prev'):.0f}bn"),
                 ("energy's cash, year to March 2026", T["cf"]["energy"], BAD, f"¥{T['cf']['energy']:.0f}bn"),
                 ("profit for owners, year to March 2025", 900.3, GOOD, "¥900bn"),
                 ("profit for owners, year to March 2026", T["profit"], GOOD, f"¥{T['profit']:.0f}bn")]
        rows = hbars(items, max_value=950, x0=0.6, top=1.6, row=0.95, length=5.6, size=17, bar_h=0.5)
        hd = tx("Mitsui: an owner's year", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("Mitsui & Co., consolidated financial results for the year ended 31 March 2026", size=12)
        beat(self,
             "Being an owner brings an owner's swings. <bookmark mark='a'/> In the year to March 2025 Mitsui's energy "
             f"businesses produced {get('mi33.cf.en.prev'):.0f} billion yen of cash; <bookmark mark='b'/> a year later, with "
             f"lower oil and gas prices, {T['cf']['energy']:.0f} billion. <bookmark mark='c'/> Profit for its owners fell "
             f"from 900 billion yen <bookmark mark='d'/> to {T['profit']:.0f} billion. A pure middleman's profit moves with "
             "the volume it handles; an owner's moves with the price of what it owns.",
             base=[rows.axis, hd, src], steps=[rows[0], rows[1], rows[2], rows[3]])

    def crops(self):
        T = R["trading"]
        q = quote(["'... as we partner with farmers to move crops from where they are grown to where they are needed'"],
                  "Bunge Global, Form 10-K for 2025", size=19).move_to([0, 2.0, 0])
        rows = [["", "revenue", "kept after the goods", "net profit per dollar"],
                ["Bunge", f"${T['bunge']['rev']:.0f}bn", f"{T['bunge']['gross']:.1f}c", f"{T['bunge']['net']:.1f}c"],
                ["ADM", f"${T['adm']['rev']:.0f}bn", f"{T['adm']['gross']:.1f}c", f"{T['adm']['net']:.1f}c"]]
        cols = [None, [CROP, WHITE, TRADE, GOOD], [CROP, WHITE, TRADE, GOOD]]
        t = table(rows, col_x=[-5.6, -3.4, -0.9, 2.6], top=0.4, row_h=0.8, size=19, colors=cols)
        ship = draw.ship(2.6).move_to([0, -2.2, 0])
        src = source("Bunge Global and ADM, Forms 10-K for 2025 via SEC company facts", size=12)
        beat(self,
             "The crop traders do the same job for grain and oilseeds. <bookmark mark='a'/> Bunge describes it in one line: "
             "moving crops from where they are grown to where they are needed. <bookmark mark='b'/> On "
             f"{T['bunge']['rev']:.0f} billion dollars of revenue in 2025 it kept {T['bunge']['net']:.1f} cents a dollar. "
             f"<bookmark mark='c'/> ADM, {T['adm']['net']:.1f}. Like Mitsui, both own much of what sits between the field "
             "and the buyer, from grain elevators to crushing plants and port terminals; in this series' reading, owning "
             "the bottlenecks is where a trader's margin is safest.",
             base=[src], steps=[q, VGroup(t[0], t[1], ship), t[2]])
