from __future__ import annotations

import numpy as np

from videos.music.music52.common import *  # noqa: F403

RC = {"1:1": TUNE, "1:2": BLUE, "1:1.4": EAR, "1:3.5": GOLD}
RNOTE = {"1:1": r"every harmonic of 220", "1:2": r"odd harmonics only: \ hollow", "1:1.4": r"5 : 7: \ a 44 Hz fundamental, \ heard as none",
         "1:3.5": r"2 : 7: \ harmonics of 110, \ sparse"}


class Ratios(SoundScene):
    def construct(self):
        chapter(self, 2, r"Ratios, \ indices and Chowning's instruments", r"What decides whether FM sounds like a horn or a bell?")
        self.ratios()
        self.reflect()
        self.heard()
        self.instruments()
        self.chowning_heard()
        self.why()

    # ------------------------------------------------------------------
    def ratios(self):
        d = load("ratios")
        rows = VGroup()
        for name, lines in d["lines"].items():
            ax = frame_axes(width=7.0, height=0.75, xlo=0, xhi=3000, ylo=0, yhi=0.7)
            st = stems([f for f, _ in lines], [a for _, a in lines], ax.to, color=RC[name], r=0.035)
            rows.add(VGroup(label(rf"$f_c : f_m = {name.replace(':', ' : ')}$", font_size=18, color=RC[name]).set_width(2.2), VGroup(ax, st),
                            label(RNOTE[name], font_size=15, color=GREY_A)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 0.2)
        cap = label(r"carrier 220 Hz, \ index 3; \ lines up to 3 kHz", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.3)
        head = label(r"the ratio decides the series", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "The index sets how bright; the ratio of carrier to modulator sets which lines. <bookmark mark='a'/> At one to one the lines fall on every harmonic of the carrier. <bookmark mark='b'/> At one to two, on the odd harmonics only, the hollow series of the clarinet. <bookmark mark='c'/> At one to one point four, which is five to seven, they are harmonics of forty-four hertz, so far below the note that no fundamental is heard: the lines sound inharmonic, a bell. <bookmark mark='d'/> At one to three point five, two to seven, they are sparse harmonics of a hundred and ten. The rule: write the ratio as whole numbers N one to N two, in lowest terms, the line-grid spacing is the carrier over N one; cancellations and hearing can change the apparent fundamental."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(ghost(rows, 0.25)))
            for mark, rr in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reflect(self):
        ax = frame_axes(width=10.0, height=2.2, xlo=-700, xhi=1400, ylo=0, yhi=1.0, center=DOWN * 0.3)
        zero = DashedLine(ax.to(0, 0), ax.to(0, 1.0), color=WHITE, stroke_width=1.5)
        neg = [(-88.0, 0.34), (-396.0, 0.49), (-704.0, 0.31)]          # |J_k(3)| for k = -1, -2, -3
        pos = [(220.0, 0.26), (528.0, 0.34), (836.0, 0.49), (1144.0, 0.31)]  # k = 0, 1, 2, 3
        sn = stems([f for f, _ in neg], [a for _, a in neg], ax.to, color=GREY_A, r=0.05)
        sp = stems([f for f, _ in pos], [a for _, a in pos], ax.to, color=EAR, r=0.05)
        sf = stems([88.0, 396.0, 704.0], [0.34, 0.49, 0.31], ax.to, color=BLUE, r=0.05)
        arrows = VGroup(*[CurvedArrow(ax.to(f, a + 0.1), ax.to(-f, a + 0.1), color=BLUE, angle=-PI / 3, stroke_width=2) for f, a in neg])
        xl = VGroup(*[label(f"{v}", font_size=14, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.1) for v in (-500, 0, 500, 1000)])
        notes = VGroup(label(r"lower sidebands below zero hertz", font_size=17, color=GREY_A),
                       label(r"fold back to positive frequencies, \ with their sign flipped", font_size=17, color=BLUE),
                       label(r"where they land between the upper ones, \ and the series is no longer simple", font_size=17, color=WHITE)).arrange(DOWN, buff=0.15).to_edge(UP, buff=1.0)
        head = label(r"sidebands below zero", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Where do the bell's lines between the others come from? <bookmark mark='a'/> With the modulator larger than the "
            "carrier, the lower sidebands, carrier minus k modulators, go below zero hertz. <bookmark mark='b'/> A sine at a "
            "negative frequency is the same as one at the positive frequency with its sign flipped, so they fold back. "
            "<bookmark mark='c'/> They land between the upper sidebands, and where two land on the same line their amplitudes "
            "add or cancel. That folding, at zero hertz rather than at the Nyquist frequency, makes FM's richest spectra."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(zero), FadeIn(xl), FadeIn(sp))
            vo.wait_until("a")
            self.play(FadeIn(sn), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(a_) for a_ in arrows], lag_ratio=0.2), FadeIn(sf), FadeIn(notes[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("ratios")
        c = clip("ratios.three")
        cells = choice_boxes([r"1 : 1", r"1 : 2", r"1 : 1.4"], width=3.0, buff=0.7, colors=[TUNE, BLUE, EAR]).move_to(UP * 0.4)
        cap = label(r"a 220 Hz carrier, \ index 3 under an envelope", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"three ratios, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear three of them: one to one, one to two, and one to one point four."):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        names = ["r11", "r12", "r114"]
        with self.listen(c) as snd:
            window(snd, r"three ratios", kind="synthesized", detail=r"two sines each", corner=DL, tag_corner=DR)
            for i, k in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        with self.voiceover(
            "One to one is bright and reedy, like a muted brass. One to two is hollow, a clarinet's cousin. One to one point four sounds less clearly pitched in this example: a metallic clang. Same index, same two oscillators; only the ratio changed."
        ):
            self.play(Indicate(cells[2], color=EAR, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def instruments(self):
        d = load("chowning")
        e = np.array(d["env"])
        tt = np.arange(len(e)) * 240 / 48000
        cells = VGroup()
        for name, ratio, txt, ys, col in ((r"brass", r"1 : 1", r"index follows the envelope: \ louder is brighter", e, TUNE),
                                           (r"bell", r"1 : 1.4", r"index dies with the note: \ the highs fade first", np.exp(-tt / 1.6 * 4), EAR),
                                           (r"drum", r"80 : 55 Hz", r"index 25, \ dying in 20 ms: \ a burst, \ then a thud", np.exp(-tt / 0.02 * 2), BLUE)):
            ax = frame_axes(width=3.2, height=1.3, xlo=0, xhi=tt[-1], ylo=0, yhi=1.05)
            cells.add(VGroup(label(name, font_size=22, color=col), label(ratio, font_size=17, color=WHITE), VGroup(ax, curve(tt, ys, ax.to, color=col, width=2.5)),
                             label(txt, font_size=15, color=GREY_A)).arrange(DOWN, buff=0.22))
        cells.arrange(RIGHT, buff=0.6).move_to(DOWN * 0.1)
        il = label(r"each curve: \ the modulation index over the note", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"Chowning's instruments \ (1973)", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Chowning's paper did not stop at spectra; it made instruments, by moving the index through each note. "
            "<bookmark mark='a'/> Brass: one to one, with the index following the loudness envelope, so the note brightens as "
            "it swells, which is what Risset had measured on real trumpets. <bookmark mark='b'/> A bell: one to one point "
            "four, the index dying with the note, so the high lines fade first. <bookmark mark='c'/> And a drum: an inharmonic "
            "ratio, eighty to fifty-five hertz, with an index of twenty-five that decays with a twenty-millisecond time constant: a burst of "
            "noise-like sidebands, then a thud."
        ) as vo:
            self.play(FadeIn(head), FadeIn(il), FadeIn(ghost(cells, 0.3)))
            for mark, cc in zip("abc", cells):
                vo.wait_until(mark)
                self.play(FadeIn(cc), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chowning_heard(self):
        d = load("chowning")
        c = clip("chowning.three")
        cells = choice_boxes([r"brass", r"bell", r"drum"], width=3.0, buff=0.7, colors=[TUNE, EAR, BLUE]).move_to(UP * 0.4)
        head = label(r"three instruments from two oscillators, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Here they are: four notes of brass, a bell, and four drum strokes, all from two sine oscillators."):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        names = ["brass", "bell", "drum"]
        with self.listen(c) as snd:
            window(snd, r"Chowning's three", kind="synthesized", detail=r"two sines each", corner=DL, tag_corner=DR)
            for i, k in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        with self.voiceover(
            "None is a convincing copy of the real thing; each catches a few useful perceptual cues: brass that brightens "
            "as it swells, a bell whose overtones die before its hum, a drum's burst and thud. That is FM's character: cheap, "
            "expressive, and slightly unreal."
        ):
            self.play(Indicate(cells[0], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"subtractive synthesis moves brightness with a filter; \ FM moves it with the index", WHITE),
            (r"the filter takes away smoothly; \ the index adds sidebands that wobble in and out \ (the Bessel ripples)", WHITE),
            (r"so FM is hard to program by ear: \ small changes of ratio or index can change everything", WHITE),
            (r"but it is exact, \ cheap, \ and stable in tune: \ no drifting circuits", WHITE),
            (r"by 1983 that was enough to make it the sound of the decade", TUNE),
        ]
        rows_scene(self, r"FM against the filter", items,
                   "Compare FM with the last part's synthesizer. <bookmark mark='b'/> Subtractive synthesis moves brightness with a "
                   "filter; FM moves it with the index. <bookmark mark='c'/> The filter takes away smoothly; the index adds "
                   "sidebands that wobble in and out, the Bessel ripples. <bookmark mark='d'/> So FM is hard to program by ear: a "
                   "small change of ratio or index can change everything. <bookmark mark='e'/> But it is exact, cheap, and stable in "
                   "tune, with no drifting circuits. <bookmark mark='f'/> By 1983 that was enough to make it the sound of the "
                   "decade.", marks="bcdef")
