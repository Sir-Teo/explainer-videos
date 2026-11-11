from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


class Edit(VoiceoverScene):
    def construct(self):
        self.card()
        self.recurrence()
        self.table()
        self.uses()

    def card(self):
        card = chapter_card(10, r"Edit distance", r"How different are two strings?", lit=(1974,),
                            extra=((1965, r"Levenshtein"), (1970, r"Needleman and Wunsch"),
                                   (1974, r"Wagner and Fischer")), part=PART)
        with self.voiceover("Chapter ten. Edit distance."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def recurrence(self):
        head = label(r"Insert, \ delete, \ substitute", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"the fewest single-character edits turning one string into another \ (Levenshtein, \ 1965)",
                  font_size=22, color=GREY_A),
            label(r"subproblem: \ $D(i, j)$, \ the distance between the first $i$ letters of $a$ and the first $j$ "
                  r"of $b$", font_size=22, color=HEAD),
            MathTex(r"D(i, j) = \min \begin{cases} D(i-1, j) + 1 & \text{delete } a_i \\ D(i, j-1) + 1 & "
                    r"\text{insert } b_j \\ D(i-1, j-1) + [a_i \ne b_j] & \text{substitute, or match} \end{cases}",
                    font_size=34, color=YES),
            label(r"the last letters must be dealt with somehow: \ these are the only three ways", font_size=21,
                  color=GREY_A),
            label('$nm$ interior updates; $(n+1)(m+1)$ allocated cells', font_size=23, color=LAM),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.6)
        boundary=MathTex(r"D(i,0)=i,\qquad D(0,j)=j",font_size=27,color=DATA).to_edge(DOWN,buff=.35)
        with self.voiceover(
            "Use unit-cost insertion, deletion and substitution. <bookmark mark='a'/> Levenshtein distance is the "
            "fewest such edits turning one string into the other. <bookmark mark='b'/> State D of i comma j compares "
            'the first i symbols with the first j. The empty-prefix boundaries are D of i comma zero equals i and D '
            "of zero comma j equals j. <bookmark mark='c'/> The final step deletes, inserts, or matches or "
            "substitutes the two last symbols. <bookmark mark='d'/> Take the minimum of the three corresponding "
            "predecessor costs; a match costs zero. <bookmark mark='e'/> There are n times m interior updates and n "
            'plus one times m plus one allocated table cells. These counts distinguish work from boundary storage.'
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
                if mk == "b": self.play(FadeIn(boundary))
        self.wait(0.3)
        self.clear_scene()

    def table(self):
        d = load("edit")
        a, b, D = d["a"], d["b"], d["D"]
        head = label(rf"\texttt{{{a}}} \ $\to$ \ \texttt{{{b}}}", font_size=34).to_edge(UP, buff=0.3)
        cw, ch = 0.52, 0.44
        x0, y0 = -6.0, 2.3
        cells = {}
        grid = VGroup()
        for i in range(len(a) + 1):
            for j in range(len(b) + 1):
                sq = Square(side_length=0.48, stroke_color=GREY_D, stroke_width=1).move_to(
                    [x0 + cw * (j + 1), y0 - ch * (i + 1), 0]).stretch_to_fit_height(0.4)
                num = mono(str(D[i][j]), 15, GREY_A).move_to(sq)
                cells[(i, j)] = VGroup(sq, num)
                grid.add(sq)
        colh = VGroup(*[mono(c, 16, LAM).move_to([x0 + cw * (j + 2), y0, 0]) for j, c in enumerate(b)])
        rowh = VGroup(*[mono(c, 16, DATA).move_to([x0, y0 - ch * (i + 2), 0]) for i, c in enumerate(a)])
        path = d["path"]
        hl = VGroup(*[cells[tuple(p)][0].copy().set_fill(HEAD, 0.35).set_stroke(HEAD, 2) for p in path])
        ops = d["ops"]
        ali = VGroup(
            mono(" ".join(a), 20, DATA),
            mono(" ".join("|" if o == "=" else "*" for o in ops), 20, GREY_B),
            mono(" ".join(b), 20, LAM),
        ).arrange(DOWN, buff=0.12).to_edge(RIGHT, buff=0.8).shift(UP * 0.6)
        side = VGroup(
            label(r"fill row by row: \ each cell needs its left, \ upper and diagonal neighbours", font_size=20,
                  color=GREY_A),
            label(rf"distance {D[-1][-1]}: \ the bottom-right cell", font_size=23, color=YES),
            label(r"walk back from it, \ always to a neighbour that produced its value: \ an optimal edit",
                  font_size=20, color=HEAD),
            label(rf"here: \ {sum(o != '=' for o in ops)} substitutions, \ then four letters kept", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(ali, DOWN, buff=0.5).to_edge(RIGHT, buff=0.4)
        if side.width > 5.4:
            side.scale_to_fit_width(5.4).to_edge(RIGHT, buff=0.4)
        empty = VGroup(MathTex(r"\epsilon",font_size=19,color=LAM).move_to([x0+cw,y0,0]),
                       MathTex(r"\epsilon",font_size=19,color=DATA).move_to([x0,y0-ch,0]))
        i=j=5
        local=VGroup(*[SurroundingRectangle(cells[p],buff=.01,color=c,stroke_width=2) for p,c in
                       [((i-1,j),NO),((i,j-1),DATA),((i-1,j-1),LAM),((i,j),YES)]])
        witness=VGroup(label("one interior update",font_size=19,color=HEAD),
            MathTex(rf"D(5,5)=\min({D[4][5]}+1,\ {D[5][4]}+1,\ {D[4][4]}+1)={D[5][5]}",font_size=23,color=YES)
        ).arrange(DOWN,buff=.13).move_to([3.5,2.0,0])
        with self.voiceover(
            "Here is the table for intention and execution, a classic example. <bookmark mark='a'/> The first row "
            "and column count the cost of building a prefix from nothing. Every other cell takes the minimum of "
            "its three neighbours, so the table fills row by row, each cell ready when it is needed. <bookmark "
            "mark='b'/> The bottom-right corner holds the answer: five. <bookmark mark='c'/> To recover the edits "
            "themselves, walk back from the corner, each time to a neighbour that could have produced the value. "
            "<bookmark mark='d'/> Here the path runs down the diagonal: five substitutions, and the final four "
            "letters, t i o n, kept."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(colh), FadeIn(rowh),FadeIn(empty))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            rows = [VGroup(*[cells[(i, j)][1] for j in range(len(b) + 1)]) for i in range(len(a) + 1)]
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.35), run_time=4)
            self.play(Create(local),FadeIn(witness))
            vo.wait_until("b")
            self.play(FadeOut(local))
            self.play(Indicate(cells[(len(a), len(b))], color=YES), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(h) for h in reversed(hl)], lag_ratio=0.2), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(ali), FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def uses(self):
        d = load("edit")
        head = label(r"Where it runs", font_size=34).to_edge(UP, buff=0.3)
        rows = [[f"{r['n']:,}", f"{r['cells']:,}", f"{r['s'] * 1000:.0f} ms" if r["s"] < 1 else f"{r['s']:.2f} s"]
                for r in d["rows"]]
        tab = grid_table([r"letters each", r"table cells", r"time, \ Python"], rows, widths=[1.9, 2.3, 1.9],
                         row_h=0.46, font_size=20, colors=[[WHITE, GREY_A, NO]] * len(rows)).next_to(
            head, DOWN, buff=0.8).to_edge(LEFT, buff=0.5)
        pts = VGroup(
            label('doubling both lengths quadruples interior updates; timings are observations', font_size=21, color=NO),
            label(rf"LCS: matches and skips, a different objective; \\ "
                  rf"\texttt{{ABCBDAB}}, \ \texttt{{BDCABA}}: \ \texttt{{{d['lcs'][1]}}}, \ length {d['lcs'][0]}",
                  font_size=20, color=GREY_A),
            label('insert/delete scripts connect LCS to file comparison \\\\ production diff also uses heuristics', font_size=20, color=HEAD),
            label(r"biology: \ aligning DNA and proteins \\ (Needleman and Wunsch, \ 1970)", font_size=20,
                  color=YES),
            label(r"spelling correction, \ speech recognition, \\ plagiarism detection", font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        if pts.width > 6.0:
            pts.scale_to_fit_width(6.0).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "These complete edit tables are timed on fixed random DNA strings. <bookmark mark='a'/> Doubling both "
            'lengths quadruples the interior cell count; elapsed times need not scale by exactly four. Every timed '
            'distance and traceback is checked outside the timer against an independent rolling-row reference. '
            "<bookmark mark='b'/> Longest common subsequence uses a related recurrence with matches and skips, rather"
            " than the same unit-substitution objective. <bookmark mark='c'/> Insert-delete scripts connect that "
            'subsequence problem to file comparison; production diff tools use several algorithms and heuristics. '
            "<bookmark mark='d'/> Biological sequence alignment generalizes the scoring, including substitution "
            "scores and gap costs. <bookmark mark='e'/> The later conditional lower bound concerns exact worst-case "
            'distance, not every practical input, approximation or scoring model.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
