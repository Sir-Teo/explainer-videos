from __future__ import annotations

from videos.music.music58.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ neural codecs and learned metrics", r"Can a machine judge what a listener will hear?")
        self.limits()
        self.metrics()
        self.problem()

    # ------------------------------------------------------------------
    def limits(self):
        items = [
            (r"a neural decoder does not add noise; \ when it lacks bits it invents plausible detail", WHITE),
            (r"invented detail can fool a listening test: \ it sounds real, \ but it is not what was played", WHITE),
            (r"they fail differently on music they were not trained on: \ unusual instruments, \ tunings, \ voices", WHITE),
            (r"and they cost far more computation than an MDCT coder, \ though less every year", WHITE),
            (r"fidelity and plausibility have come apart; \ the tests of Chapter 8 measure only the second", TUNE),
        ]
        rows_scene(self, r"what neural codecs change", items,
                   "Neural codecs change what a codec error is. <bookmark mark='b'/> Neural codec errors can include noise, altered detail and plausible reconstruction artifacts; when it "
                   "lacks bits it invents plausible detail. <bookmark mark='c'/> Invented detail can pass a listening test, because "
                   "it sounds real, though it is not what was played. <bookmark mark='d'/> These codecs fail differently on music "
                   "unlike what they were trained on: unusual instruments, tunings and voices. <bookmark mark='e'/> They cost far "
                   "more computation than an MDCT coder, though less every year. <bookmark mark='f'/> Fidelity and plausibility have "
                   "come apart, and reference-based tests assess fidelity as well as quality, while plausibility without a reference is a different task.", marks="bcdef")

    # ------------------------------------------------------------------
    def metrics(self):
        items = [
            (r"listening tests are slow and costly; \ coders are tuned by objective measures between tests", WHITE),
            (r"PEAQ \ (ITU-R BS.1387, \ 1998): \ an ear model compares the coded signal with the reference, \ and predicts the test score", WHITE),
            (r"ViSQOL and others: \ similarity of spectro-temporal patterns, \ fitted to listening data", WHITE),
            (r"learned metrics: \ networks trained on thousands of ratings; \ excellent on codecs like those they saw, \ unreliable on new kinds of error", WHITE),
            (r"optimizing a metric can exploit its blind spots, so independent evaluation is needed", TUNE),
        ]
        rows_scene(self, r"learned metrics", items,
                   "And the measures. <bookmark mark='b'/> Listening tests are slow and costly, so coders are tuned by objective "
                   "measures between them. <bookmark mark='c'/> PEAQ, the ITU's BS.1387 of 1998, runs an ear model over the coded "
                   "signal and the reference and predicts the test score. <bookmark mark='d'/> ViSQOL and others compare "
                   "spectro-temporal patterns, fitted to listening data. <bookmark mark='e'/> Learned metrics are networks trained "
                   "on thousands of ratings: excellent on errors like those they saw, unreliable on new kinds. "
                   "<bookmark mark='f'/> And optimizing a metric can exploit its blind spots, so independent evaluation is needed.", marks="bcdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"collect MUSHRA ratings for classical and neural codecs on varied music, \ including music unlike any training set", WHITE),
            (r"train metrics on some codecs, \ and test them on codecs they have never seen", WHITE),
            (r"measure how well each predicts the listeners, \ with confidence intervals, \ codec by codec", WHITE),
            (r"$\bigstar$ \ research problem: \ can a learned metric predict listeners' ratings for a kind of codec that did not exist when it was trained?", EAR),
            (r"an answer would decide whether codecs can safely be trained against metrics", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on. <bookmark mark='a'/> Collect MUSHRA ratings for classical and neural codecs on "
            "varied music, including music unlike any training set. <bookmark mark='b'/> Train metrics on some codecs, and test "
            "them on codecs they have never seen. <bookmark mark='c'/> Measure how well each predicts the listeners, with "
            "confidence intervals, codec by codec. <bookmark mark='d'/> The question: can a learned metric predict listeners' "
            "ratings for a kind of codec that did not exist when it was trained? <bookmark mark='e'/> An answer would decide "
            "whether codecs can safely be trained against metrics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
