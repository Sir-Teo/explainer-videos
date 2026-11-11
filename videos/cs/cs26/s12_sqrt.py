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
            label('the general deterministic multitape simulation resisted improvement for decades', font_size=21, color=GREY_A),
            label('Williams (2025), deterministic multitape, $t\\ge n$:\\\\ TIME$(t)\\subseteq$ SPACE$(\\sqrt{t\\log t})$',
                  font_size=24, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(grid, RIGHT, buff=0.8).align_to(grid, UP)
        fit_right(lines)
        with self.voiceover(
            "How much space can simulate a time-bounded computation? <bookmark mark='a'/> For deterministic multitape Turing machines, divide a computation into blocks. The grid is an illustration of dependency structure, not a literal implementation of the entire proof. <bookmark mark='b'/> Hopcroft, Paul and Valiant obtained a time-over-log-time space simulation in 1977. <bookmark mark='c'/> Improving that general bound resisted progress for decades. <bookmark mark='d'/> Williams's 2025 theorem gives TIME t contained in SPACE of order square root of t log t, for t at least n, in the stated multitape model. It is not an unrestricted RAM theorem. <bookmark mark='e'/> The proof reduces the simulation to implicitly generated tree-evaluation instances. Shared dependencies may be unfolded into a much larger tree, accessed on demand rather than stored in full."
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
            label('pebbling intuition suggests lower bounds; \\\\ tree evaluation in L or outside NL remains unresolved', font_size=20,
                  color=NO),
            label(r"Cook and Mertz \ (2024): \ $O(\log n \cdot \log\log n)$ space, \\ by \textbf{reusing} memory "
                  r"that already holds data, \\ and restoring it afterwards", font_size=20, color=YES),
            label('Williams: implicit tree-evaluation instances \\\\ unfold dependencies and are accessed on demand', font_size=20,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(edges, RIGHT, buff=0.6).shift(UP * 0.3)
        fit_right(lines)
        with self.voiceover(
            "Tree evaluation asks for the root value. <bookmark mark='a'/> Leaves carry values and internal nodes provide explicit tables mapping child values to a parent value. <bookmark mark='b'/> Keeping a value at each level uses height times value length space. This motivates pebbling-based algorithms and lower-bound conjectures. <bookmark mark='c'/> Proving sufficiently strong tree-evaluation lower bounds would separate small-space classes from P, but those separations remain open. <bookmark mark='d'/> Cook and Mertz found a more space-efficient evaluation algorithm using algebraic techniques. This undermines some pebbling intuitions; it does not settle membership in L or disprove the conjecture that tree evaluation is outside NL. <bookmark mark='e'/> Williams uses that improved algorithm as an ingredient in the multitape simulation theorem."
        ) as vo:
            self.play(FadeIn(head), Create(edges), FadeIn(nodes), FadeIn(tl))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def numbers(self):
        head = label('Comparing asymptotic functions, with constants omitted', font_size=32).to_edge(UP, buff=0.35)
        rows = []
        for t in (1e6, 1e9, 1e12, 1e15):
            lg = math.log2(t)
            rows.append([rf"$10^{{{int(round(math.log10(t)))}}}$", rf"${sci(t / lg, 2)}$", rf"${sci(math.sqrt(t * lg), 2)}$"])
        tab = grid_table([r"steps $t$", r"$t / \log t$ \ (1977)", r"$\sqrt{t \log t}$ \ (2025)"], rows,
                         widths=[2.0, 3.4, 3.4], row_h=0.48, font_size=21, mono_cols=(),
                         colors=[[WHITE, DATA, YES]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label('illustrative function values, not measured or guaranteed cell counts; deterministic multitape model', font_size=20, color=GREY_A),
            label('constructible $s\\ge n$: SPACE$(s)\\not\\subseteq$ TIME$(s^{2-\\varepsilon})$ for fixed $\\varepsilon>0$', font_size=22, color=HEAD),
            label('time-space separation under stated assumptions; P vs PSPACE and L vs P remain open',
                  font_size=22, color=NO),
        ).arrange(DOWN, buff=0.25).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Compare the asymptotic functions. <bookmark mark='a'/> At a trillion steps, the expressions t over log base two of t and square root of t log base two of t differ dramatically. The table evaluates those functions with constants omitted, not measured or guaranteed memory cell counts. <bookmark mark='b'/> The theorem implies that for space-constructible s at least n, and every fixed positive epsilon, some problems in SPACE s are outside TIME s to the power two minus epsilon. <bookmark mark='c'/> The machine model and constructibility conditions matter. This is a time-space separation theorem, not a resolution of P versus PSPACE or L versus P."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), FadeIn(notes[0]))
            for mk, n_ in zip("bc", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
