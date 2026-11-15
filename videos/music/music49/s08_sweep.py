from __future__ import annotations

import numpy as np

from videos.music.music49.common import *  # noqa: F403


class Sweep(SoundScene):
    def construct(self):
        chapter(self, 7, r"Measuring a room", r"How do you record a room's impulse response?")
        self.why()
        self.sweep()
        self.recovered()
        self.harmonics()
        self.why_exp()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"the obvious way: \ fire a pistol or pop a balloon, \ and record", WHITE),
            (r"but a click carries little energy, \ so the room's own noise swamps the quiet tail", WHITE),
            (r"Angelo Farina \ (2000): \ play a slow sine sweep instead, \ rising exponentially from 20 Hz to 20 kHz", WHITE),
            (r"record the room's answer, \ then convolve it with the sweep run backwards and tilted: \ out comes the impulse response", TUNE),
            (r"the sweep's energy is spread over seconds: \ far more signal above the noise", GREY_A),
        ]
        rows_scene(self, r"a click, \ or a sweep?", items,
                   "To use a real room you must measure its impulse response. <bookmark mark='b'/> The obvious way is to fire a "
                   "starting pistol or pop a balloon and record. <bookmark mark='c'/> But a click carries little energy, so the "
                   "room's own noise swamps the quiet tail. <bookmark mark='d'/> In 2000 Angelo Farina proposed playing a slow "
                   "sine sweep instead, rising exponentially from twenty hertz to twenty kilohertz. <bookmark mark='e'/> Record "
                   "the room's answer, convolve it with the sweep run backwards and tilted, and out comes the impulse response. "
                   "<bookmark mark='f'/> The sweep spreads its energy over seconds, so there is far more signal above the noise.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def sweep(self):
        d = load("sweep")
        c = clip("sweep.sweep")
        ax = frame_axes(width=11.0, height=2.0, xlo=0, xhi=1.6, ylo=0, yhi=4.5, center=UP * 0.3)
        tt = np.linspace(0, 1.6, 300)
        R = np.log(d["f2"] / d["f1"])
        fi = d["f1"] * np.exp(tt * R / d["T"])
        cv = curve(tt, np.log10(fi), ax.to, color=TUNE, width=3)
        ticks = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.1) for t, v in ((r"10 Hz", 1), (r"100", 2), (r"1 k", 3), (r"10 k", 4))])
        dot = Dot(radius=0.09, color=WHITE)
        cap = label(r"its frequency doubles at a steady rate: \ every octave gets the same time", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"an exponential sweep, \ the first 1.6 seconds of 3", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Here is the sweep. Its frequency doubles at a steady rate, so every octave gets the same time."):
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ticks), Create(cv), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"a sweep", kind="synthesized", detail=r"a sine, \ exponential", corner=DL, tag_corner=DR)
            snd.show(dot)

            def fn(m, t):
                u = min(max(t, 0.0), 1.6)
                f = d["f1"] * np.exp(u * R / d["T"])
                m.move_to(ax.to(u, np.log10(f)))
            snd.drive(dot, fn)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recovered(self):
        d = load("sweep")
        a = np.array(d["true"])
        b = np.array(d["est"])
        t = np.arange(len(a)) * 24 / 48000 * 1000
        ax1 = frame_axes(width=11.0, height=1.8, xlo=0, xhi=250, ylo=-1, yhi=1, center=UP * 0.9)
        ax2 = frame_axes(width=11.0, height=1.8, xlo=0, xhi=250, ylo=-1, yhi=1, center=DOWN * 1.5)
        c1 = curve(t, a / np.max(np.abs(a)), ax1.to, color=GREY_A, width=1.2)
        c2 = curve(t, b, ax2.to, color=TUNE, width=1.2)
        l1 = label(r"the room's true response \ (the simulation's)", font_size=17, color=GREY_A).next_to(ax1, UP, buff=0.1)
        l2 = label(r"recovered from the sweep, \ recorded with a little noise", font_size=17, color=TUNE).next_to(ax2, UP, buff=0.1)
        head = label(r"the room, \ measured", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Play the sweep into our simulated room, record the result with a little noise added, and deconvolve. "
            "<bookmark mark='a'/> On top, the room's true response, which only a simulation can know. <bookmark mark='b'/> "
            f"Below, the one recovered from the sweep. Within the sweep's band they agree, the difference "
            f"{say(-d['error_db'])} decibels below the response itself."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ax1), FadeIn(l1), Create(c1), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(ax2), FadeIn(l2), Create(c2), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def harmonics(self):
        d = load("sweep")
        v = np.array(d["distorted"])
        t = np.arange(len(v)) * 48 / 48000 - 0.8
        db = np.clip(20 * np.log10(v + 1e-9), -60, 0)
        ax = frame_axes(width=11.0, height=3.0, xlo=-0.8, xhi=0.2, ylo=-60, yhi=0, center=DOWN * 0.4)
        cv = curve(t, db, ax.to, color=TUNE, width=1.5)
        ticks = VGroup(*[label(f"{x:g} s", font_size=15, color=GREY_A).next_to(ax.to(x, -60), DOWN, buff=0.1) for x in (-0.8, -0.6, -0.4, -0.2, 0, 0.2)])
        tags = VGroup()
        for k, s in zip((2, 3, 4, 5), d["harmonic_s"]):
            tags.add(label(rf"{['', '', '2nd', '3rd', '4th', '5th'][k]}", font_size=15, color=EAR).next_to(ax.to(s, -8), UP, buff=0.05))
        main = label(r"the linear response", font_size=16, color=WHITE).next_to(ax.to(0.0, -2), UP, buff=0.05)
        cap = label(r"the loudspeaker made to distort a little \ (a soft clip); \ level in dB", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"Farina's trick: \ distortion arrives early", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The sweep has a second gift. Make the loudspeaker distort a little, as real ones do. <bookmark mark='a'/> The "
            "distortion's harmonics are copies of the sweep at two, three, four times its frequency, so the backwards sweep "
            "catches them early: <bookmark mark='b'/> the second harmonic's response arrives the time an octave takes before "
            "the main one, the third the time of an octave and a fifth, and so on. They separate cleanly from the linear "
            "response, which can be cut out alone. A balloon could never do that."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ticks), FadeIn(cap))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(main), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(tags))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why_exp(self):
        items = [
            (r"why exponential? \ each octave gets the same time, \ so the low frequencies get enough energy", WHITE),
            (r"its spectrum falls 3 dB an octave, \ like pink noise; \ the inverse filter tilts it back", WHITE),
            (r"and only an exponential sweep puts every harmonic's response at a fixed time before the main one", WHITE),
            (r"a linear sweep, \ or noise, \ smears distortion into the whole response", TUNE),
            (r"the sweep is now the standard way to measure rooms, \ loudspeakers and headphones", GREY_A),
        ]
        rows_scene(self, r"why this sweep", items,
                   "Why an exponential sweep, rather than noise or a linear sweep? <bookmark mark='b'/> It gives each octave the "
                   "same time, so the low frequencies get enough energy. <bookmark mark='c'/> Its spectrum falls three decibels an "
                   "octave, like pink noise, and the inverse filter tilts it back. <bookmark mark='d'/> And only an exponential "
                   "sweep puts every harmonic's response at a fixed time before the main one. <bookmark mark='e'/> A linear sweep, "
                   "or noise, smears the distortion through the whole response. <bookmark mark='f'/> The sweep is now the standard "
                   "way to measure rooms, loudspeakers and headphones.", marks="bcdef")
