from __future__ import annotations

import numpy as np

from videos.stats.stats44.common import *  # noqa: F403


class MarkovChains(VoiceoverScene):
    def construct(self):
        self.card()
        self.harris()
        self.drift()
        self.clt()
        self.trace()
        self.board()

    def card(self):
        card = chapter_card(8, r"Markov chains on general spaces", r"When can you trust an MCMC average?", lit=(1953,), part=PART)
        with self.voiceover("Chapter eight. Markov chains on general spaces, and when an MCMC average can be trusted."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def harris(self):
        rows = [
            cmath(r"P(x, A)", r":", r"\text{a transition kernel on a general space; \ } \pi P = \pi", font_size=32),
            cmath(r"\text{small set } C", r":", r"P(x, \cdot) \ge \varepsilon\, \nu(\cdot) \ \ \forall x \in C \ \ \text{(minorization)}", font_size=32),
            cmath(r"\text{Harris}", r":", r"\text{every set with } \pi(A) > 0 \text{ is hit infinitely often}", font_size=30),
            cmath(r"\text{split}", r":", r"\text{from } C, \text{ with probability } \varepsilon, \text{ draw from } \nu: \ \text{a regeneration}", font_size=30),
        ]
        rows[1][-1].set_color(CHAINC)
        whys = [why(r"Part 7's chains, \ uncountable"), why(r"Doeblin's idea"), why(r"Harris recurrence"), why(r"Nummelin's splitting")]
        with self.voiceover(
            "<bookmark mark='a'/> MCMC samplers run on continuous spaces, where a chain need not return to an "
            "individual point. Metropolis rejections can keep it at exactly the same point. Their theory replaces "
            "states by sets. <bookmark mark='b'/> A small set is a region from which the next step always has at "
            "least a fixed chance of being drawn from one fixed law nu: a minorization. <bookmark mark='c'/> A Harris"
            " recurrent chain hits every set of positive stationary probability infinitely often, from any start. "
            "<bookmark mark='d'/> And the minorization lets one split the chain: each visit to the small set, a coin "
            "with probability epsilon decides whether the next step is a fresh draw from nu, a regeneration. after "
            "the initial incomplete tour, successive regeneration tours are independent and identically distributed, "
            "which turns a dependent chain back into Part forty-three's independent sums."
        ) as vo:
            heading=label('Small sets allow regeneration on general state spaces',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def drift(self):
        rows = [
            cmath(r"\text{drift}", r":", r"PV(x) \le \lambda V(x) + b\, 1_C(x), \ \ \lambda < 1, \ V \ge 1", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"\|P^n(x, \cdot) - \pi\|_{TV} \le R\, V(x)\, \rho^n, \ \ \rho < 1: \ \text{geometric ergodicity}", font_size=30),
            cmath(r"\text{Gaussian AR(1)}", r":", r"V = 1 + x^2: \ PV(x) = 1 + \phi^2 x^2 + \sigma^2;\ \phi^2<\lambda<1\ \text{outside a large compact }C", font_size=30),
            cmath(r"\text{but}", r":", r"\text{RWM on a Cauchy target: \ not geometrically ergodic}", font_size=30),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"a Lyapunov function"), why(r"Meyn \& Tweedie (1993)"), why(r"an example"), why(r"Mengersen \& Tweedie (1996)")]
        with self.voiceover(
            "<bookmark mark='a'/> Speed comes from a drift condition. Find a function V, at least one, whose expected"
            " next value shrinks by a factor lambda below one, except on a small set. <bookmark mark='b'/> For a "
            "psi-irreducible aperiodic chain with the stated small-set drift and finite V, Sean Meyn and Richard "
            "Tweedie's theory shows that the chain converges to its stationary law geometrically fast in total "
            "variation, from any start, at a rate depending on V of the start. <bookmark mark='c'/> For the AR one "
            "chain, one plus x squared works for Gaussian noise of positive variance when absolute phi is below one. "
            "Choose lambda strictly between phi squared and one, and a sufficiently large compact small set. "
            "<bookmark mark='d'/> And it can fail: random-walk Metropolis on a target with tails as heavy as the "
            "Cauchy's is not geometrically ergodic, as Kerrie Mengersen and Tweedie showed in 1996; its excursions "
            "into the tails take too long to come back from."
        ) as vo:
            heading=label('Small-set drift plus irreducibility and aperiodicity gives geometric convergence',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def clt(self):
        rows = [
            cmath(r"\text{geometric ergodicity}", r"+", r"\ E_\pi |f|^{2 + \delta} < \infty", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"\sqrt n\,(\bar f_n - \pi f) \Rightarrow N(0, \sigma_f^2)", font_size=34),
            cmath(r"\sigma_f^2", r"=", r"\text{Var}_\pi f \, \big(1 + 2 \textstyle\sum_{k \ge 1} \rho_k\big) = \text{Var}_\pi f \cdot \tau", font_size=32),
            cmath(r"\text{estimate}", r":", r"\text{batch means, \ spectral variance, \ or } \tau \text{ from the autocorrelations}", font_size=30),
        ]
        rows[1][-1].set_color(MARTC)
        whys = [why(r"the conditions"), why(r"the MCMC CLT"), why(r"the autocorrelation time"), why(r"Part 27's tools, \ justified")]
        with self.voiceover(
            "<bookmark mark='a'/> For a geometrically ergodic chain and a function with a little more than two moments under "
            "the target, <bookmark mark='b'/> the MCMC average satisfies a central limit theorem, proved through the "
            "regenerations or through martingale approximation. <bookmark mark='c'/> Its variance is the target variance "
            "times the integrated autocorrelation time, tau: one plus twice the sum of the autocorrelations. <bookmark "
            "mark='d'/> Batch means, spectral estimates and effective sample sizes, all used in Part twenty-seven, are ways "
            "of estimating it. The theorem is what makes them estimates of something."
        ) as vo:
            heading=label('Geometric ergodicity and moments justify the MCMC normal limit',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def trace(self):
        d = load("mcmc")
        tr = np.asarray(d["trace"])
        A = axes([0, 2000], [-4, 4], x_length=5.6, y_length=3.0, xlabel=r"iteration", ylabel=r"$X_t$", xticks=[0, 1000, 2000],
                 yticks=[-3, 0, 3], center=[-3.4, 1.1, 0])
        B = axes([0, 60], [-0.1, 1], x_length=4.2, y_length=3.0, xlabel=r"lag $k$", ylabel=r"$\rho_k$", xticks=[0, 20, 40, 60],
                 yticks=[0, 0.5, 1], center=[3.5, 1.1, 0])
        tl = polyline(A.ax, np.arange(len(tr)), tr, CHAINC, 1.4)
        acf = np.asarray(d["acf"])
        bars = polyline(B.ax, np.arange(len(acf)), acf, MARTC, 2.5)
        side = fit_rows(VGroup(
            label(rf"random-walk Metropolis on $N(0, 1)$, \ step 0.5: \ {100 * d['accept']:.0f}\% accepted", font_size=22),
            label(rf"positive-lag truncation, $k\le60$: $\hat\tau \approx {d['tau']:.0f}$", font_size=22, color=MARTC),
            label(rf"SE of the mean: \ i.i.d.\ formula {d['se_iid']:.4f}; \ batch means {d['se_bm']:.4f}; \ $\sqrt\tau$-corrected {d['se_tau']:.4f}", font_size=22, color=S.ACCENT),
            label(r"the i.i.d.\ formula is too small by $\sqrt\tau \approx 5$", font_size=22, color=BADC),
        ), 12.4, 0.28, [0, -2.2, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A random-walk Metropolis chain for a standard normal, with small steps: {100 * d['accept']:.0f} percent are accepted, and the trace wanders slowly. <bookmark mark='b'/> Its autocorrelations decay over dozens of lags; a positive-lag truncation through lag sixty gives an approximate autocorrelation time of {d['tau']:.0f}. <bookmark mark='c'/> From two hundred thousand iterations, the standard error of the mean by the independent-draws formula is {say(d['se_iid'], 4)}; thirty finite batches give the approximate standard error {say(d['se_bm'], 4)}, and the autocorrelation correction {say(d['se_tau'], 4)}. <bookmark mark='d'/> Ignoring the dependence understates this estimated error about five-fold. These finite-batch and truncated autocorrelation estimates are approximate; consistency of batch means requires both batch length and the number of batches to grow."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(Create(tl), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(bars), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def board(self):
        show_board(self, board_rows("MCMC"),
                   "<bookmark mark='a'/> The Board, over six hundred chains of twenty thousand steps: a ninety percent interval for "
                   "the target mean with the batch-means standard error covers ninety percent: kept. <bookmark mark='b'/> With "
                   "the independent-draws standard error it covers twenty-seven percent: broken. The MCMC central limit theorem "
                   "is the difference.",
                   [("a", [0]), ("b", [1])])
