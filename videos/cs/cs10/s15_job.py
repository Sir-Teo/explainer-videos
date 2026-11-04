from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs10.common import (BG, CORE_COLORS, COST, CTRL, DATA, FUNC, HEAD, NO, PART, YES, bar_chart,
                                   grid_table, load)

MHZ = 884.9557522123894e6


class Job(VoiceoverScene):
    def construct(self):
        self.card()
        self.pebble()
        self.native()
        self.ledger()

    def card(self):
        card = chapter_card(14, r"The Job on four cores", r"What do four cores buy the Job?", part=PART)
        with self.voiceover("Chapter fourteen. The Job on four cores."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def pebble(self):
        sp = load("split")
        four = next(r for r in sp["rows"] if r["p"] == 4)
        cnt = [c / MHZ for c in four["shard_cycles"]]
        part = [c / MHZ for c in four["part_merge"]]
        total = four["seconds"]["partitioned"]
        head = label(r"Four Pebble cores, \ step by step", font_size=34).to_edge(UP, buff=0.3)
        scale = 0.75
        x0 = -5.4
        gn, gc, gm = VGroup(), VGroup(), VGroup()
        T = max(cnt)
        for k in range(4):
            y = 1.2 - k * 0.6
            gn.add(label(rf"core {k}", font_size=18, color=CORE_COLORS[k]).next_to([x0, y, 0], LEFT, buff=0.15))
            gc.add(Rectangle(width=cnt[k] * scale, height=0.4, stroke_width=0, fill_color=CORE_COLORS[k],
                             fill_opacity=0.55).move_to([x0 + cnt[k] * scale / 2, y, 0]))
            gm.add(Rectangle(width=max(part[k] * scale, 0.03), height=0.4, stroke_width=0, fill_color=YES,
                             fill_opacity=0.95).move_to([x0 + (T + part[k] / 2) * scale, y, 0]))
        axis = Line([x0, -1.0, 0], [x0 + 13 * scale, -1.0, 0], color=GREY_C)
        ticks = VGroup(*[label(rf"{s} s", font_size=15, color=GREY_B).next_to([x0 + s * scale, -1.0, 0], DOWN,
                                                                             buff=0.08) for s in (0, 4, 8, 12)])
        stats = VGroup(
            label(rf"counting: \ {min(cnt):.1f} to {max(cnt):.1f} s \ (the last quarter has the most distinct words)",
                  font_size=21, color=GREY_A),
            label(rf"merging, \ partitioned: \ {max(part):.2f} s", font_size=21, color=YES),
            label(rf"in all: \ {total:.2f} s, \ against {sp['one']['seconds']:.1f} s on one core: \ "
                  rf"{sp['one']['seconds'] / total:.2f} times faster", font_size=23, color=HEAD),
            label(rf"work {four['work_seconds']:.1f} s, \ less than one core's: \ the four tables are shorter", font_size=21,
                  color=DATA),
            label(rf"idle while the slowest core finishes: \ {100 * (1 - sum(cnt) / (4 * max(cnt))):.0f}\% \ "
                  r"(smaller pieces and work stealing would even it out)", font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now the full picture on four of Part 8's cores. <bookmark mark='a'/> Each core counts its quarter of "
            "the books. They do not finish together: the last quarter holds books with the largest vocabularies, so "
            "its table grows longest. <bookmark mark='b'/> Then the partitioned merge, a fraction of a second. "
            "<bookmark mark='c'/> In all, about twelve seconds, against fifty-seven on one core: four point eight "
            "times faster. <bookmark mark='d'/> The total work is less than one core's, because the four tables are "
            "shorter. <bookmark mark='e'/> And some of the time is wasted: three cores sit idle while the slowest "
            "finishes. Cutting the text into many smaller pieces and letting idle cores steal them, the scheduler of "
            "chapter nine, would even that out."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(ticks))
            vo.wait_until("a")
            self.play(FadeIn(gn), LaggedStart(*[GrowFromEdge(b, LEFT) for b in gc], lag_ratio=0.15), FadeIn(stats[0]))
            vo.wait_until("b")
            self.play(FadeIn(gm), FadeIn(stats[1]))
            for mk, st in zip("cde", stats[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(st))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def native(self):
        jc = {(r["threads"], r["simd"]): r for r in load("jobc")["rows"]}
        th = load("threads")["rows"]
        head = label(r"And on this computer's four cores", font_size=34).to_edge(UP, buff=0.3)
        rows = []
        base = jc[(1, False)]["seconds"]
        for (t, s) in ((1, False), (1, True), (2, False), (2, True), (4, False), (4, True)):
            r = jc[(t, s)]
            rows.append([rf"{t}", r"AVX2" if s else r"scalar", rf"{r['count']:.2f} s", rf"{r['merge']:.2f} s",
                         rf"{r['seconds']:.2f} s", rf"{base / r['seconds']:.1f}$\times$"])
        colors = [[GREY_A, YES if r[1] == "AVX2" else GREY_B, GREY_A, GREY_A, HEAD, YES] for r in rows]
        t = grid_table([r"threads", r"scan", r"count", r"merge", r"total", r"speedup"], rows,
                       [1.4, 1.5, 1.7, 1.7, 1.8, 1.7], row_h=0.48, font_size=21, colors=colors,
                       mono_cols=()).move_to(UP * 0.4)
        cap = VGroup(
            label(r"the same algorithm as Pebble's, \ in C; \ the top twenty checked against the reference",
                  font_size=19, color=GREY_B),
            label(rf"this machine's four cores, \ measured on pure arithmetic: \ {th[-1]['throughput']:.1f} times one",
                  font_size=19, color=GREY_B),
            label(rf"four cores and 32-wide vectors together: \ {base / jc[(4, True)]['seconds']:.0f} times faster "
                  r"than one plain core", font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The same experiment, for real, on this computer, with the C version of the Job. <bookmark mark='a'/> "
            f"One thread, scalar: {base:.0f} seconds. With AVX2, {jc[(1, True)]['seconds']:.0f}. Two threads, then "
            f"four: the four-thread scalar version takes {jc[(4, False)]['seconds']:.1f} seconds, again a little "
            "more than four times faster, for the same reason as on Pebble. <bookmark mark='b'/> And four threads "
            f"with vectors: {jc[(4, True)]['seconds']:.1f} seconds, {base / jc[(4, True)]['seconds']:.0f} times faster "
            "than where we started. Parallelism across cores and parallelism within a core multiply."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule), FadeIn(cap[0]), FadeIn(cap[1]))
            vo.wait_until("a")
            for r in range(1, 6):
                self.play(FadeIn(VGroup(*t.cells[r])), run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*t.cells[6])), FadeIn(cap[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        sp = load("split")
        led = sp["ledger"]
        head = label(r"Ledger row 4", font_size=38).to_edge(UP, buff=0.35)
        rows = led + [{"part": p_, "label": t} for p_, t in ((13, r"an optimizing compiler"), (16, r"sort, then count"),
                                                             (17, r"a hash table"))]
        tab = ledger_table(rows, shown=5, highlight=(4,), font_size=21, row_h=0.4, label_width=4.8).move_to(DOWN * 0.3)
        res = label(rf"{human_time(led[3]['seconds'])} $\to$ {human_time(led[4]['seconds'])}: \ four cores, \ "
                    r"partly by splitting the work, \ partly by shrinking it", font_size=25, color=COST).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "So the ledger gets its fifth row. Thirty novels: four and a half minutes on Part 6's single-cycle "
            "Pebble, two and a half with a pipeline, under a minute out of order, the same with real caches, and now "
            "twelve seconds on four cores. <bookmark mark='a'/> But be honest about where this one came from. Part of "
            "it is parallelism. Part is that splitting the text shortened the tables, which means the Job's real "
            "problem is still its algorithm: every word pays for a scan of the vocabulary. That ends this act. Act "
            "Three teaches the machine to understand a language, and in Act Four, Parts 16 and 17 replace the scan "
            "itself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), LaggedStart(*[FadeIn(r) for r in tab.rows], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()
