from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant31.common import BAD, FAC_C, GOOD, HURDLE, IC_C, PART, SPEC_C, fit_right, load

FCOL = {"size": QC.SPOT, "beta": QC.DELTA, "volatility": QC.LOSS, "momentum": QC.GAIN, "reversal": QC.OPTION}


class Attribution(VoiceoverScene):
    def construct(self):
        a = load("attribution")
        self.card()
        self.identity()
        self.brinson()
        self.bars(a)
        self.paths(a)
        self.reading(a)
        self.timing()
        self.risk_split()
        self.question()

    def card(self):
        c = chapter_card(10, r"P\&L attribution", r"Where did the money come from?", part=PART)
        with self.voiceover("Chapter ten. Every morning a risk desk answers one question about yesterday: where did the "
                            "money come from? The factor model answers it exactly."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def identity(self):
        rows = [cmath(r"h^\top r_{t+1}", r"=", r"\textstyle\sum_k \underbrace{(h^\top X_t)_k}_{\text{exposure}}\,f_{k,t+1} "
                      r"+ h^\top u_{t+1}", font_size=34, colors={r"h^\top u_{t+1}": SPEC_C}),
                cmath(r"\text{factor } k", r":", r"(h^\top X_t)_k\, f_{k,t+1}", font_size=34, colors={r"\text{factor } k": FAC_C}),
                cmath(r"\text{specific}", r":", r"h^\top u_{t+1} = \textstyle\sum_i h_i u_{i,t+1}", font_size=34,
                      colors={r"\text{specific}": SPEC_C})]
        whys = [why(r"multiply the model of Chapter 2 by the holdings: the identity holds exactly, every day"),
                why(r"each factor's contribution: the book's exposure to it, times the factor's return"),
                why(r"residual relative to this fitted factor set; not automatically skill, causation or an unspanned tradable payoff")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Multiply the fitted return identity by aligned holdings. <bookmark mark='a'/> Portfolio return is factor exposures times realised factor returns plus residual return, exactly as accounting for that model. <bookmark mark='b'/> Each factor contribution is exposure times return. <bookmark mark='c'/> Specific return means residual relative to this factor set; omitted factors, noise and fitting choices remain. It is not automatically selection skill or a payoff no traded instrument could replicate."
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

    def brinson(self):
        rows = [cmath(r"\text{allocation}", r"=", r"\textstyle\sum_s (w^P_s - w^B_s)\,(R^B_s - R^B)", font_size=34,
                      colors={r"\text{allocation}": IC_C}),
                cmath(r"\text{selection + interaction}", r"=", r"\textstyle\sum_s w^P_s\,(R^P_s - R^B_s)", font_size=34,
                      colors={r"\text{selection}": SPEC_C})]
        whys = [why(r"Brinson-style benchmark-relative allocation; sector weights sum to one in both portfolios"),
                why(r"picking better stocks within each sector; the factor model generalises both to any set of factors")]
        step = ladder(self, rows, whys, keep=2, top=2.2, x=-0.3, buff=0.7, edge=6.9)
        with self.voiceover(
            "An older benchmark-relative accounting split. <bookmark mark='a'/> Allocation uses sector weight differences times benchmark-sector return minus total benchmark return. With fully allocated sector weights it is the displayed allocation identity. <bookmark mark='b'/> Using portfolio weights on within-sector return differences combines selection and interaction. Other Brinson conventions separate those terms. Factor attribution extends the accounting idea, but its factors need not be sector portfolios."
        ) as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def bars(self, a):
        keys = [k for k in a["factors"] if k != "market"]
        vals = dict(zip(a["factors"], a["mean_factor"]))
        items = [(k, vals[k], FCOL[k]) for k in keys] + [(r"specific", a["mean_specific"], SPEC_C)]
        mx = max(abs(v) for _, v, _ in items)
        sc = 4.0 / mx
        bars = VGroup()
        for j, (nm, v, col) in enumerate(items):
            y = 2.0 - 0.7 * j
            r = Rectangle(width=max(abs(v) * sc, 0.02), height=0.42, fill_color=col, fill_opacity=0.85, stroke_width=0)
            r.move_to([0.0, y, 0], aligned_edge=LEFT if v >= 0 else RIGHT)
            nm_ = label(nm, font_size=20, color=col).move_to([-4.6, y, 0])
            val = MathTex(rf"{100 * v:+.0f}\%", font_size=24).next_to(r, RIGHT if v >= 0 else LEFT, buff=0.15)
            bars.add(VGroup(nm_, r, val))
        axis = Line([0, 2.4, 0], [0, -2.5, 0], color=GREY_C, stroke_width=1.5)
        head = label(r"Part 29's selected formula: annualised arithmetic return by fitted source", font_size=26).to_edge(UP, buff=0.3)
        foot = wrapped_label(rf"total {100 * a['mean_total']:.0f}\% a year, gross; the long--short rank book of the formula "
                             r"ts\_mean(ts\_min(vwap/high, 5), 20) on the coins, attributed daily with Chapter 2's model",
                             11.8, 16, GREY_A).to_edge(DOWN, buff=0.3)
        vol = vals["volatility"]
        with self.voiceover(
            f"""Apply the accounting to the previously selected Part twenty-nine formula in the research sample. <bookmark mark='a'/> Saved gross annualised arithmetic return is {100 * a['mean_total']:.0f} percent. <bookmark mark='b'/> The volatility-factor contribution is {100 * vol:.0f} percent. The attribution uses a fitted factor basis, not a causal experiment. <bookmark mark='c'/> Residual annualised return is {100 * a['mean_specific']:.1f} percent. This residual is model dependent and is not automatically the formula's own skill."""
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(bars[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(b[0])) for b in bars], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(b[1], b[2])) for b in bars[:-1]], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(bars[-1][1], bars[-1][2])))
        self.wait(0.4)
        self.clear_scene()

    def paths(self, a):
        tot, fac, spec = (100 * np.asarray(a[k], float) for k in ("cum_total", "cum_factor", "cum_specific"))
        x = np.arange(len(tot))
        lo = float(np.floor(min(tot.min(), fac.min(), spec.min()) / 50) * 50)
        hi = float(np.ceil(max(tot.max(), fac.max(), spec.max()) / 50) * 50)
        g = axes([0, len(x)], [lo, hi], x_length=7.4, y_length=4.4, xlabel=r"days with a full factor model, 2018--2020",
                 ylabel=r"sum of daily P\&L, \%", xticks=[], yticks=[lo, 0, hi], font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        c1 = curve(ax, x, tot, IC_C, stroke_width=3)
        c2 = curve(ax, x, fac, FAC_C, stroke_width=3)
        c3 = curve(ax, x, spec, SPEC_C, stroke_width=3)
        leg = legend([(IC_C, r"the book"), (FAC_C, r"its factor part"), (SPEC_C, r"its specific part")], font_size=17)
        leg.to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        fit_right(leg)
        st = VGroup(label(rf"Sharpe of the book: {a['sharpe_total']:.2f}", font_size=17, color=IC_C),
                    label(rf"Sharpe of the specific part: {a['sharpe_specific']:.2f}", font_size=17, color=SPEC_C),
                    label(rf"factor/total variance ratio: {100 * a['var_share_factor']:.0f}\%", font_size=17, color=FAC_C))
        st.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        fit_right(st)
        with self.voiceover(
            f"""The paths are arithmetic sums of daily fitted components. <bookmark mark='a'/> Total and factor components move closely in this sample. <bookmark mark='b'/> Residual return has its own path. <bookmark mark='c'/> Saved annualised Sharpes are {a['sharpe_total']:.2f} and {a['sharpe_specific']:.2f}. Factor-component variance divided by total variance is {100 * a['var_share_factor']:.0f} percent. This ratio is not an additive risk attribution: factor--residual covariance can matter and the ratio can exceed one."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(c1), Create(c2), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(c3), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def reading(self, a):
        cards = VGroup(
            desk_question(r"what the search found", r"substantial fitted low-volatility exposure in this research sample; a model-dependent description", width=12.4, font_size=19),
            desk_question(r"why it matters", r"compare with implementable factor alternatives after costs; a fitted regression factor is not automatically cheap to trade", width=12.4, font_size=19),
            desk_question(r"the remedy", r"mine on residuals: neutralise each candidate to the risk model's factors before "
                          r"scoring it; residualisation changes the research target and requires separate validation", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Interpret the model dependence. <bookmark mark='a'/> Much of the formula's saved return aligns with the fitted low-volatility factor. <bookmark mark='b'/> An investor could compare implementable factor alternatives, including their own costs; a regression factor is not automatically a cheap investable product. <bookmark mark='c'/> Neutralising candidates before scoring is a possible future research design, not a demonstrated repair here. Residual performance still contains omitted factors and noise, and any new search needs honest validation."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2)) if k else self.play(Indicate(cards[0]))
        self.wait(0.4)
        self.clear_scene()

    def timing(self):
        rows = [cmath(r"\tfrac1T\textstyle\sum_t e_{k,t}\,f_{k,t+1}", r"=", r"\bar e_k\,\bar f_k + "
                      r"\widehat{\operatorname{Cov}}(e_{k,t},\,f_{k,t+1})", font_size=34),
                cmath(r"\bar e_k\,\bar f_k", r":", r"\text{static exposure times realised sample factor mean}", font_size=30,
                      colors={r"\bar e_k\,\bar f_k": FAC_C}),
                cmath(r"\operatorname{Cov}", r":", r"\text{timing: more exposure before good factor days}", font_size=30,
                      colors={r"\operatorname{Cov}": HURDLE})]
        whys = [why(r"the average contribution of factor $k$, with exposure $e_{k,t} = (h_t^\top X_t)_k$, splits exactly"),
                why(r"the part a constant exposure would have earned"),
                why(r"sample covariance with divisor $T$; positive timing contribution alone does not establish repeatable skill")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "One exact sample identity. <bookmark mark='a'/> Mean exposure times next-period factor return equals mean exposure times mean factor return plus their sample covariance, defined with divisor T. <bookmark mark='b'/> The first term is static exposure times the realised sample factor mean, not proof of an expected premium or cheap replication. <bookmark mark='c'/> The covariance describes timing in this sample. Repeatable timing skill requires further evidence and aligned, available exposures."
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

    def risk_split(self):
        rows = [cmath(r"\sigma(h)", r"=", r"\textstyle\sum_i h_i\,\frac{\partial\sigma}{\partial h_i} = \sum_i h_i\,"
                      r"\frac{(\Sigma h)_i}{\sigma}", font_size=34, colors={r"\sigma(h)": HURDLE}),
                cmath(r"\text{factor } k", r":", r"\frac{(h^\top X)_k\,(F X^\top h)_k}{\sigma}", font_size=34,
                      colors={r"\text{factor } k": FAC_C}),
                cmath(r"\text{marginal}", r":", r"\frac{\partial\sigma}{\partial h_i}\ \text{tells the trader which "
                      r"position adds risk}", font_size=30)]
        whys = [why(r"risk is homogeneous of degree one in the holdings, so Euler's theorem splits it exactly into "
                    r"contributions that add up (Part 30's risk parity used the same split)"),
                why(r"under factor--residual orthogonality: exposure times covariance with the factor component, divided by portfolio volatility"),
                why(r"a contribution can be negative: a position that hedges the rest of the book")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Volatility also has an Euler attribution when covariance is fixed positive semidefinite and portfolio volatility is positive. <bookmark mark='a'/> Holding times marginal volatility contributions sum to total volatility. <bookmark mark='b'/> Under factor--residual orthogonality, the displayed factor contribution is exposure times covariance with the factor component, divided by portfolio volatility. Specific contributions complete the total. <bookmark mark='c'/> Contributions can be negative for hedges. They are shares of forecast volatility in a specified covariance model, distinct from the earlier descriptive variance ratio."
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
        q = pause_card(r"a fund's return is 12\%: its average market beta is 0.4, the market returned 20\%, and the "
                       r"covariance term is 2\%. How much is selection?")
        with self.voiceover(
            "Pause and predict. A fund returned twelve percent. Its average market beta was point four, the market "
            "returned twenty percent, and the timing term was two percent. How much came from selection?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
