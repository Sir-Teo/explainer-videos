from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs21.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Align(VoiceoverScene):
    def construct(self):
        self.card()
        self.global_()
        self.local()
        self.scale()

    def card(self):
        card = chapter_card(12, r"Alignment", r"How do you line up two texts that almost agree?", lit=(1970, 1981),
                            extra=((1970, r"Needleman--Wunsch"), (1981, r"Smith--Waterman")), part=PART)
        with self.voiceover("Chapter twelve. Alignment."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def global_(self):
        d = load("align")
        a, b = d["nw_a"], d["nw_b"]
        S = d["nw"]
        head = label(r"Global alignment: \ Part 19's edit distance, \ with scores", font_size=32).to_edge(UP, buff=0.3)
        cw = 0.48
        grid = VGroup()
        for i in range(len(a) + 1):
            for j in range(len(b) + 1):
                v = S[i][j]
                col = YES if v > -2 else (GREY_A if v > -5 else GREY_D)
                grid.add(mono(str(v), 14, col).move_to([-5.6 + j * cw, 1.8 - i * 0.42, 0]))
        top = VGroup(*[mono(c, 16, DATA).move_to([-5.6 + (j + 1) * cw, 2.25, 0]) for j, c in enumerate(b)])
        left = VGroup(*[mono(c, 16, LAM).move_to([-6.1, 1.8 - (i + 1) * 0.42, 0]) for i, c in enumerate(a)])
        side = VGroup(
            label(r"Needleman and Wunsch (1970): \ score every pair of prefixes", font_size=21, color=WHITE),
            MathTex(r"S(i, j) = \max \begin{cases} S(i-1, j-1) + s(a_i, b_j) \\ S(i-1, j) - g \\ S(i, j-1) - g "
                    r"\end{cases}", font_size=30, color=LAM),
            label(r"match $+1$, \ mismatch $-1$, \ gap $-1$", font_size=20, color=GREY_A),
            label(rf"\texttt{{{a}}} against \texttt{{{b}}}: \ score {d['nw_score']}", font_size=21, color=YES),
            label(r"biology scores with substitution matrices \ (PAM, \ BLOSUM) \ and \textbf{affine gaps}: \ "
                  r"opening a gap costs more than extending it \ (Gotoh, \ 1982)", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        if side.width > 6.6:
            side.width = 6.6
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Part 19's edit distance becomes, in biology, an alignment. <bookmark mark='a'/> Saul Needleman and "
            "Christian Wunsch, in 1970, filled the same table, but with scores to maximize: a reward for matching "
            "letters, penalties for mismatches and gaps. <bookmark mark='b'/> Each cell is the best of three: "
            "extend the alignment by a pair, or by a gap on either side. <bookmark mark='c'/> Here intention "
            "against execution, the example of Part 19. <bookmark mark='d'/> Real biology scores amino acids with "
            "substitution matrices learned from evolution, and charges more to open a gap than to extend one, "
            "because one long insertion is likelier than many short ones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(left))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.005), FadeIn(side[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), Indicate(grid[-1], color=YES))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    def local(self):
        d = load("align")
        head = label(r"Local alignment: \ the best matching \textit{part}", font_size=32).to_edge(UP, buff=0.3)
        lines = VGroup(
            label(r"Smith and Waterman (1981): \ add a fourth choice, \ $0$: \ start afresh anywhere", font_size=21,
                  color=WHITE),
            MathTex(r"H(i, j) = \max\{\,0,\ H(i-1, j-1) + s(a_i, b_j),\ H(i-1, j) - g,\ H(i, j-1) - g\,\}",
                    font_size=30, color=LAM),
            label(r"the answer is the best cell anywhere, \ traced back to its first nonzero", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.35)
        xa = d["sw_x_part"][:150].replace("\n", " ")
        ya = d["sw_y_part"][:150].replace("\n", " ")
        A = label(r"\textit{" + _esc(xa) + r"}", font_size=18, color=DATA)
        B = label(r"\textit{" + _esc(ya) + r"}", font_size=18, color=YES)
        for t in (A, B):
            if t.width > 12.8:
                t.width = 12.8
        VGroup(A, B).arrange(DOWN, buff=0.3).next_to(lines, DOWN, buff=0.45)
        cap = label(rf"the anonymous letter in \textit{{The Count of Monte Cristo}}, \ two of its versions: \ "
                    rf"{words(d['cells'])} cells, \ best score {d['sw_best']}", font_size=20, color=HEAD
                    ).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Often only part of two texts is related. <bookmark mark='a'/> Temple Smith and Michael Waterman added "
            "a fourth choice to every cell: zero, meaning start a fresh alignment here. <bookmark mark='b'/> The "
            "best local alignment is the highest cell anywhere in the table, traced back until the score drops to "
            "zero. <bookmark mark='c'/> Here are the two versions of the anonymous letter from The Count of Monte "
            "Cristo that Part 20's MinHash flagged. Smith–Waterman finds the stretch they share and lines it up, "
            "word for word, around the places where the second version was reworded."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(FadeIn(lines[2]))
            vo.wait_until("c")
            self.play(FadeIn(A), FadeIn(B), FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    def scale(self):
        head = label(r"Alignment at genome scale", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"a quadratic table is $10^{18}$ cells for two human genomes", font_size=22, color=NO),
            label(r"BLAST \ (Altschul et al., 1990): \ find short exact seeds with a hash table, \ extend only "
                  r"around them", font_size=22, color=DATA),
            label(r"read aligners: \ seeds from the FM-index of chapter 9, \ then banded dynamic programming",
                  font_size=22, color=LAM),
            label(r"exact edit distance in $O(n^{2 - \varepsilon})$ would refute SETH \ (Backurs and Indyk, 2015; \ "
                  r"Part 27)", font_size=22, color=HEAD),
            label(r"so in practice: \ heuristics with guarantees for similar strings, \ $O(nd)$ when the distance "
                  r"$d$ is small", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "The table is quadratic, and genomes are long. <bookmark mark='a'/> Two human genomes would need ten to "
            "the eighteen cells. <bookmark mark='b'/> BLAST, from 1990, one of the most cited papers in all of science, "
            "finds short exact seeds with a hash table and extends alignments only around them. <bookmark "
            "mark='c'/> Modern read aligners find their seeds with the FM-index of chapter nine. <bookmark "
            "mark='d'/> And there is a reason to settle for heuristics: an exact edit-distance algorithm in truly "
            "subquadratic time would refute the strong exponential time hypothesis, Part 19's frontier and Part "
            "27's subject. <bookmark mark='e'/> What we can do is exploit similarity: when the distance d is small, "
            "only a band of the table matters, and the work is n times d. The next chapter does exactly that."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()


def _esc(t):
    for a, b in (("\\", ""), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", ""), ("}", ""),
                 ("~", ""), ("^", ""), ('"', "")):
        t = t.replace(a, b)
    return t
