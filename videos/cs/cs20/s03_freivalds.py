from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, big, grid_table, load, mono)


def mat(n, color, s=0.28, name=None):
    cells = VGroup(*[Square(side_length=s, stroke_color=color, stroke_width=1, fill_color=color, fill_opacity=0.15)
                     for _ in range(n * n)]).arrange_in_grid(rows=n, cols=n, buff=0)
    g = VGroup(cells)
    if name:
        g.add(MathTex(name, font_size=34, color=color).next_to(cells, DOWN, buff=0.15))
    g.cells = cells
    return g


def vec(vals, color, s=0.28):
    cells = VGroup(*[VGroup(Square(side_length=s, stroke_color=color, stroke_width=1.2, fill_color=color,
                                   fill_opacity=0.15), mono(str(v), 14, WHITE)) for v in vals]).arrange(DOWN, buff=0)
    for c in cells:
        c[1].move_to(c[0])
    return cells


class Freivalds(VoiceoverScene):
    def construct(self):
        self.card()
        self.trick()
        self.proof()
        self.measured()

    def card(self):
        card = chapter_card(2, r"Checking a product with a coin", r"Can you check $AB = C$ faster than computing $AB$?",
                            lit=(1977,), extra=((1977, r"Freivalds' check"),), part=PART)
        with self.voiceover("Chapter two. Checking a product with a coin."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def trick(self):
        head = label(r"Someone hands you $C$ and claims $C = AB$", font_size=34).to_edge(UP, buff=0.35)
        n = 6
        r = [1, 0, 1, 1, 0, 1]
        A, B, Cm = mat(n, DATA, name="A"), mat(n, LAM, name="B"), mat(n, CTRL, name="C")
        rv = vec(r, YES)
        rv2 = vec(r, YES)
        lhs = VGroup(A, B, rv).arrange(RIGHT, buff=0.25)
        rhs = VGroup(Cm, rv2).arrange(RIGHT, buff=0.25)
        eq = MathTex(r"\overset{?}{=}", font_size=44)
        VGroup(lhs, eq, rhs).arrange(RIGHT, buff=0.5).move_to(UP * 0.9)
        rv_lab = label(r"$r$: \ $n$ coin flips", font_size=20, color=YES).next_to(rv, UP, buff=0.3).align_to(rv, LEFT)
        steps = VGroup(
            label(r"recompute $AB$: \ $n^3$ multiplications \ (or $n^{2.37}$ with Part 19's best)", font_size=22,
                  color=NO),
            label(r"instead: \ $Br$, \ then $A(Br)$, \ then $Cr$: \ three matrix-vector products, \ $3n^2$",
                  font_size=22, color=YES),
            label(r"if $A(Br) \ne Cr$, \ then certainly $AB \ne C$", font_size=22, color=WHITE),
            label(r"if they agree, \ $C$ is probably right: \ try fresh coins", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Someone hands you two n by n matrices, A and B, and a third, C, and claims that C is their product. "
            "<bookmark mark='a'/> Checking by recomputing the product costs n cubed multiplications, or n to the "
            "2.37 with the best methods of Part 19, which are impractical anyway. <bookmark mark='b'/> In 1977 "
            "Rūsiņš Freivalds suggested something cheaper. Flip n coins to make a random vector r of zeros and ones. "
            "Compute B times r, then A times that, and also C times r: three matrix-vector products, about three n "
            "squared operations. <bookmark mark='c'/> If the two vectors differ, C is certainly wrong. <bookmark "
            "mark='d'/> If they agree, C is probably right, and we can repeat with fresh coins. How probably?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(B), FadeIn(Cm), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(rv), FadeIn(rv2), FadeIn(rv_lab), FadeIn(steps[1]))
            self.play(Indicate(B.cells, color=YES), Indicate(rv, color=YES))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
        self.wait(0.3)
        self.clear_scene()

    def proof(self):
        head = label(r"Why a wrong $C$ is caught half the time", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            MathTex(r"D = AB - C \ne 0", font_size=36, color=NO),
            label(r"so some entry $d_{ij} \ne 0$; \ the test passes only if $Dr = 0$, \ in particular "
                  r"$(Dr)_i = 0$", font_size=22, color=WHITE),
            MathTex(r"(Dr)_i \;=\; d_{ij}\, r_j \;+\; \underbrace{\textstyle\sum_{k \ne j} d_{ik}\, r_k}_{=\,s}",
                    font_size=36, color=LAM),
            label(r"flip every coin except $r_j$ first: \ $s$ is now fixed", font_size=22, color=GREY_A),
            label(r"$(Dr)_i = 0$ needs $r_j = -s / d_{ij}$: \ at most one of $r_j = 0$, \ $r_j = 1$ works",
                  font_size=22, color=WHITE),
            MathTex(r"\Pr[\text{a wrong } C \text{ passes}] \le \tfrac12, \qquad k \text{ rounds: } \le 2^{-k}",
                    font_size=36, color=YES),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.4)
        foot = label(r"the principle of deferred decisions: \ reveal the coins in whatever order makes the proof easy",
                     font_size=20, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Suppose C is wrong. <bookmark mark='a'/> Then the difference D, A B minus C, is not the zero matrix. "
            "<bookmark mark='b'/> Some entry, d i j, is nonzero, and the test passes only if D r is the zero vector, "
            "so in particular only if its i-th entry is zero. <bookmark mark='c'/> That entry is d i j times r j, "
            "plus a sum s over the other coins. <bookmark mark='d'/> Imagine flipping every coin except r j first. "
            "The coins are independent, so this changes nothing, but now s is a fixed number. <bookmark mark='e'/> "
            "For the entry to vanish, r j must equal minus s over d i j: one particular value. At most one of "
            "the two outcomes of r j can do that. <bookmark mark='f'/> So a wrong C passes with probability at "
            "most a half, whatever A, B and C are, and k independent rounds let it through with probability at "
            "most two to the minus k. <bookmark mark='g'/> The trick of revealing the coins in a convenient order "
            "is called the principle of deferred decisions, and we will use it again."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("freivalds")
        head = label(rf"Measured: \ $n = {d['n']}$", font_size=34).to_edge(UP, buff=0.35)
        cost = grid_table([r"", r"operations", r"time here"], [
            [r"$AB$ \ (optimized BLAS)", big(d["flops_mul"]), rf"{d['t_mul']:.2f} s"],
            [r"$A(Br)$ and $Cr$", big(d["flops_check"]), rf"{d['t_check'] * 1000:.0f} ms"],
        ], widths=[4.2, 2.6, 2.2], row_h=0.5, font_size=22, mono_cols=(), colors=[[NO] * 3, [YES] * 3])
        cost.next_to(head, DOWN, buff=0.45)
        why = label(r"nearly $700\times$ fewer operations, \ but matrix-vector products wait on memory: \ "
                    rf"{d['ratio']:.0f}$\times$ faster", font_size=20, color=GREY_A).next_to(cost, DOWN, buff=0.25)
        rows = [[str(r["rounds"]), f"{r['measured']:.4f}", f"{r['bound']:.4f}"] for r in d["rounds"]]
        tab = grid_table([r"rounds", r"a wrong $C$ passed", r"bound $2^{-k}$"], rows, widths=[1.6, 3.2, 2.4],
                         row_h=0.4, font_size=20, mono_cols=(), colors=[[LAM, YES, HEAD]] * len(rows))
        tab.next_to(why, DOWN, buff=0.45).shift(LEFT * 2.6)
        side = VGroup(
            label(rf"one wrong entry, \ {d['trials']:,} trials per row", font_size=20, color=GREY_A),
            label(r"the bound is tight: \ only one coin matters", font_size=20, color=WHITE),
            label(rf"many wrong entries: \ passed {d['pass_many_wrong'] * 100:.0f}\% of the time", font_size=20,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, RIGHT, buff=0.6)
        with self.voiceover(
            f"On this machine, with matrices of size {d['n']}. <bookmark mark='a'/> Multiplying them takes sixteen "
            "billion floating-point operations, done by a heavily optimized library in about an eighth of a "
            "second. Checking takes twenty-four million operations. <bookmark mark='b'/> That is nearly seven "
            "hundred times fewer, but a matrix-vector product spends its time waiting for memory, so the check is "
            f"only about {d['ratio']:.0f} times faster in seconds, a reminder from Part 9. <bookmark mark='c'/> "
            "Now the error. We corrupted one entry of the product and tested it thousands of times. One round let "
            "it through about half the time, two rounds a quarter, and so on, right on the bound. <bookmark "
            "mark='d'/> With a single wrong entry the bound is tight, because only one coin matters. <bookmark "
            "mark='e'/> When many entries are wrong, many coins matter, and the wrong product never once got through."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*cost.cells[0])), FadeIn(cost.rule), FadeIn(VGroup(*cost.cells[1])),
                      FadeIn(VGroup(*cost.cells[2])))
            vo.wait_until("b")
            self.play(FadeIn(why))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule), FadeIn(side[0]))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()
