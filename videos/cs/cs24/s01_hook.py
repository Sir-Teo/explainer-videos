from __future__ import annotations

import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, curve, load, log_axes, mono, words)


class Hook(VoiceoverScene):
    def construct(self):
        self.race()
        self.chart()
        self.plan()

    def race(self):
        head = label(r"Two loops, \ both $O(n)$", font_size=36).to_edge(UP, buff=0.4)
        c1 = VGroup(*[mono(t, 22, DATA) for t in ("for (i = 0; i < n; i++)", "    s += a[i];")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08)
        c2 = VGroup(*[mono(t, 22, NO) for t in ("for (p = head; p; p = p->next)", "    s += p->val;")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08)
        VGroup(c1, c2).arrange(RIGHT, buff=1.6).next_to(head, DOWN, buff=0.6)
        t1 = label(r"an array, \ in order", font_size=20, color=DATA).next_to(c1, UP, buff=0.15)
        t2 = label(r"a linked list, \ nodes scattered in memory", font_size=20, color=NO).next_to(c2, UP, buff=0.15)
        m = 32
        cw = 0.36
        mem = VGroup(*[Rectangle(width=cw, height=0.5, stroke_color=GREY_D, stroke_width=1) for _ in range(m)])
        mem.arrange(RIGHT, buff=0).move_to(DOWN * 0.9)
        ml = label(r"memory", font_size=18, color=GREY_A).next_to(mem, LEFT, buff=0.2)
        sweep = VGroup(*[mem[i].copy().set_fill(DATA, 0.6) for i in range(16)])
        rng = random.Random(7)
        order = list(range(m))
        rng.shuffle(order)
        hops = VGroup(*[CurvedArrow(mem[a].get_bottom(), mem[b].get_bottom(), angle=-TAU / 6, color=NO,
                                    stroke_width=2, tip_length=0.12) for a, b in zip(order[:10], order[1:11])])
        notes = VGroup(
            label(r"the same number of additions, \ the same big-O, \ the same answer", font_size=22, color=WHITE),
            label(r"the array streams through the caches; \ each list node is a fresh trip to memory", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here are two loops that add up n numbers. <bookmark mark='a'/> The first walks an array in order. "
            "<bookmark mark='b'/> The second follows a linked list whose nodes are scattered through memory. "
            "<bookmark mark='c'/> Both do n additions, both are linear time, and they compute the same sum. Every "
            "analysis in Parts 16 to 23 would call them equal. <bookmark mark='d'/> The machine does not. The array "
            "streams through the caches a line at a time, with the prefetcher running ahead, while each list node is "
            "a separate trip to memory that cannot start until the previous one has returned."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(c1), FadeIn(t1), FadeIn(mem), FadeIn(ml))
            self.play(LaggedStart(*[FadeIn(s) for s in sweep], lag_ratio=0.08), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(c2), FadeIn(t2), FadeOut(sweep))
            self.play(LaggedStart(*[Create(h) for h in hops], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    def chart(self):
        h = load("hook")
        rows = h["rows"]
        head = label(r"Measured on this machine", font_size=34).to_edge(UP, buff=0.3)
        ax = log_axes([3, 8, 1], [-1, 3, 1], x_length=6.4, y_length=4.0, x_label=r"elements $n$",
                      y_label=r"nanoseconds per element").to_edge(LEFT, buff=0.9).shift(DOWN * 0.2)
        xs = [math.log10(r["n"]) for r in rows]
        arr = curve(ax.ax, xs, [math.log10(r["array_ns"]) for r in rows], DATA)
        lst = curve(ax.ax, xs, [math.log10(r["list_ns"]) for r in rows], NO)
        al = label(r"array", font_size=20, color=DATA).next_to(arr[0].get_end(), RIGHT, buff=0.12)
        ll = label(r"linked list", font_size=20, color=NO).next_to(lst[0].get_end(), RIGHT, buff=0.12)
        r16 = next(r for r in rows if r["logn"] == 16)
        r24 = rows[-1]
        side = VGroup(
            label(rf"$n = {words(rows[0]['n'])}$: \ {rows[0]['ratio']:.0f}$\times$ apart \\ (everything fits in L1)",
                  font_size=21, color=WHITE),
            label(rf"$n = {words(r16['n'])}$: \ {r16['ratio']:.0f}$\times$", font_size=21, color=HEAD),
            label(rf"$n = {words(r24['n'])}$: \ {r24['ratio']:.0f}$\times$ \\ ({r24['list_ns']:.0f} ns a node, \ "
                  rf"{r24['array_ns']:.1f} ns an element)", font_size=21, color=NO),
            label(r"big-O hides the constant, \\ and here the constant is \\ the memory hierarchy \ (Part 9)",
                  font_size=21, color=YES),
            label(rf"{h['cpu']} \\ gcc \texttt{{-O2}}", font_size=16, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        if side.width > 5.2:
            side.width = 5.2
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Here they are, timed on the machine that made this video. <bookmark mark='a'/> With a thousand "
            "elements everything fits in the first-level cache, and the list is already five times slower. "
            "<bookmark mark='b'/> At sixty-five thousand it is twenty-two times slower. <bookmark mark='c'/> At sixteen "
            "million the array costs a nanosecond and a half per element and the list two hundred: a hundred and "
            "forty times apart, with the same big-O. <bookmark mark='d'/> Big-O hides the constant factor, and on "
            "real hardware the constant is mostly the memory hierarchy of Part 9. This part is about the tools that "
            "real code is built from, and about engineering them for the machine."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(side[4]))
            vo.wait_until("a")
            self.play(Create(arr), Create(lst), FadeIn(al), FadeIn(ll), FadeIn(side[0]), run_time=2.5)
            for mk, n_ in zip("bcd", side[1:4]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Algorithms in Practice", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"the everyday tools: \ prefix sums, \ Fenwick and segment trees, \ range minimum and LCA",
            r"linear-time patterns: \ two pointers, \ monotonic stacks and deques, \ searching for the answer",
            r"bits: \ word tricks, \ submasks, \ the Four Russians; \ meet in the middle; \ square roots",
            r"algorithm engineering: \ search layouts, \ SIMD, \ Swiss tables, \ radix sort, \ measured",
            r"benchmarking honestly, \ and problem solving as a craft",
            r"the Job engineered \ (ledger row 10); \ the frontier: \ learned indexes and predictions",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 24 of Computer Science, Built: Algorithms in Practice. <bookmark mark='a'/> In this part: the "
            "everyday data structures of real code, prefix sums, Fenwick and segment trees, range minimum and lowest "
            "common ancestors; the linear-time patterns, two pointers, monotonic stacks and binary search on the "
            "answer; word-level tricks and the Four Russians; meet in the middle and square roots; then algorithm "
            "engineering, measured on this machine: memory layouts, vector instructions, hash tables and sorting; "
            "how to benchmark honestly; and the Job, engineered, for the ledger's tenth row."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
