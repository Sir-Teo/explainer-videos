from __future__ import annotations

import numpy as np

from videos.music.music26.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 9, r"Frontier: \ style as learned statistics", r"Can a style be learned rather than described?")
        self.learned()
        self.problem()

    # ------------------------------------------------------------------
    def learned(self):
        items = [
            (r"Meyer \ (1989): \ style is a set of choices, \ constrained, \ and so probabilities", WHITE),
            (r"n-gram and neural models trained on a corpus \ (Parts 18 and 22) \ learn those probabilities", WHITE),
            (r"a model's surprise at each note is a measure of how typical it is of the style", WHITE),
            (r"composers then become distributions: \ where does Haydn surprise, \ and where does Mozart?", TUNE),
            (r"the limits: \ small corpora, \ symbolic scores only, \ and no idea of form or wit", GREY_A),
        ]
        rows_scene(self, r"style as probability", items,
                   "The frontier treats a style as statistics learned from music. <bookmark mark='b'/> The theorist Leonard "
                   "Meyer argued in 1989 that a style is a set of choices made within constraints, and so, in effect, a set "
                   "of probabilities. <bookmark mark='c'/> Models trained on a corpus, the n-grams of Part 18 and the "
                   "grammars of Part 22, or neural networks, learn those probabilities directly. <bookmark mark='d'/> A "
                   "model's surprise at each note then measures how typical that note is of the style, "
                   "<bookmark mark='e'/> and composers become distributions: where in a phrase does Haydn surprise, and "
                   "where Mozart? <bookmark mark='f'/> The limits are the ones this part ran into: small corpora, symbolic "
                   "scores without performance, and models that know nothing of form or wit.", marks="cdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"train a model on Haydn's quartets and one on Mozart's", WHITE),
            (r"score each held-out movement by both: \ which model is less surprised?", WHITE),
            (r"compare with chapter 7's features, \ and with a listener's judgement", WHITE),
            (r"$\bigstar$ \ research problem: \ where in a movement do the two styles differ most?", EAR),
            (r"the answer would say something about the music, \ not just about the classifier", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version of the frontier. <bookmark mark='a'/> Train one model on Haydn's quartets and another on "
            "Mozart's. <bookmark mark='b'/> Score each held-out movement by both, and ask which model it surprises less. "
            "<bookmark mark='c'/> Compare the result with chapter seven's features and with listeners' judgements. "
            "<bookmark mark='d'/> And then ask the real question: where in a movement do the two styles differ most, in "
            "the themes, the transitions, the cadences, the development? <bookmark mark='e'/> An answer to that would be a "
            "statement about the music, not merely about a classifier."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
