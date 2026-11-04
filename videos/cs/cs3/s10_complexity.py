from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs3.common import CODE, COST, CTRL, DATA, FUNC, HEAD, INF, LIMIT, NO, PART, WIRE, YES, gate, load, wire


class Complexity(VoiceoverScene):
    def construct(self):
        self.card()
        self.size_depth()
        self.counting()
        self.curve()
        self.formulas()
        self.gap()

    def card(self):
        card = chapter_card(9, r"How many gates?", r"How big must a circuit be?", part=PART)
        with self.voiceover("Chapter nine. How many gates?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def size_depth(self):
        d = load("blocks")
        rows = {r["name"]: r for r in d["rows"]}
        head = label(r"Size and depth", font_size=38).to_edge(UP, buff=0.35)

        def chain(origin):
            g = VGroup()
            gs = []
            o = np.asarray(origin, float)
            for k in range(7):
                gg = gate("XOR", size=0.5).move_to(o + np.array([k * 0.95, -k * 0.3, 0]))
                gs.append(gg)
                g.add(gg)
            for a, b in zip(gs, gs[1:]):
                g.add(wire(a.out(), b.inp[0]()))
            return g

        def tree(origin):
            g = VGroup()
            o = np.asarray(origin, float)
            L = [[gate("XOR", size=0.5).move_to(o + np.array([0, 1.6 - 0.9 * i, 0])) for i in range(4)]]
            L.append([gate("XOR", size=0.5).move_to(o + np.array([1.3, 1.15 - 1.8 * i, 0])) for i in range(2)])
            L.append([gate("XOR", size=0.5).move_to(o + np.array([2.6, 0.25, 0]))])
            for lvl in L:
                g.add(*lvl)
            for lvl in (1, 2):
                for i, gg in enumerate(L[lvl]):
                    g.add(wire(L[lvl - 1][2 * i].out(), gg.inp[0]()), wire(L[lvl - 1][2 * i + 1].out(), gg.inp[1]()))
            return g

        c1 = chain(LEFT * 5.8 + UP * 1.2)
        c2 = tree(RIGHT * 1.6 + DOWN * 0.2)
        r1, r2 = rows["8-bit parity chain"], rows["8-bit parity tree"]
        l1 = label(rf"a chain: \ size {r1['gates']}, \ depth {r1['depth']}", font_size=28, color=NO).next_to(c1, DOWN,
                                                                                                         buff=0.4)
        l2 = label(rf"a tree: \ size {r2['gates']}, \ depth {r2['depth']}", font_size=28, color=YES).next_to(c2, DOWN,
                                                                                                         buff=0.3)
        defs = VGroup(label(r"\textit{size}: \ how many gates \ (area, power)", font_size=26, color=GREY_A),
                      label(r"\textit{depth}: \ the longest path from input to output \ (time)", font_size=26,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A circuit has two costs. <bookmark mark='a'/> Its size, the number of gates, is area on the chip and power. "
            "Its depth, the longest path from an input to the output, is time: every gate on that path adds a delay. "
            "<bookmark mark='b'/> Parity of eight bits, as a chain of exclusive-ors: seven gates, seven deep. "
            "<bookmark mark='c'/> The same seven gates as a tree: three deep. Same size, less than half the time, "
            "and the gap grows: a chain is n deep, a tree log n. Part 4's adders are a long fight to turn chains into "
            "trees."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(defs))
            vo.wait_until("b")
            self.play(FadeIn(c1, lag_ratio=0.05), FadeIn(l1))
            vo.wait_until("c")
            self.play(FadeIn(c2, lag_ratio=0.05), FadeIn(l2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counting(self):
        head = label(r"Shannon's counting argument \ (1949)", font_size=38).to_edge(UP, buff=0.35)
        lhs = VGroup(label(r"functions of $n$ inputs:", font_size=30, color=GREY_A),
                     MathTex(r"2^{2^n}", font_size=56, color=FUNC)).arrange(DOWN, buff=0.25).move_to(LEFT * 3.6 + UP * 0.9)
        rhs = VGroup(label(r"circuits with $s$ gates:", font_size=30, color=GREY_A),
                     MathTex(r"\le \big(16\,(n + s)^2\big)^s", font_size=46, color=CTRL)).arrange(DOWN, buff=0.25).move_to(
            RIGHT * 3.0 + UP * 0.9)
        why = note(r"each gate: \ one of 16 kinds, \ and two inputs chosen from the $n + s$ wires", font_size=22)
        why.next_to(rhs, DOWN, buff=0.2)
        concl = VGroup(label(r"if circuits are fewer than functions, \ most functions have no circuit that small",
                             font_size=28, color=HEAD),
                       MathTex(r"s\,\log_2\!\big(16 (n+s)^2\big) < 2^n \ \ \Rightarrow \ \ s \gtrsim \frac{2^n}{2n}",
                               font_size=38, color=YES),
                       label(r"so almost every function needs exponentially many gates", font_size=28, color=NO)).arrange(
            DOWN, buff=0.35).move_to(DOWN * 1.8)
        with self.voiceover(
            "How many gates does a typical function need? Shannon answered in 1949 without designing a single circuit. "
            "He counted. <bookmark mark='a'/> A function of n inputs is a truth table with two to the n rows, so there "
            "are two to the two to the n functions. For twenty inputs, a number with three hundred and fifteen thousand "
            "digits. <bookmark mark='b'/> A circuit with s gates is a list of s choices: a kind of gate, and two input "
            "wires. So there are at most about n plus s squared, to the s, of them. <bookmark mark='c'/> If there are "
            "fewer small circuits than functions, most functions have no small circuit. Solving the inequality: "
            "almost every function of n inputs needs on the order of two to the n over n gates. Exponential. A random "
            "truth table is, almost surely, hopelessly hard."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lhs))
            vo.wait_until("b")
            self.play(FadeIn(rhs), FadeIn(why))
            vo.wait_until("c")
            self.play(FadeIn(concl, lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve(self):
        d = load("counting")
        rows = d["rows"]
        head = label(r"The two towers", font_size=38).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[2, 30, 4], y_range=[0, 30, 5], x_length=6.6, y_length=4.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 20},
                  x_axis_config={"numbers_to_include": list(range(2, 31, 4))},
                  y_axis_config={"numbers_to_include": [0, 10, 20, 30]}).move_to(LEFT * 2.6 + DOWN * 0.3)
        lf = VMobject(color=FUNC, stroke_width=4).set_points_as_corners(
            [ax.c2p(r["n"], min(math.log2(r["log2_functions"]), 30)) for r in rows])
        ls = VMobject(color=CTRL, stroke_width=4).set_points_as_corners(
            [ax.c2p(r["n"], math.log2(r["s_needed"])) for r in rows])
        lin = VMobject(color=YES, stroke_width=3).set_points_as_corners(
            [ax.c2p(r["n"], math.log2(r["n"])) for r in rows])
        yl = note(r"$\log_2 \log_2$ \ \ /\ \ $\log_2$", font_size=20).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        xl = note(r"inputs $n$", font_size=20).next_to(ax, DOWN, buff=0.1)
        k1 = label(r"$\log_2\log_2$ of the number of functions: \ $n$", font_size=22, color=FUNC)
        k2 = label(r"$\log_2$ of the gates most functions need", font_size=22, color=CTRL)
        k3 = label(r"$\log_2 n$: \ a circuit of size $n$", font_size=22, color=YES)
        keys = VGroup(k1, k2, k3).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        keys.move_to(RIGHT * 1.5 + UP * 1.2, aligned_edge=LEFT)
        tab = VGroup(*[MathTex(rf"n = {r['n']}: \ s \ge {fmt(r['s_needed'])}", font_size=24, color=GREY_A)
                       for r in rows if r["n"] in (10, 16, 20, 30)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        tab.next_to(keys, DOWN, buff=0.5).align_to(keys, LEFT)
        tl = note(r"computed from the count", font_size=20).next_to(tab, DOWN, buff=0.1).align_to(tab, LEFT)
        lup = note(r"and Lupanov (1958): \ $\approx 2^n / n$ gates always suffice", font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here are the numbers, computed. <bookmark mark='a'/> The gates most functions need grow like two to the n "
            "over n: for thirty inputs, tens of millions of gates. <bookmark mark='b'/> Compare a circuit that grows "
            "like n, the kind engineers actually build, down at the bottom. <bookmark mark='c'/> And it is tight: Oleg "
            "Lupanov showed in 1958 that about two to the n over n gates are always enough, for any function. Almost "
            "every function sits at that worst case. The functions we can build are the rare exceptions."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(ls), FadeIn(k2), FadeIn(tab), FadeIn(tl), run_time=1.6)
            self.play(Create(lf), FadeIn(k1))
            vo.wait_until("b")
            self.play(Create(lin), FadeIn(k3))
            vo.wait_until("c")
            self.play(FadeIn(lup))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def formulas(self):
        head = label(r"Formulas against circuits", font_size=38).to_edge(UP, buff=0.35)
        lines = VGroup(*[label(t, font_size=28, color=c) for t, c in (
            (r"a \textit{formula} is a circuit that never reuses a gate's output: \ a tree", GREY_A),
            (r"a \textit{circuit} may share: \ one output can feed many gates", GREY_A),
            (r"parity of $n$ bits: \ a circuit of $n - 1$ XORs, \ about $4n$ gates of AND, OR, NOT", YES),
            (r"as a formula of AND, OR, NOT: \ at least $n^2$ leaves \ (Khrapchenko, 1971), \ and $n^2$ suffice", NO),
            (r"sharing can save a polynomial; \ whether it ever saves more \ is open", HEAD),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(DOWN * 0.1)
        with self.voiceover(
            "There is a second way to measure. <bookmark mark='a'/> A formula is a circuit in which every gate's output "
            "is used only once, so it is a tree, like the expressions of Part 2. A circuit may reuse a result as often "
            "as it likes. <bookmark mark='b'/> Sharing matters. Parity of n bits needs only about four n gates of and, "
            "or and not as a circuit. <bookmark mark='c'/> But as a formula, Valery Khrapchenko proved in 1971 that it "
            "needs at least n squared leaves, and n squared is enough. <bookmark mark='d'/> So sharing can save a "
            "polynomial factor. Whether it can ever save more than that, for some function, is another open question, "
            "and it is tangled up with whether problems can be solved quickly in parallel, which Part 10 meets."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(FadeIn(lines[2]))
            vo.wait_until("c")
            self.play(FadeIn(lines[3]))
            vo.wait_until("d")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gap(self):
        head = label(r"The embarrassing gap", font_size=38).to_edge(UP, buff=0.4)
        lines = VGroup(*[label(t, font_size=28, color=c) for t, c in (
            (r"almost every function needs $\approx 2^n / n$ gates", FUNC),
            (r"yet for no \textit{explicit} function \ (one we can write down, \ in NP) \\ has anyone proved more than "
             r"about $3.1\,n$ \ (Li and Yang, 2022)", LIMIT),
            (r"a superpolynomial lower bound for such a function \ would prove P $\ne$ NP", HEAD),
            (r"in restricted models we can: \ parity needs $2^{n-1}$ terms in depth 2, \\ and exponential size in any "
             r"constant depth \ (H\aa stad, 1986)", YES),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(DOWN * 0.1)
        later = note(r"why it is so hard to prove: \ Part 27", font_size=22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "And now the embarrassment. <bookmark mark='a'/> Almost every function needs exponentially many gates. "
            "<bookmark mark='b'/> Yet name a specific function, one you can actually write down and check, and nobody "
            "has proved it needs more than about three point one times n gates. That record is from 2022. "
            "<bookmark mark='c'/> The reason it matters: proving that some problem in NP needs more than polynomially "
            "many gates would prove that P is not equal to NP, the most famous open problem in the field. "
            "<bookmark mark='d'/> In weaker models we can prove such things. Parity needs exponentially many terms in "
            "depth two, as chapter six showed, and Johan Håstad proved it needs exponential size in any constant depth. "
            "Part 27 explains why the general case has resisted every technique so far."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l, shift=RIGHT * 0.1))
            self.play(FadeIn(later))
        self.wait(0.3)
        self.clear_scene()


def fmt(n) -> str:
    return f"{int(n):,}".replace(",", "{,}")
