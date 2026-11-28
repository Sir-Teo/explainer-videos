from __future__ import annotations

from videos.industry.industry36.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 10, "Called it?", "Did Salesforce reach fifty billion dollars, and how fast will Microsoft's cloud grow?",
             "Chapter ten. Called it? A software company's own long-range target, scored against its result; and our call on "
             "the fastest-growing large business in software.", lit=("change",))
        self.target()
        self.ours()
        self.watch()

    def target(self):
        C = R["called"]
        rv = C["crm"]
        q = quote(["'$50B+ FY26 Target'"], "Salesforce, investor-day presentation, Form 8-K, 24 September 2021", size=22).move_to([0, 2.2, 0])
        ch = line_chart({"revenue": ({y: v for y, v in rv.items()}, SALES)}, x=(2018, 2025), y=(0, 55),
                        xticks=[2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025], yticks=[0, 10, 20, 30, 40, 50], yfmt=lambda v: f"${v:.0f}bn",
                        ylabel="Salesforce's revenue, fiscal years to January (named for the year before)", width=7.6, height=3.0,
                        center=(-1.0, -0.9))
        goal = DashedLine(ch.ax.c2p(2018, 50), ch.ax.c2p(2025, 50), color=STOCK, stroke_width=2)
        gl = tx("the target: $50bn", 14, STOCK).next_to(ch.ax.c2p(2018.3, 50), UP, buff=0.05)
        verdict = tx(f"scored: {bn(C['crm26'])} in the year to January 2026, {100 * (1 - C['crm26'] / C['target_crm']):.0f}% short", 18, LOSS, bold=True).to_edge(DOWN, buff=0.7)
        src = source("Salesforce, Forms 8-K (September 2021 and 2022) and 10-K for fiscal 2026; SEC company facts", size=12)
        beat(self,
             "First, a company's own words. <bookmark mark='a'/> In September 2021, at the height of the boom in software "
             "shares, Salesforce told investors its target was more than fifty billion dollars of revenue in the year to "
             "January 2026. A year later it repeated the target, while warning of a two-billion-dollar drag from the strong "
             "dollar. <bookmark mark='b'/> Its revenue did keep rising, <bookmark mark='c'/> but it reached "
             f"{C['crm26']:.1f} billion: {100 * (1 - C['crm26'] / C['target_crm']):.0f} per cent short. Growth slowed from over "
             "twenty per cent a year to about ten, as customers who had bought quickly in the pandemic stopped buying more.",
             base=[src], steps=[q, VGroup(ch.frame, goal, gl, ch.lines["revenue"], ch.labels["revenue"]), verdict])

    def ours(self):
        C = R["called"]
        claim = VGroup(tx("Our call, 28 November 2026", 20, SUB, bold=True),
                       tx(f"Microsoft Cloud revenue for the year to June 2027 will be at least ${C['target']:.0f} billion.", 22, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, SUB, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0, 1.7, 0])
        why = bullets([f"for: {bn(C['cloud26'])} in fiscal 2026, up 27%; {bn(C['q1'])} in the first quarter of fiscal 2027, up 30%",
                       f"against: it needs {100 * C['need']:.0f}% growth for the year, above last year's 27%",
                       "against: data-centre capacity and power limit how fast AI services can be sold"], size=17).move_to([0, -0.8, 0])
        rule = tx("scored on Microsoft's Form 10-K for fiscal 2027: Microsoft Cloud revenue as reported; true if $275bn or more", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             f"Now ours. <bookmark mark='a'/> We say Microsoft Cloud revenue reaches at least {C['target']:.0f} billion dollars in "
             f"the year to June 2027, and give it {100 * C['prob']:.0f} per cent. <bookmark mark='b'/> It was "
             f"{C['cloud26']:.0f} billion last year, up 27 per cent, and grew 30 per cent in the first quarter of this one. The "
             f"target needs {100 * C['need']:.0f} per cent for the full year: faster than last year, slower than the latest "
             "quarter. The limit, in this series' reading, is less demand than the data centres and power to serve it. "
             "<bookmark mark='c'/> Microsoft's annual report for fiscal 2027 will settle it.",
             base=[tag], steps=[claim, why, rule])

    def watch(self):
        g = VGroup(tx("What to watch", 22, WHITE, bold=True),
                   tx("the cost of each answer: gross margins as AI use grows", 18, AI),
                   tx("the unit of sale: seats, use, or results", 18, SALES),
                   tx("retention: whether customers keep adding, or start cutting", 18, SUB)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "Three things to watch. <bookmark mark='a'/> The cost of each answer: whether gross margins keep slipping as AI "
             "use grows. <bookmark mark='b'/> The unit of sale: whether software is still sold by the seat, or by use, or by "
             "results. <bookmark mark='c'/> And retention: whether the customers already won keep adding, which is where the "
             "profit has always come from.",
             base=[tag], steps=[g[:2], g[2], g[3]])
