from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs21.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, big, grid_table, load, mono, words)


def layout(edges):
    kids = {}
    for p, c, lab, leaf in edges:
        kids.setdefault(p, []).append((c, lab, leaf))
    pos, leaves = {}, [0]

    def walk(v, depth):
        ch = kids.get(v, [])
        if not ch:
            pos[v] = (leaves[0] * 1.55, -depth * 1.35)
            leaves[0] += 1
            return
        for c, _, _ in ch:
            walk(c, depth + 1)
        pos[v] = (sum(pos[c][0] for c, _, _ in ch) / len(ch), -depth * 1.35)
    walk(0, 0)
    xs = [x for x, _ in pos.values()]
    mid = (min(xs) + max(xs)) / 2
    return {v: (x - mid, y + 2.0) for v, (x, y) in pos.items()}


def _tree(d):
    edges = d["edges"]
    pos = layout(edges)
    path = {0: ""}
    for p, c, lab, leaf in edges:
        path[c] = path[p] + lab
    dots = {}
    for v, (x, y) in pos.items():
        leaf = next((lf for p, c, lab, lf in edges if c == v), None)
        if leaf is not None:
            dots[v] = VGroup(Square(side_length=0.36, color=YES, stroke_width=2),
                             mono(str(leaf), 16, YES)).move_to([x, y, 0])
        else:
            dots[v] = Dot([x, y, 0], radius=0.09, color=DATA)
    lines = {}
    for p, c, lab, leaf in edges:
        a, b = np.array([*pos[p], 0]), np.array([*pos[c], 0])
        ln = Line(a, b, buff=0.18, color=GREY_B, stroke_width=2)
        t = mono(lab, 17, LAM).move_to((a + b) / 2 + LEFT * 0.32)
        lines[c] = VGroup(ln, t)
    leafs = {v for p, v, lab, lf in edges if lf is not None}
    return dots, lines, path, leafs, VGroup(*lines.values(), *dots.values())


