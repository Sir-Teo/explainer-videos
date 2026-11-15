from __future__ import annotations

import numpy as np

from videos.music.music48.common import *  # noqa: F403

KIND = {"none": (r"no dither", EAR), "rpdf": (r"rectangular dither, \ one step wide", BLUE), "tpdf": (r"triangular dither, \ two steps wide", TUNE)}


class Dither(SoundScene):
    def construct(self):
        chapter(self, 6, r"Dither", r"How can adding noise make a signal cleaner?")
        self.idea()
        self.moments()
        self.below()
        self.fade()
        self.theory()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"plain rounding makes the error a fixed function of the signal: \ it repeats when the signal repeats", WHITE),
            (r"a repeating error is distortion: \ new tones, \ locked to the music, \ that the ear picks out", WHITE),
            (r"dither: \ add a little random noise before rounding, \ so the error no longer depends on the signal", WHITE),
            (r"we trade a pattern for a hiss; \ the ear forgives a steady hiss far more readily", TUNE),
            (r"and the right dither does it exactly, \ not approximately", GREY_A),
        ]
        rows_scene(self, r"noise as a cure", items,
                   "Why did the noisier version sound better? <bookmark mark='b'/> Plain rounding makes the error a fixed function "
                   "of the signal: it repeats whenever the signal repeats. <bookmark mark='c'/> A repeating error is distortion: "
                   "new tones, locked to the music, which the ear picks out. <bookmark mark='d'/> Dither means adding a little "
                   "random noise before rounding, so that the error no longer depends on the signal. <bookmark mark='e'/> We trade "
                   "a pattern for a hiss, and the ear forgives a steady hiss far more readily. <bookmark mark='f'/> And the right "
                   "dither does it exactly, not approximately.", marks="bcdef")

    # ------------------------------------------------------------------
    def moments(self):
        d = load("moments")
        panels = VGroup()
        for k in ("none", "rpdf", "tpdf"):
            m = d[k]
            xs = np.array(m["x"])
            name, col = KIND[k]
            a = frame_axes(width=3.4, height=1.3, xlo=-0.5, xhi=0.5, ylo=-0.6, yhi=0.6, center=ORIGIN)
            mean = curve(xs, m["mean"], a.to, color=col, width=3)
            b = frame_axes(width=3.4, height=1.3, xlo=-0.5, xhi=0.5, ylo=0, yhi=0.35, center=ORIGIN)
            var = curve(xs, m["var"], b.to, color=col, width=3)
            g = VGroup(label(name, font_size=18, color=col), VGroup(a, mean), VGroup(b, var)).arrange(DOWN, buff=0.3)
            panels.add(g)
        panels.arrange(RIGHT, buff=0.6).move_to(DOWN * 0.15)
        side = VGroup(label(r"average error", font_size=16, color=GREY_A).next_to(panels[0][1], LEFT, buff=0.3),
                      label(r"its spread \ (variance)", font_size=16, color=GREY_A).next_to(panels[0][2], LEFT, buff=0.3))
        cap = label(r"across: \ where the input sits within one step; \ errors in steps", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"the error's average and spread, \ for every input", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        tv = d["tpdf"]["var"]
        with self.voiceover(
            "Here is the whole story in six small graphs. Across each, the input's position within one step; above, the error's "
            "average, and below, how much it spreads, averaged over thousands of dither draws. <bookmark mark='a'/> With no "
            "dither, the average error is a sawtooth: it depends entirely on the input, and it does not spread at all. "
            "<bookmark mark='b'/> With rectangular dither one step wide, the average error becomes zero for every input: no "
            "more distortion. But its spread still depends on the input, so the noise rises and falls with the music, "
            "a modulation the ear can hear. <bookmark mark='c'/> With triangular dither two steps wide, both are flat: the "
            f"average is zero and the spread is a quarter of a step squared everywhere, {say(float(np.mean(tv)), 2)} measured. "
            "The error is now plain, steady noise, whatever the music does."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(side), FadeIn(ghost(panels, 0.15)))
            for mark, p in zip("abc", panels):
                vo.wait_until(mark)
                self.play(FadeIn(p))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def below(self):
        d = load("lowsine")
        c = clip("lowsine.two")
        f = np.array(d["f"])
        ax = frame_axes(width=9.0, height=2.6, xlo=0, xhi=6000, ylo=-120, yhi=-10, center=DOWN * 0.6)
        tp = curve(f, np.clip(d["tpdf"], -120, -10), ax.to, color=TUNE, width=2)
        ticks = VGroup(*[label(f"{v // 1000} k", font_size=15, color=GREY_A).next_to(ax.to(v, -120), DOWN, buff=0.12) for v in (0, 1000, 2000, 4000, 6000)])
        peak = label(r"the 1 kHz tone, \ standing out of the noise", font_size=17, color=TUNE).next_to(ax.to(1000, -20), RIGHT, buff=0.3)
        none = label(rf"without dither: \ every one of the samples is zero \ ({d['nonzero_none']} non-zero)", font_size=19, color=EAR).move_to(UP * 1.6)
        head = label(r"a tone smaller than half a step, \ at 8 bits", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Dither does something stranger still. Take a one-kilohertz sine only 0.4 of a step high, at eight bits. "
            "<bookmark mark='a'/> Without dither, every sample rounds to zero: the tone vanishes completely. "
            "<bookmark mark='b'/> With dither, the samples flicker between levels, and on average they follow the sine: its "
            "spectrum shows the tone standing clear of the noise. Listen: silence, then the tone inside a hiss."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(none))
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(ticks), Create(tp), FadeIn(peak))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"below one step", kind="synthesized", detail=r"a sine, \ 8 bits", corner=DL, tag_corner=DR)
            pulse(snd, none, st["first"], st["second"] - 0.4, buff=0.1)
            pulse(snd, VGroup(tp, peak), st["second"], c.duration, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fade(self):
        d = load("fade")
        c = clip("fade.residues")
        tl = d["tail"]
        n = len(tl["x"])
        ax1 = frame_axes(width=5.4, height=2.2, xlo=0, xhi=n, ylo=-0.022, yhi=0.022, center=ORIGIN)
        ax2 = frame_axes(width=5.4, height=2.2, xlo=0, xhi=n, ylo=-0.022, yhi=0.022, center=ORIGIN)
        k = np.arange(n)
        g1 = VGroup(ax1, curve(k, tl["x"], ax1.to, color=GREY_B, width=1.5), curve(k, tl["none"], ax1.to, color=EAR, width=2.5),
                    label(r"no dither: \ the tail turns to steps", font_size=18, color=EAR).next_to(ax1, UP, buff=0.15))
        g2 = VGroup(ax2, curve(k, tl["x"], ax2.to, color=GREY_B, width=1.5), curve(k, tl["tpdf"], ax2.to, color=TUNE, width=1.5),
                    label(r"triangular dither: \ the tail in noise", font_size=18, color=TUNE).next_to(ax2, UP, buff=0.15))
        g = VGroup(g1, g2).arrange(RIGHT, buff=0.8).move_to(UP * 0.3)
        cap = label(rf"ten milliseconds of a piano note's quiet tail at 8 bits; \ grey: \ the note itself. \ You will hear only the errors, \ raised by {d['gain_db']} dB", font_size=16, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"a piano note fading, \ at 8 bits", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Music is full of quiet: every note fades. Take a piano note at eight bits and look at its tail, magnified. "
            "<bookmark mark='a'/> Without dither, the tail turns into a few steps. <bookmark mark='b'/> With dither, it rides in "
            "noise. Near the threshold, such differences may not survive this video's own compression, so you will hear only "
            f"the errors, the difference from the original note, raised by {say(d['gain_db'])} decibels: first without dither, "
            "then with."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(VGroup(ax1, ax2, g1[1], g2[1])))
            vo.wait_until("a")
            self.play(Create(g1[2]), FadeIn(g1[3]))
            vo.wait_until("b")
            self.play(Create(g2[2]), FadeIn(g2[3]))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"the errors, \ raised 30 dB", kind="synthesized", detail=r"residues of Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, g1, st["first"], st["second"] - 0.4, buff=0.1)
            pulse(snd, g2, st["second"], c.duration, buff=0.1)
        with self.voiceover(
            "Without dither the error is a ghost of the note itself, gritty, and it chatters as the note dies away. With "
            "dither it is a smooth hiss that does not care what the piano is doing."
        ):
            self.play(Indicate(g2, color=TUNE, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theory(self):
        items = [
            (r"Stanley Lipshitz, \ Robert Wannamaker and John Vanderkooy \ (1992): \ the theory of dither", WHITE),
            (r"rectangular dither one step wide makes the error's average independent of the signal", WHITE),
            (r"triangular dither, \ two steps wide, \ makes its average and its power independent: \ the least that does both", WHITE),
            (r"the price: \ three times the noise power of plain rounding, \ about 4.8 dB", TUNE),
            (r"every reduction of word length, \ from 24 bits to 16 for a CD, \ should be dithered", GREY_A),
        ]
        rows_scene(self, r"the theory", items,
                   "The theory was settled in 1992 by Stanley Lipshitz, Robert Wannamaker and John Vanderkooy. "
                   "<bookmark mark='b'/> Rectangular dither one step wide makes the error's average independent of the signal. "
                   "<bookmark mark='c'/> Triangular dither, two steps wide, makes both its average and its power independent, and "
                   "it is the least dither that does both. <bookmark mark='d'/> The price is three times the noise power of plain "
                   "rounding, about 4.8 decibels. <bookmark mark='e'/> So every reduction of word length, from a studio's "
                   "twenty-four bits to a CD's sixteen, should be dithered.", marks="bcde")
