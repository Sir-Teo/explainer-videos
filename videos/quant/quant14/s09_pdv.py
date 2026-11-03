from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import (BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, VAR, load, pause, real_data,
                                         running_min)


def _yr(days):
    return 1970 + np.asarray(days, float) / 365.2425


class PDV(VoiceoverScene):
    def construct(self):
        p = load("pdv")
        self.card()
        self.model(p)
        self.memories(p)
        self.replay(load("pdv_replay"), p)
        self.fit(p)
        self.markov(load("pdv4"), p)

    def card(self):
        c = chapter_card(13, r"Volatility is (mostly) path-dependent", r"How much of volatility is just the past?",
                         lit=(2024,), part=PART)
        with self.voiceover("Chapter thirteen. Volatility is mostly path-dependent."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self, p):
        rows = [cmath(r"\sigma_t", r"=", r"\beta_0 + \beta_1 R_{1,t} + \beta_2\sqrt{R_{2,t}}", font_size=40,
                      colors={r"\sigma_t": IV}),
                cmath(r"R_{1,t}", r"=", r"\sum_{t_i \le t} K_1(t - t_i)\,r_{t_i},\qquad R_{2,t} = \sum_{t_i \le t} "
                      r"K_2(t - t_i)\,r_{t_i}^2", font_size=34, colors={r"R_{1,t}": OPT}),
                cmath(r"K(\tau)", r"\propto", r"(\tau + \delta)^{-\alpha}", font_size=38, colors={r"K(\tau)": VAR})]
        whys = [why(r"Guyon and Lekeufack (2023): implied volatility as a function of the price path alone, no hidden "
                    r"random factor"),
                why(r"a trend (weighted past returns) and an activity (weighted past squared returns)"),
                why(r"time-shifted power-law kernels: memory that fades slowly, the same shape as rough volatility's "
                    r"kernel")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.0, buff=0.85, edge=6.9)
        with self.voiceover(
            "There is another way to read the same facts. In 2023 Julien Guyon and Jordan Lekeufack asked how much of "
            "volatility is simply a function of the path the price has already taken. Their answer: most of it. "
            "Write implied volatility as a constant, plus a trend term, plus the square root of an activity term. "
            "<bookmark mark='a'/> The trend is a weighted sum of past returns; the activity, of past squared returns. "
            "<bookmark mark='b'/> The weights fade with time like a shifted power law, slowly, the same shape as a "
            "rough kernel. For the S&P 500 and the VIX, they found this explains most of the variation in implied "
            "volatility, and that a model built on it fits options on both."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def memories(self, p):
        from explainer.quant.house import rough as R
        days = np.asarray(p["days"])
        n = 260
        i0 = int(np.searchsorted(days, p["split_day"])) + 120
        vol = np.asarray(p["vol"], float)
        # bitcoin's daily returns, re-derived from the House's data loader through the fitted features
        from videos.quant.quant14.compute import _pdv_data
        d_all, r_all, _ = _pdv_data()
        j0 = int(np.searchsorted(d_all, days[i0]))
        r = r_all[j0 - 1000: j0 + n]
        R1, R2 = R.pdv_features(r, 1 / 365, p["alpha1"], p["delta1"], p["alpha2"], p["delta2"], lookback=1000)
        R1, R2 = R1[1000:], np.sqrt(np.maximum(R2[1000:], 0))
        price = np.exp(np.cumsum(r[1000:]))
        b = p["beta"]
        sig = b[0] + b[1] * R1 + b[2] * R2
        dv = vol[i0: i0 + n]
        x = np.arange(n)
        g1 = axes([0, n], [price.min() * 0.95, price.max() * 1.05], x_length=7.6, y_length=2.0, ylabel=r"bitcoin price",
                  xticks=[], yticks=[], font_size=14)
        g2 = axes([0, n], [0.2, 1.0], x_length=7.6, y_length=2.4, xlabel=r"days", ylabel=r"implied volatility",
                  xticks=[0, 100, 200], yticks=[0.4, 0.6, 0.8], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=14)
        VGroup(g1, g2).arrange(DOWN, buff=0.45).to_edge(LEFT, buff=0.5)
        t = ValueTracker(1)
        lp = tracing(g1.ax, x, price, t, WHITE, stroke_width=2)
        ld = tracing(g2.ax, x, np.clip(dv, 0.2, 1.0), t, IV, stroke_width=2)
        ls = tracing(g2.ax, x, np.clip(sig, 0.2, 1.0), t, MODEL_COL["PDV"], stroke_width=2.4)
        tau = np.arange(1000) / 365

        def trail():
            i = int(t.get_value())
            k = R.tspl_kernel(tau[:i + 1], p["alpha2"], p["delta2"])
            k = k / k.max()
            return VGroup(*[Line(g1.ax.c2p(i - j, price.min() * 0.95), g1.ax.c2p(i - j, price.min() * 0.95 + 0.25 * k[j] *
                                                                                  (price.max() - price.min())),
                                 stroke_color=YELLOW, stroke_width=2, stroke_opacity=0.6) for j in range(0, i + 1, 3)])

        tr_ = always_redraw(trail)
        mx1 = max(np.abs(R1).max(), 1e-9)
        mx2 = max(R2.max(), 1e-9)
        base = RIGHT * 4.6 + DOWN * 0.6

        def bars():
            i = int(t.get_value())
            h1 = 1.6 * R1[i] / mx1
            h2 = 2.6 * R2[i] / mx2
            return VGroup(Rectangle(width=0.7, height=max(abs(h1), 0.01), stroke_width=0, fill_color=OPT,
                                    fill_opacity=0.9).move_to(base + LEFT * 0.8 + UP * h1 / 2),
                          Rectangle(width=0.7, height=max(h2, 0.01), stroke_width=0, fill_color=VAR,
                                    fill_opacity=0.9).move_to(base + RIGHT * 0.8 + UP * h2 / 2))

        bb = always_redraw(bars)
        axis = Line(base + LEFT * 1.5, base + RIGHT * 1.5, stroke_color=GREY_C)
        bl = VGroup(label(r"trend $R_1$", font_size=18, color=OPT).move_to(base + LEFT * 0.8 + DOWN * 1.9),
                    label(r"activity $\sqrt{R_2}$", font_size=18, color=VAR).move_to(base + RIGHT * 0.8 + DOWN * 1.9))
        leg = legend([(IV, r"DVOL"), (MODEL_COL["PDV"], r"rebuilt from the two memories"),
                      (YELLOW, r"the activity kernel's weights on past days")], font_size=15).to_corner(UR, buff=0.3)
        src = real_data(r"bitcoin 2024, out of sample; the fitted kernels of the next replay")
        with self.voiceover(
            "Here is the model running. Top, Bitcoin's price, day by day. Behind the moving date, the yellow trail "
            "is the activity kernel's weight on each past day. On the right, the two memories: the trend, which can "
            "be negative, and the activity, always positive. <bookmark mark='a'/> Below, implied volatility rebuilt "
            "from the two memories alone, against DVOL: when the price lurches, both jump."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(lp), FadeIn(ld), FadeIn(ls), FadeIn(tr_), FadeIn(axis), FadeIn(bb),
                      FadeIn(bl), FadeIn(leg), FadeIn(src))
            self.play(t.animate.set_value(n - 1), run_time=max(vo.remaining(0.0) - 0.5, 8), rate_func=linear)
        for m in (lp, ld, ls, tr_, bb):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def replay(self, rp, p):
        cv = running_min(rp["curve"])
        steps = np.arange(len(cv))
        best = rp["best"]
        idx = sorted(set([0, 1, 2, len(best) // 2, len(best) - 1]))
        ck = [best[i]["eval"] for i in idx]
        tau = np.asarray(rp["tau"]) * 365

        def frame(j):
            b = best[idx[j]]
            g = axes([0, 200], [0, 1.05], x_length=5.0, y_length=3.0, xlabel=r"lag (days)", ylabel=r"kernel (scaled)",
                     xticks=[0, 100, 200], yticks=[0, 1], font_size=13)
            k1 = np.asarray(b["K1"])
            k2 = np.asarray(b["K2"])
            x = b["x"]
            return VGroup(g, curve(g.ax, tau, k1 / k1.max(), OPT, stroke_width=2.5),
                          curve(g.ax, tau, k2 / k2.max(), VAR, stroke_width=2.5),
                          MathTex(rf"R^2 = {b['r2']:.2f}", font_size=28, color=MODEL_COL["PDV"]).next_to(g, UP, buff=0.1),
                          MathTex(rf"\alpha_1 = {x[0]:.2f},\ \delta_1 = {365 * x[1]:.0f}\text{{d}};\ \alpha_2 = {x[2]:.2f},\ "
                                  rf"\delta_2 = {365 * x[3]:.0f}\text{{d}}", font_size=20).next_to(g, DOWN, buff=0.15))

        rpl = TrainingReplay(steps, cv, frame, ck, ylabel=r"mean squared error, in sample", xlabel=r"evaluation",
                             color=MODEL_COL["PDV"], log_y=True)
        leg = legend([(OPT, r"trend kernel $K_1$"), (VAR, r"activity kernel $K_2$")], font_size=15).arrange(
            RIGHT, buff=0.3).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "How is it fitted? The four shape numbers, two exponents and two shifts, are searched by nonlinear "
            "least squares, and for each candidate the three betas come out of an ordinary regression: variable "
            "projection. On the right, the error as the search proceeds; on the left, the two kernels at each "
            "improvement. <bookmark mark='a'/> The trend kernel collapses toward a short memory; the activity "
            f"kernel settles into a power law shifted by about {365 * p['delta2']:.0f} days. In sample, the "
            f"fit explains {100 * p['r2_train']:.0f} percent of DVOL's variation."
        ) as vo:
            self.play(FadeIn(rpl), FadeIn(leg))
            vo.wait_until("a")
            rpl.play(self, run_time=max(vo.remaining(0.0) - 0.5, 5))
        self.wait(0.4)
        self.clear_scene()

    def markov(self, q, p):
        rows = [cmath(r"K(\tau)", r"=", r"(1 - \theta)\lambda_0 e^{-\lambda_0\tau} + \theta\lambda_1 e^{-\lambda_1\tau}",
                      font_size=38, colors={r"K(\tau)": VAR}),
                cmath(r"R_t", r"=", r"(1 - \theta)R^{(0)}_t + \theta R^{(1)}_t,\qquad dR^{(j)}_t = \lambda_j\big(r_t^n - R^{(j)}_t\big)dt",
                      font_size=34, colors={r"R_t": VAR})]
        whys = [why(r"each kernel a convex mix of two exponentials (Guyon and Lekeufack's 4-factor Markovian PDV)"),
                why(r"each exponential is an exponential moving average: four factors, each updated by one line, and the "
                    r"model is Markov")]
        step = ladder(self, rows, whys, keep=2, top=3.3, x=-0.8, buff=0.5, edge=6.9)  # both rows above the lab card
        card = lab_card(r"the 4-factor Markovian PDV", [
            "def pdv4_step(R, r, dt, lam):",
            "    e = np.exp(-lam * dt)",
            "    return e * R + (1 - e) * r / dt     # one EMA, one day",
            "",
            "for i, x in enumerate(r ** power):",
            "    R0 = pdv4_step(R0, x, dt, lam0)",
            "    R1 = pdv4_step(R1, x, dt, lam1)",
            "    out[i] = (1 - theta) * R0 + theta * R1",
        ], source="explainer/quant/house/rough.py: pdv4_step, pdv4_features", width=7.0).to_edge(DOWN, buff=1.3).to_edge(LEFT, buff=0.4)
        hl = q["half_lives_days"]
        outs = [f"half-lives (days): trend {hl[0]:.1f} / {hl[1]:.1f}, activity {hl[2]:.1f} / {hl[3]:.0f}",
                f"R^2 in sample {q['r2_train']:.2f}   out of sample {q['r2_test']:.2f}",
                f"time-shifted power law:   {q['tspl_train']:.2f}  /  {q['tspl_test']:.2f}"]
        cards = VGroup(
            wrapped_label(r"Nutz and Riveros Valdevenito (Finance and Stochastics 28(4), 2024): the 4-factor PDV SDE "
                          r"has a unique strong solution for all parameters; Andr\`es and Jourdain (2024): general kernels",
                          4.6, 17, GREY_A)).to_edge(RIGHT, buff=0.35).shift(DOWN * 1.2)
        better = q["r2_test"] > q["tspl_test"]
        verdict = ("the Markovian version does better out of sample than the power-law kernels it replaces"
                   if better else "the Markovian version gives up a little out of sample, in exchange for being Markov")
        with self.voiceover(
            "There is a Markovian version. Make each kernel a convex mix of two exponentials. <bookmark mark='a'/> "
            "Then each memory is a blend of two exponential moving averages, and the model has four factors, each "
            "updated by one line: the House's code is exactly that. <bookmark mark='b'/> Fitted the same way on "
            "Bitcoin: the activity memory splits into a fast factor of "
            f"{hl[2]:.0f} days and a slow one of {hl[3]:.0f}. Out of sample it explains {100 * q['r2_test']:.0f} "
            f"percent of DVOL, against {100 * q['tspl_test']:.0f} for the power law: {verdict}. "
            "<bookmark mark='c'/> Is it a well-defined stochastic differential equation? Marcel Nutz and Andrés "
            "Riveros Valdevenito proved it is, and Hervé Andrès and Benjamin Jourdain extended that to general kernels."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            self.play(FadeIn(card))
            vo.wait_until("b")
            lab_run(self, card, outs, run_time=2.5, font_size=17)
            vo.wait_until("c")
            self.play(FadeIn(cards))
        self.wait(0.4)
        self.clear_scene()

    def fit(self, p):
        t = _yr(p["days"])
        vol = np.asarray(p["vol"], float)
        pred = np.asarray(p["pred"], float)
        base = np.asarray(p["base"], float)
        split = _yr(p["split_day"])
        g = axes([2021.25, 2026], [0.2, 1.4], x_length=8.0, y_length=4.2, ylabel=r"bitcoin's 30-day implied volatility",
                 xticks=[2022, 2023, 2024, 2025], yticks=[0.4, 0.8, 1.2], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        ok = np.isfinite(vol)
        l_v = curve(ax, t[ok], np.clip(vol[ok], 0.2, 1.4), IV, stroke_width=2.4)
        l_p = curve(ax, t[ok], np.clip(pred[ok], 0.2, 1.4), MODEL_COL["PDV"], stroke_width=2.0)
        l_b = curve(ax, t[ok], np.clip(base[ok], 0.2, 1.4), GREY_B, stroke_width=1.6)
        cut = DashedLine(ax.c2p(split, 0.2), ax.c2p(split, 1.4), stroke_color=GREY_A, stroke_width=1.5)
        cl = label(r"fitted up to here; after it, out of sample", font_size=16, color=GREY_A).next_to(ax.c2p(split, 1.4),
                                                                                                    RIGHT, buff=0.1)
        leg = legend([(IV, r"DVOL"), (MODEL_COL["PDV"], r"path-dependent volatility, from bitcoin's returns only"),
                      (GREY_B, r"baseline: a line in the past 30 days' realized vol")], font_size=16).next_to(
            g, UP, buff=0.1).align_to(g, LEFT)
        b = p["beta"]
        side = VGroup(
            MathTex(rf"R^2:\ {p['r2_train']:.2f}\ \text{{(in)}},\ \ {p['r2_test']:.2f}\ \text{{(out)}}", font_size=28,
                    color=MODEL_COL["PDV"]),
            MathTex(rf"\text{{baseline: }} {p['r2_base_train']:.2f},\ \ {p['r2_base_test']:.2f}", font_size=26, color=GREY_B),
            MathTex(rf"\beta_2 = {b[2]:.2f}", font_size=28, color=WHITE),
            wrapped_label(rf"activity does almost all the work: its term moves implied vol by {100 * p['contrib']['activity']:.0f} "
                          rf"points (one s.d.), the trend by {100 * p['contrib']['trend']:.1f}. For the S\&P 500 the trend "
                          r"term matters (falls raise volatility); bitcoin's implied vol cares about how much it moved, "
                          r"hardly which way", 3.9, 18, GREY_A),
            wrapped_label(rf"activity's memory: a power law shifted by {365 * p['delta2']:.0f} days, exponent "
                          rf"{p['alpha2']:.2f}", 3.9, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)
        src = real_data(r"Deribit DVOL daily; Binance BTCUSDT daily returns since 2018 (kernels need 1{,}000 days of past)")
        with self.voiceover(
            "Fit it to Bitcoin. The inputs are only Bitcoin's own daily returns, going back to 2018; the target is "
            "DVOL, the market's thirty-day implied volatility. The model is fitted on 2021 to 2023, and then frozen. "
            f"<bookmark mark='a'/> In sample it explains {100 * p['r2_train']:.0f} percent of DVOL's variation. "
            f"<bookmark mark='b'/> Out of sample, in 2024 and 2025, {100 * p['r2_test']:.0f} percent, where a simple "
            "line in the last month's realized volatility, fitted the same way, does worse than a constant. "
            "<bookmark mark='c'/> And look at what does the work. Pause and predict: for Bitcoin, does it matter "
            "which way the price moved? Hardly. The activity term moves DVOL by about "
            f"{100 * p['contrib']['activity']:.0f} points, the trend term by {100 * p['contrib']['trend']:.1f}. "
            "Bitcoin's implied volatility cares how much the price has moved, with a memory that fades like a "
            "power law, and hardly which way. The S&P 500, in the next chapter, is different."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg[0]), Create(l_v), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(cut), FadeIn(cl), Create(l_p), FadeIn(leg[1]), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(l_b), FadeIn(leg[2]), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()
