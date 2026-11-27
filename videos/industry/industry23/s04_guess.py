from __future__ import annotations

from videos.industry.industry23.common import *  # noqa: F403

DAYS_COL = {"Ross": OFF, "TJX": OFF, "Burlington": OFF, "Inditex": FAST, "Urban Outfitters": FAST, "American Eagle": FAST,
            "Abercrombie & Fitch": FAST, "Deckers (HOKA, UGG)": SPORT, "NIKE": SPORT, "Lululemon": SPORT, "Kohl's": DEPT,
            "Macy's": DEPT, "Ralph Lauren": BRANDC, "Levi Strauss": BRANDC, "Tapestry (Coach)": LUX}


class Guess(VoiceoverScene):
    def construct(self):
        card(self, 3, "The buyer's guess", "What does a wrong guess cost, and who pays for it?",
             "Chapter three. The buyer's guess. Every company in this film makes the guess from chapter one, and the "
             "evidence of how well each one guesses is sitting in its warehouses.", lit=("make", "dollar"))
        self.days()
        self.why()
        self.nike()
        self.lulu()
        self.cost()

    def days(self):
        D = R["turns"]["days"]
        items = [(k, v, DAYS_COL.get(k, GREY_B), f"{v:.0f} days") for k, v in sorted(D.items(), key=lambda kv: kv[1])]
        rows = hbars(items, max_value=200, x0=-1.2, top=2.6, row=0.34, length=6.4, size=13, bar_h=0.22)
        key = VGroup(*[VGroup(Dot(radius=0.07, color=c), tx(n, 13, c)).arrange(RIGHT, buff=0.08) for n, c in
                       (("off-price", OFF), ("fast fashion and mall chains", FAST), ("sport", SPORT), ("department stores", DEPT),
                        ("brands", BRANDC), ("luxury", LUX))]).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.75)
        lab = tx("stock at year end, in days of the year's cost of sales", 15, GREY_A).to_edge(UP, buff=0.3)
        src = source("Forms 10-K via SEC company facts (inventory over cost of sales, latest fiscal year); NIKE's Form 10-K "
                     "for fiscal 2026; Inditex, FY2025 results", size=12)
        n = len(items)
        kd, md = D["Kohl's"], D["Macy's"]
        beat(self,
             "How long does stock sit before it sells? One way to see it: take what a company had in its warehouses and "
             "shops at the end of the year, and ask how many days of selling that would cover. <bookmark mark='a'/> The "
             f"fastest are the off-price shops: Ross {D['Ross']:.0f} days, TJX {D['TJX']:.0f}, and then Inditex, "
             f"{D['Inditex']:.0f}. <bookmark mark='b'/> In the middle, NIKE, about {D['NIKE']:.0f} days, and the department "
             f"stores, Kohl's and Macy's, about {kd:.0f} and {md:.0f}. <bookmark mark='c'/> At the slow "
             f"end, the brands that sell things meant to last: Ralph Lauren {D['Ralph Lauren']:.0f} days, Coach's owner "
             f"Tapestry {D['Tapestry (Coach)']:.0f}, Levi's {D['Levi Strauss']:.0f}. Jeans and leather bags are meant to sell "
             "for more than one season, so they can wait longer on the shelf than a fashion top.",
             base=[rows.axis, lab, key, src], steps=[rows[:4], rows[4:n - 4], rows[n - 4:]])

    def why(self):
        U = R["run"]["choices"]
        tags = VGroup(draw.price_tag("$40", 1.2), Arrow(LEFT, RIGHT, buff=0, stroke_color=GREY_B, stroke_width=4),
                      draw.price_tag("$8", 1.2, color=BAD)).arrange(RIGHT, buff=0.3).move_to([0, 1.8, 0])
        items = [("all early", U["far"]["markdown"], FAR, f"{100 * U['far']['markdown']:.0f}%"),
                 ("all late", U["near"]["markdown"], NEAR, f"{100 * U['near']['markdown']:.0f}%"),
                 ("base and chase", U["chase"]["markdown"], CHASE, f"{100 * U['chase']['markdown']:.0f}%")]
        rows = hbars(items, max_value=0.4, x0=-0.6, top=0.2, row=0.8, length=5.6, size=17, bar_h=0.42)
        lab = tx("the full-price value of the order given up in the sale", 15, GREY_A).move_to([0, 0.85, 0])
        est = estimate_tag("the Works' season", size=12)
        beat(self,
             "Why does it matter? Because stock that does not sell ends up in the sale. <bookmark mark='a'/> Every shirt "
             "that drops from forty dollars to eight gives up thirty-two dollars of what the buyer hoped to earn. "
             f"<bookmark mark='b'/> In the Works' season, buying everything early gives up {100 * U['far']['markdown']:.0f} "
             "per cent of the order's full-price value in the sale; <bookmark mark='c'/> buying late, "
             f"{100 * U['near']['markdown']:.0f}; <bookmark mark='d'/> the chase, {100 * U['chase']['markdown']:.0f}. "
             "Markdowns are where a wrong guess shows up in the accounts: not as a cost line of their own, but as a lower "
             "gross margin.",
             base=[est, lab], steps=[tags, rows[0], rows[1], rows[2]])

    def nike(self):
        B = R["brands"]
        q = quote(["'Repositioning NIKE Brand Digital as a full-price platform and reinvesting in wholesale",
                   "distribution. This includes liquidating inventory through increased markdowns across NIKE Direct,",
                   "and higher sales returns and discounts with our wholesale partners to reduce inventory and",
                   "create capacity for new product.'"], "NIKE, Inc., Form 10-K for fiscal 2026", size=17).move_to([0, 1.5, 0])
        items = [(f"FY{y % 100}", B["gm"][y], SPORT if y == 2024 else BAD, f"{B['gm'][y]:.1f}%") for y in (2024, 2025, 2026)]
        bars_ = vbars([(a, v - 40, c, t) for a, v, c, t in items], base_y=-2.6, height=2.6, width=1.1, gap=0.6, size=17, max_value=5.5)
        floor = tx("NIKE's gross margin (bars start at 40%)", 14, GREY_A).move_to([4.2, -1.6, 0])
        src = source("NIKE, Inc., Form 10-K for fiscal 2026", size=12)
        beat(self,
             "Even the biggest brand gets it wrong. <bookmark mark='a'/> In its 2026 report NIKE describes clearing out "
             "stock: marking it down in its own shops and on its own website, and taking back goods and giving discounts to "
             "the shops that stock it, to make room for new products. <bookmark mark='b'/> Its gross margin fell from "
             f"{B['gm'][2024]} per cent in fiscal 2024 to {B['gm'][2025]} in fiscal 2025, and was {B['gm'][2026]} in 2026, "
             f"and that despite a {B['ieepa'] / 1e3:.2f} billion dollar credit for tariffs it expects to get back, booked "
             "against its costs that year.",
             base=[src, floor], steps=[q, bars_])

    def lulu(self):
        B = R["brands"]
        a, b = B["lulu"]
        items = [("fiscal 2024", a, SPORT, f"{a:.1f}%"), ("fiscal 2025", b, BAD, f"{b:.1f}%")]
        rows = hbars(items, max_value=62, x0=-0.6, top=1.0, row=1.0, length=5.6, size=18, bar_h=0.5)
        note = tx("-2.4 points: 'primarily from higher tariffs, as well as increased markdowns'", 18, BAD, bold=True).move_to([0, -1.4, 0])
        lab = tx("Lululemon's gross margin", 16, GREY_A).move_to([0, 2.0, 0])
        src = source("lululemon athletica inc., Form 10-K for fiscal 2025", size=12)
        beat(self,
             f"Lululemon, the yoga-wear brand, keeps more than most. <bookmark mark='a'/> Its gross margin was {a} per cent "
             f"in fiscal 2024; <bookmark mark='b'/> in fiscal 2025, {b}. <bookmark mark='c'/> Its report puts 2.4 points of "
             "the fall down mainly to higher American tariffs, and to more markdowns. Its sales in mainland China grew "
             f"{B['lulu_china']} per cent that year while its American sales shrank, with fewer visits to its shops there and "
             "fewer visits ending in a sale.",
             base=[lab, src], steps=[rows[0], rows[1], note])

    def cost(self):
        F = R["fast"]
        D = R["turns"]["days"]
        c = stat_cards([(f"{D['Inditex']:.0f} days", "Inditex: stock against the year's cost of sales", FAST),
                        (f"{D['NIKE']:.0f} days", "NIKE", SPORT),
                        (f"{D['Tapestry (Coach)']:.0f} days", "Tapestry (Coach)", LUX)], y=1.0, size=40, span=12)
        note = VGroup(tx("Three ways to live with the guess:", 22, WHITE, bold=True),
                      tx("guess less (fast fashion); sell the mistakes (off-price); make too few to have any (luxury)", 18, GREY_A)
                      ).arrange(DOWN, buff=0.2).move_to([0, -1.4, 0])
        src = source("Inditex, FY2025 results; NIKE, Inc., Form 10-K for fiscal 2026; Tapestry via SEC company facts", size=12)
        beat(self,
             "So the guess costs everyone something. <bookmark mark='a'/> Inditex holds about "
             f"{D['Inditex']:.0f} days of stock, <bookmark mark='b'/> NIKE about {D['NIKE']:.0f}, <bookmark mark='c'/> and "
             f"Coach's owner {D['Tapestry (Coach)']:.0f}. <bookmark mark='d'/> The next three chapters take the three "
             "answers in turn: guess less, by making fast and close; sell the mistakes, by buying other people's leftovers; "
             "and make too few to have any, the luxury house's answer, which we come to after the sports brands.",
             base=[src], steps=[c[0], c[1], c[2], note])
