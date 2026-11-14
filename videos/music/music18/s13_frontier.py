from __future__ import annotations

import numpy as np

from videos.music.music18.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 12, r"Frontier: \ harmony at scale", r"Is there one syntax of harmony, \ or many?", extra=((2011, r"a rock corpus and a grammar of harmony"),),
                spoken="Frontier: harmony at scale")
        self.corpora()
        self.brain()
        self.grammar()
        self.open()

    # ------------------------------------------------------------------
    def corpora(self):
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"2011: \ de Clercq and Temperley: \ 200 rock songs, \ every chord annotated", WHITE),
            (r"2011: \ the McGill Billboard corpus: \ hundreds of chart songs", WHITE),
            (r"2018: \ the Annotated Beethoven Corpus: \ all 16 string quartets, \ chord by chord", WHITE),
            (r"rock: \ IV and $\flat$VII freely, \ IV$\to$I among the commonest moves: \ the backward moves of chapter 2", TUNE),
            (r"Beethoven: \ closer to Bach's syntax, \ with more chromatic chords and longer chains", WHITE))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"harmony counted at scale", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "This part counted one composer's chorales. Recent work counts harmony at scale. "
            "<bookmark mark='a'/> In 2011 Trevor de Clercq and David Temperley annotated every chord of two hundred "
            "rock songs; <bookmark mark='b'/> the same year, the McGill Billboard corpus annotated hundreds of "
            "chart songs; <bookmark mark='c'/> in 2018 a team led by Martin Rohrmeier annotated all sixteen of "
            "Beethoven's string quartets. <bookmark mark='d'/> The syntax is not the same everywhere. In rock, four "
            "and flat seven are everywhere, and four going to one is among the commonest moves of all: the "
            "backward root motions that Bach used sparingly. <bookmark mark='e'/> Beethoven's quartets stay closer to "
            "Bach's forward syntax, with more chromatic chords."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def brain(self):
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"1998: \ Patel and others: \ an out-of-key chord and an ungrammatical word evoke the same late brain response \ (P600)", WHITE),
            (r"2000: \ Koelsch and others: \ a chord out of syntax evokes an early response, \ the ERAN, \ about 0.2 seconds after it", WHITE),
            (r"in listeners with no musical training", TUNE),
            (r"the strongest response: \ a Neapolitan sixth at the end of a cadence, \ where only a tonic should be", GREY_A))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"does the brain parse harmony?", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Is harmonic syntax only a description of what composers do, or something listeners process? "
            "<bookmark mark='a'/> In 1998 Aniruddh Patel and colleagues found that a chord from a distant key, in the "
            "middle of a progression, evokes the same late brain response, measured on the scalp, as a word that "
            "breaks the grammar of a sentence. <bookmark mark='b'/> In 2000 Stefan Koelsch and colleagues found an "
            "earlier response, about a fifth of a second after a chord that breaks the expected order, which they "
            "called the early right anterior negativity. <bookmark mark='c'/> It appears in listeners with no musical "
            "training at all: years of hearing the music around them are enough. <bookmark mark='d'/> It is strongest "
            "when a cadence that should end on the tonic ends on a chord that does not belong there."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def grammar(self):
        tree = VGroup(label(r"T", font_size=34, color=FUNC_C["T"]))
        kids = VGroup(label(r"T", font_size=30, color=FUNC_C["T"]), label(r"D", font_size=30, color=FUNC_C["D"]), label(r"T", font_size=30, color=FUNC_C["T"])).arrange(RIGHT, buff=1.4)
        kids.next_to(tree, DOWN, buff=0.8)
        sub = VGroup(label(r"S", font_size=26, color=FUNC_C["S"]), label(r"D", font_size=26, color=FUNC_C["D"])).arrange(RIGHT, buff=0.7).next_to(kids[1], DOWN, buff=0.8)
        leaves = VGroup(label(r"I", font_size=26), label(r"ii", font_size=26), label(r"V", font_size=26), label(r"I", font_size=26))
        for lf, anchor in zip(leaves, (kids[0], sub[0], sub[1], kids[2])):
            lf.next_to(anchor, DOWN, buff=0.8)
        lines = VGroup(*[Line(tree.get_bottom(), k.get_top(), buff=0.1, color=GREY_B) for k in kids],
                       *[Line(kids[1].get_bottom(), s_.get_top(), buff=0.1, color=GREY_B) for s_ in sub],
                       Line(kids[0].get_bottom(), leaves[0].get_top(), buff=0.1, color=GREY_B), Line(sub[0].get_bottom(), leaves[1].get_top(), buff=0.1, color=GREY_B),
                       Line(sub[1].get_bottom(), leaves[2].get_top(), buff=0.1, color=GREY_B), Line(kids[2].get_bottom(), leaves[3].get_top(), buff=0.1, color=GREY_B))
        g = VGroup(tree, kids, sub, leaves, lines).move_to(LEFT * 3.4 + DOWN * 0.2)
        side = VGroup(label(r"Rohrmeier, \ 2011: \ a grammar of harmony, \ like a grammar of sentences", font_size=24, color=WHITE),
                      label(r"a chord can prepare one far away, \ not only the next", font_size=24, color=WHITE),
                      label(r"a table of pairs \ (this part's model) \ cannot see that", font_size=24, color=GREY_A),
                      label(r"schemata: \ Gjerdingen and Bourne \ (2015): \ a construction grammar of stock phrases", font_size=22, color=TUNE)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 6.4))
        side.move_to(RIGHT * 3.5 + DOWN * 0.1)
        with self.voiceover(
            "Is harmony a chain, each chord depending on the last, or a tree? <bookmark mark='a'/> Martin Rohrmeier "
            "proposed in 2011 a generative grammar of harmony, like the grammars linguists write for sentences: a "
            "phrase is a tonic that is prolonged, and a dominant inside it is prepared by a subdominant, which can "
            "itself be prepared, and so on. <bookmark mark='b'/> In a tree, a chord can depend on one far away, "
            "which a table of pairs, like this part's, cannot represent. <bookmark mark='c'/> Gjerdingen's schemata "
            "suggest a third picture: a construction grammar, in which the units are not single chords but stock "
            "phrases, learned whole."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open(self):
        star = VGroup(label(r"$\bigstar$ \ open", font_size=30, color=LIMIT),
                      label(r"chains, \ trees, \ or stock phrases?", font_size=30, color=WHITE),
                      label(r"which describes what listeners actually expect, \ and what they learn from hearing music?", font_size=24, color=GREY_A),
                      label(r"and can a machine discover the schemata from a corpus, \ without being told them?", font_size=26, color=TUNE)).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        with self.voiceover(
            "What remains open is which picture is right, for listeners rather than analysts. Do people hear "
            "harmony as a chain of pairs, as a tree, or as a stock of learned phrases, and does it depend on the "
            "music they grew up with? And could a machine, given a large corpus and no theory, discover the "
            "galant schemata for itself, as the Neapolitan boys learned them, from examples alone?"
        ):
            self.play(LaggedStart(*[FadeIn(x) for x in star], lag_ratio=0.5), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()
