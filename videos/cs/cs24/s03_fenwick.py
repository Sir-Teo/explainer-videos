from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono)


class Fenwick(VoiceoverScene):
    def construct(self):
        self.card()
        self.ranges()
        self.proof()
        self.timing()

    def card(self):
        card = chapter_card(2, r"Fenwick trees", r"Can a running total survive updates?", lit=(1994,),
                            extra=((1994, r"Fenwick's binary indexed tree"),), part=PART)
        with self.voiceover("Chapter two. Fenwick trees."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def ranges(self):
        d = load("fenwick")
        n = d["n"]
        head = label(r"Each cell is responsible for a power-of-two range", font_size=30).to_edge(UP, buff=0.3)
        w = 0.72
        x0 = -w * n / 2
        cols = {1: GREY_B, 2: DATA, 4: LAM, 8: HEAD, 16: YES}
        bars = VGroup()
        for i in range(1, n + 1):
            lo, hi = d["resp"][str(i)]
            length = hi - lo + 1
            y = 1.9 - math.log2(length) * 0.62
            bar = Rectangle(width=length * w - 0.06, height=0.42, stroke_width=0).set_fill(cols[length], 0.7)
            bar.move_to([x0 + (lo - 1) * w + length * w / 2, y, 0])
            bars.add(VGroup(bar, mono(str(i), 17, WHITE).move_to(bar.get_right() + LEFT * 0.25)))
        idx = VGroup(*[mono(str(i), 15, GREY_C).move_to([x0 + (i - 0.5) * w, -1.35, 0]) for i in range(1, n + 1)])
        bins = VGroup(*[mono(format(i, "05b"), 11, GREY_C).next_to(idx[i - 1], DOWN, buff=0.08)
                        for i in range(1, n + 1)])
        q = d["query_path"]
        u = d["update_path"]
        qhl = VGroup(*[SurroundingRectangle(bars[i - 1][0], color=YES, buff=0.03, stroke_width=3) for i in q])
        uhl = VGroup(*[SurroundingRectangle(bars[i - 1][0], color=NO, buff=0.03, stroke_width=3) for i in u])
        notes = VGroup(
            MathTex(r"\mathrm{lowbit}(i) = i \mathbin{\&} (-i)", r"\qquad \text{cell } i \text{ holds } a(i - "
                    r"\mathrm{lowbit}(i),\ i]", font_size=30, color=WHITE),
            label(rf"prefix(13): \ cells {', '.join(map(str, q))} \ (strip the lowest set bit: \ "
                  r"$1101 \to 1100 \to 1000$)", font_size=21, color=YES),
            label(rf"add at 5: \ cells {', '.join(map(str, u))} \ (add the lowest set bit: \ $0101 \to 0110 \to 1000 "
                  r"\to 10000$)", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Prefix sums answer in constant time, but one update can force n of them to change. Peter Fenwick's tree "
            "of 1994 balances the two, with one array and two loops. <bookmark mark='a'/> Cell i stores the sum of a "
            "range ending at i whose length is the lowest set bit of i. Odd cells hold one element; cells that are "
            "multiples of two but not four hold two; multiples of four, four; and so on. <bookmark mark='b'/> The "
            "lowest set bit is i and minus i, in two's complement, the trick from Part 4. <bookmark mark='c'/> To "
            "sum the first thirteen elements, take cell thirteen, then strip its lowest bit to get twelve, then "
            "eight, and stop at zero. Three cells cover one to thirteen exactly. <bookmark mark='d'/> To add to "
            "element five, update every cell whose range contains five: add the lowest bit instead. Five, six, eight, "
            "sixteen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(idx), FadeIn(bins))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in bars], lag_ratio=0.08), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(Create(qhl), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeOut(qhl), Create(uhl), FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def proof(self):
        d = load("fenwick")
        head = label(r"Why both loops are logarithmic", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            label('\\textbf{query}: clear one set bit per step; at most $\\lfloor\\log_2 n\\rfloor+1$ cells \\\\ responsibility ranges partition the prefix', font_size=22,
                  color=YES),
            label('\\textbf{update}: move the lowest set bit left; at most $\\lfloor\\log_2 n\\rfloor+1$ cells \\\\ update indices are $1\\ldots n$', font_size=22,
                  color=NO),
            label(r"the two loops are the binary representation read in opposite directions", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.45)
        rows = [[f"$2^{{{s['k']}}}$", f"{s['touched']:.1f}", str(s["k"])] for s in d["scale"]]
        tab = grid_table([r"$n$", r"cells touched per operation", r"$\log_2 n$"], rows, widths=[1.4, 4.2, 1.6],
                         row_h=0.36, font_size=20, mono_cols=(), colors=[[WHITE, YES, GREY_A]] * len(rows))
        tab.next_to(lines, DOWN, buff=0.4).set_x(0)
        with self.voiceover(
            "Why is it right, and why fast? <bookmark mark='a'/> A query clears one set bit of its positive "
            'index each step. Its responsibility intervals partition the requested prefix. The exact count is '
            "the index's population count, bounded by floor log base two of n plus one. <bookmark mark='b'/> An "
            'update moves its lowest set bit left until the index exceeds n, with the same logarithmic bound. '
            "Zero is a valid empty-prefix endpoint but never a valid update index. <bookmark mark='c'/> These "
            "are two traversals of the same interval representation. <bookmark mark='d'/> The table measures a "
            'fixed seeded mixture of updates and queries, with every final cell independently checked. Its '
            'average is an observation of that distribution, rather than a universal half-logarithm identity.'
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abc", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.15))
        self.wait(0.3)
        self.clear_scene()

    def timing(self):
        t = load("fenwick")["timing"]
        head = label(r"Four structures, \ measured", font_size=34).to_edge(UP, buff=0.35)
        rows = [[r"plain array", r"$O(1)$", r"$O(n)$", f"{t['plain_ns'] / 1000:,.0f} $\\mu$s"],
                [r"prefix-sum array", r"$O(n)$", r"$O(1)$", f"{t['prefix_ns'] / 1000:,.0f} $\\mu$s"],
                [r"Fenwick tree", r"$O(\log n)$", r"$O(\log n)$", f"{t['fenwick_ns']:.0f} ns"],
                [r"segment tree \ (bottom-up)", r"$O(\log n)$", r"$O(\log n)$", f"{t['segtree_ns']:.0f} ns"]]
        tab = grid_table([r"", r"update", r"prefix query", r"per operation, \ half of each"], rows,
                         widths=[4.0, 1.8, 2.2, 3.6], row_h=0.5, font_size=22, mono_cols=(),
                         colors=[[GREY_A] * 4, [GREY_A] * 4, [YES] * 4, [LAM] * 4])
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        notes = VGroup(
            label('$n=2^{20}$; naive arrays: $2^{10}$ operations; trees: $2^{20}$ \\\\ first shared trace prefix; three process runs; minima', font_size=22,
                  color=WHITE),
            label('per-operation minima for the stated trace lengths; full answer checks outside timers', font_size=22, color=YES),
            label('linear updates or queries cost more here; workload lengths differ',
                  font_size=22, color=NO),
            label(r"in practice: \ order books, \ leaderboards, \ arithmetic coding's frequency tables \ (Fenwick's "
                  r"original use)", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.24).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "How do they compare on a real machine? <bookmark mark='a'/> All four structures hold two to the "
            'twenty values, but their timed operation counts differ. The slow plain and prefix arrays receive '
            'only the first thousand and twenty-four operations; Fenwick and segment trees receive the full '
            "million-operation trace. The caption makes this distinction explicit. <bookmark mark='b'/> Read the "
            'per-operation minima from three process runs. Complete answer streams are checked against an '
            "independent block-sum reference after timing. <bookmark mark='c'/> This demonstrates the cost of "
            'linear updates or queries at this scale. It is not an equal-length, steady-state benchmark of all '
            "four structures. <bookmark mark='d'/> Fenwick's original application was arithmetic coding's "
            'frequency tables, a useful example of matching operations to a data structure.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3))
            for mk, n_ in zip("abcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
