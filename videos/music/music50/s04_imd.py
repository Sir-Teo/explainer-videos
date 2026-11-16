from __future__ import annotations

import numpy as np

from videos.music.music50.common import *  # noqa: F403


class Imd(SoundScene):
    def construct(self):
        chapter(self, 3, r"Intermodulation and the power chord", r"Why do rock guitarists play fifths?")
        self.idea()
        self.spectra()
        self.hear()
        self.difference()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"feed a shaper two tones, \ $f_1$ and $f_2$, \ and it makes their harmonics", WHITE),
            (r"and also tones at $m f_1 \pm n f_2$: \ sums and differences, \ intermodulation", WHITE),
            (r"if $f_1$ and $f_2$ are in a simple ratio, \ every new tone is a multiple of their common divisor", WHITE),
            (r"a fifth, \ 3 : 2, \ makes a harmonic series an octave below the lower note: \ one bigger chord", TUNE),
            (r"a major third, \ 5 : 4, \ makes one two octaves down, \ crowded with tones that clash with the chord", GREY_A),
        ]
        rows_scene(self, r"two tones in, \ many out", items,
                   "Now feed a shaper two tones at once. <bookmark mark='b'/> It makes the harmonics of each, <bookmark mark='c'/> "
                   "and also tones at their sums and differences, and the sums and differences of their harmonics: "
                   "intermodulation. <bookmark mark='d'/> If the two tones are in a simple ratio, every new tone is a multiple of "
                   "their common divisor. <bookmark mark='e'/> A fifth, three to two, makes a harmonic series an octave below the "
                   "lower note: the result is simply a bigger chord. <bookmark mark='f'/> A major third, five to four, makes a "
                   "series two octaves down, crowded with tones that clash.", marks="bcdef")

    # ------------------------------------------------------------------
    def spectra(self):
        d = load("imd")
        def panel(key, title, color):
            ax = frame_axes(width=5.4, height=2.8, xlo=0, xhi=1400, ylo=-45, yhi=0, center=ORIGIN)
            lines = VGroup()
            for f, v in d[key]["peaks"]:
                inp = abs(f - d[key]["f1"]) < 3 or abs(f - d[key]["f2"]) < 3
                lines.add(Line(ax.to(f, -45), ax.to(f, v), color=WHITE if inp else color, stroke_width=4 if inp else 3))
            ticks = VGroup(*[label(f"{v}", font_size=14, color=GREY_A).next_to(ax.to(v, -45), DOWN, buff=0.1) for v in (0, 500, 1000)])
            g = d[key]["gcd"]
            return VGroup(ax, lines, ticks, label(title, font_size=19, color=color).next_to(ax, UP, buff=0.2),
                          label(rf"every line a multiple of {g:.0f} Hz", font_size=16, color=GREY_A).next_to(ax, DOWN, buff=0.45))
        a = panel("fifth", r"a fifth: \ 220 and 330 Hz", TUNE)
        b = panel("third", r"a major third: \ 220 and 275 Hz", EAR)
        g = VGroup(a, b).arrange(RIGHT, buff=1.0).move_to(DOWN * 0.1)
        cap = label(r"white: \ the two tones going in; \ coloured: \ what the tanh shaper adds, \ within 45 dB", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"two tones through tanh", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Measure it. <bookmark mark='a'/> A fifth, two hundred and twenty and three hundred and thirty hertz, through the "
            "tanh shaper: every new line falls on a multiple of a hundred and ten, an octave below the lower note, a clean "
            "harmonic series. <bookmark mark='b'/> A major third, two hundred and twenty and two hundred and seventy-five: the "
            "new lines fall on multiples of fifty-five, including some that clash with the chord itself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(b))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("imd")
        c = clip("imd.two")
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.6, height=1.3, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=22, color=WHITE)).arrange(ORIGIN)
                         for t in (r"power chord: \ E, \ B, \ E", r"major chord: \ E, \ G$\sharp$, \ B, \ E")]).arrange(RIGHT, buff=1.0).move_to(UP * 0.3)
        cap = label(r"both through the same heavy distortion", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"the power chord, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear it on the guitar, through heavy distortion: a power chord, root, fifth and octave, then a full major chord. "
            "This power chord is clearer under the chosen distortion. Register, tuning and circuit matter, and distorted guitar also uses thirds and full chords."
        ):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two distorted chords", detail=r"Part 40's guitar", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["power"], st["major"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["major"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def difference(self):
        items = [
            (r"the strongest new tone is often the difference, \ $f_2 - f_1$", WHITE),
            (r"for a fifth on E and B, \ 82 and 123 Hz, \ it is 41 Hz: \ an E an octave below the root", WHITE),
            (r"so a distorted power chord sounds deeper and bigger than its notes", WHITE),
            (r"the ear makes a faint difference tone of its own, \ Tartini's tone \ (Part 4), \ from its own nonlinearity", TUNE),
            (r"intermodulation is also why distortion of a full mix sounds harsh: \ every pair of notes makes new ones", GREY_A),
        ]
        rows_scene(self, r"the difference tone", items,
                   "The strongest new tone is often the difference between the two. <bookmark mark='b'/> For a fifth on low E and B, "
                   "eighty-two and a hundred and twenty-three hertz, it is forty-one: an E an octave below the root. "
                   "<bookmark mark='c'/> So a distorted power chord sounds deeper and bigger than its notes. <bookmark mark='d'/> The "
                   "ear makes a faint difference tone of its own, Tartini's tone, from its own nonlinearity, as Part 4 described. "
                   "<bookmark mark='e'/> And intermodulation is why distorting a whole mix sounds harsh: every pair of notes makes "
                   "new ones.", marks="bcde")
