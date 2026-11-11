from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant24.common import BAD, GOOD, HML, MKT, PART, UMD, load

OWN, CROSS, DISP = UMD, HML, GREY_B


class Research(VoiceoverScene):
    def construct(self):
        t = load("momentum_decomposition")
        self.card()
        self.identity()
        self.sim(t)
        self.bars(t)
        self.table(t)
        self.reading()
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Where momentum profits come from", r"Is momentum persistence, lead--lag, or just some assets "
                          r"always earning more?", part=PART)
        with self.voiceover('For the researcher: an exact sample accounting identity splits this weighted momentum strategy into three components. The original industry calculation selects forty complete-history columns from forty-nine using the entire 1926-to-2020 window. This is a retrospective survivor-selected panel, not a point-in-time investable universe.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def identity(self):
        rows = [cmath(r"w_{i,t}", r"=", r"\tfrac1N\big(x_{i,t} - \bar x_t\big),\qquad \pi_{t} = \sum_i w_{i,t}\,r_{i,t}", font_size=30,
                      colors={r"w_{i,t}": UMD}),
                cmath(r"\bar\pi", r"=", r"\underbrace{\tfrac{N-1}{N^2}\sum_i \widehat{\operatorname{Cov}}(x_i, r_i)}_{\text{own "
                      r"persistence}}\ \underbrace{-\ \tfrac{1}{N^2}\sum_{i \ne j}\widehat{\operatorname{Cov}}(x_j, r_i)}_{\text{lead--lag}}"
                      r"\ +\ \underbrace{\tfrac1N\sum_i (\bar x_i - \bar x)(\bar r_i - \bar r)}_{\text{dispersion of means}}",
                      font_size=24, colors={r"\bar\pi": GOOD}),
                cmath(r"\text{exact}", r":", r"\text{in sample moments, no approximation}", font_size=28)]
        whys = [why(r"the weighted relative-strength strategy: long assets whose formation return $x$ beat the average, "
                    r"short the losers, in proportion"),
                why(r"Lo and MacKinlay (1990): expand $\frac1N\sum_i \bar{x_i r_i} - \bar x\bar r$ into covariances and means. An "
                    r"asset's own past predicting its future; other assets' pasts predicting it (entering with a minus); "
                    r"and assets with high average returns staying winners"),
                why('covariance denominator $T$ makes the accounting exact. Log formation signals, simple holding returns; scaled exposure is constant through time, not normalised monthly')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Define the weighted relative-strength strategy. <bookmark mark='a'/> Formation signals are sums of log returns; holding returns are simple returns, with demeaned signals divided by the asset count. <bookmark mark='b'/> The mean profit splits into own covariance, negative cross-serial covariance and a covariance of asset means. These are sample accounting components, not identified economic causes. <bookmark mark='c'/> Use covariance denominator T for exact equality. The displayed scale is one constant chosen to make average long exposure one, not monthly unit-gross normalisation."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def sim(self, t):
        s = t["sim"]
        e, th = s["estimate"], s["theory"]
        hx = [-3.6, 0.4, 3.6]
        head = VGroup(label(r"simulated check", font_size=18, color=GREY_B), label(r"estimate", font_size=20),
                      label(r"theory", font_size=20))
        rows = [(r"own persistence", e["own"], th["own"], OWN), (r"lead--lag", e["cross"], th["cross"], CROSS),
                (r"dispersion of means", e["disp"], th["disp"], DISP)]
        tab = VGroup(head)
        for name, a_, b_, col in rows:
            tab.add(VGroup(label(name, font_size=19, color=col), MathTex(rf"{1e4 * a_:.2f}", font_size=26),
                           MathTex(rf"{1e4 * b_:.2f}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.5 - 0.75 * j, 0])
            row[0].align_to(np.array([hx[0] - 2.4, 0, 0]), LEFT)
        foot = wrapped_label(rf"{s['n']} assets, {s['T']:,} periods: a common factor, independent AR(1) idiosyncratic parts "
                             rf"with $\phi = {s['phi']}$, and means spread from $-0.2\%$ to $0.4\%$; in units of $10^{{-4}}$ per "
                             r"period; theory: $\frac{N-1}{N^2}\cdot N\phi\sigma_e^2/(1 - \phi^2)$, zero, and the means' variance",
                             11.4, 16, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Check a fixed simulation with thirty assets, equal unit loadings on one iid common factor, independent AR-one idiosyncratic parts, and dispersed means. <bookmark mark='a'/> Demeaned zero-sum weights cancel the equal-loading factor path by path. Population lead-lag contribution is zero in this setup, while finite-sample estimates need not be exactly zero. Own persistence and mean dispersion approach the stated population values; unequal loadings or serially dependent factors would change the argument."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def bars(self, t):
        g = axes([-0.6, 1.6], [-900, 1000], x_length=7.6, y_length=4.4, xlabel=r"", ylabel=r"share of the average profit, \%",
                 xticks=[], yticks=[-800, -400, 0, 400, 800], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.1)
        ax = g.ax
        zero = Line(ax.c2p(-0.6, 0), ax.c2p(1.6, 0), color=GREY_C, stroke_width=1.5)
        groups = VGroup()
        for k, name in enumerate(("1-month", "12-1")):
            r = t["results"][name]
            vals = [100 * r["own"] / r["mean"], 100 * r["cross"] / r["mean"], 100 * r["disp"] / r["mean"]]
            gp = VGroup()
            for m_, (v, col) in enumerate(zip(vals, (OWN, CROSS, DISP))):
                x0 = k + (m_ - 1) * 0.28
                p0, p1 = ax.c2p(x0 - 0.12, 0), ax.c2p(x0 + 0.12, v)
                gp.add(Rectangle(width=p1[0] - p0[0], height=max(abs(p1[1] - p0[1]), 0.01), stroke_width=0,
                                 fill_color=col, fill_opacity=0.9).move_to((p0 + p1) / 2))
            gp.add(label(name + r" formation", font_size=17, color=GREY_A).next_to(ax.c2p(k, -900), DOWN, buff=0.12))
            groups.add(gp)
        leg = legend([(OWN, r"own persistence"), (CROSS, r"lead--lag (minus cross-serial covariance)"),
                      (DISP, r"dispersion of means")], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        r1, r12 = t["results"]["1-month"], t["results"]["12-1"]
        side = wrapped_label(f"Ken French's industries with a full history ({t['N']} of 49), monthly, {str(t['first'])[:4]}--{str(t['last'])[:4]}; constant scaling to average long exposure 1, not each month: {100 * r1['annual_mean']:.1f}\\% a year (Sharpe {r1['sharpe']:.2f}) and {100 * r12['annual_mean']:.1f}\\% (Sharpe {r12['sharpe']:.2f})", 3.3, 14, GREY_A).next_to(
            leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The original forty-industry panel begins in July 1926. <bookmark mark='a'/> For one-month log formation, large own and cross components nearly offset. <bookmark mark='b'/> The second rule sums twelve formation months and skips one; it differs from the classic eleven-month prior-twelve-through-two signal. Its own term is negative and its cross term dominates this sample. <bookmark mark='c'/> Mean dispersion contributes a small positive share. Large offsetting shares are algebraic descriptions, not a causal information network."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(leg), FadeIn(side))
            vo.wait_until("a")
            self.play(FadeIn(groups[0]))
            vo.wait_until("b")
            self.play(FadeIn(groups[1]))
            vo.wait_until("c")
            self.play(Indicate(groups[1][2], color=WHITE))
        self.wait(0.4)
        self.clear_scene()

    def table(self, t):
        hx = [-4.2, -1.4, 1.2, 3.6, 5.8]
        head = VGroup(label(r"$10^{-4}$ a month, $\pm$ s.e.", font_size=17, color=GREY_B), label(r"profit", font_size=20, color=GOOD),
                      label(r"own", font_size=20, color=OWN), label(r"lead--lag", font_size=20, color=CROSS),
                      label(r"means", font_size=20, color=DISP))
        tab = VGroup(head)
        for name in ("1-month", "12-1"):
            r, se = t["results"][name], t["results"][name]["se"]
            tab.add(VGroup(label(name + r" formation", font_size=19),
                           *[MathTex(rf"{1e4 * r[k]:+.2f}\ (\pm {1e4 * se[k]:.2f})", font_size=22)
                             for k in ("mean", "own", "cross", "disp")]))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.2 - 0.8 * j, 0])
            row[0].align_to(np.array([hx[0] - 2.2, 0, 0]), LEFT)
        foot = wrapped_label('Original 400-draw, 24-month nonwrapping bootstrap; final possible start omitted. Profit/error ratio is a finite-sample diagnostic; noisy offsetting components do not establish causal attribution or selection-robust inference', 11.4, 16, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The preserved standard errors use four hundred block resamples, twenty-four contiguous months per block, with no wrapping; the code excludes the final possible block start. <bookmark mark='a'/> The saved profit-to-bootstrap-error ratio for the twelve-month rule exceeds three. This is a finite bootstrap diagnostic, not universal robust inference. <bookmark mark='b'/> Individual components are noisy and offset one another. Complete-history selection, block choice, serial dependence and multiple comparisons limit interpretation; exact bookkeeping does not make causal attribution precise."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def reading(self):
        cards = VGroup(
            desk_question(r"Conrad and Kaul (1998)", 'attributed much momentum profit to dispersed mean returns; estimator and sampling bias were debated by Jegadeesh and Titman (2002). Mean dispersion alone does not identify a risk premium', width=12.4, font_size=19),
            desk_question(r"Lewellen (2002)", r"found that momentum in size, value and industry portfolios comes from "
                          r"negative cross-serial covariance, excess covariance among assets, rather than own "
                          r"autocorrelation: what the industries show here", width=12.4, font_size=19),
            desk_question(r"what it means", 'slow information diffusion is one possible interpretation, not identified by this identity. Mean dispersion is not proof of a risk premium; cross-serial covariance is not a causal news network', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Read the components with care. <bookmark mark='a'/> Mean dispersion in these selected industries is not proof of a risk premium; earlier papers disagree about its contribution in other designs. <bookmark mark='b'/> Negative cross-serial covariance contributes strongly here, consistent with the cited portfolio evidence, but definitions and samples differ. <bookmark mark='c'/> Slow information diffusion is one possible mechanism. The identity alone cannot identify news transmission, supply-chain links or a causal lead-lag network."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: individual stocks", r"with thousands of stocks the cross-serial terms are a huge, noisy "
                          r"matrix; estimating which links carry the profit (supply chains, analysts) is ongoing", width=12.4,
                          font_size=18),
            desk_question(r"open: decomposing risk, not only return", r"the identity splits the mean; momentum's crashes "
                          r"(Chapter 4) live in its higher moments, and a matching decomposition of its variance and skew "
                          r"is not standard", width=12.4, font_size=18),
            desk_question(r"open: is the lead--lag stable?", 'stability depends on risks, costs, information and arbitrage limits. A covariance pattern is not guaranteed to vanish when published', width=12.4,
                          font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> Which links help describe the noisy cross-serial covariance matrix, and what extra evidence could identify a causal transmission channel? <bookmark mark='b'/> The identity attributes a mean; explaining variance, skewness and rebound crashes requires additional modelling. <bookmark mark='c'/> Does a pattern persist after costs, risk and arbitrage limits? Publication alone need not eliminate it. Stability tests need genuinely separated data and a prespecified design."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"two assets with no autocorrelation, but asset 1's return this month predicts asset 2's next month "
                       r"positively. Does the relative-strength strategy make or lose money from this, and which term "
                       r"records it?")
        with self.voiceover(
            "Pause and predict. Two assets, no autocorrelation, but asset one's return this month predicts asset two's "
            "next month, positively. Does the strategy make or lose money from that, and which term records it?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
