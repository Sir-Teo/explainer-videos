from __future__ import annotations

import numpy as np

from videos.music.music54.common import *  # noqa: F403


class Horns(SoundScene):
    def construct(self):
        chapter(self, 8, r"Horns", r"How does a horn make a small driver loud?")
        self.mismatch()
        self.throat()
        self.directivity()
        self.history()

    # ------------------------------------------------------------------
    def mismatch(self):
        items = [
            (r"a small cone is a poor match for air: \ air is light, \ the cone heavy; \ most of its motion just sloshes air nearby", WHITE),
            (r"the radiation resistance of a small piston grows as frequency squared: \ at low frequencies it is almost nothing", WHITE),
            (r"a horn is a gradual change of area: \ a small, \ stiff throat opening into a wide mouth", WHITE),
            (r"at the throat the driver pushes a column of air that cannot get out of the way: \ a better match", TUNE),
            (r"the same idea as a gramophone's horn, \ or cupped hands", GREY_A),
        ]
        rows_scene(self, r"an acoustic transformer", items,
                   "Efficiency is a matter of matching. <bookmark mark='b'/> A small cone is a poor match for air: air is light, the "
                   "cone heavy, and most of its motion just sloshes air nearby. <bookmark mark='c'/> The resistance a small piston "
                   "feels from the air grows as the frequency squared, so at low frequencies it is almost nothing. "
                   "<bookmark mark='d'/> A horn is a gradual change of area, a small throat opening into a wide mouth, "
                   "<bookmark mark='e'/> and at the throat the driver pushes a column of air that cannot get out of the way: a "
                   "better match. <bookmark mark='f'/> It is the gramophone's horn, or a pair of cupped hands.", marks="bcdef")

    # ------------------------------------------------------------------
    def throat(self):
        d = load("horn")
        f = np.array(d["f"])
        ax = logf_axes(width=8.0, height=3.2, flo=20, fhi=5000, ylo=0, yhi=1.1, center=LEFT * 0.8 + DOWN * 0.2, ticks=(100, 1000))
        h = curve(f, d["horn"], ax.to, color=TUNE, width=3)
        p = curve(f, np.minimum(d["piston"], 1.1), ax.to, color=GREY_A, width=2.5)
        fc = DashedLine(ax.to(d["fc"], 0), ax.to(d["fc"], 1.1), color=EAR, stroke_width=1.5)
        fl = label(rf"cutoff \ {d['fc']:.0f} Hz", font_size=15, color=EAR).next_to(ax.to(d["fc"], 1.1), UP, buff=0.05)
        key = VGroup(label(r"an exponential horn's throat", font_size=17, color=TUNE), label(r"the same area as a bare piston", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.4)
        eq = MathTex(r"R = \frac{\rho c}{S}\sqrt{1 - \Big(\frac{f_c}{f}\Big)^2}, \qquad f_c = \frac{m c}{4\pi}", font_size=30).to_edge(UP, buff=1.0)
        note = label(rf"at 200 Hz the horn loads the driver {d['gain_200']:.0f} dB better than the bare piston", font_size=18, color=WHITE).to_edge(DOWN, buff=0.4)
        yl = label(r"resistance, \ re $\rho c / S$", font_size=15, color=GREY_A).next_to(ax, LEFT, buff=0.15)
        head = label(r"what the driver sees", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Here is what the driver sees, as a fraction of the best possible match. <bookmark mark='a'/> A bare piston of the throat's size: its resistance creeps up as frequency squared and only reaches full match high in the treble. <bookmark mark='b'/> An exponential horn, whose area grows by the same factor every few centimetres, as Arthur Webster described in 1919: above a cutoff set by its flare, the throat presents nearly the full match. <bookmark mark='c'/> At two hundred hertz that is {say(d['gain_200'])} decibels better loading. Below cutoff this ideal infinite exponential horn has no propagating resistance; finite horns also have termination effects and resonances, so a bass horn must be enormous."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yl), FadeIn(eq), FadeIn(ghost(VGroup(h, p), 0.25)))
            vo.wait_until("a")
            self.play(Create(p), FadeIn(key[1]))
            vo.wait_until("b")
            self.play(Create(h), FadeIn(key[0]), FadeIn(fc), FadeIn(fl), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"the gramophone's horn \ (1890s--1920s): \ no electricity, \ only matching", WHITE),
            (r"Western Electric's cinema horns \ (late 1920s): \ a few watts of valve amplifier filled a theatre", WHITE),
            (r"compression drivers and horns still carry concerts' treble \ (Part 59)", WHITE),
            (r"the cost: \ size at low frequencies, \ and a colour some call `honk'", WHITE),
            (r"one driver cannot do everything: \ hence crossovers", TUNE),
        ]
        rows_scene(self, r"horns at work", items,
                   "Horns have a long history. <bookmark mark='b'/> The gramophone's horn, from the 1890s to the 1920s, made music "
                   "loud with no electricity at all, only matching. <bookmark mark='c'/> Western Electric's cinema horns of the late "
                   "1920s let a few watts of valve amplifier fill a theatre. <bookmark mark='d'/> Compression drivers and horns still "
                   "carry the treble at concerts, as Part 59 will show. <bookmark mark='e'/> The cost is size at low frequencies, and "
                   "a colour some call honk. <bookmark mark='f'/> And no single driver can do everything: hence crossovers.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def directivity(self):
        items = [
            (r"a horn also controls where the sound goes: \ its walls set the beam's width", WHITE),
            (r"a cone beams more as the frequency rises; \ a shallow horn around a tweeter matches the woofer's width at the crossover", WHITE),
            (r"then the sound reflected from the walls has the same colour as the direct sound", WHITE),
            (r"many modern loudspeakers use such `waveguides' for this reason, \ not for loudness", WHITE),
            (r"in a room, \ even directivity can matter more than a flat axis", TUNE),
        ]
        rows_scene(self, r"waveguides for tweeters", items,
                   "Horns do a second job. <bookmark mark='b'/> A horn also controls where the sound goes: its walls set the beam's width. <bookmark mark='c'/> A cone beams more as the frequency rises, so a shallow horn around a tweeter can match the woofer's width at the crossover, <bookmark mark='d'/> and then the sound reflected from the walls has the same colour as the direct sound. <bookmark mark='e'/> Many modern loudspeakers use such waveguides for this reason, not for loudness. <bookmark mark='f'/> In a room, even directivity can matter more than a flat response on the axis.", marks="bcdef")
