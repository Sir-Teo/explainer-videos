from __future__ import annotations

import bisect
import random

from explainer.cs import *  # noqa: F403
from explainer.cs.db.bptree import BPlusTree
from videos.cs.cs35.common import (CODE, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono, num)

WORDS = "the whale ship sea ahab call me ishmael white boat oil sail".split()


def node_box(keys, color, leaf):
    cells = VGroup(*[VGroup(Rectangle(width=0.95, height=0.46, stroke_color=color, stroke_width=1.6,
                                      fill_color=BLACK, fill_opacity=0.0),
                            Text(k, font="DejaVu Sans Mono", font_size=15, color=CODE if leaf else color))
                     for k in keys]).arrange(RIGHT, buff=0)
    for c in cells:
        c[1].move_to(c[0])
    if not keys:
        cells = VGroup(Rectangle(width=0.5, height=0.46, stroke_color=color))
    return cells


def draw_tree(t: BPlusTree, width=12.5, top=1.6, dy=1.25):
    levels = [[t.root]]
    while not levels[-1][0].leaf:
        levels.append([c for n in levels[-1] for c in n.kids])
    g = VGroup()
    g.boxes = {}
    for d, lv in enumerate(levels):
        row = VGroup(*[node_box(n.keys, YES if n.leaf else HEAD, n.leaf) for n in lv])
        row.arrange(RIGHT, buff=0.35 if lv[0].leaf else 0.9)
        if row.width > width:
            row.width = width
        row.move_to([0, top - d * dy, 0])
        for n, b in zip(lv, row):
            g.boxes[id(n)] = b
        g.add(row)
    edges = VGroup()
    for lv in levels[:-1]:
        for n in lv:
            b = g.boxes[id(n)]
            for i, c in enumerate(n.kids):
                x = b.get_left()[0] + i * b.width / max(len(n.kids) - 1, 1)
                edges.add(Line([x, b.get_bottom()[1], 0], g.boxes[id(c)].get_top(), color=GREY_C, stroke_width=1.4))
    links = VGroup()
    leaves = levels[-1]
    for a, b in zip(leaves, leaves[1:]):
        links.add(Arrow(g.boxes[id(a)].get_right(), g.boxes[id(b)].get_left(), buff=0.03, color=YES,
                        stroke_width=1.5, max_tip_length_to_length_ratio=0.3))
    g.add(edges, links)
    g.edges, g.links, g.levels = edges, links, levels
    return g


