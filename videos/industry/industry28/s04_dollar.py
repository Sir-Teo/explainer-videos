from __future__ import annotations

from videos.industry.industry28.common import *  # noqa: F403


class Dollar(VoiceoverScene):
    def construct(self):
        card(self, 3, "Where the dollar goes", "What does an airline spend its fares on?",
             "Chapter three. Where the dollar goes. Delta, the most profitable of America's large airlines in 2025, spent "
             "fifty-seven billion dollars to fly. Here is where it went, and what happened in 2020, when the fares stopped "
             "and most of the costs did not.", lit=("dollar", "change"))
        self.bar()
        self.people()
        self.perhead()
        self.profit()
        self.april()
        self.stopped()
        self.rescue()

    def bar(self):
        D = R["dollar"]
        items = D["items"]
        top = items[:2]
        rest = sum(v for _, v in items[2:])
        parts = [("people", top[0][1] / D["total"], SKY), ("fuel", top[1][1] / D["total"], FUEL), ("everything else", rest / D["total"], ALL)]
        bar = viz.bar_split(parts, 1.0, width=12.0, height=0.9).move_to([0, 1.0, 0])
        labs = VGroup(*[VGroup(tx(f"{100 * v:.0f}%", 22, c, bold=True), tx(n, 15, GREY_A)).arrange(DOWN, buff=0.06).next_to(bar[i], DOWN, buff=0.2)
                        for i, (n, v, c) in enumerate(parts)])
        hd = tx(f"Delta, 2025: ${D['total']:.1f}bn of operating costs", 20, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("Delta Air Lines, Form 10-K for 2025: operating expense", size=12)
        beat(self,
             f"Of Delta's {D['total']:.1f} billion dollars of costs in 2025, <bookmark mark='a'/> "
             f"{100 * top[0][1] / D['total']:.0f} per cent went to its people: pilots, cabin crew, mechanics, agents, "
             f"{D['emp']:,.0f} of them. <bookmark mark='b'/> {100 * top[1][1] / D['total']:.0f} per cent went on fuel. "
             "<bookmark mark='c'/> The rest was everything else it takes to fly, which the next picture opens up.",
             base=[hd, src], steps=[[bar[0], labs[0]], [bar[1], labs[1]], [bar[2], labs[2]]])

    def people(self):
        D = R["dollar"]
        items = [(n, v, SKY if n == "people" else (FUEL if n == "fuel" else ALL), f"${v:.1f}bn") for n, v in D["items"]]
        rows = hbars(items, max_value=18, x0=-0.2, top=2.7, row=0.42, length=6.6, size=14, bar_h=0.28)
        src = source("Delta Air Lines, Form 10-K for 2025: operating expense", size=12)
        beat(self,
             "In full: <bookmark mark='a'/> people and fuel, <bookmark mark='b'/> then the refinery Delta owns and the other "
             "businesses it runs, the contractors who clean, cater and handle bags, the airports' landing fees and rents, "
             "the regional airlines that fly its small planes, the commissions to travel agents and booking systems, the "
             "wear on the aircraft, their maintenance, the meals, the profit-sharing paid to employees, and the rent on "
             "aircraft it leases. <bookmark mark='c'/> Almost all of it is spent whether the planes are full or not.",
             base=[src], steps=[VGroup(*rows[:2]), VGroup(*rows[2:11]), VGroup(*rows[11:])])

    def perhead(self):
        D = R["dollar"]
        sal = dict(D["items"])["people"]
        ps = get("dl28.cost.profitsharing") / 1e3
        c = stat_cards([(f"${sal:.1f}bn", "salaries, wages and benefits", SKY), (f"{D['emp']:,.0f}", "full-time equivalent staff", ALL),
                        (f"${1e9 * sal / D['emp'] / 1e3:,.0f}k", "a head, all costs of employment", SKY),
                        (f"${1e9 * ps / D['emp'] / 1e3:,.0f}k", "a head, profit-sharing", GOOD)], y=0.4, size=34, span=12.4)
        tag = estimate_tag("this series' arithmetic from Delta's Form 10-K for 2025: totals divided by staff", size=12)
        beat(self,
             f"Per person: <bookmark mark='a'/> {sal:.1f} billion dollars of pay and benefits, <bookmark mark='b'/> shared by "
             f"about {D['emp']:,.0f} people, <bookmark mark='c'/> is roughly {1e9 * sal / D['emp'] / 1e3:,.0f} thousand "
             "dollars each, counting pensions, health care and payroll taxes. <bookmark mark='d'/> On top, Delta paid "
             f"{ps:.2f} billion in profit-sharing, about {1e9 * ps / D['emp'] / 1e3:,.0f} thousand a head. In a good year an "
             "airline's people take a large share of what is left; in a bad one, the costs stay.",
             base=[tag], steps=[c[0], c[1], c[2], c[3]])

    def profit(self):
        D = R["dollar"]
        parts = [("costs", D["total"] / D["revenue"], BAD), ("operating profit", 1 - D["total"] / D["revenue"], GOOD)]
        bar = viz.bar_split(parts, 1.0, width=12.0, height=0.9).move_to([0, 0.6, 0])
        labs = VGroup(*[VGroup(tx(f"{100 * v:.0f}c", 22, c, bold=True), tx(n, 15, GREY_A)).arrange(DOWN, buff=0.06).next_to(bar[i], DOWN, buff=0.2)
                        for i, (n, v, c) in enumerate(parts)])
        note = tx(f"net income: ${D['profit']:.1f}bn on ${D['revenue']:.1f}bn of revenue", 19, GOOD, bold=True).move_to([0, -1.8, 0])
        src = source("Delta Air Lines, Form 10-K for 2025 and SEC company facts", size=12)
        beat(self,
             f"Against {D['revenue']:.1f} billion dollars of revenue, <bookmark mark='a'/> the costs took "
             f"{100 * D['total'] / D['revenue']:.0f} cents of each dollar, <bookmark mark='b'/> leaving "
             f"{100 * (1 - D['total'] / D['revenue']):.0f} cents of operating profit. <bookmark mark='c'/> After interest and "
             f"tax, {D['profit']:.1f} billion: the best result of any large American airline that year, and still only about "
             "eight cents on the dollar.",
             base=[src], steps=[[bar[0], labs[0]], [bar[1], labs[1]], note])

    def april(self):
        P = R["pandemic"]
        lf = P["lf_m"]
        items = [(m[2:4] + "/" + m[5:7] if m[5:7] in ("01", "04", "07", "10") else "", v,
                  BAD if v < 60 else (FUEL if v < 78 else SKY), f"{v:.0f}" if m in ("2020-01", "2020-04", "2021-07") else "")
                 for m, v in lf.items()]
        cols = vbars(items, base_y=-2.2, height=3.8, width=0.24, gap=0.1, size=12, max_value=100)
        lab = tx("American airlines' load factor, per cent, July 2019 to December 2021 (each month)", 16, GREY_A).to_edge(UP, buff=0.8)
        src = source("Bureau of Transportation Statistics, load factor, US air carriers (monthly), via FRED", size=12)
        i20 = list(lf).index("2020-03")
        i21 = list(lf).index("2021-06")
        beat(self,
             "In 2020 the industry ran an experiment on itself. <bookmark mark='a'/> Through 2019 American airlines flew "
             f"their planes more than four-fifths full. <bookmark mark='b'/> In April 2020 the share was {lf['2020-04']:.0f} per "
             "cent: of every seven seats flown, six were empty, and many more flights were not flown at all. "
             "<bookmark mark='c'/> It took until the summer of 2021 to get back above eighty per cent.",
             base=[lab, src], steps=[VGroup(*cols[:i20]), VGroup(*cols[i20:i21]), VGroup(*cols[i21:])])

    def stopped(self):
        F = R["pandemic"]["firms"]
        rows = VGroup()
        for i, (name, v) in enumerate(F.items()):
            y = 1.6 - 1.05 * i
            b1 = Rectangle(width=0.12 * v["rev19"], height=0.3, stroke_width=0, fill_color=GREY_B, fill_opacity=0.6)
            b1.move_to([-3.0 + 0.06 * v["rev19"], y + 0.18, 0])
            b2 = Rectangle(width=0.12 * v["rev20"], height=0.3, stroke_width=0, fill_color=SKY, fill_opacity=0.9)
            b2.move_to([-3.0 + 0.06 * v["rev20"], y - 0.18, 0])
            ls = VGroup(tx(name, 18, WHITE, bold=True).move_to([-4.7, y, 0]),
                        tx(f"2019: ${v['rev19']:.1f}bn", 13, GREY_B).next_to(b1, RIGHT, buff=0.1),
                        tx(f"2020: ${v['rev20']:.1f}bn", 13, SKY, bold=True).next_to(b2, RIGHT, buff=0.1),
                        tx(f"operating loss ${abs(v['op20']):.1f}bn", 15, BAD, bold=True).move_to([5.4, y, 0]))
            rows.add(VGroup(b1, b2, ls))
        lab = tx("revenue, 2019 and 2020, and the operating loss of 2020", 17, GREY_A).to_edge(UP, buff=0.7)
        src = source("Forms 10-K via SEC company facts", size=12)
        d = F["Delta"]
        beat(self,
             f"What did it do to the money? <bookmark mark='a'/> Delta's revenue fell from {d['rev19']:.0f} billion dollars "
             f"in 2019 to {d['rev20']:.0f} billion, and it lost {abs(d['op20']):.1f} billion before interest and tax. "
             "<bookmark mark='b'/> United, American and Southwest the same: revenue down by three-fifths or more, and "
             "billions lost each. Fuel fell with the flying, but the aircraft, the airports, the debts and most of the "
             "people still had to be paid. That is what a fixed cost means.",
             base=[lab, src], steps=[rows[0], VGroup(*rows[1:])])

    def rescue(self):
        P = R["pandemic"]
        q = quote(["'... to preserve aviation jobs and compensate air carrier industry workers, the Secretary shall provide",
                   "financial assistance that shall exclusively be used for the continuation of payment of employee wages,",
                   "salaries, and benefits to (1) passenger air carriers, in an aggregate amount up to $25,000,000,000'"],
                  "the CARES Act, Public Law 116-136, section 4112, 27 March 2020", size=17).move_to([0, 1.5, 0])
        c = stat_cards([(f"${P['psp']:.0f}bn", "for passenger airlines' payrolls", GOOD),
                        (f"{P['enplane'][2020]:.0f}m", "passengers in 2020", BAD),
                        (f"{P['enplane'][2019]:.0f}m", "in 2019", ALL)], y=-1.2, size=40, span=11)
        src = source("Public Law 116-136, section 4112 (govinfo); BTS enplanements via FRED; Delta Air Lines, Form 10-K for 2025", size=12)
        beat(self,
             "And then the government stepped in. <bookmark mark='a'/> In March 2020 Congress set aside up to "
             f"{P['psp']:.0f} billion dollars for passenger airlines, to be used only to keep paying their workers, with more "
             "for cargo airlines and contractors. <bookmark mark='b'/> That year American airlines carried "
             f"{P['enplane'][2020]:.0f} million passengers, against {P['enplane'][2019]:.0f} million the year before. "
             "<bookmark mark='c'/> An industry whose costs are fixed in advance could not shrink as fast as its customers "
             "vanished, so the taxpayer carried part of the fixed cost for a while. Some of the help came as loans, and "
             "Delta's report for 2025 records it repaying its payroll-support loans early.",
             base=[src], steps=[q, c[0], VGroup(c[1], c[2])])
