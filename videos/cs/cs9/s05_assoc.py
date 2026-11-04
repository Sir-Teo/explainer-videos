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
        with self.voiceover("Chapter four. Associativity and replacement."):
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
        cost = label(r"more ways: \ fewer conflicts, \ but every lookup compares more tags at once", font_size=24,
                     color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The cure for conflicts is to give each address a choice. Group the lines into sets; an address's index "
            "picks a set, and the line may go in any of the set's ways. <bookmark mark='a'/> With one way per set, "
            "this is the direct-mapped cache. <bookmark mark='b'/> With two ways, two lines that share an index can "
            "live side by side. <bookmark mark='c'/> With all the lines in a single set, any address can go anywhere: "
            "fully associative. <bookmark mark='d'/> More ways means fewer conflicts, but on every access the cache "
            "must compare the tag against every way of the set at once, in parallel, which costs energy and time. "
            "First-level caches today are typically eight- to twelve-way; larger, slower levels sixteen or more."
        ) as vo:
            self.play(FadeIn(head))
            for mk, g in zip("abc", (ga, gb, gc)):
                vo.wait_until(mk)
                self.play(FadeIn(g, shift=UP * 0.1))
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
            label(r"\textit{tree pseudo-LRU}: \ $w - 1$ bits per set point away from recent use \ (what hardware "
                  r"usually does)", font_size=25, color=CTRL),
            label(r"\textit{FIFO}: \ the oldest arrival; \quad \textit{random}: \ any", font_size=25, color=INF),
            label(r"\textit{Belady's optimum} \ (1966): \ the one used furthest in the future \ (needs a crystal ball)",
                  font_size=25, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.1)
        with self.voiceover(
            "When an access misses and its set is full, one line must go. <bookmark mark='a'/> The natural choice is "
            "the least recently used, LRU: the line whose last use is oldest, betting that the past predicts the "
            "future. Keeping an exact order is costly in an eight-way set, <bookmark mark='b'/> so hardware usually "
            "approximates it with a small tree of bits per set, each pointing away from the half used more recently: "
            "pseudo-LRU. <bookmark mark='c'/> Simpler still: evict the line that arrived first, or any line at "
            "random. <bookmark mark='d'/> And there is a perfect policy, found by László Bélády at IBM in 1966: evict "
            "the line whose next use is furthest in the future. No real cache can know the future, but a simulator "
            "replaying a trace can, which makes Belady's policy the yardstick for all the others."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
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
            "Here is how hardware approximates LRU cheaply. For a four-way set, keep three bits in a little tree. "
            "<bookmark mark='a'/> Each bit points towards the half of the set that was used less recently. Every "
            "access flips the bits on its path to point away from itself. <bookmark mark='b'/> Use way zero, then two, "
            "then one, and watch the bits. <bookmark mark='c'/> To choose a victim, follow the bits from the root: right, "
            "then right again, to way three, the one never used. In general they lead to a way that has not been used "
            "for a while, though not always the very least recent. "
            "Three bits instead of a full ordering; for sixteen ways, fifteen bits instead of forty-five."
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
        head = label(r"On the Job's first chapter, \ a 4 KB cache, \ 8 ways", font_size=32).to_edge(UP, buff=0.35)
        keys = ["lru", "plru", "fifo", "random", "opt (fully associative)"]
        names = [r"LRU", r"pseudo-LRU", r"FIFO", r"random", r"Belady"]
        vals = [100 * d[k] for k in keys]
        ch = bar_chart(vals, names, [DATA, CTRL, INF, FUNC, YES], height=3.6, bar_w=1.1, gap=0.9, font_size=22,
                       fmt_=lambda v: rf"{v:.1f}\%").move_to(DOWN * 0.3)
        yl = note(r"miss rate", font_size=20).next_to(ch, UP, buff=0.2).align_to(ch, LEFT)
        punch = label(r"random beats LRU here: \ a scan longer than the cache is LRU's worst case", font_size=26,
                      color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How much does the choice matter? Run the Job's first chapter through a four-kilobyte, eight-way cache. "
            "<bookmark mark='a'/> LRU misses about four percent of the accesses, and pseudo-LRU and FIFO about the "
            "same. <bookmark mark='b'/> Random replacement misses only two percent: it beats LRU. <bookmark mark='c'/> "
            "And Belady's crystal ball, three quarters of a percent. <bookmark mark='d'/> Random wins because of the "
            "Job's table scans. A scan that is a little longer than the cache is LRU's worst case: by the time the "
            "scan comes round again, LRU has thrown out exactly the line it is about to need, every time. Random "
            "keeps some lines by luck. We will meet this again, much larger, over all thirty novels."
        ) as vo:
            self.play(FadeIn(head), FadeIn(yl), FadeIn(ch[0]))
            for mk, ks in (("a", [0, 1, 2]), ("b", [3]), ("c", [4])):
                vo.wait_until(mk)
                self.play(*[GrowFromEdge(ch.bars[k], DOWN) for k in ks], *[FadeIn(ch.vals[k]) for k in ks],
                          *[FadeIn(ch.names[k]) for k in ks])
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
            label(r"today's caches: \ write-back and write-allocate, \ with a small buffer of stores in flight",
                  font_size=25, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.1)
        with self.voiceover(
            "Stores raise two more questions. <bookmark mark='a'/> When a store hits, does the new value go on to the "
            "next level at once? Write-through says yes: simple, and memory is always up to date, but every store "
            "becomes traffic. <bookmark mark='b'/> Write-back says no: mark the line dirty, and write it out only "
            "when it is evicted, so a line stored to a thousand times is written once. <bookmark mark='c'/> And when "
            "a store misses, does the line come into the cache? Write-allocate says yes, betting the program will "
            "touch it again. <bookmark mark='d'/> Almost every cache today is write-back and write-allocate. Our "
            "simulator does both, and Part 10 will meet the harder question these choices raise: when several cores "
            "each cache the same line, who sees which write?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
