from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs21.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)

CW = 0.42


def cells(s, color=GREY_B, y=0.0, x0=None, font=22):
    g = VGroup()
    for i, ch in enumerate(s):
        sq = Square(side_length=CW, stroke_color=color, stroke_width=1.2)
        g.add(VGroup(sq, mono(ch, font, WHITE).move_to(sq)))
    g.arrange(RIGHT, buff=0)
    if x0 is not None:
        g.move_to([x0 + g.width / 2, y, 0])
    else:
        g.move_to([0, y, 0])
    return g


class Naive(VoiceoverScene):
    def construct(self):
        self.card()
        self.slide()
        self.worst()

    def card(self):
        card = chapter_card(1, r"Matching, \ the obvious way", r"How much work is it to find a word?", part=PART)
        with self.voiceover("Chapter one. Matching, the obvious way."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def slide(self):
        d = load("naive")
        head = label(r"Slide the pattern along the text", font_size=34).to_edge(UP, buff=0.35)
        text = "abracadabracabra"
        pat = "abrac"
        T = cells(text, GREY_B, y=1.6)
        x0 = T[0].get_left()[0]
        P = cells(pat, DATA, y=0.9, x0=x0)
        cnt = label(r"comparisons: \ 0", font_size=24, color=HEAD).next_to(T, UP, buff=0.35)
        total = 0
        with self.voiceover(
            "Put the pattern under the text at the first position and compare left to right until a character "
            "differs. Then slide one place and start again. <bookmark mark='a'/> At most positions the first "
            "character already fails, so the work is close to one comparison per character of text. When the "
            "pattern does match, as at positions zero and seven here, we pay its whole length."
        ) as vo:
            self.play(FadeIn(head), FadeIn(T), FadeIn(P), FadeIn(cnt))
            for i in range(len(text) - len(pat) + 1):
                if i:
                    self.play(P.animate.shift(RIGHT * CW), run_time=0.18)
                j = 0
                marks = []
                while j < len(pat):
                    total += 1
                    ok = text[i + j] == pat[j]
                    marks.append(T[i + j][0].copy().set_fill(YES if ok else NO, 0.45).set_stroke(width=0))
                    if not ok:
                        break
                    j += 1
                new = label(rf"comparisons: \ {total}", font_size=24, color=HEAD).move_to(cnt)
                self.play(*[FadeIn(m) for m in marks], Transform(cnt, new), run_time=0.22)
                self.remove(*marks)
                if i == 1:
                    vo.wait_until("a")
        rows = [[r["pattern"], str(r["m"]), words(r["hits"]), f"{r['per_char']:.3f}"] for r in d["rows"]]
        tab = grid_table([r"pattern", r"$m$", r"found", r"comparisons per character"], rows,
                         widths=[4.4, 0.9, 1.6, 4.2], row_h=0.42, font_size=20, mono_cols=(0,),
                         colors=[[DATA, GREY_A, YES, HEAD]] * len(rows)).to_edge(DOWN, buff=0.4)
        tab.set_x(0)
        with self.voiceover(
            f"On the whole corpus, {words(d['n'])} characters, the naive method costs very little more than one "
            "comparison per character for every pattern we tried. English text is kind to it: most positions fail "
            "at once, and even common words like the cost under one point one."
        ):
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.25))
        self.wait(0.3)
        self.clear_scene()

    def worst(self):
        d = load("naive")
        head = label(r"But not every text is English", font_size=34).to_edge(UP, buff=0.35)
        T = cells("aaaaaaaaaaaaaa", GREY_B, y=1.4)
        P = cells("aaaab", NO, y=0.7, x0=T[0].get_left()[0])
        rows = [[words(r["n"]), words(r["m"]), words(r["cmp"]), words(r["nm"])] for r in d["worst"]]
        tab = grid_table([r"text $a^n$, \ $n$", r"pattern $a^{m-1}b$, \ $m$", r"comparisons", r"$(n - m + 1)\,m$"],
                         rows, widths=[2.8, 3.4, 2.6, 2.6], row_h=0.42, font_size=20, mono_cols=(),
                         colors=[[GREY_A, GREY_A, NO, HEAD]] * len(rows)).next_to(P, DOWN, buff=0.6)
        tab.set_x(0)
        note_ = label(r"each alignment matches $m - 1$ characters before failing: \ $\Theta(nm)$; \ DNA, \ binary "
                      r"files and adversaries find this case", font_size=21, color=WHITE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The worst case is easy to build. <bookmark mark='a'/> Search for a run of a's ending in b inside a "
            "text of nothing but a's. Every alignment matches m minus one characters before it fails. <bookmark "
            "mark='b'/> The count is exactly n minus m plus one, times m: a hundred thousand characters and a "
            "thousand-letter pattern take ninety-nine million comparisons. <bookmark mark='c'/> DNA, with its "
            "four letters, binary files, and anyone who wants to slow a server down all find this case. The next "
            "three chapters remove it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(T), FadeIn(P))
            vo.wait_until("a")
            for _ in range(3):
                self.play(P.animate.shift(RIGHT * CW), run_time=0.3)
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.25))
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()
