from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs10.common import (BG, CORE_COLORS, CTRL, DATA, FUNC, HEAD, NO, PART, YES, bar_chart, core_box,
                                   fmt, load)


class Multicore(WatchScene):
    def construct(self):
        self.card()
        self.shared()
        self.split()
        self.merges()

    def card(self):
        self.chapter(2, r"Four cores, \ one Job", r"How do you split a program across cores?", part=PART, said="Chapter two. Four cores, one Job.")

    # ------------------------------------------------------------------
    def shared(self):
        head = label(r"A shared-memory multicore", font_size=36).to_edge(UP, buff=0.35)
        cores = VGroup(*[core_box(k) for k in range(4)]).arrange(RIGHT, buff=0.55).shift(UP * 1.3)
        l1 = VGroup(*[RoundedRectangle(width=1.6, height=0.5, corner_radius=0.06, stroke_color=GREY_B,
                                       stroke_width=1.5).next_to(c, DOWN, buff=0.25) for c in cores])
        l1t = VGroup(*[label(r"L1, \ L2", font_size=18, color=GREY_B).move_to(b) for b in l1])
        l3 = RoundedRectangle(width=cores.width, height=0.6, corner_radius=0.08, stroke_color=DATA,
                              stroke_width=2).next_to(l1, DOWN, buff=0.45)
        l3t = label(r"shared last-level cache", font_size=20, color=DATA).move_to(l3)
        mem = RoundedRectangle(width=cores.width, height=0.7, corner_radius=0.08, stroke_color=NO,
                               stroke_width=2).next_to(l3, DOWN, buff=0.4)
        memt = label(r"shared address space, \ subject to protection and ordering rules", font_size=20, color=NO).move_to(mem)
        links = VGroup(*[Line(b.get_bottom(), [b.get_x(), l3.get_top()[1], 0], color=GREY_C, stroke_width=2)
                         for b in l1], Line(l3.get_bottom(), mem.get_top(), color=GREY_C, stroke_width=3))
        with self.voiceover(
            (
            "A multicore chip is several complete processors on one piece of silicon. <bookmark mark='a'/> In our "
            "example, each core has its own pipeline, registers and private caches; actual sharing hierarchies "
            "vary. <bookmark mark='b'/> They share a larger cache, and behind it one memory: the threads share an "
            "address space, subject to protection and the machine memory model. That sharing is the convenience "
            "and the danger. It is convenient because threads of one program can pass data by simply writing it "
            "to memory. It is dangerous because each core keeps copies of memory in its private caches, and two "
            "cores can disagree about what an address holds. Chapters three to six are about that danger. First, "
            "the Job."
        )
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in cores], lag_ratio=0.2), FadeIn(l1), FadeIn(l1t), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until("b")
            self.play(Create(links), FadeIn(l3), FadeIn(l3t), FadeIn(mem), FadeIn(memt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def split(self):
        self.ask(r"Split the Job across four cores. \\ How much faster?", [r"less than $4\times$",
                 r"exactly $4\times$", r"more than $4\times$"], 2,
                 say="Split the Job's text into four pieces, one per core. How much faster does it get?",
                 reveal="More than four times. Each quarter of the text has a smaller word table, so each lookup is shorter.")
        head = label(r"The plan: \ count in parallel, \ then combine", font_size=34).to_edge(UP, buff=0.35)
        text = Rectangle(width=10.0, height=0.5, stroke_color=GREY_B, stroke_width=1.5).shift(UP * 1.6)
        tl = label(rf"thirty novels, \ {load('split')['one']['bytes'] / 1e6:.0f} MB of text", font_size=20, color=GREY_B).next_to(text, UP, buff=0.12)
        cuts = VGroup(*[DashedLine(text.get_corner(UL) + RIGHT * 2.5 * k, text.get_corner(DL) + RIGHT * 2.5 * k,
                                   color=HEAD, stroke_width=2) for k in (1, 2, 3)])
        pieces = VGroup(*[Rectangle(width=2.5, height=0.5, stroke_width=0, fill_color=CORE_COLORS[k],
                                    fill_opacity=0.35).move_to(text.get_left() + RIGHT * (1.25 + 2.5 * k))
                          for k in range(4)])
        cores = VGroup(*[core_box(k, w=1.5, h=0.7, font_size=20).move_to(
            [pieces[k].get_x(), 0.3, 0]) for k in range(4)])
        arrows = VGroup(*[Arrow(pieces[k].get_bottom(), cores[k].get_top(), buff=0.08, color=CORE_COLORS[k],
                                stroke_width=2.5) for k in range(4)])
        tables = VGroup(*[VGroup(Rectangle(width=1.5, height=1.0, stroke_color=CORE_COLORS[k], stroke_width=1.5),
                                 label(r"its own \\ table", font_size=17, color=CORE_COLORS[k])).move_to(
            [pieces[k].get_x(), -1.1, 0]) for k in range(4)])
        for t in tables:
            t[1].move_to(t[0])
        comb = label(r"then: \ combine four tables into one, \ and print the top twenty", font_size=24,
                     color=HEAD).to_edge(DOWN, buff=0.5)
        rule = note(r"private counting tables; \ shared read-only input; \ merge synchronization still required", font_size=19
                    ).next_to(comb, UP, buff=0.25)
        with self.voiceover(
            (
            "Here is the plan. <bookmark mark='a'/> Cut the text into four pieces of equal size, at word "
            "boundaries. <bookmark mark='b'/> Each core counts the words of its piece, using Part 6's linear-scan "
            "counting algorithm in an abstract feature model, in a table of its own. While they count, no core "
            "ever writes anything another core reads, which removes conflicting table updates. Shared input, "
            "allocation, boundaries and the final synchronization still need care. <bookmark mark='c'/> Then the "
            "four tables must be combined into one, before selecting the top twenty. The estimate prices counting "
            "and selected merge insertions on four of Part 8's cores at Pebble's clock, with the same model of "
            "the core that gave the ledger its fifty-seven seconds. It omits routing and hashing scans, "
            "communication, coherence, bandwidth contention, barriers and final output; it is a conditional "
            "compute-cost projection, not a full multicore execution."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(text), FadeIn(tl))
            vo.wait_until("a")
            self.play(Create(cuts), FadeIn(pieces))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), FadeIn(cores))
            self.play(FadeIn(tables), FadeIn(rule))
            vo.wait_until("c")
            self.play(FadeIn(comb))
        self.wait(0.3)
        self.clear_scene()


    # ------------------------------------------------------------------
    def merges(self):
        sp = load("split")
        four = next(r for r in sp["rows"] if r["p"] == 4)
        M = 884.9557522123894e6
        cnt = [c / M for c in four["shard_cycles"]]
        head = label(r"Combining: \ three ways", font_size=34).to_edge(UP, buff=0.3)
        scale = 0.45  # inches per second
        x0 = -5.6

        def gantt(y, merge, title, color):
            g = VGroup()
            t = label(title, font_size=20, color=color).move_to([x0 - 0.1, y + 0.55, 0], aligned_edge=LEFT)
            g.add(t)
            for k in range(4):
                yy = y - k * 0.24
                g.add(Rectangle(width=cnt[k] * scale, height=0.18, stroke_width=0, fill_color=CORE_COLORS[k],
                                fill_opacity=0.55).move_to([x0 + cnt[k] * scale / 2, yy, 0]))
                for s, e in merge.get(k, []):
                    g.add(Rectangle(width=(e - s) * scale, height=0.18, stroke_width=0, fill_color=color,
                                    fill_opacity=0.95).move_to([x0 + (s + e) / 2 * scale, yy, 0]))
            return g

        T = max(cnt)
        ser = four["serial_merge"] / M
        tree = four["tree_merge"] / M
        part = [c / M for c in four["part_merge"]]
        g1 = gantt(1.5, {0: [(T, T + ser)]}, rf"core 0 merges the other three tables: \ {T + ser:.1f} s", NO)
        lv = [[c / M for c in l] for l in four["tree_levels"]]
        g2 = gantt(-0.1, {0: [(T, T + lv[0][0]), (T + max(lv[0]), T + max(lv[0]) + lv[1][0])],
                          2: [(T, T + lv[0][1])]},
                   rf"a tree: \ two merges at once, \ then one: \ {T + tree:.1f} s", CTRL)
        g3 = gantt(-1.7, {k: [(T, T + part[k])] for k in range(4)},
                   rf"by word: \ core $k$ merges the words whose hash is $k$: \ {T + max(part):.1f} s", YES)
        axis = Line([x0, -2.7, 0], [x0 + 21 * scale, -2.7, 0], color=GREY_C, stroke_width=1.5)
        ticks = VGroup(*[label(rf"{s} s", font_size=15, color=GREY_B).next_to([x0 + s * scale, -2.7, 0], DOWN,
                                                                             buff=0.08) for s in (0, 5, 10, 15, 20)])
        why = note(r"merging into one big table is a long scan per entry; \ split by word, \ each core merges a "
                   r"quarter of the words into a table a quarter the size", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Now the four tables have to become one. <bookmark mark='a'/> The obvious way: when all four are done, "
            "core zero takes each entry of the other three tables and looks it up in its own, adding the count or "
            f"appending the word. But every lookup is a scan of a table that grows to fifty-eight thousand entries, "
            f"and there are ninety thousand lookups: {ser:.0f} seconds of one core working while three wait. "
            "<bookmark mark='b'/> A tree is no better: two merges at once, then a final one, and the final merge of "
            "two big tables costs nearly as much as before. <bookmark mark='c'/> The way that works is to split the "
            "combining by word instead of by table. Give every word a number from zero to three by a simple rule, "
            "here the sum of its letters, and let core k merge, from all four tables, only the words whose number is "
            f"k. Each core builds a quarter of the final table, so its scans are a quarter as long, and four run at "
            f"once. The merge shrinks to about {max(part):.1f} seconds."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(ticks))
            for mk, g in zip("abc", (g1, g2, g3)):
                vo.wait_until(mk)
                self.play(FadeIn(g))
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()

