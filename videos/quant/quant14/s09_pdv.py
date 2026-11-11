from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import axes, data_range, skew_range
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
        c = chapter_card(13, 'Path-dependent volatility', 'How much of an implied index can return features reconstruct?',
                         lit=(2024,), part=PART)
        with self.voiceover("""Chapter thirteen. Path-dependent volatility and implied-index tracking."""):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self, p):
        rows = [cmath(r"\sigma_t", r"=", r"\beta_0 + \beta_1 R_{1,t} + \beta_2\sqrt{R_{2,t}}", font_size=40,
                      colors={r"\sigma_t": IV}),
                cmath(r"R_{1,t}", r"=", r"\sum_{t_i \le t} K_1(t - t_i)\,r_{t_i},\qquad R_{2,t} = \sum_{t_i \le t} "
                      r"K_2(t - t_i)\,r_{t_i}^2", font_size=34, colors={r"R_{1,t}": OPT}),
                cmath(r"K(\tau)", r"\propto", r"(\tau + \delta)^{-\alpha}", font_size=38, colors={r"K(\tau)": VAR})]
        whys = [why('Empirical index proxy inspired by Guyon--Lekeufack: same-day implied volatility regressed on return history'),
                why(r"a trend (weighted past returns) and an activity (weighted past squared returns)"),
                why(r"time-shifted power-law kernels: memory that fades slowly, the same shape as rough volatility's "
                    r"kernel")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.0, buff=0.85, edge=6.9)
        with self.voiceover(
            """Guyon and Lekeufack's 2023 work studies volatility as a function of price history. We first use an empirical implied-index proxy: a constant plus a trend feature plus the square root of an activity feature. This is distinct from specifying a continuous-time instantaneous-volatility pricing model. <bookmark mark='a'/> Trend weights past returns; activity weights past squared returns. Here the most recent included return is from the same day as the target index close. <bookmark mark='b'/> Shifted power-law weights are bounded at zero and can decay slowly over a finite window. A high reconstruction R squared does not prove that all volatility innovations are absent or that the index is forecastable before that day's return is observed."""
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
        vr = data_range(dv, sig)
        g2 = axes([0, n], list(vr), x_length=7.6, y_length=2.4, xlabel=r"days", ylabel=r"implied volatility",
                  xticks=[0, 100, 200], yticks=[0.4, 0.6, 0.8], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=14)
        VGroup(g1, g2).arrange(DOWN, buff=0.45).to_edge(LEFT, buff=0.5)
        t = ValueTracker(1)
        lp = tracing(g1.ax, x, price, t, WHITE, stroke_width=2)
        ld = tracing(g2.ax, x, dv, t, IV, stroke_width=2)
        ls = tracing(g2.ax, x, sig, t, MODEL_COL["PDV"], stroke_width=2.4)
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
        src = real_data('bitcoin 2024; frozen 2021--2023 fit; includes same-day return')
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
                cmath(r"R_t", r"=", r"(1 - \theta)R^{(0)}_t + \theta R^{(1)}_t,\qquad dR^{(j)}_t = \lambda_j\big(r_t^n/\Delta t - R^{(j)}_t\big)dt",
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
            wrapped_label('Nutz--Riveros Valdevenito (2024): global strong 4-factor SDE solution in the stated parameter domain. Positivity and stock martingality are separate. Andr\\`es--Jourdain (2025): general kernels under integrability, regularity and initial-activity assumptions.',
                          4.6, 17, GREY_A)).to_edge(RIGHT, buff=0.35).shift(DOWN * 1.2)
        better = q["r2_test"] > q["tspl_test"]
        verdict = ("the Markovian version does better out of sample than the power-law kernels it replaces"
                   if better else "the Markovian version gives up a little out of sample, in exchange for being Markov")
        with self.voiceover(
            f"There is a Markovian version. Make each kernel a convex mix of two exponentials. <bookmark mark='a'/> Then each memory is a blend of two exponential moving averages, and the model has four factors, each updated by one line: the House's code is exactly that. <bookmark mark='b'/> Fitted the same way on Bitcoin: the activity memory splits into a fast factor of {hl[2]:.0f} days and a slow one of {hl[3]:.0f}. Out of sample it explains {100 * q['r2_test']:.0f} percent of DVOL, against {100 * q['tspl_test']:.0f} for the power law: {verdict}. <bookmark mark='c'/> Is it a well-defined stochastic differential equation? Marcel Nutz and Andrés Riveros Valdevenito proved it is, and Hervé Andrès and Benjamin Jourdain extended that to general kernels. The displayed EMA is a daily data filter. The continuous feedback SDE theorem has a specified sign and parameter domain, positive initial activity, and separate questions of volatility positivity and stock martingality. Our unconstrained empirical regression does not verify those conditions."
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
        vr = data_range(vol, pred, base)
        g = axes([2021.25, 2026], list(vr), x_length=8.0, y_length=4.2, ylabel=r"bitcoin's 30-day implied volatility",
                 xticks=[2022, 2023, 2024, 2025], yticks=[0.4, 0.8, 1.2], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        ok = np.isfinite(vol)
        l_v = curve(ax, t[ok], vol[ok], IV, stroke_width=2.4)
        l_p = curve(ax, t[ok], pred[ok], MODEL_COL["PDV"], stroke_width=2.0)
        l_b = curve(ax, t[ok], base[ok], GREY_B, stroke_width=1.6)
        cut = DashedLine(ax.c2p(split, vr[0]), ax.c2p(split, vr[1]), stroke_color=GREY_A, stroke_width=1.5)
        cl = label(r"fitted up to here; after it, out of sample", font_size=16, color=GREY_A).next_to(ax.c2p(split, vr[1]),
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
            wrapped_label('Component standard deviations describe this pooled sample; correlated components do not form an importance decomposition. The trend exponent reaches its bound.', 3.9, 18, GREY_A),
            wrapped_label(rf"activity's memory: a power law shifted by {365 * p['delta2']:.0f} days, exponent "
                          rf"{p['alpha2']:.2f}", 3.9, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)
        src = real_data(r"Deribit DVOL daily; Binance BTCUSDT daily returns since 2018 (kernels need 1{,}000 days of past)")
        with self.voiceover(
            f"""Bitcoin's target is DVOL, a thirty-day implied-volatility index. Fit the kernels and regression on 2021 through 2023, then freeze them for 2024 and 2025. The features include the return on the target day: this is held-out-date tracking, not an advance forecast. <bookmark mark='a'/> Training R squared is {p['r2_train']:.2f}. <bookmark mark='b'/> On later dates it is {p['r2_test']:.2f}; the fitted thirty-day realized-volatility baseline has negative test R squared, measured against that test period's own mean. <bookmark mark='c'/> Over the pooled sample, the activity term has standard deviation {100 * p['contrib']['activity']:.0f} index points and trend {100 * p['contrib']['trend']:.1f}. These correlated component scales are not a causal or incremental variance decomposition. The trend exponent also reaches its search bound. The result describes this fitted proxy and sample, not a general claim that Bitcoin ignores return direction."""
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
