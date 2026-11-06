from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data, tbar, predict


class Scoring(VoiceoverScene):
    def construct(self):
        sc = load("scoring")
        r2 = load("race2")
        self.card()
        self.slider(sc)
        self.derive()
        self.table(sc)
        self.lab(r2)
        self.mcs(r2)

    def card(self):
        c = chapter_card(12, r"Scoring forecasts honestly", r"How do you grade a forecast of something you never see?",
                         part=PART)
        with self.voiceover("Chapter twelve. Scoring forecasts honestly."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def slider(self, sc):
        hh = np.asarray(sc["hh"])
        cv = sc["curves"]
        keys = ["0", "78", "5", "1"]
        names = {"0": r"the true variance itself", "78": r"realized variance from 78 returns",
                 "5": r"5 returns", "1": r"one squared return"}
        g1 = axes([0.25, 2.0], [0, 0.6], x_length=5.6, y_length=3.4, xticks=[0.5, 1, 1.5, 2], yticks=[],
                  xlabel=r"forecast $\hat h$ (true variance $= 1$)", ylabel=r"expected QLIKE (shifted)", font_size=15)
        g2 = axes([0.25, 2.0], [0, 0.6], x_length=5.6, y_length=3.4, xticks=[0.5, 1, 1.5, 2], yticks=[],
                  xlabel=r"forecast $\hat h$", ylabel=r"expected squared error on volatility (shifted)", font_size=15)
        VGroup(g1, g2).arrange(RIGHT, buff=0.8).shift(DOWN * 0.3)
        k = ValueTracker(0)

        def mk(g, key, col, which):
            def f():
                i = int(round(k.get_value()))
                y = np.asarray(cv[keys[i]][which])
                y = y - y.min()
                j = int(np.argmin(y))
                m = y <= 0.6  # draw the curve only inside the axes: no flat line where it leaves the top
                return VGroup(curve(g.ax, hh[m], y[m], col, stroke_width=4),
                              DashedLine(g.ax.c2p(hh[j], 0), g.ax.c2p(hh[j], 0.55), color=col, stroke_width=2),
                              MathTex(rf"\arg\min = {hh[j]:.2f}", font_size=24, color=col).next_to(g.ax.c2p(hh[j], 0.55), UP, buff=0.05))
            return always_redraw(f)

        c1, c2 = mk(g1, "qlike", GOOD, "qlike"), mk(g2, "msevol", BAD, "msevol")
        proxy = always_redraw(lambda: label(r"judged against: " + names[keys[int(round(k.get_value()))]], font_size=24,
                                            color=YELLOW).to_edge(UP, buff=0.5))
        hl = history_card(2005, r"Peter Hansen and Asger Lunde", r"330 ARCH-type models raced: does anything beat a "
                          r"GARCH(1,1)? On the DM--\$ rate, no; on IBM, models with leverage won", color=QC.IDEA, width=5.4,
                          font_size=18).move_to(ORIGIN)
        am = cv["1"]["argmin_msevol"]
        with self.voiceover(
            "In 2005 Peter Hansen and Asger Lunde raced three hundred and thirty models and asked: does anything "
            "beat a GARCH(1,1)? But the true variance is never observed; every forecast is judged against a noisy "
            "proxy. <bookmark mark='a'/> "
            "The true variance is one. Slide the forecast, and draw the average loss against the proxy. With the truth as the proxy, both losses are smallest at one. "
            "<bookmark mark='b'/> Now make the proxy noisier: a realized variance, then five returns, then a single "
            "squared return. The squared error on volatility slides its minimum to the left, to "
            f"variance forecast {am:.2f}, corresponding to volatility near its square root: it targets a different quantity. <bookmark mark='c'/> QLIKE's minimum does not move. That "
            "is Andrew Patton's 2011 result, and the sliding is the proof by picture."
        ) as vo:
            self.play(FadeIn(hl))
            vo.wait_until("a")
            self.play(FadeOut(hl))
            self.play(FadeIn(g1), FadeIn(g2))
            self.add(c1, c2, proxy)
            vo.wait_until("b")
            for i in (1, 2, 3):
                self.play(k.animate.set_value(i), run_time=1.5)
                self.wait(0.3)
            vo.wait_until("c")
            self.play(Indicate(c1, color=GOOD))
        for m in (c1, c2, proxy):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"L_Q(h, \hat h)", r"=", r"\frac{h}{\hat h} - \ln\frac{h}{\hat h} - 1", font_size=34),
            cmath(r"\partial_{\hat h}\,\mathbb{E}[L_Q\mid\mathcal{F}]", r"=", r"\frac{\hat h - \mathbb{E}[\tilde h\mid\mathcal{F}]}{\hat h^2}", font_size=34),
            cmath(r"\mathbb{E}[\tilde h\mid\mathcal{F}] = \mathbb{E}[h\mid\mathcal{F}]", r"\Rightarrow", r"\text{the ranking is unchanged}", font_size=34),
            cmath(r"\arg\min_{\hat\sigma}\mathbb{E}(\sqrt{\tilde h} - \hat\sigma)^2", r"=", r"\mathbb{E}\sqrt{\tilde h} < \sqrt{\mathbb{E}\tilde h}", font_size=34),
            cmath(r"DM", r"=", r"\bar d\,/\sqrt{\widehat{LRV}(d)/T},\quad d_t = L_{A,t} - L_{B,t}", font_size=34),
        ]
        whys = [why(r"QLIKE: the Gaussian negative log-likelihood, up to constants"),
                why(r"zero only where the forecast equals the proxy's conditional mean"),
                why(r"an unbiased proxy has the true variance as its mean: noise adds a constant (Patton 2011)"),
                why(r"Jensen: the square root of a noisy proxy is biased down, so this loss rewards under-forecasts"),
                why(r"Diebold and Mariano (1995): a $t$-test on the loss difference, Newey--West variance (Part 6)")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-2.2, buff=0.55, edge=6.9)
        with self.voiceover(
            """Why QLIKE is robust. Compare positive forecasts measurable to the same information set, using a positive conditionally unbiased variance proxy and finite expected losses. <bookmark mark='a'/> Differentiating expected QLIKE targets conditional mean variance. <bookmark mark='b'/> Proxy noise changes expected losses by a forecast-independent term, preserving rankings under those conditions. <bookmark mark='c'/> Taking the square root changes the target through Jensen's inequality. <bookmark mark='d'/> Diebold--Mariano compares average loss differences using a long-run variance. Its normal reference needs a suitable loss-difference CLT and positive finite long-run variance; reused test data and model selection require extra care."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.3)
        self.clear_scene()

    def table(self, sc):
        T = sc["table"]
        losses = list(T)
        proxies = list(T[losses[0]])
        cells = [label(r"loss", font_size=20, color=GREY_B)] + [label(p, font_size=19, color=GREY_B) for p in proxies]
        for ln in losses:
            cells.append(label(ln, font_size=20, color=WHITE))
            for p in proxies:
                w = T[ln][p]["winner"]
                cells.append(label(w, font_size=19, color=GOOD if w == "truth" else BAD))
        tab = VGroup(*cells).arrange_in_grid(rows=len(losses) + 1, cols=len(proxies) + 1, buff=(0.5, 0.25),
                                             col_alignments="l" + "c" * len(proxies))
        head = label(rf"which forecast wins? GARCH-simulated truth, {sc['R']} runs $\times$ {sc['T']:,} days".replace(",", "{,}"),
                     font_size=22, color=GREY_A)
        sub = label(r"candidates: the truth, $0.8\times$ the truth, $1.2\times$ the truth, a 60-day average", font_size=19,
                    color=GREY_B)
        grp = VGroup(head, sub, tab).arrange(DOWN, buff=0.35).move_to(UP * 0.4)
        pc = predict(r"Judged against squared returns, which wins under MAE: the true volatility, or 80\% of it?",
                        width=7.4, font_size=22).to_edge(DOWN, buff=0.35)
        w = T["MAE on volatility"]["squared return"]["winner"]
        verdict = ("80 percent of it. The absolute error on volatility rewards the forecast that is too low, and so does "
                   "the squared error on volatility." if w != "truth" else "The truth, here.")
        with self.voiceover(
            f"A simulation with a known answer: GARCH volatility, the truth known every day, {sc['R']} times over. Offer "
            f"four forecasts: the truth, eighty percent of it, a hundred and twenty percent, and a sixty-day moving average. "
            f"Judge them with four losses against three proxies. <bookmark mark='a'/> Pause and predict: against squared "
            f"returns, under the absolute error on volatility, which wins, the truth or eighty percent of it? <bookmark "
            f"mark='b'/> {verdict} QLIKE and the squared error on variance pick the truth under every proxy."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(VGroup(*cells[:len(proxies) + 1])))
            vo.wait_until("a")
            self.play(FadeIn(pc))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cells[len(proxies) + 1:]], lag_ratio=0.1, run_time=3))
        self.wait(0.3)
        self.clear_scene()

    def lab(self, r2):
        card = lab_card(r"QLIKE and the Diebold--Mariano test", [
            "def qlike(f, rv):",
            "    return rv / f - np.log(rv / f) - 1",
            "def diebold_mariano(loss_a, loss_b, lags=5):",
            "    d = loss_a - loss_b; n = len(d); dc = d - d.mean()",
            "    v = dc @ dc / n",
            "    for k in range(1, lags + 1):",
            "        v += 2 * (1 - k/(lags+1)) * (dc[k:] @ dc[:-k]) / n",
            "    t = d.mean() / np.sqrt(v / n)",
            "    return t",
        ], source="explainer/quant/house/vol.py", width=6.6).to_corner(UL, buff=0.3)
        mz = r2["mz"]
        names = ["GARCH", "HAR", "log-HAR", "LSTM"]
        rows = VGroup(*[MathTex(rf"\text{{{n_}: }} a = {mz[n_]['a'] * 1e4:+.1f}\times10^{{-4}},\ b = {mz[n_]['b']:.2f},\ "
                                rf"R^2 = {mz[n_]['r2']:.2f}", font_size=24, color=GREY_A) for n_ in names])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        mzg = VGroup(label(r"Mincer--Zarnowitz (1969): $RV_t = a + b\,\hat h_t + e_t$; ideal $a = 0$, $b = 1$", font_size=20,
                           color=VOL), rows).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DR, buff=0.4)
        dm = r2["dm_vs_loghar"]
        with self.voiceover(
            f"""Lab. The House's scoring tools: QLIKE and Diebold--Mariano with a Newey--West variance. Here comparisons are exploratory after reuse of the 2020 sample. <bookmark mark='a'/> Mincer--Zarnowitz calibration requires intercept zero and slope one. Log-HAR's fitted slope is about {mz['log-HAR']['b']:.1f}; that association alone does not identify its cause. Any recalibration must fit on training or validation observations and face fresh outcomes."""
        ) as vo:
            self.play(FadeIn(card))
            lab_run(self, card, [f"DM, HAR against log-HAR, 2020: t = {dm['HAR']['t']:+.2f}"], run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(mzg))
        self.wait(0.3)
        self.clear_scene()

    def mcs(self, r2):
        pv = r2["mcs"]["pvalues"]
        order = sorted(pv, key=lambda k: pv[k])
        g = axes([0, 1.0], [0, len(order)], x_length=6.0, y_length=4.6, xticks=[0, 0.1, 0.25, 0.5, 1.0], yticks=[],
                 xlabel=r"model confidence set $p$-value, QLIKE, 2020", font_size=16).to_edge(LEFT, buff=2.2).shift(DOWN * 0.1)
        ax = g.ax
        bars, labs = VGroup(), VGroup()
        for i, k in enumerate(order):
            y = len(order) - i - 0.5
            l_, r_ = ax.c2p(0, y), ax.c2p(pv[k], y)
            hgt = ax.c2p(0, 0.6)[1] - ax.c2p(0, 0)[1]
            bars.add(Rectangle(width=max(r_[0] - l_[0], 0.02), height=hgt, stroke_width=0, fill_color=GOOD if pv[k] >= 0.1 else BAD,
                               fill_opacity=0.8).move_to((l_ + r_) / 2))
            labs.add(label(k, font_size=19, color=GREY_A).next_to(l_, LEFT, buff=0.12))
        cut = DashedLine(ax.c2p(0.1, 0), ax.c2p(0.1, len(order)), color=YELLOW, stroke_width=3)
        cut2 = DashedLine(ax.c2p(0.25, 0), ax.c2p(0.25, len(order)), color=GREY_B, stroke_width=2)
        surv = r2["mcs"]["survivors"]
        out25 = [k for k in order if pv[k] < 0.25]
        side = VGroup(
            wrapped_label('Hansen--Lunde--Nason (2011): nominal coverage within a fixed candidate set under valid bootstrap conditions; selection needs separate treatment', 4.6, 19, GREY_A),
            label(rf"at 90\%: {len(surv)} of {len(order)} survive", font_size=22, color=YELLOW),
            label(rf"at 75\%: " + ", ".join(out25) + r" out", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3)
        out_txt = ", ".join(out25)
        verdict = ("All of them survive. A single year, with one March in it, cannot separate these models with ninety "
                   "percent confidence." if len(surv) == len(order) else
                   "The set shrinks to the models listed in yellow.")
        with self.voiceover(
            f"""Last, many models at once. The Hansen--Lunde--Nason model confidence set repeatedly tests equal predictive accuracy and removes a worst model. Nominal coverage concerns a best model within a fixed candidate set, under valid dependence and bootstrap assumptions. It is not a guarantee after adaptive model selection. <bookmark mark='a'/> Here, {verdict} <bookmark mark='b'/> At seventy-five percent, {out_txt} drop out. Next: training the networks."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(labs), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.15), Create(cut), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(cut2), FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()
