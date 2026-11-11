from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


class Persist(VoiceoverScene):
    def construct(self):
        self.card()
        self.copying()
        self.measured()
        self.cache()

    def card(self):
        card = chapter_card(13, r"Persistence, \ and the memory hierarchy", r"Can an update keep the past?",
                            lit=(1989,), extra=((1989, r"Driscoll, \ Sarnak, \ Sleator and Tarjan"),
                                                (1998, r"Okasaki: \ purely functional data structures")), part=PART)
        with self.voiceover("Chapter thirteen. Persistence, and the memory hierarchy."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def copying(self):
        head = label(r"Path copying", font_size=34).to_edge(UP, buff=0.3)

        def nd(k, col=DATA):
            return VGroup(Circle(radius=0.26, stroke_color=col, stroke_width=2, fill_color=BG, fill_opacity=1),
                          mono(str(k), 18, WHITE))
        P = {50: [-2.0, 1.6], 30: [-3.4, 0.5], 70: [-0.6, 0.5], 20: [-4.1, -0.6], 40: [-2.7, -0.6], 60: [-1.3, -0.6],
             80: [0.1, -0.6]}
        old = {k: nd(k).move_to([x, y, 0]) for k, (x, y) in P.items()}
        oe = VGroup(*[Line(old[a].get_center(), old[b].get_center(), buff=0.26, color=GREY_B, stroke_width=1.6)
                      for a, b in ((50, 30), (50, 70), (30, 20), (30, 40), (70, 60), (70, 80))])
        n50 = nd(50, HEAD).move_to([2.4, 1.6, 0])
        n70 = nd(70, HEAD).move_to([3.4, 0.5, 0])
        n80 = nd(80, HEAD).move_to([4.1, -0.6, 0])
        n90 = nd(90, YES).move_to([4.8, -1.7, 0])
        ne = VGroup(Line(n50.get_center(), n70.get_center(), buff=0.26, color=HEAD, stroke_width=2),
                    Line(n70.get_center(), n80.get_center(), buff=0.26, color=HEAD, stroke_width=2),
                    Line(n80.get_center(), n90.get_center(), buff=0.26, color=HEAD, stroke_width=2),
                    DashedLine(n50.get_center(), old[30].get_center(), buff=0.26, color=HEAD, stroke_width=1.6),
                    DashedLine(n70.get_center(), old[60].get_center(), buff=0.26, color=HEAD, stroke_width=1.6))
        v0 = label(r"version 1", font_size=19, color=GREY_B).next_to(old[50], UP, buff=0.15)
        v1 = label(r"version 2: \ insert 90", font_size=19, color=HEAD).next_to(n50, UP, buff=0.15)
        pts = VGroup(
            label(r"never change a node: \ copy the path from the root to the change, \ share everything else",
                  font_size=22, color=GREY_A),
            label(r"every old version stays complete and searchable: \ \textbf{persistence}", font_size=22,
                  color=YES),
            label(r"common in functional programming \ (Part 14), \ Git's trees \ (Part 41), \ and "
                  r"copy-on-write databases", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A mutable update normally discards the previous state. <bookmark mark='a'/> Path copying "
            "preserves it: copy the search path to the new leaf, and let the copies point to unchanged "
            "old subtrees. <bookmark mark='b'/> Two roots now describe two complete search trees sharing "
            "most nodes. Old versions remain searchable. <bookmark mark='c'/> Persistent structures are "
            "common in functional programming, copy-on-write systems and content-addressed trees such as "
            "Git. They do not imply that every value in every functional language uses this particular "
            "representation. Driscoll, Sarnak, Sleator and Tarjan developed a general persistence "
            "framework in 1989."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(n) for n in old.values()], Create(oe), FadeIn(v0))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            self.play(FadeIn(n50), FadeIn(n70), FadeIn(n80), FadeIn(n90), Create(ne), FadeIn(v1), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("persist")
        head = label(r"What persistence costs", font_size=34).to_edge(UP, buff=0.3)
        rows = [[words(r["n"]), f"{r['copied_per_insert']:.1f}", f"{2 * r['ln']:.1f}", f"{r['full_copy']:,.0f}"]
                for r in d["rows"]]
        tab = grid_table([r"versions", r"nodes copied per insert", r"$\approx 2 \ln n$", r"copying the whole tree"],
                         rows, widths=[2.2, 3.6, 2.2, 3.6], row_h=0.5, font_size=20,
                         colors=[[WHITE, YES, GREY_A, NO]] * len(rows)).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"each insert copies one path: \ the depth of a random tree, \ about $2 \ln n$ \ (chapter 5)", font_size=22,
                  color=GREY_A),
            label(r"a hundred thousand complete versions, \ about twenty new nodes each",
                  font_size=22, color=YES),
            label(r"Okasaki \ (1998): \ queues, \ heaps and more, \ persistent with amortized bounds intact",
                  font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Is it expensive? <bookmark mark='a'/> We kept every version of a tree through a hundred "
            "thousand random inserts. Each insert copied about twenty-one nodes, the length of one path, "
            "which is chapter five's depth of a random tree. Copying the whole tree for each version "
            "would cost fifty thousand nodes per insert. <bookmark mark='b'/> So a hundred thousand "
            "complete versions cost about twenty nodes each. <bookmark mark='c'/> Chris Okasaki's book "
            "showed how far the idea goes: queues, heaps and more, persistent and still efficient."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def cache(self):
        d = load("cache")
        head = label(r"The memory hierarchy decides", font_size=34).to_edge(UP, buff=0.3)
        rows = d["rows"]
        ax = Axes(x_range=[3, 7.2, 1], y_range=[0, 3.5, 1], x_length=6.4, y_length=3.8,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        series = [("array", r"sorted array, \ binary search", DATA), ("map", r"\texttt{std::map}, \ red--black", NO),
                  ("unordered", r"\texttt{std::unordered\_map}, \ chaining", LAM),
                  ("open", r"open addressing, \ one array", YES)]
        curves, keys_ = VGroup(), VGroup()
        for k, name, col in series:
            pts = [ax.c2p(np.log10(r["n"]), np.log10(max(r[k], 1))) for r in rows]
            curves.add(VGroup(VMobject(color=col, stroke_width=3).set_points_as_corners(pts),
                              *[Dot(p, radius=0.05, color=col) for p in pts]))
            last = rows[-1][k]
            keys_.add(label(rf"{name}: \ {last:.0f} ns", font_size=19, color=col))
        keys_.arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        xt = VGroup(*[label(t, font_size=15, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v, t in ((3, "1,000"), (5, "100,000"), (7, "10 million"))])
        yt = VGroup(*[label(t, font_size=15, color=GREY_B).next_to(ax.c2p(3, v), LEFT, buff=0.1)
                      for v, t in ((0, "1 ns"), (1, "10 ns"), (2, "100 ns"), (3, r"1 $\mu$s"))])
        xl = label(r"keys", font_size=17, color=GREY_B).next_to(xt, DOWN, buff=0.1)
        yl = label(r"time per lookup, \ this machine, \ log scale", font_size=17, color=GREY_B).next_to(
            ax, UP, buff=0.1).align_to(ax, LEFT)
        last = rows[-1]
        note_ = VGroup(
            label(rf"same checked values; \ open table load {100 * last['load']:.1f}\% at {words(last['capacity'])} slots",
                  font_size=20, color=HEAD),
            label(r"minimum of three repeats; \ lookup + result-vector write; \ no hardware-counter causal claim",
                  font_size=19, color=GREY_B),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.28)
        with self.voiceover(
            "Counting steps does not predict elapsed time by itself. <bookmark mark='a'/> These four "
            "implementations answer the same seeded successful uint32 lookups, with last assignment "
            "winning for duplicate keys. We check every returned value outside the timer, including "
            "distinct keys twelve and thirteen. <bookmark mark='b'/> The timer includes lookups and "
            "writing the result vector, and excludes construction, query generation, and verification. "
            "Each point is the minimum of three repeats on this host. Actual unique-key counts and "
            "open-table loads are recorded. <bookmark mark='c'/> The curves show different costs on this "
            "workload, not a universal ranking. Layout, branches, allocation, hashing and cache behavior "
            "can all matter. <bookmark mark='d'/> We did not collect hardware performance counters, so "
            "these timings alone do not identify the number of cache misses or prove which mechanism "
            "caused the gap."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(keys_[0]))
            vo.wait_until("b")
            self.play(Create(curves[1]), FadeIn(keys_[1]))
            vo.wait_until("c")
            self.play(Create(curves[2]), FadeIn(keys_[2]), Create(curves[3]), FadeIn(keys_[3]))
            vo.wait_until("d")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()
