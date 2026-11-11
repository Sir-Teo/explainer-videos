from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, curve, grid_table, load, mono, words)


def human_bytes(b):
    for unit, v in (("GiB", 1 << 30), ("MiB", 1 << 20), ("KiB", 1 << 10)):
        if b >= v:
            return f"{b / v:.0f} {unit}"
    return f"{b} B"


class Layouts(VoiceoverScene):
    def construct(self):
        self.card()
        self.eytzinger()
        self.measured()
        self.branches()

    def card(self):
        card = chapter_card(9, r"Algorithm engineering I: \ layouts", r"Where should the data live for binary search?",
                            lit=(1590, 2017), extra=((1590, r"Eytzinger's genealogies"), (2017, r"Khuong--Morin")),
                            part=PART)
        with self.voiceover("Chapter nine. Algorithm engineering, part one: layouts."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def eytzinger(self):
        head = label(r"The same 15 keys, \ three layouts", font_size=34).to_edge(UP, buff=0.3)
        keys = list(range(10, 160, 10))
        n = len(keys)
        eyt = [None] * (n + 1)
        it = iter(keys)

        def build(k):
            if k <= n:
                build(2 * k)
                eyt[k] = next(it)
                build(2 * k + 1)
        build(1)
        cw = 0.6

        def row(vals, y, color, path=()):
            g = VGroup()
            for i, v in enumerate(vals):
                b = Rectangle(width=cw, height=0.5, stroke_color=GREY_B, stroke_width=1.2).set_fill(
                    color, 0.55 if i in path else 0.08)
                g.add(VGroup(b, mono(str(v), 17, WHITE).move_to(b)))
            g.arrange(RIGHT, buff=0).move_to([0, y, 0])
            return g
        target = 110
        # sorted: the probes of binary search
        lo, hi, probes = 0, n - 1, []
        while lo <= hi:
            m = (lo + hi) // 2
            probes.append(m)
            if keys[m] < target:
                lo = m + 1
            elif keys[m] > target:
                hi = m - 1
            else:
                break
        r1 = row(keys, 1.7, DATA, probes)
        l1 = label(r"sorted: \ probes jump across the array", font_size=20, color=DATA).next_to(r1, UP, buff=0.12)
        k, ep = 1, []
        while k <= n:
            ep.append(k - 1)
            if eyt[k] == target:
                break
            k = 2 * k + (eyt[k] < target)
        r2 = row(eyt[1:], -0.1, LAM, ep)
        l2 = label(r"Eytzinger \ (breadth-first): \ node $k$'s children at $2k$, $2k + 1$", font_size=20,
                   color=LAM).next_to(r2, UP, buff=0.12)
        notes = VGroup(
            label('sorted: early probes are far apart; cache misses are not counted here', font_size=21,
                  color=DATA),
            label('Eytzinger: grouped top levels; prefetch a contiguous future candidate region \\\\ the guarded address stays inside the allocation', font_size=21, color=LAM),
            label(r"B-tree layout: \ 16 keys per 64-byte node, \ compared with one AVX-512 instruction; \ "
                  r"$\log_{17} n$ levels", font_size=21, color=HEAD),
            label(r"Khuong and Morin (2017): \ ``Array layouts for comparison-based searching''", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Search layout changes the concrete implementation of a lower-bound query. <bookmark mark='a'/> In a "
            'sorted array, binary search visits progressively smaller intervals, often at distant addresses. '
            "<bookmark mark='b'/> Eytzinger order stores an implicit tree breadth first, with children at twice "
            'the parent index and twice plus one. This groups top levels and can make a future region suitable '
            'for explicit prefetching. Our code bounds the prefetch address within the allocation. <bookmark '
            "mark='c'/> The array B-tree packs sixteen thirty-two-bit keys into a sixty-four-byte node and uses "
            "an AVX-512 vector comparison, followed by a mask count and child selection. <bookmark mark='d'/> "
            'Khuong and Morin study these layouts. Our experiment measures the exact retained implementations on '
            'this host; it does not measure a cache-miss rate or prove which microarchitectural mechanism caused '
            'a speed difference.'
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(r1), FadeIn(l1), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(r2), FadeIn(l2), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("layouts")
        rows = d["rows"]
        head = label(r"Nanoseconds per search, \ by array size", font_size=32).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[12, 28, 2], y_range=[0, 1000, 200], x_length=7.0, y_length=4.4,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.0).shift(DOWN * 0.2)
        yt = VGroup(*[mono(str(v), 15, GREY_B).next_to(ax.c2p(12, v), LEFT, buff=0.1) for v in range(0, 1001, 200)])
        xt = VGroup(*[mono(human_bytes(1 << k), 14, GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.12)
                      for k in range(12, 29, 4)])
        xs = [math.log2(r["bytes"]) for r in rows]
        series = [("branchy", r"sorted, \ branchy", NO), ("branchless", r"sorted, \ branchless", GREY_A),
                  ("eytzinger", r"Eytzinger + prefetch", LAM), ("btree", r"B-tree, \ AVX-512", YES)]
        curves = VGroup(*[curve(ax, xs, [r[key] for r in rows], col, dots=True) for key, _, col in series])
        keys = VGroup(*[label(txt, font_size=18, color=col) for _, txt, col in series]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax.c2p(12.3, 1000), DR, buff=0.05)
        caches = VGroup()
        big_ = rows[-1]
        small = rows[0]
        side = VGroup(
            label(rf"{words(small['bytes'] // 4)} keys: \\ branchy {small['branchy']:.0f} ns, \ B-tree "
                  rf"{small['btree']:.0f} ns", font_size=20, color=WHITE),
            label(rf"{words(big_['bytes'] // 4)} keys \ ({human_bytes(big_['bytes'])}): \\ {big_['branchy']:.0f} ns "
                  rf"against {big_['btree']:.0f} ns, \ {big_['branchy'] / big_['btree']:.1f}$\times$", font_size=20,
                  color=YES),
            label('latency alone does not identify cache or branch misses', font_size=20,
                  color=GREY_A),
            label('same lookup specification; different scalar, SIMD and memory work', font_size=20,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3)
        if side.width > 5.0:
            side.width = 5.0
            side.to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "Each size receives a million generated lookup queries. <bookmark mark='a'/> The red curve is "
            'ordinary binary search, with minima from three repetitions. Full sources, ISA flags and raw clock '
            "reads accompany the data. <bookmark mark='b'/> Branch-free binary search changes the instruction "
            "sequence. Its relative performance is specific to this processor and workload. <bookmark mark='c'/> "
            "Eytzinger order adds a different layout and explicit prefetching. <bookmark mark='d'/> The array "
            'B-tree uses sixteen-way AVX-512 comparisons within a node. Every actual answer is checked after '
            "timing against a certified lower-bound value. <bookmark mark='e'/> These implementations perform "
            'different scalar and SIMD work. Their elapsed times alone do not isolate cache misses, branch '
            'misses or prefetch effects. They share a lookup specification, rather than an identical comparison '
            'trace.'
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(caches))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(keys[0]), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(curves[1]), FadeIn(keys[1]), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(curves[2]), FadeIn(keys[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(curves[3]), FadeIn(keys[3]), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def branches(self):
        b = load("branches")
        head = label(r"When branches do matter", font_size=34).to_edge(UP, buff=0.35)
        code_ = VGroup(*[mono(t, 22, c) for t, c in (("for (i = 0; i < n; i++)", WHITE),
                                                      ("    if (a[i] >= 128) s += a[i];", NO),
                                                      ("// or, with no branch:", GREY_B),
                                                      ("    s += a[i] & -(a[i] >= 128);", YES))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(head, DOWN, buff=0.45)
        rows = [[r"with a branch", f"{b['random_branchy']:.2f}", f"{b['sorted_branchy']:.2f}"],
                [r"branch-free \ (a mask)", f"{b['random_branchless']:.2f}", f"{b['sorted_branchless']:.2f}"]]
        tab = grid_table([rf"ns per element, \ {words(b['n'])} 32-bit values in $[0,255]$", r"shuffled", r"sorted"], rows,
                         widths=[5.4, 2.0, 2.0], row_h=0.48, font_size=22, mono_cols=(),
                         colors=[[NO] * 3, [YES] * 3])
        tab.next_to(code_, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label('shuffled versus sorted: measured time, not a measured miss rate',
                  font_size=21, color=NO),
            label(r"each misprediction throws away the pipeline's speculative work \ (Parts 7 and 8)", font_size=21,
                  color=WHITE),
            label('mask version: inspect its actual instructions and measured times', font_size=21,
                  color=YES),
            label('branch effects depend on code, data, compiler and processor',
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Branches are another possible cost. <bookmark mark='a'/> This experiment stores values from zero to "
            'two hundred and fifty-five in thirty-two-bit integers, then sums those at least a hundred and '
            "twenty-eight. <bookmark mark='b'/> We compare shuffled and sorted order using the same multiset. "
            'The branchy function disables if-conversion and vectorization. A separate histogram certifies the '
            'sum. The observed timing difference is consistent with a branch-prediction explanation, but no '
            "branch-miss counter was collected. <bookmark mark='c'/> A mask-based function provides another "
            "implementation on the same inputs. <bookmark mark='d'/> Read all four measured times. Their "
            'ordering describes these loops; it does not establish that predictable branches are universally '
            'free or that binary search is always limited by memory.'
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(code_[:2]))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[1])),
                      FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(code_[2:]), FadeIn(VGroup(*tab.cells[2])), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()
