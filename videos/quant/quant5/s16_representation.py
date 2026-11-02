from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, pause


class Representation(VoiceoverScene):
    def construct(self):
        h = load("hedge_rates")
        self.card()
        self.live(h)
        self.proof()
        self.rates(h)

    def card(self):
        c = chapter_card(10, r"Martingale representation: why a hedge exists", r"Is every payoff a trading strategy?",
                         part=PART)
        with self.voiceover("Chapter ten. Martingale representation, and Clark-Ocone: why a hedge exists, and when "
                            "it does not."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def live(self, h):
        t = np.asarray(h["t"])
        W, M = np.asarray(h["W"]), np.asarray(h["M"])
        g1 = axes([0, 1], [W.min() - 0.1, W.max() + 0.1], x_length=7.6, y_length=2.0, ylabel=r"$W_t$", xticks=[],
                  yticks=[0], font_size=15)
        lo = min(M.min(), min(min(v["V"]) for v in h["hedges"].values())) - 0.1
        hi = max(M.max(), max(max(v["V"]) for v in h["hedges"].values())) + 0.1
        g2 = axes([0, 1], [lo, hi], x_length=7.6, y_length=3.6, xlabel=r"time",
                  ylabel=r"$M_t = \mathbb{E}[W_1^2 \mid \mathcal{F}_t] = W_t^2 + 1 - t$ and the hedge",
                  xticks=[0, 0.5, 1], yticks=[1], font_size=15)
        VGroup(g1, g2).arrange(DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        tk = ValueTracker(0)
        lw = tracing(g1.ax, t, W, tk, BM, stroke_width=2)
        lm = tracing(g2.ax, t, M, tk, ITO, stroke_width=3)

        def hedge(n, col):
            d = h["hedges"][str(n)]
            tt, V = np.asarray(d["t"]), np.asarray(d["V"])
            pts = [g2.ax.c2p(tt[0], V[0])]
            for k in range(1, len(tt)):
                pts += [g2.ax.c2p(tt[k], V[k - 1]), g2.ax.c2p(tt[k], V[k])] if n <= 16 else [g2.ax.c2p(tt[k], V[k])]
            return VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(pts), V[-1]
        h8, v8 = hedge(8, DRIFT)
        h512, v512 = hedge(512, DRIFT)
        gap8 = Line(g2.ax.c2p(1, M[-1]), g2.ax.c2p(1, v8), color=JUMP, stroke_width=6)
        gap512 = Line(g2.ax.c2p(1, M[-1]), g2.ax.c2p(1, v512), color=JUMP, stroke_width=6)
        side = VGroup(
            MathTex(r"F = W_1^2", font_size=32),
            MathTex(r"V_t = \mathbb{E}F + \sum_k H_{t_k}\,\Delta W_k,\quad H_t = 2W_t", font_size=28, color=DRIFT),
            MathTex(rf"n = 8:\ |V_1 - F| = {abs(v8 - M[-1]):.3f}", font_size=28, color=JUMP),
            MathTex(rf"n = 512:\ |V_1 - F| = {abs(v512 - M[-1]):.3f}", font_size=28, color=JUMP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Why does a hedge exist at all? Take a payoff that depends on a Brownian path: W at time one, squared. "
            "Its expectation given the path so far is a martingale, W squared plus the time remaining. "
            "<bookmark mark='a'/> Watch the path and the martingale unroll together. <bookmark mark='b'/> A trader "
            "starts with the payoff's expected value, one, and holds two W units of the Brownian asset, rebalancing "
            "eight times. The green staircase is the trader's wealth: near the martingale, but it misses at the end "
            "by the red gap. <bookmark mark='c'/> Rebalance five hundred and twelve times, and the wealth lies on top "
            "of the martingale. The payoff is a trading strategy. Every Brownian payoff is, and the proof says why."
        ) as vo:
            self.add(lw, lm)
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(tk.animate.set_value(len(t) - 1), run_time=5, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(h8), FadeIn(side[1]), run_time=2)
            self.play(Create(gap8), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(ReplacementTransform(h8, h512), ReplacementTransform(gap8, gap512), FadeIn(side[3]), run_time=2)
        for m in (lw, lm):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        rows = [cmath(r"\mathcal{E}^h_T", r"=", r"e^{\int_0^T h\,dW - \frac12\int_0^T h^2\,dt} = 1 + \int_0^T h_t\,\mathcal{E}^h_t\,dW_t",
                      font_size=32),
                cmath(r"Y \perp \mathcal{E}^h_T \ \forall h", r"\Rightarrow", r"\mathbb{E}\big[Y e^{\sum_i \lambda_i W_{t_i}}\big] = 0 "
                      r"\ \forall \lambda \Rightarrow Y = 0", font_size=32),
                cmath(r"F", r"=", r"\mathbb{E}F + \int_0^T H_t\,dW_t, \qquad M_t = M_0 + \int_0^t H\,dW", font_size=32,
                      colors={r"\int_0^T H_t\,dW_t": DRIFT}),
                cmath(r"H_t", r"=", r"\mathbb{E}\big[D_t F \mid \mathcal{F}_t\big]", font_size=36,
                      colors={r"\mathbb{E}\big[D_t F \mid \mathcal{F}_t\big]": ITO}),
                cmath(r"F = W_T^3:\ \ H_t", r"=", r"3\big(W_t^2 + T - t\big)", font_size=32)]
        whys = [why(r"exponentials are integrals: the stochastic exponential solves $d\mathcal{E} = h\mathcal{E}\,dW$"),
                why(r"they are total in $L^2(\mathcal{F}^W_T)$: orthogonal to all of them means zero (Fourier uniqueness)"),
                why(r"limits of integrals are integrals, by the isometry: every square-integrable $F$ (It\^o 1951)"),
                why(r"Clark (1970), Ocone (1984): $D_t F$, the Malliavin derivative, is $F$'s sensitivity to a bump in "
                    r"$dW$ at $t$"),
                why(r"$D_t W_T^3 = 3W_T^2$, and $\mathbb{E}[W_T^2 \mid \mathcal{F}_t] = W_t^2 + T - t$")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-1.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "The proof idea is short. First, exponentials are integrals: by the lemma, a stochastic exponential is "
            "one plus a stochastic integral. <bookmark mark='a'/> Second, they are rich enough: a variable orthogonal "
            "to all of them has zero Fourier transform at every finite set of times, so it is zero. "
            "<bookmark mark='b'/> Third, the isometry: limits of integrals are integrals. So every square-integrable "
            "payoff is its mean plus a stochastic integral, and every Brownian martingale a running integral: the "
            "martingale representation theorem. <bookmark mark='c'/> It says a hedge exists, not what it is. Clark "
            "and Ocone gave the formula: the expected Malliavin derivative, the payoff's sensitivity to a bump in the "
            "path at time t. For a call it is the delta of Part ten. <bookmark mark='d'/> For W cubed it is three "
            "times W squared plus the time remaining."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.5)
        self.clear_scene()

    def rates(self, h):
        ns = np.asarray(h["ns"])
        x = np.log2(ns)
        sd = {k: np.log10(np.asarray(v)) for k, v in h["sd"].items()}
        lo = min(v.min() for v in sd.values()) - 0.2
        hi = max(v.max() for v in sd.values()) + 0.2
        g = axes([x[0] - 0.3, x[-1] + 0.3], [lo, hi], x_length=7.0, y_length=4.6, xlabel=r"rebalances $n$ (log scale)",
                 ylabel=r"spread of the hedge error (log scale)", xticks=list(x), xfmt=lambda u: f"{2 ** int(u):,}".replace(",", "{,}"),
                 yticks=[-1, 0], yfmt=lambda u: rf"10^{{{int(u)}}}" if u else "1", font_size=16).to_edge(LEFT, buff=0.6)
        g.shift(DOWN * 0.3)
        ax = g.ax
        cols = {"w2": ITO, "call": DRIFT, "two": JUMP}
        bands = {k: seed_band(ax, x, sd[k], cols[k]) for k in sd}
        theory = DashedVMobject(curve(ax, x, np.log10(h["theory_w2"]), WHITE, stroke_width=2), num_dashes=20)
        leg = legend([(ITO, rf"$W_1^2$, hedged with $2W$: slope {h['slope']['w2']:.2f}"),
                      (DRIFT, rf"a Black--Scholes call, delta-hedged: slope {h['slope']['call']:.2f}"),
                      (JUMP, rf"$X_1^2$, $X = 0.8W + 0.6B$, hedged in $W$ alone: slope {h['slope']['two']:.2f}"),
                      (WHITE, r"$\sqrt{2/n}$: chapter 2's QV error")], font_size=19).to_corner(UR, buff=0.35)
        rows = [cmath(r"F - V_T", r"=", r"\sum_k (\Delta W_k)^2 - T", font_size=30)]
        why0 = why(r"for $F = W_T^2$ the discrete hedge's error is exactly the quadratic-variation error", 19)
        VGroup(rows[0], why0).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(leg, DOWN, buff=0.35).align_to(leg, LEFT)
        pc, ans = pause(r"Hedge $W_T^2$ with four times as many trades. The error's spread?", r"It halves: "
                        r"$\sqrt{2/n}$.", width=5.4, font_size=21)
        VGroup(pc, ans).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DR, buff=0.35)
        flat = h["slope"]["two"] > -0.15
        verdict = (f"stays flat, slope {h['slope']['two']:.2f}: no amount of trading in W hedges the noise in B."
                   if flat else f"falls, slope {h['slope']['two']:.2f}, more than expected.")
        with self.voiceover(
            "How fast does a discrete hedge converge? Five seeds of four thousand paths each, rebalanced from eight to "
            "two thousand times. <bookmark mark='a'/> For W squared, the hedge error is exactly the quadratic-variation "
            "error of chapter two, and its spread follows the square root of two over n: slope minus a half. "
            "<bookmark mark='b'/> A Black-Scholes call hedged with its delta converges at the same rate, minus a half, "
            "as Part eleven will explain. <bookmark mark='c'/> Now break the theorem's assumption. Let the payoff "
            "depend on a second, independent Brownian motion B, and hedge with W alone. The error "
            + verdict + " The market is incomplete, and Parts eleven and thirteen live there. "
            "<bookmark mark='d'/> A pause: four times as many trades. The spread halves."
        ) as vo:
            self.play(FadeIn(g), Create(theory), FadeIn(leg[3]))
            vo.wait_until("a")
            self.play(FadeIn(bands["w2"]), FadeIn(leg[0]), FadeIn(rows[0]), FadeIn(why0))
            vo.wait_until("b")
            self.play(FadeIn(bands["call"]), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(FadeIn(bands["two"]), FadeIn(leg[2]))
            vo.wait_until("d")
            self.play(FadeIn(pc), FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
