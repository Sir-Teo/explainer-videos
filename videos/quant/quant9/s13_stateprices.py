from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import (ARB, CALL, FWD, P_C, PART, Q_C, answer_under, illustration, load, pause_at,
                                        real_data)

S3 = np.array([80.0, 100.0, 125.0])
PI = np.array([0.25, 0.40, 0.35])   # an illustrative real-world measure (the stock's expected return is positive)


def segment(price):
    """The risk-neutral measures (q1, q2, q3) >= 0, summing to one, with q.S3 = price: the ends of the segment."""
    pts = []
    for i, j in ((0, 1), (0, 2), (1, 2)):
        a, b = S3[i], S3[j]
        if min(a, b) - 1e-9 <= price <= max(a, b) + 1e-9 and a != b:
            w = (price - b) / (a - b)
            q = np.zeros(3)
            q[i], q[j] = w, 1 - w
            pts.append(q)
    out = []
    for q in pts:
        if not any(np.allclose(q, r) for r in out):
            out.append(q)
    return out


class StatePrices(VoiceoverScene):
    def construct(self):
        f, k = load("ftap"), load("kernel")
        self.card()
        self.derive()
        self.bars(f)
        self.simplex_tri()
        self.kernel(k)
        self.predict()

    def card(self):
        c = chapter_card(5, r"State prices, the discount factor, and $Q$", r"Why is $Q$ not a forecast?",
                         lit=(1976,), part=PART)
        with self.voiceover("Chapter five. State prices, the discount factor, and Q."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        h = history_card(1964, r"Kenneth Arrow; Gerard Debreu (1959)", r"a security that pays one unit in a single "
                         r"state of the world and nothing in any other: with one for every state, any payoff can be "
                         r"built, and its price is the sum of state prices", width=5.0, font_size=20)
        h.to_corner(UL, buff=0.3)
        rows = [cmath(r"p", r"=", r"\sum_j \psi_j\, d_j", font_size=38, colors={r"p": FWD}),
                cmath(r"p", r"=", r"\sum_j \pi_j\,\frac{\psi_j}{\pi_j}\, d_j = \mathbb{E}^P[m\, d]", font_size=36,
                      colors={r"\mathbb{E}^P[m\, d]": P_C}),
                cmath(r"\sum_j \psi_j", r"=", r"\frac{1}{1 + r}", font_size=36),
                cmath(r"q_j = (1 + r)\psi_j", r"\Rightarrow", r"p = \frac{1}{1 + r}\,\mathbb{E}^Q[d]", font_size=36,
                      colors={r"p = \frac{1}{1 + r}\,\mathbb{E}^Q[d]": Q_C}),
                cmath(r"\frac{dQ}{dP}", r"=", r"\frac{q_j}{\pi_j} = (1 + r)\, m_j", font_size=36,
                      colors={r"\frac{dQ}{dP}": Q_C})]
        whys = [why(r"linear pricing: $\psi_j$ is the price of the Arrow security for state $j$ (Ross 1978)", 21),
                why(r"multiply and divide by the real probabilities $\pi_j > 0$: $m = \psi / \pi$ is the stochastic "
                    r"discount factor", 21),
                why(r"the bond pays 1 in every state: the state prices sum to its price", 21),
                why(r"rescale to sum to one: a probability $Q$, and prices are discounted $Q$-expectations", 21),
                why(r"the density of $Q$ with respect to $P$ is the discount factor, normalized: $Q$ is $P$ reweighted", 21)]
        step = ladder(self, rows, whys, keep=4, top=1.2, x=-0.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "Name that normal. Kenneth Arrow, in 1964, imagined a security paying one unit in a "
            "single state: its price is the state price, and any payoff is a bundle of them. "
            "<bookmark mark='a'/> Multiply and divide by each state's real probability: a price is an "
            "expectation of payoff times m, the stochastic discount factor. <bookmark mark='b'/> The "
            "bond pays one everywhere, so the state prices sum to one over one plus r. <bookmark "
            "mark='c'/> Rescale them to sum to one: a probability, Q, and prices are discounted "
            "Q-expectations, as Stephen Ross wrote in 1978. <bookmark mark='d'/> Q's density against "
            "P is the discount factor, normalized. Q is not a forecast: it is P reweighted."
            " A worked example with the state prices at a stock price of a hundred: five thirteenths, "
            "four thirteenths, four thirteenths. At zero rates they already sum to one, so this Q is "
            "the same three numbers, and a call struck at a hundred, paying twenty-five only in the "
            "boom, is worth four thirteenths of twenty-five, about seven point seven."
        ) as vo:
            self.play(FadeIn(h))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.3)
        self.clear_scene()

    def bars(self, f):
        psi = np.asarray(f["ftap_100"]["psi"])
        m = psi / PI
        q = psi / psi.sum()
        g = axes([0, 3], [0, 1.7], x_length=6.0, y_length=4.4, ylabel=r"", xticks=[], yticks=[0, 0.5, 1.0, 1.5],
                 font_size=17)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        names = VGroup(*[label(t, font_size=19, color=GREY_A).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.12)
                         for i, t in enumerate((r"crash: 80", r"flat: 100", r"boom: 125"))])
        tr = [ValueTracker(v) for v in PI]
        col = [ValueTracker(0.0)]

        def bar(i):
            def mk():
                v = tr[i].get_value()
                c = interpolate_color(ManimColor(P_C), ManimColor(Q_C), col[0].get_value())
                return Rectangle(width=1.1, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                 fill_color=c, fill_opacity=0.85).move_to(ax.c2p(i + 0.5, v / 2))
            return always_redraw(mk)

        bs_ = VGroup(*[bar(i) for i in range(3)])
        nums = VGroup(*[DecimalNumber(PI[i], num_decimal_places=2, font_size=24) for i in range(3)])
        for i, n_ in enumerate(nums):
            n_.add_updater(lambda mm, i=i: mm.set_value(tr[i].get_value()).next_to(ax.c2p(i + 0.5, tr[i].get_value()),
                                                                                   UP, buff=0.08))
        stage = [label(t, font_size=26, color=c) for t, c in
                 ((r"$P$: real probabilities (illustrative)", P_C), (r"$m = \psi/\pi$: the discount factor", ARB),
                  (r"$Q = (1 + r)\psi$: the same bars, renormalized", Q_C))]
        for s_ in stage:
            s_.next_to(g, UP, buff=0.15).align_to(g, LEFT)
        side = VGroup(
            MathTex(rf"\psi = ({psi[0]:.3f},\ {psi[1]:.3f},\ {psi[2]:.3f})", font_size=28, color=Q_C),
            MathTex(rf"m = ({m[0]:.2f},\ {m[1]:.2f},\ {m[2]:.2f})", font_size=28, color=ARB),
            MathTex(rf"Q = ({q[0]:.3f},\ {q[1]:.3f},\ {q[2]:.3f})", font_size=28, color=Q_C),
            MathTex(rf"\mathbb{{E}}^P[S_1] = {PI @ S3:.2f},\ \ \mathbb{{E}}^Q[S_1] = {q @ S3:.2f}", font_size=28),
            wrapped_label(r"the crash state's bar grows: the market pays more for a dollar there than its probability "
                          r"alone would say; under $Q$ the stock earns exactly the riskless rate (here zero)", 4.6, 20,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = illustration(r"$P$ illustrative; state prices from chapter 3's market at a stock price of 100, $r = 0$")
        with self.voiceover(
            "As one animation: three states, crash, flat, boom; amber bars are made-up real "
            "probabilities under which the stock should rise. <bookmark mark='a'/> Divide state "
            f"prices by them: the discount factor is {m[0]:.2f} in the crash, below one elsewhere. A "
            "dollar in a crash is dear. <bookmark mark='b'/> Renormalize and the bars turn purple: Q. "
            "The crash bar grew, the boom bar shrank, and under Q the stock is expected to stay at a "
            "hundred."
            " And the discount factor's average under P is the bond's price, one over one plus r: here "
            "exactly one."
        ) as vo:
            self.play(FadeIn(g), FadeIn(names), FadeIn(stage[0]), FadeIn(src), *[FadeIn(b_) for b_ in bs_],
                      FadeIn(nums))
            vo.wait_until("a")
            self.play(FadeOut(stage[0]), FadeIn(stage[1]), *[tr[i].animate.set_value(m[i]) for i in range(3)],
                      FadeIn(side[0]), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeOut(stage[1]), FadeIn(stage[2]), *[tr[i].animate.set_value(q[i]) for i in range(3)],
                      col[0].animate.set_value(1.0), FadeIn(side[2]), FadeIn(side[3]), run_time=2)
            self.play(FadeIn(side[4]))
        for n_ in nums:
            n_.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def simplex_tri(self):
        A_, B_, C_ = np.array([-3.0, -2.2, 0]), np.array([3.0, -2.2, 0]), np.array([0.0, 2.9, 0])

        def P2(q):
            return q[0] * A_ + q[1] * B_ + q[2] * C_

        tri = Polygon(A_, B_, C_, stroke_color=GREY_B, stroke_width=2, fill_color=GREY_E, fill_opacity=0.3)
        vl = VGroup(label(r"all mass on the crash", font_size=19).next_to(A_, DOWN, buff=0.15),
                    label(r"all mass on flat", font_size=19).next_to(B_, DOWN, buff=0.15),
                    label(r"all mass on the boom", font_size=19).next_to(C_, UP, buff=0.12))
        tri_g = VGroup(tri, vl).shift(LEFT * 2.6 + DOWN * 0.2)
        shift = LEFT * 2.6 + DOWN * 0.2
        p = ValueTracker(100.0)

        def seg():
            ends = segment(p.get_value())
            if len(ends) < 2:
                if len(ends) == 1:
                    return Dot(P2(ends[0]) + shift, radius=0.1, color=ARB)
                return VGroup()
            return Line(P2(ends[0]) + shift, P2(ends[1]) + shift, color=Q_C, stroke_width=8)

        S_ = always_redraw(seg)
        rd = DecimalNumber(100, num_decimal_places=0, font_size=30, color=FWD)
        rd.add_updater(lambda m: m.set_value(p.get_value()))
        side = VGroup(
            VGroup(label(r"stock price today", font_size=22, color=FWD), rd).arrange(RIGHT, buff=0.15),
            wrapped_label(r"the triangle: every probability on the three states; the purple segment: those that "
                          r"price the stock, $80 q_1 + 100 q_2 + 125 q_3 = $ its price", 4.8, 20, GREY_A),
            MathTex(r"\text{ends: } (\tfrac59, 0, \tfrac49)\ \text{ and } (0, 1, 0)", font_size=28, color=Q_C),
            wrapped_label(r"many measures: the market is incomplete (chapter 7); none: arbitrage, exactly when "
                          r"chapter 3's line pierced the corner", 4.8, 20, ARB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Here Q is not unique. The triangle holds every probability on three states. <bookmark "
            "mark='a'/> The measures that price the stock form the purple segment, from five ninths "
            "on the crash and four ninths on the boom, to everything on the flat state. <bookmark "
            "mark='b'/> Raise the price: the segment slides to the boom corner, shrinks to a point at "
            "a hundred and twenty-five, and leaves the triangle at the same price where the free "
            "payoffs pierced the corner."
            " Every point on the segment prices the bond and the stock correctly; the points disagree "
            "only about claims the two assets cannot build."
        ) as vo:
            self.play(FadeIn(tri_g), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.add(S_)
            self.play(FadeIn(side[2]))
            vo.wait_until("b")
            self.play(p.animate.set_value(125.0), run_time=3.5, rate_func=smooth)
            self.play(p.animate.set_value(130.0), FadeIn(side[3]), run_time=1.2)
        rd.clear_updaters()
        S_.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def kernel(self, k):
        x = np.asarray(k["grid"]) / k["F"]
        q, p_, m = (np.asarray(k[n]) for n in ("q", "p", "m"))
        lo, hi = np.asarray(k["lo"]), np.asarray(k["hi"])
        top = max(q.max(), p_.max())
        g1 = axes([0.8, 1.25], [0, 1.05], x_length=5.6, y_length=2.4, ylabel=r"densities at expiry (scaled)",
                  xticks=[], yticks=[], font_size=16)
        g2 = axes([0.8, 1.25], [0, 2.2], x_length=5.6, y_length=2.6, ylabel=r"$m = q / p$, the pricing kernel",
                  xlabel=r"bitcoin price at expiry, over the forward", xticks=[0.8, 0.9, 1.0, 1.1, 1.2],
                  yticks=[0, 1, 2], font_size=16)
        VGroup(g1, g2).arrange(DOWN, buff=0.45).to_edge(LEFT, buff=0.7).shift(DOWN * 0.1)
        qc = curve(g1.ax, x, q / top, Q_C, stroke_width=4)
        pc = curve(g1.ax, x, p_ / top, P_C, stroke_width=4)
        leg = legend([(Q_C, r"$q$: the Surface's 16-day density"), (P_C, r"$p$: 16-day returns, 2021--2025")],
                     font_size=17).move_to(g1.ax.c2p(1.13, 0.85))
        bd = band(g2.ax, x, np.clip(lo, 0, 2.2), np.clip(hi, 0, 2.2), ARB, 0.2)
        mc = curve(g2.ax, x, np.clip(m, 0, 2.2), ARB, stroke_width=4)
        one = DashedLine(g2.ax.c2p(0.8, 1), g2.ax.c2p(1.25, 1), color=GREY_C, stroke_width=1.5)
        right = ("falls steeply in the up states, beyond the band's reach of the peak" if k["right_sig"] else
                 "falls in the up states, but within the band")
        left = ("and rises again in the down states, as theory says it should" if k["rising_left"] else
                "but does not rise in the down states, as a decreasing kernel would; the band there is wide")
        side = VGroup(
            label(rf"{k['n_windows']} windows of {k['h_days']} days", font_size=22, color=P_C),
            wrapped_label(rf"the kernel peaks near {k['peak_x']:.2f} times the forward, at {k['peak_m']:.2f}; it {right}",
                          4.6, 20, ARB),
            wrapped_label(left, 4.6, 20, GREY_A),
            wrapped_label(r"a hump instead of a falling curve is the ``pricing kernel puzzle'' (Jackwerth 2000), "
                          r"found in index options and in bitcoin's", 4.6, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = real_data(r"$q$: Deribit, 10 Dec 2025 (the Surface); $p$: Binance BTCUSDT daily closes, Apr 2021--Nov 2025, "
                        r"Gaussian kernel; band: 1,000 stationary-bootstrap draws (5--95\%)")
        verdict = ("It has a hump: it rises toward the forward and falls away above it, beyond the band. "
                   if k["shape"] == "hump" else "It falls from left to right, as theory says. ")
        with self.voiceover(
            "Now a real discount factor. Q: the Surface's density for Bitcoin sixteen days out. P: "
            f"sixteen-day returns over four and a half years, {k['n_windows']} windows, smoothed. "
            "<bookmark mark='a'/> Their ratio is the pricing kernel, with a band from a thousand "
            "resamples. <bookmark mark='b'/> "
            f"{verdict}"
            "A risk-averse investor would make it fall everywhere; a hump is the pricing kernel "
            "puzzle Jens Jackwerth found in 2000. <bookmark mark='c'/> And the band is wide: P is the "
            "hard half of the ratio."
            f" Sixteen-day returns had a standard deviation of {100 * k['vol_ret']:.0f} percent over "
            "the sample."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(src), Create(qc), FadeIn(leg[0]))
            self.play(Create(pc), FadeIn(leg[1]), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(one), FadeIn(bd), Create(mc), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), Indicate(bd, color=ARB, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def predict(self):
        card = pause_at(r"In some state, $Q$ gives a crash twice the probability that $P$ does. Is the discount factor "
                        r"$m$ in that state above or below $1/(1 + r)$?")
        with self.voiceover(
            "Pause and predict. Q gives a crash twice P's probability. Is the discount factor there "
            "above or below one over one plus r? <bookmark mark='a'/> Above: twice as high. Where Q "
            "is heavier than P, a dollar is dear."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"above: $q/\pi = (1 + r)\,m = 2$, so $m = 2/(1 + r)$; where $Q$ is "
                                                r"heavier than $P$, a dollar is dear")))
        self.wait(0.4)
        self.clear_scene()
