from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import PART, load


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        env2 = load("envelope2")
        self.card()
        self.module(env, env2)
        self.lab(load("house_fc"))

    def card(self):
        c = chapter_card(18, r"The volatility forecaster", r"How does the House forecast risk, and keep itself honest?",
                         part=PART)
        with self.voiceover("Chapter eighteen. The volatility forecaster."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def module(self, env, env2):
        chart = house_chart(PART, lit=("data",)).scale(0.5).to_edge(UP, buff=0.15)
        rows = [
            (r"\texttt{realized\_variance}, \texttt{bipower\_variation}, \texttt{signature\_plot}", r"measures from intraday prices"),
            (r"\texttt{two\_scale\_rv}, \texttt{realized\_kernel}, \texttt{bns\_jump\_z}", r"noise-robust measures; the jump test"),
            (r"\texttt{garch\_fit}, \texttt{garch\_t\_fit}, \texttt{news\_impact}, \texttt{nelson\_elog}", r"the GARCH zoo by likelihood"),
            (r"\texttt{dcc\_fit}, \texttt{sv\_qml}", r"dynamic correlation; stochastic volatility"),
            (r"\texttt{har\_fit}, \texttt{har\_cj}, \texttt{forecast}", r"HAR, HARQ, HAR-CJ; the desk's forecast"),
            (r"\texttt{markov\_switching}, \texttt{hamilton\_filter}, \texttt{kalman\_states}", r"hidden regimes and hidden levels"),
            (r"\texttt{ljung\_box}, \texttt{arma\_fit}, \texttt{adf}, \texttt{df\_simulate}", r"identification and unit roots"),
            (r"\texttt{engle\_granger}, \texttt{ecm\_fit}, \texttt{johansen}", r"cointegration"),
            (r"\texttt{qlike}, \texttt{diebold\_mariano}, \texttt{mincer\_zarnowitz}, \texttt{model\_confidence\_set}",
             r"scoring forecasts"),
            (r"\texttt{vol\_target}, \texttt{vra}", r"how the industry uses them"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=18, color=QC.HOUSE), label(b, font_size=17, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 8.4)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.2:
            tab.scale_to_fit_width(13.2)
        rule = wrapped_label(r"Rule 8: every forecast is scored out of sample, against a simple benchmark, with a loss "
                             r"that is robust to noise in what it is judged against. Part 7 registered "
                             rf"{env2['part7_trials']} models; the series' trial counter reads {env2['trials']}.",
                             12.6, 21, QC.HOUSE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The House's data desk now carries a volatility forecaster, the engine the volatility desk will run on "
            "when it opens in Part ten. <bookmark mark='a'/> Measures from intraday prices, corrected for noise, with "
            "a jump test. The GARCH family by likelihood, with fat tails and asymmetry, dynamic correlation and "
            "stochastic volatility. HAR and its cousins. Regimes and the Kalman filter. Identification, unit roots and "
            "cointegration. And the scoring rules, each checked against simulated data with a known answer. "
            "<bookmark mark='b'/> The eighth rule: every forecast is scored out of sample, against a simple "
            "benchmark, with a loss that stays honest when the target is measured with noise. Every model in this "
            f"part was registered before it was scored, {env2['part7_trials']} in all, and the series' trial counter "
            f"now reads {env2['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=6))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def lab(self, h):
        card = lab_card(r"the desk's forecast", [
            "def forecast(rv, horizon=22):",
            "    lrv = np.log(rv)",
            "    fit = har_fit(lrv)                    # log-HAR",
            "    _, y = _har_design(lrv)",
            "    s2 = np.var(y - fit['fitted'])        # log-normal mean",
            "    path, out = list(lrv), []",
            "    for _ in range(horizon):",
            "        nxt = har_predict(fit['beta'], np.array(path))[-1]",
            "        path.append(nxt); out.append(np.exp(nxt + s2 / 2))",
            "    return np.array(out)",
        ], source="explainer/quant/house/vol.py", width=7.4).to_edge(UP, buff=0.4)
        T = list(h["us_T"])
        term = h["us_term"]
        outs = [f">>> forecast(btc_rv)   # on {h['btc_date']}",
                f"Bitcoin: tomorrow {100 * h['btc_next']:.0f}%, next 22 days {100 * h['btc_month']:.0f}% (annualised)",
                ">>> garch_forecast(...)   # US market, the same day",
                "US: " + ", ".join(f"{t}d {100 * v:.1f}%" for t, v in zip(T, term)) + f";  long run {100 * h['us_long']:.1f}%"]
        up = term[-1] > term[0]
        shape = ("rises with the horizon: the market was calmer than its long-run level, and GARCH expects it to "
                 "revert upward." if up else "falls with the horizon: volatility is expected to revert down.")
        with self.voiceover(
            f"Lab. This is how a desk calls it: the forecaster, iterating log-HAR forward with the log-normal correction. "
            f"On the last day of the research window, the thirty-first of December 2020, it says Bitcoin's volatility "
            f"tomorrow is about {100 * h['btc_next']:.0f} percent a year, and {100 * h['btc_month']:.0f} percent over "
            f"the next month. <bookmark mark='a'/> For the American market, GARCH's term structure {shape}"
        ) as vo:
            self.play(FadeIn(card))
            lab_run(self, card, outs[:2], run_time=1.6)
            vo.wait_until("a")
            out2 = VGroup(*[Text(o, font="DejaVu Sans Mono", font_size=19, color=WHITE if i else QC.GAIN)
                            for i, o in enumerate(outs[2:])]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            out2.scale(getattr(card, "text_scale", 1.0)).next_to(card.out, DOWN, buff=0.15).align_to(card.out, LEFT)
            keep_in_frame(out2)
            self.play(AddTextLetterByLetter(out2[0]), run_time=0.6)
            self.play(AddTextLetterByLetter(out2[1]), run_time=1.0)
        self.wait(0.4)
        self.clear_scene()
