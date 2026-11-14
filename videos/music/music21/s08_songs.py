from __future__ import annotations

import numpy as np

from videos.music.music21.common import *  # noqa: F403

BARS_C = {"C": "#F5C542", "F": "#A3E635", "G": "#F472B6"}


class Songs(SoundScene):
    def construct(self):
        chapter(self, 7, r"Song forms", r"How are songs built?")
        self.forms()
        self.blues()

    # ------------------------------------------------------------------
    def forms(self):
        d = load("forms")
        imgs = Group()
        for name, t in (("AABA", r"AABA: \ the 32-bar song"), ("verse-chorus", r"verse and chorus")):
            imgs.add(Group(label(t, font_size=24, color=GREY_A), ssm_image(d[name]["ssm"], size=3.6)).arrange(DOWN, buff=0.25))
        imgs.arrange(RIGHT, buff=0.8).move_to(LEFT * 2.6 + DOWN * 0.2)
        rows_ = VGroup(*[label(t, font_size=23, color=c_) for t, c_ in (
            (r"strophic: \ one tune, \ new words each verse", WHITE),
            (r"AABA: \ Tin Pan Alley, \ 1920s to 1950s; \ B is the bridge", WHITE),
            (r"verse and chorus: \ the chorus returns with the same words", WHITE),
            (r"the chorus is a refrain: \ a rondo in disguise", TUNE))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 4.4))
        rows_.move_to(RIGHT * 4.6 + DOWN * 0.1)
        with self.voiceover(
            "Songs have forms of their own. <bookmark mark='a'/> The oldest is strophic: one tune, sung again with new "
            "words for each verse, as in most folk songs and hymns. <bookmark mark='b'/> The popular songs of Tin Pan "
            "Alley, from the 1920s to the 1950s, were mostly AABA: two statements, a contrasting bridge, and a return, "
            "thirty-two bars in all. <bookmark mark='c'/> Rock and pop songs alternate verses, whose words change, with a "
            "chorus, whose words do not. <bookmark mark='d'/> The chorus is a refrain, and its picture shows it: a "
            "lattice of bright blocks, like the rondo's."
        ) as vo:
            self.play(FadeIn(imgs), FadeIn(rows_[0]))
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        c = clip("forms.aaba")
        with self.listen(c) as snd:
            window(snd, r"AABA on the Tune", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            self.add(diag_cursor(snd, imgs[0][1], d["AABA"]["beats"], d["AABA"]["beat"]))
            pulse(snd, imgs[0][0], 0.0, c.duration, buff=0.08)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def blues(self):
        d = load("blues")
        c = clip("blues.twelve")
        cells = VGroup()
        for k, b in enumerate(d["bars"]):
            box = RoundedRectangle(width=1.5, height=0.9, corner_radius=0.1, stroke_color=BARS_C[b], stroke_width=2.5, fill_color=BARS_C[b], fill_opacity=0.15)
            cells.add(VGroup(box, label({"C": r"I", "F": r"IV", "G": r"V"}[b], font_size=28, color=WHITE).move_to(box)))
        cells.arrange_in_grid(rows=3, cols=4, buff=(0.2, 0.25)).move_to(LEFT * 2.4 + DOWN * 0.2)
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"the twelve-bar blues: \ three lines of four bars", WHITE),
            (r"I for four bars; \ IV, \ IV, \ I, \ I; \ V, \ IV, \ I, \ I", WHITE),
            (r"a form that is a chord progression", TUNE),
            (r"repeated for as long as the singer has verses \ (Part 38)", GREY_A))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 5.6))
        rows_.move_to(RIGHT * 3.8 + DOWN * 0.1)
        with self.voiceover(
            "One song form is nothing but a chord progression: the twelve-bar blues. Three lines of four bars: four bars "
            "of the home chord; two of the subdominant and two of home; then dominant, subdominant, and home. Here it "
            "is with the Tune's first notes as a riff."
        ):
            self.play(FadeIn(cells), FadeIn(rows_[0]), FadeIn(rows_[1]))
        with self.listen(c) as snd:
            window(snd, r"twelve bars on the Tune's head", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for k, b in enumerate(d["bars"]):
                flash(snd, [cells[k][0]], [d["starts"][k] * d["beat"]], hot=WHITE, base=BARS_C[b], hold=4 * d["beat"] * 0.8)
        with self.voiceover(
            "The form is the progression, repeated as long as the singer has verses, and the melody is free to change "
            "every time. Part 38 is about the blues, and Part 39 builds jazz on top of it."
        ):
            self.play(FadeIn(rows_[2]), FadeIn(rows_[3]))
        self.wait(0.4)
        self.clear_scene()
