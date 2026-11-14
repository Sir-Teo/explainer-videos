from __future__ import annotations

import numpy as np

from videos.music.music33.common import *  # noqa: F403

LET = ["C", r"C$\sharp$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]


class Even(SoundScene):
    def construct(self):
        chapter(self, 2, r"One shape, \ rhythm and scale", r"What does a bell pattern have to do with a major scale?")
        self.same()
        self.maximal()
        self.layers()
        self.everywhere()

    # ------------------------------------------------------------------
    def same(self):
        d = load("even")
        c = clip("even.two")
        gb = necklace(d["bell"]["pattern"], radius=1.4, color=TUNE).move_to(LEFT * 3.2 + UP * 0.2)
        gp = necklace(d["pentatonic"]["pattern"], radius=1.4, color=BLUE).move_to(RIGHT * 3.2 + UP * 0.2)
        nb = VGroup(*[label(LET[o], font_size=17, color=TUNE).move_to(gb[0].get_center() + 1.75 * np.array([np.cos(PI / 2 - o * TAU / 12), np.sin(PI / 2 - o * TAU / 12), 0])) for o in d["bell"]["onsets"]])
        np_ = VGroup(*[label(LET[o], font_size=17, color=BLUE).move_to(gp[0].get_center() + 1.75 * np.array([np.cos(PI / 2 - o * TAU / 12), np.sin(PI / 2 - o * TAU / 12), 0])) for o in d["pentatonic"]["onsets"]])
        cap = VGroup(label(r"E(7, 12): \ gaps 2 2 1 2 2 2 1: \ the major scale", font_size=21, color=TUNE).next_to(gb, DOWN, buff=0.55),
                     label(r"E(5, 12): \ gaps 2 2 3 2 3: \ the pentatonic scale", font_size=21, color=BLUE).next_to(gp, DOWN, buff=0.55))
        head = label(r"twelve pulses, \ or twelve semitones", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Put the bell pattern's seven strokes round a clock of twelve, and read the clock as twelve semitones instead of "
            "twelve pulses. <bookmark mark='a'/> The strokes fall on C, D, E, F, G, A and B: the major scale. Its gaps, two, "
            "two, one, two, two, two, one, are the scale's tones and semitones. <bookmark mark='b'/> E of five, twelve gives "
            "the pentatonic scale, C, D, E, G, A. Both are rotations of the Euclidean necklaces. Listen: each rhythm on the clave, then the same positions played as notes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(gb), FadeIn(gp))
            vo.wait_until("a")
            self.play(FadeIn(nb), FadeIn(cap[0]))
            vo.wait_until("b")
            self.play(FadeIn(np_), FadeIn(cap[1]))
        with self.listen(c) as snd:
            window(snd, r"rhythm, \ then scale, \ twice", detail=r"Part 11's clave, \ Part 7's piano", corner=DL, tag_corner=DR)
            p = d["pulse"]
            for key, g, rk, sk in (("bell", gb, "bell", "diatonic"), ("pentatonic", gp, "five", "pentatonic")):
                ons = d[key]["onsets"]
                for cc in range(2):
                    for j, o in enumerate(ons):
                        t0 = d["starts"][rk] + (cc * 12 + o) * p
                        pulse(snd, g.dots[j], t0, t0 + p * 0.9, buff=0.04)
                for j, o in enumerate(ons):
                    t0 = d["starts"][sk] + o * p * 1.6
                    pulse(snd, g.dots[j], t0, t0 + p * 1.5, buff=0.04)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def maximal(self):
        items = [
            (r"Clough and Douthett \ (1991): \ maximally even sets", WHITE),
            (r"for any k and n there is exactly one maximally even shape, \ up to rotation", WHITE),
            (r"it is the Euclidean rhythm E(k, n): \ the same object, \ found twice", TUNE),
            (r"Part 12 found the diatonic scale maximally even; \ Part 32 found it the most even seven-note chord", WHITE),
            (r"Toussaint's surprise: \ many timelines of the world are this shape", GREY_A),
        ]
        rows_scene(self, r"maximal evenness", items,
                   "Music theory had already named the shape. <bookmark mark='b'/> In 1991 John Clough and Jack Douthett defined "
                   "maximally even sets: <bookmark mark='c'/> for any number of notes and any number of places there is exactly "
                   "one most even arrangement, up to rotation. <bookmark mark='d'/> It is the Euclidean rhythm: the same object, "
                   "found twice, once for scales and once for neutron pulses. <bookmark mark='e'/> Part 12 found the diatonic "
                   "scale maximally even, and Part 32 found it the most even seven-note chord. <bookmark mark='f'/> Toussaint's "
                   "surprise was that so many of the world's rhythmic timelines have the same shape.", marks="cdef")

    # ------------------------------------------------------------------
    def everywhere(self):
        items = [
            (r"leap years: \ 8 leap years in 33, \ spread evenly \ (the Persian calendar)", WHITE),
            (r"drawing a straight line on a pixel grid: \ Bresenham's algorithm, \ the same spacing", WHITE),
            (r"Sturmian words and the golden ratio: \ even spacing with an irrational rate", WHITE),
            (r"the same problem every time: \ k events in n slots, \ as smoothly as possible", TUNE),
            (r"chapter 3 runs it with an irrational step: \ the fifth", GREY_A),
        ]
        rows_scene(self, r"the same shape elsewhere", items,
                   "The shape turns up wherever things must be spread evenly. <bookmark mark='b'/> The Persian calendar spreads "
                   "eight leap years through thirty-three. <bookmark mark='c'/> A computer drawing a straight line on a grid of "
                   "pixels steps up at Euclidean intervals, by Bresenham's algorithm. <bookmark mark='d'/> With an irrational rate "
                   "the pattern never repeats: Sturmian words, and the golden ratio. <bookmark mark='e'/> It is always the same "
                   "problem: k events in n slots, as smoothly as possible. <bookmark mark='f'/> The next chapter runs it with an "
                   "irrational step, the perfect fifth.", marks="cdef")

    # ------------------------------------------------------------------
    def layers(self):
        d = load("layers")
        c = clip("layers.three")
        cols = [GREY_B, BLUE, TUNE]
        g = VGroup()
        for L, col in zip(d["layers"], cols):
            n = len(L["pattern"])
            row = VGroup(*[Square(0.42, stroke_color=DIM, stroke_width=1, fill_color=col if ch == "x" else BLACK, fill_opacity=0.9 if ch == "x" else 0) for ch in L["pattern"]]).arrange(RIGHT, buff=0.05)
            g.add(VGroup(label(L["name"], font_size=19, color=col), row).arrange(RIGHT, buff=0.4))
        g.arrange(DOWN, buff=0.35, aligned_edge=RIGHT).move_to(UP * 0.2)
        names = VGroup(label(r"E(3, 8), \ twice", font_size=17, color=GREY_A), label(r"E(5, 16)", font_size=17, color=GREY_A), label(r"E(7, 16)", font_size=17, color=GREY_A))
        for i in range(3):
            names[i].next_to(g[i], RIGHT, buff=0.3)
        head = label(r"layering Euclidean rhythms", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Layer three Euclidean rhythms over the same sixteen pulses: the tresillo twice on a low drum, five strokes on a "
            "woodblock, seven on a clave. Each layer is as even as it can be on its own; together they interlock, coinciding "
            "on the first pulse and drifting apart in between. Electronic musicians build grooves exactly this way. Listen, "
            "four times round."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(names))
        with self.listen(c) as snd:
            window(snd, r"three layers", detail=r"Part 9's drum, \ Part 11's kit", corner=DL, tag_corner=DR)
            p = d["pulse"]
            for cyc in range(4):
                for li, L in enumerate(d["layers"]):
                    for i, ch in enumerate(L["pattern"]):
                        if ch == "x":
                            t0 = (cyc * d["n"] + i) * p
                            pulse(snd, g[li][1][i], t0, t0 + p * 0.9, buff=0.02)
        self.wait(0.3)
        self.clear_scene()
