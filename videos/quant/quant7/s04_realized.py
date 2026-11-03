from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data, tbar


class Realized(VoiceoverScene):
    def construct(self):
        z = load("realized")
        s = load("signature")
        self.card()
        self.squares(s)
        self.signature(s)
        self.derive(s)
        self.measures(z, s)

    def card(self):
        c = chapter_card(9, r"Realized volatility", r"Can you measure volatility after the fact?", lit=(2003,), part=PART)
        with self.voiceover("Chapter nine. Realized volatility."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def squares(self, s):
        x = np.asarray(s["examples"]["20190626"])
        n = len(x)
        g = axes([0, 24], [-0.02, 0.2], x_length=11.0, y_length=2.6, xticks=[0, 6, 12, 18, 24],
                 xfmt=lambda u: f"{int(u):02d}{{:}}00", yticks=[0, 0.1, 0.2], yfmt=lambda u: f"{100 * u:+.0f}\\%" if u else "0",
                 ylabel=r"Bitcoin on 26 June 2019: log price since midnight (UTC), one-minute closes", font_size=15)
        g.to_edge(UP, buff=0.5)
        ax = g.ax
        hrs = np.arange(n) / 60
        path = curve(ax, hrs, x, RET, stroke_width=2)
        base_y = -2.0
        side_scale = 9.0  # screen units per unit of log return

        def row(k, col):
            r = np.diff(x[::k])
            sq = VGroup()
            xx = -5.5
            width = 11.0
            for i, v in enumerate(r):
                a = abs(v) * side_scale
                sq.add(Square(side_length=max(a, 0.004), stroke_width=0.6, stroke_color=col, fill_color=col,
                              fill_opacity=0.5).move_to([xx + width * (i + 0.5) / len(r), base_y + a / 2, 0]))
            return sq, float(np.sqrt(np.sum(r ** 2) * 365))

        rows = [row(k, c) for k, c in ((30, VOL), (10, FC), (5, GOOD), (1, BAD))]
        base = Line([-5.6, base_y, 0], [5.6, base_y, 0], color=GREY_C, stroke_width=2)
        ro = MathTex(rf"\textstyle\sum r_i^2:\ {100 * rows[0][1]:.0f}\%\text{{ a year}}", font_size=34, color=VOL).to_edge(DOWN, buff=0.4)
        cap = label(r"each square: one interval's return, squared (side $|r_i|$, area $r_i^2$)", font_size=19,
                    color=GREY_A).next_to(base, DOWN, buff=0.15)
        names = [r"every 30 minutes", r"every 10 minutes", r"every 5 minutes", r"every minute"]
        nm = label(names[0], font_size=24, color=VOL).next_to(ro, UP, buff=0.15)
        with self.voiceover(
            "Can volatility be measured after the fact? Here is one wild day of Bitcoin, minute by minute: the "
            "twenty-sixth of June 2019. <bookmark mark='a'/> Cut the day "
            "into half-hours. Each half-hour's return gets a square, with side the size of the move and area its "
            "square. Add up the areas: that is realized variance. <bookmark mark='b'/> Cut finer, ten minutes, five "
            "minutes: the squares multiply six-fold and shrink, while their total moves far less. <bookmark mark='c'/> In the limit "
            "it is the quadratic variation of Part five, the integral of the instantaneous variance over the day. "
            "Andersen, Bollerslev, Diebold and Labys built on this around 2000: volatility becomes observable. <bookmark mark='d'/> At every minute, though, "
            "the total creeps up again. Why?"
        ) as vo:
            self.play(FadeIn(g), Create(path), run_time=2)
            vo.wait_until("a")
            self.play(Create(base), FadeIn(cap), LaggedStart(*[FadeIn(q) for q in rows[0][0]], lag_ratio=0.03, run_time=2),
                      FadeIn(ro), FadeIn(nm))
            vo.wait_until("b")
            cur = rows[0][0]
            for k in (1, 2):
                r2 = MathTex(rf"\textstyle\sum r_i^2:\ {100 * rows[k][1]:.0f}\%\text{{ a year}}", font_size=34,
                             color=[VOL, FC, GOOD, BAD][k]).move_to(ro)
                self.play(ReplacementTransform(cur, rows[k][0]), Transform(ro, r2),
                          Transform(nm, label(names[k], font_size=24, color=[VOL, FC, GOOD, BAD][k]).move_to(nm)), run_time=1.5)
                cur = rows[k][0]
            vo.wait_until("d")
            r2 = MathTex(rf"\textstyle\sum r_i^2:\ {100 * rows[3][1]:.0f}\%\text{{ a year}}", font_size=34, color=BAD).move_to(ro)
            self.play(ReplacementTransform(cur, rows[3][0]), Transform(ro, r2),
                      Transform(nm, label(names[3], font_size=24, color=BAD).move_to(nm)), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    def signature(self, s):
        steps = np.asarray(s["steps"], float)
        s19, sall = np.asarray(s["sig_2019"]), np.asarray(s["sig_all"])
        lo = float(min(s19.min(), sall.min())) - 0.05
        hi = float(max(s19.max(), sall.max())) + 0.05
        g = axes([0, 62], [lo, hi], x_length=6.2, y_length=4.4, xticks=[1, 5, 10, 15, 20, 30, 60],
                 yticks=[round(v, 1) for v in np.arange(np.ceil(lo * 10) / 10, hi, 0.1)], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 xlabel=r"sampling interval $\Delta$ (minutes)", ylabel=r"average realized volatility, annualised",
                 font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        k = ValueTracker(0)
        dots = always_redraw(lambda: VGroup(*[Dot(ax.c2p(steps[i], s19[i]), radius=0.08, color=GOOD)
                                               for i in range(len(steps) - 1, len(steps) - 2 - int(k.get_value()), -1)]))
        l19 = curve(ax, steps, s19, GOOD, stroke_width=3)
        lall = curve(ax, steps, sall, ALT, stroke_width=3)
        leg = legend([(GOOD, r"2019"), (ALT, r"Aug.\ 2017 -- 2020")], font_size=19).next_to(g, UP, buff=0.1).align_to(g, RIGHT)
        rise = s19[0] / s19[3] - 1
        rise_all = sall[0] / sall[3] - 1
        side = VGroup(
            wrapped_label(r"the signature plot (Andersen, Bollerslev, Diebold and Labys 2000)", 5.2, 19, GREY_A),
            MathTex(rf"\text{{2019: }}1\text{{ min }} {100 * s19[0]:.0f}\%,\ 5\text{{ min }} {100 * s19[3]:.0f}\%,\ "
                    rf"60\text{{ min }} {100 * s19[-1]:.0f}\%", font_size=26, color=GOOD),
            MathTex(rf"\text{{whole sample: }}{100 * sall[0]:.0f}\%,\ {100 * sall[3]:.0f}\%,\ {100 * sall[-1]:.0f}\%",
                    font_size=26, color=ALT),
            wrapped_label(rf"noise variance per minute $\hat\eta^2 = RV_{{1}}/2n$: median ${s['eta2_median'] * 1e8:.0f}\times 10^{{-8}}$",
                          5.2, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        pc = pause_card(r"Sampling every second gives 86{,}400 returns a day. Better than every 5 minutes?", width=5.2,
                        font_size=21).next_to(side, DOWN, buff=0.3).align_to(side, LEFT)
        with self.voiceover(
            "Build the answer point by point. For every day of 2019, compute realized volatility at a sampling "
            "interval of an hour, then thirty minutes, and so on down to one minute, and average. <bookmark mark='a'/> "
            f"The line rises as the interval shrinks: in 2019, one-minute sampling reads {100 * rise:.1f} percent more "
            "than five-minute sampling. <bookmark mark='b'/> Over the whole sample, with the thinner markets of 2017 and "
            f"2018, the gap is {100 * rise_all:.0f} percent. The culprit is microstructure noise: trades bounce between "
            "the bid and the ask, and every bounce adds a little square that has nothing to do with volatility."
            " <bookmark mark='c'/> Pause and predict: is sampling every "
            "second better? No: the more often you sample, the more bounces you add up."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            self.add(dots)
            self.play(k.animate.set_value(len(steps) - 1), run_time=3, rate_func=linear)
            vo.wait_until("a")
            self.play(Create(l19), FadeIn(side[1]), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(lall), FadeIn(leg[1]), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(pc))
        dots.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def derive(self, s):
        rows = [
            cmath(r"RV_n = \sum_{i=1}^n r_i^2", r"\to", r"\int_0^1\sigma_s^2\,ds = IV", font_size=34),
            cmath(r"\sqrt{n}\,(RV_n - IV)", r"\Rightarrow", r"MN\Big(0,\ 2\int_0^1\sigma_s^4\,ds\Big),\quad "
                  r"\widehat{IQ} = \tfrac{n}{3}\sum r_i^4", font_size=34),
            cmath(r"r_i = r_i^* + u_i - u_{i-1}", r"\Rightarrow", r"\mathbb{E}RV_n = IV + 2n\eta^2", font_size=34),
            cmath(r"MSE(n) \approx 4n^2\eta^4 + \frac{2\,IQ}{n}", r"\Rightarrow", r"n^* = \Big(\frac{IQ}{4\eta^4}\Big)^{1/3}",
                  font_size=34),
            cmath(r"TSRV", r"=", r"\overline{RV}^{(K)} - \frac{\bar n}{n}RV^{(all)}", font_size=34),
            cmath(r"RK", r"=", r"\gamma_0 + \sum_{h=1}^{H}k\Big(\frac{h}{H+1}\Big)(\gamma_h + \gamma_{-h})", font_size=34),
        ]
        whys = [why(r"quadratic variation (Part 5): the squares converge to the integrated variance"),
                why(r"Barndorff-Nielsen and Shephard (2002): an error band from the realized quarticity"),
                why(r"iid noise $u$ of variance $\eta^2$: each return gains $2\eta^2$, cross terms vanish"),
                why(r"bias squared plus variance, set the derivative to zero (Bandi and Russell 2008)"),
                why(r"Zhang, Mykland and A\"it-Sahalia (2005): average $K$ sparse grids, subtract the noise from the dense one"),
                why(r"Barndorff-Nielsen, Hansen, Lunde and Shephard (2008): add back the noise's autocovariances")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-1.8, buff=0.5, edge=6.9)
        q = np.asarray(s["nstar_min_q"])
        res = MathTex(rf"\text{{Bitcoin, per day: }} n^* \Rightarrow \Delta^* \approx {s['nstar_min_median']:.0f}\text{{ minutes "
                      rf"(median; quartiles }}{q[0]:.0f}\text{{--}}{q[1]:.0f})", font_size=28, color=GOOD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The theory. The sum of squares converges to the integrated variance, <bookmark "
            "mark='a'/> with an error, derived by Barndorff-Nielsen and Shephard in 2002, that shrinks like one over "
            "root n and is estimated from fourth powers. <bookmark "
            "mark='b'/> Now add noise to every observed price. Each observed return gains the difference of two noise "
            "terms, and summing n squares adds two n times the noise variance: a bias that grows with n. <bookmark "
            "mark='c'/> Bias against error: minimising the sum gives an optimal number of samples, Federico Bandi and "
            f"Jeffrey Russell's rule. For Bitcoin it says sample about every {s['nstar_min_median']:.0f} minutes. "
            "<bookmark mark='d'/> Or keep all the data and remove the bias: the two-scale estimator averages several "
            "sparse grids and subtracts the noise measured on the dense one, <bookmark mark='e'/> and the realized "
            "kernel adds back the autocovariances the noise creates. Pre-averaging, spot volatility and irregular "
            "sampling extend these ideas."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            self.play(FadeIn(res))
            vo.wait_until("d")
            step(4)
            vo.wait_until("e")
            step(5)
        self.wait(0.3)
        self.clear_scene()

    def measures(self, z, s):
        names = [("vol_rv1", r"RV,\\1-minute", BAD), ("vol_rv5", r"RV,\\5-minute", RET), ("vol_tsrv", r"two-scale\\RV", VOL),
                 ("vol_rk", r"realized\\kernel", VOL), ("vol_bv", r"bipower\\(no jumps)", ALT)]
        g = axes([0, len(names)], [0, 1.2], x_length=6.0, y_length=3.4, ylabel=r"Bitcoin's average volatility, Aug.\ 2017 -- 2020",
                 xticks=[], yticks=[0, 0.4, 0.8, 1.2], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16)
        g.to_corner(UL, buff=0.5).shift(DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[tbar(ax, i + 0.5, z[k], c, width=0.55) for i, (k, _, c) in enumerate(names)])
        vals = VGroup(*[MathTex(f"{100 * z[k]:.0f}\\%", font_size=22, color=c).next_to(b, UP, buff=0.06)
                        for (k, _, c), b in zip(names, bars)])
        labs = VGroup(*[Tex(r"\begin{tabular}{c}" + n_ + r"\end{tabular}", font_size=15,
                            color=GREY_A).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.1) for i, (_, n_, _) in enumerate(names)])
        t, rv, se = (np.asarray(s[k]) for k in ("clt_t", "clt_rv", "clt_se"))
        vol, lo, hi = (np.sqrt(np.maximum(v, 1e-12) * 365) for v in (rv, rv - 1.96 * se, rv + 1.96 * se))
        g2 = axes([2019, 2020], [0, 2.0], x_length=6.0, y_length=3.0, xticks=[2019, 2019.5, 2020],
                  xfmt=lambda u: {2019: "Jan", 2019.5: "Jul", 2020: "Jan"}[round(u * 2) / 2], yticks=[0, 1, 2],
                  yfmt=lambda u: f"{100 * u:.0f}\\%", ylabel=r"2019, each day: RV with its 95\% band (BNS)", font_size=15)
        g2.to_corner(UR, buff=0.5).shift(DOWN * 0.2)
        bd = band(g2.ax, t, np.clip(lo, 0, 2), np.clip(hi, 0, 2), VOL, 0.3)
        ln = curve(g2.ax, t, np.clip(vol, 0, 2), VOL, stroke_width=1.6)
        rel = float(np.median(1.96 * se / rv))
        src = real_data(rf"Binance BTCUSDT one-minute candles; {z['n_days']:,} days".replace(",", "{,}"))
        with self.voiceover(
            "On three and a half years of Bitcoin: one-minute sums give an average volatility of "
            f"{100 * z['vol_rv1']:.0f} percent, five-minute sums {100 * z['vol_rv5']:.0f}. <bookmark mark='a'/> The two "
            f"noise-corrected estimators, using every minute, land near {100 * z['vol_tsrv']:.0f}. Bipower variation, next chapter, is lower still. <bookmark mark='b'/> And each day's measure "
            "comes with an error band from the central limit theorem: with five-minute returns, the half-width is "
            f"typically {100 * rel:.0f} percent of the variance. Realized variance is a measurement, not the truth, and "
            "that will matter when forecasts are scored against it."
            " Next: the simplest model built on that measurement, and still one of the strongest."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(labs), *[GrowFromEdge(b, DOWN) for b in bars[:2]], FadeIn(vals[:2]))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(b, DOWN) for b in bars[2:]], FadeIn(vals[2:]))
            vo.wait_until("b")
            self.play(FadeIn(g2), FadeIn(bd), Create(ln), run_time=2)
        self.wait(0.3)
        self.clear_scene()
