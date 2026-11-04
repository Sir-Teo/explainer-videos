from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import rates as R
from videos.quant.quant18.common import CURV, LEVEL, PART, SLOPE, load


def positions():
    """Four positions off the curve of 31 December 2025: their key-rate DV01s at the PCA maturities, and the dollar
    risk (per 100 of face) of a one-standard-deviation daily move in each factor."""
    c, p, f, im = load("curve_day")["20251231"], load("pca"), load("fly"), load("immunize")
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
        out[k] = {"dv01": float(kr.sum()), "krd": kr, "factor": np.abs(L @ kr) * sd}
    return keys, out


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
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
            big = int(np.argmax(r["factor"]))
            for k in range(3):
                col = [LEVEL, SLOPE, CURV][k]
                row.add(MathTex(f"{r['factor'][k]:.3f}", font_size=28, color=col if k == big else GREY_B).move_to(
                    [xs[2 + k], y, 0]))
            cells.add(row)
        title = label(r"Four positions, three ways to report them", font_size=30).to_edge(UP, buff=0.4)
        foot = wrapped_label(r"\$ per 100 of face: DV01 for a 1 bp parallel fall; factor columns, the size of the loss "
                             r"or gain in a one-standard-deviation daily move of each factor (chapter 10), from the key-rate "
                             r"DV01s at nine maturities. Curve: 31 December 2025", 12.4, 18, GREY_A).to_edge(DOWN, buff=0.4)
        st, im = out[names[1]], out[names[3]]
        with self.voiceover(
            "Rule eighteen is about how the desk sees a position. Four of them, each reported three ways: the single "
            "DV01, and the risk in each of the three factors. <bookmark mark='a'/> A plain ten-year note: all three "
            "agree, it is a level bet. <bookmark mark='b'/> The steepener: a DV01 of zero, and a real slope risk. "
            "<bookmark mark='c'/> The butterfly: small in every factor, which is the point of it, and why chapter "
            "sixteen's risk lived elsewhere. <bookmark mark='d'/> And the immunized pension fund: a DV01 of zero, and "
            f"its largest exposure is to curvature, {im['factor'][2]:.2f} per hundred on an ordinary day. A barbell "
            "against a bullet is a curvature trade, whether its owner meant one or not."
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
        rule = wrapped_label(r"Rule 18: every curve the House builds reprices its inputs and is checked against an "
                             r"independent fit; every rates position is reported by its key-rate DV01s and its exposure "
                             r"to level, slope and curvature, never by one duration number; and every hedge is tested on "
                             r"twists and on the largest historical moves, not only on parallel shifts.  "
                             rf"One strategy tested here: the counter reads {env['trials']}.", 12.4, 21,
                             QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The rates desk opens with these tools. <bookmark mark='a'/> Bond arithmetic; the curve and its bootstrap; "
            "the Svensson fit; factors, factor-neutral trades and key rates; swaps, futures and SOFR; and the term "
            "premium, the Taylor rule, and the leveraged hedge in a fire sale. <bookmark mark='b'/> And the eighteenth "
            "rule. Every curve the House builds reprices its inputs and is checked against an independent fit. Every "
            "rates position is reported by its key-rate risks and its exposure to level, slope and curvature, never by "
            "one duration number. And every hedge is tested on twists and on the largest moves in history, not only on "
            f"parallel shifts. One strategy was tested in this part, the butterfly, and the counter reads "
            f"{env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["rates"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
