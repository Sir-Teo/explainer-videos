from __future__ import annotations

from videos.industry.industry26.common import *  # noqa: F403


class Owners(VoiceoverScene):
    def construct(self):
        card(self, 8, "Who owns them, and who runs them", "Who owns the buildings, and who earns from looking after them?",
             "Chapter eight. Who owns them, and who runs them. A building has an owner, a lender, a manager, a leasing agent "
             "and a cleaner, and they are rarely the same company.", lit=("dollar", "moat"))
        self.reit()
        self.blackstone()
        self.breit()
        self.cbre()
        self.services()

    def reit(self):
        q = quote(["'To qualify as a REIT, we are required each year to distribute at least 90% of our REIT taxable income'"],
                  "Prologis, Inc., Form 10-K for 2025", size=18).move_to([0, 1.8, 0])
        g = VGroup(VGroup(draw.office_tower(0.7), draw.warehouse(1.6), draw.mall(1.6)).arrange(RIGHT, buff=0.3),
                   Arrow(LEFT, RIGHT, stroke_color=GREY_B),
                   VGroup(draw.coin_stack(5, r=0.22), tx("90% to shareholders", 16, VALUE, bold=True)).arrange(DOWN, buff=0.15)
                   ).arrange(RIGHT, buff=0.5).move_to([0, -0.7, 0])
        div = tx(f"Realty Income's dividend: {get('o.divyield'):.1f}% of its share price, end of 2025", 17, INCOME).to_edge(DOWN, buff=0.8)
        src = source("Prologis, Inc. and Realty Income Corporation, Forms 10-K for 2025", size=12)
        beat(self,
             "Most of the companies in this film are real estate investment trusts. <bookmark mark='a'/> An American REIT "
             "pays no corporate income tax, so long as it hands at least ninety per cent of its taxable income to its "
             "shareholders every year. <bookmark mark='b'/> So it cannot grow from its own profits the way other companies do: "
             "to buy or build it must borrow or sell new shares. That makes a REIT's cost of money, the price of its shares "
             f"and its bonds, the heart of its business. <bookmark mark='c'/> Realty Income's dividend, for instance, was "
             f"{get('o.divyield'):.1f} per cent of its share price at the end of 2025.",
             base=[src], steps=[q, g, div])

    def blackstone(self):
        O = R["owners"]
        c = VGroup(stat_cards([(f"${O['bx']:.0f}bn", "real estate managed by Blackstone, end of 2025", VALUE),
                               (f"${R['sectors'][0]['assets']:.0f}bn", "Prologis's total assets, for scale", SHED)], y=1.6, size=38, span=9.0),
                   stat_cards([(f"${O['listed']:.1f}tn", "total assets of all the listed owners in this film", INCOME),
                               (f"${O['fsr_cre'] / 1e3:.1f}tn", "all American commercial property, the Federal Reserve's count", ALL)],
                              y=-0.4, size=38, span=9.0))
        sky = draw.skyline(5.0).move_to([0, -2.4, 0]).scale(0.6)
        draw.light(sky.windows, 0.8)
        src = source("Blackstone Inc. and Prologis, Inc., Forms 10-K for 2025; SEC company facts; Federal Reserve, Financial Stability Report, November 2026", size=12)
        beat(self,
             "Not every owner is listed. <bookmark mark='a'/> Blackstone, a private investment firm, managed "
             f"{O['bx']:.0f} billion dollars of real estate at the end of 2025, on behalf of investors that, in its words, "
             "include pension funds, insurance companies and individual investors. <bookmark mark='b'/> That is more than "
             "three times the assets of Prologis, the largest listed landlord. <bookmark mark='c'/> And all the listed owners in this film "
             f"together hold about {O['listed']:.1f} trillion dollars of assets, against {O['fsr_cre'] / 1e3:.1f} trillion "
             "for all American commercial property in the Federal Reserve's count: most buildings are owned outside the "
             "stock market.",
             base=[sky, src], steps=[c[0][0], c[0][1], c[1]])

    def breit(self):
        q = quote(["'market volatility drove a material increase in BREIT repurchase requests beginning in late 2022, and",
                   "pursuant to the terms of the vehicle, BREIT began to prorate such requests beginning in November 2022'"],
                  "Blackstone Inc., Form 10-K for 2025", size=17).move_to([0, 1.7, 0])
        why = bullets(["a listed REIT's price changes every second; an unlisted fund's value is an appraisal, revised slowly",
                       "when listed prices fell in 2022, the unlisted fund still looked worth what it had",
                       "investors who could, asked for their money back at the higher value; the fund had to ration them"],
                      size=17).move_to([0, -0.8, 0])
        tag = estimate_tag("this series' reading of listed against appraised values", size=12)
        beat(self,
             "And unlisted owners face the same arithmetic, more slowly. <bookmark mark='a'/> Blackstone's property fund for "
             "individual investors, BREIT, saw a rush of requests to withdraw money in late 2022, and from November 2022 paid "
             "out only part of what was asked. <bookmark mark='b'/> In this series' reading, the reason is the formula: listed "
             "property shares are priced every second, at today's rates; an unlisted fund is valued by appraisers who move "
             "slowly. When rates jumped, the listed prices fell at once, the appraisals did not, and investors who could leave "
             "at the appraised value tried to.",
             base=[tag], steps=[q, why])

    def cbre(self):
        C = R["owners"]["cbre"]
        parts = [("running clients' buildings", C["fm"] / 100, SHED), ("managing construction projects", C["pm"] / 100, OFFICE),
                 ("leasing", C["lease"] / 100, INCOME), ("selling buildings", C["sales"] / 100, VALUE),
                 ("everything else", 1 - (C["fm"] + C["pm"] + C["lease"] + C["sales"]) / 100, ALL)]
        bar = viz.bar_split(parts, 1.0, width=12.4, height=0.9).move_to([0, 0.6, 0])
        labs = VGroup(*[VGroup(tx(f"{100 * v:.0f}%", 20, c, bold=True), tx(n, 13, GREY_A)).arrange(DOWN, buff=0.06).next_to(bar[i], DOWN, buff=0.2)
                        for i, (n, v, c) in enumerate(parts)])
        hd = tx(f"CBRE, 2025: ${C['rev']:.1f}bn of revenue", 22, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("CBRE Group, Inc., Form 10-K for 2025", size=12)
        beat(self,
             "Then there are the companies that look after buildings for their owners. The largest, CBRE, took in "
             f"{C['rev']:.1f} billion dollars in 2025. <bookmark mark='a'/> Half of it, {C['fm']:.0f} per cent, came from "
             "running other companies' buildings and offices: cleaning, maintenance, security, energy. "
             f"<bookmark mark='b'/> {C['pm']:.0f} per cent from managing building projects. <bookmark mark='c'/> Leasing, the "
             f"business of finding tenants, {C['lease']:.0f} per cent, <bookmark mark='d'/> and selling buildings only "
             f"{C['sales']:.0f}. <bookmark mark='e'/> The largest name in commercial property is mostly a services company.",
             base=[hd, src], steps=[[bar[i], labs[i]] for i in range(5)])

    def services(self):
        S = R["owners"]["svc"]
        series = {k: ({y: 100 * v[y][1] for y in v}, c) for (k, v), c in zip(S.items(), (VALUE, OFFICE, SHOP))}
        ch = line_chart(series, x=(2019, 2025), y=(-4, 8), xticks=[2019, 2021, 2023, 2025], yticks=[-4, 0, 4, 8],
                        yfmt=lambda v: f"{v:.0f}%", ylabel="net income per dollar of revenue", width=9.0, height=4.4,
                        center=(-1.0, -0.45), nudge={"JLL": -0.2})
        zero = DashedLine(ch.ax.c2p(2019, 0), ch.ax.c2p(2025, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        pt = tx(f"{R['owners']['cbre']['passthrough']:.0f}% of CBRE's revenue is passed straight through: mostly wages of staff in clients' buildings",
                14, GREY_B).to_edge(UP, buff=0.5)
        src = source("CBRE, JLL and Cushman & Wakefield, Forms 10-K via SEC company facts; CBRE Form 10-K for 2025", size=12)
        cb = S["CBRE"]
        beat(self,
             "And they keep little of it. <bookmark mark='a'/> CBRE kept "
             f"{100 * cb[2025][1]:.1f} cents of each dollar in 2025, JLL {100 * S['JLL'][2025][1]:.1f}, and Cushman & "
             f"Wakefield under one. <bookmark mark='b'/> {R['owners']['cbre']['passthrough']:.0f} per cent of CBRE's revenue is "
             "passed straight through, mostly the wages of people working in its clients' buildings. The owners keep the "
             "rent; the people who look after the buildings keep a fee.",
             base=[ch.frame, zero, src], steps=[[ch.lines[k] for k in S] + [ch.labels[k] for k in S], pt])
