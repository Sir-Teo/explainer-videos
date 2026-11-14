from __future__ import annotations

import numpy as np

from videos.music.music17.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 12, r"Frontier: \ machines that write chorales", r"Who writes the best Bach that is not Bach, \ and how would we know?",
                extra=((2017, r"DeepBach and Coconet"),), spoken="Frontier: machines that write chorales")
        self.history()
        self.judging()
        self.open()

    # ------------------------------------------------------------------
    def history(self):
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"1988: \ Ebcio\u{g}lu's CHORAL: \ about 350 rules, \ written by hand", WHITE),
            (r"2005: \ Allan and Williams: \ a hidden Markov model of chords under a tune \ (this part's search, \ learned)", WHITE),
            (r"2016: \ BachBot \ (Liang): \ a recurrent network trained on the chorales", WHITE),
            (r"2017: \ DeepBach \ (Hadjeres, \ Pachet and Nielsen): \ every voice resampled, \ one note at a time", WHITE),
            (r"2017: \ Coconet \ (Huang and others): \ fill in a score with holes; \ 2019, \ Google's Bach Doodle", WHITE),
            (r"the chorales: \ a standard test set for machines that write music", TUNE))]).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(DOWN * 0.1)
        rows_.scale_to_fit_width(min(rows_.width, 12.8))
        head = label(r"Bach's chorales as a benchmark", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The chorales became the first benchmark of music written by machine. <bookmark mark='a'/> In "
            "1988 Kemal Ebcioglu's program harmonized them with about three hundred and fifty rules, "
            "written by hand. <bookmark mark='b'/> In 2005 Moray Allan and Christopher Williams learned "
            "the harmonizer instead, as a hidden Markov model of chords under a tune, solved by the same "
            "Viterbi search as this part's. <bookmark mark='c'/> Then neural networks: BachBot in 2016, "
            "<bookmark mark='d'/> DeepBach in 2017, which rewrites one note of one voice at a time, again "
            "and again, until all four voices agree with what it has learned, <bookmark mark='e'/> and "
            "Coconet, which learned to fill in a score with holes in it, and in 2019 harmonized tunes "
            "typed in by millions of people in Google's Bach Doodle. <bookmark mark='f'/> These models "
            "write the moving inner voices this part's search could not."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcdef", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def judging(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"likelihood: \ how probable the model finds Bach's own notes \ (needs no listener)", WHITE),
            (r"rules: \ count the faults \ (chapter 5: \ Bach himself is not perfect)", WHITE),
            (r"agreement: \ the same chord as Bach \ (chapter 1: \ Bach disagrees with Bach)", WHITE),
            (r"listening tests: \ can people tell it from Bach?", TUNE))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"how to judge a chorale that is not Bach's", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "And how should they be judged? This part has tried three ways, and each has a flaw. "
            "<bookmark mark='a'/> A model's likelihood measures how well it predicts Bach's notes, but a "
            "model can predict well and still write dull music. <bookmark mark='b'/> Counting faults "
            "rewards caution, and Bach himself has faults. <bookmark mark='c'/> Agreement with Bach's "
            "chords punishes every other good answer. <bookmark mark='d'/> So the strongest claims rest "
            "on listening tests: play people real and generated chorales and ask which is Bach. In the "
            "tests reported by BachBot's and DeepBach's authors, many listeners, including trained "
            "musicians, often could not tell. But who listens, to how much, and what they are asked, "
            "changes the answer."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open(self):
        star = VGroup(label(r"$\bigstar$ \ open", font_size=30, color=LIMIT),
                      label(r"what is style, \ in numbers?", font_size=30, color=WHITE),
                      label(r"a measure that a teacher, \ a listener and Bach's own variety would all agree with", font_size=24, color=GREY_A),
                      label(r"and is a style a set of rules, \ a probability, \ or something neither captures?", font_size=26, color=TUNE)).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        with self.voiceover(
            "What remains open is a definition. When we say a harmonization is in Bach's style, what is "
            "being claimed, and how should it be measured, so that a teacher's judgement, a listener's ear, "
            "and Bach's own habit of setting one tune many ways all come out right? Whether a style is best "
            "described as rules, as probabilities, or as something neither captures, is still argued."
        ):
            self.play(LaggedStart(*[FadeIn(x) for x in star], lag_ratio=0.5), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()
