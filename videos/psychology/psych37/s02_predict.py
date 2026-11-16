from __future__ import annotations

from videos.psychology.psych37.common import *  # noqa: F403
from videos.psychology.psych37.s01_hook import coins

QUESTIONS = [
    (r"1", r"In fifteen small-scale societies, \ what was the lowest average ultimatum offer?", CROWD),
    (r"2", r"In speed dating, \ how much of one person's desire for a particular partner could machine learning "
           r"predict from over 100 measured traits?", PERSON),
    (r"3", r"Across 148 studies, \ how much higher were the odds of survival for people with stronger social "
           r"relationships?", GOOD),
    (r"4", r"A divorce model is 90\% accurate on the couples it was fitted to. \ How accurate is it on new couples?",
     AUTH),
]


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.respond()
        self.quiz()

    def card(self):
        card = chapter_card(1, r"On you: \ an offer, \ and four numbers", r"Would you accept two coins out of ten?",
                            lit=(), part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter one. On you: an offer, and four numbers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def respond(self):
        stage = demo_stage(13.2, 6.2, center=[0, -0.2, 0])
        keep = coins(8, CROWD).move_to([-2.0, 1.0, 0])
        give = coins(2, MODEL).move_to([2.6, 1.0, 0])
        lk = label(r"the proposer keeps", font_size=18, color=CROWD).next_to(keep, UP, buff=0.2)
        lg = label(r"you get", font_size=18, color=MODEL).next_to(give, UP, buff=0.2)
        ask = wrapped_label(r"accept, \ and you get 2 and the stranger 8; \ reject, \ and both get nothing", 10.0, 24,
                            YOU).move_to([0, -0.8, 0])
        clock = countdown_ring(0.4).move_to([5.4, -1.9, 0])
        with self.voiceover(
            "First, play the responder. <bookmark mark='a'/> A stranger you'll never meet has ten coins, keeps "
            "eight, and offers you two. <bookmark mark='b'/> If you accept, you get two and they get eight. If you "
            "reject, neither of you gets anything. <bookmark mark='c'/> Decide now: accept or reject? "
            "<bookmark mark='d'/> Many people reject an offer like this, and they're not confused about the "
            "arithmetic."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(keep), FadeIn(give), FadeIn(lk), FadeIn(lg))
            vo.wait_until("b")
            self.play(FadeIn(ask))
            vo.wait_until("c")
            self.play(FadeIn(clock))
            self.play(clock.animate.rotate(-TAU), run_time=3.0)
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
            "Now four numbers to write down before the part answers them. <bookmark mark='a'/> One: the same game "
            "was played in fifteen small-scale societies. What was the lowest average offer? "
            "<bookmark mark='b'/> Two: after a round of speed dating, how much of one person's desire for a "
            "particular partner could machine learning predict, from over a hundred measured traits? "
            "<bookmark mark='c'/> Three: across a hundred and forty-eight studies, how much higher were the odds of "
            "survival for people with stronger social relationships? <bookmark mark='d'/> And four: a divorce "
            "model is ninety percent accurate on the couples it was fitted to. How accurate is it on new couples? "
            "Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(4.0)
        self.clear_scene()
