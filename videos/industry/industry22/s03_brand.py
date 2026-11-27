from __future__ import annotations

from videos.industry.industry22.common import *  # noqa: F403


class Brand(VoiceoverScene):
    def construct(self):
        card(self, 2, "What a brand is worth", "Where does a dollar of soap go?",
             "Chapter two. What a brand is worth. Follow a dollar spent on Procter and Gamble's products, and see how little "
             "of it is the factory. A brand is a promise a shopper can trust without checking, and the company is paid for "
             "keeping that promise.", lit=("dollar", "moat"))
        self.dollar()
        self.research()
        self.margins()

    def dollar(self):
        D = R["dollar"]
        parts = [("making and shipping", D["make"], STORE), ("advertising", D["ads"], ADS),
                 ("selling, research, running the company", D["other"], "#9AA3B2"), ("operating profit", D["op"], GOOD)]
        bar = viz.bar_split([(n, v, c) for n, v, c in parts], 1.0, width=12.0, height=0.9).move_to([0, 0.7, 0])
        labs = VGroup()
        for i, (n, v, c) in enumerate(parts):
            t = VGroup(tx(f"{100 * v:.0f}c", 24, c, bold=True), tx(n, 13, GREY_A)).arrange(DOWN, buff=0.06)
            if t.width > bar[i].width + 0.3:
                t.scale_to_fit_width(bar[i].width + 0.3)
            t.next_to(bar[i], DOWN, buff=0.25)
            labs.add(t)
        net = tx(f"after interest and tax: {100 * D['net']:.0f}c of net profit", 18, GOOD, bold=True).move_to([0, -1.9, 0])
        jug = draw.detergent(1.0).move_to([-5.6, 2.4, 0])
        src = source("The Procter & Gamble Company, Form 10-K for fiscal 2026: gross margin, advertising, operating margin, net "
                     "earnings", size=12)
        beat(self,
             "Take a dollar of P&G's sales in fiscal 2026. <bookmark mark='a'/> About "
             f"{100 * D['make']:.0f} cents paid for making the product and getting it to the shop: materials, factories, "
             f"freight. <bookmark mark='b'/> {100 * D['ads']:.0f} cents went on advertising. <bookmark mark='c'/> "
             f"{100 * D['other']:.0f} cents on everything else it takes to sell and run the business, research included. "
             f"<bookmark mark='d'/> And {100 * D['op']:.0f} cents was operating profit, {100 * D['net']:.0f} after interest "
             "and tax. Half the price is the product; the other half is the brand, and what it costs to keep it.",
             base=[jug, src], steps=[[bar[0], labs[0]], [bar[1], labs[1]], [bar[2], labs[2]], [bar[3], labs[3], net]])

    def research(self):
        E = R["extra"]
        items = [("advertising", E["ads"], ADS, f"${E['ads']:.1f}bn"), ("research and development", E["rnd"], GOOD, f"${E['rnd']:.1f}bn")]
        rows = hbars(items, max_value=11, x0=-0.4, top=1.2, row=1.1, length=6.2, size=19, bar_h=0.55)
        brands = VGroup(tx("Tide, Ariel, Pampers, Gillette, Crest, Oral-B, Head & Shoulders, Pantene,", 16, BRAND),
                        tx("Olay, SK-II, Always, Charmin, Bounty, Dawn, Febreze, Vicks ...", 16, BRAND)).arrange(DOWN, buff=0.08).move_to([0, -1.6, 0])
        src = source("The Procter & Gamble Company, Form 10-K for fiscal 2026: advertising and research costs; major brands", size=12)
        beat(self,
             "Compare the two ways P&G spends on the future. <bookmark mark='a'/> On advertising, "
             f"{E['ads']:.1f} billion dollars in fiscal 2026. <bookmark mark='b'/> On research and development, "
             f"{E['rnd']:.1f} billion, about a fifth as much. <bookmark mark='c'/> The company does invent: new detergents, "
             "new razors, new nappies. But most of what it spends on keeping its premium goes on making sure shoppers "
             "remember the names, many of them decades old.",
             base=[rows.axis, src], steps=[rows[0], rows[1], brands])

    def margins(self):
        G = R["margins"]["gm"]
        items = [(k, v, BAD if k in ("Philip Morris International",) else DRINK if k in ("Coca-Cola", "Monster", "PepsiCo", "Brown-Forman", "Coca-Cola Consolidated")
                  else BRAND if k in ("Colgate-Palmolive", "Procter & Gamble", "Church & Dwight", "Clorox", "Kimberly-Clark") else GOOD,
                  f"{100 * v:.0f}%") for k, v in sorted(G.items(), key=lambda kv: -kv[1])]
        rows = hbars(items, max_value=0.75, x0=-0.4, top=2.4, row=0.36, length=6.2, size=14, bar_h=0.24)
        lab = tx("gross margin, latest fiscal year: what is left of a dollar of sales after making and shipping", 15, GREY_A).to_edge(UP, buff=0.55)
        src = source("Forms 10-K via SEC company facts: revenue and cost of sales", size=12)
        top, bot = items[0], items[-1]
        beat(self,
             "Across the industry the gap varies with what is being sold. <bookmark mark='a'/> Philip Morris International "
             f"and Coca-Cola keep {100 * G['Philip Morris International']:.0f} and {100 * G['Coca-Cola']:.0f} cents of each "
             "dollar after the cost of what they sell. <bookmark mark='b'/> Colgate keeps "
             f"{100 * G['Colgate-Palmolive']:.0f}, P&G {100 * G['Procter & Gamble']:.0f}. <bookmark mark='c'/> Food makers, "
             f"whose ingredients are a bigger share of the price, keep less: Hershey {100 * G['Hershey']:.0f}, Mondelez "
             f"{100 * G['Mondelez']:.0f}. And Coca-Cola Consolidated, a bottler that fills and delivers Coca-Cola's drinks "
             f"in parts of America, keeps {100 * G['Coca-Cola Consolidated']:.0f}, against Coca-Cola's {100 * G['Coca-Cola']:.0f}. "
             "The more of the price that is the name, and the less that is the stuff, the wider the gap.",
             base=[rows.axis, lab, src], steps=[VGroup(*rows[:2]), VGroup(*rows[2:6]), VGroup(*rows[6:])])
