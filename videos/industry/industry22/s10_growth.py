from __future__ import annotations

from videos.industry.industry22.common import *  # noqa: F403


class Growth(VoiceoverScene):
    def construct(self):
        card(self, 8, "Where growth comes from", "How does a mature brand company grow?",
             "Chapter eight. Where growth comes from. Most of these products are bought by people who already buy them. "
             "So how does a company grow? There are three ways: sell a better version of the same thing, sell it in "
             "new places, or build a new brand for a new habit.", lit=("change",))
        self.segments()
        self.abroad()
        self.monster()
        self.q1()

    def segments(self):
        G = R["growth"]["seg"]
        items = [(k, g, BRAND if g >= 4 else GREY_B, f"+{g}%  (${v:.1f}bn)") for k, (v, g) in sorted(G.items(), key=lambda kv: -kv[1][1])]
        rows = hbars(items, max_value=8, x0=0.6, top=1.6, row=0.8, length=5.6, size=17, bar_h=0.42)
        lab = tx("P&G's segments, fiscal 2026: sales growth and sales", 16, GREY_A).to_edge(UP, buff=0.9)
        src = source("The Procter & Gamble Company, Form 10-K for fiscal 2026: segment results", size=12)
        beat(self,
             "Look inside P&G. <bookmark mark='a'/> Beauty grew seven per cent in fiscal 2026, four points of it from "
             "selling more; its skin care grew on the premium SK-II brand, which sells above the category's average price. <bookmark mark='b'/> Grooming and "
             "health care grew four per cent, mostly from currency and price. <bookmark mark='c'/> The two biggest "
             f"businesses, fabric and home care, {G['Fabric & Home Care'][0]:.0f} billion dollars, and baby, feminine and "
             f"family care, {G['Baby, Feminine & Family Care'][0]:.0f} billion, grew two per cent and one. Growth comes from "
             "premium versions of familiar things, and from new places. The biggest businesses, detergent and nappies, "
             "grew slowest; beauty, with its premium creams, grew fastest.",
             base=[rows.axis, lab, src], steps=[rows[0], VGroup(rows[1], rows[2]), VGroup(rows[3], rows[4])])

    def abroad(self):
        G = R["growth"]
        wm = draw.world_map(width=11.0).move_to([0, 0.2, 0])
        dots = VGroup(*[Dot(wm.p(lo, la), radius=0.12, color=PRICE) for lo, la in ((-60, -15), (78, 22), (115, 30), (20, 0), (30, 50), (105, 10))])
        c = tx(f"Colgate: about two-thirds of its sales outside America, {G['colgate_em']}% in emerging markets", 19, PRICE, bold=True).to_edge(DOWN, buff=0.9)
        src = source("Colgate-Palmolive Company, Form 10-K 2025", size=12)
        beat(self,
             "New places. <bookmark mark='a'/> Colgate makes about two-thirds of its sales outside the United States, and "
             f"{G['colgate_em']} per cent of all its sales in emerging markets: Latin America, Asia beyond Japan, Africa and "
             "Eurasia, and Central Europe. <bookmark mark='b'/> Selling the same brands in new countries is how a company "
             "grows when the shoppers at home already have a tube in the bathroom.",
             base=[wm, src], steps=[dots, c])

    def monster(self):
        E = R["extra"]
        m = E["mnst"]
        ch = line_chart({"Monster": (m, GOOD)}, x=(2012, 2025), y=(0, 9), xticks=[2012, 2015, 2018, 2021, 2025],
                        yticks=[0, 3, 6, 9], yfmt=lambda v: f"${v:.0f}bn", ylabel="Monster Beverage's revenue", width=8.6,
                        height=4.0, center=(-0.8, -0.5), label_end=False)
        m0 = marker(ch.ax, 2012, m[2012], f"2012: ${m[2012]:.1f}bn", GOOD, side=UP)
        m1 = marker(ch.ax, 2025, m[2025], f"2025: ${m[2025]:.1f}bn", GOOD, side=LEFT)
        cn = draw.can(1.2, color="#2E3645", band=GOOD).move_to([5.0, 1.0, 0])
        src = source("Monster Beverage Corporation, Forms 10-K via SEC company facts: revenue and cost of sales", size=12)
        beat(self,
             "And new brands can still be built. <bookmark mark='a'/> Monster sold "
             f"{m[2012]:.1f} billion dollars of energy drinks in 2012. <bookmark mark='b'/> In 2025 it sold "
             f"{m[2025]:.1f} billion, keeping {100 * E['mnst_gm']:.0f} cents of each dollar after the cost of making them, "
             "almost as much as Coca-Cola. Coca-Cola's bottlers distribute some of its brands. A new category, with a "
             "brand built for it, can still grow into a giant.",
             base=[ch.frame, cn, src], steps=[m0, [ch.lines["Monster"], m1]])

    def q1(self):
        C = R["called"]
        c = stat_cards([(f"+{C['q1']}%", "P&G's organic sales, July to September 2026", GOOD),
                        ("+2 / +1", "points from volume / from mix; pricing minor", VOL)], y=0.8, size=44, span=12)
        note = tx("After three years led by price, volume grew again.", 19, WHITE, bold=True).move_to([0, -1.5, 0])
        src = source("The Procter & Gamble Company, Form 8-K of 22 October 2026 (Exhibit 99.1)", size=12)
        beat(self,
             "And the latest quarter shows the healthiest kind of growth. <bookmark mark='a'/> In the three months to "
             f"September 2026, P&G's organic sales rose {C['q1']} per cent, <bookmark mark='b'/> two points from selling more "
             "and one from a richer mix, with pricing only a minor part. <bookmark mark='c'/> After three years in which "
             "growth was mostly price, shoppers were buying more again.",
             base=[src], steps=[c[0], c[1], note])
