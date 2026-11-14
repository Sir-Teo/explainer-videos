from __future__ import annotations

import numpy as np

from videos.music.music22.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 12, r"Frontier: \ grammars from data", r"Can a program discover music's grammar?", extra=((2018, r"jazz harmony parsed"),),
                spoken="Frontier: grammars from data")
        self.induced()
        self.jazz()
        self.open()

    # ------------------------------------------------------------------
    def induced(self):
        d = load("learned")
        lat = d["bits"]["latent"]
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"induction: \ start with symbols that mean nothing, \ and let the data give them meaning", WHITE),
            (rf"chapter 7: \ 4 invented symbols, \ {lat['4']['test']:.2f} bits a chord; \ 12, \ {lat['12']['test']:.2f}", WHITE),
            (r"what the symbols learn need not be the theory's categories", TUNE),
            (r"the hard part: \ training gets stuck, \ and different starts find different grammars", WHITE),
            (r"neural networks now model harmony far better, \ with no symbols at all", GREY_A))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"grammars induced from data", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The frontier is to let the data write the grammar. <bookmark mark='a'/> Start with symbols that mean "
            "nothing and every rule allowed, and let training give them meaning. <bookmark mark='b'/> In chapter seven, "
            f"a grammar with four invented symbols reached {say(lat['4']['test'], 2)} bits a chord, and one with twelve "
            f"reached {say(lat['12']['test'], 2)}. <bookmark mark='c'/> And what the symbols learn need not be "
            "the theory's categories: even the six-rule grammar drifted in training, its symbol for the subdominant "
            "region ending up emitting the tonic chord more often than any other. "
            "<bookmark mark='d'/> The difficulty is the training itself: it gets stuck, and different starting points "
            "find different grammars. <bookmark mark='e'/> Meanwhile neural networks predict harmony far better than "
            "either, with no explicit symbols at all, which leaves the old question open in a new form: is the grammar "
            "in the music, or only in our description of it?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def jazz(self):
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"jazz standards: \ long chains of ii--V's, \ dominants of dominants", WHITE),
            (r"2018: \ Daniel Harasim and colleagues in Rohrmeier's group: \ a parser for jazz chord sequences", WHITE),
            (r"2020: \ Rohrmeier, \ \textit{The Syntax of Jazz Harmony}", WHITE),
            (r"annotated trees for jazz standards: \ a treebank, \ as linguists build for sentences", TUNE),
            (r"the deepest nesting yet measured in harmony is in jazz \ (Part 39)", GREY_A))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"where the trees are deepest", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The richest ground for grammars of harmony has turned out to be jazz. <bookmark mark='a'/> Jazz standards "
            "are built from long chains of two-five progressions, dominants of dominants of dominants, exactly the nesting "
            "a recursive grammar describes. <bookmark mark='b'/> In 2018 Daniel Harasim and colleagues in Rohrmeier's "
            "group built a grammar-based parser for jazz chord sequences, <bookmark mark='c'/> and in 2020 Rohrmeier set out the "
            "syntax of jazz harmony. <bookmark mark='d'/> The field is building annotated trees for standards, a treebank "
            "like those linguists build for sentences. <bookmark mark='e'/> Part 39 will take one of those trees apart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"open: \ which reductions do listeners actually make, \ and can they be measured?", WHITE),
            (r"open: \ does any grammar beat chord n-grams on long pieces, \ where depth could pay?", WHITE),
            (r"$\bigstar$ \ research problem: \ an experiment that measures a listener's reduction directly", TUNE))]).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"what is still open", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "And the open questions. <bookmark mark='a'/> Which reductions do listeners actually make, and can they be "
            "measured, for instance by asking which of two skeletons a passage sounds like, as chapter one did? "
            "<bookmark mark='b'/> Does any grammar beat chord pairs on long pieces, where depth has room to pay? "
            "<bookmark mark='c'/> And this part's research problem: design an experiment that measures a listener's "
            "reduction directly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bc", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
