from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)

SIDE = 5.6
ORG = np.array([-3.0, -0.4, 0])
DEPTH = [DATA, YES, LAM, HEAD, CTRL, GREY_B, GREY_C]


def S(p):
    return ORG + np.array([(p[0] - 0.5) * SIDE, (p[1] - 0.5) * SIDE, 0])


class KdTree(VoiceoverScene):
    def construct(self):
        self.card()
        self.build()
        self.measured()
        self.others()

    def card(self):
        card = chapter_card(10, r"Range searching", r"Which points lie in this rectangle?", lit=(1975, 1978),
                            extra=((1975, r"Bentley's kd-tree"), (1978, r"range trees")), part=PART)
        with self.voiceover("Chapter ten. Range searching."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def build(self):
        d = load("kd")
        P = d["P"]
        head = label(r"A kd-tree: \ split at the median, \ alternating $x$ and $y$", font_size=30).to_edge(UP, buff=0.3)
        frame = Square(side_length=SIDE, color=GREY_B, stroke_width=1.5).move_to(S((0.5, 0.5)))
        pts = VGroup(*[Dot(S(p), radius=0.055, color=WHITE) for p in P])
        levels = {}
        for x0, y0, x1, y1, dep in d["cells"]:
            levels.setdefault(dep, VGroup()).add(Line(S((x0, y0)), S((x1, y1)), color=DEPTH[min(dep, 6)],
                                                      stroke_width=max(3.2 - 0.5 * dep, 1.0)))
        (lx, ly), (hx, hy) = d["box"]
        q = Rectangle(width=(hx - lx) * SIDE, height=(hy - ly) * SIDE, color=NO, stroke_width=3).move_to(
            S(((lx + hx) / 2, (ly + hy) / 2))).set_fill(NO, 0.1)
        inside = VGroup(*[Dot(S(P[i]), radius=0.08, color=NO) for i in d["inside"]])
        side = VGroup(
            label(r"split the points at the median $x$; \\ split each half at its median $y$; \ repeat", font_size=21,
                  color=WHITE),
            label(r"$O(n \log n)$ to build, \ $O(n)$ space, \ depth $\log_2 n$", font_size=21, color=DATA),
            label(r"a query descends only into cells \\ that meet the rectangle", font_size=21, color=NO),
            label(rf"here: \ {len(d['inside'])} points reported, \ {d['visited']} of "
                  rf"{2 * len(P) - 1} nodes visited", font_size=21, color=HEAD),
            label(r"a vertical line crosses $O(\sqrt n)$ cells: \\ a query costs $O(\sqrt n + k)$", font_size=21,
                  color=YES),
            label(r"Bentley (1975), \ as a Stanford undergraduate", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        if side.width > 5.4:
            side.width = 5.4
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "A database of shops, each with a position, is asked for every shop in a rectangle on the map. Checking "
            "every shop is linear; we want the answer in time close to its size. <bookmark mark='a'/> Jon Bentley's "
            "kd-tree, from 1975, splits the points at their median x, then each half at its median y, then each "
            "quarter at its median x again, alternating, until every cell holds one point. <bookmark mark='b'/> It "
            "takes n log n to build and linear space. <bookmark mark='c'/> To answer a query, descend from the root "
            "into every cell that meets the rectangle, and report the points inside. <bookmark mark='d'/> Here the "
            "query visits forty-six of the hundred and nineteen nodes. <bookmark mark='e'/> Why is that cheap? A "
            "vertical line crosses only the cells along one path in every two levels, about the square root of n "
            "of them, so the query costs root n for the rectangle's boundary plus the k points reported. "
            "<bookmark mark='f'/> Bentley invented it as an undergraduate at Stanford."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(pts))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            for dep in sorted(levels):
                self.play(LaggedStart(*[Create(x) for x in levels[dep]], lag_ratio=0.05),
                          run_time=0.6 + 0.15 * dep)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Create(q))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(inside, scale=1.5))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("kd")
        head = label(r"Square queries of side 0.02 in the unit square", font_size=32).to_edge(UP, buff=0.35)
        rows = [[words(r["n"]), f"{r['k']:.1f}", f"{r['visited']:.0f}", f"{r['sqrt_n']:.0f}",
                 f"{r['visited'] / (r['sqrt_n'] + r['k']):.2f}", f"{r['build_s']:.2f} s"] for r in d["rows"]]
        tab = grid_table([r"points $n$", r"reported $k$", r"nodes visited", r"$\sqrt n$", r"visited$/(\sqrt n + k)$",
                          r"build"], rows, widths=[2.2, 2.0, 2.2, 1.4, 3.2, 1.6], row_h=0.5, font_size=21,
                         mono_cols=(), colors=[[WHITE, HEAD, NO, GREY_A, YES, GREY_A]] * len(rows))
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        notes = VGroup(
            label(r"averages of 40 queries; \ the visits stay below $\sqrt n + k$, \ far below $n$",
                  font_size=22, color=WHITE),
            label(r"the $\sqrt n$ is the price of linear space: \ in $d$ dimensions it becomes $n^{1 - 1/d}$", font_size=22,
                  color=NO),
        ).arrange(DOWN, buff=0.3).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "We built kd-trees of up to three hundred thousand random points and asked forty small square queries "
            "of each. <bookmark mark='a'/> The visits stay below root n plus k: about three "
            "hundred and thirty nodes for three hundred thousand points, where a scan would look at all of them. "
            "<bookmark mark='b'/> The square root is the price of linear space, and it gets worse with dimension: in "
            "d dimensions a kd-tree query costs n to the one minus one over d, a warning for chapter twelve."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3))
            for mk, nt in zip("ab", notes):
                vo.wait_until(mk)
                self.play(FadeIn(nt))
        self.wait(0.3)
        self.clear_scene()

    def others(self):
        head = label(r"Spending space to save time", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"\textbf{range trees}: \ a balanced tree on $x$, \ each node holding its points sorted by $y$",
                  font_size=22, color=DATA),
            label(r"$O(n \log n)$ space, \ $O(\log^2 n + k)$ per query", font_size=22, color=WHITE),
            label(r"\textbf{fractional cascading} \ (Chazelle and Guibas, 1986): \ link each list to its children's, "
                  r"\ so one binary search serves a whole path: \ $O(\log n + k)$", font_size=22, color=LAM),
            label(r"\textbf{interval trees} and \textbf{segment trees}: \ which intervals contain a point?", font_size=22,
                  color=YES),
            label(r"in databases, \ R-trees \ (Guttman, 1984) \ group nearby rectangles in pages of a B-tree \ "
                  r"(Part 17): \ PostGIS, \ SQLite, \ every map server", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.34).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "If we can afford more space, queries get faster. <bookmark mark='a'/> A range tree is a balanced tree "
            "on x in which every node also keeps its points sorted by y. <bookmark mark='b'/> It uses n log n space "
            "and answers in log squared n plus k. <bookmark mark='c'/> Bernard Chazelle and Leonidas Guibas removed "
            "a log with fractional cascading: each sorted list keeps pointers into its children's lists, so a "
            "single binary search at the root serves the whole path down. <bookmark mark='d'/> Interval trees and "
            "segment trees answer the other common question, which stored intervals contain a given point. "
            "<bookmark mark='e'/> Databases use R-trees, which pack nearby rectangles into the pages of a B-tree; "
            "they sit under PostGIS, SQLite's spatial index and most map servers."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
