from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, Shelves,
                                  bar_chart, box, fmt, load, mono)


class Assoc(VoiceoverScene):
    def construct(self):
        self.card()
        self.ways()
        self.replace()
        self.plru()
        self.measured()
        self.writes()

    def card(self):
        card = chapter_card(4, r"Associativity and replacement", r"When a line must go, which one?", lit=(1966,),
                            extra=((1966, r"Belady: \ the optimal policy"),), part=PART)
        with self.voiceover(
            "Chapter four. Associativity and replacement."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def ways(self):
        head = label(r"The same eight lines, \ arranged three ways", font_size=34).to_edge(UP, buff=0.35)
        a = Shelves(8, 1, w=0.9, h=0.32, font_size=12)
        b = Shelves(4, 2, w=0.9, h=0.32, font_size=12)
        c = Shelves(1, 8, w=0.5, h=0.32, set_labels=False)
        ga = VGroup(a, label(r"direct-mapped \\ 8 sets $\times$ 1 way", font_size=20, color=NO))
        gb = VGroup(b, label(r"2-way set-associative \\ 4 sets $\times$ 2 ways", font_size=20, color=DATA))
        gc = VGroup(c, label(r"fully associative \\ 1 set $\times$ 8 ways", font_size=20, color=YES))
        for g in (ga, gb, gc):
            g[1].next_to(g[0], DOWN, buff=0.3)
        row = VGroup(ga, gb, gc).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to(UP * 0.2)
        cost = label("more eligible ways; \\ mapping, replacement, latency and energy still matter", font_size=24,
                     color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Set associativity gives a line several eligible locations. <bookmark mark='a'/> One way per set is "
            "direct mapping. <bookmark mark='b'/> Two ways allow two lines with the same set index to coexist. "
            "<bookmark mark='c'/> Put every line in one set and the cache is fully associative. <bookmark mark='d'/> "
            "More ways require additional tag checks or other lookup machinery, with design-dependent latency and "
            "energy costs. At fixed total capacity the index changes as the number of sets falls. Actual "
            "associativities vary by core and cache level, and more ways do not guarantee fewer misses under every "
            "replacement policy and mapping."
        ) as vo:
            self.play(FadeIn(head))
            for mk, g in zip("abc", (ga, gb, gc)):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(g, shift=UP * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
            vo.wait_until("d")
            self.play(FadeIn(cost))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replace(self):
        head = label(r"A set is full: \ which line goes?", font_size=36).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"\textit{LRU}: \ the least recently used \ (a timestamp, \ or an order, \ per set)", font_size=25,
                  color=DATA),
            label("\\textit{tree pseudo-LRU}: \\ $w - 1$ direction bits; \\ one recency approximation", font_size=25, color=CTRL),
            label(r"\textit{FIFO}: \ the oldest arrival; \quad \textit{random}: \ any", font_size=25, color=INF),
            label(r"\textit{Belady's optimum} \ (1966): \ the one used furthest in the future \ (needs a crystal ball)",
                  font_size=25, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.1)
        with self.voiceover(
            "A miss to a full set requires a victim. <bookmark mark='a'/> LRU evicts the least recently referenced "
            "resident line, using past recency as a heuristic. <bookmark mark='b'/> Tree pseudo-LRU maintains a "
            "small direction tree; it approximates recency but does not reproduce exact LRU. Hardware also uses "
            "other policies. <bookmark mark='c'/> FIFO tracks insertion order; random replacement chooses a resident "
            "victim according to its random generator. <bookmark mark='d'/> Belady's MIN evicts the resident line "
            "whose next reference is farthest away. Its optimality assumes a fixed trace, capacity, initially "
            "specified state, uniform miss cost and the same forced-insertion rules. A fully associative MIN result "
            "is not a like-for-like replacement-only comparison with a set-associative cache."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plru(self):
        head = label(r"Tree pseudo-LRU: \ three bits for four ways", font_size=34).to_edge(UP, buff=0.35)
        ways = VGroup(*[box(1.2, 0.6, rf"\text{{way {k}}}", DATA, 20) for k in range(4)]).arrange(RIGHT, buff=0.35)
        ways.move_to(DOWN * 1.6)
        n0 = Circle(radius=0.32, color=CTRL).move_to(UP * 1.2)
        n1 = Circle(radius=0.32, color=CTRL).move_to(UP * 0.0 + LEFT * 1.6)
        n2 = Circle(radius=0.32, color=CTRL).move_to(UP * 0.0 + RIGHT * 1.6)
        edges = VGroup(Line(n0.get_bottom(), n1.get_top(), color=GREY_D), Line(n0.get_bottom(), n2.get_top(), color=GREY_D),
                       *[Line(n.get_bottom(), w.get_top(), color=GREY_D) for n, w in
                         ((n1, ways[0]), (n1, ways[1]), (n2, ways[2]), (n2, ways[3]))])
        bits = [0, 0, 0]

        def bitlabels():
            return VGroup(*[MathTex(str(b), font_size=30, color=CTRL).move_to(n) for b, n in zip(bits, (n0, n1, n2))])

        cur = bitlabels()
        rule = label(r"each bit points to the half used \textit{less} recently: \ follow the bits to the victim",
                     font_size=24, color=HEAD).to_edge(DOWN, buff=0.35)
        seq = [0, 2, 1]
        with self.voiceover(
            "A four-way set can represent approximate recency with three tree bits. <bookmark mark='a'/> Each bit "
            "points toward a subtree to consider for replacement. Touching a way updates its path to point away from "
            "that way. <bookmark mark='b'/> Follow the shown accesses to ways zero, two and one. Unvisited ways "
            "still need valid-bit and free-slot handling. <bookmark mark='c'/> Once the set is full, follow the tree "
            "to its candidate victim. It need not be the exact least recently used way. An arbitrary exact order of "
            "sixteen ways has sixteen factorial possibilities, requiring at least forty-five bits to encode; a tree "
            "uses fifteen direction bits. Real implementation state and update costs depend on the chosen encoding."
        ) as vo:
            self.play(FadeIn(head), Create(edges), Create(n0), Create(n1), Create(n2), FadeIn(ways), FadeIn(cur))
            vo.wait_until("a")
            self.play(FadeIn(rule))
            vo.wait_until("b")
            for w in seq:
                # point away from the used half
                bits[0] = 1 if w < 2 else 0
                if w < 2:
                    bits[1] = 1 if w == 0 else 0
                else:
                    bits[2] = 1 if w == 2 else 0
                new = bitlabels()
                self.play(Indicate(ways[w], color=YES), Transform(cur, new), run_time=0.9)
            vo.wait_until("c")
            v = (2 + (0 if bits[2] == 0 else 1)) if bits[0] else (0 if bits[1] == 0 else 1)
            self.play(Indicate(ways[v], color=NO, scale_factor=1.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        d = load("policies")["rows"]["4"]
        head = label(r"Chapter 1: \ 4 KiB; \ eight-way policies versus fully associative MIN", font_size=30).to_edge(UP, buff=0.35)
        keys = ["lru", "plru", "fifo", "random", "opt (fully associative)"]
        names = [r"LRU", r"pseudo-LRU", r"FIFO", r"random", r"Belady"]
        vals = [100 * d[k] for k in keys]
        ch = bar_chart(vals, names, [DATA, CTRL, INF, FUNC, YES], height=3.6, bar_w=1.1, gap=0.9, font_size=22,
                       fmt_=lambda v: rf"{v:.1f}\%").move_to(DOWN * 0.3)
        yl = note(r"miss rate", font_size=20).next_to(ch, UP, buff=0.2).align_to(ch, LEFT)
        punch = label(r"random beats LRU here: \ a scan longer than the cache is LRU's worst case", font_size=26,
                      color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Replay the same chapter-1 data references from an empty four-kibibyte cache. <bookmark mark='a'/> The "
            "LRU, pseudo-LRU and FIFO bars use eight-way sets. <bookmark mark='b'/> The seeded random policy has "
            "fewer misses on this trace. A single seed is not a distribution-wide performance guarantee. <bookmark "
            "mark='c'/> The MIN bar has the same capacity but is fully associative, so it also removes set-placement "
            "restrictions. <bookmark mark='d'/> Repeated scans slightly longer than a cache can punish LRU: each "
            "next reference finds its line just evicted. Random replacement sometimes preserves useful lines. "
            "Performance still depends on scan lengths, intervening accesses, mapping and policy; measured miss "
            "ratios do not directly give execution-time speedups."
        ) as vo:
            self.play(FadeIn(head), FadeIn(yl), FadeIn(ch[0]))
            for mk, ks in (("a", [0, 1, 2]), ("b", [3]), ("c", [4])):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(*[GrowFromEdge(ch.bars[k], DOWN) for k in ks], *[FadeIn(ch.vals[k]) for k in ks],
                          *[FadeIn(ch.names[k]) for k in ks])
                if mk == 'a':
                    vo.wait_until(mk)
            vo.wait_until("d")
            self.play(FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def writes(self):
        head = label(r"And writes?", font_size=38).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"\textit{write-through}: \ every store goes on to the next level too; \ simple, \ and traffic-heavy",
                  font_size=25, color=INF),
            label(r"\textit{write-back}: \ mark the line dirty; \ write it out only when it is evicted", font_size=25,
                  color=DATA),
            label(r"\textit{write-allocate}: \ a store that misses brings the line in \ (or not: \ "
                  r"\textit{no-write-allocate})", font_size=25, color=CTRL),
            label("common policies vary; \\ hierarchy timing omits full write/coherence traffic",
                  font_size=25, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.1)
        with self.voiceover(
            "Stores add propagation and allocation choices. <bookmark mark='a'/> Write-through sends a store toward "
            "the next level, often through a buffer. It does not by itself make every copy or DRAM instantly "
            "current. <bookmark mark='b'/> Write-back marks a line dirty and propagates it on eviction or another "
            "required action, such as a flush or coherence request. Repeated updates can be combined while the line "
            "remains resident. <bookmark mark='c'/> Write-allocate brings a missed store's line into the cache; "
            "no-write-allocate can send the store onward instead. Partial stores and coherence ownership complicate "
            "real traffic. <bookmark mark='d'/> Our single-cache simulator counts dirty evictions and write-through "
            "events. The hierarchy's demand-latency model does not price complete write-back, coherence or bandwidth "
            "traffic."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()
