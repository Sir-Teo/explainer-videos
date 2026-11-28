from __future__ import annotations

from videos.industry.industry32.common import *  # noqa: F403


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: a marketplace for a year", "You set the fees, the ads and the delivery promise. Who stays?",
             "Chapter one. Run it. You run an online marketplace for a year. You do not own the goods; you bring buyers and "
             "sellers together, deliver the parcels, and take a cut.", lit=("unit", "make"))
        self.sides()
        self.base()
        self.take()
        self.who()
        self.ads()
        self.speed()
        self.lesson()

    def sides(self):
        buyers = draw.crowd(12, h=0.42, color=SHOP, cols=4).move_to([-4.8, 0.6, 0])
        sellers = VGroup(*[draw.shop(0.8, color=MARKET) for _ in range(6)]).arrange_in_grid(2, 3, buff=0.25).move_to([4.8, 0.6, 0])
        page = draw.web_page(3.0, cols=3, rows=2).move_to([0, 0.6, 0])
        bl = tx("buyers", 18, SHOP, bold=True).next_to(buyers, DOWN, buff=0.25)
        sl = tx("sellers", 18, MARKET, bold=True).next_to(sellers, DOWN, buff=0.25)
        a1 = CurvedArrow(buyers.get_top() + UP * 0.2, sellers.get_top() + UP * 0.2, angle=-TAU / 6, color=SHOP)
        a2 = CurvedArrow(sellers.get_bottom() + DOWN * 0.7, buyers.get_bottom() + DOWN * 0.7, angle=-TAU / 6, color=MARKET)
        t1 = tx("more buyers bring more sellers", 15, SHOP).next_to(a1, UP, buff=0.05)
        t2 = tx("more sellers bring more buyers", 15, MARKET).next_to(a2, DOWN, buff=0.05)
        tag = estimate_tag("the Works: a two-sided marketplace (explainer/industry/works/marketplace.py)", size=12)
        beat(self,
             "A marketplace has two kinds of customer. <bookmark mark='a'/> Buyers come for choice, low prices and fast "
             "delivery. <bookmark mark='b'/> Sellers come for buyers. <bookmark mark='c'/> And each side comes because of "
             "the other: more buyers draw more sellers, and more sellers mean more choice, which draws more buyers. That "
             "loop is why the first marketplace in a country is so hard to dislodge, and why your prices matter twice: "
             "every fee you charge a seller changes how many buyers you have.",
             base=[page, tag], steps=[VGroup(buyers, bl), VGroup(sellers, sl), VGroup(a1, a2, t1, t2)])

    def base(self):
        U = R["run"]
        b = U["base"]
        c = stat_cards([(f"{b['buyers'] / 1e6:.0f}m", "buyers", SHOP), (f"{b['sellers'] / 1e3:.0f}k", "sellers", MARKET),
                        (bn(b["gmv"]), "spent by buyers (GMV)", ALL), (bn(b["revenue"]), "your fees and ads", MARKET),
                        (bn(b["profit"]), "your profit", GOOD)], y=0.2, size=34, span=12.8)
        pk = VGroup(*[draw.parcel(0.55) for _ in range(7)]).arrange(RIGHT, buff=0.3).move_to([0, -2.2, 0])
        tag = estimate_tag(f"the Works: ${U['basket']:.0f} orders, a {100 * U['take']:.0f}% take rate, ads of "
                           f"{100 * U['ad']:.0f}% of sales, two-day delivery", size=12)
        beat(self,
             f"Start where the Works settles. You charge sellers {100 * U['take']:.0f} per cent of each sale in commission "
             f"and delivery fees, sell them advertising worth {100 * U['ad']:.0f} per cent more, and promise delivery in two "
             f"days. <bookmark mark='a'/> {b['buyers'] / 1e6:.0f} million buyers and {b['sellers'] / 1e3:.0f} thousand "
             f"sellers decide it is worth it. <bookmark mark='b'/> Buyers spend {b['gmv'] / 1e9:.0f} billion dollars a year: "
             "the gross merchandise value, the number every marketplace reports first. <bookmark mark='c'/> You take "
             f"{b['revenue'] / 1e9:.1f} billion of it, and after delivering {b['orders'] / 1e6:.0f} million parcels and "
             f"paying for the site, {b['profit'] / 1e9:.1f} billion is profit.",
             base=[pk, tag], steps=[VGroup(c[0], c[1]), c[2], VGroup(c[3], c[4])])

    def take(self):
        U = R["run"]
        T = U["by_take"]
        rev = {100 * t: s["revenue"] / 1e9 for t, s in T.items()}
        pro = {100 * t: s["profit"] / 1e9 for t, s in T.items()}
        ch = line_chart({"your revenue": (rev, MARKET), "your profit": (pro, GOOD)}, x=(10, 45), y=(-4, 16),
                        xticks=[10, 15, 20, 25, 30, 35, 40, 45], yticks=[-4, 0, 4, 8, 12, 16], xfmt=lambda v: f"{v:.0f}%",
                        yfmt=lambda v: f"${v:.0f}bn", ylabel="the Works: a year's revenue and profit by the take rate",
                        width=8.6, height=4.3, center=(-1.0, -0.45), nudge={"your profit": -0.3})
        tr = max(rev, key=rev.get)
        tp = max(pro, key=pro.get)
        m1 = marker(ch.ax, tr, rev[tr], f"most revenue: {tr:.0f}%", MARKET, side=UP)
        m2 = marker(ch.ax, tp, pro[tp], f"most profit: {tp:.0f}%", GOOD, side=DOWN)
        tag = estimate_tag("the Works: sellers pass half of any extra fee into their prices", size=12)
        beat(self,
             "Your first lever is the take rate. <bookmark mark='a'/> Raise it and you earn more on each sale, but sellers "
             "with thin margins leave and the rest raise their prices, so buyers leave too. Revenue rises, then turns over, "
             f"peaking at a take rate of about {tr:.0f} per cent. <bookmark mark='b'/> Profit peaks a little higher, at "
             f"{tp:.0f}, because every lost order is also a parcel you no longer pay to deliver. <bookmark mark='c'/> Push "
             "much past that and the marketplace empties: below a certain size, the loop runs backwards.",
             base=[ch.frame, tag], steps=[VGroup(ch.lines["your revenue"], ch.labels["your revenue"], m1),
                                          VGroup(ch.lines["your profit"], ch.labels["your profit"], m2),
                                          marker(ch.ax, near(pro, 42.5), pro[near(pro, 42.5)], "the market empties", BAD, side=DOWN + LEFT)])

    def who(self):
        T = R["run"]["by_take"]
        rows = [["take rate", "sellers", "buyers", "spent by buyers", "your profit"]]
        cols = [None]
        for t in (0.15, 0.3, 0.4):
            s = T[t]
            rows.append([f"{100 * t:.0f}%", f"{s['sellers'] / 1e3:.0f}k", f"{s['buyers'] / 1e6:.0f}m", bn(s["gmv"]), bn(s["profit"])])
            cols.append([MARKET, MARKET, SHOP, ALL, GOOD if s["profit"] > 0 else BAD])
        t = table(rows, col_x=[-5.6, -3.0, -0.6, 1.8, 4.4], top=1.6, row_h=0.8, size=19, colors=cols)
        tag = estimate_tag("the Works", size=12)
        beat(self,
             "Here is who answers. <bookmark mark='a'/> At a fifteen per cent take rate "
             f"{T[0.15]['sellers'] / 1e3:.0f} thousand sellers and {T[0.15]['buyers'] / 1e6:.0f} million buyers come, but you "
             f"lose {abs(T[0.15]['profit']) / 1e9:.1f} billion dollars: fees that low do not pay for the deliveries. "
             f"<bookmark mark='b'/> At thirty per cent, fewer of both, and the most profit. <bookmark mark='c'/> At forty, "
             f"only {T[0.4]['sellers'] / 1e3:.0f} thousand sellers find it worth their while. The take rate is a price, and "
             "like any price it is bounded by what the customers, here both kinds, can do instead.",
             base=[t[0], tag], steps=[t[1], t[2], t[3]])

    def ads(self):
        A = R["run"]["by_ad"]
        buy = {100 * a: s["buyers"] / 1e6 for a, s in A.items()}
        pro = {100 * a: s["profit"] / 1e9 for a, s in A.items()}
        page = draw.web_page(2.6, cols=3, rows=2, sponsored=(0, 2, 4), accent=ADS).move_to([4.9, 1.2, 0])
        ch = line_chart({"profit, $bn": (pro, GOOD)}, x=(0, 14), y=(-1, 5), xticks=[0, 2, 4, 6, 8, 10, 12, 14],
                        yticks=[-1, 0, 1, 2, 3, 4, 5], xfmt=lambda v: f"{v:.0f}%", yfmt=lambda v: f"${v:.0f}bn",
                        ylabel="the Works: profit by sellers' ad spending, as a share of sales", width=7.2, height=4.0,
                        center=(-2.0, -0.5), label_end=False)
        best = max(pro, key=pro.get)
        m = marker(ch.ax, best, pro[best], f"best: {best:.0f}%", GOOD, side=UP)
        k12 = near(pro, 12)
        m2 = marker(ch.ax, k12, pro[k12], f"12%: {buy[k12]:.0f}m buyers", BAD, side=RIGHT)
        tag = estimate_tag("the Works: ads earn money but clutter the results buyers came for", size=12)
        beat(self,
             "Your second lever is advertising. <bookmark mark='a'/> Sellers will pay to appear at the top of the results, "
             "and that money costs you almost nothing to collect. <bookmark mark='b'/> So profit rises as you sell more "
             f"ads, up to about {best:.0f} per cent of sales. <bookmark mark='c'/> Then the sponsored products crowd out the "
             "ones buyers wanted, they find what they came for less often, and they leave: at twelve per cent of sales, you "
             f"keep only {buy[k12]:.0f} million of your buyers.",
             base=[ch.frame, tag], steps=[page, VGroup(ch.lines["profit, $bn"], m), m2])

    def speed(self):
        U = R["run"]
        D, B = U["by_days"], U["big_days"]
        rows = [["delivery promise", "buyers", "cost an order", "profit", "four times bigger: cost an order", "profit"]]
        cols = [None]
        for d in (1.0, 2.0, 3.0):
            s, b = D[d], B[d]
            rows.append([f"{d:.0f} day{'s' if d > 1 else ''}", f"{s['buyers'] / 1e6:.0f}m", f"${s['cost_per_order']:.2f}", bn(s["profit"]),
                         f"${b['cost_per_order']:.2f}", bn(b["profit"])])
            cols.append([WHITE, SHOP, DELIV, GOOD, DELIV, GOOD])
        t = table(rows, col_x=[-6.6, -3.9, -2.4, -0.4, 1.4, 5.3], top=1.5, row_h=0.8, size=17, colors=cols)
        van = draw.van(1.4).move_to([-4.8, -2.4, 0])
        tag = estimate_tag("the Works: faster delivery needs more warehouses and vans, a cost shared over every order", size=12)
        beat(self,
             "Your third lever is speed. <bookmark mark='a'/> Promise next-day delivery and you win "
             f"{D[1.0]['buyers'] / 1e6:.0f} million buyers, but each order costs ${D[1.0]['cost_per_order']:.2f} to deliver "
             "against eight dollars for two days, because you need more warehouses, closer to people, and more vans running "
             f"half full. <bookmark mark='b'/> At two days you make the most. <bookmark mark='c'/> At three you save little "
             "and lose many buyers. Now make the marketplace four times bigger: the network is shared over four times the "
             f"parcels, a one-day order costs ${B[1.0]['cost_per_order']:.2f}, and fast delivery becomes affordable. Speed is "
             "a game of fixed costs, and the biggest player can afford it first.",
             base=[t[0], van, tag], steps=[t[1], t[2], t[3]])

    def lesson(self):
        g = VGroup(tx("What Run it shows", 22, WHITE, bold=True),
                   tx("a marketplace sells to two sides, and each side comes for the other", 18, MARKET),
                   tx("the take rate is a price: too low loses money, too high empties the market", 18, SHOP),
                   tx("ads are nearly pure profit, until they crowd out what buyers came for", 18, ADS),
                   tx("fast delivery is a fixed cost: it pays only at great scale", 18, DELIV)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' summary of the Works' marketplace", size=12)
        beat(self,
             "So: <bookmark mark='a'/> a marketplace sells to two sides at once. <bookmark mark='b'/> Its fee is bounded "
             "by what both sides can do instead. <bookmark mark='c'/> Its advertising is the most profitable thing it "
             "sells, up to a point. <bookmark mark='d'/> And its delivery promise is a bet on scale. Now to the real "
             "companies, starting with a question that sounds like accounting and is really about the business: who owns "
             "the stock?",
             base=[tag], steps=[g[:2], g[2], g[3], g[4]])
