from __future__ import annotations

from videos.industry.industry28.common import *  # noqa: F403


class Lessors(VoiceoverScene):
    def construct(self):
        card(self, 7, "Who owns the planes", "Who makes the money from the aircraft?",
             "Chapter seven. Who owns the planes. Many airlines do not own their aircraft: they rent them, from companies "
             "whose whole business is owning planes.", lit=("moat", "dollar"))
        self.margins()
        self.scale()
        self.why()

    def margins(self):
        L = R["lessors"]
        items = [("AerCap, aircraft lessor", 100 * L["aer"], GOOD, f"{100 * L['aer']:.0f}%"),
                 ("Air Lease, aircraft lessor", 100 * L["al"], GOOD, f"{100 * L['al']:.0f}%"),
                 ("Delta", 100 * L["dal"], SKY, f"{100 * L['dal']:.1f}%"), ("United", 100 * L["ual"], SKY, f"{100 * L['ual']:.1f}%"),
                 ("Southwest", 100 * L["luv"], CASH, f"{100 * L['luv']:.1f}%")]
        rows = hbars(items, max_value=30, x0=0.0, top=1.8, row=0.8, length=6.0, size=17, bar_h=0.45)
        lab = tx("net income per dollar of revenue, median of 2021-2025", 17, GREY_A).to_edge(UP, buff=0.8)
        planes = VGroup(*[draw.plane(1.0) for _ in range(4)]).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.9)
        src = source("Forms 10-K and 20-F via SEC company facts", size=12)
        beat(self,
             "Compare what the owners and the users of the same aircraft keep. <bookmark mark='a'/> AerCap, an aircraft "
             f"lessor, kept a median of {100 * L['aer']:.0f} cents of each dollar of "
             f"revenue as profit from 2021 to 2025; Air Lease, {100 * L['al']:.0f}. <bookmark mark='b'/> The airlines that fly "
             f"them: Delta {100 * L['dal']:.0f}, United {100 * L['ual']:.0f}, Southwest {100 * L['luv']:.0f}.",
             base=[rows.axis, lab, planes, src], steps=[VGroup(*rows[:2]), VGroup(*rows[2:])])

    def scale(self):
        L = R["lessors"]
        items = [("AerCap, revenue", L["aer_rev"], GOOD, f"${L['aer_rev']:.1f}bn"), ("AerCap, net income", L["aer_ni"], GOOD, f"${L['aer_ni']:.2f}bn"),
                 ("Delta, revenue", L["dal_rev"], SKY, f"${L['dal_rev']:.1f}bn"), ("Delta, net income", L["dal_ni"], SKY, f"${L['dal_ni']:.1f}bn")]
        rows = hbars(items, max_value=70, x0=-1.0, top=1.6, row=0.9, length=6.4, size=17, bar_h=0.45)
        lab = tx("2025", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("AerCap Holdings, Form 20-F for 2025; Delta Air Lines, Form 10-K for 2025; via SEC company facts", size=12)
        beat(self,
             f"Look at the scale. <bookmark mark='a'/> AerCap's revenue in 2025 was {L['aer_rev']:.1f} billion dollars, and "
             f"it kept {L['aer_ni']:.2f} billion. <bookmark mark='b'/> Delta's revenue was {L['dal_rev']:.0f} billion, more "
             f"than seven times as much, and it kept {L['dal_ni']:.1f} billion. A lessor with a fraction of the revenue made "
             "three-quarters of the profit of America's most profitable airline.",
             base=[rows.axis, lab, src], steps=[VGroup(*rows[:2]), VGroup(*rows[2:])])

    def why(self):
        g = VGroup(tx("Why the lessor keeps more", 22, WHITE, bold=True),
                   tx("an aircraft holds its value for decades, and can be moved to another airline anywhere", 18, GOOD),
                   tx("the lessor is paid a fixed rent each month; the airline carries the fares, the fuel and the crews", 18, SKY),
                   tx("and since 2020 the makers, Part 18's Airbus and Boeing, have delivered fewer planes than airlines want", 18, BIZ)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, 0.2, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        tag = estimate_tag("this series' reading; Part 18 covers the aircraft makers", size=12)
        beat(self,
             "In this series' reading, <bookmark mark='a'/> an aircraft keeps its value for decades and can be flown by any "
             "airline anywhere, so the owner can always find another tenant. <bookmark mark='b'/> The lessor takes a fixed "
             "rent; the airline takes the fares, the fuel and the crews, all the risks of this film. <bookmark mark='c'/> And "
             "the aircraft makers of Part 18 have delivered fewer planes than airlines wanted, which makes every plane already "
             "flying more valuable to whoever owns it. As in property and shipping, the steadier money is in owning the asset "
             "and renting it out.",
             base=[tag], steps=[g[:2], g[2], g[3]])
