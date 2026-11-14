from __future__ import annotations

import numpy as np

from videos.psychology.psych10.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.cave()
        self.result()
        self.question()
        self.objectives()

    def cave(self):
        k = archive.KLEITMAN_1938.data
        head = heading(rf"Mammoth Cave, Kentucky, {k['year']}")
        cx = -3.7
        ground = Line([cx - 3.1, 2.0, 0], [cx + 3.1, 2.0, 0], color=GREY_B, stroke_width=4)
        sun = Circle(radius=0.3, stroke_width=0, fill_color=LIGHTC, fill_opacity=1).move_to([cx - 2.2, 2.65, 0])
        rays = VGroup(*[Line(sun.get_center() + 0.4 * np.array([np.cos(a), np.sin(a), 0]),
                             sun.get_center() + 0.55 * np.array([np.cos(a), np.sin(a), 0]), color=LIGHTC, stroke_width=3)
                        for a in np.linspace(0, TAU, 10, endpoint=False)])
        cavern = Ellipse(width=6.0, height=3.1, color=GREY_C, stroke_width=3, fill_color="#0B0E14", fill_opacity=1)
        cavern.move_to([cx, -0.1, 0])
        shaft = Rectangle(width=0.5, height=0.9, stroke_width=0, fill_color="#0B0E14", fill_opacity=1)
        shaft.move_to([cx + 1.6, 1.6, 0])
        walls = VGroup(Line([cx + 1.35, 2.0, 0], [cx + 1.35, 1.2, 0], color=GREY_C, stroke_width=3),
                       Line([cx + 1.85, 2.0, 0], [cx + 1.85, 1.1, 0], color=GREY_C, stroke_width=3))
        kl = VGroup(little_person(1.45, CLOCKC), label(rf"Kleitman, {k['kleitman_age']}", font_size=30, color=CLOCKC))
        kl.arrange(DOWN, buff=0.12).move_to([cx - 1.3, -0.15, 0])
        ri = VGroup(little_person(1.45, SLEEPC), label(rf"Richardson, {k['student_age']}", font_size=30, color=SLEEPC))
        ri.arrange(DOWN, buff=0.12).move_to([cx + 1.3, -0.15, 0])
        cave = VGroup(cavern, shaft, walls, ground, sun, rays)
        unit = 6.2 / 168
        bars = VGroup()
        for row, (n, hours, col, name) in enumerate(((7, 24, GREY_B, r"7 days of 24 hours"),
                                                    (6, k["day_hours"], THRESH, rf"6 days of {k['day_hours']} hours"))):
            y = -2.3 - 0.6 * row
            cells = VGroup(*[Rectangle(width=hours * unit - 0.04, height=0.3, stroke_width=0, fill_color=col,
                                       fill_opacity=0.8).move_to([cx - 3.1 + (i + 0.5) * hours * unit, y, 0])
                             for i in range(n)])
            bars.add(VGroup(cells, label(name, font_size=25, color=col).next_to(cells, RIGHT, buff=0.25)))
        rows = rows_of([
            (r"no daylight reaches; \ the temperature never changes", WHITE),
            (rf"two men stay for {k['days']} days", WHITE),
            (r"the question: \ is the body's daily rhythm a habit copied from the sun, \ or does the body keep time "
             r"by itself?", THRESH),
            (rf"the test: \ live by a day of {k['day_hours']} hours, \ and take your temperature around the clock", WHITE),
        ], 6.1, 32, 0.4).move_to([3.75, 0.35, 0])
        keep_in_frame(rows)
        src = historical_tag(archive.KLEITMAN_1938.cite)
        with self.voiceover(
            f"In the early summer of {k['year']}, two men walked into Mammoth Cave in Kentucky, and stayed "
            f"for {k['days']} days. Nathaniel Kleitman was a physiologist at the University of Chicago, "
            f"{k['kleitman_age']} years old, and one of very few scientists anywhere who studied sleep. With "
            f"him was his student Bruce Richardson, who was {k['student_age']}. <bookmark mark='a'/> Deep in "
            "the cave no daylight reaches, and the temperature never changes. <bookmark mark='b'/> The "
            "question they took down with them was simple. Everyone's body runs on a daily rhythm. Body "
            "temperature, for one, is lowest before dawn and highest in the evening. Is that rhythm a "
            "habit, copied from the sun and the clocks? Or does the body keep time by itself? "
            f"<bookmark mark='c'/> So they changed the length of the day. They lived by a day of "
            f"{k['day_hours']} hours: <bookmark mark='d'/> six of their days to seven of everyone else's. "
            "They ate, worked and slept by that schedule, and took their temperatures around the clock. If "
            "the rhythm is a habit, a month should be enough to retrain it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(cave), FadeIn(kl), FadeIn(ri))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2], shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.15), FadeIn(bars[0]))
            vo.wait_until("d")
            self.play(FadeIn(bars[1], lag_ratio=0.1))
        self.clear_scene()

    def result(self):
        k = archive.KLEITMAN_1938.data
        head = heading(r"What the thermometers showed")
        t = np.linspace(0, 168, 600)
        panels, dots = VGroup(), VGroup()
        specs = [(rf"Richardson, {k['student_age']}", SLEEPC, 28.0, 1.25), (rf"Kleitman, {k['kleitman_age']}", CLOCKC, 24.0, -1.45)]
        for name, col, period, y in specs:
            A = axes([0, 168], [-1.4, 1.4], x_length=7.8, y_length=1.9, xticks=[], yticks=[], xlabel=r"", ylabel=r"",
                     center=[-2.75, y, 0])
            ax = A.ax
            grid = VGroup(*[DashedLine(ax.c2p(d * 28, -1.4), ax.c2p(d * 28, 1.4), color=THRESH, stroke_width=2,
                                       stroke_opacity=0.7) for d in range(7)])
            wave = curve(ax, t, -np.cos(TAU * (t - 20.0) / period), col, stroke_width=4)
            mins = VGroup(*[Dot(ax.c2p(20.0 + j * period, -1.0), radius=0.09, color=WHITE)
                            for j in range(int((168 - 20) // period) + 1)])
            lab = label(name, font_size=29, color=col).next_to(ax.c2p(0, 1.4), UP, buff=0.1, aligned_edge=LEFT)
            panels.add(VGroup(A, grid, wave, lab))
            dots.add(mins)
        days = VGroup(*[label(rf"cave day {d + 1}", font_size=23, color=THRESH).move_to(panels[1][0].ax.c2p(d * 28 + 14, -1.4)
                                                                                         + DOWN * 0.3) for d in range(6)])
        rows = rows_of([
            (rf"his rhythm stretched toward {k['day_hours']} hours: \ the low point falls at the same place in every cave "
             r"day", SLEEPC),
            (r"his kept its 24-hour course for the whole month: \ the low point comes four hours earlier in each cave "
             r"day", CLOCKC),
            (r"two men, two answers: \ as an experiment, hopeless", GREY_A),
            (r"something inside Kleitman was keeping time, \ with no sun and no clock to copy", THRESH),
        ], 4.7, 29, 0.3).move_to([4.5, -0.15, 0])
        keep_in_frame(rows)
        src = historical_tag(archive.KLEITMAN_1938.cite)
        tag = note(r"a drawing of the reported pattern, \ not the data").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here's what the thermometers showed, drawn as a sketch. The dashed lines are the cave's days. "
            "<bookmark mark='a'/> Richardson's rhythm stretched. During the month it came to run close to "
            f"the cave's {k['day_hours']} hours, with its low point at the same place in each cave day. "
            "<bookmark mark='b'/> Kleitman's didn't move. His temperature kept its twenty-four-hour course "
            "for the whole month, rising and falling in step with a sun he couldn't see. He grew sleepy at "
            "about ten each evening, whatever the cave's schedule said he should be doing. "
            "<bookmark mark='c'/> Two men, two answers. As an experiment it's hopeless: with two people, "
            "anything could explain the difference. The newspapers suggested age. <bookmark mark='d'/> But "
            "Kleitman's stubborn curve was a sign of something that took sixty more years to pin down. "
            "Something inside him was keeping time, with no sun and no clock to copy."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), *[FadeIn(VGroup(p[0], p[1], p[3])) for p in panels], FadeIn(days))
            vo.wait_until("a")
            self.play(Create(panels[0][2]), run_time=2.5)
            self.play(FadeIn(dots[0], lag_ratio=0.3), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(panels[1][2]), run_time=2.5)
            self.play(FadeIn(dots[1], lag_ratio=0.3), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def question(self):
        head = heading(r"The brain lives in a body")
        s = load("sleep")
        mini = axes([48, 120], [0, 1], x_length=2.3, y_length=0.9, xticks=[], yticks=[], xlabel=r"", ylabel=r"")
        keep = (s["t"] >= 48) & (s["t"] <= 120)
        saw = VGroup(mini, curve(mini.ax, s["t"][keep], s["S"][keep], SLEEPC, stroke_width=4))
        icons = [clock_icon(0.5, CLOCKC, 4.33), saw, droplet(0.95, HORM), capsule(1.1, 0.42, DRUG)]
        names = [(r"a clock", CLOCKC, r"it keeps its own time, \ and light sets it"),
                 (r"a pressure to sleep", SLEEPC, r"it grows through every waking hour"),
                 (r"hormones", HORM, r"signals carried in the blood, \ slower than any nerve"),
                 (r"drugs", DRUG, r"molecules from outside, \ working the brain's own machinery")]
        cards = VGroup()
        for i, (icon, (name, col, what)) in enumerate(zip(icons, names)):
            x = -5.25 + 3.5 * i
            box = RoundedRectangle(width=3.25, height=4.7, corner_radius=0.15, color=col, stroke_width=2.5, fill_color=col,
                                   fill_opacity=0.06).move_to([x, 0.5, 0])
            icon.move_to([x, 1.9, 0])
            nm = label(name, font_size=34, color=col).move_to([x, 0.75, 0])
            wh = wrapped_label(what, 2.85, 29, WHITE)
            wh.move_to([x, -0.6, 0])
            cards.add(VGroup(box, icon, nm, wh))
        end = wrapped_label(r"Each one changes what a mind can do, hour by hour. \ Each can be written down as a small "
                            r"model, \ with numbers that can be checked.", 12.6, 31, THRESH).move_to([0, -2.85, 0])
        with self.voiceover(
            "Nine parts so far have built the neuron, the circuit, the brain, the instruments that read "
            "it, and the genes that vary it. All of them treated the brain as if it were the same at every "
            "hour of the day. It isn't. The brain lives in a body. <bookmark mark='a'/> There's a clock in "
            "it, and today we'll build one. <bookmark mark='b'/> There's a pressure to sleep that grows "
            "through every waking hour, and we'll build that too. <bookmark mark='c'/> There are hormones: "
            "signals carried in the blood, slower than any nerve. <bookmark mark='d'/> And there are "
            "drugs: molecules from outside that work the brain's own machinery. <bookmark mark='e'/> Each "
            "of the four changes what a mind can do, hour by hour. And each can be written down as a small "
            "model, with numbers that can be checked. So the question for this part is: what is the same "
            "mind doing at four in the afternoon and at four in the morning, and why is it so different?"
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(VGroup(c[0], c[1])) for c in cards])
            for mark_, c in zip("abcd", cards):
                vo.wait_until(mark_)
                self.play(FadeIn(VGroup(*c[2:]), shift=UP * 0.15), Indicate(c[1], color=WHITE, scale_factor=1.1))
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 10", font_size=34, color=GREY_B), label(r"Chemistry and Clocks", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the clock inside: \ its period, \ where it is, \ and why a 28-hour day defeats it",
            r"how light sets the clock, \ and what a flight across time zones does to it",
            r"sleep in the laboratory: \ stages, cycles and dreams",
            r"two processes that decide when you sleep; \ what losing sleep does, \ and why you do not notice",
            r"hormones: \ a loop that switches itself off",
            r"drugs: \ where they act, \ how much is enough, \ and why the body fights back",
        ], color=P.ACCENT, font_size=32, width=13.2)
        with self.voiceover(
            "Part ten: chemistry and clocks. <bookmark mark='a'/> We'll build the clock inside: its "
            "period, where it sits, and why a twenty-eight-hour day defeats it. <bookmark mark='b'/> We'll "
            "see how light sets the clock, and what a flight across time zones does to it. "
            "<bookmark mark='c'/> We'll go into the sleep laboratory, for the stages, the cycles and the "
            "dreams. <bookmark mark='d'/> We'll put two processes together to decide when you sleep, and "
            "see what losing sleep does, and why you don't notice. <bookmark mark='e'/> We'll meet the "
            "hormones, through one loop that switches itself off. <bookmark mark='f'/> And we'll take the "
            "drugs: where they act, how much is enough, and why the body fights back."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark_, r in zip("bcdef", obj.rows[1:]):
                vo.wait_until(mark_)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
