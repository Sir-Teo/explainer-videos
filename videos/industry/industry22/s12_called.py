from __future__ import annotations

from videos.industry.industry22.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 10, "Called it?", "How well does a brand company forecast its own growth?",
             "Chapter ten. Called it? Procter and Gamble tells investors each summer how much it expects its sales to grow.",
             lit=("change",))
        self.pg()
        self.need()
        self.ours()

    def pg(self):
        C = R["called"]
        pa = viz.plot_axes([-1, 6], [0, 3], x_length=10.0, y_length=3.6, xticks=[-1, 0, 1, 2, 3, 4, 5, 6],
                           xfmt=lambda v: f"{int(v)}%", grid=False, size=13).move_to([0.4, 0.3, 0])
        ax = pa.ax
        y25, y26, y27 = 2.5, 1.5, 0.5
        r25 = Line(ax.c2p(C["g25"][0], y25), ax.c2p(C["g25"][1], y25), stroke_color=PRICE, stroke_width=12)
        l25 = tx(f"July 2024: organic sales growth of {C['g25'][0]}-{C['g25'][1]}% in fiscal 2025", 14, PRICE).next_to(r25, UP, buff=0.12)
        a25 = marker(ax, C["a25"], y25, f"actual: {C['a25']}%", BAD, side=DOWN)
        r26 = Line(ax.c2p(C["g26"][0], y26), ax.c2p(C["g26"][1], y26), stroke_color=PRICE, stroke_width=12)
        l26 = tx(f"July 2025: organic sales growth of {C['g26'][0]}-{C['g26'][1]}% in fiscal 2026", 14, PRICE).next_to(r26, UP, buff=0.12)
        a26 = marker(ax, C["a26"], y26, f"actual: {C['a26']}%", GOOD, side=DOWN)
        r27 = Line(ax.c2p(C["g27"][0], y27), ax.c2p(C["g27"][1], y27), stroke_color=PRICE, stroke_width=12)
        l27 = tx(f"July 2026: {C['g27'][0]}-{C['g27'][1]}% in fiscal 2027", 14, PRICE).next_to(r27, DOWN, buff=0.12)
        q1 = marker(ax, C["q1"], y27, f"first quarter: {C['q1']}%", GOOD, side=UP)
        nm = VGroup(tx("FY25", 20, WHITE, bold=True).next_to(ax.c2p(-1, y25), LEFT, buff=0.3), tx("FY26", 20, WHITE, bold=True).next_to(ax.c2p(-1, y26), LEFT, buff=0.3),
                    tx("FY27", 20, WHITE, bold=True).next_to(ax.c2p(-1, y27), LEFT, buff=0.3))
        src = source("The Procter & Gamble Company, Forms 8-K of 30 July 2024, 29 July 2025, 29 July 2026 and 22 October 2026; "
                     "Forms 10-K for fiscal 2025 and 2026", size=12)
        beat(self,
             "P&G forecasts organic sales growth: growth without currency, acquisitions and sales of businesses. "
             f"<bookmark mark='a'/> In July 2024 it expected {C['g25'][0]} to {C['g25'][1]} per cent for fiscal 2025, and "
             f"delivered {C['a25']}, below the bottom of its range. In July 2025 it expected {C['g26'][0]} to {C['g26'][1]} per cent for the year to June "
             f"2026, a wide range in an uncertain year. <bookmark mark='b'/> It delivered {C['a26']} per cent, in the lower "
             f"half. <bookmark mark='c'/> In July 2026 it expected {C['g27'][0]} to {C['g27'][1]} per cent for fiscal 2027, "
             "with about a billion dollars of higher costs for materials, energy and transport ahead. <bookmark mark='d'/> "
             f"Then the first quarter came in at {C['q1']} per cent, above the whole range, and P&G kept its forecast "
             "unchanged. Unlike Lilly in Part 20 and Intuitive in Part 21, whose forecasts leaned low, P&G's have lately "
             "leaned high.",
             base=[pa, nm, src], steps=[[r25, l25, a25, r26, l26], a26, [r27, l27], q1])

    def need(self):
        C = R["called"]
        rest = (4 * C["g27"][1] - C["q1"]) / 3
        items = [("first quarter, actual", C["q1"], GOOD, f"{C['q1']}%"),
                 ("each later quarter, needed for 3%", rest, PRICE, f"{rest:.1f}%"),
                 ("fiscal 2026, the whole year", C["a26"], GREY_B, f"{C['a26']}%")]
        rows = hbars(items, max_value=5, x0=0.6, top=1.2, row=1.0, length=5.6, size=17, bar_h=0.5)
        tag = estimate_tag("this series' arithmetic: equal-sized quarters", size=12)
        beat(self,
             "What would it take to reach the top of the range? <bookmark mark='a'/> The first quarter grew "
             f"{C['q1']} per cent. <bookmark mark='b'/> For the year to reach {C['g27'][1]} per cent, treating the quarters as "
             f"equal, the other three would need to average about {rest:.1f} per cent. <bookmark mark='c'/> In the whole of "
             f"fiscal 2026 P&G managed {C['a26']}. The first quarter makes it possible; the year before makes it hard.",
             base=[rows.axis, tag], steps=[rows[0], rows[1], rows[2]])

    def ours(self):
        C = R["called"]
        claim = VGroup(tx("Our call, 27 November 2026", 20, PRICE, bold=True),
                       tx(f"P&G's organic sales growth for fiscal 2027 will be {C['g27'][1]}% or more, the top of its range.", 21, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, PRICE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([0, 1.7, 0])
        why = bullets([f"for: the first quarter grew {C['q1']}%, with volume back",
                       "against: a billion dollars of higher costs, and a forecast left unchanged after a strong quarter",
                       f"its record: {C['a25']}% against {C['g25'][0]}-{C['g25'][1]}%, then {C['a26']}% against {C['g26'][0]}-{C['g26'][1]}%"], size=18).move_to([0, -0.4, 0])
        rule = tx("scored on P&G's fiscal 2027 results, due late July 2027", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             f"Now ours. <bookmark mark='a'/> We say P&G's organic sales will grow {C['g27'][1]} per cent or more in fiscal "
             f"2027, the top of its range, and give it {100 * C['prob']:.0f} per cent. <bookmark mark='b'/> For: a first "
             f"quarter at {C['q1']} per cent, with shoppers buying more. Against: rising costs, which tempt a company to "
             "raise prices and lose volume; a company that did not raise its own forecast after a strong start; and two "
             "years in which it landed in the lower part of its range or below it. "
             "<bookmark mark='c'/> P&G's results next July will settle it, and the call stays in the log either way.",
             base=[tag], steps=[claim, why, rule])
