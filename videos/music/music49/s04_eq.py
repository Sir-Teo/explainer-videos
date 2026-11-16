from __future__ import annotations

import numpy as np

from videos.music.music49.common import *  # noqa: F403

NAMES = {"lowpass": (r"low-pass, \ 1 kHz", BLUE), "highpass": (r"high-pass, \ 1 kHz", EAR), "peak": (r"peak, \ 1 kHz, \ +9 dB", TUNE),
         "lowshelf": (r"low shelf, \ 200 Hz, \ +6 dB", GOLD), "highshelf": (r"high shelf, \ 5 kHz, \ +6 dB", "#A3E635")}


class Eq(SoundScene):
    def construct(self):
        chapter(self, 3, r"Equalizers", r"How do engineers shape a sound's colour?")
        self.shapes()
        self.quiz()
        self.analog()
        self.parametric()
        self.practice()

    # ------------------------------------------------------------------
    def shapes(self):
        d = load("biquads")
        f = d["f"]
        ax = logf_axes(width=9.0, height=3.6, flo=20, fhi=24000, ylo=-30, yhi=12, center=DOWN * 0.3 + LEFT * 1.2)
        cs = VGroup(*[curve(f, np.clip(d[k]["db"], -30, 12), ax.to, color=NAMES[k][1], width=3) for k in NAMES])
        key = VGroup(*[label(NAMES[k][0], font_size=17, color=NAMES[k][1]) for k in NAMES]).arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        yl = label(r"gain, \ dB", font_size=16, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        head = label(r"five biquads from the cookbook", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here are five biquads from the cookbook, drawn as gain against frequency. <bookmark mark='a'/> A low-pass at "
            "one kilohertz lets the lows through and rolls off the highs at twelve decibels an octave. <bookmark mark='b'/> A "
            "high-pass does the opposite. <bookmark mark='c'/> A peak lifts a band around one kilohertz by nine decibels. "
            "<bookmark mark='d'/> A low shelf raises everything below two hundred hertz, <bookmark mark='e'/> and a high shelf "
            "everything above five kilohertz. A studio equalizer is a few of these in series, with knobs for the frequency, "
            "the width and the gain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yl))
            for mark, c, k in zip("abcde", cs, key):
                vo.wait_until(mark)
                self.play(Create(c), FadeIn(k))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("eq")
        c = clip("eq.four")
        card = listen_card(r"A groove, \ dry. \ Then three times, \ each through one filter: \ a low-pass at 800 Hz, \ a high-pass at 2 kHz, \ "
                           r"and a 12 dB boost at 1 kHz, \ in some order. \ Which was which?", width=10.4)
        with self.voiceover(
            "Train your ears on them. A groove, dry. Then three times, each through one filter: a low-pass at eight hundred "
            "hertz, a high-pass at two kilohertz, and a twelve-decibel boost at one kilohertz, in some order. Which was which?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=2.6, height=1.1, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=22, color=WHITE)).arrange(ORIGIN)
                         for t in (r"dry", r"first", r"second", r"third")]).arrange(RIGHT, buff=0.5).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        keys = ["dry", "first", "second", "third"]
        with self.listen(c) as snd:
            window(snd, r"a groove, \ filtered", detail=r"Part 40's drums, \ bass, \ Part 7's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i < 3 else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        ans = VGroup(*[label(t, font_size=17, color=TUNE).next_to(boxes[i + 1], DOWN, buff=0.3) for i, t in enumerate([r"high-pass", r"+12 dB at 1 kHz", r"low-pass"])])
        with self.voiceover(
            "The first was the high-pass: no kick, no bass, only cymbals and the top of the piano, small and thin. The "
            "second was the boost: everything is there, but honky, as if through a cardboard tube. The third was the "
            "low-pass: warm and muffled, the cymbals gone dull."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def analog(self):
        d = load("biquads")
        rows_ = text_rows([
            (r"filters were first analogue circuits: \ capacitors, \ inductors, \ resistors, \ described by $H(s)$", WHITE),
            (r"Stephen Butterworth \ (1930): \ the flattest possible pass band, \ $|H|^2 = 1 / (1 + (\omega/\omega_c)^{2N})$", WHITE),
            (r"the bilinear transform maps the analogue filter to a digital one: \ $s = 2f_s\,(1 - z^{-1})/(1 + z^{-1})$", TUNE),
            (r"it squeezes the whole analogue frequency axis onto the circle, \ so the cutoff is prewarped to land in the right place", WHITE),
            (rf"our second-order Butterworth at 1 kHz matches SciPy's to {d['butter_match']:.0e}", GREY_A),
        ], font_size=22)
        head = label(r"analogue prototypes", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Most of these designs began as analogue circuits. <bookmark mark='a'/> Capacitors, inductors and resistors, "
            "described by a transfer function in s. <bookmark mark='b'/> Stephen Butterworth found in 1930 the filter with "
            "the flattest possible pass band. <bookmark mark='c'/> The bilinear transform maps an analogue filter to a digital "
            "one by substituting for s. <bookmark mark='d'/> It squeezes the whole infinite analogue frequency axis onto the "
            "circle, so the cutoff has to be prewarped to land in the right place. <bookmark mark='e'/> Our own second-order "
            "Butterworth at one kilohertz, built this way, matches SciPy's to within rounding."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def parametric(self):
        items = [
            (r"early equalizers had a few fixed frequencies and boosts, \ chosen by switches", WHITE),
            (r"George Massenburg \ (1972): \ the parametric equalizer, \ every band's frequency, \ width and gain continuously adjustable", WHITE),
            (r"the width is set by Q: \ the centre frequency over the bandwidth", WHITE),
            (r"a graphic equalizer instead fixes many narrow bands and gives each a slider", TUNE),
            (r"both are biquads in series, \ the cookbook's peak and shelf filters", GREY_A),
        ]
        rows_scene(self, r"the parametric equalizer", items,
                   "The studio equalizer has a short history. <bookmark mark='b'/> Early ones had a few fixed frequencies and boosts, chosen by switches. <bookmark mark='c'/> In 1972 George Massenburg described the parametric equalizer, in which every band's frequency, width and gain can be set continuously. <bookmark mark='d'/> The width is set by Q, the centre frequency divided by the bandwidth. <bookmark mark='e'/> A graphic equalizer instead fixes many narrow bands and gives each a slider. <bookmark mark='f'/> Digital equalizers can use biquads, while parallel, FIR and analog architectures also exist.", marks="bcdef")

    # ------------------------------------------------------------------
    def practice(self):
        items = [
            (r"cut before you boost: \ removing a mud band often helps more than lifting the rest", WHITE),
            (r"high-pass unwanted lows where useful; \ choose the cutoff for the source", WHITE),
            (r"a narrow cut can remove a resonance; \ a broad, \ gentle shelf changes a whole mix's colour", WHITE),
            (r"equalizing two instruments in complementary ways separates them \ (Part 41's masking)", TUNE),
            (r"Part 56 does this to a real mix", GREY_A),
        ]
        rows_scene(self, r"equalizing in practice", items,
                   "Engineers have rules of thumb. <bookmark mark='b'/> Cut before you boost: removing a muddy band often helps more than lifting the rest. <bookmark mark='c'/> High-pass unwanted low-frequency content where useful; select the cutoff by source and arrangement rather than applying one hundred hertz to everything. <bookmark mark='d'/> A narrow cut can remove a resonance; a broad, gentle shelf changes a whole mix's colour. <bookmark mark='e'/> And equalizing two instruments in complementary ways separates them, the masking of Part 41. <bookmark mark='f'/> Part 56 does this to a real mix.", marks="bcdef")
