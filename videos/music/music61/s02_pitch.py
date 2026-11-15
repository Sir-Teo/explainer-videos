from __future__ import annotations

import numpy as np

from videos.music.music61.common import *  # noqa: F403


class Pitch(SoundScene):
    def construct(self):
        chapter(self, 1, r"One voice's pitch", r"How does a machine find the pitch of one voice?")
        self.problem()
        self.difference()
        self.missing()
        self.yin_steps()
        self.heard()
        self.uses()

    # ------------------------------------------------------------------
    def problem(self):
        items = [
            (r"pitch is a percept; \ the machine measures the fundamental frequency, \ $f_0$: \ the rate at which the wave repeats", WHITE),
            (r"the obvious answer, \ the strongest peak of the spectrum, \ is often wrong: \ a formant can make the third harmonic loudest", WHITE),
            (r"and the fundamental can be missing altogether \ (Part 4), \ while the ear still hears it", WHITE),
            (r"so look for repetition in time: \ how far must the wave be shifted to match itself?", TUNE),
        ]
        rows_scene(self, r"what to measure", items,
                   "Start with one voice. <bookmark mark='b'/> Pitch is a percept; what a machine measures is the fundamental "
                   "frequency, f nought, the rate at which the wave repeats. <bookmark mark='c'/> The obvious method, taking the "
                   "strongest peak of the spectrum, is often wrong: a formant can make the third harmonic the loudest. "
                   "<bookmark mark='d'/> And the fundamental can be missing altogether, as Part 4 showed, while the ear still hears "
                   "it. <bookmark mark='e'/> So look for repetition in time instead: how far must the wave be shifted to match "
                   "itself?", marks="bcde")

    # ------------------------------------------------------------------
    def difference(self):
        sr = 48000
        t = np.arange(int(0.03 * sr)) / sr
        x = np.sin(2 * np.pi * 220 * t) + 0.6 * np.sin(2 * np.pi * 440 * t + 0.7) + 0.4 * np.sin(2 * np.pi * 660 * t + 1.9)
        taus = np.arange(1, 600)
        W = 400
        d = np.array([np.sum((x[:W] - x[k:k + W]) ** 2) for k in taus])
        dn = d / (np.cumsum(d) / taus)
        a1 = frame_axes(width=10.0, height=1.3, xlo=0, xhi=len(x), ylo=-2.2, yhi=2.2, center=UP * 1.6)
        w1 = curve(np.arange(len(x)), x, a1.to, color=GREY_B, width=2)
        a2 = frame_axes(width=10.0, height=1.8, xlo=0, xhi=600, ylo=0, yhi=2.2, center=DOWN * 1.0)
        c2 = curve(taus, np.clip(dn, 0, 2.2), a2.to, color=TUNE, width=3)
        thr = DashedLine(a2.to(0, 0.1), a2.to(600, 0.1), color=EAR, stroke_width=2)
        T0 = sr / 220
        mark = VGroup(Dot(a2.to(T0, dn[int(T0) - 1]), radius=0.08, color=EAR),
                      label(r"$\tau = 1/220$ s: \ the period", font_size=16, color=EAR).next_to(a2.to(T0, 0.4), UP, buff=0.1))
        eq = MathTex(r"d(\tau) = \sum_j (x_j - x_{j+\tau})^2, \qquad d'(\tau) = \frac{d(\tau)}{\frac{1}{\tau}\sum_{k \le \tau} d(k)}",
                     font_size=30, color=WHITE).to_edge(DOWN, buff=0.25)
        xl = label(r"lag $\tau$, \ in samples at 48 kHz", font_size=14, color=GREY_A).next_to(a2, DOWN, buff=0.1)
        head = label(r"YIN's difference function \ (de Cheveigné and Kawahara, \ 2002)", font_size=24, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is how YIN, published by Alain de Cheveigné and Hideki Kawahara in 2002, does it. <bookmark mark='a'/> Take "
            "a wave, here a 220-hertz tone with two overtones. <bookmark mark='b'/> Shift it by a lag tau and add up the squared "
            "differences. At a lag of one period the wave matches itself, and the difference dips to nearly nothing. YIN divides "
            "the difference by its own running average, which removes the trivial match at lag zero and puts every dip on one "
            "scale. <bookmark mark='c'/> The first dip under a threshold, a tenth, is the period: one two-hundred-and-twentieth of "
            "a second. The same dip recurs at two and three periods; taking the first avoids reporting the octave below."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a1), FadeIn(eq))
            vo.wait_until("a")
            self.play(Create(w1), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(a2), FadeIn(xl), Create(c2), run_time=1.8)
            vo.wait_until("c")
            self.play(Create(thr), FadeIn(mark))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def missing(self):
        d = load("pitch")
        c = clip("pitch.missing")
        bars = VGroup(*[Rectangle(width=0.35, height=2.2 / k if k > 1 else 0.02, stroke_width=0, fill_color=TUNE if k > 1 else EAR, fill_opacity=0.9)
                        for k in range(1, 9)]).arrange(RIGHT, buff=0.4, aligned_edge=DOWN).move_to(UP * 0.4 + LEFT * 2.5)
        labs = VGroup(*[label(f"{220 * k}", font_size=13, color=GREY_A).next_to(b, DOWN, buff=0.1) for k, b in enumerate(bars, 1)])
        nothing = label(r"nothing at 220 Hz", font_size=16, color=EAR).next_to(bars[0], UP, buff=0.4)
        res = VGroup(label(r"YIN reports", font_size=20, color=GREY_A), label(rf"{d['missing_f0']:.1f} Hz", font_size=40, color=TUNE)).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.6 + UP * 0.4)
        head = label(r"a missing fundamental", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Listen to a tone made of the second to eighth partials of 220 hertz, with nothing at 220 itself. You still hear 220, and so does YIN, because the wave still repeats every two-hundred-and-twentieth of a second."):
            self.play(FadeIn(head), FadeIn(bars), FadeIn(labs), FadeIn(nothing))
        with self.listen(c) as snd:
            window(snd, r"partials 2 to 8", kind="synthesized", detail=r"no fundamental", corner=DL, tag_corner=DR)
            pulse(snd, bars, 0.0, c.duration, rate=5.0, color=GREY_B, buff=0.1)
        self.play(FadeIn(res))
        self.wait(1.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def yin_steps(self):
        d = load("pitch")
        items = [
            (r"1. \ the difference function, \ not the autocorrelation: \ no bias toward short lags", WHITE),
            (r"2. \ divide by its running mean: \ the zero-lag match disappears, \ and dips share one scale", WHITE),
            (r"3. \ the first dip under a threshold: \ fewer octave errors", WHITE),
            (r"4. \ parabolic interpolation between lags: \ accuracy finer than one sample", WHITE),
            (rf"on a steady tone: \ YIN {d['bias_yin']:+.1f} cents; \ plain autocorrelation of the same frame {d['bias_acf']:+.1f} cents, \ pulled toward short lags", TUNE),
        ]
        rows_scene(self, r"YIN's steps", items,
                   "YIN improves on plain autocorrelation in four steps. <bookmark mark='b'/> It uses the difference function, "
                   "which does not favour short lags the way autocorrelation of a finite frame does. <bookmark mark='c'/> It "
                   "divides by the running mean, so the match at lag zero disappears and every dip is on one scale. "
                   "<bookmark mark='d'/> It takes the first dip under a threshold, which avoids most octave errors. "
                   "<bookmark mark='e'/> And it interpolates between lags, for accuracy finer than one sample. "
                   f"<bookmark mark='f'/> On a steady tone, YIN is within {say(abs(d['bias_yin']), 1)} cents; the plain "
                   f"autocorrelation of the same frame is pulled {say(abs(d['bias_acf']), 1)} cents sharp.", marks="bcdef")

    # ------------------------------------------------------------------
    def uses(self):
        items = [
            (r"tuners: \ a pitch tracker and a needle, \ in every guitarist's pocket", WHITE),
            (r"pitch correction: \ Auto-Tune \ (1997) \ came from autocorrelation methods its inventor had used to read seismic data", WHITE),
            (r"query by humming, \ singing lessons that score your intonation, \ karaoke", WHITE),
            (r"speech: \ intonation and stress; \ biology: \ bird song and whale song", WHITE),
            (r"and every analysis of a sung performance in this series, \ from the maqam of Part 35 to the voice of Part 8", TUNE),
        ]
        rows_scene(self, r"where one voice's pitch is used", items,
                   "Tracking one voice's pitch is everywhere. <bookmark mark='b'/> In tuners: a pitch tracker and a needle, in every "
                   "guitarist's pocket. <bookmark mark='c'/> In pitch correction: Auto-Tune, released in 1997, grew out of "
                   "autocorrelation methods its inventor, Andy Hildebrand, had used to read seismic data for oil exploration. "
                   "<bookmark mark='d'/> In query by humming, in singing lessons that score intonation, in karaoke. "
                   "<bookmark mark='e'/> In speech, for intonation and stress, and in biology, for bird song and whale song. "
                   "<bookmark mark='f'/> And in every analysis of a sung performance in this series.", marks="bcdef")

    # ------------------------------------------------------------------
    def heard(self):
        d = load("pitchheard")
        c = clip("pitchheard.three")
        boxes = choice_boxes([r"the voice", r"YIN's pitch, \ as a sine", r"both together"], width=3.6, height=0.9, buff=0.4, size=18).move_to(UP * 0.6)
        note = label(rf"voiced in {100 * d['voiced_share']:.0f}\% of frames; \ where the sine and the voice agree, \ they fuse into one sound", font_size=17, color=GREY_A).next_to(boxes, DOWN, buff=0.6)
        head = label(r"checking a pitch track by ear", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A pitch tracker can be checked by ear. Hear the sung Tune; then YIN's pitch track, played as a pure tone that "
            "follows it; then the two together."
        ):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        ks = ["voice", "track", "both"]
        with self.listen(c) as snd:
            window(snd, r"voice, \ track, \ both", kind="synthesized", detail=r"Part 8's voice; \ a sine", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.3 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.06)
        with self.voiceover(
            "Where the tracker is right, the tone and the voice fuse into one sound; an octave error or a wrong note would "
            "stand out at once as a second line. Researchers listen to their pitch tracks this way, because a wrong frame "
            "is easier to hear than to find in a table."
        ):
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()
