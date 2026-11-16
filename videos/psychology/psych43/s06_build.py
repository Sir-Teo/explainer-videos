from __future__ import annotations

from videos.psychology.psych43.common import *  # noqa: F403


class Build(VoiceoverScene):
    def construct(self):
        self.card()
        self.strip()
        self.checks()

    def card(self):
        card = chapter_card(5, r"Building the experiment", r"What happens on every trial?", lit=(), part=PART,
                            scale=("person",), marr=("how",))
        with self.voiceover("Chapter five. Building the experiment."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def strip(self):
        head = heading(r"The trial strip")
        steps = (("fixation", r"700 to 1{,}200 ms, \\ at random", GREY_B), ("word", r"until a key", PERSON),
                 ("feedback", r"300 ms", SYMP))
        boxes = VGroup()
        for name, dur, c in steps:
            boxes.add(VGroup(word_chip(name, color=c, font_size=18, width=2.4), label(dur, font_size=14, color=GREY_A))
                      .arrange(DOWN, buff=0.15))
        boxes.arrange(RIGHT, buff=0.5).move_to([0, 1.5, 0])
        arrows = VGroup(*[Arrow(boxes[i][0].get_right(), boxes[i + 1][0].get_left(), buff=0.05, color=GREY_B,
                                stroke_width=3, max_tip_length_to_length_ratio=0.3) for i in range(2)])
        rows = rows_of([
            (r"the Stroop task as a trial strip: \ what appears, \ for how long, \ and what ends it; \ every timing "
             r"is written down", WHITE),
            (r"counterbalancing: \ congruent and incongruent trials in a random order, \ each colour equally often "
             r"as word and as ink, \ and response keys swapped across participants", MODEL),
            (r"the fixation lasts a random time, \ so no one can respond to the rhythm instead of the word "
             r"(Part 1's foreperiod)", PERSON),
        ], 12.4, 22, 0.42).move_to([0, -1.3, 0])
        with self.voiceover(
            "Building the experiment means writing down every trial. <bookmark mark='a'/> For the Stroop task on the "
            "site: a fixation cross, a colour word that stays until a key is pressed, and brief feedback. "
            "Every timing is fixed in advance. <bookmark mark='b'/> Counterbalancing: congruent and incongruent "
            "trials in a random order, each colour used equally often as a word and as an ink, and the response keys "
            "swapped across participants. <bookmark mark='c'/> And the fixation lasts a random time, so no one can "
            "respond to the rhythm instead of the word. That's Part 1's foreperiod."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.3), Create(arrows))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def checks(self):
        head = heading(r"Checks built in")
        rows = rows_of([
            (r"attention checks: \ an occasional trial with an obvious answer; \ the rule for excluding people who "
             r"miss them is fixed in advance", SYMP),
            (r"timing: \ a browser's clock and screen add delay and jitter; \ validate them with a photodiode or "
             r"a known stimulus, \ as Part 1 measured", PERSON),
            (r"a pilot: \ run the whole pipeline on a few people to find the bugs, \ and throw their data away", MODEL),
            (r"the experiment, \ its code and its materials are shared, \ so anyone can run the same study", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        with self.voiceover(
            "Checks are built in. <bookmark mark='a'/> Attention checks: an occasional trial with an obvious answer, "
            "and the rule for excluding people who miss them is fixed in advance. <bookmark mark='b'/> Timing: a "
            "browser's clock and screen add delay and jitter. Validate them with a light sensor on the screen, or a "
            "known stimulus, as Part 1 did. <bookmark mark='c'/> A pilot: run the whole pipeline on a few people to "
            "find the bugs, and set their data aside. <bookmark mark='d'/> And the experiment, its code and its "
            "materials are shared, so that anyone can run the same study."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
