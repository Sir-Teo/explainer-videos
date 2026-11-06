from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, cells_row, gnode, load, mono)


def tree_pos(parent, origin, dx=0.75, dy=0.95):
    """Leaves left to right in depth-first order; internal nodes centred over their children."""
    kids = {}
    for v, p in enumerate(parent):
        if p >= 0:
            kids.setdefault(p, []).append(v)
    pos, x = {}, [0]

    def walk(v, d):
        ch = kids.get(v, [])
        for c in ch:
            walk(c, d + 1)
        if ch:
            px = np.mean([pos[c][0] for c in ch])
        else:
            px = x[0]
            x[0] += 1
        pos[v] = np.array([px, -d, 0.0])
    walk(0, 0)
    return {v: origin + np.array([p[0] * dx, p[1] * dy, 0]) for v, p in pos.items()}


class RangeMin(VoiceoverScene):
    def construct(self):
        self.card()
        self.sparse()
        self.lca()
        self.cartesian()

    def card(self):
        card = chapter_card(4, r"Range minimum and lowest common ancestors", r"Can a range minimum be one lookup?",
                            lit=(1984, 2000), extra=((1984, r"Harel--Tarjan"), (2000, r"Bender--Farach-Colton")),
                            part=PART)
        with self.voiceover("Chapter four. Range minimum, and lowest common ancestors."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def sparse(self):
        d = load("rmq")
        a, T = d["a"], d["table"]
        l, r = d["query"]
        j = d["j"]
        head = label(r"The sparse table: \ minima of every power-of-two window", font_size=30).to_edge(UP, buff=0.3)
        w = 0.62
        x0 = -w * len(a) / 2 + w / 2
        rows = VGroup()
        for lev, row in enumerate(T):
            g = VGroup()
            for i, idx in enumerate(row):
                c = np.array([x0 + i * w, 2.0 - lev * 0.62, 0])
                sq = Rectangle(width=w, height=0.5, stroke_color=GREY_B, stroke_width=1.0).move_to(c)
                g.add(VGroup(sq, mono(str(a[idx]), 18, WHITE if lev == 0 else HEAD).move_to(c)))
            rows.add(g)
        levl = VGroup(*[label(rf"$2^{lev}$", font_size=18, color=GREY_A).next_to(rows[lev], LEFT, buff=0.2)
                        for lev in range(len(T))])
        idx = VGroup(*[mono(str(i), 14, GREY_C).next_to(rows[0][i], UP, buff=0.06) for i in range(len(a))])
        w1 = SurroundingRectangle(rows[j][l], color=YES, buff=0.03, stroke_width=3)
        w2 = SurroundingRectangle(rows[j][r - (1 << j) + 1], color=YES, buff=0.03, stroke_width=3)
        notes = VGroup(
            label(rf"row $j$ holds the minimum of each window of length $2^j$: \ {d['cells']} cells, \ "
                  r"$O(n \log n)$", font_size=21, color=HEAD),
            label(rf"query $[{l}, {r}]$: \ two windows of length $2^{j} = {1 << j}$, \ "
                  rf"$[{d['windows'][0][0]}, {d['windows'][0][1]}]$ and $[{d['windows'][1][0]}, {d['windows'][1][1]}]$, "
                  rf"\ overlap: \ min {d['min']}", font_size=21, color=YES),
            label(r"overlap is harmless because $\min(x, x) = x$: \ \textbf{idempotence} buys $O(1)$ queries",
                  font_size=21, color=WHITE),
            label(r"(a sum would count the overlap twice: \ use a Fenwick tree for sums)", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "If the array never changes, a range minimum can be a single lookup. <bookmark mark='a'/> Precompute "
            "the minimum of every window whose length is a power of two. Row zero is the array itself; each row is "
            "built from the one above, the smaller of two neighbouring windows. That is n log n numbers. <bookmark "
            "mark='b'/> To answer positions two to twelve, a range of eleven, take the largest power of two that "
            "fits, eight, and look up two windows of length eight: one starting at the left end, one ending at the "
            "right end. <bookmark mark='c'/> They overlap, and for the minimum that does not matter, because the "
            "minimum of a number with itself is that number. <bookmark mark='d'/> For a sum the overlap would be "
            "counted twice, which is why sums use the trees of the last two chapters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(idx), FadeIn(levl[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(rw, lv)) for rw, lv in zip(rows[1:], levl[1:])], lag_ratio=0.4),
                      FadeIn(notes[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(w1), Create(w2), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def lca(self):
        d = load("rmq")
        parent = d["parent"]
        head = label(r"Lowest common ancestors, \ two ways", font_size=32).to_edge(UP, buff=0.3)
        pos = tree_pos(parent, np.array([-6.0, 2.1, 0]), dx=0.62, dy=0.9)
        edges = VGroup(*[Line(pos[p], pos[v], color=GREY_B, stroke_width=1.6, buff=0.24)
                         for v, p in enumerate(parent) if p >= 0])
        nodes = VGroup(*[gnode(str(v), pos[v], color=DATA, r=0.24, font=17) for v in range(len(parent))])
        eul, dep = d["euler"], d["depth"]
        cw = 0.36
        x0 = -0.4
        tour = VGroup()
        for i, (v, dd) in enumerate(zip(eul, dep)):
            c = np.array([x0 + (i % 12) * cw, 1.3 - (i // 12) * 1.25, 0])
            tour.add(VGroup(mono(str(v), 16, WHITE).move_to(c), mono(str(dd), 13, GREY_C).move_to(c + DOWN * 0.32)))
        tl = label(r"Euler tour: \ node, \ and its depth below", font_size=19, color=GREY_A).next_to(tour, UP,
                                                                                                   buff=0.15)
        tl.align_to(tour, LEFT)
        f7, f4 = d["first"]["7"], d["first"]["4"]
        span = VGroup(*[SurroundingRectangle(tour[i], color=YES, buff=0.02, stroke_width=2) for i in range(f7, f4 + 1)])
        notes = VGroup(
            label(rf"LCA(7, 4): \ the shallowest node between their first visits \ (positions {f7}--{f4}): \ "
                  rf"node {d['lca_7_4']}", font_size=21, color=YES),
            label(r"so LCA is range minimum on the depths: \ $O(n \log n)$ to build, \ $O(1)$ per query", font_size=21,
                  color=HEAD),
            label(rf"\textbf{{binary lifting}}: \ store each node's $2^j$-th ancestor; \ LCA(9, 11) = "
                  rf"{d['lca_9_11']} after {d['lift_steps']} jump{'' if d['lift_steps'] == 1 else 's'}", font_size=21, color=LAM),
            label(r"used everywhere trees are queried: \ version control's merge base \ (Part 41), \ taxonomies, \ "
                  r"phylogenies", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In a rooted tree, the lowest common ancestor of two nodes is the deepest node above both. <bookmark "
            "mark='a'/> Walk around the tree, writing down each node every time you pass it, with its depth. "
            "<bookmark mark='b'/> Between the first visits of nodes seven and four, the tour must climb to their common "
            "ancestor and no higher, so the shallowest node in that stretch is the answer: node one. <bookmark "
            "mark='c'/> Lowest common ancestor is range minimum on the depths, and the sparse table answers it in "
            "constant time. <bookmark mark='d'/> The other classic is binary lifting: store each node's ancestor "
            "two to the j levels up. Lift the deeper node to the same depth, then lift both by decreasing powers of "
            "two while they differ. Version control finds the merge base of two branches this way, as Part 41 "
            "will show."
        ) as vo:
            self.play(FadeIn(head), Create(edges), FadeIn(nodes))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in tour], lag_ratio=0.05), FadeIn(tl), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(span), FadeIn(notes[0]), Indicate(nodes[d["lca_7_4"]], color=YES))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]), FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def cartesian(self):
        d = load("rmq")
        a, par = d["a"], d["cartesian"]
        head = label(r"The other direction: \ the Cartesian tree", font_size=32).to_edge(UP, buff=0.3)
        n = len(a)
        depth = [0] * n
        for i in range(n):
            k, dd = i, 0
            while par[k] != -1:
                k = par[k]
                dd += 1
            depth[i] = dd
        w = 0.7
        pos = {i: np.array([-w * n / 2 + w * (i + 0.5), 2.0 - depth[i] * 0.72, 0]) for i in range(n)}
        edges = VGroup(*[Line(pos[par[i]], pos[i], color=GREY_B, stroke_width=1.5, buff=0.22)
                         for i in range(n) if par[i] != -1])
        nodes = VGroup(*[gnode(str(a[i]), pos[i], color=HEAD, r=0.22, font=16) for i in range(n)])
        notes = VGroup(
            label(r"root: \ the minimum; \ left and right subtrees: \ the same, \ recursively, \ on each side",
                  font_size=21, color=HEAD),
            label(r"built in $O(n)$ with one stack \ (chapter 5's monotonic stack)", font_size=21, color=WHITE),
            label(r"RMQ$(l, r)$ on the array $=$ LCA$(l, r)$ in this tree: \ the two problems are \textbf{the same}",
                  font_size=21, color=YES),
            label(r"Bender and Farach-Colton (2000): \ $O(n)$ preprocessing, \ $O(1)$ queries, \ by going back and "
                  r"forth \ (Fischer and Heun: \ $2n + o(n)$ bits)", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The reduction runs the other way as well. <bookmark mark='a'/> The Cartesian tree of an array puts "
            "the minimum at the root, builds the left part's tree to its left and the right part's to its right, and "
            "so on down. <bookmark mark='b'/> One left-to-right pass with a stack builds it, the monotonic stack of "
            "the next chapter. <bookmark mark='c'/> The minimum of any range of the array is the lowest common "
            "ancestor of its two ends in this tree. So range minimum and lowest common ancestor are the same "
            "problem. <bookmark mark='d'/> Michael Bender and Martín Farach-Colton used the two reductions together "
            "to reach linear preprocessing and constant queries, and Johannes Fischer and Volker Heun squeezed the "
            "structure into two bits per element."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(nd) for nd in nodes], lag_ratio=0.06), Create(edges), FadeIn(notes[0]),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()
