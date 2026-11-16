from __future__ import annotations

from videos.psychology.psych56.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"A line-up where the culprit is absent: \ how often does a witness pick someone anyway?", PERSON),
    (r"2", r"People judging whether others are lying: \ what share of judgements are right?", MODEL),
    (r"3", r"In a laboratory, \ students falsely accused of crashing a computer: \ what share sign a confession?", AUTH),
    (r"4", r"An IQ score of 71 with reliability 0.97: \ the 95\% interval?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        card_section(self, 1, r"On you: \ a line-up, \ and four numbers", r"Would you recognize him?")
        self.lineup()
        self.quiz()

    def lineup(self):
        d = load("onyou")
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        faces = VGroup(*[VGroup(Circle(0.42, color=GREY_B, stroke_width=3),
                                label(str(k + 1), font_size=20, color=GREY_A).shift(DOWN * 0.7)) for k in range(6)])
        faces.arrange(RIGHT, buff=0.35).move_to([-2.4, 0.8, 0])
        rows = rows_of([
            (r"on the course site: \ a short staged event, \ then a six-person line-up, \ and your confidence", WHITE),
            (rf"Psyche's witnesses, \ culprit present: \ {100 * d['present_culprit']:.0f}\% pick the culprit, \ "
             rf"{100 * d['present_filler']:.0f}\% a filler, \ {100 * d['present_none']:.0f}\% no one", GOOD),
            (rf"culprit absent: \ {100 * d['absent_any']:.0f}\% still pick someone; \ if the suspect is innocent, \ "
             rf"{100 * d['absent_suspect']:.0f}\% pick him", AUTH),
            (r"a fair line-up spreads mistaken picks over fillers: \ known-innocent people, \ whose choice clears the "
             r"suspect", MODEL),
        ], 6.0, 19, 0.38).move_to([3.4, -0.4, 0])
        tag = psyche_tag(r"\texttt{work.lineup\_roc}, \ $d'$ = 1.5, \ moderate criterion")
        with self.voiceover(
            "First, a line-up. <bookmark mark='a'/> On the course site there's a short staged event, then a "
            "six-person line-up, and you give your confidence. <bookmark mark='b'/> Among Psyche's witnesses, when "
            "the culprit is present, about fifty-six percent pick him, thirty-one percent pick a filler, and thirteen "
            "percent pick no one. <bookmark mark='c'/> When the culprit is absent, sixty-four percent still pick "
            "someone, and if the suspect is innocent, eleven percent pick him. <bookmark mark='d'/> A fair line-up "
            "spreads mistaken picks over fillers, known-innocent people whose choice clears the suspect."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(tag), FadeIn(faces))
            for m, r in zip("abcd", rows):
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
            "Now four numbers. <bookmark mark='a'/> One: in a line-up where the culprit is absent, how often does a "
            "witness pick someone anyway? <bookmark mark='b'/> Two: when people judge whether others are lying, what "
            "share of their judgements are right? <bookmark mark='c'/> Three: in a laboratory, students falsely "
            "accused of crashing a computer are asked to sign a confession. What share sign? <bookmark mark='d'/> And "
            "four: an IQ score of seventy-one, from a test with reliability zero point nine seven. What's the "
            "ninety-five percent interval? Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()
