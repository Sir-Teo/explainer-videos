from __future__ import annotations

import numpy as np

from videos.music.music30.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 9, r"Frontier: \ composing with machines, \ listening to data", r"What can sound tell us that a graph cannot?")
        self.cac()
        self.sonification()
        self.ai()
        self.problem()

    # ------------------------------------------------------------------
    def cac(self):
        items = [
            (r"computer-assisted composition: \ OpenMusic, \ Max, \ SuperCollider: \ processes, \ constraints, \ spectra in code", WHITE),
            (r"the composer writes the process; \ the machine computes the notes, \ the composer chooses", WHITE),
            (r"live coding: \ music written and changed as code during a performance", WHITE),
            (r"the question that remains: \ which choices are the composer's?", TUNE),
            (r"Part 65 returns with machines that learn from music", GREY_A),
        ]
        rows_scene(self, r"composing with machines", items,
                   "The frontier has two sides. The first is composing with machines. <bookmark mark='c'/> Composers now write "
                   "processes, constraints and spectral analyses directly in code, in environments like OpenMusic, Max and "
                   "SuperCollider, <bookmark mark='d'/> and the machine computes the notes from which the composer chooses. "
                   "<bookmark mark='e'/> In live coding, the code itself is written and changed during the performance. "
                   "<bookmark mark='f'/> Which choices are then the composer's is a real question, which Part 65 takes up with "
                   "machines that learn.", marks="cdef")

    # ------------------------------------------------------------------
    def sonification(self):
        items = [
            (r"sonification: \ data turned into sound so that the ear can find patterns", WHITE),
            (r"the Geiger counter's clicks: \ a Poisson process you can hear \ (chapter four)", WHITE),
            (r"heartbeats, \ seismic records, \ gravitational waves sped up into the audible range", WHITE),
            (r"the ear is good at rhythm, \ periodicity and change: \ things a static graph can hide", TUNE),
            (r"the evidence for when sonification helps is still thin", EAR),
        ]
        rows_scene(self, r"listening to data", items,
                   "The second side turns the studio around: sound as a way of reading data. <bookmark mark='b'/> In sonification, data become sound so that the ear can find their patterns. <bookmark mark='c'/> A Geiger counter can approximate a Poisson counting process under steady conditions; detector dead time and changing sources affect it, made audible. <bookmark mark='d'/> Heartbeats, earthquake records and gravitational waves have been sped up into the audible range. <bookmark mark='e'/> The ear is very good at rhythm, periodicity and change, things a static graph can hide. <bookmark mark='f'/> But careful evidence of when sonification really helps, compared with a picture, is still thin.", marks="cdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"take series with a known hidden pattern: \ a weak periodicity, \ a change of rate, \ a rare burst", WHITE),
            (r"present them as a plot, \ as a sonification, \ and as both, \ to many listeners", WHITE),
            (r"measure how often and how fast each pattern is found, \ against chance", WHITE),
            (r"$\bigstar$ \ research problem: \ for which patterns does listening beat looking?", EAR),
            (r"Poisson clouds and phasing, \ from this part, \ are natural test cases", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Make data series with a known hidden pattern: a weak periodicity, a "
            "change of rate, a rare burst. <bookmark mark='b'/> Present them to many people as a plot, as sound, and as both. "
            "<bookmark mark='c'/> Measure how often and how quickly each pattern is found, against chance. "
            "<bookmark mark='d'/> For which patterns does listening beat looking? <bookmark mark='e'/> This part's Poisson "
            "clouds and drifting loops are natural test cases: a change of density, a slow change of phase."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ai(self):
        items = [
            (r"neural networks now generate audio directly, \ sample by sample or from learned codes", WHITE),
            (r"timbre transfer: \ one instrument's sound given another's performance", WHITE),
            (r"musique concrète's question returns: \ what is a sound object when a machine invents it?", WHITE),
            (r"composers use these systems as new studios", TUNE),
            (r"Part 66 builds generative audio and asks what it learned", GREY_A),
        ]
        rows_scene(self, r"learned sound", items,
                   "And the studio itself is changing again. <bookmark mark='b'/> Neural networks now generate audio directly, sample by sample or from learned codes, <bookmark mark='c'/> and can transfer timbre, giving one instrument's sound another's performance. <bookmark mark='d'/> Schaeffer's question returns: what is a sound object when a machine invents it? <bookmark mark='e'/> Composers already use these systems as new studios. <bookmark mark='f'/> Part 66 builds generative audio, and asks what it has learned.", marks="cdef")
