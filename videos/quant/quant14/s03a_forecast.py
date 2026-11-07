from __future__ import annotations

import numpy as np

from videos.quant.quant14.common import axes, data_range, skew_range

from explainer.quant import *  # noqa: F403
from explainer.quant.house import rough as R
from videos.quant.quant14.common import BAD, IV, OPT, PART, ROUGH, RV, VAR, illustration, load, pause, real_data


class Forecast(VoiceoverScene):
    def construct(self):
        f = load("rfsv_forecast")
        r = load("roughness")
        self.card()
        self.weights(f, r)
        self.derive()
        self.race(f)
        self.memory()

    def card(self):
        c = chapter_card(4, r"Forecasting with a rough memory", r"What does roughness buy a forecaster?", part=PART)
        with self.voiceover("Chapter four. Forecasting with a rough memory."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def weights(self, f, r):
        H = float(r["H"])
        L = 40
        g = axes([0.5, L + 0.5], [0, 0.5], x_length=9.0, y_length=3.2, xlabel='observation index $j$ (1 = today)',
                 ylabel='normalized daily weight', xticks=[1, 10, 20, 30, 40], yticks=[0, 0.25, 0.5],
                 font_size=15).to_edge(DOWN, buff=0.7).to_edge(LEFT, buff=0.8)
        D = ValueTracker(1.0)

        def bars():
            w = R.rfsv_weights(H, D.get_value(), 250)[:L]
            unit = g.ax.c2p(0, 1)[1] - g.ax.c2p(0, 0)[1]
            return VGroup(*[Rectangle(width=0.16, height=max(v * unit, 0.002), stroke_width=0, fill_color=ROUGH,
                                      fill_opacity=0.85).move_to(g.ax.c2p(j + 1, v / 2))
                            for j, v in enumerate(w)])
        b = always_redraw(bars)
        Dr = readout(r"\text{horizon}\ \Delta =", lambda: D.get_value(), digits=0, font_size=32, color=YELLOW,
                     unit=r"\ \text{d}").next_to(g, UP, buff=0.25).align_to(g, RIGHT)
        har = [0.4, 0.35, 0.25]
        hw = np.array([har[0] * (j == 0) + har[1] / 5 * (j < 5) + har[2] / 22 * (j < 22) for j in range(L)])
        stair = VMobject(stroke_color=VAR, stroke_width=3).set_points_as_corners(
            [g.ax.c2p(j + 0.5 + s, hw[j]) for j in range(L) for s in (0, 1)])
        hl = legend([(ROUGH, 'finite-window rough predictor: $w_j\\propto 1/((j+\\Delta)j^{H+1/2})$'),
                     (VAR, r"HAR's staircase: yesterday, last week, last month (Corsi 2009; Part 7)")],
                    font_size=17).to_corner(UL, buff=0.4)
        q = pause(r"$H = 0.1$. As the horizon grows, does the weight on yesterday rise or fall?", width=5.6,
                  font_size=21).to_corner(UR, buff=0.3)
        src = illustration(rf"$H = {H:.2f}$, bitcoin's measured roughness; HAR coefficients illustrative")
        with self.voiceover(
            """The fractional Brownian benchmark also gives a conditional-mean predictor from its whole past. Here we discretize and normalize its weights over a finite two hundred fifty-day window. Most mass is on recent observations, followed by a decaying tail. <bookmark mark='a'/> As the forecast horizon grows, does the most recent observation gain or lose weight? <bookmark mark='b'/> It loses weight: the predictor spreads further into the past. <bookmark mark='c'/> The illustrative HAR staircase combines today's value, the five-day mean and the twenty-two-day mean. It can approximate a distributed-lag shape. This comparison motivates HAR; it does not prove why HAR performs well in every market."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(b), FadeIn(Dr), FadeIn(hl[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(D.animate.set_value(20.0), run_time=4)
            self.play(D.animate.set_value(1.0), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(stair), FadeIn(hl[1]), FadeOut(q))
        b.clear_updaters()
        Dr.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\log\sigma_t^2", r"=", r"\nu\,W^H_t + c", font_size=40, colors={r"\log\sigma_t^2": RV}),
                cmath(r"\mathbb{E}\big[W^H_{t + \Delta}\,\big|\,\mathcal{F}_t\big]", r"=",
                      r"\frac{\cos(H\pi)}{\pi}\,\Delta^{H + 1/2}\int_{-\infty}^t \frac{W^H_s\,ds}{(t - s + \Delta)(t - s)^{H + 1/2}}",
                      font_size=34, colors={r"\mathbb{E}\big[W^H_{t + \Delta}\,\big|\,\mathcal{F}_t\big]": ROUGH}),
                cmath(r"\int_0^\infty \frac{du}{(u + 1)\,u^{H + 1/2}}", r"=", r"\frac{\pi}{\cos(H\pi)}", font_size=36,
                      colors={r"\int_0^\infty \frac{du}{(u + 1)\,u^{H + 1/2}}": GREY_A}),
                cmath(r"\widehat{\log\sigma^2_{t + \Delta}}", r"=", r"\sum_{j \ge 1} w_j \log\sigma^2_{t + 1 - j},\quad "
                      r"w_j \propto \frac{1}{(j + \Delta)\,j^{H + 1/2}}", font_size=36,
                      colors={r"\widehat{\log\sigma^2_{t + \Delta}}": ROUGH})]
        whys = [why(r"the rough fractional stochastic volatility (RFSV) model: log variance is a fractional Brownian "
                    r"motion, with $W^H$ in Mandelbrot and Van Ness's form (Part 5)"),
                why(r"the conditional mean of fBm given its whole past, $H < \tfrac12$ (Nuzman and Poor 2000, theorem 4.2; "
                    r"Gatheral, Jaisson and Rosenbaum 2018, eq. 5.1)"),
                why(r"substitute $t - s = \Delta u$: the constant makes the weights integrate to one, so the forecast is a "
                    r"weighted average of the past"),
                why(r"discretised on days and normalised: the House's \texttt{rfsv\_predict}")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.0, buff=0.7, edge=6.9)
        with self.voiceover(
            "The formula. In the rough fractional stochastic volatility model, log variance is nu times a fractional "
            "Brownian motion, plus a constant. <bookmark mark='a'/> The expected value of fractional Brownian motion "
            "delta ahead, given its whole past, is an integral of the past against this kernel, with a constant in "
            "front, cosine of H pi over pi. It is a theorem of Carl Nuzman and Vincent Poor, and it is equation "
            "five point one of the roughness paper. <bookmark mark='b'/> Where does that constant come from? "
            "Substitute t minus s equals delta times u: the kernel integrates to pi over cosine H pi, so the "
            "constant simply makes the weights add up to one. The forecast is a weighted average of the past. "
            "<bookmark mark='c'/> On daily data, the integral becomes a sum with these weights, normalised: the "
            "House's function, and the bars you just saw."
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

    def race(self, f):
        e18, e24 = f["2018-2020"], f["2024-2025"]
        models = ["rough", "HAR", "AR(1)", "last value"]
        cols = {"rough": ROUGH, "HAR": VAR, "AR(1)": IV, "last value": GREY_B}
        s = e18["series"]
        n = len(s["y"])
        x = np.arange(n)
        y, pr, ph = (np.asarray(s[k]) for k in ("y", "rough", "HAR"))
        lo, hi = data_range(y, pr, ph)
        g = axes([0, n], [lo, hi], x_length=6.4, y_length=2.6, ylabel=r"log realized variance, 5 days ahead",
                 xticks=[], yticks=[], font_size=14).to_corner(UL, buff=0.4).shift(DOWN * 0.2)
        tr = ValueTracker(0)
        ly = tracing(g.ax, x, y, tr, GREY_B, stroke_width=1.2)
        lr = tracing(g.ax, x, pr, tr, ROUGH, stroke_width=2)
        lh = tracing(g.ax, x, ph, tr, VAR, stroke_width=1.6)
        leg = legend([(GREY_B, 'realized (2018--2020 test dates)'), (ROUGH, r"rough forecast"), (VAR, r"HAR")],
                     font_size=15).next_to(g, DOWN, buff=0.15).align_to(g, LEFT)
        head = VGroup(label(r"", font_size=18), *[label(m_, font_size=17, color=cols[m_]) for m_ in models])
        rows = [head]
        for era, e in (("2018--20", e18), ("2024--25", e24)):
            for D in ("1", "5", "20"):
                best = max(models, key=lambda m_: e[D]["r2"][m_])
                rows.append([label(rf"{era}, {D} d", font_size=17, color=GREY_A)] +
                            [MathTex(f"{e[D]['r2'][m_]:.2f}", font_size=22,
                                     color=YELLOW if m_ == best else WHITE) for m_ in models])
        grid = VGroup(*[c for r_ in rows for c in r_]).arrange_in_grid(rows=len(rows), cols=5, buff=(0.32, 0.16),
                                                                         col_alignments="lcccc")
        cap = label('retrospective $R^2$; coefficients refit every 20 days; full-era $H$; test-mean denominator', font_size=16,
                    color=GREY_A)
        tab = VGroup(cap, grid).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.2)
        if tab.width > 6.4:
            tab.scale_to_fit_width(6.4)
        # four out-of-sample blocks, each model's R^2: the spread of the race
        bg = axes([0.5, 4.5], [-0.6, 0.8], x_length=5.6, y_length=2.2, xlabel=r"test block (2018--2020, 5 days ahead)",
                  xticks=[1, 2, 3, 4], yticks=[-0.5, 0, 0.5], font_size=13).to_corner(DL, buff=0.45)
        blines = VGroup(*[curve(bg.ax, np.arange(1, 5), e18["5"]["blocks"][m_], cols[m_],
                                stroke_width=2.5) for m_ in models])
        src = real_data('BTCUSDT realized variance; coefficients use known targets, but $H$ uses each full era',
                        corner=DR)
        with self.voiceover(
            f"""A retrospective comparison across two Bitcoin eras, at one, five and twenty days ahead. Regression coefficients are refitted every twenty days using targets already observed. But the rough predictor's H is estimated from the entire era, including its test dates. This is not a fully real-time forecast test. <bookmark mark='a'/> The plot shows the five-day comparison in the older era, with all observed values and predictions preserved. <bookmark mark='b'/> Across six horizon-era pairs, the rough version beats HAR in {f['rough_wins']} and HAR in {6 - f['rough_wins']}. Scores divide squared errors by variation around the test period's own mean, an unavailable future benchmark at prediction time. At twenty days all four scores are negative. <bookmark mark='c'/> The four chronological blocks show unstable rankings. These data support a comparison of fitted predictor shapes, without a demonstrated deployable advantage or a statistical superiority test."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(ly), FadeIn(lr), FadeIn(lh), FadeIn(src))
            vo.wait_until("a")
            self.play(tr.animate.set_value(n - 1), run_time=6, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(bg), LaggedStart(*[Create(l_) for l_ in blines], lag_ratio=0.2))
        for m_ in (ly, lr, lh):
            m_.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def memory(self):
        a = history_card(1998, r"Comte and Renault: long memory in continuous-time stochastic volatility",
                         '$H>1/2$: persistent fractional increments and long-range dependence; paths remain nondifferentiable.',
                         color=VAR, width=6.2, font_size=21)
        b = history_card(2018, r"Gatheral, Jaisson and Rosenbaum: volatility is rough",
                         '$H<1/2$: rough local paths and antipersistent fBm increments; a predictor can still use distant past levels.',
                         color=ROUGH, width=6.2, font_size=21)
        grid = VGroup(a, b).arrange(RIGHT, buff=0.4, aligned_edge=UP).move_to(UP * 0.4)
        note_ = wrapped_label('Local regularity, long-range dependence and predictive memory require distinct assumptions.', 11.0, 22, GREY_A).next_to(grid, DOWN, buff=0.45)
        with self.voiceover(
            """A distinction about memory. Comte and Renault used fractional volatility with H above one half to represent long-range dependence. Such fractional Brownian paths remain nondifferentiable. <bookmark mark='a'/> H below one half instead describes rougher paths and negatively correlated fractional Brownian increments. The predictor still uses a tail of past levels. That tail is not the conventional long-range dependence of positively correlated increments with H above one half. Local roughness, stationary long memory and forecast persistence are separate properties. Next: rough Bergomi for option prices."""
        ) as vo:
            self.play(FadeIn(a, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(b, shift=UP * 0.2), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()
