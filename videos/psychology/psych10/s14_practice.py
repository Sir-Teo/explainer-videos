from __future__ import annotations

import numpy as np

from videos.psychology.psych10.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.schools()
        self.insomnia()
        self.work()

    def card(self):
        card = chapter_card(13, r"In practice: \ schedules, schools and insomnia", r"Where is this part put to work?",
                            lit=(), part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover(
            "Chapter thirteen. In practice: schedules, schools and insomnia."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def schools(self):
        s = archive.DUNSTER_2018.data
        ro = archive.ROENNEBERG_2004.data
        head = heading(r"Schools: \ the late clock and the early bell")
        x0, x1 = -6.4, -0.4

        def X(h):
            return x0 + (x1 - x0) * (h - 6) / 4

        axis = VGroup(Line([x0, -0.9, 0], [x1, -0.9, 0], color=GREY_C, stroke_width=2))
        for h in (6, 7, 8, 9, 10):
            axis.add(Line([X(h), -0.9, 0], [X(h), -0.8, 0], color=GREY_C, stroke_width=2))
            axis.add(label(rf"{h}:00", font_size=23, color=GREY_A).move_to([X(h), -1.2, 0]))
        t0, t1 = 7 + 50 / 60, 8 + 45 / 60
        before = VGroup(Line([X(t0), -0.9, 0], [X(t0), 1.3, 0], color=GREY_B, stroke_width=4),
                        label(rf"before: \ {s['from']}", font_size=28, color=GREY_B).next_to([X(t0), 1.3, 0], UP, buff=0.1))
        after = VGroup(Line([X(t1), -0.9, 0], [X(t1), 0.6, 0], color=MODEL, stroke_width=4),
                       label(rf"after: \ {s['to']}", font_size=28, color=MODEL).next_to([X(t1), 0.6, 0], UP, buff=0.1))
        move = Arrow([X(t0), 0.1, 0], [X(t1), 0.1, 0], buff=0.05, color=THRESH, stroke_width=5,
                     max_tip_length_to_length_ratio=0.2)
        ml = label(rf"{s['shift_min']} min", font_size=27, color=THRESH).next_to(move, DOWN, buff=0.08)
        nums = VGroup(big_number(rf"$+{s['more_sleep_min']}$ min", r"more sleep a night, measured at the wrist", SLEEPC, 54, 3.0),
                      big_number(rf"$+{s['grades_pct']}$\%", r"grades", MODEL, 54, 3.0)).arrange(RIGHT, buff=0.5, aligned_edge=UP)
        nums.move_to([-3.4, -2.45, 0])
        rows = rows_of([
            (rf"through the teens the clock moves later: \ latest at about {ro['latest_women']:.0f} to "
             rf"{ro['latest_men']:.0f}", SLEEPC),
            (r"a school day that starts before eight cuts the end off a teenager's night", WHITE),
            (rf"Seattle moved its high schools' start {s['shift_min']} minutes later; \ wrist monitors, \ the spring before "
             r"and the spring after", WHITE),
            (r"they did not just go to bed later: \ most of the time was kept as sleep", MODEL),
            (r"two schools, \ different students each year, \ before and after: \ not an experiment", BAD),
        ], 6.0, 28, 0.26).move_to([3.65, -0.2, 0])
        keep_in_frame(rows)
        src = published_tag(archive.DUNSTER_2018.cite + r"; \ " + archive.ROENNEBERG_2004.cite)
        with self.voiceover(
            "Three places where this part is put to work. First, schools. <bookmark mark='a'/> Chapter "
            "five ended on a fact: through the teens the clock moves later, and it's latest at about "
            "twenty. A sixteen-year-old who can't fall asleep before midnight isn't being difficult. So "
            "a school day that starts before eight cuts the end off their night, every night. "
            f"<bookmark mark='b'/> Seattle moved the start of its high schools {s['shift_min']} minutes "
            "later, from ten to eight to a quarter to nine. Researchers put activity monitors on the "
            "wrists of students at two schools, in the spring before and the spring after. "
            f"<bookmark mark='c'/> Sleep went up by {s['more_sleep_min']} minutes a night. The students "
            "didn't just go to bed later. They kept most of the extra time as sleep. And grades were "
            f"{s['grades_pct']} percent higher. <bookmark mark='d'/> Now read it the way Part 2 taught "
            "you. It compares two different years of students, before and after, in two schools. It "
            "isn't an experiment, and the authors don't claim that the sleep caused the grades. But the "
            "direction is what the two processes predict, and school districts have been acting on it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(axis), FadeIn(before))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            self.wait(7.0)
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(GrowArrow(move), FadeIn(ml), FadeIn(after), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(nums[0], scale=1.1), FadeIn(rows[3]))
            self.wait(5.0)
            self.play(FadeIn(nums[1], scale=1.1))
            vo.wait_until("d")
            self.play(FadeIn(rows[4], shift=UP * 0.1))
        self.clear_scene()

    def insomnia(self):
        tr = archive.TRAUER_2015.data
        head = heading(r"Insomnia: \ a treatment built from this lecture")
        parts = [
            (r"spend less time in bed", SLEEPC, r"builds the pressure: \ process~S"),
            (r"rise at the same time; \ light in the morning", CLOCKC, r"anchors the clock: \ process~C"),
            (r"use the bed only for sleep", THRESH, r"undoes a learned link between bed and lying awake: \ Part 16"),
        ]
        cards = VGroup()
        for i, (what, col, why_) in enumerate(parts):
            x = -4.55 + 4.55 * i
            box = RoundedRectangle(width=4.2, height=2.5, corner_radius=0.15, color=col, stroke_width=2.5, fill_color=col,
                                   fill_opacity=0.07).move_to([x, 1.35, 0])
            a = wrapped_label(what, 3.7, 31, col).move_to([x, 2.0, 0])
            b = wrapped_label(why_, 3.7, 28, WHITE).move_to([x, 0.8, 0])
            cards.add(VGroup(box, a, b))
        nums = VGroup(big_number(rf"${tr['onset_min']}$ min", r"sooner asleep", MODEL, 56, 3.2),
                      big_number(rf"${tr['awake_min']}$ min", r"less time awake in the night", MODEL, 56, 3.4),
                      big_number(rf"$+{tr['efficiency_points']}$", r"points of sleep efficiency: \ the share of time in bed "
                                                                 r"spent asleep", MODEL, 56, 3.8)).arrange(RIGHT, buff=0.7,
                                                                                                           aligned_edge=UP)
        nums.move_to([0, -1.55, 0])
        cap = label(rf"{tr['trials']} randomized trials, \ {num(tr['people'])} people", font_size=28, color=GREY_A)
        cap.next_to(nums, DOWN, buff=0.25)
        src = published_tag(archive.TRAUER_2015.cite)
        with self.voiceover(
            "Second, insomnia: the commonest sleep complaint there is. The treatment that guidelines put "
            "first isn't a pill. It's a short course of behavioural therapy, and each of its parts is "
            "something from this lecture. <bookmark mark='a'/> Spend less time in bed. It sounds cruel, "
            "and it works by building up the pressure: process S. <bookmark mark='b'/> Get up at the "
            "same time every day, and get light in the morning. That anchors the clock: process C. "
            "<bookmark mark='c'/> And use the bed only for sleep. Someone who has lain awake there for "
            "months has learned to be awake there. That's conditioning, and it's Part 16. "
            f"<bookmark mark='d'/> {tr['trials']} randomized trials, pooled in 2015: people fell asleep "
            f"{tr['onset_min']} minutes sooner, and spent {tr['awake_min']} minutes less awake during "
            "the night. Those are modest numbers, honestly reported, and Part 42 will ask what a number "
            "like that means for a patient."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), *[FadeIn(c[0]) for c in cards])
            for mark_, c in zip("abc", cards):
                vo.wait_until(mark_)
                self.play(FadeIn(c[1]), FadeIn(c[2]))
            vo.wait_until("d")
            self.play(FadeIn(cap), LaggedStart(*[FadeIn(n_, scale=1.1) for n_ in nums], lag_ratio=0.6), run_time=5.0)
        self.clear_scene()

    def work(self):
        d = load("dose")
        left = round(100 * 0.5 ** (6 / d["half_life"]))
        head = heading(r"At work, \ and at home")
        jobs = [
            (r"fatigue risk", OPP, r"airlines, railways, hospitals and armies roster their crews with descendants of the "
                                   r"two-process model: \ recent sleep and time of day in, \ predicted alertness out"),
            (r"sleep clinics", SLEEPC, r"psychologists deliver the insomnia treatment; \ technologists score each night "
                                       r"into its stages"),
            (r"drug development", DRUG, r"every trial of a psychiatric drug begins with chapter ten: \ a dose-response "
                                        r"curve and a half-life"),
        ]
        rows = VGroup()
        for name, col, what in jobs:
            rows.add(VGroup(label(name, font_size=32, color=col), wrapped_label(what, 12.2, 28, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, 0.95, 0])
        you = rows_of([
            (r"for yourself: \ rise at the same time, and get light early: \ the clock", CLOCKC),
            (r"do not carry a debt you cannot feel: \ the pressure", SLEEPC),
            (rf"do the caffeine arithmetic: \ a coffee at 17:00 is still {left}\% there at 23:00", DRUG),
        ], 12.2, 30, 0.24).move_to([0, -2.0, 0]).align_to(rows, LEFT)
        tag = psyche_tag(rf"computed: a half-life of {d['half_life']:.0f} hours")
        with self.voiceover(
            "And third, work. <bookmark mark='a'/> Anyone whose job runs through the night is fighting "
            "both processes at once, and the people who schedule them now use models. Airlines, "
            "railways, hospitals and armies roster their crews with descendants of the two-process "
            "model. They take in a person's recent sleep and the time of day, and put out a predicted "
            "level of alertness. <bookmark mark='b'/> Sleep clinics employ psychologists to deliver the "
            "insomnia treatment, and technologists who score each night into its stages. "
            "<bookmark mark='c'/> And drug development runs on chapter ten. Every trial of every "
            "psychiatric drug begins with a dose-response curve and a half-life. <bookmark mark='d'/> "
            "For yourself, the part compresses into three lines. Get up at the same time, and get light "
            "early: that's the clock. Don't carry a debt you can't feel: that's the pressure. And do "
            f"the caffeine arithmetic. With a five-hour half-life, a coffee at five in the afternoon is "
            f"still {left} percent there at eleven."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(r[0]) for r in rows])
            for mark_, r in zip("abc", rows):
                vo.wait_until(mark_)
                self.play(FadeIn(r[1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(y, shift=UP * 0.1) for y in you], lag_ratio=0.8), run_time=9.0)
        self.clear_scene()
