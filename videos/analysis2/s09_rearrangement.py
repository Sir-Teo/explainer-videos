from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis2.common import load, plain_axes, polyline


def log_axes(x_max_exp, y_range, x_length=10.8, y_length=4.0, center=(0.2, -1.0, 0)):
    ax = plain_axes([0, x_max_exp + 0.1, 1], y_range, x_length, y_length, numbers=False).move_to(center)
    ticks = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=22, color=GREY_B).next_to(ax.c2p(k, y_range[0]), DOWN, buff=0.12)
                     for k in range(0, int(x_max_exp) + 1)])
    return ax, ticks


class Rearrangement(VoiceoverScene):
    def construct(self):
        self.card()
        self.piles()
        self.overshoot()
        self.swing()
        self.safe()
        self.fourier()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(8, r"Rearrangements", r"Which infinite sums can be reordered?", lit=(1854,), part=2)
        with self.voiceover(
            "Chapter eight. Back to the hook, where reordering one series produced any sum we liked. Riemann proved "
            "this in the same 1854 work where he defined his integral. Now we have the tools to see why it works, and "
            "when it can't happen."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def piles(self):
        head = label(r"\textbf{Rudin 3.54} \ If $\sum a_n$ converges, but not absolutely, then for any "
                     r"$-\infty \le \alpha \le \beta \le \infty$", font_size=28).to_edge(UP, buff=0.4)
        head2 = label(r"some rearrangement has partial sums with $\liminf = \alpha$ and $\limsup = \beta$.", font_size=28)
        head2.next_to(head, DOWN, buff=0.1)
        w = 0.36
        pos = VGroup(*[Rectangle(width=0.32, height=2.2 / (2 * k + 1), stroke_width=0, fill_color=C.SEQ,
                                 fill_opacity=0.85).move_to([-5.6 + w * k, -0.6 + 1.1 / (2 * k + 1), 0])
                       for k in range(14)])
        neg = VGroup(*[Rectangle(width=0.32, height=2.2 / (2 * k + 2), stroke_width=0, fill_color=C.PATHOLOGY,
                                 fill_opacity=0.85).move_to([0.9 + w * k, -0.6 + 1.1 / (2 * k + 2), 0])
                       for k in range(14)])
        pl = MathTex(r"p_n:\ 1, \tfrac13, \tfrac15, \ldots", font_size=30, color=C.SEQ).next_to(pos, DOWN, buff=0.3)
        nl = MathTex(r"q_n:\ \tfrac12, \tfrac14, \tfrac16, \ldots", font_size=30, color=C.PATHOLOGY).next_to(neg, DOWN,
                                                                                                            buff=0.3)
        facts = VGroup(label(r"$\sum p_n = \infty$ \ and \ $\sum q_n = \infty$ \ (if either were finite, $\sum |a_n|$ "
                             r"would be too)", font_size=26),
                       label(r"and $p_n, q_n \to 0$ \ (the series converges)", font_size=26)).arrange(DOWN, buff=0.12)
        facts.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Rudin's version is even stronger than the hook. <bookmark mark='t'/> If a series converges but not "
            "absolutely, then for any two targets alpha below beta there's a rearrangement whose partial sums have lower "
            "limit alpha and upper limit beta. <bookmark mark='a'/> Split the terms into two piles: the positive ones, "
            "<bookmark mark='b'/> and the sizes of the negative ones. <bookmark mark='c'/> Both piles have infinite sums: "
            "if one pile were finite, then since the series converges the other would be too, and the series would "
            "converge absolutely. <bookmark mark='d'/> And in both piles the terms go to zero."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(head), FadeIn(head2))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in pos], lag_ratio=0.06), FadeIn(pl))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in neg], lag_ratio=0.06), FadeIn(nl))
            vo.wait_until("c")
            self.play(FadeIn(facts[0]))
            vo.wait_until("d")
            self.play(FadeIn(facts[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def overshoot(self):
        d = load("rearrange")
        s, t = d["s_pi"], d["t_pi"]
        K = len(s)
        X1 = math.log10(K) + 0.1
        ax, ticks = log_axes(math.log10(K), [2.0, 4.2, 0.5], x_length=10.8, y_length=4.4, center=(0.2, -1.0, 0))
        yl = VGroup(*[MathTex(f"{v:g}", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (2, 3, 4)])
        k = np.arange(1, K + 1)
        lk = np.log10(k)
        curve = polyline(ax, lk, np.clip(s[:K], 2.0, 4.2), color=C.SEQ, stroke_width=2)
        pi_l = DashedLine(ax.c2p(0, math.pi), ax.c2p(X1, math.pi), color=WHITE, stroke_width=1.5)
        # the overshoot bound: between crossings, |s_k - pi| is at most the term that made the last crossing; take the
        # running max over the later crossings, a nonincreasing envelope
        e = s[:K] - math.pi
        cross = [j for j in range(1, K) if e[j - 1] * e[j] <= 0 or (j == 1 and e[0] >= 0)]
        k0 = cross[0]
        last = np.searchsorted(cross, np.arange(k0, K), side="right") - 1
        ct = np.abs(t[cross])
        later_max = np.maximum.accumulate(ct[::-1])[::-1]
        env = later_max[last]
        e_hi = polyline(ax, lk[k0:], np.clip(math.pi + env, 2.0, 4.2), color=C.EPS, stroke_width=2.5)
        e_lo = polyline(ax, lk[k0:], np.clip(math.pi - env, 2.0, 4.2), color=C.EPS, stroke_width=2.5)
        head = VGroup(label(r"The algorithm: \ add $p$'s until the sum exceeds the target, then $q$'s until it is below; "
                            r"repeat.", font_size=27),
                      label(r"Each crossing overshoots by at most the last term used, and those terms $\to 0$.",
                            font_size=27, color=C.EPS)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.4)
        pl = MathTex(r"\pi", font_size=32).next_to(ax.c2p(X1, math.pi), RIGHT, buff=0.1)
        with self.voiceover(
            "Now the hook's algorithm, which is Rudin's proof. <bookmark mark='a'/> Take positive terms until the sum "
            "passes the target, then negative terms until it falls below, and repeat; here on a logarithmic axis, out "
            "to four thousand terms. Because each pile is infinite, "
            "every crossing happens: there's always enough left. <bookmark mark='b'/> Every term eventually gets used. "
            "<bookmark mark='c'/> And each time the sum crosses the target, it overshoots by at most the last term "
            "used. Those terms go to zero, so the overshoots do too: the rearranged series converges to pi."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head[0]), Create(ax), FadeIn(ticks), FadeIn(yl), Create(pi_l), FadeIn(pl))
            self.play(Create(curve), run_time=2.5)
            vo.wait_until("b")
            self.wait(0.2)
            vo.wait_until("c")
            self.play(FadeIn(head[1]), Create(e_hi), Create(e_lo))
        assert np.all(np.abs(s[k0:K] - math.pi) <= env + 1e-15)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def swing(self):
        d = load("swing")
        s = d["sums"]
        al, be = float(d["alpha"]), float(d["beta"])
        K = len(s)
        ax, ticks = log_axes(math.log10(K), [-0.6, 1.6, 0.5], center=(0.2, -1.0, 0))
        k = np.arange(1, K + 1)
        curve = polyline(ax, np.log10(k), np.clip(s, -0.6, 1.6), color=C.FREQ, stroke_width=2)
        lines = VGroup(DashedLine(ax.c2p(0, be), ax.c2p(math.log10(K) + 0.1, be), color=C.EPS, stroke_width=2),
                       DashedLine(ax.c2p(0, al), ax.c2p(math.log10(K) + 0.1, al), color=C.CLOSED_SET, stroke_width=2))
        labs = VGroup(MathTex(r"\beta = 1", font_size=28, color=C.EPS).next_to(ax.c2p(math.log10(K) + 0.1, be), RIGHT,
                                                                               buff=0.1),
                      MathTex(r"\alpha = 0", font_size=28, color=C.CLOSED_SET).next_to(ax.c2p(math.log10(K) + 0.1, al),
                                                                                       RIGHT, buff=0.1))
        yl = VGroup(*[MathTex(f"{v:g}", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0, 0.5, 1, 1.5)])
        head = label(r"Two targets: \ climb past $\beta$, fall below $\alpha$, forever", font_size=32).to_edge(UP, buff=0.4)
        sub = label(r"the turning points approach $\beta$ and $\alpha$; \ every value in between is a subsequential "
                    r"limit", font_size=26, color=GREY_A).next_to(head, DOWN, buff=0.12)
        with self.voiceover(
            "With two targets, the same idea gives any upper and lower limits. <bookmark mark='a'/> Climb past one, "
            "then fall below zero, then climb past one again, forever. On a logarithmic axis, each swing takes about "
            "seven times as many terms as the last, <bookmark mark='b'/> and the turning points close in on the two "
            "targets: the lim sup is one and the lim inf is zero."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks), FadeIn(yl), Create(lines), FadeIn(labs))
            vo.wait_until("a")
            self.play(Create(curve), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(sub))
            dots = VGroup(*[Dot(ax.c2p(math.log10(j + 1), s[j]), radius=0.06, color=WHITE)
                            for j in list(d["peaks"]) + list(d["troughs"])])
            self.play(LaggedStart(*[FadeIn(x, scale=1.5) for x in dots], lag_ratio=0.1))
        pk = d["peaks"]
        assert np.all(np.diff(s[pk] - be) < 0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def safe(self):
        thm = label(r"\textbf{Rudin 3.55} \ If $\sum a_n$ converges absolutely, every rearrangement converges to the "
                    r"same sum.", font_size=30).to_edge(UP, buff=0.45)
        N = 6
        toks = VGroup(*[MathTex(rf"a_{{{i}}}", font_size=34) for i in range(1, 13)]).arrange(RIGHT, buff=0.35)
        toks.move_to([0, 1.2, 0])
        for i in range(N):
            toks[i].set_color(C.EPS)
        brace = Brace(VGroup(*toks[N:]), DOWN, color=GREY_B)
        bl = MathTex(r"\sum_{n > N} |a_n| < \varepsilon", font_size=30).next_to(brace, DOWN, buff=0.1)
        order = [3, 7, 1, 10, 0, 5, 2, 8, 4, 11, 6, 9]
        rt = VGroup(*[MathTex(rf"a_{{{i + 1}}}", font_size=34, color=C.EPS if i < N else WHITE) for i in order]).arrange(
            RIGHT, buff=0.35).move_to([0, -1.2, 0])
        mark = 8  # by this point the rearrangement has used a_1 ... a_N
        mbr = Brace(VGroup(*rt[:mark + 1]), DOWN, color=C.EPS)
        ml = label(r"once $a_1, \ldots, a_N$ have all appeared, the two partial sums differ only by terms beyond $N$: "
                   r"less than $\varepsilon$", font_size=24, color=GREY_A).next_to(mbr, DOWN, buff=0.15)
        with self.voiceover(
            "Absolute convergence makes all this impossible. <bookmark mark='t'/> If the absolute values have a finite "
            "sum, every rearrangement converges, to the same value. <bookmark mark='a'/> Given epsilon, choose N so that "
            "all the terms past N have total size less than epsilon. <bookmark mark='b'/> A rearrangement shuffles the "
            "terms, but after finitely many steps it has used each of the first N. <bookmark mark='c'/> From then on, "
            "the original and rearranged partial sums share those terms, and differ only by terms past N, whose total "
            "size is less than epsilon."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(FadeIn(toks), FadeIn(brace), FadeIn(bl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.3) for x in rt], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(mbr), FadeIn(ml))
        assert set(order[:mark + 1]) >= set(range(N))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fourier(self):
        d = load("swing")
        s = d["sin_sums"]
        K = len(s)
        ax, ticks = log_axes(math.log10(K), [0.5, 3.5, 0.5], center=(0.2, -1.1, 0))
        yl = VGroup(*[MathTex(f"{v:g}", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (1, 2, 3)])
        k = np.arange(1, K + 1)
        curve = polyline(ax, np.log10(k), s, color=C.APPROX, stroke_width=2.5)
        nat = DashedLine(ax.c2p(0, (math.pi - 1) / 2), ax.c2p(math.log10(K) + 0.1, (math.pi - 1) / 2), color=C.FUNC,
                         stroke_width=2)
        tgt = DashedLine(ax.c2p(0, 3), ax.c2p(math.log10(K) + 0.1, 3), color=C.EPS, stroke_width=2)
        nl = MathTex(r"\tfrac{\pi - 1}{2}", font_size=28, color=C.FUNC).next_to(nat, RIGHT, buff=0.1)
        tl = MathTex(r"3", font_size=28, color=C.EPS).next_to(tgt, RIGHT, buff=0.1)
        head = VGroup(label(r"The sawtooth series is conditionally convergent:", font_size=30),
                      MathTex(r"\sum_k \frac{\sin k}{k}, \text{ reordered greedily, sums to } 3", font_size=34,
                              color=C.APPROX)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        used = [int(v) for v in d["sin_used"]]
        stat = label(rf"after $2 \times 10^6$ terms: \ {float(d['sin_final']):.5f}, \ using {fmt_int(used[0])} "
                     rf"positive terms and only {fmt_int(used[1])} negative ones", font_size=24, color=GREY_A)
        stat.to_edge(DOWN, buff=0.2)
        moral = label(r"So the order of a Fourier series (by frequency) is part of its meaning.", font_size=28,
                      color=C.EPS).next_to(stat, UP, buff=0.15)
        with self.voiceover(
            "And the Fourier thread. <bookmark mark='a'/> The sawtooth series at x equal to one converges to pi minus "
            "one over two, but only conditionally. <bookmark mark='b'/> So it, too, can be reordered to sum to anything. "
            "Here it is, steered to three. <bookmark mark='c'/> After two million terms it's within three hundred "
            "thousandths, having used nearly all the positive terms and only a couple of thousand negative ones. "
            "<bookmark mark='d'/> When we write a Fourier series, the order, by frequency, is part of what we mean. "
            "Summing in a different way is an interchange of limits, and that's exactly the question the rest of the "
            "series is about."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head[0]), Create(ax), FadeIn(ticks), FadeIn(yl), Create(nat), FadeIn(nl))
            vo.wait_until("b")
            self.play(FadeIn(head[1]), Create(tgt), FadeIn(tl))
            self.play(Create(curve), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(stat))
            vo.wait_until("d")
            self.play(FadeIn(moral))
        assert abs(float(d["sin_final"]) - 3) < 1e-4
        self.wait(0.5)
        self.clear_scene()
