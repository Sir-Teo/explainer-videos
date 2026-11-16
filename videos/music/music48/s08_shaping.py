from __future__ import annotations

import numpy as np

from videos.music.music48.common import *  # noqa: F403

ORD = {"0": (r"flat \ (plain dither)", GREY_A), "1": (r"first order, \ $1 - z^{-1}$", BLUE), "2": (r"second order, \ $(1 - z^{-1})^2$", TUNE)}


class Shaping(SoundScene):
    def construct(self):
        chapter(self, 7, r"Noise shaping", r"Can the noise be moved where we cannot hear it?")
        self.feedback()
        self.spectra()
        self.listen_()
        self.practice()

    # ------------------------------------------------------------------
    def feedback(self):
        rows_ = text_rows([
            (r"the noise cannot be removed, \ but it can be moved", WHITE),
            (r"remember each sample's rounding error, \ and subtract it from the next sample before rounding", WHITE),
            (r"the error reaches the output as $e[n] - e[n-1]$: \ filtered by $1 - z^{-1}$, \ a high-pass", TUNE),
            (r"twice over, \ $(1 - z^{-1})^2$: \ steeper still; \ the noise's total grows, \ but it leaves the low frequencies", WHITE),
            (r"C. Chapin Cutler's patent \ (1954) \ first described feeding the error back this way", GREY_A),
        ], font_size=23)
        head = label(r"error feedback", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Dither leaves us with a steady hiss. Can it be made quieter? <bookmark mark='a'/> The noise cannot be removed, "
            "but it can be moved. <bookmark mark='b'/> Remember each sample's rounding error, and subtract it from the next "
            "sample before rounding that one. <bookmark mark='c'/> Then the error reaches the output as each error minus the one "
            "before: filtered by one minus z to the minus one, a high-pass filter. <bookmark mark='d'/> Do it twice over and the "
            "filter is steeper. The noise's total power grows, but it leaves the low frequencies, where the ear is most "
            "sensitive. <bookmark mark='e'/> C. Chapin Cutler's patent of 1954 first described feeding the error back this way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spectra(self):
        d = load("shaping")
        f = np.array(d["f"])
        ax = frame_axes(width=9.4, height=3.6, xlo=0, xhi=24000, ylo=-160, yhi=-30, center=DOWN * 0.3 + LEFT * 0.8)
        cs = {}
        for k in ("0", "1", "2"):
            P = np.clip(np.array(d[k]["P"]), -160, -30)
            cs[k] = curve(f, P, ax.to, color=ORD[k][1], width=3)
        ticks = VGroup(*[label(f"{v // 1000} k", font_size=15, color=GREY_A).next_to(ax.to(v, -160), DOWN, buff=0.12) for v in (0, 4000, 8000, 12000, 16000, 20000, 24000)])
        yl = label(r"error power in each band, \ dB", font_size=16, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        key = VGroup(*[label(ORD[k][0], font_size=17, color=ORD[k][1]) for k in ("0", "1", "2")]).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3).shift(UP * 0.8)
        nums = VGroup(*[label(rf"total {d[k]['total_db']:.0f} dB; \ below 4 kHz {d[k]['below4k_db']:.0f} dB", font_size=15, color=ORD[k][1]) for k in ("0", "1", "2")]).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(key, DOWN, buff=0.5)
        band = Rectangle(width=ax.to(4000, 0)[0] - ax.to(0, 0)[0], height=3.6, stroke_width=0, fill_color=WHITE, fill_opacity=0.06).move_to([(ax.to(0, 0)[0] + ax.to(4000, 0)[0]) / 2, ax.to(0, -95)[1], 0])
        head = label(r"the error of the Tune at 8 bits, \ three ways", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        z, t1, t2 = d["0"], d["1"], d["2"]
        with self.voiceover(
            "Here are the error spectra of the Tune at eight bits. <bookmark mark='a'/> Plain dither: flat, the same at every "
            f"frequency. <bookmark mark='b'/> First-order shaping tilts it up. <bookmark mark='c'/> Second order tilts it "
            f"further. In numbers, the total error power rises from {say(z['total_db'])} to {say(t2['total_db'])} decibels, "
            f"but below four kilohertz, the shaded band where the ear is keenest, it falls from {say(z['below4k_db'])} to "
            f"{say(t2['below4k_db'])}. The noise is louder, and quieter where it matters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ticks), FadeIn(yl), FadeIn(band))
            for mark, k in zip("abc", ("0", "1", "2")):
                vo.wait_until(mark)
                self.play(Create(cs[k]), FadeIn(key[int(k)]), FadeIn(nums[int(k)]), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def listen_(self):
        d = load("shaping")
        c = clip("shaping.residues")
        f = np.array(d["f"])
        def pan(k, title):
            ax = frame_axes(width=5.0, height=2.2, xlo=0, xhi=24000, ylo=-160, yhi=-30, center=ORIGIN)
            P = np.clip(np.array(d[k]["P"]), -160, -30)
            return VGroup(ax, curve(f, P, ax.to, color=ORD[k][1], width=3), label(title, font_size=18, color=ORD[k][1]).next_to(ax, UP, buff=0.15))
        g = VGroup(pan("0", r"flat"), pan("2", r"second order")).arrange(RIGHT, buff=1.0).move_to(UP * 0.3)
        cap = label(rf"only the errors, \ raised by {d['gain_db']} dB: \ the music is not playing", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"the two errors, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Hear the two errors on their own, raised by {say(d['gain_db'])} decibels: first the flat one, then the shaped. "
            "Listen to where the hiss sits."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"flat, \ then shaped", kind="synthesized", detail=r"residues, \ raised 24 dB", corner=DL, tag_corner=DR)
            pulse(snd, g[0], st["first"], st["second"] - 0.4, buff=0.1)
            pulse(snd, g[1], st["second"], c.duration, buff=0.1)
        with self.voiceover(
            "The flat error is a full, broad hiss. The shaped one is thinner and higher, a fizz near the top of hearing, where "
            "our ears are much less sensitive."
        ):
            self.play(Indicate(g[1], color=TUNE, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def practice(self):
        items = [
            (r"Michael Gerzon and Peter Craven \ (1989): \ shape the noise to follow the threshold of hearing", WHITE),
            (r"commercial dithers for mastering do exactly this when 24-bit masters become 16-bit CDs", WHITE),
            (r"the noise you perceive drops, \ though the measured total rises", WHITE),
            (r"the cost: \ prefer strong shaping at final delivery; \\ later processing can expose or accumulate its noise", TUNE),
            (r"pushed to the extreme, \ with many times the sample rate, \ shaping makes one bit enough: \ chapter 8", GREY_A),
        ]
        rows_scene(self, r"shaping to the ear", items,
                   "In 1989 Michael Gerzon and Peter Craven worked out how to shape the noise to follow the threshold of hearing. <bookmark mark='b'/> Commercial mastering dithers do exactly this when twenty-four-bit masters become sixteen-bit CDs. <bookmark mark='c'/> The noise you perceive drops, though the measured total rises. <bookmark mark='d'/> The cost: reserve strong final noise shaping for delivery when possible; repeated quantization and later processing can accumulate or expose shaped noise, rather than being mathematically forbidden. <bookmark mark='e'/> Pushed to the extreme, with many times the sample rate, shaping makes one bit enough. That is chapter eight.", marks="bcde")
