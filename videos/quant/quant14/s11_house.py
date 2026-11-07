from __future__ import annotations

import numpy as np

from videos.quant.quant14.common import axes, data_range, skew_range

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import (BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, VAR, load, pause, real_data)


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        sp = load("calib_speed")
        self.card()
        self.speed(sp)
        self.lineage()
        self.recognition()
        self.short_end()
        self.module(env)

    def card(self):
        c = chapter_card(17, r"What desks use, and the rough lab", r"What runs on a trading desk, and on what evidence?",
                         lit=(2021,), part=PART)
        with self.voiceover("Chapter seventeen. What desks use, and the rough lab."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def speed(self, sp):
        items = [("rBergomi MC", r"rough Bergomi, Monte Carlo (20{,}000 paths)", MODEL_COL["rBergomi"]),
                 ("rough Heston", r"rough Heston, Adams + COS", MODEL_COL["rough Heston"]),
                 ("lifted Heston", r"lifted Heston, 20 factors + COS", VAR),
                 ("neural (Part 17)", r"neural surrogate (Part 17)", QC.HOUSE)]
        vals = np.array([sp[k] for k, _, _ in items])
        lo, hi = np.floor(np.log10(vals.min())) - .3, np.ceil(np.log10(vals.max())) + .3
        g = axes([lo, hi], [-0.5, len(items) - 0.5], x_length=7.0, y_length=3.6, xlabel='seconds per recorded pricing-map evaluation (log); outputs and accuracy differ', xticks=[-3, -2, -1, 0, 1, 2],
                 xfmt=lambda u: {-3: "0.001", -2: "0.01", -1: "0.1", 0: "1", 1: "10", 2: "100"}[int(round(u))], yticks=[],
                 font_size=14).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        t = ValueTracker(0)

        def bars():
            grp = VGroup()
            for i, ((_, nm, c), v) in enumerate(zip(items, vals)):
                y = len(items) - 1 - i
                x = lo + (np.log10(v) - lo) * t.get_value()
                grp.add(Rectangle(width=max(ax.c2p(x, 0)[0] - ax.c2p(lo, 0)[0], 0.01), height=0.45, stroke_width=0,
                                  fill_color=c, fill_opacity=0.85).move_to(ax.c2p((lo + x) / 2, y)))
            return grp

        bb = always_redraw(bars)
        names = VGroup(*[label(nm, font_size=17, color=c).next_to(ax.c2p(lo, len(items) - 1 - i), LEFT, buff=0.15)
                         for i, (_, nm, c) in enumerate(items)])
        nums = VGroup(*[MathTex(f"{v:.3g}" + r"\,\text{s}", font_size=22).next_to(ax.c2p(np.log10(v),
                                                                                       len(items) - 1 - i), RIGHT, buff=0.1)
                        for i, v in enumerate(vals)])
        ratio = sp["rBergomi MC (Part 17)"] / sp["neural (Part 17)"]
        q = pause('Does one fast pricing-map evaluation establish a 5-second calibration?', width=5.4, font_size=21).to_corner(UL, buff=0.35)
        src = real_data('shared-machine illustration; Part 17 neural/MC ratio belongs to its own benchmark; excludes training', corner=DL)
        with self.voiceover(
            f"""These timings compare single pricing-map evaluations, not completed calibrations. The Monte Carlo, fractional-Adams and lifted-Heston calculations also differ in output, discretization and accuracy. Can a five-second recalibration deadline be decided from them alone? <bookmark mark='a'/> No. The original Part seventeen benchmark compares its neural map with the Monte Carlo map it imitates; its measured evaluation ratio is about {ratio:,.0f}. Training is an offline cost, and the surrogate is limited by its training domain and approximation error. Part fourteen's other bars use the recorded implementations on this shared machine. <bookmark mark='b'/> Total calibration time also depends on the number of optimizer evaluations, derivatives, data handling and required accuracy. This illustration motivates faster maps; it does not establish a universal desk deadline or industry adoption rate."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(names), FadeIn(bb), FadeIn(src), FadeIn(q))
            vo.wait_until("a")
            self.play(t.animate.set_value(1.0), run_time=4)
            self.play(FadeIn(nums))
            vo.wait_until("b")
        bb.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def lineage(self):
        cards = VGroup(
            history_card(2018, r"Bayer and Stemper", r"Deep calibration of rough stochastic volatility models: a network "
                         r"learns the model's pricing map offline; calibration then needs no simulation.", color=QC.HOUSE,
                         width=4.2, font_size=18),
            history_card(2021, r"Horvath, Muguruza and Tomas (Quantitative Finance 21(1))", r"Deep learning volatility: "
                         r"the full implied volatility surface of rough Bergomi calibrated in milliseconds; Risk's Rising "
                         r"Star award.", color=QC.HOUSE, width=4.2, font_size=18),
            history_card(2022, r"Rosenbaum and Zhang (Risk)", r"Deep calibration of the quadratic rough Heston model: "
                         r"one network for S\&P 500 and VIX smiles together.", color=QC.HOUSE, width=4.2,
                         font_size=18)).arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to(UP * 0.4)
        arrows = VGroup(*[Arrow(cards[i].get_right(), cards[i + 1].get_left(), buff=0.05, color=GREY_B, stroke_width=3)
                          for i in range(2)])
        hedge = wrapped_label(r"hedging under rough volatility: hedge with the forward variance curve (variance swaps) as "
                              r"instruments, not a spot volatility state (Fukasawa, Horvath and Tankov, \textit{Rough "
                              r"Volatility} ch. 6)", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            """Published work on faster calibration. Bayer and Stemper train a pricing map offline; Horvath, Muguruza and Tomas develop deep calibration, and Rosenbaum and Zhang apply neural methods to quadratic rough Heston and joint SPX/VIX fitting. <bookmark mark='a'/> Surrogates replace repeated numerical pricing within their training domain. <bookmark mark='b'/> Part seventeen implements one original benchmark; its performance is specific to that setup. <bookmark mark='c'/> Forward-variance hedging theory uses instruments spanning relevant curve risks. A finite set of traded variance swaps does not automatically hedge every curve direction or complete the market."""
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(GrowArrow(arrows[0]), FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[1]), FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(hedge))
        self.wait(0.4)
        self.clear_scene()

    def recognition(self):
        a = firm_card(r"Risk Awards 2021", r"Quants of the Year: Jim Gatheral and Mathieu Rosenbaum, for the quadratic rough "
                      r"Heston model and the joint S\&P 500/VIX calibration (Risk, 2020). Gatheral, as reported by Baruch "
                      r"College: ``Rough volatility has finally found acceptance as the right way to model volatility, and "
                      r"people are actually using it in practice.''", source=r"risk.net; newscenter.baruch.cuny.edu",
                      width=6.2, font_size=20)
        b = firm_card(r"Risk Awards 2023", r"Rising Star in quant finance: Sigurd Emil R{\o}mer, whose calibrations of fifteen "
                      r"years of S\&P options found one-factor rough models too weak in the smile's term structure, and "
                      r"classical two-factor volatility enough for S\&P and VIX together.", source=r"riskawards.com; "
                      r"Quantitative Finance 22(10)", width=6.2, font_size=20)
        grid = VGroup(a, b).arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(ORIGIN)
        with self.voiceover(
            "Recognition, from both sides. Risk named Jim Gatheral and Mathieu Rosenbaum its Quants of the Year for "
            "2021, for the quadratic rough Heston model. Gatheral, as Baruch College reported it: rough volatility "
            "has finally found acceptance, and people are actually using it in practice. <bookmark mark='a'/> Two "
            "years later Risk's Rising Star award went to Sigurd Rømer, whose fifteen years of S&P calibrations are "
            "among the strongest evidence that one-factor rough models are not enough. The field rewards both the "
            "idea and its sharpest test."
        ) as vo:
            self.play(FadeIn(a, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(b, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def short_end(self):
        a = firm_card(r"Cboe: VIX1D", r"Launched 24 April 2023: a one-day volatility index, computed from the mid-quotes of "
                      r"P.M.-settled SPX weekly options expiring today and tomorrow, for the growing group of investors "
                      r"trading same-day options.", source=r"Cboe press release, 24 April 2023", width=7.0, font_size=21)
        note_ = wrapped_label('very short expiries demand intraday data, transaction-cost awareness and finite-resolution validation; this part starts near two days', 9.0, 22, GOLD).next_to(a, DOWN, buff=0.4)
        VGroup(a, note_).move_to(ORIGIN)
        with self.voiceover(
            """Cboe launched VIX1D on April twenty-fourth 2023, using short-expiry SPX option mid-quotes. It measures a one-day implied horizon, rather than the local derivative of the smile at zero maturity. <bookmark mark='a'/> These markets make short-horizon modeling practical work. Our Bitcoin data begin near two days and do not settle zero-day behavior. Intraday sampling, spreads, index construction and finite-difference resolution all matter."""
        ) as vo:
            self.play(FadeIn(a, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def module(self, env):
        chart = house_chart(PART, lit=("vol",)).scale(0.5).to_edge(UP, buff=0.15)
        rows = [
            (r"\texttt{rbergomi\_paths}, \texttt{volterra\_riemann}", r"rough Bergomi by the hybrid scheme; the naive scheme"),
            (r"\texttt{rough\_heston\_cf}, \texttt{frac\_riccati}", r"the fractional Riccati equation by Adams; COS prices"),
            (r"\texttt{lifted\_heston\_cf}, \texttt{lift\_weights}", r"the Markovian lift, $N$ factors"),
            (r"\texttt{log\_rv\_scaling}, \texttt{rfsv\_predict}", r"the roughness estimator; the rough forecast"),
            (r"\texttt{fou\_paths}, \texttt{skew\_term\_fit}", r"the bias map's simulator; power law and bounded skew fits"),
            (r"\texttt{fit\_pdv}, \texttt{pdv4\_features}", r"path-dependent volatility, power-law and 4-factor Markovian"),
            (r"\texttt{qrh\_paths}, \texttt{sigvol\_logS}", r"quadratic rough Heston; signature volatility"),
            (r"\texttt{hawkes\_branching\_powerlaw}", r"order flow by branching (in \texttt{sim})"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=17, color=QC.HOUSE), label(b_, font_size=16, color=GREY_A)) for a_, b_ in rows])
        for r_ in tab:
            r_[1].next_to(r_[0], RIGHT, buff=0.3)
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].set_x(tab.get_left()[0] + 6.2 + r_[1].width / 2)
        tab.next_to(chart, DOWN, buff=0.2)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        tab.set_x(0)
        # the scoreboard: each row's winner from the computed numbers
        f = load("rfsv_forecast")
        rb, b2, sg = load("rbergomi"), load("bergomi2f"), load("sigvol")
        pd, p4 = load("pdv"), load("pdv4")
        surf = min([("rough Bergomi", rb["rmse"]), ("two-factor Bergomi", b2["rmse"]), ("signature", sg["rmse_out"])],
                   key=lambda r: r[1])[0]
        fc = "rough" if f["rough_wins"] > 3 else ("HAR" if f["rough_wins"] < 3 else "a tie")
        trk = "4-factor PDV" if p4["r2_test"] > pd["r2_test"] else "power-law PDV"
        board = VGroup(
            label('Qualified comparisons: same-date option fit; retrospective predictor race; same-day return-based index tracking. These do not by themselves certify model adoption.', font_size=18, color=WHITE),
            wrapped_label(r"Rule 14: a new model is adopted only if it beats the simpler one out of sample, on the quantity "
                          r"it is for (prices, hedges or forecasts), with its estimator checked on synthetic data whose "
                          rf"answer is known.  The trial counter still reads {env['trials']}.", 12.6, 19, QC.HOUSE),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"""The lab contains simulators, Riccati solvers, lifts, roughness estimators, return-history filters, transport and signature models. <bookmark mark='a'/> Each has a distinct target and numerical budget. <bookmark mark='b'/> Rule fourteen requires validation against a simpler model on the task it is intended for. The same-date pricing winner is {surf}; the retrospective rough versus HAR winner is {fc}; the held-out-date implied-index tracker is {trk}. Different information sets prevent a single adoption ranking. Fresh seeds are numerical validation, not unseen market data. No strategy trial was added; the part's counter remains {env['trials']}. Next: selected research."""
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.3, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(board))
        self.wait(0.4)
        self.clear_scene()
