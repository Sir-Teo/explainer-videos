from __future__ import annotations

import math

import numpy as np

from videos.stats.stats43.common import *  # noqa: F403


class LargeDeviations(VoiceoverScene):
    def construct(self):
        self.card()
        self.cramer()
        self.rate()
        self.urn()
        self.sanov()

    def card(self):
        card = chapter_card(12, r"Large deviations", r"How rare is a rare event?", lit=(1938,), part=PART)
        with self.voiceover("Chapter twelve. Large deviations: how rare is a rare event?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def cramer(self):
        rows = [
            cmath(r"\Lambda(t)", r"=", r"\log E e^{tX}, \ \ I(a) = \sup_t \big(t a - \Lambda(t)\big)", font_size=34),
            cmath(r"\text{Chernoff}", r":", r"P(\bar X_n \ge a) \le e^{-t n a} E e^{t S_n} = e^{-n(ta - \Lambda(t))} \ \forall t \ge 0", font_size=30),
            cmath(r"\text{so}", r":", r"P(\bar X_n \ge a) \le e^{-n I(a)} \ \ (a > \mu)", font_size=34),
            cmath(r"\text{Cram\'er}", r":", r"\tfrac1n \log P(\bar X_n \ge a) \to -I(a)", font_size=34),
        ]
        rows[3][-1].set_color(S.ACCENT)
        whys = [why(r"the rate: \ a Legendre transform"), why(r"Markov on $e^{t S_n}$"), why(r"optimize $t$"), why(r"Cram\'er (1938): \ exponential rate; iid and MGF near zero")]
        with self.voiceover(
            "<bookmark mark='a'/> The central limit theorem describes deviations of the order of one over root n. For"
            " iid summands whose MGF is finite near zero, Cramer's theorem describes fixed deviations from the mean "
            "on an exponential probability scale. Heavy-tailed laws need not have this behavior. The rate is a "
            "Legendre transform: the supremum over t of t a minus the log moment generating function. <bookmark "
            "mark='b'/> The upper bound is Markov's inequality applied to e to the t S n, for any positive t. "
            "<bookmark mark='c'/> Optimizing t gives Chernoff's bound, e to the minus n times the rate. <bookmark "
            "mark='d'/> Harald Cramér, an actuary as well as a mathematician, proved in 1938, with insurance ruin in "
            "mind, that exponential rate; iid and MGF near zero on the exponential scale: the logarithm of the probability, divided by n, "
            "tends to minus the rate."
        ) as vo:
            heading=label('Cramer large deviations require a finite MGF near zero',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rate(self):
        d = load("ld")
        a = np.asarray(d["a"])
        A = axes([0, 1], [0, 1.2], x_length=7.4, y_length=4.4, xlabel=r"$a$", ylabel=r"$I(a)$, \ Bernoulli($0.6$)", xticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
                 yticks=[0, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        ra = clip_curve(ax, a, d["rate"], LAWC, 4, ymax=1.2)
        qu = clip_curve(ax, a, d["quad"], LIMC, 3, ymax=1.2)
        side = fit_rows(VGroup(
            label(r"$I(a) = a \log\frac{a}{p} + (1 - a)\log\frac{1 - a}{1 - p}$", font_size=24, color=LAWC),
            label(r"$= \text{KL}(a \,\|\, p)$: \ a Kullback--Leibler divergence", font_size=24, color=LAWC),
            label(r"gold: \ the CLT's $(a - p)^2 / (2p(1 - p))$", font_size=24, color=LIMC),
            label(r"they agree near $p$; \ far out, \ the CLT is wrong", font_size=24, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For coin flips with success probability point six, the rate function has a closed form, "
            "<bookmark mark='b'/> and it is a Kullback–Leibler divergence: how far the observed frequency a is from p in "
            "information. <bookmark mark='c'/> In gold, the quadratic rate that the normal approximation implies. <bookmark "
            "mark='d'/> Near p the two agree, which is why the central limit theorem works for moderate deviations; far from "
            "p the quadratic is wrong in both directions, and normal approximations to very small tail probabilities can be "
            "off by orders of magnitude. That is the regime of the p-values in a genome scan, Part thirty-three."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(ra), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(qu), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def urn(self):
        d = load("ld")
        ns = np.log10(np.asarray(d["ns"], float))
        A = axes([2, 4.5], [-6, 0], x_length=7.4, y_length=4.4, xlabel=r"draws $n$", ylabel=r"$P(|\bar X_n - 0.6| \ge 0.02)$",
                 xticks=[2, 3, 4], yticks=[-6, -4, -2, 0], log_x=True, xfmt=lambda v: f"10^{{{int(v)}}}", yfmt=lambda v: f"10^{{{int(v)}}}",
                 center=[-2.5, 0.2, 0])
        ax = A.ax
        lg = lambda v: np.log10(np.maximum(np.asarray(v, float), np.finfo(float).tiny))  # noqa: E731
        ex = clip_curve(ax, ns, lg(d["exact"]), LAWC, 4, ymin=-6)
        cl = clip_curve(ax, ns, lg(d["clt"]), LIMC, 3, ymin=-6)
        ch = clip_curve(ax, ns, lg(d["chernoff"]), S.PRIOR, 3, ymin=-6)
        tgt = DashedLine(ax.c2p(2, math.log10(d["target"])), ax.c2p(4.5, math.log10(d["target"])), color=GREY_B, stroke_width=2)
        bern = DashedLine(ax.c2p(math.log10(d["n_bernoulli"]), -6), ax.c2p(math.log10(d["n_bernoulli"]), 0), color=BADC, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(r"Bernoulli's urn: \ 3 white, \ 2 black; \ odds 1000:1", font_size=22),
            label(rf"exact, safe for all later sizes: \ $n = {d['n_exact']:,}$", font_size=22, color=LAWC),
            label(rf"normal approximation: \ $n = {d['n_clt']:,}$", font_size=22, color=LIMC),
            label(rf"Chernoff's bound: \ $n = {d['n_chernoff']:,}$ \ (guaranteed)", font_size=22, color=S.PRIOR),
            label(rf"Bernoulli's own bound (1713): \ $n = {d['n_bernoulli']:,}$", font_size=22, color=BADC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Part six's oldest example. Jacob Bernoulli asked how many draws from an urn with three white tokens to two black would make it a thousand to one that the observed share lies within one fiftieth of three fifths. <bookmark mark='b'/> The first admissible exact sample size is 6,481, but lattice oscillations can take later sizes back above the threshold. Checking every size through the Chernoff cutoff gives a sample size safe for every larger n of {d['n_exact']:,} draws. <bookmark mark='c'/> The normal approximation gets close, at {d['n_clt']:,}: this is a moderate deviation. <bookmark mark='d'/> Chernoff's large-deviation bound, which is a guarantee rather than an approximation, needs {d['n_chernoff']:,}. <bookmark mark='e'/> Bernoulli's own bound, in 1713, demanded {d['n_bernoulli']:,}. The exponential rate he did not have is the difference between a theorem and a useful one."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tgt), FadeIn(museum_tag(r"Bernoulli, \ \emph{Ars Conjectandi} (1713), \ IV.5")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ex), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ch), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(bern), FadeIn(side[4]))
        self.clear_scene()

    def sanov(self):
        rows = fit_rows(VGroup(
            label(r"Sanov (1957): \ the empirical law $L_n$ of $n$ draws from $P$", font_size=26),
            label(r"$P(L_n \in A)\approx e^{-n\inf_{Q\in A}\mathrm{KL}(Q\|P)}$ for rate-continuity sets", font_size=28, color=LAWC),
            label(r"the most likely way for something unlikely to happen: \ the nearest $Q$ in KL", font_size=24, color=S.ACCENT),
            label(r"testing $P$ against $Q$: \ the best type II error decays like $e^{-n \, \text{KL}(P \| Q)}$ \ (Stein's lemma, \ Part 46)", font_size=24, color=GOODC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Ivan Sanov lifted Cramér's theorem from averages to whole empirical distributions. "
            "<bookmark mark='b'/> The chance that the empirical law of n draws from P falls in a set A decays like e "
            "to the minus n times the infimum of KL of Q relative to P over Q in A, when the interior and closure "
            "rate bounds agree. In general Sanov gives lower and upper bounds for the interior and closure rather "
            "than equality for every set. <bookmark mark='c'/> Conditioned on the rare event, under the additional "
            "regularity and uniqueness conditions for Gibbs conditioning, the sample concentrates near the minimizing"
            " law: the most likely way for something unlikely to happen. <bookmark mark='d'/> In testing, the same "
            "divergence is the exponent of the best type two error, Chernoff and Stein's lemma, which Part forty-six "
            "proves."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
