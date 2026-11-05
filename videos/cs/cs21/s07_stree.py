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


class SuffixTree(VoiceoverScene):
    def construct(self):
        self.card()
        self.tree()
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
        edges = d["edges"]
        pos = layout(edges)
        dots = {}
        for v, (x, y) in pos.items():
            leaf = next((lf for p, c, lab, lf in edges if c == v), None)
            if leaf is not None:
                dots[v] = VGroup(Square(side_length=0.36, color=YES, stroke_width=2),
                                 mono(str(leaf), 16, YES)).move_to([x, y, 0])
            else:
                dots[v] = Dot([x, y, 0], radius=0.09, color=DATA)
        lines = VGroup()
        for p, c, lab, leaf in edges:
            a, b = np.array([*pos[p], 0]), np.array([*pos[c], 0])
            ln = Line(a, b, buff=0.18, color=GREY_B, stroke_width=2)
            t = mono(lab, 17, LAM).move_to((a + b) / 2 + LEFT * 0.32)
            lines.add(VGroup(ln, t))
        side = VGroup(
            label(r"each path from the root spells a substring; \ each leaf is a suffix \ (its start in the box)",
                  font_size=20, color=WHITE),
            label(r"branch only where suffixes differ: \ at most $n$ leaves, \ $n - 1$ branching nodes", font_size=20,
                  color=DATA),
            label(r"edge labels are stored as (start, end) pointers into the text: \ $O(n)$ space", font_size=20,
                  color=GREY_A),
            label(r"search for $P$: \ walk down from the root, \ $O(m)$; \ the leaves below count the occurrences",
                  font_size=20, color=YES),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "What if the text, rather than the pattern, is fixed, and we will search it many times? <bookmark "
            "mark='a'/> Take every suffix of banana, with an end marker, and store them all in one tree. Each "
            "path from the root spells a substring, and each leaf is a whole suffix; the box says where it starts. "
            "<bookmark mark='b'/> The tree branches only where suffixes start to differ, so there are at most n "
            "leaves and fewer than n branching nodes. <bookmark mark='c'/> The edge labels are stored as two "
            "pointers into the text, so the whole tree takes linear space. <bookmark mark='d'/> To find a "
            "pattern, walk down from the root: m steps, however long the text, and the leaves below the end of the "
            "walk are its occurrences. A n a ends inside the branch with two leaves, at positions one and three."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.15), *[FadeIn(x) for x in dots.values()],
                      run_time=3.0)
            self.play(FadeIn(side[0]))
            for mk, s_ in zip("bcd", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(s_))
        self.wait(0.3)
        self.clear_scene()

    def uses(self):
        s = load("sa")
        head = label(r"What a suffix tree answers", font_size=34).to_edge(UP, buff=0.35)
        rows = VGroup(
            label(r"\textbf{longest repeated substring}: \ the deepest branching node", font_size=22, color=DATA),
            label(rf"in \textit{{Moby-Dick}}: \ {s['md_repeat_len']} characters, \ a chapter title that appears in the "
                  r"contents and again in the text", font_size=20, color=GREY_A),
            label(r"\textbf{longest common substring} of two texts: \ one tree for both \ (generalized), \ $O(n)$",
                  font_size=22, color=LAM),
            label(r"\textbf{number of distinct substrings}: \ the total length of all edges", font_size=22,
                  color=YES),
            label(rf"in \textit{{Moby-Dick}}: \ {big(s['md_distinct_substrings'])}", font_size=20, color=GREY_A),
            label(r"building it: \ Weiner (1973), \ McCreight (1976), \ Ukkonen (1995, \ online); \ Farach (1997) "
                  r"for large alphabets", font_size=20, color=WHITE),
            label(r"the catch: \ 10--20 bytes per character \ (pointers, \ child lists, \ suffix links)", font_size=22,
                  color=NO),
        ).arrange(DOWN, buff=0.27).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "Many questions become walks in this tree. <bookmark mark='a'/> The longest repeated substring is "
            "the deepest branching node. <bookmark mark='b'/> In Moby-Dick, it is a chapter title of a hundred "
            "characters, which appears in the table of contents and again at the head of its chapter. <bookmark "
            "mark='c'/> Put two texts in one tree, and the deepest node with leaves from both gives their longest "
            "common substring in linear time, which dynamic programming needs quadratic time for. <bookmark "
            "mark='d'/> The number of distinct substrings is just the total length of all the edges: <bookmark "
            "mark='e'/> for Moby-Dick, seven hundred and forty-one billion. <bookmark mark='f'/> Peter Weiner first "
            "built the tree in linear time in 1973; Esko Ukkonen's 1995 algorithm builds it online, a character at a "
            "time. <bookmark mark='g'/> The catch is memory: ten to twenty bytes for every character of text. For "
            "the novels, half a gigabyte. The next chapter keeps almost all the power in a fraction of the space."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdefg", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
