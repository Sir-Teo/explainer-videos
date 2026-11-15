from __future__ import annotations

import numpy as np

from videos.music.music50.common import *  # noqa: F403

KC = {"hard": (r"hard clip", EAR), "tanh": (r"tanh", TUNE), "cubic": (r"cubic soft clip", BLUE)}


class Shape(SoundScene):
    def construct(self):
        chapter(self, 1, r"Nonlinearity makes new frequencies", r"Where does distortion's sound come from?")
        self.rule()
        self.curves()
        self.harmonics_()
        self.three()
        self.fuzz()
        self.symmetry()
        self.devices()

    # ------------------------------------------------------------------
    def rule(self):
        items = [
            (r"a linear system can only change the level and timing of the frequencies it is given \ (Part 49)", WHITE),
            (r"a nonlinear one creates new frequencies", WHITE),
            (r"the simplest: \ a waveshaper, \ $y = f(x)$, \ sample by sample, \ with no memory", WHITE),
            (r"if $f$ bends, \ a pure tone comes out with harmonics: \ the bend is in the waveform, \ the harmonics in the spectrum", TUNE),
            (r"amplifiers driven too hard, \ tape saturated, \ valves and pedals all bend", GREY_A),
        ]
        rows_scene(self, r"new frequencies", items,
                   "Every effect in Part 49 was linear: it could change the level and timing of the frequencies it was given, and "
                   "nothing else. <bookmark mark='b'/> A nonlinear system creates new frequencies. <bookmark mark='c'/> The "
                   "simplest is a waveshaper: each output sample a fixed function of the input sample, with no memory. "
                   "<bookmark mark='d'/> If that function bends, a pure tone comes out with harmonics: the bend is in the "
                   "waveform, the harmonics in the spectrum. <bookmark mark='e'/> Amplifiers driven too hard, saturated tape, "
                   "valves and pedals all bend.", marks="bcde")

    # ------------------------------------------------------------------
    def curves(self):
        d = load("shapers")["curves"]
        ax = frame_axes(width=4.4, height=4.0, xlo=-1.5, xhi=1.5, ylo=-1.3, yhi=1.3, center=DOWN * 0.3)
        line = DashedLine(ax.to(-1.3, -1.3), ax.to(1.3, 1.3), color=GREY_B, stroke_width=1.5)
        cs = VGroup(*[curve(d["x"], d[k], ax.to, color=KC[k][1], width=3) for k in ("hard", "tanh", "cubic")])
        key = VGroup(*[label(KC[k][0], font_size=18, color=KC[k][1]) for k in ("hard", "tanh", "cubic")]).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.5)
        xl = label(r"input", font_size=16, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yl = label(r"output", font_size=16, color=GREY_A).next_to(ax, LEFT, buff=0.2)
        head = label(r"three ways to bend", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Three shapers. The dashed line is no shaping at all. <bookmark mark='a'/> A hard clip follows it until a limit, "
            "then flattens abruptly: the transistor or the digital ceiling. <bookmark mark='b'/> The hyperbolic tangent "
            "bends smoothly, like a valve. <bookmark mark='c'/> A cubic soft clip bends early and gently, and flattens at "
            "the top."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(line), FadeIn(xl), FadeIn(yl))
            for mark, c, k in zip("abc", cs, key):
                vo.wait_until(mark)
                self.play(Create(c), FadeIn(k))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def harmonics_(self):
        d = load("shapers")
        groups = VGroup()
        for i, k in enumerate(("hard", "tanh", "cubic")):
            g = harm_bars(d[k], width=0.26, gap=0.42, floor=-60, height=2.6, color=KC[k][1], x0=0, y0=0)
            groups.add(VGroup(g, label(KC[k][0], font_size=18, color=KC[k][1]).next_to(g, UP, buff=0.3)))
        groups.arrange(RIGHT, buff=0.9).move_to(DOWN * 0.3)
        cap = label(r"bars: \ harmonics 1 to 9 of a 1 kHz sine driven three times past the bend, \ dB re the fundamental, \ from -60", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"what each bend adds", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        h, t, q = d["hard"], d["tanh"], d["cubic"]
        with self.voiceover(
            "Drive a one-kilohertz sine three times past the bend and measure the harmonics. <bookmark mark='a'/> The hard clip: "
            f"the third at {say(h[2])} decibels, the fifth at {say(h[4])}, the seventh at {say(h[6])}. <bookmark mark='b'/> The "
            f"tanh: {say(t[2])}, {say(t[4])} and {say(t[6])}. <bookmark mark='c'/> The cubic: {say(q[2])}, {say(q[4])} and "
            f"{say(q[6])}, its upper harmonics falling slowest of the three. And all three add only odd harmonics: the second, "
            "fourth and sixth are missing entirely."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(ghost(VGroup(*groups), 0.25)))
            for mark, g in zip("abc", groups):
                vo.wait_until(mark)
                self.play(FadeIn(g))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fuzz(self):
        d = load("fuzz")
        c = clip("fuzz.two")
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.0, height=1.2, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=24, color=WHITE)).arrange(ORIGIN)
                         for t in (r"clean", r"driven")]).arrange(RIGHT, buff=1.6).move_to(UP * 0.6)
        notes = VGroup(*[Rectangle(width=1.6 * dd, height=0.12, stroke_width=0, fill_color=TUNE, fill_opacity=0.9).move_to([-3.6 + 2.6 * a + 0.8 * dd, -1.8 + 0.08 * (m - 40), 0]) for m, a, dd in d["riff"]])
        head = label(r"a riff, \ clean and driven", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear it on a guitar: a riff, clean, then through a hard-driven shaper and a loudspeaker's band limit."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(notes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"clean, \ then driven", detail=r"Part 40's guitar", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["clean"], st["fuzz"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["fuzz"], c.duration, buff=0.08)
            for key in ("clean", "fuzz"):
                flash(snd, list(notes), [st[key] + a for _, a, _ in d["riff"]], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def symmetry(self):
        items = [
            (r"a shaper that treats positive and negative alike, \ $f(-x) = -f(x)$, \ makes only odd harmonics", WHITE),
            (r"because an odd function of a cosine is a sum of odd cosines", WHITE),
            (r"make it lopsided, \ as a single valve or a biased transistor is, \ and even harmonics appear", WHITE),
            (r"the second harmonic is an octave: \ even distortion sounds `warm', \ odd distortion `edgy'", TUNE),
            (r"the shape of the bend is the timbre of the distortion", GREY_A),
        ]
        rows_scene(self, r"why only odd harmonics?", items,
                   "Why only odd harmonics? <bookmark mark='b'/> A shaper that treats positive and negative alike, an odd function, "
                   "makes only odd harmonics, <bookmark mark='c'/> because an odd function of a cosine is a sum of odd cosines. "
                   "<bookmark mark='d'/> Make it lopsided, as a single valve or a biased transistor is, and even harmonics appear. "
                   "<bookmark mark='e'/> The second harmonic is an octave, so even distortion is often called warm, and odd "
                   "distortion edgy. <bookmark mark='f'/> The shape of the bend is the timbre of the distortion.", marks="bcdef")

    # ------------------------------------------------------------------
    def devices(self):
        items = [
            (r"valves bend softly and lopsidedly: \ a rich second harmonic, \ then a gentle rounding", WHITE),
            (r"transistors and op-amps stay clean until they hit the rail, \ then clip hard", WHITE),
            (r"tape saturates gently and compresses as it goes, \ with a little high-frequency loss", WHITE),
            (r"fuzz pedals clip almost to a square wave; \ overdrives clip softly, \ often after a filter", TUNE),
            (r"each has a shape, \ and the shape is the sound", GREY_A),
        ]
        rows_scene(self, r"valves, \ transistors and tape", items,
                   "Each device has its own bend. <bookmark mark='b'/> Valves bend softly and lopsidedly, with a rich second "
                   "harmonic, then a gentle rounding. <bookmark mark='c'/> Transistors and op-amps stay clean until they hit their "
                   "supply rail, and then clip hard. <bookmark mark='d'/> Tape saturates gently and compresses as it goes, losing a "
                   "little of its top. <bookmark mark='e'/> Fuzz pedals clip almost to a square wave; overdrives clip softly, often "
                   "after a filter that shapes which frequencies distort. <bookmark mark='f'/> Each has a shape, and the shape is "
                   "the sound.", marks="bcdef")

    # ------------------------------------------------------------------
    def three(self):
        d = load("shapers3")
        c = clip("shapers3.three")
        cells = VGroup(*[VGroup(RoundedRectangle(width=3.2, height=1.2, corner_radius=0.15, stroke_color=KC[k][1]), label(KC[k][0], font_size=22, color=WHITE)).arrange(ORIGIN) for k in ("hard", "tanh", "cubic")]).arrange(RIGHT, buff=0.5).move_to(UP * 0.3)
        cap = label(r"one guitar note, \ driven five times into each, \ with no speaker filter to soften it", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"three bends, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the three bends on one guitar note, each driven five times past its knee, raw, with no loudspeaker to soften them."):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        keys = ["hard", "tanh", "cubic"]
        with self.listen(c) as snd:
            window(snd, r"three shapers", detail=r"Part 40's guitar", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i < 2 else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        with self.voiceover("The hard clip buzzes; the tanh is rounder; the cubic is the softest. Raw, all three are harsh: real amplifiers filter before and after the bend."):
            self.play(Indicate(cells[1], color=TUNE, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()
