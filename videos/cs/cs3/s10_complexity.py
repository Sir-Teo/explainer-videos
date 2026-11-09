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
            "and the gap grows: a chain is n minus one deep, a balanced tree ceiling log base two of n. Part 4's adders are a long fight to turn chains into "
            "trees."
        ) as vo:
            self.play(FadeIn(head), FadeIn(c1, lag_ratio=0.05), FadeIn(l1))
            vo.wait_until("a")
            self.play(FadeIn(defs))
            vo.wait_until("b")
            self.play(Circumscribe(c1, color=HEAD))
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
        concl = VGroup(label(r"if small circuits are a vanishing fraction of all functions, \ almost all functions need larger circuits",
                             font_size=28, color=HEAD),
                       MathTex(r"\frac{\#\{\text{functions with size}\le s\}}{2^{2^n}} \le 2^{\,s\log_2(16(n+s)^2)-2^n}",
                               font_size=32, color=YES),
                       label(r"so almost every function needs exponentially many gates", font_size=28, color=NO)).arrange(
            DOWN, buff=0.35).move_to(DOWN * 1.8)
        with self.voiceover(
            "How many gates does a typical function need? Shannon answered in 1949 without designing a single circuit. "
            "He counted. <bookmark mark='a'/> A function of n inputs is a truth table with two to the n rows, so there "
            "are two to the two to the n functions. For twenty inputs, a number with three hundred and fifteen thousand "
            "digits. <bookmark mark='b'/> A circuit with s gates is a list of s choices: a kind of gate, and two input "
            "wires. So there are at most about n plus s squared, to the s, of them. <bookmark mark='c'/> If the count of "
            "small circuits is a vanishing fraction of the function count, almost all functions need larger circuits. "
            "Almost every function of n inputs needs on the order of two to the n over n gates. Exponential. A random "
            "truth table is, almost surely, hopelessly hard."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lhs))
            vo.wait_until("a")
            self.play(Circumscribe(lhs, color=HEAD))
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
        defs = VGroup(label(r"AND/OR/NOT basis: \ a \textit{formula} is a tree, with no shared outputs", font_size=26,
                            color=GREY_A),
                      label(r"a \textit{circuit} may share: \ one output can feed many gates", font_size=26,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(head, DOWN, buff=0.3)
        # parity of four bits as an and/or formula with negations at the leaves: 16 leaves
        xor = lambda u, v: [(u, 0), (v, 1), (u, 1), (v, 0)]       # (u and not v) or (not u and v)
        xnor = lambda u, v: [(u, 0), (v, 0), (u, 1), (v, 1)]      # (u and v) or (not u and not v)
        lits = xor(1, 2) + xnor(3, 4) + xnor(1, 2) + xor(3, 4)
        vcol = {1: DATA, 2: CTRL, 3: FUNC, 4: HEAD}
        cx, top, dy, sp = -3.2, 0.9, 0.78, 0.4
        leaf_y = top - 4 * dy
        leaves = VGroup(*[MathTex(rf"\bar x_{v}" if neg else rf"x_{v}", font_size=24, color=vcol[v]).move_to(
            [cx + (i - 7.5) * sp, leaf_y, 0]) for i, (v, neg) in enumerate(lits)])
        nodes, edges = VGroup(), VGroup()
        below = [m.get_center() for m in leaves]
        for lvl in (3, 2, 1, 0):
            sym = r"\wedge" if lvl % 2 else r"\vee"
            here = []
            for i in range(2 ** lvl):
                kids = below[2 * i: 2 * i + 2]
                p = np.array([(kids[0][0] + kids[1][0]) / 2, top - lvl * dy, 0])
                for k in kids:
                    d = (k - p) / np.linalg.norm(k - p)
                    edges.add(Line(p + d * 0.17, k - d * (0.17 if lvl < 3 else 0.2), color=GREY_C, stroke_width=2))
                nodes.add(VGroup(Circle(0.17, stroke_color=GREY_A, stroke_width=2, fill_color="#121722",
                                        fill_opacity=1), MathTex(sym, font_size=22, color=GREY_A)).move_to(p))
                here.append(p)
            below = here
        ftree = VGroup(edges, nodes, leaves)
        flab = label(r"formula: \ 16 leaves \ $= n^2$", font_size=26, color=NO).next_to(leaves, DOWN, buff=0.25)
        # the same function as a circuit: three XORs, each input read once
        o = np.array([2.6, -0.9, 0])
        g1 = gate("XOR", size=0.6).move_to(o + np.array([-0.4, 0.75, 0]))
        g2 = gate("XOR", size=0.6).move_to(o + np.array([-0.4, -0.75, 0]))
        g3 = gate("XOR", size=0.6).move_to(o + np.array([1.2, 0, 0]))
        ins = VGroup()
        for gg, (u, v) in ((g1, (1, 2)), (g2, (3, 4))):
            for pin, w in zip(gg.inp, (u, v)):
                ins.add(MathTex(rf"x_{w}", font_size=24, color=vcol[w]).next_to(pin(), LEFT, buff=0.35))
                ins.add(Line(pin() + LEFT * 0.3, pin(), color=WIRE, stroke_width=2))
        circ = VGroup(g1, g2, g3, ins, wire(g1.out(), g3.inp[0]()), wire(g2.out(), g3.inp[1]()),
                      Line(g3.out(), g3.out() + RIGHT * 0.4, color=WIRE, stroke_width=2))
        clab = label(r"circuit: \ 3 XORs \ $=$ 12 AND/OR/NOT gates", font_size=26, color=YES).next_to(circ, DOWN, buff=0.45)
        khr = label(r"AND/OR/NOT formulas: \ $\ge n^2$ leaves; \ attained when $n = 2^k$ \ (Khrapchenko, 1971)", font_size=26,
                    color=NO).to_edge(DOWN, buff=0.3).shift(UP * 0.0)
        tail = label(r"sharing can save a polynomial; \ whether it ever saves more \ is open", font_size=26,
                     color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "There is a second way to measure. <bookmark mark='a'/> Fix the same basis of and, or and not for both. A formula is a circuit in which every gate's output "
            "is used only once, so it is a tree, like the expressions of Part 2. A circuit may reuse a result as often "
            "as it likes. <bookmark mark='b'/> Sharing matters. Parity of n bits needs only about four n gates of and, "
            "or and not as a circuit. <bookmark mark='c'/> But as a formula, Valery Khrapchenko proved in 1971 that it "
            "needs at least n squared leaves. Powers of two attain that bound; for general n the order is quadratic. <bookmark mark='d'/> So sharing can save a "
            "polynomial factor. Whether it can ever save more than that, for some function, is another open question, "
            "and it is tangled up with whether problems can be solved quickly in parallel, which Part 10 meets."
        ) as vo:
            self.play(FadeIn(head), FadeIn(circ, lag_ratio=0.05), FadeIn(clab))
            vo.wait_until("a")
            self.play(FadeIn(defs))
            vo.wait_until("b")
            self.play(Circumscribe(circ, color=HEAD))
            vo.wait_until("c")
            self.play(Create(edges), FadeIn(nodes), run_time=1.6)
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in leaves], lag_ratio=0.06), FadeIn(flab))
            self.play(FadeIn(khr))
            vo.wait_until("d")
            self.play(FadeOut(khr), FadeIn(tail))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gap(self):
        head = label(r"The embarrassing gap", font_size=38).to_edge(UP, buff=0.4)
        n = 100
        most = math.log10(2 ** n / n)
        leading = math.log10(4 * n)
        scale, x0, y0 = 0.36, -5.6, 0.15
        axis = NumberLine(x_range=[0, 30, 5], length=30 * scale, color=GREY_C, include_ticks=True,
                          stroke_width=2).move_to([x0 + 15 * scale, y0, 0])
        ticks = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=22, color=GREY_B).next_to(axis.n2p(k), DOWN, buff=0.15)
                         for k in range(0, 31, 5)])
        cap = note(rf"leading terms at $n = {n}$ inputs \ (log scale; lower-order terms omitted)", font_size=22).next_to(
            axis, DOWN, buff=0.6).align_to(axis, LEFT)
        bar_most = Rectangle(width=most * scale, height=0.34, stroke_width=0, fill_color=FUNC, fill_opacity=0.85)
        bar_most.move_to(axis.n2p(0) + UP * 1.55, aligned_edge=LEFT)
        bar_pr = Rectangle(width=leading * scale, height=0.34, stroke_width=0, fill_color=LIMIT, fill_opacity=0.9)
        bar_pr.move_to(axis.n2p(0) + UP * 0.75, aligned_edge=LEFT)
        l_most = label(rf"almost every function: \ $\approx 2^n/n \approx 10^{{{most:.0f}}}$", font_size=26,
                       color=FUNC).next_to(bar_most, UP, buff=0.15).align_to(bar_most, LEFT)
        l_pr = label(r"reported: \ $4n-O(\log n)$ \\ Mishra and Santhanam, \ November 2026 preprint", font_size=24,
                     color=LIMIT).next_to(bar_pr, RIGHT, buff=0.25)
        lines = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"a superpolynomial lower bound for one function in NP \ would prove P $\ne$ NP", HEAD),
            (r"in restricted models we can: \ parity needs $2^{n-1}$ terms in depth 2, \\ and exponential size in any "
             r"constant depth \ (H\aa stad, 1986); \ why the rest is so hard: \ Part 27", YES),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.35).align_to(axis, LEFT)
        with self.voiceover(
            "And now the embarrassment. <bookmark mark='a'/> Almost every function needs exponentially many gates. "
            "<bookmark mark='b'/> Yet for explicit functions the lower bounds remain linear. Li and Yang reached "
            "three point one n in 2022. A November 2026 preprint by Om Swostik Mishra and Rahul Santhanam reports "
            "four n minus a logarithmic term. Even that is tiny beside the exponential bound for almost every function. "
            "<bookmark mark='c'/> The reason it matters: proving that some problem in NP needs more than polynomially "
            "many gates would prove that P is not equal to NP, the most famous open problem in the field. "
            "<bookmark mark='d'/> In weaker models we can prove such things. Parity needs exponentially many terms in "
            "depth two, as chapter six showed, and Johan Håstad proved it needs exponential size in any constant depth. "
            "Part 27 explains why the general case has resisted every technique so far."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(ticks), FadeIn(cap))
            vo.wait_until("a")
            self.play(GrowFromEdge(bar_most, LEFT), FadeIn(l_most), run_time=1.6)
            vo.wait_until("b")
            self.play(GrowFromEdge(bar_pr, LEFT), FadeIn(l_pr))
            self.play(Indicate(bar_pr, color=NO))
            vo.wait_until("c")
            self.play(FadeIn(lines[0], shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(lines[1], shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

def fmt(n) -> str:
    return f"{int(n):,}".replace(",", "{,}")
