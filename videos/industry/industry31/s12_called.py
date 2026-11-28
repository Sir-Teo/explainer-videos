from __future__ import annotations

from videos.industry.industry31.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 10, "Called it?", "Did the robot warehouse win, and will the club keep growing?",
             "Chapter ten. Called it? A grocer's bet on robots, made in 2021 and scored in 2026, and our own call on the "
             "warehouse club.", lit=("change",))
        self.kroger()
        self.ours()
        self.watch()

    def kroger(self):
        q1 = quote(["'The future success of the digital business will also depend on ... customer fulfillment centers",
                    "powered by Ocado'"], "Kroger, Form 10-K for fiscal 2020 (March 2021)", size=18).move_to([0, 2.0, 0])
        q2 = quote(["'closing facilities in Pleasant Prairie, Wis.; Frederick, Md.; and Groveland, Fla. in January 2026, which",
                    "had not met operational or financial expectations, and canceled plans for the site in Charlotte, N.C.'"],
                   "Kroger, Form 10-K for fiscal 2025", size=17).move_to([0, -0.1, 0])
        verdict = tx(f"scored: ${R['online']['ocado']:.1f}bn of charges; online orders move to stores and delivery partners", 20, BAD, bold=True).move_to([0, -2.2, 0])
        src = source("Kroger, Forms 10-K for fiscal 2020 and 2025", size=12)
        beat(self,
             "First, a company's own forecast. <bookmark mark='a'/> In 2021 Kroger told investors that its digital "
             "future would depend partly on automated warehouses built with Ocado. <bookmark mark='b'/> Five years later "
             "it closed three of them and cancelled a fourth, because they 'had not met operational or financial "
             "expectations'. <bookmark mark='c'/> Kroger now serves online orders mainly from its stores and through delivery partners. Right "
             "that online grocery would grow; wrong about the machine that would serve it. A warehouse full of robots needs "
             "a lot of orders from close by to pay for itself, and Kroger's did not get them.",
             base=[src], steps=[q1, q2, verdict])

    def ours(self):
        C = R["called"]
        a, b, c = C["members"]
        claim = VGroup(tx("Our call, 28 November 2026", 20, CLUB, bold=True),
                       tx(f"Costco will report more than {C['line']:.0f} million paid members", 22, WHITE, bold=True),
                       tx("at the end of its 2027 fiscal year (about 29 August 2027).", 22, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, CLUB, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0, 1.7, 0])
        why = bullets([f"for: {a:.1f}m (2024), {b:.1f}m (2025), {c:.1f}m (2026): it needs {C['line'] - c:.1f}m more, about last year's {c - b:.1f}m",
                       "for: renewals above 92% in the US and Canada, and new warehouses opening",
                       f"against: growth slowed from {b - a:.1f}m to {c - b:.1f}m; a weaker economy or a fee rise could slow it more"],
                      size=17).move_to([0, -0.8, 0])
        rule = tx("scored on Costco's Form 10-K for fiscal 2027: paid members at year-end; true if above 87.0 million", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             f"Now ours. <bookmark mark='a'/> We say Costco will report more than {C['line']:.0f} million paid members at "
             f"the end of its 2027 year, and give it {100 * C['prob']:.0f} per cent: a little better than even. "
             f"<bookmark mark='b'/> For: it needs {C['line'] - c:.1f} million more, about what it added last year, renewals "
             "are above ninety-two per cent in its home markets, and it keeps opening warehouses. Against: the yearly gain "
             f"slowed from {b - a:.1f} million to {c - b:.1f} million, and a weaker economy could slow it further. "
             "<bookmark mark='c'/> Costco's annual report for 2027 will settle it, and we will score this call on the "
             "day it is published, whichever way it goes.",
             base=[tag], steps=[claim, why, rule])

    def watch(self):
        g = VGroup(tx("What to watch", 22, WHITE, bold=True),
                   tx("food prices: whether they rise faster than incomes again", 18, GROCER),
                   tx("online: whether store-picked orders stay profitable as they grow", 18, ONLINE),
                   tx("the suppliers: whether own labels keep taking shelf space from the brands", 18, GOODS)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "Three things to watch. <bookmark mark='a'/> Food prices: if they again rise faster than incomes, shoppers "
             "trade down to the clubs and discounters. <bookmark mark='b'/> Online: whether orders picked in stores stay "
             "profitable as they grow. <bookmark mark='c'/> And the suppliers: whether the retailers' own labels keep "
             "taking shelf space from the brands of Part 22. Each of those moves the few cents that decide whether a grocer "
             "has a good year or a bad one.",
             base=[tag], steps=[g[:2], g[2], g[3]])
