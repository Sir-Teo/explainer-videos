from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs, funding
from videos.quant.quant2.common import ro, CCP, LOSS, PART, TRADE, lab, load, real_data

C_ = {r"\sigma_t^2": LOSS, r"\lambda": QC.HOUSE, r"\text{IM}_t": CCP, r"\ell(\lambda)": QC.IDEA}
Z99 = 2.326


def row(*parts, fs=36):
    return cmath(*parts, colors=C_, font_size=fs)


def _x(d):
    d = int(d)
    return date(d // 10000, (d // 100) % 100, d % 100).toordinal()


class MarginModel(VoiceoverScene):
    def construct(self):
        m = load("imodel")
        self.card()
        self.span()
        self.ewma_math(m)
        self.breathing(m)
        self.fit(m)
        self.procyclical(m)

    def card(self):
        c = chapter_card(9, r"How much margin?", r"How does a clearing house size its margin, and when does it bite?",
                         lit=(1987, 2022), part=PART)
        with self.voiceover("Chapter nine. How much margin? Models, and procyclicality."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def span(self):
        # a short straddle on an index future under SPAN's 16 scenarios (illustrative: S = 100, 30 days, 20% vol)
        S0, T, v0, scan, vscan = 100.0, 30 / 365, 0.20, 6.0, 0.04

        def val(S, v):
            return -(bs.price(S, 100.0, T, v) + bs.price(S, 100.0, T, v, cp=-1))
        base = val(S0, v0)
        scen = []
        for frac in (0, 1 / 3, -1 / 3, 2 / 3, -2 / 3, 1, -1):
            for dv in (vscan, -vscan):
                scen.append((frac, dv, val(S0 + frac * scan, v0 + dv) - base, 1.0))
        for frac in (3, -3):
            scen.append((frac, 0.0, 0.30 * (val(S0 + frac * scan, v0) - base), 0.3))
        pnl = np.array([s[2] for s in scen])
        worst = int(np.argmin(pnl))
        g = axes([0, 17], [pnl.min() * 1.15, max(pnl.max(), 0.5) * 1.3], x_length=7.4, y_length=4.0,
                 xlabel=r"SPAN's 16 scenarios", ylabel=r"P\&L of a short straddle, per unit", font_size=17)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, (frac, dv, p, cov) in enumerate(scen, start=1):
            col = LOSS if p < 0 else QC.GAIN
            if i > 14:
                col = QC.CRISIS
            h = ax.c2p(0, p)[1] - ax.c2p(0, 0)[1]
            bars.add(Rectangle(width=0.32, height=max(abs(h), 0.01), stroke_width=0, fill_color=col, fill_opacity=0.85)
                     .move_to(ax.c2p(i, p / 2)))
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(17, 0), color=GREY_C, stroke_width=1.5)
        box = SurroundingRectangle(bars[worst], color=YELLOW, buff=0.06)
        txt = VGroup(
            label(r"price moves of 0, $\pm\frac13$, $\pm\frac23$, $\pm1$ price scan range,", font_size=21),
            label(r"each with volatility up and down: 14 scenarios", font_size=21),
            label(r"plus two extremes: 3 scan ranges, 30\% of the loss counted", font_size=21, color=QC.CRISIS),
            label(r"the scanning charge is the worst scenario", font_size=22, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.35).shift(UP * 0.8)
        src = note(r"CME Group, SPAN risk arrays; the straddle is illustrative (S = 100, 30 days, 20\% vol, scan 6)",
                   font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "How big should margin be? The CME's classic answer, SPAN, revalues a position under sixteen scenarios: the "
            "price unchanged or moved a third, two thirds or a whole scan range each way, with volatility up and down, plus "
            "two extreme moves counted at thirty percent. <bookmark mark='a'/> A short straddle earns a little when nothing "
            "happens and loses on every big move. <bookmark mark='b'/> The margin is the worst scenario: simple, and blind "
            "outside its grid."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(txt[:3]), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, UP if p < 0 else DOWN) for b, p in zip(bars, pnl)],
                                  lag_ratio=0.12, run_time=3))
            vo.wait_until("b")
            self.play(Create(box), FadeIn(txt[3]))
        self.wait(0.4)
        self.clear_scene()

    def ewma_math(self, m):
        rows = [
            row(r"\sigma_t^2", r"=", r"\lambda\,\sigma_{t-1}^2 + (1-\lambda)\,r_{t-1}^2"),
            row(r"\text{IM}_t", r"=", r"z_{0.99}\,\sigma_t\sqrt{h}\cdot N"),
            row(r"\ell(\lambda)", r"=", r"-\tfrac12 \sum_t \Big(\ln \sigma_t^2 + \frac{r_t^2}{\sigma_t^2}\Big)"),
            row(r"LR", r"=", r"-2\ln\frac{0.99^{T-x}\,0.01^{x}}{(1-\hat p)^{T-x}\,\hat p^{x}} \sim \chi^2_1"),
        ]
        whys = [why(r"exponentially weighted variance: yesterday's estimate, nudged by yesterday's squared return"),
                why(r"a 99\% Gaussian VaR over the close-out time $h$ days, on notional $N$"),
                why(r"choose $\lambda$ by likelihood: the Gaussian log-likelihood of the returns"),
                why(r"Kupiec's test: $x$ breaches in $T$ days against the promised 1\%, $\hat p = x/T$")]
        step = ladder(self, rows, whys, keep=4, top=2.7, x=-1.2, buff=0.5, edge=6.9)
        with self.voiceover(
            "Most clearing houses now use value-at-risk models instead. The simplest worth using is the exponentially "
            "weighted variance of RiskMetrics: today's variance estimate is yesterday's, nudged by yesterday's squared return, "
            "with a memory lambda. A lambda of point nine seven gives yesterday's return a weight of three percent and a memory "
            "of about a month. <bookmark mark='a'/> Initial margin is then a ninety-nine percent Gaussian value-at-risk over "
            "the days it would take to close out a defaulter. <bookmark mark='b'/> How fast should it forget? Choose lambda by "
            "maximum likelihood: the Gaussian log-likelihood of the returns, given the variances the recursion predicts. "
            "<bookmark mark='c'/> And check it the way a regulator would: count the days losses broke through the margin, "
            "and test the count against the promised one percent with Kupiec's likelihood ratio."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def breathing(self, m):
        d = np.asarray(m["date87"])
        r = np.asarray(m["r87"], float)
        mg = np.asarray(m["m87"], float)
        x = np.array([_x(v) for v in d], float)
        x = x - x[0]
        g = axes([0, x[-1]], [-0.22, 0.15], x_length=8.4, y_length=4.4, ylabel=r"daily return, US market, 1987",
                 xticks=[x[list(d).index(v)] for v in (19870701, 19871001, 19871201)],
                 xfmt=lambda v: {0: "Jul"}.get(int(v), "Oct" if v < 120 else "Dec"), yticks=[-0.2, -0.1, 0, 0.1],
                 yfmt=lambda v: f"{100 * v:+.0f}\\%" if v else "0", font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        k = ValueTracker(0)
        bnd = always_redraw(lambda: band(ax, x[:max(int(k.get_value()), 2)],
                                         -mg[:max(int(k.get_value()), 2)] / np.sqrt(2),
                                         mg[:max(int(k.get_value()), 2)] / np.sqrt(2), CCP, 0.3))
        bars = always_redraw(lambda: VGroup(*[Line(ax.c2p(xx, 0), ax.c2p(xx, rr), stroke_width=2.5,
                                                   color=LOSS if abs(rr) > mm / np.sqrt(2) else GREY_B)
                                              for xx, rr, mm in zip(x[:int(k.get_value())], r[:int(k.get_value())],
                                                                    mg[:int(k.get_value())])]))
        i19 = list(d).index(19871019)
        key = m["key"]
        res = VGroup(
            MathTex(rf"\text{{19 Oct: }}{100 * np.expm1(r[i19]):.1f}\%", font_size=32, color=LOSS),
            MathTex(rf"\text{{2-day margin: }}{100 * key['19870901']:.1f}\% \to {100 * key['19871016']:.1f}\% \to "
                    rf"{100 * key['19871020']:.1f}\%", font_size=28, color=CCP),
            label(r"margin arrives after the loss", font_size=24, color=QC.IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        card = lab_card(r"EWMA margin", [
            "def ewma_margin(r, lam=0.97, z=2.326, h=2):",
            "    v = np.empty(len(r)); v[0] = r[:20].var()",
            "    for t in range(1, len(r)):",
            "        v[t] = lam * v[t-1] + (1 - lam) * r[t-1]**2",
            "    return z * np.sqrt(h * v)",
        ], source="explainer/quant/house/funding.py", width=5.6, font_size=16).to_corner(DR, buff=0.3)
        src = real_data(r"Kenneth French, daily US market; band: the 1-day 99\% level, $\lambda = 0.97$", corner=DL)
        with self.voiceover(
            "Run it through 1987, lambda point nine seven. The band is the one-day ninety-nine percent level; bars are daily "
            f"returns, red when they break through. <bookmark mark='a'/> The nineteenth of October: {100 * np.expm1(r[i19]):.1f} "
            f"percent, far through the band. Only afterwards does margin balloon, from {100 * key['19871016']:.1f} percent of "
            f"notional to {100 * key['19871020']:.1f}. Margin arrives after the loss. <bookmark mark='b'/> The House's "
            "implementation is the recursion, five lines."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            self.add(bnd, bars)
            self.play(k.animate.set_value(i19 - 1), run_time=6, rate_func=linear)
            vo.wait_until("a")
            self.play(k.animate.set_value(i19 + 1), run_time=1.5)
            self.play(FadeIn(res[0]))
            self.play(k.animate.set_value(len(d)), run_time=3, rate_func=linear)
            self.play(FadeIn(res[1:]))
            vo.wait_until("b")
            self.play(FadeIn(card))
            lab(self, card, [f"ewma_margin(r)[16 Oct 87] = {key['19871016']:.4f}",
                             f"ewma_margin(r)[20 Oct 87] = {key['19871020']:.4f}"], direction=LEFT)
        for mm in (bnd, bars):
            mm.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def fit(self, m):
        grid = np.asarray(m["grid"], float)
        eras = np.asarray(m["eras"], float)
        ll = np.asarray(m["ll"], float)
        lln = (ll - ll.max()) / m["T"] * 1000
        path = np.asarray(m["lam_path"], float)
        g = axes([0.90, 0.995], [-1.2, 0.1], x_length=6.0, y_length=3.6, xlabel=r"$\lambda$",
                 ylabel=r"log-likelihood (per 1,000 days, from its peak)", xticks=[0.9, 0.94, 0.98],
                 yticks=[-1, -0.5, 0], font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        eb = band(ax, grid, np.clip(eras.min(0), -1.2, 0.1), np.clip(eras.max(0), -1.2, 0.1), QC.IDEA, 0.2)
        lc = curve(ax, grid, np.clip(lln, -1.2, 0.1), QC.IDEA)
        it = ValueTracker(0)

        def lam_now():
            i = int(np.clip(it.get_value(), 0, len(path) - 1))
            return float(path[i])
        dot = always_redraw(lambda: Dot(ax.c2p(lam_now(), float(np.interp(lam_now(), grid, lln))), radius=0.09,
                                        color=QC.HOUSE))
        rd = ro(r"\lambda =", lam_now, digits=3, font_size=32, color=QC.HOUSE).to_edge(RIGHT, buff=1.2).shift(UP * 2.4)
        rd2 = ro(r"\text{iteration}", lambda: it.get_value(), digits=0, font_size=26).next_to(rd, DOWN, buff=0.2)
        res = VGroup(
            MathTex(rf"\hat\lambda_{{\text{{US 1926--2020}}}} = {m['lam_hat']:.3f}", font_size=30, color=QC.HOUSE),
            MathTex(rf"\hat\lambda_{{\text{{BTC 2018--2025}}}} = {m['btc_lam']:.3f}", font_size=30, color=QC.HOUSE),
            MathTex(rf"\text{{breaches at }}\lambda = 0.97:\ {100 * m['breach_rate']:.2f}\%\ \text{{of days (promised 1\%)}}",
                    font_size=26, color=LOSS),
            MathTex(rf"\text{{Kupiec }} LR = {m['kupiec']['LR']:.0f},\ p < 10^{{-10}}", font_size=26, color=LOSS),
            MathTex(rf"\text{{constant }}\sigma\text{{ baseline: }}{100 * m['breach_rate_const']:.2f}\%,\ LR = "
                    rf"{m['kupiec_const']['LR']:.0f}", font_size=24, color=GREY_A),
            MathTex(rf"\text{{BTC at }}\lambda = 0.97:\ {100 * m['btc_breach']:.2f}\%", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(rd2, DOWN, buff=0.4).to_edge(RIGHT, buff=0.35)
        leg = label(r"band: the same curve in five 19-year eras", font_size=18, color=QC.IDEA).next_to(g, UP, buff=0.1)
        with self.voiceover(
            "Now fit lambda, and watch the fit run. The curve is the log-likelihood over lambda on ninety-four years of daily "
            "returns; the band is the same curve computed separately in five eras of nineteen years. A golden-section search "
            "closes in on the peak, iteration by iteration. <bookmark mark='a'/> It lands at "
            f"{m['lam_hat']:.3f} for the American market, a memory of about two weeks, and {m['btc_lam']:.3f} for Bitcoin. "
            "<bookmark mark='b'/> Then the backtest. With lambda at point nine seven, losses broke the ninety-nine percent "
            f"margin on {100 * m['breach_rate']:.1f} percent of days, {m['breaches']} times in {m['T']:,} days, double the "
            "promise, and Kupiec rejects the model resoundingly. The constant-volatility baseline fails too, at "
            f"{100 * m['breach_rate_const']:.1f} percent, with its misses bunched in crises. The culprit in both is the "
            "Gaussian assumption: daily returns have fatter tails than any normal. Clearing houses add stress add-ons for "
            "exactly this."
        ) as vo:
            self.play(FadeIn(g), FadeIn(eb), Create(lc), FadeIn(leg))
            self.add(dot)
            self.play(FadeIn(rd), FadeIn(rd2))
            self.play(it.animate.set_value(len(path) - 1), run_time=5, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(res[0]), FadeIn(res[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x_) for x_ in res[2:]], lag_ratio=0.4))
        dot.clear_updaters()
        rd.clear_updaters()
        rd2.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def procyclical(self, m):
        rt = m["ratios"]
        d = np.asarray(m["d_2020"])
        mg = np.asarray(m["m_2020"], float)
        x = np.array([_x(v) for v in d], float)
        x = x - x[0]
        g = axes([0, x[-1]], [0, 0.16], x_length=5.6, y_length=3.2, ylabel=r"2-day margin, US market, 2020",
                 yticks=[0, 0.05, 0.1, 0.15], yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=16)
        g.to_corner(UL, buff=0.45).shift(DOWN * 0.2)
        ln = curve(g.ax, x, mg, CCP)
        rows = VGroup(*[MathTex(rf"{y}:\ {100 * rt[y]['lo']:.1f}\% \to {100 * rt[y]['hi']:.1f}\%\ (\times"
                                rf"{rt[y]['ratio']:.1f})", font_size=28, color=CCP) for y in ("1987", "2008", "2020")])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(g, DOWN, buff=0.45).align_to(g, LEFT)
        apc = wrapped_label(r"EU rules (EMIR, RTS 153/2013, Art.\ 28) make CCPs choose a tool against this: a buffer "
                            r"of at least 25\% of margin, released in stress; at least 25\% weight on stressed "
                            r"observations; or a floor from a 10-year look-back", 5.8, 19, GREY_A)
        apc.to_edge(RIGHT, buff=0.35).shift(UP * 2.2)
        c1 = crisis_card(r"8 March 2022", r"LME nickel", r"The three-month nickel price more than doubled within "
                         r"hours; the London Metal Exchange suspended trading and cancelled that morning's trades. "
                         r"In March 2025 the FCA fined the LME \pounds 9.2 million over its systems and controls.",
                         width=5.8, font_size=18)
        c2 = crisis_card(r"September 2022", r"UK pension funds (LDI)", r"Long gilt yields rose by more than a "
                         r"percentage point in days; leveraged pension hedges faced collateral calls they met by "
                         r"selling gilts, until the Bank of England stepped in to buy.", width=5.8, font_size=18)
        VGroup(c1, c2).arrange(DOWN, buff=0.2).next_to(apc, DOWN, buff=0.25).align_to(apc, LEFT)
        q = desk_question(r"A faster-reacting margin model: is the market safer?", r"the CCP is; its members get "
                          r"their biggest calls on the worst day", width=6.0, font_size=20)
        q.to_corner(DL, buff=0.3)
        with self.voiceover(
            f"And the bite: within the year, this model's margin rose {rt['1987']['ratio']:.1f}-fold in 1987, "
            f"{rt['2008']['ratio']:.1f}-fold in 2008, {rt['2020']['ratio']:.1f}-fold in 2020. It asks for cash exactly when "
            "cash is scarce. <bookmark mark='a'/> European rules make clearing houses add a damper: a releasable buffer, "
            "weight on stressed history, or a ten-year floor. <bookmark mark='b'/> When calls outrun markets, things break: "
            "LME nickel in March 2022, trading suspended and trades cancelled, later fined; British pension funds' gilt "
            "hedges that September, until the Bank of England bought. Pause and predict: is a faster margin model safer?"
        ) as vo:
            self.play(FadeIn(g), Create(ln, run_time=2))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.4))
            vo.wait_until("a")
            self.play(FadeIn(apc))
            vo.wait_until("b")
            self.play(FadeIn(c1, shift=UP * 0.2))
            self.play(FadeIn(c2, shift=UP * 0.2))
            self.play(FadeIn(q))
        self.wait(1.0)
        self.clear_scene()
