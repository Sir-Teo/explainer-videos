from __future__ import annotations

from videos.industry.industry36.common import *  # noqa: F403


class Cost(VoiceoverScene):
    def construct(self):
        card(self, 2, "All fixed, all up front", "Where does a dollar of software revenue go?",
             "Chapter two. All fixed, all up front. In most industries in this series, a dollar of revenue goes first to "
             "making the thing. In software it goes somewhere else.", lit=("make", "dollar"))
        self.dollar()
        self.copy()
        self.compare()
        self.stock()
        self.why()

    def dollar(self):
        Cr = R["cost"]["crm"]
        rev = Cr["rev"]
        parts = [("hosting, support, services", Cr["cost"] / rev, HOST), ("engineering", Cr["rnd"] / rev, ENG),
                 ("sales and marketing", Cr["sm"] / rev, SALES), ("administration", Cr["ga"] / rev, GA),
                 ("restructuring", Cr["restr"] / rev, LOSS), ("operating income", Cr["op"] / rev, PROFIT)]
        bar = viz.bar_split(parts, 1.0, width=12.6, height=0.9).move_to([0, 0.8, 0])
        labs = VGroup()
        for i, (n_, v, c) in enumerate(parts):
            lab = VGroup(tx(f"{100 * v:.0f}c" if v >= 0.02 else f"{100 * v:.1f}c", 18, c, bold=True), tx(n_, 11, GREY_A)).arrange(DOWN, buff=0.05)
            lab.next_to(bar[i], DOWN if i % 2 == 0 else UP, buff=0.18)
            labs.add(lab)
        hd = tx(f"a dollar of Salesforce's revenue, year to January 2026 ({bn(rev)})", 20, WHITE, bold=True).to_edge(UP, buff=0.6)
        src = source("Salesforce, Form 10-K for fiscal 2026", size=12)
        beat(self,
             "Take Salesforce, founded in 1999 to rent business software over the internet. <bookmark mark='a'/> Of each "
             f"dollar of its revenue, {100 * parts[0][1]:.0f} cents went on running the service: data centres, support, and "
             f"the consultants who set it up. <bookmark mark='b'/> {100 * parts[1][1]:.0f} cents on engineers. "
             f"<bookmark mark='c'/> {100 * parts[2][1]:.0f} cents on selling: the largest cost of all. <bookmark mark='d'/> "
             f"{100 * parts[3][1]:.0f} on administration, <bookmark mark='e'/> one on restructuring, <bookmark mark='f'/> and "
             f"{100 * parts[5][1]:.0f} cents was operating income. More than twice as much went to selling the product as to "
             "building it.",
             base=[hd, src], steps=[VGroup(bar[i], labs[i]) for i in range(6)])

    def copy(self):
        H = R["hook"]
        items = [("licences and devices: cost per dollar sold", 100 * H["pcost"] / H["product"], LIC, f"{100 * H['pcost'] / H['product']:.0f}c"),
                 ("services and cloud: cost per dollar sold", 100 * H["scost"] / H["service"], HOST, f"{100 * H['scost'] / H['service']:.0f}c")]
        rows = hbars(items, max_value=40, x0=1.2, top=1.0, row=1.3, length=4.8, size=17, bar_h=0.65)
        hd = tx("Microsoft, fiscal 2026: what each kind of revenue costs to deliver", 20, WHITE, bold=True).to_edge(UP, buff=0.8)
        note = tx(f"product revenue {bn(H['product'])}, cost {bn(H['pcost'])}; service revenue {bn(H['service'])}, cost {bn(H['scost'])}", 16, GREY_B).to_edge(DOWN, buff=0.8)
        src = source("Microsoft, Form 10-K for fiscal 2026", size=12)
        beat(self,
             "Microsoft's accounts show the difference between a copy and a service. <bookmark mark='a'/> On licences and "
             f"devices, it spent {100 * H['pcost'] / H['product']:.0f} cents to deliver each dollar sold, and most of that was "
             "the consoles and laptops it builds rather than copies of software. <bookmark mark='b'/> On services and the cloud, "
             f"{100 * H['scost'] / H['service']:.0f} cents: running a service means running computers, every hour, for every "
             "customer. <bookmark mark='c'/> As software moves into the cloud, its cost of revenue rises, though it is still "
             "small beside a carmaker's or a grocer's.",
             base=[rows.axis, hd, src], steps=[rows[0], rows[1], note])

    def compare(self):
        Co = R["cost"]["companies"]
        names = ["Salesforce", "ServiceNow", "CrowdStrike", "Datadog", "Snowflake", "Atlassian", "HubSpot"]
        rows_ = []
        for i, n_ in enumerate(names):
            c = Co[n_]
            y = 2.1 - 0.66 * i
            parts = [("cost", c["cost"], HOST), ("R&D", c["rnd"], ENG), ("S&M", c["sm"], SALES)]
            x = -2.2
            g = VGroup(tx(n_, 15, WHITE).move_to([-3.4, y, 0], aligned_edge=RIGHT))
            for _, v, col in parts:
                w = 7.0 * v
                g.add(Rectangle(width=max(w, 0.01), height=0.4, stroke_width=0, fill_color=col, fill_opacity=0.95).move_to([x + w / 2, y, 0]))
                g.add(tx(f"{100 * v:.0f}", 12, "#1B2230", bold=True).move_to([x + w / 2, y, 0]) if w > 0.35 else VGroup())
                x += w
            g.add(tx(f"{100 * c['op']:+.0f}%", 15, PROFIT if c["op"] >= 0 else LOSS, bold=True).move_to([x + 0.55, y, 0]))
            rows_.append(g)
        key = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=c, fill_opacity=1), tx(t, 13, c)).arrange(RIGHT, buff=0.08)
                       for t, c in (("cost of revenue", HOST), ("engineering", ENG), ("sales and marketing", SALES), ("operating margin", PROFIT))]
                    ).arrange(RIGHT, buff=0.4).to_edge(UP, buff=1.05)
        hd = tx("cents of each revenue dollar, latest fiscal year", 21, WHITE, bold=True).to_edge(UP, buff=0.45)
        src = source("Forms 10-K via SEC company facts", size=12)
        beat(self,
             "Across the industry the shape repeats. <bookmark mark='a'/> Salesforce and ServiceNow, mature and profitable. "
             "<bookmark mark='b'/> CrowdStrike and Datadog, still investing: they spend between a quarter and almost half of "
             "their revenue on engineering. <bookmark mark='c'/> Snowflake, the most extreme, spends more on selling and "
             "engineering than it takes in after its costs, and loses money on every dollar. <bookmark mark='d'/> Atlassian "
             "and HubSpot show the two ways to sell: Atlassian, with half its revenue in engineering and a quarter in sales, "
             "and HubSpot the other way round.",
             base=[hd, key, src], steps=[VGroup(rows_[0], rows_[1]), VGroup(rows_[2], rows_[3]), rows_[4], VGroup(rows_[5], rows_[6])])

    def stock(self):
        Co = R["cost"]["companies"]
        names = ["Snowflake", "Atlassian", "CrowdStrike", "Datadog", "ServiceNow", "Salesforce", "Adobe"]
        items = [(n_, 100 * Co[n_]["sbc"], STOCK, f"{100 * Co[n_]['sbc']:.0f}c") for n_ in names]
        rows = hbars(items, max_value=36, x0=0.4, top=2.1, row=0.6, length=5.4, size=16, bar_h=0.36)
        hd = tx("stock given to employees, cents per dollar of revenue", 21, WHITE, bold=True).to_edge(UP, buff=0.5)
        note = tx("a real cost: it dilutes the owners, though no cash leaves the company", 17, GREY_B).to_edge(DOWN, buff=0.8)
        src = source("Forms 10-K via SEC company facts (share-based compensation)", size=12)
        beat(self,
             "There is a cost the income statement shows but the cash flow does not. <bookmark mark='a'/> Software companies "
             f"pay their people partly in shares. Snowflake handed out stock worth {100 * Co['Snowflake']['sbc']:.0f} cents for "
             f"every dollar of revenue, Atlassian {100 * Co['Atlassian']['sbc']:.0f}, <bookmark mark='b'/> the older companies "
             f"less: Salesforce {100 * Co['Salesforce']['sbc']:.0f}, Adobe {100 * Co['Adobe']['sbc']:.0f}. "
             "<bookmark mark='c'/> No cash leaves the company, so cash flow looks better than profit; but each share given "
             "away is a slice of the company the owners no longer have.",
             base=[rows.axis, hd, src], steps=[VGroup(*rows[:4]), VGroup(*rows[4:]), note])

    def why(self):
        lines = [("making one more copy costs almost nothing: gross margins mostly 70 to 90%", HOST),
                 ("the engineering is a fixed cost, paid before the first sale and every year after", ENG),
                 ("customers must be found one by one, and that is the biggest cost of all", SALES),
                 ("so the business is a bet that customers, once won, stay for years", PROFIT)]
        g = VGroup(*[tx(t, 19, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.1, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        beat(self,
             "So the economics run backwards from a factory's. <bookmark mark='a'/> Making one more copy costs almost "
             "nothing. <bookmark mark='b'/> The engineering is a fixed cost, paid before the first sale. "
             "<bookmark mark='c'/> Finding customers, one by one, is the biggest cost of all. <bookmark mark='d'/> So the "
             "whole business is a bet that customers, once won, stay for years.",
             base=[head("Why software's costs look the way they do")], steps=list(g))
