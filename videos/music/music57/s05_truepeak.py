from __future__ import annotations

import numpy as np

from videos.music.music57.common import *  # noqa: F403


class TruePeak(SoundScene):
    def construct(self):
        chapter(self, 4, r"Inter-sample peaks", r"Can a signal go over full scale without a single sample doing so?")
        self.sine()
        self.measure()
        self.master_overs()
        self.why()
        self.converters()

    # ------------------------------------------------------------------
    def sine(self):
        d = load("truepeak")
        ax = frame_axes(width=10.4, height=3.6, xlo=0, xhi=16, ylo=-1.6, yhi=1.6, center=DOWN * 0.4)
        fs = VGroup(DashedLine(ax.to(0, 1), ax.to(16, 1), color=RED, stroke_width=2), DashedLine(ax.to(0, -1), ax.to(16, -1), color=RED, stroke_width=2))
        fsl = label(r"full scale", font_size=15, color=RED).next_to(ax.to(16, 1), RIGHT, buff=0.1)
        cont = VMobject(stroke_color=TUNE, stroke_width=3).set_points_smoothly([ax.to(x, v) for x, v in zip(d["fine_t"], d["fine"])])
        st = stems(list(range(16)), d["samples"], ax.to, color=WHITE, r=0.07)
        note = label(rf"a sine at a quarter of the sample rate, \ sampled 45$^\circ$ off its peaks: \ every sample at full scale, \ the wave {d['sine_tp']:.1f} dB above \ (exactly +3.01)", font_size=17, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"a peak between the samples", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Can a signal go over full scale when no sample does? <bookmark mark='a'/> Take a sine at a quarter of the sample "
            "rate, sampled forty-five degrees away from its peaks, and scale it so that every sample sits exactly at full "
            "scale. A sample-peak meter reads nought. <bookmark mark='b'/> But the samples stand for a continuous wave, the one "
            "a converter will rebuild, and that wave peaks three decibels higher, between the samples. An inter-sample peak."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(fs), FadeIn(fsl), FadeIn(ghost(cont, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(st))
            vo.wait_until("b")
            self.play(Create(cont), FadeIn(note), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measure(self):
        items = [
            (r"BS.1770's true-peak meter: \ oversample 4 times \ (a low-pass interpolator), \ then take the largest value", WHITE),
            (r"at 48 kHz this catches inter-sample peaks to within about half a decibel", WHITE),
            (r"the unit: \ dBTP, \ decibels relative to full scale, \ true peak", WHITE),
            (r"Monochord's meter oversamples with a polyphase filter; \ it agrees with ffmpeg's to a tenth of a decibel", TUNE),
        ]
        rows_scene(self, r"measuring the true peak", items,
                   "So the standard measures the true peak. <bookmark mark='b'/> Oversample by four, with a low-pass "
                   "interpolating filter, and take the largest value. <bookmark mark='c'/> At forty-eight kilohertz that catches "
                   "inter-sample peaks to within about half a decibel. <bookmark mark='d'/> The unit is the dBTP, decibels relative "
                   "to full scale, true peak. <bookmark mark='e'/> Monochord's meter oversamples with a polyphase filter, and agrees "
                   "with ffmpeg's to a tenth.", marks="bcde")

    # ------------------------------------------------------------------
    def master_overs(self):
        d = load("truepeak")
        rows = VGroup(VGroup(label(r"master", font_size=17, color=GREY_A), label(r"loudness", font_size=17, color=GREY_A), label(r"sample peak", font_size=17, color=GREY_A), label(r"true peak", font_size=17, color=GREY_A)))
        for nm, v, col in ((r"clipped at $-0.1$ dBFS", d["clipped"], EAR), (r"look-ahead limiter, \ $-1$ dBTP", d["limited"], TUNE)):
            rows.add(VGroup(label(nm, font_size=19, color=col), label(rf"{v['lufs']:.1f} LUFS", font_size=19, color=WHITE), label(rf"{v['sample']:.1f} dBFS", font_size=19, color=WHITE),
                            label(rf"{v['true']:+.1f} dBTP", font_size=19, color=col)))
        rows.arrange(DOWN, buff=0.45)
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(-4.2 + 3.0 * i)
        rows.move_to(UP * 0.2)
        note = label(r"a clipped master's flat tops are corners, \ and corners ring between the samples when the wave is rebuilt", font_size=17, color=WHITE).to_edge(DOWN, buff=0.6)
        head = label(r"overs in a real master", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "This is not a curiosity. <bookmark mark='a'/> Push our mix to about minus seven LUFS by clipping its samples at "
            f"minus nought point one: every sample is legal, and the true peak is plus {say(d['clipped']['true'], 1)} dBTP. "
            "Flat tops are corners, and corners ring between the samples when the wave is rebuilt. <bookmark mark='b'/> "
            "Monochord's limiter, which watches the oversampled signal, holds the true peak at minus one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(note))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"a converter that rebuilds a wave above full scale clips in its analogue stage: \ distortion on playback", WHITE),
            (r"sample-rate conversion rebuilds the wave too, \ and lands new samples on the peaks", WHITE),
            (r"lossy codecs \ (Part 58) \ change the waveform; \ their decoded peaks overshoot by a decibel or more", WHITE),
            (r"so delivery specifications ask for $-1$ dBTP, \ or $-2$ for low bit rates: \ room for the wave to be rebuilt", TUNE),
        ]
        rows_scene(self, r"why it matters", items,
                   "Why does it matter? <bookmark mark='b'/> A converter that rebuilds a wave above full scale clips in its analogue "
                   "stage: distortion on playback that no meter in the studio showed. <bookmark mark='c'/> Sample-rate conversion "
                   "rebuilds the wave too, and lands new samples on the peaks. <bookmark mark='d'/> And lossy codecs, the subject of "
                   "Part 58, change the waveform, and their decoded peaks overshoot by a decibel or more. <bookmark mark='e'/> So "
                   "delivery specifications ask for minus one dBTP, or minus two for low bit rates: room for the wave to be rebuilt.", marks="bcde")

    # ------------------------------------------------------------------
    def converters(self):
        items = [
            (r"a converter rebuilds the wave with an interpolating filter: \ the same arithmetic as the true-peak meter, \ at a finer step", WHITE),
            (r"many converters leave a few decibels of headroom above digital full scale for exactly these overs; \ some leave none", WHITE),
            (r"a master that is legal sample by sample can still distort on a cheap player", WHITE),
            (r"the true-peak ceiling provides headroom relative to a specified reconstruction estimate; later processing and playback implementations can still change peaks", TUNE),
        ]
        rows_scene(self, r"inside the converter", items,
                   "Where do the overs actually happen? <bookmark mark='b'/> A converter rebuilds the wave with an interpolating "
                   "filter: the same arithmetic as the true-peak meter, at a finer step. <bookmark mark='c'/> Many converters leave a "
                   "few decibels of headroom above digital full scale for exactly these overs; some leave none. "
                   "<bookmark mark='d'/> So a master that is legal sample by sample can still distort on a cheap player. "
                   "<bookmark mark='e'/> The true-peak ceiling provides headroom relative to a specified reconstruction estimate; later processing and playback implementations can still change peaks.", marks="bcde")
