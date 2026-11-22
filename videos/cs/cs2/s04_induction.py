from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs2.common import CTRL, DATA, HEAD, NO, PART, YES, grid_squares, load

LEVEL_COLORS = [C.CS_HEAD, C.CS_CONTROL, C.CS_DATA, C.CS_FUNC]


def domino(h=1.1, w=0.32, color=GREY_B) -> Rectangle:
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=2, fill_color="#1B2130", fill_opacity=1)


class Induction(WatchScene):
    def construct(self):
        self.card()
        self.dominoes()
        self.gauss()
        self.horses()
        self.tromino()

    def card(self):
        self.chapter(3, r"Induction", r"How do you prove infinitely many things at once?", part=PART, said="Chapter three. Induction.")

    # ------------------------------------------------------------------
    def dominoes(self):
        head = label(r"Induction", font_size=40).to_edge(UP, buff=0.4)
        ds = VGroup(*[domino() for _ in range(12)]).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.3)
        nums = VGroup(*[MathTex(str(i), font_size=24, color=GREY_B).next_to(d, DOWN, buff=0.15) for i, d in
                        enumerate(ds)])
        dots = MathTex(r"\cdots", font_size=40, color=GREY_B).next_to(ds, RIGHT, buff=0.3)
        base = label(r"base: \ $P(0)$", font_size=30, color=YES)
        step = label(r"step: \ $P(n) \Rightarrow P(n + 1)$ \ for every $n$", font_size=30, color=CTRL)
        concl = label(r"so: \ $P(n)$ for every $n$", font_size=32, color=HEAD)
        VGroup(base, step).arrange(RIGHT, buff=1.0).next_to(head, DOWN, buff=0.5)
        concl.next_to(nums, DOWN, buff=0.5)
        with self.voiceover(
            "Most of the statements this series cares about are about infinitely many things: every input, every "
            "length, every number of steps. You cannot check them one by one. Induction proves them all at once. "
            "<bookmark mark='a'/> Line up dominoes, one for each natural number. <bookmark mark='b'/> Show that the "
            "first one falls: that is the base case, P of zero. <bookmark mark='c'/> And show that whenever one falls, "
            "it knocks over the next: if P of n is true, so is P of n plus one, for every n. That is the inductive "
            "step. <bookmark mark='d'/> Then every domino falls. Nothing is checked infinitely many times; two finite "
            "arguments cover them all."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(d, shift=UP * 0.2) for d in ds], lag_ratio=0.06),
                      FadeIn(nums), FadeIn(dots))
            vo.wait_until("a")
            self.play(Indicate(nums, color=HEAD, scale_factor=1.05))
            vo.wait_until("b")
            self.play(FadeIn(base), ds[0].animate.set_stroke(YES))
            vo.wait_until("c")
            self.play(FadeIn(step))
            vo.wait_until("d")
            for i, d in enumerate(ds):
                d.set_stroke(YES)
                self.play(Rotate(d, -1.0, about_point=d.get_corner(DR)), run_time=0.22)
            self.play(FadeIn(concl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gauss(self):
        head = label(r"$1 + 2 + \cdots + n = \dfrac{n(n + 1)}{2}$", font_size=40).to_edge(UP, buff=0.35)
        n, s = 6, 0.42
        o = np.array([-5.6, -2.6, 0])
        stair = VGroup(*[Square(s, stroke_color=BACKGROUND, stroke_width=2, fill_color=DATA, fill_opacity=0.9).move_to(
            o + np.array([(c + 0.5) * s, (r + 0.5) * s, 0])) for c in range(n) for r in range(c + 1)])
        copy = VGroup(*[Square(s, stroke_color=BACKGROUND, stroke_width=2, fill_color=CTRL, fill_opacity=0.9).move_to(
            o + np.array([(c + 0.5) * s, (r + 0.5) * s, 0])) for c in range(n) for r in range(c + 1, n + 1)])
        rect = label(r"two staircases make an \\ $n \times (n + 1)$ rectangle", font_size=26, color=GREY_A)
        rect.next_to(VGroup(stair, copy), UP, buff=0.3)
        proof = VGroup(*[MathTex(t, font_size=36, color=c) for t, c in (
            (r"\text{base: } 1 = \tfrac{1 \cdot 2}{2}", YES),
            (r"\text{step: assume } 1 + \cdots + n = \tfrac{n(n+1)}{2}", GREY_A),
            (r"1 + \cdots + n + (n+1) = \tfrac{n(n+1)}{2} + (n + 1)", CTRL),
            (r"= \tfrac{(n+1)(n+2)}{2}", HEAD),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 2.6 + DOWN * 0.2)
        why = note(r"the picture finds the formula; \ induction proves it", font_size=24).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "A first example: the sum one plus two up to n. <bookmark mark='a'/> A picture guesses the answer. Stack "
            "the numbers as a staircase. <bookmark mark='b'/> A second copy, turned over, completes an n by n plus one "
            "rectangle, so the sum is half of n times n plus one. <bookmark mark='c'/> Induction proves it. The base "
            "case: one is one times two over two. <bookmark mark='d'/> The step: assume it for n. Add the next number, "
            "n plus one, to both sides. <bookmark mark='e'/> Factor, and the right side is exactly the formula for n "
            "plus one. That pattern, a picture or an experiment to find the claim and induction to prove it, is how "
            "Part 16 will find and prove the running times of algorithms."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(q, scale=0.6) for q in stair], lag_ratio=0.03), run_time=1.6)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(q, shift=DOWN * 0.2) for q in copy], lag_ratio=0.03), FadeIn(rect),
                      run_time=1.6)
            for mk, l in zip("cde", (proof[0], proof[1:3], proof[3])):
                vo.wait_until(mk)
                self.play(FadeIn(l, shift=RIGHT * 0.15))
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()


    # ------------------------------------------------------------------
    def horses(self):
        self.ask(r"A proof by induction that all horses are one colour. \\ Where does it break?",
                 [r"the base case", r"the step from one horse to two", r"the step for large $n$"], 1,
                 say="Here is a proof that every horse is the same colour. It must be wrong. Where does it break?",
                 reveal="At the step from one horse to two, where the two groups don't overlap.")
        head = label(r"A false proof: \ ``all horses are the same colour''", font_size=38).to_edge(UP, buff=0.4)
        cols = [DATA, DATA, DATA, DATA, DATA]
        horses = VGroup(*[Circle(0.32, stroke_color=WHITE, stroke_width=2, fill_color=c, fill_opacity=0.7)
                          for c in cols]).arrange(RIGHT, buff=0.35).move_to(UP * 0.6)
        g1 = SurroundingRectangle(horses[:-1], color=CTRL, buff=0.15, corner_radius=0.15)
        g2 = SurroundingRectangle(horses[1:], color=YES, buff=0.27, corner_radius=0.2)
        arg = label(r"step: \ the first $n$ share a colour, \ the last $n$ share a colour, \\ and the two groups "
                    r"overlap, \ so all $n + 1$ share one", font_size=27, color=GREY_A).next_to(horses, DOWN, buff=0.6)
        two = VGroup(Circle(0.32, stroke_color=WHITE, stroke_width=2, fill_color=DATA, fill_opacity=0.7),
                     Circle(0.32, stroke_color=WHITE, stroke_width=2, fill_color=NO, fill_opacity=0.7)).arrange(
            RIGHT, buff=0.9).next_to(arg, DOWN, buff=0.7)
        b1 = SurroundingRectangle(two[0], color=CTRL, buff=0.12)
        b2 = SurroundingRectangle(two[1], color=YES, buff=0.12)
        bug = label(r"$n = 1 \to 2$: \ the groups do not overlap. \ The step fails exactly once, \ and once is enough.",
                    font_size=26, color=NO).next_to(two, DOWN, buff=0.4)
        with self.voiceover(
            "Induction is only as good as its step, and the step must work for every n. Here is a famous false proof. "
            "Claim: in any group of horses, all are the same colour. <bookmark mark='a'/> The base case, one horse, is "
            "fine. The step: take n plus one horses. The first n share a colour, by assumption. So do the last n. "
            "<bookmark mark='b'/> The groups overlap, so all n plus one share a colour. <bookmark mark='c'/> Where is "
            "the bug? Go from one horse to two. The first group is the first horse; the second group is the second "
            "horse. They do not overlap at all. The step fails at exactly one value of n, and one failure is enough to "
            "break the chain. Off-by-one errors in proofs and off-by-one errors in loops are the same mistake."
        ) as vo:
            self.play(FadeIn(head), FadeIn(horses))
            vo.wait_until("a")
            self.play(Create(g1), Create(g2))
            vo.wait_until("b")
            self.play(FadeIn(arg))
            vo.wait_until("c")
            self.play(FadeIn(two), Create(b1), Create(b2))
            self.play(FadeIn(bug))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tromino(self):
        d = load("tromino")
        n = 2 ** d["n"]
        cell = 0.66
        board = grid_squares(n, n, cell=cell).move_to(LEFT * 2.6 + DOWN * 0.3)
        hr, hc = d["hole"]
        hole = board.sq[(hr, hc)].copy().set_fill(BLACK, 1).set_stroke(NO, 3)
        head = label(r"Tiling a $2^n \times 2^n$ board, \ one square removed, \ with L-shaped pieces", font_size=34)
        head.to_edge(UP, buff=0.3)

        def piece(cells, color):
            sqs = [board.sq[tuple(c)].copy().set_fill(color, 0.85).set_stroke(BACKGROUND, 2) for c in cells]
            return VGroup(*sqs)

        by_level = {}
        for p in d["pieces"]:
            by_level.setdefault(p["level"], []).append(p)
        steps = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"base: \ $1 \times 1$ with its square removed: \ nothing to tile", YES),
            (r"step: \ cut the board into four quarters", GREY_A),
            (r"one quarter holds the hole; \ one piece in the centre \\ makes a hole in each of the others", HEAD),
            (r"four smaller boards, \ each with one square removed: \\ tile each by the same rule", CTRL),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.6 + DOWN * 0.1)
        count = note(rf"computed: \ ${len(d['pieces'])}$ pieces $= (4^3 - 1)/3$", font_size=22).next_to(
            board, DOWN, buff=0.2)

        def cuts(size):
            g = VGroup()
            for r0 in range(0, n, size):
                for c0 in range(0, n, size):
                    tl = board.sq[(r0, c0)].get_corner(UL)
                    mid = size / 2 * cell
                    g.add(Line(tl + RIGHT * mid, tl + RIGHT * mid + DOWN * size * cell, color=WHITE, stroke_width=2.5),
                          Line(tl + DOWN * mid, tl + DOWN * mid + RIGHT * size * cell, color=WHITE, stroke_width=2.5))
            return g

        with self.voiceover(
            "Induction does more than verify formulas. It builds things. <bookmark mark='a'/> Take a board two to the n "
            "squares on a side, remove any one square, and try to tile the rest with L-shaped pieces of three squares. "
            "Is it always possible? <bookmark mark='b'/> Induction on n. A one by one board with its square removed is "
            "empty: nothing to do. <bookmark mark='c'/> For the step, cut the board into four quarters. "
            "<bookmark mark='d'/> One of them contains the hole. Place one piece in the centre, covering a corner of "
            "each of the other three quarters. <bookmark mark='e'/> Now there are four smaller boards, each missing one "
            "square, and the induction hypothesis tiles each of them. Read the proof as a program, and it is a "
            "recursive algorithm. Here it runs: the centre piece first, then each quarter's centre piece, then each "
            "sixteenth's."
        ) as vo:
            self.play(FadeIn(head), FadeIn(board), FadeIn(hole))
            vo.wait_until("b")
            self.play(FadeIn(steps[0]))
            vo.wait_until("c")
            c1 = cuts(n)
            self.play(FadeIn(steps[1]), Create(c1))
            vo.wait_until("d")
            self.play(FadeIn(steps[2]), FadeIn(piece(by_level[0][0]["cells"], LEVEL_COLORS[0])))
            vo.wait_until("e")
            self.play(FadeIn(steps[3]))
            for lvl in sorted(by_level):
                if lvl == 0:
                    continue
                size = n // 2 ** lvl
                cc = cuts(size)
                self.play(Create(cc), run_time=0.6)
                self.play(LaggedStart(*[FadeIn(piece(p["cells"], LEVEL_COLORS[lvl % 4]), scale=0.8)
                                        for p in by_level[lvl]], lag_ratio=0.08), run_time=1.6)
            self.play(FadeIn(count))
        self.wait(0.3)
        self.clear_scene()
