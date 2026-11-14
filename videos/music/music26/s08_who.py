from __future__ import annotations

import numpy as np

from videos.music.music26.common import *  # noqa: F403


class Who(SoundScene):
    def construct(self):
        chapter(self, 7, r"Who wrote this, \ fairly", r"Can a program tell Haydn from Mozart?")
        self.test()
        self.why()

    # ------------------------------------------------------------------
    def test(self):
        d = load("style")
        conf = d["conf26"]
        names = ("haydn", "mozart", "beethoven")
        tab = VGroup()
        tab.add(VGroup(label(r"", font_size=18), *[label(rf"called {n.title()}", font_size=18, color=GREY_A) for n in names]))
        for n in names:
            tab.add(VGroup(label(n.title(), font_size=20, color=WHITE), *[label(str(conf[n][m]), font_size=22, color=TUNE if n == m else GREY_B) for m in names]))
        for i, row in enumerate(tab):
            for k, cell in enumerate(row):
                cell.move_to([[-5.8, -3.9, -2.2, -0.5][k], 1.3 - 0.55 * i, 0])
        side = VGroup(*[label(s, font_size=22, color=c_) for s, c_ in (
            (rf"one genre, \ one city, \ one generation: \ {d['n']} quartet movements", WHITE),
            (rf"Part 24's twelve counterpoint features: \ {100 * d['acc24']:.0f} in 100", WHITE),
            (rf"eight Classical features: \ {100 * d['acc26']:.0f} in 100", TUNE),
            (rf"always guessing Mozart, \ the largest group: \ {100 * d['chance']:.0f} in 100", EAR),
            (rf"the best single feature: \ {d['singles'][0][0]} \ ({100 * d['singles'][0][1]:.0f})", GREY_A))]).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 6.4))
        side.move_to(RIGHT * 3.6 + DOWN * 0.1)
        with self.voiceover(
            "Part 24 ended with a demand: a fair attribution test, holding genre, place and time fixed. These quartets are "
            "exactly that. <bookmark mark='a'/> One genre, one city, one generation, thirty-three movements. "
            "<bookmark mark='b'/> First, Part 24's twelve features, built for sixteenth-century counterpoint: hidden one at "
            f"a time, the movements are attributed correctly {say(round(100 * d['acc24']))} times in a hundred. "
            "<bookmark mark='c'/> Then eight features built for this style: harmonic rhythm, periodic phrasing, cadence "
            f"rate, who leads, how often the lead changes, density, register span, accompaniment figures. "
            f"{say(round(100 * d['acc26']))} in a hundred. <bookmark mark='d'/> But always guessing Mozart, who has the "
            f"most movements, would score {say(round(100 * d['chance']))}. <bookmark mark='e'/> The table shows why: "
            "Beethoven is recognized two times in three, mostly by his register; Haydn and Mozart are confused with each "
            "other almost as often as not."
        ) as vo:
            self.play(FadeIn(tab))
            for mark, r in zip("abcde", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"thirty-three pieces is a small sample: \ a few movements either way change the score", WHITE),
            (r"the features are coarse: \ no themes, \ no harmony beyond chord changes, \ no dynamics", WHITE),
            (r"Haydn and Mozart wrote in one shared language, \ and learned from each other", TUNE),
            (r"what tells them apart for a listener \ (wit, \ melody, \ timing) \ is not yet a number", WHITE),
            (r"an honest result: \ style is easier to hear than to count", GREY_A),
        ]
        rows_scene(self, r"why it is hard", items,
                   "Why so hard? <bookmark mark='b'/> Partly the sample: thirty-three movements, so that a few either way "
                   "change the score. <bookmark mark='c'/> Partly the features, which know nothing of themes, harmony "
                   "beyond its rate of change, or dynamics. <bookmark mark='d'/> But mostly the music: Haydn and Mozart "
                   "wrote in one shared language and learned from each other; that was the point of the style. "
                   "<bookmark mark='e'/> What tells them apart for an experienced listener, the wit, the melodic shape, the "
                   "timing of a surprise, has not yet been turned into a number. <bookmark mark='f'/> The honest result is "
                   "that style, here, is easier to hear than to count.", marks="cdef")
