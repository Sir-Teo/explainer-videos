from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, cells_row, load, mono)


class Monotone(VoiceoverScene):
    def construct(self):
        self.card()
        self.window()
        self.substring()
        self.stacks()

    def card(self):
        card = chapter_card(5, r"Two pointers and monotonic stacks", r"How can a nested loop run in linear time?",
                            lit=(1977,), extra=((1977, r"Knuth--Morris--Pratt's amortization"),), part=PART)
        with self.voiceover("Chapter five. Two pointers, and monotonic stacks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def window(self):
        d = load("monotone")
        a, k, tr, mx = d["a"], d["k"], d["trace"], d["max"]
        head = label(r"The maximum of every window", font_size=34).to_edge(UP, buff=0.3)
        row = cells_row(a, w=0.66, h=0.58, font=22).move_to(UP * 1.6)
        win = SurroundingRectangle(VGroup(*row.boxes[0:k]), color=HEAD, buff=0.05, stroke_width=3)
        dql = label(r"deque \ (indices, \ values decreasing)", font_size=20, color=LAM).move_to(LEFT * 4.6 + DOWN * 0.1)

        def dq_mob(ix):
            g = VGroup(*[VGroup(Rectangle(width=0.66, height=0.58, stroke_color=LAM, stroke_width=2).set_fill(LAM, 0.2),
                                mono(str(a[i]), 22, WHITE)) for i in ix])
            for b in g:
                b[1].move_to(b[0])
            g.arrange(RIGHT, buff=0.08).next_to(dql, RIGHT, buff=0.4)
            return g
        dq = dq_mob(tr[0])
        outl = label(r"maxima", font_size=20, color=YES).move_to(LEFT * 4.6 + DOWN * 1.3)
        outs = VGroup(*[mono(str(v), 22, YES) for v in mx]).arrange(RIGHT, buff=0.3).next_to(outl, RIGHT, buff=0.4)
        notes = VGroup(
            label(r"arriving: \ pop every smaller value from the back \ (it can never be a maximum again)",
                  font_size=21, color=LAM),
            label(r"leaving: \ drop the front once it falls out of the window; \ the front is always the maximum",
                  font_size=21, color=HEAD),
            label(rf"each index enters once and leaves at most once: \ {d['pops']} pops for {len(a)} elements; \ "
                  r"$O(n)$, \ not $O(nk)$", font_size=21, color=YES),
            label(r"\textbf{two pointers}: \ both ends of the window only move forward, \ so the total work is linear",
                  font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Slide a window of four along an array and report the largest value in each position of the window. "
            "Checking all four each time costs n times k. <bookmark mark='a'/> Keep instead a double-ended queue of "
            "positions whose values decrease from front to back. When a new value arrives, every smaller value at "
            "the back can never be a window's maximum again, because the newcomer is larger and will stay longer; "
            "pop them. <bookmark mark='b'/> When the front falls out of the window, drop it. The front is always the "
            "current maximum. <bookmark mark='c'/> Each position enters the queue once and leaves at most once, so "
            "the whole pass is linear, however wide the window. <bookmark mark='d'/> This is the two-pointer "
            "pattern: both ends of the window only move forward. The inner loop looks quadratic, and the amortized "
            "count proves it linear."
        ) as vo:
            self.play(FadeIn(head), FadeIn(row), FadeIn(dql), FadeIn(outl))
            self.play(Create(win), FadeIn(dq))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            for i in range(1, len(a)):
                lo = max(0, i - k + 1)
                new_win = SurroundingRectangle(VGroup(*row.boxes[lo:i + 1]), color=HEAD, buff=0.05, stroke_width=3)
                new_dq = dq_mob(tr[i])
                anims = [Transform(win, new_win), Transform(dq, new_dq)]
                if i >= k - 1:
                    anims.append(FadeIn(outs[i - k + 1]))
                self.play(*anims, run_time=0.55)
                if i == 6:
                    vo.wait_until("b")
                    self.play(FadeIn(notes[1]), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def substring(self):
        text = "abcabcbbdaef"
        head = label(r"Two pointers: \ the longest stretch without a repeat", font_size=32).to_edge(UP, buff=0.35)
        cw = 0.66
        cells = VGroup(*[VGroup(Rectangle(width=cw, height=0.58, stroke_color=GREY_B, stroke_width=1.2),
                                mono(ch, 24, WHITE)) for ch in text])
        for c in cells:
            c[1].move_to(c[0])
        cells.arrange(RIGHT, buff=0).next_to(head, DOWN, buff=0.7)
        steps, last, lo, best = [], {}, 0, (0, 0)
        for hi, ch in enumerate(text):
            if ch in last and last[ch] >= lo:
                lo = last[ch] + 1
            last[ch] = hi
            if hi - lo + 1 > best[1] - best[0]:
                best = (lo, hi + 1)
            steps.append((lo, hi))
        win = SurroundingRectangle(cells[0], color=HEAD, buff=0.04, stroke_width=3)
        notes = VGroup(
            label(r"the right end advances one letter at a time; \ a repeat moves the left end just past its last "
                  r"occurrence", font_size=21, color=HEAD),
            label(r"a table of last positions makes each move $O(1)$; \ the left end never moves back", font_size=21,
                  color=WHITE),
            label(rf"best here: \ ``{text[best[0]:best[1]]}'', \ {best[1] - best[0]} letters; \ $2n$ pointer moves at "
                  r"most, \ against $O(n^2)$ windows", font_size=21, color=YES),
            label(r"the same skeleton: \ minimum window covering a set, \ subarrays with sum $\le S$, \ deduplicating "
                  r"streams", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.22).next_to(cells, DOWN, buff=0.8)
        with self.voiceover(
            "The window need not have a fixed width. <bookmark mark='a'/> Find the longest stretch of this string "
            "with no repeated letter. Move the right end one letter at a time. When the new letter already occurs "
            "inside the window, jump the left end to just past that earlier occurrence. <bookmark mark='b'/> A table "
            "of each letter's last position makes every move constant time, and the left end never moves backwards. "
            "<bookmark mark='c'/> So the whole scan is at most two n pointer moves, where checking every window "
            "would be quadratic. <bookmark mark='d'/> The same two-pointer skeleton finds the smallest window "
            "containing a set of words, or the longest subarray whose sum stays under a budget."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), Create(win))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            for lo, hi in steps:
                self.play(Transform(win, SurroundingRectangle(VGroup(*cells[lo:hi + 1]), color=HEAD, buff=0.04,
                                                              stroke_width=3)), run_time=0.45)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            best_box = SurroundingRectangle(VGroup(*cells[best[0]:best[1]]), color=YES, buff=0.1, stroke_width=3)
            self.play(Create(best_box), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def stacks(self):
        d = load("monotone")
        h = d["h"]
        area, lo, hi, hh = d["rect"]
        head = label(r"Monotonic stacks: \ the largest rectangle under a histogram", font_size=30).to_edge(UP, buff=0.3)
        bw, sc = 0.5, 0.46
        x0, y0 = -6.6, -1.6
        bars = VGroup(*[Rectangle(width=bw, height=v * sc, stroke_color=GREY_B, stroke_width=1.2).set_fill(DATA, 0.55)
                        .move_to([x0 + i * bw + bw / 2, y0 + v * sc / 2, 0]) for i, v in enumerate(h)])
        vals = VGroup(*[mono(str(v), 16, GREY_A).next_to(b, DOWN, buff=0.08) for v, b in zip(h, bars)])
        best = Rectangle(width=(hi - lo + 1) * bw, height=hh * sc, stroke_color=YES, stroke_width=3).set_fill(YES, 0.3)
        best.move_to([x0 + (lo + hi + 1) * bw / 2, y0 + hh * sc / 2, 0])
        side = VGroup(
            label(r"\textbf{next greater element}: \ keep a stack of positions still waiting; \\ each new value "
                  r"answers every smaller one on top", font_size=21, color=LAM),
            label(r"the stack's values are monotone, \ hence the name; \\ each position is pushed and popped once",
                  font_size=21, color=WHITE),
            label(r"histogram: \ when a bar is popped, \ the bar that popped it and the one below it \\ are its "
                  r"right and left limits: \ a candidate rectangle", font_size=21, color=HEAD),
            label(rf"best here: \ height {hh}, \ bars {lo}--{hi}, \ area {area} \\ (brute force agrees: "
                  rf"{d['rect_brute']})", font_size=21, color=YES),
            label(r"the same idea: \ stock spans, \ trapping rain water, \\ the skyline problem, \ maximal "
                  r"rectangles of 1s", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.2)
        if side.width > 6.2:
            side.width = 6.2
            side.to_edge(RIGHT, buff=0.35).shift(DOWN * 0.2)
        with self.voiceover(
            "A stack can be monotone too. <bookmark mark='a'/> For each element, find the next element to its right "
            "that is larger. Keep a stack of positions still waiting for an answer. Each new value answers every "
            "smaller value on top of the stack, pops them, and waits itself. <bookmark mark='b'/> The waiting values "
            "are always in decreasing order, and each position is pushed and popped once: linear time again. "
            "<bookmark mark='c'/> The famous application is the largest rectangle under a histogram. When a bar is "
            "popped, the bar that popped it is the first lower bar to its right, and the bar beneath it on the stack "
            "is the first lower bar to its left. Between them lies the widest rectangle of that bar's height. "
            "<bookmark mark='d'/> Here the best has height four across four bars, area sixteen, and brute force "
            "agrees. <bookmark mark='e'/> Stock spans, trapped rain water and the skyline problem are the same "
            "stack in different clothes."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.06),
                      FadeIn(vals))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(best), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()
