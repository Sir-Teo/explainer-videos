from __future__ import annotations

import numpy as np

from videos.music.music31.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.film()
        self.question()
        self.plan()

    # ------------------------------------------------------------------
    def film(self):
        d = load("hook")
        c = clip("hook.film")
        cells = VGroup(*[VGroup(label(tex_triad(n), font_size=40, color=TUNE if n == "C" else EAR)) for n in d["chain"]]).arrange(RIGHT, buff=0.9).move_to(UP * 0.6)
        moves = VGroup(*[label(m, font_size=22, color=GREY_A).move_to((cells[i].get_center() + cells[i + 1].get_center()) / 2 + DOWN * 0.8) for i, m in enumerate(d["moves"])])
        head = label(r"a progression in the manner of a film score \ (ours)", font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        cap = label(r"C major and E major share one note; \ C major and A$\flat$ major share one note: \ no key holds both", font_size=21, color=GREY_A).to_edge(DOWN, buff=1.1)
        with self.voiceover(
            "Listen to a progression of our own, in the manner of a film score at a moment of wonder: C major, E major, C "
            "major again, A flat major, F, and home. Every chord is an ordinary major triad. But C major and E major share "
            "only one note, and no key contains both; the same is true of C and A flat. Functional harmony, tonic, "
            "subdominant, dominant, has nothing to say about these moves, and audiences love them."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"C, \ E, \ C, \ A$\flat$, \ F, \ C", detail=r"Part 7's bowed string", corner=DL, tag_corner=DR)
            for i in range(len(cells)):
                pulse(snd, cells[i], i * d["unit"], (i + 1) * d["unit"] - 0.1, buff=0.12)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        items = [
            (r"Riemann \ (1880s): \ every chord is tonic, \ dominant or subdominant of a key", WHITE),
            (r"chromatic music after Wagner moves between chords that no single key holds", WHITE),
            (r"David Lewin \ (1987): \ stop naming the chords; \ name the moves between them", TUNE),
            (r"three moves that keep two notes and shift one: \ P, \ L, \ R", WHITE),
            (r"they form a group; \ the part builds it, \ and its twin", GREY_A),
        ]
        rows_scene(self, r"name the moves", items,
                   "The tool to describe them came late. <bookmark mark='b'/> The nineteenth-century theorist Hugo Riemann "
                   "taught that every chord is the tonic, dominant or subdominant of some key. <bookmark mark='c'/> But music "
                   "after Wagner moves between chords that no single key holds. <bookmark mark='d'/> In 1987 David Lewin "
                   "proposed a change of view: stop naming the chords, and name the moves between them. "
                   "<bookmark mark='e'/> Three moves do most of the work: each keeps two notes of a triad and shifts the third. "
                   "<bookmark mark='f'/> They form a group, and this part builds it, and its twin.", marks="cdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"P, \ L and R: \ the parsimonious moves, \ heard",
            r"two groups of 24, \ built by brute force: \ they commute",
            r"the Tonnetz: \ every triad a triangle on a torus",
            r"hexatonic and octatonic cycles, \ and the long chain through all 24 triads",
            r"film's chromatic mediants, \ and jazz's major-third cycles",
            r"do listeners feel these distances?",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. First the three moves, P, L and R, heard. <bookmark mark='b'/> Then the two groups of "
            "twenty-four operations they belong to, built by brute force, and a surprising fact about how they fit together. "
            "<bookmark mark='c'/> The Tonnetz, a map on which every triad is a triangle and the whole space is a torus. "
            "<bookmark mark='d'/> Cycles, and the long chain through all twenty-four triads. <bookmark mark='e'/> Film's "
            "chromatic mediants and jazz's cycles of major thirds. <bookmark mark='f'/> And the frontier: do listeners "
            "actually feel these distances?"
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
