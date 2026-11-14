from __future__ import annotations

import numpy as np

from videos.music.music36.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ bells and tunings measured", r"What can acoustics tell archaeology?")
        self.bells()
        self.tunings()
        self.problem()
        self.ethics()

    # ------------------------------------------------------------------
    def bells(self):
        items = [
            (r"finite-element models of the Zeng bells reproduce their two notes from their shapes", WHITE),
            (r"thickness maps from scans show where founders scraped bronze to tune", WHITE),
            (r"replicas have been cast, \ and the originals played on rare occasions", WHITE),
            (r"open question: \ how were the bells designed before the physics existed?", TUNE),
            (r"von Falkenhausen's \textit{Suspended Music} \ (1993) \ reads the bells as history", GREY_A),
        ]
        rows_scene(self, r"the bells as data", items,
                   "The bells are now studied as acoustic objects. <bookmark mark='b'/> Finite-element models of their shapes "
                   "reproduce their two notes, <bookmark mark='c'/> and thickness maps show where founders scraped bronze away to "
                   "tune them. <bookmark mark='d'/> Replicas have been cast, and the originals played on rare occasions. "
                   "<bookmark mark='e'/> An open question is how they were designed, so precisely, long before the physics "
                   "existed. <bookmark mark='f'/> Lothar von Falkenhausen's Suspended Music reads the bells as history.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def tunings(self):
        items = [
            (r"measured gamelan tunings: \ how much do slendro and pelog vary, \ and along which dimensions?", WHITE),
            (r"do musicians hear a gamelan as slendro by its step sizes, \ its contour, \ or its repertoire?", WHITE),
            (r"Sethares's hypothesis: \ scales fit spectra; \ tests on measured instruments are mixed", WHITE),
            (r"cross-cultural studies find that musical training shapes which intervals sound `right'", TUNE),
            (r"Part 47 takes up universals and their limits", GREY_A),
        ]
        rows_scene(self, r"tunings as data", items,
                   "The tunings are studied the same way. <bookmark mark='b'/> How much do measured slendro and pelog tunings "
                   "vary, and along which dimensions? <bookmark mark='c'/> Do musicians recognise slendro by its step sizes, its "
                   "melodic contours, or its repertoire? <bookmark mark='d'/> Sethares's hypothesis, that scales fit spectra, "
                   "has had mixed tests on measured instruments. <bookmark mark='e'/> And cross-cultural studies find that musical "
                   "experience shapes which intervals sound right. <bookmark mark='f'/> Part 47 takes up universals and their "
                   "limits.", marks="cdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"measure the spectra and tunings of many gamelans, \ instrument by instrument", WHITE),
            (r"compute each set's dissonance minima from its own spectra", WHITE),
            (r"test whether the tuning sits nearer those minima than chance would place it", WHITE),
            (r"$\bigstar$ \ research problem: \ do gamelan tunings fit their instruments' spectra?", EAR),
            (r"the answer would say whether timbre shapes scales, \ or tradition does", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Measure the spectra and tunings of many gamelans, instrument by "
            "instrument. <bookmark mark='b'/> Compute each set's dissonance minima from its own spectra. "
            "<bookmark mark='c'/> Test whether the tuning sits nearer those minima than chance would place it. "
            "<bookmark mark='d'/> Do gamelan tunings fit their instruments' spectra? <bookmark mark='e'/> The answer would "
            "say whether timbre shapes scales, or tradition does."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ethics(self):
        items = [
            (r"archaeological instruments raise questions of display, \ playing and replication", WHITE),
            (r"recordings made in colonial times sit in European archives", WHITE),
            (r"communities ask for access, \ return, \ and a say in how music is used", WHITE),
            (r"research with instruments and traditions is research with people", TUNE),
            (r"Part 67 sets out how to do it well", GREY_A),
        ]
        rows_scene(self, r"heritage and ownership", items,
                   "Research here raises questions of ownership. <bookmark mark='b'/> Archaeological instruments raise questions of display, playing and replication. <bookmark mark='c'/> Many recordings of Asian music made in colonial times sit in European archives, <bookmark mark='d'/> and communities ask for access, for return, and for a say in how their music is used. <bookmark mark='e'/> Research with instruments and traditions is research with people. <bookmark mark='f'/> Part 67 sets out how to do it well.", marks="cdef")
