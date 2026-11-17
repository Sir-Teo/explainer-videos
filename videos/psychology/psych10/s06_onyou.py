from __future__ import annotations

import numpy as np

from videos.psychology.psych10.common import *  # noqa: F403


def _hm(h: float) -> str:
    """A length of time as text: 1.5 -> 1 h 30."""
    m = int(round(h * 60))
    return rf"{m} min" if m < 60 else rf"{m // 60} h {m % 60:02d}"


class OnYou(VoiceoverScene):
    def construct(self):
        self.card()
        self.ask()
        self.read()

    def card(self):
        card = chapter_card(5, r"On you: \ your chronotype", r"Where does your clock sit, and how far is your timetable from it?",
                            lit=(), part=PART, scale=("person",), marr=("what",))
        with self.voiceover(
            "Chapter five. On you: your chronotype."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def ask(self):
        stage = demo_stage(13.0, 6.2, r"On you: \ four numbers", center=[0, -0.2, 0])
        c = stage.box.get_center()
        blocks = VGroup()
        for i, (when, col) in enumerate(((r"on days when you work or study", GREY_B),
                                         (r"on free days, \ when no alarm rings", SLEEPC))):
            x = c[0] - 3.1 + 6.2 * i
            box = RoundedRectangle(width=5.6, height=3.4, corner_radius=0.15, color=col, stroke_width=2.5, fill_color=col,
                                   fill_opacity=0.07).move_to([x, c[1] + 0.35, 0])
            top = label(when, font_size=32, color=col).move_to([x, c[1] + 1.5, 0])
            q1 = label(r"I fall asleep at about \ \rule{1.6cm}{0.4pt}", font_size=32).move_to([x, c[1] + 0.5, 0])
            q2 = label(r"I wake at about \ \rule{1.6cm}{0.4pt}", font_size=32).move_to([x, c[1] - 0.45, 0])
            q2.align_to(q1, LEFT)
            blocks.add(VGroup(box, top, q1, q2))
        ask = label(r"Settle on all four before going on.", font_size=32, color=P.ACCENT).move_to([c[0], c[1] - 2.2, 0])
        ring = countdown_ring(0.4).move_to(stage.box.get_corner(UR) + np.array([-0.65, -0.65, 0]))
        with self.voiceover(
            "Your turn, and you'll need four numbers. <bookmark mark='a'/> On days when you work or "
            "study: about what time do you fall asleep, and what time do you wake? <bookmark mark='b'/> "
            "And on free days, when no alarm rings: when do you fall asleep, and when do you wake by "
            "yourself? <bookmark mark='c'/> Take a few seconds, and settle on all four."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(blocks[0][0]), FadeIn(blocks[1][0]))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*blocks[0][1:])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*blocks[1][1:])))
            vo.wait_until("c")
            self.play(FadeIn(ask))
        self.add(ring)
        self.play(ring.t.animate.set_value(0.0), run_time=7.0, rate_func=linear)
        self.clear_scene()

    def read(self):
        d = load("chrono")
        ro = archive.ROENNEBERG_2004.data
        head = heading(r"The middle of your sleep")
        x0, x1 = -6.3, 1.9          # the axis runs from 20:00 to 12:00 the next day

        def X(h):                   # h in hours after midnight; evening hours are negative
            return x0 + (x1 - x0) * (h + 4) / 16

        axis = VGroup(Line([x0, -2.6, 0], [x1, -2.6, 0], color=GREY_C, stroke_width=2))
        for h in (-4, -2, 0, 2, 4, 6, 8, 10, 12):
            axis.add(Line([X(h), -2.6, 0], [X(h), -2.5, 0], color=GREY_C, stroke_width=2))
            axis.add(label(rf"{h % 24}:00", font_size=23, color=GREY_A).move_to([X(h), -2.9, 0]))
        names = {"early": r"an early sleeper", "middle": r"a middle sleeper", "late": r"a late sleeper"}
        order = [1, 0, 2]            # the worked example first, then the early and the late one
        ys = {1: 1.4, 0: -0.05, 2: -1.5}
        groups = {}
        for k in order:
            y = ys[k]
            g = VGroup()
            for off, mid, dur, col in ((0.3, d["mid_work"][k], d["sleep_work"][k], GREY_B),
                                       (-0.3, d["mid_free"][k], d["sleep_free"][k], SLEEPC)):
                a, b = mid - dur / 2, mid + dur / 2
                bar = Rectangle(width=X(b) - X(a), height=0.44, stroke_width=0, fill_color=col, fill_opacity=0.85)
                bar.move_to([(X(a) + X(b)) / 2, y + off, 0])
                dot = Dot([X(mid), y + off, 0], radius=0.1, color=WHITE)
                g.add(VGroup(bar, dot))
            nm = label(names[d["names"][k]], font_size=29, color=WHITE).move_to([0, y + 0.82, 0]).align_to(
                np.array([x0, 0, 0]), LEFT)
            gap = VGroup(Line([X(d["mid_work"][k]), y + 0.3, 0], [X(d["mid_work"][k]), y - 0.3, 0], color=THRESH, stroke_width=2),
                         Line([X(d["mid_work"][k]), y - 0.3, 0], [X(d["mid_free"][k]), y - 0.3, 0], color=THRESH, stroke_width=6))
            jl = label(_hm(d["jetlag"][k]), font_size=36, color=THRESH).move_to([3.0, y, 0])
            groups[k] = VGroup(nm, g, gap, jl)
        lg = VGroup(label(r"grey: \ asleep on work days", font_size=26, color=GREY_B),
                    label(r"purple: \ on free days", font_size=26, color=SLEEPC),
                    label(r"white dots: \ the midpoints", font_size=26, color=WHITE)).arrange(RIGHT, buff=0.45)
        lg.move_to([(x0 + x1) / 2 + 0.3, 2.82, 0])
        keep_in_frame(lg, 0.4)
        jhead = label(r"social jetlag", font_size=28, color=THRESH).move_to([3.0, 2.25, 0])
        notes = rows_of([
            (r"chronotype: \ the midpoint on free days", SLEEPC),
            (r"social jetlag: \ how far the timetable sits from the clock", THRESH),
            (rf"chronotype moves with age: \ latest at about {ro['latest_women']:.0f} to {ro['latest_men']:.0f}", DATA),
        ], 2.7, 28, 0.4).move_to([5.55, 0.1, 0])
        keep_in_frame(notes)
        src = published_tag(archive.ROENNEBERG_2004.cite)
        tag = psyche_tag(r"computed: three example sleepers")
        with self.voiceover(
            "Here's how to read your numbers. <bookmark mark='a'/> Take the middle of your sleep on free "
            "days. This sleeper is asleep at half past midnight and awake at nine, so the midpoint is a "
            "quarter to five. That midpoint is called your chronotype, and it's a fair guide to where "
            "your clock sits. <bookmark mark='b'/> Now the same for work days: half past eleven to seven, "
            "with its midpoint at a quarter past three. The distance between the two midpoints, an hour "
            "and a half here, has a name: social jetlag. It's how far your timetable sits from your "
            "clock. <bookmark mark='c'/> An early sleeper hardly moves between work days and free days: "
            "forty-five minutes. <bookmark mark='d'/> A late sleeper's free-day midpoint is past seven in "
            "the morning, and work drags it back by more than three hours. Every Monday that person "
            "flies three time zones east, and every Friday night flies back. And look at the lengths of "
            "the bars: six hours on work nights, eight and a half when free. The pressure of chapter "
            "four is being paid off at the weekend. <bookmark mark='e'/> So where's yours? Chronotypes "
            "differ between people by hours. They're partly inherited. And they move with age: later "
            f"and later through the teens, latest at about {ro['latest_women']:.0f} to "
            f"{ro['latest_men']:.0f}, and then slowly earlier for the rest of life. That last fact comes "
            "back in chapter thirteen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(axis), FadeIn(lg), FadeIn(groups[1][0]),
                      FadeIn(groups[1][1][0][0]), FadeIn(groups[1][1][1][0]))
            vo.wait_until("a")
            self.play(FadeIn(groups[1][1][1][1], scale=2.0), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(groups[1][1][0][1], scale=2.0), Create(groups[1][2]), FadeIn(groups[1][3]), FadeIn(jhead),
                      FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(groups[0], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(groups[2], shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(notes[2]))
        self.clear_scene()
