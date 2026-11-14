from __future__ import annotations

import numpy as np

from videos.music.music33.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ tilings and open problems", r"What is still unknown?", extra=((1974, r"Fuglede's conjecture"),))
        self.fuglede()
        self.coven()
        self.open()
        self.problem()
        self.field()

    # ------------------------------------------------------------------
    def fuglede(self):
        items = [
            (r"Fuglede \ (1974): \ a shape tiles space by translation exactly when it has an orthogonal basis of exponentials", WHITE),
            (r"`spectral' \ = \ a Fourier series exists on it; \ `tiles' \ = \ copies fill space", WHITE),
            (r"Tao \ (2004): \ false in 5 dimensions and more; \ later counterexamples down to 3", WHITE),
            (r"in 1 and 2 dimensions, \ and for cyclic groups, \ it is still open in general", TUNE),
            (r"a rhythmic canon is a tiling of a cycle: \ the conjecture asks the same of canons", GREY_A),
        ]
        rows_scene(self, r"the spectral conjecture", items,
                   "The canons lead to an open problem. <bookmark mark='b'/> In 1974 Bent Fuglede conjectured that a shape tiles "
                   "space by translation exactly when it carries a basis of pure frequencies, an exact Fourier series. "
                   "<bookmark mark='c'/> Spectral means the Fourier series exists; tiling means copies fill space. "
                   "<bookmark mark='d'/> Terence Tao showed in 2004 that it is false in five dimensions and more, and later work "
                   "brought counterexamples down to three. <bookmark mark='e'/> In one and two dimensions, and for cyclic groups, "
                   "it is still open in general. <bookmark mark='f'/> A rhythmic canon is a tiling of a cycle, so the conjecture "
                   "asks the same question of canons.", marks="cdef")

    # ------------------------------------------------------------------
    def coven(self):
        items = [
            (r"Coven and Meyerowitz \ (1999): \ two conditions on a rhythm's polynomial, \ T1 and T2", WHITE),
            (r"a rhythm satisfying both tiles; \ every tiling rhythm satisfies T1", WHITE),
            (r"whether every tiling rhythm satisfies T2 is open", TUNE),
            (r"Amiot and others test it on Vuza canons by computer: \ no counterexample yet", WHITE),
            (r"the canon of chapter 5 passes: \ one more data point", GREY_A),
        ]
        rows_scene(self, r"when does a rhythm tile?", items,
                   "There is a sharper question. <bookmark mark='b'/> In 1999 Ethan Coven and Aaron Meyerowitz gave two "
                   "conditions on a rhythm, written in terms of its polynomial, called T1 and T2. <bookmark mark='c'/> A rhythm "
                   "satisfying both tiles, and every rhythm that tiles satisfies T1. <bookmark mark='d'/> Whether every tiling "
                   "rhythm also satisfies T2 is open. <bookmark mark='e'/> Emmanuel Amiot and others have tested it on large "
                   "families of Vuza canons by computer, without finding a counterexample. <bookmark mark='f'/> The canon of "
                   "chapter five is one more data point.", marks="cdef")

    # ------------------------------------------------------------------
    def open(self):
        items = [
            (r"classify all Vuza canons of a given period \ (done for 72, \ 108, \ 120 ...; \ not in general)", WHITE),
            (r"why do so many traditional timelines sit near maximal evenness? \ culture, \ motor control, \ or memory?", WHITE),
            (r"which temperaments make good harmony for which timbres?", WHITE),
            (r"de Bruijn rhythms, \ oddity, \ homometry: \ enumerations with no formula yet", TUNE),
            (r"Part 67: \ how to do research in music, \ including in its mathematics", GREY_A),
        ]
        rows_scene(self, r"other open problems", items,
                   "Other questions are open too. <bookmark mark='b'/> Classifying all Vuza canons of a given period is done "
                   "for the smallest periods, not in general. <bookmark mark='c'/> Why so many traditional timelines sit near "
                   "maximal evenness, whether culture, motor control or memory, is not settled. <bookmark mark='d'/> Which "
                   "temperaments make good harmony for which timbres is an open design question. <bookmark mark='e'/> And many "
                   "of this part's counts have no formula, only enumeration. <bookmark mark='f'/> Part 67 is about doing research "
                   "in music, including its mathematics.", marks="cdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"collect timelines from many traditions, \ with their cultural sources documented", WHITE),
            (r"measure each one's distance from maximal evenness, \ against random rhythms of the same size", WHITE),
            (r"test whether evenness predicts how easily listeners tap along or remember the pattern", WHITE),
            (r"$\bigstar$ \ research problem: \ is maximal evenness a cultural choice or a cognitive constraint?", EAR),
            (r"the answer would say what the mathematics explains about music, \ and what it only describes", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Collect timelines from many traditions, with their sources documented. "
            "<bookmark mark='b'/> Measure each one's distance from maximal evenness, against random rhythms of the same size. "
            "<bookmark mark='c'/> Test whether evenness predicts how easily listeners tap along or remember the pattern. "
            "<bookmark mark='d'/> Is maximal evenness a cultural choice, or a constraint of the mind? <bookmark mark='e'/> "
            "The answer would say what the mathematics explains about music, and what it only describes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def field(self):
        items = [
            (r"the Society for Mathematics and Computation in Music \ (2006), \ and its journal", WHITE),
            (r"Mazzola's \textit{Topos of Music} \ (2002); \ Lewin; \ Tymoczko; \ Toussaint; \ Amiot", WHITE),
            (r"computation made it possible: \ enumerations and searches no one could do by hand", WHITE),
            (r"the best results explain something a musician already hears", TUNE),
            (r"this part's verified claims live in its tests, \ as every part's do", GREY_A),
        ]
        rows_scene(self, r"a field of its own", items,
                   "Mathematical music theory is now a field of its own. <bookmark mark='b'/> It has a society, founded in 2006, and its own journal. <bookmark mark='c'/> Its books include Guerino Mazzola's Topos of Music and the work of Lewin, Tymoczko, Toussaint and Amiot. <bookmark mark='d'/> Computation made much of it possible: enumerations and searches no one could do by hand. <bookmark mark='e'/> The best of its results explain something a musician already hears. <bookmark mark='f'/> This part's claims, like every part's, are checked in its tests.", marks="cdef")
