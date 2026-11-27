from __future__ import annotations

from videos.industry.industry28.common import *  # noqa: F403


class Cheap(VoiceoverScene):
    def construct(self):
        card(self, 6, "Low cost, and lower", "Can an airline win by being cheapest?",
             "Chapter six. Low cost, and lower. Southwest built a large and long-profitable airline on low fares; a generation "
             "of imitators cut fares further, charged for everything else, and found the limit.", lit=("moat", "change"))
        self.margins()
        self.spirit()
        self.southwest()
        self.why()

    def margins(self):
        M = R["cheap"]["margins"]
        cols = {"Delta": SKY, "Southwest": CASH, "JetBlue": FUEL, "Spirit": BAD}
        series = {k: ({y: 100 * v for y, v in M[k].items() if y >= 2021}, c) for k, c in cols.items()}
        ch = line_chart(series, x=(2021, 2025), y=(-25, 15), xticks=[2021, 2022, 2023, 2024, 2025], yticks=[-20, -10, 0, 10],
                        yfmt=lambda v: f"{v:.0f}%", ylabel="operating profit per dollar of revenue", width=9.0, height=4.4,
                        center=(-1.2, -0.45))
        zero = DashedLine(ch.ax.c2p(2021, 0), ch.ax.c2p(2025, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        src = source("Forms 10-K via SEC company facts (operating income over revenue)", size=12)
        beat(self,
             "Since the pandemic the order has reversed. <bookmark mark='a'/> Delta, the full-service network airline, "
             f"kept about {100 * M['Delta'][2025]:.0f} cents of operating profit on each dollar in 2025. "
             f"<bookmark mark='b'/> Southwest, about {100 * M['Southwest'][2025]:.1f}. <bookmark mark='c'/> JetBlue lost money "
             f"every year from 2021. <bookmark mark='d'/> And Spirit lost {abs(100 * M['Spirit'][2024]):.0f} cents on every "
             "dollar in 2024.",
             base=[ch.frame, zero, src], steps=[[ch.lines["Delta"], ch.labels["Delta"]], [ch.lines["Southwest"], ch.labels["Southwest"]],
                                                [ch.lines["JetBlue"], ch.labels["JetBlue"]], [ch.lines["Spirit"], ch.labels["Spirit"]]])

    def spirit(self):
        a, b = R["cheap"]["planes"]
        row1 = VGroup(*[draw.plane(0.42) for _ in range(int(a // 8))]).arrange_in_grid(rows=3, buff=(0.05, 0.08)).move_to([-3.4, 0.3, 0])
        row2 = VGroup(*[draw.plane(0.42) for _ in range(int(b // 8))]).arrange_in_grid(rows=3, buff=(0.05, 0.08)).move_to([3.4, 0.3, 0])
        l1 = tx(f"end of 2024: {a:.0f} aircraft", 18, ALL, bold=True).next_to(row1, DOWN, buff=0.3)
        l2 = tx(f"end of 2025: {b:.0f}", 18, BAD, bold=True).next_to(row2, DOWN, buff=0.3)
        steps = bullets(["November 2024: Chapter 11", "March 2025: out of bankruptcy", "August 2025: Chapter 11 again"],
                        size=18).move_to([0, -2.2, 0])
        src = source("Spirit Aviation Holdings, Form 10-K for 2025 (each plane here stands for eight)", size=12)
        beat(self,
             "Spirit is the cautionary tale. <bookmark mark='a'/> It flew "
             f"{a:.0f} aircraft at the end of 2024. <bookmark mark='b'/> It filed for bankruptcy in November 2024, came out "
             "in March 2025, and filed again in August 2025. <bookmark mark='c'/> By the end of 2025 it had "
             f"{b:.0f} aircraft. The cheapest fares in America had not covered the cost of flying.",
             base=[src], steps=[[row1, l1], steps, [row2, l2]])

    def southwest(self):
        C = R["cheap"]
        (f0, f1), (p0, p1), (l0, l1) = C["luv_fare"], C["luv_pax"], C["luv_lf"]
        d = dumbbell([("average fare ($)", f0, f1)], x=(170, 200), center=(0.8, 1.2), width=7.2, height=1.0,
                     xticks=[170, 180, 190, 200], xfmt=lambda v: f"${v:.0f}", size=16)
        e = dumbbell([("passengers (m)", p0 / 1e3, p1 / 1e3)], x=(130, 145), center=(0.8, -0.4), width=7.2, height=1.0,
                     xticks=[130, 135, 140, 145], xfmt=lambda v: f"{v:.0f}m", size=16)
        g = dumbbell([("load factor (%)", l0, l1)], x=(75, 82), center=(0.8, -2.0), width=7.2, height=1.0,
                     xticks=[75, 77, 79, 81], xfmt=lambda v: f"{v:.0f}%", size=16)
        lab = tx("Southwest, 2024 (grey) to 2025: bag fees from 28 May 2025, assigned seats from 27 January 2026", 16,
                 GREY_A).to_edge(UP, buff=0.7)
        src = source("Southwest Airlines, Form 10-K for 2025", size=12)
        beat(self,
             "Even Southwest changed course. For decades it let every passenger check two bags free and board without an "
             "assigned seat. <bookmark mark='a'/> From May 2025 it charged for bags on most fares, and from January 2026 it "
             f"assigned seats, sold in bundles. Its average fare rose from {f0:.0f} to {f1:.0f} dollars. "
             f"<bookmark mark='b'/> It carried fewer passengers, {p1 / 1e3:.0f} million instead of {p0 / 1e3:.0f}, "
             f"<bookmark mark='c'/> and its planes were less full, {l1:.1f} per cent against {l0:.1f}. Yet it reports that "
             f"more than {C['luv_q4']:.0f} per cent of 2025's operating income came in the fourth quarter, once the changes had "
             "taken hold: fewer passengers, each paying more.",
             base=[lab, src], steps=[d, e, g])

    def why(self):
        g = VGroup(tx("Why the cheapest lost", 22, WHITE, bold=True),
                   tx("their whole advantage was cost, and wages, airports and fuel rose for everyone", 18, BAD),
                   tx("the big airlines sold 'basic economy' seats at their fares on the same planes", 18, SKY),
                   tx("and the big airlines had what they lacked: business travellers, long routes and the card money", 18, CARD)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, 0.2, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "Why? In this series' reading, <bookmark mark='a'/> a low-cost airline's only advantage is its cost, and "
             "wages, airport fees and fuel rose for everyone after 2021. <bookmark mark='b'/> The big airlines learned to sell "
             "bare seats, 'basic economy', at low-cost fares on the same planes they fly anyway, the Run it trick of selling "
             "one seat at two prices. <bookmark mark='c'/> And the big airlines had what the cheap ones lacked: business "
             "travellers, long international routes, and the bank in the airline.",
             base=[tag], steps=[g[:2], g[2], g[3]])
