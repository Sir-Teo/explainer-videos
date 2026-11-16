from __future__ import annotations

from videos.psychology.psych36.common import *  # noqa: F403
from videos.psychology.psych36.s01_hook import matrix_table

QUESTIONS = [
    (r"1", r"Identical r\'esum\'es, \ with names that sound white or Black: \ how many more callbacks did the "
           r"white names get?", CROWD),
    (r"2", r"Take the Implicit Association Test twice, \ weeks apart: \ how well do your two scores correlate?", MODEL),
    (r"3", r"In US hiring experiments from 1989 to 2015, \ how much did discrimination against Black applicants "
           r"fall?", AUTH),
    (r"4", r"A registered study of 2{,}064 Dutch pupils tested whether a stereotype lowers girls' maths scores: \ "
           r"by how much did it?", PERSON),
]


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.allocate()
        self.quiz()

    def card(self):
        card = chapter_card(1, r"On you: \ a group, \ and four numbers", r"Which column would you choose?", lit=(),
                            part=PART, scale=("group",), marr=("what",))
        with self.voiceover("Chapter one. On you: a group, and four numbers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def allocate(self):
        d = load("matrix")
        stage = demo_stage(13.2, 6.2, center=[0, -0.2, 0])
        intro = wrapped_label(r"you preferred the ``Klee'' pictures; \ you will never meet either boy; \ the points "
                              r"are real money for them, \ not for you", 11.0, 22, WHITE).move_to([0, 1.9, 0])
        T = matrix_table(d["ingroup"], d["outgroup"]).move_to([0.3, 0.2, 0])
        ask = wrapped_label(r"pick a column, \ and remember why", 8.0, 24, YOU).move_to([0, -1.6, 0])
        clock = countdown_ring(0.4).move_to([5.4, -1.6, 0])
        with self.voiceover(
            "First, take the boys' place. <bookmark mark='a'/> You preferred the Klee pictures. You'll never meet "
            "either of these boys, and the points are real money for them, not for you. "
            "<bookmark mark='b'/> The top number goes to a boy in your group, and the bottom number to a boy in "
            "the other. <bookmark mark='c'/> Pick a column, and remember why you picked it. "
            "<bookmark mark='d'/> Most people pick the middle, or the right. Many of Tajfel's boys did not."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(intro))
            vo.wait_until("b")
            self.play(FadeIn(T))
            vo.wait_until("c")
            self.play(FadeIn(ask), FadeIn(clock))
            self.play(clock.animate.rotate(-TAU), run_time=4.0)
            vo.wait_until("d")
        self.wait(1.0)
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = VGroup()
        for n, q, c in QUESTIONS:
            rows.add(VGroup(label(n, font_size=34, color=c), wrapped_label(q, 9.4, 22, WHITE),
                            label(r"\underline{\hspace{1.2cm}}", font_size=26, color=YOU)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, -0.3, 0])
        with self.voiceover(
            "Now four numbers to write down before the part answers them. <bookmark mark='a'/> One: identical "
            "résumés were sent out with names that sound white or Black. How many more callbacks did the white "
            "names get? <bookmark mark='b'/> Two: take the Implicit Association Test twice, weeks apart. How well "
            "do your two scores correlate? <bookmark mark='c'/> Three: in American hiring experiments from 1989 to "
            "2015, how much did discrimination against Black applicants fall? <bookmark mark='d'/> And four: a "
            "registered study of over two thousand Dutch pupils tested whether a stereotype lowers girls' maths "
            "scores. By how much did it? Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(4.0)
        self.clear_scene()
