from __future__ import annotations

from videos.industry.industry23.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 11, "Called it?", "Can a fashion company forecast its own margin?",
             "Chapter eleven. Called it? Inditex gives no number for next year's sales. It forecasts its gross margin, the number "
             "that tells you how well it guessed.", lit=("change",))
        self.guide()
        self.need()
        self.ours()

    def guide(self):
        C = R["called"]
        pa = viz.plot_axes([57.0, 60.0], [0, 2], x_length=10.0, y_length=2.8, xticks=[57.0, 57.5, 58.0, 58.5, 59.0, 59.5, 60.0],
                           xfmt=lambda v: f"{v:.1f}%", grid=False, size=13).move_to([0.4, 0.4, 0])
        ax = pa.ax
        band = Line(ax.c2p(C["lo"], 1.2), ax.c2p(C["hi"], 1.2), stroke_color=PRICE, stroke_width=14)
        bl = tx(f"guidance for 2026: stable, +/-50 bps: {C['lo']:.1f}% to {C['hi']:.1f}%", 15, PRICE).next_to(band, UP, buff=0.15)
        base = marker(ax, C["base"], 1.2, f"FY2025: {C['base']}%", WHITE, side=DOWN)
        h1 = marker(ax, C["h1"], 0.5, f"first half of 2026: {C['h1']}%", GOOD, side=DOWN)
        src = source("Inditex, FY2025 results and interim 1H2026 results", size=12)
        beat(self,
             "Inditex gives one forecast a year that matters here. <bookmark mark='a'/> With its results in March 2026 it "
             f"said it expected 'a stable gross margin', within half a point either way of the previous year's "
             f"{C['base']} per cent: somewhere between {C['lo']:.1f} and {C['hi']:.1f}. <bookmark mark='b'/> That is the "
             "year it was measuring against. <bookmark mark='c'/> In the first half of 2026 it reported "
             f"{C['h1']} per cent, {100 * (C['h1'] - C['h1_prev']):.0f} basis points better than a year before, and "
             "repeated the forecast unchanged.",
             base=[pa, src], steps=[[band, bl], base, h1])

    def need(self):
        C = R["called"]
        items = [("first half of 2026, actual", C["h1"], GOOD, f"{C['h1']}%"),
                 ("second half of 2025, actual", C["h2_gm25"], GREY_B, f"{C['h2_gm25']:.1f}%"),
                 (f"second half of 2026, needed for {C['call']}%", C["need"], PRICE, f"{C['need']:.1f}%")]
        rows = hbars([(a, v - 55, c, t) for a, v, c, t in items], max_value=5, x0=0.8, top=1.2, row=1.0, length=5.0, size=17, bar_h=0.5)
        floor = tx("bars start at 55%", 12, GREY_B).move_to([0.8, -1.8, 0])
        tag = estimate_tag(f"this series' arithmetic: the second half's sales grow {100 * C['growth']:.1f}%, as the first half's did", size=12)
        beat(self,
             f"What would it take for the full year to reach {C['call']} per cent? <bookmark mark='a'/> The first half is "
             f"in, at {C['h1']}. <bookmark mark='b'/> The second half of 2025, which holds the winter sale, ran at "
             f"{C['h2_gm25']:.1f}. <bookmark mark='c'/> If the second half's sales grow as the first half's did, the second "
             f"half of 2026 would need {C['need']:.1f} per cent: about the same as last year's. Not much to ask, unless the "
             "winter sale is deeper than last year's.",
             base=[rows.axis, floor, tag], steps=[rows[0], rows[1], rows[2]])

    def ours(self):
        C = R["called"]
        claim = VGroup(tx("Our call, 27 November 2026", 20, PRICE, bold=True),
                       tx(f"Inditex's gross margin for the year to January 2027 will be {C['call']}% or more.", 22, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, PRICE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([0, 1.7, 0])
        why = bullets([f"for: the first half was {C['h1']}%, 40 basis points up on the year before",
                       "against: the second half holds the deepest sale, and its fourth quarter ran at 54.8% last year",
                       f"its own guidance, {C['lo']:.1f}-{C['hi']:.1f}%, puts {C['call']}% near the top"], size=18).move_to([0, -0.4, 0])
        rule = tx("scored on Inditex's FY2026 results, due March 2027", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             f"Now ours. <bookmark mark='a'/> We say Inditex's gross margin for the year to January 2027 will be "
             f"{C['call']} per cent or more, and give it {100 * C['prob']:.0f} per cent: a little better than even. "
             "<bookmark mark='b'/> For: a first half up forty basis points, and a business built to guess less. Against: "
             "the half still to come holds the winter sale, when last year's margin fell to its lowest, and its own forecast "
             f"puts {C['call']} per cent near the top of the range. <bookmark mark='c'/> Inditex's results in March 2027 "
             "will settle it, and the call stays in the log either way.",
             base=[tag], steps=[claim, why, rule])
