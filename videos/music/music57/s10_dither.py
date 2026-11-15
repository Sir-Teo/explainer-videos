from __future__ import annotations

import numpy as np

from videos.music.music57.common import *  # noqa: F403

DCOL = {"rounded": EAR, "dithered": BLUE, "shaped": TUNE}


class Dither(SoundScene):
    def construct(self):
        chapter(self, 9, r"Dither", r"Why add noise on purpose?")
        self.words()
        self.error()
        self.spectra()
        self.heard()
        self.when()

    # ------------------------------------------------------------------
    def words(self):
        d = load("dither")
        items = [
            (rf"Part 48: \ each bit is 6 dB; \ 16 bits give a range of {d['snr_16']:.0f} dB, \ 24 bits {d['snr_24']:.0f}", WHITE),
            (r"a master is made in 32-bit floating point and delivered in 24 or 16 bits: \ its word length must be cut", WHITE),
            (r"rounding a loud signal leaves an error that looks like noise", WHITE),
            (r"rounding a quiet one leaves an error that follows the signal: \ distortion, \ worst in fades and reverberation tails", TUNE),
        ]
        rows_scene(self, r"cutting the word length", items,
                   "The last step of the chain is the smallest. <bookmark mark='b'/> Part 48 showed that each bit is worth six "
                   f"decibels: sixteen bits give a range of {say(d['snr_16'])} decibels, twenty-four bits {say(d['snr_24'])}. "
                   "<bookmark mark='c'/> A master is made in thirty-two-bit floating point and delivered in twenty-four or sixteen "
                   "bits, so its word length must be cut. <bookmark mark='d'/> Rounding a loud signal leaves an error that looks like "
                   "noise. <bookmark mark='e'/> But rounding a quiet one leaves an error that follows the signal: distortion, worst "
                   "in fades and reverberation tails, exactly where music is most delicate.", marks="bcde")

    # ------------------------------------------------------------------
    def error(self):
        t = np.linspace(0, 1, 400)
        x = 2.6 * np.sin(2 * np.pi * 2 * t)
        rq = np.round(x)
        rng = np.random.default_rng(3)
        dq = np.round(x + rng.random(400) - rng.random(400))
        a1 = frame_axes(width=5.4, height=2.6, xlo=0, xhi=1, ylo=-3.5, yhi=3.5, center=LEFT * 3.2 + DOWN * 0.3)
        a2 = frame_axes(width=5.4, height=2.6, xlo=0, xhi=1, ylo=-3.5, yhi=3.5, center=RIGHT * 3.2 + DOWN * 0.3)
        s1 = VMobject(stroke_color=GREY_B, stroke_width=1.5).set_points_smoothly([a1.to(a, b) for a, b in zip(t, x)])
        s2 = VMobject(stroke_color=GREY_B, stroke_width=1.5).set_points_smoothly([a2.to(a, b) for a, b in zip(t, x)])
        r1 = VMobject(stroke_color=EAR, stroke_width=2.5).set_points_as_corners([a1.to(a, b) for a, b in zip(t, rq)])
        r2 = VMobject(stroke_color=BLUE, stroke_width=1.2).set_points_as_corners([a2.to(a, b) for a, b in zip(t, dq)])
        l1 = label(r"rounded: \ a staircase; \ its error repeats with the wave", font_size=16, color=EAR).next_to(a1, UP, buff=0.15)
        l2 = label(r"dithered: \ noisy, \ but on average the wave itself", font_size=16, color=BLUE).next_to(a2, UP, buff=0.15)
        note = label(r"a sine only 2.6 steps tall: \ TPDF dither adds random noise of two steps, \ peak to peak, \ before rounding", font_size=17, color=WHITE).to_edge(DOWN, buff=0.45)
        head = label(r"rounding, \ with and without dither", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "See it on a sine only two and a half quantization steps tall. <bookmark mark='a'/> Rounded, it becomes a "
            "staircase, and its error repeats with every cycle: harmonics that were never in the music. "
            "<bookmark mark='b'/> Now add a little random noise before rounding, triangular-distributed, two steps from peak to "
            "peak. Each sample is noisier, but the error no longer follows the wave; on average the output is the wave itself, "
            "plus a steady hiss. Stanley Lipshitz and John Vanderkooy proved in the 1980s that triangular dither makes the "
            "error's first two moments independent of the signal."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a1), FadeIn(a2), FadeIn(s1), FadeIn(s2), FadeIn(note))
            vo.wait_until("a")
            self.play(Create(r1), FadeIn(l1), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(r2), FadeIn(l2), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spectra(self):
        d = load("dither")
        f = np.array(d["f"])
        ax = logf_axes(width=9.4, height=3.0, flo=50, fhi=20000, ylo=-40, yhi=0, center=DOWN * 0.4, ticks=(100, 1000, 10000))
        cs = VGroup(*[curve(f, np.clip(np.array(d["err"][k]) - 0.0, -40, 0), ax.to, color=DCOL[k], width=3) for k in ("rounded", "dithered", "shaped")])
        key = VGroup(label(r"rounded: \ peaks at the note's harmonics", font_size=16, color=EAR), label(r"dithered: \ flat hiss", font_size=16, color=BLUE),
                     label(r"noise-shaped: \ hiss pushed above 10 kHz", font_size=16, color=TUNE)).arrange(RIGHT, buff=0.5).to_edge(UP, buff=1.0)
        yl = label(r"the error's spectrum, \ dB \ (relative)", font_size=15, color=GREY_A).next_to(ax, LEFT, buff=0.1)
        yl.scale_to_fit_width(min(yl.width, 1.6))
        note = label(rf"a piano note from Part 38, \ cut to {d['bits']} bits so that the effect can be heard", font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"where the error goes", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the error's spectrum for a real note, Part 38's piano dying away, cut to eight bits so that the effect will "
            "be audible. <bookmark mark='a'/> Rounded: the error has a shape, peaks that track the note. "
            "<bookmark mark='b'/> Dithered: flat hiss. <bookmark mark='c'/> And noise-shaped: the rounding error is fed back "
            "and filtered, so the hiss is pushed up above ten kilohertz, where the ear is least sensitive, and the middle "
            "becomes quieter than plain dither."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yl), FadeIn(note), FadeIn(ghost(cs, 0.25)))
            for mark, cv, k in zip("abc", cs, key):
                vo.wait_until(mark)
                self.play(Create(cv), FadeIn(k), run_time=1.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("dither")
        c = clip("dither.three")
        boxes = choice_boxes([r"rounded", r"dithered", r"noise-shaped"], width=2.8, height=0.9, buff=0.9, size=20).move_to(UP * 0.4)
        note = label(r"8 bits, \ each turned up 18 dB; \ listen to the end of the note", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        head = label(r"a fading note, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear all three, turned up eighteen decibels. Listen to the end of the note, as it fades."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"rounded, \ dithered, \ shaped", kind="physical model", detail=r"Part 38's piano, \ 8 bits", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["rounded"], st["dithered"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["dithered"], st["shaped"] - 0.3, buff=0.08)
            pulse(snd, boxes[2], st["shaped"], c.duration, buff=0.08)
        with self.voiceover(
            "Rounded, the fade turns gritty and buzzy, and then cuts off dead. Dithered, a steady hiss, and the note fades "
            "smoothly into it, audible even below the hiss. Shaped, the hiss is higher and thinner, and seems quieter."
        ):
            self.play(Indicate(boxes[1], color=BLUE, scale_factor=1.04))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def when(self):
        items = [
            (r"dither once, \ at the last step, \ whenever the word length is cut: \ to 24 bits as well as to 16", WHITE),
            (r"at 16 bits the dither's hiss sits near $-96$ dBFS: \ inaudible in a loud master, \ audible in a quiet classical fade", WHITE),
            (r"never dither twice; \ never cut the word length without it", WHITE),
            (r"lossy codecs \ (Part 58) \ work from the high-resolution master, \ not from a dithered 16-bit file", TUNE),
        ]
        rows_scene(self, r"when to dither", items,
                   "The practice is simple. <bookmark mark='b'/> Dither once, at the very last step, whenever the word length is "
                   "cut, to twenty-four bits as well as to sixteen. <bookmark mark='c'/> At sixteen bits the hiss sits near minus "
                   "ninety-six dBFS: inaudible in a loud master, audible in a quiet classical fade on headphones. "
                   "<bookmark mark='d'/> Never dither twice, and never cut the word length without it. <bookmark mark='e'/> And lossy "
                   "codecs, the subject of Part 58, should start from the high-resolution master, not from a dithered sixteen-bit "
                   "file.", marks="bcde")
