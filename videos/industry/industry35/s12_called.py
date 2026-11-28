from __future__ import annotations

from videos.industry.industry35.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 10, "Called it?", "How long did the travel slump really last, and how fast will it grow now?",
             "Chapter ten. Called it? A travel agent's own warning in the depth of the pandemic, scored against what "
             "followed; and our call on how many nights it will sell in 2027.", lit=("change",))
        self.booking()
        self.ours()
        self.watch()

    def booking(self):
        C = R["called"]
        N = C["nights"]
        q = quote(["'We expect to continue to see severely reduced new travel and restaurant reservation bookings",
                   "as compared to 2019 levels for the foreseeable future.'"], "Booking Holdings, Form 10-K for 2020 (February 2021)", size=18).move_to([0, 2.15, 0])
        ch = line_chart({"room nights, millions": ({y: v for y, v in N.items()}, AGENT)}, x=(2019, 2025), y=(0, 1400),
                        xticks=[2019, 2020, 2021, 2022, 2023, 2024, 2025], yticks=[0, 400, 800, 1200], yfmt=lambda v: f"{v:.0f}",
                        ylabel="Booking Holdings' room nights, millions", width=7.6, height=3.0, center=(-1.0, -0.95))
        base19 = DashedLine(ch.ax.c2p(2019, N[2019]), ch.ax.c2p(2025, N[2019]), color=GREY_B, stroke_width=1.5)
        verdict = tx(f"scored: above 2019 by 2022 ({N[2022]}m against {N[2019]}m); {N[2025]:,}m in 2025", 18, GOOD, bold=True).to_edge(DOWN, buff=0.7)
        src = source("Booking Holdings, Forms 10-K for 2020, 2023 and 2025", size=12)
        beat(self,
             "First, a company's own words. <bookmark mark='a'/> In February 2021, with travel at its lowest, Booking "
             "Holdings told investors it expected severely reduced bookings, compared with 2019, for the foreseeable future. "
             "In the same report it assumed that two of its businesses, KAYAK and OpenTable, would not return to their 2019 "
             f"profits within five years. <bookmark mark='b'/> Its room nights had fallen from {N[2019]} million in 2019 to "
             f"{N[2020]} million. <bookmark mark='c'/> They passed the 2019 level in 2022, the year after the warning, "
             f"<bookmark mark='d'/> and reached {N[2025]:,} million in 2025. The foreseeable future was shorter than it looked: "
             "travel came back faster than the travel companies themselves expected.",
             base=[src], steps=[q, VGroup(ch.frame, base19), VGroup(ch.lines["room nights, millions"], ch.labels["room nights, millions"]), verdict])

    def ours(self):
        C = R["called"]
        N = C["nights"]
        claim = VGroup(tx("Our call, 28 November 2026", 20, AGENT, bold=True),
                       tx(f"Booking Holdings will report at least {C['target'] / 1e3:.2f} billion room nights", 22, WHITE, bold=True),
                       tx("for 2027.", 22, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, AGENT, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0, 1.7, 0])
        why = bullets([f"for: {N[2023]:,}m (2023), {N[2024]:,}m (2024), {N[2025]:,}m (2025): growth of 9% and 8%",
                       f"against: {C['q9']:,}m in the first nine months of 2026, up {100 * (C['q9'] / C['q9prev'] - 1):.0f}%; at that pace "
                       f"2026 ends near {C['est26']:,.0f}m",
                       f"against: 2027 would then need {100 * C['need']:.0f}%, faster than 2026"], size=17).move_to([0, -0.8, 0])
        rule = tx("scored on Booking Holdings' Form 10-K for 2027: room nights as reported; true if 1,400 million or more", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             f"Now ours. <bookmark mark='a'/> We say Booking will fall short of {C['target'] / 1e3:.1f} billion room nights in "
             f"2027, and give it {100 * C['prob']:.0f} per cent of reaching it. <bookmark mark='b'/> Its room nights grew nine "
             f"per cent in 2024 and eight in 2025, but only six in the first nine months of 2026. At that pace 2026 ends near "
             f"{C['est26']:,.0f} million, and 2027 would need growth of {100 * C['need']:.0f} per cent: faster than this year, "
             "when the trend is slowing. <bookmark mark='c'/> Booking's annual report for 2027 will settle it.",
             base=[tag], steps=[claim, why, rule])

    def watch(self):
        g = VGroup(tx("What to watch", 22, WHITE, bold=True),
                   tx("supply: how many new rooms the owners can finance and build", 18, OWNER),
                   tx("direct against agents: whether the brands' loyalty schemes win the booking", 18, BRAND),
                   tx("the rules: parity clauses, gatekeeper duties, cities' limits on short-term rentals", 18, AGENT)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "Three things to watch. <bookmark mark='a'/> Supply: the brands grow only as fast as owners can borrow to build, "
             "so interest rates set the pace of the pipeline. <bookmark mark='b'/> Direct against the agents: whether loyalty "
             "programmes keep the guest, or the agents and the search engines take a growing share of every night. "
             "<bookmark mark='c'/> And the rules: what competition authorities allow the agents to demand, and what cities "
             "allow in their flats.",
             base=[tag], steps=[g[:2], g[2], g[3]])
