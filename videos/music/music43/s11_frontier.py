from __future__ import annotations

import numpy as np

from videos.music.music43.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ learning to perform", r"Can a machine learn expression from recordings?")
        self.data()
        self.models()
        self.accompany()
        self.problem()

    # ------------------------------------------------------------------
    def data(self):
        items = [
            (r"computer-monitored pianos record every key and pedal: \ onset, \ velocity, \ release", WHITE),
            (r"the MAESTRO dataset \ (Hawthorne and colleagues, \ 2019): \ about 200 hours of competition performances, \ aligned to the audio", WHITE),
            (r"aligned with scores \ (ASAP, \ 2020): \ every performed note matched to its written note", WHITE),
            (r"large aligned datasets expand reproducible expression research", TUNE),
            (r"the deviations from the exact are now data", GREY_A),
        ]
        rows_scene(self, r"performance as data", items,
                   "Seashore's deviations from the exact are now data. <bookmark mark='b'/> Computer-monitored pianos record "
                   "every key and pedal: when it went down, how fast, when it came up. <bookmark mark='c'/> The MAESTRO dataset of "
                   "2019 holds about two hundred hours of competition performances recorded this way, aligned to the audio. "
                   "<bookmark mark='d'/> Datasets such as ASAP match every performed note to its written note. "
                   "<bookmark mark='e'/> These datasets expand the scale and reproducibility of expression research beyond earlier large performance collections.",
                   marks="bcde")

    # ------------------------------------------------------------------
    def models(self):
        items = [
            (r"the Basis Mixer \ (Grachten, \ Cancino-Chac\'on and colleagues): \ score features in, \ timing and loudness out", WHITE),
            (r"VirtuosoNet \ (Jeong and colleagues, \ 2019): \ a hierarchical network over notes, \ beats and measures", WHITE),
            (r"models trained on audio generate performances directly, \ with no score at all \ (Part 66)", WHITE),
            (r"evaluation is the hard part: \ listening tests, \ and the distance to a human's version of the same piece", TUNE),
            (r"what they learn is the common part; \ whether they can learn an interpretation is open", GREY_A),
        ]
        rows_scene(self, r"learned models of expression", items,
                   "Models learn expression from these data. <bookmark mark='b'/> The Basis Mixer, from Maarten Grachten, Carlos "
                   "Cancino-Chacón and colleagues, maps features of the score to timing and loudness. <bookmark mark='c'/> "
                   "VirtuosoNet, in 2019, uses a hierarchical network over notes, beats and measures. <bookmark mark='d'/> Models "
                   "trained on audio now generate performances directly, with no score at all, Part 66's subject. "
                   "<bookmark mark='e'/> Evaluation is the hard part: listening tests, and the distance to a human's version of "
                   "the same piece. <bookmark mark='f'/> What they learn is the common part; whether a model can learn an "
                   "interpretation is open.", marks="bcdef")

    # ------------------------------------------------------------------
    def accompany(self):
        items = [
            (r"Dannenberg, \ and separately Vercoe \ (1984): \ the first computer accompanists, \ following a soloist through the score", WHITE),
            (r"Raphael's \textit{Music Plus One}: \ a probabilistic model of the soloist's timing, \ learned in rehearsal", WHITE),
            (r"the accompanist is chapter 6's partner, \ with an estimated alpha and a prediction of the next note", WHITE),
            (r"ensemble research now records eye gaze, \ breathing and body sway alongside onsets", TUNE),
            (r"leadership shows in movement before it shows in sound", GREY_A),
        ]
        rows_scene(self, r"machines that play along", items,
                   "Machines also play along. <bookmark mark='b'/> In 1984 Roger Dannenberg and, separately, Barry Vercoe built the first "
                   "computer accompanists, following a soloist through the score. <bookmark mark='c'/> Christopher Raphael's Music "
                   "Plus One models the soloist's timing probabilistically and learns it in rehearsal: <bookmark mark='d'/> "
                   "chapter six's partner, with an estimated alpha and a prediction of the next note. <bookmark mark='e'/> "
                   "Ensemble research now records eye gaze, breathing and body sway alongside the onsets, "
                   "<bookmark mark='f'/> and finds that leadership shows in movement before it shows in sound.", marks="bcdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"take many recordings of one piece by many pianists, \ aligned note by note to the score", WHITE),
            (r"split each tempo curve into what the score's structure predicts and what is left", WHITE),
            (r"ask listeners which recordings share an `interpretation', \ blind to the pianist", WHITE),
            (r"$\bigstar$ \ research problem: \ is an interpretation a measurable object, \ separable from the common part and the noise?", EAR),
            (r"an answer would let a model be asked for an interpretation, \ not only a plausible performance", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Take many recordings of one piece by many pianists, aligned note by "
            "note to the score. <bookmark mark='b'/> Split each tempo curve into what the score's structure predicts and what "
            "is left. <bookmark mark='c'/> Ask listeners which recordings share an interpretation, without telling them who "
            "is playing. <bookmark mark='d'/> Is an interpretation a measurable object, separable from the common part and "
            "from noise? <bookmark mark='e'/> An answer would let a model be asked for an interpretation, not only for a "
            "plausible performance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
