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
        self.rule()

    def card(self):
        c = chapter_card(18, r"The volatility forecaster", r"How does the House forecast risk, and keep itself honest?",
                         part=PART)
        with self.voiceover("Chapter eighteen. The volatility forecaster."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def module(self, env, env2):
        chart = house_chart(PART, lit=("data",)).scale(0.5).to_edge(UP, buff=0.15)
        rows = [
            ("realized_variance, bipower_variation", r"measures from intraday prices"),
            ("two_scale_rv, realized_kernel", r"noise-robust measures; the jump test"),
            ("garch_fit, garch_t_fit", r"the GARCH zoo by likelihood"),
            ("dcc_fit, sv_qml", r"dynamic correlation; stochastic volatility"),
            ("har_fit, forecast", r"HAR, HARQ, HAR-CJ; the desk's forecast"),
            ("markov_switching, kalman_states", r"hidden regimes and hidden levels"),
            ("arma_fit, adf", r"identification and unit roots"),
            ("engle_granger, johansen", r"cointegration"),
            ("qlike, diebold_mariano", r"scoring forecasts"),
            ("vol_target, vra", r"how the industry uses them"),
        ]
        tab = VGroup(*[VGroup(data_text(a, font="DejaVu Sans Mono", font_size=18, color=QC.HOUSE),
                              label(b, font_size=18, color=GREY_A)).arrange(RIGHT, buff=0.4)
                       for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 7.8)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.2:
            tab.scale_to_fit_width(13.2)
        rule = wrapped_label(
            f"Rule 8 is prospective; this reused 2020 comparison is exploratory. Part 7: {env2['part7_trials']} "
            f"registrations; {env2['trials']} trials through this part.", 12.6, 21, QC.HOUSE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"""The House's data desk now carries a volatility forecaster. <bookmark mark='a'/> Intraday measures, noise corrections, GARCH, stochastic volatility, HAR, hidden states, cointegration and scoring tools. <bookmark mark='b'/> Rule eight is the prospective standard. This 2020 comparison was reused, with later entrants recorded; it was not wholly prospective. The registry counts {env2['part7_trials']} trials here, and {env2['trials']} through this part. The separate 2021-onward holdout remains sealed."""
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
            f"Lab. This is how a desk calls it: a recursive plug-in log-HAR illustration with a constant residual-variance correction, not exact multi-step lognormal moments. "
            f"On the last day of the research window, the thirty-first of December 2020, it says Bitcoin's volatility "
            f"tomorrow is about {100 * h['btc_next']:.0f} percent a year, and {100 * h['btc_month']:.0f} percent over "
            f"the next 22 Bitcoin calendar days, as annualized RMS volatility. <bookmark mark='a'/> For the American market, GARCH's term structure {shape}"
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

    def rule(self):
        items = [
            (r"out of sample", r"prospective goal: untouched test data; this reused 2020 comparison is exploratory"),
            (r"against a benchmark", r"HAR and log-HAR: four coefficients that any new model must beat"),
            (r"with a robust loss", r"QLIKE ranking robustness needs a positive conditionally unbiased variance proxy"),
            (r"with a test", r"DM under its conditions; nested models may need CW; joint inference needs care"),
            (r"registered", r"every model counted by the trial counter before its score is seen"),
        ]
        rows = VGroup(*[VGroup(label(a, font_size=26, color=QC.HOUSE), label(b, font_size=21, color=GREY_A))
                        .arrange(DOWN, aligned_edge=LEFT, buff=0.08) for a, b in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Rule 8, in five parts", font_size=34).to_edge(UP, buff=0.5)
        rows.next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            """Rule eight, unpacked, as the prospective standard. Keep evaluation data untouched while choosing models, compare with simple benchmarks, and use loss and inference appropriate to the proxy and nesting. <bookmark mark='a'/> This chapter's 2020 comparison was reused and later entrants counted, so its rankings are exploratory. QLIKE robustness requires a positive conditionally unbiased variance proxy. DM and the confidence set have regularity conditions; nested squared-error comparisons may need Clark--West. Registrations expose search history, and the separate 2021-onward holdout stays sealed."""
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_) for r_ in rows[:2]], lag_ratio=0.4))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[2:]], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()
