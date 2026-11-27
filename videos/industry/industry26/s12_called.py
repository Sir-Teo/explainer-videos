from __future__ import annotations

from videos.industry.industry26.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 10, "Called it?", "How well do property's own forecasts hold up?",
             "Chapter ten. Called it? A company that went public on a forecast of the office market, a landlord's promise "
             "about its own buildings, and our own call.", lit=("change",))
        self.wework()
        self.bxp()
        self.ours()

    def wework(self):
        C = R["called"]
        q = quote(["'Among the approximately 255 million potential members across our 280 target cities globally,",
                   "we estimate a total opportunity of $3.0 trillion'"], "The We Company, Form S-1, 14 August 2019", size=17).move_to([0, 1.8, 0])
        W = C["we_rev"]
        c = stat_cards([(f"${C['we_tam']:.1f}tn", "the opportunity it saw, 2019", VALUE),
                        (f"${W[2022][0]:.1f}bn", "its revenue in 2022", ALL),
                        ("Chapter 11", "6 November 2023", BAD)], y=-0.6, size=36, span=11)
        src = source("The We Company, Form S-1 of 14 August 2019; WeWork Inc., Forms 10-K via SEC company facts and Form 8-K of "
                     "7 November 2023", size=12)
        beat(self,
             "WeWork first. <bookmark mark='a'/> In its 2019 filing to go public, it estimated its opportunity at "
             f"{C['we_tam']:.1f} trillion dollars, across 255 million potential members in 280 cities. <bookmark mark='b'/> "
             f"From 2019 to 2022 its revenue was between {min(v[0] for v in W.values()):.1f} and "
             f"{max(v[0] for v in W.values()):.1f} billion dollars a year, and it lost money in every one of those years. "
             "<bookmark mark='c'/> It filed for bankruptcy protection in November 2023. The forecast measured how many people "
             "might want a desk; the business depended on how long they would promise to pay for one.",
             base=[src], steps=[q, [c[0], c[1]], c[2]])

    def bxp(self):
        C = R["called"]
        q = quote(["'we remain on track to achieve occupancy improvements by year-end 2026, consistent with the targets",
                   "outlined at our September 2025 Investor Day'"], "BXP, Inc., Form 10-K for 2025", size=17).move_to([0, 1.8, 0])
        c = stat_cards([(f"{C['occ25']:.1f}%", "occupied, end of 2025", BAD),
                        (f"{C['q3']:.1f}%", "occupied, September 2026", VALUE),
                        (f"{C['leased']:.1f}%", "leased, September 2026", GOOD)], y=-0.6, size=38, span=11)
        src = source("BXP, Inc., Form 10-K for 2025; Form 8-K of 27 October 2026", size=12)
        beat(self,
             "Then BXP. <bookmark mark='a'/> In February 2026 it told shareholders it was on track to raise occupancy by the "
             "end of the year, as it had promised investors in September 2025. <bookmark mark='b'/> It was "
             f"{C['occ25']:.1f} per cent occupied at the end of 2025 <bookmark mark='c'/> and {C['q3']:.1f} by September 2026, "
             f"<bookmark mark='d'/> with {C['leased']:.1f} per cent signed. So far, it is keeping that promise; the year-end "
             "figure comes in January.",
             base=[src], steps=[q, c[0], c[1], c[2]])

    def ours(self):
        C = R["called"]
        claim = VGroup(tx("Our call, 27 November 2026", 20, VALUE, bold=True),
                       tx(f"BXP's total portfolio occupancy will be {C['call']:.1f}% or more", 22, WHITE, bold=True),
                       tx("at 31 December 2027.", 22, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, VALUE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0, 1.7, 0])
        why = bullets([f"for: {C['leased']:.1f}% already leased; four quarters of gains; new office construction 'has effectively halted'",
                       "against: occupancy fell every year from 2019 to 2025; San Francisco was 77% let",
                       "against: a slower economy, or tenants who leave when their leases end, would undo it"], size=18).move_to([0, -0.5, 0])
        rule = tx("scored on BXP's results for 2027, due January 2028", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             f"Now ours. <bookmark mark='a'/> We say BXP's occupancy will be {C['call']:.0f} per cent or more at the end of "
             f"2027, and give it {100 * C['prob']:.0f} per cent. <bookmark mark='b'/> For: {C['leased']:.1f} per cent of its "
             "space is already leased, so signed tenants alone would carry it most of the way; it has gained four quarters "
             "running; and almost no new offices are being built to compete. Against: its occupancy fell every year from 2019 "
             "to 2025, San Francisco is still a quarter empty, and a weaker economy or tenants leaving at the end of their "
             "leases could undo the gains. <bookmark mark='c'/> BXP's results for 2027 will settle it, and the call stays in "
             "the log either way.",
             base=[tag], steps=[claim, why, rule])
