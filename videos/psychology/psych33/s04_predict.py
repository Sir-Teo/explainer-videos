from __future__ import annotations

from videos.psychology.psych33.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"How strongly does a child's honesty in one situation predict their honesty in another?", PERSON),
    (r"2", r"How strongly does a person's average over sixteen situations predict their average over sixteen others?",
     PERSON),
    (r"3", r"Sort people into types on four dimensions, \ each measured as reliably as a good test. \ What share get "
           r"the same four-letter type when tested again?", O_),
    (r"4", r"What share of the differences between people in personality traits comes from differences in their "
           r"genes?", A_),
]


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.quiz()
        self.inventory()

    def card(self):
        card = chapter_card(3, r"On you: \ four numbers", r"How consistent are people, \ and how stable are types?",
                            lit=(), part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter three. On you: four numbers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = VGroup()
        for n, q, c in QUESTIONS:
            rows.add(VGroup(label(n, font_size=34, color=c), wrapped_label(q, 9.4, 23, WHITE),
                            label(r"\underline{\hspace{1.2cm}}", font_size=26, color=YOU)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.3, 0])
        scale = label(r"answer each with a correlation or a share, \ from 0 to 1", font_size=20, color=GREY_B)
        scale.next_to(rows, DOWN, buff=0.35)
        with self.voiceover(
            "Your turn. Write down four numbers before the part answers them. <bookmark mark='a'/> One: how strongly "
            "does a child's honesty in one situation predict their honesty in another, as a correlation? "
            "<bookmark mark='b'/> Two: how strongly does a person's average over sixteen situations predict their "
            "average over sixteen other situations? <bookmark mark='c'/> Three: sort people into types on four "
            "dimensions, each measured as reliably as a good test. What share get the same four-letter type when "
            "they're tested again? <bookmark mark='d'/> And four: what share of the differences between people in "
            "personality traits comes from differences in their genes? Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(scale))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(4.0)
        self.clear_scene()

    def inventory(self):
        head = heading(r"And a profile of your own")
        bars_ = VGroup()
        demo = [0.62, 0.48, 0.3, 0.71, 0.55]
        for i, (t, v) in enumerate(zip(("A", "C", "E", "N", "O"), demo)):
            y = 1.6 - 0.75 * i
            track = Line([-3.0, y, 0], [3.0, y, 0], color=GREY_D, stroke_width=10)
            dot = Dot([-3.0 + 6.0 * v, y, 0], radius=0.13, color=TRAIT_COL[t])
            bars_.add(VGroup(track, dot, label(TRAIT_NAME[t], font_size=22, color=TRAIT_COL[t])
                             .next_to(track, LEFT, buff=0.3)))
        note = label(r"an illustration, \ not anyone's result", font_size=18, color=GREY_B).next_to(bars_, DOWN,
                                                                                                     buff=0.3)
        rows = rows_of([
            (r"this part's interactive gives you the same 25 items the SAPA sample answered, \ and places you on "
             r"five continua against their 2{,}800 people", YOU),
            (r"nothing you answer is stored or sent; \ the result is five positions, \ not a type", GREY_A),
        ], 12.0, 22, 0.3).move_to([0, -2.7, 0])
        with self.voiceover(
            "There's also a profile of your own. <bookmark mark='a'/> This part's interactive gives you the same "
            "twenty-five items the SAPA sample answered, and places you on five continua against their two thousand "
            "eight hundred people. <bookmark mark='b'/> Nothing you answer is stored or sent, and the result is five "
            "positions, not a type. Chapter four explains why that matters."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(b) for b in bars_], lag_ratio=0.2), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
        self.clear_scene()
