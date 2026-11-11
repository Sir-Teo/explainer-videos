from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs57.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


class Hook(VoiceoverScene):
    def construct(self):
        self.puzzle()
        self.questions()
        self.plan()

    def puzzle(self):
        d = load("descent")
        rows = d["rows"]
        head = label(r"More parameters than examples, \ and it still works", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 200, 50], y_range=[-1, 2, 1], x_length=9.0, y_length=4.4,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.5)
        xt = VGroup(*[label(rf"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, -1), DOWN, buff=0.1)
                      for v in (0, 50, 100, 150, 200)])
        yt = VGroup(*[label(rf"$10^{{{v}}}$", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (-1, 0, 1, 2)])
        xl = label(r"parameters $p$ \ (examples: \ $n = 50$)", font_size=18, color=GREY_A).next_to(ax, DOWN,
                                                                                               buff=0.45)
        yl = label(r"test error", font_size=18, color=GREY_A).next_to(ax, LEFT, buff=0.7).shift(UP * 1.5)
        pts = [ax.c2p(r["p"], math.log10(max(r["test"], 0.1))) for r in rows]
        left = [p for p, r in zip(pts, rows) if r["p"] <= d["n"]]
        right = [p for p, r in zip(pts, rows) if r["p"] >= d["n"]]
        c1 = VMobject(color=NO, stroke_width=3).set_points_as_corners(left)
        c2 = VMobject(color=YES, stroke_width=3).set_points_as_corners(right)
        peak = DashedLine(ax.c2p(d["n"], -1), ax.c2p(d["n"], 2), color=HEAD, stroke_width=1.5)
        pl = label(r"$p = n$: \ the model can fit any data, \ noise included", font_size=17, color=HEAD).next_to(
            ax.c2p(d["n"], 2), RIGHT, buff=0.2).shift(DOWN * 0.2)
        best = min(rows, key=lambda r: r["test"])
        note_ = note(r"minimum-norm least squares on Gaussian features; \ median of 50 trials", font_size=16).to_edge(
            DOWN, buff=0.3)
        with self.voiceover(
            "Here is a puzzle that learning theory had to face. <bookmark mark='a'/> We fit fifty noisy examples with "
            "a linear model that uses p features. With few features the model is too simple. As p grows, the error on "
            "new data rises, slowly and then steeply, the classical picture of overfitting. <bookmark mark='b'/> At p equal "
            "to fifty the model can fit anything, noise included, and the test error explodes. <bookmark mark='c'/> "
            "And then, past that point, adding still more parameters makes the error fall again, to below where it "
            f"started: at {best['p']} features it is lower than any model with fewer parameters than examples. "
            "This is double descent. To understand it we first need the classical theory: when is learning possible "
            "at all, and how many examples does it take?"
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(note_))
            vo.wait_until("a")
            self.play(Create(c1), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(peak), FadeIn(pl))
            vo.wait_until("c")
            self.play(Create(c2), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def questions(self):
        head = label(r"Three questions, \ three kinds of answer", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup()
        for q, a, col in ((r"How many examples does learning need?", r"PAC learning and the VC dimension", HEAD),
                          (r"What if an adversary picks the examples?", r"online learning, \ regret and bandits",
                           YES),
                          (r"What can never be learned efficiently?", r"cryptography and statistical queries", NO)):
            box = RoundedRectangle(width=12.0, height=1.2, corner_radius=0.15, stroke_color=col, stroke_width=2,
                                   fill_color=BG, fill_opacity=1)
            g = VGroup(label(q, font_size=24, color=WHITE), label(a, font_size=20, color=col)).arrange(
                DOWN, buff=0.15).move_to(box)
            rows.add(VGroup(box, g))
        rows.arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.5)
        foot = note(r"Valiant \ (1984); \ Vapnik and Chervonenkis \ (1971); \ Littlestone \ (1988); \ Kearns and "
                    r"Valiant \ (1994)", font_size=16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "AI, Built showed machines that learn. This part asks what can be proved about them. "
            "<bookmark mark='a'/> How many examples does a learner need before its answers are probably "
            "approximately correct? Leslie Valiant made the question precise in 1984, and the answer is a single "
            "number, the VC dimension. <bookmark mark='b'/> What if no distribution exists and an adversary picks "
            "every example? Then the right measure is regret, and the answers include the bandits of Part 44. "
            "<bookmark mark='c'/> And what can never be learned efficiently, however much data there is? There the "
            "answers come from cryptography."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.15))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Learning Theory", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"PAC learning and the finite-class bound",
            r"VC dimension, \ Sauer--Shelah, \ and the fundamental theorem",
            r"margins: \ the perceptron, \ boosting",
            r"online learning, \ regret and bandits",
            r"what cannot be learned: \ parity and cryptography",
            r"double descent, \ and learning as compression",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 57 of Computer Science, Built. <bookmark mark='a'/> We will define probably approximately "
            "correct learning; prove that the VC dimension decides how many examples are needed; see why margins, "
            "not dimensions, govern the perceptron and boosting; learn online against an adversary and bound the "
            "regret; meet problems that cannot be learned efficiently; and return to double descent and to learning "
            "as compression."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (DATA, KERN, LAM, NO, YES)
