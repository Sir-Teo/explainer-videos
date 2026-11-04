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
        with self.voiceover("For the researcher: Chapter 3 found momentum across stocks, industries and time. Why does "
                            "it work? An exact accounting identity splits a momentum strategy's average profit into three "
                            "pieces, each a different story. Here it is, applied to ninety-four years of industries."):
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
                why(r"the identity holds with sample means and covariances, so the three parts add up to the realized "
                    r"average profit exactly")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Take the simplest momentum strategy. <bookmark mark='a'/> Each month, weight every asset by how far its "
            "formation return beat the average: long winners, short losers, in proportion. <bookmark mark='b'/> Andrew "
            "Lo and Craig MacKinlay showed in 1990 that its average profit is exactly three terms. Own persistence: "
            "an asset's own past predicting its own future. Lead-lag: other assets' pasts predicting it, entering with "
            "a minus sign, so negative cross-serial covariance helps. And the dispersion of means: some assets simply "
            "earn more on average, and they tend to be the winners. <bookmark mark='c'/> With sample moments the "
            "identity is exact."
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
            "Check the bookkeeping on a world where we know the answer: thirty assets with persistent idiosyncratic "
            "returns, a common factor that moves all of them together, and a spread of average returns. "
            "<bookmark mark='a'/> The estimated own-persistence term matches its theoretical value, the lead-lag term "
            "is zero as it should be, and the dispersion term is the variance of the means."
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
                p0, p1 = ax.c2p(x0 - 0.12, 0), ax.c2p(x0 + 0.12, np.clip(v, -900, 1000))
                gp.add(Rectangle(width=p1[0] - p0[0], height=max(abs(p1[1] - p0[1]), 0.01), stroke_width=0,
                                 fill_color=col, fill_opacity=0.9).move_to((p0 + p1) / 2))
            gp.add(label(name + r" formation", font_size=17, color=GREY_A).next_to(ax.c2p(k, -900), DOWN, buff=0.12))
            groups.add(gp)
        leg = legend([(OWN, r"own persistence"), (CROSS, r"lead--lag (minus cross-serial covariance)"),
                      (DISP, r"dispersion of means")], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        r1, r12 = t["results"]["1-month"], t["results"]["12-1"]
        side = wrapped_label(rf"Ken French's industries with a full history ({t['N']} of 49), monthly, "
                             rf"{str(t['first'])[:4]}--{str(t['last'])[:4]}; as \$1-long, \$1-short strategies: "
                             rf"{100 * r1['annual_mean']:.1f}\% a year (Sharpe {r1['sharpe']:.2f}) and "
                             rf"{100 * r12['annual_mean']:.1f}\% (Sharpe {r12['sharpe']:.2f})", 3.3, 14, GREY_A).next_to(
            leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Now the industries, from 1926. <bookmark mark='a'/> With a one-month formation period, own persistence "
            "is huge, nine times the whole profit, and lead-lag almost cancels it: industries continue their own "
            "last month, but follow others' last month too. <bookmark mark='b'/> With the classic twelve-month "
            "formation, skipping a month, the picture flips. An industry's own past year predicts slightly lower "
            "returns: the own term is negative. All of the profit, and more, comes from the lead-lag term, negative "
            "cross-serial covariance. <bookmark mark='c'/> And the dispersion of means, the idea that momentum just buys "
            "assets that always earn more, contributes about five percent."
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
        foot = wrapped_label(r"standard errors from a block bootstrap (24-month blocks, 400 draws). The profit is "
                             r"significant; its components individually are not, because own and cross terms are large and "
                             r"negatively correlated", 11.4, 16, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "With standard errors. <bookmark mark='a'/> The profits themselves are clearly positive: the twelve-month "
            "strategy's t-statistic is above three. <bookmark mark='b'/> But the components, individually, are not "
            "significant: the own and lead-lag terms are large, noisy, and move against each other. The decomposition "
            "is exact; what it can tell us from ninety-four years is less precise than it looks."
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
            desk_question(r"Conrad and Kaul (1998)", r"argued that most momentum profit is the dispersion of mean returns, "
                          r"which would make it a risk premium in disguise; Jegadeesh and Titman (2002) showed their tests "
                          r"overstated it", width=12.4, font_size=19),
            desk_question(r"Lewellen (2002)", r"found that momentum in size, value and industry portfolios comes from "
                          r"negative cross-serial covariance, excess covariance among assets, rather than own "
                          r"autocorrelation: what the industries show here", width=12.4, font_size=19),
            desk_question(r"what it means", r"if winners outperform because news about other assets reaches them slowly, "
                          r"momentum is about the speed at which information spreads across assets, Part 7's lead--lag, "
                          r"not about any one asset's own trend", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "How to read it. <bookmark mark='a'/> Jennifer Conrad and Gautam Kaul argued in 1998 that most momentum "
            "profit is the dispersion of means, which would make it a risk premium in disguise; Narasimhan Jegadeesh and "
            "Sheridan Titman showed their tests overstated that part. Here it is five percent. <bookmark mark='b'/> "
            "Jonathan Lewellen found in 2002 that momentum in size, value and industry portfolios comes from negative "
            "cross-serial covariance, not own autocorrelation. The industries agree. <bookmark mark='c'/> If so, "
            "momentum is about how slowly information spreads across assets, Part 7's lead-lag, rather than any one "
            "asset's own trend."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
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
            desk_question(r"open: is the lead--lag stable?", r"if cross-serial covariances are the source, they should be "
                          r"traded away over time; whether they have shrunk since the 1990s is not settled", width=12.4,
                          font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> With thousands of stocks the cross-serial terms are a huge, noisy "
            "matrix; finding which links carry the profit, supply chains or shared analysts, is ongoing. "
            "<bookmark mark='b'/> The identity splits the mean; momentum's crashes live in its higher moments, and a "
            "matching decomposition of its risk is not standard. <bookmark mark='c'/> And if lead-lag is the source, it "
            "should be traded away; whether it has shrunk since the nineties is not settled."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
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
