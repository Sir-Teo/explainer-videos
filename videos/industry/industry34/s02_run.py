from __future__ import annotations

from videos.industry.industry34.common import *  # noqa: F403


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: a franchise for a year", "You run one burger restaurant. Then you set the fees for thousands.",
             "Chapter one. Run it. First you are a franchisee: you pay for the kitchen, hire the crew and run one burger "
             "restaurant for a year. Then you switch sides and become the franchisor.", lit=("unit", "dollar"))
        self.store()
        self.dollar()
        self.payback()
        self.risks()
        self.sales()
        self.switch()
        self.lesson()

    def store(self):
        U = R["run"]
        b = U["base"]
        rs = draw.restaurant(4.0).move_to([0, 1.2, 0])
        c = stat_cards([(f"${U['auv'] / 1e6:.1f}m", "sales a year", OP), (f"${U['store']['invest'] / 1e6:.1f}m", "your own investment", ALL),
                        (k(b["profit"]), "left for you a year", GOOD)], y=-1.6, size=36, span=11)
        tag = estimate_tag("the Works: a franchised restaurant with the average sales of a U.S. franchised McDonald's (explainer/industry/works/franchise.py)", size=12)
        beat(self,
             "Here is your restaurant. <bookmark mark='a'/> It sells about "
             f"{U['auv'] / 1e6:.1f} million dollars a year: McDonald's franchisees' sales in America, divided by their "
             f"restaurants. <bookmark mark='b'/> You put in {U['store']['invest'] / 1e6:.1f} million of your own for the "
             "kitchen, the seats and the signs; the franchisor owns or leases the land and building. "
             f"<bookmark mark='c'/> After a year of running it, {b['profit'] / 1e3:.0f} thousand dollars is yours.",
             base=[rs, tag], steps=[c[0], c[1], c[2]])

    def dollar(self):
        U = R["run"]
        b = U["base"]
        s = b["sales"]
        parts = [("food and paper", b["food"] / s, FOODC), ("crew and managers", b["labour"] / s, LABC), ("rent and royalties", b["fees"] / s, FR),
                 ("advertising fund", b["ad"] / s, ADC), ("utilities, repairs, cards", b["other"] / s, OTHER), ("delivery apps", b["apps"] / s, APPS),
                 ("yours", b["profit"] / s, GOOD)]
        bar = viz.bar_split(parts, 1.0, width=12.6, height=0.9).move_to([0, 0.9, 0])
        labs = VGroup()
        for i, (n, v, c) in enumerate(parts):
            lab = VGroup(tx(f"{100 * v:.0f}c" if v >= 0.06 else f"{100 * v:.1f}c", 18, c, bold=True), tx(n, 11, GREY_A)).arrange(DOWN, buff=0.05)
            lab.next_to(bar[i], DOWN if i % 2 == 0 else UP, buff=0.18)
            labs.add(lab)
        hd = tx("a dollar at your restaurant", 20, WHITE, bold=True).to_edge(UP, buff=0.6)
        tag = estimate_tag("the Works: food and crew are McDonald's company-store shares; rent and royalties its take on franchised sales; "
                           "the rest this series' assumptions", size=12)
        beat(self,
             f"Follow a dollar. <bookmark mark='a'/> {100 * parts[0][1]:.0f} cents buys the food and the paper, "
             f"<bookmark mark='b'/> {100 * parts[1][1]:.0f} pays the crew and managers. <bookmark mark='c'/> "
             f"{100 * parts[2][1]:.0f} cents goes to the franchisor as rent and royalties, <bookmark mark='d'/> four into the "
             "shared advertising fund, <bookmark mark='e'/> ten to the power company, the repairer, the card companies and the "
             f"insurer, <bookmark mark='f'/> and three to the delivery apps. <bookmark mark='g'/> About {100 * parts[6][1]:.0f} "
             "cents is yours.",
             base=[hd, tag], steps=[VGroup(bar[i], labs[i]) for i in range(7)])

    def payback(self):
        U = R["run"]
        b = U["base"]
        years = VGroup(*[RoundedRectangle(corner_radius=0.08, width=1.5, height=1.0, stroke_width=0, fill_color=GOOD, fill_opacity=0.8)
                         for _ in range(4)]).arrange(RIGHT, buff=0.25).move_to([-1.0, 0.6, 0])
        ylab = VGroup(*[tx(f"year {i + 1}", 15, WHITE, bold=True).move_to(years[i]) for i in range(4)])
        inv = tx(f"${U['store']['invest'] / 1e6:.1f}m back after about {b['payback']:.0f} years", 22, GOOD, bold=True).move_to([0, -1.0, 0])
        q = tx(f"Wingstop says it targets a franchisee cash return of about {get('wg34.coc'):.0f}% in a new restaurant's second year", 16, GREY_B).move_to([0, -2.0, 0])
        tag = estimate_tag("the Works; Wingstop, Form 10-K for 2025", size=12)
        beat(self,
             f"<bookmark mark='a'/> At {b['profit'] / 1e3:.0f} thousand dollars a year, your "
             f"{U['store']['invest'] / 1e6:.1f} million comes back in about {b['payback']:.0f} years. <bookmark mark='b'/> "
             "Then the restaurant earns for you, for as long as the franchise lasts. Franchisors compete for good operators "
             f"on exactly this number: <bookmark mark='c'/> Wingstop tells its investors it aims for franchisees to earn about "
             f"{get('wg34.coc'):.0f} per cent of their investment back in cash in a new restaurant's second year.",
             base=[tag], steps=[VGroup(years, ylab), inv, q])

    def risks(self):
        U = R["run"]
        rows = [["", "your profit", "per dollar", "years to pay back"]]
        cols = [None]
        for name, key, col in (("a normal year", "base", GOOD), ("sales 10% lower", "drop10", BAD), ("wages 20% higher", "wage20", BAD),
                               ("twice as much through apps", "apps30", APPS), ("fees of 15% instead of 12.7%", "fee15", FR)):
            r = U[key]
            rows.append([name, k(r["profit"]), f"{100 * r['margin']:.1f}c", f"{r['payback']:.1f}"])
            cols.append([WHITE, col, col, col])
        t = table(rows, col_x=[-6.2, -1.0, 1.6, 3.8], top=1.9, row_h=0.72, size=18, colors=cols)
        tag = estimate_tag("the Works: managers and minimum crews do not shrink with sales", size=12)
        beat(self,
             "Now the dangers. <bookmark mark='a'/> In a normal year you keep "
             f"{100 * U['base']['margin']:.1f} cents a dollar. <bookmark mark='b'/> If sales fall ten per cent, your managers and "
             f"minimum crew still cost the same, and profit falls to {U['drop10']['profit'] / 1e3:.0f} thousand. "
             f"<bookmark mark='c'/> If wages rise a fifth, it falls to {U['wage20']['profit'] / 1e3:.0f} thousand, and paying "
             f"back your investment takes {U['wage20']['payback']:.0f} years. <bookmark mark='d'/> If twice as many orders come "
             f"through delivery apps, their commission takes {U['base']['profit'] / 1e3 - U['apps30']['profit'] / 1e3:.0f} "
             f"thousand of it. <bookmark mark='e'/> And if the franchisor charged fifteen per cent instead of "
             f"{100 * U['take']:.1f}, you would keep {U['fee15']['profit'] / 1e3:.0f} thousand.",
             base=[t[0], tag], steps=[t[1], t[2], t[3], t[4], t[5]])

    def switch(self):
        U = R["run"]
        Fr = U["franchisor"]
        tot = {100 * t: r["total"] / 1e9 for t, r in Fr.items()}
        st = {100 * t: r["stores"][-1] / 1e3 for t, r in Fr.items()}
        ch = line_chart({"ten years' profit, $bn": (tot, FR), "stores after ten years, thousands": (st, OP)}, x=(6, 18), y=(0, 12),
                        xticks=[6, 8, 10, 12, 14, 16, 18], yticks=[0, 3, 6, 9, 12], xfmt=lambda v: f"{v:.0f}%", yfmt=lambda v: f"{v:.0f}",
                        ylabel="the Works' franchisor, starting with 1,000 restaurants", width=8.0, height=4.3, center=(-1.6, -0.45),
                        nudge={"stores after ten years, thousands": -0.25})
        best = max(tot, key=tot.get)
        kk = near(tot, 100 * U["take"])
        m1 = marker(ch.ax, best, tot[best], f"best: {best:.1f}%", FR, side=UP)
        m2 = marker(ch.ax, kk, st[kk], f"{100 * U['take']:.1f}%: McDonald's take", WHITE, side=DOWN + LEFT)
        tag = estimate_tag(f"the Works: {U['pool']:.0f} would-be franchisees a year; each opens if the store pays back within their own "
                           f"patience (median {U['patience']:.0f} years)", size=12)
        beat(self,
             "Now switch sides. You are the franchisor, with a thousand restaurants and a choice of fee. "
             "<bookmark mark='a'/> Charge more and every restaurant pays you more, but each one pays back its owner more "
             "slowly, and fewer people sign up to open the next. <bookmark mark='b'/> Over ten years the network grows "
             f"fastest at low fees, and your profit is highest at about {best:.1f} per cent. <bookmark mark='c'/> That is close "
             f"to the {100 * U['take']:.1f} per cent McDonald's collected from its franchisees' sales in 2025; with this "
             "series' assumptions about franchisees' patience it is a coincidence, not a proof, but it shows the trade: the "
             "fee is bounded by what an owner will accept to open the next store.",
             base=[ch.frame, tag], steps=[VGroup(ch.lines["stores after ten years, thousands"], ch.labels["stores after ten years, thousands"]),
                                         VGroup(ch.lines["ten years' profit, $bn"], ch.labels["ten years' profit, $bn"], m1), m2])

    def lesson(self):
        g = VGroup(tx("What Run it shows", 22, WHITE, bold=True),
                   tx("the franchisee carries the investment, the staff and the risk of a bad year", 18, OP),
                   tx("the franchisor takes a share of sales, good year or bad, on someone else's capital", 18, FR),
                   tx("wages, sales and delivery apps can each take most of an owner's margin", 18, BAD),
                   tx("the fee is bounded by what it takes to persuade the next owner to open", 18, GOOD)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' summary of the Works' franchise", size=12)
        beat(self,
             "So: <bookmark mark='a'/> the franchisee carries the investment, the crew and the risk of a bad year. "
             "<bookmark mark='b'/> The franchisor takes a share of sales, good year or bad, on someone else's capital. "
             "<bookmark mark='c'/> The owner's few cents can vanish with a fall in sales, a rise in wages or a shift to the "
             "apps. <bookmark mark='d'/> And the franchisor's fee is limited by one thing: someone has to want to open the "
             "next restaurant.",
             base=[tag], steps=[g[:2], g[2], g[3], g[4]])

    def sales(self):
        U = R["run"]
        bs = {100 * (x - 1): v / 1e3 for x, v in U["by_sales"].items()}
        ch = line_chart({"profit": (bs, GOOD)}, x=(-20, 20), y=(0, 700), xticks=[-20, -10, 0, 10, 20], yticks=[0, 200, 400, 600],
                        xfmt=lambda v: f"{v:+.0f}%", yfmt=lambda v: f"${v:.0f}k", ylabel="the Works' franchisee: a year's profit, by sales against normal",
                        width=8.2, height=4.3, center=(-1.4, -0.45), label_end=False)
        lo, hi = bs[near(bs, -20)], bs[near(bs, 20)]
        m1 = marker(ch.ax, -20, lo, f"20% lower: ${lo:.0f}k", BAD, side=DOWN + RIGHT)
        m2 = marker(ch.ax, 20, hi, f"20% higher: ${hi:.0f}k", GOOD, side=UP + LEFT)
        tag = estimate_tag("the Works: managers and minimum crews do not shrink with sales", size=12)
        beat(self,
             "Sales are the owner's great lever, in both directions. <bookmark mark='a'/> Twenty per cent below normal, the "
             f"restaurant makes {lo:.0f} thousand dollars: more than half the profit is gone. <bookmark mark='b'/> Twenty per cent above, "
             f"{hi:.0f} thousand, half as much again. Food, fees and apps rise and fall with sales; the managers, the minimum "
             "crew and the building do not. That is why franchisees care more than anyone about the brand's advertising and "
             "where the next restaurant opens: a new one too close takes sales from theirs.",
             base=[ch.frame, tag], steps=[VGroup(ch.lines["profit"], m1), m2])