class SuffixTree(VoiceoverScene):
    def construct(self):
        self.card()
        self.tree()
        self.ukkonen()
        self.uses()

    def card(self):
        card = chapter_card(6, r"Suffix trees", r"Can we index every substring at once?", lit=(1973, 1995),
                            extra=((1973, r"Weiner's suffix tree"), (1995, r"Ukkonen's online build")), part=PART)
        with self.voiceover("Chapter six. Suffix trees."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tree(self):
        d = load("stree")
        head = label(r"Every suffix of \texttt{banana\$}, \ in one tree", font_size=34).to_edge(UP, buff=0.3)
        dots, lines, path, leafs, tree = _tree(d)
        tree.scale(0.85).next_to(head, DOWN, buff=0.35)
        by = {pp: v for v, pp in path.items()}
        walk = VGroup(lines[by["a"]][0], lines[by["ana"]][0]).copy().set_color(HEAD).set_stroke(width=5)
        below = [v for v in leafs if path[v].startswith("ana")]
        lines = VGroup(*lines.values())
        side = VGroup(
            label(r"each path from the root spells a substring; \ each leaf is a suffix \ (its start in the box)",
                  font_size=20, color=WHITE),
            label(r"branch only where suffixes differ: \ at most $n$ leaves, \ $n - 1$ branching nodes", font_size=20,
                  color=DATA),
            label(r"edge labels are stored as (start, end) pointers into the text: \ $O(n)$ space", font_size=20,
                  color=GREY_A),
            label('search $O(m)$ with constant-time child lookup; \\\\ report $O(\\mathrm{occ})$ more; \\ count via stored subtree sizes',
                  font_size=20, color=YES),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Fix the text and search it repeatedly. <bookmark mark='a'/> Put every suffix of banana with a unique end marker into one compact tree. Each leaf gives its suffix's start. <bookmark mark='b'/> Branch only where suffixes differ, leaving at most n leaves and fewer than n branching nodes for the indexed text. <bookmark mark='c'/> The theoretical representation stores edge labels as intervals into the original text; our small drawing materializes labels for convenience. <bookmark mark='d'/> With constant-time child lookup, a pattern walk costs order m. Stored subtree sizes give its count; reporting all matching leaves adds work proportional to the output. Ana reaches the branch with starts one and three."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.15), *[FadeIn(x) for x in dots.values()],
                      run_time=3.0)
            self.play(FadeIn(side[0]))
            for mk, s_ in zip("bc", side[1:3]):
                vo.wait_until(mk)
                self.play(FadeIn(s_))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Create(walk), run_time=1.5)
            self.play(*[Indicate(dots[v], color=HEAD, scale_factor=1.3) for v in below])
        self.wait(0.3)
        self.clear_scene()

    def ukkonen(self):
        head = label("Ukkonen's idea \\ (our small tree uses SA + LCP)", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"inserting the $n$ suffixes one by one: \ $O(n^2)$ characters walked", font_size=22, color=NO),
            label(r"Ukkonen (1995): \ grow the tree for $t_1 \dots t_i$ \\ into the tree for $t_1 \dots t_{i+1}$, \ online",
                  font_size=22, color=WHITE),
            label('\\textbf{suffix links}: \\ from $c\\alpha$ to $\\alpha$ \\\\ related suffix-shortening idea; \\ a different invariant', font_size=22, color=LAM),
            label(r"\textbf{open leaves}: \ a leaf's edge ends at ``the current end'', \\ so every leaf grows for free",
                  font_size=22, color=YES),
            label(r"active point + edge skipping + suffix links: \\ amortized $O(n)$ for fixed alphabet", font_size=22,
                  color=HEAD),
            label('linear-time theory assumes constant-time child lookup; \\ the diagram is a conceptual illustration', font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        lines.width = min(lines.width, 6.0)
        lines.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.3)
        dots, edg, path, leafs, tree = _tree(load("stree"))
        tree.scale(0.72).to_edge(LEFT, buff=0.25).shift(DOWN * 0.3)
        by = {pp: v for v, pp in path.items()}
        links = VGroup()
        for v, pp in path.items():
            if v not in leafs and pp:
                links.add(DashedVMobject(CurvedArrow(dots[v].get_center(), dots[by[pp[1:]]].get_center(), angle=0.5,
                                                     color=LAM, stroke_width=2.4, tip_length=0.16), num_dashes=18))
        open_ = [edg[v][0] for v in leafs]
        with self.voiceover(
            "Our small drawing is constructed from a suffix array and LCP values. Ukkonen is the theoretical online alternative: naive suffix insertion can walk a quadratic number of characters. <bookmark mark='a'/> Esko Ukkonen's algorithm extends the tree one character at a time instead, turning the tree of the first i characters into the tree of the first i plus one. <bookmark mark='b'/> Two tricks make that cheap. Suffix links join the node for c followed by alpha to the node for alpha, so the algorithm can jump from one suffix to the next shorter one without walking down from the root: a related suffix-shortening idea, although these links have a different invariant from Aho–Corasick. <bookmark mark='c'/> And leaf edges are left open, ending at whatever the current end of the text is, so all the leaves grow by a character at once, for free. <bookmark mark='d'/> The full construction also maintains an active point and skips whole edges. With constant-time child lookup, its amortized work is linear. <bookmark mark='e'/> The same links and the same accounting as Knuth–Morris–Pratt and Aho–Corasick: string algorithms keep rediscovering one idea."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tree), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(lines[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(lines[2], shift=UP * 0.1), LaggedStart(*[Create(x) for x in links], lag_ratio=0.4),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(lines[3], shift=UP * 0.1), *[Indicate(x, color=YES) for x in open_])
            for mk, ln in zip("de", lines[4:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def uses(self):
        s = load("sa")
        head = label(r"What a suffix tree answers", font_size=34).to_edge(UP, buff=0.35)
        rows = VGroup(
            label(r"\textbf{longest repeated substring}: \ the deepest branching node", font_size=22, color=DATA),
            label(rf"in \textit{{Moby-Dick}}: \ {s['md_repeat_len']} characters, \ a chapter title \\ that appears in the "
                  r"contents and again in the text", font_size=20, color=GREY_A),
            label(r"\textbf{longest common substring} of two texts: \ \\ one tree for both \ (generalized), \ $O(n)$",
                  font_size=22, color=LAM),
            label('original $n$ bytes: \\ distinct substrings \\\\ = edge-length sum minus $(n+1)$ terminal endings', font_size=22,
                  color=YES),
            label(rf"in \textit{{Moby-Dick}}: \ {big(s['md_distinct_substrings'])}", font_size=20, color=GREY_A),
            label(r"building it: \ Weiner (1973), \ McCreight (1976), \\ Ukkonen (1995, \ online); \ Farach (1997) "
                  r"for large alphabets", font_size=20, color=WHITE),
            label('pointer-rich trees can be large; \\\\ actual allocated bytes depend on the representation', font_size=22,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        rows.width = min(rows.width, 7.0)
        rows.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.2)
        dots, edg, path, leafs, tree = _tree(load("stree"))
        tree.scale(0.6).to_edge(LEFT, buff=0.25).shift(DOWN * 0.2)
        by = {pp: v for v, pp in path.items()}
        deep = VGroup(edg[by["a"]][0], edg[by["ana"]][0]).copy().set_color(DATA).set_stroke(width=5)
        tag = mono("ana", 18, DATA).next_to(dots[by["ana"]], RIGHT, buff=0.12)
        with self.voiceover(
            "Many questions become walks in this tree. <bookmark mark='a'/> The longest repeated substring is the deepest branching node. <bookmark mark='b'/> In Moby-Dick, it is a chapter title of a hundred characters, which appears in the table of contents and again at the head of its chapter. <bookmark mark='c'/> Put two texts in one tree, and the deepest node with leaves from both gives their longest common substring in linear time, which dynamic programming needs quadratic time for. <bookmark mark='d'/> For n original bytes plus one unique appended end marker, the edge-length sum includes n plus one extra terminated substrings. Subtract them to count the original text: <bookmark mark='e'/> for Moby-Dick, seven hundred and forty-one billion. <bookmark mark='f'/> Peter Weiner first built the tree in linear time in 1973; Esko Ukkonen's 1995 algorithm builds it online, a character at a time. <bookmark mark='g'/> The catch is representation: nodes, child structures and suffix links can take substantial memory. We do not measure a full-corpus suffix tree's allocated size here. The next chapter uses a compact integer array."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tree))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=UP * 0.1), Create(deep), FadeIn(tag))
            for mk, r in zip("bcdefg", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
                if mk == "d":
                    self.play(*[Indicate(x[1], color=YES) for x in edg.values()])
        self.wait(0.3)
        self.clear_scene()
