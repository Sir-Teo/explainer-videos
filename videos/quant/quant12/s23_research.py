from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SIM, SPOT, load

N_COL = {"0.002": RV, "0.01": IV, "0.05": BAD}


class Research(VoiceoverScene):
    def construct(self):
        t = load("density_theory")
        self.card()
        self.error()
        self.optimum()
        self.mse_plot(t)
        self.rate(t)
        self.btc(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Reading the density from noisy prices", r"How accurately can option prices tell you the "
                          r"market's distribution?", part=PART)
        with self.voiceover("For the researcher: Part 9 showed that butterflies, divided by the square of their width, "
                            "converge to the risk-neutral density. That limit assumes exact prices. Real prices carry "
                            "errors, and a second derivative magnifies them. Here is exactly how much, and the width "
                            "that balances the two errors."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def error(self):
        rows = [cmath(r"\hat q_h(K)", r"=", r"\frac{\tilde C(K - h) - 2\tilde C(K) + \tilde C(K + h)}{h^2},\quad \tilde C = C + "
                      r"\eta,\ \ \eta \sim (0, s^2)", font_size=30, colors={r"\hat q_h(K)": SIM}),
                cmath(r"\mathbb E\,\hat q_h - q", r"=", r"\frac{h^2}{12}\,q''(K) + O(h^4)", font_size=32,
                      colors={r"\mathbb E\,\hat q_h - q": LV}),
                cmath(r"\operatorname{Var}\hat q_h", r"=", r"\frac{(1 + 4 + 1)\,s^2}{h^4} = \frac{6s^2}{h^4}", font_size=32,
                      colors={r"\operatorname{Var}\hat q_h": BAD})]
        whys = [why(r"zero rates; the butterfly of width $h$ on prices observed with independent errors of size $s$"),
                why(r"Taylor: $C(K \pm h) = C \pm hC' + \frac{h^2}{2}C'' \pm \frac{h^3}{6}C''' + \frac{h^4}{24}C''''$, and "
                    r"$C'' = q$, so the even terms leave $q + \frac{h^2}{12}q''$: a wide butterfly blurs the density"),
                why(r"the weights are $1, -2, 1$, divided by $h^2$: the error is amplified by $h^{-2}$, its variance by "
                    r"$h^{-4}$. A narrow butterfly reads noise")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Take the butterfly estimate. <bookmark mark='a'/> Three call prices at strikes h apart, each observed with "
            "an independent error of size s, combined with weights one, minus two, one, over h squared. "
            "<bookmark mark='b'/> Expand the prices in a Taylor series. The odd terms cancel, and since the second "
            "derivative of the call is the density, what remains is the density plus h squared over twelve times its "
            "second derivative. A wide butterfly blurs the density. <bookmark mark='c'/> And the errors: weights one, "
            "four and one in the variance, divided by h to the fourth. A narrow butterfly reads mostly noise."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def optimum(self):
        rows = [cmath(r"\operatorname{MSE}(h)", r"=", r"\frac{h^4}{144}\,q''^2 + \frac{6s^2}{h^4}", font_size=32,
                      colors={r"\operatorname{MSE}(h)": OPT}),
                cmath(r"h^*", r"=", r"\Big(\frac{864\,s^2}{q''^2}\Big)^{1/8}", font_size=34, colors={r"h^*": SIM}),
                cmath(r"\operatorname{MSE}(h^*)", r"=", r"\frac{2\sqrt6}{12}\,|q''|\,s\quad\Rightarrow\quad "
                      r"\operatorname{RMSE} \propto s^{1/2}", font_size=30, colors={r"\operatorname{MSE}(h^*)": BAD})]
        whys = [why(r"squared bias plus variance"),
                why(r"setting the derivative to zero balances the two: $h^8 = 864s^2/q''^2$"),
                why(r"at the optimum the two terms are equal; the error falls only like the square root of the noise. "
                    r"Halving the price errors improves the density by about 30\%, not 50\%: the price of a second "
                    r"derivative, as in nonparametric statistics")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "So there is a best width. <bookmark mark='a'/> The mean squared error is the squared bias, growing like h "
            "to the fourth, plus the variance, shrinking like h to the minus four. <bookmark mark='b'/> Balance them: "
            "the best width is the eighth root of eight hundred and sixty-four s squared over the density's curvature "
            "squared. <bookmark mark='c'/> At that width the two terms are equal, and the error falls only like the "
            "square root of the noise. Halve the errors in prices, and the density improves by about thirty percent, "
            "not fifty. That is the price of a second derivative, as every nonparametric statistician knows."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def mse_plot(self, t):
        a = t["at"]["atm"]
        h = np.asarray(t["h"], float)
        g = axes([-0.7, 1.05], [-4.0, 0.5], x_length=8.0, y_length=4.2, xlabel=r"butterfly half-width $h$, \% of the forward",
                 ylabel=r"root mean squared error of $\hat q_h$ at the money (log scale)",
                 xticks=[np.log10(0.25), 0.0, np.log10(3), 1.0], yticks=[-4, -3, -2, -1, 0],
                 xfmt=lambda v: f"{10 ** v:g}", yfmt=lambda v: f"10^{{{int(v)}}}", font_size=15,
                 log_x=True).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        lines, dots, stars = VGroup(), VGroup(), VGroup()
        xs = np.log10(h)
        for s_, r in a["noise"].items():
            col = N_COL[s_]
            lines.add(curve(ax, xs, np.log10(np.sqrt(np.asarray(r["mse_th"]))), col, stroke_width=3))
            sel = np.arange(0, len(h), 3)
            dots.add(VGroup(*[Dot(ax.c2p(xs[j], np.log10(np.sqrt(r["mse_sim"][j]))), radius=0.05, color=col) for j in sel]))
            stars.add(Star(n=5, outer_radius=0.12, color=col, fill_opacity=1).move_to(
                ax.c2p(np.log10(r["h_star"]), np.log10(r["rmse_star"]))))
        qline = DashedLine(ax.c2p(-0.7, np.log10(a["q"])), ax.c2p(1.05, np.log10(a["q"])), color=GREY_B, stroke_width=1.5)
        qlab = label(r"the density itself", font_size=15, color=GREY_B).next_to(ax.c2p(-0.7, np.log10(a["q"])), UR, buff=0.06)
        leg = legend([(N_COL[k], rf"price error $s = {k}$ per 100") for k in a["noise"]], font_size=16).to_edge(
            RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"a lognormal at {100 * t['sigma']:.0f}\% volatility, 30 days; lines: the formula, dots: "
                             r"4{,}000 noisy draws per width, stars: $h^*$. Above the dashed line the estimate is "
                             r"larger than the thing it estimates", 3.3, 14, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        r1 = a["noise"]["0.01"]
        with self.voiceover(
            "Simulate it: a lognormal at sixty percent volatility, thirty days, the butterfly at the money. "
            "<bookmark mark='a'/> With price errors of two thousandths of a percent of the forward, the error falls steeply "
            "as the butterfly widens, then rises again once the bias takes over. <bookmark mark='b'/> With larger "
            "errors the whole curve moves up and the best width moves right. <bookmark mark='c'/> The stars mark the "
            f"formula's best width: at a price error of a hundredth of a percent, {r1['h_star']:.1f} percent of the forward, "
            f"and the simulation's best is {r1['h_best_sim']:.1f}. Narrower than that, and the estimate is mostly noise: "
            "at the tightest widths, larger than the density it estimates."
        ) as vo:
            self.play(FadeIn(g), Create(qline), FadeIn(qlab), FadeIn(side))
            for k, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                if k == 0:
                    self.play(Create(lines[0]), FadeIn(dots[0]), FadeIn(leg[0]), run_time=1.3)
                else:
                    self.play(Create(lines[1]), FadeIn(dots[1]), FadeIn(leg[1]), Create(lines[2]), FadeIn(dots[2]),
                              FadeIn(leg[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(stars))
        self.wait(0.4)
        self.clear_scene()

    def rate(self, t):
        hx = [-3.6, -0.6, 1.6, 3.8, 5.8]
        head = VGroup(label(r"price error $s$, per 100", font_size=18, color=GREY_B), label(r"$h^*$, formula", font_size=20),
                      label(r"$h^*$, simulated", font_size=20), label(r"RMSE at $h^*$", font_size=20),
                      label(r"relative", font_size=20))
        a = t["at"]["atm"]
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(MathTex(k, font_size=26, color=N_COL[k]),
                                                 MathTex(rf"{r['h_star']:.1f}\%", font_size=26),
                                                 MathTex(rf"{r['h_best_sim']:.1f}\%", font_size=26),
                                                 MathTex(rf"{1e4 * r['rmse_star']:.1f}\times 10^{{-4}}", font_size=26),
                                                 MathTex(rf"{100 * r['rmse_star'] / a['q']:.1f}\%", font_size=26))
                                          for k, r in a["noise"].items()]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.5 - 0.75 * j, 0])
            tab.add(row)
        foot = wrapped_label(r"at the money; the simulated best is the best of the widths tried (a grid of 0.25\%). Each "
                             r"fivefold increase in the noise multiplies the best error by $\sqrt5 \approx 2.24$; the "
                             r"same holds in the put wing at 85", 11.6, 16, GREY_A).to_edge(DOWN, buff=0.6)
        rs = [r["rmse_star"] for r in a["noise"].values()]
        with self.voiceover(
            "The numbers. <bookmark mark='a'/> The best widths from the formula and from the simulation agree, to "
            "within the grid of widths tried. <bookmark mark='b'/> And the best error, relative to the density: one "
            "percent at the smallest noise, then a little over two, then about five. Each fivefold rise in the "
            f"noise multiplies it by {rs[1] / rs[0]:.2f}: the square root of five."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1], r_[2])) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[3], r_[4])) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def btc(self, t):
        b = t["btc"]
        sd_adj = np.sqrt(6) * b["noise_sd"] / b["strike_spacing_pct"] ** 2
        sd_b = b["atm_iv"] * np.sqrt(30 / 365)
        q_atm = 1 / (100 * sd_b * np.sqrt(2 * np.pi))
        rows = [(r"trades, 20--45 days, within 15\% of spot", rf"{b['n_trades']:,}".replace(",", "{,}")),
                (r"trade price $-$ mark price: robust s.d., per 100 of the forward", rf"{b['noise_sd']:.3f}"),
                (r"listed strike spacing near the money", rf"{b['strike_spacing_pct']:.2f}\%"),
                (r"at-the-money volatility, 30 days (the Surface)", rf"{100 * b['atm_iv']:.0f}\%"),
                (r"best half-width $h^*$", rf"{b['h_star']:.1f}\%"),
                (r"noise alone with adjacent strikes, relative to the density", rf"\pm{100 * sd_adj / q_atm:.0f}\%")]
        tab = VGroup()
        for j, (a_, v) in enumerate(rows):
            r_ = VGroup(label(a_, font_size=19, color=GREY_A), MathTex(v, font_size=28, color=IV if j >= 4 else WHITE))
            r_[0].move_to([-1.6, 2.2 - 0.62 * j, 0]).align_to(np.array([-6.4, 0, 0]), LEFT)
            r_[1].move_to([5.2, 2.2 - 0.62 * j, 0])
            tab.add(r_)
        foot = wrapped_label(r"Deribit BTC options on the Surface's two days, 10 and 11 December 2025; each trade's price "
                             r"against Deribit's mark price at that moment, both in BTC per BTC. The mark is itself a "
                             r"smoothed model, which is why densities built from marks and fits (Part 9) look clean", 11.8, 16,
                             GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "How noisy are real prices? Take every Bitcoin option trade on the Surface's two days with a month or so "
            "to run. <bookmark mark='a'/> Against Deribit's own mark price at that moment, trades scatter by about "
            f"{b['noise_sd']:.3f} per hundred of the forward. <bookmark mark='b'/> Listed strikes sit about one percent "
            f"apart. But at forty-six percent volatility the best butterfly is {b['h_star']:.0f} percent wide: eight "
            "strikes on each side, not one. <bookmark mark='c'/> Built from adjacent strikes, the density from trades "
            f"would carry noise of plus or minus {100 * sd_adj / q_atm:.0f} percent of itself. Every clean density you "
            "have seen from such data was smoothed, by a model, a fit or the exchange's mark; the smoothing is the "
            "estimate's real content."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]), FadeIn(tab[4]))
            vo.wait_until("c")
            self.play(FadeIn(tab[5]))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: shape constraints and optimal rates", r"densities are non-negative and integrate to one; "
                          r"estimators that impose no-arbitrage shapes (A\"it-Sahalia and Duarte 2003) beat raw butterflies, "
                          r"but optimal rates under realistic, correlated quote errors are not settled", width=12.4,
                          font_size=18),
            desk_question(r"open: errors that are not independent", r"bid--ask bounce, stale quotes and a common forward "
                          r"error correlate across strikes; a common error cancels in a butterfly, a stale one does not",
                          width=12.4, font_size=18),
            desk_question(r"open: inference on the tails", r"the tails, where crash probabilities live, have few quotes and "
                          r"wide spreads; confidence bands for tail probabilities from option prices are rarely reported",
                          width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> Densities are non-negative and integrate to one. Estimators "
            "that impose those shapes beat raw butterflies, but optimal rates with realistic quote errors are not "
            "settled. <bookmark mark='b'/> Real errors are not independent: bid-ask bounce, stale quotes and a common "
            "error in the forward correlate across strikes. A common error cancels in a butterfly; a stale one does "
            "not. <bookmark mark='c'/> And in the tails, where crash probabilities live, quotes are few and spreads "
            "wide: confidence bands for tail probabilities read from options are rarely reported at all."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a new data feed cuts price errors by a factor of 16. By what factor do the best butterfly width and "
                       r"the best density error change?")
        with self.voiceover(
            "Pause and predict. A better data feed cuts price errors sixteenfold. By what factor do the best butterfly "
            "width, and the best density error, change?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
