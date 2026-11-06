from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, curve, grid_table, load, mono, words)


def human_bytes(b):
    for unit, v in (("GB", 1 << 30), ("MB", 1 << 20), ("KB", 1 << 10)):
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
            label(r"sorted: \ the first probes are far apart, \ each a cache miss on a large array", font_size=21,
                  color=DATA),
            label(r"Eytzinger: \ the top of the tree is packed at the front, \ hot in cache; \ the next four levels "
                  r"are one cache line ahead, \ so \textbf{prefetch} them", font_size=21, color=LAM),
            label(r"B-tree layout: \ 16 keys per 64-byte node, \ compared with one AVX-512 instruction; \ "
                  r"$\log_{17} n$ levels", font_size=21, color=HEAD),
            label(r"Khuong and Morin (2017): \ ``Array layouts for comparison-based searching''", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Binary search is optimal in comparisons, and on a large array it is slow, for the reason of the opening "
            "chapter. <bookmark mark='a'/> Here are fifteen sorted keys and the probes for one hundred and ten: the "
            "middle, then a quarter of the way along, and so on. On a big array every early probe lands on a "
            "different cache line, far from the last. <bookmark mark='b'/> The Eytzinger layout, named after a "
            "sixteenth-century genealogist who numbered ancestors this way, stores the implicit search tree "
            "breadth-first: the root, then its two children, then four grandchildren. Node k's children sit at two "
            "k and two k plus one. The top levels are packed together and stay in cache, and the next few levels of "
            "any path lie in one predictable region, so the program can prefetch them before it knows which way it "
            "will go. <bookmark mark='c'/> Or pack sixteen keys into each sixty-four-byte node, a B-tree in an "
            "array, and compare a query against all sixteen with one vector instruction. <bookmark mark='d'/> Paul-"
            "Virgile Khuong and Pat Morin measured these layouts in 2017; here they are on this machine."
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
        for name, b in (("L1", 48 << 10), ("L2", 2 << 20), ("L3", 260 << 20)):
            x = math.log2(b)
            if 12 <= x <= 28:
                caches.add(DashedLine(ax.c2p(x, 0), ax.c2p(x, 1000), color=GREY_D, stroke_width=1.2))
                caches.add(mono(name, 14, GREY_B).next_to(ax.c2p(x, 1000), UP, buff=0.05))
        big_ = rows[-1]
        small = rows[0]
        side = VGroup(
            label(rf"{words(small['bytes'] // 4)} keys: \ branchy {small['branchy']:.0f} ns, \ B-tree "
                  rf"{small['btree']:.0f} ns", font_size=20, color=WHITE),
            label(rf"{words(big_['bytes'] // 4)} keys \ ({human_bytes(big_['bytes'])}): \ {big_['branchy']:.0f} ns "
                  rf"against {big_['btree']:.0f} ns, \ {big_['branchy'] / big_['btree']:.1f}$\times$", font_size=20,
                  color=YES),
            label(r"branch-free code did not help on this CPU: \ the misses are memory, \ not branches", font_size=20,
                  color=GREY_A),
            label(r"the layout changes nothing in the RAM model \ and everything on the machine", font_size=20,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3)
        if side.width > 4.6:
            side.width = 4.6
            side.to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "A million random searches at each size, from a thousand keys to sixty-four million. <bookmark "
            "mark='a'/> Plain binary search climbs from seventy nanoseconds to nine hundred as the array outgrows "
            "each cache. <bookmark mark='b'/> On this processor the branch-free version is barely faster: the cost is "
            "the memory, not mispredicted branches. That differs between machines, which is why you measure. "
            "<bookmark mark='c'/> The Eytzinger layout with prefetching is three to four times faster at every size. "
            "<bookmark mark='d'/> And the B-tree layout, sixteen keys compared at once, is fastest of all: about five "
            "times faster than the textbook at sixty-four million keys. <bookmark mark='e'/> Every one of them makes "
            "about log n comparisons. The layout changes nothing in the model of Part 16, and everything on the "
            "machine."
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
                                                      ("", WHITE),
                                                      ("    s += a[i] & -(a[i] >= 128);", YES))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(head, DOWN, buff=0.45)
        rows = [[r"with a branch", f"{b['random_branchy']:.2f}", f"{b['sorted_branchy']:.2f}"],
                [r"branch-free \ (a mask)", f"{b['random_branchless']:.2f}", f"{b['sorted_branchless']:.2f}"]]
        tab = grid_table([rf"ns per element, \ {words(b['n'])} random bytes", r"shuffled", r"sorted"], rows,
                         widths=[5.4, 2.0, 2.0], row_h=0.48, font_size=22, mono_cols=(),
                         colors=[[NO] * 3, [YES] * 3])
        tab.next_to(code_, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label(rf"shuffled data: \ the branch is a coin flip, \ mispredicted half the time: \ "
                  rf"{b['random_branchy'] / b['sorted_branchy']:.1f}$\times$ slower than the same loop on sorted data",
                  font_size=21, color=NO),
            label(r"each misprediction throws away the pipeline's speculative work \ (Parts 7 and 8)", font_size=21,
                  color=WHITE),
            label(r"the mask version has no branch to mispredict: \ the same speed on any data", font_size=21,
                  color=YES),
            label(r"so: \ predictable branches are nearly free; \ unpredictable ones on hot paths are worth removing",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Branch-free search did not help this processor, but that does not mean branches are free. <bookmark "
            "mark='a'/> Here is a loop that adds up the bytes of an array that are at least a hundred and "
            "twenty-eight, with an if. <bookmark mark='b'/> On shuffled data that if is a coin flip. The predictor of "
            "Parts 7 and 8 guesses wrong half the time, and every wrong guess throws away the work the pipeline did "
            "speculatively. On sorted data the branch goes one way and then the other, and is almost always "
            "predicted. The same loop, the same values, five times faster. <bookmark mark='c'/> Replace the if with "
            "a mask, the comparison turned into all ones or all zeros, and there is nothing left to predict: the "
            "same speed on either data. <bookmark mark='d'/> Predictable branches are nearly free. Unpredictable ones "
            "in a hot loop are worth removing, and binary search's were not the bottleneck because the memory was."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(code_[:2]))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[1])),
                      FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(code_[3]), FadeIn(VGroup(*tab.cells[2])), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

