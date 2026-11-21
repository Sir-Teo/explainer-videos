from __future__ import annotations

from videos.economics.econ68.common import *  # noqa: F403


class Design(VoiceoverScene):
    def construct(self):
        card(self, 3, r"The design, \ and its threats", r"What variation identifies the effect, \ and what could "
             r"fool it?", "Chapter three. The design, and its threats.", scale=("city",), horizon=("a year",))
        self.three()
        self.picture()
        self.threats()

    def three(self):
        cards = point_cards([
            (r"crossings: \ difference in differences", r"the two tunnels into the zone against eight crossings "
             r"elsewhere, \ each month of 2025 against the same month of 2024 \ (Part 4)", TOLL),
            (r"buses: \ difference in differences", r"routes inside the business district against routes outside, "
             r"\ year on year", BUS),
            (r"the clock: \ a discontinuity in time", r"the toll falls at 9 pm and rises at 5 am: \ entries just "
             r"before and just after each \ (Parts 47 and 49)", DATA),
            (r"the placebos", r"the same comparisons in 2023 and 2024, \ before any charge, \ should show "
             r"nothing", MODEL),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"three designs, \ and their placebos", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Three designs, each from earlier in the series. <bookmark mark='a'/> For crossings, a difference in "
            "differences: the two tunnels into the zone against eight crossings elsewhere, each month of 2025 "
            "against the same month a year before, so that seasons cancel. <bookmark mark='b'/> For buses, the "
            "same comparison: routes inside the business district against routes outside. <bookmark mark='c'/> For "
            "the clock, a discontinuity in time: the toll falls at nine at night and rises at five in the morning, "
            "so compare the minutes just before and just after. <bookmark mark='d'/> And for each, placebos: the "
            "same comparisons in 2023 and 2024, when there was no charge, should find nothing."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def picture(self):
        ax = plane([0, 4], [0, 10], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.6, y_length=4.6, xticks=[],
                   yticks=[], ylabel=r"log traffic", font_size=14)
        yrs = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(ax.ax.c2p(x, 0), DOWN, buff=0.12)
                       for x, t in ((0.5, "2023"), (1.5, "2024"), (2.5, "2025"), (3.5, "2026"))])
        start = vline(ax, 2.0, 0, 10, TOLL, 2.0)
        ctrl = path(ax, [0.5, 1.5, 2.5, 3.5], [4.0, 4.3, 4.6, 4.9], CTRL, 3.0, smooth=False)
        treat = path(ax, [0.5, 1.5, 2.5, 3.5], [7.0, 7.15, 6.9, 7.05], TOLL, 3.0, smooth=False)
        cf = DashedLine(ax.ax.c2p(1.5, 7.15), ax.ax.c2p(2.5, 7.45), color=TOLL, stroke_width=2.0)
        cf_trend = DashedLine(ax.ax.c2p(1.5, 7.15), ax.ax.c2p(2.5, 7.3), color=GREY_A, stroke_width=2.0)
        gap = DoubleArrow(ax.ax.c2p(2.62, 6.9), ax.ax.c2p(2.62, 7.45), buff=0, color=WHITE, stroke_width=2,
                          tip_length=0.14)
        side = VGroup(
            label(r"parallel trends: \\ without the charge, \\ the tunnels would have moved \\ like the other "
                  r"crossings", font_size=17, color=CTRL),
            label(r"the placebo years test it: \\ if the tunnels were already \\ drifting, \ the gap must be cut",
                  font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(ax.ax, RIGHT, buff=0.5)
        if side.get_right()[0] > 6.9:
            side.scale_to_fit_width(6.9 - side.get_left()[0])
        tag = island_tag(r"a sketch, \ not data", corner=DL, font_size=12)
        with self.voiceover(
            "Draw the identifying assumption before using it. <bookmark mark='a'/> The other crossings, in blue, "
            "and the tunnels, in red, year by year. <bookmark mark='b'/> The difference in differences assumes that "
            "without the charge the tunnels would have moved like the other crossings: the dashed red line. The "
            "effect is the gap between it and what happened. <bookmark mark='c'/> But if the tunnels were already "
            "drifting down before the charge, the right counterfactual is the grey line, and part of the gap is the "
            "drift. The placebo years are how we find out."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(yrs), FadeIn(start), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ctrl), Create(treat), run_time=1.8)
            vo.wait_until("b")
            self.play(Create(cf), GrowFromCenter(gap), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Create(cf_trend), FadeIn(side[1]))
        self.clear_scene()

    def threats(self):
        rows = VGroup(
            label(r"1. \ a trend: \ the tunnels were already losing traffic \ (chapter two)", font_size=21,
                  color=TOLL),
            label(r"2. \ diversion: \ drivers who avoid the tunnels may use other crossings, \ or the free East River "
                  r"bridges", font_size=21, color=CTRL),
            label(r"3. \ a smaller dose: \ tunnel users get a partial credit for the toll they already pay",
                  font_size=21, color=DATA),
            label(r"4. \ other news: \ the pandemic's recovery, \ office attendance, \ fares, \ weather", font_size=21,
                  color=GREY_A),
            label(r"5. \ the clock measures retiming, \ not how many trips were given up", font_size=21, color=MODEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(UP * 0.1)
        head = label(r"the threats, \ written before the results", font_size=28, color=E.ACCENT).to_edge(UP,
                                                                                                    buff=0.45)
        with self.voiceover(
            "Then write the threats down, before seeing a single estimate. <bookmark mark='a'/> One, a trend: the "
            "tunnels were already losing traffic. <bookmark mark='b'/> Two, diversion: drivers who avoid the "
            "tunnels may use other crossings, which would make the comparison group grow and the effect look "
            "bigger, or the free East River bridges, which are not in this data at all. <bookmark mark='c'/> Three, "
            "a smaller dose: tunnel drivers get a partial credit for the toll they already pay. <bookmark mark='d'/> "
            "Four, other news: the recovery from the pandemic, office attendance, fares and weather. <bookmark "
            "mark='e'/> Five, the clock design measures when people travel, not how many trips they gave up. A list "
            "like this, written first, is what separates a design from a story told afterwards."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
