from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import credit as CR
from videos.quant.quant20.common import (BAD, GBMC, LOGIT, PART, RISKY, ask, fit_right, grid_fn, house_lab,
                                         illustration, load, surf3d_axes)


class Models(VoiceoverScene, ThreeDScene):
    def construct(self):
        m = load("models")
        self.card()
        self.task(m)
        self.trees()
        self.roc(m)
        self.table(m)
        self.calib(m)
        self.surface(m)
        self.importance(m)

    def card(self):
        c = chapter_card(9, r"Logit and boosted trees, sealed", r"How well can accounts predict bankruptcy?", lit=(2001,),
                         part=PART)
        with self.voiceover("Chapter nine. A logit and boosted trees, trained on the past and tested on years sealed in "
                            "advance."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def task(self, m):
        rows = [cmath(r"\mathbb{P}(y_{i,t} = 1)", r"=", r"\frac{1}{1 + e^{-(\beta_0 + \beta^\top x_{i,t})}}", font_size=38,
                      colors={r"\mathbb{P}(y_{i,t} = 1)": LOGIT}),
                cmath(r"F_K(x)", r"=", r"F_0 + \eta\sum_{k=1}^{K} f_k(x),\quad f_k = \text{a depth-3 tree fitted to the "
                      r"gradient}", font_size=32, colors={r"F_K(x)": GBMC}),
                cmath(r"\text{fit}", r"\ ", r"2010\text{--}16,\quad \text{choose}\ 2017\text{--}20,\quad \text{sealed}\ "
                      r"2021\text{--}23", font_size=32, colors={r"\text{fit}": WHITE})]
        whys = [why(r"Shumway (2001): a logit on firm-years is a discrete-time hazard model; Campbell, Hilscher and "
                    r"Szilagyi (2008) added market variables. Twelve inputs: Altman's five and seven more, standardised"),
                why(r"gradient boosting (Friedman, 2001): each small tree corrects the last ones' errors on the log-loss; "
                    r"the House's own implementation, stopped when the validation loss stops falling"),
                why(rf"both registered before the hold-out was opened; the trial counter goes to {m['trials']}")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.0, buff=0.7, edge=6.9)
        with self.voiceover(
            "Two models on the same twelve inputs: Altman's five ratios, and seven more, among them net income, cash "
            "flow, cash, leverage, size and interest. The first is a logit, which Tyler Shumway showed in 2001 is a "
            "hazard model when it is fitted to firm-years. <bookmark mark='a'/> The second is gradient-boosted trees, "
            "hundreds of small decision trees, each one fitted to the errors of the ones before. <bookmark mark='b'/> "
            "Both are fitted to 2010 through 2016, tuned on 2017 to 2020, and registered with the House before the "
            "firm-years of 2021 to 2023 are opened. The trial counter rises by two, to "
            f"{m['trials']}."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def trees(self):
        def node(t, c_=GREY_B, w=2.6):
            r_ = RoundedRectangle(corner_radius=0.12, width=w, height=0.62, stroke_color=c_, stroke_width=2)
            return VGroup(r_, label(t, font_size=16).move_to(r_))
        root = node(r"liabilities / assets $>$ 0.9?").move_to(UP * 2.0)
        l1 = node(r"operating profit / assets $<$ $-$0.1?").move_to(LEFT * 3.2 + UP * 0.5)
        r1 = node(r"market equity / liabilities $<$ 0.3?").move_to(RIGHT * 3.2 + UP * 0.5)
        leaves = VGroup(*[node(t, c_, 1.9).move_to(p_) for t, c_, p_ in [
            (r"$-0.4$", GBMC, LEFT * 4.8 + DOWN * 1.1), (r"$+0.3$", BAD, LEFT * 1.6 + DOWN * 1.1),
            (r"$+0.1$", GBMC, RIGHT * 1.6 + DOWN * 1.1), (r"$+0.9$", BAD, RIGHT * 4.8 + DOWN * 1.1)]])
        edges = VGroup(Line(root.get_bottom(), l1.get_top(), color=GREY_C), Line(root.get_bottom(), r1.get_top(), color=GREY_C),
                       *[Line(a.get_bottom(), b.get_top(), color=GREY_C) for a, b in
                         [(l1, leaves[0]), (l1, leaves[1]), (r1, leaves[2]), (r1, leaves[3])]])
        foot = wrapped_label(r"one tree of many (schematic values): each leaf adds to the log-odds of bankruptcy. Trees "
                             r"capture interactions a logit cannot: high leverage matters far more when the market "
                             r"equity cushion is thin. The House grows them on histogram splits with Newton leaf values",
                             12.0, 19, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "What does one tree do? It asks a few questions in turn. Is the company's debt more than ninety percent "
            "of its assets? <bookmark mark='a'/> If so, is the market's cushion thin? Each leaf adds a little to the "
            "log-odds of bankruptcy. <bookmark mark='b'/> A logit can only add up its inputs; trees can say that "
            "leverage matters much more when the equity cushion is thin. That is an interaction, and credit is full "
            "of them."
        ) as vo:
            self.play(FadeIn(root))
            vo.wait_until("a")
            self.play(Create(edges[:2]), FadeIn(l1), FadeIn(r1))
            vo.wait_until("b")
            self.play(Create(edges[2:]), FadeIn(leaves), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def roc(self, m):
        g = axes([0, 1], [0, 1], x_length=5.4, y_length=5.0, xlabel=r"survivors flagged (false positive rate)",
                 ylabel=r"bankruptcies caught", xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], font_size=14
                 ).to_edge(LEFT, buff=1.2).shift(DOWN * 0.2)
        ax = g.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_C, stroke_width=1.5)
        cols = {"altman": RISKY, "logit": LOGIT, "gbm": GBMC}
        lines = VGroup()
        for k, c_ in cols.items():
            fp, tp = (np.asarray(x) for x in m["roc"][k])
            lines.add(curve(ax, fp, tp, c_, stroke_width=3))
        h = m["results"]["holdout"]["auc"]
        side = VGroup(
            legend([(RISKY, rf"Altman's Z (1968), AUC {h['altman']:.3f}"), (LOGIT, rf"logit, AUC {h['logit']:.3f}"),
                    (GBMC, rf"boosted trees, AUC {h['gbm']:.3f}")], font_size=18),
            MathTex(rf"\text{{top 10\% of scores: }} {100 * m['top_decile_capture']:.0f}\%\ \text{{of bankruptcies}}",
                    font_size=26, color=GBMC),
            wrapped_label(r"the sealed years, 2021--2023, seen once. The accuracy ratio used by rating agencies is "
                          r"$2\,\text{AUC} - 1$", 4.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "The sealed years, opened once. Each curve shows, as the threshold loosens, the share of bankruptcies "
            "caught against the share of survivors wrongly flagged. <bookmark mark='a'/> Altman's formula, fifty-seven "
            f"years old, scores {h['altman']:.2f}. The logit, {h['logit']:.2f}. <bookmark mark='b'/> The trees, "
            f"{h['gbm']:.2f}: the companies in their riskiest tenth went on to account for "
            f"{100 * m['top_decile_capture']:.0f} percent of the bankruptcies."
        ) as vo:
            self.play(FadeIn(g), Create(diag))
            vo.wait_until("a")
            self.play(Create(lines[0]), Create(lines[1]), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lines[2]), FadeIn(side[1]), FadeIn(side[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def table(self, m):
        r = m["results"]
        hx = [-4.6, -1.6, 0.9, 3.4, 5.6]
        heads = [r"", r"Altman", r"logit", r"trees", r"defaults"]
        rows = VGroup(VGroup(*[label(h_, font_size=20, color=GREY_A).move_to([x, 2.0, 0]) for h_, x in zip(heads, hx)]))
        for i, (k, nm) in enumerate([("fit", r"fit, 2010--16"), ("validation", r"validation, 2017--20"),
                                     ("holdout", r"sealed, 2021--23")]):
            y = 1.2 - 0.75 * i
            a = r[k]["auc"]
            rows.add(VGroup(label(nm, font_size=20).move_to([hx[0], y, 0]),
                            *[MathTex(f"{a[mm]:.3f}", font_size=28).move_to([x, y, 0]) for mm, x in
                              zip(("altman", "logit", "gbm"), hx[1:4])],
                            MathTex(f"{r[k]['defaults']}", font_size=26, color=GREY_A).move_to([hx[4], y, 0])))
        b = r["holdout"]["brier"]
        foot = wrapped_label(
            rf"AUC by period. The trees' fit-period score ({r['fit']['auc']['gbm']:.3f}) falls to "
            rf"{r['holdout']['auc']['gbm']:.3f}: some of what they learned was the fit years' noise, the gap a "
            rf"backtest never shows. Brier score in the sealed years: trees {b['gbm']:.4f}, logit {b['logit']:.4f}, "
            rf"the base rate alone {b['base']:.4f}: rare events leave little room to improve on 'nobody defaults'",
            12.4, 18, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The same scores, period by period. <bookmark mark='a'/> On the years they were fitted to, the trees look "
            f"almost perfect, {r['fit']['auc']['gbm']:.2f}. On the validation years, less; on the sealed years, "
            f"{r['holdout']['auc']['gbm']:.2f}. The fall is what the trees learned that was only noise. The logit "
            "barely falls at all: it had less capacity to memorize. <bookmark mark='b'/> And by the Brier score, the "
            "mean squared error of the probabilities, every model is only slightly better than predicting the base "
            "rate for everyone, because bankruptcies are rare. Ranking is easy to improve; probabilities are hard."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def calib(self, m):
        pr, re = np.asarray(m["calib"]["pred"]) * 100, np.asarray(m["calib"]["real"]) * 100
        g = axes([0, 9], [0, 9], x_length=5.0, y_length=5.0, xlabel=r"predicted, \%", ylabel=r"realised, \%",
                 xticks=[0, 3, 6, 9], yticks=[0, 3, 6, 9], font_size=14).to_edge(LEFT, buff=1.4).shift(DOWN * 0.2)
        ax = g.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(9, 9), color=GREY_C, stroke_width=1.5)
        dots = VGroup(*[Dot(ax.c2p(min(a, 9), min(b, 9)), color=GBMC, radius=0.08) for a, b in zip(pr, re)])
        side = VGroup(
            label(r"the trees' sealed-year forecasts, in ten groups", font_size=20, color=GREY_A),
            MathTex(rf"\text{{riskiest tenth: predicted }} {pr[-1]:.1f}\%,\ \text{{realised }} {re[-1]:.1f}\%", font_size=24),
            MathTex(rf"\text{{next: }} {pr[-2]:.1f}\%\ \text{{vs}}\ {re[-2]:.1f}\%", font_size=24, color=BAD),
            wrapped_label(r"the sealed years held 2022--23's rise in bankruptcies; the base rate the models learned was "
                          r"that of calmer years, so the middle groups are under-forecast. Calibration drifts with the "
                          r"cycle; ranking survives it", 4.4, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "Are the probabilities right? Sort the sealed firm-years into ten groups by predicted risk, and compare "
            "each group's forecast with what happened. <bookmark mark='a'/> The riskiest tenth is close: "
            f"{pr[-1]:.1f} percent predicted, {re[-1]:.1f} realised. <bookmark mark='b'/> The next groups were "
            "under-forecast: bankruptcies rose in 2022 and 2023 above the rate of the calmer years the models learned. "
            "A desk that uses these probabilities, not just the ranking, must re-anchor them to the cycle."
        ) as vo:
            self.play(FadeIn(g), Create(diag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.15), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def surface(self, m):
        p = m["pdp"]
        q = np.asarray(p["q"])
        G = np.asarray(p["gbm"]) * 100  # rows: leverage quantile; columns: cushion quantile
        f = grid_fn(q, q, G)
        top = float(np.ceil(G.max()))
        ax = surf3d_axes([0.05, 0.95, 0.3], [0.05, 0.95, 0.3], [0, top, top / 2], x_length=6.0, y_length=4.8, z_length=3.0)
        ax.shift(RIGHT * 0.9 + DOWN * 0.3)
        surf = Surface(lambda u, w: ax.c2p(u, w, f(u, w)), u_range=(0.05, 0.95), v_range=(0.05, 0.95),
                       resolution=(18, 18), fill_opacity=0.85, stroke_width=0.4, stroke_color=GREY_D,
                       checkerboard_colors=False)
        surf.set_fill_by_value(axes=ax, colorscale=[(QC.GAIN, 0), (QC.IMPLIED, top / 3), (QC.LOSS, top)], axis=2)
        lev, cus = np.asarray(p["lev"]), np.asarray(p["cushion"])
        key = label(rf"market cushion ME/TL, percentile (across: {cus[0]:.2f} to {cus[-1]:.0f}); leverage TL/TA, "
                    rf"percentile (back: {lev[0]:.2f} to {lev[-1]:.2f}); bankruptcy probability, \% (up); other inputs "
                    r"at their medians", font_size=17, color=GREY_A).to_corner(UL, buff=0.3)
        self.set_camera_orientation(phi=65 * DEGREES, theta=-55 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(key)
        self.remove(key)
        with self.voiceover(
            "What shape did the trees learn? Hold every input at its median, and vary two: leverage, and the market's "
            "cushion over the debt. <bookmark mark='a'/> The surface is a staircase, not a slope: the risk is flat "
            "over most of the range and then jumps, near the point where liabilities reach the assets, and jumps "
            "higher where the cushion is thin. <bookmark mark='b'/> A logit would draw a smooth tilted sheet. The "
            "steps are thresholds the trees found in the fit years, and some of them are noise, which is part of why "
            "their score fell out of sample."
        ) as vo:
            self.play(Create(ax), FadeIn(key))
            self.play(Create(surf), run_time=2.5)
            vo.wait_until("a")
            self.move_camera(theta=-130 * DEGREES, run_time=5)
            vo.wait_until("b")
        self.wait(0.3)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=0.5)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0, zoom=1.0, frame_center=ORIGIN)

    def importance(self, m):
        f, imp, b = m["features"], np.asarray(m["gbm_importance"]), np.asarray(m["logit_beta"])[1:]
        order = np.argsort(imp)[::-1]
        bars = VGroup()
        for i, k in enumerate(order):
            y = 2.4 - 0.4 * i
            w = imp[k] * 22
            bars.add(VGroup(label(f[k], font_size=17).move_to([-3.6, y, 0], aligned_edge=RIGHT),
                            Rectangle(width=max(w, 0.02), height=0.28, stroke_width=0, fill_color=GBMC,
                                      fill_opacity=0.8).move_to([-3.4 + w / 2, y, 0]),
                            MathTex(f"{b[k]:+.2f}", font_size=22, color=BAD if b[k] > 0 else LOGIT).move_to([3.4, y, 0])))
        heads = VGroup(label(r"share of the trees' split gain", font_size=18, color=GBMC).move_to([-1.6, 2.95, 0]),
                       label(r"logit coefficient", font_size=18, color=GREY_A).move_to([3.4, 2.95, 0]))
        card = house_lab(r"one split, by histogram", CR.GBM._grow, "gl, hl, cl = np.cumsum", 4, width=6.2)
        card.scale(0.8).to_corner(DR, buff=0.3)
        with self.voiceover(
            "What do the trees rely on? <bookmark mark='a'/> Leverage and operating profit lead, then working capital "
            "and the market's cushion: Altman's ratios, and Merton's. The logit agrees on the signs: more debt and "
            "larger size, given equity, raise the risk; more market equity, profit and liquidity lower it. "
            "<bookmark mark='b'/> And the House's split, for the record: cumulative sums of the gradients across "
            "histogram bins, and the gain of every possible cut at once."
        ) as vo:
            self.play(FadeIn(heads))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in bars], lag_ratio=0.12, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(card))
        q = ask(r"the trees score 0.98 on the years they were fitted to and 0.90 on the sealed ones. Which number "
                r"would a vendor put in the brochure, and which should you use?")
        with self.voiceover("The trees score near perfect on the years they learned from, and point nine on the sealed "
                            "ones. Which number goes in the brochure, and which should you use?"):
            self.play(FadeOut(card), FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
