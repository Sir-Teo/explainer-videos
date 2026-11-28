from __future__ import annotations

from videos.industry.industry34.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 10, "Called it?", "Did delivery become profitable, and will McDonald's reach fifty thousand restaurants?",
             "Chapter ten. Called it? A delivery company's warning about its own losses, scored against what followed; and our "
             "call on McDonald's own target.", lit=("change",))
        self.dash()
        self.ours()
        self.watch()

    def dash(self):
        C = R["called"]
        ni, rv = C["ni"], C["revs"]
        q = quote(["'We have a history of net losses, we anticipate increasing expenses in the future, and we may not be able",
                   "to maintain or increase profitability in the future.'"], "DoorDash, prospectus, December 2020", size=18).move_to([0, 2.1, 0])
        ch = line_chart({"revenue, $bn": ({y: v for y, v in rv.items()}, APPS), "net income, $bn": ({y: v for y, v in ni.items()}, GOOD)},
                        x=(2018, 2025), y=(-2, 14), xticks=[2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025], yticks=[0, 4, 8, 12],
                        yfmt=lambda v: f"${v:.0f}bn", ylabel="DoorDash", width=7.4, height=3.0, center=(-1.2, -1.0),
                        nudge={"net income, $bn": -0.2})
        zero = DashedLine(ch.ax.c2p(2018, 0), ch.ax.c2p(2025, 0), color=GREY_B, stroke_width=1.5)
        verdict = tx(f"scored: losses every year to 2023; ${ni[2024] * 1e3:.0f}m profit in 2024, ${ni[2025] * 1e3:.0f}m in 2025", 18, GOOD, bold=True).to_edge(DOWN, buff=0.7)
        src = source("DoorDash, prospectus (Form 424B4, 2020) and Forms 10-K via SEC company facts", size=12)
        beat(self,
             "First, a company's own words. <bookmark mark='a'/> When DoorDash listed its shares in December 2020, it told "
             f"investors it had a history of losses, {C['loss19']:.0f} million dollars in 2019 alone, and might not stay "
             "profitable even if it got there. <bookmark mark='b'/> Its revenue then grew more than fifteen-fold, "
             f"<bookmark mark='c'/> but the losses continued until 2023. <bookmark mark='d'/> In 2024 it made "
             f"{ni[2024] * 1e3:.0f} million and in 2025 {ni[2025] * 1e3:.0f} million. The warning was honest, and the "
             "doubters were wrong too: delivery did become profitable, but only at enormous scale, on about a cent of every "
             "dollar it carries.",
             base=[src], steps=[q, VGroup(ch.frame, zero, ch.lines["revenue, $bn"], ch.labels["revenue, $bn"]),
                                VGroup(ch.lines["net income, $bn"], ch.labels["net income, $bn"]), verdict])

    def ours(self):
        C = R["called"]
        rs = C["rest"]
        claim = VGroup(tx("Our call, 28 November 2026", 20, FR, bold=True),
                       tx(f"McDonald's will report at least {C['target']:,} restaurants worldwide", 22, WHITE, bold=True),
                       tx("at 31 December 2027, meeting its own target.", 22, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, FR, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0, 1.7, 0])
        why = bullets([f"for: {rs[2023]:,} (2023), {rs[2024]:,} (2024), {rs[2025]:,} (2025); it expects about {C['net26']:,} net additions in 2026",
                       f"against: that leaves about {C['need27']:,} to add in 2027, more than any year so far",
                       "against: openings abroad depend on licensees' capital and on local economies"], size=17).move_to([0, -0.8, 0])
        rule = tx(f"scored on McDonald's Form 10-K for 2027: restaurants at year-end; true if {C['target']:,} or more", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             f"Now ours. <bookmark mark='a'/> McDonald's has set itself a target of {C['target']:,} restaurants by the end of "
             f"2027. We say it will fall short, and give it only {100 * C['prob']:.0f} per cent of making it. "
             f"<bookmark mark='b'/> It added {rs[2024] - rs[2023]:,} restaurants in 2024 and {rs[2025] - rs[2024]:,} in 2025, "
             f"and expects about {C['net26']:,} in 2026. That would leave about {C['need27']:,} to add in 2027 alone, more than "
             "in any of those years. <bookmark mark='c'/> McDonald's annual report for 2027 will settle it, and we will score "
             "the call when it is published.",
             base=[tag], steps=[claim, why, rule])

    def watch(self):
        g = VGroup(tx("What to watch", 22, WHITE, bold=True),
                   tx("prices: how much more diners will pay as wages rise", 18, LABC),
                   tx("delivery: whether apps bring new customers or take a cut of old ones", 18, APPS),
                   tx("growth: whether franchisees keep queuing to open new restaurants", 18, FR)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "Three things to watch. <bookmark mark='a'/> Prices: restaurant prices have risen faster than prices in "
             "general, and the question is when diners stop paying. <bookmark mark='b'/> Delivery: whether the apps bring "
             "new customers or simply take a commission on old ones. <bookmark mark='c'/> And growth: a franchisor grows only "
             "as fast as owners queue to open new restaurants, which depends on how quickly those restaurants pay back.",
             base=[tag], steps=[g[:2], g[2], g[3]])
