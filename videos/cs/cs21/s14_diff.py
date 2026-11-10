from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs21.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, big, grid_table, load, mono, words)


class Diff(VoiceoverScene):
    def construct(self):
        self.card()
        self.graph()
        self.greedy()
        self.history()

    def card(self):
        card = chapter_card(13, r"Myers' diff", r"What changed between two versions of a file?", lit=(1986,),
                            extra=((1986, r"Myers' $O(ND)$ diff"),), part=PART)
        with self.voiceover("Chapter thirteen. Myers' diff."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def graph(self):
        d = load("diff")
        a, b = d["ex_a"], d["ex_b"]
        head = label(r"The edit graph", font_size=34).to_edge(UP, buff=0.3)
        P, grid, diag, top, left = _graph(a, b)
        path, x, y = [P(0, 0)], 0, 0
        for op, _ in d["ex_ops"]:
            if op == "=":
                x, y = x + 1, y + 1
            elif op == "-":
                x += 1
            else:
                y += 1
            path.append(P(x, y))
        route = VMobject(color=HEAD, stroke_width=5).set_points_as_corners(path)
        side = VGroup(
            label(r"$A$ along the top, \ $B$ down the side", font_size=21, color=WHITE),
            label(r"right: \ delete a line of $A$; \ down: \ insert a line of $B$ \ (cost 1)", font_size=21,
                  color=NO),
            label(r"diagonal, \ where the lines are equal: \ keep it \ (free)", font_size=21, color=YES),
            label(r"a diff is a path from corner to corner; \ the shortest has $D$ steps that aren't free", font_size=21,
                  color=HEAD),
            label(rf"\texttt{{{a}}} $\to$ \texttt{{{b}}}: \ $D = {d['ex_D']}$ \ (Myers' own example)", font_size=21,
                  color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.2)
        if side.width > 6.4:
            side.width = 6.4
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Every git diff answers one question: what is the shortest list of line insertions and deletions that "
            "turns one file into another? Gene Myers drew it as a graph. <bookmark mark='a'/> Put the lines of "
            "the old file along the top and the new file down the side. <bookmark mark='b'/> A step right deletes "
            "a line of the old file, and a step down inserts a line of the new one; each costs one. <bookmark "
            "mark='c'/> Wherever two lines are equal there is a diagonal, which keeps the line and costs nothing. "
            "<bookmark mark='d'/> A diff is a path from the top-left corner to the bottom-right, and the best diff "
            "is the shortest path, Part 18's problem, on a grid. <bookmark mark='e'/> For Myers' own example, A B C "
            "A B B A against C B A B A C, five edits, and as many free diagonals as possible."
        ) as vo:
            self.play(FadeIn(head), Create(grid), FadeIn(top), FadeIn(left))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(diag), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(route), FadeIn(side[4]), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    def greedy(self):
        d = load("diff")
        a, b = d["ex_a"], d["ex_b"]
        head = label('$O(N(D+1))$: \\ follow the diagonals', font_size=34).to_edge(UP, buff=0.35)
        P, grid, diag, top, left = _graph(a, b)
        diag.set_stroke(opacity=0.5)
        ks = VGroup()
        for k in range(-4, 6):
            at = P(k, 0) + np.array([-0.2, 0.2, 0]) if k >= 0 else P(0, -k) + np.array([-0.2, 0.2, 0])
            if k >= 0:
                at = at + UP * 0.45
            else:
                at = at + LEFT * 0.45
            ks.add(mono(str(k), 13, GREY_B).move_to(at))
        fronts = _fronts(a, b)
        cols = color_gradient([LAM, HEAD], len(fronts))
        layers = []
        for D, pts in enumerate(fronts):
            g = VGroup()
            pts = [q for q in pts if q[2][0] <= len(a) and q[2][1] <= len(b)]
            for st, mid, en in pts:
                if D:
                    g.add(Line(P(*st), P(*mid), color=cols[D], stroke_width=3))
                if en != mid:
                    g.add(Line(P(*mid), P(*en), color=cols[D], stroke_width=5))
                g.add(Dot(P(*en), radius=0.07, color=cols[D]))
            g.add(mono(f"D={D}", 15, cols[D]).next_to(P(*pts[-1][2]), DR, buff=0.05))
            layers.append(g)
        lines = VGroup(
            label(r"number the diagonals $k = x - y$; \\ a path with $D$ edits ends on a diagonal in $[-D, D]$",
                  font_size=21, color=WHITE),
            label(r"for $D = 0, 1, 2, \dots$: \ on each diagonal, \\ keep only the \textbf{furthest-reaching} path",
                  font_size=21, color=LAM),
            label(r"extend it from the best neighbour by one edit, \\ then slide down free diagonals \ "
                  r"(a \textbf{snake})", font_size=21, color=YES),
            label('$N=n+m$, \\ $D$ counts insertions/deletions: \\\\ $O(N(D+1))$ time; \\ stored trace $O(D^2)$',
                  font_size=21, color=HEAD),
            label(r"patience diff \ (Bram Cohen): \\ anchor first on lines that appear once in each file",
                  font_size=20, color=GREY_A),
            label(r"three-way merge: \ diff each side against the ancestor; \\ conflicts where both changed",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        lines.width = min(lines.width, 6.4)
        lines.to_edge(RIGHT, buff=0.35).shift(DOWN * 0.2)
        with self.voiceover(
            "Dijkstra's algorithm would work, but Myers found something better in 1986. <bookmark mark='a'/> Number the diagonals by x minus y. A path with D edits can only end on diagonals from minus D to D. <bookmark mark='b'/> For D equals zero, one, two and so on, keep, for each diagonal, only the path that has reached furthest along it. <bookmark mark='c'/> Each new path is the best neighbour's path plus one edit, followed by a slide down every free diagonal it can, which Myers called a snake. <bookmark mark='d'/> The first path to reach the corner is a shortest diff, after order N times the quantity D plus one work, where N is the two lengths added and D counts insertions and deletions, so similar files are fast. <bookmark mark='e'/> Patience diff, by Bram Cohen, first anchors on lines that appear exactly once in each file, which keeps code blocks together. <bookmark mark='f'/> And three-way merge, the heart of git merge, diffs both branches against their common ancestor and uses the overlapping edits to identify candidate conflicts; exact merge behavior depends on the merge strategy."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(diag), FadeIn(top), FadeIn(left))
            vo.wait_until("a")
            self.play(FadeIn(lines[0], shift=UP * 0.1), FadeIn(ks))
            vo.wait_until("b")
            self.play(FadeIn(lines[1], shift=UP * 0.1))
            for g in layers[:3]:
                self.play(Create(g), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(lines[2], shift=UP * 0.1))
            for g in layers[3:-1]:
                self.play(Create(g), run_time=1.0)
            vo.wait_until("d")
            self.play(FadeIn(lines[3], shift=UP * 0.1), Create(layers[-1]))
            self.play(Flash(P(len(a), len(b)), color=HEAD))
            vo.wait_until("e")
            self.play(FadeIn(lines[4], shift=UP * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(lines[5], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def history(self):
        d = load("diff")
        rows = d["rows"]
        head = label(rf"This course's syllabus, \ {d['revisions']} versions", font_size=32).to_edge(UP, buff=0.35)
        show = [r for r in rows if r["D"] > 0][:]
        ax = Axes(x_range=[0, len(show) + 1, 5], y_range=[0, 3.5, 1], x_length=6.2, y_length=3.4,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        bars = VGroup()
        for k, r in enumerate(show):
            h = np.log10(r["D"])
            b = Rectangle(width=0.16, height=max(h * 3.4 / 3.5, 0.03), stroke_width=0,
                          fill_color=YES if r["D"] == r["git"] else HEAD, fill_opacity=0.85)
            b.move_to(ax.c2p(k + 1, 0) + UP * b.height / 2)
            bars.add(b)
        yl = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v, t in ((0, "1"), (1, "10"), (2, "100"), (3, "1000"))])
        xt = label(r"each commit that changed it, \ oldest first", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yt = label(r"lines changed, $D$", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        first = rows[0]
        diffs = sum(1 for r in rows if r["git"] != r["D"])
        side = VGroup(
            label(rf"the first rewrite: \ {words(first['D'])} edits \\ between {words(first['n'])} and "
                  rf"{words(first['m'])} lines, \ {first['seconds']:.2f} s", font_size=20, color=WHITE),
            label(r"checked edit distance $D$; \ timing is a host observation", font_size=20, color=YES),
            label(r"each $D$ checked against $n + m - 2\,\mathrm{LCS}$ \\ (quadratic DP): \ minimal", font_size=20,
                  color=LAM),
            label(rf"\texttt{{git diff --minimal}}: \ {diffs} different distances among {len(rows)} pairs", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        if side.width > 5.6:
            side.width = 5.6
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            f"We ran Myers on adjacent pairs in the {d['revisions']} captured syllabus revisions, in chronological order. Full commit IDs and content hashes fix the input history. <bookmark mark='a'/> The chart shows the exact insertion-and-deletion distances. The timing shown is a host observation for that pair. <bookmark mark='b'/> Similar adjacent revisions usually have smaller D. Identical files still need a linear scan, hence N times the quantity D plus one. <bookmark mark='c'/> Every script reconstructs both inputs, and every distance equals the independent quadratic LCS reference. A shortest script describes a possible transformation, not the author's causal edit history. <bookmark mark='d'/> Git's minimal diff has a different line count on {diffs} of these {len(rows)} pairs. Its preprocessing and heuristics can choose a different script. This is not evidence of corrupt output."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yl), FadeIn(xt), FadeIn(yt),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(bars[0], color=HEAD))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()


def _graph(a, b, s=0.72, X0=-6.0, Y0=2.2):
    def P(x, y):
        return np.array([X0 + x * s, Y0 - y * s, 0])
    grid = VGroup()
    for x in range(len(a) + 1):
        grid.add(Line(P(x, 0), P(x, len(b)), color=GREY_D, stroke_width=1))
    for y in range(len(b) + 1):
        grid.add(Line(P(0, y), P(len(a), y), color=GREY_D, stroke_width=1))
    diag = VGroup(*[Line(P(x, y), P(x + 1, y + 1), color=YES, stroke_width=2)
                    for x in range(len(a)) for y in range(len(b)) if a[x] == b[y]])
    top = VGroup(*[mono(c, 20, DATA).move_to(P(x + 0.5, -0.45)) for x, c in enumerate(a)])
    left = VGroup(*[mono(c, 20, LAM).move_to(P(-0.45, y + 0.5)) for y, c in enumerate(b)])
    return P, grid, diag, top, left


def _fronts(a, b):
    """Myers' furthest-reaching D-paths: for each D, a list of (start, after the edit, end of the snake)."""
    n, m = len(a), len(b)
    V, out = {1: 0}, []
    for D in range(n + m + 1):
        pts = []
        for k in range(-D, D + 1, 2):
            if k == -D or (k != D and V[k - 1] < V[k + 1]):
                x0 = V[k + 1]
                y0, x = x0 - (k + 1), x0
            else:
                x0 = V[k - 1]
                y0, x = x0 - (k - 1), x0 + 1
            y = x - k
            mid = (x, y)
            while x < n and y < m and a[x] == b[y]:
                x, y = x + 1, y + 1
            V[k] = x
            pts.append(((x0, y0) if D else (0, 0), mid, (x, y)))
            if x >= n and y >= m:
                out.append(pts)
                return out
        out.append(pts)
    return out
