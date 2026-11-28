from __future__ import annotations

from videos.industry.industry35.common import *  # noqa: F403


class Light(VoiceoverScene):
    def construct(self):
        card(self, 4, "Why the brand owns nothing", "If owning hotels is good business, why did the brands sell them?",
             "Chapter four. Why the brand owns nothing. Marriott split itself in 1993. Hilton did the same in 2017. Why do the "
             "companies with the names keep giving away the buildings?", lit=("moat", "dollar"))
        self.roa()
        self.spin()
        self.pipe()
        self.why()

    def roa(self):
        L = R["light"]["roa"]
        order = [k for k in sorted(L, key=lambda k: -(L[k]["roa"] or -1)) if L[k]["roa"] is not None]
        items = [(k, L[k]["roa"], BRAND if L[k]["group"] == "brand" else OWNER, f"{L[k]['roa']:.1f}%") for k in order]
        rows = hbars(items, max_value=25, x0=0.6, top=2.3, row=0.52, length=5.6, size=15, bar_h=0.34)
        hd = tx("operating income on assets, median of the last five years", 20, WHITE, bold=True).to_edge(UP, buff=0.35)
        key = VGroup(tx("hotel brands", 16, BRAND, bold=True), tx("hotel owners", 16, OWNER, bold=True)).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.75)
        src = source("Forms 10-K and 20-F, via SEC company facts (Hyatt does not tag operating income)", size=12)
        brands = VGroup(*[rows[i] for i, k in enumerate(order) if L[k]["group"] == "brand"])
        owners = VGroup(*[rows[i] for i, k in enumerate(order) if L[k]["group"] == "owner"])
        beat(self,
             "Here is the arithmetic. <bookmark mark='a'/> The hotel brands, IHG, Choice, Marriott, Hilton and Wyndham, earned "
             "between twelve and twenty-two cents of operating income on each dollar of assets over the last five years. "
             "<bookmark mark='b'/> The companies that own hotels, Host, Park, Apple Hospitality and Ryman, earned between three "
             "and eight. The owner's money is tied up in concrete; the brand's is tied up in contracts, software and a name. "
             "<bookmark mark='c'/> In this series' reading, investors also prize steady fees more than the profits of "
             "buildings that rise and fall with every recession.",
             base=[rows.axis, hd, src], steps=[brands, owners, key])

    def spin(self):
        Hh = R["light"]["hlt_hist"]
        rev = {y: v[0] for y, v in Hh.items() if y >= 2017}
        op = {y: v[1] for y, v in Hh.items() if v[1] is not None and y >= 2017}
        ch = line_chart({"Hilton's revenue": (rev, BRAND), "its operating income": (op, GOOD)}, x=(2017, 2025), y=(0, 13),
                        xticks=[2017, 2019, 2021, 2023, 2025], yticks=[0, 4, 8, 12], yfmt=lambda v: f"${v:.0f}bn",
                        ylabel="Hilton, $bn a year (revenue includes reimbursed costs)", width=8.6, height=4.2, center=(-1.0, -0.45))
        mk = marker(ch.ax, 2017, rev[2017], "January 2017: its hotels spun off as Park", OWNER, side=RIGHT)
        mk[1].shift(DOWN * 0.45)
        P = R["light"]["pk"]
        note = tx(f"Park Hotels in 2025: revenue {bn(P['rev'], 2)}, net loss {bn(-P['ni'], 2)}", 16, OWNER).to_edge(DOWN, buff=0.75)
        src = source("Hilton Worldwide and Park Hotels & Resorts, Forms 10-K; SEC company facts", size=12)
        beat(self,
             "Hilton did it in one step. <bookmark mark='a'/> On 3 January 2017 it spun off the hotels it owned as a separate "
             "company, Park Hotels and Resorts, and its timeshare business as Hilton Grand Vacations. <bookmark mark='b'/> "
             "Since then, apart from the pandemic, its revenue has risen every year, and its operating income has gone from "
             f"{op[2017]:.1f} billion dollars in 2017 to {op[2025]:.1f} billion in 2025. "
             f"<bookmark mark='c'/> Park, which kept the buildings, had {P['rev']:.1f} billion dollars of revenue in 2025 and "
             f"lost {-P['ni'] * 1e3:.0f} million.",
             base=[ch.frame, src], steps=[mk, VGroup(*ch.lines.values(), *ch.labels.values()), note])

    def pipe(self):
        L = R["light"]
        c = stat_cards([(f"{L['pipe'] / 1e3:,.0f}k", "rooms in Marriott's pipeline", BRAND),
                        (f"{L['hl_pipe'] / 1e3:,.0f}k", "rooms in Hilton's pipeline", BRAND),
                        (f"{L['nug']:.1f}%", "Hilton's net unit growth, 2025", GOOD)], y=0.6, size=36, span=11.5)
        cranes = VGroup(*[draw.tower_crane(1.2) for _ in range(3)]).arrange(RIGHT, buff=1.4).move_to([0, -2.0, 0])
        note = tx(f"Marriott's rooms at the end of September 2026: {L['q3']:,}", 17, GREY_B).to_edge(DOWN, buff=0.4)
        src = source("Marriott International and Hilton Worldwide, Forms 10-K for 2025; Marriott, 10-Q for the third quarter of 2026", size=12)
        beat(self,
             "And they grow on other people's money. <bookmark mark='a'/> At the end of 2025 Marriott had nearly "
             f"{L['pipe'] / 1e3:.0f} thousand rooms in its pipeline of hotels signed or being built, <bookmark mark='b'/> "
             f"Hilton {L['hl_pipe'] / 1e3:.0f} thousand. <bookmark mark='c'/> Hilton's system grew {L['nug']:.1f} per cent in "
             "a year. Nearly all of those rooms are paid for by owners, who borrow to build them and then pay the brand a share "
             "of every night they sell. <bookmark mark='d'/> By September 2026 Marriott's system had "
             f"{L['q3'] / 1e6:.2f} million rooms.",
             base=[cranes, src], steps=[c[0], c[1], c[2], note])

    def why(self):
        lines = [("capital: owners pay for the buildings; the brand grows without borrowing", OWNER),
                 ("steadiness: fees on revenue fall less in a bad year than a building's profit", BRAND),
                 ("specialization: owners chase property returns, brands chase guests", AGENT),
                 ("the conflict: the brand earns on revenue, the owner on profit", BAD)]
        g = VGroup(*[tx(t, 19, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.1, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        beat(self,
             "Why does it work? In this series' reading, four reasons. <bookmark mark='a'/> Capital: the owners pay for the "
             "buildings, so the brand can add hundreds of hotels a year without borrowing for them. <bookmark mark='b'/> "
             "Steadiness: a share of revenue falls less in a recession than the profit of a hotel with a mortgage. "
             "<bookmark mark='c'/> Specialization: pension funds and property companies want buildings; the brand wants "
             "guests. <bookmark mark='d'/> And the conflict built into it: the brand is paid on revenue, the owner on what is "
             "left. More rooms in a city, or a costly new standard for every bathroom, can please the brand and hurt the owner.",
             base=[head("Why the brands sold the buildings")], steps=list(g))
