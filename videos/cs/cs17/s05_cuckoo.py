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
            label(r"finite kick cutoff: \ rebuild safely; \ cutoff alone does not prove no placement exists", font_size=21,
                  color=NO),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        x = mono("X", 24, HEAD).next_to(t1[2], UP, buff=0.5)
        with self.voiceover(
            "In 2001 Rasmus Pagh and Flemming Rodler found a way to make every lookup cost two probes, "
            "not on average, but always. <bookmark mark='a'/> Keep two tables and two independent hash "
            "functions. Every key lives either at h one of x in the first table, or at h two of x in the "
            "second. A find looks in those two places and nowhere else. <bookmark mark='b'/> To insert, "
            "put the key in its first-table slot. If that slot was taken, the old key is kicked out, like"
            " a cuckoo's egg, to its place in the other table, possibly kicking out another. <bookmark "
            "mark='c'/> Usually the chain of kicks ends quickly. If it runs into a cycle, the pair of "
            "hash functions is bad: choose new ones and rebuild."
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
        head = label(r"Finite failures and an ideal-model threshold", font_size=34).to_edge(UP, buff=0.3)
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
        yl = label(r"exceeded 500 kicks, \ 40 seeded trials", font_size=17, color=GREY_B).next_to(
            ax, UP, buff=0.1).align_to(ax, LEFT)
        side = VGroup(
            label(r"the \textbf{cuckoo graph}: \ a vertex per slot, \ an edge per key", font_size=21, color=GREY_A),
            label(r"a placement exists iff every component has at most as many edges as vertices", font_size=21,
                  color=GREY_A),
            label(r"ideal independent choices: \ excess-edge components appear near load $1/2$ "
                  r"\ (Erd\H{o}s and R\'enyi, \ 1960)", font_size=20, color=HEAD),
            label(r"bucket sizes, \ number of choices and insertion policy change the model and threshold",
                  font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        if side.width > 5.6:
            side.scale_to_fit_width(5.6).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The classical two-choice cuckoo threshold is a random-graph statement, not a finite kick "
            "limit. <bookmark mark='a'/> Here we run forty seeded trials per load on two tables of two "
            "thousand slots, stopping when an insertion exceeds five hundred kicks. The plotted fraction "
            "is that experimental failure event. <bookmark mark='b'/> Model each slot as a vertex and "
            "each key's two choices as an edge. A placement can orient each edge toward a distinct "
            "occupied vertex. <bookmark mark='c'/> In the ideal independent-choice model, excess edges in"
            " a component obstruct placement, and the asymptotic threshold is near one half of total "
            "slots. <bookmark mark='d'/> Our cutoff can stop a long insertion without proving such an "
            "obstruction. A production implementation needs a safe rebuild or stash; this experiment "
            "stops immediately on failure."
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
            MathTex(r"\mathbb{E}\Bigl[\sum_i b_i^2\Bigr]\le n+2\binom n2\frac1n<2n", font_size=32, color=YES),
            label(r"and $b^2$ slots make $b$ keys collision-free with probability $> \tfrac12$: \ the birthday bound "
                  r"again", font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.25).next_to(head, DOWN, buff=0.45)
        rows = [[words(f["n"]), words(f["space"]), f"{f['space'] / f['n']:.2f}", str(f["max_bucket"])] for f in
                d["fks"]]
        tab = grid_table([r"keys", r"slots in all", r"per key", r"largest bucket"], rows,
                         widths=[2.2, 2.6, 2.0, 2.6], row_h=0.45, font_size=19).next_to(steps, DOWN, buff=0.4)
        sizes = [2, 1, 0, 3, 0, 0]
        assert sum(sizes) == 6 and sum(b*b for b in sizes) == 14
        example = VGroup(
            VGroup(*[MathTex(rf"{b}^2={b*b}", font_size=27, color=DATA) for b in sizes]).arrange(RIGHT, buff=0.4),
            label(r"one outcome: \ 6 keys, \ 6 buckets, \ 14 secondary slots; \ expectation averages random functions",
                  font_size=19, color=HEAD),
        ).arrange(DOWN, buff=0.18).move_to(DOWN * 2.7)
        with self.voiceover(
            "A fixed key set permits a stronger lookup guarantee. <bookmark mark='a'/> FKS hashing "
            "chooses functions during construction and retries until its tested conditions hold. The "
            "abstract scheme has constant worst-case lookup with linear space under the stated word and "
            "hashing model. <bookmark mark='b'/> First hash n keys into n buckets. In this six-key "
            "example the bucket sizes are two, one, zero, three, zero, zero. <bookmark mark='c'/> "
            "Allocate the square of each bucket's size for its secondary table: fourteen slots in this "
            "particular outcome. <bookmark mark='d'/> Over the random first-level hash, universality "
            "gives an upper bound below two n for the expected sum of squares. A single outcome can "
            "exceed its expectation, so construction also retries a first level whose sum is too large. "
            "<bookmark mark='e'/> A fresh universal secondary hash into b squared slots has collision "
            "probability less than one half by a union bound. Retrying gives a collision-free mapping. "
            "<bookmark mark='f'/> Our finite construction experiment checks these mappings and counts "
            "slots and retries. It does not implement a stored dictionary query interface; the two-hash "
            "lookup statement belongs to the complete FKS scheme."
        ) as vo:
            self.play(FadeIn(head), FadeIn(example))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
            vo.wait_until("f")
            self.play(FadeOut(example), FadeIn(tab))
        self.wait(0.3)
        self.clear_scene()
