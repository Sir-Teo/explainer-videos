from __future__ import annotations

import numpy as np

from videos.music.music25.common import *  # noqa: F403


class Monody(SoundScene):
    def construct(self):
        chapter(self, 1, r"A new kind of song", r"How do you make one voice carry a drama?", extra=((1602, r"Caccini's \textit{Le nuove musiche}"),))
        self.camerata()
        self.two()
        self.graces()
        self.recit()

    # ------------------------------------------------------------------
    def camerata(self):
        items = [
            (r"Florence, \ the 1570s and 80s: \ the Camerata, \ scholars and musicians in Count Bardi's house", WHITE),
            (r"their reading of the Greeks: \ one voice, \ clear words, \ simple support, \ moved the passions", WHITE),
            (r"polyphony, \ they said, \ tears the poetry to pieces", WHITE),
            (r"monody: \ one voice over a bass, \ the harmony filled in by a player", TUNE),
            (r"1602: \ Giulio Caccini prints \textit{Le nuove musiche}, \ the new music", GREY_A),
        ]
        rows_scene(self, r"the Camerata", items,
                   "In the 1570s and 1580s a group of scholars and musicians met in the Florentine house of Count Giovanni "
                   "de' Bardi, and later historians called them the Camerata. Galilei was one of them. "
                   "<bookmark mark='b'/> They read the Greek writers on music and concluded that ancient music had moved "
                   "its listeners because it was one voice, with clear words and simple support. "
                   "<bookmark mark='c'/> Polyphony, they complained, tore the poetry to pieces, every voice singing a "
                   "different word at a different time. <bookmark mark='d'/> Their answer was monody: one voice over a bass "
                   "line, with the harmony filled in by a player on a lute or harpsichord. <bookmark mark='e'/> In 1602 "
                   "Giulio Caccini printed a collection of such songs and called it, simply, The New Music.")

    # ------------------------------------------------------------------
    def two(self):
        d = load("monody")
        c = clip("monody.two")
        gr = voices_roll([d["recitative"], d["rec_bass"]], width=5.6, height=2.6, colors=[TUNE, GREY_A], lo=40, hi=74, bar_h=0.13).move_to(LEFT * 3.3 + DOWN * 0.3)
        ga = voices_roll([d["aria"], d["aria_bass"]], width=5.6, height=2.6, colors=[EAR, GREY_A], lo=40, hi=80, bar_h=0.13).move_to(RIGHT * 3.3 + DOWN * 0.3)
        lr = label(r"recitative: \ speech in pitch, \ the bass held", font_size=21, color=TUNE).next_to(gr, UP, buff=0.35)
        la = label(r"aria: \ a shaped tune, \ the bass walking", font_size=21, color=EAR).next_to(ga, UP, buff=0.35)
        head = label(r"two ways to sing over a bass \ (ours)", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Monody soon split into two manners. In recitative, the voice follows the rhythm of speech, on repeated "
            "notes, over a bass that holds still, and the drama moves forward. In the aria, the voice sings a shaped "
            "tune in a regular rhythm over a bass that moves too, and the drama stops to feel. Here is a short example of "
            "each, computed for the film: first the recitative, then the aria."
        ):
            self.play(FadeIn(head), FadeIn(gr), FadeIn(ga), FadeIn(lr), FadeIn(la))
        with self.listen(c) as snd:
            window(snd, r"recitative, \ then aria", detail=r"a synthetic voice, \ harpsichord", kind="synthesized", corner=DL, tag_corner=DR)
            flash_voices(snd, gr, [d["recitative"], d["rec_bass"]], d["starts"]["recitative"], d["unit"], colors=[TUNE, GREY_A])
            flash_voices(snd, ga, [d["aria"], d["aria_bass"]], d["starts"]["aria"], d["unit"], colors=[EAR, GREY_A])
            pulse(snd, lr, d["starts"]["recitative"], d["starts"]["aria"] - 0.5, buff=0.08)
            pulse(snd, la, d["starts"]["aria"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recit(self):
        items = [
            (r"the bass and its chords became the frame of everything: \ the basso continuo", WHITE),
            (r"the melody and the bass are the composition; \ the middle is filled in", WHITE),
            (r"a new texture: \ not equal voices, \ but a top and a bottom", TUNE),
            (r"Part 24's Monteverdi: \ the words the mistress of the harmony", GREY_A),
            (r"for the next 150 years, \ almost every piece has a continuo", WHITE),
        ]
        rows_scene(self, r"a top and a bottom", items,
                   "The consequence went far beyond song. <bookmark mark='b'/> The bass and the chords above it became the "
                   "frame of almost all music for a century and a half, the basso continuo, the continuous bass. "
                   "<bookmark mark='c'/> What the composer wrote was the melody and the bass; the middle was filled in by "
                   "the player. <bookmark mark='d'/> The texture of Palestrina, equal voices, gave way to a polarity, a top "
                   "and a bottom. <bookmark mark='e'/> It is Monteverdi's second practice from Part 24 made into a "
                   "system: the words govern the melody, and the bass governs the harmony. <bookmark mark='f'/> From 1600 "
                   "to about 1750, almost every piece of Western art music, sacred or secular, sung or played, has a "
                   "continuo part.", marks="cdef")

    # ------------------------------------------------------------------
    def graces(self):
        items = [
            (r"Caccini's preface: \\ how to sing the new music", WHITE),
            (r"the \\textit{esclamazione}: \\ a note begun softly and swelled, \\ for a cry of feeling", WHITE),
            (r"the \\textit{trillo}: \\ one note repeated faster and faster, \\ in the throat", WHITE),
            (r"\\textit{sprezzatura}: \\ a noble carelessness of rhythm, \\ as in speech", TUNE),
            (r"the written notes are a skeleton; \\ the singer supplies the life", GREY_A),
        ]
        rows_scene(self, r"the singer's graces", items,
                   "Caccini's book is also a singing manual. <bookmark mark='b'/> Its preface explains how the new music should be sung. <bookmark mark='c'/> The esclamazione, a note begun softly and swelled, for a cry of feeling. <bookmark mark='d'/> The trillo, a single note repeated faster and faster in the throat, which is not our trill at all. <bookmark mark='e'/> And sprezzatura, a noble carelessness, letting the rhythm bend as speech does. <bookmark mark='f'/> The written notes were a skeleton, and the singer supplied the life: the same lesson as Part 22's reductions, from the other side.", marks="cdef")
