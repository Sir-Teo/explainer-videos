from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import BAD, COIN, GOOD, HURDLE, LINEAR, MOM, NET, PART, TREE, ask, comma, fit_right, illustration, load


class Toolkit(VoiceoverScene):
    def construct(self):
        t = load("toolkit")
        self.card()
        self.bars(t)
        self.fracdiff(t["fracdiff"])
        self.barrier()
        self.meta(t["meta"])
        self.unique(t["uniqueness"])
        self.question()

    def card(self):
        c = chapter_card(12, r"The practitioner's toolkit", r"Which of the tricks pay for themselves?", lit=(2018,),
                         part=PART)
        with self.voiceover('Chapter twelve. Practitioner tools: activity sampling, finite fractional filters, daily-close labels and concurrency weights, each with explicit implementation limits.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def bars(self, t):
        e = np.linspace(-6, 6, 61)
        c = (e[:-1] + e[1:]) / 2
        panels = VGroup()
        for k, title, col in (("time", r"daily bars", LINEAR), ("dollar", r"dollar bars", TREE)):
            h = np.asarray(t[k]["hist"], float)
            h = h / t[k]["n"] / (e[1] - e[0])
            top = max(.45,float(h.max())*1.15)
            g = axes([-6, 6], [0, top], x_length=5.4, y_length=3.0, xlabel=r"standardised return", ylabel=r"density",
                     xticks=[-6, -3, 0, 3, 6], yticks=[0,round(top/2,2),round(top,2)], font_size=12)
            ax = g.ax
            w = ax.c2p(e[1], 0)[0] - ax.c2p(e[0], 0)[0]
            bars = VGroup(*[Rectangle(width=w * 0.9, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0,
                                      fill_color=col, fill_opacity=0.75).move_to(
                [ax.c2p(x, 0)[0], (ax.c2p(0, v)[1] + ax.c2p(0, 0)[1]) / 2, 0]) for x, v in zip(c, h) if v > 0])
            xs = np.linspace(-6, 6, 200)
            nrm = curve(ax, xs, np.exp(-xs ** 2 / 2) / np.sqrt(2 * np.pi), WHITE, stroke_width=2)
            cap = VGroup(label(title, font_size=20, color=col),
                         MathTex(rf"\text{{excess kurtosis}}\ {t[k]['kurt']:.1f}", font_size=22)).arrange(RIGHT, buff=0.3)
            panels.add(VGroup(cap, VGroup(g, bars, nrm)).arrange(DOWN, buff=0.15))
        panels.arrange(RIGHT, buff=0.6).move_to(UP * 0.2)
        foot = wrapped_label(rf"Original hourly close-times-volume proxy: {comma(t['time']['n'])} daily returns, {comma(t['dollar']['n'])} activity-bar returns. Displayed histogram window runs from -6 to +6 SD; outside counts: {int(t['time']['n']-sum(t['time']['hist']))} daily, {int(t['dollar']['n']-sum(t['dollar']['hist']))} activity. Densities use full sample counts; omitted tails are not normality evidence.",12.4,22,GREY_A).to_edge(DOWN,buff=.3)
        foot2 = None
        head = label(r"Tool 1: the clock", font_size=30).to_edge(UP, buff=0.45)
        with self.voiceover(
            f"The original changes the sampling clock. <bookmark mark='a'/> It uses hourly base volume times close as a traded-value proxy and closes an activity bar when a cumulative threshold is crossed. Multiple crossings inside one hour collapse to one observed end, so the bar count need not match the daily count. These are activity bars, not imbalance or run bars. <bookmark mark='b'/> Saved excess kurtosis is {t['dollar']['kurt']:.2f} for activity bars and {t['time']['kurt']:.2f} for daily returns. Both can remain fat-tailed. The saved histogram omits observations outside six standard deviations; their counts are disclosed. Squared-return autocorrelations are {t['dollar']['ac_sq']:.3f} and {t['time']['ac_sq']:.3f}, without a universal claim that the sampling scheme removes clustering."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2),FadeIn(panels[0]))
            vo.wait_until("a")
            self.wait(.1)
            vo.wait_until("b")
            self.play(FadeIn(panels[1]), FadeIn(foot))
        self.add(illustration(r"Binance BTCUSDT hourly; the House's \texttt{ml.dollar\_bars}", corner=UR))
        self.wait(0.4)
        self.clear_scene()

    def fracdiff(self, f):
        ds, adf, cor = np.asarray(f["d"]), np.asarray(f["adf"]), np.asarray(f["corr"])
        lo=float(np.floor(min(adf.min(),f["crit"])-1));hi=float(np.ceil(max(adf.max(),0)+1))
        g = axes([0, 1], [lo, hi], x_length=6.0, y_length=4.0, xlabel=r"differencing order $d$",
                 ylabel=r"ADF statistic", xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=list(np.linspace(lo,hi,5)), font_size=13).to_edge(
            LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        la = curve(ax, ds, adf, NET, stroke_width=3)
        crit = DashedLine(ax.c2p(0, f["crit"]), ax.c2p(1, f["crit"]), color=HURDLE, stroke_width=2)
        corlo=min(0,float(cor.min())-.05);corhi=max(1.0,float(cor.max())+.05)
        g2 = axes([0, 1], [corlo, corhi], x_length=4.8, y_length=4.0, xlabel=r"differencing order $d$",
                  ylabel=r"correlation with the price", xticks=[0, 0.5, 1.0], yticks=list(np.linspace(corlo,corhi,5)), font_size=13).to_edge(
            RIGHT, buff=0.6).shift(DOWN * 0.3)
        lc = curve(g2.ax, ds, cor, COIN, stroke_width=3)
        k = int(np.flatnonzero(adf < f["crit"])[0])
        dot1 = Dot(ax.c2p(ds[k], adf[k]), color=GOOD, radius=0.08)
        dot2 = Dot(g2.ax.c2p(ds[k], cor[k]), color=GOOD, radius=0.08)
        rows = [cmath(r"(1 - L)^d x_t", r"=", r"\textstyle\sum_{k \ge 0} w_k\, x_{t-k},\quad w_k = -w_{k-1}\frac{d - k + 1}{k}",
                      font_size=32, colors={r"(1 - L)^d x_t": NET})]
        rows[0].to_edge(UP, buff=0.4)
        foot = wrapped_label(rf"Finite truncated filters and a fixed-lag-one ADF diagnostic. First sampled crossing: d={ds[k]:.1f}, correlation {cor[k]:.2f}; critical value {f['crit']:.2f}. Selecting d after checking many values does not certify stationarity, memory preservation or predictive value.",12.0,23,GREY_A).to_edge(DOWN,buff=.25)
        with self.voiceover(
            f"Fractional filtering requires careful interpretation. <bookmark mark='a'/> The infinite fractional-difference weights have polynomial decay for a noninteger order, but this implementation truncates them. Prices need not have a unit root and ordinary returns need not be stationary. <bookmark mark='b'/> The first sampled order crossing the fixed-lag ADF threshold is {ds[k]:.1f}, with correlation {cor[k]:.2f} to log price; the order-one correlation is {cor[-1]:.2f}. A correlation is not a preserved-memory fraction. Fixed critical values and selecting among several orders do not certify stationarity or useful forecasting information."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(g), FadeIn(g2), Create(crit))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Create(la), Create(lc), run_time=2)
            self.play(FadeIn(dot1), FadeIn(dot2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def barrier(self):
        rng = np.random.default_rng(4)
        P = 100 * np.exp(np.cumsum(rng.normal(0.002, 0.02, 40)))
        i0, h = 8, 20
        up, dn = P[i0] * 1.08, P[i0] * 0.92
        lo, hi = float(min(P.min(), dn) * .95), float(max(P.max(), up) * 1.08)
        g = axes([0, 39], [lo, hi], x_length=8.0, y_length=4.0, xlabel=r"days",
                 ylabel=r"price", xticks=[0,10,20,30,39], yticks=list(np.linspace(lo,hi,5)), font_size=18).move_to(LEFT * 1.4 + DOWN * 0.3)
        ax = g.ax
        line = curve(ax, np.arange(40), P, COIN, stroke_width=3)
        box = VGroup(Line(ax.c2p(i0, up), ax.c2p(i0 + h, up), color=GOOD, stroke_width=2.5),
                     Line(ax.c2p(i0, dn), ax.c2p(i0 + h, dn), color=BAD, stroke_width=2.5),
                     Line(ax.c2p(i0 + h, dn), ax.c2p(i0 + h, up), color=HURDLE, stroke_width=2.5))
        hit = int(np.flatnonzero((P[i0 + 1:i0 + h + 1] >= up) | (P[i0 + 1:i0 + h + 1] <= dn))[0]) + i0 + 1 if \
            np.any((P[i0 + 1:i0 + h + 1] >= up) | (P[i0 + 1:i0 + h + 1] <= dn)) else i0 + h
        dot = Dot(ax.c2p(hit, P[hit]), color=GOOD if P[hit] >= up else (BAD if P[hit] <= dn else HURDLE), radius=0.09)
        side = VGroup(label(r"upper: take profit $(+1)$", font_size=18, color=GOOD),
                      label(r"lower: stop loss $(-1)$", font_size=18, color=BAD),
                      label(r"vertical: time's up (the sign then)", font_size=18, color=HURDLE),
                      wrapped_label('Empirical helper uses daily closes, arithmetic price thresholds and timeout return signs. Intraday crossing and executable fills are not modelled; volatility scaling does not equalise all risks.', 3.4, 15, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)
        stamp=illustration(r"Fixed simulated path; not market data")
        with self.voiceover(
            "Triple barriers define a target rather than a complete execution model. <bookmark mark='a'/> The fixed illustration shows upper, lower and timeout boundaries. The unchanged empirical helper checks daily closes and arithmetic price changes; recent volatility sets the scale, and a timeout receives the realised return's sign, rather than always zero. Intraday crossings, executable fills and costs are absent. Volatility scaling does not guarantee equal risk in calm and stressed markets."
        ) as vo:
            self.play(FadeIn(g), Create(line),FadeIn(stamp))
            vo.wait_until("a")
            self.play(Create(box), FadeIn(side), run_time=1.5)
            self.play(FadeIn(dot, scale=1.5))
        self.wait(0.4)
        self.clear_scene()

    def meta(self, m):
        rows = VGroup(
            MathTex(r"\text{primary: the side}\ \ s_t = \operatorname{sign}(P_t / P_{t-20} - 1)", font_size=30, color=MOM),
            MathTex(r"\text{secondary: }\ \Pr(\text{side matches barrier/timeout sign}\mid\text{features}) > \tfrac12 ?",
                    font_size=30, color=TREE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.6)
        hx = [-3.6, 1.0, 4.4]
        head = VGroup(label(r"Bitcoin, held-out period", font_size=18, color=GREY_B), label(r"every bet", font_size=18, color=MOM),
                      label(r"meta-labelled", font_size=18, color=TREE))
        data = [(r"bets taken", r"100\%", rf"{100 * m['taken']:.0f}\%"),
                (r"precision (barrier hit in the bet's favour)", rf"{100 * m['precision_primary']:.0f}\%",
                 rf"{100 * m['precision_meta']:.0f}\%"),
                (r"mean per opportunity, \%", rf"{100 * m['mean_primary']:.1f}", rf"{100 * m['mean_meta']:.1f}"),
                (r"its standard deviation, \%", rf"{100 * m['sd_primary']:.1f}", rf"{100 * m['sd_meta']:.1f}"),
                (r"mean / sd", rf"{m['mean_primary'] / m['sd_primary']:.2f}", rf"{m['mean_meta'] / m['sd_meta']:.2f}")]
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(label(a, font_size=18, color=GREY_A), MathTex(b, font_size=24),
                                                 MathTex(c, font_size=24)) for a, b, c in data]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.0 - 0.6 * j, 0])
            row[0].align_to(np.array([hx[0] - 3.0, 0, 0]), LEFT)
            tab.add(row)
        foot = wrapped_label('Original daily-close Bitcoin illustration. Training labels are not purged at the split; opportunities overlap; gross log payoffs omit costs. The boosted meta-model does not use uniqueness weights.', 12.0, 17, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"Meta-labelling here filters a fixed momentum side. <bookmark mark='a'/> Its target is whether the side matches the daily-close barrier or timeout sign, not merely whether a profit barrier was hit. The original training split does not purge crossing label spans, and its boosted fit does not use uniqueness weights. <bookmark mark='b'/> The saved filter keeps {100*m['taken']:.1f} percent of opportunities. Precision is {100*m['precision_primary']:.1f} percent before filtering and {100*m['precision_meta']:.1f} afterward. Per-opportunity mean-to-standard-deviation ratios are {m['mean_primary']/m['sd_primary']:.3f} and {m['mean_meta']/m['sd_meta']:.3f}. These gross, overlapping opportunities are not an executable independent portfolio track record."
        ) as vo:
            self.play(FadeIn(rows))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def unique(self,u):
        cards=VGroup(desk_question(r"What concurrency weights measure",rf"{comma(u['n'])} labels; mean uniqueness {u['mean']:.3f}; sum {u['effective']:.1f}. This sum is not an independent sample count.",width=12.0,font_size=25),desk_question(r"Inclusive endpoints matter",r"For fixed spans $[i,i+h]$, interior concurrency is $h+1$, so uniqueness is $1/(h+1)$. Early barrier endings and edges change it.",width=12.0,font_size=25),desk_question(r"What inference still needs",r"Dependence, return covariance and the estimator determine uncertainty. The original meta-classifier does not use these weights.",width=12.0,font_size=25)).arrange(DOWN,buff=.35)
        if cards.height>6.8:cards.scale_to_fit_height(6.8)
        with self.voiceover(f"Uniqueness measures average inverse label concurrency. The saved {u['n']} labels have mean weight {u['mean']:.3f} and sum {u['effective']:.1f}. This is not an equivalent number of independent observations. For inclusive fixed spans from i to i plus h, interior concurrency is h plus one, giving uniqueness one over h plus one. Half-open spans use a different convention. Early barriers and sample edges alter the average. Dependence and the estimator still determine standard errors, and the original meta-classifier does not use these weights."):
            self.play(FadeIn(cards))
        self.clear_scene()

    def question(self):
        q = ask(r"a secondary model doubles the precision of your bets but takes only one bet in ten. When is that "
                r"better than taking every bet, and how would you decide before trading?")
        with self.voiceover(
            "Pause and predict. A secondary model doubles the precision of your bets, but takes only one bet in ten. "
            "When is that better than taking every bet, and how would you decide before trading?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
