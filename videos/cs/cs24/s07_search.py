from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, cells_row, grid_table, load, mono, words)


class Searching(VoiceoverScene):
    def construct(self):
        self.card()
        self.answer()
        self.pitfalls()
        self.gallop()

    def card(self):
        card = chapter_card(6, r"Searching for the answer", r"When can you binary-search something that isn't an array?",
                            lit=(1946, 1976), extra=((1946, r"Mauchly's binary search"), (1976, r"Bentley--Yao")),
                            part=PART)
        with self.voiceover("Chapter six. Searching for the answer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def answer(self):
        d = load("search")
        w, days = d["w"], d["days"]
        head = label(r"Binary search on the answer", font_size=34).to_edge(UP, buff=0.3)
        pk = cells_row(w, w=0.6, h=0.55, font=20, labels=False).next_to(head, DOWN, buff=0.45)
        pkl = label(rf"packages, \ shipped in order, \ within {days} days", font_size=20, color=GREY_A).next_to(pk, DOWN,
                                                                                                         buff=0.15)
        pred = d["pred"]
        cw = 0.27
        strip = VGroup(*[Rectangle(width=cw, height=0.42, stroke_width=0.6, stroke_color=GREY_D)
                         .set_fill(YES if p["ok"] else NO, 0.65) for p in pred]).arrange(RIGHT, buff=0)
        strip.next_to(pkl, DOWN, buff=0.6)
        ends = VGroup(mono(str(pred[0]["cap"]), 16, GREY_A).next_to(strip, LEFT, buff=0.15),
                      mono(str(pred[-1]["cap"]), 16, GREY_A).next_to(strip, RIGHT, buff=0.15))
        sl = label(r"each capacity: \ red if it fails, \ green if it works", font_size=20, color=GREY_A).next_to(
            strip, UP, buff=0.3)
        probes = VGroup()
        for c, ok in d["trace"]:
            i = c - pred[0]["cap"]
            probes.add(Triangle(color=WHITE, fill_opacity=1).scale(0.09).rotate(PI).next_to(strip[i], UP, buff=0.03))
        notes = VGroup(
            label(r"the question ``can capacity $c$ do it?'' \ is \textbf{monotone}: \ false, \ \ldots, \ false, \ true, "
                  r"\ \ldots, \ true", font_size=21, color=WHITE),
            label(rf"binary-search the boundary: \ {d['calls']} checks, \ each a greedy $O(n)$ pass: \ capacity "
                  rf"{d['cap']}", font_size=21, color=YES),
            label(r"the pattern: \ minimize the largest load, \ maximize the smallest gap, \ the earliest day that "
                  r"works", font_size=21, color=LAM),
            label(r"Knuth: \ binary search was published in 1946; \ the first version correct for every $n$, \ in 1960",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Binary search works on a monotone predicate, not just a sorted array. <bookmark mark='a'/> These "
            "nonnegative package weights must be shipped in order within four days. <bookmark mark='b'/> A "
            'greedy feasibility check fills each day until the next package would exceed capacity. Larger '
            "capacities remain feasible. <bookmark mark='c'/> Search between the largest weight and the total "
            'weight. The routine first checks that the upper bound is feasible, and counts that actual predicate '
            "call along with the search calls. The minimum capacity is eighteen. <bookmark mark='d'/> State the "
            'monotonicity and feasible-endpoint contract before applying this pattern to other problems. '
            "<bookmark mark='e'/> The displayed lower-bound implementation has a separate half-open interval "
            'invariant. Tests cover empty arrays and boundary answers; finite tests support the implementation '
            'while the invariant explains its correctness.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(pk))
            vo.wait_until("a")
            self.play(FadeIn(pkl))
            vo.wait_until("b")
            self.play(FadeIn(strip), FadeIn(ends), FadeIn(sl), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.1) for p in probes], lag_ratio=0.5), FadeIn(notes[1]),
                      run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def pitfalls(self):
        head = label(r"Getting binary search right", font_size=34).to_edge(UP, buff=0.35)
        code_ = VGroup(*[mono(t, 21, c) for t, c in (
            ("lo, hi = 0, n          # search elements in [lo, hi)", WHITE),
            ("while lo < hi:", WHITE),
            ("    mid = lo + (hi - lo) // 2", YES),
            ("    if a[mid] < x: lo = mid + 1", WHITE),
            ("    else:          hi = mid", WHITE),
            ("return lo             # first i with a[i] >= x, or n", WHITE))]).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.08)
        code_.next_to(head, DOWN, buff=0.45)
        notes = VGroup(
            label(r"\textbf{the invariant}: \ everything left of \texttt{lo} is $< x$, \ everything from \texttt{hi} on "
                  r"is $\ge x$; \ the gap shrinks every step", font_size=21, color=YES),
            label(r"half-open ranges $[lo, hi)$: \ no $\pm 1$ guesswork, \ and an empty range is $lo = hi$", font_size=21,
                  color=DATA),
            label(r"\texttt{(lo + hi) / 2} overflows once arrays pass $2^{30}$ elements: \ the bug Bloch found in Java's "
                  r"library \ (2006), \ there for nine years", font_size=21, color=NO),
            label(r"return the \textbf{boundary}, \ not ``found'': \ lower and upper bounds answer more questions",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.22).next_to(code_, DOWN, buff=0.45)
        with self.voiceover(
            "Binary search is famous for being easy to get wrong, so here is a version to trust. <bookmark "
            "mark='a'/> Keep an invariant: everything to the left of lo is smaller than x, and everything from hi "
            "onwards is at least x. Each step shrinks the gap between them, and when it closes, lo is the answer. "
            "<bookmark mark='b'/> Use half-open ranges, from lo up to but not including hi, and the plus-or-minus-one "
            "guesswork disappears: the empty range is simply lo equal to hi. <bookmark mark='c'/> Compute the middle "
            "as lo plus half the difference. Adding lo and hi first overflows a 32-bit integer once an array has a "
            "billion elements, a bug Joshua Bloch found in 2006 in Java's own library, where it had sat for nine "
            "years. <bookmark mark='d'/> And return the boundary, the first position not less than x, rather than "
            "just found or not found. Lower and upper bounds answer counting and range questions too."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code_))
            for mk, n_ in zip("abcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def gallop(self):
        d = load("search")
        head = label(r"Galloping: \ search near where you are", font_size=34).to_edge(UP, buff=0.3)
        rows = [[words(r["d"]), str(r["gallop"]), str(r["binary"])] for r in d["gallop"]]
        tab = grid_table([r"answer $d$ places away", r"galloping probes", r"binary search probes"], rows,
                         widths=[3.2, 2.6, 3.0], row_h=0.38, font_size=20, mono_cols=(),
                         colors=[[WHITE, YES, GREY_A]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.5)
        notes = VGroup(
            label(r"probe $1, 2, 4, 8, \ldots$ places ahead \\ until you pass the target, \\ then binary-search the "
                  r"last gap", font_size=21, color=WHITE),
            label(r"$O(1+\log(d+1))$ reads for distance $d$: \\ Bentley and Yao (1976)", font_size=21, color=YES),
            label(r"the measured crossover depends on \\ the exact loops and target", font_size=21, color=HEAD),
            label(r"used where searches are local: \\ merging sorted runs \ (Timsort), \\ intersecting posting lists \ "
                  r"(Part 47)", font_size=21, color=LAM),
            label(r"\textbf{ternary search}: \ for the peak of a \\ unimodal function, \ discard a third each step",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(tab, RIGHT, buff=0.5).align_to(tab, UP)
        room = 7.0 - notes.get_left()[0]
        if notes.width > room:
            notes.width = room
            notes.next_to(tab, RIGHT, buff=0.5).align_to(tab, UP)
        with self.voiceover(
            "Sometimes you know roughly where the answer is. <bookmark mark='a'/> Galloping probes exponentially "
            'increasing distances, then binary-searches the bracket. This routine searches a sorted suffix '
            'starting at the supplied index. To obtain the global lower bound, all preceding elements must be '
            "smaller than the target. <bookmark mark='b'/> Work is logarithmic in the distance plus one. The "
            'table counts actual key reads for both methods, including bound construction, instead of '
            "substituting a logarithmic estimate. <bookmark mark='c'/> Close answers can need fewer reads; the "
            "crossover depends on the exact search loops and target. <bookmark mark='d'/> Merging sorted runs "
            "and intersecting posting lists often provide a useful starting position. <bookmark mark='e'/> "
            'Ternary search is a separate pattern for a unimodal objective on a valid finite interval; an '
            'arbitrary function need not satisfy that premise.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.15))
            for mk, n_ in zip("abcde", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
