from __future__ import annotations

import numpy as np

from videos.music.music26.common import *  # noqa: F403


class Style(SoundScene):
    def construct(self):
        chapter(self, 1, r"A style of shared expectations", r"Why could a piece be funny?", extra=((1781, r"Haydn's Op. 33"),))
        self.galant()
        self.schemata()
        self.joke()

    # ------------------------------------------------------------------
    def galant(self):
        items = [
            (r"after 1730: \ the galant style, \ from Italian opera: \ a tune over a simple bass", WHITE),
            (r"short phrases, \ clear cadences, \ slow harmony under quick melody", WHITE),
            (r"the public grows: \ concerts, \ printed music for amateurs, \ the keyboard in every parlour", WHITE),
            (r"a shared vocabulary of stock patterns: \ the schemata of Part 18", TUNE),
            (r"Rosen's \textit{The Classical Style} \ (1971): \ Haydn, \ Mozart, \ Beethoven made it dramatic", GREY_A),
        ]
        rows_scene(self, r"from galant to Classical", items,
                   "The Classical style grew out of a lighter one. <bookmark mark='b'/> From about 1730 composers trained "
                   "in Italian opera wrote in a galant manner, a tune over a simple bass, <bookmark mark='c'/> with short "
                   "phrases, clear cadences, and harmony that moves slowly under a quick melody. "
                   "<bookmark mark='d'/> Its audience was growing: public concerts, printed music for amateurs, a keyboard "
                   "in every comfortable parlour. <bookmark mark='e'/> It rested on a shared vocabulary of stock patterns, "
                   "the schemata of Part 18, which every trained musician knew. <bookmark mark='f'/> Charles Rosen's book "
                   "The Classical Style argued that Haydn, Mozart and Beethoven turned this polite language into drama.", marks="cdef")

    # ------------------------------------------------------------------
    def schemata(self):
        items = [
            (r"the Romanesca, \ the Prinner, \ the Fonte, \ the Monte, \ the Ponte: \ named by Robert Gjerdingen \ (2007)", WHITE),
            (r"each a bass and a melody that move together in a known way", WHITE),
            (r"taught to apprentices in Naples through partimenti \ (Part 25)", WHITE),
            (r"a listener who knows them hears what is coming, \ and notices when it does not come", TUNE),
            (r"Part 18 found few in Bach's chorales: \ they belong to this style", GREY_A),
        ]
        rows_scene(self, r"the stock patterns", items,
                   "Those patterns now have names. <bookmark mark='b'/> The musicologist Robert Gjerdingen, in 2007, "
                   "revived and named them: the Romanesca, the Prinner, the Fonte, the Monte, the Ponte, and a dozen more. "
                   "<bookmark mark='c'/> Each is a bass line and a melody moving together in a known way. "
                   "<bookmark mark='d'/> Apprentices learned them in Naples, through the partimenti of Part 25. "
                   "<bookmark mark='e'/> A listener who knows them hears what is coming, and notices when it does not "
                   "come. <bookmark mark='f'/> Part 18's detector found few of them in Bach's chorales, which was the wrong "
                   "repertory: they belong to the galant and Classical style.", marks="cdef")

    # ------------------------------------------------------------------
    def joke(self):
        items = [
            (r"Haydn, \ String Quartet Op. 33 No. 2 \ (1781), \ finale: \ a cheerful rondo", WHITE),
            (r"near the end: \ an Adagio, \ then the tune in fragments, \ separated by silences", WHITE),
            (r"each fragment could be the end; \ none is \ (until the last, \ after a long rest)", WHITE),
            (r"the joke works only if everyone knows how a piece ends", TUNE),
            (r"Classical style: \ conventions so shared that they can be played with", GREY_A),
        ]
        rows_scene(self, r"a joke about endings", items,
                   "Haydn's joke shows how strong the expectations were. <bookmark mark='b'/> The finale of his String "
                   "Quartet Opus 33 Number 2, of 1781, is a cheerful rondo, <bookmark mark='c'/> but near the end it "
                   "slows to an Adagio, then breaks its tune into fragments separated by silences, "
                   "<bookmark mark='d'/> each of which could be the end and is not, until after a long rest the opening "
                   "phrase returns, and stops in mid-air. <bookmark mark='e'/> The joke only works because everyone in the "
                   "room knew exactly how a piece ought to end. <bookmark mark='f'/> That is the Classical style: "
                   "conventions so firmly shared that a composer could play with them, and the audience would get it.", marks="cdef")
