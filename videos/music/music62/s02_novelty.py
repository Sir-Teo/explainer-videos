from __future__ import annotations

import numpy as np

from videos.music.music62.common import *  # noqa: F403


class Novelty(SoundScene):
    def construct(self):
        chapter(self, 1, r"Where the beats might be", r"What does a machine listen to when it looks for the beat?")
        self.what()
        self.curve()
        self.periodic()

    # ------------------------------------------------------------------
    def what(self):
        items = [
            (r"a beat is a percept: \ the pulse listeners tap, \ not a sound; \ it can fall in silence", WHITE),
            (r"but beats usually coincide with note starts, \ accents, \ chord changes", WHITE),
            (r"so start from Part 61's spectral flux: \ a curve that rises wherever something begins", WHITE),
            (r"subtract its local mean, \ keep what sticks up: \ the novelty curve", TUNE),
        ]
        rows_scene(self, r"what to listen for", items,
                   "A beat is not a sound. <bookmark mark='b'/> It is the pulse a listener taps, and it can fall in silence, "
                   "inside a held note or a rest. <bookmark mark='c'/> But beats usually coincide with note starts, accents and "
                   "chord changes. <bookmark mark='d'/> So machines start from Part 61's spectral flux, a curve that rises "
                   "wherever something begins. <bookmark mark='e'/> Subtract its local mean, keep what sticks up, and you have the "
                   "novelty curve.", marks="bcde")

    # ------------------------------------------------------------------
    def curve(self):
        d = load("tempo")
        t, nov = np.array(d["t"]), np.array(d["nov"])
        ax = frame_axes(width=11.0, height=2.4, xlo=0, xhi=t[-1], ylo=0, yhi=1.05, center=DOWN * 0.2)
        cv = curve(t, nov, ax.to, color=TUNE, width=2)
        beats = VGroup(*[Line(ax.to(b, 0), ax.to(b, -0.2), color=GREY_B, stroke_width=3) for b in np.arange(0, t[-1], 0.6)])
        bars = VGroup(*[Line(ax.to(b, 0), ax.to(b, -0.35), color=WHITE, stroke_width=3) for b in np.arange(0, t[-1], 2.4)])
        xt = VGroup(*[label(f"{v:g} s", font_size=13, color=GREY_A).next_to(ax.to(v, -0.35), DOWN, buff=0.08) for v in range(0, int(t[-1]) + 1, 2)])
        note = label(r"grey ticks: \ the beats, \ every 0.6 s \ (100 a minute); \ white: \ every fourth", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"the session's novelty curve", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the novelty curve of Part 56's session playing the Tune's first two phrases. <bookmark mark='a'/> Kick, "
            "snare, hi-hat, bass, guitar, piano and voice all start things, and the curve is a forest of peaks. "
            "<bookmark mark='b'/> But the forest has a rhythm: the tallest peaks fall on the beats, every six tenths of a "
            "second, a hundred a minute."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt))
            vo.wait_until("a")
            self.play(Create(cv), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(beats), FadeIn(bars), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def periodic(self):
        d = load("tempo")
        A = np.array(d["A"])
        bpm = np.array(d["bpm_axis"])
        pic = picture(A[::-1], 0, 1, 8.0, 3.2).move_to(DOWN * 0.3 + LEFT * 0.6)
        lo, hi = bpm.min(), bpm.max()
        y0, y1 = pic.get_bottom()[1], pic.get_top()[1]

        def ypos(b):                                 # rows run from the slowest lag (top of the array) to the fastest
            k = np.argmin(np.abs(bpm - b))
            return y1 - (y1 - y0) * (k + 0.5) / len(bpm)
        ticks = VGroup(*[label(f"{b}", font_size=13, color=GREY_A).move_to([pic.get_left()[0] - 0.35, ypos(b), 0]) for b in (50, 100, 200)])
        yl = label(r"beats a minute", font_size=14, color=GREY_A).rotate(PI / 2).next_to(ticks, LEFT, buff=0.15)
        xl = label(r"time through the passage", font_size=14, color=GREY_A).next_to(pic, DOWN, buff=0.15)
        side = VGroup(label(r"bright rows: \ periods at which the novelty repeats", font_size=17, color=WHITE),
                      label(r"100: \ the beat", font_size=17, color=TUNE), label(r"200: \ the eighth notes", font_size=17, color=WHITE),
                      label(r"50: \ every second beat", font_size=17, color=WHITE)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(pic, RIGHT, buff=0.4)
        head = label(r"a tempogram", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How fast? <bookmark mark='a'/> Slide a six-second window along the novelty curve and correlate it with itself at "
            "every lag, as YIN did for pitch, but a thousand times slower. Each column is one window, each row a tempo. "
            "<bookmark mark='b'/> The brightest row is a hundred beats a minute. But the rows at two hundred, the eighth notes, "
            "and fifty, every second beat, are bright too: rhythm repeats at every level of its own hierarchy."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pic), FadeIn(ticks), FadeIn(yl), FadeIn(xl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in side[1:]], lag_ratio=0.4), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()
