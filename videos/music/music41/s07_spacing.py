from __future__ import annotations

import numpy as np

from videos.music.music41.common import *  # noqa: F403

NN = ["C", r"C$\sharp$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]


class Spacing(SoundScene):
    def construct(self):
        chapter(self, 6, r"Spacing", r"Why are low notes spread wide and high notes close together?")
        self.series()
        self.hear()
        self.numbers()
        self.layers()
        self.rules()

    # ------------------------------------------------------------------
    def series(self):
        ks = list(range(1, 11))
        dots = VGroup()
        for k in ks:
            y = -2.4 + 1.5 * np.log2(k)
            dots.add(VGroup(Dot([0, y, 0], radius=0.09, color=TUNE), label(rf"{k}", font_size=16, color=GREY_A).move_to([-0.5, y, 0])))
        gaps = VGroup()
        for a, b, txt in ((1, 2, r"an octave"), (2, 3, r"a fifth"), (3, 4, r"a fourth"), (4, 5, r"a major third"), (5, 6, r"a minor third")):
            ya, yb = -2.4 + 1.5 * np.log2(a), -2.4 + 1.5 * np.log2(b)
            gaps.add(label(txt, font_size=16, color=WHITE).move_to([1.4, (ya + yb) / 2, 0], aligned_edge=LEFT))
        g = VGroup(dots, gaps).move_to(LEFT * 3.0 + DOWN * 0.1)
        side = VGroup(label(r"the harmonic series: \ wide intervals at the bottom, \ close ones at the top", font_size=20, color=WHITE),
                      label(r"orchestrators voice chords the same way: \ octaves and fifths in the bass, \ thirds above", font_size=20, color=TUNE),
                      label(r"a chord spaced like the series sounds like one rich tone", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(RIGHT * 2.8)
        head = label(r"the harmonic series as a guide to spacing", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Part 1's harmonic series is also a guide to spacing. <bookmark mark='a'/> Its intervals are wide at the bottom, "
            "an octave, then a fifth, a fourth, and close at the top, thirds and smaller. <bookmark mark='b'/> Orchestrators "
            "voice chords the same way, octaves and fifths in the bass, thirds above, and a chord spaced like the series "
            "sounds like one rich tone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(gaps), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("spacing")
        c = clip("spacing.three")
        cols = VGroup()
        for name, notes in d["voicings"].items():
            stack = VGroup(*[label(NN[m % 12] + str(m // 12 - 1), font_size=20, color=WHITE) for m in reversed(notes)]).arrange(DOWN, buff=0.15)
            cols.add(VGroup(label(name, font_size=20, color=TUNE), stack).arrange(DOWN, buff=0.3))
        cols.arrange(RIGHT, buff=1.6).move_to(UP * 0.3)
        with self.voiceover(
            "Hear one C major chord three ways on string sections: close and low, C, E, G in the cellos' low register; open, "
            "C, G and E spread over two octaves; and close and high, in the violins."
        ):
            self.play(FadeIn(cols))
        with self.listen(c) as snd:
            window(snd, r"three spacings", kind="synthesized", detail=r"additive string sections", corner=DL, tag_corner=DR)
            for k, name in enumerate(d["voicings"]):
                t0 = d["starts"][name]
                pulse(snd, cols[k], t0, t0 + 2.3, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def numbers(self):
        d = load("spacing")
        r = d["roughness"]
        mx = max(r.values())
        bars = VGroup()
        for i, (name, v) in enumerate(r.items()):
            w = 6.0 * v / mx
            bars.add(VGroup(label(name, font_size=20, color=WHITE).move_to([-2.4, 1.0 - 0.9 * i, 0], aligned_edge=RIGHT),
                            Rectangle(width=w, height=0.45, stroke_width=0, fill_color=EAR, fill_opacity=0.85).move_to([-2.1 + w / 2, 1.0 - 0.9 * i, 0]),
                            label(f"{v:.2f}", font_size=18, color=WHITE).move_to([-2.1 + w + 0.4, 1.0 - 0.9 * i, 0])))
        cap = label(r"Part 5's sensory roughness, \ computed from the measured string partials", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"roughness of the three spacings", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Part 5 explains why. Compute the sensory roughness of each chord from the strings' measured partials. "
            f"<bookmark mark='a'/> Close and low is the roughest, {r['close, low']:.2f}: low thirds put partials within a "
            f"critical band of each other. Spread open, the roughness falls to {r['open']:.2f}, and the same close chord "
            f"high up is smoothest of all, {r['close, high']:.2f}, because critical bands are wider in semitones at the "
            "bottom of hearing. Low thirds sound muddy for a reason the ear's filters explain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rules(self):
        items = [
            (r"the `low interval limit': \ below about C3, \ avoid thirds; \ use octaves and fifths", WHITE),
            (r"the outer voices carry the chord: \ bass and melody, \ with the inner parts filling between", WHITE),
            (r"spacing changes colour: \ the same notes, \ close or open, \ are different sounds", WHITE),
            (r"Part 17's voicing rules for choirs, \ rediscovered with instruments", TUNE),
            (r"chapter 7: \ how parts are arranged in time, \ textures", GREY_A),
        ]
        rows_scene(self, r"rules of spacing", items,
                   "From this come rules of spacing. <bookmark mark='b'/> Below about C three, avoid thirds and use octaves and "
                   "fifths: arrangers call it the low interval limit. <bookmark mark='c'/> The outer voices carry the chord, bass "
                   "and melody, with the inner parts filling between. <bookmark mark='d'/> And spacing changes colour: the same "
                   "notes, close or open, are different sounds. <bookmark mark='e'/> These are Part 17's voicing rules for choirs, "
                   "rediscovered with instruments. <bookmark mark='f'/> Chapter seven turns to how parts are arranged in time.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def layers(self):
        items = [
            (r"an orchestral texture is usually layered by register: \ bass, \ middle harmony, \ melody, \ high colour", WHITE),
            (r"each layer gets its own instruments: \ the ear separates them as Part 45's streams", WHITE),
            (r"gaps between layers keep the texture clear; \ crowding a register muddies it", WHITE),
            (r"the same lesson as the harmonic series: \ space at the bottom, \ density at the top", TUNE),
            (r"chapter 7 turns to how the layers move in time", GREY_A),
        ]
        rows_scene(self, r"registral layers", items,
                   "Spacing also works on a larger scale. <bookmark mark='b'/> An orchestral texture is usually layered by register: a bass, a middle harmony, a melody, a high colour. <bookmark mark='c'/> Each layer gets its own instruments, and the ear separates them as streams, Part 45's subject. <bookmark mark='d'/> Gaps between layers keep the texture clear, and crowding one register muddies it. <bookmark mark='e'/> It is the harmonic series' lesson again: space at the bottom, density at the top. <bookmark mark='f'/> Chapter seven turns to how the layers move in time.", marks="cdef")
