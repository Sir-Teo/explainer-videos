from __future__ import annotations

from videos.industry.industry26.common import *  # noqa: F403


class Office(VoiceoverScene):
    def construct(self):
        card(self, 6, "Offices after 2020", "What happens to a building when its tenants need less of it?",
             "Chapter six. Offices after 2020. For a century the office was the safest kind of commercial building. Then "
             "its tenants discovered they could work from home.", lit=("change", "moat"))
        self.bxp()
        self.cities()
        self.rents()
        self.weakest()
        self.labs()
        self.quality()

    def bxp(self):
        O = R["office"]
        occ = dict(O["bxp"])
        occ[2026.75] = O["q3"]
        ch = line_chart({"BXP's offices, share let": (occ, OFFICE)}, x=(2017, 2027), y=(84, 95), xticks=[2017, 2019, 2021, 2023, 2025, 2027],
                        yticks=[84, 86, 88, 90, 92, 94], yfmt=lambda v: f"{v:.0f}%", xfmt=lambda v: f"{int(v)}",
                        ylabel="BXP: in-service portfolio occupancy, end of each year, and September 2026", width=9.0,
                        height=4.4, center=(-1.0, -0.45), label_end=False)
        m1 = marker(ch.ax, 2019, occ[2019], f"2019: {occ[2019]:.1f}%", GOOD, side=UP)
        m2 = marker(ch.ax, 2025, occ[2025], f"2025: {occ[2025]:.1f}%", BAD, side=DOWN)
        m3 = marker(ch.ax, 2026.75, O["q3"], f"Sept 2026: {O['q3']:.1f}%", VALUE, side=UP)
        tower = draw.office_tower(0.9).move_to([5.8, 0.2, 0])
        draw.light(tower.windows, occ[2025] / 100)
        src = source("BXP, Inc. (Boston Properties), Forms 10-K for 2017-2025; Form 8-K of 27 October 2026", size=12)
        beat(self,
             f"BXP owns {O['sqft']:.1f} million square feet of some of America's best offices, in Boston, New York, San "
             f"Francisco, Los Angeles, Seattle and Washington. <bookmark mark='a'/> At the end of 2019 its buildings were "
             f"{occ[2019]:.1f} per cent let. <bookmark mark='b'/> Occupancy then fell every year for six years, to "
             f"{occ[2025]:.1f} per cent at the end of 2025. <bookmark mark='c'/> In 2026 it began to climb: "
             f"{O['q3']:.1f} per cent by September, the fourth quarterly rise in a row, with {O['leased']:.1f} per cent signed.",
             base=[ch.frame, tower, src], steps=[[ch.lines["BXP's offices, share let"], m1], m2, m3])

    def cities(self):
        items = [("Boston", get("bxp.occ.boston"), GOOD), ("Washington, DC", get("bxp.occ.dc"), GOOD),
                 ("Los Angeles", get("bxp.occ.la"), VALUE), ("New York", get("bxp.occ.ny"), VALUE),
                 ("Seattle", get("bxp.occ.seattle"), BAD), ("San Francisco", get("bxp.sf"), BAD)]
        rows = hbars([(n, v, c, f"{v:.1f}%") for n, v, c in items], max_value=100, x0=-0.6, top=2.0, row=0.7, length=6.4,
                     size=17, bar_h=0.42)
        lab = tx("BXP: share of its offices let in each city, end of 2025", 17, GREY_A).to_edge(UP, buff=0.7)
        src = source("BXP, Inc., Form 10-K for 2025", size=12)
        beat(self,
             "The average hides the cities. <bookmark mark='a'/> In Boston and Washington BXP's buildings were more than "
             f"ninety per cent let at the end of 2025. <bookmark mark='b'/> In Los Angeles and New York, about "
             f"{get('bxp.occ.la'):.0f} and {get('bxp.occ.ny'):.0f}. <bookmark mark='c'/> In Seattle and San Francisco, "
             f"{get('bxp.occ.seattle'):.0f} and {get('bxp.sf'):.0f}: nearly a quarter of the space "
             "empty.",
             base=[lab, src], steps=[VGroup(*rows[:2]), VGroup(*rows[2:4]), VGroup(*rows[4:])])

    def rents(self):
        items = [("Boston", get("bxp.renew.boston"), GOOD, f"{get('bxp.renew.boston'):+.1f}%"),
                 ("all BXP", get("bxp.renew"), BAD, f"{get('bxp.renew'):+.1f}%"),
                 ("San Francisco", get("bxp.renew.sf"), BAD, f"{get('bxp.renew.sf'):+.1f}%")]
        rows = hbars(items, max_value=32, x0=0.0, top=1.2, row=1.0, length=4.8, size=18, bar_h=0.5)
        lab = tx("BXP: cash rent on leases that began in 2025, against the old lease on the same space", 16, GREY_A).to_edge(UP, buff=0.8)
        src = source("BXP, Inc., Form 10-K for 2025: change in second-generation cash rents, net", size=12)
        beat(self,
             "And the rents. When a lease ends and the space is let again, BXP reports the new rent against the old. "
             f"<bookmark mark='a'/> In Boston, new leases in 2025 paid {get('bxp.renew.boston'):.0f} per cent more. "
             f"<bookmark mark='b'/> Across the whole company, {abs(get('bxp.renew')):.1f} per cent less. "
             f"<bookmark mark='c'/> In San Francisco, {abs(get('bxp.renew.sf')):.0f} per cent less: a tenant renewing there "
             "paid about two-thirds of what the space had fetched before. Lower occupancy and lower rent together are Run "
             "it's office.",
             base=[lab, src], steps=[rows[0], rows[1], rows[2]])

    def weakest(self):
        O = R["office"]
        H = O["hpp_pl"]
        items = [(str(y), H[y][1], GOOD if H[y][1] > 0 else BAD, f"{H[y][1]:+.2f}") for y in range(2019, 2026)]
        cols = vbars([(a, abs(b), c, d) for a, b, c, d in items], base_y=-1.8, height=2.8, width=0.75, gap=0.4, size=14, max_value=0.7)
        cols.shift(LEFT * 2.4)
        lab = tx("Hudson Pacific: net income, $bn a year", 16, GREY_A).next_to(cols, UP, buff=0.5)
        c = stat_cards([(f"{O['hpp']:.1f}%", "of its offices let, end of 2025", BAD)], y=0.8, size=40, span=4)
        c.shift(RIGHT * 4.2)
        src = source("Hudson Pacific Properties, Form 10-K for 2025 and Forms 10-K via SEC company facts", size=12)
        beat(self,
             "Lower down the market it is worse. <bookmark mark='a'/> Hudson Pacific owns offices and film studios, "
             f"mostly on America's west coast. It earned a small profit in 2019, 2020 and 2021, then lost money four years running, "
             f"{abs(H[2025][1]):.2f} billion dollars in 2025 alone, on revenue of {H[2025][0]:.2f} billion. "
             f"<bookmark mark='b'/> At the end of 2025 only {O['hpp']:.1f} per cent of its offices were let.",
             base=[lab, src], steps=[cols, c])

    def labs(self):
        A = R["office"]["are"]
        items = [(str(y), (A[y][2] or 0), BAD if (A[y][2] or 0) > 0.3 else VALUE, f"${(A[y][2] or 0):.2f}bn") for y in range(2019, 2026)]
        cols = vbars(items, base_y=-1.8, height=3.0, width=0.8, gap=0.45, size=14, max_value=2.4)
        lab = tx("Alexandria Real Estate Equities: impairment charges, a year", 16, GREY_A).to_edge(UP, buff=0.8)
        flask = draw.flask(0.9).move_to([5.6, 1.2, 0])
        src = source("Alexandria Real Estate Equities, Forms 10-K via SEC company facts", size=12)
        beat(self,
             "It is not only desks. <bookmark mark='a'/> Alexandria lets laboratories to drug and biotechnology companies. "
             f"Its revenue doubled, from {A[2019][0]:.1f} billion dollars in 2019 to {A[2024][0]:.1f} billion in 2024, as it "
             f"built. Then it wrote its buildings down: {A[2023][2]:.2f} billion dollars in 2023 and {A[2025][2]:.1f} billion "
             f"in 2025, when it lost {abs(A[2025][1]):.1f} billion. A laboratory is an office with plumbing, and it met the "
             "same arithmetic.",
             base=[lab, flask, src], steps=[cols])

    def quality(self):
        G = R["hook"]["gmv"]
        rows = VGroup(
            tx(f"SL Green: Manhattan same-store offices {get('slg.occ'):.1f}% let, end of 2025", 19, GOOD, bold=True),
            tx("BXP: 'new office construction has effectively halted'", 19, VALUE, bold=True),
            tx(f"the model of 2022: New York office values {G['short']:.0f}% in 2020, {G['long']:.0f}% in the long run", 19, BAD, bold=True),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.4, 0])
        towers = VGroup(*[draw.office_tower(0.6, seed=s) for s in (1, 2, 3, 4)]).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.9)
        for t, s in zip(towers, (0.95, 0.9, 0.6, 0.5)):
            draw.light(t.windows, s)
        src = source("SL Green Realty, Form 10-K for 2025; BXP, Inc., Form 10-K for 2025; Gupta, Mittal and Van Nieuwerburgh (2022)", size=12)
        beat(self,
             "So the office has split in two. <bookmark mark='a'/> The newest towers in the best places are filling: SL "
             f"Green's Manhattan buildings were {get('slg.occ'):.1f} per cent let, counting leases signed but not yet begun. "
             "<bookmark mark='b'/> Almost nothing new is being built, so, in this series' reading, as old buildings empty, "
             "tenants crowd into the good ones. <bookmark mark='c'/> The 2022 study expected this, a flight to quality, with "
             "lower-quality buildings seeing 'much more dramatic swings' than the best. In this series' reading the office is "
             "not dead; the second-rate office may be.",
             base=[towers, src], steps=[rows[0], rows[1], rows[2]])
