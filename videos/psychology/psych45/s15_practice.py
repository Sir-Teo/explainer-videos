from __future__ import annotations

from videos.psychology.psych45.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.where()
        self.machines()

    def card(self):
        card = chapter_card(14, r"In practice: \ exams, \ clinics and machines", r"Where does item response theory "
                            r"run?", lit=(), part=PART, scale=("person", "society"), marr=("how",))
        with self.voiceover("Chapter fourteen. In practice: exams, clinics and machines."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def where(self):
        head = heading(r"Where it runs")
        data = (
            (r"admissions and licensing", r"adaptive admission and licensing exams; \ every new item pre-tested "
                                          r"unscored inside a live test, \ then calibrated", MODEL),
            (r"language tests", r"adaptive placement and proficiency tests, \ each level tied to a common scale", SYMP),
            (r"clinical short forms", r"item banks for symptoms such as fatigue, \ pain and depression; \ a handful "
                                      r"of adaptive questions instead of a long form", GOOD),
            (r"learning platforms", r"knowledge tracing and Elo ratings deciding the next exercise", PERSON),
        )
        rows = VGroup()
        for what, how, c in data:
            rows.add(VGroup(word_chip(what, color=c, font_size=18, width=4.0), wrapped_label(how, 7.8, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.2, 0])
        with self.voiceover(
            "Where it runs. <bookmark mark='a'/> Admission and licensing exams, many of them adaptive. New items are "
            "tried out unscored inside live tests, then calibrated. <bookmark mark='b'/> Language tests that place "
            "people on a common scale of levels. <bookmark mark='c'/> Clinical item banks for symptoms such as fatigue, "
            "pain and depression, where a handful of adaptive questions replaces a long form. "
            "<bookmark mark='d'/> And learning platforms, where knowledge tracing and Elo ratings decide the next "
            "exercise."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def machines(self):
        head = heading(r"Measuring machines")
        rows = rows_of([
            (r"benchmarks for AI systems are tests: \ items of different difficulty and discrimination, \ given to "
             r"many test-takers", WHITE),
            (r"fit an item response model to models' answers, \ and the benchmark shrinks: \ a small set of "
             r"informative items ranks systems almost as well as thousands", MODEL),
            (r"items with low or negative discrimination are often mislabelled; \ an item everyone gets right tells "
             r"nothing", PERSON),
            (r"the same questions apply: \ is the item calibrated, \ does it function the same for every kind of "
             r"system, \ and is the scale stable as the systems change? \ (\emph{Statistics, Built} Part 64)", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "And one new kind of test-taker. <bookmark mark='a'/> Benchmarks for AI systems are tests: items of "
            "different difficulty and discrimination, given to many test-takers. <bookmark mark='b'/> Fit an item "
            "response model to the systems' answers, and a small set of informative items ranks systems almost as "
            "well as thousands. <bookmark mark='c'/> Items with low or negative discrimination are often mislabelled, "
            "and an item every system gets right tells you nothing. <bookmark mark='d'/> The same questions apply. Is "
            "the item calibrated? Does it function the same for every kind of system? And is the scale stable as the "
            "systems change? Statistics, Built takes this up in Part 64."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
