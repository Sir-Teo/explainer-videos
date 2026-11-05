from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


class Closest(VoiceoverScene):
    def construct(self):
        self.card()
        self.split()
        self.strip()
        self.measured()

    def card(self):
        card = chapter_card(8, r"The closest pair", r"Must we compare every pair of points?", lit=(1975,),
                            extra=((1975, r"Shamos and Hoey"),), part=PART)
        with self.voiceover("Chapter eight. The closest pair."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def split(self):
        d = load("closest")
        head = label(r"Divide and conquer, \ in the plane", font_size=34).to_edge(UP, buff=0.3)
        pts = sorted(map(tuple, d["show"]))
        dots = VGroup(*[Dot([x, y, 0], radius=0.06, color=DATA) for x, y in pts])
        mid = len(pts) // 2
        xm = (pts[mid - 1][0] + pts[mid][0]) / 2
        line = DashedLine([xm, 2.7, 0], [xm, -3.1, 0], color=GREY_B, stroke_width=2)

        def best(ps):
            b, pair = math.inf, None
            for i in range(len(ps)):
                for j in range(i + 1, len(ps)):
                    dd = math.dist(ps[i], ps[j])
                    if dd < b:
                        b, pair = dd, (ps[i], ps[j])
            return b, pair
        dl, pl = best(pts[:mid])
        dr, pr = best(pts[mid:])
        segl = Line([*pl[0], 0], [*pl[1], 0], color=YES, stroke_width=4)
        segr = Line([*pr[0], 0], [*pr[1], 0], color=LAM, stroke_width=4)
        side = VGroup(
            label(r"sort by $x$; \ split at the median", font_size=22, color=GREY_A),
            label(r"solve each half recursively: \ $\delta_L$ and $\delta_R$", font_size=22, color=GREY_A),
            label(r"$\delta = \min(\delta_L, \delta_R)$: \ the only better pair must cross the line", font_size=22,
                  color=HEAD),
            label(r"and cross it within $\delta$ of the line", font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Given a million points, which two are closest? Comparing every pair is half a trillion distances. "
            "<bookmark mark='a'/> Michael Shamos and Dan Hoey's divide and conquer, from 1975: sort the points "
            "from left to right and split them at the median. <bookmark mark='b'/> Find the closest pair on each "
            "side, recursively. <bookmark mark='c'/> Call the smaller of the two distances delta. Any pair closer "
            "than delta must have one point on each side of the line. <bookmark mark='d'/> And both of its points "
            "must lie within delta of the line, in a thin strip."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dots))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(segl), Create(segr), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            delta = min(dl, dr)
            strip = Rectangle(width=2 * delta, height=5.8, stroke_width=0, fill_color=HEAD, fill_opacity=0.15).move_to(
                [xm, -0.2, 0])
            self.play(FadeIn(strip), FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def strip(self):
        head = label(r"Why the strip is cheap", font_size=34).to_edge(UP, buff=0.3)
        s = 1.1
        c0 = np.array([-3.2, -0.6, 0])
        box = Rectangle(width=4 * s, height=2 * s, color=HEAD, stroke_width=2.5).move_to(c0)
        grid = VGroup(*[Line(c0 + np.array([x * s - 2 * s, -s, 0]), c0 + np.array([x * s - 2 * s, s, 0]),
                             color=GREY_D, stroke_width=1.5) for x in (1, 2, 3)],
                      Line(c0 + np.array([-2 * s, 0, 0]), c0 + np.array([2 * s, 0, 0]), color=GREY_D, stroke_width=1.5))
        mid = DashedLine(c0 + np.array([0, -1.4 * s, 0]), c0 + np.array([0, 1.4 * s, 0]), color=GREY_B)
        p = Dot(c0 + np.array([-0.6 * s, -s, 0]), radius=0.09, color=YES)
        pl = MathTex(r"p", font_size=28, color=YES).next_to(p, DOWN, buff=0.08)
        dl = label(r"$2\delta$ wide, \ $\delta$ high", font_size=20, color=HEAD).next_to(box, UP, buff=0.15)
        sq = label(r"8 squares of side $\delta / 2$", font_size=20, color=GREY_A).next_to(box, DOWN, buff=0.45)
        steps = VGroup(
            label(r"sort the strip by $y$; \ compare each point $p$ only with those above it within $\delta$",
                  font_size=21, color=GREY_A),
            label(r"they lie in a $2\delta \times \delta$ box, \ cut into eight $\frac{\delta}{2}$ squares", font_size=21,
                  color=GREY_A),
            label(r"two points in one square would be closer than $\frac{\delta}{\sqrt 2} < \delta$, \ on the same "
                  r"side: \ impossible", font_size=21, color=HEAD),
            label(r"so at most 7 comparisons per point: \ the strip costs $O(n)$", font_size=22, color=YES),
            MathTex(r"T(n) = 2\,T(n/2) + O(n) = O(n \log n)", font_size=32, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        if steps.width > 6.8:
            steps.scale_to_fit_width(6.8).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The strip could hold almost every point, so why is it cheap? <bookmark mark='a'/> Sort the strip's "
            "points from bottom to top, and compare each point only with the points above it, less than delta "
            "higher. <bookmark mark='b'/> Those all lie in a box two delta wide and delta high, which cuts into "
            "eight squares of side delta over two. <bookmark mark='c'/> Each square lies on one side of the line, "
            "and any two points in it would be less than delta apart, closer than the best pair on that side. So "
            "each square holds at most one point. <bookmark mark='d'/> Hence each point needs at most seven "
            "comparisons, and the strip costs linear time. <bookmark mark='e'/> Two half-size problems and linear "
            "work: n log n, by the same recurrence as merge sort and the FFT."
        ) as vo:
            self.play(FadeIn(head), Create(box), Create(mid), FadeIn(p), FadeIn(pl), FadeIn(dl))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(Create(grid), FadeIn(sq), FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("closest")
        head = label(r"Counted and timed", font_size=34).to_edge(UP, buff=0.3)
        rows = [[f"{r['n']:,}", f"{r['brute_computations']:,}", f"{r['dist_computations']:,}",
                 f"{r['s'] * 1000:.0f} ms" if r["s"] < 1 else f"{r['s']:.2f} s"] for r in d["rows"]]
        tab = grid_table([r"points", r"all pairs", r"divide and conquer", r"time"], rows,
                         widths=[2.2, 3.6, 3.6, 2.2], row_h=0.5, font_size=21,
                         colors=[[WHITE, NO, YES, LAM]] * len(rows)).next_to(head, DOWN, buff=0.5)
        r1k = d["rows"][1]
        last = d["rows"][-1]
        brute_last = r1k["brute_s"] / r1k["brute_computations"] * last["brute_computations"]
        pts = VGroup(
            label(rf"most comparisons made by any one point in a strip: \ {max(r['strip_max'] for r in d['rows'])} "
                  r"\ (the bound says 7)", font_size=21, color=HEAD),
            label(rf"a hundred thousand points: \ {last['s']:.1f} s, \ against about {brute_last / 60:.0f} minutes "
                  r"for all pairs", font_size=21, color=YES),
            label(r"randomized: \ expected $O(n)$ by hashing grid cells \ (Rabin, \ 1976)", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "On random points, the counts tell the story. <bookmark mark='a'/> At a hundred thousand points, all "
            "pairs would be five billion distances; divide and conquer computed a hundred and forty-two thousand. "
            "In practice no point ever needed more than two comparisons in a strip; seven is only the worst case. "
            "<bookmark mark='b'/> It took a little over a second, where all pairs would take a quarter of an hour. "
            "<bookmark mark='c'/> Michael Rabin showed in 1976 that randomness does better still, expected linear "
            "time, by hashing points into grid cells of the right size."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, p in zip("abc", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
