from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data, tbar, predict


class Har(VoiceoverScene):
    def construct(self):
        s = load("signature")
        h = load("har")
        hr = load("har_roll")
        self.card()
        self.jumps(s)
        self.cascade(h, hr)
        self.lab(h, hr)
        self.harq(h, hr)

    def card(self):
        c = chapter_card(10, r"Jumps and HAR", r"Which past predicts tomorrow?", lit=(2003,), part=PART)
        with self.voiceover("Chapter ten. Jumps, and the HAR model."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def jumps(self, s):
        rng = np.random.default_rng(12)
        r = 0.6 * rng.standard_normal(24)
        r[13] += 4.2
        x0, w = -6.3, 0.32  # the bars keep to the left two-thirds; the formulas take the right
        base = 0.6
        sq = VGroup(*[Square(side_length=max(abs(v) * 0.3, 0.01), stroke_width=1, stroke_color=RET, fill_color=RET,
                             fill_opacity=0.5).move_to([x0 + w * i, base + abs(v) * 0.15, 0]) for i, v in enumerate(r)])
        rect = VGroup(*[Rectangle(width=max(abs(r[i - 1]) * 0.3, 0.01), height=max(abs(r[i]) * 0.3, 0.01), stroke_width=1,
                                  stroke_color=ALT, fill_color=ALT, fill_opacity=0.5).move_to([x0 + w * i, base - 2.4 + abs(r[i]) * 0.15, 0])
                        for i in range(1, len(r))])
        l1 = label(r"RV: squares $r_i^2$; the jump is one giant square", font_size=20, color=RET).move_to([-3.2, 2.9, 0])
        l2 = label(r"BV: rectangles $|r_i|\,|r_{i-1}|$; the jump is paired with a small neighbour", font_size=20,
                   color=ALT).move_to([-3.2, -2.2, 0])
        rows = [
            cmath(r"BV", r"=", r"\tfrac{\pi}{2}\sum|r_i||r_{i-1}| \to \int\sigma^2", font_size=30),
            cmath(r"RV - BV", r"\to", r"\textstyle\sum_{s\le 1}J_s^2", font_size=30),
            cmath(r"z", r"=", r"\frac{(RV - BV)/RV}{\sqrt{(\tfrac{\pi^2}{4} + \pi - 5)\tfrac1n\max(1, TQ/BV^2)}}", font_size=30),
        ]
        whys = [why(r"noise-free limit with isolated finite-activity jumps; $\mathbb{E}|z|=\sqrt{2/\pi}$", font_size=19),
                why(r"the jumps' contribution", font_size=19),
                why(r"Barndorff-Nielsen and Shephard (2006): $N(0,1)$ without jumps", font_size=19)]
        grp = VGroup(*[VGroup(r_, w_).arrange(DOWN, aligned_edge=LEFT, buff=0.08) for r_, w_ in zip(rows, whys)])
        grp.arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        if grp.width > 5.3:
            grp.scale_to_fit_width(5.3).to_edge(RIGHT, buff=0.3)
        res = VGroup(
            MathTex(rf"\text{{nominal jump detections at }}1\%: {100 * s['jump_share_1pct']:.0f}\%", font_size=26, color=BAD),
            MathTex(rf"\text{{at }}0.1\%: {100 * s['jump_share_01pct']:.0f}\%", font_size=26, color=BAD),
            MathTex(rf"\text{{12 March 2020: }} z = {s['z_0312']:.2f}", font_size=26, color=VOL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DR, buff=0.35)
        storm = s["z_0312"] < 2.326
        verdict = ("The nominal test does not detect a jump. That does not prove there were no jumps; finite sampling and noise matter."
                   if storm else "The nominal test rejects the continuous-path null, subject to its assumptions.")
        with self.voiceover(
            f"Realized variance counts jumps too: one sudden move, one giant square. Ole Barndorff-Nielsen and Neil Shephard "
            f"found a measure that ignores it. <bookmark mark='a'/> Instead of squaring each return, multiply its size "
            f"by its neighbour's. A jump is paired with an ordinary neighbour, so its rectangle stays thin: bipower variation "
            f"converges to the continuous part alone, and the difference from realized variance is the jumps. <bookmark "
            f"mark='b'/> Their 2006 test turns the difference into a z-score. <bookmark mark='c'/> On Bitcoin's five-minute "
            f"returns, {100 * s['jump_share_1pct']:.0f} percent of days show a jump at the one percent level. And the "
            f"twelfth of March 2020? z is {s['z_0312']:.2f}. {verdict}"
        ) as vo:
            self.play(FadeIn(l1), LaggedStart(*[GrowFromEdge(q, DOWN) for q in sq], lag_ratio=0.05, run_time=2))
            vo.wait_until("a")
            self.play(FadeIn(l2), LaggedStart(*[GrowFromEdge(q, DOWN) for q in rect], lag_ratio=0.05, run_time=2))
            self.play(Indicate(sq[13], color=BAD), Indicate(VGroup(rect[12], rect[13]), color=ALT))
            self.play(FadeIn(grp[0]), FadeIn(grp[1]))
            vo.wait_until("b")
            self.play(FadeIn(grp[2]))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    def cascade(self, h, hr):
        eq = MathTex(r"RV_{t+1}", r"=", r"b_0", r"+ b_d\,RV_t", r"+ b_w\,\overline{RV}_{t-4:t}", r"+ b_m\,\overline{RV}_{t-21:t}",
                     font_size=34).to_edge(UP, buff=0.45)
        eq[3].set_color(BAD)
        eq[4].set_color(RET)
        eq[5].set_color(GOOD)
        tt = np.asarray(h["cascade_t"])
        g = axes([2019, 2020], [0, 2.7], x_length=6.0, y_length=3.0, ylabel=r"Bitcoin's volatility in 2019",
                 xticks=[2019, 2019.5, 2020], xfmt=lambda u: {2019: "Jan", 2019.5: "Jul", 2020: "Jan"}[round(u * 2) / 2],
                 yticks=[0, 1.0, 2.0], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15).to_corner(DL, buff=0.45)
        ax = g.ax
        cd = curve(ax, tt, h["cascade_d"], BAD, stroke_width=1.2).set_stroke(opacity=0.7)
        cw = curve(ax, tt, h["cascade_w"], RET, stroke_width=2.5)
        cm = curve(ax, tt, h["cascade_m"], GOOD, stroke_width=4)
        lags = np.arange(1, 23)
        hw, gw = np.asarray(hr["har_w"]), np.asarray(hr["garch_w"])
        g2 = axes([0, 23], [0, 0.45], x_length=5.6, y_length=2.6, xticks=[1, 5, 22], yticks=[0, 0.2, 0.4],
                  xlabel=r"lag (days)", ylabel=r"weight on $RV_{t-k+1}$", font_size=15).to_corner(UR, buff=0.45).shift(DOWN * 0.9)
        st = VGroup(*[Rectangle(width=0.18, height=max(g2.ax.c2p(0, v)[1] - g2.ax.c2p(0, 0)[1], 0.003), stroke_width=0,
                                fill_color=VOL, fill_opacity=0.85).move_to(g2.ax.c2p(k, v / 2)) for k, v in zip(lags, hw)])
        gl = curve(g2.ax, lags, gw, FC, stroke_width=3)
        leg = legend([(VOL, r"HAR's implied AR(22): a staircase"), (FC, r"GARCH-style: geometric decay")], font_size=17)
        leg.next_to(g2, DOWN, buff=0.15).align_to(g2, LEFT)
        lag = np.asarray(hr["lags"])
        e, ha, a1 = (np.asarray(hr[k]) for k in ("acf_emp", "acf_har", "acf_ar1"))
        g3 = axes([0, 2.05], [-0.05, 1.0], x_length=5.0, y_length=2.4, log_x=True, xticks=[0, 1, 2], yticks=[0, 0.5, 1],
                  xlabel=r"lag (days, log scale)", ylabel=r"autocorrelation of log RV", font_size=14)
        g3.move_to(g2)
        c_e = VGroup(*[Dot(g3.ax.c2p(np.log10(L), v), radius=0.035, color=WHITE) for L, v in zip(lag, e)])
        c_h = curve(g3.ax, np.log10(lag), ha, VOL, stroke_width=3)
        c_a = curve(g3.ax, np.log10(lag), np.maximum(a1, -0.05), FC, stroke_width=3)
        leg3 = legend([(WHITE, r"Bitcoin"), (VOL, r"fitted log-HAR, simulated"), (FC, r"AR(1), same lag-1")], font_size=17)
        leg3.next_to(g3, DOWN, buff=0.15).align_to(g3, LEFT)
        with self.voiceover(
            """With a measured variance every day, forecasting becomes a regression. Corsi's HAR uses yesterday and trailing five- and twenty-two-observation averages. Those are stock-market trading-week and month conventions; Bitcoin trades every calendar day. <bookmark mark='a'/> The averages move at different speeds. <bookmark mark='b'/> Expanding them gives an AR-twenty-two with tied staircase weights. <bookmark mark='c'/> The fitted log-HAR can mimic slow sample autocorrelation decay over these horizons; it does not establish true power-law memory."""
        ) as vo:
            self.play(FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(cd), Create(cw), Create(cm), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(g2), LaggedStart(*[GrowFromEdge(b, DOWN) for b in st], lag_ratio=0.08), FadeIn(leg[0]))
            self.play(Create(gl), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(FadeOut(VGroup(g2, st, gl, leg)), FadeIn(g3), FadeIn(c_e), FadeIn(leg3))
            self.play(Create(c_h), Create(c_a), run_time=2)
        self.wait(0.3)
        self.clear_scene()

    def lab(self, h, hr):
        card = lab_card(r"HAR by least squares", [
            "def har_fit(rv):",
            "    d = rv[21:-1]",
            "    w = [rv[t-4:t+1].mean() for t in range(21, len(rv)-1)]",
            "    m = [rv[t-21:t+1].mean() for t in range(21, len(rv)-1)]",
            "    X = np.column_stack([np.ones(len(d)), d, w, m])",
            "    beta, *_ = np.linalg.lstsq(X, rv[22:], rcond=None)",
            "    return beta",
        ], source="explainer/quant/house/vol.py", width=6.6).to_corner(UL, buff=0.3)
        b, t = h["HAR"]["beta"], h["HAR"]["t"]
        rb = np.asarray(hr["roll_b"])
        rt = np.asarray(hr["roll_t"])
        g = axes([0, 3], [-0.2, 0.7], x_length=4.4, y_length=3.2, xticks=[], yticks=[0, 0.3, 0.6], font_size=15,
                 ylabel=r"rolling 252-day coefficients").to_corner(DR, buff=0.6)
        k = ValueTracker(0)
        cols = (BAD, RET, GOOD)
        bars = always_redraw(lambda: VGroup(*[tbar(g.ax, j + 0.5, float(rb[int(k.get_value())][j + 1]), cols[j], width=0.6)
                                              for j in range(3)]))
        names = VGroup(*[MathTex(n_, font_size=26, color=c_).next_to(g.ax.c2p(j + 0.5, -0.2), DOWN, buff=0.1)
                         for j, (n_, c_) in enumerate(((r"b_d", BAD), (r"b_w", RET), (r"b_m", GOOD)))])
        date = always_redraw(lambda: MathTex(rf"\text{{window ending }} {rt[int(k.get_value())]:.2f}", font_size=24,
                                             color=GREY_A).next_to(g, UP, buff=0.15))
        with self.voiceover(
            "Lab. The House's HAR: three columns, the day, the week's average and the month's, and least squares. "
            "<bookmark mark='a'/> Fitted on Bitcoin through 2019, yesterday and the month carry the weight: "
            f"{b[1]:.2f} and {b[3]:.2f}, with the week near zero, and an R squared of {h['HAR']['r2']:.2f}. "
            "<bookmark mark='b'/> But are the coefficients stable? Refit on 252 rolling Bitcoin observations, about eight months, and watch them as the "
            "window slides from 2018 to the end of 2020. Yesterday's weight stays near a half, but the week and the "
            "month trade places: this short window has difficulty distinguishing them, because the two averages move together."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, [f"b0 = {b[0]:.1e}  bd = {b[1]:.2f}  bw = {b[2]:.2f}  bm = {b[3]:.2f}",
                                 f"Newey-West t: {t[1]:.1f}, {t[2]:.1f}, {t[3]:.1f};  R2 = {h['HAR']['r2']:.2f}"], run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(names))
            self.add(bars, date)
            self.play(k.animate.set_value(len(rt) - 1), run_time=max(vo.remaining(1.0) - 0.3, 4), rate_func=linear)
        bars.clear_updaters()
        date.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def harq(self, h, hr):
        rows = [
            cmath(r"RV_t", r"=", r"IV_t + u_t,\quad \operatorname{Var}u_t \approx 2\,IQ_t/n", font_size=34),
            cmath(r"b_{eff}", r"=", r"b\,\frac{\operatorname{Var}IV}{\operatorname{Var}IV + \operatorname{Var}u}", font_size=34),
            cmath(r"b_{d,t}", r"=", r"b_d + b_q\sqrt{RQ_t}", font_size=34),
        ]
        whys = [why(r"the measurement error of the last chapter's CLT"),
                why('scalar classical independent measurement error: attenuation illustration, not the exact multivariate HAR formula'),
                why(r"HARQ (Bollerslev, Patton and Quaedvlieg 2016): trust yesterday less when it was noisy; $b_q < 0$")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-2.4, buff=0.55, edge=6.9)
        bq, tq = h["HARQ"]["beta"], h["HARQ"]["t"]
        cj = np.asarray(hr["cj"])
        lh = np.asarray(hr["loghar"])
        side = VGroup(
            MathTex(rf"\text{{HARQ on Bitcoin: }} b_q = {bq[4]:.1f}\ \ (t = {tq[4]:.1f})", font_size=28, color=ALT),
            MathTex(rf"\text{{HAR-CJ: jump part }} b_J = {cj[4]:.2f}", font_size=28, color=BAD),
            MathTex(rf"\text{{log-HAR: }} b_d = {lh[1]:.2f},\ b_w = {lh[2]:.2f},\ b_m = {lh[3]:.2f}", font_size=28, color=GOOD),
            wrapped_label(r"HAR-CJ (Andersen, Bollerslev and Diebold 2007) gives the continuous and the jump parts their "
                          r"own coefficients; log-HAR fits the logarithm, which tames the spikes", 11.0, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        pc = predict(r"If yesterday's RV was measured very noisily, should HAR trust it more or less?", width=5.4,
                        font_size=21).to_corner(UR, buff=0.3)
        sig = abs(tq[4]) > 2
        verdict = ("and on Bitcoin it is significant." if sig else
                   "the sign is right, but on three years of Bitcoin it is not significant.")
        with self.voiceover(
            f"""Pause and predict: if yesterday's realized variance is noisy, should the model trust it less? <bookmark mark='a'/> Quarticity helps estimate measurement uncertainty. <bookmark mark='b'/> Scalar classical independent measurement error gives attenuation; this is not an exact multivariate HAR law. <bookmark mark='c'/> HARQ lets the daily coefficient adjust with quarticity. Here it is negative but weakly estimated, {verdict} <bookmark mark='d'/> HAR-CJ treats jumps separately, and log-HAR fits logs. Next: roughness."""
        ) as vo:
            self.play(FadeIn(pc))
            vo.wait_until("a")
            self.play(FadeOut(pc))
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(FadeIn(side[0]))
            vo.wait_until("d")
            self.play(FadeIn(side[1:]))
        self.wait(0.3)
        self.clear_scene()
