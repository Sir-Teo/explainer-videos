from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs21.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Kmp(VoiceoverScene):
    def construct(self):
        self.card()
        self.borders()
        self.automaton()
        self.amortized()

    def card(self):
        card = chapter_card(3, r"Knuth, \ Morris and Pratt: \ never look back", r"What does a mismatch teach us?",
                            lit=(1977,), extra=((1977, r"Knuth--Morris--Pratt"),), part=PART)
        with self.voiceover('Chapter three. Knuth, Morris and Pratt: never look back.'):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def borders(self):
        d = load("kmp")
        head = label(r"What a mismatch tells you", font_size=34).to_edge(UP, buff=0.35)
        pat = d["pattern"]
        fail = d["fails"][pat]
        cells = VGroup(*[VGroup(Square(side_length=0.6, stroke_color=DATA, stroke_width=1.5),
                                mono(c, 26, WHITE)) for c in pat]).arrange(RIGHT, buff=0)
        for c in cells:
            c[1].move_to(c[0])
        cells.next_to(head, DOWN, buff=0.6)
        idx = VGroup(*[mono(str(j), 16, GREY_B).next_to(c, UP, buff=0.08) for j, c in enumerate(cells)])
        fl = VGroup(*[mono(str(f), 22, YES).next_to(c, DOWN, buff=0.15) for f, c in zip(fail, cells)])
        flab = label(r"fail$[j]$", font_size=20, color=YES).next_to(fl, LEFT, buff=0.3)
        lines = VGroup(
            label(r"suppose $j$ characters matched and the next one fails", font_size=22, color=WHITE),
            label(r"the text's last $j$ characters \textbf{are} the pattern's first $j$: \ we already know them",
                  font_size=22, color=WHITE),
            label(r"fail$[j]$: \ the longest proper prefix of $p_1 \dots p_j$ that is also a suffix of it \ (a "
                  r"\textbf{border})", font_size=22, color=YES),
            label(r"shift the pattern so that border lines up, \ and continue from there: \ the text pointer never "
                  r"moves back", font_size=22, color=HEAD),
            label(r"for \texttt{ababa}: \ the border \texttt{aba}, \ so fail $= 3$", font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.24).to_edge(DOWN, buff=0.4)
        txt = "ababab" + pat[4:]

        def row(w, col):
            g = VGroup(*[VGroup(Square(side_length=0.5, stroke_color=col, stroke_width=1.5), mono(c, 22, WHITE))
                         for c in w]).arrange(RIGHT, buff=0)
            for c in g:
                c[1].move_to(c[0])
            return g
        T = row(txt, GREY_B).move_to(UP * 0.85)
        Pp = row(pat, DATA).next_to(T, DOWN, buff=0.12).align_to(T, LEFT)
        tl = label(r"text", font_size=18, color=GREY_B).next_to(T, LEFT, buff=0.25)
        pl = label(r"pattern", font_size=18, color=DATA).next_to(Pp, LEFT, buff=0.25)
        ptr = Arrow(T[5].get_top() + UP * 0.45, T[5].get_top(), buff=0.02, color=HEAD, stroke_width=3,
                    max_tip_length_to_length_ratio=0.35)
        with self.voiceover(
            "Suppose j characters of the pattern have matched, and the next one fails. <bookmark mark='a'/> The "
            "naive method slides one place and re-reads text it has already seen. But those j characters of text "
            "are exactly the first j characters of the pattern, so we know them without looking. <bookmark "
            "mark='b'/> The only useful question is how far the pattern can shift so that what we have seen still "
            "matches. The answer is the longest proper prefix of those j characters that is also a suffix of them, "
            "called a border. <bookmark mark='c'/> Shift the pattern so the border lines up, and carry on comparing "
            "from the same text position. The text is read once, left to right, and never backed up. <bookmark "
            "mark='d'/> For the pattern a b a b a c a, after a b a b a the border is a b a, so we continue as if "
            "three characters had matched. The table is computed from the pattern alone, in linear time, by running "
            "the same idea on the pattern against itself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(idx))
            self.play(FadeIn(lines[0]), FadeIn(T), FadeIn(Pp), FadeIn(tl), FadeIn(pl), FadeIn(ptr))
            self.play(*[T[k][0].animate.set_fill(YES, 0.35) for k in range(5)],
                      *[Pp[k][0].animate.set_fill(YES, 0.35) for k in range(5)],
                      T[5][0].animate.set_fill(NO, 0.5), Pp[5][0].animate.set_fill(NO, 0.5))
            vo.wait_until("a")
            self.play(FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(FadeIn(lines[2]), FadeIn(fl), FadeIn(flab))
            self.play(*[T[k][0].animate.set_fill(LAM, 0.5) for k in (2, 3, 4)],
                      *[Pp[k][0].animate.set_fill(LAM, 0.5) for k in (0, 1, 2)])
            vo.wait_until("c")
            self.play(FadeIn(lines[3]))
            self.play(*[Pp[k][0].animate.set_fill(BLACK, 0) for k in range(3, 7)], run_time=0.5)
            self.play(Pp.animate.shift(RIGHT * 1.0), pl.animate.shift(RIGHT * 1.0), run_time=1.5)
            self.play(Indicate(ptr, color=HEAD), T[5][0].animate.set_fill(YES, 0.35),
                      Pp[3][0].animate.set_fill(YES, 0.35))
            vo.wait_until("d")
            self.play(FadeIn(lines[4]), Indicate(fl[4], color=LAM))
        self.wait(0.3)
        self.clear_scene()

    def automaton(self):
        d = load("kmp")
        pat = d["pattern"]
        auto = d["auto"]
        head = label(r"The same idea as an automaton \ (Part 12)", font_size=34).to_edge(UP, buff=0.35)
        m = len(pat)
        xs = np.linspace(-5.6, 5.6, m + 1)
        y = 0.6
        nodes = VGroup()
        for q in range(m + 1):
            c = Circle(radius=0.34, color=YES if q == m else DATA, stroke_width=2.5)
            if q == m:
                c = VGroup(c, Circle(radius=0.27, color=YES, stroke_width=2))
            nodes.add(VGroup(c, mono(str(q), 20, WHITE)).move_to([xs[q], y, 0]))
        fwd = VGroup()
        for q in range(m):
            a = Arrow([xs[q] + 0.34, y, 0], [xs[q + 1] - 0.34, y, 0], buff=0.02, stroke_width=2.5, color=DATA,
                      max_tip_length_to_length_ratio=0.2)
            fwd.add(VGroup(a, mono(pat[q], 18, DATA).next_to(a, UP, buff=0.05)))
        back = VGroup()
        for q in range(m + 1):
            for ci, ch in enumerate("abc"):
                t = auto[q][ci]
                if t == q + 1 or t == 0:
                    continue
                start, end = np.array([xs[q], y - 0.34, 0]), np.array([xs[t], y - 0.34, 0])
                if t == q:
                    continue
                arc = ArcBetweenPoints(start, end, angle=-0.9 if t < q else 0.9, color=HEAD, stroke_width=1.8)
                arc.add_tip(tip_length=0.12)
                back.add(VGroup(arc, mono(ch, 15, HEAD).move_to(arc.point_from_proportion(0.5) + DOWN * 0.15)))
        note_ = label(r"every other transition goes back to state 0", font_size=19, color=GREY_B).next_to(nodes, UP,
                                                                                                buff=0.6)
        text = d["trace_text"]
        tr = d["trace"]
        tcells = VGroup(*[VGroup(Square(side_length=0.42, stroke_color=GREY_C, stroke_width=1),
                                 mono(c, 18, WHITE)) for c in text]).arrange(RIGHT, buff=0).to_edge(DOWN, buff=1.0)
        for c in tcells:
            c[1].move_to(c[0])
        states = VGroup(*[mono(str(s), 16, YES).next_to(c, DOWN, buff=0.1) for s, c in zip(tr, tcells)])
        tok = Dot(nodes[0].get_center(), radius=0.12, color=HEAD)
        with self.voiceover(
            "The failure table is really a finite automaton, the kind Part 12 built from regular expressions. "
            "<bookmark mark='a'/> State q means: the last q characters read match the first q of the pattern. "
            "Each matching character moves one state right. <bookmark mark='b'/> A mismatch follows the border "
            "back: from state five, a b means the last characters read are a b a b, state four. Every other "
            "transition returns to the start. <bookmark mark='c'/> Now feed it text, one character at a time, "
            "with no backtracking at all. When it reaches state seven, the pattern has just ended."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nodes), FadeIn(fwd))
            vo.wait_until("a")
            self.play(Indicate(nodes[3], color=DATA))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(b) for b in back], lag_ratio=0.2), FadeIn(note_))
            vo.wait_until("c")
            self.play(FadeIn(tcells), FadeIn(tok))
            for k, s in enumerate(tr):
                self.play(tok.animate.move_to(nodes[s].get_center()), FadeIn(states[k]),
                          tcells[k][0].animate.set_fill(HEAD, 0.3), run_time=0.35)
            self.play(Flash(nodes[m], color=YES))
        self.wait(0.3)
        self.clear_scene()

    def amortized(self):
        d = load("kmp")
        head = label(r"Never more than $2n$ comparisons", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"each comparison either matches, \ and the text pointer $i$ advances, \ or fails, \ and the "
                  r"pattern shifts right", font_size=22, color=WHITE),
            label(r"$i$ advances at most $n$ times; \ the pattern's start $i - j$ also moves right at most $n$ times",
                  font_size=22, color=WHITE),
            MathTex(r"\text{comparisons} \le 2n \qquad \text{(and } O(m) \text{ to build the table)}", font_size=36,
                    color=YES),
            label(rf"the worst case of chapter 1: \ $a^{{{d['worst_n']}}}$ against $a^{{99}}b$: \ "
                  rf"{words(d['worst_cmp'])} comparisons, \ not ten million", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        rows = [[r["pattern"], words(r["cmp"]), f"{r['per_char']:.3f}"] for r in d["rows"]]
        tab = grid_table([r"pattern, \ on the corpus", r"comparisons", r"per character"], rows,
                         widths=[4.0, 3.2, 2.6], row_h=0.42, font_size=20, mono_cols=(0,),
                         colors=[[DATA, GREY_A, YES]] * len(rows)).to_edge(DOWN, buff=0.45)
        tab.set_x(0)
        with self.voiceover(
            "How much work is that? <bookmark mark='a'/> Every comparison either matches, and the text position "
            "moves right, or fails, and the pattern's starting position moves right. <bookmark mark='b'/> Each "
            "of those can move right at most n times, <bookmark mark='c'/> so there are at most two n comparisons "
            "in all, plus linear work to build the table. This is an amortized argument, like Part 16's doubling "
            "arrays: a single character can cost several comparisons, but never many on average. <bookmark "
            "mark='d'/> Chapter one's worst case, which cost the naive method ten million comparisons, costs "
            f"{words(d['worst_cmp'])}. <bookmark mark='e'/> On the novels, Knuth–Morris–Pratt is no faster than "
            "naive search; it is never slower, whatever the text."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()
