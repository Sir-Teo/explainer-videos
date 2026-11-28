from __future__ import annotations

from videos.industry.industry30.common import *  # noqa: F403


class Towers(VoiceoverScene):
    def construct(self):
        card(self, 5, "The landlord of the air", "Who makes money from the towers?",
             "Chapter five. The landlord of the air. Much of the time a carrier's antennas hang on a tower someone else "
             "owns: a company whose business is owning towers, and whose biggest customers are the carriers.", lit=("moat", "dollar"))
        self.amt()
        self.us()
        self.tenants()
        self.world()
        self.margins()

    def amt(self):
        T = R["towers"]
        tw = VGroup(*[draw.cell_tower(1.8) for _ in range(5)]).arrange(RIGHT, buff=0.6).move_to([0, 1.6, 0])
        c = stat_cards([(f"{T['sites']:,.0f}", "American Tower's sites worldwide", TOWER), (f"{T['us_sites']:,.0f}", "in the US and Canada", ALL),
                        (f"${T['per_site'] / 1e3:,.0f}k", "revenue a site a year there", GOOD), (f"${T['opex_site'] / 1e3:,.1f}k", "operating costs a site", BAD)],
                       y=-1.3, size=34, span=12.6)
        src = source("American Tower, Form 10-K for 2025: U.S. & Canada property segment", size=12)
        beat(self,
             f"<bookmark mark='a'/> American Tower owned {T['sites']:,.0f} communications sites at the end of 2025, "
             f"<bookmark mark='b'/> {T['us_sites']:,.0f} of them in the United States and Canada. <bookmark mark='c'/> "
             f"Each of those brought in about {T['per_site'] / 1e3:,.0f} thousand dollars a year, <bookmark mark='d'/> and "
             f"cost about {T['opex_site'] / 1e3:,.0f} thousand to run: ground rent, power and upkeep.",
             base=[tw, src], steps=[c[0], c[1], c[2], c[3]])

    def us(self):
        T = R["towers"]
        parts = [("costs", T["us_opex"] / T["us_rev"], BAD), ("segment operating profit", T["us_profit"] / T["us_rev"], GOOD),
                 ("overheads", 1 - (T["us_opex"] + T["us_profit"]) / T["us_rev"], ALL)]
        bar = viz.bar_split(parts, 1.0, width=12.0, height=0.9).move_to([0, 0.6, 0])
        labs = VGroup(*[VGroup(tx(f"{100 * v:.0f}c", 22, c, bold=True), tx(n, 14, GREY_A)).arrange(DOWN, buff=0.06).next_to(bar[i], DOWN, buff=0.2)
                        for i, (n, v, c) in enumerate(parts)])
        hd = tx(f"American Tower, US and Canada, 2025: a dollar of its ${T['us_rev'] / 1e3:.2f}bn of property revenue", 20, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("American Tower, Form 10-K for 2025: U.S. & Canada property segment", size=12)
        beat(self,
             f"Put that together for the whole American business. <bookmark mark='a'/> Of each dollar of rent, about "
             f"{100 * parts[0][1]:.0f} cents went on running the sites; <bookmark mark='b'/> "
             f"{100 * parts[1][1]:.0f} cents was left as the segment's operating profit, <bookmark mark='c'/> before a "
             "few cents of overheads, depreciation and interest. Few businesses anywhere keep so much of what they take in.",
             base=[hd, src], steps=[VGroup(bar[0], labs[0]), VGroup(bar[1], labs[1]), VGroup(bar[2], labs[2])])

    def tenants(self):
        T = R["towers"]
        B = T["by_tenants"]
        towers = VGroup()
        for n in (1, 2, 3):
            t = draw.cell_tower(2.0)
            for i, a in enumerate(t.antennas):
                if i // 2 >= n:
                    a.set_fill(opacity=0.12)
            towers.add(VGroup(t, tx(f"{n} tenant{'s' if n > 1 else ''}", 16, WHITE, bold=True).next_to(t, DOWN, buff=0.15),
                              tx(f"{100 * B[n]['yld']:.0f}% a year", 22, GOOD if n > 1 else ALL, bold=True).next_to(t, DOWN, buff=0.6)))
        towers.arrange(RIGHT, buff=1.6).move_to([0, 0.4, 0])
        tag = estimate_tag(f"the Works: a ${T['build'] / 1e3:.0f}k tower, ${T['rent'] / 1e3:.0f}k a year a tenant (assumptions), "
                           f"${T['opex_site'] / 1e3:.1f}k a year to run (American Tower's average)", size=12)
        beat(self,
             "Why is that such a good business? Because a tower costs almost the same with one tenant or four. "
             f"<bookmark mark='a'/> In the Works, a tower costs {T['build'] / 1e3:.0f} thousand dollars to build and each "
             f"tenant pays {T['rent'] / 1e3:.0f} thousand a year: with one tenant it returns "
             f"{100 * B[1]['yld']:.0f} per cent a year. <bookmark mark='b'/> Add a second carrier's antennas and it returns "
             f"{100 * B[2]['yld']:.0f}. <bookmark mark='c'/> A third, {100 * B[3]['yld']:.0f}. At American Tower's revenue "
             f"per site, the average American tower carries about {T['implied']:.1f} tenants at this rent. Every new tenant "
             "is almost pure profit, and the carriers, competing with each other, keep needing more antennas on the same "
             "towers.",
             base=[tag], steps=[towers[0], towers[1], towers[2]])

    def world(self):
        items = [("U.S. & Canada", 5248.7, TOWER, "$5.25bn"), ("Latin America", 1642.6, FOREIGN, "$1.64bn"),
                 ("Africa & Asia-Pacific", 1422.9, FOREIGN, "$1.42bn"), ("Data centers", 1053.1, EQUIP, "$1.05bn"),
                 ("Europe", 937.7, FOREIGN, "$0.94bn")]
        rows = hbars(items, max_value=5600, x0=0.4, top=1.8, row=0.8, length=5.4, size=17, bar_h=0.42)
        lab = tx("American Tower: property revenue by segment, 2025", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("American Tower, Form 10-K for 2025", size=12)
        beat(self,
             "The same model works anywhere phones are spreading. <bookmark mark='a'/> American Tower's sites in the "
             "United States and Canada brought in 5.25 billion dollars in 2025. <bookmark mark='b'/> Latin America, Africa, "
             "Asia and Europe together brought in about four billion more, and it has added data centers, the next kind "
             "of building every network needs.",
             base=[rows.axis, lab, src], steps=[rows[0], VGroup(*rows[1:])])

    def margins(self):
        T = R["towers"]
        tm = R["three"]["margins"]["T-Mobile"]
        ch = line_chart({"American Tower": (T["amt_margin"], TOWER), "T-Mobile": (tm, WIRELESS)}, x=(2015, 2025),
                        y=(0, 50), xticks=[2015, 2017, 2019, 2021, 2023, 2025], yticks=[0, 10, 20, 30, 40, 50],
                        yfmt=lambda v: f"{v:.0f}%", ylabel="operating profit per dollar of revenue", width=9.0, height=4.4,
                        center=(-1.2, -0.45))
        src = source("Forms 10-K via SEC company facts; American Tower, Form 10-K for 2025 (significant customers, churn)", size=12)
        beat(self,
             f"<bookmark mark='a'/> American Tower kept {T['amt_margin'][2025]:.0f} cents of operating profit per dollar in "
             f"2025. <bookmark mark='b'/> Its biggest tenant, T-Mobile, which paid {get('amt30.tmus'):.0f} per cent of its "
             f"revenue, kept {tm[2025]:.0f}; AT&T paid {get('amt30.att'):.0f} per cent and Verizon {get('amt30.vz'):.0f}. "
             "The tenants come and go "
             f"slowly: lost rent was about {T['churn']:.0f} per cent of American Tower's billings in 2025. As with ships and "
             "aircraft, the steadiest money is in owning the asset everyone needs and renting it out.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["American Tower"], ch.labels["American Tower"]),
                                         VGroup(ch.lines["T-Mobile"], ch.labels["T-Mobile"])])
