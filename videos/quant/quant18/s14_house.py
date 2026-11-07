from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import rates as R
from videos.quant.quant18.common import CURV, LEVEL, PART, SLOPE, butterfly_example, load


def positions():
    """Four positions off the curve of 31 December 2025: their key-rate DV01s at the PCA maturities, and the dollar
    risk (per 100 of face) of a one-standard-deviation daily move in each factor."""
    c, p, f, im = load("curve_day")["20251231"], load("pca"), butterfly_example(), load("immunize")
    cv = R.Curve(c["nodes_t"], c["nodes_z"])
    keys = np.asarray(p["mats"], float)
    L, sd = np.asarray(p["loadings"]), np.asarray(p["sd_bp"])

    def note(cpn, T):
        t = np.arange(1, int(2 * T) + 1) / 2
        cf = np.full(len(t), 100 * cpn / 2)
        cf[-1] += 100
        return t, cf
    n2, n5, n10 = note(0.035, 2), note(0.0375, 5), note(0.04, 10)
    d = {k: R.key_rate_dv01(*v, cv, keys).sum() for k, v in (("2", n2), ("5", n5), ("10", n10))}
    w = np.asarray(f["weights"])
    pos = {
        r"long the 10-year note": [n10],
        r"2s10s steepener, DV01-neutral": [(n2[0], n2[1] * d["10"] / d["2"]), (n10[0], -n10[1])],
        r"2s5s10s butterfly (chapter 16)": [(n2[0], n2[1] * w[0] * d["5"] / d["2"]), n5,
                                            (n10[0], n10[1] * w[2] * d["5"] / d["10"])],
        r"the immunized fund (chapter 7)": [(np.array([5.0]), np.array([im["v1"] / cv.df(5.0)])),
                                            (np.array([30.0]), np.array([im["v2"] / cv.df(30.0)])),
                                            (np.array([15.0]), np.array([-im["L"] / cv.df(15.0)]))],
    }
    out = {}
    for k, fl in pos.items():
        kr = sum(R.key_rate_dv01(t, cf, cv, keys) for t, cf in fl)
        out[k] = {"dv01": float(kr.sum()), "krd": kr, "factor": -(L @ kr) * sd}
    return keys, out


class House(VoiceoverScene):
    def construct(self):
        from explainer.quant.house import pit
        env = {"trials": pit.trials_upto(PART)}
        self.card()
        self.report()
        self.module(env)

    def card(self):
        c = chapter_card(19, r"Rule 18: the rates desk", r"What does the House report for a rates position?", part=PART)
        with self.voiceover("Chapter nineteen. The House's eighteenth rule, and its rates desk."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def report(self):
        keys, out = positions()
        names = list(out)
        head = VGroup(*[label(h, font_size=19, color=c_) for h, c_ in
                        ((r"position", GREY_A), (r"DV01", WHITE), (r"level", LEVEL), (r"slope", SLOPE),
                         (r"curvature", CURV))])
        xs = [-4.4, -0.6, 1.4, 3.2, 5.0]
        y0 = 1.6
        for h, x in zip(head, xs):
            h.move_to([x, y0 + 0.7, 0])
        cells = VGroup()
        for i, n in enumerate(names):
            r = out[n]
            y = y0 - 0.95 * i
            row = VGroup(label(n, font_size=19).move_to([xs[0], y, 0]),
                         MathTex(f"{r['dv01']:+.3f}", font_size=28).move_to([xs[1], y, 0]))
            big = int(np.argmax(np.abs(r["factor"])))
            for k in range(3):
                col = [LEVEL, SLOPE, CURV][k]
                row.add(MathTex(f"{r['factor'][k]:+.3f}", font_size=28, color=col if k == big else GREY_B).move_to(
                    [xs[2 + k], y, 0]))
            cells.add(row)
        title = label(r"Four positions, three ways to report them", font_size=30).to_edge(UP, buff=0.4)
        foot = wrapped_label(r"Dollars: note face 100; steepener 10y face 100; fly 5y face 100; fund liability PV 100. DV01 sums one-sided 1bp key-bump value changes. Factor columns are signed first-order P\&L for a positive one-SD fitted PCA shock, not VaR or confidence limits. Coupon cash flows leave residual factor exposures.", 12.4, 16, GREY_A).to_edge(DOWN, buff=0.35)
        st, im = out[names[1]], out[names[3]]
        with self.voiceover(
            "These four illustrative positions are reported by aggregate key-rate DV01 and signed first-order profit or loss under positive one-standard-deviation fitted factor shocks. Their notional conventions are stated below. A standard deviation is not a stress limit or a confidence bound. <bookmark mark='a'/> The ten-year note has exposures to the fitted factors; level is not literally a parallel shift. <bookmark mark='b'/> The steepener cancels the displayed aggregate bump sensitivity but retains factor risk. <bookmark mark='c'/> The butterfly uses the same full-sample yield weights as chapter sixteen. Actual coupon cash flows distribute its key-rate risk, so the two point-maturity neutrality equations do not transfer exactly. <bookmark mark='d'/> The matched-value and duration fund still has nonzero factor exposures. These are local sensitivities, not realized daily returns or a certificate that any hedge survives large twists."
        ) as vo:
            self.play(FadeIn(title), FadeIn(head), FadeIn(foot))
            for i, m in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m)
                self.play(FadeIn(cells[i], shift=RIGHT * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def module(self, env):
        chart = house_chart(PART, lit=("rates",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{bond\_price}, \texttt{bond\_yield}, \texttt{bond\_risk}", r"price, yield, duration, convexity, DV01"),
            (r"\texttt{Curve}, \texttt{bootstrap\_par}", r"zero, forward and par rates; the curve that reprices its inputs"),
            (r"\texttt{nss}, \texttt{fit\_nss}", r"Nelson--Siegel--Svensson, fitted by regression and polish"),
            (r"\texttt{curve\_pca}, \texttt{fly\_weights}, \texttt{key\_rate\_dv01}", r"factors, factor-neutral trades, key "
                                                                                     r"rates"),
            (r"\texttt{par\_swap\_rate}, \texttt{conversion\_factor}, \texttt{compound\_in\_arrears}",
             r"swaps, futures, SOFR"),
            (r"\texttt{acm\_decompose}, \texttt{taylor\_rule}, \texttt{ldi\_spiral}",
             r"the term premium, the policy rule, a leveraged hedge in a fire sale"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=18, color=QC.HOUSE), label(b, font_size=18, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 7.0)
        tab.next_to(chart, DOWN, buff=0.3)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(rf"Rule 18: report pricing conventions and fit errors, key-rate and factor exposures, and the shocks actually tested. These examples do not implement a complete desk validation service. No butterfly return test or new registration in this pass; existing cumulative counter through Part 18: {env['trials']}.", 12.4, 20, QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            f"The rates module provides bond arithmetic, curves and bootstraps, parametric fits, factor and key-rate calculations, single-curve instrument examples and model illustrations. <bookmark mark='a'/> An exact synthetic-input bootstrap and an approximate fitted curve have different validation criteria. Report their conventions, residuals and independent comparisons. <bookmark mark='b'/> Rule eighteen is a proposed reporting standard: show key-rate and factor exposures and test stated parallel, twist and funding scenarios. These demonstrations are not a complete desk validation service, and they do not establish that every hedge was tested against all historical shocks. No butterfly return test or new registration is performed in this pass. The existing cumulative counter through Part eighteen is {env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["rates"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
