from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant30.common import BAD, EST_C, EW_C, GOOD, HRP_C, HURDLE, PART, RMT_C, RP_C, SHRINK_C, fit_right, load

SHOW = [("1/N", EW_C), ("sample tangency", EST_C), ("sample GMV", BAD), ("long-only GMV", QC.OPTION),
        ("LW const-corr GMV", SHRINK_C), ("nonlinear GMV", GOOD), ("RMT-clipped GMV", RMT_C), ("ERC", RP_C),
        ("HRP", HRP_C)]


class OneOverN(VoiceoverScene):
    def construct(self):
        r = load("rolling")
        self.card()
        self.dgu()
        self.table(r, "120")
        self.risk(r)
        self.costs(r)
        self.window(r)
        self.combos()
        self.question()

    def card(self):
        c = chapter_card(2, r"The humble 1/N", r"Can any optimizer beat dividing the money equally?", part=PART)
        with self.voiceover("Chapter two. The simplest rule needs no estimates at all: divide the money equally. Can any "
                            "optimizer beat it out of sample?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def dgu(self):
        card = firm_card(r"DeMiguel, Garlappi and Uppal (2009)", r"`Optimal versus naive diversification: how inefficient "
                         r"is the 1/N portfolio strategy?', \textit{Review of Financial Studies}: fourteen optimizers, "
                         r"from sample mean-variance to Bayesian and constrained versions, against equal weights on seven "
                         r"data sets",
                         numbers=((r"0", r"of the fourteen consistently beat 1/N in Sharpe ratio or certainty equivalent"),
                                  (r"\approx 3{,}000", r"months of data the sample mean-variance rule would need to beat "
                                                       r"1/N with 25 assets; about 6,000 with 50")),
                         source=r"RFS 22 (2009)", kind=r"Paper file", width=10.6, font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "In 2009 Victor DeMiguel, Lorenzo Garlappi and Raman Uppal ran the contest Part twenty-three previewed. "
            "<bookmark mark='a'/> Fourteen optimizers, from the plain sample rule to Bayesian and constrained versions, "
            "against equal weights on seven data sets. None beat one over N consistently. <bookmark mark='b'/> Their "
            "calibration: the sample mean-variance rule would need about three thousand months of data to beat it with "
            "twenty-five assets, and about six thousand with fifty. That is two hundred and fifty, and five hundred, "
            "years."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def table(self, r, W):
        res = r["res"][W]
        hx = [-4.2, -0.9, 1.4, 3.6, 5.6]
        head = VGroup(label(r"rule", font_size=17, color=GREY_B), label(r"Sharpe ratio", font_size=17, color=GREY_B),
                      label(r"volatility", font_size=17, color=GREY_B), label(r"turnover / month", font_size=17,
                                                                               color=GREY_B),
                      label(r"gross", font_size=17, color=GREY_B))
        tab = VGroup(head)
        for n, col in SHOW:
            x = res[n]
            tab.add(VGroup(label(n, font_size=18, color=col), MathTex(f"{x['sharpe']:.2f}", font_size=24),
                           MathTex(rf"{100 * x['vol']:.1f}\%", font_size=24),
                           MathTex(rf"{100 * x['turnover']:.0f}\%", font_size=24), MathTex(f"{x['gross']:.1f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.7 - 0.52 * j, 0])
        foot = wrapped_label(rf"the 49 industries, rebalanced monthly on the trailing {W} months, 1980--2020, before "
                             r"costs; turnover: half target-weight changes, excluding drift and financing; gross: absolute weights", 11.4, 15, GREY_A
                             ).to_edge(DOWN, buff=0.35)
        ew, tan = res["1/N"], res["sample tangency"]
        lw, nl = res["LW const-corr GMV"], res["nonlinear GMV"]
        with self.voiceover(
            f"""Our retrospective rolling comparison uses forty-nine industries, 1980 through 2020, with ten-year trailing windows. <bookmark mark='a'/> Equal weights have annualised Sharpe {ew['sharpe']:.2f}; the saved normalised sample inverse-covariance mean direction has {tan['sharpe']:.2f}, with target-weight turnover {100 * tan['turnover']:.0f} percent a month. Normalisation can reverse its positive-Sharpe direction and produce high gross exposure. <bookmark mark='b'/> Constant-correlation and nonlinear GMV record {lw['sharpe']:.2f} and {nl['sharpe']:.2f}. These selected research comparisons do not prove that estimated means always fail or identify a future winner."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:3]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[3:]], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def risk(self, r):
        res = r["res"]["120"]
        names = [n for n, _ in SHOW if n not in ("sample tangency",)]
        cols = dict(SHOW)
        ym = float(np.ceil(max(100 * res[n]["vol"] for n in names) / 5) * 5)
        g = axes([-0.5, len(names) - 0.5], [0, ym], x_length=9.6, y_length=4.2, xlabel=r"",
                 ylabel=r"volatility, a year, \%", xticks=[], yticks=[0, ym / 2, ym], font_size=15).move_to(LEFT * 0.4 + DOWN * 0.1)
        ax = g.ax
        pred = VGroup()
        real = VGroup()
        labs = VGroup()
        for k, n in enumerate(names):
            v, pv = 100 * res[n]["vol"], 100 * res[n]["pred_vol"]
            real.add(Rectangle(width=0.32, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                               fill_color=cols[n], fill_opacity=0.85).move_to(ax.c2p(k + 0.18, 0), aligned_edge=DOWN))
            pred.add(Rectangle(width=0.32, height=max(ax.c2p(0, pv)[1] - ax.c2p(0, 0)[1], 0.01), stroke_color=cols[n],
                               stroke_width=1.5, fill_opacity=0).move_to(ax.c2p(k - 0.18, 0), aligned_edge=DOWN))
            labs.add(label(n.replace(" GMV", ""), font_size=13, color=cols[n]).rotate(PI / 6).next_to(ax.c2p(k, 0), DOWN,
                                                                                                       buff=0.3))
        leg = legend([(GREY_A, r"outlined: trailing sample-covariance risk of each rule"), (GREY_A, r"filled: what it had")],
                     font_size=15).to_corner(UR, buff=0.35)
        sg = res["sample GMV"]
        with self.voiceover(
            f"""Compare a common trailing-window risk metric with realised risk. <bookmark mark='a'/> Outlined bars apply the sample covariance to every rule's weights, even when a different covariance estimator chose those weights. Filled bars measure the following monthly portfolio returns. Sample GMV records {100 * sg['pred_vol']:.1f} percent against {100 * sg['vol']:.1f}. This is not each shrinkage estimator reporting its own forecast, nor a proof that every inverted matrix always understates risk. The research theorem studies a narrower fixed Gaussian model."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(labs))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in pred], lag_ratio=0.1))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in real], lag_ratio=0.1))
        self.wait(0.4)
        self.clear_scene()

    def costs(self, r):
        res = r["res"]["120"]
        names = ["1/N", "LW const-corr GMV", "nonlinear GMV", "long-only GMV", "HRP", "sample GMV"]
        hx = [-3.8, -0.8, 1.6, 4.2]
        head = VGroup(label(r"rule, 10-year windows", font_size=18, color=GREY_B), label(r"gross", font_size=18, color=GREY_B),
                      label(r"net at 10 bp", font_size=18, color=GREY_B), label(r"net at 50 bp", font_size=18, color=GREY_B))
        tab = VGroup(head)
        cols = dict(SHOW)

        def net(x, bp):
            m = x["mean"] - 2 * x["turnover"] * bp / 1e4 * 12
            return m / x["vol"]
        for n in names:
            x = res[n]
            tab.add(VGroup(label(n, font_size=18, color=cols[n]), MathTex(f"{x['sharpe']:.2f}", font_size=24),
                           MathTex(f"{net(x, 10):.2f}", font_size=24), MathTex(f"{net(x, 50):.2f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.2 - 0.62 * j, 0])
        foot = wrapped_label(r"Sharpe ratios; fixed cost per target-weight change; omits drift, financing and impact. 10 and 50 bp "
                             r"are chosen sensitivity assumptions, not measured implementation costs", 11.4, 15,
                             GREY_A).to_edge(DOWN, buff=0.4)
        sg, lw = res["sample GMV"], res["LW const-corr GMV"]
        lw10, lw50, sg50 = net(lw, 10), net(lw, 50), net(sg, 50)
        with self.voiceover(
            f"""A fixed cost sensitivity, not a complete net backtest. <bookmark mark='a'/> Charge ten or fifty basis points on absolute target-weight changes and subtract the average charge from the mean, keeping gross volatility in the denominator. Shrunk GMV's proxy Sharpe is {lw10:.2f} or {lw50:.2f}; sample GMV reaches {sg50:.2f} at fifty basis points. The turnover proxy omits drift between rebalances, financing and impact. Fixed equal weights therefore show zero target-change cost even though maintaining them can require trading. Actual net Sharpe also depends on the time path of costs."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.25))
        self.wait(0.4)
        self.clear_scene()

    def window(self, r):
        a, b = r["res"]["60"], r["res"]["120"]
        rows = VGroup()
        for n in ("sample GMV", "LW const-corr GMV", "nonlinear GMV", "1/N"):
            rows.add(VGroup(label(n, font_size=20, color=dict(SHOW)[n]),
                            MathTex(rf"{100 * a[n]['vol']:.1f}\%", font_size=26), MathTex(rf"{100 * b[n]['vol']:.1f}\%",
                                                                                         font_size=26)))
        head = VGroup(label(r"realised volatility", font_size=18, color=GREY_B), label(r"5-year window", font_size=18,
                                                                                       color=GREY_B),
                      label(r"10-year window", font_size=18, color=GREY_B))
        tab = VGroup(head, *rows)
        hx = [-3.4, 1.0, 3.8]
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.8 * j, 0])
        sa, sb = a["sample GMV"]["vol"], b["sample GMV"]["vol"]
        la, lb = a["LW const-corr GMV"]["vol"], b["LW const-corr GMV"]["vol"]
        with self.voiceover(
            f"""Window length changes the noise and recency trade-off. <bookmark mark='a'/> Here sample GMV's annualised realised volatility is {100 * sa:.1f} percent with sixty months and {100 * sb:.1f} with a hundred and twenty. Constant-correlation shrinkage records {100 * la:.1f} and {100 * lb:.1f}. This research sample shows less sensitivity after shrinkage; it does not guarantee that a short window is safe or optimal when covariance changes."""
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def combos(self):
        cards = VGroup(
            desk_question(r"Kan and Zhou (2007): a three-fund rule", r"hold cash, the estimated tangency portfolio and the "
                          r"estimated minimum-variance portfolio, with weights chosen to minimise the expected loss from "
                          r"estimation error: the minimum-variance fund absorbs much of the tangency fund's noise",
                          width=12.4, font_size=19),
            desk_question(r"Tu and Zhou (2011): combine with 1/N", r"a weighted average of 1/N and an optimizer, the weight "
                          r"chosen from the data, beats both parts in their simulations: shrinkage of the weights toward a "
                          r"fixed weight target that needs no estimated means or covariance", width=12.4, font_size=19),
            desk_question(r"the common thread", r"every fix shrinks something toward something simpler: the means, the "
                          r"covariance, or the weights themselves", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label(r"Neither the optimizer nor 1/N alone: combine them", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "If neither the optimizer nor one over N is right, combine them. <bookmark mark='a'/> Raymond Kan and Guofu Zhou "
            "proposed in 2007 a three-fund rule: cash, the estimated tangency portfolio, and the estimated minimum-variance "
            "portfolio, mixed to minimise the expected loss from estimation error. <bookmark mark='b'/> Jun Tu and Zhou "
            "then combined an optimizer directly with one over N, with the mixing weight chosen from the data. "
            "<bookmark mark='c'/> The common thread runs through the whole part: every fix shrinks something toward "
            "something simpler, whether the means, the covariance or the weights themselves."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"1/N uses no mean or covariance estimate. Which exposure and implementation risks can still "
                       r"matter?")
        with self.voiceover(
            'Pause and predict. Equal money needs no estimated expected-return or covariance inputs. Which exposures, asset-selection and implementation risks does that leave unresolved?'
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
