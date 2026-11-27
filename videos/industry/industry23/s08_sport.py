from __future__ import annotations

from videos.industry.industry23.common import *  # noqa: F403

CHAL_COL = {"On": "#F6C453", "Lululemon": BAD, "Deckers (HOKA, UGG)": FAST, "NIKE": SPORT}


class Sport(VoiceoverScene):
    def construct(self):
        card(self, 6, "Sport: the brand and the contract factory", "What does NIKE actually do with a dollar?",
             "Chapter six. Sport. The sports brands sit between fast fashion and luxury: they sell the same shoe for "
             "years, but they still have to guess how many, and they own a name worth more than their factories would be.",
             lit=("dollar", "moat"))
        self.dollar()
        self.revenue()
        self.channels()
        self.challengers()

    def dollar(self):
        D = R["dollar"]
        parts = [("the product, made and delivered", D["make"], DEPT), ("demand creation: ads and athletes", D["demand"], PRICE),
                 ("shops, staff, offices, the rest", D["other"], FAST), ("net income", D["net"], GOOD)]
        bar = viz.bar_split(parts, 1.0, width=12.0, height=0.9).move_to([0, 0.6, 0])
        labs = VGroup()
        for i, (n, v, c) in enumerate(parts):
            t = VGroup(tx(f"{100 * v:.0f}c", 22, c, bold=True), tx(n, 13, GREY_A)).arrange(DOWN, buff=0.06)
            if t.width > bar[i].width + 0.4:
                t.scale_to_fit_width(bar[i].width + 0.4)
            t.next_to(bar[i], DOWN if i % 2 == 0 else UP, buff=0.2)
            labs.add(t)
        shoe = draw.sneaker(2.0).move_to([0, 2.7, 0])
        src = source("NIKE, Inc., Form 10-K for fiscal 2026: revenues, cost of sales, demand creation expense, net income", size=12)
        beat(self,
             f"Take a dollar of NIKE's sales in the year to May 2026. <bookmark mark='a'/> About {100 * D['make']:.0f} cents "
             "paid for the product: mostly what NIKE paid for the goods, landed, plus its warehouses and the costs of "
             "designing them. <bookmark mark='b'/> "
             f"About {100 * D['demand']:.0f} cents went on what NIKE calls demand creation: advertising, and the contracts "
             f"with athletes and teams. <bookmark mark='c'/> About {100 * D['other']:.0f} cents ran its own shops, its "
             f"websites, its offices and its people. <bookmark mark='d'/> And {100 * D['net']:.0f} cents was left as profit. "
             "It was a poor year by NIKE's standards, but the shape is the business: the factory gets a little over half, "
             "and the rest is the brand and the selling.",
             base=[shoe, src], steps=[[bar[0], labs[0]], [bar[1], labs[1]], [bar[2], labs[2]], [bar[3], labs[3]]])

    def revenue(self):
        B = R["brands"]
        ch = line_chart({"NIKE": (B["nke_rev"], SPORT)}, x=(2015, 2026), y=(25, 55), xticks=[2015, 2017, 2019, 2021, 2023, 2026],
                        yticks=[25, 30, 35, 40, 45, 50, 55], xfmt=lambda v: f"FY{int(v) % 100:02d}", yfmt=lambda v: f"${v:.0f}bn",
                        ylabel="NIKE's revenue, fiscal years to May", width=9.4, height=4.4, center=(-0.6, -0.45), label_end=False)
        pk = max(B["nke_rev"], key=B["nke_rev"].get)
        m1 = marker(ch.ax, pk, B["nke_rev"][pk], f"FY{pk % 100}: ${B['nke_rev'][pk]:.1f}bn", SPORT, side=UP)
        m2 = marker(ch.ax, 2026, B["nke_rev"][2026], f"FY26: ${B['nke_rev'][2026]:.1f}bn", BAD, side=DOWN)
        src = source("NIKE, Inc., Forms 10-K via SEC company facts", size=12)
        beat(self,
             "NIKE's sales grew for most of a decade. <bookmark mark='a'/> They peaked at "
             f"{B['nke_rev'][pk]:.1f} billion dollars in the year to May {pk}, <bookmark mark='b'/> and fell to "
             f"{B['nke_rev'][2025]:.1f} billion the next year, and {B['nke_rev'][2026]:.1f} the year after. In this series' "
             "reading, part of the fall was a choice that went wrong, and NIKE's own figures show the choice.",
             base=[ch.frame, src], steps=[[ch.lines["NIKE"], m1], m2])

    def channels(self):
        C = R["brands"]["channel"]
        items = []
        for y in (2024, 2025, 2026):
            w, d = C[y]
            items += [(f"FY{y % 100} wholesale", w / 1e3, DEPT, f"${w / 1e3:.1f}bn"), (f"FY{y % 100} NIKE Direct", d / 1e3, SPORT, f"${d / 1e3:.1f}bn")]
        rows = hbars(items, max_value=30, x0=-0.2, top=2.2, row=0.62, length=6.4, size=16, bar_h=0.36)
        lab = tx("NIKE Brand sales: to other shops (wholesale) and through its own shops and apps (NIKE Direct)", 15, GREY_A).to_edge(UP, buff=0.4)
        q = tx("'reinvesting in wholesale distribution'", 18, PRICE, bold=True).move_to([0, -2.1, 0])
        src = source("NIKE, Inc., Form 10-K for fiscal 2026", size=12)
        w24, d24 = C[2024]
        w26, d26 = C[2026]
        beat(self,
             "For years NIKE pushed to sell more through its own shops and apps, and less through other people's shops. "
             f"<bookmark mark='a'/> In fiscal 2024 it sold {w24 / 1e3:.1f} billion dollars through other shops and "
             f"{d24 / 1e3:.1f} billion directly. <bookmark mark='b'/> In fiscal 2025 both fell. <bookmark mark='c'/> In "
             f"fiscal 2026 the direct business fell again, to {d26 / 1e3:.1f} billion, and the wholesale business grew back "
             f"to {w26 / 1e3:.1f}. <bookmark mark='d'/> NIKE's 2026 report describes 'reinvesting in wholesale "
             "distribution'. Our reading: selling direct keeps the margin a retailer would take, but it also leaves the "
             "brand carrying all of the stock and all of the guessing, and away from the shops where many of its "
             "customers still bought their shoes.",
             base=[rows.axis, lab, src], steps=[rows[:2], rows[2:4], rows[4:], q])

    def challengers(self):
        B = R["brands"]
        base = 2019
        nke = {y: v / B["nke_rev"][base] for y, v in B["nke_rev"].items() if y >= base}
        lulu = {y: v / B["lulu_rev"][base] for y, v in B["lulu_rev"].items() if y >= base}
        on = {y: v / B["on_rev"][base] for y, v in B["on_rev"].items() if y >= base}
        deck = {y: v / B["deck_rev"][base] for y, v in B["deck_rev"].items() if y >= base}
        series = {"On": (on, CHAL_COL["On"]), "Lululemon": (lulu, CHAL_COL["Lululemon"]),
                  "Deckers (HOKA, UGG)": (deck, CHAL_COL["Deckers (HOKA, UGG)"]), "NIKE": (nke, CHAL_COL["NIKE"])}
        ch = line_chart(series, x=(2019, 2026), y=(0, 12), xticks=list(range(2019, 2027)), yticks=[0, 1, 2, 4, 6, 8, 10, 12],
                        yfmt=lambda v: f"x{v:.0f}", ylabel="sales against the fiscal year ending in 2019 (= 1), own currency",
                        width=9.4, height=4.4, center=(-0.9, -0.45), nudge={"Deckers (HOKA, UGG)": -0.25, "Lululemon": 0.2})
        src = source("Forms 10-K and 20-F via SEC company facts; each fiscal year placed at the year it ends in (On reports "
                     "in Swiss francs, by calendar year; its latest is 2025)", size=12)
        beat(self,
             "Meanwhile, smaller brands grew around it. <bookmark mark='a'/> NIKE's sales in its latest year were about "
             f"{nke[2026]:.1f} times those of the year ending in 2019. <bookmark mark='b'/> Lululemon's were "
             f"{lulu[2026]:.1f} times; Deckers, owner of HOKA and UGG, {deck[2026]:.1f} times; and On, the Swiss running "
             f"brand, {on[2025]:.0f} times by 2025, from a small start. Lululemon's report says it does not own or operate "
             "any factories at all. The contract factory that made NIKE a giant works for its challengers too.",
             base=[ch.frame, src], steps=[[ch.lines["NIKE"], ch.labels["NIKE"]],
                                          [ch.lines[k] for k in ("Lululemon", "Deckers (HOKA, UGG)", "On")] +
                                          [ch.labels[k] for k in ("Lululemon", "Deckers (HOKA, UGG)", "On")]])
