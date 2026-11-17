from __future__ import annotations

from videos.psychology.psych44.common import *  # noqa: F403
from videos.psychology.psych44.diagrams import three

QUESTIONS = [
    (r"1", r"Nine ability tests, \ three factors, \ 301 children: \ does the model pass the chi-square test of exact "
           r"fit?", PERSON),
    (r"2", r"Two traits correlate 0.5; \ each is measured by three items with loadings 0.6. \ What do the sum scores "
           r"correlate?", MODEL),
    (r"3", r"A randomized treatment, \ a measured mediator, \ no real indirect effect. \ Can the analysis still find "
           r"one?", SYMP),
    (r"4", r"How many different diagrams can fit a correlation matrix exactly as well as the true one?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.draw()
        self.quiz()

    def card(self):
        card = chapter_card(1, r"On you: \ draw a model, \ and four numbers", r"Can you find an equally good diagram?",
                            lit=(), part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter one. On you: draw a model, and four numbers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def draw(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        stories = VGroup(*[wrapped_label(t, 3.8, 18, c) for t, c in (
            (r"stress (X) disturbs sleep (M), \ which lowers mood (Y)", GOOD),
            (r"low mood (Y) disturbs sleep (M), \ which raises stress (X)", SYMP),
            (r"poor sleep (M) raises both stress (X) and low mood (Y)", MODEL))]).arrange(RIGHT, buff=0.5)
        stories.move_to([0, 1.3, 0])
        diags = VGroup(*[three(k, c).scale(0.5) for k, c in (("chain", GOOD), ("reverse", SYMP), ("fork", MODEL))])
        for d_, s_ in zip(diags, stories):
            d_.next_to(s_, DOWN, buff=0.35)
        coll = VGroup(three("collider", AUTH).scale(0.5),
                      wrapped_label(r"but this one, \ stress and mood both disturbing sleep, \ fits worse", 4.6, 17,
                                    AUTH)).arrange(RIGHT, buff=0.4).move_to([0, -1.8, 0])
        with self.voiceover(
            "First, three stories. <bookmark mark='a'/> Stress disturbs sleep, which lowers mood. Or low mood "
            "disturbs sleep, which raises stress. Or poor sleep raises both stress and low mood. "
            "<bookmark mark='b'/> Draw each one as a diagram. All three imply the same correlation matrix, and fit "
            "any data equally well. <bookmark mark='c'/> One diagram on the same three variables does differ: stress "
            "and mood both disturbing sleep. That one implies stress and mood are uncorrelated, and it can be "
            "rejected. On the course site, you can try to draw a model that fits as well as the true one."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in stories], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in diags], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(coll))
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
            "Now four numbers to write down before the part answers them. <bookmark mark='a'/> One: nine ability "
            "tests, three factors, three hundred and one children. Does the model pass the chi-square test of exact "
            "fit? <bookmark mark='b'/> Two: two traits correlate zero point five, and each is measured by three items "
            "with loadings of zero point six. What do the sum scores correlate? <bookmark mark='c'/> Three: a "
            "randomized treatment, a measured mediator, and no real indirect effect. Can the analysis still find one? "
            "<bookmark mark='d'/> And four: how many different diagrams can fit a correlation matrix exactly as well "
            "as the true one? Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(4.0)
        self.clear_scene()
