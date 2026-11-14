from __future__ import annotations

import numpy as np

from videos.psychology.psych10.common import *  # noqa: F403


class Stress(VoiceoverScene):
    def construct(self):
        self.card()
        self.messengers()
        self.loop()
        self.stressor()
        self.two_jobs()

    def card(self):
        card = chapter_card(8, r"The stress loop", r"How does a signal in the blood switch itself off?", lit=(),
                            part=PART, scale=("molecule", "brain", "person"), marr=("how", "tissue"))
        with self.voiceover(
            "Chapter eight. The stress loop."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def messengers(self):
        head = heading(r"A private message, \ and a broadcast")
        cols = [(r"a synapse", VOLT, [r"across a gap of twenty millionths of a millimetre", r"to one neighbouring cell",
                                     r"in about a thousandth of a second"]),
                (r"a hormone", HORM, [r"into the blood, \ and so everywhere", r"to every cell that carries its receptor",
                                     r"in seconds; \ its effects last minutes to hours"])]
        heads = [r"travels", r"reaches", r"takes"]
        table = VGroup()
        for j, (name, col, cells) in enumerate(cols):
            x = -1.0 + 5.0 * j
            colg = VGroup(label(name, font_size=36, color=col).move_to([x, 2.0, 0]))
            for i, c in enumerate(cells):
                colg.add(wrapped_label(c, 4.3, 30, WHITE).move_to([x, 0.75 - 1.3 * i, 0]))
            table.add(colg)
        hs = VGroup(*[label(h, font_size=30, color=GREY_A).move_to([-5.3, 0.75 - 1.3 * i, 0]) for i, h in enumerate(heads)])
        icon = droplet(0.8, HORM).next_to(table[1][0], RIGHT, buff=0.3)
        end = wrapped_label(r"One you have met: \ melatonin, the signal for night. \ Now the best studied in psychology: "
                            r"\ cortisol.", 12.4, 30, THRESH).move_to([0, -2.95, 0])
        with self.voiceover(
            "The nervous system isn't the only way one part of the body tells another what to do. "
            "<bookmark mark='a'/> A synapse, as Part 6 showed, passes a chemical across a gap of twenty "
            "millionths of a millimetre, to one neighbouring cell, in about a thousandth of a second. "
            "It's a private message. <bookmark mark='b'/> A hormone is a chemical released into the "
            "blood. It goes everywhere, and every cell that carries the right receptor responds. It "
            "takes seconds to arrive, and its effects last from minutes to hours. It's a broadcast. "
            "<bookmark mark='c'/> You've met one already: melatonin, the signal for night. Now for the "
            "one that psychology has studied most: cortisol, the hormone of stress."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hs), FadeIn(table[0][0]), FadeIn(table[1][0]), FadeIn(icon))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in table[0][1:]], lag_ratio=0.7), run_time=6.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in table[1][1:]], lag_ratio=0.7), run_time=8.0)
            vo.wait_until("c")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def loop(self):
        d = load("stress")
        hp, mp = spoken_time(d["peak_hour"])
        assert hp == 7 and 25 <= mp <= 35, (hp, mp)
        head = heading(r"Three glands, \ and a brake")
        lp = loop_diagram([r"the hypothalamus releases a first hormone", r"the pituitary releases a second, into the blood",
                           r"the adrenal glands release cortisol"], [CLOCKC, VOLT, HORM], width=12.4, font_size=27,
                          feedback=r"cortisol turns both of them down").scale(1.04).move_to([0, 0.9, 0])
        t = d["t"]
        k = (t >= 48) & (t <= 96)
        A = axes([48, 96], [0, 0.6], x_length=6.6, y_length=2.1, xticks=[], yticks=[],
                 xlabel=r"two days; \ shaded: the night", ylabel=r"cortisol", center=[-3.4, -1.85, 0])
        ax = A.ax
        A.add(hour_labels(ax, [48, 60, 72, 84, 96], 0))
        nights = night_bands(ax, 48, 96, y0=0, y1=0.6)
        line = curve(ax, t[k], d["cortisol"][k], HORM, stroke_width=4.5)
        rows = rows_of([
            (r"cortisol frees energy, \ and holds back what can wait: \ digestion, growth, repair", HORM),
            (rf"left alone, the loop follows the clock: \ highest at about {clock_time(d['peak_hour'])}, \ lowest in the "
             rf"evening: \ a {d['swing']:.0f}-fold swing", WHITE),
        ], 5.6, 28, 0.28).move_to([3.9, -1.8, 0])
        keep_in_frame(rows)
        rows[0].move_to([0, -1.6, 0])
        tag = psyche_tag(r"computed: Psyche's stress loop (a model)")
        with self.voiceover(
            "The stress system is a chain of three glands. <bookmark mark='a'/> A threat, or just the "
            "clock in the morning, makes the hypothalamus release a first hormone. That makes the "
            "pituitary, the gland just beneath it, release a second into the blood. And that makes the "
            "adrenal glands, which sit on top of the kidneys, release cortisol. <bookmark mark='b'/> "
            "Cortisol frees up energy, and holds back the things that can wait: digestion, growth, "
            "repair. It's a budget for an emergency. <bookmark mark='c'/> And then the important part. "
            "Cortisol acts back on the hypothalamus and the pituitary, and turns them down. The end of "
            "the chain is a brake on its start. <bookmark mark='d'/> Left alone, the loop follows the "
            "clock. In the model, cortisol peaks at about half past seven, around waking, and it's lowest "
            f"in the evening: a {d['swing']:.0f}-fold swing, every day. You wake up on a tide of it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(lp.boxes[0]))
            vo.wait_until("a")
            self.play(LaggedStart(FadeIn(lp.arrows[0]), FadeIn(lp.boxes[1]), FadeIn(lp.arrows[1]), FadeIn(lp.boxes[2]),
                                  lag_ratio=0.9), run_time=9.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(lp.back[0]), FadeIn(lp.back[1]), FadeIn(lp.back[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(lp.animate.scale(0.8).move_to([0, 1.8, 0]), FadeOut(rows[0]))
            self.play(FadeIn(A), FadeIn(nights), Create(line), FadeIn(rows[1]), run_time=3.0)
        self.clear_scene()

    def stressor(self):
        d = load("stress")
        t = d["t"]
        k = (t >= 57) & (t <= 66)
        hours = t[k] - 58.0
        extra, extra_w = (d["hit"] - d["cortisol"])[k], (d["worn"] - d["worn_base"])[k]
        more = 100 * (d["worn_mean_ratio"] - 1)
        head = heading(r"On, \ and then off")
        A = axes([-1, 8], [0, 0.2], x_length=6.8, y_length=4.3, xticks=[0, 2, 4, 6, 8], yticks=[],
                 xlabel=r"hours after the stressor begins", ylabel=r"", center=[-3.3, -0.45, 0])
        ax = A.ax
        A.add(label(r"cortisol above its daily curve", font_size=24, color=GREY_A).move_to(ax.c2p(5.4, 0.192)))
        band = Rectangle(width=abs(ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]), height=abs(ax.c2p(0, 0.2)[1] - ax.c2p(0, 0)[1]),
                         stroke_width=0, fill_color=BAD, fill_opacity=0.15).move_to((ax.c2p(0, 0) + ax.c2p(1, 0.2)) / 2)
        bl = label(r"the stressor", font_size=24, color=BAD).next_to(band, UP, buff=0.05)
        good = curve(ax, hours, extra, HORM, stroke_width=4.5)
        bad = curve(ax, hours, extra_w, OPP, stroke_width=4.5)
        gl = label(r"the brake at full strength", font_size=26, color=HORM).move_to(ax.c2p(5.9, 0.055))
        wl = label(r"the brake worn down", font_size=26, color=OPP).move_to(ax.c2p(4.4, 0.15))
        rows = rows_of([
            (r"ten in the morning: \ one hour of something alarming", WHITE),
            (rf"cortisol rises, \ the brake takes hold, \ and within ${d['gone_hours']:.1f}$ hours of the end it is back", HORM),
            (rf"wear the brake down to 30\%: \ a bigger rise, \ a slower return, \ and a daily level {more:.0f}\% higher with "
             r"no stressor at all", OPP),
            (r"the danger is not the response: \ it is a response that cannot switch off", BAD),
            (r"a signal that shuts off its own source, after a delay: \ the clock gene's loop, in another tissue", THRESH),
        ], 5.0, 28, 0.24).move_to([4.3, -0.3, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: Psyche's stress loop (a model)")
        with self.voiceover(
            "Now stress it. At ten in the morning: one hour of something alarming. <bookmark mark='a'/> "
            "Cortisol rises above its daily curve, it peaks, and then the brake takes hold. Within "
            f"{d['gone_hours']:.1f} hours of the end, it's back where it would have been. That's what a "
            "stress response is for: on, and then off. <bookmark mark='b'/> Now wear the brake down, to "
            "thirty percent of its strength. The same stressor produces a bigger rise and a slower "
            f"return. And across the whole day, the cortisol level is {more:.0f} percent higher, with no "
            "stressor at all. <bookmark mark='c'/> That's the worry about stress that never stops. The "
            "danger isn't the response. It's a response that can't switch off, because then the things "
            "cortisol holds back are held back all the time. A weakened brake in this loop is one of the "
            "oldest biological findings in severe depression, and it's waiting in Part 40. "
            "<bookmark mark='d'/> And notice the design. A signal that shuts off its own source, after a "
            "delay. It's the clock gene's loop from chapter one, in a different tissue, at a different "
            "speed. Biology uses it everywhere, and now you can recognise it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(band), FadeIn(bl), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(good), FadeIn(gl), FadeIn(rows[1]), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(bad), FadeIn(wl), FadeIn(rows[2]), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4], shift=UP * 0.1))
        self.clear_scene()

    def two_jobs(self):
        head = heading(r"Two things to carry forward")
        lt = label(r"1. \ Hormones do two jobs", font_size=33, color=HORM)
        life = Line([-6.4, 1.3, 0], [-0.6, 1.3, 0], color=GREY_B, stroke_width=3)
        win = Rectangle(width=1.5, height=0.5, stroke_width=0, fill_color=HORM, fill_opacity=0.5).move_to([-5.65, 1.3, 0])
        act = VGroup(*[Rectangle(width=0.35, height=0.5, stroke_width=0, fill_color=CLOCKC, fill_opacity=0.5).move_to(
            [x, 1.3, 0]) for x in (-2.9, -2.1, -1.3)])
        wl = wrapped_label(r"early in life: \ organize, \ for good", 2.4, 26, HORM).next_to(win, DOWN, buff=0.15)
        al = wrapped_label(r"later: \ activate, \ and wear off", 2.6, 26, CLOCKC).next_to(act, DOWN, buff=0.15)
        ph = wrapped_label(r"1959, guinea pigs: \ testosterone before birth changed how daughters behaved as adults, "
                           r"permanently; \ given to adults, it did not. \ In people the evidence is indirect", 5.9, 29,
                           WHITE)
        ph.move_to([-3.5, -1.55, 0])
        lt.move_to([-3.5, 2.4, 0]).align_to(ph, LEFT)
        rt = label(r"2. \ A famous curve, \ and its thin beginning", font_size=33, color=THRESH)
        A = axes([0, 1], [0, 1.1], x_length=3.6, y_length=1.7, xticks=[], yticks=[], xlabel=r"arousal", ylabel=r"performance",
                 center=[3.6, 0.85, 0])
        x = np.linspace(0.03, 0.97, 60)
        hump = DashedVMobject(curve(A.ax, x, 4 * x * (1 - x), THRESH, stroke_width=4), num_dashes=30)
        q = label(r"?", font_size=60, color=BAD).move_to(A.ax.c2p(0.5, 0.45))
        yd = wrapped_label(r"1908: \ mice, in small groups, choosing between two boxes under electric shocks. \ The word "
                           r"arousal is not in the paper; \ the smooth curve was drawn later. \ Part 28 looks for better "
                           r"evidence", 5.9, 28, WHITE)
        yd.move_to([3.7, -1.75, 0])
        rt.move_to([3.7, 2.4, 0]).align_to(yd, LEFT)
        keep_in_frame(VGroup(rt, yd))
        src = published_tag(archive.PHOENIX_1959.cite + r"; \ " + archive.TEIGEN_1994.cite)
        tag = note(r"the curve: a drawing of the textbook figure").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Two more things about hormones, briefly, because both will come back. <bookmark mark='a'/> "
            "First: hormones do two different jobs, at two times of life. In 1959 a team in Kansas gave "
            "testosterone to pregnant guinea pigs. Their daughters, as adults, behaved differently in "
            "mating, and permanently. Given to adult females, the same hormone didn't do that. "
            "<bookmark mark='b'/> So early in life, during a window, a hormone can organize the nervous "
            "system for good. Later it can only activate what's there, and the effect wears off with the "
            "hormone. In people the evidence for organizing effects is indirect, and Parts 30 and 31 "
            "will handle it with care. <bookmark mark='c'/> Second: a warning about a famous curve. "
            "Every textbook has it. Performance is best at moderate arousal, and falls away on both "
            "sides. It's called the Yerkes-Dodson law. <bookmark mark='d'/> The experiment was done in "
            "1908, on mice, in small groups, learning to pick the right one of two boxes under electric "
            "shocks of different strengths. The word arousal isn't in the paper. The smooth curve was "
            "drawn by later writers. The idea may well be right. But its evidence isn't that experiment, "
            "and Part 28 will go looking for better."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(lt), FadeIn(life))
            vo.wait_until("a")
            self.play(FadeIn(ph))
            vo.wait_until("b")
            self.play(FadeIn(win), FadeIn(wl), FadeIn(act, lag_ratio=0.3), FadeIn(al))
            vo.wait_until("c")
            self.play(FadeIn(rt), FadeIn(A), Create(hump), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(q, scale=1.5), FadeIn(yd))
        self.clear_scene()
