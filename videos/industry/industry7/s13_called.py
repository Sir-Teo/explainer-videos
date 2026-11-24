from __future__ import annotations

from explainer.industry.calls import calls
from explainer.industry.register import get
from videos.industry.industry7.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 14, "Called it?", "What happens to a market size once someone builds a business on it?",
             "Chapter fourteen. Called it?", lit=("change",))
        self.theirs()
        self.ours()
        self.scoreboard()

    def theirs(self):
        W = R["wework"]
        rows = [(VGroup(draw.person(0.5, color=STONE), RoundedRectangle(corner_radius=0.04, width=0.9, height=0.12,
                                                                       stroke_width=0, fill_color="#C9A26B",
                                                                       fill_opacity=1)).arrange(DOWN, buff=0.02),
                 "WeWork, August 2019", f"a ${W['total']:.0f} trillion opportunity",
                 "share sale withdrawn September 2019; Chapter 11, November 2023", "#E8554E"),
                (VGroup(draw.bottle(0.8, color=WATER)), "Beverage Marketing, May 2025",
                 f"bottled water to about {get('water.bmc.forecast'):.0f} gallons a person by around 2030",
                 f"pending: {get('water.bmc.percap.2023'):.1f} in 2023, {get('water.bmc.percap.2024'):.1f} in 2024", GOLD)]
        cards = VGroup()
        for pic, who, claim, outcome, col in rows:
            pic.scale_to_fit_height(0.9)
            t_ = VGroup(tx(who, 22, WHITE, bold=True), tx(claim, 19, GREY_A), tx(outcome, 18, col)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08)
            cards.add(VGroup(pic, t_).arrange(RIGHT, buff=0.5))
        cards.arrange(DOWN, aligned_edge=LEFT, buff=0.8).move_to([0, 0.3, 0])
        lesson = tx("A market size is only as good as the definition, and the business, built on it.", 20, GOLD,
                    bold=True).to_edge(DOWN, buff=0.6)
        src = source("The We Company, Forms S-1 and RW (2019); WeWork Inc., Form 8-K (2023); Beverage Marketing, May 2025",
                     size=13)
        with self.voiceover(
            "Every part ends with forecasts. This part's are market sizes that someone built on. "
            f"<bookmark mark='a'/> WeWork's {W['total']:.0f} trillion dollars counted every office worker in its "
            "target cities as a possible member. The share sale was withdrawn within weeks, and in November 2023 the "
            "company filed for bankruptcy. The opportunity was "
            "real in the sense that the money is spent on offices. It was never WeWork's to take. "
            "<bookmark mark='b'/> And a forecast still open: the Beverage Marketing Corporation expects Americans to "
            f"drink about {get('water.bmc.forecast'):.0f} gallons of bottled water each by around the end of this "
            f"decade. In 2024 they drank {get('water.bmc.percap.2024'):.1f}. At the pace of the last year it would "
            "arrive on time; at the pace of the year before, it would not. <bookmark mark='c'/> A market size is "
            "only as good as its definition, and as the business that is built on it."
        ) as vo:
            chead = tx("Market sizes that someone built on", 26, GOLD, bold=True).to_edge(UP, buff=0.6)
            self.play(FadeIn(src), FadeIn(chead), *[FadeIn(c_[0], scale=0.8) for c_ in cards])
            for c_, m in zip(cards, "ab"):
                vo.wait_until(m)
                self.play(FadeIn(c_[1], shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(lesson, shift=UP * 0.1))
        self.clear_scene()

    def ours(self):
        c = calls(7, ours=True)[0]
        C = R["census"]
        box = RoundedRectangle(corner_radius=0.15, width=12.2, height=2.5, fill_color="#141A24", fill_opacity=1,
                               stroke_color=GOLD, stroke_width=2).move_to(UP * 2.0)
        body = VGroup(tx("This series' call, made 24 November 2026", 22, GOLD, bold=True),
                      tx("The Census Bureau's shipments of US bottled water manufacturers for 2026", 19),
                      tx(f"will be above $7.5bn (2024: ${C['shipments'][-1]:.2f}bn).", 19),
                      tx("Probability: 65%. Scored on the Census's first figure for 2026, about mid-2028.", 17, GOLD)
                      ).arrange(DOWN, buff=0.12).move_to(box)
        pa = viz.plot_axes([2011.5, 2026.8], [0, 10], x_length=8.4, y_length=3.0, xticks=[2012, 2016, 2020, 2024],
                           yticks=[5, 7.5, 10], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}bn", size=14)
        pa.move_to([0.4, -1.75, 0])
        bars = viz.year_bars(pa, C["years"], C["shipments"], FACTORY, width=0.5)
        ghost = Rectangle(width=0.5, height=pa.ax.c2p(0, 7.5)[1] - pa.ax.c2p(0, 0)[1], stroke_color=GOLD, stroke_width=2,
                          fill_opacity=0).move_to(pa.ax.c2p(2026, 0), aligned_edge=DOWN)
        q = tx("?", 30, GOLD, bold=True).next_to(ghost, UP, buff=0.08)
        line = DashedLine(pa.ax.c2p(2011.5, 7.5), pa.ax.c2p(2026.8, 7.5), stroke_color=GOLD, stroke_width=1.5)
        with self.voiceover(
            "And this series' own call. <bookmark mark='a'/> When the Census Bureau publishes its figure for 2026, "
            "American bottled-water plants will have shipped more than seven and a half billion dollars' worth, "
            f"against {C['shipments'][-1]:.2f} billion in 2024. <bookmark mark='b'/> For it: Americans drink a little "
            "more bottled water every year, and the plants that make it are counted the same way each time. "
            "<bookmark mark='c'/> Against it: producer prices have been flat since 2023, and this series fell by a "
            "sixth in a single year, from 2022 to 2023. We put it at sixty-five percent, and will score it when the "
            "figure appears, in about the middle of 2028."
        ) as vo:
            self.play(FadeIn(box), FadeIn(body[0]))
            vo.wait_until("a")
            self.play(FadeIn(body[1:3]), FadeIn(pa), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.06),
                      run_time=2.0)
            self.play(Create(line), Create(ghost), FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(bars[-1], color=WHITE))
            vo.wait_until("c")
            self.play(Indicate(bars[-2], color="#E8554E"), FadeIn(body[3]))
        self.clear_scene()
        assert "bottled water" in c.claim

    def scoreboard(self):
        """The series' open calls so far, one per part, with the month each can be scored."""
        short = {1: "smartphone shipments in 2026 below 1.15 billion",
                 2: "health care to outnumber factories and shops by 2030 (40%)",
                 3: "Microsoft's free cash flow falls in fiscal 2027 as profit rises (65%)",
                 4: "solar to beat coal in some month of 2027 (55%)",
                 5: "seven of ten top-return industries still near the top in 2028 (75%)",
                 6: "Micron to report a quarter 25% below its peak by 2028 (55%)",
                 7: "bottled-water shipments for 2026 above $7.5bn (65%)"}
        mine = sorted(calls(ours=True), key=lambda c: c.due)
        rows = VGroup()
        for c in mine:
            due = c.due
            row = VGroup(tx(f"Part {c.part}", 18, GOLD, bold=True), tx(short.get(int(c.part), c.claim[:60]), 18, WHITE),
                         tx(f"due {due}", 17, GREY_B))
            row[1].next_to(row[0], RIGHT, buff=0.35)
            row[2].next_to(row[1], RIGHT, buff=0.35)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0, -0.2, 0])
        for r_ in rows:
            r_[1].align_to(rows[0][1], LEFT)
            r_[2].align_to([5.2, 0, 0], LEFT)
        if rows.width > 13.2:
            rows.scale_to_fit_width(13.2)
        head = tx("The scoreboard: this series' open calls", 26, GOLD, bold=True).to_edge(UP, buff=0.5)
        first = mine[0]
        src = source("this series' calls: explainer/industry/calls.py, each with its scoring rule and source", size=13)
        with self.voiceover(
            "Every part of this series has made a call like that, with a date and a rule for scoring it. "
            "<bookmark mark='a'/> Here they are, ordered by when they come due. <bookmark mark='b'/> The first, on "
            f"smartphone shipments, can be scored in {first.due[:4]}, when the year's first full count of phones "
            "shipped is published; the last, on jobs in health care, not until 2031. <bookmark mark='c'/> "
            "When a call comes due, the series will show the result in the part it belongs to, right or wrong, and "
            "keep the record. A forecaster who never writes down a number, a date and a probability can never be "
            "shown to be wrong, and so can never be shown to be any good."
        ) as vo:
            self.play(FadeIn(src), FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.2), run_time=3.0)
            vo.wait_until("b")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.03))
            vo.wait_until("c")
            self.play(Indicate(rows[-1], color=WHITE, scale_factor=1.03))
        self.clear_scene()
