from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.quant import *  # noqa: F403
from videos.quant.quant10.common import CASH, DEL, OPT, PART, PP, QQ, SPOT, load

C_ = {r"\mu": PP, r"r": CASH, r"\mathbb Q": QQ, r"\mathbb P": PP, r"S_T": SPOT, r"S_0": SPOT, r"S": SPOT,
      r"W^{\mathbb Q}_t": QQ, r"W_t": PP, r"V_0": OPT, r"N(d_1)": DEL, r"N(d_2)": QQ}


def row(*parts, fs=36):
    return cmath(*parts, colors=C_, font_size=fs)


class RiskNeutral(VoiceoverScene):
    def construct(self):
        d = load("riskneutral")
        self.card()
        self.feynman_kac()
        self.two_worlds(d)
        self.integral(d)
        self.meaning(d)

    def card(self):
        c = chapter_card(3, r"The price as an expectation", r"Whose probabilities price an option?",
                         lit=(1979, 1981), part=PART)
        with self.voiceover("Chapter three. The price as an expectation."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def feynman_kac(self):
        pde = row(r"\partial_t V + r S\,\partial_S V + \tfrac12\sigma^2 S^2\,\partial_{SS} V - r V = 0", fs=46)
        arrow = MathTex(r"\Big\Updownarrow", font_size=50, color=GREY_B)
        fk = row(r"V_0", r"=", r"e^{-", r"r", r"T}\,", r"\mathbb E^{", r"\mathbb Q", r"}\big[\max(", r"S_T",
                 r"- K,\,0)\big]", fs=54)
        sde = row(r"dS = ", r"r", r"\,S\,dt + \sigma S\,", r"dW^{\mathbb Q}_t", fs=42)
        g = VGroup(pde, arrow, fk, sde).arrange(DOWN, buff=0.4)
        fk_note = why(r"Feynman--Kac (Part 5): a PDE's solution is an expectation over paths")
        fk_note.next_to(arrow, RIGHT, buff=0.4)
        sde_note = why(r"under $\mathbb Q$ the stock drifts at $r$, not $\mu$")
        sde_note.next_to(sde, RIGHT, buff=0.4)
        with self.voiceover(
            "Part five ended with the Feynman-Kac theorem: the solution of an equation like this one can be "
            "written as an average over random paths. <bookmark mark='a'/> Read the Black-Scholes equation that "
            "way, and the option's value today is the discounted average of its payoff, the average taken over "
            "paths of a stock that grows at the riskless rate r. <bookmark mark='b'/> Not at mu. The average is "
            "not over the world's probabilities, which we call P, but over another set of probabilities, Q, under "
            "which every asset is expected to earn exactly the riskless rate. Q is called the risk-neutral "
            "measure, and it is the most important object in derivatives pricing. Harrison and Kreps in 1979, "
            "and Harrison and Pliska in 1981, proved that its existence is the same thing as the absence of "
            "arbitrage. That is Part nine's theorem. Here we watch it work."
        ) as vo:
            self.play(FadeIn(pde))
            vo.wait_until("a")
            self.play(FadeIn(arrow), FadeIn(fk_note), Write(fk))
            vo.wait_until("b")
            self.play(FadeIn(sde), FadeIn(sde_note))
            self.play(Circumscribe(fk[6], color=QQ))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def two_worlds(self, d):
        S0, K, T, r, mu, sig = d["S0"], d["K"], d["T"], d["r"], d["mu"], d["sigma"]
        lo, hi = 40, 260
        g = axes([0, 1], [lo, hi], x_length=6.2, y_length=4.6, xlabel=r"years", ylabel=r"stock price",
                 xticks=[0, 0.5, 1], yticks=[50, 100, 150, 200, 250], font_size=18)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        t = d["t"]
        P = d["paths_P"]
        Z = (np.log(P / S0) - (mu - 0.5 * sig ** 2) * t) / sig  # the same Brownian paths ...
        Q = S0 * np.exp((r - 0.5 * sig ** 2) * t + sig * Z)  # ... with the drift r instead of mu
        fanP = path_fan(ax, t, P, color=PP, opacity=0.35, stroke_width=1.3)
        fanQ = path_fan(ax, t, Q, color=QQ, opacity=0.35, stroke_width=1.3)
        kline = DashedLine(ax.c2p(0, K), ax.c2p(1, K), color=QC.STRIKE, stroke_width=1.5)
        densP = side_density(ax, d["ST_P"], (lo, hi), bins=55, width=1.6, color=PP, opacity=0.6)
        densQ = side_density(ax, d["ST_Q"], (lo, hi), bins=55, width=1.6, color=QQ, opacity=0.6)
        right_x = 4.35
        tab = VGroup(
            label(r"discounted average payoff", font_size=26, color=GREY_A),
            VGroup(MathTex(r"\mathbb P:", font_size=34, color=PP),
                   MathTex(rf"{d['mc_P']:.2f}", font_size=34, color=PP),
                   label(rf"($\mu = {100 * mu:.0f}\%$)", font_size=22, color=PP)).arrange(RIGHT, buff=0.2),
            VGroup(MathTex(r"\mathbb Q:", font_size=34, color=QQ),
                   MathTex(rf"{d['mc_Q']:.2f} \pm {d['se_Q']:.2f}", font_size=34, color=QQ),
                   label(rf"($r = {100 * r:.0f}\%$)", font_size=22, color=QQ)).arrange(RIGHT, buff=0.2),
            VGroup(label(r"Black--Scholes:", font_size=26, color=OPT),
                   MathTex(rf"{d['exact']:.2f}", font_size=34, color=OPT)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([right_x, 1.0, 0])
        gir = VGroup(label(r"Girsanov: reweight each $\mathbb P$-path by", font_size=24, color=GREY_A),
                     MathTex(r"\frac{d\mathbb Q}{d\mathbb P} = e^{-\theta W_T - \frac12\theta^2 T},\quad "
                             r"\theta = \frac{\mu - r}{\sigma}", font_size=30, color=QQ),
                     VGroup(label(r"reweighted $\mathbb P$ average:", font_size=24, color=GREY_A),
                            MathTex(rf"{d['mc_W']:.2f}", font_size=32, color=QQ)).arrange(RIGHT, buff=0.2))
        gir.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(tab, DOWN, buff=0.55).align_to(tab, LEFT)
        for m in (tab, gir):
            if m.width > 4.9:
                m.scale_to_fit_width(4.9)
        VGroup(tab, gir).to_edge(RIGHT, buff=0.35)
        params = note(rf"$S_0 = K = 100$, $T = 1$, $\sigma = {100 * sig:.0f}\%$; "
                      rf"{d['n_mc']:,} simulated outcomes".replace(",", "{,}"), font_size=18).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Here are two worlds built from the same random numbers. In amber, the real world: the stock grows "
            f"at an expected {100 * mu:.0f} percent a year. <bookmark mark='a'/> Average the discounted payoff of "
            f"a one-year at-the-money call over these paths and you get {d['mc_P']:.2f}. That is not the "
            "option's price. <bookmark mark='b'/> In violet, the same paths with the drift replaced by the "
            f"riskless rate, {100 * r:.0f} percent. Their distribution at the end sits lower. Average the "
            f"discounted payoff over these, and you get {d['mc_Q']:.2f}, give or take {d['se_Q']:.2f}: the "
            f"Black-Scholes price, {d['exact']:.2f}. <bookmark mark='c'/> And Girsanov's theorem says the two "
            "worlds are the same paths with different weights. Weight each real-world path by this exponential, "
            "which tilts probability away from the paths that went up fastest, and the real-world average turns "
            f"into the risk-neutral one: {d['mc_W']:.2f}. The theta in it, mu minus r over sigma, is the market "
            "price of risk: the extra return per unit of volatility that investors demand, and that the option's "
            "price does not need to know."
        ) as vo:
            self.play(FadeIn(g), Create(kline))
            self.play(LaggedStart(*[Create(m) for m in fanP], lag_ratio=0.02, run_time=3))
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in densP], lag_ratio=0.01, run_time=1.5))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(ReplacementTransform(fanP, fanQ), ReplacementTransform(densP, densQ), run_time=2.5)
            self.play(FadeIn(tab[2]), FadeIn(params))
            self.play(FadeIn(tab[3]))
            vo.wait_until("c")
            self.play(FadeIn(gir, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def integral(self, d):
        rows = [
            row(r"\mathbb E^{\mathbb Q}[(", r"S_T", r"- K)^+]", r"=",
                r"\mathbb E^{\mathbb Q}\big[", r"S_T", r"\,\mathbf 1\{", r"S_T", r"> K\}\big]", r"-",
                r"K\,", r"\mathbb Q(", r"S_T", r"> K)"),
            row(r"\mathbb Q(", r"S_T", r"> K)", r"=", r"\mathbb Q\big(Z > -d_2\big)", r"=", r"N(d_2)"),
            row(r"\mathbb E^{\mathbb Q}\big[", r"S_T", r"\,\mathbf 1\{", r"S_T", r"> K\}\big]", r"=",
                r"S_0", r"e^{", r"r", r"T}\,", r"\mathbb Q^S(", r"S_T", r"> K)"),
            row(r"\mathbb Q^S(", r"S_T", r"> K)", r"=", r"N(d_1)"),
            row(r"V_0", r"=", r"S_0", r"N(d_1)", r"-", r"K e^{-", r"r", r"T}", r"N(d_2)", fs=46),
        ]
        whys = [why(r"split the payoff where it switches on"),
                why(r"$\ln S_T = \ln S_0 + (r - \tfrac12\sigma^2)T + \sigma\sqrt T Z$"),
                why(r"weight by $S_T/(S_0 e^{rT})$: the stock as numeraire"),
                why(r"under that measure the drift is $r + \tfrac12\sigma^2$"),
                why(r"discount by $e^{-rT}$")]
        defs = note(r"$d_{1,2} = \dfrac{\ln(S_0/K) + (r \pm \tfrac12\sigma^2)T}{\sigma\sqrt T}$",
                    font_size=30, color=GREY_A).to_edge(DOWN, buff=0.45)
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-1.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Now the expectation can be done by hand. Split the payoff at the strike: the average of the final "
            "price over the outcomes that finish in the money, minus the strike times the probability of finishing "
            "in the money. <bookmark mark='a'/> The second piece is a normal probability. Under Q the log of the "
            "final price is normal with mean r minus half sigma squared, times T, so the chance of ending above "
            "the strike is N of d two. <bookmark mark='b'/> The first piece has a trick. Weight each outcome by the "
            "final price relative to its forward: that is another change of measure, the one that uses the stock "
            "itself as the unit of account. <bookmark mark='c'/> Under it the drift is r plus half sigma squared, "
            "and the probability becomes N of d one. <bookmark mark='d'/> Put the pieces together and discount: "
            "the Black-Scholes formula. The same one the equation gives, by a completely different road."
        ) as vo:
            self.play(FadeIn(defs))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            self.play(Create(SurroundingRectangle(rows[4], color=OPT, buff=0.18, corner_radius=0.1)))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def meaning(self, d):
        S0, K, T, r, sig = d["S0"], d["K"], d["T"], d["r"], d["sigma"]
        g = axes([40, 260], [0, 0.019], x_length=8.6, y_length=3.4, xlabel=r"stock price in one year",
                 xticks=[50, 100, 150, 200, 250], font_size=20).shift(DOWN * 0.9)
        ax = g.ax
        xs = np.linspace(40, 260, 400)
        m = np.log(S0) + (r - 0.5 * sig ** 2) * T
        dens = stats.lognorm.pdf(xs, s=sig * np.sqrt(T), scale=np.exp(m))
        line = curve(ax, xs, dens, QQ, stroke_width=4)
        right = xs >= K
        area = Polygon(*[ax.c2p(x, y) for x, y in zip(xs[right], dens[right])], ax.c2p(xs[right][-1], 0),
                       ax.c2p(K, 0), stroke_width=0, fill_color=QQ, fill_opacity=0.35)
        kline = DashedLine(ax.c2p(K, 0), ax.c2p(K, 0.0185), color=QC.STRIKE, stroke_width=1.5)
        klab = MathTex("K", font_size=28, color=QC.STRIKE).next_to(kline, UP, buff=0.08)
        lab2 = VGroup(MathTex(r"N(d_2)", font_size=40, color=QQ), MathTex(rf"= {d['N_d2']:.3f}", font_size=36))
        lab2.arrange(RIGHT, buff=0.15)
        lab2b = label(r"the $\mathbb Q$-probability the call finishes in the money", font_size=24, color=QQ)
        lab1 = VGroup(MathTex(r"N(d_1)", font_size=40, color=DEL), MathTex(rf"= {d['N_d1']:.3f}", font_size=36))
        lab1.arrange(RIGHT, buff=0.15)
        lab1b = label(r"the hedge ratio $\Delta$: shares held per option", font_size=24, color=DEL)
        top = VGroup(VGroup(lab2, lab2b).arrange(DOWN, buff=0.12), VGroup(lab1, lab1b).arrange(DOWN, buff=0.12))
        top.arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.5)
        check = note(rf"simulated: {100 * d['q_itm']:.1f}\% of $\mathbb Q$-outcomes finish above $K$; "
                     rf"{100 * d['p_itm']:.1f}\% of $\mathbb P$-outcomes do", font_size=20).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The two Ns have meanings worth keeping. N of d two is the risk-neutral probability that the call "
            f"finishes in the money: here {d['N_d2']:.3f}, the shaded area, and {100 * d['q_itm']:.1f} percent of "
            f"our simulated risk-neutral outcomes did. In the real world, with its higher drift, "
            f"{100 * d['p_itm']:.1f} percent did: Q's probabilities are not forecasts. <bookmark mark='a'/> N of d "
            f"one is the delta, {d['N_d1']:.3f} shares per option. So the formula reads like a recipe: hold N of "
            "d one shares, borrow K e to the minus r T times N of d two, and the portfolio is the option. "
            "Replication and expectation are one statement seen from two sides."
        ) as vo:
            self.play(FadeIn(g), Create(line), Create(kline), FadeIn(klab))
            self.play(FadeIn(area), FadeIn(top[0]))
            self.play(FadeIn(check))
            vo.wait_until("a")
            self.play(FadeIn(top[1]))
        self.wait(0.4)
        self.clear_scene()
