from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, slots, words)


class Cuckoo(VoiceoverScene):
    def construct(self):
        self.card()
        self.kicks()
        self.threshold()
        self.perfect()

    def card(self):
        card = chapter_card(4, r"Cuckoo hashing and perfect hashing", r"Can every lookup take two probes?",
                            lit=(2001,), extra=((1984, r"Fredman, Koml\'os and Szemer\'edi"),
                                                (2001, r"Pagh and Rodler: \ cuckoo hashing")), part=PART)
        with self.voiceover("Chapter four. Cuckoo hashing, and perfect hashing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def kicks(self):
        head = label(r"Two tables, \ two hash functions", font_size=34).to_edge(UP, buff=0.3)
        m = 8
        t1 = slots([False] * m, w=0.8, h=0.6, color=DATA).move_to(UP * 1.3)
        t2 = slots([False] * m, w=0.8, h=0.6, color=LAM).move_to(DOWN * 0.3)
        l1 = label(r"$T_1[h_1(x)]$", font_size=22, color=DATA).next_to(t1, LEFT, buff=0.3)
        l2 = label(r"$T_2[h_2(x)]$", font_size=22, color=LAM).next_to(t2, LEFT, buff=0.3)

        def put(table, i, s, col):
            t = mono(s, 22, WHITE).move_to(table[i])
            return t
        a = put(t1, 2, "A", DATA)
        b = put(t2, 5, "B", LAM)
        c = put(t1, 6, "C", DATA)
        pts = VGroup(
            label(r"every key is in one of exactly two places: \ \textbf{find costs two probes, \ always}",
                  font_size=22, color=YES),
            label(r"insert $x$: \ put it in $T_1$; \ if that slot was taken, \ kick the old key to its other "
                  r"table, \ and repeat", font_size=21, color=GREY_A),
            label(r"a cycle of kicks means a bad pair of functions: \ pick new ones and rebuild", font_size=21,
                  color=NO),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        x = mono("X", 24, HEAD).next_to(t1[2], UP, buff=0.5)
        with self.voiceover(
            "In 2001 Rasmus Pagh and Flemming Rodler found a way to make every lookup cost two probes, not "
            "on average, but always. <bookmark mark='a'/> Keep two tables and two independent hash functions. "
            "Every key lives either at h one of x in the first table, or at h two of x in the second. A find looks "
            "in those two places and nowhere else. <bookmark mark='b'/> To insert, put the key in its first-table "
            "slot. If that slot was taken, the old key is kicked out, like a cuckoo's egg, to its place in the "
            "other table, possibly kicking out another. <bookmark mark='c'/> Usually the chain of kicks ends "
            "quickly. If it runs into a cycle, the pair of hash functions is bad: choose new ones and rebuild."
        ) as vo:
            self.play(FadeIn(head), FadeIn(t1), FadeIn(t2), FadeIn(l1), FadeIn(l2), FadeIn(a), FadeIn(b), FadeIn(c))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(x), FadeIn(pts[1]))
            self.play(x.animate.move_to(t1[2]), a.animate.move_to(t2[5].get_center() + UP * 0.0), run_time=1)
            self.play(b.animate.move_to(t1[6].get_center()), c.animate.move_to(t2[1]), run_time=1)
            self.play(t1[2].animate.set_fill(DATA, 0.5), t2[5].animate.set_fill(LAM, 0.5),
                      t1[6].animate.set_fill(DATA, 0.5), t2[1].animate.set_fill(LAM, 0.5))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def threshold(self):
        d = load("cuckoo")
        head = label(r"The threshold at half full", font_size=34).to_edge(UP, buff=0.3)
        rows = d["rows"]
        ax = Axes(x_range=[0.28, 0.57, 0.05], y_range=[0, 1, 0.25], x_length=6.4, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        pts = [ax.c2p(r["load"], r["fail"]) for r in rows]
        line = VGroup(VMobject(color=NO, stroke_width=3).set_points_as_corners(pts),
                      *[Dot(p, radius=0.06, color=NO) for p in pts])
        th = DashedLine(ax.c2p(0.5, 0), ax.c2p(0.5, 1), color=HEAD, stroke_width=2)
        thl = label(r"$\tfrac12$", font_size=20, color=HEAD).next_to(th, UP, buff=0.08)
        xt = VGroup(*[label(f"{v:.2f}", font_size=15, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v in (0.3, 0.4, 0.5)])
        yt = VGroup(*[label(t, font_size=15, color=GREY_B).next_to(ax.c2p(0.28, v), LEFT, buff=0.1)
                      for v, t in ((0, "0"), (0.5, "50\\%"), (1, "100\\%"))])
        xl = label(rf"keys per slot, \ two tables of {words(d['m'])}", font_size=17, color=GREY_B).next_to(
            xt, DOWN, buff=0.1)
        yl = label(r"insertions that hit a cycle, \ 40 trials", font_size=17, color=GREY_B).next_to(
            ax, UP, buff=0.1).align_to(ax, LEFT)
        side = VGroup(
            label(r"the \textbf{cuckoo graph}: \ a vertex per slot, \ an edge per key", font_size=21, color=GREY_A),
            label(r"inserting succeeds while no component has more edges than vertices", font_size=21,
                  color=GREY_A),
            label(r"a random graph with $n$ edges on $2m$ vertices grows such cycles at $n/2m = \tfrac12$ "
                  r"\ (Erd\H{o}s and R\'enyi, \ 1960)", font_size=20, color=HEAD),
            label(r"in practice: \ four slots per bucket, \ or more hash functions, \ push the threshold past 95\%",
                  font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        if side.width > 5.6:
            side.scale_to_fit_width(5.6).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Cuckoo hashing works only if the tables are not too full, and the limit is sharp. <bookmark "
            "mark='a'/> We inserted keys into two tables of two thousand slots, forty times at each load, and "
            "counted how often an insertion ran into a cycle. Below forty percent, never. Past one half, most of "
            "the time. <bookmark mark='b'/> The reason is a graph. Make each slot a vertex and each key an edge "
            "between its two possible slots. Insertion succeeds as long as no connected piece has more edges than "
            "vertices. <bookmark mark='c'/> A random graph develops such pieces suddenly, when the number of edges "
            "reaches half the number of vertices: Paul Erdős and Alfréd Rényi's threshold from 1960. <bookmark "
            "mark='d'/> Real cuckoo tables put four keys in each bucket, or use more hash functions, and run safely "
            "above ninety-five percent full."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(line), Create(th), FadeIn(thl), run_time=2)
            for mk, s in zip("bcd", (side[:2], side[2], side[3])):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()

    def perfect(self):
        d = load("cuckoo")
        head = label(r"Perfect hashing \ (Fredman, \ Koml\'os and Szemer\'edi, \ 1984)", font_size=32).to_edge(
            UP, buff=0.3)
        steps = VGroup(
            label(r"for a \textbf{fixed} set of $n$ keys: \ no collisions at all, \ $O(n)$ space", font_size=23,
                  color=GREY_A),
            label(r"level 1: \ hash into $n$ buckets; \ bucket $i$ gets $b_i$ keys", font_size=22, color=DATA),
            label(r"level 2: \ bucket $i$ gets its own table of $b_i^2$ slots, \ and a hash with no collision there",
                  font_size=22, color=LAM),
            MathTex(r"\mathbb{E}\Bigl[\sum_i b_i^2\Bigr] = n + 2\binom{n}{2}\frac1n < 2n", font_size=32, color=YES),
            label(r"and $b^2$ slots make $b$ keys collision-free with probability $> \tfrac12$: \ the birthday bound "
                  r"again", font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.25).next_to(head, DOWN, buff=0.45)
        rows = [[words(f["n"]), words(f["space"]), f"{f['space'] / f['n']:.2f}", str(f["max_bucket"])] for f in
                d["fks"]]
        tab = grid_table([r"keys", r"slots in all", r"per key", r"largest bucket"], rows,
                         widths=[2.2, 2.6, 2.0, 2.6], row_h=0.45, font_size=19).next_to(steps, DOWN, buff=0.4)
        with self.voiceover(
            "If the set of keys is fixed in advance, like the keywords of a language or the words of a dictionary "
            "on disk, we can do better still. <bookmark mark='a'/> Michael Fredman, János Komlós and Endre "
            "Szemerédi showed in 1984 how to store n keys with no collisions at all, in linear space. <bookmark "
            "mark='b'/> First hash into n buckets. <bookmark mark='c'/> Then give each bucket its own small table, "
            "with room for the square of its size, and a hash function with no collisions inside it. <bookmark "
            "mark='d'/> The squares add up to less than two n on average: the same counting of colliding pairs as "
            "in chapter one. <bookmark mark='e'/> And a table with b squared slots holds b keys without a "
            "collision more than half the time, so a few retries suffice. <bookmark mark='f'/> Measured, the "
            "whole structure takes about three slots per key, and every lookup is two hashes and one comparison."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
            vo.wait_until("f")
            self.play(FadeIn(tab))
        self.wait(0.3)
        self.clear_scene()
