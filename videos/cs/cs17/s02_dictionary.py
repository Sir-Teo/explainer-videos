from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, slots, words)


class Dictionary(VoiceoverScene):
    def construct(self):
        self.card()
        self.adt()
        self.idea()
        self.birthday()
        self.corpus()

    def card(self):
        card = chapter_card(1, r"The dictionary, \ and the birthday bound",
                            r"How soon do random choices collide?", lit=(1953,),
                            extra=((1953, r"Luhn: \ hashing, \ at IBM"),), part=PART)
        with self.voiceover("Chapter one. The dictionary, and the birthday bound."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def adt(self):
        head = label(r"One interface, \ many implementations", font_size=34).to_edge(UP, buff=0.3)
        rows = [
            [r"unsorted list \ (the Job v0)", r"$O(n)$", r"$O(1)$", r"no"],
            [r"sorted array", r"$O(\log n)$", r"$O(n)$", r"yes"],
            [r"balanced search tree", r"$O(\log n)$", r"$O(\log n)$", r"yes"],
            [r"hash table", r"$O(1)$ expected", r"$O(1)$ expected", r"no"],
        ]
        tab = grid_table([r"implementation", r"find", r"insert", r"in order?"], rows, widths=[4.6, 2.8, 2.8, 2.0],
                         row_h=0.62, font_size=22, mono_cols=(),
                         colors=[[NO, NO, WHITE, GREY_B], [WHITE, WHITE, NO, YES], [LAM, LAM, LAM, YES],
                                 [YES, YES, YES, GREY_B]]).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"an \textbf{abstract data type} says what the operations do; \ a data structure says how",
                  font_size=22, color=GREY_A),
            label(r"Liskov and Zilles \ (1974): \ program against the interface, \ choose the structure later",
                  font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.18).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "A dictionary specifies operations before choosing a representation. <bookmark mark='a'/> An "
            "unsorted list can append a new entry in constant amortized time, but locating a key scans "
            "the list. A sorted array uses logarithmic comparisons to search and linear shifting to "
            "insert. A balanced tree offers logarithmic operations and sorted traversal. Hash tables "
            "offer expected constant table work under hashing and load assumptions; resizing adds an "
            "amortized qualification. Hashing a long string still reads its characters. <bookmark "
            "mark='b'/> Abstract data types let us choose the representation behind that interface. "
            "Liskov and Zilles helped formalize this separation in 1974."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab.rule), LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells], lag_ratio=0.3),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(pts))
        self.wait(0.3)
        self.clear_scene()

    def idea(self):
        head = label(r"Hashing: \ compute where the key lives", font_size=34).to_edge(UP, buff=0.3)
        keys = ["the", "whale", "ship", "sea", "ahab", "white"]
        m = 11
        hv = [sum(ord(c) * 31 ** i for i, c in enumerate(w)) % m for w in keys]
        table = slots([False] * m, w=0.75, h=0.62).move_to(DOWN * 0.9)
        idx = VGroup(*[mono(str(i), 15, GREY_B).next_to(c, DOWN, buff=0.08) for i, c in enumerate(table)])
        words_ = VGroup(*[mono(w, 22, CODE) for w in keys]).arrange(RIGHT, buff=0.55).move_to(UP * 1.7)
        fx = MathTex(r"h(\text{key}) \in \{0, 1, \ldots, m - 1\}", font_size=32).move_to(UP * 0.6)
        note_ = label(r"two keys with the same slot: \ a \textbf{collision}", font_size=22, color=NO).to_edge(
            DOWN, buff=0.6)
        with self.voiceover(
            "The idea is older than most of computing: Hans Peter Luhn proposed it at IBM in 1953. "
            "<bookmark mark='a'/> Turn the key into a number with a hash function, and use that number, "
            "reduced to the table's size, as the place to store it. <bookmark mark='b'/> Then finding a "
            "key is computing its hash and looking in one place, whatever the size of the table. "
            "<bookmark mark='c'/> The catch is that two keys can land in the same slot. Everything in the"
            " next three chapters is about what to do then, and the first question is how soon it "
            "happens."
        ) as vo:
            self.play(FadeIn(head), FadeIn(words_), FadeIn(table), FadeIn(idx))
            vo.wait_until("a")
            self.play(Write(fx))
            vo.wait_until("b")
            seen = {}
            for w_, s in zip(words_, hv):
                tgt = table[s]
                col = NO if s in seen else DATA
                sc = min(1.0, 0.66 / w_.width)
                self.play(w_.animate.scale(sc).move_to(tgt.get_center() + UP * (0.55 + 0.38 * seen.get(s, 0))),
                          tgt.animate.set_fill(col, 0.85), run_time=0.6)
                seen[s] = seen.get(s, 0) + 1
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    def birthday(self):
        d = load("birthday")
        head = label(r"The birthday bound", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 80, 10], y_range=[0, 1, 0.25], x_length=6.2, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.8).shift(DOWN * 0.4)
        pts = [ax.c2p(r["n"], r["p"]) for r in d["curve"]]
        curve = VMobject(color=CTRL, stroke_width=3).set_points_smoothly(pts)
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(80, 0.5), color=GREY_C, stroke_width=1.5)
        mark = Dot(ax.c2p(23, 0.5073), color=HEAD, radius=0.07)
        ml = label(r"23 people: \ 50.7\%", font_size=19, color=HEAD).next_to(mark, RIGHT, buff=0.12)
        xt = VGroup(*[label(str(v), font_size=15, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v in (0, 20, 40, 60, 80)])
        yt = VGroup(*[label(t, font_size=15, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v, t in ((0, "0"), (0.5, r"$\tfrac12$"), (1, "1"))])
        xl = label(r"people, \ $m = 365$ days", font_size=17, color=GREY_B).next_to(xt, DOWN, buff=0.1)
        side = VGroup(
            MathTex(r"\Pr[\text{no collision}] = \prod_{i=0}^{n-1}\Bigl(1 - \frac{i}{m}\Bigr)", font_size=30),
            MathTex(r"\approx \exp\Bigl(-\sum_i \frac{i}{m}\Bigr) = e^{-n(n-1)/2m}", font_size=30),
            label(r"independent uniform choices: \ collisions likely around $\sqrt m$", font_size=22, color=YES),
            label(r"$1 - x \le e^{-x}$, \ and it is nearly equal for small $x$", font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        if side.width > 6.0:
            side.scale_to_fit_width(6.0)
        with self.voiceover(
            "Suppose each key independently chooses one of m slots uniformly. <bookmark mark='a'/> For n "
            "at most m, the chance of no collision is this product: each new key avoids every earlier "
            "choice. <bookmark mark='b'/> The exponential approximation retains n times n minus one over "
            "two m. It is accurate when the small-factor approximation is appropriate; the exponential "
            "also gives a one-sided bound. <bookmark mark='c'/> Under the equal, independent birthday "
            "model, twenty-three people have about a fifty point seven percent chance of a shared "
            "birthday. <bookmark mark='d'/> Collisions become likely around the square-root scale. Likely"
            " is not certain, and a deterministic hash requires a separate analysis."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(Create(curve), Create(half), run_time=2)
            self.play(FadeIn(mark), FadeIn(ml))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

    def corpus(self):
        d = load("birthday")
        head = label(r"The birthday bound, \ on our vocabulary", font_size=34).to_edge(UP, buff=0.3)
        rows = [
            [rf"{words(d['distinct'])} distinct words, \ hash mod 16,777,213", f"{d['expected_full']:.0f}",
             words(d["full_collisions"])],
            [rf"reduced to $m = 2^{{17}}$ = {words(d['m'])} slots", f"{d['expected_pairs']:,.0f}",
             words(d["slot_pairs"])],
        ]
        tab = grid_table([r"", r"uniform-hash expected pairs", r"fixed-hash observed pairs"], rows, widths=[6.6, 3.2, 2.4],
                         row_h=0.6, font_size=21, mono_cols=(),
                         colors=[[WHITE, GREY_A, HEAD], [WHITE, GREY_A, NO]]).next_to(head, DOWN, buff=0.7)
        pts = VGroup(
            MathTex(r"\mathbb{E}[\text{colliding pairs}] = \binom{n}{2}\frac{1}{m}", font_size=32),
            label(r"fixed polynomial hash observations; \ uniform expectation is a separate model", font_size=22,
                  color=GREY_A),
            label(r"so a table must compare the keys themselves, \ and decide where the second one goes",
                  font_size=22, color=YES),
        ).arrange(DOWN, buff=0.25).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Here are two different quantities on the same vocabulary. <bookmark mark='a'/> Independent "
            "uniform hashes would give n choose two over m expected colliding pairs. Our polynomial hash "
            "is fixed, so its count is a deterministic observation, not a random-family guarantee. "
            "<bookmark mark='b'/> On fifty-seven thousand eight hundred and ninety-five distinct words, "
            "the full hash has one hundred and one colliding pairs. Reducing it to the slot table gives "
            "twelve thousand four hundred and ninety-five pairs. Excess keys and colliding pairs are "
            "different statistics if three keys share a value, even though the full-hash counts coincide "
            "here. <bookmark mark='c'/> The table must compare complete keys and resolve collisions; a "
            "matching hash alone never proves equality."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*[c for r in tab.cells for c in r])))
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()
