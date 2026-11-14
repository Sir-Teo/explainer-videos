from __future__ import annotations

import numpy as np

from videos.music.music26.common import *  # noqa: F403


class Piano(SoundScene):
    def construct(self):
        chapter(self, 8, r"The fortepiano and the metronome", r"What did the new instruments change?", extra=((1815, r"Maelzel's metronome"),))
        self.fortepiano()
        self.metronome()
        self.debate()

    # ------------------------------------------------------------------
    def fortepiano(self):
        items = [
            (r"Cristofori's hammer harpsichord \ (Florence, \ about 1700) \ becomes the Viennese fortepiano", WHITE),
            (r"leather-covered hammers, \ a light action, \ five octaves: \ soft and loud by touch \ (Part 7)", WHITE),
            (r"the harpsichord could not make a crescendo; \ the fortepiano could", WHITE),
            (r"dynamics become part of the composition: \ \textit{p}, \ \textit{f}, \ \textit{sf}, \ crescendo", TUNE),
            (r"by Beethoven's late sonatas: \ six octaves and more, \ iron bracing coming", GREY_A),
        ]
        rows_scene(self, r"an instrument that can be soft and loud", items,
                   "The keyboard changed under the composers' hands. <bookmark mark='b'/> Bartolomeo Cristofori's harpsichord "
                   "with hammers, built in Florence around 1700, had become by the 1780s the Viennese fortepiano: "
                   "<bookmark mark='c'/> leather-covered hammers, a light action, five octaves, soft or loud by the touch "
                   "of the finger, as Part 7 simulated. <bookmark mark='d'/> A harpsichord cannot make a crescendo; the "
                   "fortepiano can, <bookmark mark='e'/> and dynamics became part of the composition, written into the score "
                   "as piano, forte, sudden accents and crescendos. <bookmark mark='f'/> By Beethoven's last sonatas the "
                   "instrument had six octaves and more, and iron bracing was on its way.", marks="cdef")

    # ------------------------------------------------------------------
    def metronome(self):
        items = [
            (r"1815: \ Johann Nepomuk Maelzel patents the metronome \ (after Winkel's design)", WHITE),
            (r"1817: \ Beethoven publishes metronome marks for his first eight symphonies", WHITE),
            (r"for the first time a composer's tempo is a number", TUNE),
            (r"many of the marks are very fast: \ faster than most performers have played them", WHITE),
            (r"was his metronome broken? \ did he misread it? \ did he mean them?", EAR),
        ]
        rows_scene(self, r"tempo as a number", items,
                   "A machine changed tempo too. <bookmark mark='b'/> In 1815 Johann Nepomuk Maelzel patented the "
                   "metronome, borrowing the design of the Dutch inventor Dietrich Winkel. <bookmark mark='c'/> In 1817 "
                   "Beethoven published metronome marks for his first eight symphonies, <bookmark mark='d'/> and for the "
                   "first time a composer's tempo was a number rather than a word. <bookmark mark='e'/> Many of the marks "
                   "are very fast, faster than most performers have dared, <bookmark mark='f'/> and the argument about them "
                   "has run for two centuries.")

    # ------------------------------------------------------------------
    def debate(self):
        items = [
            (r"hypothesis 1: \ the metronome was faulty", WHITE),
            (r"hypothesis 2: \ he read the wrong edge of the weight, \ or misjudged in his deafness", WHITE),
            (r"hypothesis 3: \ he meant them, \ and later performers slowed down", WHITE),
            (r"the evidence: \ marks in many works, \ the machine's mechanics, \ others' marks of the time", TUNE),
            (r"a statistical study of all his marks \ (Martín-Castro and Ucar, \ 2020) \ found a consistent slowing of about 12 beats a minute", GREY_A),
        ]
        rows_scene(self, r"Beethoven's puzzling marks", items,
                   "There are three kinds of explanation. <bookmark mark='b'/> The machine was faulty; "
                   "<bookmark mark='c'/> or Beethoven misread it, perhaps reading the scale at the wrong edge of the "
                   "sliding weight, or misjudged because of his deafness; <bookmark mark='d'/> or he meant the marks, and "
                   "later performers slowed down. <bookmark mark='e'/> The evidence is the marks themselves, across many "
                   "works, the mechanics of the machine, and other composers' marks of the time. <bookmark mark='f'/> A "
                   "statistical study published in 2020 compared his marks with tempos in recordings and argued for a "
                   "systematic misreading worth about twelve beats a minute. The film could not obtain that study's data "
                   "to recompute it; it stays here as a claim to check, which is what the problems at the end ask.", marks="cdef")
