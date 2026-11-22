from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs2.common import COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES, fmt, load
from videos.cs.cs2.s05_structural import tree_mob


def strip(code: str, unit=0.55, color_sq=DATA, color_dom=CTRL) -> VGroup:
    """A 1 x n strip tiled by squares ('|') and dominoes ('=')."""
    g = VGroup()
    x = 0.0
    for ch in code:
        w = unit if ch == "|" else 2 * unit
        g.add(Rectangle(width=w - 0.04, height=unit - 0.04, stroke_color=WHITE, stroke_width=1.5,
                        fill_color=color_sq if ch == "|" else color_dom, fill_opacity=0.75).move_to([x + w / 2, 0, 0]))
        x += w
    return g


def polygon_tri(tris, n_vertices=5, radius=0.62, color=FUNC) -> VGroup:
    angs = [PI / 2 + 2 * PI * k / n_vertices for k in range(n_vertices)]
    pts = [np.array([radius * np.cos(a), radius * np.sin(a), 0]) for a in angs]
    poly = Polygon(*pts, stroke_color=GREY_B, stroke_width=2)
    diag = VGroup()
    sides = {tuple(sorted((k, (k + 1) % n_vertices))) for k in range(n_vertices)}
    seen = set()
    for t in tris:
        for a, b in ((t[0], t[1]), (t[1], t[2]), (t[0], t[2])):
            e = tuple(sorted((a, b)))
            if e not in sides and e not in seen:
                seen.add(e)
                diag.add(Line(pts[a], pts[b], color=color, stroke_width=3))
    return VGroup(poly, diag)


def mountain(path, unit=0.22, color=INF) -> VGroup:
    pts = [np.array([0.0, 0.0, 0.0])]
    for s in path:
        pts.append(pts[-1] + np.array([unit, s * unit, 0]))
    line = VMobject(color=color, stroke_width=3).set_points_as_corners(pts)
    base = Line(pts[0], pts[-1], color=GREY_D, stroke_width=1.5)
    return VGroup(base, line)


