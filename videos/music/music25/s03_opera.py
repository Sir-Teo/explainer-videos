from __future__ import annotations

import numpy as np

from videos.music.music25.common import *  # noqa: F403


class Opera(SoundScene):
    def construct(self):
        chapter(self, 2, r"Opera", r"What happens when a whole drama is sung?", extra=((1607, r"Monteverdi's \textit{Orfeo}"),))
        self.first()
        self.orfeo()
        self.lament()
        self.venice()

    # ------------------------------------------------------------------
    def first(self):
        items = [
            (r"1598 and 1600, \ Florence: \ Jacopo Peri's \textit{Dafne} and \textit{Euridice}, \ dramas sung throughout", WHITE),
            (r"for court weddings and festivities: \ a few hundred guests", WHITE),
            (r"the subject: \ Orpheus, \ the singer whose song moves the gods of the dead", TUNE),
            (r"recitative carries the story; \ choruses and songs mark its stations", WHITE),
            (r"the oldest opera whose music survives complete: \ \textit{Euridice}", GREY_A),
        ]
        rows_scene(self, r"the first operas", items,
                   "The Florentines soon set whole dramas to music. <bookmark mark='b'/> In 1598 Jacopo Peri's Dafne, and "
                   "in 1600 his Euridice, were sung from beginning to end, <bookmark mark='c'/> as entertainments for "
                   "court celebrations, before a few hundred guests. <bookmark mark='d'/> The story they chose, again and "
                   "again, was Orpheus, the singer whose song persuades the gods of the dead to give back his wife: a myth "
                   "about the power of music itself. <bookmark mark='e'/> Recitative carried the story; choruses and "
                   "strophic songs marked its stations. <bookmark mark='f'/> Euridice is the oldest opera whose music "
                   "survives complete.", marks="cdef")

    # ------------------------------------------------------------------
    def orfeo(self):
        items = [
            (r"1607, \ Mantua: \ Monteverdi's \textit{Orfeo}", WHITE),
            (r"an orchestra named in the score: \ strings, \ recorders, \ cornetts, \ trombones, \ continuo instruments", WHITE),
            (r"a toccata, \ ritornellos that return between strophes, \ choruses, \ dances", WHITE),
            (r"Orpheus's plea to Charon: \ every resource of the new style and the old ornament", TUNE),
            (r"opera as a form, \ not an experiment", GREY_A),
        ]
        rows_scene(self, r"Orfeo", items,
                   "Seven years later Monteverdi, then at the court of Mantua, wrote his Orfeo. <bookmark mark='b'/> Its "
                   "printed score names its instruments, unusually for the time: strings, recorders, cornetts, trombones "
                   "and a variety of continuo instruments, harpsichords, organs, lutes. <bookmark mark='c'/> It opens with "
                   "a fanfare-like toccata, and instrumental ritornellos return between the strophes of the songs, the "
                   "first hint of the returning sections of chapter six. <bookmark mark='d'/> At its centre Orpheus pleads "
                   "with the ferryman of the dead in a song that uses every resource of the new style and of the old art of "
                   "ornament. <bookmark mark='e'/> With Orfeo, opera gained a particularly influential early example.")

    # ------------------------------------------------------------------
    def lament(self):
        d = load("lament")
        c = clip("opera.lament")
        g = voices_roll([d["melody"], d["bass"]], width=11.0, height=3.0, colors=[EAR, GREY_A], bar_h=0.13).move_to(DOWN * 0.2)
        head = label(r"a lament over a falling ground \ (ours)", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(r"A G F E, \ again and again: \ the descending tetrachord, \ the sign of grief", font_size=22, color=WHITE).next_to(g, DOWN, buff=0.35)
        with self.voiceover(
            "Opera also gave grief its own sound. A bass that falls by step through four notes, A, G, F, E, repeated "
            "over and over, with a voice lamenting above it, became one influential lament convention: Monteverdi's Lament of the "
            "Nymph uses it, and half a century later Dido's lament in Purcell's opera uses a chromatic form of it. Here is one built for the "
            "film: the ground three times, the voice rising and falling against it."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"a lament on a ground", detail=r"a synthetic voice, \ harpsichord", kind="synthesized", corner=UL, tag_corner=UR)
            flash_voices(snd, g, [d["melody"], d["bass"]], 0.0, d["unit"], colors=[EAR, GREY_A])
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def venice(self):
        items = [
            (r"1637, \ Venice: \ the first public opera house, \ San Cassiano: \ anyone with a ticket", WHITE),
            (r"by 1700, \ Venice had seen hundreds of new operas, \ several houses competing each season", WHITE),
            (r"singers became stars; \ the aria grew, \ the recitative shrank", WHITE),
            (r"the da capo aria: \ A, \ B, \ A again, \ the return ornamented by the singer", TUNE),
            (r"Handel's London operas \ (chapter 9) \ are its heirs", GREY_A),
        ]
        rows_scene(self, r"opera for a paying public", items,
                   "Then opera left the court. <bookmark mark='b'/> In 1637 the first public opera house opened in Venice, "
                   "the Teatro San Cassiano, where anyone with a ticket could come. <bookmark mark='c'/> By the end of the "
                   "century Venice had seen hundreds of new operas, with several houses competing each carnival season. "
                   "<bookmark mark='d'/> Singers became stars, the arias grew, and the recitative shrank to the story's "
                   "bare connective tissue. <bookmark mark='e'/> The standard aria became the da capo aria: a first "
                   "section, a contrasting second, and the first again, which the singer was expected to ornament. "
                   "<bookmark mark='f'/> Handel's London operas, in chapter nine, are its heirs.", marks="cdef")
