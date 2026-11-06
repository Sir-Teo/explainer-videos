from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, load, mono, words)


def sign_image(fl, ex=None, scale=4):
    """The orientation signs as pixels: left blue, right green, zero grey; wrong ones (against ``ex``) in red."""
    fl = np.asarray(fl)
    img = np.zeros(fl.shape + (3,), dtype=np.uint8)
    img[fl > 0] = (74, 144, 226)
    img[fl < 0] = (91, 209, 122)
    img[fl == 0] = (90, 90, 100)
    if ex is not None:
        ex = np.asarray(ex)
        img[(fl != ex)] = (255, 92, 92)
    img = img[::-1]                                     # row 0 at the bottom
    img = np.repeat(np.repeat(img, scale, axis=0), scale, axis=1)
    m = ImageMobject(img)
    m.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return m


class Hook(VoiceoverScene):
    def construct(self):
        self.question()
        self.grid()
        self.plan()

    def question(self):
        d = load("hook")
        ex = d["example"]
        head = label(r"Is $p$ to the left of the line through $q$ and $r$?", font_size=34).to_edge(UP, buff=0.35)
        line = Line(LEFT * 6.2 + DOWN * 2.4, LEFT * 0.4 + UP * 1.1, color=GREY_B, stroke_width=2.5)
        q = Dot(line.point_from_proportion(0.62), color=DATA, radius=0.08)
        r = Dot(line.point_from_proportion(0.92), color=DATA, radius=0.08)
        p = Dot(line.point_from_proportion(0.12), color=HEAD, radius=0.08)
        labs = VGroup(MathTex("q = (12, 12)", font_size=28, color=DATA).next_to(q, DR, buff=0.12),
                      MathTex("r = (24, 24)", font_size=28, color=DATA).next_to(r, DR, buff=0.12),
                      MathTex("p", font_size=30, color=HEAD).next_to(p, UP + LEFT, buff=0.1))
        pv = VGroup(mono(f"p.x = {ex['p'][0]}", 20, HEAD), mono(f"p.y = {ex['p'][1]}", 20, HEAD)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.5).shift(UP * 1.2)
        names = ["orient(p, q, r)", "orient(q, r, p)", "orient(r, p, q)"]
        word = {1: ("left", DATA), 0: ("on the line", GREY_B), -1: ("right", YES)}
        rows = VGroup()
        for nm, s in zip(names, ex["signs"]):
            w, c = word[s]
            rows.add(VGroup(mono(nm, 20, WHITE), mono(f"{s:+d}", 22, c), label(w, font_size=22, color=c)
                            ).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(pv, DOWN, buff=0.45).align_to(pv, LEFT)
        truth = label(r"exactly: \ \textbf{right}, \ always", font_size=24, color=YES).next_to(rows, DOWN, buff=0.4
                                                                                            ).align_to(rows, LEFT)
        VGroup(pv, rows, truth).to_edge(RIGHT, buff=0.45)
        cap = label(rf"one question asked three ways in double precision: \ three answers. \ Near this line, \ "
                    rf"{words(d['disagree'])} of the {words(d['n'] ** 2)} nearest floats disagree with themselves",
                    font_size=20, color=NO).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is the most basic question in computational geometry. Is the point p to the left of the line "
            "through q and r, or to the right, or on it? <bookmark mark='a'/> Take q at twelve, twelve and r at "
            "twenty-four, twenty-four, and put p a whisker from the point one half, one half, a few floating-point "
            "steps off the line. <bookmark mark='b'/> The test is a two by two determinant, and the answer should "
            "not depend on which point we list first. In double precision it does. Ask it one way and p is on the "
            "left. Rotate the three points and p is exactly on the line. Rotate again and p is on the right. "
            "<bookmark mark='c'/> The true answer is right, every time. <bookmark mark='d'/> This is not a rare "
            "accident: near this line, thousands of the nearest floating-point points get contradictory answers, "
            "and algorithms built on contradictory answers crash, loop forever, or return hulls that are not "
            "convex."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(q), FadeIn(r))
            vo.wait_until("a")
            self.play(FadeIn(labs), FadeIn(p), FadeIn(pv))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.1) for x in rows], lag_ratio=0.6), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(truth))
            vo.wait_until("d")
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    def grid(self):
        o = load("orient")
        head = label(r"Every float within 256 steps of $(\tfrac12, \tfrac12)$", font_size=32).to_edge(UP, buff=0.3)
        img = sign_image(o["grid_float"], scale=3).set_height(5.2).move_to(LEFT * 3.0 + DOWN * 0.35)
        img2 = sign_image(o["grid_float"], o["grid_exact"], scale=3).set_height(5.2).move_to(img)
        key = VGroup(
            label(r"blue: \ floating point says \textbf{left}", font_size=22, color=DATA),
            label(r"green: \ it says \textbf{right}", font_size=22, color=YES),
            label(r"grey: \ it says \textbf{on the line}", font_size=22, color=GREY_B),
            label(rf"red: \ \textbf{{wrong}}: \ {words(o['wrong'])} of 65,536", font_size=22, color=NO),
            label(rf"the true line holds {o['zero_exact']} of these points; \ floating point puts "
                  rf"{words(o['zero_float'])} on it", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        if key.width > 6.4:
            key.width = 6.4
            key.to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Kettner and his colleagues drew the picture in 2008. <bookmark mark='a'/> Take every float within two "
            "hundred and fifty-six steps of one half, one half, a grid of sixty-five thousand points, and colour "
            "each by what floating point says: blue for left, green for right, grey for on the line. The true line "
            "runs exactly along the diagonal. <bookmark mark='b'/> Instead of a clean split, a speckled band. "
            "<bookmark mark='c'/> Mark the wrong answers in red: nearly twelve thousand. This part starts by "
            "fixing that test, and then builds on it the beautiful structures of the plane."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(img), FadeIn(key[:3]))
            vo.wait_until("b")
            self.play(Indicate(img, scale_factor=1.02))
            vo.wait_until("c")
            self.play(FadeIn(img2), FadeIn(key[3:]))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Geometry", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"the orientation test, \ and how to make it exact without paying for exactness",
            r"convex hulls, \ the sweep line, \ and guarding an art gallery",
            r"Voronoi diagrams by Fortune's sweep; \ Delaunay triangulations, \ and the lifting map between them",
            r"randomized incremental algorithms, \ and backwards analysis to price them",
            r"linear programming in the plane, \ kd-trees, \ point location, \ and high dimensions",
            r"duality, \ motion planning, \ and the frontier: \ exactness, \ 3SUM, \ nearest neighbours",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 22 of Computer Science, Built: Geometry. <bookmark mark='a'/> In this part: the orientation test, "
            "made exact at almost no cost; convex hulls, the sweep line, and guards for an art gallery; Voronoi "
            "diagrams grown by a sweep of parabolas, and Delaunay triangulations, which turn out to be the shadow of "
            "a three-dimensional hull; randomized algorithms and the backwards analysis that prices them; linear "
            "programming, range search, point location and the curse of high dimensions; and motion planning for "
            "a robot."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
