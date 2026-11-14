from __future__ import annotations

import numpy as np

from videos.psychology.psych10.common import *  # noqa: F403


class Loss(VoiceoverScene):
    def construct(self):
        self.card()
        self.design()
        self.lapses()
        self.unnoticed()

    def card(self):
        card = chapter_card(6, r"What sleep loss does", r"And would you know?", lit=(), part=PART,
                            scale=("mind", "person"), marr=("what",))
        with self.voiceover(
            "Chapter six. What sleep loss does."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def design(self):
        v = archive.VAN_DONGEN_2003.data
        head = heading(r"Do not ask. \ Assign")
        groups = VGroup()
        cols = {8: MODEL, 6: THRESH, 4: BAD}
        for i, h in enumerate(v["hours_in_bed"]):
            y = 1.55 - 1.3 * i
            nights = VGroup(*[VGroup(Rectangle(width=0.32, height=0.96, stroke_color=GREY_D, stroke_width=1.5),
                                     Rectangle(width=0.32, height=0.96 * h / 8, stroke_width=0, fill_color=cols[h],
                                               fill_opacity=0.85))
                              for _ in range(v["days"])])
            for cell in nights:
                cell[1].align_to(cell[0], DOWN)
            nights.arrange(RIGHT, buff=0.08).move_to([-2.3, y, 0])
            lab = label(rf"{h} hours in bed", font_size=31, color=cols[h]).next_to(nights, LEFT, buff=0.3)
            groups.add(VGroup(lab, nights))
        keep_in_frame(groups)
        gcap = label(rf"{v['days']} nights, \ by lot", font_size=26, color=GREY_A).next_to(groups, DOWN, buff=0.2)
        scr = RoundedRectangle(width=3.0, height=1.9, corner_radius=0.12, color=GREY_B, stroke_width=3, fill_color="#05070B",
                               fill_opacity=1).move_to([4.5, 1.1, 0])
        lamp = Dot(scr.get_center(), radius=0.2, color=BAD)
        rows = rows_of([
            (r"watch the screen; \ when the light comes on, press: \ ten minutes of it", WHITE),
            (r"a rested person almost never misses", GREY_A),
            (r"the measure: \ lapses, \ responses so slow that attention had gone", THRESH),
        ], 4.7, 29, 0.25).next_to(scr, DOWN, buff=0.4)
        keep_in_frame(rows)
        src = published_tag(archive.VAN_DONGEN_2003.cite)
        with self.voiceover(
            "Part 2's rule was: don't ask, assign. In 2003 Hans Van Dongen and David Dinges, in "
            "Philadelphia, did that with sleep. <bookmark mark='a'/> Healthy adults moved into the "
            f"laboratory for two weeks. By lot, each was given eight hours in bed a night, or six, or "
            "four. <bookmark mark='b'/> Several times a day they did the simplest attention task there "
            "is. Watch a screen. When a light comes on, at a moment you can't predict, press a button. "
            "Keep that up for ten minutes. <bookmark mark='c'/> A rested person almost never misses. The "
            "measure is the number of lapses: responses so slow that, for a moment, the person had "
            "stopped attending."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), *[FadeIn(g[0]) for g in groups])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g[1], lag_ratio=0.05) for g in groups], lag_ratio=0.4), FadeIn(gcap), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(scr), FadeIn(rows[0]))
            self.play(FadeIn(lamp, scale=0.5), run_time=0.3)
            self.play(FadeOut(lamp), run_time=0.3)
            self.wait(1.6)
            self.play(FadeIn(lamp, scale=0.5), run_time=0.3)
            self.play(FadeOut(lamp), run_time=0.3)
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
        self.clear_scene()

    def lapses(self):
        d = load("debt")
        v = archive.VAN_DONGEN_2003.data
        e4, e6, ratio = d["excess_4"], d["excess_6"], d["ratio"]
        need = 24 - d["threshold"]
        head = heading(r"Two weeks, \ day by day")
        A = axes([0, 14], [0, 11], x_length=6.6, y_length=4.4, xticks=[0, 2, 4, 6, 8, 10, 12, 14], yticks=[],
                 xlabel=r"days of the schedule", ylabel=r"lapses in a test", center=[-3.35, -0.4, 0])
        ax = A.ax
        cols = {8: MODEL, 6: THRESH, 4: BAD}
        lines = {}
        for h in v["hours_in_bed"]:
            ln = curve(ax, np.r_[0, d["days"]], np.r_[1.0, d[f"lapses_{h}"]], cols[h], stroke_width=4.5)
            lab = label(rf"{h} h", font_size=28, color=cols[h]).next_to(ax.c2p(14, float(d[f"lapses_{h}"][-1])), RIGHT, buff=0.1)
            lines[h] = VGroup(ln, lab)
        rows = rows_of([
            (r"eight hours: \ nothing much", MODEL),
            (r"six hours: \ worse each day, in nearly a straight line; \ four hours: \ about twice as fast", THRESH),
            (rf"published: \ after two weeks on six hours, \ as impaired as after up to {v['equivalent_nights']} nights "
             r"with no sleep", DATA),
            (rf"the rule that fitted: \ every hour awake past ${d['threshold']:.2f}$ in a day adds to the deficit", WHITE),
            (rf"$24 - {d['threshold']:.2f} = {need:.2f}$ hours of sleep to stay level", WHITE),
        ], 5.2, 28, 0.24).move_to([4.2, -0.3, 0])
        keep_in_frame(rows)
        src = published_tag(archive.VAN_DONGEN_2003.cite)
        tag = psyche_tag(r"drawn from the published rule; \ the vertical scale is arbitrary")
        with self.voiceover(
            "<bookmark mark='a'/> With eight hours in bed, nothing much happened. <bookmark mark='b'/> "
            "With six hours, lapses grew, day after day, in nearly a straight line, with no sign of "
            "levelling off. With four hours they grew about twice as fast. <bookmark mark='c'/> After two "
            "weeks on six hours a night, people were as impaired as people in a fourth group, who'd been "
            f"kept awake for up to {v['equivalent_nights']} nights running. And six hours isn't an "
            "extreme. Plenty of people call it a normal week. <bookmark mark='d'/> The rule that fitted "
            "the data is simple. Every hour of wakefulness beyond about sixteen in a day, "
            f"{d['threshold']:.2f} by their estimate, adds to the deficit, and the deficits add up. The "
            "picture here is that rule, drawn. Its vertical scale is arbitrary, but the ratio isn't. "
            f"Four hours in bed is {e4:.1f} hours over the line each day. Six hours is {e6:.1f}. So the "
            f"four-hour line climbs {ratio:.1f} times as fast. <bookmark mark='e'/> And twenty-four "
            f"minus {d['threshold']:.2f} leaves a little over eight hours: the sleep it takes to stay "
            "level."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(lines[8][0]), FadeIn(lines[8][1]), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines[6][0]), FadeIn(lines[6][1]), run_time=2.5)
            self.play(Create(lines[4][0]), FadeIn(lines[4][1]), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4], shift=UP * 0.1))
        self.clear_scene()

    def unnoticed(self):
        head = heading(r"And they did not know")
        A = axes([0, 14], [0, 1.1], x_length=6.6, y_length=4.2, xticks=[0, 2, 4, 6, 8, 10, 12, 14], yticks=[],
                 xlabel=r"days on six hours a night", ylabel=r"", center=[-3.35, -0.4, 0])
        ax = A.ax
        t = np.linspace(0, 14, 120)
        perf = curve(ax, t, 0.07 + 0.93 * t / 14, THRESH, stroke_width=4.5)
        felt = curve(ax, t, 0.07 + 0.36 * (1 - np.exp(-t / 2.2)), GREY_A, stroke_width=4.5)
        pl = label(r"lapses", font_size=28, color=THRESH).next_to(ax.c2p(11.2, 0.82), UL, buff=0.1)
        fl = wrapped_label(r"how sleepy they said they felt", 3.4, 28, GREY_A).next_to(ax.c2p(9.2, 0.43), DOWN, buff=0.25)
        gap = DoubleArrow(ax.c2p(13.4, 0.46), ax.c2p(13.4, 0.94), color=BAD, stroke_width=4, buff=0.02,
                          max_tip_length_to_length_ratio=0.12)
        rows = rows_of([
            (r"for a few days the ratings rose with the lapses", WHITE),
            (r"then the ratings levelled off; \ the lapses kept climbing", BAD),
            (r"Part 1: \ introspection uses the instrument that sleep loss has degraded. \ A stopwatch does not", THRESH),
            (r"``I do fine on six hours'' is what this experiment says people will report", GREY_A),
        ], 5.2, 29, 0.28).move_to([4.2, -0.3, 0])
        keep_in_frame(rows)
        src = published_tag(archive.VAN_DONGEN_2003.cite)
        tag = note(r"a drawing of the published pattern, \ not the data").to_corner(DR, buff=0.3)
        with self.voiceover(
            "And here's the finding that matters most. Alongside the task, people rated how sleepy they "
            "felt. <bookmark mark='a'/> For the first few days the ratings rose with the lapses. "
            "<bookmark mark='b'/> Then the ratings levelled off, while the lapses kept climbing. By the "
            "end, the people on six hours were performing like someone who'd missed a night or two, and "
            "reporting that they felt only slightly sleepy. <bookmark mark='c'/> This is Part 1 again. "
            "Introspection uses the very instrument that sleep loss has degraded, so the report can't be "
            "trusted. A ten-minute task and a stopwatch can. <bookmark mark='d'/> So when someone tells "
            "you they do fine on six hours, they may be one of the few people who do. Or they may be "
            "telling you exactly what this experiment says they would."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(perf), Create(felt), FadeIn(pl), FadeIn(fl), FadeIn(rows[0]), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.play(GrowFromCenter(gap), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()
