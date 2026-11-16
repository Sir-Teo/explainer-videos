from __future__ import annotations

from videos.psychology.psych57.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"Patients with irritable bowel syndrome are told openly that their pill contains nothing. \ Do they "
           r"improve more than untreated patients?", PERSON),
    (r"2", r"People at high risk of diabetes: \ how much did an intensive lifestyle programme cut new cases?", MODEL),
    (r"3", r"Patients prescribed long-term medicines: \ roughly what share take them as prescribed?", AUTH),
    (r"4", r"A mental health service where everyone waits for full therapy: \ what share recover within six "
           r"months?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        card_section(self, 1, r"On you: \ a pill with nothing in it, \ and four numbers", r"Can a pill work if you "
                     r"know it is empty?")
        self.pill()
        self.quiz()

    def pill(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        bottle = VGroup(RoundedRectangle(width=1.6, height=2.2, corner_radius=0.2, color=SYMP, fill_opacity=0.15),
                        label(r"PLACEBO", font_size=20, color=SYMP), label(r"no active ingredient", font_size=13,
                                                                             color=GREY_A))
        bottle[1].move_to(bottle[0]).shift(UP * 0.2)
        bottle[2].next_to(bottle[1], DOWN, buff=0.15)
        bottle.move_to([-4.2, 0.0, 0])
        rows = rows_of([
            (r"an open-label placebo: \ patients are told the pills are inert, \ like sugar pills, \ and that placebos "
             r"have helped others", WHITE),
            (r"on the course site: \ predict whether open-label placebo patients improved more than patients who "
             r"got nothing, \ then see the trial", PERSON),
            (r"the answer in chapter four, \ and why it is contested", MODEL),
            (r"nothing you enter is stored or sent", YOU),
        ], 7.4, 21, 0.4).move_to([2.2, -0.3, 0])
        with self.voiceover(
            "First, a prediction. <bookmark mark='a'/> In an open-label placebo trial, patients are told that the "
            "pills are inert, like sugar pills, and that placebos have helped other people. <bookmark mark='b'/> On "
            "the course site, predict whether these patients improved more than patients who got nothing, then see "
            "the trial. <bookmark mark='c'/> The answer comes in chapter four, along with why it's contested. "
            "<bookmark mark='d'/> Nothing you enter is stored or sent."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(bottle))
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
            "Now four numbers. <bookmark mark='a'/> One: patients with irritable bowel syndrome are told openly that "
            "their pill contains nothing. Do they improve more than untreated patients? <bookmark mark='b'/> Two: "
            "people at high risk of diabetes. How much did an intensive lifestyle programme cut new cases? "
            "<bookmark mark='c'/> Three: patients prescribed long-term medicines. Roughly what share take them as "
            "prescribed? <bookmark mark='d'/> And four: a mental health service where everyone waits for full "
            "therapy. What share recover within six months? Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()
