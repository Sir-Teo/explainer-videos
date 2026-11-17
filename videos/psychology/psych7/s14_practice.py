from __future__ import annotations

import numpy as np

from videos.psychology.psych7.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.case()
        self.honest()
        self.many()
        self.report()

    def card(self):
        card = chapter_card(13, r"In practice: one patient, one question",
                            r"Is this score lower than it should be?", lit=(), part=PART, scale=("brain", "person"),
                            marr=("why",))
        with self.voiceover(
            "Chapter thirteen. In practice: one patient, one question."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _line(self, d, y=0.2):
        A = axes([20, 40], [0, 1], x_length=11.0, y_length=0.9, xticks=[20, 25, 30, 35, 40], yticks=[],
                 xlabel=r"score on a 40-point memory test", ylabel=r"", center=[0, y, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(float(c), 0.45), radius=0.14, color=SPARED) for c in d["controls"]])
        case = Dot(ax.c2p(d["case"], 0.45), radius=0.18, color=LESION)
        mean = DashedLine(ax.c2p(d["mean"], 0), ax.c2p(d["mean"], 1.1), color=GREY_A, stroke_width=2.5)
        mean_l = label(rf"controls' mean {d['mean']:.1f}", font_size=25, color=GREY_A).next_to(mean, UP, buff=0.05)
        case_l = label(rf"the patient: \ {d['case']:.0f}", font_size=27, color=LESION).next_to(case, UP, buff=0.2)
        return A, dots, case, mean, mean_l, case_l

    def case(self):
        d = load("practice")
        head = heading(r"A clinical neuropsychologist's working day")
        intro = VGroup(
            wrapped_label(r"A teacher of 58, three months after a small stroke. \ She says her memory is not "
                          r"what it was.", 12.6, 29, WHITE),
            wrapped_label(r"The question is never ``is she damaged?'' \ It is: \ is this score lower than it "
                          r"should be, for her?", 12.6, 29, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(head, DOWN, buff=0.3)
        A, dots, case, mean, mean_l, case_l = self._line(d, y=-0.75)
        z = VGroup(
            MathTex(rf"z = \frac{{{d['case']:.0f} - {d['mean']:.2f}}}{{{d['sd']:.2f}}} = {d['z']:.2f}", font_size=40),
            label(rf"about 1 healthy person in {fmt_int(round(d['one_in_z'], -2))} scores that low", font_size=28,
                  color=THRESH),
        ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.55)
        tag = note(r"an invented case").to_corner(DR, buff=0.15)
        with self.voiceover(
            "Most people who use this part for a living aren't mapping the brain. They're clinical "
            "neuropsychologists, and their unit of work is one person. <bookmark mark='a'/> Here's an "
            "invented one. A teacher, fifty-eight, three months after a small stroke. She says her memory "
            "isn't what it was. <bookmark mark='b'/> The question is never, is she damaged? The scan "
            "answered that. It's this: is her score lower than it should be, for someone like her? "
            "<bookmark mark='c'/> So she takes a memory test scored out of forty, and so do eight healthy "
            f"people of her age and schooling. They average {d['mean']:.0f}. <bookmark mark='d'/> She scores "
            f"{d['case']:.0f}. <bookmark mark='e'/> The textbook move is a z-score: her distance from the "
            f"controls' mean, in their standard deviations. It comes to {abs(d['z']):.1f} below. On the "
            f"normal curve, that's a score you'd see in about one healthy person in "
            f"{fmt_int(round(d['one_in_z'], -2))}. Case closed, it seems."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(intro[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(intro[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(A), LaggedStart(*[FadeIn(k, scale=1.5) for k in dots], lag_ratio=0.2), FadeIn(mean),
                      FadeIn(mean_l), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(case, scale=2.0), FadeIn(case_l))
            vo.wait_until("e")
            self.play(FadeIn(z, shift=UP * 0.1))
        self.clear_scene()

    def honest(self):
        d = load("practice")
        head = heading(r"Eight controls are a sample, \ not the population")
        A, dots, case, mean, mean_l, case_l = self._line(d, y=1.2)
        eq = VGroup(MathTex(r"t = \frac{x - \bar{c}}{s\,\sqrt{(n + 1)/n}}", font_size=38),
                    MathTex(rf"=\; {d['t']:.2f}", font_size=38),
                    label(rf"on $n - 1 = {d['df']}$ degrees of freedom", font_size=30)).arrange(RIGHT, buff=0.35)
        eq.move_to([0, -0.9, 0])
        if eq.width > 12.6:
            eq.width = 12.6
        table = VGroup(
            VGroup(label(r"treating the eight as the truth ($z$)", font_size=28, color=GREY_A),
                   label(rf"about 1 in {fmt_int(round(d['one_in_z'], -2))}", font_size=34, color=GREY_A)).arrange(
                RIGHT, buff=0.6),
            VGroup(label(r"treating the eight as a sample ($t$)", font_size=28, color=THRESH),
                   label(rf"about 1 in {d['one_in_t']:.0f}", font_size=34, color=THRESH)).arrange(RIGHT, buff=0.6),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.25).to_edge(DOWN, buff=0.6)
        src = note(r"the test: Crawford \& Howell (1998)").to_corner(DR, buff=0.15)
        ratio = d["one_in_z"] / d["one_in_t"]
        with self.voiceover(
            "But look at what the z-score took for granted. It used the controls' mean and standard "
            "deviation as if they were the population's. They're estimates, from eight people. With eight "
            "people, the standard deviation alone could easily be off by a quarter. <bookmark mark='a'/> The "
            "honest version treats the controls as a sample. The patient is one more observation, and you "
            "ask how far she lies from them, allowing for how poorly eight people pin the population down. "
            "That's a t-test with one person on one side, and it's the standard method for a single case. "
            f"<bookmark mark='b'/> Here it gives t of {d['t']:.1f}, on seven degrees of freedom. "
            f"<bookmark mark='c'/> About one healthy person in {d['one_in_t']:.0f} would score that low. Not "
            f"one in {fmt_int(round(d['one_in_z'], -2))}. The z-score overstated how rare she is by a factor "
            f"of {ratio:.0f}. <bookmark mark='d'/> She's still unusual. But one in "
            f"{d['one_in_t']:.0f} is a different sentence to write in a report that decides whether someone "
            "goes back to work. This is Part 4, applied to one person."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(dots), FadeIn(case), FadeIn(mean), FadeIn(mean_l),
                      FadeIn(case_l), FadeIn(src))
            vo.wait_until("a")
            self.play(Write(eq[0]))
            vo.wait_until("b")
            self.play(FadeIn(eq[1]), FadeIn(eq[2]), FadeIn(table[0]))
            vo.wait_until("c")
            self.play(FadeIn(table[1], shift=UP * 0.1))
            vo.wait_until("d")
        self.clear_scene()

    def many(self):
        d = load("practice")
        head = heading(r"Nobody gives one test")
        A = axes([0, 30], [0, 1.0], x_length=6.4, y_length=4.2, xticks=[0, 10, 20, 30], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: pct(v), xlabel=r"tests in the battery", ylabel=r"", center=[-3.3, -0.5, 0])
        ax = A.ax
        ylab = wrapped_label(r"chance that a healthy person ``fails'' at least one", 6.0, 24, GREY_A).next_to(
            A, UP, buff=0.12)
        c = curve(ax, np.r_[0, d["k"]], np.r_[0, d["at_least_one"]], THRESH, stroke_width=5)
        marks = VGroup()
        for k, v in ((10, d["ten"]), (20, d["twenty"])):
            marks.add(VGroup(Dot(ax.c2p(k, v), radius=0.09, color=WHITE),
                             label(pct(v), font_size=28, color=WHITE).next_to(ax.c2p(k, v), UL, buff=0.08)))
        rows = VGroup(
            wrapped_label(r"``fails'': \ scores below the 5th percentile of healthy people", 5.8, 29, WHITE),
            label(r"$P($at least one of $k) = 1 - 0.95^{\,k}$", font_size=31, color=THRESH),
            wrapped_label(rf"10 tests: \ {pct(d['ten'])}. \ \ 20 tests: \ {pct(d['twenty'])}.", 5.6, 30, WHITE),
            wrapped_label(r"One low score in a long battery is what health looks like. \ A deficit is a "
                          r"pattern: \ several low scores that go together, \ and a reason.", 5.8, 29, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to([3.7, -0.3, 0])
        keep_in_frame(rows)
        tag = note(r"computed, for independent tests").to_corner(DR, buff=0.15)
        with self.voiceover(
            "There's a second trap, and you met it in Part 4 under another name. Nobody gives one test. A "
            "clinic's battery has ten or twenty. <bookmark mark='a'/> Call a score a failure if it's below "
            "the fifth percentile of healthy people. On one test, a healthy person fails five times in a "
            "hundred. <bookmark mark='b'/> On ten independent tests, the chance of failing at least one is "
            f"{100 * d['ten']:.0f} percent. <bookmark mark='c'/> On twenty, it's {100 * d['twenty']:.0f} "
            "percent. Real tests are "
            "correlated, so the true figures are somewhat lower. They're nowhere near five percent. "
            "<bookmark mark='d'/> So one low score in a long battery isn't a finding. It's what a healthy "
            "person looks like. A deficit is a pattern: several low scores that belong together, where the "
            "damage says they should be, with the rest intact. That's a dissociation, inside one patient. "
            "And as in chapter four, the difference between two of her scores needs its own test, against "
            "how much the same two scores differ in healthy people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(ylab), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            self.play(Create(c), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(marks[0], scale=1.5))
            vo.wait_until("c")
            self.play(FadeIn(marks[1], scale=1.5), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def report(self):
        head = heading(r"What goes in the report")
        items = [
            (r"the question, \ in the referrer's words", WHITE),
            (r"what she could do before: \ schooling, work, \ tests that damage usually spares", WHITE),
            (r"each score against people like her, \ with the size of the control sample in the arithmetic",
             THRESH),
            (r"how many tests were given, \ and how many low scores that many tests produce by chance", THRESH),
            (r"the pattern: \ what is low, what is intact, \ and whether the scan says it should be", SPARED),
            (r"what it means on Monday morning: \ a classroom, a timetable, thirty names", P.ACCENT),
        ]
        rows = VGroup(*[wrapped_label(rf"{k + 1}. \ {t}", 12.6, 33, col) for k, (t, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        keep_in_frame(rows)
        with self.voiceover(
            "So here's the shape of a careful report. <bookmark mark='a'/> The question, in the words of "
            "whoever asked it. <bookmark mark='b'/> What she could do before, estimated from her schooling, "
            "her work, and the kinds of test that damage usually spares. <bookmark mark='c'/> Each score "
            "set against people like her, with the size of the comparison group in the arithmetic. "
            "<bookmark mark='d'/> How many tests were given, and how many low scores that many tests "
            "produce by chance. <bookmark mark='e'/> The pattern: what's low, what's intact, and whether "
            "the scan says it should be so. <bookmark mark='f'/> And last, what it means on Monday "
            "morning, in a classroom, with a timetable and thirty names to remember. The method of this "
            "part, from Broca onward, is in that list. One person, compared fairly, on tasks chosen to "
            "tell two explanations apart."
        ) as vo:
            self.play(FadeIn(head))
            for k, mark_ in enumerate("abcdef"):
                vo.wait_until(mark_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
        self.clear_scene()
