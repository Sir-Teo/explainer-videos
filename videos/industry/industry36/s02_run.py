from __future__ import annotations

from videos.industry.industry36.common import *  # noqa: F403


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: a software company for five years", "You run a subscription software company. Where should the next dollar go?",
             "Chapter one. Run it. You run a software company that rents its product by the year. You have a sales team, a "
             "team of engineers, and a choice about where the next dollar goes.", lit=("unit", "dollar"))
        self.company()
        self.year()
        self.leverage()
        self.choice()
        self.cash()
        self.price()
        self.lesson()

    def company(self):
        C = R["run"]["company"]
        U = R["run"]["unit"]
        c = VGroup(*[VGroup(tx(a, 30, col, bold=True), tx(b_, 14, GREY_A)).arrange(DOWN, buff=0.06) for a, b_, col in (
            (mn(C["arr0"]), "annual recurring revenue (ARR)", SUB),
            (f"{100 * C['gm']:.0f}%", "gross margin: hosting and support take the rest", HOST),
            (f"{C['reps']:.0f}", f"salespeople, each bringing in {mn(C['productivity'], 2)} of new ARR a year", SALES),
            (f"{100 * C['churn']:.0f}% / {100 * C['expansion']:.0f}%", "of ARR lost each year / added by customers who stay", PROFIT))]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([1.6, 0.0, 0])
        lap = draw.laptop(2.2).move_to([-4.2, 0.2, 0])
        tag = estimate_tag("the Works: a subscription company; every input is this series' assumption (explainer/industry/works/saas.py)", size=12)
        beat(self,
             f"Here is your company. <bookmark mark='a'/> Customers pay you {C['arr0'] / 1e6:.0f} million dollars a year for "
             "subscriptions: that is your annual recurring revenue. <bookmark mark='b'/> Running the software for them, the "
             f"servers and the support, costs {100 * (1 - C['gm']):.0f} cents of each dollar. <bookmark mark='c'/> "
             f"{C['reps']:.0f} salespeople each bring in about {C['productivity'] / 1e3:.0f} thousand dollars of new subscriptions "
             f"a year. <bookmark mark='d'/> And each year customers who leave or cut back take away {100 * C['churn']:.0f} per "
             f"cent of your revenue, while those who stay buy {100 * C['expansion']:.0f} per cent more.",
             base=[lap, tag], steps=list(c))

    def year(self):
        U = R["run"]["unit"]
        C = R["run"]["company"]
        items = [("new customers, from the sales team", U["new"] / 1e6, SALES, mn(U["new"])),
                 ("more from customers who stay", U["expanded"] / 1e6, PROFIT, mn(U["expanded"])),
                 ("lost to customers who leave or cut back", -U["churned"] / 1e6, LOSS, "-" + mn(U["churned"]))]
        rows = hbars(items, max_value=50, x0=0.8, top=1.4, row=1.0, length=4.6, size=17, bar_h=0.55)
        hd = tx("the first year's change in ARR", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        note = tx(f"the sales team costs {mn(U['sm'])} a year; it pays back in about {U['payback_months']:.0f} months of gross profit",
                  17, GREY_B).to_edge(DOWN, buff=0.8)
        tag = estimate_tag("the Works", size=12)
        beat(self,
             f"Follow the first year. <bookmark mark='a'/> The sales team brings in {U['new'] / 1e6:.0f} million dollars of new "
             f"subscriptions. <bookmark mark='b'/> Customers who stay add {U['expanded'] / 1e6:.0f} million. "
             f"<bookmark mark='c'/> Customers who leave take {U['churned'] / 1e6:.0f} million away. <bookmark mark='d'/> The "
             f"sales team costs {U['sm'] / 1e6:.0f} million a year, including the marketing and the engineers who help it sell. "
             f"Each dollar of new business takes about {U['payback_months']:.0f} months of gross profit to pay that back: "
             "software companies win customers at a loss and make their money if the customers stay.",
             base=[rows.axis, hd, tag], steps=[rows[0], rows[1], rows[2], note])

    def leverage(self):
        b = R["run"]["base"]
        ys = [1, 2, 3, 4, 5]
        arr = {y: b["arr"][4 * y - 1] / 1e6 for y in ys}
        gr = {y: 100 * b["growth"][4 * y - 1] for y in ys}
        om = {y: 100 * b["op_margin"][4 * y - 1] for y in ys}
        ch = line_chart({"growth of ARR, % a year": (gr, SUB), "operating margin, %": (om, PROFIT)}, x=(1, 5), y=(0, 50),
                        xticks=ys, yticks=[0, 10, 20, 30, 40, 50], xfmt=lambda v: f"year {int(v)}", yfmt=lambda v: f"{v:.0f}%",
                        ylabel="the company with no new hiring", width=8.4, height=4.2, center=(-1.0, -0.45))
        tag = estimate_tag("the Works: the same salespeople and engineers for five years", size=12)
        beat(self,
             "Now leave the company alone for five years: no new hires. <bookmark mark='a'/> Growth slows, from "
             f"{gr[1]:.0f} per cent in the first year to {gr[5]:.0f} in the fifth, because the same salespeople add the same "
             f"new business to an ever larger base. <bookmark mark='b'/> But the operating margin climbs from {om[1]:.0f} to "
             f"{om[5]:.0f} per cent, because the costs stay put while the revenue keeps growing. ARR reaches "
             f"{arr[5]:.0f} million. This is operating leverage, and in this series' reading it is why investors have forgiven young software "
             "companies their losses.",
             base=[ch.frame, tag], steps=[VGroup(ch.lines["growth of ARR, % a year"], ch.labels["growth of ARR, % a year"]),
                                          VGroup(ch.lines["operating margin, %"], ch.labels["operating margin, %"])])

    def choice(self):
        A = R["run"]["alloc"]
        xs = sorted(A)
        arr5 = {100 * s_: A[s_]["arr"][-1] / 1e6 for s_ in xs}
        ch = line_chart({"ARR after five years, $m": (arr5, SUB)}, x=(0, 100), y=(540, 600), xticks=[0, 25, 50, 75, 100],
                        yticks=[540, 560, 580, 600], xfmt=lambda v: f"{v:.0f}%", yfmt=lambda v: f"${v:.0f}m",
                        ylabel="share of an extra $30m a year spent on salespeople (the rest on engineers)", width=8.4, height=4.0,
                        center=(-1.0, -0.4))
        best = max(xs, key=lambda s_: A[s_]["arr"][-1])
        mk = marker(ch.ax, 100 * best, A[best]["arr"][-1] / 1e6, f"half and half: {mn(A[best]['arr'][-1])}", SUB, side=UP)
        tag = estimate_tag("the Works: engineering lowers churn and lifts expansion and sales with a lag; extra salespeople crowd the market", size=12)
        beat(self,
             "Now the board gives you an extra 30 million dollars a year. Salespeople, or engineers? "
             f"<bookmark mark='a'/> Put it all into engineering and ARR after five years is {A[0.0]['arr'][-1] / 1e6:.0f} million: "
             "a better product loses fewer customers and sells more to the ones it has, but slowly. All into sales, "
             f"{A[1.0]['arr'][-1] / 1e6:.0f} million: new salespeople sell at once, but each one finds the market a little more "
             f"crowded. <bookmark mark='b'/> Half and half does best on growth: {A[0.5]['arr'][-1] / 1e6:.0f} million.",
             base=[ch.frame, tag], steps=[VGroup(*ch.lines.values(), *ch.labels.values()), mk])

    def cash(self):
        A = R["run"]["alloc"]
        items = [("all engineers", A[0.0]["cum_cash"] / 1e6, ENG, f"{mn(A[0.0]['cum_cash'])}, margin {100 * A[0.0]['op_margin'][-1]:.0f}%"),
                 ("half and half", A[0.5]["cum_cash"] / 1e6, SUB, f"{mn(A[0.5]['cum_cash'])}, margin {100 * A[0.5]['op_margin'][-1]:.0f}%"),
                 ("all salespeople", A[1.0]["cum_cash"] / 1e6, SALES, f"{mn(A[1.0]['cum_cash'])}, margin {100 * A[1.0]['op_margin'][-1]:.0f}%")]
        rows = hbars(items, max_value=800, x0=-0.2, top=1.3, row=1.1, length=4.8, size=17, bar_h=0.6)
        hd = tx("cash generated over the five years, and the fifth year's operating margin", 20, WHITE, bold=True).to_edge(UP, buff=0.8)
        tag = estimate_tag("the Works: customers pay a year in advance, so cash runs ahead of profit", size=12)
        beat(self,
             "But growth is not the only score. <bookmark mark='a'/> Spent on engineers, the money leaves a company that "
             f"generates {A[0.0]['cum_cash'] / 1e6:.0f} million dollars of cash over five years and ends with a "
             f"{100 * A[0.0]['op_margin'][-1]:.0f} per cent margin, because it keeps its customers. <bookmark mark='b'/> Half "
             f"and half, {A[0.5]['cum_cash'] / 1e6:.0f} million. <bookmark mark='c'/> All on salespeople, only "
             f"{A[1.0]['cum_cash'] / 1e6:.0f} million: every salesperson is a cost every year, while customers keep leaving at "
             "the old rate. Growth and profit pull in different directions, and the board has to choose.",
             base=[rows.axis, hd, tag], steps=list(rows))

    def price(self):
        P = R["run"]["price"]
        c = stat_cards([(mn(P[None]["arr"][-1]), "ARR after five years, prices unchanged", SUB),
                        (mn(P[2]["arr"][-1]), "with prices 10% higher from the third quarter", PROFIT)], y=1.6, size=38, span=11)
        tagd = draw.price_tag("+10%", 1.4).move_to([0, -0.2, 0])
        note = tx("more customers leave for a year, and fewer new ones sign, but the rest pay more", 18, GREY_B).move_to([0, -2.0, 0])
        tag = estimate_tag("the Works: churn up 3 points for a year; new business down with a price elasticity of 1.5", size=12)
        beat(self,
             "And one more lever, the cheapest of all. <bookmark mark='a'/> Leave prices alone, and ARR after five years is "
             f"{P[None]['arr'][-1] / 1e6:.0f} million. <bookmark mark='b'/> Raise them ten per cent in the third quarter, and "
             f"it is {P[2]['arr'][-1] / 1e6:.0f} million, <bookmark mark='c'/> even though more customers leave that year and "
             "fewer new ones sign. Customers who depend on a product rarely leave over ten per cent; that is the business's "
             "real asset, and the next chapters are about why.",
             base=[tag, tagd], steps=[c[0], c[1], note])

    def lesson(self):
        lines = [("the first copy is expensive; the rest are almost free", ENG),
                 ("customers are won at a loss and paid back over years, if they stay", SALES),
                 ("costs stay put while revenue compounds: margins rise with scale", PROFIT),
                 ("salespeople buy growth now; engineers buy retention later", SUB)]
        g = VGroup(*[tx(t, 19, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.1, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        beat(self,
             "So: <bookmark mark='a'/> the first copy is expensive and the rest are almost free. <bookmark mark='b'/> "
             "Customers are won at a loss and paid back over years, if they stay. <bookmark mark='c'/> The costs stay put "
             "while the revenue compounds, so margins rise with scale. <bookmark mark='d'/> And salespeople buy growth now, "
             "while engineers buy loyalty later.",
             base=[head("Run it: what the company taught")], steps=list(g))
