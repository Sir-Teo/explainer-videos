from __future__ import annotations

import numpy as np

from videos.music.music35.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ measuring makam", r"What do pitch histograms say about theory?")
        self.compute()
        self.standards()
        self.problem()
        self.fair()
        self.ai()

    # ------------------------------------------------------------------
    def compute(self):
        items = [
            (r"computational makam analysis \ (Bozkurt and colleagues, \ 2000s--2010s; \ CompMusic)", WHITE),
            (r"pitch tracked from recordings; \ the tonic found; \ pitch histograms per makam", WHITE),
            (r"histogram peaks compared with theory's pitches: \ several notes differ by a comma or more", WHITE),
            (r"makam recognised automatically from histograms, \ well above chance", TUNE),
            (r"Part 34's raga studies used the same tools", GREY_A),
        ]
        rows_scene(self, r"measuring makam", items,
                   "Computers have measured this music too. <bookmark mark='b'/> Barış Bozkurt and colleagues, and later the "
                   "CompMusic project, <bookmark mark='c'/> tracked pitch in recordings, found the tonic and drew pitch "
                   "histograms for each makam. <bookmark mark='d'/> Comparing histogram peaks with theory's pitches, they found "
                   "several notes differing by a comma or more. <bookmark mark='e'/> They also recognised makams automatically "
                   "from the histograms, well above chance. <bookmark mark='f'/> Part 34's raga studies used the same tools.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def standards(self):
        items = [
            (r"standardization has defenders: \ notation, \ teaching, \ ensembles, \ software", WHITE),
            (r"and critics: \ it may replace a living, \ flexible intonation with a grid", WHITE),
            (r"data-driven tuning: \ instruments and software that follow measured practice", WHITE),
            (r"but whose practice? \ which singer, \ which city, \ which decade?", TUNE),
            (r"a measurement describes; \ it does not decide what the music should be", GREY_A),
        ]
        rows_scene(self, r"standards and their critics", items,
                   "The debate continues. <bookmark mark='b'/> Standardization has defenders: notation, teaching, ensembles and "
                   "software all need it. <bookmark mark='c'/> It has critics, who fear a flexible, living intonation replaced by "
                   "a grid. <bookmark mark='d'/> Some propose data-driven tunings that follow measured practice. "
                   "<bookmark mark='e'/> But whose practice: which singer, which city, which decade? <bookmark mark='f'/> A "
                   "measurement describes; it does not decide what the music should be.", marks="cdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"collect recordings of one maqam by many musicians, \ across regions and decades", WHITE),
            (r"measure each note's pitch in context: \ rising and falling, \ stressed and passing", WHITE),
            (r"model how a note's pitch depends on maqam, \ direction, \ performer and era", WHITE),
            (r"$\bigstar$ \ research problem: \ what determines where a musician places a neutral note?", EAR),
            (r"the answer would turn `half-flat' from a sign into a description", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Collect recordings of one maqam by many musicians, across regions and "
            "decades. <bookmark mark='b'/> Measure each note's pitch in its context: rising and falling, stressed and passing. "
            "<bookmark mark='c'/> Model how a note's pitch depends on the maqam, the direction, the performer and the era. "
            "<bookmark mark='d'/> What determines where a musician places a neutral note? <bookmark mark='e'/> The answer "
            "would turn half-flat from a sign into a description."
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
            (r"software for maqam: \ tuning tables, \ notation programs with half-flat signs", WHITE),
            (r"recognition systems trained on recordings name the maqam of a piece", WHITE),
            (r"generative models can now produce maqam-like melodies", WHITE),
            (r"the risk: \ models trained on a few famous recordings narrow the tradition", TUNE),
            (r"Parts 61 to 66 build these tools; \ this part shows what they must respect", GREY_A),
        ]
        rows_scene(self, r"machines and maqam", items,
                   "Machines are entering this music. <bookmark mark='b'/> There is software for maqam: tuning tables, and notation programs with half-flat signs. <bookmark mark='c'/> Recognition systems trained on recordings can name the maqam of a piece, <bookmark mark='d'/> and generative models can produce maqam-like melodies. <bookmark mark='e'/> The risk is that models trained on a few famous recordings narrow the tradition they imitate. <bookmark mark='f'/> Parts 61 to 66 build these tools; this part shows what they must respect.", marks="cdef")

    # ------------------------------------------------------------------
    def fair(self):
        items = [
            (r"work with musicians from the start: \ their categories, \ not only ours", WHITE),
            (r"record many performers, \ regions and generations, \ not only the famous", WHITE),
            (r"share data and credit; \ return results to the community", WHITE),
            (r"measure intonation in context, \ with uncertainty, \ before drawing a grid", TUNE),
            (r"Part 67 sets out how to do research in music well", GREY_A),
        ]
        rows_scene(self, r"studying a living tradition fairly", items,
                   "Studying a living tradition fairly takes care. <bookmark mark='b'/> Work with musicians from the start, using their categories as well as ours. <bookmark mark='c'/> Record many performers, regions and generations, not only the famous. <bookmark mark='d'/> Share data and credit, and return results to the community. <bookmark mark='e'/> Measure intonation in its context, with its uncertainty, before drawing any grid. <bookmark mark='f'/> Part 67 sets out how to do research in music well.", marks="cdef")