class Recurrences(WatchScene):
    def construct(self):
        self.card()
        self.tilings()
        self.catalan()
        self.recurrence()

    def card(self):
        self.chapter(11, r"Counting by recursion", r"What if the answer for $n$ is built from smaller answers?", part=PART, said="Chapter eleven. Counting by recursion.")

    # ------------------------------------------------------------------
    def tilings(self):
        self.ask(r"Tile a strip of length 6 \\ with squares and dominoes. \\ How many ways?", [r"8", r"13", r"21"], 1,
                 say="Tile a strip six long with squares and dominoes. How many ways?",
                 reveal="Thirteen. Each count is the sum of the two before it.")
        d = load("catalan")
        head = label(r"Tiling a strip with squares and dominoes", font_size=38).to_edge(UP, buff=0.35)
        rows = VGroup(*[strip(t) for t in d["tilings4"]]).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        rows.move_to(LEFT * 3.6 + DOWN * 0.3)
        rl = label(r"length 4: \ 5 ways", font_size=28, color=GREY_A).next_to(rows, UP, buff=0.3)
        rec = MathTex(r"T(n) = T(n - 1) + T(n - 2)", font_size=42, color=CTRL).move_to(RIGHT * 3.0 + UP * 1.5)
        why = label(r"the first tile is a square \ (then $n - 1$ left) \\ or a domino \ (then $n - 2$ left)",
                    font_size=26, color=GREY_A).next_to(rec, DOWN, buff=0.3)
        fib = MathTex(r"1,\ 1,\ 2,\ 3,\ 5,\ 8,\ 13,\ 21,\ 34,\ 55,\ \dots", font_size=38, color=YES).next_to(
            why, DOWN, buff=0.5)
        fl = note(r"the Fibonacci numbers; \ Part 1's worst cases for Euclid", font_size=22).next_to(fib, DOWN, buff=0.15)
        with self.voiceover(
            "Some counts are easiest to describe in terms of smaller counts. <bookmark mark='a'/> In how many ways can a "
            "strip of length n be tiled with squares and dominoes? For length four, here are all five. "
            "<bookmark mark='b'/> Look at the first tile. If it is a square, what is left is a strip of length n minus "
            "one, tiled any way. If it is a domino, a strip of length n minus two. So the count is the sum of the two "
            "before it. <bookmark mark='c'/> One, one, two, three, five, eight: the Fibonacci numbers, which were Part "
            "1's worst cases for Euclid's algorithm. A recurrence like this is also a program, and a slow one if you "
            "run it naively; Part 22 fixes that with dynamic programming."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rl), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(rec), FadeIn(why))
            vo.wait_until("c")
            self.play(Write(fib), FadeIn(fl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def catalan(self):
        d = load("catalan")
        objs = d["objects"]
        head = label(r"Five of everything: \ the Catalan numbers", font_size=38).to_edge(UP, buff=0.3)
        cols_x = [-3.6 + 2.2 * i for i in range(5)]
        rows_y = [2.1, 0.75, -0.75, -2.3]
        names = VGroup(*[label(t, font_size=22, color=c) for t, c in (
            (r"brackets", DATA), (r"full binary \\ trees", CTRL), (r"triangulations", FUNC), (r"mountain ranges", INF))])
        for nm, y in zip(names, rows_y):
            nm.move_to([-5.9, y, 0])
        grid = []
        for i, o in enumerate(objs):
            x = cols_x[i]
            w = MathTex(r"\texttt{" + o["word"] + "}", font_size=34, color=DATA).move_to([x, rows_y[0], 0])
            t = tree_mob(o["tree"], dx=0.42, dy=0.32, r=0.07).move_to([x, rows_y[1], 0])
            tri = polygon_tri(o["triangles"]).move_to([x, rows_y[2], 0])
            m = mountain(o["path"]).move_to([x, rows_y[3], 0])
            grid.append((w, t, tri, m))
        bij = VGroup(note(r"\texttt{(}$A$\texttt{)}$B$ $\leftrightarrow$ a root with $A$ on the left, $B$ on the right",
                          font_size=20),
                     note(r"each internal node is a triangle; \ each open bracket a step up", font_size=20)).arrange(
            RIGHT, buff=0.8).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Chapter four's balanced brackets had a count: one, one, two, five. Those numbers count a surprising "
            "number of other things. <bookmark mark='a'/> Here are the five bracket strings with three pairs. "
            "<bookmark mark='b'/> Each one is a full binary tree: open bracket, A, close bracket, B, becomes a root with A "
            "hanging to the left and B to the right. Five trees with three internal nodes. <bookmark mark='c'/> Each tree is a way "
            "to cut a pentagon into triangles with diagonals that do not cross: the root is the triangle on the bottom "
            "edge, and its subtrees triangulate the two sides. Five triangulations. <bookmark mark='d'/> And each bracket "
            "string is a mountain range: up for an open bracket, down for a close, never below sea level. Five again. "
            "These are bijections, so all four counts are the same number, for every size: the Catalan numbers."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(names[k]), LaggedStart(*[FadeIn(g[k], shift=DOWN * 0.1) for g in grid],
                                                        lag_ratio=0.15), run_time=1.6)
            self.play(FadeIn(bij))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recurrence(self):
        d = load("catalan")
        cat = d["catalan"]
        head = label(r"The Catalan recurrence", font_size=38).to_edge(UP, buff=0.35)
        rec = MathTex(r"C_{n+1} = \sum_{k=0}^{n} C_k\, C_{n-k}", font_size=44, color=CTRL).next_to(head, DOWN, buff=0.45)
        why = label(r"split \texttt{(}$A$\texttt{)}$B$: \ $A$ has $k$ pairs, \ $B$ has $n - k$", font_size=28,
                    color=GREY_A).next_to(rec, DOWN, buff=0.3)
        closed = MathTex(r"C_n = \frac{1}{n + 1}\binom{2n}{n}", font_size=44, color=YES).next_to(why, DOWN, buff=0.45)
        seq = MathTex(r",\ ".join(fmt(c) for c in cat[:13]), font_size=34, color=DATA).next_to(closed, DOWN, buff=0.5)
        sl = note(r"$C_0, \dots, C_{12}$, \ computed both ways, \ and by listing every bracket string up to $n = 8$",
                  font_size=22).next_to(seq, DOWN, buff=0.15)
        grow = note(r"they grow like $4^n / n^{3/2}$: \ the number of ways to parse an ambiguous sentence, \ "
                    r"or to bracket a product (Part 22)", font_size=22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The bracket picture gives a recurrence directly. <bookmark mark='a'/> Every non-empty string is an open "
            "bracket, a string A, a close bracket, and a string B. If A has k pairs, B has the remaining n minus k, "
            "and the two can be chosen independently: multiply, then add over k. <bookmark mark='b'/> The recurrence "
            "has a closed form too, one over n plus one, times two n choose n, which a clever bijection with "
            "paths proves. <bookmark mark='c'/> One, one, two, five, fourteen, forty-two, a hundred and thirty-two, "
            "growing roughly like four to the n. They count the ways to parse an ambiguous sentence, or to bracket a "
            "long product of matrices, which Part 22 optimizes."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rec), FadeIn(why))
            vo.wait_until("b")
            self.play(Write(closed))
            vo.wait_until("c")
            self.play(Write(seq), FadeIn(sl))
            self.play(FadeIn(grow))
        self.wait(0.3)
        self.clear_scene()

