from __future__ import annotations

from videos.industry.industry28.common import *  # noqa: F403


class Seat(VoiceoverScene):
    def construct(self):
        card(self, 2, "A seat-mile", "What does an airline sell, and what does it cost to make?",
             "Chapter two. A seat-mile. Airlines measure everything by one unit: one seat flown one mile, whether anyone sits "
             "in it or not.", lit=("unit", "make"))
        self.unit()
        self.jargon()
        self.three()
        self.load()
        self.breakeven()
        self.southwest()

    def unit(self):
        S = R["seat"]
        plane = draw.plane(3.6).move_to([0, 2.0, 0])
        c = stat_cards([(f"{S['dal_asm'] / 1e3:,.0f}bn", "seat-miles Delta flew in 2025", SKY),
                        (f"{S['dal_rpm'] / 1e3:,.0f}bn", "of them with a paying passenger", LEISURE),
                        (f"{100 * S['dal_rpm'] / S['dal_asm']:.0f}%", "the load factor", BIZ)], y=-0.4, size=40, span=11)
        src = source("Delta Air Lines, Form 10-K for 2025", size=12)
        beat(self,
             "An available seat-mile is one seat flown one mile. <bookmark mark='a'/> In 2025 Delta flew "
             f"{S['dal_asm'] / 1e3:,.0f} billion of them. <bookmark mark='b'/> {S['dal_rpm'] / 1e3:,.0f} billion carried a "
             f"paying passenger. <bookmark mark='c'/> The share that did, {100 * S['dal_rpm'] / S['dal_asm']:.0f} per cent, is "
             "the load factor. Every airline's results come down to what it earns on a seat-mile and what a seat-mile costs.",
             base=[plane, src], steps=[c[0], c[1], c[2]])

    def jargon(self):
        S = R["seat"]
        c = stat_cards([(f"{S['dal_yield']:.2f}c", "yield: paid per passenger-mile", LEISURE),
                        (f"{S['dal_prasm']:.2f}c", "PRASM: ticket money per seat-mile", SKY),
                        (f"{S['dal'][0]:.2f}c", "TRASM: all revenue per seat-mile", GOOD)], y=1.2, size=36, span=12)
        d = stat_cards([(f"{S['dal'][1]:.2f}c", "CASM: all cost per seat-mile", BAD),
                        (f"{S['dal_casmex']:.2f}c", "CASM-ex: without fuel and the refinery", FUEL)], y=-1.3, size=36, span=9)
        src = source("Delta Air Lines, Form 10-K for 2025: operating statistics", size=12)
        beat(self,
             "Airlines have a vocabulary for this, and five words cover most of it. <bookmark mark='a'/> The yield: what a "
             f"passenger paid for each mile flown, {S['dal_yield']:.2f} cents at Delta in 2025. <bookmark mark='b'/> Multiply "
             f"by the load factor and you get passenger revenue per seat-mile, {S['dal_prasm']:.2f} cents. "
             "<bookmark mark='c'/> Add everything else, cargo, the bank's payments for miles, the refinery's sales, and it "
             f"is {S['dal'][0]:.2f}. <bookmark mark='d'/> Against that, the cost of a seat-mile, {S['dal'][1]:.2f} cents, "
             f"<bookmark mark='e'/> or {S['dal_casmex']:.2f} without fuel and the refinery, the part managers say they "
             "control.",
             base=[src], steps=[c[0], c[1], c[2], d[0], d[1]])

    def three(self):
        S = R["seat"]
        rows = VGroup()
        for i, (name, (rev, cost, lf), col) in enumerate((("Delta", S["dal"], SKY), ("Southwest", S["luv"], CASH), ("Spirit", S["save"], BAD))):
            y = 1.7 - 1.45 * i
            b1 = Rectangle(width=0.26 * rev, height=0.38, stroke_width=0, fill_color=GOOD, fill_opacity=0.85).move_to([-2.6 + 0.13 * rev, y + 0.22, 0])
            b2 = Rectangle(width=0.26 * cost, height=0.38, stroke_width=0, fill_color=BAD, fill_opacity=0.85).move_to([-2.6 + 0.13 * cost, y - 0.22, 0])
            gap = rev - cost
            rows.add(VGroup(tx(name, 20, col, bold=True).move_to([-4.6, y, 0]), b1, tx(f"revenue {rev:.2f}c", 15, GOOD, bold=True).next_to(b1, RIGHT, buff=0.1),
                            b2, tx(f"cost {cost:.2f}c", 15, BAD, bold=True).next_to(b2, RIGHT, buff=0.1),
                            tx(f"{gap:+.2f}c a seat-mile", 18, GOOD if gap > 0 else BAD, bold=True).move_to([5.5, y, 0])))
        lab = tx("revenue and cost per available seat-mile, 2025, US cents", 17, GREY_A).to_edge(UP, buff=0.6)
        src = source("Forms 10-K for 2025 of Delta, Southwest and Spirit Aviation Holdings", size=12)
        d, l, s_ = S["dal"], S["luv"], S["save"]
        beat(self,
             "Three airlines, three answers. <bookmark mark='a'/> Delta earned "
             f"{d[0]:.2f} cents for each seat-mile in 2025 and spent {d[1]:.2f}: a margin of about two cents. "
             f"<bookmark mark='b'/> Southwest earned {l[0]:.2f} and spent {l[1]:.2f}: a quarter of a cent. "
             f"<bookmark mark='c'/> Spirit, the cheapest of them, earned {s_[0]:.2f} and spent {s_[1]:.2f}: it lost almost "
             "two cents on every seat it flew one mile.",
             base=[lab, src], steps=[rows[0], rows[1], rows[2]])

    def load(self):
        S = R["seat"]
        items = [("Delta", S["dal"][2], SKY, f"{S['dal'][2]:.0f}%"), ("Spirit", S["save"][2], BAD, f"{S['save'][2]:.1f}%"),
                 ("Southwest", S["luv"][2], CASH, f"{S['luv'][2]:.1f}%")]
        rows = hbars(items, max_value=100, x0=-0.6, top=1.2, row=1.0, length=6.4, size=18, bar_h=0.5)
        lab = tx("load factor, 2025: the share of seat-miles that carried a paying passenger", 16, GREY_A).to_edge(UP, buff=0.8)
        src = source("Forms 10-K for 2025 of Delta, Southwest and Spirit Aviation Holdings", size=12)
        beat(self,
             "The difference is not mostly how full the planes were. <bookmark mark='a'/> Delta's were "
             f"{S['dal'][2]:.0f} per cent full, <bookmark mark='b'/> Spirit's {S['save'][2]:.0f}, <bookmark mark='c'/> "
             f"Southwest's {S['luv'][2]:.0f}. A few points of load factor matter, but the gap between Delta and Spirit is in "
             "the price of each seat: who is sitting in it, and what they paid.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1], rows[2]])

    def breakeven(self):
        S = R["seat"]
        be = {}
        for k, (rev, cost, lf) in (("Delta", S["dal"]), ("Southwest", S["luv"]), ("Spirit", S["save"])):
            per_pax = rev / (lf / 100)                 # revenue per passenger-mile
            be[k] = (100 * cost / per_pax, lf)
        g = dumbbell([(k, b, a) for k, (b, a) in be.items()], x=(50, 100), center=(0.0, -0.4), width=8.0, height=3.6,
                     xticks=[50, 60, 70, 80, 90, 100], xfmt=lambda v: f"{v:.0f}%", size=17)
        for i, (k, (b, a)) in enumerate(be.items()):
            g.rows[i].add(tx(f"needs {b:.0f}%, flew {a:.0f}%", 15, GOOD if a >= b else BAD, bold=True)
                          .move_to(g.ax.c2p(100, 2.5 - i) + RIGHT * 1.45))
        lab = tx("grey: how full the planes had to be to cover costs at 2025's fares; coloured: how full they were", 16,
                 GREY_A).to_edge(UP, buff=0.8)
        tag = estimate_tag("this series' arithmetic from each Form 10-K for 2025: cost per seat-mile over revenue per passenger-mile", size=12)
        d, l, s_ = be["Delta"], be["Southwest"], be["Spirit"]
        beat(self,
             "Turn the same numbers around and ask: how full must a plane be to pay for itself? <bookmark mark='a'/> At "
             f"Delta's 2025 fares, about {d[0]:.0f} per cent full; it flew {d[1]:.0f}. <bookmark mark='b'/> Southwest needed "
             f"about {l[0]:.0f} and flew {l[1]:.0f}, a thin cushion. <bookmark mark='c'/> Spirit, at its fares, needed its "
             f"planes about {s_[0]:.0f} per cent full, every flight, all year. It flew {s_[1]:.0f}.",
             base=[g.frame, lab, tag], steps=[g.rows[0], g.rows[1], g.rows[2]])

    def southwest(self):
        S = R["seat"]
        c = stat_cards([(f"${S['luv_fare']:.0f}", "Southwest's average fare, 2025", CASH),
                        (f"{S['luv_stage']:,.0f} miles", "its average flight", SKY),
                        (f"{S['luv_pax'] / 1e3:,.0f}m", "passengers it carried", LEISURE),
                        (f"{S['luv_planes']:,.0f}", "aircraft", ALL)], y=0.6, size=34, span=12.4)
        planes = VGroup(*[draw.plane(1.2) for _ in range(5)]).arrange(RIGHT, buff=0.3).move_to([0, -1.6, 0])
        src = source("Southwest Airlines, Form 10-K for 2025", size=12)
        beat(self,
             "To put the cents in human terms: <bookmark mark='a'/> Southwest's average fare in 2025 was "
             f"{S['luv_fare']:.0f} dollars, <bookmark mark='b'/> for an average flight of {S['luv_stage']:,.0f} miles. "
             f"<bookmark mark='c'/> It carried {S['luv_pax'] / 1e3:,.0f} million passengers <bookmark mark='d'/> on "
             f"{S['luv_planes']:,.0f} aircraft, flying {S['luv_trips'] / 1e6:.2f} million trips with about "
             f"{S['luv_seats']:.0f} seats on each, nearly four thousand departures a day. It kept about a quarter of a cent per "
             "seat-mile as operating profit: on a typical flight, a few hundred dollars.",
             base=[planes, src], steps=[c[0], c[1], c[2], c[3]])
