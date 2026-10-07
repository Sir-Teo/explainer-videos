from __future__ import annotations

import datetime as dt

import numpy as np

from explainer import *  # noqa: F403
from videos.opposing_forces.common import TimeChart, data, label, last, show_chapter_card, source, tagged, ts, window, ym


def fed_path():
    """(t, upper, lower) step points of the Fed's target range."""
    ch = data()["fed_upper_daily_changes"]
    pts = []
    for i, (d, up, lo) in enumerate(ch):
        day = dt.date.fromisoformat(d)
        t = ym(day.year, day.month, day.day)
        if pts:
            pts.append((t, pts[-1][1], pts[-1][2]))
        pts.append((t, up, lo))
    pts.append((ym(2026, 10, 6), pts[-1][1], pts[-1][2]))
    return np.array(pts)


class FedDilemma(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 9, r"The Fed's dilemma")
        self.path()
        self.constituencies()

    # ------------------------------------------------------------------
    def path(self):
        p = fed_path()
        p = p[p[:, 0] >= 2021.5]
        changes = [(c[0], c[1]) for c in data()["fed_upper_daily_changes"] if c[0] >= "2025-01-01"]
        assert [c[1] for c in changes] == [4.25, 4.0, 3.75, 4.0] and changes[-1][0] == "2026-09-17"
        t2, y2 = ts("dgs2_weekly")
        t2, y2 = window(t2, y2, 2021.5)
        y2_now = last("dgs2_daily")
        assert y2_now > p[-1, 1] + 0.7
        ch = TimeChart((2021.5, 2026.85), (0, 6), width=10.4, height=4.6, x_ticks=range(2022, 2027),
                       y_ticks=[0, 1, 2, 3, 4, 5, 6], y_fmt=lambda y: rf"{y:g}\%").move_to(DOWN * 0.45)
        band = Polygon(*([ch.c2p(a, b) for a, b in zip(p[:, 0], p[:, 1])] + [ch.c2p(a, b) for a, b in zip(p[::-1, 0], p[::-1, 2])]),
                       stroke_width=0, fill_color=C.POLICY, fill_opacity=0.55)
        edge = ch.line(p[:, 0], p[:, 1], C.POLICY, 3)
        t_band = tagged(r"the Fed's target range", font_size=26, color=C.POLICY).move_to(ch.c2p(2022.6, 4.9))
        l2 = ch.line(t2, y2, C.RATE, 3).set_stroke(opacity=0.9)
        t_2 = tagged(rf"2-year Treasury yield: {y2_now:.2f}\%", font_size=26, color=C.RATE).next_to(
            ch.c2p(2026.8, y2_now), UP, buff=0.2).shift(LEFT * 1.6)
        cuts25 = tagged(r"2025: three cuts", font_size=24, color=C.POLICY).move_to(ch.c2p(2025.3, 2.9))
        hike26 = tagged(r"Sept 2026: a hike", font_size=24, color=C.POLICY).move_to(ch.c2p(2026.25, 2.25))
        src = source(r"FRED (DFEDTARU, DFEDTARL, DGS2)")
        with self.voiceover(
            "So what can the Federal Reserve do? <bookmark mark='a'/> Here's its policy rate. It raised rates hard in "
            "2022 and 2023, then started cutting. <bookmark mark='b'/> In late 2025 it cut three more times, <bookmark "
            "mark='c'/> and last month, in September 2026, it reversed course and raised rates again."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ch), FadeIn(src))
            self.play(FadeIn(band), Create(edge), FadeIn(t_band), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(cuts25))
            vo.wait_until("c")
            self.play(FadeIn(hike26))

        msg = tagged(r"the market's message: the 2025 cuts were a mistake; reverse them", font_size=28, color=YELLOW)
        msg.to_edge(UP, buff=0.4)
        with self.voiceover(
            "The bond market wants more. <bookmark mark='y'/> The two-year Treasury yield, which roughly tracks where "
            "investors expect the Fed's rate to be over the next couple of years, is about 4.8 percent: well above the "
            "Fed's current range. <bookmark mark='m'/> Timmer reads the market's message bluntly: the Fed shouldn't have "
            "eased in 2025, and now it needs to take those cuts back."
        ) as vo:
            vo.wait_until("y")
            self.play(Create(l2), FadeIn(t_2), run_time=2)
            vo.wait_until("m")
            self.play(FadeIn(msg, shift=DOWN * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def constituencies(self):
        mort = last("mortgage_weekly")
        lever = VGroup(RoundedRectangle(width=2.6, height=1.3, corner_radius=0.2, stroke_color=C.POLICY, stroke_width=3,
                                        fill_color=C.POLICY, fill_opacity=0.2),
                       label(r"one interest rate", font_size=30, color=C.POLICY))
        lever[1].move_to(lever[0])
        lever.move_to(LEFT * 4.6)
        who = [
            (r"the government", r"can push the problem down the road, if markets let it", 0.55, C.DEBT),
            (r"homebuyers", rf"mortgage rates at {mort:.1f}\%", 0.9, C.MORTGAGE),
            (r"weaker companies", r"must refinance at higher rates", 0.85, C.EQUAL_WEIGHT),
            (r"AI hyperscalers", r"returns far above the cost of money: don't care", 0.05, C.EARNINGS),
        ]
        rows = VGroup()
        for name, why, pain, col in who:
            meter = VGroup(Rectangle(width=2.2, height=0.32, stroke_color=GREY_B, stroke_width=2),
                           Rectangle(width=max(0.03, 2.2 * pain), height=0.32, stroke_width=0, fill_color=C.RATE,
                                     fill_opacity=0.85))
            meter[1].align_to(meter[0], LEFT)
            text = VGroup(label(name, font_size=30, color=col), label(why, font_size=22, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.06)
            rows.add(VGroup(text, meter).arrange(RIGHT, buff=0.4))
        for r in rows:
            r[1].align_to(rows[0][1], LEFT)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(RIGHT * 1.6)
        for r in rows:
            r[1].move_to([rows.get_right()[0] - 1.1, r[1].get_y(), 0])
        pain_l = label(r"how much a hike hurts (schematic)", font_size=24, color=C.RATE).next_to(rows, UP, buff=0.3)
        pain_l.align_to(rows[0][1], LEFT)
        wires = VGroup(*[Line(lever.get_right(), r[0].get_left() + LEFT * 0.15, color=GREY_D, stroke_width=2) for r in rows])
        with self.voiceover(
            "But the Fed has one blunt instrument, and many different borrowers on the other end of it. <bookmark "
            "mark='a'/> The government can keep pushing its problem down the road, as long as the bond market lets it. "
            "<bookmark mark='b'/> Homebuyers can't: they face mortgage rates above seven percent. <bookmark mark='c'/> "
            "Neither can weaker companies that need to refinance their debt. <bookmark mark='d'/> And the AI giants "
            "barely notice: the returns they expect on what they borrow are far above the Fed's price of money."
        ) as vo:
            self.play(FadeIn(lever), FadeIn(pain_l))
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(Create(wires[i]), FadeIn(rows[i], shift=RIGHT * 0.2), run_time=0.7)

        line = tagged(r"one rate, many constituencies: the Fed is stuck", font_size=32, color=YELLOW).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Raise rates enough to satisfy the bond market, and you crush the borrowers who are already struggling, "
            "while barely touching the ones driving the boom. <bookmark mark='s'/> That's why Timmer describes the Fed as "
            "stuck."
        ) as vo:
            vo.wait_until("s")
            self.play(FadeIn(line, shift=UP * 0.2))
        self.clear_scene()
