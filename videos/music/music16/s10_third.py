from __future__ import annotations

import numpy as np

from videos.music.music16.common import *  # noqa: F403
from videos.music.music16.s09_second import species_scene


class Third(SoundScene):
    def construct(self):
        chapter(self, 9, r"Four notes against one", r"What else can a dissonance do?")
        self.figures()
        self.hear()

    def figures(self):
        def fig(notes, cf, diss):
            g = duet([[(p, k, 1) for k, p in enumerate(notes)], [(cf, 0, 4)]], width=3.6, height=2.2, lo=58, hi=78, thick=0.15)
            for k in diss:
                g.notes[0][k].set_fill(EAR)
            return g
        a = fig([72, 74, 76, 77], 60, (1, 3))
        b = fig([76, 77, 76, 74], 60, (1, 3))
        cfig = fig([72, 69, 71, 72], 60, (2,))
        cells = VGroup(VGroup(label(r"passing", font_size=28, color=TUNE), a, label(r"step, \ step, \ step", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.25),
                       VGroup(label(r"neighbouring", font_size=28, color=TUNE), b, label(r"step away, \ step back", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.25),
                       VGroup(label(r"a skip to a consonance", font_size=28, color=TUNE), cfig, label(r"the dissonance still steps", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.25)).arrange(RIGHT, buff=0.8).move_to(DOWN * 0.3)
        head = label(r"four quarter notes to each note of the cantus", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Third species gives the new voice four notes to each one of the cantus, and two kinds of "
            "dissonance. <bookmark mark='a'/> The passing note, as before. <bookmark mark='b'/> And the "
            "neighbouring note: a step away from a consonance and straight back, a decoration of a "
            "single note. <bookmark mark='c'/> The line may skip between consonances, but every "
            "dissonance is still reached and left by step. The first note of each group must be "
            "consonant. Everything the ear might hear as a mistake is placed so that it is heard as "
            "motion."
        ) as vo:
            self.play(FadeIn(head))
            for mark, cell in zip("abc", cells):
                vo.wait_until(mark)
                self.play(FadeIn(cell))
        self.wait(0.4)
        self.clear_scene()

    def hear(self):
        d = load("species")["3"]
        species_scene(self, 3,
                      "Here is a third-species line over the same cantus. Pink, again, for the dissonances.",
                      f"{len(d['dissonances'])} dissonances in forty-one notes, every one of them passing "
                      "or neighbouring, every one on a weak beat. Now three notes in four begin while the "
                      "cantus holds still. And the new voice has become a melody in its own right: listen "
                      "to it alone in your head, and it would make sense.",
                      r"pink: \ passing and neighbouring dissonances")
