from __future__ import annotations

from videos.industry.industry22.common import *  # noqa: F403

OFFSET = {"Procter & Gamble": UP, "PepsiCo": DOWN, "Coca-Cola": UP, "AB InBev": DOWN, "Mondelez": UP, "Altria": UP,
          "Philip Morris International": DOWN, "Monster": UP, "Brown-Forman": UP, "Church & Dwight": UP, "Hershey": UP,
          "Constellation": DOWN}
CALLOUT = {"Colgate-Palmolive": (1.45, 0.16), "Keurig Dr Pepper": (1.3, 0.205), "General Mills": (1.45, 0.085),
           "Kimberly-Clark": (1.42, 0.05), "Estee Lauder": (1.24, -0.025), "Clorox": (0.66, 0.045),
           "Coca-Cola Consolidated": (0.78, 0.01), "Campbell's": (0.9, 0.035), "Conagra": (1.1, 0.035)}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 9, "The landscape, November 2026", "Who sells the world's everyday brands, and who keeps the most?",
             "Chapter nine. The landscape, as of November 2026. Who sells the everyday brands, and who keeps the most of "
             "what they charge?", lit=("moat", "change"))
        self.scatter()
        self.admargin()
        self.map()

    def scatter(self):
        C = R["landscape"]["companies"]
        lx = np.log10
        pa = viz.plot_axes([0.5, 2.05], [-0.05, 0.35], x_length=10.0, y_length=4.9, xticks=[np.log10(5), 1, np.log10(30), 2],
                           yticks=[0, 0.1, 0.2, 0.3], xfmt=lambda v: f"${10 ** v:.0f}bn", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="net income per dollar of revenue, median of 2021-2025", size=13).move_to([-0.3, -0.5, 0])
        zero = DashedLine(pa.ax.c2p(0.5, 0), pa.ax.c2p(2.05, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        xl = tx("revenue, latest fiscal year (log scale)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        groups: dict = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            r = 0.05 + 0.03 * np.sqrt(c["rev"] / 10)
            if c["name"] in CALLOUT:
                groups.setdefault(c["group"], VGroup()).add(callout(pa.ax, lx(c["rev"]), c["margin"], c["name"], col,
                                                                    CALLOUT[c["name"]], size=12, radius=r))
                continue
            d = Dot(pa.ax.c2p(lx(c["rev"]), c["margin"]), radius=r, color=col, fill_opacity=0.85)
            lab = tx(c["name"], 12, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.06)
            groups.setdefault(c["group"], VGroup()).add(VGroup(d, lab))
        key = VGroup(*[VGroup(Dot(radius=0.08, color=GROUP_COL[g]), tx(n, 13, GROUP_COL[g])).arrange(RIGHT, buff=0.08)
                       for g, n in (("home", "home and personal care"), ("food", "food"), ("drink", "drinks"),
                                    ("tobacco", "tobacco"))]).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.95)
        hd = tx("Consumer goods: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Forms 10-K and 20-F via SEC company facts (median of 2021-2025)", size=12)
        g = {c["name"]: c for c in C}
        with self.voiceover(
            "Here is the industry in one picture: each company by its revenue and by what it typically kept of each dollar. "
            f"<bookmark mark='a'/> The home and personal care makers: P&G, the largest, kept about {100 * g['Procter & Gamble']['margin']:.0f} "
            f"cents; Colgate and Church and Dwight about {100 * g['Colgate-Palmolive']['margin']:.0f}; Clorox and Estee "
            "Lauder less, about six. <bookmark mark='b'/> The food makers, from Hershey's "
            f"{100 * g['Hershey']['margin']:.0f} down to Conagra's {100 * g['Conagra']['margin']:.0f}. <bookmark mark='c'/> "
            f"The drinks makers spread the widest: Coca-Cola {100 * g['Coca-Cola']['margin']:.0f}, Monster "
            f"{100 * g['Monster']['margin']:.0f}, Brown-Forman's whiskey {100 * g['Brown-Forman']['margin']:.0f}; PepsiCo and "
            f"AB InBev about ten; the bottler seven. <bookmark mark='d'/> And at the top, the tobacco companies: Altria "
            f"{100 * g['Altria']['margin']:.0f}, Philip Morris International {100 * g['Philip Morris International']['margin']:.0f}. "
            "Size alone does not decide it: PepsiCo, the largest by revenue, keeps less than half of what Coca-Cola keeps on "
            "each dollar, and much of what it sells is snacks, and drinks it bottles itself, the heavier end of the trade, where the "
            "brand is a smaller part of the price."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(zero), FadeIn(xl), FadeIn(hd), FadeIn(key), FadeIn(src), run_time=1.0)
            for mk, grp in zip("abcd", ("home", "food", "drink", "tobacco")):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(x) for x in groups[grp]], lag_ratio=0.1), run_time=1.4)
        self.clear_scene()

    def admargin(self):
        A = R["ads"]["share"]
        G = R["margins"]["gm"]
        names = [n for n in A if n in G]
        pa = viz.plot_axes([0, 0.15], [0.2, 0.75], x_length=9.0, y_length=4.6, xticks=[0, 0.05, 0.10, 0.15],
                           yticks=[0.2, 0.4, 0.6], xfmt=lambda v: f"{100 * v:.0f}%", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="gross margin", size=13).move_to([-0.6, -0.5, 0])
        xl = tx("advertising as a share of sales", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        off = {"PepsiCo": UP, "Philip Morris International": RIGHT, "Mondelez": DOWN, "General Mills": UP, "Hershey": DOWN,
               "Kimberly-Clark": UP, "Monster": UP, "Coca-Cola": UP, "Colgate-Palmolive": RIGHT, "Procter & Gamble": UP,
               "Church & Dwight": RIGHT, "Clorox": LEFT, "Brown-Forman": DOWN}
        dots = VGroup()
        for n in names:
            col = SMOKE if n == "Philip Morris International" else ADS
            d = Dot(pa.ax.c2p(A[n], G[n]), radius=0.08, color=col)
            dots.add(VGroup(d, tx(n, 12, col, bold=True).next_to(d, off.get(n, UP), buff=0.06)))
        lo = VGroup(*[d for d, n in zip(dots, names) if A[n] < 0.08])
        hi = VGroup(*[d for d, n in zip(dots, names) if A[n] >= 0.08])
        src = source("Forms 10-K via SEC company facts, latest fiscal year: advertising, revenue and cost of sales", size=12)
        beat(self,
             "One more picture of the whole industry: how much each company advertises against how much it keeps after the "
             "cost of its products. <bookmark mark='a'/> The food makers advertise little and keep little: Mondelez, "
             "General Mills and Hershey, five cents of advertising or less, gross margins in the thirties or below. "
             "<bookmark mark='b'/> The heavy advertisers, Colgate, P&G, Coca-Cola, Church and Dwight and Brown-Forman, keep "
             "between forty-five and sixty-two cents. Where the name matters most, companies spend most to keep it, and "
             "keep most for it. The exceptions are PepsiCo, which also bottles drinks and sells snacks, and the tobacco company, "
             "which keeps the most while advertising little.",
             base=[pa, xl, head("Advertising against gross margin"), src], steps=[lo, hi])

    def map(self):
        cols = [("Home and personal", BRAND, ["Procter & Gamble", "Unilever", "L'Oreal", "Colgate-Palmolive", "Kimberly-Clark",
                                              "Kao", "Hindustan Unilever", "Clorox", "Church & Dwight", "Estee Lauder"]),
                ("Food", GOOD, ["Nestle", "Mondelez", "Danone", "Kraft Heinz", "General Mills", "Hershey", "Mengniu"]),
                ("Drinks", DRINK, ["Coca-Cola and its bottlers", "PepsiCo", "Keurig Dr Pepper", "Monster", "Nongfu Spring"]),
                ("Alcohol", PRICE, ["AB InBev", "Diageo", "Kweichow Moutai", "Constellation", "Brown-Forman"]),
                ("Tobacco", SMOKE, ["Philip Morris International", "Altria", "BAT", "China National Tobacco", "ITC"]),
                ("The buyers", BAD, ["Walmart", "Costco", "Kroger", "Amazon", "Aldi, Lidl"])]
        g = VGroup()
        for i, (title, col, names) in enumerate(cols):
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([-6.2 + 2.2 * i, 2.2, 0], aligned_edge=UL)
            g.add(box)
        note = tx("Names only where this film has not measured them: Unilever, L'Oreal, Kao, Hindustan Unilever, Nestle, Danone, "
                  "Kraft Heinz, Mengniu, Nongfu Spring, Diageo, Kweichow Moutai, BAT, China National Tobacco, ITC and the "
                  "retailers", 13, GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        beat(self,
             "And the map. <bookmark mark='a'/> The home and personal care makers, American, European, Japanese and Indian. "
             "<bookmark mark='b'/> The food makers. <bookmark mark='c'/> The soft drinks companies and their bottlers. "
             "<bookmark mark='d'/> The brewers and distillers, among them China's Kweichow Moutai. <bookmark mark='e'/> The "
             "tobacco companies, including China's state monopoly. <bookmark mark='f'/> And the buyers, the retailers whose "
             "shelves they all compete for. Many report outside America's securities regulator, so this film shows them by "
             "name only.",
             base=[head("The map of the business"), note], steps=list(g))
