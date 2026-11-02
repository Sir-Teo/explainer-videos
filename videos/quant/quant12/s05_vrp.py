from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, load, real_data


def _t(s):
    d = date.fromisoformat(s)
    return d.year + (d.timetuple().tm_yday - 1) / 365


class VRP(VoiceoverScene):
    def construct(self):
        h = load("history")
        self.card()
        self.series(h)
        self.svix(h)

    def card(self):
        c = chapter_card(5, r"The variance risk premium, measured", r"Why is implied above realized on average?", part=PART)
        with self.voiceover("Chapter five. The variance risk premium, measured."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def series(self, h):
        rows = h["rows"]
        t = np.array([_t(r["day"]) for r in rows])
        kv = np.sqrt(np.array([r["kvar"] for r in rows]))
        rv = np.sqrt(np.array([r["rv"] if r["rv"] is not None and np.isfinite(r["rv"]) else np.nan for r in rows]))
        g = axes([2024, 2026], [0.2, 1.0], x_length=7.6, y_length=4.2, ylabel=r"30-day bitcoin volatility",
                 xticks=[2024, 2024.5, 2025, 2025.5, 2026], xfmt=lambda u: {0: "Jan 24", 1: "Jul 24", 2: "Jan 25", 3: "Jul 25",
                                                                              4: "Jan 26"}[round((u - 2024) * 2)],
                 yticks=[0.2, 0.4, 0.6, 0.8, 1.0], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        ok = np.isfinite(rv)
        lk = curve(ax, t, np.clip(kv, 0.2, 1.0), IV, stroke_width=3)
        lr = curve(ax, t[ok], np.clip(rv[ok], 0.2, 1.0), RV, stroke_width=2.5)
        leg = legend([(IV, r"variance-swap rate, from each week's surface"), (RV, r"realized over the next 30 days")],
                     font_size=18).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = VGroup(
            MathTex(rf"{100 * h['kvar_vol_mean']:.0f}\% \ \text{{implied vs}}\ {100 * h['rv_vol_mean']:.0f}\%\ \text{{realized}}",
                    font_size=30),
            label(rf"the premium was positive in {100 * h['share_positive']:.0f}\% of {h['n']} weeks", font_size=22,
                  color=IV),
            MathTex(rf"t = {h['vrp_t']:.1f}\ \ (\text{{Newey--West}})", font_size=30, color=OPT),
            wrapped_label(r"Carr and Wu (2009) measured it on stocks: investors pay to be long variance, because variance "
                          r"spikes when wealth falls; Bollerslev, Tauchen and Zhou (2009) found it predicts stock returns",
                          4.2, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = real_data(r"weekly surfaces from Deribit trades, January 2024 -- November 2025; Binance BTCUSDT hourly")
        with self.voiceover(
            "The desk question: why is implied volatility above realized on average? Measure it. Every Wednesday for "
            "two years, the House built a surface from that morning's Deribit trades and read off the thirty-day "
            "variance-swap rate. <bookmark mark='a'/> Then it measured the variance Bitcoin actually realized over the "
            f"next thirty days. On average, implied {100 * h['kvar_vol_mean']:.0f} percent, realized "
            f"{100 * h['rv_vol_mean']:.0f}. <bookmark mark='b'/> The premium was positive in "
            f"{100 * h['share_positive']:.0f} percent of weeks, with a t-statistic of {h['vrp_t']:.1f} once the "
            "overlap of the windows is accounted for. Peter Carr and Liuren Wu measured the same premium on stocks in "
            "2009. Investors pay to own variance because variance spikes exactly when wealth falls: it is insurance, "
            "and insurance costs more than its expected payout."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg[0]), Create(lk), run_time=2)
            vo.wait_until("a")
            self.play(Create(lr), FadeIn(leg[1]), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def svix(self, h):
        rows = [cmath(r"\mathbb{E}_t[R_{T}] - R_f", r"\ge", r"\frac{1}{R_f}\,\text{var}^Q_t(R_T) = R_f\,\text{SVIX}^2_t",
                      font_size=36, colors={r"\mathbb{E}_t[R_{T}] - R_f": OPT})]
        whys = [why(r"Martin (2017): if the market's return is negatively correlated with the discount factor, the "
                    r"risk-neutral variance, read from options, is a lower bound on the expected excess return")]
        step = ladder(self, rows, whys, keep=1, top=2.6, x=-0.6, buff=0.8, edge=6.9)
        notes = VGroup(
            wrapped_label(r"for the S\&P 500 the bound averaged about 5\% a year, and it surged in crises: expected "
                          r"returns rise when options are dear", 11.0, 21, GREY_A),
            wrapped_label(rf"for bitcoin, from the same weekly surfaces, the bound averages {100 * h['svix_bound_mean']:.0f}\% "
                          r"a year; it holds only if bitcoin is the kind of asset whose falls coincide with bad times for its "
                          r"marginal investor, which is an assumption, not a fact", 11.0, 21, IV),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Option prices can say something about expected returns, too. Ian Martin showed in 2017 that, under a mild "
            "condition, the risk-neutral variance of the market's return, read straight from options, is a lower bound "
            "on its expected excess return. <bookmark mark='a'/> For the S&P 500 the bound has averaged about five "
            "percent a year, and it surges in crises. For Bitcoin, the same weekly surfaces give a bound averaging "
            f"{100 * h['svix_bound_mean']:.0f} percent a year, but only if Bitcoin's falls come in bad times for whoever "
            "holds it. That is an assumption, not a measurement."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n_) for n_ in notes], lag_ratio=0.5, run_time=3))
        self.wait(0.4)
        self.clear_scene()
