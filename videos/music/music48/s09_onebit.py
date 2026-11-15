from __future__ import annotations

import numpy as np

from videos.music.music48.common import *  # noqa: F403


class Onebit(SoundScene):
    def construct(self):
        chapter(self, 8, r"One bit", r"How can a stream of yes-or-no answers carry music?")
        self.modulator()
        self.density()
        self.osr()
        self.speeds()
        self.dsd()

    # ------------------------------------------------------------------
    def modulator(self):
        rows_ = text_rows([
            (r"keep a running total of the input minus the output; \ output $+1$ if the total is positive, \ $-1$ if not", WHITE),
            (r"the output is crude, \ but its running average follows the input: \ errors are always corrected at the next step", WHITE),
            (r"this is noise shaping with one bit: \ the error is pushed up in frequency, \ out of the audio band", TUNE),
            (r"run it 64 times faster than 48 kHz, \ and almost all the noise lies far above hearing", WHITE),
            (r"Hiroshi Inose, \ Yasuhiko Yasuda and Jun Murakami \ (1962) \ named it delta-sigma modulation", GREY_A),
        ], font_size=23)
        head = label(r"a one-bit modulator", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The hook's one-bit version came from a delta-sigma modulator, and it is simple. <bookmark mark='a'/> Keep a "
            "running total of the input minus the output, and output plus one if the total is positive, minus one if not. "
            "<bookmark mark='b'/> Each output is crude, but its running average follows the input, because every error is "
            "corrected at the next step. <bookmark mark='c'/> It is noise shaping, with one bit: the error is pushed up in "
            "frequency. <bookmark mark='d'/> Run it sixty-four times faster than forty-eight kilohertz, and almost all the "
            "noise lies far above hearing, where a filter can remove it. <bookmark mark='e'/> Hiroshi Inose, Yasuhiko Yasuda "
            "and Jun Murakami named it delta-sigma modulation in 1962."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def density(self):
        d = load("deltasigma")
        bits = d["bits"]
        n = len(bits)
        ax = frame_axes(width=12.0, height=2.4, xlo=0, xhi=n, ylo=-1.1, yhi=1.1, center=UP * 0.9)
        k = np.arange(n)
        slow = curve(k, d["slow"], ax.to, color=WHITE, width=3)
        dens = curve(k, d["density"], ax.to, color=TUNE, width=3)
        strip = bits_strip(bits, width=12.0, height=0.8).move_to(DOWN * 1.6)
        sl = label(r"the bits: \ gold for $+1$, \ blue for $-1$", font_size=16, color=GREY_A).next_to(strip, DOWN, buff=0.2)
        key = VGroup(label(r"white: \ the input, \ one slow cycle", font_size=16, color=WHITE), label(r"gold: \ the average of the last 24 bits", font_size=16, color=TUNE)).arrange(RIGHT, buff=0.8).next_to(ax, UP, buff=0.15)
        head = label(r"600 bits of a slow sine", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Watch it work on one slow cycle of a sine. <bookmark mark='a'/> Six hundred output bits. Where the input is high, "
            "the bits are mostly plus one; where it is low, mostly minus one; near zero, they alternate. <bookmark mark='b'/> "
            "Average the bits over a short window, as a low-pass filter does, and the average traces the input. The "
            "information is in the density of the ones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(slow), FadeIn(key[0]))
            vo.wait_until("a")
            self.play(FadeIn(strip, lag_ratio=0.01), FadeIn(sl), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(dens), FadeIn(key[1]), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def osr(self):
        d = load("deltasigma")
        r1, r2 = d["rows"]["1"], d["rows"]["2"]
        p = line_plot([[r["snr"] for r in r1], [r["snr"] for r in r2]], width=7.5, height=3.4, ylo=0, yhi=100, colors=[BLUE, TUNE],
                      xlabel=r"oversampling: \ times 48 kHz", ylabel=r"signal to noise below 20 kHz, \ dB", yticks=(0, 50, 100), size=17)
        xt = VGroup(*[label(f"{r['osr']}", font_size=15, color=GREY_A).next_to(p.to(i, 0), DOWN, buff=0.12) for i, r in enumerate(r1)])
        p.add(xt)
        p.move_to(DOWN * 0.2)
        d1 = VGroup(*[Dot(p.to(i, r["snr"]), radius=0.07, color=BLUE) for i, r in enumerate(r1)])
        d2 = VGroup(*[Dot(p.to(i, r["snr"]), radius=0.07, color=TUNE) for i, r in enumerate(r2)])
        key = VGroup(label(r"first order: \ about 9 dB more each time the rate doubles", font_size=17, color=BLUE),
                     label(r"second order: \ about 15 dB more", font_size=17, color=TUNE)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).to_corner(UL, buff=0.6).shift(DOWN * 0.7)
        head = label(r"one bit, \ measured", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        def gain(r):
            return (r[-1]["snr"] - r[0]["snr"]) / (len(r) - 1)
        with self.voiceover(
            "How good is one bit? Measure the noise below twenty kilohertz for a sine, at rates from eight to a hundred and "
            "twenty-eight times forty-eight kilohertz. <bookmark mark='a'/> With one integrator, each doubling of the rate buys "
            f"about {say(gain(r1), 1)} decibels: theory says nine. <bookmark mark='b'/> With two integrators, about "
            f"{say(gain(r2), 1)}: theory says fifteen. At sixty-four times, the second-order modulator reaches "
            f"{say(r2[3]['snr'])} decibels, and real converters use five or more integrators and a few bits to go far beyond."
        ) as vo:
            self.play(FadeIn(head), FadeIn(p[0]), FadeIn(p[2:]))
            vo.wait_until("a")
            self.play(Create(p.lines[0]), FadeIn(d1), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(Create(p.lines[1]), FadeIn(d2), FadeIn(key[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def speeds(self):
        d = load("speeds")
        c = clip("speeds.three")
        cells = VGroup()
        for k, t in (("1", r"48 kHz \ (1 times)"), ("8", r"384 kHz \ (8 times)"), ("64", r"3.072 MHz \ (64 times)")):
            v = d["snr"][k]
            cells.add(VGroup(RoundedRectangle(width=3.4, height=1.7, corner_radius=0.15, stroke_color=GREY_B),
                             VGroup(label(t, font_size=21, color=WHITE), label(rf"signal to error {v:.0f} dB", font_size=18, color=TUNE if v > 40 else EAR)).arrange(DOWN, buff=0.25)).arrange(ORIGIN))
        cells.arrange(RIGHT, buff=0.5).move_to(UP * 0.2)
        cap = label(r"the same second-order modulator, \ one bit, \ at three speeds; \ each filtered back to 48 kHz", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"one bit, \ at three speeds", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear why speed matters. The same one-bit modulator running at forty-eight kilohertz, at eight times that, and at "
            "sixty-four times, each filtered back to forty-eight kilohertz."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"one bit, \ three speeds", kind="synthesized", detail=r"Part 7's piano, \ delta-sigma", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["1"], st["8"] - 0.4, buff=0.08)
            pulse(snd, cells[1], st["8"], st["64"] - 0.4, buff=0.08)
            pulse(snd, cells[2], st["64"], c.duration, buff=0.08)
        with self.voiceover(
            "At the audio rate itself, one bit is a harsh buzz with the tune buried in it: the noise has nowhere to go. At "
            f"eight times, the tune is clear in a hiss, {say(d['snr']['8'])} decibels below it. At sixty-four times, "
            f"{say(d['snr']['64'])} decibels: the noise has been pushed almost entirely above hearing and filtered away."
        ):
            self.play(Indicate(cells[2], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dsd(self):
        d = load("deltasigma")
        items = [
            (r"almost every converter today, \ in phones and studios alike, \ is a delta-sigma converter", WHITE),
            (r"it samples millions of times a second with a few bits, \ then filters and decimates to 48 kHz and 24 bits", WHITE),
            (rf"the Super Audio CD \ (1999) \ stored the one-bit stream itself: \ Direct Stream Digital, \ {d['dsd_rate']:,} bits a second", WHITE),
            (r"its noise rises steeply above 20 kHz and must be filtered on playback", TUNE),
            (r"the hook's first version was such a stream, \ filtered back to 48 kHz", GREY_A),
        ]
        rows_scene(self, r"one bit in practice", items,
                   "This is not a curiosity. <bookmark mark='b'/> Almost every converter today, in phones and studios alike, is a "
                   "delta-sigma converter: <bookmark mark='c'/> it samples millions of times a second with a few bits, then "
                   "filters and decimates to forty-eight kilohertz and twenty-four bits. <bookmark mark='d'/> The Super Audio CD, "
                   "in 1999, stored the one-bit stream itself, Direct Stream Digital, at 2,822,400 bits a second for each channel, "
                   "sixty-four times the CD rate. <bookmark mark='e'/> Its noise rises steeply above twenty kilohertz and must be "
                   "filtered on playback. <bookmark mark='f'/> The hook's first version was such a stream, filtered back to "
                   "forty-eight kilohertz.", marks="bcdef")
