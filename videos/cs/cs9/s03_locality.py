from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, fmt, load,
                                  size_label)


class Locality(VoiceoverScene):
    def construct(self):
        self.card()
        self.scatter()
        self.reuse()
        self.curve()

    def card(self):
        card = chapter_card(2, r"Locality", r"Why does a small memory help a big program?", lit=(1968,),
                            extra=((1968, r"Denning: \ the working set"),), part=PART)
        with self.voiceover("Chapter two. Locality."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def scatter(self):
        d = load("trace")
        sc = d["scatter"]
        head = label(r"Every memory access of the Job's first chapter", font_size=34).to_edge(UP, buff=0.3)
        steps = np.array(sc["step"])
        addr = np.array(sc["addr"])
        table = (addr >= 65536) & (addr < 524288)
        pool = addr >= 524288
        ax_t = Axes(x_range=[0, steps.max(), steps.max() / 4], y_range=[0, 1, 1], x_length=11.0, y_length=2.2,
                    tips=False, axis_config={"color": GREY_D}).move_to(UP * 0.85)
        ax_p = Axes(x_range=[0, steps.max(), steps.max() / 4], y_range=[0, 1, 1], x_length=11.0, y_length=1.3,
                    tips=False, axis_config={"color": GREY_D}).move_to(DOWN * 1.55)
        tmax = max(addr[table].max() - 65536, 1)
        pmax = max(addr[pool].max() - 524288, 1)
        dots_t = VGroup(*[Dot(ax_t.c2p(s, (a - 65536) / tmax), radius=0.012, color=DATA)
                          for s, a in zip(steps[table], addr[table])])
        dots_p = VGroup(*[Dot(ax_p.c2p(s, (a - 524288) / pmax), radius=0.015, color=CTRL)
                          for s, a in zip(steps[pool], addr[pool])])
        lt = label(rf"the word table \ ({tmax / 1024:.1f} KB)", font_size=20, color=DATA).next_to(ax_t, LEFT, buff=0.1)
        lp = label(rf"the letters \ ({pmax / 1024:.1f} KB)", font_size=20, color=CTRL).next_to(ax_p, LEFT, buff=0.1)
        for l_ in (lt, lp):
            if l_.get_left()[0] < -7:
                l_.shift(RIGHT * (-6.9 - l_.get_left()[0]))
        xl = note(rf"time: \ {d['instructions']:,} instructions \quad (one dot for every {d['accesses'] // len(steps)} accesses)",
                  font_size=18).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Caches work because programs are not random. Here is every load and store the Job makes in its first "
            "chapter, a hundred fifty-five thousand of them: time runs to the right, and the address goes up. "
            "<bookmark mark='a'/> The word table. Each scan is a diagonal stroke: the Job reads entry after entry, "
            "address after address, then starts again from the bottom for the next word. As new words arrive, the "
            "strokes reach higher. <bookmark mark='b'/> Below, the letters of the words, read when an entry has the "
            "right length, and written when a new word is added: scattered, but returning again and again to the same "
            "places. <bookmark mark='c'/> These are the two kinds of locality. Spatial: after reading one address, a "
            "program soon reads the ones next to it. Temporal: after reading an address, it soon reads it again. Peter "
            "Denning gave this its classic form in 1968: at any moment a program is using a small working set of its "
            "memory, and that set changes slowly."
        ) as vo:
            self.play(FadeIn(head), Create(ax_t), Create(ax_p), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(lt), LaggedStart(*[FadeIn(x) for x in dots_t], lag_ratio=0.0005), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(lp), LaggedStart(*[FadeIn(x) for x in dots_p], lag_ratio=0.002), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reuse(self):
        d = load("trace")
        head = label(r"Reuse distance: \ how many other lines since the last time?", font_size=32).to_edge(UP, buff=0.35)
        h = np.array(d["reuse_hist16"][:64], float)
        h0 = h / h.sum()
        ax = Axes(x_range=[0, 64, 8], y_range=[0, 1, 0.25], x_length=10, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(DOWN * 0.2)
        bars = VGroup(*[Rectangle(width=10 / 64 * 0.9, height=max(3.6 * v, 0.005), stroke_width=0, fill_color=DATA,
                                  fill_opacity=0.85).move_to(ax.c2p(k + 0.5, 0), aligned_edge=DOWN)
                        for k, v in enumerate(h0)])
        xt = VGroup(*[label(str(16 * k), font_size=16, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.1)
                      for k in range(0, 65, 8)])
        xl = note(r"distinct cache lines touched since this line's last access \ (LRU stack distance)",
                  font_size=18).next_to(xt, DOWN, buff=0.1)
        frac0 = h0[0]
        key = VGroup(
            label(rf"{100 * frac0:.0f}\% of the accesses: \ fewer than 16 lines since the last use", font_size=24,
                  color=YES),
            label(r"a cache of $C$ lines with LRU hits exactly the accesses with distance below $C$", font_size=24,
                  color=HEAD),
        ).arrange(DOWN, buff=0.15).next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Temporal locality can be measured. For every access, count the distinct cache lines touched since the "
            "same line was last used: its reuse distance, or LRU stack distance, an idea from Richard Mattson and his "
            "colleagues at IBM in 1970. <bookmark mark='a'/> For the Job's first chapter, almost every access has a "
            "tiny reuse distance. <bookmark mark='b'/> And here is why the measure matters. A cache that holds C lines "
            "and evicts the least recently used one hits exactly the accesses whose reuse distance is less than C. "
            "One pass over a trace gives the hit rate of every cache size at once."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(FadeIn(key[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve(self):
        d = load("trace")
        sc = load("scans")
        head = label(r"Miss rate against cache size", font_size=36).to_edge(UP, buff=0.3)
        caps = d["capacities_lines"]
        mr = d["miss_curve"]
        ax = Axes(x_range=[0, 14, 2], y_range=[0, 1, 0.25], x_length=5.6, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(LEFT * 3.4 + DOWN * 0.4)
        ax.y_axis.add_numbers([0, 0.5, 1], font_size=16, num_decimal_places=1)
        xt = VGroup(*[label(size_label(64 << k), font_size=14, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.1)
                      for k in range(0, 15, 4)])
        c1 = VMobject(color=DATA, stroke_width=4).set_points_as_corners([ax.c2p(k, m) for k, m in enumerate(mr)])
        t1 = label(rf"chapter 1: \ {d['distinct_lines']} lines in all", font_size=20, color=DATA).next_to(ax, UP,
                                                                                                    buff=0.1)
        rows = sc["rows"]
        ax2 = Axes(x_range=[0, len(rows) - 1, 1], y_range=[0, 1, 0.25], x_length=5.6, y_length=3.6, tips=False,
                   axis_config={"color": GREY_C, "font_size": 16}).move_to(RIGHT * 3.4 + DOWN * 0.4)
        ax2.y_axis.add_numbers([0, 0.5, 1], font_size=16, num_decimal_places=1)
        xt2 = VGroup(*[label(size_label(r["kb"] * 1024), font_size=14, color=GREY_B).next_to(ax2.c2p(k, 0), DOWN,
                                                                                            buff=0.1)
                       for k, r in enumerate(rows) if k % 2 == 0])
        c2 = VMobject(color=NO, stroke_width=4).set_points_as_corners([ax2.c2p(k, r["lru"]) for k, r in enumerate(rows)])
        t2 = label(rf"thirty novels: \ the table, \ {sc['table_kb']:.0f} KB", font_size=20, color=NO).next_to(ax2, UP,
                                                                                                       buff=0.1)
        note_ = label(r"the cliff is where the working set fits", font_size=26, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "From the reuse distances, the miss rate of every size of cache. <bookmark mark='a'/> On the first "
            "chapter, the Job touches only ninety-two lines of memory in all, under six kilobytes, and the curve "
            "falls to almost nothing by eight kilobytes. <bookmark mark='b'/> Over all thirty novels the picture "
            "changes. The table grows to six hundred eighty kilobytes, and the miss rate of its reads stays high, "
            "eighty-eight percent at thirty-two kilobytes, until the cache is big enough to hold the whole table; then "
            "it drops off a cliff. <bookmark mark='c'/> Every miss curve has this shape somewhere. The cliff is where "
            "the working set fits."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xt), FadeIn(t1), Create(c1, run_time=1.5))
            vo.wait_until("b")
            self.play(Create(ax2), FadeIn(xt2), FadeIn(t2), Create(c2, run_time=1.5))
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()
