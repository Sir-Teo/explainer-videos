from __future__ import annotations

from videos.industry.industry31.common import *  # noqa: F403


class Club(VoiceoverScene):
    def construct(self):
        card(self, 5, "Paying to shop", "Why do 84 million households pay Costco for the right to shop there?",
             "Chapter five. Paying to shop. The warehouse club turns the retailer's thin margin inside out: sell the goods "
             "at nearly cost, and charge for the door.", lit=("moat", "dollar"))
        self.members()
        self.split()
        self.executive()
        self.renew()
        self.others()

    def members(self):
        C = R["club"]
        a, b, c = C["members"]
        items = [("2024", a, ALL, f"{a:.1f}m"), ("2025", b, ALL, f"{b:.1f}m"), ("2026", c, CLUB, f"{c:.1f}m")]
        cols = vbars(items, base_y=-2.0, height=3.6, width=1.6, gap=0.8, size=18, max_value=90)
        lab = tx("Costco's paid members at the end of each fiscal year", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Costco Wholesale, Form 10-K for fiscal 2026", size=12)
        beat(self,
             f"<bookmark mark='a'/> Costco had {a:.1f} million paid members at the end of its 2024 year, "
             f"<bookmark mark='b'/> {b:.1f} million a year later, <bookmark mark='c'/> and {c:.1f} million in 2026, each "
             "paying an annual fee for a card that opens the warehouse door, with more cards for the household on top.",
             base=[lab, src], steps=[cols[0], cols[1], cols[2]])

    def split(self):
        C = R["club"]
        parts = [("merchandise, sold at an 11% gross margin", (C["op"] - C["fees"]) / C["op"], GOODS), ("membership fees", C["fees"] / C["op"], CLUB)]
        bar = viz.bar_split(parts, 1.0, width=12.0, height=0.9).move_to([0, 0.6, 0])
        labs = VGroup(*[VGroup(tx(f"{100 * v:.0f}%", 22, c, bold=True), tx(n, 14, GREY_A)).arrange(DOWN, buff=0.06).next_to(bar[i], DOWN, buff=0.2)
                        for i, (n, v, c) in enumerate(parts)])
        hd = tx(f"Costco's ${C['op']:.1f}bn of operating income, fiscal 2026: where it came from (this series' split)", 19, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("Costco Wholesale, Form 10-K for fiscal 2026; SEC company facts", size=12)
        beat(self,
             f"Split Costco's {C['op']:.1f} billion dollars of operating income in two. <bookmark mark='a'/> On "
             f"{C['sales']:.0f} billion dollars of goods it kept about {C['merch_margin']:.0f} cents in the dollar before "
             "running the warehouses, far less than a supermarket, and after running them the goods contributed only about "
             f"{100 * parts[0][1]:.0f} per cent of the profit. <bookmark mark='b'/> The membership fees, "
             f"{C['fees']:.1f} billion dollars with almost no cost attached, made up the other {100 * parts[1][1]:.0f} per "
             "cent. Costco is, in this series' reading, a subscription business that happens to sell groceries.",
             base=[hd, src], steps=[VGroup(bar[0], labs[0]), VGroup(bar[1], labs[1])])

    def executive(self):
        c = stat_cards([(f"${get('co31.fee'):.0f}", "a year for a basic US membership", CLUB),
                        (f"{get('co31.exec'):.1f}m", "Executive members, who pay more for a 2% reward", GOOD),
                        ("75.2%", "of Costco's sales are to them", MASS)], y=0.6, size=38, span=12)
        cards = VGroup(*[RoundedRectangle(corner_radius=0.08, width=1.5, height=0.95, stroke_width=0, fill_color=c, fill_opacity=0.9)
                         for c in (CLUB, CLUB, GOOD, GOOD, GOOD)]).arrange(RIGHT, buff=0.3).move_to([0, -1.8, 0])
        src = source("Costco Wholesale, Form 10-K for fiscal 2026", size=12)
        beat(self,
             f"<bookmark mark='a'/> A basic American membership costs {get('co31.fee'):.0f} dollars a year, with a free card "
             f"for the household. <bookmark mark='b'/> {get('co31.exec'):.1f} million members pay extra for an Executive "
             "membership, which earns them 'generally' two per cent back on what they buy. <bookmark mark='c'/> Those "
             "members bought about three-quarters of everything Costco sold. The reward is a reason to buy more at Costco, "
             "and a reason not to let the card lapse.",
             base=[cards, src], steps=[c[0], c[1], c[2]])

    def others(self):
        M = R["dollar"]["margins"]
        items = [("Costco", M["Costco"]["net"], CLUB, f"{M['Costco']['net']:.1f}c"), ("BJ's", M["BJ's"]["net"], CLUB, f"{M['BJ' + chr(39) + 's']['net']:.1f}c"),
                 ("Walmart", M["Walmart"]["net"], MASS, f"{M['Walmart']['net']:.1f}c"), ("Kroger", M["Kroger"]["net"], GROCER, f"{M['Kroger']['net']:.1f}c")]
        rows = hbars(items, max_value=4, x0=0.4, top=1.6, row=0.85, length=5.4, size=17, bar_h=0.42)
        lab = tx("net profit per dollar of revenue, latest fiscal year", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Forms 10-K via SEC company facts", size=12)
        beat(self,
             "Does the model work for anyone else? <bookmark mark='a'/> BJ's, a smaller warehouse club, "
             f"kept {M['BJ' + chr(39) + 's']['net']:.1f} cents per dollar in its latest year, close to Costco's "
             f"{M['Costco']['net']:.1f}. <bookmark mark='b'/> Walmart kept {M['Walmart']['net']:.1f} and Kroger "
             f"{M['Kroger']['net']:.1f}. Charging at the door does not make the margin fat; it makes it steady, because the "
             "fee arrives whether or not the members buy a television that year.",
             base=[rows.axis, lab, src], steps=[VGroup(*rows[:2]), VGroup(*rows[2:])])

    def renew(self):
        C = R["club"]
        c = stat_cards([(f"{C['renew']:.1f}%", "renew in the US and Canada", CLUB), (f"{C['renew_ww']:.1f}%", "renew worldwide", ALL),
                        ("Kirkland", "its own label, 'generally' higher-margin", GOODS)], y=0.6, size=38, span=12)
        cartg = VGroup(*[draw.cart(0.9, color=CLUB) for _ in range(6)]).arrange(RIGHT, buff=0.3).move_to([0, -1.8, 0])
        src = source("Costco Wholesale, Form 10-K for fiscal 2026", size=12)
        beat(self,
             f"<bookmark mark='a'/> And the members come back: {C['renew']:.1f} per cent renewed in the United States and "
             f"Canada, <bookmark mark='b'/> {C['renew_ww']:.1f} per cent worldwide. <bookmark mark='c'/> Its own label, "
             "Kirkland Signature, carries 'generally' higher margins than the national brands, Costco says. Low prices "
             "keep members renewing; renewals pay the profit; and the profit lets the prices stay low. In this series' "
             "reading, it is a loop rivals find very hard to break into, because copying it means years of selling at cost "
             "before enough members arrive to pay for the warehouses.",
             base=[cartg, src], steps=[c[0], c[1], c[2]])
