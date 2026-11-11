from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, load, real_data, simulated


class Gyongy(VoiceoverScene):
    def construct(self):
        g = load("gyongy")
        m = load("lv_mc")
        self.card()
        self.derive()
        self.cloud(g)
        self.reprice(m)

    def card(self):
        c = chapter_card(7, 'Gy\\"ongy: a diffusion local twin', r"Why does Dupire's formula work at all?",
                         part=PART)
        with self.voiceover("""Chapter seven. A diffusion's local-volatility twin, under the mimicking theorem's conditions."""):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"dS_t = \sigma_t S_t\,dW_t", r"\Rightarrow", r"\partial_T C = \tfrac12 K^2\,\mathbb{E}\big[\sigma_T^2\,"
                      r"\delta(S_T - K)\big]", font_size=36, colors={r"dS_t = \sigma_t S_t\,dW_t": SPOT}),
                cmath(r"\partial_T C", r"=", r"\tfrac12 K^2\,p(K, T)\;\mathbb{E}\big[\sigma_T^2 \mid S_T = K\big]", font_size=36,
                      colors={r"\partial_T C": OPT}),
                cmath(r"\sigma^2_{\text{loc}}(K, T)", r"=", r"\mathbb{E}^Q\big[\sigma_T^2 \mid S_T = K\big]", font_size=40,
                      colors={r"\sigma^2_{\text{loc}}(K, T)": LV}),
                cmath(r"\text{same } p(\cdot, T)\ \forall T", r"\not\Rightarrow", r"\text{same joint law of } (S_{T_1}, S_{T_2})",
                      font_size=34, colors={r"\text{same } p(\cdot, T)\ \forall T": BAD})]
        whys = [why('a continuous stochastic-volatility diffusion with suitable integrability; Tanaka--Meyer gives the local-time term'),
                why(r"condition on where the price ends: the spike picks out $S_T = K$"),
                why(r"compare with Chapter 6: Dupire's function is the expected variance given the price (Gy\"ongy 1986)"),
                why(r"the twin matches every expiry's distribution one at a time, not how they are joined: "
                    r"Chapter 8's warning")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.65, edge=6.9)
        with self.voiceover(
            """Why can one function of price and time reproduce a stochastic-volatility diffusion's marginal laws? Work under a fixed risk-neutral measure with a continuous Ito price, zero carry, and suitable integrability and existence conditions. Tanaka's formula gives the call's maturity slope. <bookmark mark='a'/> Conditioning at the strike gives density times conditional instantaneous variance. <bookmark mark='b'/> Comparison with Dupire yields local variance as that conditional expectation. Gyongy's mimicking theorem and its extensions justify a corresponding Markov diffusion under appropriate regularity. It is not a theorem for arbitrary jumps or every possible model. <bookmark mark='c'/> It matches each single-date law, not the joint law across dates."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def cloud(self, g):
        fx, fv = np.asarray(g["fan_x"]), np.asarray(g["fan_v"])
        cx, cv = np.asarray(g["cloud_x"]), np.asarray(g["cloud_v"])
        ks, dup, cond = np.asarray(g["k"]), np.asarray(g["dupire"]), np.asarray(g["cond"])
        T = g["T"]
        tt = np.linspace(0, T, fx.shape[1])
        gL = axes([0, T], [-0.8, 0.8], x_length=4.2, y_length=4.2, xlabel=r"years", ylabel=r"$\ln S_t$",
                  xticks=[0, T], yticks=[-0.5, 0, 0.5], font_size=15).to_edge(LEFT, buff=0.4).shift(DOWN * 0.3)
        gR = axes([-1.2, 0.8], [0, 1.4], x_length=6.4, y_length=4.2, xlabel=r"$\ln S_T$",
                  ylabel=r"volatility: $\sqrt{v_T}$, or local", xticks=[-0.5, 0, 0.5], yticks=[0, 0.5, 1.0],
                  yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15).next_to(gL, RIGHT, buff=0.7)
        paths = VGroup(*[curve(gL.ax, tt, np.clip(x, -0.8, 0.8), interpolate_color(ManimColor(QC.SPOT), ManimColor(BAD),
                                                                                     float(np.clip(np.sqrt(v[-1]), 0, 1))),
                               stroke_width=1.2) for x, v in zip(fx, fv)])
        m = np.isfinite(cx) & np.isfinite(cv) & (cv >= 0)
        dots = VGroup(*[Dot(gR.ax.c2p(a, float(min(np.sqrt(b), 1.4))), radius=0.02, color=GREY_B, fill_opacity=0.6)
                        for a, b in zip(cx[m], cv[m])])
        tr = ValueTracker(-0.55)
        slab = always_redraw(lambda: Rectangle(width=gR.ax.c2p(0.05, 0)[0] - gR.ax.c2p(0, 0)[0],
                                               height=gR.ax.c2p(0, 1.4)[1] - gR.ax.c2p(0, 0)[1], stroke_width=0,
                                               fill_color=QC.HOUSE, fill_opacity=0.18).move_to(gR.ax.c2p(tr.get_value(), 0.7)))
        ok = np.isfinite(cond)
        gold = VGroup(*[Dot(gR.ax.c2p(a, b), radius=0.07, color=QC.HOUSE) for a, b in zip(ks[ok], cond[ok])])
        dl = curve(gR.ax, ks, np.clip(dup, 0, 1.4), QC.Q, stroke_width=4)  # a model (Q) curve, apart from the gold dots
        p = g["params"]
        head = MathTex(rf"\text{{Heston: }} v_0 = {p['v0']},\ \kappa = {p['kappa']},\ \theta = {p['theta']},\ \xi = {p['xi']},"
                       rf"\ \rho = {p['rho']}", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        leg = legend([(QC.HOUSE, r"$\sqrt{\mathbb{E}[v_T \mid \ln S_T]}$, from 100{,}000 paths"),
                      (QC.Q, r"Dupire, from Heston's own option prices (COS)")], font_size=17).next_to(gR, UP, buff=0.1
                                                                                                  ).align_to(gR, LEFT)
        src = simulated('Heston QE: 100{,}000 paths computed; 20 fans and 1{,}500 terminal points shown')
        gap = g["max_gap"]
        with self.voiceover(
            "Check it by simulation. Take a stochastic volatility model, Heston's, with Bitcoin-like parameters, and "
            "run a hundred thousand paths for three months. Each path is coloured by its final volatility. "
            "<bookmark mark='a'/> At the end, every path is a point: where the price finished, and how volatile it was "
            "at that moment. A cloud, with no function in sight. <bookmark mark='b'/> Now slide a thin slab across it, "
            "and at each price average the variance of the paths inside: the gold dots. <bookmark mark='c'/> Then, "
            "separately, price options in the Heston model with Fourier methods, and push those prices through "
            f"Dupire's formula: the purple line. The dots land on the line, within {gap:.1f} volatility points across "
            "the strikes. The expected variance given the price is Dupire's local variance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(gL), FadeIn(src))
            self.play(LaggedStart(*[Create(x) for x in paths], lag_ratio=0.05, run_time=4))
            vo.wait_until("a")
            self.play(FadeIn(gR), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.002, run_time=2.5))
            vo.wait_until("b")
            self.add(slab)
            seq = list(np.where(ok)[0])
            for i in seq:
                self.play(tr.animate.set_value(float(ks[i])), FadeIn(gold[seq.index(i)]), run_time=0.35)
            slab.clear_updaters()
            self.play(FadeOut(slab))
            vo.wait_until("c")
            self.play(Create(dl), FadeIn(leg), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def reprice(self, m):
        conv = m["conv"]
        ks = np.asarray(m["ks"])
        ref = np.asarray(m["conv_ssvi"])
        g = axes([-0.3, 0.3], [0.35, 0.65], x_length=6.4, y_length=4.0, xlabel=r"log-moneyness (51 days)",
                 ylabel=r"implied volatility", xticks=[-0.2, 0, 0.2], yticks=[0.4, 0.5, 0.6],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        target = curve(g.ax, ks, np.clip(ref, 0.35, 0.65), IV, stroke_width=4)
        keys = sorted(conv, key=int)
        cur = curve(g.ax, ks, np.clip(np.asarray(conv[keys[0]]), 0.35, 0.65), LV, stroke_width=3)
        cnt = MathTex(rf"\text{{paths: }} {int(keys[0]):,}".replace(",", "{,}"), font_size=30, color=LV).next_to(g, UP, buff=0.1)
        leg = legend([(IV, r"the Surface (SSVI)"), (LV, r"local-vol Monte Carlo")], font_size=17).next_to(cnt, RIGHT, buff=0.5)
        rep = m["rep"]
        lines = VGroup(*[label(rf"{r['days']} days: {r['rmse_ssvi']:.2f} vol pts from SSVI, {r['rmse_quote']:.2f} from "
                               rf"the quotes", font_size=19, color=GREY_A) for r in rep]).arrange(DOWN, aligned_edge=LEFT,
                                                                                                   buff=0.15)
        lines.to_edge(RIGHT, buff=0.4).shift(UP * 0.4)
        foot = wrapped_label(r"the short end misses most: a daily simulation of a local vol that is steepest in the first "
                             r"days, and Monte Carlo noise in the wings", 4.8, 18, GREY_B).next_to(lines, DOWN, buff=0.35)
        src = real_data(r"40{,}000 paths under the Surface's Dupire local vol, 4 steps a day")
        r0, r1 = rep[0], rep[-1]
        with self.voiceover(
            f"""Now simulate the fitted Surface's local volatility. This is a finite numerical repricing check, with time discretization and Monte Carlo error. Here is the fifty-one-day smile. <bookmark mark='a'/> Five hundred, two thousand, eight thousand, then forty thousand paths progressively stabilize its estimate. <bookmark mark='b'/> The sampled-strike RMSE against the fitted smile is {r1['rmse_ssvi']:.2f} volatility points at {r1['days']} days and {r0['rmse_ssvi']:.2f} at {r0['days']} days. Those are average errors, not uniform bounds or proof of exact repricing at every strike. The short end is harder with quarter-day simulation steps. Matching today's marginal prices still does not determine tomorrow's joint dynamics."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(target), FadeIn(leg), FadeIn(cnt), Create(cur))
            vo.wait_until("a")
            for k_ in keys[1:]:
                new = curve(g.ax, ks, np.clip(np.asarray(conv[k_]), 0.35, 0.65), LV, stroke_width=3)
                newc = MathTex(rf"\text{{paths: }} {int(k_):,}".replace(",", "{,}"), font_size=30, color=LV).move_to(cnt)
                self.play(Transform(cur, new), Transform(cnt, newc), run_time=1.2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in lines], lag_ratio=0.3, run_time=2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
