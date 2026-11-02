from __future__ import annotations

import itertools

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, INFO, MART, P_C, PART

OUTCOMES = ["".join(o) for o in itertools.product("HT", repeat=3)]
X = np.array([o.count("H") for o in OUTCOMES], float)


def cond_exp(n):
    """E[X | the first n tosses], outcome by outcome."""
    out = np.empty(8)
    for i, o in enumerate(OUTCOMES):
        same = [j for j, p in enumerate(OUTCOMES) if p[:n] == o[:n]]
        out[i] = X[same].mean()
    return out


class Information(VoiceoverScene):
    def construct(self):
        self.card()
        self.filtration()
        self.projection()

    def card(self):
        c = chapter_card(1, r"Information and conditional expectation", r"What do you know, and when?", part=PART)
        with self.voiceover("Chapter one. Information, and conditional expectation."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def filtration(self):
        w = 1.32
        cells = VGroup(*[VGroup(RoundedRectangle(width=w - 0.12, height=0.7, corner_radius=0.08, stroke_color=GREY_B,
                                                 stroke_width=1.5),
                                MathTex(o, font_size=30)) for o in OUTCOMES]).arrange(RIGHT, buff=0.12)
        for c in cells:
            c[1].move_to(c[0])
        cells.to_edge(UP, buff=1.0).shift(RIGHT * 0.6)
        xs = VGroup(*[MathTex(rf"{int(v)}", font_size=26, color=GREY_A).next_to(c, UP, buff=0.12)
                      for c, v in zip(cells, X)])
        xlab = MathTex(r"X = \#\text{heads}", font_size=28, color=GREY_A).next_to(xs, LEFT, buff=0.3)

        def blocks(n):
            g = VGroup()
            size = 8 // 2 ** n
            for b in range(2 ** n):
                grp = VGroup(*cells[b * size:(b + 1) * size])
                g.add(SurroundingRectangle(grp, buff=0.05, color=INFO, stroke_width=3, corner_radius=0.1))
            return g

        base_y = cells.get_bottom()[1] - 0.4
        unit = 0.8

        def bars(n):
            vals = cond_exp(n)
            g = VGroup()
            for c, v in zip(cells, vals):
                r = Rectangle(width=w - 0.4, height=v * unit + 1e-3, stroke_width=0, fill_color=MART, fill_opacity=0.8)
                r.move_to([c.get_x(), base_y, 0], aligned_edge=UP)
                t = MathTex(f"{v:g}", font_size=24, color=MART).next_to(r, DOWN, buff=0.08)
                g.add(VGroup(r, t))
            return g

        nlab = [MathTex(rf"\mathcal{{F}}_{n}", r"\text{: after toss } " + str(n) if n else r"\text{: before any toss}",
                        font_size=32, color=INFO) for n in range(4)]
        for m in nlab:
            m.to_corner(DL, buff=0.6)
        elab = MathTex(r"\mathbb{E}[X \mid \mathcal{F}_n]", font_size=34, color=MART).to_corner(DR, buff=0.6)
        current_b, current_bar = blocks(0), bars(0)
        defs = VGroup(
            label(r"a filtration: the questions you can answer at each time, growing", font_size=22, color=INFO),
            label(r"conditional expectation: the best guess of $X$ given what you know", font_size=22, color=MART),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=1.4)
        with self.voiceover(
            "Probability in finance is about information: what you know, and when. Toss a coin three times. There are "
            "eight possible worlds, and X counts the heads in each. <bookmark mark='a'/> Before any toss you cannot "
            "tell the worlds apart: they all sit in one block. Your best guess of X is its average, one and a half, "
            "in every world. <bookmark mark='b'/> After the first toss, the worlds split in two. If it was heads, the "
            "best guess is two; if tails, one. <bookmark mark='c'/> After the second toss, four blocks, and four "
            "guesses. <bookmark mark='d'/> After the third, you know X exactly. <bookmark mark='e'/> The growing "
            "sequence of partitions is called a filtration: the questions you can answer at each time. And the best "
            "guess on each block, the average over the worlds you can't yet tell apart, is the conditional "
            "expectation of X given what you know. Watch the guess: it moves only when information arrives, and "
            "on average it doesn't move at all."
        ) as vo:
            self.play(FadeIn(cells), FadeIn(xs), FadeIn(xlab))
            vo.wait_until("a")
            self.play(Create(current_b), FadeIn(nlab[0]), FadeIn(elab), LaggedStart(*[GrowFromEdge(b[0], UP) for b in current_bar]),
                      FadeIn(VGroup(*[b[1] for b in current_bar])))
            for n, mark in zip((1, 2, 3), ("b", "c", "d")):
                vo.wait_until(mark)
                nb, nbar = blocks(n), bars(n)
                self.play(ReplacementTransform(current_b, nb), ReplacementTransform(current_bar, nbar),
                          ReplacementTransform(nlab[n - 1], nlab[n]), run_time=1.5)
                current_b, current_bar = nb, nbar
            vo.wait_until("e")
            self.play(FadeIn(defs))
        self.wait(0.4)
        self.clear_scene()

    def projection(self):
        o = np.array([-2.6, -1.6, 0])
        plane = Polygon(o + np.array([-2.2, -0.6, 0]), o + np.array([3.6, -0.6, 0]), o + np.array([5.2, 1.4, 0]),
                        o + np.array([-0.6, 1.4, 0]), stroke_color=INFO, stroke_width=1.5, fill_color=INFO,
                        fill_opacity=0.12)
        line = Line(o + np.array([-1.6, -0.35, 0]), o + np.array([4.6, 0.55, 0]), color=DRIFT, stroke_width=3)
        tip = o + np.array([2.2, 3.4, 0])
        foot = o + np.array([2.2, 0.75, 0])
        d = line.get_unit_vector()
        foot2 = line.get_start() + np.dot(foot - line.get_start(), d) * d
        vX = Arrow(o, tip, buff=0, color=WHITE, stroke_width=4)
        vP = Arrow(o, foot, buff=0, color=MART, stroke_width=4)
        err = DashedLine(tip, foot, color=GREY_B)
        ra = VGroup(Line(foot + UP * 0.25, foot + UP * 0.25 + LEFT * 0.25), Line(foot + LEFT * 0.25, foot + UP * 0.25 + LEFT * 0.25)).set_stroke(GREY_B, 1.5)
        vP2 = Arrow(o, foot2, buff=0, color=DRIFT, stroke_width=4)
        err2 = DashedLine(foot, foot2, color=GREY_B)
        lX = MathTex(r"X", font_size=34).next_to(tip, UP, buff=0.1)
        lP = MathTex(r"\mathbb{E}[X \mid \mathcal{G}]", font_size=30, color=MART).next_to(foot, RIGHT, buff=0.15)
        lP2 = MathTex(r"\mathbb{E}[X \mid \mathcal{H}]", font_size=30, color=DRIFT).next_to(foot2, DOWN, buff=0.2)
        lplane = label(r"everything you could compute from $\mathcal{G}$", font_size=20, color=INFO).next_to(
            plane, DOWN, buff=0.1).align_to(plane, LEFT)
        lline = label(r"from less information, $\mathcal{H} \subset \mathcal{G}$", font_size=20, color=DRIFT).next_to(
            line.get_end(), RIGHT, buff=0.1)
        side = VGroup(
            label(r"the closest variable you can compute:", font_size=22, color=GREY_A),
            MathTex(r"\mathbb{E}[X \mid \mathcal{G}] = \arg\min_{Z\ \mathcal{G}\text{-measurable}} \mathbb{E}[(X - Z)^2]",
                    font_size=28, color=MART),
            label(r"the error is orthogonal to all of them", font_size=22, color=GREY_A),
            MathTex(r"\mathbb{E}\big[(X - \mathbb{E}[X \mid \mathcal{G}])\,Z\big] = 0", font_size=28),
            label(r"the tower property: project twice, or once", font_size=22, color=GREY_A),
            MathTex(r"\mathbb{E}\big[\mathbb{E}[X \mid \mathcal{G}] \mid \mathcal{H}\big] = \mathbb{E}[X \mid \mathcal{H}]",
                    font_size=28, color=DRIFT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.4)
        with self.voiceover(
            "There is a picture behind this. Think of random variables as vectors, with the length of a vector its "
            "root mean square. The variables you could compute from your information form a flat subspace, here a "
            "plane. <bookmark mark='a'/> The conditional expectation of X is the point of that plane closest to X: "
            "its orthogonal projection. The error, what you can't know, is at right angles to everything you can. "
            "That is why conditional expectation is the best forecast in mean square, and why least-squares "
            "regression, in Part six, is the same operation with data. <bookmark mark='b'/> Now take even less "
            "information, a line inside the plane. Projecting X onto the plane and then onto the line lands in the "
            "same place as projecting straight onto the line. That is the tower property: your forecast of my "
            "forecast, when you know less than I do, is just your forecast."
        ) as vo:
            self.play(FadeIn(plane), FadeIn(lplane), GrowArrow(vX), FadeIn(lX))
            vo.wait_until("a")
            self.play(Create(err), GrowArrow(vP), FadeIn(lP), FadeIn(ra), FadeIn(side[:4]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(lline))
            self.play(Create(err2), GrowArrow(vP2), FadeIn(lP2), FadeIn(side[4:]))
        self.wait(0.4)
        self.clear_scene()
