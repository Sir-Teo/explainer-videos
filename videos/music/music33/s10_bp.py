from __future__ import annotations

import numpy as np

from videos.music.music33.common import *  # noqa: F403


class Bp(SoundScene):
    def construct(self):
        chapter(self, 9, r"A scale without octaves", r"What if the octave were not special?", extra=((1972, r"Bohlen"),))
        self.idea()
        self.hear()
        self.why()
        self.since()

    # ------------------------------------------------------------------
    def idea(self):
        d = load("bp")
        rows_ = text_rows([
            (rf"Heinz Bohlen \ (1972), \ Kees van Prooijen, \ John Pierce \ (1980s): \ divide 3:1, \ the `tritave', \ into 13 equal steps", WHITE),
            (rf"each step: \ {d['step_cents']:.1f} cents; \ the tritave: \ {d['tritave_cents']:.1f} cents", WHITE),
            (r"its consonances use only odd numbers: \ 3:5:7 is its major triad", TUNE),
            (rf"9/7 within {abs(d['ratios']['9/7']['error']):.1f} cents, \ 7/5 within {abs(d['ratios']['7/5']['error']):.1f}, \ 5/3 within {abs(d['ratios']['5/3']['error']):.1f}", WHITE),
            (r"it fits tones whose partials are odd harmonics: \ the clarinet's low register \ (Part 8)", GREY_A),
        ], font_size=23)
        head = label(r"the Bohlen--Pierce scale", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Most tunings discussed so far have used octave repetition. What if it were not? <bookmark mark='a'/> In 1972 Heinz "
            "Bohlen, and independently Kees van Prooijen and John Pierce, divided the ratio three to one, an octave and a "
            "fifth, the tritave, into thirteen equal steps. <bookmark mark='b'/> Each step is about one hundred and forty-six "
            "cents. <bookmark mark='c'/> Its consonances are built only from odd numbers: three, five, seven is its major "
            "triad. <bookmark mark='d'/> And the steps approximate those ratios well: nine sevenths within four cents, seven "
            "fifths within three. <bookmark mark='e'/> It suits tones with only odd harmonics, like a clarinet's low register "
            "from Part 8, whose odd-harmonic spectrum changes the usual partial-overlap advantage of the octave."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("bp")
        c = clip("bp.three")
        step = d["step_cents"]
        ax = VGroup()
        L = 10.0
        line = Line(LEFT * L / 2, RIGHT * L / 2, color=GREY_B).move_to(UP * 0.9)
        ticks = VGroup()
        for k in range(14):
            x = -L / 2 + L * k * step / d["tritave_cents"]
            ticks.add(VGroup(Line([x, 0.75, 0], [x, 1.05, 0], color=TUNE, stroke_width=3), label(str(k), font_size=15, color=GREY_A).move_to([x, 0.5, 0])))
        oct_x = -L / 2 + L * 1200 / d["tritave_cents"]
        octave = VGroup(DashedLine([oct_x, 0.6, 0], [oct_x, 1.4, 0], color=EAR), label(r"octave: \ falls between steps 8 and 9", font_size=16, color=EAR).move_to([oct_x, 1.65, 0]))
        cells = VGroup(label(r"the 13 steps, \ odd harmonics", font_size=22, color=TUNE), label(r"3:5:7 on odd harmonics", font_size=22, color=WHITE),
                       label(r"3:5:7 on all harmonics", font_size=22, color=GREY_A)).arrange(RIGHT, buff=1.0).move_to(DOWN * 1.0)
        head = label(r"one tritave in 13 equal steps", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            'Here is the scale, thirteen steps from G up to the D an octave and a fifth higher, on a synthetic tone of odd harmonics only. Notice there is no octave: it falls between the eighth and ninth steps. Then the three, five, seven chord, first on odd harmonics, where it sounds settled, then on tones with all harmonics, where the added partials change the interactions and perceived quality.'
        ):
            self.play(FadeIn(head), FadeIn(line), FadeIn(ticks), FadeIn(octave), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"Bohlen--Pierce", kind="synthesized", detail=r"additive tones", corner=DL, tag_corner=DR)
            for k in range(14):
                pulse(snd, ticks[k][0], d["starts"]["scale"] + k * 0.3, d["starts"]["scale"] + k * 0.3 + 0.28, buff=0.05)
            pulse(snd, cells[0], d["starts"]["scale"], d["starts"]["odd"] - 0.4, buff=0.08)
            pulse(snd, cells[1], d["starts"]["odd"], d["starts"]["all"] - 0.4, buff=0.08)
            pulse(snd, cells[2], d["starts"]["all"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"Part 5: \ consonance depends on the timbre's partials, \ not only on the ratios", WHITE),
            (r"for odd-harmonic tones the octave's partials do not line up well; \ the tritave's do", WHITE),
            (r"Mathews, \ Pierce and colleagues \ (late 1980s): \ listening tests found its chords heard as consonant", WHITE),
            (r"the octave is a fact about harmonic timbres, \ not a law of music", TUNE),
            (r"Part 52 builds timbres to fit any tuning", GREY_A),
        ]
        rows_scene(self, r"why it works", items,
                   "Why does it work at all? <bookmark mark='b'/> Part 5 showed that consonance depends on a timbre's partials, not only on the ratio. <bookmark mark='c'/> For tones with only odd harmonics the octave's partials do not line up well, while the tritave's do. <bookmark mark='d'/> Max Mathews, John Pierce and colleagues ran listening tests in the late 1980s and found its chords heard as consonant, especially on odd-harmonic tones. <bookmark mark='e'/> Timbre affects consonance; octave equivalence also involves perception, learning and musical practice, so this does not derive or abolish it. <bookmark mark='f'/> Part 52 builds timbres to fit any tuning.", marks="cdef")

    # ------------------------------------------------------------------
    def since(self):
        items = [
            (r"BP clarinets: \ instruments built for the scale \ (Stephen Fox, \ 2000s)", WHITE),
            (r"Georg Hajdu, \ Elaine Walker and others compose for it", WHITE),
            (r"symposia on the scale \ (Boston, \ 2010)", WHITE),
            (r"its Lambda mode, \ 9 of the 13 steps, \ plays the role of the diatonic", TUNE),
            (r"a small repertory, \ and a test of how much of tonality is learned", GREY_A),
        ]
        rows_scene(self, r"Bohlen--Pierce since", items,
                   "The scale has a small life of its own. <bookmark mark='b'/> Clarinets built for it, the BP clarinets, were made by Stephen Fox in the 2000s. <bookmark mark='c'/> Composers including Georg Hajdu and Elaine Walker have written for it. <bookmark mark='d'/> A symposium on the scale was held in Boston in 2010. <bookmark mark='e'/> Its Lambda mode, nine of the thirteen steps, plays the role the diatonic scale plays in ours. <bookmark mark='f'/> A small repertory, and a fine test of how much of tonality is learned.", marks="cdef")
