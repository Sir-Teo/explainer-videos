from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs3.common import CODE, COST, CTRL, DATA, FUNC, HEAD, INF, LIMIT, NO, PART, YES, load

GRAY = [0, 1, 3, 2]  # Gray-code order of two bits


def cube_points(scale=1.6, origin=ORIGIN):
    """The eight corners of the 3-cube abc, in an oblique projection: a to the right, b up, c into the page."""
    pts = {}
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                pts[(a, b, c)] = np.asarray(origin) + scale * np.array([a + 0.55 * c, b + 0.4 * c, 0])
    return pts


class Normal(VoiceoverScene):
    def construct(self):
        self.card()
        self.cube()
        self.kmap()
        self.parity()
        self.hard()

    def card(self):
        card = chapter_card(6, r"Normal forms and maps", r"How small can a formula for a function be?", part=PART)
        with self.voiceover("Chapter six. Normal forms and maps."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def cube(self):
        head = label(r"A function on three inputs is a coloured cube", font_size=36).to_edge(UP, buff=0.35)
        P = cube_points(1.9, LEFT * 4.2 + DOWN * 1.8)
        maj = {k: int(sum(k) >= 2) for k in P}
        edges = VGroup()
        for k in P:
            for i in range(3):
                if k[i] == 0:
                    j = list(k)
                    j[i] = 1
                    edges.add(Line(P[k], P[tuple(j)], color=GREY_D, stroke_width=2))
        dots = VGroup()
        labs = VGroup()
        for k, p in P.items():
            dots.add(Dot(p, radius=0.13, color=YES if maj[k] else GREY_C))
            labs.add(MathTex("".join(map(str, k)), font_size=24, color=GREY_A).next_to(p, DL if k[2] == 0 else UR,
                                                                                         buff=0.06))
        dnf = MathTex(r"\text{DNF: } \bar a b c + a \bar b c + a b \bar c + a b c", font_size=32, color=GREY_A).move_to(
            RIGHT * 2.8 + UP * 1.8)
        dl = note(r"one term per green corner: \ 4 terms, \ 12 literals", font_size=22).next_to(dnf, DOWN, buff=0.12)
        imps = [((0, 1, 1), (1, 1, 1), r"bc"), ((1, 0, 1), (1, 1, 1), r"ac"), ((1, 1, 0), (1, 1, 1), r"ab")]
        thick = VGroup(*[Line(P[a], P[b], color=HEAD, stroke_width=9) for a, b, _ in imps])
        mn = MathTex(r"\text{minimal: } ab + bc + ac", font_size=36, color=YES).next_to(dl, DOWN, buff=0.5)
        ml = note(r"an edge of green corners is a term with one variable dropped: \ an \textit{implicant}", font_size=22)
        ml.next_to(mn, DOWN, buff=0.12)
        face = label(r"a green face would drop two variables", font_size=24, color=GREY_B).next_to(ml, DOWN, buff=0.35)
        with self.voiceover(
            "Chapter five's normal form always works, but it can be wasteful. Here is a way to see the waste. "
            "<bookmark mark='a'/> A function of three inputs assigns a value to each of the eight corners of a cube, "
            "one corner for each input pattern. This one is majority: green where at least two inputs are one. "
            "<bookmark mark='b'/> The disjunctive normal form has one term per green corner: four terms. "
            "<bookmark mark='c'/> But two green corners joined by an edge differ in one variable only, and that "
            "variable does not matter there: a b c and a b not c together are just a b. So cover the green corners "
            "with edges, or, better, whole faces. Three edges cover majority: a b plus b c plus a c."
        ) as vo:
            self.play(FadeIn(head), Create(edges), FadeIn(dots), FadeIn(labs))
            vo.wait_until("b")
            self.play(FadeIn(dnf), FadeIn(dl))
            vo.wait_until("c")
            self.play(Create(thick), run_time=1.6)
            self.play(Write(mn), FadeIn(ml), FadeIn(face))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def grid4(self, ones, cell=0.85, origin=ORIGIN):
        g = VGroup()
        g.sq = {}
        for r in range(4):
            for c in range(4):
                ab, cd = GRAY[r], GRAY[c]
                m = (ab << 2) | cd
                sq = Square(cell, stroke_color=GREY_C, stroke_width=1.5,
                            fill_color=YES if m in ones else "#121722", fill_opacity=0.55 if m in ones else 1)
                sq.move_to(np.asarray(origin) + np.array([(c - 1.5) * cell, (1.5 - r) * cell, 0]))
                t = MathTex("1" if m in ones else "0", font_size=28, color=WHITE if m in ones else GREY_D).move_to(sq)
                g.sq[m] = sq
                g.add(VGroup(sq, t))
        rl = VGroup(*[MathTex(format(GRAY[r], "02b"), font_size=24, color=DATA).next_to(
            g.sq[(GRAY[r] << 2) | GRAY[0]], LEFT, buff=0.15) for r in range(4)])
        cl = VGroup(*[MathTex(format(GRAY[c], "02b"), font_size=24, color=CTRL).next_to(
            g.sq[(GRAY[0] << 2) | GRAY[c]], UP, buff=0.12) for c in range(4)])
        corner = MathTex(r"AB \backslash CD", font_size=22, color=GREY_B).next_to(rl, UP, buff=0.15).shift(LEFT * 0.1)
        g.add(rl, cl, corner)
        g.cell = cell
        return g

    def kmap(self):
        d = load("kmap")
        ones = set(d["minterms"])
        head = label(r"Karnaugh maps: \ the 4-cube, \ unfolded", font_size=36).to_edge(UP, buff=0.3)
        g = self.grid4(ones, origin=LEFT * 3.4 + DOWN * 0.4)
        gl = note(r"rows and columns in Gray-code order: \ neighbours differ in one bit, \\ and the edges wrap around "
                  r"(a torus)", font_size=21).next_to(g, DOWN, buff=0.3)
        cols = [HEAD, CTRL, FUNC, INF]
        loops = VGroup()
        for k, (v, mask, name) in enumerate(d["cover"]):
            cells = [m for m in range(16) if (m & ~mask) == v and m in ones]
            grp = VGroup(*[g.sq[m].copy().set_fill(opacity=0).set_stroke(cols[k], 5) for m in cells])
            loops.add(grp)
        names = VGroup(*[MathTex(n.replace("'", r"'"), font_size=34, color=cols[k]) for k, (_, _, n) in
                         enumerate(d["cover"])])
        f = MathTex(r"f = " + " + ".join(n.replace("'", "^{\\prime}") for _, _, n in d["cover"]), font_size=38,
                    color=YES).move_to(RIGHT * 3.4 + UP * 1.4)
        cmp = VGroup(label(rf"DNF: \ {d['dnf_terms']} terms of 4 literals", font_size=26, color=GREY_A),
                     label(rf"minimal: \ {len(d['cover'])} terms of 2", font_size=26, color=YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).next_to(f, DOWN, buff=0.4)
        qm = VGroup(label(r"Quine--McCluskey: \ merge terms that differ in one bit, \\ repeatedly, \ to find every "
                          r"\textit{prime implicant}; \\ then choose the fewest that cover", font_size=24,
                          color=GREY_A),
                    note(rf"here: \ {len(d['primes'])} prime implicants, \ {len(d['cover'])} needed \ (computed)",
                         font_size=22)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(cmp, DOWN, buff=0.45)
        with self.voiceover(
            "With four inputs the cube has sixteen corners, and in 1953 Maurice Karnaugh found a way to flatten it. "
            "<bookmark mark='a'/> Lay the corners out in a four by four grid, with rows and columns in Gray-code "
            "order, so that cells side by side differ in exactly one bit. The left edge is next to the right edge, and "
            "the top to the bottom: the map is really a torus. <bookmark mark='b'/> Now groups of ones in rectangles of "
            "two, four or eight cells are terms with variables dropped. Here three groups cover everything, including "
            "the four corners, which are neighbours on the torus. <bookmark mark='c'/> Ten terms of four literals "
            "become three terms of two. <bookmark mark='d'/> For more inputs, maps fail and an algorithm takes over: "
            "Quine and McCluskey's method merges terms that differ in one bit, again and again, to find every prime "
            "implicant, and then picks the fewest that cover the function."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(gl))
            vo.wait_until("b")
            for lp in loops:
                self.play(Create(lp), run_time=0.9)
            vo.wait_until("c")
            self.play(Write(f), FadeIn(cmp))
            vo.wait_until("d")
            self.play(FadeIn(qm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def parity(self):
        d = load("parity")
        head = label(r"Where normal forms explode: \ parity", font_size=38).to_edge(UP, buff=0.35)
        ones = {m for m in range(16) if bin(m).count("1") % 2}
        g = self.grid4(ones, cell=0.7, origin=LEFT * 4.2 + DOWN * 0.2)
        gl = note(r"a checkerboard: \ no two 1s touch, \\ nothing merges", font_size=21).next_to(g, DOWN, buff=0.3)
        rows = d["rows"]
        ax = Axes(x_range=[2, 12, 2], y_range=[0, 12, 2], x_length=5.4, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18},
                  x_axis_config={"numbers_to_include": list(range(2, 13, 2))},
                  y_axis_config={"numbers_to_include": [0, 4, 8, 12]}).move_to(RIGHT * 2.8 + DOWN * 0.3)
        dnf = VMobject(color=NO, stroke_width=4).set_points_as_corners(
            [ax.c2p(r["n"], np.log2(r["dnf_terms"])) for r in rows])
        tree = VMobject(color=YES, stroke_width=4).set_points_as_corners(
            [ax.c2p(r["n"], np.log2(r["xors"])) for r in rows])
        yl = note(r"$\log_2$ of the size", font_size=20).next_to(ax, UP, buff=0.1)
        xl = note(r"inputs $n$", font_size=20).next_to(ax, DOWN, buff=0.1)
        l1 = label(r"DNF: \ $2^{n-1}$ terms", font_size=26, color=NO).next_to(ax.c2p(12, 11), LEFT, buff=0.2)
        l2 = label(r"XOR tree: \ $n - 1$ gates", font_size=26, color=YES).next_to(ax.c2p(12, np.log2(11)), UP,
                                                                                   buff=0.2).shift(LEFT * 0.8)
        dual = note(r"CNF, \ the and-of-ors dual, \ explodes the same way; \ depth matters (chapter 9)", font_size=22)
        dual.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Normal forms can be terrible. <bookmark mark='a'/> Parity, which is one when an odd number of inputs are "
            "one, makes a perfect checkerboard on the map. No two ones are neighbours, nothing merges, and every one of "
            "the eight ones needs its own term. <bookmark mark='b'/> With n inputs the normal form needs two to the n "
            "minus one terms, which for sixty-four inputs is about nine billion billion terms. "
            "<bookmark mark='c'/> But a tree of n minus one exclusive-or gates computes it easily. The two-level form, an "
            "or of ands, is a poor model of what circuits can do; depth, how many layers deep a circuit is, changes "
            "everything, and chapter nine measures it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(gl))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), Create(dnf), FadeIn(l1))
            vo.wait_until("c")
            self.play(Create(tree), FadeIn(l2), FadeIn(dual))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hard(self):
        head = label(r"How hard is it to find the smallest formula?", font_size=36).to_edge(UP, buff=0.4)
        lines = VGroup(*[label(t, font_size=28, color=c) for t, c in (
            (r"given a truth table: \ the minimal two-level form is NP-hard \ (Masek, 1979)", GREY_A),
            (r"given a DNF: \ ``is there an equivalent DNF with $\le k$ terms?'' \\ is $\Sigma_2^p$-complete \ "
             r"(Umans, 2001): \ harder than NP, \ as far as anyone knows", LIMIT),
            (r"so real tools use heuristics: \ Espresso (Berkeley, 1980s), \ ABC, \ Yosys", YES),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(DOWN * 0.1)
        later = note(r"NP and the polynomial hierarchy: \ Part 26", font_size=22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "So how hard is it to find the smallest formula for a function? <bookmark mark='a'/> Even for two-level "
            "forms, starting from the truth table, it is NP-hard, a word Part 26 makes precise: no efficient method is "
            "known, and probably none exists. <bookmark mark='b'/> Starting from a DNF, asking whether an equivalent DNF with fewer terms "
            "exists is even harder, complete for the second level of the polynomial hierarchy. "
            "<bookmark mark='c'/> So the logic synthesis tools that design real chips use clever heuristics, and do "
            "not promise the smallest circuit. They are extremely good at it anyway."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("a")
            for mk, l in zip("bc", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(l, shift=RIGHT * 0.1))
            self.play(FadeIn(later))
        self.wait(0.3)
        self.clear_scene()
