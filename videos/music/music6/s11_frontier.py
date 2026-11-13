from __future__ import annotations

import numpy as np

from videos.music.music6.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ tuning that moves", r"Must an instrument have one tuning?", lit=(1983,), extra=((2005, r"Lehman's reading of Bach's title page"),))
        self.adaptive()
        self.bach()
        self.open()

    # ------------------------------------------------------------------
    def adaptive(self):
        d = load("pump")
        g = axes([0, 4.3], [-110, 12], x_length=6.4, y_length=3.2, xlabel=r"times round the progression", ylabel=r"the note C (cents)", xticks=[0, 1, 2, 3, 4], yticks=[-100, -50, 0], font_size=20)
        g.move_to(RIGHT * 3.0 + DOWN * 0.6)
        pure = VMobject(stroke_color=BAD, stroke_width=3).set_points_as_corners([g.ax.c2p(k, v) for k, v in enumerate(d["drift"])])
        fixed = Line(g.ax.c2p(0, 0), g.ax.c2p(4.3, 0), color=NARROW, stroke_width=3)
        xs = np.linspace(0, 4.3, 200)
        adapt = curve(g.ax, xs, -9.0 * np.abs(np.sin(np.pi * xs)) ** 0.8, GOOD)
        leg = VGroup(label(r"pure chords, \ held notes: \ drifts", font_size=22, color=BAD), label(r"a fixed temperament: \ stays, \ and beats", font_size=22, color=NARROW),
                     label(r"adaptive: \ nearly pure, \ and pulled back", font_size=22, color=GOOD)).arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(g, UP, buff=0.25)
        tag = label(r"the green curve is a sketch", font_size=18, color=GREY_C).next_to(g, DOWN, buff=0.75).align_to(g, RIGHT)
        notes = VGroup(label(r"a synthesizer can retune every note \\ while it is sounding", font_size=28, color=GREY_A),
                       label(r"so: \ make each chord as pure as possible, \\ and spread the comma where it shows least", font_size=28, color=GOOD),
                       label(r"used today in organs, \ software instruments \\ and notation programs", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(LEFT * 3.6 + DOWN * 0.2)
        with self.voiceover(
            "Every system in this part froze a keyboard into one compromise. An electronic instrument has no "
            "need to. <bookmark mark='a'/> It can retune any note, by any amount, while the note is sounding. So "
            "it can do what a good choir does: hear which chord is being played, make that chord as pure as it "
            "can, and spread the leftover comma where it will be noticed least. <bookmark mark='b'/> On our "
            "progression, pure chords drift, and a fixed temperament stays put but beats. An adaptive tuning "
            "can stay close to pure in every chord and still come home. <bookmark mark='c'/> Schemes of this "
            "kind are built into some electronic organs, software instruments and notation programs today. "
            "They raise a new question, which nobody has settled: when a chord's notes glide a few cents to "
            "meet each other, do listeners hear better tuning, or a wobble?"
        ) as vo:
            frozen = label(r"every tuning so far: \ one compromise, \ frozen into the instrument", font_size=32, color=GREY_A).to_edge(UP, buff=0.5)
            self.play(FadeIn(frozen), run_time=0.6)
            vo.wait_until("a")
            self.play(FadeOut(frozen), FadeIn(notes[0]))
            self.wait(max(vo.until("b") - 6.0, 0.1))
            self.play(FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(g), Create(pure), Create(fixed), FadeIn(leg[0]), FadeIn(leg[1]), run_time=2.0)
            self.play(Create(adapt), FadeIn(leg[2]), FadeIn(tag), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bach(self):
        loops = VGroup()
        kinds = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2]
        for k, kind in enumerate(kinds):
            c0 = LEFT * 4.4 + RIGHT * 0.8 * k + UP * 1.9
            outer = Circle(radius=0.33, color=GREY_A, stroke_width=3).move_to(c0)
            inner = VGroup(*[Circle(radius=0.11, color=GREY_A, stroke_width=2).move_to(c0 + DOWN * 0.05 + RIGHT * 0.07 * j) for j in range(kind)])
            loops.add(VGroup(outer, inner))
        cap = label(r"the row of loops above Bach's title, \ 1722 \ (a sketch of its pattern: three kinds of loop)", font_size=20, color=GREY_C).next_to(loops, DOWN, buff=0.25)
        card = history_card(2005, r"Bradley Lehman, \ \textit{Early Music}",
                            r"reads the loops as tuning instructions: eleven fifths, tempered by three different amounts. A temperament ``hidden in plain sight''.", width=5.6, font_size=20).move_to(LEFT * 3.3 + DOWN * 1.4)
        crit = VGroup(label(r"the replies, \ 2005 to 2006:", font_size=24, color=GREY_B),
                      label(r"which way up is the drawing?", font_size=26, color=BAD), label(r"which loop is which note?", font_size=26, color=BAD),
                      label(r"other readings fit the same loops", font_size=26, color=BAD), label(r"or it is only a flourish", font_size=26, color=BAD)
                      ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(RIGHT * 3.5 + DOWN * 1.4)
        with self.voiceover(
            "The second open question is three hundred years old. We know Bach's keyboard was well tempered. We "
            "do not know how. He left no table. <bookmark mark='a'/> At the top of the title page of the "
            "Well-Tempered Clavier, in his own hand, is a row of eleven loops, of three different kinds. For "
            "two and a half centuries it was taken for decoration. <bookmark mark='b'/> In 2005 the "
            "harpsichordist Bradley Lehman proposed that it is a tuning diagram: eleven loops for eleven "
            "fifths, and the three kinds of loop for three amounts of tempering. Read his way, it gives a "
            "specific temperament, and recordings have been made in it. <bookmark mark='c'/> The replies came "
            "at once. Which way up should the drawing be read? Which loop is which fifth? Other scholars "
            "derived different temperaments from the same loops, and some maintain that it is simply a "
            "flourish. There is no agreement. The best-known title in keyboard music names a tuning that may "
            "be lost."
        ) as vo:
            ask = label(r"Bach's keyboard was well tempered. \quad How?", font_size=36, color=LIMIT).move_to(DOWN * 0.2)
            self.play(FadeIn(ask), run_time=0.6)
            vo.wait_until("a")
            self.play(FadeOut(ask), LaggedStart(*[Create(l) for l in loops], lag_ratio=0.12), FadeIn(cap), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(card))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x) for x in crit], lag_ratio=0.5), run_time=5.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open(self):
        head = label(r"What is not known", font_size=40, color=LIMIT).to_edge(UP, buff=0.4)
        rows = rows_card([
            (r"adaptive tuning", r"how pure can chords be made, \ in real time, \ before the retuning itself is heard? \\ What do listeners prefer?"),
            (r"historical tunings", r"what did Bach, \ Mozart or Chopin actually hear? \ Written instructions are rare and vague; \\ surviving organ pipes are some of the only hard evidence"),
            (r"the map of temperaments", r"every temperament is a choice of which commas to make vanish. \\ The geometry of all such choices is still being charted. \quad $\rightarrow$ Part 33"),
        ], left=-6.5, text_left=-2.9, top=1.5, step=1.55, name_size=26, text_size=21, color=LIMIT)
        with self.voiceover(
            "Three things, then, that are not known. <bookmark mark='a'/> How pure can an adaptive tuning make "
            "its chords before the retuning itself becomes audible, and what do listeners actually prefer? "
            "<bookmark mark='b'/> What did Bach, or Mozart, or Chopin hear? Written tuning instructions from "
            "their time are rare and vague, and a few surviving organ pipes are some of the only hard evidence "
            "we have. <bookmark mark='c'/> And the mathematics. Every temperament is a choice of which commas to "
            "make disappear: the Pythagorean, the syntonic, or others we have not met. The space of all such "
            "choices has a geometry, and mapping it is a small, active corner of mathematics and music theory "
            "that we will visit in Part 33."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abc", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()
