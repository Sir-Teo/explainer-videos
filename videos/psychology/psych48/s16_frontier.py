from __future__ import annotations

from videos.psychology.psych48.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.open_questions()

    def card(self):
        card = chapter_card(15, r"Frontier: \ amortized inference and discovered models", r"Can the fitting, \ and "
                            r"the models, \ be learned?", lit=(), part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter fifteen. Frontier: amortized inference and discovered models."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def three(self):
        head = heading(r"Three frontiers")
        data = (
            (r"amortized inference", r"train a network once, \ on millions of simulations, \ to map data to "
                                     r"parameters; \ then fitting a new person is instant, \ even for models without a "
                                     r"likelihood", MODEL),
            (r"model discovery", r"search over programs, \ or let a network propose equations, \ for the model that "
                                 r"best predicts held-out people; \ then check it is still interpretable", PERSON),
            (r"a foundation model of behaviour", r"to count as a model of the mind it would need to predict new "
                                                 r"tasks, \ reproduce the classic effects for the right reasons, \ and "
                                                 r"be checked like any other", GOOD),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=16, width=4.0), wrapped_label(how, 8.4, 19, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, -0.2, 0])
        with self.voiceover(
            "Three frontiers. <bookmark mark='a'/> Amortized inference trains a network once, on millions of "
            "simulations, to map data to parameters. Then fitting a new person is instant, even for models without a "
            "likelihood. <bookmark mark='b'/> Model discovery searches over programs, or lets a network propose "
            "equations, for the model that best predicts held-out people, and then checks it's still interpretable. "
            "<bookmark mark='c'/> And a foundation model of behaviour. To count as a model of the mind, it would need "
            "to predict new tasks, reproduce the classic effects for the right reasons, and be checked like any "
            "other model."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"how many trials does a parameter need before it can be a trait?", WHITE),
            (r"can a model be both a strong predictor and an explanation?", MODEL),
            (r"how should model comparison work when every candidate is wrong?", AUTH),
            (r"what would a discovered model have to show to be believed?", PERSON),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        with self.voiceover(
            "Open questions. <bookmark mark='a'/> How many trials does a parameter need before it can be a trait? "
            "<bookmark mark='b'/> Can a model be both a strong predictor and an explanation? <bookmark mark='c'/> How "
            "should model comparison work when every candidate is wrong? <bookmark mark='d'/> And what would a "
            "discovered model have to show to be believed?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
