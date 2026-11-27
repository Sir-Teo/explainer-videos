from __future__ import annotations

from videos.industry.industry19.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 11, "Called it?", "How well does the robot industry forecast itself?",
             "Chapter eleven. Called it? Every autumn the International Federation of Robotics counts last year's "
             "robots and forecasts the next. How good are its forecasts?", lit=("change",))
        self.ifr()
        self.cat()
        self.ours()

    def cat(self):
        B = R["backlog"]
        a = VGroup(tx("February 2026, Caterpillar's annual report:", 17, GREY_A),
                   tx("2026 sales to grow 'around the top end of our 5 to 7 percent' target", 19, WHITE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([0, 1.6, 0])
        b = VGroup(tx("October 2026, its third-quarter report:", 17, GREY_A),
                   tx("'sales and revenues growth in the mid-to-high teens'", 19, MACHINE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([0, 0.0, 0])
        b.align_to(a, LEFT)
        c = tx("Eight months, and the company's own forecast of its year more than doubled.", 19, PRICE, bold=True).move_to([0, -1.8, 0])
        src = source("Caterpillar Inc., Form 10-K 2025 and Form 10-Q for the third quarter of 2026", size=12)
        beat(self,
             "Companies forecast themselves too. <bookmark mark='a'/> In February 2026 Caterpillar expected its sales "
             f"to grow around {B['outlook']} per cent that year. <bookmark mark='b'/> By October it expected growth in the "
             "mid-to-high teens. <bookmark mark='c'/> A backlog tells a maker a great deal about the coming year, and "
             "still the year surprised it. Forecasting machine demand is hard even from inside the factory.",
             base=[src], steps=[a, b, c])

    def ifr(self):
        C = R["called"]
        rows = [("2022", "October 2022: 'almost 570,000'", C["fc2022"], C["act2022"]),
                ("2024", "September 2024: 'level off at 541,000'", C["fc2024"], C["act2024"]),
                ("2025", "October 2022: 2022 to 2025, 'medium to upper single-digit' growth", sum(C["implied2025"]) / 2, C["act2025"])]
        pa = viz.plot_axes([450, 750], [0, 3], x_length=9.0, y_length=3.6, xticks=[500, 600, 700], xfmt=lambda v: f"{int(v)}k",
                           grid=False, size=13).move_to([0.8, -0.3, 0])
        ax = pa.ax
        steps_ = []
        for i, (yr, said, fc, act) in enumerate(rows):
            y = 2.5 - i
            f = Dot(ax.c2p(fc / 1e3, y), radius=0.1, color=PRICE)
            a = Dot(ax.c2p(act / 1e3, y), radius=0.1, color=GOOD if abs(act / fc - 1) < 0.03 else BAD)
            ln = Line(f.get_center(), a.get_center(), stroke_color=GREY_B, stroke_width=2)
            nm = tx(yr, 20, WHITE, bold=True).next_to(ax.c2p(450, y), LEFT, buff=0.3)
            s1 = tx(said, 13, PRICE).next_to(f, UP, buff=0.12)
            s2 = tx(f"actual {act / 1e3:,.0f}k", 13, a.get_color(), bold=True).next_to(a, DOWN, buff=0.12)
            if i == 2:
                band = Line(ax.c2p(C["implied2025"][0] / 1e3, y), ax.c2p(C["implied2025"][1] / 1e3, y), stroke_color=PRICE,
                            stroke_width=8, stroke_opacity=0.5)
                steps_.append(VGroup(band, f, a, ln, nm, s1, s2))
            else:
                steps_.append(VGroup(f, a, ln, nm, s1, s2))
        key = tx("world installations of industrial robots: forecast (gold) against outcome", 15, GREY_A).to_edge(DOWN, buff=0.7)
        src = source("International Federation of Robotics, press releases of 13 October 2022, 24 September 2024 and 24 "
                     "September 2026; AI Index Report 2026 via Our World in Data", size=12)
        beat(self,
             "Three of its forecasts, against what happened. <bookmark mark='a'/> In October 2022 it expected almost "
             f"570,000 robots to be installed that year; {C['act2022']:,} were, three per cent fewer. "
             "<bookmark mark='b'/> In September 2024 it expected installations that year to level off at 541,000; they "
             f"were about {C['act2024'] / 1e3:.0f} thousand, right on. <bookmark mark='c'/> But its medium-term view of "
             "2022 was too high: growth in the mid to upper single digits each year to 2025 would have meant about "
             f"{C['implied2025'][0] / 1e3:.0f} to {C['implied2025'][1] / 1e3:.0f} thousand robots in 2025. The count was "
             f"a little over {C['act2025'] / 1e3:.0f} thousand. A forecaster close to its industry is good on the next "
             "year, and hopeful about the years after.",
             base=[pa, key, src], steps=steps_)

    def ours(self):
        C = R["called"]
        claim = VGroup(tx("Our call, 27 November 2026", 20, PRICE, bold=True),
                       tx(f"World installations of industrial robots in 2026 will come in below the IFR's {C['fc2026'] / 1e3:.0f},000.", 21, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, PRICE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([0, 1.7, 0])
        why = bullets(["for: its medium-term forecast of 2022 ran high, and Japan and Germany are buying fewer",
                       "against: its one-year forecasts have been close, and China's installations rose 20% in 2025",
                       "the forecast needs 9% growth on 2025"], size=18).move_to([0, -0.4, 0])
        rule = tx("scored on the IFR's World Robotics press release of autumn 2027", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             "Now ours. <bookmark mark='a'/> The IFR forecasts that the world will install "
             f"{C['fc2026'] / 1e3:.0f} thousand robots in 2026, nine per cent more than in 2025. We say it will come in "
             f"below that, and give it {100 * C['prob']:.0f} per cent. <bookmark mark='b'/> For: its longer forecasts have "
             "run high, and Japan and Germany are buying fewer robots. Against: its one-year forecasts have been close, "
             "and China's purchases rose by a fifth last year. <bookmark mark='c'/> The IFR's own count, next autumn, "
             "will settle it.",
             base=[tag], steps=[claim, why, rule])
