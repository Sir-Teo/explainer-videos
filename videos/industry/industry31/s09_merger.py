from __future__ import annotations

from videos.industry.industry31.common import *  # noqa: F403


class Merger(VoiceoverScene):
    def construct(self):
        card(self, 7, "The merger that was stopped", "Why couldn't the two biggest supermarket chains combine?",
             "Chapter seven. The merger that was stopped. Kroger and Albertsons tried to combine to face Walmart and "
             "Costco. A court said no.", lit=("moat", "change"))
        self.two()
        self.court()
        self.town()
        self.why()

    def two(self):
        Fm = R["formats"]
        items = [("Kroger supermarkets", Fm["kr"][0], GROCER, f"{Fm['kr'][0]:,}"), ("Albertsons stores", Fm["aci"][0], GROCER, f"{Fm['aci'][0]:,}"),
                 ("together", Fm["kr"][0] + Fm["aci"][0], MASS, f"{Fm['kr'][0] + Fm['aci'][0]:,}")]
        rows = hbars(items, max_value=5200, x0=0.4, top=1.3, row=1.0, length=5.6, size=18, bar_h=0.5)
        rv = tx(f"revenue: Kroger ${Fm['kr'][1]:.0f}bn and Albertsons ${Fm['aci'][1]:.0f}bn, against Walmart's ${R['hook']['wmt_rev']:.0f}bn", 17, GREY_A).to_edge(DOWN, buff=1.0)
        src = source("Kroger and Albertsons, Forms 10-K for fiscal 2025; SEC company facts", size=12)
        beat(self,
             f"<bookmark mark='a'/> Kroger runs {Fm['kr'][0]:,} supermarkets. <bookmark mark='b'/> Albertsons, under 22 "
             f"names including Safeway and Vons, runs {Fm['aci'][0]:,} stores. <bookmark mark='c'/> Together, nearly five "
             f"thousand stores and about {Fm['kr'][1] + Fm['aci'][1]:.0f} billion dollars of sales: still well short of "
             "Walmart. Bigger buying power, cheaper lorries and lower prices against the giants were, in this series' "
             "reading, the heart of the case the two companies made for combining.",
             base=[rows.axis, src], steps=[rows[0], rows[1], VGroup(rows[2], rv)])

    def court(self):
        q = quote(["'On December 10, 2024, pursuant to a decision of United States District Court for the District of Oregon",
                   "in the case Federal Trade Commission et al. v. The Kroger Company and Albertsons Companies, Inc. ...",
                   "the court issued a preliminary injunction enjoining the consummation of the merger.'"],
                  "Kroger, Form 10-K for fiscal 2025", size=17).move_to([0, 1.4, 0])
        g = bullets(["11 December 2024: Kroger delivered a notice terminating the merger agreement",
                     "Albertsons sued Kroger for a $600 million termination fee and further damages"], size=18).move_to([0, -1.2, 0])
        src = source("Kroger, Form 10-K for fiscal 2025", size=12)
        beat(self,
             "<bookmark mark='a'/> The Federal Trade Commission and nine states sued to stop the deal, and on 10 December "
             "2024 a federal court in Oregon granted an injunction blocking it. <bookmark mark='b'/> The next day Kroger "
             "ended the agreement, and Albertsons sued Kroger for a 600 million dollar break fee and more, accusing it "
             "of breaking the agreement. A merger agreed in October 2022 ended, two years and two months later, in lawsuits "
             "between the companies that had wanted to become one, while both kept running their stores.",
             base=[src], steps=[q, g])

    def town(self):
        streets = VGroup(*[Line([-5.5, y, 0], [5.5, y, 0], stroke_color=GREY_D, stroke_width=3) for y in (-1.5, 0.0, 1.5)],
                         *[Line([x, -2.4, 0], [x, 2.4, 0], stroke_color=GREY_D, stroke_width=3) for x in (-3.5, 0.0, 3.5)])
        a = VGroup(draw.shop(1.0, color=GROCER), tx("Kroger", 14, GROCER, bold=True)).arrange(DOWN, buff=0.08).move_to([-2.0, 0.8, 0])
        b = VGroup(draw.shop(1.0, color=GROCER), tx("Albertsons", 14, GROCER, bold=True)).arrange(DOWN, buff=0.08).move_to([1.6, 0.8, 0])
        c = VGroup(draw.shop(1.3, color=MASS), tx("Walmart, 12 miles away", 14, MASS, bold=True)).arrange(DOWN, buff=0.08).move_to([4.6, -2.0, 0])
        houses = VGroup(*[draw.house(0.35).move_to([x, y, 0]) for x in (-4.5, -1.0, 0.8, 2.6) for y in (-0.8, 2.0)])
        tag = estimate_tag("this series' illustration of a local grocery market", size=12)
        beat(self,
             "Picture a town, as the regulators do. <bookmark mark='a'/> A Kroger and an Albertsons a few streets apart "
             "compete for the same households every week, on price, freshness and queues. <bookmark mark='b'/> The nearest "
             "Walmart supercentre is a long drive away. Merge the two supermarkets and, for the people in those houses, "
             "the choice falls from two shops to one. Multiply that by hundreds of towns, and that is the case the court "
             "heard.",
             base=[streets, houses, tag], steps=[VGroup(a, b), c])

    def why(self):
        g = VGroup(tx("Why a court cared, in this series' reading", 21, WHITE, bold=True),
                   tx("shoppers buy groceries close to home: the market is the town, not the nation", 18, GROCER),
                   tx("in many towns the two chains were each other's nearest rival", 18, MASS),
                   tx("removing a nearby rival can raise prices even for a firm smaller than the leader", 18, BAD),
                   tx("Walmart's national size did not change the choice in a given neighbourhood", 18, ALL)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' reading of a grocery merger review; Economics, Built's merger part works through the tools", size=12)
        beat(self,
             "Why would a court block two companies that were still smaller than Walmart? In this series' reading, "
             "<bookmark mark='a'/> because people buy groceries near home, so the market that matters is the town. "
             "<bookmark mark='b'/> In many towns a Kroger and an Albertsons store were each other's nearest rival. "
             "<bookmark mark='c'/> Removing a nearby rival can raise prices even for a company smaller than the national "
             "leader, <bookmark mark='d'/> because Walmart's national size does not change the choice on a given street.",
             base=[tag], steps=[g[:2], g[2], g[3], g[4]])
