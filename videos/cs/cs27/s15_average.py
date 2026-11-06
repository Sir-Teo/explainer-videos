from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs27.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, load, words)


class Average(VoiceoverScene):
    def construct(self):
        self.card()
        self.planted()
        self.oneway()
        self.bridge()

    def card(self):
        card = chapter_card(14, r"Average case and one-way functions", r"Can hardness be put to work?",
                            lit=(1986, 2005), extra=((1986, r"Levin"), (1996, r"Ajtai"), (2005, r"Regev: \ LWE")),
                            part=PART)
        with self.voiceover("Chapter fourteen. Average case, and one-way functions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def planted(self):
        d = load("planted")
        n = d["n"]
        head = label(r"A hidden clique", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 130, 20], y_range=[0, 1.05, 0.25], x_length=6.0, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.7).to_edge(
            LEFT, buff=1.0)
        xt = VGroup(*[label(str(x), font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in (20, 40, 60, 80, 100, 120)])
        yt = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.08)
                      for y, t in ((0.5, r"50\%"), (1.0, r"100\%"))])
        xl = label(r"size $k$ of the planted clique", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.35)
        yl = label(r"recovered", font_size=17, color=GREY_A).rotate(PI / 2).next_to(ax, LEFT, buff=0.45)
        pts = [ax.c2p(r["k"], r["rate"]) for r in d["rows"]]
        dots = VGroup(*[Dot(p, radius=0.07, color=YES) for p in pts])
        curve = VMobject(color=YES, stroke_width=2.5).set_points_as_corners(pts)
        x1, x2 = d["two_log"], d["sqrt_nlogn"]
        v1 = DashedLine(ax.c2p(x1, 0), ax.c2p(x1, 1.05), color=HEAD, stroke_width=2)
        v2 = DashedLine(ax.c2p(x2, 0), ax.c2p(x2, 1.05), color=NO, stroke_width=2)
        l1 = label(r"$2 \log_2 n$", font_size=17, color=HEAD).next_to(v1, UP, buff=0.08)
        l2 = label(r"$\sqrt{n \ln n}$", font_size=17, color=NO).next_to(v2, UP, buff=0.08)
        r70 = next(r["rate"] for r in d["rows"] if r["k"] == 70)
        notes = VGroup(
            label(rf"a random graph on {words(n)} vertices; \\ hide a clique on $k$ of them", font_size=20,
                  color=WHITE),
            label(r"the largest clique occurring naturally: \\ about $2 \log_2 n \approx 20$", font_size=20,
                  color=HEAD),
            label(r"so above 20 the clique is \textbf{determined}: \\ exhaustive search would find it", font_size=20,
                  color=GREY_A),
            label(rf"by degrees, \ in polynomial time: \\ none below 70, \ {r70 * 100:.0f}\% at 70, \ all from 80",
                  font_size=20, color=YES),
            label(r"spectral methods reach $c\sqrt n$ \ (Alon, \\ Krivelevich, \ Sudakov, 1998): \ no better known",
                  font_size=20, color=NO),
            label(r"the \textbf{planted clique conjecture}: \\ between the lines, \ no efficient algorithm", font_size=20,
                  color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(ax, RIGHT, buff=0.7).align_to(ax, UP).shift(UP * 0.3)
        fit_right(notes)
        with self.voiceover(
            "NP-completeness is about the worst case. Cryptography needs problems that are hard on random instances. "
            "<bookmark mark='a'/> Here is the favourite test case. Take a random graph on a thousand vertices, and "
            "secretly add all the edges among k of them. <bookmark mark='b'/> A random graph already has cliques of "
            "about twice log n vertices, here about twenty. <bookmark mark='c'/> So once k is above twenty, the "
            "hidden clique is the only one that large, and trying every set of vertices would find it. <bookmark "
            "mark='d'/> A polynomial algorithm, taking the vertices of highest degree and cleaning up, finds nothing "
            "below seventy, and every clique from eighty on, near the square root of n log n. <bookmark mark='e'/> "
            "Spectral methods improve the constant, to any multiple of root n, but nobody knows a polynomial "
            "algorithm below that. <bookmark mark='f'/> The conjecture that none exists is now used as an assumption, "
            "like SETH, to explain why problems in statistics and machine learning have the same gap."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(v1), FadeIn(l1), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(p) for p in dots], lag_ratio=0.1), Create(curve), Create(v2), FadeIn(l2),
                      FadeIn(notes[3]), run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(notes[4]))
            vo.wait_until("f")
            self.play(FadeIn(notes[5]))
        self.wait(0.3)
        self.clear_scene()

    def oneway(self):
        d = load("oneway")
        head = label(r"Easy one way, \ hard the other", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[20, 84, 8], y_range=[0, 8, 1], x_length=6.0, y_length=3.8,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.6).to_edge(
            LEFT, buff=1.0)
        xt = VGroup(*[label(str(x), font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in (24, 40, 56, 72)])
        yt = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(ax.c2p(20, y + 8), LEFT, buff=0.08)
                      for y, t in ((-7, r"0.1 $\mu$s"), (-6, r"1 $\mu$s"), (-4, r"0.1 ms"), (-2, r"10 ms"),
                                   (0, r"1 s"))])
        xl = label(r"bits in $N = pq$", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.35)
        def lg(t):
            return math.log10(t) + 8
        mp = [ax.c2p(r["bits"], lg(r["mul_s"])) for r in d["rows"]]
        fp = [ax.c2p(r["bits"], lg(r["factor_s"])) for r in d["rows"]]
        md = VGroup(*[Dot(p, radius=0.07, color=DATA) for p in mp])
        fd = VGroup(*[Dot(p, radius=0.07, color=NO) for p in fp])
        ml = VMobject(color=DATA, stroke_width=2).set_points_as_corners(mp)
        fl = VMobject(color=NO, stroke_width=2).set_points_as_corners(fp)
        lm = label(r"multiply $p \times q$", font_size=18, color=DATA).next_to(md[-1], UP, buff=0.15).shift(LEFT * 0.7)
        lf = label(r"factor $N$ \ (Pollard's rho)", font_size=18, color=NO).next_to(fd[-1], LEFT, buff=0.15).shift(
            UP * 0.15)
        last = d["rows"][-1]
        notes = VGroup(
            label(r"a \textbf{one-way function}: \ easy to compute, \\ hard to invert \textbf{on random inputs}",
                  font_size=20, color=WHITE),
            label(rf"{last['bits']} bits: \ multiplying takes {last['mul_s'] * 1e9:.0f} ns; \\ factoring, \ "
                  rf"{last['factor_s']:.1f} s", font_size=20, color=NO),
            label(r"rho takes about $N^{1/4}$ steps: \ each 8 bits \\ cost about $4\times$", font_size=20, color=GREY_A),
            label(r"the best method, \ the number field sieve, \\ is subexponential: \ RSA-250 \ (829 bits) \\ fell in "
                  r"2020, \ after 2,700 core-years", font_size=20, color=HEAD),
            label(r"nobody has \textbf{proved} any function one-way: \\ that would prove P $\ne$ NP", font_size=20,
                  color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "Cryptography needs something stronger: a function that is easy to compute and hard to invert on random "
            "inputs. <bookmark mark='a'/> Multiplication is the classic candidate. <bookmark mark='b'/> Multiplying "
            "two forty-bit primes takes about fifty nanoseconds. Factoring their product with Pollard's rho method "
            "took half a second. <bookmark mark='c'/> Rho needs about the fourth root of N steps, so every eight "
            "more bits cost about four times as much. <bookmark mark='d'/> The best known method, the number field "
            "sieve, is faster, but still worse than polynomial: the 829-bit challenge number RSA-250 fell in 2020, "
            "after about two thousand seven hundred core-years. <bookmark mark='e'/> Yet nobody has proved any "
            "function one-way. A proof would imply P is not NP."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), LaggedStart(*[FadeIn(p) for p in md], lag_ratio=0.1), Create(ml), FadeIn(lm))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in fd], lag_ratio=0.1), Create(fl), FadeIn(lf), FadeIn(notes[1]))
            for mk, n_ in zip("cde", notes[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def bridge(self):
        head = label(r"From hardness to cryptography", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"\textbf{Levin} \ (1986): \ average-case completeness: \ problems hard on average if any "
                  r"distributional NP problem is", font_size=22, color=WHITE),
            label(r"\textbf{H\aa stad, \ Impagliazzo, \ Levin, \ Luby} \ (1999): \ any one-way function gives a "
                  r"pseudorandom generator", font_size=22, color=DATA),
            label(r"and from those: \ private-key encryption, \ signatures, \ commitments \ (chapter 7): \ "
                  r"\textbf{Minicrypt}", font_size=22, color=YES),
            label(r"\textbf{Ajtai} \ (1996): \ for lattices, \ the average case is as hard as the \textbf{worst} case",
                  font_size=22, color=HEAD),
            label(r"\textbf{Regev} \ (2005): \ learning with errors; \ the basis of post-quantum public keys \ "
                  r"(ML-KEM, \ Part 30)", font_size=22, color=LAM),
            label(r"but basing cryptography on NP-hardness itself seems out of reach \ (Feigenbaum and Fortnow; \ "
                  r"Bogdanov and Trevisan)", font_size=22, color=NO),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This is the bridge to the next acts of the series. <bookmark mark='a'/> Leonid Levin started a theory "
            "of average-case completeness in 1986. <bookmark mark='b'/> Johan Håstad, Russell Impagliazzo, Levin "
            "and Michael Luby proved that any one-way function at all can be turned into a pseudorandom generator. "
            "<bookmark mark='c'/> From those come private-key encryption, signatures and the commitments of chapter "
            "seven: Impagliazzo's Minicrypt. Part 29 builds it. <bookmark mark='d'/> Miklós Ajtai found problems on "
            "lattices whose random instances are as hard as their worst ones, <bookmark mark='e'/> and Oded Regev's "
            "learning with errors turned that into public-key encryption that resists quantum computers, now "
            "standardized, in Part 30. <bookmark mark='f'/> What nobody can do is base cryptography on an NP-complete "
            "problem: results of Joan Feigenbaum and Lance Fortnow, and of Andrej Bogdanov and Luca Trevisan, "
            "suggest the standard techniques cannot."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
