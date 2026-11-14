from __future__ import annotations

import numpy as np

from videos.psychology.psych14.common import *  # noqa: F403


def panel(arr, title, color, height=3.3, hi=1.0):
    img = picture(np.asarray(arr), height, smooth=True, lo=0.0, hi=hi)
    cap = label(title, font_size=26, color=color).next_to(img, UP, buff=0.15)
    return Group(img, cap)


class Lightness(VoiceoverScene):
    def construct(self):
        self.card()
        self.product()
        self.retinex()
        self.result()
        self.limits()

    def card(self):
        card = chapter_card(8, r"The two squares, \ explained", r"How can equal light look unequal?",
                            lit={1971: r"Land \& McCann", 1995: r"Adelson"}, part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter eight. The two squares, explained."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def product(self):
        d = load("shadow")
        head = heading(r"Light = surface $\times$ illumination")
        L = panel(d["lum"], r"the light reaching the eye", WORLD, hi=0.85)
        R = panel(d["refl"], r"the surfaces", POST, hi=0.85)
        I_ = panel(d["illum"], r"the illumination", PRIOR, hi=1.0)
        row = Group(L, MathTex(r"=", font_size=56), R, MathTex(r"\times", font_size=56), I_).arrange(RIGHT, buff=0.35)
        row.move_to([0, 0.6, 0])
        if row.width > 13.4:
            row.scale_to_fit_width(13.4)
        rows = rows_of([
            (r"the eye receives only the product; \ the visual system wants the first factor", WHITE),
            (r"one equation, \ two unknowns at every point: \ the inverse problem again", LIKE),
            (r"to split them, \ assume something about each: \ surfaces change abruptly, \ light changes smoothly", PRIOR),
        ], 12.4, 28, 0.3).to_edge(DOWN, buff=0.7)
        tag = psyche_tag(r"computed: \ Psyche's checkerboard and its shadow")
        with self.voiceover(
            "Back to the two squares. <bookmark mark='a'/> The light reaching your eye from any point is the product "
            "of two things: how much light falls on the surface there, and what fraction the surface reflects. The "
            "picture on the left is the product of the two on the right: a checkerboard of surfaces, and a soft "
            "shadow. <bookmark mark='b'/> The eye receives only the product. What the visual system wants is the first "
            "factor, the surfaces, because surfaces are what things are made of. But at every point there's one "
            "number and two unknowns: the inverse problem again. <bookmark mark='c'/> To split them, you need an "
            "assumption about each. A natural pair: surfaces change abruptly, at their edges, while illumination "
            "changes smoothly, across shadows and gradients."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(L))
            vo.wait_until("a")
            self.play(FadeIn(row[1:]))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def retinex(self):
        head = heading(r"Retinex: \ keep the sharp edges, \ drop the gentle ones")
        steps = VGroup(
            MathTex(r"\log L = \log R + \log E", font_size=40),
            MathTex(r"\nabla \log L \;\to\; \text{keep where } |\nabla \log L| > \tau, \ \text{else } 0", font_size=40,
                    color=PRIOR),
            MathTex(r"\log \hat R = \text{integrate the kept edges, \ anchor the brightest at white}", font_size=40,
                    color=POST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, 1.0, 0])
        rows = rows_of([
            (r"logs turn the product into a sum", WHITE),
            (r"the checkerboard's edges are steep; \ the shadow's soft edge is gentle, \ and is thrown away", PRIOR),
            (r"Land and McCann, \ 1971: \ a model of lightness built from an inventor's colour experiments", GREY_A),
        ], 12.4, 28, 0.3).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Edwin Land, the inventor of the Polaroid camera, and John McCann turned that pair of assumptions into an "
            "algorithm in 1971. They called it retinex, from retina and cortex. <bookmark mark='a'/> Take logs, and "
            "the product becomes a sum: log light equals log reflectance plus log illumination. "
            "<bookmark mark='b'/> Now take differences between neighbouring points. Where the difference is large, "
            "it's an edge between surfaces: keep it. Where it's small, it's a gentle change in the light: set it to "
            "zero. <bookmark mark='c'/> Then add the kept edges back up, and anchor the result by calling the "
            "brightest surface white. What's left is an estimate of the surfaces alone."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(steps[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(steps[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Write(steps[2]), FadeIn(rows[2]))
        self.clear_scene()

    def result(self):
        d = load("shadow")
        head = heading(r"What retinex sees")
        L = panel(d["lum"], r"the light", WORLD, height=3.5, hi=0.85)
        R = panel(d["retinex"], r"retinex's surfaces", POST, height=3.5, hi=1.0)
        pair = Group(L, R).arrange(RIGHT, buff=0.6).move_to([-2.9, 0.3, 0])
        rows = rows_of([
            (rf"light: \ A {d['lum_A']:.2f}, \ B {d['lum_B']:.2f}", WORLD),
            (rf"retinex: \ A {d['ret_A']:.2f}, \ B {d['ret_B']:.2f}", POST),
            (rf"the true surfaces: \ A {d['refl_A']:.1f}, \ B {d['refl_B']:.1f}, \ \ a ratio of 2; \ retinex finds {d['ret_B'] / d['ret_A']:.2f}", GREY_A),
            (r"you, \ like retinex, \ see the surfaces: \ the illusion is the right answer about the board", YOU),
        ], 4.0, 26, 0.34).move_to([4.9, 0.0, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ retinex on Psyche's checkerboard, \ $\tau$ = 0.05")
        with self.voiceover(
            "Here's the result. <bookmark mark='a'/> On the left, the light, where squares A and B both send point "
            "four. <bookmark mark='b'/> On the right, retinex's estimate of the surfaces. The shadow is gone. Square A "
            "comes out at point five, and B at nearly one: B is about twice as light as A. <bookmark mark='c'/> The true "
            "surfaces, which we know because we built the board, are point four and point eight: also a ratio of "
            "two. Retinex gets the absolute levels wrong, because its anchor guesses that the brightest square is "
            "white, but the ratio very nearly right. <bookmark mark='d'/> And that's what you saw. The illusion was "
            "the correct answer about the board, and a wrong answer only about the picture of it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(L))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(R), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def limits(self):
        head = heading(r"Where edges are not enough")
        rows = rows_of([
            (r"the same edges can be a shadow, \ a stain or a fold: \ lightness depends on what the edge is taken to be", WHITE),
            (r"Gilchrist, \ 1977: \ change only the apparent depth of a surface, \ and its lightness changes", LIKE),
            (r"Knill and Kersten, \ 1991: \ the same shading, \ seen as a curved surface or a flat one, \ changes lightness", LIKE),
            (r"so lightness is inference about the scene, \ not filtering of the image", POST),
            (r"retinex is a good first model, \ and the dress of Part 13 was the same problem in colour", PRIOR),
        ], 12.6, 28, 0.38).move_to([0, -0.1, 0])
        with self.voiceover(
            "Retinex is a good first model. It isn't the whole story. <bookmark mark='a'/> The same edge in an image "
            "could be the border of a shadow, a stain on a surface, or a fold where a surface turns away from the "
            "light, and how light a surface looks depends on which the visual system decides it is. "
            "<bookmark mark='b'/> In 1977, Alan Gilchrist changed nothing but the apparent depth of a surface, making "
            "it seem to lie in a different plane, and its lightness changed dramatically. <bookmark mark='c'/> In "
            "1991, David Knill and Daniel Kersten showed that the same pattern of shading looks different in "
            "lightness depending on whether it's seen as a curved surface or a flat one. <bookmark mark='d'/> So "
            "lightness is an inference about the whole scene, its shapes, its lights and its surfaces together, not "
            "a filter on the image. <bookmark mark='e'/> The dress, at the end of Part 13, was the same problem in "
            "colour: one image, two theories of the light, two sets of surfaces."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
