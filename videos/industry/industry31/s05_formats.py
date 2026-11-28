from __future__ import annotations

from videos.industry.industry31.common import *  # noqa: F403


class Formats(VoiceoverScene):
    def construct(self):
        card(self, 4, "Big boxes and small ones", "Why does one chain build huge stores and another tiny ones?",
             "Chapter four. Big boxes and small ones. The same business comes in very different sizes, each a bet about "
             "how far a shopper will travel and how much she will buy.", lit=("make", "moat"))
        self.sizes()
        self.per_store()
        self.per_foot()
        self.dollar_general()
        self.dg_money()

    def sizes(self):
        Fm = R["formats"]
        boxes = VGroup(Rectangle(width=4.2, height=1.6, stroke_color=CLUB, stroke_width=3), Rectangle(width=3.0, height=1.4, stroke_color=MASS, stroke_width=3),
                       Rectangle(width=1.6, height=1.0, stroke_color=GROCER, stroke_width=3), Rectangle(width=0.6, height=0.5, stroke_color=DOLLAR, stroke_width=3)
                       ).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).move_to([0, 0.8, 0])
        labs = VGroup(tx("warehouse club", 15, CLUB, bold=True), tx("supercentre", 15, MASS, bold=True), tx("supermarket", 15, GROCER, bold=True),
                      tx("dollar store", 15, DOLLAR, bold=True))
        for lb, b in zip(labs, boxes):
            lb.next_to(b, DOWN, buff=0.15)
        c = stat_cards([(f"{Fm['cost'][0]:,}", "Costco warehouses", CLUB), (f"{Fm['wmt_us'][0]:,}", "Walmart U.S. stores", MASS),
                        (f"{Fm['kr'][0]:,}", "Kroger supermarkets", GROCER), (f"{Fm['dg'][0]:,}", "Dollar General stores", DOLLAR)],
                       y=-1.9, size=32, span=12.6)
        src = source("Forms 10-K of Costco (fiscal 2026), Walmart (fiscal 2026), Kroger and Dollar General (fiscal 2025)", size=12)
        beat(self,
             "Four formats, drawn roughly to scale. <bookmark mark='a'/> Costco runs "
             f"{Fm['cost'][0]} warehouses, averaging about 148 thousand square feet. <bookmark mark='b'/> Walmart's "
             f"American business runs {Fm['wmt_us'][0]:,} stores, most of them supercentres selling food and everything "
             f"else. <bookmark mark='c'/> Kroger runs {Fm['kr'][0]:,} supermarkets. <bookmark mark='d'/> Dollar General "
             f"runs {Fm['dg'][0]:,} small stores, more than any other retailer in America.",
             base=[boxes, labs, src], steps=[c[0], c[1], c[2], c[3]])

    def per_store(self):
        Fm = R["formats"]
        items = [("a Costco warehouse", 1e3 * Fm["cost"][1] / Fm["cost"][0], CLUB),
                 ("a Walmart U.S. store", 1e3 * Fm["wmt_us"][1] / Fm["wmt_us"][0], MASS),
                 ("a Kroger supermarket", 1e3 * Fm["kr"][1] / Fm["kr"][0], GROCER),
                 ("an Albertsons store", 1e3 * Fm["aci"][1] / Fm["aci"][0], GROCER),
                 ("a Dollar General store", 1e3 * Fm["dg"][1] / Fm["dg"][0], DOLLAR)]
        rows = hbars([(n, v, c, f"${v:,.0f}m") for n, v, c in items], max_value=340, x0=0.6, top=1.8, row=0.8, length=5.4, size=17, bar_h=0.42)
        lab = tx("sales per store a year (company sales over stores, this series' arithmetic)", 16, GREY_A).to_edge(UP, buff=0.8)
        src = source("Forms 10-K of Costco, Walmart, Kroger, Albertsons and Dollar General; SEC company facts", size=12)
        v = [x[1] for x in items]
        beat(self,
             f"What each one sells in a year. <bookmark mark='a'/> An average Costco warehouse, about {v[0]:.0f} million "
             f"dollars. <bookmark mark='b'/> A Walmart supercentre, about {v[1]:.0f} million. <bookmark mark='c'/> A Kroger "
             f"or Albertsons supermarket, {v[2]:.0f} and {v[3]:.0f} million. <bookmark mark='d'/> A Dollar General, about "
             f"{v[4]:.1f} million. The club sells a narrow range of big packs to people who drive in and fill a car; the "
             "dollar store sells small packs to people who drop in on the way home. The supermarket sits between them, and, in "
             "this series' reading, is squeezed from both sides.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1], VGroup(rows[2], rows[3]), rows[4]])

    def per_foot(self):
        Fm = R["formats"]
        cpf = 1e9 * Fm["cost"][1] / (Fm["cost"][2] * 1e6)
        wpf = 1e9 * Fm["wmt_us"][1] / (Fm["wmt_us"][2] * 1e6)
        items = [("Costco: sales per square foot", cpf, CLUB, f"${cpf:,.0f}"), ("Walmart U.S.: sales per square foot", wpf, MASS, f"${wpf:,.0f}")]
        rows = hbars(items, max_value=2400, x0=0.8, top=1.0, row=1.2, length=5.2, size=18, bar_h=0.6)
        lab = tx("a year, this series' arithmetic (Costco: warehouses times their average size)", 16, GREY_A).to_edge(UP, buff=0.8)
        src = source("Costco and Walmart, Forms 10-K for fiscal 2026", size=12)
        beat(self,
             "The best single measure of a shop is what each square foot sells. <bookmark mark='a'/> Costco's warehouses "
             f"sell about {cpf:,.0f} dollars of goods per square foot a year. <bookmark mark='b'/> Walmart's American stores, "
             f"about {wpf:,.0f}. Costco gets about three times as much through each foot of floor by selling fewer items in "
             "bigger packs, stacked to the ceiling on pallets, to members who come to fill a trolley.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1]])

    def dg_money(self):
        Fm = R["formats"]
        M = R["dollar"]["margins"]["Dollar General"]
        c = stat_cards([(f"${1e3 * Fm['dg'][1] / Fm['dg'][0]:.1f}m", "sales per store a year", DOLLAR), (f"{M['gross']:.0f}%", "gross margin", GOOD),
                        (f"{M['net']:.1f}%", "net margin", GOOD)], y=0.4, size=38, span=11)
        src = source("Dollar General, Form 10-K for fiscal 2025, via SEC company facts", size=12)
        beat(self,
             "The small store's economics are different again. <bookmark mark='a'/> A Dollar General sells about "
             f"{1e3 * Fm['dg'][1] / Fm['dg'][0]:.1f} million dollars a year, a sixtieth of a Walmart supercentre. "
             f"<bookmark mark='b'/> But it keeps {M['gross']:.0f} cents of each dollar after paying for the goods, more than "
             f"Walmart; in this series' reading, because shoppers pay for nearness and small packs. <bookmark mark='c'/> After running thousands of "
             f"tiny stores with a handful of staff each, it ends with {M['net']:.1f} cents: much the same as the giants.",
             base=[src], steps=[c[0], c[1], c[2]])

    def dollar_general(self):
        Fm = R["formats"]
        dots = VGroup(*[Dot(radius=0.035, color=DOLLAR).move_to([np.cos(a) * r_, np.sin(a) * r_ * 0.6, 0])
                        for a, r_ in zip(np.linspace(0, 40 * np.pi, 220), np.sqrt(np.linspace(0.02, 1, 220)) * 4.6)]).move_to([0, 0.4, 0])
        q = quote(["'approximately 75% of the U.S. population located within five miles of a Dollar General store'"],
                  "Dollar General, Form 10-K for fiscal 2025", size=18).move_to([0, -2.2, 0])
        src = source("Dollar General, Form 10-K for fiscal 2025", size=12)
        beat(self,
             f"<bookmark mark='a'/> Dollar General's {Fm['dg'][0]:,} stores, in rural, suburban and urban places alike, are "
             "scattered so thickly that it says about three-quarters of Americans live within five miles of one. "
             "<bookmark mark='b'/> In this series' reading, it wins not on price but on the trip saved: the shop that is "
             "closest wins the small, frequent basket.",
             base=[src], steps=[dots, q])
