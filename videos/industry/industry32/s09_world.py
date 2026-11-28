from __future__ import annotations

from videos.industry.industry32.common import *  # noqa: F403


class World(VoiceoverScene):
    def construct(self):
        card(self, 7, "Made in China, sold everywhere", "What happens when the factory sells straight to the shopper?",
             "Chapter seven. Made in China, sold everywhere. The newest giant of online shopping did not build a shop or a "
             "network in America. It connected Chinese factories to American phones.", lit=("change",))
        self.pdd()
        self.split()
        self.minimis()
        self.world()

    def pdd(self):
        W = R["world"]
        P = W["pdd_rev"]
        ch = line_chart({"PDD's revenue": (P, MARKET)}, x=(2018, 2025), y=(0, 70), xticks=[2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
                        yticks=[0, 20, 40, 60], yfmt=lambda v: f"${v:.0f}bn",
                        ylabel=f"PDD Holdings' revenue, $bn a year (yuan at RMB{W['rate']:.2f} to the dollar, end-2025)",
                        width=8.6, height=4.3, center=(-1.2, -0.45), label_end=False)
        m = marker(ch.ax, 2022.7, P[2022] + 0.7 * (P[2023] - P[2022]), "Temu launches, September 2022", BAD, side=LEFT)
        m2 = marker(ch.ax, 2025, P[2025], f"2025: ${P[2025]:.0f}bn", MARKET, side=LEFT)
        ph = draw.phone(1.6, screen=MARKET).move_to([5.4, 1.4, 0])
        src = source("PDD Holdings, Forms 20-F via SEC company facts; Form 20-F for 2025", size=12)
        beat(self,
             "<bookmark mark='a'/> PDD Holdings runs Pinduoduo, a Chinese marketplace whose buyers team up with friends for lower prices. Its revenue "
             f"was about {P[2018]:.0f} billion dollars in 2018 and {P[2022]:.0f} billion in 2022. <bookmark mark='b'/> In "
             "September 2022 it launched Temu in North America, then Oceania and Europe: an app selling goods shipped "
             f"straight from Chinese makers at very low prices. <bookmark mark='c'/> By 2025 PDD's revenue was "
             f"{P[2025]:.0f} billion dollars.",
             base=[ch.frame, ph, src], steps=[ch.lines["PDD's revenue"], m, m2])

    def split(self):
        W = R["world"]
        d = W["pdd"]
        rows = VGroup()
        for i, y in enumerate((2023, 2025)):
            oms, ts = d[y]
            tot = oms + ts
            bar = viz.bar_split([("ads", oms, ADS), ("transactions", ts, MARKET)], 450, width=10.0 * tot / 450, height=0.8)
            bar.move_to([-1.2 - 5.0 * (1 - tot / 450), 1.0 - 1.9 * i, 0])
            lab = tx(str(y), 20, WHITE, bold=True).next_to(bar, LEFT, buff=0.3)
            t1 = tx(f"online marketing RMB{oms:.0f}bn ({100 * oms / tot:.0f}%)", 15, ADS).next_to(bar[0], DOWN, buff=0.12)
            t2 = tx(f"transaction services RMB{ts:.0f}bn ({100 * ts / tot:.0f}%)", 15, MARKET).next_to(bar[1], DOWN, buff=0.12)
            if y == 2023:
                t2.next_to(bar[1], UP, buff=0.12)
            rows.add(VGroup(lab, bar, t1, t2))
        hd = tx("PDD Holdings' revenue by kind, billions of yuan", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("PDD Holdings, Form 20-F for 2025", size=12)
        a, b = d[2023], d[2025]
        beat(self,
             "Where did the growth come from? <bookmark mark='a'/> In 2023, "
             f"{100 * a[0] / sum(a):.0f} per cent of PDD's revenue was advertising sold to merchants on its platforms and "
             f"{100 * a[1] / sum(a):.0f} per cent transaction services. <bookmark mark='b'/> By 2025 transaction services, "
             f"the fees that include Temu's, were half: {b[1]:.0f} billion yuan, more than twice as much in two years. A "
             "marketplace that began as an advertising business added a cross-border store on top.",
             base=[hd, src], steps=[rows[0], rows[1]])

    def minimis(self):
        rows = [["the rule", "what changed"],
                ["Section 321: low-value parcels to one person a day entered without duty", "before 2025"],
                ["no longer for low-value imports from China", "2 May 2025"],
                ["eliminated for imports from all countries", "29 August 2025"]]
        cols = [None, [WHITE, GREY_A], [WHITE, BAD], [WHITE, BAD]]
        t = table(rows, col_x=[-6.2, 3.2], top=1.8, row_h=0.8, size=18, colors=cols)
        pk = VGroup(*[draw.parcel(0.5) for _ in range(6)]).arrange(RIGHT, buff=0.3).move_to([0, -1.7, 0])
        q = tx("Amazon: 'China-based sellers account for significant portions of our third-party seller services and advertising revenues'",
               14, GREY_B).to_edge(DOWN, buff=0.75)
        if q.width > 13:
            q.scale_to_fit_width(13)
        src = source("PDD Holdings, Form 20-F for 2025; Amazon.com and eBay, Forms 10-K for 2025", size=12)
        beat(self,
             "The model leaned on a rule. <bookmark mark='a'/> Under section 321 of America's Tariff Act, a parcel worth "
             "less than a set value, sent to one person on one day, came in without duty. <bookmark mark='b'/> On 2 May 2025 the exemption ended for parcels from China, "
             "<bookmark mark='c'/> and on 29 August for every country. eBay says the change held back the growth of what "
             "its buyers spent in 2025, and Amazon warns that sellers based in China account for significant portions of its seller fees "
             "and advertising. The cheapest way to cross the Pacific got dearer for everyone.",
             base=[t[0], pk, q, src], steps=[t[1], t[2], t[3]])

    def world(self):
        W = R["world"]
        mp = draw.world_map(12.0, lon=(-130, 160), lat=(-45, 60)).move_to([0, -0.2, 0])
        spots = [(-50, -15, f"MercadoLibre: ${W['meli_gmv']:.0f}bn of goods; ${W['meli_tpv']:.0f}bn through Mercado Pago", MARKET, DOWN),
                 (106, 2, f"Shopee: ${W['shopee']:.0f}bn of goods, 13.9bn orders", MARKET, DOWN),
                 (127, 37, f"Coupang: {W['cpng']:.1f}m customers", SHOP, UP),
                 (114, 32, f"Alibaba's quick commerce: RMB{W['baba_quick']:.0f}bn, +47%", SUBS, LEFT)]
        dots = VGroup()
        for lon, lat, text, col, side in spots:
            d = Dot(mp.p(lon, lat), radius=0.12, color=col)
            lab = tx(text, 14, col, bold=True).next_to(d, side, buff=0.12)
            dots.add(VGroup(d, lab))
        src = source("MercadoLibre and Coupang, Forms 10-K for 2025; Sea Limited and Alibaba, Forms 20-F", size=12)
        beat(self,
             "And elsewhere, the shapes differ. <bookmark mark='a'/> In Latin America, MercadoLibre sold "
             f"{W['meli_gmv']:.0f} billion dollars of goods in 2025, but its payments arm, Mercado Pago, handled "
             f"{W['meli_tpv']:.0f} billion: in a region its filing describes as having many people without bank accounts, the marketplace became a bank. "
             f"<bookmark mark='b'/> In Southeast Asia, Shopee handled {W['shopee']:.0f} billion dollars of goods in almost "
             "fourteen billion orders: small baskets, many of them. <bookmark mark='c'/> In South Korea, Coupang built its "
             "own network. <bookmark mark='d'/> And in China the race has moved to delivery within the hour: Alibaba's "
             "quick commerce grew forty-seven per cent in a year.",
             base=[mp, src], steps=list(dots))
