from __future__ import annotations

from videos.psychology.psych50.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"28 people answer one question on a 1-to-7 scale. \ The paper reports a mean of 5.19. \ Possible?", PERSON),
    (r"2", r"A drug's true effect is 0.2; \ only significant trials, \ and a few others, \ are published. \ What does "
           r"a meta-analysis of the published trials find?", AUTH),
    (r"3", r"One dataset, \ a small true effect, \ 96 defensible analyses. \ What share come out significant?", MODEL),
    (r"4", r"Of the 263 findings in this series' Ledger so far, \ what share failed or were retracted?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.grim()
        self.quiz()

    def card(self):
        card = chapter_card(1, r"On you: \ a mean that cannot be, \ and four numbers", r"Can arithmetic catch an "
                            r"error?", lit=(), part=PART, scale=("society",), marr=("what",))
        with self.voiceover("Chapter one. On you: a mean that cannot be, and four numbers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def grim(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = rows_of([
            (r"28 people each give a whole number from 1 to 7", WHITE),
            (r"so the total is a whole number, \ and the mean is that total divided by 28", MODEL),
            (r"a total of 145 gives 5.18; \ 146 gives 5.21; \ no total gives 5.19", AUTH),
            (r"a reported mean of 5.19 is impossible: \ a typo, \ an exclusion not mentioned, \ or worse", PERSON),
            (r"on the site: \ five reported means to test, \ and the check that finds them", YOU),
        ], 11.8, 23, 0.36).move_to([0, -0.3, 0])
        eq = MathTex(r"\frac{145}{28} = 5.179\ldots \qquad \frac{146}{28} = 5.214\ldots", font_size=40,
                     color=THRESH).move_to([0, 2.2, 0])
        with self.voiceover(
            "First, a test you can do in your head. <bookmark mark='a'/> Twenty-eight people each give a whole "
            "number from one to seven. <bookmark mark='b'/> So the total is a whole number, and the mean is that "
            "total divided by twenty-eight. <bookmark mark='c'/> A total of a hundred and forty-five gives five point "
            "one eight. A hundred and forty-six gives five point two one. No total gives five point one nine. "
            "<bookmark mark='d'/> So a reported mean of five point one nine is impossible: a typo, an exclusion "
            "nobody mentioned, or worse. <bookmark mark='e'/> On the course site you can test five reported means "
            "yourself."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15), *( [FadeIn(eq)] if m == "c" else []))
        self.wait(1.0)
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = VGroup()
        for n, q, c in QUESTIONS:
            rows.add(VGroup(label(n, font_size=34, color=c), wrapped_label(q, 9.4, 21, WHITE),
                            label(r"\underline{\hspace{1.2cm}}", font_size=26, color=YOU)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, -0.3, 0])
        with self.voiceover(
            "Now four numbers. <bookmark mark='a'/> One: twenty-eight people answer one question on a one-to-seven "
            "scale, and the paper reports a mean of five point one nine. Possible? <bookmark mark='b'/> Two: a drug's "
            "true effect is zero point two, and only significant trials, plus a few others, are published. What does a "
            "meta-analysis of the published trials find? <bookmark mark='c'/> Three: one dataset with a small true "
            "effect, and ninety-six defensible analyses. What share come out significant? <bookmark mark='d'/> And "
            "four: of the two hundred and sixty-three findings in this series' Ledger so far, what share failed or "
            "were retracted? Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()
