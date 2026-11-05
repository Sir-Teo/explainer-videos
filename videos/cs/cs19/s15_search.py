from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


def first_queens(n):
    sol = []

    def go(r):
        if r == n:
            return True
        for c in range(n):
            if all(c != pc and abs(c - pc) != r - pr for pr, pc in enumerate(sol)):
                sol.append(c)
                if go(r + 1):
                    return True
                sol.pop()
        return False
    go(0)
    return sol


class Search(VoiceoverScene):
    def construct(self):
        self.card()
        self.queens()
        self.counts()
        self.cover()
        self.sudoku()

    def card(self):
        card = chapter_card(14, r"Backtracking and Dancing Links", r"How do you search a space too big to list?",
                            lit=(2000,), extra=((1848, r"the eight queens"), (2000, r"Knuth: \ Dancing Links")),
                            part=PART)
        with self.voiceover("Chapter fourteen. Backtracking and Dancing Links."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def queens(self):
        head = label(r"Eight queens \ (Bezzel, \ 1848)", font_size=34).to_edge(UP, buff=0.3)
        n, s = 8, 0.58
        c0 = [-3.6, -0.3, 0]
        board = VGroup(*[Square(side_length=s, stroke_width=0, fill_color="#2a3142" if (r + c) % 2 else "#1b2030",
                                fill_opacity=1).move_to([c0[0] + (c - 3.5) * s, c0[1] + (3.5 - r) * s, 0])
                         for r in range(n) for c in range(n)])
        sol = first_queens(8)

        def queen(r, c, col=YES):
            return VGroup(Circle(radius=0.2, color=col, fill_color=col, fill_opacity=0.8, stroke_width=1.5),
                          mono("Q", 14, BG)).move_to([c0[0] + (c - 3.5) * s, c0[1] + (3.5 - r) * s, 0])
        side = VGroup(
            label(r"place 8 queens so that none attacks another", font_size=22, color=GREY_A),
            label(r"\textbf{backtracking}: \ one queen per row; \ try each safe column; \\ if none is safe, \ undo "
                  r"the last choice and try its next column", font_size=21, color=HEAD),
            label(r"a whole subtree is skipped the moment a partial placement fails", font_size=21, color=YES),
            label(r"Nauck \ (1850): \ 92 solutions", font_size=22, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        # a short trace of the first rows, with one backtrack
        trace = [(0, 0), (1, 2), (2, 4), (3, 1), (4, 3)]
        with self.voiceover(
            "When no clever structure is known, we search. <bookmark mark='a'/> In 1848 the chess player Max "
            "Bezzel asked how to place eight queens on a chessboard so that none attacks another. <bookmark "
            "mark='b'/> Backtracking places one queen per row. In each row it tries the safe columns in turn; when "
            "a row has no safe column, it undoes the previous choice and moves that queen on. <bookmark mark='c'/> "
            "The power of the method is what it does not do: as soon as a partial placement fails, everything "
            "that would extend it is skipped. <bookmark mark='d'/> Here is the first solution found, and Franz "
            "Nauck showed in 1850 that there are ninety-two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(board))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            qs = VGroup()
            for r, c in trace:
                q = queen(r, c, HEAD)
                qs.add(q)
                self.play(FadeIn(q, scale=0.6), run_time=0.35)
            self.play(qs[-1].animate.set_opacity(0.2), run_time=0.3)
            self.play(FadeOut(qs), run_time=0.4)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(*[FadeIn(queen(r, c)) for r, c in enumerate(sol)], FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def counts(self):
        d = load("search")
        head = label(r"What pruning buys", font_size=34).to_edge(UP, buff=0.3)
        def big(v):
            if v < 1e6:
                return f"{v:,}"
            e = len(str(v)) - 1
            return rf"${v / 10 ** e:.1f} \times 10^{{{e}}}$"
        rows = [[str(r["n"]), f"{r['solutions']:,}", f"{r['nodes']:,}", big(r["placements"]),
                 f"{r['s'] * 1000:.0f} ms" if r["s"] < 1 else f"{r['s']:.1f} s"]
                for r in d["queens"] if r["n"] in (4, 6, 8, 10, 12, 13, 14)]
        tab = grid_table([r"$n$", r"solutions", r"search nodes", r"placements, \ one per row", r"time"], rows,
                         widths=[1.2, 2.2, 2.8, 3.4, 1.8], row_h=0.46, font_size=20,
                         colors=[[WHITE, YES, HEAD, NO, LAM]] * len(rows)).next_to(head, DOWN, buff=0.5)
        r8 = next(r for r in d["queens"] if r["n"] == 8)
        pts = VGroup(
            label(rf"8 queens: \ {r8['nodes']:,} nodes, \ against {r8['placements']:,} placements", font_size=22,
                  color=YES),
            label(r"still exponential: \ each extra queen multiplies the work by about five \ (bitmasks make each "
                  r"node cheap)", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Counted on this machine. <bookmark mark='a'/> For eight queens, backtracking visits two thousand and "
            "fifty-seven partial placements, out of almost seventeen million ways to put one queen in each row. "
            "<bookmark mark='b'/> But pruning does not change the nature of the problem: the search still grows "
            "exponentially, about five to six times per extra queen, and fourteen queens take twenty-seven million "
            "nodes and sixteen seconds, even with each node checked by a few bit operations."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
        self.wait(0.3)
        self.clear_scene()

    def cover(self):
        head = label(r"Exact cover, \ and dancing links", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"\textbf{exact cover}: \ choose rows of a 0--1 matrix so that every column has exactly one 1",
                  font_size=21, color=GREY_A),
            label(r"Sudoku: \ 729 rows \ (cell, \ digit), \ 324 columns: \ each cell filled; \ each digit once per "
                  r"row, \ column and box", font_size=21, color=HEAD),
            label(r"Algorithm X: \ pick the column with \textbf{fewest} 1s, \ try each row in it, \ remove what it "
                  r"conflicts with, \ recurse", font_size=21, color=GREY_A),
            label(r"\textbf{dancing links}: \ remove $x$ from a doubly linked list, \ keeping $x$'s pointers:",
                  font_size=21, color=YES),
            MathTex(r"L[R[x]] \gets L[x], \quad R[L[x]] \gets R[x] \qquad \text{undo:} \quad L[R[x]] \gets x, \quad "
                    r"R[L[x]] \gets x", font_size=28, color=LAM),
            label(r"so backtracking restores the matrix in exactly the time it took to change it \ (Hitotumatu and "
                  r"Noshita, \ 1979; \ Knuth, \ 2000)", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.27).next_to(head, DOWN, buff=0.45)
        # a tiny linked list: a <-> x <-> b, x unlinked and relinked
        y = -3.2
        a = VGroup(Square(0.5, color=DATA), mono("a", 16, WHITE)).move_to([-2.0, y, 0])
        x = VGroup(Square(0.5, color=HEAD), mono("x", 16, WHITE)).move_to([0, y, 0])
        b = VGroup(Square(0.5, color=DATA), mono("b", 16, WHITE)).move_to([2.0, y, 0])
        ax_ = Arrow(a.get_right(), x.get_left(), buff=0.05, stroke_width=2, color=GREY_B)
        xb = Arrow(x.get_right(), b.get_left(), buff=0.05, stroke_width=2, color=GREY_B)
        ab = CurvedArrow(a.get_top(), b.get_top(), angle=-0.6, color=YES, stroke_width=2.5, tip_length=0.15)
        with self.voiceover(
            "Sudoku is a better showcase. <bookmark mark='a'/> It is an exact cover problem: choose some rows of a "
            "zero–one matrix so that every column contains exactly one one. <bookmark mark='b'/> Each row is a "
            "digit placed in a cell, seven hundred and twenty-nine of them, and each column is a constraint, three "
            "hundred and twenty-four: every cell filled, and every digit once in every row, column and box. "
            "<bookmark mark='c'/> Knuth's Algorithm X picks the constraint with the fewest options, tries each, "
            "deletes everything that conflicts with it, and recurses. <bookmark mark='d'/> The trick that makes it "
            "fast: to delete an element from a doubly linked list, point its neighbours at each other, but leave "
            "the element's own pointers alone. <bookmark mark='e'/> Then undoing is two assignments, and the "
            "element dances back into place. <bookmark mark='f'/> Backtracking restores the whole matrix in "
            "exactly the time it took to change it. Knuth named the technique dancing links in 2000, crediting "
            "Hitotumatu and Noshita, 1979."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a), FadeIn(x), FadeIn(b), Create(ax_), Create(xb))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
            self.play(Create(ab), x.animate.shift(DOWN * 0.45).set_opacity(0.5), FadeOut(ax_), FadeOut(xb))
            vo.wait_until("e")
            self.play(FadeIn(pts[4]), FadeOut(ab), x.animate.shift(UP * 0.45).set_opacity(1), FadeIn(ax_),
                      FadeIn(xb))
            vo.wait_until("f")
            self.play(FadeIn(pts[5]))
        self.wait(0.3)
        self.clear_scene()

    def sudoku(self):
        d = load("search")
        hard = d["sudoku"][-1]
        head = label(r"Three Sudokus", font_size=34).to_edge(UP, buff=0.3)
        g, sol = hard["grid"], hard["solution"]
        s = 0.42
        c0 = [-4.0, -0.4, 0]
        cells = VGroup()
        given = VGroup()
        filled = VGroup()
        for i in range(81):
            r, c = divmod(i, 9)
            p = [c0[0] + (c - 4) * s, c0[1] + (4 - r) * s, 0]
            cells.add(Square(side_length=s, stroke_color=GREY_D, stroke_width=1).move_to(p))
            if g[i] != ".":
                given.add(mono(g[i], 17, WHITE).move_to(p))
            else:
                filled.add(mono(sol[i], 17, YES).move_to(p))
        thick = VGroup(*[Line([c0[0] - 4.5 * s + 3 * k * s, c0[1] + 4.5 * s, 0],
                              [c0[0] - 4.5 * s + 3 * k * s, c0[1] - 4.5 * s, 0], color=GREY_B, stroke_width=2.5)
                         for k in range(4)],
                       *[Line([c0[0] - 4.5 * s, c0[1] + 4.5 * s - 3 * k * s, 0],
                              [c0[0] + 4.5 * s, c0[1] + 4.5 * s - 3 * k * s, 0], color=GREY_B, stroke_width=2.5)
                         for k in range(4)])
        short = [r"newspaper, \ easy", r"AI Escargot \ (2006)", r"Inkala \ (2012)"]
        rows = [[nm, str(r["givens"]), f"{r['naive_nodes']:,}", f"{r['dlx_nodes']:,}",
                 f"{r['dlx_s'] * 1000:.0f} ms"] for nm, r in zip(short, d["sudoku"])]
        tab = grid_table([r"puzzle", r"givens", r"nodes, \ in order", r"nodes, \ DLX", r"DLX"], rows,
                         widths=[2.6, 1.0, 1.7, 1.4, 1.1], row_h=0.5, font_size=18, mono_cols=(),
                         colors=[[GREY_A, WHITE, NO, YES, LAM]] * 3).to_edge(RIGHT, buff=0.3).shift(UP * 1.2)
        pts = VGroup(
            label(r"fewest options first is most of the gain: \\ hard puzzles force guesses, \ and DLX guesses well",
                  font_size=19, color=HEAD),
            label(r"the same engine tiles pentominoes; \\ generalized Sudoku is NP-complete \ (Part 26)",
                  font_size=19, color=GREY_A),
            label(r"branch and bound adds an optimistic estimate, \\ and prunes what cannot win \ (Part 23)",
                  font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(tab, DOWN, buff=0.45).align_to(tab, LEFT)
        with self.voiceover(
            "Here is Arto Inkala's puzzle of 2012, often called the hardest Sudoku, with twenty-one givens, solved. "
            "<bookmark mark='a'/> Plain backtracking, filling cells in reading order, needed fifty thousand "
            "search nodes on it. Dancing links, always branching on the most constrained choice, needed under "
            "three thousand, and seventy milliseconds. <bookmark mark='b'/> Most of the gain is the choice of "
            "what to branch on: fewest options first. <bookmark mark='c'/> The same engine tiles boards with "
            "pentominoes and solves scheduling puzzles, and Part 26 shows that Sudoku on larger boards is "
            "NP-complete, so nothing fundamentally better than clever search is expected. <bookmark mark='d'/> When the goal is "
            "the best solution rather than any, branch and bound adds an optimistic estimate to each node and "
            "prunes what cannot win, the method of Part 23's integer programs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(thick), FadeIn(given))
            self.play(LaggedStart(*[FadeIn(f) for f in filled], lag_ratio=0.03), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(tab))
            for mk, p in zip("bcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
