from __future__ import annotations

import numpy as np

from videos.psychology.psych13.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.everywhere()
        self.chroma()
        self.design()

    def card(self):
        card = chapter_card(14, r"In practice: \ screens, \ codecs and palettes", r"Where is this theory built in?",
                            lit=(), part=PART, scale=("mind", "culture"), marr=("what",))
        with self.voiceover("Chapter fourteen. In practice: screens, codecs and palettes."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def everywhere(self):
        head = heading(r"Engineering on the standard observer")
        rows = rows_of([
            (r"a screen: \ three primaries, \ chosen from the 1931 diagram, \ mixed to make metamers of the world", LIGHT),
            (r"a camera: \ three filters over its sensor, \ playing the part of the cones", MCONE),
            (r"a colour standard (sRGB, \ the one the web assumes): \ a triangle on the diagram and a curve for "
             r"brightness", SCONE),
            (r"image and video codecs: \ spend bits where the CSF is high, \ fewer where it is low", CENTRE),
            (r"brightness steps, \ fonts, \ warning lights: \ thresholds and Weber fractions", GREY_A),
        ], 12.0, 29, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "Almost every piece of imaging technology you own is built on this part. <bookmark mark='a'/> A screen "
            "never reproduces the light of a scene. It mixes three primaries into a metamer, a different light that "
            "gives your cones the same three numbers. <bookmark mark='b'/> A camera puts three coloured filters over "
            "its sensor, playing the part of the cones. <bookmark mark='c'/> The colour standard the web assumes, "
            "sRGB, is a triangle on the 1931 diagram and a curve for brightness. <bookmark mark='d'/> And image and "
            "video compression spends its bits where your contrast sensitivity is high, and saves them where it's "
            "low. <bookmark mark='e'/> Even brightness controls, fonts and warning lights are designed with "
            "thresholds and Weber fractions in mind."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def chroma(self):
        d = load("practice")
        head = heading(r"Throw away colour detail, \ not brightness detail")
        a = picture(d["original"], 3.2).move_to([-4.6, 0.8, 0])
        b = picture(d["chroma_cut"], 3.2).move_to([0, 0.8, 0])
        c = picture(d["luma_cut"], 3.2).move_to([4.6, 0.8, 0])
        la = label(r"original", font_size=24, color=GREY_A).next_to(a, UP, buff=0.15)
        lb = wrapped_label(r"colour at a quarter of the resolution", 3.6, 22, MODEL).next_to(b, UP, buff=0.15)
        lc = wrapped_label(r"brightness at a quarter of the resolution", 3.6, 22, BAD).next_to(c, UP, buff=0.15)
        rows = rows_of([
            (r"the eye's colour channels have far lower acuity than its brightness channel", WHITE),
            (r"so codecs split an image into brightness and two colour differences, \ and store the colour at half "
             r"resolution each way: \ the 4:2:0 of video", MODEL),
            (rf"{num(d['bits_full'])} samples become {num(d['bits_420'])}: \ half the data, \ for a loss most people "
             rf"never notice", GREY_A),
        ], 12.4, 25, 0.22).to_edge(DOWN, buff=0.8)
        tag = psyche_tag(r"computed: \ a synthetic scene, \ coarsened four times in brightness or in colour")
        with self.voiceover(
            "Here's one trick in detail. <bookmark mark='a'/> Your colour channels, the opponent ones of chapter ten, "
            "have much lower acuity than your brightness channel. <bookmark mark='b'/> So nearly every image and video "
            "format splits a picture into brightness and two colour-difference signals, and stores the colour at "
            "half the resolution in each direction. On the left, a picture. In the middle, its colour stored at a "
            "quarter of the resolution: look closely, and it's hard to tell. On the right, its brightness at a "
            "quarter of the resolution instead: the thin lines and edges are smeared at once. <bookmark mark='c'/> "
            "Storing colour coarsely halves the data, for a loss most people never notice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(a), FadeIn(la))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(lb), FadeIn(rows[1]))
            self.play(FadeIn(c), FadeIn(lc))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def design(self):
        d = load("opponent")
        head = heading(r"Designing for every eye")
        rows = rows_of([
            (r"one reader in twelve men cannot separate colours that differ only in red versus green", LCONE),
            (r"so: \ never code a meaning in red against green alone", WHITE),
            (r"vary lightness as well as hue, \ add shapes or labels, \ and choose palettes checked against "
             r"dichromacy (chapter 10)", MODEL),
            (r"the same projection used in this film is built into design tools, \ to preview a figure as a "
             r"dichromat sees it", GREY_A),
        ], 7.2, 27, 0.36).move_to([2.6, -0.2, 0])
        keep_in_frame(rows)
        pal = VGroup(*[swatch(c, 0.7) for c in d["sims"]["okabe_none"]]).arrange(DOWN, buff=0.08).move_to([-4.6, -0.2, 0])
        pal2 = VGroup(*[swatch(c, 0.7) for c in d["sims"]["okabe_M"]]).arrange(DOWN, buff=0.08).next_to(pal, RIGHT, buff=0.3)
        l1 = label(r"normal", font_size=20, color=GREY_A).next_to(pal, UP, buff=0.12)
        l2 = label(r"no M cones", font_size=20, color=MCONE).next_to(pal2, UP, buff=0.12)
        tag = published_tag(archive.OKABE_ITO.cite)
        with self.voiceover(
            "And there's a rule for anyone who makes figures, maps or dashboards. <bookmark mark='a'/> Roughly one "
            "man in twelve can't separate colours that differ only along the red-green axis. <bookmark mark='b'/> So "
            "never put a meaning in red against green alone: stop and go, good and bad, up and down. "
            "<bookmark mark='c'/> Vary lightness as well as hue, add shapes or labels, and use palettes that have "
            "been checked against the projections of chapter ten, like Okabe and Ito's, shown here as seen normally "
            "and without middle cones. <bookmark mark='d'/> The same projection used in this film is built into "
            "common design tools, so you can preview a figure as a colour-blind reader will see it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(pal), FadeIn(l1))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(pal2), FadeIn(l2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
