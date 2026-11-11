from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs1.common import ADV, CODE, CTRL, DATA, HEAD, INF, LIMIT, NO, PART, YES, fmt, load

MONO_ = "DejaVu Sans Mono"


def bit(b, size=0.42, color=None):
    sq = Square(size, stroke_width=1, stroke_color=GREY_D, fill_color=BACKGROUND, fill_opacity=1)
    t = Text(str(b), font=MONO_, font_size=int(size * 52), color=color or (C.BIT1 if b else C.BIT0))
    return VGroup(sq, t.move_to(sq))


class Diagonal(VoiceoverScene):
    def construct(self):
        self.card()
        self.counting()
        self.programs()
        self.cantor()
        self.problems()

    def card(self):
        card = chapter_card(10, r"More problems than programs", r"Is every problem solved by some program?",
                            lit=(1874, 1891), part=PART)
        with self.voiceover("Chapter ten. More problems than programs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def counting(self):
        head = label(r"Two infinite sets are the same size \\ if they can be paired off, one to one", font_size=34)
        head.to_edge(UP, buff=0.35)
        nat = VGroup(*[MathTex(str(i), font_size=34, color=DATA) for i in range(9)]).arrange(RIGHT, buff=0.75)
        ev = VGroup(*[MathTex(str(2 * i), font_size=34, color=INF) for i in range(9)])
        for a, b in zip(nat, ev):
            b.next_to(a, DOWN, buff=0.9)
        VGroup(nat, ev).move_to(UP * 0.9)
        dots = VGroup(MathTex(r"\cdots", color=GREY_B).next_to(nat, RIGHT), MathTex(r"\cdots", color=GREY_B).next_to(ev, RIGHT))
        links = VGroup(*[Line(a.get_bottom(), b.get_top(), buff=0.1, color=GREY_C, stroke_width=2) for a, b in zip(nat, ev)])
        # the grid of pairs, and the zig-zag through it
        n = 6
        grid = VGroup()
        pos = {}
        for i in range(n):
            for j in range(n):
                t = MathTex(rf"({i},{j})", font_size=24, color=GREY_A)
                t.move_to([-6.0 + j * 1.12, -1.0 - i * 0.52, 0])
                t.add_background_rectangle(color=BACKGROUND, opacity=1, buff=0.03)
                pos[(i, j)] = t.get_center()
                grid.add(t)
        order = []
        for s_ in range(n):  # boustrophedon along the anti-diagonals, as Cantor walks them
            diag_ = [(i, s_ - i) for i in range(s_ + 1)]
            order += diag_ if s_ % 2 else diag_[::-1]
        path = VMobject(color=HEAD, stroke_width=3, stroke_opacity=0.75).set_points_as_corners([pos[p] for p in order])
        path.set_z_index(-1)
        nums = VGroup(*[MathTex(str(k + 1), font_size=19, color=HEAD).move_to(pos[p] + UP * 0.25 + RIGHT * 0.42)
                        for k, p in enumerate(order[:15])])
        gl = label(r"pairs, \ and so fractions: \ walk the diagonals", font_size=26, color=HEAD)
        gl.next_to(grid, RIGHT, buff=0.6).align_to(grid, UP).shift(DOWN * 0.2)
        cl = label(r"\textit{countable}: \ listed as \\ first, second, third, \dots", font_size=28, color=INF)
        cl.next_to(gl, DOWN, buff=0.5).align_to(gl, LEFT)
        with self.voiceover(
            "To compare problems with programs, we need to compare infinite sets, and the tool is Georg Cantor's, from "
            "the 1870s. Two sets have the same size if their elements can be paired off, one to one, with none left "
            "over. <bookmark mark='a'/> The natural numbers and the even numbers: pair n with two n. So there are as "
            "many even numbers as numbers. <bookmark mark='b'/> Pairs of numbers, and so fractions: lay them out in a "
            "grid and walk the diagonals, numbering as you go. Every pair gets a number. <bookmark mark='c'/> A set that "
            "can be listed like this, first, second, third, is called countable."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(nat), FadeIn(ev), Create(links), FadeIn(dots), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(grid, lag_ratio=0.01), FadeIn(gl))
            self.play(Create(path), LaggedStart(*[FadeIn(k) for k in nums], lag_ratio=0.1), run_time=2.6,
                      rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(cl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def programs(self):
        d = load("machines")
        head = label(r"Programs can be listed", font_size=40).to_edge(UP, buff=0.4)
        strings = [""] + [format(k, f"0{L}b") for L in range(1, 4) for k in range(2 ** L)]
        row = VGroup()
        for s in strings[:13]:
            t = Text(s if s else "ε", font=MONO_, font_size=26, color=CODE)
            row.add(t)
        row.arrange(RIGHT, buff=0.42).move_to(UP * 1.6)
        idx = VGroup(*[MathTex(str(i + 1), font_size=20, color=GREY_B).next_to(t, UP, buff=0.12)
                       for i, t in enumerate(row)])
        more = MathTex(r"\cdots", color=GREY_B).next_to(row, RIGHT)
        rl = label(r"every finite string, \ shortest first, \ then in dictionary order", font_size=26,
                   color=GREY_A).next_to(row, DOWN, buff=0.35)
        tab = VGroup()
        for c in d["counts"]:
            tab.add(VGroup(label(rf"{c['n']} states:", font_size=26, color=GREY_A),
                           label(rf"${fmt(c['count'])}$ machines", font_size=26, color=CTRL)).arrange(RIGHT, buff=0.3))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(DOWN * 1.6 + RIGHT * 2.8)
        tl = label(r"machines with $n$ states and 2 symbols: \ $(4n+4)^{2n}$", font_size=26, color=CTRL)
        tl.next_to(tab, UP, buff=0.3)
        con = label(r"descriptions $\langle M \rangle$ are strings, \\ so the machines can be listed: \\ "
                    r"$M_1,\ M_2,\ M_3,\ \dots$", font_size=30, color=CODE).move_to(DOWN * 1.6 + LEFT * 3.6)
        with self.voiceover(
            "Programs are countable. <bookmark mark='a'/> Every program, and every machine description, is a finite "
            "string of symbols. List all finite strings: the empty string, then those of length one, then length two, "
            "in dictionary order, and so on. Every string appears somewhere in the list. <bookmark mark='b'/> So the "
            "machines can be listed too: M one, M two, M three, and so on, in the order of their descriptions. "
            "<bookmark mark='c'/> The list grows fast: there are about twenty thousand machines with two states, "
            "sixty trillion with five. But it is a list."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in row], lag_ratio=0.1), FadeIn(idx), FadeIn(more), FadeIn(rl))
            vo.wait_until("b")
            self.play(FadeIn(con))
            vo.wait_until("c")
            self.play(FadeIn(tl), LaggedStart(*[FadeIn(t) for t in tab], lag_ratio=0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cantor(self):
        rng = np.random.default_rng(11)
        R, K = 7, 10
        M = rng.integers(0, 2, (R, K))
        size = 0.48
        rows = VGroup()
        for i in range(R):
            r = VGroup(*[bit(int(M[i, j]), size) for j in range(K)]).arrange(RIGHT, buff=0)
            rows.add(r)
        rows.arrange(DOWN, buff=0).move_to(UP * 0.55 + RIGHT * 0.6)
        names = VGroup(*[MathTex(rf"s_{i + 1}", font_size=28, color=INF).next_to(rows[i], LEFT, buff=0.3)
                         for i in range(R)])
        dots_r = VGroup(*[MathTex(r"\cdots", font_size=26, color=GREY_B).next_to(r, RIGHT, buff=0.15) for r in rows])
        vdots = MathTex(r"\vdots", font_size=30, color=GREY_B).next_to(rows, DOWN, buff=0.1)
        head = label(r"Cantor (1891): \ no list of infinite 0-1 sequences contains them all", font_size=32)
        head.to_edge(UP, buff=0.3)
        tag = note(r"illustrative: any list would do", font_size=22).to_corner(DR, buff=0.3)
        diag = VGroup(*[SurroundingRectangle(rows[i][i], color=HEAD, buff=0, stroke_width=3) for i in range(R)])
        new = VGroup(*[bit(1 - int(M[i, i]), size, color=ADV) for i in range(R)]).arrange(RIGHT, buff=0)
        new.next_to(vdots, DOWN, buff=0.35).align_to(rows, LEFT)
        nn = MathTex(r"d", font_size=32, color=ADV).next_to(new, LEFT, buff=0.3)
        rule = label(r"$d$ differs from $s_k$ \ in place $k$", font_size=30, color=ADV).next_to(new, RIGHT, buff=0.6)
        with self.voiceover(
            "Now a set that is not countable. <bookmark mark='a'/> Suppose someone hands you a list of infinite "
            "sequences of zeros and ones, s one, s two, s three, and claims it contains every such sequence. "
            "<bookmark mark='b'/> Look at the diagonal: the first digit of the first sequence, the second digit of the "
            "second, and so on. <bookmark mark='c'/> Now build a new sequence, d, by flipping every diagonal digit. "
            "<bookmark mark='d'/> d is not s one: they differ in the first place. It is not s two: they differ in the "
            "second. It differs from the k-th sequence in the k-th place, so it is nowhere in the list. "
            "<bookmark mark='e'/> Any list misses something. The infinite sequences cannot be listed: there are "
            "strictly more of them than there are natural numbers."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(n, r, d_)) for n, r, d_ in zip(names, rows, dots_r)], lag_ratio=0.15),
                      FadeIn(vdots), FadeIn(tag), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(b) for b in diag], lag_ratio=0.2), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(nn), LaggedStart(*[TransformFromCopy(rows[i][i], new[i]) for i in range(R)],
                                              lag_ratio=0.2), run_time=2.4)
            vo.wait_until("d")
            for i in range(3):
                self.play(Indicate(rows[i][i], color=ADV), Indicate(new[i], color=ADV), run_time=0.7)
            self.play(FadeIn(rule))
            vo.wait_until("e")
            self.play(Indicate(new, color=ADV, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        strings = [""] + [format(k, f"0{L}b") for L in range(1, 4) for k in range(2 ** L)]
        strings = strings[:13]
        cols = VGroup(*[Text(s if s else "ε", font=MONO_, font_size=18, color=CODE) for s in strings])
        cells = VGroup(*[bit(int(s == s[::-1]), 0.66) for s in strings]).arrange(RIGHT, buff=0)
        cells.move_to(UP * 0.9)
        for t, c in zip(cols, cells):
            t.next_to(c, UP, buff=0.18)
        more = MathTex(r"\cdots", color=GREY_B).next_to(cells, RIGHT)
        pl = label(r"the problem ``is it a palindrome?'' \ as a 0-1 sequence over all strings", font_size=28,
                   color=DATA).next_to(cols, UP, buff=0.35)
        left = VGroup(label(r"programs", font_size=34, color=CODE), label(r"countable", font_size=28, color=GREY_A))
        right = VGroup(label(r"problems", font_size=34, color=DATA), label(r"uncountable", font_size=28, color=GREY_A))
        left.arrange(DOWN, buff=0.15).move_to(DOWN * 1.6 + LEFT * 3.6)
        right.arrange(DOWN, buff=0.15).move_to(DOWN * 1.6 + RIGHT * 3.6)
        less = MathTex(r"<", font_size=90, color=LIMIT).move_to(DOWN * 1.6)
        concl = label(r"so most problems have no program at all \\ but this argument names none of them", font_size=30,
                      color=LIMIT).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now connect the two. <bookmark mark='a'/> A yes-or-no problem about strings, like is it a palindrome, is "
            "exactly an infinite sequence of zeros and ones: for each string in our list, a one if the answer is yes and "
            "a zero if it is no. Empty string, yes. Zero, yes. One, yes. Zero zero, yes. Zero one, no. And every "
            "infinite sequence is some problem. <bookmark mark='b'/> So the problems are uncountable, and the programs "
            "are countable. There are strictly more problems than programs. <bookmark mark='c'/> Most problems, in a "
            "precise sense almost all of them, cannot be solved by any program. But notice: this argument proves they "
            "exist without naming a single one. Turing named one. And it is a problem you would very much like to "
            "solve."
        ) as vo:
            self.play(FadeIn(pl), LaggedStart(*[FadeIn(VGroup(t, c)) for t, c in zip(cols, cells)], lag_ratio=0.1),
                      FadeIn(more), run_time=2.2)
            vo.wait_until("b")
            self.play(FadeIn(left), FadeIn(right), FadeIn(less, scale=1.3))
            vo.wait_until("c")
            self.play(FadeIn(concl))
        self.wait(0.3)
        self.clear_scene()
