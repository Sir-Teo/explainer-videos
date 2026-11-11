from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs2.common import COST, CTRL, DATA, FUNC, HEAD, NO, PART, YES, load


class Pigeonhole(VoiceoverScene):
    def construct(self):
        self.card()
        self.basic()
        self.monotone()
        self.proof()
        self.random()
        self.compression()

    def card(self):
        card = chapter_card(9, r"Pigeons", r"What must happen, just because there is not enough room?", part=PART)
        with self.voiceover("Chapter nine. Pigeons."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def basic(self):
        head = label(r"The pigeonhole principle", font_size=38).to_edge(UP, buff=0.35)
        holes = VGroup(*[RoundedRectangle(width=1.1, height=1.0, corner_radius=0.1, stroke_color=GREY_B,
                                          stroke_width=2) for _ in range(6)]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.6)
        birds = VGroup(*[Dot(radius=0.14, color=DATA) for _ in range(7)]).arrange(RIGHT, buff=0.55).move_to(UP * 1.2)
        st = label(r"$n + 1$ pigeons, \ $n$ holes: \ some hole gets two", font_size=30, color=YES).next_to(
            holes, DOWN, buff=0.5)
        gen = label(r"$N$ things in $k$ boxes: \ some box holds at least $\lceil N / k \rceil$", font_size=30,
                    color=CTRL).next_to(st, DOWN, buff=0.3)
        ex = note(r"9 million Londoners, \ at most about 150{,}000 hairs on a head: \ some 60 of them have exactly the "
                  r"same number", font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The simplest principle in mathematics, and one of the most productive. <bookmark mark='a'/> Put seven "
            "pigeons into six holes, and some hole gets at least two. <bookmark mark='b'/> More generally, put N things "
            "into k boxes and some box holds at least N over k, rounded up. <bookmark mark='c'/> London has about nine "
            "million people, and nobody has more than about a hundred and fifty thousand hairs on their head. So at "
            "least sixty Londoners have exactly the same number of hairs, and nobody has to count."
        ) as vo:
            self.play(FadeIn(head), FadeIn(holes), FadeIn(birds))
            vo.wait_until("a")
            tgt = [0, 1, 2, 3, 4, 5, 2]
            self.play(*[b.animate.move_to(holes[t].get_center() + (LEFT * 0.22 if k == 6 else
                                                                   (RIGHT * 0.22 if k == 2 else ORIGIN)))
                        for k, (b, t) in enumerate(zip(birds, tgt))], run_time=1.6)
            self.play(holes[2].animate.set_stroke(NO, 4), FadeIn(st))
            vo.wait_until("b")
            self.play(FadeIn(gen))
            vo.wait_until("c")
            self.play(FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def monotone(self):
        d = load("monotone")
        seq = d["seq"]
        head = label(r"Erd\H{o}s and Szekeres (1935)", font_size=38).to_edge(UP, buff=0.35)
        thm = theorem_card(r"monotone subsequences", r"Any $n^2 + 1$ distinct numbers, in any order, contain an "
                           r"increasing or a decreasing run of $n + 1$ (not necessarily adjacent).", width=8.6,
                           font_size=24).next_to(head, DOWN, buff=0.3)
        ax_o = np.array([-5.0, -3.0, 0])
        dx, dy = 0.95, 0.42
        pts = [ax_o + np.array([i * dx, v * dy, 0]) for i, v in enumerate(seq)]
        dots = VGroup(*[Dot(p, radius=0.11, color=DATA) for p in pts])
        nums = VGroup(*[MathTex(str(v), font_size=26, color=GREY_B).next_to(dots[i], DOWN, buff=0.15)
                        for i, v in enumerate(seq)])
        inc = [1, 3, 6, 8]  # 2, 4, 7, 8
        assert [seq[i] for i in inc] == sorted(seq[i] for i in inc)
        inc_line = VMobject(color=YES, stroke_width=4).set_points_as_corners([pts[i] for i in inc])
        tl = label(r"$10 = 3^2 + 1$ numbers: \ a run of $4$ must exist \ \ ($2, 4, 7, 8$)", font_size=26,
                   color=YES).to_corner(DR, buff=0.4)
        with self.voiceover(
            "Here is the principle proving something that does not look like pigeons at all. "
            "<bookmark mark='a'/> Paul Erdős and George Szekeres, 1935: any n squared plus one different numbers, in "
            "any order, contain a run of n plus one that only goes up, or only goes down. The run need not be "
            "adjacent; you may skip. <bookmark mark='b'/> Ten numbers, so n is three: there must be a run of four. Here "
            "one is: two, four, seven, eight."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(dd, shift=UP * 0.2) for dd in dots], lag_ratio=0.1), FadeIn(nums))
            self.play(Create(inc_line), *[dots[i].animate.set_color(YES) for i in inc], FadeIn(tl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof(self):
        d = load("monotone")
        seq, inc, dec = d["seq"], d["inc"], d["dec"]
        head = label(r"The proof: \ label every number", font_size=38).to_edge(UP, buff=0.35)
        row = VGroup()
        for v, i_, d_ in zip(seq, inc, dec):
            row.add(VGroup(MathTex(str(v), font_size=42, color=DATA),
                           MathTex(rf"({i_}, {d_})", font_size=32, color=HEAD)).arrange(DOWN, buff=0.22))
        row.arrange(RIGHT, buff=0.36).next_to(head, DOWN, buff=0.5)
        key = note(r"(longest increasing run ending here, \ longest decreasing run ending here)", font_size=22)
        key.next_to(row, DOWN, buff=0.2)
        why = label(r"two numbers never get the same label: \\ if the later one is bigger, its first coordinate is "
                    r"bigger; \\ if smaller, its second", font_size=26, color=GREY_A).move_to(LEFT * 3.4 + DOWN * 1.4)
        # the 3 x 3 grid of possible labels if no run of 4
        cell = 0.62
        grid = VGroup()
        gpos = {}
        for a in range(1, 4):
            for b in range(1, 4):
                sq = Square(cell, stroke_color=GREY_C, stroke_width=1.5).move_to(
                    RIGHT * (3.0 + (a - 2) * cell) + DOWN * (1.5 + (2 - b) * cell) + UP * 0.0)
                gpos[(a, b)] = sq.get_center()
                grid.add(sq)
        gl = label(r"if no run of 4: \ only $3 \times 3 = 9$ labels", font_size=24, color=NO).next_to(grid, UP, buff=0.2)
        concl = label(r"10 numbers, 9 labels: \ impossible", font_size=28, color=YES).next_to(grid, DOWN, buff=0.25)
        with self.voiceover(
            "The proof is a pigeonhole argument in disguise. <bookmark mark='a'/> Give every number a label: the length "
            "of the longest increasing run that ends at it, and the length of the longest decreasing run that ends at "
            "it. <bookmark mark='b'/> No two numbers get the same label. Take an earlier one and a later one. If the "
            "later is bigger, it can extend every increasing run that ends at the earlier one, so its first coordinate "
            "is bigger. If smaller, its second coordinate is. <bookmark mark='c'/> Now suppose there were no run of "
            "four. Every coordinate would be one, two or three: only nine possible labels. <bookmark mark='d'/> Ten "
            "numbers, nine labels, all different. Impossible. So a run of four exists."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*[r[0] for r in row])))
            self.play(LaggedStart(*[FadeIn(r[1]) for r in row], lag_ratio=0.12), FadeIn(key), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(why))
            vo.wait_until("c")
            self.play(Create(grid), FadeIn(gl))
            vo.wait_until("d")
            self.play(*[TransformFromCopy(r[1], r[1].copy().scale(0.62).move_to(
                gpos[(i_, d_)] if i_ <= 3 and d_ <= 3 else gpos[(3, 1)] + RIGHT * cell * 1.3))
                for r, i_, d_ in zip(row, inc, dec)], run_time=1.8)
            self.play(FadeIn(concl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def random(self):
        d = load("monotone")
        head = label(r"Sharp, \ and what random orders do", font_size=38).to_edge(UP, buff=0.35)
        t = d["tight"]
        pts = [np.array([-5.2 + i * 0.6, -1.4 + v * 0.32, 0]) for i, v in enumerate(t)]
        dots = VGroup(*[Dot(p, radius=0.09, color=DATA) for p in pts])
        tl = label(r"$9 = 3^2$ numbers \\ with no run of $4$", font_size=26, color=GREY_A).next_to(dots, UP, buff=0.4)
        seq_t = MathTex(r"3,2,1,\ 6,5,4,\ 9,8,7", font_size=30, color=DATA).next_to(dots, DOWN, buff=0.3)
        rows = VGroup()
        hdr = VGroup(MathTex("n", font_size=30), MathTex(r"\text{longest increasing (mean)}", font_size=28),
                     MathTex(r"\div \sqrt n", font_size=30))
        rows.add(hdr)
        for r in d["random"]:
            rows.add(VGroup(MathTex(f"{r['n']:,}".replace(",", "{,}"), font_size=30, color=DATA),
                            MathTex(f"{r['mean']:.1f}", font_size=30, color=CTRL),
                            MathTex(f"{r['ratio']:.2f}", font_size=30, color=YES)))
        for r in rows:
            r[0].move_to(RIGHT * 0.6)
            r[1].move_to(RIGHT * 3.3)
            r[2].move_to(RIGHT * 5.8)
        for i, r in enumerate(rows):
            r.shift(UP * (1.6 - 0.58 * i))
        cap = note(r"random permutations, \ computed; \ the ratio tends to $2$ \ (Vershik--Kerov, Logan--Shepp, 1977)",
                   font_size=22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The bound is sharp. <bookmark mark='a'/> Three, two, one, six, five, four, nine, eight, seven: nine "
            "numbers, and the longest run either way is three. <bookmark mark='b'/> And for a random order of n numbers, "
            "the theorem promises a run of about root n. The truth, computed here for random permutations up to a "
            "hundred thousand, is about twice that: the longest increasing run, divided by root n, creeps up towards two, "
            "a fact proved in 1977. Patience sorting, a card game, computes this length, and Part 22 meets it as an "
            "algorithm for longest increasing subsequences."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(dots, lag_ratio=0.1), FadeIn(tl), FadeIn(seq_t))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.3), run_time=2.4)
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compression(self):
        head = label(r"No compressor shrinks everything", font_size=38).to_edge(UP, buff=0.35)
        L = VGroup(*[Text(format(k, "03b"), font="DejaVu Sans Mono", font_size=24, color=DATA) for k in range(8)]).arrange(
            DOWN, buff=0.18).move_to(LEFT * 3.2 + DOWN * 0.2)
        shorter = [""] + [format(k, f"0{n}b") for n in (1, 2) for k in range(2 ** n)]
        R = VGroup(*[Text(s if s else "ε", font="DejaVu Sans Mono", font_size=24, color=CTRL) for s in shorter]).arrange(
            DOWN, buff=0.24).move_to(RIGHT * 1.0 + DOWN * 0.2)
        ll = label(r"$2^3 = 8$ strings of length 3", font_size=26, color=DATA).next_to(L, UP, buff=0.3)
        rl = label(r"$1 + 2 + 4 = 7$ shorter strings", font_size=26, color=CTRL).next_to(R, UP, buff=0.3)
        arrows = VGroup(*[Arrow(L[k].get_right(), R[k].get_left(), buff=0.15, stroke_width=2.5, color=GREY_C,
                                max_tip_length_to_length_ratio=0.08) for k in range(7)])
        left_over = Arrow(L[7].get_right(), R[6].get_left(), buff=0.15, stroke_width=3, color=NO,
                          max_tip_length_to_length_ratio=0.08)
        txt = VGroup(label(r"two inputs would share an output, \\ and could not both be recovered", font_size=26,
                           color=NO),
                     label(r"so a lossless compressor \\ that shrinks some inputs \\ must lengthen others", font_size=26,
                           color=YES),
                     note(r"\textit{AI, Built}, Part 1: \ compression is prediction", font_size=22)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.4).move_to(RIGHT * 4.6 + DOWN * 0.2)
        with self.voiceover(
            "One more, with a practical sting. <bookmark mark='a'/> There are eight bit strings of length three, and only "
            "seven strictly shorter ones, counting the empty string. <bookmark mark='b'/> A compressor that made every "
            "length-three input shorter would have to send two of them to the same output, and then it could not tell "
            "them apart when decompressing. <bookmark mark='c'/> The same count works at every length: two to the n "
            "strings of length n, two to the n minus one shorter ones. So every lossless compressor that shrinks some "
            "files makes others longer. Compressors win only because the files we care about are not random, which is "
            "where AI, Built began."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(L), FadeIn(ll), FadeIn(R), FadeIn(rl))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), run_time=1.6)
            self.play(GrowArrow(left_over), FadeIn(txt[0]))
            vo.wait_until("c")
            self.play(FadeIn(txt[1]), FadeIn(txt[2]))
        self.wait(0.3)
        self.clear_scene()
