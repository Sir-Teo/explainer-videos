from __future__ import annotations

import numpy as np

from videos.music.music46.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ the predicting brain", r"Is all of music prediction?")
        self.predictive()
        self.culture()
        self.machines()
        self.problem()

    # ------------------------------------------------------------------
    def predictive(self):
        items = [
            (r"predictive processing: \ the brain continually predicts its input and learns from the errors", WHITE),
            (r"Koelsch, \ Vuust and Friston \ (2019): \ musical pleasure as the reduction of prediction error, \ weighted by its precision", WHITE),
            (r"precision is our uncertainty, \ inverted: \ errors count more when expectations were firm", WHITE),
            (r"it explains Cheung's interaction, \ and the build and drop", TUNE),
            (r"but a framework that explains everything must still be tested on what it predicts", GREY_A),
        ]
        rows_scene(self, r"predictive processing", items,
                   "The broadest current account is predictive processing. <bookmark mark='b'/> The brain continually predicts its "
                   "input and learns from the errors. <bookmark mark='c'/> Stefan Koelsch, Peter Vuust and Karl Friston argued in "
                   "2019 that musical pleasure comes from reducing prediction error, weighted by its precision, "
                   "<bookmark mark='d'/> where precision is our uncertainty, inverted: errors count more when expectations were "
                   "firm. <bookmark mark='e'/> It explains Cheung's interaction, and the build and the drop. <bookmark mark='f'/> "
                   "But a framework that explains everything must still be tested on what it predicts.", marks="bcdef")

    # ------------------------------------------------------------------
    def machines(self):
        items = [
            (r"large generative models of music are, \ underneath, \ next-token predictors: \ listeners of a kind", WHITE),
            (r"their surprise can be read note by note, \ as ours was, \ and compared with people's", WHITE),
            (r"early studies find large models predict expectedness ratings and brain responses well", WHITE),
            (r"they also learn styles from far more music than any person hears", TUNE),
            (r"Part 65 builds a small one", GREY_A),
        ]
        rows_scene(self, r"models as listeners", items,
                   "Machines have become listeners too. <bookmark mark='b'/> Large generative models of music are, underneath, "
                   "next-token predictors, <bookmark mark='c'/> so their surprise can be read note by note, as ours was, and "
                   "compared with people's. <bookmark mark='d'/> Early studies find that large models predict expectedness ratings "
                   "and brain responses well, <bookmark mark='e'/> though they learn from far more music than any person hears. "
                   "<bookmark mark='f'/> Part 65 builds a small one.", marks="bcdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"train listener models on different amounts of music, \ from a child's exposure to a model's", WHITE),
            (r"compare their surprise with listeners' ratings, \ brain responses and pleasure, \ moment by moment", WHITE),
            (r"find which model, \ and which amount of experience, \ predicts each person best", WHITE),
            (r"$\bigstar$ \ research problem: \ how much of musical pleasure is predicted by surprise and uncertainty alone?", EAR),
            (r"an answer would bound what expectation explains, \ and show what it leaves out", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Train listener models on different amounts of music, from a child's "
            "exposure to a large model's. <bookmark mark='b'/> Compare their surprise with listeners' ratings, brain responses "
            "and pleasure, moment by moment. <bookmark mark='c'/> Find which model, and which amount of experience, predicts "
            "each person best. <bookmark mark='d'/> How much of musical pleasure is predicted by surprise and uncertainty "
            "alone? <bookmark mark='e'/> An answer would bound what expectation explains, and show what it leaves out."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def culture(self):
        items = [
            (r"Krumhansl and colleagues \ (2000): \ Finnish listeners and North Sami yoiks; \ expectations followed what each group knew", WHITE),
            (r"listeners from other traditions bring other schemas: \ Part 34's ragas, \ Part 35's maqam", WHITE),
            (r"models trained on one culture predict that culture's listeners best \ (chapter 4)", WHITE),
            (r"expectation is universal; \ what is expected is learned", TUNE),
            (r"Part 47: \ what, \ if anything, \ every musical culture shares", GREY_A),
        ]
        rows_scene(self, r"expectation across cultures", items,
                   "Expectation also depends on where you grew up. <bookmark mark='b'/> In 2000 Carol Krumhansl and colleagues "
                   "studied North Sami yoiks with Finnish and Sami listeners, and expectations followed what each group knew. "
                   "<bookmark mark='c'/> Listeners from other traditions bring other schemas, Part 34's ragas and Part 35's maqam, "
                   "<bookmark mark='d'/> and models trained on one culture predict that culture's listeners best. "
                   "<bookmark mark='e'/> Expectation is universal; what is expected is learned. <bookmark mark='f'/> Part 47 asks "
                   "what, if anything, every musical culture shares.", marks="bcdef")
