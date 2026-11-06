from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, sci)


class Sqrt(VoiceoverScene):
    def construct(self):
        self.card()
        self.blocks()
        self.tree()
        self.numbers()

    def card(self):
        card = chapter_card(11, r"Time in square-root space", r"How little memory does a long computation need?",
                            lit=(1977, 2025), extra=((1977, r"Hopcroft--Paul--Valiant"), (2025, r"Williams")),
                            part=PART)
        with self.voiceover("Chapter eleven. Time in square-root space."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def blocks(self):
        head = label(r"A computation of $t$ steps, \ cut into blocks", font_size=32).to_edge(UP, buff=0.3)
        nb, nt = 8, 6
        cw, ch = 0.62, 0.5
        grid = VGroup()
        for i in range(nb):
            for j in range(nt):
                r = Rectangle(width=cw, height=ch, stroke_color=GREY_B, stroke_width=1.0)
                r.move_to(LEFT * 5.4 + RIGHT * j * cw + UP * 1.8 + DOWN * i * ch)
                grid.add(r)
        gl = VGroup(label(r"time $\downarrow$ \ ($t/b$ blocks of $b$ steps)", font_size=18, color=GREY_A),
                    label(r"tape $\rightarrow$ \ (blocks of $b$ cells)", font_size=18, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(grid, DOWN, buff=0.2).align_to(grid, LEFT)
        hl = VGroup(*[grid[i * nt + j].copy().set_fill(HEAD, 0.5) for i, j in ((3, 2), (2, 1), (2, 2), (2, 3))])
        lines = VGroup(
            label(r"the contents of one block depend only on \\ the blocks just above it and beside it",
                  font_size=21, color=WHITE),
            label(r"Hopcroft, \ Paul and Valiant \ (1977): \\ $\mathrm{TIME}(t) \subseteq \mathrm{SPACE}(t / \log t)$, "
                  r"\ by pebbling this graph", font_size=21, color=DATA),
            label(r"for 48 years, \ nobody did better", font_size=21, color=GREY_A),
            label(r"Williams \ (February 2025): \\ $\mathrm{TIME}(t) \subseteq \mathrm{SPACE}(\sqrt{t \log t})$",
                  font_size=24, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(grid, RIGHT, buff=0.8).align_to(grid, UP)
        fit_right(lines)
        with self.voiceover(
            "Every computation of t steps uses at most t cells of memory. Can it always get by with fewer? "
            "<bookmark mark='a'/> Draw the computation as a grid: time downwards, tape across, cut into blocks of b "
            "steps and b cells. <bookmark mark='b'/> What a block contains at the end depends only on the block "
            "above it and its neighbours. <bookmark mark='c'/> In 1977 John Hopcroft, Wolfgang Paul and Leslie "
            "Valiant used that structure to simulate t steps in about t over log t space. <bookmark mark='d'/> For "
            "almost fifty years nobody improved it, and many believed nothing much better was possible. <bookmark "
            "mark='e'/> In February 2025 Ryan Williams proved that t steps can be simulated in space about the "
            "square root of t log t."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid), FadeIn(gl))
            vo.wait_until("b")
            self.play(FadeIn(hl), FadeIn(lines[0]))
            for mk, ln in zip("cde", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def tree(self):
        head = label(r"The key: \ evaluating a tree in very little space", font_size=32).to_edge(UP, buff=0.3)
        pts = {}
        for d in range(4):
            for i in range(2 ** d):
                pts[(d, i)] = np.array([-5.6 + (i + 0.5) * 5.6 / 2 ** d, 1.6 - d * 1.05, 0])
        edges = VGroup(*[Line(pts[(d, i)], pts[(d + 1, c)], stroke_width=1.6, color=GREY_B)
                         for (d, i) in pts if d < 3 for c in (2 * i, 2 * i + 1)])
        nodes = VGroup(*[Circle(radius=0.2, color=(YES if d == 3 else LAM), stroke_width=2).set_fill(BG, 1)
                         .move_to(p) for (d, i), p in pts.items()])
        tl = label(r"leaves: \ values; \ each node: \ a function of its two children", font_size=18,
                   color=GREY_A).next_to(edges, DOWN, buff=0.3)
        lines = VGroup(
            label(r"\textbf{tree evaluation}: \ compute the root \\ (Cook, \ McKenzie, \ Wehr, \ Braverman, \ Santhanam, "
                  r"\ 2012)", font_size=20, color=WHITE),
            label(r"the obvious way keeps a value per level: \\ space $\approx$ height $\times$ value size", font_size=20,
                  color=GREY_A),
            label(r"it was conjectured to be optimal, \ which would have separated L from P", font_size=20,
                  color=NO),
            label(r"Cook and Mertz \ (2024): \ $O(\log n \cdot \log\log n)$ space, \\ by \textbf{reusing} memory "
                  r"that already holds data, \\ and restoring it afterwards", font_size=20, color=YES),
            label(r"Williams: \ the block grid of a computation \\ \textbf{is} a tree-evaluation instance", font_size=20,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(edges, RIGHT, buff=0.6).shift(UP * 0.3)
        fit_right(lines)
        with self.voiceover(
            "Williams's proof rests on a problem called tree evaluation. <bookmark mark='a'/> The leaves of a tree "
            "hold values; each internal node applies a function to its children's values; compute the root. "
            "<bookmark mark='b'/> The obvious method keeps one value per level of the tree, <bookmark mark='c'/> and "
            "this was conjectured to be essentially optimal; proving it would have separated logarithmic space from "
            "polynomial time. <bookmark mark='d'/> In 2024 James Cook and Ian Mertz refuted the conjecture. Their "
            "algorithm computes into memory that is already full of other data, adding and later subtracting, so "
            "the same bits serve many purposes at once. <bookmark mark='e'/> Williams's step was to see that the "
            "block structure of any computation can be arranged as a tree-evaluation instance, so the Cook-Mertz "
            "algorithm applies."
        ) as vo:
            self.play(FadeIn(head), Create(edges), FadeIn(nodes), FadeIn(tl))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def numbers(self):
        head = label(r"How much memory, \ for a trillion steps", font_size=32).to_edge(UP, buff=0.35)
        rows = []
        for t in (1e6, 1e9, 1e12, 1e15):
            lg = math.log2(t)
            rows.append([rf"$10^{{{int(round(math.log10(t)))}}}$", rf"${sci(t / lg, 2)}$", rf"${sci(math.sqrt(t * lg), 2)}$"])
        tab = grid_table([r"steps $t$", r"$t / \log t$ \ (1977)", r"$\sqrt{t \log t}$ \ (2025)"], rows,
                         widths=[2.0, 3.4, 3.4], row_h=0.48, font_size=21, mono_cols=(),
                         colors=[[WHITE, DATA, YES]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label(r"cells of a multitape Turing machine, \ constants ignored", font_size=20, color=GREY_A),
            label(r"a consequence: \ some problems solvable in \textbf{linear space} \\ need nearly \textbf{quadratic "
                  r"time} on such machines", font_size=22, color=HEAD),
            label(r"a step towards P $\ne$ PSPACE, \ still far from it; \ and it shows how much is unknown",
                  font_size=22, color=NO),
        ).arrange(DOWN, buff=0.25).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "How big a difference is it? <bookmark mark='a'/> For a trillion steps, the 1977 bound allows about "
            "twenty-five billion cells; the new bound, about six million. <bookmark mark='b'/> It has a striking "
            "corollary. If a linear-space problem could always be solved in much less than quadratic time, this "
            "simulation would contradict the space hierarchy theorem. So some problems that fit in linear space "
            "need nearly quadratic time on multitape machines. <bookmark mark='c'/> It is a small step towards "
            "separating P from PSPACE, and still far from it. But it is a reminder of how much is unknown: a "
            "fifty-year-old bound fell to a new idea about reusing memory."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), FadeIn(notes[0]))
            for mk, n_ in zip("bc", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
