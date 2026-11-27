from __future__ import annotations

from videos.industry.industry29.common import *  # noqa: F403


class Driverless(VoiceoverScene):
    def construct(self):
        card(self, 8, "The truck without a driver", "When will lorries drive themselves?",
             "Chapter eight. The truck without a driver. Much of a truck's cost is the person in it, so a company that removes "
             "the person changes the arithmetic of Run it.", lit=("change",))
        self.plan()
        self.now()
        self.maths()

    def plan(self):
        C = R["called"]
        q1 = quote(["'We plan to initially launch Aurora Horizon, our driverless trucking product, in late 2023 in Texas'"],
                   "Aurora Innovation, Form 10-K for 2021 (March 2022)", size=19).move_to([0, 1.8, 0])
        q2 = quote(["'In April 2025, we launched driverless commercial operations with Hirschbach and Uber Freight'"],
                   "Aurora Innovation, Form 10-K for 2025", size=19).move_to([0, 0.1, 0])
        s = draw.semi(3.2, cab_color=SKY).move_to([0, -2.1, 0])
        src = source("Aurora Innovation, Forms 10-K for 2021 and 2025", size=12)
        beat(self,
             "Aurora, founded in 2017, is one of the American companies trying. <bookmark mark='a'/> In "
             "March 2022 it told investors it planned to launch driverless trucks in Texas in late 2023. "
             "<bookmark mark='b'/> It launched in April 2025, about a year and a half late, hauling freight in Texas for "
             "paying customers. <bookmark mark='c'/> A lorry with nobody in the cab, on an American highway, "
             "for money.",
             base=[src], steps=[q1, q2, s])

    def now(self):
        C = R["called"]
        c = stat_cards([(f"{C['miles']:,.0f}", "driverless miles by September 2026", SKY), ("20+", "driverless trucks built", ALL),
                        (f"${1e3 * C['aur_rev']:.0f}m", "revenue in 2025", GOOD), (f"-${abs(C['aur_loss']):.2f}bn", "operating loss in 2025", BAD)],
                       y=0.8, size=34, span=12.6)
        g = tx(f"its aim: 'to exit 2027 with more than {C['target']:,.0f} driverless trucks in operation'", 19, SKY, bold=True).move_to([0, -1.6, 0])
        src = source("Aurora Innovation, third-quarter 2026 shareholder letter (Form 8-K) and Form 10-K for 2025; SEC company facts", size=12)
        beat(self,
             "Where it stands, as of its October 2026 letter. <bookmark mark='a'/> Its trucks had driven more than half a "
             "million miles with nobody aboard. <bookmark mark='b'/> It had twenty or more driverless trucks built and "
             f"coming into service. <bookmark mark='c'/> In 2025 it earned about {1e3 * C['aur_rev']:.0f} million dollars "
             f"<bookmark mark='d'/> and spent {abs(C['aur_loss']):.1f} billion more than that. <bookmark mark='e'/> It aims "
             f"to have more than {C['target']:,.0f} driverless trucks running by the end of 2027, against America's "
             f"{R['hook']['carriers']:,.0f} trucking firms.",
             base=[src], steps=[c[0], c[1], c[2], c[3], g])

    def maths(self):
        U = R["run"]
        g = VGroup(tx("What a driverless truck would change, in this series' reading", 21, WHITE, bold=True),
                   tx("the cost a mile falls by whatever the driver's share of it is", 18, SKY),
                   tx("the truck can run nearly all day, so its fixed costs spread over more miles", 18, GOOD),
                   tx("but the trip home is still empty unless someone finds a load: Run it's network still wins", 18, RAIL)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, 0.2, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "What would it change? In this series' reading, <bookmark mark='a'/> the cost of a mile falls by whatever the "
             "driver's share of it is. <bookmark mark='b'/> A truck without a driver need not stop for rest, so its tractor "
             "and trailer are paid for over more miles. <bookmark mark='c'/> But it still has to come home, so the network "
             "that finds it a load still wins. The likely winners are the companies with the most freight in the most "
             "places, which is why Aurora's first customers are large carriers and brokers. And until the trucks run in "
             "thousands, not dozens, the half a million firms of chapter four have nothing to fear from them.",
             base=[tag], steps=[g[:2], g[2], g[3]])
