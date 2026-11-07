from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, load, pause, real_data, tbar


def _year(ts):
    d = datetime.fromtimestamp(ts, tz=timezone.utc)
    return d.year + (d.timetuple().tm_yday - 1) / 365


class VRP(VoiceoverScene):
    def construct(self):
        e = load("edge")
        env = load("envelope")
        self.card()
        self.series(e)
        self.result(e, env)
        self.cross_section()
        self.kelly(load("kelly"))

    def card(self):
        c = chapter_card(7, r"Forecast diagnostics, and how much to bet", r"When is implied volatility too high?",
                         part=PART)
        with self.voiceover("""Chapter seven. Forecast diagnostics, and how much to bet."""):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def series(self, e):
        t = np.array([_year(x) for x in e["t"]])
        iv, fv, rv = (np.asarray(e[k], float) for k in ("iv", "fvol", "rv"))
        ymax = max(1.6, float(np.ceil(max(iv.max(), fv.max(), rv.max()) * 5) / 5))
        g = axes([2022, 2026], [0, ymax], x_length=8.4, y_length=4.2, ylabel=r"bitcoin volatility, annualised",
                 xticks=[2022, 2023, 2024, 2025, 2026], xfmt=lambda u: f"{int(u)}", yticks=[0, 0.4, 0.8, 1.2, 1.6],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        tr = ValueTracker(0.0)
        li = tracing(ax, t, iv, tr, VEGA, stroke_width=3)
        lf = curve(ax, t, fv, ALT, stroke_width=2.5)
        lr = curve(ax, t, rv, GAMMA, stroke_width=1.5).set_stroke(opacity=0.7)
        leg = legend([(VEGA, r"model input: entry-day DVOL proxy"), (ALT, r"HAR diagnostic: includes entry-day variance"),
                      (GAMMA, r"realized over the next 30 days")], font_size=18).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = VGroup(
            wrapped_label(r"Part 10: hypothetical DVOL-priced dollar-call windows had a positive sample mean and a fat loss tail", 3.8, 20, GREY_A),
            wrapped_label(r"Sinclair's rule: sell only when implied is above your own forecast of what will be "
                          r"realized", 3.8, 20, ALT),
            wrapped_label(r"cached HAR: past-only fits, but full entry-day variance enters its next-day forecast; used as a monthly proxy", 3.8, 20, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Deribit DVOL and Binance BTCUSDT hourly, 2021--2025")
        with self.voiceover(
            """Chapter six measured a historical premium. Part ten's hypothetical dollar calls used DVOL as a pricing proxy and hourly spot hedges; they were not executable Deribit trades. <bookmark mark='a'/> A seller might compare implied volatility with a forecast. Here the HAR coefficients are refitted weekly using earlier days, but the cached input includes the full entry calendar day's variance, including hours after the eight a.m. entry. It is a next-day forecast reused as a monthly proxy. This is a retrospective diagnostic, not an available-at-entry signal. <bookmark mark='b'/> The green curve is realized volatility over the following month, aligned to each window's start. Spikes still matter, but this comparison cannot establish a tradable forecasting edge."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]), FadeIn(leg[0]))
            self.add(li)
            self.play(tr.animate.set_value(len(t) - 1), run_time=max(vo.until("a") - 0.2, 1.0), rate_func=linear)
            vo.wait_until("a")
            self.play(Create(lf), FadeIn(leg[1]), FadeIn(side[1]), FadeIn(side[2]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lr), FadeIn(leg[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def result(self, e, env):
        g = axes([0, 2], [-0.5, 2.5], x_length=4.6, y_length=4.0, ylabel=r"average P\&L of a month, per 100 of bitcoin",
                 xticks=[], yticks=[-0.5, 0, 0.5, 1, 1.5, 2, 2.5], font_size=17).to_edge(LEFT, buff=1.0).shift(DOWN * 0.2)
        ax = g.ax
        vals = [(e["nonoverlap_on"], e["se_on"], ALT, r"implied $>$ forecast", e["n_on"]),
                (e["nonoverlap_off"], e["se_off"], GREY_B, r"implied $\le$ forecast", e["n_off"])]
        objs = VGroup()
        for i, (m, se, c, lab, n) in enumerate(vals):
            b = tbar(ax, i + 0.5, m, c, width=0.55)
            err = Line(ax.c2p(i + 0.5, m - 2 * se), ax.c2p(i + 0.5, m + 2 * se), color=WHITE, stroke_width=2)
            txt = wrapped_label(lab + f" ({n} months)", 1.9, 18, GREY_A).next_to(ax.c2p(i + 0.5, -0.5), DOWN, buff=0.12)
            objs.add(VGroup(b, err, txt))
        diff = e["nonoverlap_on"] - e["nonoverlap_off"]
        se_d = float(np.hypot(e["se_on"], e["se_off"]))
        side = VGroup(
            label(r"retrospective diagnostic split, disjoint windows:", font_size=22, color=GREY_A),
            MathTex(rf"{e['nonoverlap_on']:.2f}\ \ \text{{vs}}\ \ {e['nonoverlap_off']:.2f}", font_size=34),
            MathTex(rf"\text{{difference }} {diff:.2f},\ \ t \approx {diff / se_d:.1f}", font_size=30, color=ALT),
            wrapped_label(rf"one existing logged specification; the as-of-chapter trial counter reads {env['trials']}. A $t$ of "
                          r"two on a few dozen months is a reason to keep watching, not to lever up (Part 6)", 4.6, 20,
                          GREY_A),
            wrapped_label(r"bars: two ordinary standard errors; disjoint windows can still be dependent; timing leakage prevents a trading interpretation",
                          4.6, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            f"""Split disjoint thirty-day windows by the cached diagnostic. When DVOL exceeded it, the hypothetical short call earned {e['nonoverlap_on']:.2f} per hundred of Bitcoin; otherwise, {e['nonoverlap_off']:.2f}. <bookmark mark='a'/> The difference divided by the ordinary standard error is about {diff / se_d:.1f}. Disjoint windows do not imply independence, and the entry-day timing leakage prevents calling this a trading test. <bookmark mark='b'/> The code specification exists in the registry; that record alone does not prove it preceded calculation. The chapter counter is {env['trials']}. Neither registration nor this t-statistic repairs unavailable information."""
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[FadeIn(o) for o in objs], lag_ratio=0.4), FadeIn(side[0]),
                      FadeIn(side[1]), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[2]), FadeIn(side[4]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def cross_section(self):
        card = theorem_card(r"Goyal and Saretto (2009)", r"Sort US stocks each month on historical minus implied "
                            r"volatility. Buying straddles on the stocks whose implied is far below their own history, "
                            r"and selling them where it is far above, earned large average returns, 1996--2006: the "
                            r"forecaster's edge, across a cross-section of stocks.",
                            who=r"\textit{Cross-section of option returns and volatility}, JFE", color=QC.IDEA, width=7.4,
                            font_size=22).to_edge(LEFT, buff=0.6)
        side = VGroup(
            wrapped_label(r"one asset through time (this chapter) against thousands of stocks at once: the same idea, "
                          r"with many more assets, whose returns can still be correlated", 4.4, 21, GREY_A),
            wrapped_label(r"Part 25 asks how many such sorts survive once you count everything that was tried", 4.4, 20,
                          ALT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "With one asset, this sample has only a few dozen disjoint months; they need not be independent. The same idea across thousands of "
            "stocks gives far more. Amit Goyal and Alessio Saretto sorted American stocks every month on their "
            "historical volatility minus their implied volatility, and traded straddles on the extremes: long where "
            "implied was far below the stock's own history, short where it was far above. <bookmark mark='a'/> From "
            "1996 to 2006 the spread earned large average returns. Part twenty-five asks how many such sorts survive "
            "once you count every sort that was tried."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def kelly(self, k):
        f, gg = np.asarray(k["f"]), np.asarray(k["g"])
        top = float(gg.max())
        xmax = max(k["f_gauss"], k["f_ruin"]) * 1.1
        g = axes([0, xmax], [-0.1, top * 1.3], x_length=7.0, y_length=4.0, xlabel=r"leverage $f$ (notional per unit of "
                 r"capital)", ylabel=r"sample mean log growth per 30-day window, $g(f)$", xticks=[0, 10, 20, 30, 40, 50],
                 yticks=[0, round(top, 2)], font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        ax = g.ax
        line = curve(ax, f, gg, OPT, stroke_width=3.5)
        wall = DashedLine(ax.c2p(k["f_ruin"], -0.1), ax.c2p(k["f_ruin"], top * 1.3), color=QC.LOSS, stroke_width=3)
        walll = label(rf"sample ruin wall: $1/|x_{{\min}}| = {k['f_ruin']:.0f}$", font_size=18, color=QC.LOSS).next_to(
            ax.c2p(k["f_ruin"], top * 1.3), UP, buff=0.05)
        gk = DashedLine(ax.c2p(k["f_gauss"], -0.1), ax.c2p(k["f_gauss"], top * 1.3), color=GREY_B, stroke_width=2)
        gkl = label(rf"mean--variance heuristic $\mu/\sigma^2 = {k['f_gauss']:.0f}$", font_size=18, color=GREY_B).next_to(
            ax.c2p(k["f_gauss"], top * 0.6), LEFT, buff=0.08)  # left of its line: the notes take the right
        x = ValueTracker(0.0)
        dot = always_redraw(lambda: Dot(ax.c2p(x.get_value(), float(np.interp(x.get_value(), f, gg))), radius=0.08,
                                        color=YELLOW))
        ro = always_redraw(lambda: MathTex(rf"f = {x.get_value():.1f},\ \ g = {float(np.interp(x.get_value(), f, gg)):.3f}",
                                           font_size=26, color=YELLOW).next_to(g, UP, buff=0.1).align_to(g, RIGHT))
        half = float(np.interp(k["f_emp"] / 2, f, gg))
        rows = [cmath(r"g(f)", r"=", r"\mathbb{E}\log(1 + fX) \approx f\mu - \tfrac12 f^2\mathbb E[X^2]", font_size=32),
                cmath(r"f^*_{\text{quadratic}}", r"=", r"\mu/\mathbb E[X^2]", font_size=32),
                cmath(r"f", r"<", r"1/|x_{\min}|\quad(\log 0 = -\infty)", font_size=32)]
        eqs = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
        notes = VGroup(
            wrapped_label(rf"sample optimum {k['f_emp']:.1f}, near the sample bankruptcy wall; worst observed window "
                          rf"{100 * k['min']:.1f}\% of notional. Future losses need not respect that wall", 4.6, 19, GREY_A),
            wrapped_label(rf"half that leverage keeps {100 * half / k['g_max']:.0f}\% of the growth, and survives a month "
                          r"twice as bad as any seen", 4.6, 19, GAMMA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(eqs, DOWN, buff=0.35).align_to(eqs, LEFT)
        src = real_data(rf"Part 10's {k['n']} one-month P\&Ls of a sold, hourly-hedged 30-day bitcoin call, one started each "
                       r"day (they overlap), as returns on notional")
        pc = pause(r"Does the worst observed loss bound an unseen loss?", width=4.6, font_size=21,
                   corner=DR).shift(UP * 0.4)  # the left corner holds the chart's axis label; clear the source line
        at_wall = k["f_emp"] > 0.9 * k["f_ruin"]
        ksay = (f"The curve keeps rising until it hits the wall at {k['f_ruin']:.0f}: in this sample the optimum is "
                "simply as close to ruin as the worst month allows, which only means the sample has not yet seen a "
                "worse month." if at_wall else
                f"The curve peaks at {k['f_emp']:.0f}, well before the wall at {k['f_ruin']:.0f}.")
        with self.voiceover(
            f"""Sizing has another trap. Expected log wealth is approximately f times the mean minus half f squared times the second moment. The quadratic optimizer is mean over the second moment; the displayed mean-over-variance heuristic is about {k['f_gauss']:.0f}, not an exact Gaussian Kelly optimum. <bookmark mark='a'/> A Gaussian has an unbounded loss tail. Here the red line instead uses the worst observed loss: it is a sample bankruptcy wall, not a guaranteed future bound. <bookmark mark='b'/> These {k['n']} monthly windows overlap. Their fitted optimum is {k['f_emp']:.1f}, close to that wall, which shows how strongly this in-sample answer depends on the worst observation. <bookmark mark='c'/> Half retains {100 * half / k['g_max']:.0f} percent of fitted growth and survives twice that observed loss; larger unseen losses can still ruin it. This diagnostic supplies no implementable leverage recommendation. Next: quoting both sides."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(eqs[0]), FadeIn(eqs[1]), FadeIn(gk), FadeIn(gkl))
            vo.wait_until("a")
            self.play(FadeIn(eqs[2]), Create(wall), FadeIn(walll))
            vo.wait_until("b")
            self.play(Create(line), run_time=1.5)
            self.add(dot, ro)
            self.play(x.animate.set_value(k["f_emp"]), run_time=max(vo.until("c") - 0.5, 1.0))
            self.play(FadeIn(notes[0]))
            self.play(x.animate.set_value(k["f_emp"] / 2), FadeIn(notes[1]), FadeIn(pc), run_time=1.5)
        dot.clear_updaters()
        ro.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
