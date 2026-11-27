from __future__ import annotations

from videos.industry.industry23.common import *  # noqa: F403

CONCEPT = {"zara": "Zara, Zara Home, Lefties", "bershka": "Bershka", "stradivarius": "Stradivarius", "pullbear": "Pull&Bear",
           "massimo": "Massimo Dutti", "oysho": "Oysho"}


class Fast(VoiceoverScene):
    def construct(self):
        card(self, 4, "Fast fashion", "How does Inditex guess less?",
             "Chapter four. Fast fashion. The first answer to the buyer's problem is to make the guess smaller: buy less "
             "before the season, and make more of what sells while it is still selling.", lit=("make", "moat"))
        self.concepts()
        self.model()
        self.cash()
        self.profit()
        self.half()

    def concepts(self):
        F = R["fast"]
        items = [(CONCEPT[k], v / 1e3, FAST if k == "zara" else GREY_B, f"€{v / 1e3:.1f}bn") for k, v in F["concepts"].items()]
        rows = hbars(items, max_value=30, x0=-0.6, top=1.8, row=0.62, length=6.6, size=17, bar_h=0.38)
        lab = tx("Inditex's sales by chain, the year to January 2026", 16, GREY_A).to_edge(UP, buff=0.8)
        src = source("Inditex, FY2025 results: net sales by concept", size=12)
        z = F["concepts"]["zara"] / 1e3
        beat(self,
             f"Inditex runs {get('itx.formats')} chains of shops, and one of them is most of the business. <bookmark mark='a'/> Zara, with "
             f"Zara Home and the cheaper Lefties, sold {z:.1f} billion euros of the group's {R['hook']['sales']:.1f} "
             f"billion: {100 * z / R['hook']['sales']:.0f} per cent. <bookmark mark='b'/> The others, Bershka, Stradivarius, "
             "Pull and Bear, Massimo Dutti and the lingerie chain Oysho, are each one to three billion. The group is "
             f"Spanish, and two thirds of what it sells is sold in Europe: {get('itx.spain')} per cent in Spain and "
             f"{get('itx.europe')} per cent in the rest of Europe, close to where it can make clothes quickly.",
             base=[rows.axis, lab, src], steps=[rows[:1], rows[1:]])

    def model(self):
        q = quote(["'The business model we enjoy, characterised by flexibility, responsiveness",
                   "and within-season proximity sourcing, permits us to react to fashion trends'"],
                  "Inditex, FY2025 results", size=20).move_to([0, 2.2, 0])
        far = VGroup(draw.ship(1.6) if hasattr(draw, "ship") else Square(), tx("far: cheap, ordered early, on a forecast", 16, FAR)
                     ).arrange(DOWN, buff=0.15).move_to([-3.6, -0.3, 0])
        near = VGroup(draw.truck(1.6) if hasattr(draw, "truck") else Square(), tx("near: dearer, ordered once the season shows", 16, NEAR)
                      ).arrange(DOWN, buff=0.15).move_to([3.6, -0.3, 0])
        rule = tx("the base from far away, the hits from nearby: the chase from chapter one", 19, CHASE, bold=True).move_to([0, -2.2, 0])
        src = source("Inditex, FY2025 results", size=12)
        beat(self,
             "Inditex describes its own model in one sentence. <bookmark mark='a'/> 'Flexibility, responsiveness and "
             "within-season proximity sourcing': making part of each season close to home, during the season. "
             "<bookmark mark='b'/> Clothes made far away are cheaper, but must be ordered months ahead, on a forecast. "
             "<bookmark mark='c'/> Clothes made nearby cost more, but can be ordered once the first weeks have shown what "
             "is selling. <bookmark mark='d'/> Do both, and you have the chase from chapter one: a base bought early and "
             "cheaply, and the hits made again, quickly, close to the shops.",
             base=[src], steps=[q, far, near, rule])

    def cash(self):
        F = R["fast"]
        s = 0.55
        inv = Rectangle(width=1.6, height=F["inventory"] * s, stroke_width=0, fill_color=FAST, fill_opacity=0.9)
        rec = Rectangle(width=1.6, height=F["receivables"] * s, stroke_width=0, fill_color=GOOD, fill_opacity=0.9)
        hold = VGroup(inv, rec).arrange(UP, buff=0).move_to([-2.0, -2.4, 0], aligned_edge=DOWN)
        pay = Rectangle(width=1.6, height=F["payables"] * s, stroke_width=0, fill_color=BAD, fill_opacity=0.9).move_to([1.2, -2.4, 0], aligned_edge=DOWN)
        l1 = VGroup(tx(f"stock €{F['inventory']:.2f}bn", 15, FAST, bold=True).next_to(inv, LEFT, buff=0.15),
                    tx(f"owed by customers €{F['receivables']:.2f}bn", 15, GOOD, bold=True).next_to(rec, LEFT, buff=0.15))
        l2 = tx(f"owed to suppliers and others €{F['payables']:.2f}bn", 15, BAD, bold=True).next_to(pay, RIGHT, buff=0.15)
        diff = tx(f"€{-F['owc']:.1f}bn more owed than tied up", 22, PRICE, bold=True).move_to([0, 2.6, 0])
        src = source("Inditex, FY2025 results: operating working capital at 31 January 2026", size=12)
        beat(self,
             "Speed also changes where the money sits. <bookmark mark='a'/> At the end of January 2026 Inditex had "
             f"{F['inventory']:.1f} billion euros of clothes in its shops and warehouses, and was owed about "
             f"{F['receivables']:.1f} billion. <bookmark mark='b'/> But it owed its suppliers and others "
             f"{F['payables']:.1f} billion. <bookmark mark='c'/> The difference, {-F['owc']:.1f} billion euros, is money "
             "the business does not have to find: customers pay at the till, and the bills to suppliers fall due later. "
             "A company whose stock turns in about seventy days, and which pays later than that, is in effect lent its "
             "working money by the people it buys from.",
             base=[src], steps=[[hold, l1], [pay, l2], diff])

    def profit(self):
        F = R["fast"]
        c = stat_cards([(f"{R['hook']['gm']}%", "gross margin: kept after the cost of the clothes", FAST),
                        (f"{F['ebit_margin']}%", "operating margin, after shops, staff and logistics", PRICE),
                        (f"€{F['net']:.1f}bn", "net income, the year to January 2026", GOOD)], y=0.9, size=40, span=12)
        stores = tx(f"{R['hook']['stores']:,} shops in {R['hook']['markets']} markets; selling space to grow about "
                    f"{F['space']}% in 2026", 18, GREY_A).move_to([0, -1.2, 0])
        src = source("Inditex, FY2025 results", size=12)
        beat(self,
             "And it pays. <bookmark mark='a'/> In the year to January 2026 Inditex kept "
             f"{R['hook']['gm']} per cent of its sales after the cost of the clothes, <bookmark mark='b'/> "
             f"{F['ebit_margin']} per cent after running its shops, paying its staff and moving the clothes, "
             f"<bookmark mark='c'/> and made {F['net']:.1f} billion euros of net income. <bookmark mark='d'/> It did that "
             f"from {R['hook']['stores']:,} shops and online, and expected its selling space to grow by about "
             f"{F['space']} per cent in 2026: still opening, in a trade it calls highly fragmented.",
             base=[src], steps=[c[0], c[1], c[2], stores])

    def half(self):
        F = R["fast"]
        (s1, g1), (s0, g0) = F["h1"], F["h1_prev"]
        items = [("first half of 2025", s0, GREY_B, f"€{s0:.1f}bn, margin {g0}%"),
                 ("first half of 2026", s1, FAST, f"€{s1:.1f}bn, margin {g1}%")]
        rows = hbars(items, max_value=22, x0=-0.4, top=0.9, row=1.1, length=5.4, size=18, bar_h=0.55)
        note = tx(f"sales +{100 * (s1 / s0 - 1):.1f}%; gross margin +{100 * (g1 - g0):.0f} basis points", 20, GOOD, bold=True).move_to([0, -1.6, 0])
        src = source("Inditex, interim 1H2026 results (1 February to 31 July 2026)", size=12)
        beat(self,
             "The latest half-year. <bookmark mark='a'/> From February to July 2025 Inditex sold "
             f"{s0:.1f} billion euros at a gross margin of {g0} per cent. <bookmark mark='b'/> In the same months of 2026, "
             f"{s1:.1f} billion, at {g1} per cent. <bookmark mark='c'/> Sales up {100 * (s1 / s0 - 1):.1f} per cent, "
             f"{get('itx.h1.cc')} per cent at constant exchange rates, "
             "and the margin a little higher. Chapter eleven makes a forecast out of that margin.",
             base=[src], steps=[rows[0], rows[1], note])
