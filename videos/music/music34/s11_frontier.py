from __future__ import annotations

import numpy as np

from videos.music.music34.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ computing raga", r"Can a machine recognise a raga?")
        self.compmusic()
        self.limits()
        self.problem()
        self.generation()

    # ------------------------------------------------------------------
    def compmusic(self):
        items = [
            (r"CompMusic \ (2011--2017, \ Xavier Serra and colleagues): \ large corpora of Hindustani and Carnatic recordings", WHITE),
            (r"pitch tracked from recordings; \ the tonic Sa found automatically from the drone", WHITE),
            (r"raga recognised from pitch histograms and phrase patterns, \ well above chance among dozens of ragas", WHITE),
            (r"tala tracked, \ sam found, \ tabla strokes transcribed", TUNE),
            (r"the tools are Part 61's and 62's, \ tuned to this music", GREY_A),
        ]
        rows_scene(self, r"what computers can do", items,
                   "Computers have studied this music closely. <bookmark mark='b'/> The CompMusic project, led by Xavier Serra "
                   "from 2011, built large collections of Hindustani and Carnatic recordings. <bookmark mark='c'/> It tracked "
                   "pitch from the recordings and found the tonic automatically from the drone. <bookmark mark='d'/> It "
                   "recognised ragas from pitch histograms and characteristic phrases, well above chance among dozens of ragas. "
                   "<bookmark mark='e'/> And it tracked tala, found sam, and transcribed tabla strokes. <bookmark mark='f'/> The "
                   "tools are those of Parts 61 and 62, tuned to this music.", marks="cdef")

    # ------------------------------------------------------------------
    def limits(self):
        items = [
            (r"recognition is not understanding: \ a histogram cannot say why a phrase is beautiful", WHITE),
            (r"intonation studies show variation: \ by singer, \ by raga, \ by phrase, \ by decade", WHITE),
            (r"datasets favour famous performers and recorded eras", WHITE),
            (r"the most useful studies were built with musicians, \ not only about them", TUNE),
            (r"a model of a living tradition must be checked by its practitioners", GREY_A),
        ]
        rows_scene(self, r"what they cannot", items,
                   "There are limits. <bookmark mark='b'/> Recognising a raga is not understanding it: a histogram cannot say "
                   "why a phrase is beautiful. <bookmark mark='c'/> Intonation studies show variation by singer, raga, phrase and "
                   "decade. <bookmark mark='d'/> Datasets favour famous performers and the recorded era. <bookmark mark='e'/> The "
                   "most useful studies were built with musicians, not only about them. <bookmark mark='f'/> A model of a living "
                   "tradition has to be checked by the people who practise it.", marks="cdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"collect performances of ragas that share a scale, \ with musicians' annotations of their phrases", WHITE),
            (r"model each raga by its phrases and gamakas, \ not only its pitch histogram", WHITE),
            (r"ask trained listeners which features they use to tell the ragas apart, \ and compare", WHITE),
            (r"$\bigstar$ \ research problem: \ what do listeners attend to when they recognise a raga?", EAR),
            (r"the answer would show how much of a raga lives in its notes, \ and how much in their motion", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Collect performances of ragas that share a scale, with musicians' "
            "annotations of their phrases. <bookmark mark='b'/> Model each raga by its phrases and gamakas, not only its "
            "pitch histogram. <bookmark mark='c'/> Ask trained listeners which features they use to tell the ragas apart, and "
            "compare. <bookmark mark='d'/> What do listeners attend to when they recognise a raga? <bookmark mark='e'/> The "
            "answer would show how much of a raga lives in its notes, and how much in their motion."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def generation(self):
        items = [
            (r"generative models can now produce raga-like melodies from recordings", WHITE),
            (r"they learn the scale and common phrases quickly; \ gamaka and long-form shape, \ less well", WHITE),
            (r"questions of consent and credit arise when a living tradition is modelled", WHITE),
            (r"the tradition's own teachers are the right judges of whether a model plays a raga", TUNE),
            (r"Part 65 builds machines that compose; \ Part 66, \ machines that make sound", GREY_A),
        ]
        rows_scene(self, r"machines that play ragas", items,
                   "Machines now try to play this music. <bookmark mark='b'/> Generative models trained on recordings can produce raga-like melodies. <bookmark mark='c'/> They pick up the scale and common phrases quickly; the gamakas and the long-form shape of a performance, less well. <bookmark mark='d'/> Questions of consent and credit arise when a living tradition is modelled from its musicians' recordings. <bookmark mark='e'/> And the tradition's own teachers are the right judges of whether a model is playing a raga at all. <bookmark mark='f'/> Part 65 builds machines that compose, and Part 66 machines that make sound.", marks="cdef")
