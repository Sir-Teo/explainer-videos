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
            label('$2\\log_2n$ is an asymptotic reference, not a finite uniqueness certificate', font_size=20,
                  color=GREY_A),
            label(rf"by degrees, \ in polynomial time: \\ none below 70, \ {r70 * 100:.0f}\% at 70, \ all from 80",
                  font_size=20, color=YES),
            label('spectral recovery: sufficiently large $c\\sqrt n$ in its stated random model',
                  font_size=20, color=NO),
            label(r"the \textbf{planted clique conjecture}: \\ between the lines, \ no efficient algorithm", font_size=20,
                  color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(ax, RIGHT, buff=0.7).align_to(ax, UP).shift(UP * 0.3)
        fit_right(notes)
        with self.voiceover(
            "Worst-case NP-hardness does not establish average-case cryptographic hardness. Planted clique gives a specific distributional example. <bookmark mark='a'/> Generate a thousand-vertex random graph with independent fair edges, then plant a clique on a uniformly chosen vertex subset. Every actual graph and planted subset is retained. <bookmark mark='b'/> Twice the base-two logarithm of n is a rough asymptotic reference for the largest background clique. It is not a deterministic finite threshold proving uniqueness of the planted set. <bookmark mark='c'/> The degree heuristic selects high-degree vertices and applies the stated score-based cleanup. Each plotted recovery rate uses twenty actual trials, so sampling uncertainty matters. <bookmark mark='d'/> Spectral algorithms reach different size regimes under their own assumptions and success guarantees. The finite degree experiment does not establish an optimal recovery threshold. <bookmark mark='e'/> Planted-clique hardness conjectures specify the clique-size regime, distribution, recovery or detection task and computational model. <bookmark mark='f'/> Information-theoretic identifiability and efficient recoverability are different questions. We do not infer either general theorem merely from this plotted curve."
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
        xl = label('median actual product bit length', font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.35)
        def lg(t):
            return math.log10(t) + 8
        mp = [ax.c2p(sorted(r["actual_bits"])[len(r["actual_bits"]) // 2], lg(r["mul_s"])) for r in d["rows"]]
        fp = [ax.c2p(sorted(r["actual_bits"])[len(r["actual_bits"]) // 2], lg(r["factor_s"])) for r in d["rows"]]
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
            label(rf"{min(last['actual_bits'])}--{max(last['actual_bits'])} actual bits: \ multiplying takes {last['mul_s'] * 1e9:.0f} ns; \\ factoring, \ "
                  rf"{last['factor_s']:.1f} s", font_size=20, color=NO),
            label('rho: balanced-factor random-map heuristic $N^{1/4}$; bounded runs and full update counts', font_size=20, color=GREY_A),
            label('number field sieve: a stronger factoring method; RSA-250 (2020) is a dated example', font_size=20, color=HEAD),
            label(r"nobody has \textbf{proved} any function one-way: \\ that would prove P $\ne$ NP", font_size=20,
                  color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "A one-way function must be efficiently computable yet hard for every probabilistic polynomial-time inverter on its specified random-input distribution. <bookmark mark='a'/> Success means finding any valid preimage, and the allowed success probability must be negligible as the security parameter grows. A finite timing difference is not that definition. <bookmark mark='b'/> The experiment multiplies sampled balanced primes and factors their products with bounded Brent-style rho. We retain every prime, actual product bit length, factor, raw timing and count of all modular orbit updates. <bookmark mark='c'/> The familiar fourth-root-of-the-product rho estimate assumes balanced factors and random-map heuristic behaviour. Actual trials can vary, and budget exhaustion returns no factor without a primality or hardness conclusion. <bookmark mark='d'/> More powerful factoring methods exist; dated record factorizations and this small rho implementation should not be conflated. <bookmark mark='e'/> Factoring-based one-way-function candidates require an appropriate input and preimage domain and an average-case hardness assumption. Their existence does not follow from P differing from NP alone."
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
            label('Ajtai: specified average-case lattice problems from worst-case approximate lattice assumptions',
                  font_size=22, color=HEAD),
            label(r"\textbf{Regev} \ (2005): \ learning with errors; \ the basis of post-quantum public keys \ "
                  r"(ML-KEM, \ Part 30)", font_size=22, color=LAM),
            label(r"but basing cryptography on NP-hardness itself seems out of reach \ (Feigenbaum and Fortnow; \ "
                  r"Bogdanov and Trevisan)", font_size=22, color=NO),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Average-case complexity provides the bridge from algorithms to cryptographic assumptions. <bookmark mark='a'/> Levin’s distributional problems specify both a language and an efficiently samplable input distribution; the reduction must preserve the relevant average-case guarantees. <bookmark mark='b'/> Håstad, Impagliazzo, Levin and Luby showed that one-way functions imply pseudorandom generators, with the necessary quantitative reductions. <bookmark mark='c'/> Further constructions give fundamental private-key primitives. Public-key encryption requires additional capabilities and does not follow from an arbitrary one-way function by this theorem. <bookmark mark='d'/> Ajtai’s lattice results relate particular average-case problems to specified worst-case approximate lattice problems, with dimension and approximation parameters. <bookmark mark='e'/> Regev’s original LWE result uses a quantum reduction from appropriate worst-case lattice problems under its modulus and noise conditions. This is not a proof that every lattice problem or every encryption system is secure. <bookmark mark='f'/> Worst-case-to-average-case reductions from unrestricted NP-complete problems face known barriers in particular reduction models. Those barriers do not establish that cryptography is impossible."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
