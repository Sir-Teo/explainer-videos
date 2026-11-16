from __future__ import annotations

import numpy as np

from videos.music.music29.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ homometry and perception", r"What does a crystal have to do with a chord?")
        self.crystals()
        self.dft()
        self.others()
        self.problem()

    # ------------------------------------------------------------------
    def crystals(self):
        items = [
            (r"X-ray crystallography measures the distances between atoms, \ not their positions", WHITE),
            (r"Patterson \ (1944): \ two different arrangements can give the same distances: \ `homometric' sets", WHITE),
            (r"Z-related sets: homometric, distinct TnI classes\\sets within one class are homometric too", TUNE),
            (r"the hexachord theorem is a theorem about crystals: \ a six-note set and its complement are homometric", WHITE),
            (r"music theory and physics found the same fact from different ends", GREY_A),
        ]
        rows_scene(self, r"a fact from crystallography", items,
                   "The hexachord theorem has a surprising relative. <bookmark mark='b'/> In X-ray crystallography the "
                   "diffraction pattern reveals the distances between atoms, not their positions. <bookmark mark='c'/> In 1944 "
                   "the crystallographer Lindo Patterson showed that two different arrangements can have exactly the same "
                   "distances; such sets are called homometric. <bookmark mark='d'/> On a circle of twelve points, homometric "
                   "sets are exactly the Z-related sets of chapter four, <bookmark mark='e'/> and the hexachord theorem is a "
                   "statement physicists also know: on this finite cyclic twelve-point universe, a six-note subset and its complement are homometric. "
                   "<bookmark mark='f'/> Music theory and physics found the same fact from different ends.", marks="cdef")

    # ------------------------------------------------------------------
    def dft(self):
        rows_ = text_rows([
            (r"treat a set as twelve 0s and 1s, \ and take its discrete Fourier transform", WHITE),
            (r"the interval vector is determined by the set's size and the magnitudes of its six Fourier coefficients", WHITE),
            (r"homometric sets: \ the same magnitudes, \ different phases", WHITE),
            (r"Lewin \ (1959), \ Quinn \ (2006), \ Amiot \ (2016): \ a whole theory of harmony from these magnitudes", TUNE),
            (r"the same mathematics as Part 3's spectrum, \ on a circle of twelve notes", GREY_A),
        ], font_size=24)
        head = label(r"the same fact, \ in Fourier's language", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The modern way to say it uses the Fourier transform from Part 3. <bookmark mark='a'/> Write a set as twelve "
            "zeros and ones round the circle and take its discrete Fourier transform. <bookmark mark='b'/> The interval "
            "vector turns out to be determined by the set's size and the magnitudes of its six Fourier coefficients. "
            "<bookmark mark='c'/> Homometric sets have the same magnitudes and different phases. <bookmark mark='d'/> "
            "David Lewin noticed this in 1959; Ian Quinn and Emmanuel Amiot have since built a theory of harmonic quality on "
            "those magnitudes. <bookmark mark='e'/> It is Part 3's spectrum, applied to a circle of twelve notes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"play listeners pairs of chords: \ Z-related, \ the same class, \ or unrelated", WHITE),
            (r"measure judged similarity, \ and compare with the Fourier magnitudes and with the interval vector", WHITE),
            (r"control for register, \ spacing and loudness, \ which the theory ignores", WHITE),
            (r"$\bigstar$ \ research problem: \ do listeners hear interval content, \ or only surface features?", EAR),
            (r"an answer would say how much of set theory is perception and how much is bookkeeping", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version of the frontier. <bookmark mark='a'/> Play listeners pairs of chords that are Z-related, in "
            "the same class, or unrelated. <bookmark mark='b'/> Measure how similar they judge them, and compare with the "
            "Fourier magnitudes and with the interval vectors. <bookmark mark='c'/> Control for register, spacing and "
            "loudness, which the theory ignores. <bookmark mark='d'/> Do listeners hear interval content at all, or only "
            "surface features? <bookmark mark='e'/> The answer would say how much of set theory is perception, and how much "
            "is bookkeeping."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def others(self):
        items = [
            (r"Elisabeth Lutyens in Britain: \ an early serialist, \ nicknamed `Twelve-Tone Lizzie'", WHITE),
            (r"Ruth Crawford Seeger's String Quartet \ (1931): \ her own rules of `dissonant counterpoint'", WHITE),
            (r"Josef Matthias Hauer: \ a twelve-tone system of his own, \ before and beside Schoenberg's", WHITE),
            (r"Schoenberg's pupils in Los Angeles included John Cage", TUNE),
            (r"the method had more than one inventor, \ and many voices", GREY_A),
        ]
        rows_scene(self, r"others in the room", items,
                   "The usual story has one inventor. It had several. <bookmark mark='b'/> In Britain, Elisabeth Lutyens wrote serial music early, and was nicknamed Twelve-Tone Lizzie. <bookmark mark='c'/> In America, Ruth Crawford Seeger's String Quartet of 1931 followed her own rules of dissonant counterpoint. <bookmark mark='d'/> In Vienna, Josef Matthias Hauer had worked out a twelve-tone system of his own, before and beside Schoenberg's. <bookmark mark='e'/> And in Los Angeles, where Schoenberg taught after fleeing Germany in 1933, his pupils included John Cage. <bookmark mark='f'/> The method had more than one inventor, and many voices.", marks="cdef")
