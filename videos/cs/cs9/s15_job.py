from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, bar_chart, fmt,
                                  load, sci, size_label)


class Job(VoiceoverScene):
    def construct(self):
        self.card()
        self.scans()
        self.price()
        self.ledger()

    def card(self):
        card = chapter_card(14, r"The Job meets memory", r"What do real caches cost the Job?", part=PART)
        with self.voiceover("Chapter fourteen. The Job meets memory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def scans(self):
        sc = load("scans")
        head = label(r"Thirty novels: \ the table's misses, \ counted exactly", font_size=34).to_edge(UP, buff=0.3)
        idea = VGroup(
            label(r"every scan reads lines $0, 1, \dots, e$ of the table", font_size=24, color=GREY_A),
            label(r"line $\ell$ hits in an LRU cache of $C$ lines \ $\iff$ \ the last scan that reached $\ell$ was "
                  r"shorter than $C$", font_size=24, color=HEAD),
            label(rf"so {sc['words'] / 1e6:.1f} million scans give all {sc['line_reads'] / 1e9:.1f} billion line reads' "
                  r"fates, \ in seconds", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.18).next_to(head, DOWN, buff=0.3)
        rows = sc["rows"]
        ax = Axes(x_range=[0, len(rows) - 1, 1], y_range=[0, 1, 0.25], x_length=8.0, y_length=2.8, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).to_edge(DOWN, buff=0.75)
        ax.y_axis.add_numbers([0, 0.5, 1], font_size=16, num_decimal_places=1)
        xt = VGroup(*[label(size_label(r["kb"] * 1024), font_size=15, color=GREY_B).next_to(ax.c2p(k, 0), DOWN,
                                                                                           buff=0.1)
                      for k, r in enumerate(rows)])
        lru = VMobject(color=NO, stroke_width=4).set_points_as_corners([ax.c2p(k, r["lru"]) for k, r in enumerate(rows)])
        front = VMobject(color=YES, stroke_width=4).set_points_as_corners(
            [ax.c2p(k, r["keep_front"]) for k, r in enumerate(rows)])
        ll = label(r"LRU", font_size=20, color=NO).next_to(ax.c2p(3, rows[3]["lru"]), UP, buff=0.1)
        lf = label(r"keep the front of the table", font_size=20, color=YES).next_to(ax.c2p(5, rows[5]["keep_front"]),
                                                                                   LEFT, buff=0.1)
        with self.voiceover(
            "Now the Job, over all thirty novels. Simulating three billion cache-line reads one by one would take "
            "hours, but the table scans have a structure that gives the answer exactly. <bookmark mark='a'/> Every "
            "scan reads the table's lines from the first up to some last line. <bookmark mark='b'/> Between one read of "
            "line l and the next, the lines touched are exactly the lines of the previous scan that reached l. So in "
            "an LRU cache of C lines, line l hits if and only if that scan was shorter than C. <bookmark mark='c'/> A "
            "stack of recent scan lengths then gives the fate of every one of the three billion reads from four and a "
            "half million scans, in seconds. <bookmark mark='d'/> The result: LRU misses almost every table read until "
            "the cache holds the whole table, which is the scan pathology of chapter four at full scale. A cache that "
            "simply kept the front of the table would do far better at every size: the Frontier chapter returns to "
            "that."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abc", idea):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(xt))
            self.play(Create(lru), FadeIn(ll), run_time=1.5)
            self.play(Create(front), FadeIn(lf), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def price(self):
        j = load("job")
        head = label(r"What the misses cost", font_size=36).to_edge(UP, buff=0.35)
        p = j["clocks"]["pebble"]
        n = j["clocks"]["this machine"]
        lines = VGroup(
            label(rf"in the corpus run: \ {100 * j['m_table']:.0f}\% of table reads and {100 * j['m_pool']:.0f}\% of "
                  r"letter reads miss L1", font_size=24, color=GREY_A),
            label(rf"at Pebble's 885 MHz \ (latencies {', '.join(map(str, p['latencies']))} cycles): \ the core hides "
                  rf"them: \ $+{100 * j['change']:.2f}\%$", font_size=24, color=YES),
            label(rf"turn off the prefetcher: \ $+{100 * j['no_prefetch_change']:.1f}\%$", font_size=24, color=CTRL),
            label(rf"the same memory at this machine's 2.8 GHz \ ({', '.join(map(str, n['latencies']))} cycles): \ "
                  rf"$+{100 * n['prefetch']['extra_cycles'] / j['row2']['cycles']:.0f}\%$", font_size=24, color=NO),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 0.1)
        with self.voiceover(
            "What do all those misses cost? We measured it on Part 8's core, running the scan with this machine's "
            "latencies converted to Pebble's clock, and the letter comparisons too, and weighted the results by how "
            "often each kind of read misses in the corpus run. <bookmark mark='a'/> Over the run, ninety-one percent "
            "of table reads and fifty-seven percent of letter reads miss the first-level cache. <bookmark mark='b'/> "
            "And at eight hundred eighty-five megahertz, the core hides them: the second-level cache is five cycles "
            "away, the out-of-order window covers that, and the prefetcher keeps ahead of the scan. The Job slows by "
            "five hundredths of a percent. <bookmark mark='c'/> Without the prefetcher, two percent. <bookmark "
            "mark='d'/> But give the same memory a core as fast as this machine's, two point eight gigahertz, and the "
            "same nanoseconds become three times as many cycles: then the misses cost fourteen percent. The memory "
            "wall, again, is a ratio."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        j = load("job")
        head = label(r"Ledger row 3", font_size=38).to_edge(UP, buff=0.35)
        rows = j["ledger"] + [{"part": p_, "label": t} for p_, t in ((10, r"four cores"), (13, r"an optimizing compiler"),
                                                                     (16, r"sort, then count"), (17, r"a hash table"))]
        led = ledger_table(rows, shown=4, highlight=(3,), font_size=21, row_h=0.4, label_width=4.8).move_to(DOWN * 0.3)
        res = label(rf"{human_time(j['ledger'][2]['seconds'])} $\to$ {human_time(j['ledger'][3]['seconds'])}: \ "
                    r"real memory, \ almost free \ (for this program, \ at this clock)", font_size=26,
                    color=COST).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "So the ledger's fourth row is almost exactly its third: fifty-seven seconds for thirty novels, with real "
            "caches and real DRAM where Part 8 assumed every load took two cycles. <bookmark mark='a'/> This is not "
            "the usual story, and it is worth saying why. The Job reads memory in the friendliest way there is, in "
            "order, again and again, and Pebble's clock is slow. Programs that chase pointers, like a hash table or a "
            "tree, behave like the staircase's random walk, and at a modern clock they would pay in full. The Job's "
            "real problem is not where its data lives but how much of it it reads: three billion lines to count four "
            "and a half million words. Only a better algorithm fixes that, and Parts 16 and 17 bring two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(led.axis), LaggedStart(*[FadeIn(r) for r in led.rows], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()