class Indexes(VoiceoverScene):
    def construct(self):
        self.card()
        self.grow()
        self.fanout()
        self.clustering()

    def card(self):
        card = chapter_card(8, r"Indexes", r"How do you find one row among billions in three reads?",
                            lit=(1972, 1979), extra=((1972, r"Bayer and McCreight: \ B-trees"),
                                                     (1979, r"Comer: \ the ubiquitous B-tree")), part=PART)
        with self.voiceover("Chapter eight. Indexes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def grow(self):
        head = label(r"A B+ tree, \ grown one key at a time", font_size=36).to_edge(UP, buff=0.3)
        t = BPlusTree(order=4)
        snaps = {}
        for k, w in enumerate(WORDS, start=1):
            t.insert(w, k)
            if k in (3, 4, 8, 12):
                snaps[k] = draw_tree(t)
        cap = {3: r"a leaf holds up to three keys, \ sorted", 4: r"a fourth key: \ the leaf splits, \ and a copy of "
               r"its middle key goes up as a separator",
               8: r"more splits; \ the root gathers separators", 12: r"the root splits: \ the only way the tree "
               r"grows taller, \ so every leaf stays at the same depth"}
        caps = {k: label(v, font_size=20, color=WHITE).to_edge(DOWN, buff=1.2) for k, v in cap.items()}
        count = {k: label(rf"{k} keys inserted:  " + r", \ ".join(rf"\texttt{{{w}}}" for w in WORDS[:k]),
                          font_size=16, color=GREY_B).next_to(head, DOWN, buff=0.2) for k in snaps}
        final = snaps[12]
        lines = VGroup(
            label(r"search for \texttt{whale}: \ one node per level: \ $\ge$ \texttt{sea}, \ go right; \ $\ge$ "
                  r"\texttt{the}, \ go right; \ found in the leaf", font_size=19, color=HEAD),
            label(r"a range: \ find the first leaf, \ then follow the links", font_size=19, color=YES),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The index nearly every database uses is the B-tree of Rudolf Bayer and Edward McCreight, from 1972, in "
            "the variant called the B-plus tree. Here we insert twelve words from Moby Dick into a tiny one, where "
            "each node holds at most three keys. <bookmark mark='a'/> The first three go into one leaf, in order. "
            "<bookmark mark='b'/> The fourth overflows it. The leaf splits into two, and a copy of the first key of "
            "the right half goes up into a new root, as a separator: smaller keys to the left, others to the right. "
            "<bookmark mark='c'/> More inserts, more leaf splits, and each split adds a separator to the root. "
            "<bookmark mark='d'/> When the root itself is full, it splits, and a new root appears above it. That is "
            "the only way the tree grows taller, so every leaf is always at the same depth, and the tree is always "
            "balanced. <bookmark mark='e'/> To search, start at the root and follow the separators down, one node per "
            "level. <bookmark mark='f'/> And all the keys are in the leaves, linked in order, so a range is a search "
            "for its first key followed by a walk along the leaves."
        ) as vo:
            self.play(FadeIn(head))
            prev = None
            for mk, k in zip("abcd", (3, 4, 8, 12)):
                vo.wait_until(mk)
                new = VGroup(snaps[k], caps[k], count[k])
                if prev is None:
                    self.play(FadeIn(new))
                else:
                    self.play(FadeOut(prev), FadeIn(new))
                prev = new
            vo.wait_until("e")
            self.play(FadeOut(caps[12]), FadeIn(lines[0]))
            boxes = [final.boxes[id(final.levels[0][0])]]
            n = final.levels[0][0]
            while not n.leaf:
                n = n.kids[bisect.bisect_right(n.keys, "whale")]
                boxes.append(final.boxes[id(n)])
            for b in boxes:
                self.play(Indicate(b, color=KERN, scale_factor=1.12), run_time=0.6)
            vo.wait_until("f")
            self.play(FadeIn(lines[1]), LaggedStart(*[Indicate(a, color=YES) for a in final.links], lag_ratio=0.2))
        self.wait(0.3)
        self.clear_scene()

    def fanout(self):
        b = load("btree")
        head = label(r"Wide nodes, \ few levels", font_size=36).to_edge(UP, buff=0.3)
        lv = [r for r in b["levels"] if r["rows"] in (10 ** 3, 10 ** 5, 10 ** 6, 10 ** 8, 10 ** 9, 10 ** 11, 10 ** 12)]
        tab = grid_table([r"keys", r"levels, \ fanout 400"],
                         [[rf"$10^{{{len(str(r['rows'])) - 1}}}$", str(r["levels"])] for r in lv],
                         widths=[2.0, 2.8], row_h=0.42, font_size=20, mono_cols=())
        tab.move_to([-4.3, -0.2, 0])
        for r in range(1, len(lv) + 1):
            tab.cells[r][1].set_color(YES)
        lines = VGroup(
            label(r"a real node is a page: \ 4 KiB holds about 400 keys \\ and pointers, \ so each level multiplies "
                  r"the reach by 400", font_size=20, color=WHITE),
            label(r"a trillion keys in five levels; \ the top levels stay in \\ memory, \ so a lookup costs about "
                  r"one disk read", font_size=20, color=HEAD),
            label(rf"our index on the Job's \texttt{{word}} column: \ {num(b['distinct'])} \\ distinct words, \ "
                  rf"{num(b['rows'])} rows: \ height {b['height']}, \ {b['nodes']} nodes", font_size=20, color=YES),
            label(r"a binary tree would need 16 levels for those words: \\ Part 17's balanced trees suit memory, \ "
                  r"not disks", font_size=20, color=NO),
            label(r"each insert may split a few nodes: \ $O(\log_{400} n)$ pages; \\ every index on a table slows "
                  r"its writes", font_size=20, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        lines.next_to(tab, RIGHT, buff=0.7)
        with self.voiceover(
            "In a real database each node is a page of the disk. <bookmark mark='a'/> A four-kilobyte page holds "
            "about four hundred keys and pointers, so each level multiplies the number of keys reachable by four "
            "hundred. <bookmark mark='b'/> A thousand keys need two levels, a million three, a billion four, a "
            "trillion five. The top levels are small enough to stay in memory, so finding any key costs about one "
            "read from the disk. <bookmark mark='c'/> Our database's index on the Job's word column covers four point "
            "six million rows and fifty-eight thousand distinct words in a tree two levels high. "
            "<bookmark mark='d'/> A binary search tree, from Part 17, would be at least sixteen levels deep, and on a "
            "disk each level is a seek. <bookmark mark='e'/> The price is paid on writes: each insert may split nodes, "
            "and a table with five indexes does six writes for every new row."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def clustering(self):
        b = load("btree")
        head = label(r"Where the rows are matters", font_size=36).to_edge(UP, buff=0.3)
        sub = label(rf"\texttt{{word BETWEEN 'whale' AND 'whales'}}: \ {num(b['hits'])} rows of the Job's "
                    rf"{num(b['rows'])}", font_size=20, color=WHITE).next_to(head, DOWN, buff=0.3)
        rng = random.Random(4)
        strip_u = VGroup(*[Rectangle(width=0.11, height=0.5, stroke_width=0, fill_color=GREY_D, fill_opacity=0.6)
                           for _ in range(100)]).arrange(RIGHT, buff=0.02)
        strip_c = strip_u.copy()
        for k in rng.sample(range(100), 21):
            strip_u[k].set_fill(NO, 0.95)
        for k in range(40, 41):
            strip_c[k].set_fill(YES, 0.95)
        ul = label(rf"\textbf{{unclustered}}: \ rows lie in book order, \ so they fall on {num(b['pages_unclustered'])} "
                   r"different pages", font_size=19, color=NO)
        cl = label(rf"\textbf{{clustered}}: \ the table itself is stored in \texttt{{word}} order: \ "
                   rf"{b['pages_clustered']} pages", font_size=19, color=YES)
        gu = VGroup(ul, strip_u).arrange(DOWN, buff=0.15)
        gc = VGroup(cl, strip_c).arrange(DOWN, buff=0.15)
        VGroup(gu, gc).arrange(DOWN, buff=0.45).next_to(sub, DOWN, buff=0.45)
        kinds = VGroup(
            label(r"a table can be clustered on only one key; \ the optimizer weighs this when it costs an index scan",
                  font_size=19, color=WHITE),
            label(r"\textbf{hash} index: \ equality only, \ one probe; \ \textbf{bitmap}: \ a bit per row per value, "
                  r"for analytics", font_size=19, color=HEAD),
            label(r"\textbf{LSM tree} \ (Part 34): \ for write-heavy stores; \ \textbf{inverted} index: \ word to "
                  r"documents, \ for search", font_size=19, color=LAM),
            label(r"a \textbf{covering} index holds every column a query needs: \ the table is never read",
                  font_size=19, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Finding keys in the index is only half of the work: the rows themselves must be fetched. "
            "<bookmark mark='a'/> Take the range from whale to whales: seventeen hundred rows of the Job's four point "
            "six million. <bookmark mark='b'/> The words table is stored in the order of the books, so those rows are "
            "scattered, and fetching them touches 966 different pages, more than one for every two rows. "
            "<bookmark mark='c'/> If the table were stored sorted by word, clustered on that key, the same rows would "
            "sit together on eighteen pages, fifty times fewer. <bookmark mark='d'/> A table can be in only one order, "
            "so it can be clustered on only one key, and the optimizer accounts for this when it estimates the cost "
            "of using an index. <bookmark mark='e'/> There are other kinds of index for other jobs: hash indexes for "
            "pure equality, bitmaps for analytics, the LSM trees of Part 34 for heavy writing, and inverted indexes "
            "for text. <bookmark mark='f'/> And an index that contains every column a query needs answers it "
            "without reading the table at all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sub))
            vo.wait_until("b")
            self.play(FadeIn(gu))
            vo.wait_until("c")
            self.play(FadeIn(gc))
            vo.wait_until("d")
            self.play(FadeIn(kinds[0]))
            vo.wait_until("e")
            self.play(FadeIn(kinds[1]), FadeIn(kinds[2]))
            vo.wait_until("f")
            self.play(FadeIn(kinds[3]))
        self.wait(0.3)
        self.clear_scene()


_ = (DATA, mono, NO)
