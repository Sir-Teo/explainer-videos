from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, pause, sci

QCOL = QC.Q


class Sampling(VoiceoverScene):
    def construct(self):
        i = load("is_run")
        o = load("observability")
        self.card()
        self.lab(i)
        self.race(i)
        self.observe(o)
        self.why_prices(o)

    def card(self):
        c = chapter_card(9, r"Girsanov at work, and what it cannot change", r"Which parameters can a path reveal?",
                         part=PART)
        with self.voiceover("Chapter nine. Girsanov at work, and the one thing it cannot change."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def lab(self, i):
        card = lab_card(r"a digital by importance sampling", [
            "def is_digital(S0, K, sigma, T, n, seed=0):",
            "    z = np.random.default_rng(seed).standard_normal(n)",
            "    th = (np.log(K/S0) + 0.5*sigma**2*T) / (sigma*np.sqrt(T))",
            "    zs = z + th                          # the drift moves the paths ...",
            "    w = np.exp(-th*zs + 0.5*th**2)       # ... and dQ/dP moves them back",
            "    ST = S0*np.exp(-0.5*sigma**2*T + sigma*np.sqrt(T)*zs)",
            "    pay = (ST > K) * w",
            "    return pay.mean(), pay.std()/np.sqrt(n), pay",
        ], source="explainer/quant/house/sim.py", width=8.6, font_size=17).to_edge(UP, buff=0.35)
        card.code[3].set_color(QCOL)
        card.code[4].set_color(QCOL)
        outs = ["is_digital(100, 160, 0.2, 1.0, 20000)",
                f"({i['is_mean']:.5f}, {i['is_sd']:.5f})    exact {i['exact']:.5f}",
                f"plain Monte Carlo: {i['plain_mean']:.4f} +/- {i['plain_sd']:.4f}"]
        with self.voiceover(
            "Girsanov is also a computational tool. Price a digital option paying one dollar if a stock now at a "
            "hundred ends the year above a hundred and sixty. Almost no simulated path gets there. "
            "<bookmark mark='a'/> The House's version: shift every Gaussian draw so the typical path ends at the "
            "strike, and multiply each payoff by the likelihood ratio that undoes the shift, Girsanov's Z for one "
            "Gaussian. <bookmark mark='b'/> Run it with twenty thousand draws."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(Indicate(card.code[3:5], color=QCOL, scale_factor=1.02))
            vo.wait_until("b")
            lab_run(self, card, outs, font_size=19)
        self.wait(0.4)
        self.clear_scene()

    def race(self, i):
        idx = np.log10(np.asarray(i["idx"]))
        ex = i["exact"]
        g = axes([idx[0], idx[-1]], [0, 0.02], x_length=8.4, y_length=4.4, xlabel=r"paths simulated (log scale)",
                 ylabel=r"running estimate of the digital", xticks=[2, 3, 4], xfmt=lambda u: rf"10^{{{int(u)}}}",
                 yticks=[0, 0.005, 0.01, 0.015, 0.02], font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        exact = DashedLine(ax.c2p(idx[0], ex), ax.c2p(idx[-1], ex), color=WHITE, stroke_width=2)
        el = MathTex(rf"N(d_2) = {ex:.5f}", font_size=24).next_to(ax.c2p(idx[-1], ex), UP, buff=0.1).align_to(
            ax.c2p(idx[-1], ex), RIGHT)
        pm, ps = np.asarray(i["plain"]), np.asarray(i["plain_se"])
        im, is_ = np.asarray(i["is"]), np.asarray(i["is_se"])
        tk = ValueTracker(0)
        clip = lambda y: np.clip(y, 0, 0.02)  # noqa: E731

        def upto(arr_lo, arr_hi, col):
            def make():
                n = int(np.clip(tk.get_value(), 1, len(idx) - 1)) + 1
                return band(ax, idx[:n], clip(arr_lo[:n]), clip(arr_hi[:n]), col, 0.25)
            return always_redraw(make)
        b1 = upto(pm - 2 * ps, pm + 2 * ps, GREY_B)
        b2 = upto(im - 2 * is_, im + 2 * is_, QCOL)
        l1 = tracing(ax, idx, clip(pm), tk, GREY_A, stroke_width=3)
        l2 = tracing(ax, idx, clip(im), tk, QCOL, stroke_width=3)
        leg = legend([(GREY_A, r"plain Monte Carlo, $\pm 2$ s.e."), (QCOL, r"re-weighted by $Z$, $\pm 2$ s.e.")],
                     font_size=21).to_corner(UR, buff=0.4)
        vr = MathTex(rf"\text{{variance}} \div {i['var_ratio']:.0f}", font_size=40, color=DRIFT).next_to(leg, DOWN,
                                                                                                     buff=0.5)
        with self.voiceover(
            "Watch the two estimates race, path by path, each with a band of two standard errors. "
            "<bookmark mark='a'/> The plain estimate sits at zero for the first few hundred paths, then jumps every "
            "time a rare path pays, and its band stays wide. The re-weighted one locks onto the exact price almost at "
            "once: half its paths now pay, each with a small weight. <bookmark mark='b'/> Both are unbiased, but the "
            f"variance is {i['var_ratio']:.0f} times smaller: one re-weighted path is worth about {i['var_ratio']:.0f} "
            "plain ones. The shift was chosen by eye, to put the typical path at the strike; how to choose it "
            "optimally, and when re-weighting backfires, is Part sixteen's subject. Every risk system that prices "
            "rare events uses some version of this."
        ) as vo:
            self.add(b1, b2, l1, l2)
            self.play(FadeIn(g), Create(exact), FadeIn(el), FadeIn(leg))
            vo.wait_until("a")
            self.play(tk.animate.set_value(len(idx) - 1), run_time=7, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(vr, scale=1.2))
        for m in (b1, b2, l1, l2):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def observe(self, o):
        t = np.asarray(o["run_t"])
        g1 = axes([0, 1], [0.15, 0.25], x_length=5.6, y_length=2.6, ylabel=r"$\hat\sigma$ from quadratic variation",
                  xticks=[0, 1], yticks=[0.15, 0.2, 0.25], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15)
        g2 = axes([0, 1], [-1.0, 1.2], x_length=5.6, y_length=2.6, xlabel=r"years observed",
                  ylabel=r"$\hat\mu$ from the endpoint", xticks=[0, 1], yticks=[-1, 0, 1],
                  yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15)
        VGroup(g1, g2).arrange(DOWN, buff=0.45).to_edge(LEFT, buff=0.5)
        tk = ValueTracker(0)
        ls = tracing(g1.ax, t, np.clip(o["run_s"], 0.15, 0.25), tk, ITO, stroke_width=3)
        lm = tracing(g2.ax, t, np.clip(o["run_m"], -1.0, 1.2), tk, JUMP, stroke_width=3)
        tr1 = DashedLine(g1.ax.c2p(0, o["sigma"]), g1.ax.c2p(1, o["sigma"]), color=WHITE, stroke_width=1.5)
        tr2 = DashedLine(g2.ax.c2p(0, o["mu"]), g2.ax.c2p(1, o["mu"]), color=WHITE, stroke_width=1.5)
        rows = [cmath(r"\hat\sigma^2", r"=", r"\frac1T \sum (\Delta \log S)^2, \quad \operatorname{sd}(\hat\sigma) \approx "
                      r"\frac{\sigma}{\sqrt{2n}}", font_size=28, colors={r"\frac{\sigma}{\sqrt{2n}}": ITO}),
                cmath(r"\hat\mu", r"=", r"\frac{\log(S_T/S_0)}{T} + \tfrac12\sigma^2, \quad \operatorname{sd}(\hat\mu) = "
                      r"\frac{\sigma}{\sqrt T}", font_size=28, colors={r"\frac{\sigma}{\sqrt T}": JUMP})]
        side = VGroup(rows[0], label(rf"over 200 simulated years: sd ${sci(o['sd_sigma'], 1)}$ against "
                                     rf"${sci(o['sd_sigma_theory'], 1)}$", font_size=19, color=ITO),
                      rows[1], label(rf"over 200 simulated years: sd {o['sd_mu']:.3f} against {o['sd_mu_theory']:.2f}",
                                     font_size=19, color=JUMP)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        side.to_edge(RIGHT, buff=0.3).shift(UP * 0.4)
        pc, ans = pause(r"Sample every second instead of every minute. Which estimate improves?",
                        r"Only $\hat\sigma$, by $\sqrt{60}$; $\hat\mu$ depends on $T$ alone.", width=5.6, font_size=20)
        pc.next_to(side, DOWN, buff=0.3).align_to(side, LEFT)
        ans.next_to(pc, DOWN, buff=0.1).align_to(pc, LEFT)
        with self.voiceover(
            "Now the limit of the theorem: it changes drift, never volatility. Simulate a year of one-minute prices, "
            "twenty percent volatility and eight percent drift, and estimate both as the year unrolls. "
            "<bookmark mark='a'/> The volatility estimate, from squared returns, settles within days. The drift "
            "estimate wanders across tens of points all year. <bookmark mark='b'/> The volatility estimate's error "
            "shrinks with the number of observations, half a million of them. The drift estimate depends only on the "
            "first and last prices, so its error shrinks only with the length of history. Two hundred simulated "
            f"years: {o['sd_mu']:.2f} for the drift, against {o['sd_sigma'] * 1e4:.0f} hundredths of a point for the "
            "volatility. <bookmark mark='c'/> A pause: sample every second instead of every minute; which estimate "
            "improves? <bookmark mark='d'/> Only the volatility."
        ) as vo:
            self.add(ls, lm)
            self.play(FadeIn(g1), FadeIn(g2), Create(tr1), Create(tr2))
            vo.wait_until("a")
            self.play(tk.animate.set_value(len(t) - 1), run_time=6, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(pc))
            vo.wait_until("d")
            self.play(FadeIn(ans))
        for m in (ls, lm):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def why_prices(self, o):
        rows = VGroup(
            label(r"two models, $\sigma = 20\%$ and $\sigma = 21\%$:", font_size=26, color=GREY_A),
            MathTex(r"P_{20}\big(\langle \log S\rangle_T = 0.04\,T\big) = 1, \qquad P_{21}\big(\langle \log S\rangle_T = "
                    r"0.04\,T\big) = 0", font_size=32, color=ITO),
            label(r"they disagree with certainty about an observable event: the measures are singular, and no $Z$ "
                  r"turns one into the other", font_size=24, color=GREY_A),
            label(r"two models with different drifts agree on every such event: they are equivalent, and $Z$ converts "
                  r"one into the other", font_size=24, color=GREY_A),
            MathTex(r"\Rightarrow\ \text{prices may depend on } \sigma,\ \text{never on } \mu", font_size=36,
                    color=QCOL),
            label(r"the risk-neutral measure of Parts 9 and 10 changes $\mu$ to $r$ and keeps $\sigma$", font_size=22,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "This asymmetry is the root of option pricing. Take two models that differ only in volatility, twenty and "
            "twenty-one percent. The quadratic variation of the log price is a property of one path: one model says "
            "it is four hundredths per year with certainty, the other says that is impossible. <bookmark mark='a'/> "
            "The measures are singular: no likelihood ratio connects them. Two models that differ only in drift are "
            "equivalent, and Girsanov's Z converts one into the other. <bookmark mark='b'/> So a price, which must "
            "not depend on whose drift you believe, can depend on volatility and cannot depend on mu. The "
            "risk-neutral measure of Parts nine and ten swaps the drift for the riskless rate and keeps sigma."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("b")
            self.play(FadeIn(rows[4], scale=1.1), FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()
