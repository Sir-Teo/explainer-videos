from __future__ import annotations

from videos.psychology.psych62.common import *  # noqa: F403

PAIRS = [(0, False), (120, True), (60, False), (180, False), (60, True), (150, True)]

QUESTIONS = [
    (r"1", r"Mental-rotation slopes rose for 53 of 54 people (Part 24). \ Is one person's slope a reliable "
           r"measure: \ split-half reliability above 0.7, \ or below?", PERSON),
    (r"2", r"The Ledger has 322 rows. \ What share held up (replicated, \ smaller, \ or the finding stands)?", MODEL),
    (r"3", r"Psyche can sit 7 of the Battery's 13 tasks with one set of parameters. \ How many match their "
           r"published signatures?", AUTH),
    (r"4", r"Kant made three objections. \ How many survive?", KANT),
]


class Predict(VoiceoverScene):
    def construct(self):
        card_section(self, 1, r"On you: \ the last experiment, \ and four numbers", r"Same, \ or mirror?")
        self.rotation()
        self.quiz()

    def pair(self, angle, mirror):
        left = label(r"R", font_size=120, color=WHITE).move_to([-2.2, -0.2, 0])
        right = label(r"R", font_size=120, color=WHITE)
        if mirror:
            right.flip(UP)
        right.rotate(-np.deg2rad(angle)).move_to([2.2, -0.2, 0])
        return VGroup(left, right)

    def rotation(self):
        head = heading(r"Same letter, \ or its mirror image?")
        note = wrapped_label(r"say ``same'' or ``mirror'' aloud for each pair, \ as fast as you can", 9.0, 22, YOU)
        note.to_edge(DOWN, buff=0.6)
        pairs = [self.pair(a, m) for a, m in PAIRS]
        with self.voiceover(
            "First, the last experiment on you, the one that opens this part's question. <bookmark mark='a'/> "
            "Each pair shows the letter R on the left, and on the right either the same R turned, or its mirror "
            "image turned. Say same or mirror aloud for each one, as fast as you can. <bookmark mark='b'/> Here they "
            "come."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(note))
            vo.wait_until("b")
        for p in pairs:
            self.play(FadeIn(p), run_time=0.3)
            self.wait(2.4)
            self.play(FadeOut(p), run_time=0.2)
        answers = VGroup(*[label(rf"{i + 1}:\ {'mirror' if m else 'same'}, \ {a}$^\circ$", font_size=22,
                                 color=MODEL if m else GOOD) for i, (a, m) in enumerate(PAIRS)])
        answers.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-3.6, -0.3, 0])
        rows = rows_of([
            (r"most people take longer the further the letter is turned: \ Part 24's mental rotation, \ about a "
             r"tenth of a second per 10 degrees for three-dimensional shapes", WHITE),
            (r"the slope of time against angle is everyone's: \ a robust effect", MODEL),
            (r"but is your slope a stable fact about you? \ That is this dissertation's question", YOU),
        ], 6.0, 20, 0.36).move_to([3.2, -0.3, 0])
        with self.voiceover(
            "Here are the answers. <bookmark mark='a'/> Most people take longer the further the letter is turned. "
            "That's Part 24's mental rotation, about a tenth of a second for every ten degrees with three-dimensional "
            "shapes. <bookmark mark='b'/> The slope of time against angle is everyone's: a robust effect. "
            "<bookmark mark='c'/> But is your slope a stable fact about you? That's this dissertation's question."
        ) as vo:
            self.play(FadeOut(note), LaggedStart(*[FadeIn(a_) for a_ in answers], lag_ratio=0.2))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = VGroup()
        for n, q, c in QUESTIONS:
            rows.add(VGroup(label(n, font_size=34, color=c), wrapped_label(q, 9.4, 21, WHITE),
                            label(r"\underline{\hspace{1.2cm}}", font_size=26, color=YOU)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, -0.3, 0])
        with self.voiceover(
            "Now the last four numbers of the series. <bookmark mark='a'/> One: mental-rotation slopes rose for "
            "fifty-three of fifty-four people in Part 24. Is one person's slope a reliable measure, with a split-half "
            "reliability above zero point seven, or below? <bookmark mark='b'/> Two: the Ledger has three hundred and "
            "twenty-two rows. What share held up? <bookmark mark='c'/> Three: Psyche can sit seven of the Battery's "
            "thirteen tasks with one set of parameters. How many match their published signatures? "
            "<bookmark mark='d'/> And four: Kant made three objections. How many survive? Pause here, and write them "
            "down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()
