from __future__ import annotations

import numpy as np

from videos.music.music3.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ sharper than the limit", r"Is Gabor's limit the last word?", lit=(1807,),
                extra=((1976, r"reassignment"), (2013, r"listeners beat the uncertainty limit")))
        self.reassign()
        self.ears()
        self.open()

    # ------------------------------------------------------------------
    def reassign(self):
        d = load("reassign")
        a = picture(d["plain"], -45, 0, 5.9, 3.7)
        b = picture(d["sharp"], -45, 0, 5.9, 3.7)
        Group(a, b).arrange(RIGHT, buff=0.6).move_to(DOWN * 0.1)
        caps = VGroup(label(r"an ordinary spectrogram", font_size=26, color=GREY_A).next_to(a, UP, buff=0.12),
                      label(r"the same data, \ reassigned", font_size=26, color=TUNE).next_to(b, UP, buff=0.12))
        sig = label(r"a rising sweep, \ a click, \ and a steady tone", font_size=24, color=GREY_B).to_edge(UP, buff=0.35)
        res = label(rf"nine tenths of the energy: \ in {d['cells_plain']:,} cells before, \ {d['cells_sharp']:,} after".replace(",", "{,}"), font_size=26, color=GOOD)
        res.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Gabor's limit is a limit on a picture made by smearing a sound through one window. It is not a limit "
            "on what can be known, if you are willing to assume something. <bookmark mark='a'/> Each cell of a "
            "spectrogram holds the energy of a patch of time and frequency, and credits it to the centre of the "
            "patch. But two more transforms, costing almost nothing, tell you where inside the patch the energy "
            "really sits. Move it there, <bookmark mark='b'/> and the blurred sweep becomes a line, the click a "
            "sharp stroke. The method is called reassignment. <bookmark mark='c'/> On this test sound it packs the "
            f"same energy into {say(d['ratio'], 1)} times fewer cells. It works whenever each patch holds only one "
            "thing, and it fails, honestly, when two things overlap."
        ) as vo:
            self.play(FadeIn(sig), FadeIn(a), FadeIn(caps[0]))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(caps[1]))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ears(self):
        d = load("reassign")["oppenheim"]
        card = history_card(2013, r"Jacob Oppenheim and Marcelo Magnasco",
                            r"\textit{Physical Review Letters}: listeners asked to judge the timing and the pitch of a "
                            r"short note at once", width=6.0).to_corner(UL, buff=0.45)
        # the limit as a region
        g = axes([0, 4], [0, 4], x_length=4.6, y_length=3.6, xlabel=r"uncertainty in time", ylabel=r"uncertainty in pitch", xticks=[], yticks=[], font_size=20)
        g.move_to(RIGHT * 3.4 + UP * 0.2)
        xs = np.linspace(0.27, 4, 80)
        hyper = curve(g.ax, xs, 1.0 / xs, BAD, stroke_width=3)
        lim = label(r"the limit for any single window", font_size=22, color=BAD).move_to(g.ax.c2p(2.7, 1.0))
        dots = VGroup(*[Dot(g.ax.c2p(x, y), radius=0.07, color=EAR) for x, y in ((0.5, 0.9), (0.4, 0.5), (0.7, 0.35), (0.3, 0.26), (0.9, 0.6), (0.6, 1.2))])
        tag = label(r"schematic", font_size=18, color=GREY_C).next_to(g, DOWN, buff=0.35)
        res = VGroup(label(r"most listeners did better than the limit", font_size=28, color=EAR),
                     label(rf"the best, \ by a factor of {d['best']}", font_size=28, color=EAR),
                     label(r"the limit binds linear analysis: \ the ear is not linear", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        res.move_to(LEFT * 3.3 + DOWN * 1.6)
        with self.voiceover(
            "And there is an older device that does better than a spectrogram. In 2013 two physicists in New York "
            "asked listeners to judge two things at once about a short note: whether it came before or after "
            "another, and whether it was higher or lower. <bookmark mark='a'/> A spectrogram cannot get both right "
            "beyond Gabor's limit. <bookmark mark='b'/> Most of the listeners could. The best, a professional "
            f"musician, beat the limit by a factor of {say(d['best'])}. <bookmark mark='c'/> No law of mathematics "
            "was broken. The limit holds for analysis that is linear, where the response to two sounds is the sum "
            "of the responses to each. The ear is not linear, and it has had a very long time to learn what sounds "
            "are like. What it actually does is the subject of the next part."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(hyper), FadeIn(lim), FadeIn(tag))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in dots], lag_ratio=0.2), FadeIn(res[0]), FadeIn(res[1]))
            vo.wait_until("c")
            self.play(FadeIn(res[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open(self):
        items = VGroup(
            label(r"open, \ and active", font_size=28, color=LIMIT),
            label(r"sharper pictures: \ reassignment, \ synchrosqueezing (Daubechies, Lu and Wu, 2011), \ superresolution", font_size=24),
            label(r"which picture should a listening machine start from: \ a spectrogram, \ constant Q, \ or the raw wave? \ (Parts 61--66)", font_size=24),
            label(r"how much of timbre a short list of numbers can capture, \ and what the ear uses instead", font_size=24),
            label(r"$\bigstar$ \ Build a reassigned constant-Q transform, \ and measure how well it finds the onsets and pitches of Monochord's notes.",
                  font_size=24, color=TUNE),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        if items.width > 13.2:
            items.scale_to_fit_width(13.2)
        items.move_to(ORIGIN)
        with self.voiceover(
            "This is a live field. Sharper pictures of sound are still being invented. <bookmark mark='a'/> The "
            "machines that listen to music, which we build at the end of this series, have to choose what picture "
            "to start from, and the choice is not settled. <bookmark mark='b'/> Nor is the question of how much of "
            "an instrument's character a handful of numbers can hold. <bookmark mark='c'/> The research problem for "
            "this part is to combine two of this part's ideas."
        ) as vo:
            self.play(FadeIn(items[0]), FadeIn(items[1]))
            for mark, it in zip("abc", items[2:]):
                vo.wait_until(mark)
                self.play(FadeIn(it, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()
