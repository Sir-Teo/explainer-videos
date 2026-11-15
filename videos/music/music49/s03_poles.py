from __future__ import annotations

import numpy as np

from videos.music.music49.common import *  # noqa: F403


class Poles(SoundScene):
    def construct(self):
        chapter(self, 2, r"Poles and zeros", r"How does feeding the output back make a filter?")
        self.onepole()
        self.plane()
        self.ring()
        self.biquad()
        self.stability()

    # ------------------------------------------------------------------
    def onepole(self):
        d = load("onepole")
        imp = d["impulse"]
        ax = frame_axes(width=5.4, height=2.4, xlo=0, xhi=len(imp), ylo=0, yhi=0.12, center=LEFT * 3.3 + DOWN * 0.6)
        st = stems(list(range(len(imp))), imp, ax.to, color=TUNE, r=0.04)
        fa = logf_axes(width=5.4, height=2.4, flo=20, fhi=24000, ylo=-30, yhi=3, center=RIGHT * 3.3 + DOWN * 0.6, ticks=(100, 1000, 10000))
        cv = curve(d["f"], np.clip(d["db"], -30, 3), fa.to, color=TUNE, width=3)
        la = label(r"its impulse response: \ each sample 0.9 of the last", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.2)
        lb = label(rf"its frequency response: \ down 3 dB near {d['cut_hz']:.0f} Hz", font_size=17, color=GREY_A).next_to(fa, UP, buff=0.2)
        eq = MathTex(r"y[n] = (1 - a)\,x[n] + a\,y[n-1], \qquad a = 0.9", font_size=38).to_edge(UP, buff=0.9)
        head = label(r"the simplest filter with feedback", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Now feed the output back. <bookmark mark='a'/> The simplest filter: each output is a tenth of the input plus "
            "nine-tenths of the previous output. <bookmark mark='b'/> Its impulse response never quite ends: each sample is "
            "nine-tenths of the last, a decaying exponential. <bookmark mark='c'/> Its frequency response falls with "
            f"frequency, down three decibels near {say(d['cut_hz'])} hertz: a low-pass filter. Slow changes pass; fast "
            "ones are averaged away."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(la), FadeIn(st, lag_ratio=0.05), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(fa), FadeIn(lb), Create(cv))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plane(self):
        d = load("biquads")["peak"]
        zp = zplane(d["poles"], d["zeros"], radius=1.6).move_to(LEFT * 3.3 + DOWN * 0.4)
        ang = 2 * np.pi * 1000 / 48000
        pt = Dot(zp.circle.get_center() + 1.6 * np.array([np.cos(ang), np.sin(ang), 0]), radius=0.08, color=WHITE)
        lbl = VGroup(label(r"$\times$ \ poles", font_size=18, color=EAR), label(r"$\circ$ \ zeros", font_size=18, color=BLUE), label(r"$\bullet$ \ a frequency, \ on the circle", font_size=18, color=WHITE)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(zp, DOWN, buff=0.3)
        rows_ = text_rows([
            (r"a frequency is a point on the unit circle: \ 0 Hz on the right, \ the Nyquist frequency on the left", WHITE),
            (r"the gain there is the product of its distances to the zeros, \ over the product of its distances to the poles", WHITE),
            (r"a pole near the circle makes a peak; \ a zero near it, \ a dip", TUNE),
            (r"a filter is a choice of where to put a few poles and zeros", GREY_A),
        ], font_size=19, width=6.6).move_to(RIGHT * 3.0 + DOWN * 0.2)
        head = label(r"the z-plane", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "There is a map that explains every such filter: the z-plane. <bookmark mark='a'/> Each frequency is a point on "
            "the unit circle, zero hertz on the right and the Nyquist frequency on the left. <bookmark mark='b'/> The "
            "filter's gain at that frequency is the product of the point's distances to the zeros, divided by the product "
            "of its distances to the poles. <bookmark mark='c'/> So a pole close to the circle makes a peak where the "
            "circle passes it, and a zero close to the circle makes a dip. These are the poles and zeros of a peaking "
            "equalizer at one kilohertz. <bookmark mark='d'/> Designing a filter is choosing where to put a few poles and "
            "zeros."
        ) as vo:
            self.play(FadeIn(head), FadeIn(zp), FadeIn(lbl), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r), FadeIn(pt) if mark == "a" else Indicate(zp.poles, color=EAR) if mark == "c" else Wait(0.1))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ring(self):
        d = load("ring")
        c = clip("ring.two")
        i2, i50 = d["info"]["2"], d["info"]["50"]
        def cell(q, info, color):
            zp = zplane([[info["pole_radius"] * np.cos(2 * np.pi * 440 / 48000 * 8), info["pole_radius"] * np.sin(2 * np.pi * 440 / 48000 * 8)],
                         [info["pole_radius"] * np.cos(2 * np.pi * 440 / 48000 * 8), -info["pole_radius"] * np.sin(2 * np.pi * 440 / 48000 * 8)]], [[1, 0], [-1, 0]], radius=1.1)
            return VGroup(zp, label(rf"Q {q}: \ pole radius {info['pole_radius']:.4f}", font_size=17, color=color)).arrange(DOWN, buff=0.25)
        g = VGroup(cell(2, i2, BLUE), cell(50, i50, TUNE)).arrange(RIGHT, buff=2.0).move_to(UP * 0.1)
        cap = label(r"poles drawn at eight times their true angle, \ so the two can be told apart", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.9)
        head = label(r"a pole near the circle rings", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear what a pole near the circle does. Four clicks through a band-pass filter at four hundred and forty hertz: "
            f"first a wide one, its poles at radius {say(i2['pole_radius'], 3)}; then a narrow one, its poles at "
            f"{say(i50['pole_radius'], 4)}, almost on the circle."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"a wide pole, \ then a narrow one", kind="synthesized", detail=r"clicks, \ a band-pass", corner=DL, tag_corner=DR)
            pulse(snd, g[0], st["wide"], st["narrow"] - 0.3, buff=0.1)
            pulse(snd, g[1], st["narrow"], c.duration, buff=0.1)
        with self.voiceover(
            "The wide filter turns each click into a short tick. The narrow one rings at four hundred and forty hertz for a "
            f"quarter of a second: each step, the ringing keeps {say(i50['pole_radius'], 4)} of itself. A resonance is a pole "
            "close to the circle."
        ):
            self.play(Indicate(g[1], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def biquad(self):
        items = [
            (r"two poles and two zeros: \ the biquad, \ $y[n] = b_0x[n] + b_1x[n-1] + b_2x[n-2] - a_1y[n-1] - a_2y[n-2]$", WHITE),
            (r"five numbers make a low-pass, \ a high-pass, \ a band-pass, \ a notch, \ a peak or a shelf", WHITE),
            (r"Robert Bristow-Johnson's `cookbook' gives the five numbers for each, \ from a frequency, \ a width and a gain", WHITE),
            (r"higher-order filters are biquads in series", TUNE),
            (r"chapter 3 puts them to work", GREY_A),
        ]
        rows_scene(self, r"the biquad", items,
                   "The workhorse is the biquad: two poles and two zeros. <bookmark mark='b'/> Each output is a weighted sum of "
                   "the last three inputs and the last two outputs: five numbers. <bookmark mark='c'/> Those five numbers make a "
                   "low-pass, a high-pass, a band-pass, a notch, a peak or a shelf. <bookmark mark='d'/> Robert Bristow-Johnson's "
                   "cookbook gives the five numbers for each, from a frequency, a width and a gain. <bookmark mark='e'/> "
                   "Higher-order filters are biquads in series. <bookmark mark='f'/> Chapter three puts them to work.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def stability(self):
        items = [
            (r"every pole must lie inside the unit circle", WHITE),
            (r"a pole at radius $r$ makes the impulse response decay as $r^n$: \ inside, \ it dies away", WHITE),
            (r"on the circle it rings forever; \ outside it grows until the numbers overflow", WHITE),
            (r"a feedback loop is a filter whose poles you place; \ place one outside and it screams", TUNE),
            (r"the same rule will make reverberation decay at exactly the rate we choose", GREY_A),
        ]
        rows_scene(self, r"stability", items,
                   "One rule governs feedback. <bookmark mark='b'/> Every pole must lie inside the unit circle. <bookmark mark='c'/> "
                   "A pole at radius r makes the impulse response decay like r to the n: inside the circle, it dies away. "
                   "<bookmark mark='d'/> On the circle it rings forever; outside, it grows until the numbers overflow. "
                   "<bookmark mark='e'/> A feedback loop is a filter whose poles you place, and if you place one outside, it "
                   "screams. <bookmark mark='f'/> The same rule will make reverberation decay at exactly the rate we choose.",
                   marks="bcdef")
