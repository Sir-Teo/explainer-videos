from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs10.common import (BG, CORE_COLORS, CTRL, DATA, FUNC, HEAD, NO, PART, YES, bar_chart, core_box,
                                   fmt, load)


class Multicore(VoiceoverScene):
    def construct(self):
        self.card()
        self.shared()
        self.split()
        self.shards()
        self.merges()
        self.heaps()

    def card(self):
        card = chapter_card(2, r"Four cores, \ one Job", r"How do you split a program across cores?", part=PART)
        with self.voiceover("Chapter two. Four cores, one Job."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

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
    def shards(self):
        sp = load("split")
        one = sp["one"]
        four = next(r for r in sp["rows"] if r["p"] == 4)
        secs = [c / (884.9557522123894e6) for c in four["shard_cycles"]]
        head = label(r"Counting: \ each core's quarter", font_size=34).to_edge(UP, buff=0.35)
        ch = bar_chart(secs, [rf"core {k} \\ {four['shard_distinct'][k]:,} words" for k in range(4)],
                       CORE_COLORS, height=3.2, bar_w=1.1, gap=1.0, vmax=one["seconds"] / 4 * 1.15,
                       fmt_=lambda v: f"{v:.1f} s", font_size=20).move_to(DOWN * 0.3)
        y0 = ch.bars[0].get_bottom()[1]
        q = one["seconds"] / 4
        h = 3.2 * q / (one["seconds"] / 4 * 1.15)
        ql = DashedLine([ch.get_left()[0] - 0.2, y0 + h, 0], [ch.get_right()[0] + 0.2, y0 + h, 0], color=HEAD,
                        stroke_width=2.5)
        qlab = label(rf"a quarter of one core's time: \ {q:.1f} s", font_size=20, color=HEAD).next_to(ql, UP,
                                                                                                     buff=0.1)
        why = label(rf"private tables: \ {min(four['shard_distinct']):,}--{max(four['shard_distinct']):,} entries; \ "
                    r"many lookup prefixes shrink", font_size=22, color=YES).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            f"Each bar is one shard's fitted counting time. <bookmark mark='a'/> Perfect division of fifty-seven seconds would give about fourteen seconds per core. <bookmark mark='b'/> The projected slowest shard takes {max(secs):.0f} seconds, below that reference. <bookmark mark='c'/> A quarter of this text contains roughly half the full vocabulary. Smaller private tables reduce many lookup prefixes, so the total scan work falls. Common words can still be found near the front; not every lookup becomes exactly half as long. The feature model prices the actual shard features rather than assuming a universal factor of two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch[0]), FadeIn(ch.names))
            vo.wait_until("a")
            self.play(Create(ql), FadeIn(qlab))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(b, DOWN) for b in ch.bars], *[FadeIn(v) for v in ch.vals])
            vo.wait_until("c")
            self.play(FadeIn(why))
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

    # ------------------------------------------------------------------
    def heaps(self):
        sp = load("split")
        rows = sp["rows"]
        one = sp["one"]
        head = label(r"Why a quarter of the text has half the words", font_size=34).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[0, 5.5, 1], y_range=[0, 60000, 20000], x_length=6.5, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).shift(LEFT * 1.6 + DOWN * 0.4)
        pts = [(0, 0)] + [(np.log2(32 // r["p"]), np.mean(r["shard_distinct"])) for r in rows if r["p"] > 1] + [
            (5, one["distinct"])]
        pts = sorted(pts)
        xt = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(ax.c2p(x, 0), DOWN, buff=0.12) for x, t in
                      zip(range(6), [r"$\frac{1}{32}$", r"$\frac{1}{16}$", r"$\frac{1}{8}$", r"$\frac14$",
                                     r"$\frac12$", r"all"])])
        yt = VGroup(*[label(rf"{v // 1000}K", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (20000, 40000, 60000)])
        xl = label(r"fraction of the text \ (log scale)", font_size=18, color=GREY_B).next_to(ax, DOWN, buff=0.45)
        line = VMobject(color=DATA, stroke_width=4).set_points_as_corners([ax.c2p(x, y) for x, y in pts[1:]])
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.06, color=DATA) for x, y in pts[1:]])
        law = MathTex(r"V(n) \approx K n^{\beta}, \quad \beta \approx \tfrac12", font_size=36, color=HEAD).next_to(
            ax, RIGHT, buff=0.5).shift(UP * 0.8)
        lname = label(r"Heaps' law \ (1978): \ distinct words grow \\ like a power of the text, \ less than 1",
                      font_size=20, color=GREY_A).next_to(law, DOWN, buff=0.3)
        warn = label(r"superlinear model gain: \ shrinking tables reduces scan work; \ Part 16 changes the algorithm",
                     font_size=22, color=NO).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            (
            "Why does a quarter of the text hold half the vocabulary? <bookmark mark='a'/> Count the distinct "
            "words in a thirty-second of the corpus, a sixteenth, an eighth, and so on. The count grows, but more "
            "and more slowly: common words appear in every piece, and only rare ones are new. <bookmark "
            "mark='b'/> This is Heaps' law, named for Harold Heaps in 1978: the number of distinct words in a "
            "text of n words grows roughly like n to a power below one, often around one half in illustrative "
            "English corpora, with the fitted exponent depending on corpus and tokenization. <bookmark mark='c'/> "
            "So be careful with the Job's superlinear speedup. In this model it comes from reducing the work of a "
            "linear-scan dictionary: each lookup visits a prefix, possibly the whole vocabulary. This can become "
            "quadratic in the worst case; the observed corpus need not follow an exact quadratic law. Splitting "
            "the text makes the tables shorter, which is the same as making the algorithm better. In Part 16 a "
            "better algorithm removes the scan, and with it this free gift."
        )
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(dots), run_time=2)
            vo.wait_until("b")
            self.play(Write(law), FadeIn(lname))
            vo.wait_until("c")
            self.play(FadeIn(warn))
        self.wait(0.3)
        self.clear_scene()
