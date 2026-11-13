from __future__ import annotations

import numpy as np

from videos.music.music9.common import *  # noqa: F403


class Plates(SoundScene):
    def construct(self):
        chapter(self, 6, r"Plates and sand", r"How do you see a vibration?", lit=(1807,), extra=((1787, r"Chladni's figures"),))
        self.sand()
        self.prize()

    # ------------------------------------------------------------------
    def sand(self):
        d = load("plates")
        figs = d["figs"]
        cells = Group()
        for k, f in enumerate(figs):
            img = sand_image(np.asarray(d[f"fig{k}"]), 1.75)
            cells.add(Group(img, label(rf"{f['pitch']:.0f}", font_size=26, color=TUNE).next_to(img, DOWN, buff=0.1)))
        cells.arrange_in_grid(rows=2, cols=4, buff=(0.45, 0.3)).move_to(RIGHT * 1.9 + DOWN * 0.35)
        notes = VGroup(label(r"a metal plate, \\ held at its middle, \\ bowed on its edge", font_size=26, color=GREY_A),
                       label(r"sand is thrown off \\ the parts that move", font_size=26, color=SKIN),
                       label(r"and settles on \\ the lines that stay still", font_size=26, color=SKIN),
                       label(r"under each: \ its pitch, \\ in units of the lowest", font_size=22, color=TUNE)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(LEFT * 5.0 + DOWN * 0.2)
        with self.voiceover(
            "A bar is stiff in one direction. Widen it into a plate and it is stiff in two, with a still "
            "richer crowd of modes. How would you ever find out what they look like? In 1787 a lawyer and "
            "amateur musician in Wittenberg, Ernst Chladni, found a way that needs no instruments at all. "
            "<bookmark mark='a'/> Hold a metal plate at its middle. Scatter fine sand on it. Draw a violin "
            "bow down its edge until it sings. <bookmark mark='b'/> Wherever the plate is moving, the sand "
            "is thrown into the air. It comes to rest only on the lines where the plate stands still. "
            "<bookmark mark='c'/> And so the sand draws the mode. Touch the edge with a finger in a "
            "different place, bow again, and another figure appears, with another pitch. Chladni filled "
            "books with them. These are computed, by a formula that Walther Ritz worked out in 1909, and "
            "under each is its pitch: the more lines, the higher the note. Chladni toured Europe with his "
            "plates, and audiences paid to watch sound become visible."
        ) as vo:
            rng = np.random.default_rng(3)
            dust = sand_image(0.12 + 0.5 * rng.random((141, 141)), 3.2).move_to(RIGHT * 1.9 + DOWN * 0.2)
            dl = label(r"a plate, \ dusted with sand", font_size=24, color=GREY_B).next_to(dust, DOWN, buff=0.15)
            self.play(FadeIn(notes[0]), FadeIn(dust), FadeIn(dl))
            vo.wait_until("a")
            self.play(FadeOut(dust), FadeOut(dl), FadeIn(cells[0][0]), FadeIn(cells[1][0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(cells[k][0]) for k in range(2, 8)], lag_ratio=0.4), run_time=6.0)
            self.play(LaggedStart(*[FadeIn(c[1]) for c in cells], lag_ratio=0.2), FadeIn(notes[3]), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def prize(self):
        head = label(r"What the sand started", font_size=38, color=GREY_A).to_edge(UP, buff=0.4)
        rows = rows_card([
            (r"1809", r"Chladni's plates are shown to Napoleon, \ who puts up a prize \\ for whoever can explain them."),
            (r"1816", r"Sophie Germain wins it, \ at her third attempt, \\ with the first equation for a vibrating plate."),
            (r"1850, \ 1909", r"Kirchhoff corrects the conditions at the edge; \ Ritz computes the figures, \\ and invents a method engineers still use every day."),
            (r"today", r"violin makers sprinkle glitter on a free top plate over a loudspeaker, \\ and carve until two of its figures appear at the right pitches."),
        ], left=-6.4, text_left=-3.9, top=1.9, step=1.42, name_size=28, text_size=23, color=HIST)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "The sand started something. <bookmark mark='a'/> In 1809, in Paris, the plates were shown to Napoleon, "
            "who was impressed enough to fund a prize for anyone who could explain them mathematically. "
            "<bookmark mark='b'/> It was won in 1816, at her third attempt, by Sophie Germain, who had "
            "taught herself mathematics from her father's library and corresponded with Gauss under a "
            "man's name. Her equation for the bending of a plate is, with corrections, the one used today. "
            "<bookmark mark='c'/> Kirchhoff got the edges right in 1850, and in 1909 Walther Ritz computed "
            "the figures themselves, by a method of trial shapes that is now the foundation of how "
            "engineers compute anything that bends. <bookmark mark='d'/> And the sand is still in use. A "
            "violin maker lays a half-carved top plate over a loudspeaker, sprinkles it with glitter, and "
            "carves until two particular figures, a cross and a ring, appear at the right pitches. It is "
            "Part 7's tap tone, made visible."
        ) as vo:
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
