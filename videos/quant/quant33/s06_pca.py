from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant33.common import BAD, COST_C, FAC_C, GOOD, HURDLE, OU_C, PART, RES_C, fit_right, load


class Residuals(VoiceoverScene):
    def construct(self):
        p = load("pca")
        self.card()
        self.idea()
        self.eigen()
        self.residual()
        self.refine()
        self.paths(p)
        self.configs(p)
        self.scatter(p)
        self.periods(p)
        self.costs(p)
        self.netting()
        self.question()

    def card(self):
        c = chapter_card(5, r"Eigenportfolios and residuals", r"What if every asset is paired with the whole market at "
                         r"once?", part=PART)
        with self.voiceover('Chapter five. Avellaneda and Lee studied factor residuals instead of isolated pairs. We examine an industry proxy, keeping its original calculations fixed and separating synthetic residual statistics from executable wealth.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def idea(self):
        rows = [cmath(r"r_{i,t}", r"=", r"\textstyle\sum_k \beta_{ik} F_{k,t} + u_{i,t}", font_size=38,
                      colors={r"F_{k,t}": FAC_C, r"u_{i,t}": RES_C}),
                cmath(r"X_{i,t}", r"=", r"\textstyle\sum_{s\le t} u_{i,s}", font_size=38, colors={r"X_{i,t}": RES_C}),
                cmath(r"X_{i,t}", r"\sim", r"\text{OU}\ \Rightarrow\ s_{i,t} = (X_{i,t} - \hat\theta_i)/\hat s_{\text{eq},i}",
                      font_size=32)]
        whys = [why(r"each asset's return is its exposure to a few common factors plus a residual: Part 31's risk model, "
                    r"with factors taken from the data"),
                why(r"the cumulative residual: the asset's price, with the factors removed"),
                why(r"model it as Chapter 4's OU process and trade its s-score: a pair with the whole market")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The idea. <bookmark mark='a'/> Write each asset's return as exposures to a few common factors, plus a "
            "residual: Part thirty-one's risk model, with the factors taken from the data. <bookmark mark='b'/> Add up "
            "the residuals: that is the asset's price with the market, sectors and styles removed. "
            "<bookmark mark='c'/> Treat it as an Ornstein-Uhlenbeck spread and trade its s-score. Each asset becomes a "
            "pair with the whole market, and there is no screening of pairs at all."
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

    def eigen(self):
        rows = [cmath(r"C", r"=", r"\operatorname{Corr}(r_{t-251}, \dots, r_t) = V\Lambda V^\top", font_size=36),
                cmath(r"Q^{(k)}_i", r"=", r"\frac{v^{(k)}_i}{\hat\sigma_i}", font_size=38, colors={r"Q^{(k)}_i": FAC_C}),
                cmath(r"F_{k,t}", r"=", r"\textstyle\sum_i Q^{(k)}_i r_{i,t}", font_size=36)]
        whys = [why(r"the correlation matrix of the last year's daily returns, and its eigenvectors (Part 30's spectrum)"),
                why(r"an eigenportfolio: invest in proportion to the eigenvector divided by each asset's volatility"),
                why(r"its return is a factor; the first is the market, the next ones sectors and styles")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The factors are eigenportfolios. <bookmark mark='a'/> Take the correlation matrix of the last year's daily "
            "returns and its eigenvectors, Part thirty's spectrum again. <bookmark mark='b'/> Invest in each eigenvector, "
            "scaled by each asset's volatility. <bookmark mark='c'/> The first eigenportfolio is the market; the next "
            "few are sectors and styles. On the forty-nine industries the House keeps five, re-estimated every month."
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

    def residual(self):
        rows = [cmath(r"r_{i}", r"=", r"\alpha_i + \beta_i^\top F + u_i\ \ \text{on the last 60 days}", font_size=34),
                cmath(r"\text{trade}", r":", r"\text{long } i \text{ and short } \beta_i^\top Q \text{ when } s_i < -1.25",
                      font_size=32, colors={r"\text{trade}": RES_C}),
                cmath(r"\text{proxy}", r"=", r"\text{position} \times u_{i,t+1}\ \ \text{(synthetic fitted residual)}",
                      font_size=30)]
        whys = [why(r"each day, regress each industry on the five factor returns over a 60-day window"),
                why(r"a factor hedge removes fitted factor exposure; the cumulative OLS residual has a constrained endpoint"),
                why(r"intercept removal, changing fitted weights and financing prevent an automatic cash-flow interpretation")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The implementation matters. <bookmark mark='a'/> Regress each industry on five factors with an intercept over the last sixty observations. The factors use trailing two hundred fifty-two day correlations through the current close, refitted every twenty-one days. <bookmark mark='b'/> The intercept makes fitted residuals sum to approximately zero in each window. Their cumulative path is therefore tied down at its endpoint: apparent reversion can partly be a fitting constraint. <bookmark mark='c'/> Tomorrow's synthetic residual subtracts the fitted intercept as well as factor returns. A stock-minus-factor hedge does not automatically earn that subtracted intercept. Its weights also need financing and rebalancing. These statistics are a diagnostic proxy, not verified cash-flow profit."
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

    def refine(self):
        cards = VGroup(
            desk_question(r"how many factors", r"Avellaneda and Lee used either 15 eigenportfolios or as many as needed to "
                          r"explain 55\% of the variance, and also tried sector ETFs as factors; Part 30's spectrum says "
                          r"the eigenvalues above the noise edge are the ones worth keeping", width=12.4, font_size=19),
            desk_question(r"drift in the residual", r"they adjust the s-score for the residual's own drift, "
                          r"$s - \alpha/(\kappa\,\hat s_{\text{eq}})$, so a residual that is trending is not mistaken "
                          r"for one that is stretched", width=12.4, font_size=19),
            desk_question(r"trading time", r"measured in volume rather than days, residuals revert more cleanly: they "
                          r"report a volume-adjusted version did better than the plain one", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Avellaneda and Lee's own refinements. <bookmark mark='a'/> How many factors? They used fifteen "
            "eigenportfolios, or as many as explain fifty-five percent of the variance, and also tried sector funds as "
            "factors; Part thirty's spectrum keeps the eigenvalues above the noise edge. <bookmark mark='b'/> They "
            "adjust the s-score for the residual's own drift, so a residual that is trending is not mistaken for one "
            "that is stretched. <bookmark mark='c'/> And they measure time in traded volume rather than days, which, "
            "they report, made the residuals revert more cleanly."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def paths(self, p):
        d = np.asarray(p["dates"], float)
        x = d // 10000 + ((d // 100) % 100 - 0.5) / 12
        al = p["al"]
        yg, yn = 100 * np.asarray(al["cum_gross"], float), 100 * np.asarray(al["cum"], float)
        lo = float(np.floor(min(yg.min(), yn.min()) / 20) * 20)
        hi = float(np.ceil(max(yg.max(), yn.max()) / 20) * 20)
        g = axes([x[0], x[-1]], [lo, hi], x_length=7.4, y_length=4.4, xlabel=r"1994--2020",
                 ylabel=r"cumulative proxy P\&L, \% of active-signal gross", xticks=[1995, 2005, 2015], yticks=[lo, 0, hi],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        n = min(len(x), len(yg))
        c1 = curve(ax, x[:n], yg[:n], RES_C, stroke_width=3)
        c2 = curve(ax, x[:n], yn[:n], COST_C, stroke_width=3)
        zero = DashedLine(ax.c2p(x[0], 0), ax.c2p(x[-1], 0), color=GREY_C, stroke_width=1)
        leg = legend([(RES_C, r"before costs"), (COST_C, r"after the 5 bp cost proxy")], font_size=16).to_edge(RIGHT, buff=0.4)
        leg.shift(UP * 1.6)
        fit_right(leg)
        st = VGroup(label(rf"Sharpe, gross: {al['gross']['sharpe']:.2f}", font_size=16, color=RES_C),
                    label(rf"Sharpe, net: {al['net']['sharpe']:.2f}", font_size=16, color=COST_C))
        st.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        fit_right(st)
        ga, na = al["gross"], al["net"]
        self.add(g, c1, zero, leg)
        with self.voiceover(
            f"The stored industry proxy, with Avellaneda and Lee's thresholds. <bookmark mark='a'/> Before its cost charge, the annualized synthetic mean is {100 * ga['mean']:.1f} percent, with Sharpe {ga['sharpe']:.2f}. <bookmark mark='b'/> With its five-basis-point, two-leg turnover proxy, the mean is {100 * na['mean']:+.1f} percent and Sharpe {na['sharpe']:.2f}. The normalization is the number of active industry signals, not the total gross capital of industry and hedge positions. Cumulative lines add these synthetic daily values. Positive gross performance does not by itself establish economically tradable reversion."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(c1), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(st), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    def configs(self, p):
        cf = p["configs"]
        keys = [k for k in cf if not k.endswith("theory")]
        hx = [-4.4, -2.0, 0.4, 2.8, 5.0]
        head = VGroup(label(r"factors / window / open band", font_size=16, color=GREY_B),
                      label(r"Sharpe, gross", font_size=16, color=RES_C), label(r"Sharpe, net", font_size=16, color=COST_C),
                      label(r"daily turnover", font_size=16, color=GREY_B), label(r"vol", font_size=16, color=GREY_B))
        tab = VGroup(head)
        for k in keys + ["5f/60d/theory"]:
            r = cf[k]
            name = k.replace("f/", " factors, ").replace("d/", " days, ").replace("theory", "research band")
            tab.add(VGroup(label(name, font_size=17, color=HURDLE if k.endswith("theory") else WHITE),
                           MathTex(f"{r['gross']['sharpe']:.2f}", font_size=22), MathTex(f"{r['sharpe']:.2f}", font_size=22),
                           MathTex(rf"{100 * r['turnover']:.0f}\%", font_size=22),
                           MathTex(rf"{100 * r['vol']:.1f}\%", font_size=22)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.7 - 0.5 * j - (0.15 if j == len(tab) - 1 else 0), 0])
        foot = wrapped_label(rf"1994--2020, the research years; all {p['n_trials']} rules reuse this research sample "
                             r"(evaluation protocol in Chapter 10)", 11.0, 16, GREY_A).to_edge(DOWN, buff=0.35)
        th = cf["5f/60d/theory"]
        best_g = max(keys, key=lambda k: cf[k]["gross"]["sharpe"])
        bg, bn = cf[best_g]["gross"]["sharpe"], cf[best_g]["sharpe"]
        bt = 100 * cf[best_g]["turnover"]
        self.add(tab[0], tab[1], foot)
        with self.voiceover(
            f"Nine stored research configurations: eight combinations of factor count, fitting window and entry threshold, plus the mathematical band. <bookmark mark='a'/> The best gross configuration has sample Sharpe {bg:.2f}. <bookmark mark='b'/> Its charged proxy Sharpe is {bn:.2f}, with discrete-signal turnover {bt:.0f} percent daily. <bookmark mark='c'/> The research-band proxy has charged Sharpe {th['sharpe']:.2f}, and turnover {100 * th['turnover']:.0f} percent. It was added after the earlier comparisons. All nine share data and modeling choices. This comparison is neither independent confirmation of the band nor an executable cost audit; no new registration or sealed evaluation is performed here."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1])) for r_ in tab[1:-1]], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[2:])) for r_ in tab[1:-1]], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(FadeIn(tab[-1], shift=UP * 0.1))
            self.play(Indicate(tab[-1][2], color=GOOD))
        self.wait(0.4)
        self.clear_scene()

    def scatter(self, p):
        cf = p["configs"]
        tv = np.array([100 * cf[k]["turnover"] for k in cf])
        sh = np.array([cf[k]["sharpe"] for k in cf])
        gs = np.array([cf[k]["gross"]["sharpe"] for k in cf])
        g = axes([5, 40], [-1.2, 1.6], x_length=7.4, y_length=4.4, xlabel=r"daily turnover, \% of gross",
                 ylabel=r"Sharpe ratio, 1994--2020", xticks=[10, 20, 30, 40], yticks=[-1, 0, 1], font_size=15)
        g.move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(5, 0), ax.c2p(40, 0), color=GREY_C, stroke_width=1)
        dg = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=RES_C) for a, b in zip(tv, gs)])
        dn = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=COST_C) for a, b in zip(tv, sh)])
        links = VGroup(*[Line(ax.c2p(a, b), ax.c2p(a, c), color=GREY_D, stroke_width=1) for a, b, c in zip(tv, gs, sh)])
        b1, b0 = np.polyfit(tv, sh, 1)
        fit = Line(ax.c2p(5, b0 + 5 * b1), ax.c2p(40, b0 + 40 * b1), color=COST_C, stroke_width=2, stroke_opacity=0.7)
        leg = legend([(RES_C, r"before costs"), (COST_C, r"after costs")], font_size=16).to_edge(RIGHT, buff=0.4)
        leg.shift(UP * 1.6)
        fit_right(leg)
        st = wrapped_label(rf"each 10 points of turnover cost about {abs(10 * b1):.2f} of Sharpe", 3.8, 16, GREY_A)
        st.next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        fit_right(st)
        gm, gsd = float(gs.mean()), float(gs.std())
        self.add(g, dg, zero, leg)
        with self.voiceover(
            "All nine rules on one picture. <bookmark mark='a'/> Before costs they are bunched together, Sharpe ratios "
            f"around {gm:.1f}. <bookmark mark='b'/> After costs they fall onto a line in turnover: every ten points of "
            f"daily turnover cost about {abs(10 * b1):.2f} of Sharpe ratio. The choice of factors and windows moves a rule "
            "a little up or down; how much it trades moves it along the line, and that is what decides the sign."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dg], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(Create(links), LaggedStart(*[FadeIn(d_) for d_ in dn], lag_ratio=0.1))
            self.play(Create(fit), FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def periods(self, p):
        pg, pn = p["periods_gross"], p["periods"]
        hx = [-3.4, -0.6, 2.2]
        head = VGroup(label(r"the research-band proxy", font_size=18, color=GREY_B), label(r"Sharpe, gross", font_size=18,
                                                                                     color=RES_C),
                      label(r"Sharpe, net", font_size=18, color=COST_C))
        tab = VGroup(head)
        for k in pg:
            tab.add(VGroup(label(k.replace("-", "--"), font_size=20), MathTex(f"{pg[k]['sharpe']:.2f}", font_size=26),
                           MathTex(f"{pn[k]['sharpe']:.2f}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.4 - 0.85 * j, 0])
        foot = wrapped_label(r"five eigenportfolios, 60-day residuals, the research chapter's band; Avellaneda and Lee "
                             r"report their stock version strongest before the early 2000s", 11.0, 16, GREY_A)
        foot.to_edge(DOWN, buff=0.6)
        k0 = list(pg)
        g0, g1, g2 = pg[k0[0]]["sharpe"], pg[k0[1]]["sharpe"], pg[k0[2]]["sharpe"]
        n0, n1, n2 = pn[k0[0]]["sharpe"], pn[k0[1]]["sharpe"], pn[k0[2]]["sharpe"]
        self.add(tab[0], tab[1], foot)
        with self.voiceover(
            "By era, for the research-band proxy. <bookmark mark='a'/> Before costs, Sharpe ratios of "
            f"{g0:.2f}, {g1:.2f} and {g2:.2f}: strongest in the 1990s, weakest from 2003 to 2010, and partly back "
            "after. <bookmark mark='b'/> After costs, "
            f"{n0:.2f}, {n1:.2f} and {n2:.2f}. Almost all of the net profit was earned in the first era. The same "
            "costs that are a small tax on a strong premium wipe out a weak one."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1])) for r_ in tab[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_[2]) for r_ in tab[1:]], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def costs(self, p):
        cards = VGroup(
            desk_question(r"the stored cost proxy", r"twice a fixed one-way rate times discrete-signal changes divided by the new active count; no full hedge reconstruction",
                          width=12.4, font_size=19),
            desk_question(r"missing turnover", r"active-count changes rescale held weights; an empty new book omits its exit charge. Both need explicit accounting", width=12.4,
                          font_size=19),
            desk_question(r"no proven conservative direction", r"net actual hedge holdings and charge financing, borrow and impact; omitted costs and separate-hedge overcharges can offset unpredictably", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "The cost proxy has three important limits. <bookmark mark='a'/> It charges twice a fixed one-way rate times changes in discrete signals divided by the new active count. It does not reconstruct each hedge trade. <bookmark mark='b'/> When that count changes, held positions are rescaled, but those trades are missing from the turnover measure. When the new book is empty, the code sets net profit to zero and omits the final exit charge even if signals changed. <bookmark mark='c'/> These omissions can understate costs; separate hedges can overstate them before netting. The combined error has no proven conservative direction. The original financial algorithm is preserved, and the lesson labels its output as a proxy."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def netting(self):
        rows = [cmath(r"h_i", r"=", r"-w_i\, \beta_i^\top Q", font_size=36, colors={r"h_i": FAC_C}),
                cmath(r"\textstyle\sum_i |\Delta h_i|", r"\ \ge\ ", r"\big|\Delta \textstyle\sum_i h_i\big|", font_size=36),
                cmath(r"\text{net hedge}", r"=", r"-\Big(\textstyle\sum_i w_i \beta_i\Big)^\top Q", font_size=34,
                      colors={r"\text{net hedge}": GOOD})]
        whys = [why(r"each position's own factor hedge: a short basket of eigenportfolios"),
                why(r"the triangle inequality: trading each hedge separately costs at least as much as trading their "
                    r"sum, and usually much more, because hedges of longs and shorts cancel"),
                why(r"a desk holds one net hedge for the whole book; a full accounting must reconstruct each position and hedge; the "
                    r"current proxy has no established conservative direction")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "For actual holdings, netting has a useful algebraic bound. <bookmark mark='a'/> Each industry position suggests a factor hedge. <bookmark mark='b'/> The triangle inequality says the absolute trade in their sum cannot exceed the sum of absolute separate trades, for the same holdings and linear unit costs. <bookmark mark='c'/> This does not validate the stored turnover proxy, which never reconstructs those hedge holdings and omits some rebalancing and exits. Full cash-flow accounting, borrow, financing, impact and actual tradable factor exposures are prerequisites for a net-performance claim."
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

    def question(self):
        q = pause_card(r"a residual book earns a gross Sharpe of 0.8 at 4\% volatility and turns over 20\% of its gross "
                       r"daily. At 5 bp a side on both legs, what is left?")
        working = MathTex('\\mu_g=S_g\\sigma=0.8(0.04),\\qquad \\mathrm{TC}=2(5\\cdot10^{-4})(0.2)(252)', font_size=32).move_to(UP * 0.8)
        if working.width > 12.1:
            working.scale_to_fit_width(12.1)
        setup_note = wrapped_label('A chosen two-leg, constant-turnover illustration. Subtract deterministic costs from the annual mean; unchanged volatility is a further approximation.', 11.7, 23).move_to(DOWN * 0.9)
        self.add(working, setup_note, q)
        with self.voiceover(
            "Pause and predict. A residual book earns a gross Sharpe ratio of point eight at four percent volatility, "
            "and turns over twenty percent of its gross every day. At five basis points a side on both legs, what is "
            "left?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
