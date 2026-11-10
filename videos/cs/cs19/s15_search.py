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
            label('partial nodes versus complete assignments; observed counts do not prove a growth law', font_size=21, color=NO),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "These counts enumerate all solutions, rather than stopping at the first. <bookmark mark='a'/> For eight "
            'queens the search visits two thousand and fifty-seven partial-placement nodes, including the root. The '
            'comparison n to the n counts complete row-by-row assignments, so the two columns count different '
            "objects. <bookmark mark='b'/> Pruning removes invalid branches but does not prove a polynomial worst-"
            'case algorithm. The table reports the actual node counts and elapsed times through fourteen queens, with'
            ' solution totals checked against known values. A bitmask makes each safe-column operation cheap; it does'
            ' not turn an exponential search tree into a linear one.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
        self.wait(0.3)
        self.clear_scene()

    def cover(self):
        head=label("Exact cover and reversible links",font_size=34).to_edge(UP,buff=.3)
        pts=[
            label("choose rows: exactly one 1 in every constraint column",font_size=22,color=HEAD).move_to([0,2.55,0]),
            label("Sudoku before givens: 729 candidate rows, 324 constraints",font_size=21,color=GREY_A).move_to([0,1.98,0]),
            label("Algorithm X: fewest-options column; try a row; remove conflicts; recurse",font_size=21,color=GREY_A).move_to([0,1.4,0]),
            label("unlink x; retain its own links",font_size=21,color=YES).move_to([3.15,.45,0]),
            MathTex(r"L[R[x]]\gets x,\quad R[L[x]]\gets x",font_size=24,color=LAM).move_to([3.15,-2.45,0]),
            label("undo in reverse order, including early-stop returns",font_size=21,color=HEAD).to_edge(DOWN,buff=.28),
        ]
        tab=grid_table(["row","A","B","C"],[["r0","1","0","0"],["r1","0","1","1"],["r2","1","1","0"],["r3","0","0","1"]],
                       widths=[1.0,.72,.72,.72],row_h=.45,font_size=20,mono_cols=()).move_to([-3.5,-.7,0])
        cover=VGroup(*[SurroundingRectangle(VGroup(*tab.cells[i]),buff=.06,color=YES,stroke_width=2) for i in (1,2)])
        cover_note=label("r0 + r1: each column covered once",font_size=18,color=YES).next_to(tab,DOWN,buff=.3)
        y=-.9
        a=VGroup(Square(.55,color=DATA),mono("a",18,WHITE)).move_to([1,y,0])
        x=VGroup(Square(.55,color=HEAD),mono("x",18,WHITE)).move_to([3.15,y,0])
        b=VGroup(Square(.55,color=DATA),mono("b",18,WHITE)).move_to([5.3,y,0])
        links=VGroup(*[Arrow(u.get_right()+UP*.11,v.get_left()+UP*.11,buff=.06,color=GREY_B,stroke_width=2) for u,v in ((a,x),(x,b))],
                     *[Arrow(v.get_left()+DOWN*.11,u.get_right()+DOWN*.11,buff=.06,color=GREY_B,stroke_width=2) for u,v in ((a,x),(x,b))])
        bypass=VGroup(CurvedArrow(a.get_top(),b.get_top(),angle=-.55,color=YES,stroke_width=2,tip_length=.13),
                      CurvedArrow(b.get_bottom(),a.get_bottom(),angle=-.55,color=LAM,stroke_width=2,tip_length=.13))
        unlink=MathTex(r"L[R[x]]\gets L[x],\quad R[L[x]]\gets R[x]",font_size=22,color=YES).move_to([3.15,-1.8,0])
        with self.voiceover(
            "Exact cover chooses rows so every constraint column is covered exactly once. <bookmark mark='a'/> The "
            "small binary matrix makes that condition visible. <bookmark mark='b'/> Sudoku has up to seven hundred "
            'and twenty-nine candidate cell-digit rows and three hundred and twenty-four constraints, before givens '
            "filter candidates. <bookmark mark='c'/> Algorithm X chooses a column with fewest remaining options, "
            "tries a row and temporarily removes conflicts. <bookmark mark='d'/> Dancing Links unlinks a node by "
            "reconnecting its neighbors while retaining its own links. <bookmark mark='e'/> Restore in reverse order,"
            " and the original structure returns. <bookmark mark='f'/> Our solver now restores links even when a "
            'solution limit stops search early, so the same object can be solved again. Its update counter includes '
            'both cover and uncover pointer writes, excluding construction.'
        ) as vo:
            self.play(FadeIn(head),FadeIn(tab),FadeIn(a),FadeIn(x),FadeIn(b),Create(links))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]),Create(cover),FadeIn(cover_note))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]),FadeIn(unlink),Create(bypass),FadeOut(links),x.animate.shift(DOWN*.5).set_opacity(.4))
            vo.wait_until("e")
            self.play(FadeIn(pts[4]),FadeOut(bypass),FadeIn(links),x.animate.shift(UP*.5).set_opacity(1))
            vo.wait_until("f")
            self.play(FadeIn(pts[5]))
        self.wait(.3)
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
            label('naive: first solution; DLX: exhaustion or two solutions \\\\ node definitions and stopping rules differ',
                  font_size=19, color=HEAD),
            label(r"the same engine tiles pentominoes; \\ generalized Sudoku is NP-complete \ (Part 26)",
                  font_size=19, color=GREY_A),
            label(r"branch and bound adds an optimistic estimate, \\ and prunes what cannot win \ (Part 23)",
                  font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(tab, DOWN, buff=0.45).align_to(tab, LEFT)
        with self.voiceover(
            "Here are three fixed Sudoku instances, including Inkala's 2012 puzzle with twenty-one givens. <bookmark "
            "mark='a'/> The two solvers' node counts refer to their own search procedures. Naive search stops at its "
            'first solution; Dancing Links searches until exhaustion or two solutions, allowing a uniqueness check. '
            "Both outputs satisfy every given, row, column and box. <bookmark mark='b'/> Fewest-options branching is "
            'a major part of the difference; the benchmark does not isolate it from representation and '
            "implementation. <bookmark mark='c'/> A count of one after exhaustive termination certifies uniqueness; a"
            ' count capped at two means at least two, not an exact total. Generalized Sudoku hardness does not '
            "establish a worst-case bound from these three examples. <bookmark mark='d'/> Optimization search can add"
            ' bounds to discard branches that cannot improve the incumbent, the subject of Part twenty-three.'
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
