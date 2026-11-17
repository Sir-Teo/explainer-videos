from __future__ import annotations

import numpy as np

from videos.psychology.psych13.common import *  # noqa: F403
from videos.psychology.psych13.s09_cones import spectrum_strip, wl_axes


class Opponent(VoiceoverScene):
    def construct(self):
        self.card()
        self.hering()
        self.channels()
        self.deficiency()

    def card(self):
        card = chapter_card(10, r"Opponent colours and colour blindness", r"Why is there no reddish green?",
                            lit={1878: r"Hering", 1957: r"Hurvich and Jameson"}, part=PART, scale=("circuit", "mind"),
                            marr=("how",))
        with self.voiceover("Chapter ten. Opponent colours, and colour blindness."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def hering(self):
        head = heading(r"Hering's puzzle")
        pairs = VGroup()
        for a, b, ok in (("#d33", "#3b3", False), ("#33d", "#dd3", False), ("#d33", "#dd3", True), ("#3b3", "#33d", True)):
            sw = VGroup(Square(0.8, stroke_width=0, fill_color=a, fill_opacity=1), Square(0.8, stroke_width=0, fill_color=b,
                                                                                      fill_opacity=1)).arrange(RIGHT, buff=0)
            mark = MathTex(r"\checkmark" if ok else r"\times", font_size=40, color=MODEL if ok else BAD)
            pairs.add(VGroup(sw, mark).arrange(RIGHT, buff=0.3))
        pairs.arrange_in_grid(2, 2, buff=(1.0, 0.5)).move_to([-3.6, 0.2, 0])
        cap = VGroup(label(r"reddish yellow: \ orange", font_size=22, color=GREY_A),
                     label(r"bluish green: \ teal", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT).next_to(
            pairs, DOWN, buff=0.35)
        rows = rows_of([
            (r"Ewald Hering, \ 1878: \ some hues mix in experience, \ some never do", WHITE),
            (r"no colour looks reddish green, \ or bluish yellow", BAD),
            (r"so, \ he proposed, \ colour is coded by opposed pairs: \ red against green, \ blue against yellow, \ "
             r"and light against dark", LIGHT),
            (r"for eighty years this looked like a rival to Young's three receptors; \ both were right, \ at "
             r"different stages", GREY_A),
        ], 5.6, 27, 0.34).move_to([3.4, -0.1, 0])
        keep_in_frame(rows)
        with self.voiceover(
            "Three cones explain matching. They don't explain what colours look like. <bookmark mark='a'/> In 1878 "
            "Ewald Hering pointed out that some hues mix in experience and some never do. Orange looks reddish "
            "yellow; teal looks bluish green. <bookmark mark='b'/> But nothing looks reddish green, or bluish yellow. "
            "<bookmark mark='c'/> So, he proposed, colour is coded in opposed pairs: red against green, blue against "
            "yellow, and light against dark. A signal can be red or green, but not both. <bookmark mark='d'/> For "
            "eighty years Hering's pairs and Young's three receptors looked like rival theories. Both were right, at "
            "different stages of the same machine."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pairs), FadeIn(cap))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r))
        self.clear_scene()

    def channels(self):
        d = load("opponent")
        head = heading(r"From three cones to three opposed channels")
        A = wl_axes([-2.8, -0.2, 0], y_length=4.0, x_length=6.8, ylabel=r"channel response", yr=(-1.0, 2.0), yt=(-1, 0, 1, 2))
        ax = A.ax
        wl = d["wl"]
        zero = DashedLine(ax.c2p(390, 0), ax.c2p(720, 0), color=GREY_D, stroke_width=1.5)
        o = d["opp"]
        lum = curve_in(ax, wl, o[:, 0], WHITE, stroke_width=4)
        rg = curve_in(ax, wl, o[:, 1], LCONE, stroke_width=4)
        by = curve_in(ax, wl, o[:, 2], SCONE, stroke_width=4)
        strip = spectrum_strip(6.8).next_to(ax, DOWN, buff=0.08).align_to(ax, LEFT)
        z = Dot(ax.c2p(d["zero_lm"], 0), radius=0.08, color=LIGHT)
        zl = label(rf"{d['zero_lm']:.0f} nm", font_size=21, color=LIGHT).next_to(z, UP, buff=0.12)
        lg = legend([(WHITE, r"L + M: \ light-dark"), (LCONE, r"L $-$ M: \ red-green"), (SCONE, r"S $-$ (L + M): \ blue-yellow")],
                    font_size=21).move_to([4.2, 1.6, 0])
        rows = rows_of([
            (r"subtract one cone's signal from another's, \ and the result can be positive or negative, \ never both",
             WHITE),
            (r"where the red-green channel crosses zero, \ the colour is neither red nor green: \ near the yellow "
             r"observers call pure, \ about 575 to 580 nm", LIGHT),
            (r"Hurvich and Jameson, \ 1957: \ measured the channels by cancelling hues, \ adding green until no red "
             r"was left", GREY_A),
            (r"cells that add some cones and subtract others are found from the retina onward", CENTRE),
        ], 4.8, 23, 0.27).move_to([4.2, -1.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ weighted differences of the cone curves")
        with self.voiceover(
            "Here's how three cones become three opposed signals. <bookmark mark='a'/> Add the long and middle cones "
            "and you get brightness. Subtract them, and you get a signal that's positive for long wavelengths and "
            "negative for middle ones: red against green. Subtract the sum of long and middle from the short cones, "
            "and you get blue against yellow. A difference can be positive or negative, but never both at once. "
            "That's why there's no reddish green. <bookmark mark='b'/> Where the red-green channel crosses zero, a "
            "light is neither red nor green. With these weights that's near five eighty nanometres, close to the "
            "yellow that observers call pure, with no red or green in it. <bookmark mark='c'/> In 1957 Leo Hurvich "
            "and Dorothea Jameson measured such channels by cancellation: add green to a light until no red is "
            "left, and the amount needed is the strength of the red. <bookmark mark='d'/> And cells that add some "
            "cones and subtract others have been recorded from the retina onward."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(strip), FadeIn(tag), Create(zero))
            vo.wait_until("a")
            self.play(Create(lum), Create(rg), Create(by), FadeIn(lg), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(z), FadeIn(zl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def deficiency(self):
        d = load("opponent")
        head = heading(r"Colour blindness: \ a lost dimension")
        sims = d["sims"]

        def row(key, y, text, col):
            sw = VGroup(*[swatch(c, 0.62) for c in sims[key]]).arrange(RIGHT, buff=0.06)
            lab = label(text, font_size=21, color=col)
            g = VGroup(lab, sw).arrange(RIGHT, buff=0.3)
            return g

        dist = d["dist"]
        left = VGroup(label(r"a rainbow palette", font_size=24, color=WHITE),
                      row("rainbow_none", 0, rf"normal \ ($\Delta E$ {dist['rainbow_none'][0]:.0f})", GREY_A),
                      row("rainbow_L", 0, rf"no L cones \ ({dist['rainbow_L'][0]:.0f})", LCONE),
                      row("rainbow_M", 0, rf"no M cones \ ({dist['rainbow_M'][0]:.0f})", MCONE)).arrange(DOWN, aligned_edge=RIGHT, buff=0.25)
        right = VGroup(label(r"Okabe and Ito's palette", font_size=24, color=WHITE),
                       row("okabe_none", 0, rf"normal \ ({dist['okabe_none'][0]:.0f})", GREY_A),
                       row("okabe_L", 0, rf"no L cones \ ({dist['okabe_L'][0]:.0f})", LCONE),
                       row("okabe_M", 0, rf"no M cones \ ({dist['okabe_M'][0]:.0f})", MCONE)).arrange(DOWN, aligned_edge=RIGHT, buff=0.25)
        g = VGroup(left, right).arrange(RIGHT, buff=0.8).move_to([0, 0.9, 0])
        keep_in_frame(g)
        rows = rows_of([
            (r"about 8\% of men and 0.5\% of women of northern European ancestry lack or have altered L or M cones: \ "
             r"the genes are on the X chromosome", WHITE),
            (r"with two cone types, \ the red-green axis collapses: \ every colour lies on a plane; \ colours that "
             r"differ only along the lost axis become identical", LCONE),
            (r"numbers in brackets: \ the smallest colour difference between any two swatches, \ CIE $\Delta E$", GREY_A),
        ], 12.4, 24, 0.24)
        rows.next_to(g, DOWN, buff=0.55)
        tags = VGroup(published_tag(archive.OKABE_ITO.cite), psyche_tag(r"computed: \ dichromacy as a projection"))
        with self.voiceover(
            "The same algebra explains colour blindness. <bookmark mark='a'/> About eight percent of men and half a "
            "percent of women of northern European ancestry have missing or altered long or middle cones. The "
            "genes for those two pigments sit on the X chromosome, which is why men, with one X, are affected so "
            "much more often. John Dalton, the chemist, described his own case in 1794. <bookmark mark='b'/> With "
            "only two cone types, the red-green dimension collapses. Every colour lands on a plane, and colours that "
            "differed only along the lost direction become identical. Here are two palettes, as seen with all three "
            "cones and simulated without one. In the familiar rainbow palette, the red and the brown become almost "
            "indistinguishable without long cones. Masataka Okabe and Kei Ito's palette was designed to stay "
            "distinct either way. <bookmark mark='c'/> The numbers measure the smallest difference between any two "
            "swatches."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tags), FadeIn(left[0]), FadeIn(left[1]), FadeIn(right[0]), FadeIn(right[1]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(left[2:]), FadeIn(right[2:]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
