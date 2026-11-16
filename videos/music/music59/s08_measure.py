from __future__ import annotations

import numpy as np

from videos.music.music59.common import *  # noqa: F403


class Measure(SoundScene):
    def construct(self):
        chapter(self, 7, r"Measuring a system", r"How do you measure a loudspeaker while the band is playing?")
        self.method()
        self.result()
        self.pitfalls()
        self.tuning()

    # ------------------------------------------------------------------
    def method(self):
        lines = VGroup(
            MathTex(r"x: \text{ what goes into the system (the desk's output)}, \quad y: \text{ what a microphone hears}", font_size=28),
            MathTex(r"H(f) = \frac{\overline{S_{xy}(f)}}{\overline{S_{xx}(f)}} \qquad (\text{cross- over auto-spectrum, averaged})", font_size=32, color=TUNE),
            MathTex(r"\gamma^2(f) = \frac{|\overline{S_{xy}}|^2}{\overline{S_{xx}}\;\overline{S_{yy}}} \qquad (\text{coherence: } 1 \text{ if } y \text{ is all } x)", font_size=32),
            MathTex(r"h(t) = \mathcal{F}^{-1}\{H\}: \text{ its peak is the delay}", font_size=30),
        ).arrange(DOWN, buff=0.45).move_to(DOWN * 0.1)
        head = label(r"dual-channel measurement", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Part 49 measured a room with a sweep. A live system cannot stop for a sweep, so engineers measure with the music "
            "itself. <bookmark mark='a'/> Take the signal going into the system and what a measurement microphone hears in the "
            "audience. <bookmark mark='b'/> Average their cross-spectrum and the input's auto-spectrum over many blocks; their "
            "ratio is the transfer function, in bands where the input has sufficient excitation and the linear, stationary and noise assumptions are adequate. <bookmark mark='c'/> The coherence says how much "
            "of the microphone's signal is explained by the input: near one where the music had energy and the room is quiet, "
            "lower where uncorrelated noise, time variation, inadequate averaging or windowing intrude; a stable linear reverberant path does not inherently reduce coherence. <bookmark mark='d'/> And the inverse transform's peak is the "
            "delay, which tells the engineer how far the microphone is from the loudspeaker."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.25)))
            for mark, ln in zip("abcd", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def result(self):
        d = load("measure")
        f = np.array(d["f"])
        mag = np.array(d["mag_db"])
        true = np.array(d["true_db"])
        ref = np.max(true)
        a1 = logf_axes(width=10.0, height=2.2, flo=30, fhi=16000, ylo=-40, yhi=5, center=UP * 0.7, ticks=(100, 1000, 10000))
        a2 = logf_axes(width=10.0, height=1.2, flo=30, fhi=16000, ylo=0, yhi=1, center=DOWN * 1.9, ticks=(100, 1000, 10000))
        def smooth(v, db=True, k=6):
            """About a sixth of an octave, averaged (the points are log-spaced, some 37 an octave), in power for dB."""
            v = np.asarray(v, float)
            x = 10 ** (v / 10) if db else v
            y = np.convolve(np.r_[np.full(k // 2, x[0]), x, np.full(k // 2, x[-1])], np.ones(k) / k, mode="valid")
            return 10 * np.log10(y) if db else y
        ref = np.max(smooth(true))
        tr = curve(f, np.clip(smooth(true) - ref, -40, 5), a1.to, color=GREY_B, width=5)
        me = curve(f, np.clip(smooth(mag) - ref, -40, 5), a1.to, color=TUNE, width=2.5)
        co = curve(f, smooth(d["coherence"], db=False), a2.to, color=BLUE, width=2.5)
        l1 = label(r"the transfer function, \ smoothed to a sixth of an octave: \ measured with music \ (gold) \ over the true one \ (grey)", font_size=15, color=GREY_A).next_to(a1, UP, buff=0.05).align_to(a1, LEFT)
        l2 = label(r"coherence", font_size=15, color=BLUE).next_to(a2, UP, buff=0.05).align_to(a2, LEFT)
        note = label(rf"delay found: \ {d['delay_ms']:.1f} ms \ (true: \ {d['true_delay_ms']:.1f} ms)", font_size=17, color=TUNE).to_edge(DOWN, buff=0.15)
        head = label(r"measured with the Tune", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is that measurement made with our session playing the Tune, through a simulated hall and a little noise. "
            "<bookmark mark='a'/> The measured transfer function follows the true one where the music has energy. "
            "<bookmark mark='b'/> The coherence shows where to trust it: high in the bands the band filled, falling where the "
            "music was thin and the room's reverberation and noise dominate. <bookmark mark='c'/> And the delay is found to the "
            "sample. Programs like Smaart and SysTune show exactly these three traces at every mixing desk."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a1), FadeIn(a2), FadeIn(ghost(VGroup(tr, me, co), 0.25)))
            vo.wait_until("a")
            self.play(Create(tr), Create(me), FadeIn(l1), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(co), FadeIn(l2), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pitfalls(self):
        items = [
            (r"the crowd is noise to the measurement: \ coherence falls when they sing along, \ so engineers average longer", WHITE),
            (r"the microphone's signal must be delayed by the delay found, \ or the two blocks hold different music", WHITE),
            (r"a long block resolves bass but smears in the room's reflections; \ so the block shortens as frequency rises", WHITE),
            (r"one microphone describes one seat: \ engineers average several, \ and never equalize a single seat's notch", WHITE),
            (r"wind and temperature change the delay through the night: \ the measurement runs all show", TUNE),
        ]
        rows_scene(self, r"what can go wrong", items,
                   "The method has pitfalls, and every engineer learns them. <bookmark mark='b'/> To the measurement, the crowd is "
                   "noise: the coherence falls when they sing along, so the averages run longer. <bookmark mark='c'/> The "
                   "microphone's signal must first be delayed by the delay found, or the two blocks hold different music and the "
                   "coherence collapses. <bookmark mark='d'/> A long block resolves the bass but smears in the room's reflections, so "
                   "analysers shorten the block as frequency rises, keeping a constant number of cycles in each. "
                   "<bookmark mark='e'/> One microphone describes one seat; engineers average several, and never equalize a notch "
                   "that only one seat hears. <bookmark mark='f'/> And wind and temperature change the delay through the night, so "
                   "the measurement runs all show.", marks="bcdef")

    # ------------------------------------------------------------------
    def tuning(self):
        items = [
            (r"time-align the parts of the system: \ subwoofers to arrays, \ arrays to fills, \ towers to the stage", WHITE),
            (r"equalize each zone to a target curve, \ only where the coherence says the measurement is real", WHITE),
            (r"cut, \ don't boost: \ a boost into a reflection's notch only adds energy elsewhere", WHITE),
            (r"then walk the room and listen: \ the measurement says what is there, \ the ear says whether it is right", TUNE),
        ]
        rows_scene(self, r"tuning a system", items,
                   "With these traces a system is tuned. <bookmark mark='b'/> Its parts are aligned in time: subwoofers to arrays, arrays to fills, towers to the stage. <bookmark mark='c'/> Each zone is equalized to a target curve, but only where the coherence says the measurement is real. <bookmark mark='d'/> Cut, don't boost: boosting a deep spatial cancellation is generally ineffective and can waste headroom. <bookmark mark='e'/> And then the engineer walks the room and listens: the measurement says what is there, the ear whether it is right.", marks="bcde")
