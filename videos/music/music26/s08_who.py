from __future__ import annotations

import numpy as np

from videos.music.music26.common import *  # noqa: F403


class Who(SoundScene):
    def construct(self):
        chapter(self, 7, r"Who wrote this, \ fairly", r"Can a program tell Haydn from Mozart?")
        self.test()
        self.scatter()
        self.null()
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
    def scatter(self):
        d = load("style")
        X = np.array(d["X"])
        fi = d["features"].index("register span")
        fj = d["features"].index("cadences per bar")
        xs, ys = X[:, fi], 100 * X[:, fj]
        ax = Axes(x_range=[18, 42, 4], y_range=[0, 16, 4], x_length=7.6, y_length=4.4, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 18}).move_to(LEFT * 2.0 + DOWN * 0.4)
        xl = label(r"register span \ (semitones, \ lowest to highest note)", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        yl = label(r"cadences per 100 bars", font_size=18, color=GREY_A).next_to(ax.y_axis, UP, buff=0.2).shift(RIGHT * 0.8)
        col = {"haydn": BLUE, "mozart": TUNE, "beethoven": EAR}
        dots = {c: VGroup() for c in col}
        for x, y_, c in zip(xs, ys, d["y"]):
            dots[c].add(Dot(ax.c2p(x, y_), radius=0.07, color=col[c]))
        key = VGroup(*[label(n, font_size=22, color=col[c]) for c, n in (("haydn", r"Haydn"), ("mozart", r"Mozart"), ("beethoven", r"Beethoven"))]).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 4.6 + UP * 1.2)
        note = label(r"each dot: \ one movement", font_size=19, color=GREY_A).next_to(key, DOWN, buff=0.5)
        with self.voiceover(
            "Look at the two best single features together, one dot for each movement. Across, the register span, from the "
            "cello's lowest note to the first violin's highest. Up, the cadences the detector finds in a hundred bars. "
            "<bookmark mark='a'/> Haydn's movements. <bookmark mark='b'/> Mozart's, on top of them. <bookmark mark='c'/> "
            "And Beethoven's, spread to the right: he uses more of the instruments' range, and that is most of what the "
            "test can see. Haydn and Mozart occupy the same cloud."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(note))
            for mark, c in zip("abc", ("haydn", "mozart", "beethoven")):
                vo.wait_until(mark)
                self.play(LaggedStart(*[FadeIn(x_, scale=0.5) for x_ in dots[c]], lag_ratio=0.08), FadeIn(key[("haydn", "mozart", "beethoven").index(c)]), run_time=1.4)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def null(self):
        d = load("style")
        n = len(d["y"])
        counts = np.bincount(np.round(np.array(d["null"]) * n).astype(int), minlength=n + 1)
        ks = list(range(4, 25))
        real = int(round(d["acc26"] * n))
        bars = columns([counts[k] for k in ks], [str(k) if k % 2 == 0 else "" for k in ks], width=8.4, height=2.8, color=GREY_B,
                       hot=(ks.index(real),), hot_color=TUNE, font_size=16)
        bars.move_to(LEFT * 1.8 + DOWN * 0.3)
        t = label(r"movements attributed correctly, \ out of 33: \ 2000 shuffles of the composers' names", font_size=19, color=GREY_A).next_to(bars, UP, buff=0.35)
        side = VGroup(*[label(s, font_size=22, color=c_) for s, c_ in (
            (rf"shuffled: \ about {np.mean(d['null']) * n:.0f} right", GREY_A),
            (rf"real names: \ {real} right", TUNE),
            (rf"as good by luck: \ {100 * d['p_perm']:.0f} in 100", WHITE),
            (r"real information, \ but not much", EAR))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 4.2))
        side.move_to(RIGHT * 4.6 + DOWN * 0.2)
        with self.voiceover(
            "Is the test then learning nothing? The standard way to ask is to shuffle the names. Give the thirty-three "
            "movements their composers' names at random, run the same test, and count the hits; do it two thousand times. "
            f"<bookmark mark='a'/> With shuffled names the test gets about {say(round(np.mean(d['null']) * n))} right, by luck. "
            f"<bookmark mark='b'/> With the real names it gets {say(real)}. <bookmark mark='c'/> Only about "
            f"{say(round(100 * d['p_perm']))} shuffles in a hundred do as well. <bookmark mark='d'/> So the features carry "
            "real information about the composer, though less than a trivial rule that always says Mozart: two different "
            "questions, and both answers are true."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            for mark, r in zip("abcd", side):
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
