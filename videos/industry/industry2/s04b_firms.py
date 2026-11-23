from __future__ import annotations

from videos.industry.industry2.common import *  # noqa: F403

SECTOR_SHORT = {"Retail Trade": "Retail", "Transportation and Warehousing": "Transport and warehouses",
                "Management of Companies and Enterprises": "Head offices",
                "Administrative and Support and Waste Management and Remediation Services": "Admin and waste",
                "Information": "Information", "Finance and Insurance": "Finance and insurance", "Utilities": "Utilities",
                "Health Care and Social Assistance": "Health care", "Professional, Scientific, and Technical Services":
                "Professional services", "Manufacturing": "Manufacturing", "Accommodation and Food Services":
                "Hotels and restaurants", "Wholesale Trade": "Wholesale", "Educational Services": "Education",
                "Arts, Entertainment, and Recreation": "Arts and recreation", "Real Estate and Rental and Leasing":
                "Real estate", "Mining, Quarrying, and Oil and Gas Extraction": "Mining, oil and gas",
                "Construction": "Construction", "Other Services (except Public Administration)":
                "Repairs, salons, laundries", "Agriculture, Forestry, Fishing and Hunting": "Forestry, fishing, farm services"}


class Firms(VoiceoverScene):
    def construct(self):
        card(self, 4, "Big firms and small", "Is the economy run by giants or by small businesses?",
             "Chapter four. Big firms and small.", lit=("unit", "moat"))
        self.sizes()
        self.sectors()

    def sizes(self):
        F = R["firms"]
        tot = F["total"]
        bins = F["bins"]
        L = 5.0
        rows = VGroup()
        for k, b in enumerate(bins):
            y = 1.6 - k * 0.68
            pf, pj, pr = b["firms"] / tot["firms"], b["jobs"] / tot["jobs"], b["receipts"] / tot["receipts"]
            lab = T(b["label"], 19, I.TEXT).move_to(np.array([0, y, 0]))
            fb = Rectangle(width=max(L * pf, 0.02), height=0.46, fill_color="#7EC8F5", fill_opacity=0.9,
                           stroke_width=0).move_to(np.array([-1.05, y, 0]), aligned_edge=RIGHT)
            jb = Rectangle(width=max(L * pj, 0.02), height=0.46, fill_color="#F2A65A", fill_opacity=0.9,
                           stroke_width=0).move_to(np.array([1.05, y, 0]), aligned_edge=LEFT)
            ft = T(f"{100 * pf:.{1 if pf < 0.01 else 0}f}%" if pf >= 0.001 else f"{100 * pf:.2f}%", 17,
                   "#7EC8F5").next_to(fb, LEFT, buff=0.1)
            jt = T(f"{100 * pj:.0f}%", 17, "#F2A65A").next_to(jb, RIGHT, buff=0.1)
            rows.add(VGroup(lab, fb, jb, ft, jt))
        heads = VGroup(TB("share of firms", 21, "#7EC8F5").move_to(np.array([-3.4, 2.35, 0])),
                       TB("employees per firm", 19, I.DIM).move_to(np.array([0, 2.35, 0])),
                       TB("share of jobs", 21, "#F2A65A").move_to(np.array([3.4, 2.35, 0])))
        top = T(f"America's {tot['firms'] / 1e6:.1f} million businesses with employees, 2022", 24, I.TEXT
                ).to_edge(UP, buff=0.35)
        big = bins[-1]
        call = VGroup(TB(f"{big['firms']:,.0f} firms", 30, "#F2A65A"), T("with 5,000 or more employees:", 18, I.TEXT),
                      T(f"{100 * big['jobs'] / tot['jobs']:.0f}% of the jobs,", 18, I.TEXT),
                      T(f"{100 * big['receipts'] / tot['receipts']:.0f}% of all sales", 18, I.TEXT)
                      ).arrange(DOWN, buff=0.06).move_to(np.array([4.95, -0.95, 0]))
        G = F["giants"]
        giants = T(f"{G['firms']:.0f} firms with 20,000 or more: {100 * G['jobs'] / tot['jobs']:.0f}% of all private "
                   "payroll jobs", 21, I.ACCENT).to_edge(DOWN, buff=0.5)
        src = source("US Census Bureau, Statistics of US Businesses, 2022 (private employers; excludes farms' crop and "
                     "livestock production, railroads and government)", size=13)
        small = bins[0]
        with self.voiceover(
            f"Behind the industries are firms, and they come in every size. <bookmark mark='a'/> In 2022 America had "
            f"{tot['firms'] / 1e6:.1f} million private businesses with at least one employee. <bookmark mark='b'/> "
            f"Most are tiny: four million of them, almost two in three, had fewer than five people on the payroll. "
            f"<bookmark mark='c'/> Now look at the other side. Those four million tiny firms employed about five "
            f"percent of all private payroll workers. <bookmark mark='d'/> At the far end were {big['firms']:,.0f} "
            "firms with five thousand or more employees: about one firm in every three thousand. They employed 36 "
            "percent of the workers, and made 46 percent of all the sales. <bookmark mark='e'/> And the 546 largest, "
            "with twenty thousand or more each, employed a quarter of everyone working for a private business. "
            "Small firms are most of the firms. Big firms are most of the jobs."
        ) as vo:
            self.play(FadeIn(top), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(heads[1]), LaggedStart(*[FadeIn(r[0]) for r in rows], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(heads[0]), LaggedStart(*[AnimationGroup(GrowFromEdge(r[1], RIGHT), FadeIn(r[3]))
                                                      for r in rows], lag_ratio=0.12), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(heads[2]), LaggedStart(*[AnimationGroup(GrowFromEdge(r[2], LEFT), FadeIn(r[4]))
                                                      for r in rows], lag_ratio=0.12), run_time=2)
            vo.wait_until("d")
            self.play(Indicate(rows[-1], color="#F2A65A", scale_factor=1.04), FadeIn(call, shift=LEFT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(giants, shift=UP * 0.1))
        self.clear_scene()
        assert small["firms"] / tot["firms"] > 0.6

    def sectors(self):
        S = R["firms"]["sectors"]
        items = [(SECTOR_SHORT.get(n, n), g, "#F2A65A" if g > 0.3 else ("#7EC8F5" if g > 0.1 else "#7BD88F"), "")
                 for n, g, s, j in S]
        rows = viz.margin_ladder(items, max_value=0.55, bar_len=5.4, row_h=0.305, size=15, name_w=3.9)
        rows.move_to(LEFT * 0.6 + DOWN * 0.35)
        head = T("Share of each industry's jobs in firms with 20,000 or more employees, 2022", 22, I.TEXT
                 ).to_edge(UP, buff=0.35)
        notes = VGroup(
            VGroup(TB("Giants", 20, "#F2A65A"), T("chains, networks, platforms:", 16, I.TEXT),
                   T("one system spread over", 16, I.TEXT), T("thousands of places", 16, I.TEXT)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.05),
            VGroup(TB("Small firms", 20, "#7BD88F"), T("work done on site,", 16, I.TEXT),
                   T("local and by hand:", 16, I.TEXT), T("builders, salons, repairs", 16, I.TEXT)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.05),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.2)
        src = source("US Census Bureau, Statistics of US Businesses, 2022", size=14)
        ret = next(g for n, g, s, j in S if n == "Retail Trade")
        con = next(g for n, g, s, j in S if n == "Construction")
        with self.voiceover(
            "How big the firms are depends on the industry. <bookmark mark='a'/> In retail, half of all the jobs "
            f"are in firms with twenty thousand or more employees: Walmart, Amazon, Target, Kroger, Home Depot. "
            "Transport and warehousing, the office services that hire out cleaners and guards, information, "
            "finance: all above a third. <bookmark mark='b'/> Near the bottom, construction, with three jobs in a "
            "hundred in giant firms, and the repair shops, hair salons and laundries, with two. <bookmark mark='c'/> "
            "The pattern has a logic. Where one company can spread the same system, brand and buying power over "
            "thousands of stores, routes or branches, the giants win. Where the work is done on site, locally and "
            "by hand, small firms do. Part five of this series asks why some industries end up with a few firms "
            "and others with thousands, and Part seven how to measure who has what share."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:6]], lag_ratio=0.15), run_time=1.8)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[6:]], lag_ratio=0.08), run_time=2)
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Indicate(rows[0], color="#F2A65A", scale_factor=1.03),
                      Indicate(rows[-3], color="#7BD88F", scale_factor=1.03))
        self.clear_scene()
        assert 0.45 < ret < 0.55 and con < 0.04
