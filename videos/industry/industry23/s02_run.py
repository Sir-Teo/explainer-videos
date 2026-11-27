from __future__ import annotations

from videos.industry.industry23.common import *  # noqa: F403

CH_COL = {"far": FAR, "near": NEAR, "chase": CHASE}
CH_NAME = {"far": "all early, from far away", "near": "all late, from nearby", "chase": "a base early, the rest chased late"}


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: buy the season",
             "A new T-shirt goes on sale in the spring. How many do you order, and when?",
             "Chapter one. Run it. You are the buyer for a clothes shop, and a new T-shirt goes on sale next spring. You "
             "have to decide how many to order, and when, before anybody has bought a single one.", lit=("make", "dollar"))
        self.market()
        self.curve()
        self.order()
        self.three()
        self.where()
        self.forecast()
        self.answer()

    def market(self):
        U = R["run"]
        shirt = draw.tshirt(1.6).move_to([-4.6, 1.3, 0])
        tag = draw.price_tag(f"${U['price']:.0f}", 1.0).next_to(shirt, RIGHT, buff=0.3)
        facts = VGroup(tx(f"it sells for ${U['price']:.0f}; on average, {U['mean'] / 1e3:.0f},000 people will want one", 17, WHITE),
                       tx(f"order now, from a factory far away: ${U['cost_far']:.0f} a shirt, delivered", 17, FAR),
                       tx(f"order once the season starts, from a factory nearby: ${U['cost_near']:.0f} a shirt", 17, NEAR),
                       tx(f"whatever is left at the end goes in the sale at ${U['clearance']:.0f}", 17, BAD),
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([1.6, -0.9, 0])
        est = estimate_tag("the Works: an illustrative style and season", size=12)
        beat(self,
             f"Here is the shirt. <bookmark mark='a'/> It will sell for {U['price']:.0f} dollars, and on average about "
             f"{U['mean'] / 1e3:.0f} thousand people will want one. But that is only an average. <bookmark mark='b'/> You can "
             f"order now, months ahead, from a factory on the other side of the world, for {U['cost_far']:.0f} dollars a "
             f"shirt, shipping included. <bookmark mark='c'/> Or you can wait until the first weeks of the season have "
             f"shown how it is selling, and order from a factory nearby, for {U['cost_near']:.0f} dollars: dearer, because "
             "the factory is nearer and the order is rushed. <bookmark mark='d'/> Whatever you have not sold when the "
             f"season ends goes in the sale, at {U['clearance']:.0f} dollars, eighty per cent off.",
             base=[shirt, tag, est], steps=[facts[0], facts[1], facts[2], facts[3]])

    def curve(self):
        C = R["curve"]
        U = R["run"]
        pts = {x / 1e3: y for x, y in zip(C["x"], C["pdf"])}
        ch = line_chart({"demand": (pts, FAR)}, x=(0, 300), y=(0, 1.2), xticks=[0, 50, 100, 150, 200, 250, 300],
                        yticks=[0], xfmt=lambda v: f"{v:.0f}k", yfmt=lambda v: "", ylabel="how likely each level of demand is",
                        width=9.6, height=4.2, center=(-0.4, -0.5), label_end=False)
        ax = ch.ax
        mean = DashedLine(ax.c2p(U["mean"] / 1e3, 0), ax.c2p(U["mean"] / 1e3, 1.1), stroke_color=WHITE, stroke_width=2)
        ml = tx(f"average {U['mean'] / 1e3:.0f}k", 14, WHITE).next_to(ax.c2p(U["mean"] / 1e3, 1.1), UP, buff=0.05)
        band = Line(ax.c2p(C["p10"] / 1e3, 0.08), ax.c2p(C["p90"] / 1e3, 0.08), stroke_color=PRICE, stroke_width=10)
        bl = tx(f"8 seasons in 10: {C['p10'] / 1e3:.0f}k to {C['p90'] / 1e3:.0f}k", 15, PRICE, bold=True).next_to(band, RIGHT, buff=0.15)
        est = estimate_tag(f"the Works: demand lognormal, forecast error {100 * U['cv_far']:.0f}% of the mean, months ahead", size=12)
        beat(self,
             "Months ahead, this is all you know. <bookmark mark='a'/> Demand could be anywhere along this curve: most "
             "likely somewhere below the average, because a few styles become hits and most do not, <bookmark mark='b'/> "
             f"with the average itself at {U['mean'] / 1e3:.0f} thousand. <bookmark mark='c'/> In eight seasons out of ten "
             f"the shirt will sell somewhere between {C['p10'] / 1e3:.0f} thousand and {C['p90'] / 1e3:.0f} thousand. A "
             f"forecast that wide is normal for a new style: here the error is {100 * U['cv_far']:.0f} per cent of the "
             "average.",
             base=[ch.frame, est], steps=[ch.lines["demand"], [mean, ml], [band, bl]])

    def order(self):
        U, C = R["run"], R["curve"]
        q = C["far"] / 1e3
        left = VGroup(tx("one more shirt ordered:", 18, GREY_A),
                      tx(f"if it sells: +${U['price'] - U['cost_far']:.0f}", 22, GOOD, bold=True),
                      tx(f"if it ends up in the sale: -${U['cost_far'] - U['clearance']:.0f}", 22, BAD, bold=True)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-3.6, 1.0, 0])
        ratio = MathTex(r"\frac{%d}{%d + %d} = %.1f\%%" % (U["price"] - U["cost_far"], U["price"] - U["cost_far"],
                                                         U["cost_far"] - U["clearance"], 100 * U["ratio_far"]),
                        font_size=48, color=PRICE).move_to([3.2, 1.0, 0])
        rl = tx("order until the last shirt has this chance of selling", 16, PRICE).next_to(ratio, DOWN, buff=0.25)
        res = VGroup(tx(f"the best single early order: {q:.0f},000 shirts", 22, FAR, bold=True),
                     tx(f"{100 * C['p_short']:.1f}% chance of selling out; most seasons end with shirts in the sale", 17, GREY_A)
                     ).arrange(DOWN, buff=0.18).move_to([0, -1.9, 0])
        est = estimate_tag("the Works: the newsvendor's rule", size=12)
        beat(self,
             "So how many do you order? Think about the last shirt. <bookmark mark='a'/> If it sells, you make "
             f"{U['price'] - U['cost_far']:.0f} dollars on it. If it ends up in the sale, you lose "
             f"{U['cost_far'] - U['clearance']:.0f}. <bookmark mark='b'/> So it is worth ordering as long as the last shirt "
             f"has at least a {100 * U['ratio_far']:.1f} per cent chance of selling: twenty-eight dollars to gain against "
             "four to lose. This is an old result, the newsvendor's rule, named after a boy deciding how many papers to "
             "buy in the morning. <bookmark mark='c'/> On this curve it means ordering "
             f"{q:.0f} thousand shirts, far more than the average, because a missed sale costs so much more than a "
             "shirt in the sale. You will rarely sell out; most seasons, you will have shirts to clear.",
             base=[est], steps=[left, [ratio, rl], res])

    def three(self):
        U = R["run"]
        Ch = U["choices"]
        items = [(CH_NAME[k], Ch[k]["profit"] / 1e6, CH_COL[k], f"${Ch[k]['profit'] / 1e6:.2f}m") for k in ("far", "near", "chase")]
        rows = hbars(items, max_value=2.8, x0=0.6, top=1.4, row=1.1, length=5.6, size=18, bar_h=0.55)
        lab = tx("the season's expected profit, after the sale", 16, GREY_A).to_edge(UP, buff=0.9)
        est = estimate_tag("the Works: expected values over every way the season can turn out", size=12)
        b = Ch["chase"]
        beat(self,
             "Now the three ways to buy. <bookmark mark='a'/> All early, from far away, at the best quantity: on average "
             f"the season earns {Ch['far']['profit'] / 1e6:.2f} million dollars. <bookmark mark='b'/> All late, from "
             "nearby, after the first weeks have shown how the shirt is selling: you order much closer to what people "
             f"want, but every shirt costs four dollars more, and you earn {Ch['near']['profit'] / 1e6:.2f} million, less "
             f"than the early order. <bookmark mark='c'/> Or both: order {b['base'] / 1e3:.0f} thousand early and cheaply, "
             "then, if the first weeks show a hit, order more from nearby. You top up in about "
             f"{100 * b['topped']:.0f} seasons out of a hundred, and earn {b['profit'] / 1e6:.2f} million, more than either.",
             base=[rows.axis, lab, est], steps=[rows[0], rows[1], rows[2]])

    def where(self):
        Ch = R["run"]["choices"]
        rows = [["", "all early", "all late", "base and chase"]]
        for key, nm, f in (("ordered", "shirts ordered", lambda v: f"{v / 1e3:.0f}k"), ("cleared", "left for the sale", lambda v: f"{v / 1e3:.0f}k"),
                           ("lost", "customers who found none", lambda v: f"{v / 1e3:.1f}k"),
                           ("gm", "gross margin", lambda v: f"{100 * v:.1f}%")):
            rows.append([nm] + [f(Ch[k][key]) for k in ("far", "near", "chase")])
        tbl = table(rows, col_x=[-5.6, -0.9, 1.6, 3.9], top=1.8, row_h=0.62, size=18,
                    colors=[[None, FAR, NEAR, CHASE]] + [[WHITE, FAR, NEAR, CHASE]] * 4)
        note = tx("Inditex, the year to January 2026: a gross margin of 58.3%", 17, FAST, bold=True).move_to([0, -1.9, 0])
        est = estimate_tag("the Works' season", size=12)
        src = source("Inditex, FY2025 results", size=12)
        beat(self,
             "Where does the difference come from? <bookmark mark='a'/> The early order buys "
             f"{Ch['far']['ordered'] / 1e3:.0f} thousand shirts and sends {Ch['far']['cleared'] / 1e3:.0f} thousand of "
             "them, on average, to the sale. <bookmark mark='b'/> The late order sends only "
             f"{Ch['near']['cleared'] / 1e3:.0f} thousand to the sale, but pays more for every shirt. <bookmark mark='c'/> "
             f"The chase sends {Ch['chase']['cleared'] / 1e3:.0f} thousand, turns away the fewest customers, and keeps a "
             f"gross margin of {100 * Ch['chase']['gm']:.1f} per cent, against {100 * Ch['far']['gm']:.1f} for the early "
             f"order. <bookmark mark='d'/> Inditex's gross margin in its last full year was {R['hook']['gm']} per cent. "
             "The Works' numbers are made up; the shape is not. Being able to wait and see is worth paying for, as long "
             "as you only pay for it on part of the order.",
             base=[est, src], steps=[tbl[:2], tbl[2:3], tbl[3:], note])

    def forecast(self):
        cv = R["run"]["cv"]
        pts = {100 * k: v / 1e6 for k, v in cv.items()}
        ch = line_chart({"early order": (pts, FAR)}, x=(20, 100), y=(1.8, 2.8), xticks=[20, 40, 60, 80, 100],
                        yticks=[1.8, 2.0, 2.2, 2.4, 2.6, 2.8], xfmt=lambda v: f"{v:.0f}%", yfmt=lambda v: f"${v:.1f}m",
                        ylabel="expected profit of the best early order", width=9.0, height=4.2, center=(-0.6, -0.5),
                        label_end=False)
        xl = tx("forecast error months ahead, as a share of average demand", 14, GREY_B).next_to(ch.ax, DOWN, buff=0.5)
        now = marker(ch.ax, 60, pts[60], f"this shirt: ${pts[60]:.2f}m", FAR, side=UP)
        good = marker(ch.ax, 20, pts[20], f"a near-certain basic: ${pts[20]:.2f}m", GOOD, side=UP)
        good[1].shift(RIGHT * 1.4)
        est = estimate_tag("the Works' season", size=12)
        beat(self,
             "The whole problem is the forecast. <bookmark mark='a'/> Here is what the best early order earns as the "
             "forecast gets worse. <bookmark mark='b'/> For this shirt, with an error of sixty per cent, "
             f"{pts[60]:.2f} million. <bookmark mark='c'/> For a plain basic whose demand is known within twenty per cent, "
             f"{pts[20]:.2f} million, with no need to chase at all. That is why basics, plain T-shirts, socks, jeans in "
             "the usual sizes, can be bought far away and early, and why the fashionable lines are the ones worth making "
             "close to home.",
             base=[ch.frame, xl, est], steps=[ch.lines["early order"], now, good])

    def answer(self):
        Ch = R["run"]["choices"]
        c = stat_cards([(f"${Ch['far']['profit'] / 1e6:.2f}m", "all early: cheap, but blind", FAR),
                        (f"${Ch['near']['profit'] / 1e6:.2f}m", "all late: informed, but dear", NEAR),
                        (f"${Ch['chase']['profit'] / 1e6:.2f}m", "a base early, the hits chased", CHASE)], y=0.9, size=40, span=12)
        note = tx("A markdown is the price of a wrong guess; speed is a way to guess less.", 20, WHITE, bold=True).move_to([0, -1.4, 0])
        est = estimate_tag("the Works' season", size=12)
        beat(self,
             f"So the answer. <bookmark mark='a'/> Buying everything early is cheap but blind. <bookmark mark='b'/> Buying "
             f"everything late is informed but dear. <bookmark mark='c'/> Buying a base early and chasing the hits beats "
             f"both, by about {100 * (Ch['chase']['profit'] / Ch['far']['profit'] - 1):.0f} per cent here. "
             "<bookmark mark='d'/> Every shirt in the sale is the cost of a guess that was wrong. The rest of the industry "
             "is a set of different answers to that one problem: guess less, sell the mistakes somewhere else, or make "
             "so few that there are none.",
             base=[est], steps=[c[0], c[1], c[2], note])
