from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, GOOD, IV, OPT, PART, SPOT, illustration, load, axes, data_range


class Asian(VoiceoverScene):
    def construct(self):
        a = load("asian")
        sc = load("asian_scatter")
        self.card()
        self.live(sc)
        self.derive(sc)
        self.scatter(sc, a)
        self.lab(a)

    def card(self):
        c = chapter_card(6, r"Averages and extremes: Asians and lookbacks", r"Why is an option on the average so much "
                         r"cheaper, and how do you price it fast?", lit=(1979, 1990), part=PART)
        with self.voiceover("Chapter six. Averages and extremes: Asian options and lookbacks."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def live(self, sc):
        p = np.asarray(sc["path"])
        avg = np.concatenate([[p[0]], np.asarray(sc["avg"])])
        mn = np.asarray(sc["min"])
        n = len(p) - 1
        t = np.arange(n + 1)
        lo, hi = float(min(p.min(), avg.min())) - 3, float(p.max()) + 3
        g = axes([0, n], [lo, hi], x_length=7.4, y_length=4.4, xlabel=r"trading days, one year", ylabel=r"price",
                 xticks=[0, 63, 126, 189, 252], yticks=[round(lo + 3), 100, round(hi - 3)], font_size=15)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        k = DashedLine(ax.c2p(0, 100), ax.c2p(n, 100), stroke_color=GREY_C, stroke_width=1.5)
        tr = ValueTracker(0)
        lp = tracing(ax, t, p, tr, SPOT, stroke_width=2.2)
        la = tracing(ax, t, avg, tr, QC.HOUSE, stroke_width=3)
        lm = tracing(ax, t, mn, tr, IV, stroke_width=3)
        leg = legend([(SPOT, r"the price"), (QC.HOUSE, r"its running average"), (IV, r"its running minimum")],
                     font_size=17).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        A, ST, m = float(avg[-1]), float(p[-1]), float(mn[-1])
        side = VGroup(
            MathTex(rf"\text{{Asian call: }} (A - 100)^+ = {max(A - 100, 0):.2f}", font_size=30, color=QC.HOUSE),
            MathTex(rf"\text{{vanilla call: }} (S_T - 100)^+ = {max(ST - 100, 0):.2f}", font_size=30, color=SPOT),
            MathTex(rf"\text{{lookback: }} S_T - \min S = {ST - m:.2f}", font_size=30, color=IV),
            wrapped_label(r"the average moves slowly and forgets the last day's spike; the minimum only ever falls. One "
                          r"payoff is tamer than the price, the other wilder", 4.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        src = illustration(r"one simulated year, 25\% volatility, daily fixings")
        with self.voiceover(
            "Two path-dependent payoffs on one path: a gold line trails the price, its running average, and a blue one, "
            "its running minimum. <bookmark mark='a'/> The average moves slowly and shrugs off the last day's spike, which "
            "is why commodity contracts settle on averages. The minimum only ever falls. <bookmark mark='b'/> An Asian call "
            "pays the average minus the strike; a floating lookback pays the final price minus the lowest one."
        ) as vo:
            self.play(FadeIn(g), Create(k), FadeIn(leg), FadeIn(src))
            self.add(lp, la, lm)
            vo.wait_until("a")
            self.play(tr.animate.set_value(n), run_time=6, rate_func=linear)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x_) for x_ in side], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def derive(self, sc):
        rows = [
            cmath(r"\log G", r"=", r"\tfrac1n\textstyle\sum_i \log S_{t_i} \sim \mathcal N\big(m_G,\ s_G^2\big)", font_size=34,
                  colors={r"\log G": QC.HOUSE}),
            cmath(r"\operatorname{Var}\log G", r"\to", r"\frac{\sigma^2}{T^2}\int_0^T\!\!\int_0^T \min(s, t)\,ds\,dt = "
                  r"\frac{\sigma^2 T}{3}", font_size=32, colors={r"\operatorname{Var}\log G": QC.HOUSE}),
            cmath(r"\hat\theta_{cv}", r"=", r"\bar Y_A - b\,(\bar Y_G - \mu_G),\quad \operatorname{Var} = "
                  r"\operatorname{Var}\bar Y_A\,(1 - \rho^2)", font_size=32, colors={r"\hat\theta_{cv}": GOOD}),
            cmath(r"u_t + \tfrac12\sigma^2\big(q(t) - x\big)^2 u_{xx}", r"=", r"0,\quad V = S_0\,u(0, X_0)",
                  font_size=32, colors={r"u_t + \tfrac12\sigma^2\big(q(t) - x\big)^2 u_{xx}": IV}),
        ]
        whys = [why(r"$m_G = \log S_0 + (r - q - \tfrac{\sigma^2}{2})\bar t$, $s_G^2 = \tfrac{\sigma^2}{n^2}"
                    r"\sum_{i,j}\min(t_i, t_j)$: a linear map of a Gaussian vector is Gaussian, so the geometric Asian "
                    r"is log-normal, priced in closed form (Kemna and Vorst 1990)"),
                why(r"$\iint \min(s,t) = T^3/3$: the effective volatility is $\sigma/\sqrt 3$, which is why Asians are "
                    r"cheap"),
                why(rf"optimal $b = \operatorname{{Cov}}/\operatorname{{Var}}$; the measured correlation $\rho = "
                    rf"{sc['rho']:.4f}$ cuts the noise {sc['ratio']:.0f}-fold"),
                why(r"Shreve II 7.5; Vecer (2001): change to the numeraire $S$, with $X_t$ the remaining average per unit "
                    r"of $S$, and the two-dimensional problem in $(S, A)$ becomes one PDE in $x$")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.6, buff=0.75, edge=6.9)
        pp = pause_card(r"Why is an Asian call worth about half a vanilla?", width=5.4).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Why are Asians cheap? The log of the geometric average is an average of Gaussian log prices, so it is "
            "Gaussian, with a variance built from the minimum of every pair of fixing times. <bookmark mark='a'/> In "
            "continuous time that double integral is T cubed over three: averaging divides the variance by three. "
            "<bookmark mark='p'/> So why is an Asian call worth about half a vanilla? Its effective volatility is about "
            "fifty-eight percent of the price's. <bookmark mark='b'/> The arithmetic average has no closed form, but moves "
            "almost exactly with the geometric one: simulate both, and correct by the geometric one's known error. "
            "<bookmark mark='c'/> Or change the numeraire to the stock, as Shreve does after Vecer, and the problem in "
            "spot and average collapses to one equation in one variable."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("p")
            self.play(FadeIn(pp))
            vo.wait_until("b")
            self.play(FadeOut(pp))
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def scatter(self, sc, a):
        ya, yg = np.asarray(sc["ya"]), np.asarray(sc["yg"])
        top = float(np.quantile(ya, 0.99)) * 1.1
        g = axes([0, top], [0, top], x_length=5.0, y_length=5.0, xlabel=r"geometric Asian payoff",
                 ylabel=r"arithmetic Asian payoff", xticks=[0, round(top / 2), round(top)],
                 yticks=[0, round(top / 2), round(top)], font_size=15).to_edge(LEFT, buff=0.9).shift(DOWN * 0.1)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.025, color=QC.HOUSE, fill_opacity=0.6)
                        for x, y in zip(yg, ya) if x < top and y < top])
        b = sc["b"]
        mx, my = float(yg.mean()), float(ya.mean())
        line = Line(ax.c2p(0, my - b * mx), ax.c2p(top, my + b * (top - mx)), stroke_color=GOOD, stroke_width=3)
        side = VGroup(
            MathTex(rf"b = {b:.3f},\quad \rho = {sc['rho']:.4f}", font_size=32, color=GOOD),
            wrapped_label(rf"{len(ya):,} paths: the two payoffs fall on a line. What the control variate leaves to "
                          rf"estimate is only the thin scatter around it: the noise falls {sc['ratio']:.0f}-fold, as if "
                          rf"with {sc['ratio'] ** 2:.0f} times the paths".replace(",", "{,}"), 4.8, 19, GREY_A),
            MathTex(rf"\text{{geometric (closed form) }} {a['geo_cf']:.2f},\ \text{{arithmetic }} {a['price']:.2f},"
                    rf"\ \text{{vanilla }} {a['vanilla']:.2f}", font_size=26, color=OPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        src = illustration(r"one-year at-the-money Asian calls, 25\% volatility, 252 daily fixings")
        lk = wrapped_label(rf"a lookback pays $S_T - \min S$: {a['lookback_cf']:.1f} watched continuously (Goldman, Sosin "
                           rf"and Gatto 1979; Conze and Viswanathan 1991), {a['lookback_mc_daily']:.1f} at daily closes. "
                           r"A shout option, a cousin, lets the holder lock in the gain once", 4.8, 18, IV)
        lk.next_to(side, DOWN, buff=0.3).align_to(side, LEFT)
        with self.voiceover(
            "See the control variate. Each dot is one path: across, its geometric Asian payoff; up, its arithmetic one. "
            f"<bookmark mark='a'/> They fall on a line, with correlation {sc['rho']:.4f}, and what is left to estimate is "
            f"the thin scatter around it: the noise falls {sc['ratio']:.0f}-fold, as if we had run {sc['ratio'] ** 2:.0f} "
            f"times the paths. Geometric {a['geo_cf']:.2f} in closed form, arithmetic {a['price']:.2f}, vanilla "
            f"{a['vanilla']:.2f}: about half. <bookmark mark='b'/> The lookback needs no simulation: reflection gives "
            "Goldman, Sosin and Gatto's closed form, "
            f"{a['lookback_cf']:.1f} watched continuously, against {a['lookback_mc_daily']:.1f} at daily closes, chapter "
            "four's lesson again."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.002, run_time=3))
            vo.wait_until("a")
            self.play(Create(line), LaggedStart(*[FadeIn(x_) for x_ in side], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(lk))
        self.wait(0.4)
        self.clear_scene()

    def lab(self, a):
        card = lab_card(r"the geometric Asian, the control variate", [
            "def geometric_asian_call(S, K, T, sigma, n, r=0.0, q=0.0):",
            "    dt = T / n",
            "    t = dt * np.arange(1, n + 1)",
            "    mu = np.log(S) + (r - q - 0.5 * sigma ** 2) * t.mean()",
            "    var = sigma ** 2 * np.sum(np.minimum.outer(t, t)) / n ** 2",
            "    sG = np.sqrt(var)",
            "    d1 = (mu - np.log(K) + var) / sG",
            "    return np.exp(-r * T) * (np.exp(mu + 0.5 * var) * N(d1)",
            "                             - K * N(d1 - sG))",
        ], source="explainer/quant/house/exotics.py", width=7.8, font_size=17).to_corner(UL, buff=0.35)
        rows = a["rows"]
        outs = [f"geometric_asian_call(100, 100, 1, 0.25, 252, 0.02)  ->  {a['geo_cf']:.2f}",
                f"arithmetic, with the control variate: {a['price']:.2f}   vanilla: {a['vanilla']:.2f}",
                f"noise at {rows[-1]['n']:,} paths: {rows[-1]['sd_plain']:.4f} plain, {rows[-1]['sd_cv']:.4f} with it"]
        with self.voiceover(
            "In the House's library the geometric Asian is eight lines: the mean of the log average, its variance "
            "from the matrix of minimum times, and a Black–Scholes formula with those two numbers. "
            "<bookmark mark='a'/> Run it on the one-year call. The geometric Asian is worth "
            f"{a['geo_cf']:.2f}, the arithmetic one, by simulation with this control variate, {a['price']:.2f}."
            " With the pieces in hand, the snowball itself. Next."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs, font_size=17)
        self.wait(0.4)
        self.clear_scene()

