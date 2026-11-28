from __future__ import annotations

from videos.industry.industry32.common import *  # noqa: F403


class Direct(VoiceoverScene):
    def construct(self):
        card(self, 8, "Buying customers", "What does it cost to sell online when you have no marketplace of your own?",
             "Chapter eight. Buying customers. A brand that sells only from its own website has no shop window on a high "
             "street. Every customer has to be found, usually by paying an advertising platform to find them.", lit=("dollar", "moat"))
        self.maths()
        self.cohort()
        self.share()
        self.brands()
        self.lesson()

    def maths(self):
        D = R["direct"]
        c = stat_cards([(f"${D['first']:.0f}", "the first order", BRAND), (f"{100 * D['margin']:.0f}%", "kept after goods, postage, returns", GOOD),
                        ("$60", "paid to ads to win the customer", ADS), (f"{100 * D['retention']:.0f}%", "still buying a year later", SHOP)],
                        y=0.6, size=36, span=12.6)
        ph = draw.phone(1.3, screen=ADS).move_to([0, -1.9, 0])
        tag = estimate_tag("the Works: a direct brand (this series' assumptions)", size=12)
        beat(self,
             "Here is the arithmetic of a direct brand in the Works. <bookmark mark='a'/> A new customer's first order is "
             f"{D['first']:.0f} dollars. <bookmark mark='b'/> After the goods, the postage and the returns, the brand keeps "
             f"{100 * D['margin']:.0f} per cent of it, {D['first'] * D['margin']:.0f} dollars. <bookmark mark='c'/> But "
             "it paid sixty dollars in ads to win that customer, so the first order loses money. <bookmark mark='d'/> The "
             f"bet is on what comes next: {100 * D['retention']:.0f} per cent of customers buy again the following year, "
             f"spending {D['repeat']:.0f} dollars, and fewer each year after.",
             base=[ph, tag], steps=[c[0], c[1], c[2], c[3]])

    def cohort(self):
        D = R["direct"]
        ser = {f"${c:.0f} a customer": ({y: v for y, v in enumerate(D["cac"][c])}, col)
               for c, col in ((30.0, GOOD), (60.0, MARKET), (90.0, BAD))}
        ch = line_chart(ser, x=(0, 5), y=(-60, 50), xticks=[0, 1, 2, 3, 4, 5], yticks=[-60, -40, -20, 0, 20, 40],
                        xfmt=lambda v: f"year {v:.0f}", yfmt=lambda v: f"${v:.0f}",
                        ylabel="the Works: a customer's cumulative profit after the cost of winning them", width=8.4, height=4.3,
                        center=(-1.4, -0.45), nudge={"$60 a customer": 0.1})
        zero = DashedLine(ch.ax.c2p(0, 0), ch.ax.c2p(5, 0), color=GREY_B)
        L = D["life"]
        tag = estimate_tag("the Works: a direct brand with 40% retention", size=12)
        beat(self,
             f"<bookmark mark='a'/> If ads cost thirty dollars a customer, the brand is ahead from the first order and each "
             f"customer is worth {L[30.0]:.0f} dollars over a lifetime. <bookmark mark='b'/> At sixty dollars, it takes two "
             f"years to earn the cost back, and a customer is worth only {L[60.0]:.0f}. <bookmark mark='c'/> At ninety, it "
             f"never does: every customer loses {abs(L[90.0]):.0f} dollars, and growing faster means losing faster. A direct "
             "brand's whole business rests on the price of an advertising click, which is set by someone else's auction.",
             base=[ch.frame, zero, tag], steps=[VGroup(ch.lines["$30 a customer"], ch.labels["$30 a customer"]),
                                               VGroup(ch.lines["$60 a customer"], ch.labels["$60 a customer"]),
                                               VGroup(ch.lines["$90 a customer"], ch.labels["$90 a customer"])])

    def share(self):
        S = R["direct"]["mkt_share"]
        order = sorted(S, key=lambda k: -S[k])
        col = {"Allbirds": BRAND, "Warby Parker": BRAND, "FIGS": BRAND, "Revolve": SHOP, "Wayfair": SHOP, "Chewy": SHOP,
               "Etsy": MARKET, "eBay": MARKET}
        items = [(k, S[k], col.get(k, ALL), f"{S[k]:.0f}%") for k in order]
        rows = hbars(items, max_value=35, x0=-0.4, top=2.2, row=0.62, length=6.2, size=17, bar_h=0.38)
        hd = tx("Marketing as a share of revenue, latest year", 21, WHITE, bold=True).to_edge(UP, buff=0.5)
        note = tx("selling and marketing, or marketing, expense as each company reports it", 14, GREY_B).to_edge(DOWN, buff=0.75)
        src = source("Forms 10-K via SEC company facts", size=12)
        beat(self,
             "The real companies show the same pressure. <bookmark mark='a'/> The marketplaces spend heavily to bring "
             f"buyers in: Etsy {S['Etsy']:.0f} per cent of its revenue, part of it paying other sites to show its sellers' "
             f"goods, and eBay {S['eBay']:.0f}. <bookmark mark='b'/> Allbirds, the shoe brand, {S['Allbirds']:.0f} per "
             f"cent. <bookmark mark='c'/> FIGS, Revolve and Warby Parker between twelve and fifteen. <bookmark mark='d'/> "
             f"And at the bottom, Chewy, at {S['Chewy']:.1f} per cent: most of its sales come from customers on Autoship.",
             base=[rows.axis, hd, note, src], steps=[VGroup(*[r for r, k in zip(rows, order) if k in ("Etsy", "eBay")]),
                                                     VGroup(*[r for r, k in zip(rows, order) if k == "Allbirds"]),
                                                     VGroup(*[r for r, k in zip(rows, order) if k in ("FIGS", "Revolve", "Warby Parker", "Wayfair")]),
                                                     VGroup(*[r for r, k in zip(rows, order) if k == "Chewy"])])

    def brands(self):
        B = R["direct"]["brands"]
        ser = {"Allbirds": ({y: v * 1e3 for y, v in B["BIRD"].items()}, BRAND), "Warby Parker": ({y: v * 1e3 for y, v in B["WRBY"].items()}, SHOP),
               "FIGS": ({y: v * 1e3 for y, v in B["FIGS"].items()}, GOOD)}
        ch = line_chart(ser, x=(2019, 2025), y=(0, 900), xticks=[2019, 2020, 2021, 2022, 2023, 2024, 2025], yticks=[0, 300, 600, 900],
                        yfmt=lambda v: f"${v:.0f}m", ylabel="revenue, $m a year", width=8.4, height=4.3, center=(-1.4, -0.45),
                        nudge={"FIGS": -0.15})
        a = B["BIRD"]
        pk = max(a, key=a.get)
        src = source("Allbirds, Warby Parker and FIGS, Forms 10-K via SEC company facts", size=12)
        beat(self,
             f"<bookmark mark='a'/> Allbirds' revenue peaked at {a[pk] * 1e3:.0f} million dollars in {pk} and fell to "
             f"{a[max(a)] * 1e3:.0f} million in {max(a)}; it has lost money every year since it listed. "
             f"<bookmark mark='b'/> Warby Parker, selling glasses, kept growing, to "
             f"{B['WRBY'][max(B['WRBY'])] * 1e3:.0f} million. <bookmark mark='c'/> FIGS, selling medical scrubs, has made a "
             "profit in most years. In this series' reading, the brands that lasted found customers who return without "
             "being bought twice.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["Allbirds"], ch.labels["Allbirds"]),
                                         VGroup(ch.lines["Warby Parker"], ch.labels["Warby Parker"]),
                                         VGroup(ch.lines["FIGS"], ch.labels["FIGS"])])

    def lesson(self):
        g = VGroup(tx("Buying customers", 22, WHITE, bold=True),
                   tx("a direct brand rents its shop window from an ad platform, by the click", 18, ADS),
                   tx("it pays off only if customers come back without being bought again", 18, GOOD),
                   tx("so subscriptions, habits and physical shops are worth more than they look", 18, SHOP)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "In this series' reading: <bookmark mark='a'/> a brand that sells only online rents its shop window from "
             "an advertising platform, by the click. <bookmark mark='b'/> It works only if customers come back on their "
             "own. <bookmark mark='c'/> So the dull things, a subscription, a habit, a shop on a real street, are worth more "
             "than they look. The marketplaces win both ways: they sell the ads and they own the habit.",
             base=[tag], steps=[g[:2], g[2], g[3]])
