from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load

K = 160.0


class Girsanov(VoiceoverScene):
    def construct(self):
        g = load("girsanov")
        self.card()
        self.theorem()
        self.sampling(g)
        self.representation()

    def card(self):
        c = chapter_card(4, r"Girsanov and martingale representation", r"Is drift just a change of measure?", part=PART)
        with self.voiceover("Chapter four. Girsanov's theorem, and martingale representation."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def theorem(self):
        th = theorem_card(r"Girsanov", r"Let $W$ be a Brownian motion under $P$, and $Z_T = \exp\big(-\int_0^T \theta_t\,dW_t - "
                          r"\tfrac12 \int_0^T \theta_t^2\,dt\big)$. Under $dQ = Z_T\,dP$, the process $\widetilde W_t = W_t + "
                          r"\int_0^t \theta_s\,ds$ is a Brownian motion.", who=r"Cameron and Martin (1944), Girsanov (1960)",
                          color=STRAT, width=9.6, font_size=24).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"a drift can be added or removed by reweighting the paths, without moving any of them", font_size=24,
                  color=GREY_A),
            label(r"the weight is the continuous-time version of Part 4's likelihood ratio on a coin", font_size=24,
                  color=GREY_A),
            label(r"volatility cannot be changed this way: $P$ and $Q$ must agree on the quadratic variation", font_size=24,
                  color=JUMP),
            label(r"so prices can be computed in a world where every asset drifts at the riskless rate (Parts 9, 10)",
                  font_size=24, color=STRAT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(th, DOWN, buff=0.5)
        with self.voiceover(
            "Part four changed the measure on a coin. Here is the same idea for Brownian motion. Reweight every path by "
            "an exponential of the path itself, and Brownian motion acquires a drift; or, read the other way, a "
            "drift disappears. The paths don't move. Only their probabilities change. <bookmark mark='a'/> The weight "
            "is the continuous version of the coin's likelihood ratio. <bookmark mark='b'/> What cannot be changed is "
            "the volatility: two equivalent measures must agree on the quadratic variation, because it can be read "
            "off a single path. <bookmark mark='c'/> That asymmetry is the whole of option pricing. The drift of a "
            "stock, which nobody can estimate well, can be swapped for the riskless rate; the volatility, which can "
            "be measured, stays."
        ) as vo:
            self.play(FadeIn(th, shift=UP * 0.2), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.wait(0.4)
        self.clear_scene()

    def sampling(self, g):
        Sp, Si, w = (np.asarray(g[k]) for k in ("S_plain", "S_is", "w_is"))
        ax_ = axes([40, 260], [0, 1], x_length=6.6, y_length=1.6, xlabel=r"$S_T$", xticks=[60, 100, 160, 220],
                   yticks=[], font_size=16)
        top = ax_.copy()
        bot = axes([40, 260], [0, 1], x_length=6.6, y_length=1.6, xlabel=r"$S_T$", xticks=[60, 100, 160, 220], yticks=[],
                   font_size=16)
        VGroup(top, bot).arrange(DOWN, buff=1.0).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        rng = np.random.default_rng(0)

        def strip(gr, S, colors, sizes):
            ax = gr.ax
            jit = rng.random(len(S)) * 0.8 + 0.1
            return VGroup(*[Dot(ax.c2p(min(s, 259), j), radius=r_, color=c, fill_opacity=0.8)
                            for s, j, c, r_ in zip(S, jit, colors, sizes)])

        cp = [JUMP if s > K else GREY_B for s in Sp]
        dp = strip(top, Sp, cp, [0.035] * len(Sp))
        wn = w / w.max()
        ci = [JUMP if s > K else GREY_B for s in Si]
        di = strip(bot, Si, ci, list(0.02 + 0.05 * np.sqrt(wn)))
        kl = VGroup(*[DashedLine(gr.ax.c2p(K, 0), gr.ax.c2p(K, 1), color=JUMP, stroke_width=2) for gr in (top, bot)])
        t1 = label(r"plain: simulate the real-world paths", font_size=20, color=GREY_A).next_to(top, UP, buff=0.1).align_to(top, LEFT)
        t2 = label(r"Girsanov: push every path up, then weight it by $Z$ (dot size)", font_size=20, color=GREY_A).next_to(
            bot, UP, buff=0.1).align_to(bot, LEFT)
        side = VGroup(
            label(r"a digital paying 1 if $S_T > 160$; $S_0 = 100$, $\sigma = 20\%$", font_size=21, color=GREY_A),
            MathTex(rf"\text{{exact: }} {g['exact']:.5f}", font_size=30),
            MathTex(rf"\text{{plain: }} {g['plain_mean']:.4f} \pm {g['plain_se']:.4f}", font_size=30, color=GREY_A),
            label(rf"{g['hits_plain']} of {g['n']:,} paths finish above 160".replace(",", "{,}"), font_size=20, color=GREY_B),
            MathTex(rf"\text{{reweighted: }} {g['is_mean']:.5f} \pm {g['is_se']:.5f}", font_size=30, color=STRAT),
            label(rf"{g['hits_is']:,} of {g['n']:,} finish above 160".replace(",", "{,}"), font_size=20, color=GREY_B),
            MathTex(rf"\text{{variance }} \div {g['var_ratio']:.0f}", font_size=34, color=DRIFT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Girsanov is also a computational tool. Price a digital option that pays one dollar if the stock, now at a "
            "hundred, ends the year above a hundred and sixty. By plain simulation, almost every path ends below "
            f"the strike: only {g['hits_plain']} of twenty thousand pay, and the estimate is noisy. "
            "<bookmark mark='a'/> Now add a drift that pushes the typical path up to the strike, and correct for it "
            "by weighting each path with Girsanov's likelihood ratio. Half the paths now pay, each with a small "
            f"weight. <bookmark mark='b'/> Both estimates are unbiased, but the variance falls by a factor of "
            f"{g['var_ratio']:.0f}: one reweighted path is worth fifty plain ones. This is importance sampling, and "
            "every risk system that prices rare events uses it."
        ) as vo:
            self.play(FadeIn(top), FadeIn(t1), Create(kl[0]), FadeIn(side[0]), FadeIn(side[1]))
            self.play(LaggedStart(*[FadeIn(d) for d in dp], lag_ratio=0.003, run_time=2))
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("a")
            self.play(FadeIn(bot), FadeIn(t2), Create(kl[1]))
            self.play(LaggedStart(*[FadeIn(d) for d in di], lag_ratio=0.003, run_time=2))
            self.play(FadeIn(side[4]), FadeIn(side[5]))
            vo.wait_until("b")
            self.play(FadeIn(side[6]))
        self.wait(0.4)
        self.clear_scene()

    def representation(self):
        th = theorem_card(r"Martingale representation", r"Every martingale $M$ of the information generated by $W$ is a "
                          r"stochastic integral: $M_t = M_0 + \int_0^t H_s\,dW_s$ for some predictable $H$.",
                          who=r"It\^o (1951); Clark (1970) and Ocone (1984) give $H$", color=ITO, width=9.6,
                          font_size=25).to_edge(UP, buff=0.6)
        rows = [cmath(r"V_t", r"=", r"\mathbb{E}_Q[\text{payoff} \mid \mathcal{F}_t]", r"=", r"V_0 + \int_0^t H_s\,d\widetilde W_s",
                      font_size=36, colors={r"V_t": ITO}),
                cmath(r"H_t", r"=", r"\Delta_t\,\sigma S_t", r"\;\Rightarrow\;", r"\text{hold } \Delta_t \text{ shares}",
                      font_size=36, colors={r"\text{hold } \Delta_t \text{ shares}": DRIFT})]
        VGroup(*rows).arrange(DOWN, buff=0.5).next_to(th, DOWN, buff=0.6)
        notes = VGroup(
            label(r"the discounted price of any claim is a $Q$-martingale; the theorem writes it as trading gains", font_size=23,
                  color=GREY_A),
            label(r"so in a market driven by one Brownian motion, every payoff can be hedged: the market is complete", font_size=23,
                  color=GREY_A),
            label(r"add jumps, or a second source of noise, and the representation fails: Parts 11 and 13", font_size=23, color=JUMP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(VGroup(*rows), DOWN, buff=0.5)
        with self.voiceover(
            "Why does a hedge exist at all? Because of a second theorem. In a world whose only randomness is one "
            "Brownian motion, every martingale is a stochastic integral against it. <bookmark mark='a'/> Apply it to "
            "an option's discounted price, which is a martingale under the pricing measure. It becomes a sum of "
            "trading gains: hold H at each moment and you replicate the option exactly. The integrand is the delta of "
            "Part ten, and Clark and Ocone gave a formula for it in general. <bookmark mark='b'/> This is what "
            "completeness means. And it is fragile: add jumps, or a second source of noise like a random volatility, "
            "and not every payoff can be hedged any more. Parts eleven and thirteen live in that world."
        ) as vo:
            self.play(FadeIn(th, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Write(rows[0]))
            self.play(Write(rows[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(n) for n in notes], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()
