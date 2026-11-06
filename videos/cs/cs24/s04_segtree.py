from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, cells_row, grid_table, load, mono, words)


def seg_layout(n, top=2.45, width=12.0, dy=0.88):
    """Node k of a segment tree over n leaves (n a power of two): its centre and width."""
    pos = {}
    depth = int(math.log2(n))
    for d in range(depth + 1):
        cnt = 1 << d
        w = width / cnt
        for i in range(cnt):
            k = cnt + i
            pos[k] = (np.array([-width / 2 + w * (i + 0.5), top - d * dy, 0]), w)
    return pos


class SegmentTrees(VoiceoverScene):
    def construct(self):
        self.card()
        self.tree()
        self.monoid()
        self.lazy()

    def card(self):
        card = chapter_card(3, r"Segment trees", r"What if the question is not a sum?", lit=(1977,),
                            extra=((1977, r"Bentley's segment trees"),), part=PART)
        with self.voiceover("Chapter three. Segment trees."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tree(self):
        d = load("segtree")
        a = d["a"]
        n = len(a)
        l, r = d["query"]
        head = label(r"A tree of ranges", font_size=34).to_edge(UP, buff=0.3)
        pos = seg_layout(n)

        def rng(k):
            depth = int(math.log2(k))
            span = n >> depth
            lo = (k - (1 << depth)) * span
            return lo, lo + span - 1

        def mn(k):
            lo, hi = rng(k)
            return min(a[lo:hi + 1])
        nodes = VGroup()
        for k, (c, w) in pos.items():
            box = RoundedRectangle(width=w - 0.08, height=0.62, corner_radius=0.08, stroke_color=GREY_B,
                                   stroke_width=1.2).move_to(c)
            nodes.add(VGroup(box, mono(str(mn(k)), 18 if k < n else 20, WHITE).move_to(c)))
        nodes.k = list(pos.keys())
        cover = {c[0] for c in d["cover"]}
        hl = VGroup(*[nodes[i][0].copy().set_stroke(YES, 3).set_fill(YES, 0.25)
                      for i, k in enumerate(nodes.k) if k in cover])
        idx = VGroup(*[mono(str(i), 14, GREY_C).next_to(pos[n + i][0], DOWN, buff=0.38) for i in range(n)])
        span = VGroup(Line(pos[n + l][0] + DOWN * 0.75 + LEFT * 0.3, pos[n + r][0] + DOWN * 0.75 + RIGHT * 0.3,
                           color=YES, stroke_width=4))
        notes = VGroup(
            label(r"each node holds the minimum of its range; \ any associative operation works \ (a \textbf{monoid})",
                  font_size=21, color=WHITE),
            label(rf"query $[{l}, {r}]$: \ {len(cover)} covering nodes, \ {d['visits']} visited, \ minimum {d['min']}; \ "
                  r"never more than $2 \log_2 n$ covering nodes", font_size=21, color=YES),
            label(r"update a leaf: \ fix the $\log_2 n$ nodes above it", font_size=21, color=LAM),
            label(r"min, \ max, \ gcd, \ sum, \ matrix products, \ ``maximum subarray'' with a 4-tuple per node",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Fenwick trees need an operation you can undo, like subtraction. For the minimum of a range you cannot "
            "subtract, and you need a segment tree. <bookmark mark='a'/> Build a balanced tree over the array. Each "
            "node holds the minimum of the stretch below it: the leaves are the elements, the root the whole array. "
            "Any associative operation works the same way. <bookmark mark='b'/> To answer positions three to twelve, "
            "descend from the root and stop at every node whose range lies entirely inside the query. Four nodes "
            "cover this range. At most two per level ever do, so a query costs logarithmic time. <bookmark "
            "mark='c'/> Changing one element changes only the nodes above it, one per level. <bookmark mark='d'/> "
            "Minimum, maximum, greatest common divisor, matrix products: anything associative. Even the maximum "
            "subarray sum, if each node keeps four numbers instead of one."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(x) for x in nodes], lag_ratio=0.02), FadeIn(idx), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(span), FadeIn(hl), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def monoid(self):
        head = label(r"A node can carry more than one number", font_size=32).to_edge(UP, buff=0.35)
        L = [3, -4, 5, -1]
        R = [2, -6, 4, 1]

        def summary(a):
            tot = sum(a)
            pre = max(sum(a[:i + 1]) for i in range(len(a)))
            suf = max(sum(a[i:]) for i in range(len(a)))
            best = max(sum(a[i:j + 1]) for i in range(len(a)) for j in range(i, len(a)))
            return tot, pre, suf, best
        sl, sr = summary(L), summary(R)
        tot = sl[0] + sr[0]
        pre = max(sl[1], sl[0] + sr[1])
        suf = max(sr[2], sr[0] + sl[2])
        best = max(sl[3], sr[3], sl[2] + sr[1])
        assert best == summary(L + R)[3]

        def box(vals, a, color):
            cells = VGroup(*[VGroup(Rectangle(width=0.55, height=0.48, stroke_color=GREY_B, stroke_width=1.1),
                                    mono(str(v), 18, WHITE)) for v in a])
            for c in cells:
                c[1].move_to(c[0])
            cells.arrange(RIGHT, buff=0)
            t = MathTex(rf"\text{{sum}}\ {vals[0]},\ \text{{pre}}\ {vals[1]},\ \text{{suf}}\ {vals[2]},\ "
                        rf"\text{{best}}\ {vals[3]}", font_size=24, color=color).next_to(cells, DOWN, buff=0.15)
            return VGroup(cells, t)
        bl = box(sl, L, DATA)
        br = box(sr, R, LAM)
        VGroup(bl, br).arrange(RIGHT, buff=1.2).next_to(head, DOWN, buff=0.6)
        comb = VGroup(
            MathTex(rf"\text{{sum}} = {sl[0]} + {sr[0]} = {tot}", font_size=28, color=WHITE),
            MathTex(rf"\text{{pre}} = \max({sl[1]},\ {sl[0]} + {sr[1]}) = {pre}", font_size=28, color=WHITE),
            MathTex(rf"\text{{suf}} = \max({sr[2]},\ {sr[0]} + {sl[2]}) = {suf}", font_size=28, color=WHITE),
            MathTex(rf"\text{{best}} = \max({sl[3]},\ {sr[3]},\ {sl[2]} + {sr[1]}) = {best}", font_size=28, color=YES),
        ).arrange(DOWN, buff=0.18).next_to(VGroup(bl, br), DOWN, buff=0.5)
        notes = VGroup(
            label(r"the best stretch is in the left half, \ the right half, \ or crosses the middle: \ left's best "
                  r"suffix plus right's best prefix", font_size=21, color=HEAD),
            label(r"four numbers combine associatively, \ so the segment tree answers ``maximum subarray in $[l, r]$'' "
                  r"with updates", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.18).next_to(comb, DOWN, buff=0.35)
        with self.voiceover(
            "The trick that makes segment trees so flexible is that a node can carry a small record instead of one "
            "number. <bookmark mark='a'/> Take the maximum-sum stretch of consecutive elements, the problem Bentley "
            "made famous. For each half, keep four numbers: its total, its best prefix, its best suffix, and its "
            "best stretch anywhere. <bookmark mark='b'/> Two halves combine in constant time. The total adds. The "
            "best prefix is either the left's, or the whole left plus the right's best prefix, and the suffix is the "
            "mirror image. <bookmark mark='c'/> And the best stretch lies in the left half, in the right half, or "
            "across the middle, where it is the left's best suffix joined to the right's best prefix. Here the "
            "winner is the one that crosses: six, which brute force confirms. <bookmark mark='d'/> Because this combination is associative, "
            "the segment tree can answer the maximum subarray of any range, while elements change underneath it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bl), FadeIn(br))
            vo.wait_until("b")
            self.play(FadeIn(comb[:3]))
            vo.wait_until("c")
            self.play(FadeIn(comb[3]), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    def lazy(self):
        d = load("segtree")
        head = label(r"Lazy propagation: \ update a range in $O(\log n)$", font_size=32).to_edge(UP, buff=0.35)
        rows = [[words(r["n"]), f"{r['naive']:.0f}", f"{r['lazy']:.0f}"] for r in d["lazy"]]
        tab = grid_table([r"$n$", r"elements touched, \ one by one", r"nodes visited, \ lazily"], rows,
                         widths=[1.6, 3.6, 3.2], row_h=0.42, font_size=21, mono_cols=(),
                         colors=[[WHITE, NO, YES]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label(r"``add $v$ to every element of $[l, r]$'': \ stop at the covering nodes, \ and leave a \textbf{tag} "
                  r"there", font_size=22, color=WHITE),
            label(r"push the tag down only when a later operation needs to go below it", font_size=22, color=LAM),
            label(r"random ranges, \ 500 per size: \ the lazy tree's work grows like $\log n$", font_size=22,
                  color=YES),
            label(r"\textbf{persistence}: \ copy only the $\log n$ nodes on the path, \ and every old version stays "
                  r"queryable", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "What if the updates are ranges too? <bookmark mark='a'/> To add a value to every element from l to r, "
            "descend as a query does, and at each covering node, update its summary and leave a tag saying: everything "
            "below me owes this amount. <bookmark mark='b'/> The tag is pushed to the children only when a later "
            "query or update has to go beneath it. That laziness is the whole trick. <bookmark mark='c'/> On random "
            "ranges, touching every element costs about a quarter of n per update; the lazy tree visits a few dozen "
            "nodes, growing with the logarithm. <bookmark mark='d'/> And because an update changes only one path of "
            "nodes, you can copy that path instead of overwriting it, and keep every past version of the array, "
            "queryable, for the price of a logarithm per update. That is a persistent segment tree."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()
