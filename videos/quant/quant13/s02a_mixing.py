from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, load, pause, simulated


def _gauss(x, m, v):
    return np.exp(-0.5 * (x - m) ** 2 / v) / np.sqrt(2 * np.pi * v)


class Mixing(VoiceoverScene):
    def construct(self):
        m = load("mixing")
        self.card()
        self.crowd(m)
        self.derive()
        self.check(m)

    def card(self):
        c = chapter_card(2, r"Random volatility makes a smile", r"Why does a moving volatility curve the smile?",
                         lit=(1987,), part=PART)
        with self.voiceover("Chapter two. Random volatility makes a smile."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def _panels(self, m, key):
        cr = m["crowd"][key]
        xs = np.linspace(-1.0, 0.8, 181)
        top = axes([-1.0, 0.8], [0, 3.2], x_length=6.6, y_length=2.6, xlabel=r"$\ln S_T / S_0$, three months",
                   ylabel=r"density", xticks=[-0.8, -0.4, 0, 0.4], yticks=[0, 1, 2, 3], font_size=15)
        mean, var = np.asarray(cr["mean"]), np.asarray(cr["var"])
        thin = VGroup(*[curve(top.ax, xs, np.clip(_gauss(xs, a, b), 0, 3.2), VAR, stroke_width=1.2).set_stroke(opacity=0.35)
                        for a, b in zip(mean, var)])
        env = curve(top.ax, xs, np.clip(np.mean([_gauss(xs, a, b) for a, b in zip(mean, var)], axis=0), 0, 3.2), IV,
                    stroke_width=4)
        kk = np.asarray(m["kk"])
        bot = axes([-0.6, 0.6], [0.35, 0.75], x_length=6.6, y_length=2.2, xlabel=r"log-moneyness $k$",
                   ylabel=r"implied volatility", xticks=[-0.5, 0, 0.5], yticks=[0.4, 0.5, 0.6, 0.7],
                   yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15)
        sm = curve(bot.ax, kk, np.clip(np.asarray(cr["iv"]), 0.35, 0.75), OPT, stroke_width=4)
        top_g = VGroup(top, thin, env)
        bot_g = VGroup(bot, sm)
        VGroup(top_g, bot_g).arrange(DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
        return VGroup(top_g, bot_g)

    def crowd(self, m):
        keys = ["0_0", "0.5_0", "1_0", "2_0", "1_fit"]
        P = [self._panels(m, k) for k in keys]
        dial = VGroup(label(r"vol of vol, times the fitted $\xi$", font_size=22, color=GREY_A),
                      *[MathTex(t, font_size=34, color=c) for t, c in
                        ((r"0\ \ (\text{Black--Scholes})", GREY_B), (r"\tfrac12", VAR), (r"1", VAR), (r"2", VAR),
                         (r"1,\ \ \rho = %.2f" % m["params"][4], BAD))]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        dial.to_edge(RIGHT, buff=0.7).shift(UP * 1.2)
        arrow = Arrow(LEFT * 0.6, ORIGIN, color=WHITE, stroke_width=4, max_tip_length_to_length_ratio=0.35)
        arrow.next_to(dial[1], LEFT, buff=0.15)
        note_ = wrapped_label(r"thin curves: $\ln S_T$ given one simulated variance path, each a Gaussian; gold: their "
                              r"average, the model's density; below, the smile it prices", 4.6, 19, GREY_A)
        note_.next_to(dial, DOWN, buff=0.5).align_to(dial, LEFT)
        atm, wing = m["atm"], m["wing"]
        pp = pause(r"Double the vol of vol, with $\rho = 0$. Which moves more: the at-the-money vol or the wings?",
                   width=4.8).to_corner(DR, buff=0.3)
        src = simulated(r"the fitted Heston, three months; 40 variance paths per setting", corner=DL)
        cur = P[0]
        with self.voiceover(
            (
            "Why does moving volatility make a smile? Take the fitted Heston and switch off the correlation. With no "
            "vol of vol, the log price in three months is one Gaussian, and the smile is flat. <bookmark mark='a'/> "
            "Let the variance move. Each thin curve is the law of the log price given one variance path: Gaussian "
            "again, with that path's variance. The model's density is the crowd's average, in gold. "
            "<bookmark mark='b'/> Turn the vol of vol up: calm paths narrow, wild ones wide, and the average gets a "
            "sharp peak and fat tails. The smile lifts at both ends. <bookmark mark='p'/> Double it again: which "
            "moves more, the at-the-money vol or the wings? <bookmark mark='c'/> The wings rise, from "
            f"{100 * wing['1']:.0f} to {100 * wing['2']:.0f} percent; at the money it falls, from {100 * atm['1']:.1f} "
            f"to {100 * atm['2']:.1f}. Symmetric, as it must be. <bookmark mark='d'/> Restore the correlation, minus "
            f"{abs(m['params'][4]):.2f}: high-variance paths come with falls, the wide Gaussians slide left, and the "
            "smile tilts into a skew."
        )
        ) as vo:
            self.play(FadeIn(cur), FadeIn(dial[:2]), GrowArrow(arrow), FadeIn(src))
            vo.wait_until("a")
            self.play(Transform(cur, P[1]), FadeIn(dial[2]), arrow.animate.next_to(dial[2], LEFT, buff=0.15),
                      FadeIn(note_), run_time=2)
            vo.wait_until("b")
            self.play(Transform(cur, P[2]), FadeIn(dial[3]), arrow.animate.next_to(dial[3], LEFT, buff=0.15), run_time=2)
            vo.wait_until("p")
            self.play(FadeIn(pp))
            vo.wait_until("c")
            self.play(FadeOut(pp), Transform(cur, P[3]), FadeIn(dial[4]), arrow.animate.next_to(dial[4], LEFT, buff=0.15),
                      run_time=2)
            vo.wait_until("d")
            self.play(Transform(cur, P[4]), FadeIn(dial[5]), arrow.animate.next_to(dial[5], LEFT, buff=0.15), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\ln S_T \,\big|\, \{v_s\}", r"\sim", r"\mathcal{N}\Big(\!-\tfrac12 \int_0^T\! v\,ds,\ "
                      r"\int_0^T\! v\,ds\Big)\qquad (\rho = 0)", font_size=32, colors={r"\ln S_T \,\big|\, \{v_s\}": SPOT}),
                cmath(r"C", r"=", r"\mathbb{E}\Big[C_{\text{BS}}\big(S_0, K, T, \bar\sigma^2_T\big)\Big],\quad "
                      r"\bar\sigma^2_T = \tfrac1T\!\int_0^T\! v\,ds", font_size=32, colors={r"C": OPT}),
                cmath(r"C", r"\approx", r"C_{\text{BS}}\big(\mathbb{E}\bar\sigma^2\big) + \tfrac12\,"
                      r"\partial^2_{\sigma^2} C_{\text{BS}}\ \operatorname{Var}\big(\bar\sigma^2\big)", font_size=32,
                      colors={r"C": OPT}),
                cmath(r"\partial^2_{\sigma} C_{\text{BS}}", r"=", r"\text{vega}\cdot\frac{d_1 d_2}{\sigma}", font_size=34,
                      colors={r"\partial^2_{\sigma} C_{\text{BS}}": VAR}),
                cmath(r"W^1", r"=", r"\rho\,W^2 + \sqrt{1-\rho^2}\,W^\perp", font_size=34, colors={r"W^1": SPOT}),
                cmath(r"C", r"=", r"\mathbb{E}\Big[C_{\text{BS}}\big(S_0\,\xi_T,\ K,\ T,\ (1-\rho^2)\,\bar\sigma^2_T\big)"
                      r"\Big],\ \ \xi_T = e^{\rho\int\!\sqrt v\,dW^2 - \frac{\rho^2}{2}\int v\,ds}", font_size=30,
                      colors={r"C": OPT})]
        whys = [why(r"$W^1$ is independent of the variance path: given the path, the log price is a sum of independent "
                    r"Gaussian increments", 20),
                why(r"the tower property: average Black--Scholes over the realized variance (Hull and White 1987)", 20),
                why(r"Taylor to second order in the vol of vol; the first-order term vanishes on average", 20),
                why(r"differentiate vega $= S\sqrt T\varphi(d_1)$: positive where $|d_1 d_2|$ is large (the wings), "
                    r"negative at the money: the wings rise, the centre falls, symmetrically (Renault and Touzi 1996)", 20),
                why(r"split the price's noise into the part along the variance's noise and the part orthogonal to it", 20),
                why(r"condition on $W^2$: the price is lognormal again, with its spot moved by $\xi_T$; when $\rho < 0$ "
                    r"high-variance paths have small $\xi_T$: the skew (Romano and Touzi 1997)", 20)]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.4, buff=0.75, edge=6.9)
        hist = label(r"Hull and White; Scott; Wiggins (1987) \textperiodcentered\ Stein and Stein (1991) "
                     r"\textperiodcentered\ Renault and Touzi (1996) \textperiodcentered\ Romano and Touzi (1997)",
                     font_size=18, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            (
            "Now the proof. With no correlation, the price's Brownian motion is independent of the variance path, so "
            "given the path the log price is Gaussian with the integrated variance. <bookmark mark='a'/> By the tower "
            "property the price is Black–Scholes averaged over realized variance: Hull and White's theorem of 1987. "
            "<bookmark mark='b'/> Expand to second order in the vol of vol: the correction is half Black–Scholes's "
            "curvature in variance times the variance of the realized variance. <bookmark mark='c'/> That curvature "
            "is vega times d-one d-two over sigma: negative at the money, positive in the wings. So the wings rise "
            "and the centre falls, symmetrically: Renault and Touzi. <bookmark mark='d'/> With correlation, split "
            "the price's noise along and across the variance's noise. <bookmark mark='e'/> Condition on the "
            "variance's noise: the price is lognormal again, with less variance and a spot shifted by xi T. When rho "
            "is negative, high-variance paths have small xi T. That is Romano and Touzi's formula: the skew."
        )
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            self.play(FadeIn(hist))
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            vo.wait_until("e")
            step(5)
        self.wait(0.4)
        self.clear_scene()

    def check(self, m):
        r = m["rows"]
        k = np.asarray(r["k"])
        g = axes([-0.45, 0.45], [0.38, 0.62], x_length=6.8, y_length=4.2, xlabel=r"log-moneyness, three months",
                 ylabel=r"implied volatility", xticks=[-0.4, -0.2, 0, 0.2, 0.4], yticks=[0.4, 0.45, 0.5, 0.55, 0.6],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        kk = np.linspace(-0.4, 0.4, 13)
        cosl = curve(ax, kk, np.asarray(r["cos_iv"]), WHITE, stroke_width=3)

        def bars(ivs, ses, prices, col, dx):
            out = VGroup()
            for kx, v, s_, p in zip(k, ivs, ses, prices):
                # the price error bar mapped to vol by the local vega
                vega = 1.0 * np.sqrt(m["T"]) * np.exp(-0.5 * (kx / (v * np.sqrt(m["T"])) - 0.5 * v * np.sqrt(m["T"])) ** 2) / np.sqrt(2 * np.pi)
                dv = 2 * s_ / max(vega, 1e-6)
                y0, y1 = np.clip(v - dv, 0.38, 0.62), np.clip(v + dv, 0.38, 0.62)
                out.add(VGroup(Line(ax.c2p(kx + dx, y0), ax.c2p(kx + dx, y1), color=col, stroke_width=3),
                               Dot(ax.c2p(kx + dx, np.clip(v, 0.38, 0.62)), radius=0.05, color=col)))
            return out

        plain = bars(r["plain_iv"], r["plain_se"], r["plain"], GREY_B, -0.012)
        cond = bars(r["cond_iv"], r["cond_se"], r["cond"], IV, 0.012)
        leg = legend([(WHITE, r"COS, exact"), (GREY_B, r"plain Monte Carlo, $\pm 2$ s.e."),
                      (IV, r"Romano--Touzi conditional, $\pm 2$ s.e.")], font_size=17).next_to(g, UP, buff=0.12).align_to(g, LEFT)
        ratio = float(np.median(r["se_ratio"]))
        zmax = float(np.max(np.abs(r["z"])))
        inside = zmax < 2
        side = VGroup(
            wrapped_label(f"{m['N']:,}".replace(",", "{,}") + r" variance paths by Andersen's QE scheme, the same paths for "
                          r"both estimators", 4.4, 19, GREY_A),
            MathTex(rf"\text{{standard error}}\ \div\ {ratio:.0f}", font_size=34, color=IV),
            wrapped_label(r"median over 13 strikes: averaging Black--Scholes over the paths removes the price noise "
                          r"given the path, and keeps only the noise of the variance", 4.4, 19, GREY_A),
            MathTex(rf"\max |z| = {zmax:.1f}", font_size=30, color=RV if inside else BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.45)
        verdict = (f"Every strike agrees with the exact price within {zmax:.1f} standard errors, so the formula holds."
                   if inside else
                   f"The largest gap is {zmax:.1f} standard errors: the time step of the simulation shows, a reminder "
                   "that the theorem is exact but the variance paths are not.")
        src = simulated(r"the fitted Heston, three months, 13 strikes")
        with self.voiceover(
            (
            (
            f"The theorem is also an algorithm. Simulate {m['N']:,} variance paths of the fitted model. Plain Monte "
            "Carlo also simulates the price: grey error bars. <bookmark mark='a'/> The conditional estimator plugs "
            f"each path's shifted spot and reduced variance into Black–Scholes: bars about {ratio:.0f} times "
            "narrower, because the price's own noise, given the path, has been integrated out exactly. At the money "
            f"the exact implied volatility is {100 * r['cos_iv'][6]:.2f} percent and the conditional estimate "
            f"{100 * r['cond_iv'][6]:.2f}. <bookmark mark='b'/> Across all thirteen strikes: {verdict} Desks use this "
            "conditional Monte Carlo whenever a model is Gaussian given its volatility path."
        )
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(cosl), FadeIn(leg[0]), FadeIn(side[0]))
            self.play(FadeIn(leg[1]), LaggedStart(*[FadeIn(b_) for b_ in plain], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(leg[2]), LaggedStart(*[FadeIn(b_) for b_ in cond], lag_ratio=0.1), FadeIn(side[1]),
                      FadeIn(side[2]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()
