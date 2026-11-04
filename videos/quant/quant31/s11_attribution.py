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
                why(r"what is left: the return from picking assets, after every factor is accounted for")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Multiply the factor model by the holdings. <bookmark mark='a'/> The book's return is a sum, over factors, of "
            "its exposure times the factor's return, plus the specific part. The identity holds exactly, every day. "
            "<bookmark mark='b'/> Each factor's contribution is exposure times return. <bookmark mark='c'/> The specific "
            "part is the return from picking assets after every factor is accounted for: the part a factor ETF cannot "
            "replicate."
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
                cmath(r"\text{selection}", r"=", r"\textstyle\sum_s w^P_s\,(R^P_s - R^B_s)", font_size=34,
                      colors={r"\text{selection}": SPEC_C})]
        whys = [why(r"Brinson, Hood and Beebower (1986): over- or under-weighting sectors that beat the benchmark"),
                why(r"picking better stocks within each sector; the factor model generalises both to any set of factors")]
        step = ladder(self, rows, whys, keep=2, top=2.2, x=-0.3, buff=0.7, edge=6.9)
        with self.voiceover(
            "Traditional managers know an older version. <bookmark mark='a'/> Gary Brinson and coauthors split a fund's "
            "return over its benchmark into allocation, from over-weighting the sectors that did well, "
            "<bookmark mark='b'/> and selection, from picking better stocks within each sector. The factor model "
            "generalises both: sectors become any factors, and selection becomes the specific return."
        ) as vo:
            vo.wait_until("a")
            step(0)
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
        head = label(r"Part 29's mined alpha, 2018--2020: return a year, by source", font_size=26).to_edge(UP, buff=0.3)
        foot = wrapped_label(rf"total {100 * a['mean_total']:.0f}\% a year, gross; the long--short rank book of the formula "
                             r"ts\_mean(ts\_min(vwap/high, 5), 20) on the coins, attributed daily with Chapter 2's model",
                             11.8, 16, GREY_A).to_edge(DOWN, buff=0.3)
        vol = vals["volatility"]
        with self.voiceover(
            "Now apply it to the best signal of Part twenty-nine, the mined alpha that beat every combination in Chapter "
            "seven. <bookmark mark='a'/> Over the research years it earned "
            f"{100 * a['mean_total']:.0f} percent a year before costs. <bookmark mark='b'/> Of that, {100 * vol:.0f} "
            "percent came from the volatility factor: the book was short the volatile coins, and the volatility factor "
            "lost heavily. The other factors roughly cancel. <bookmark mark='c'/> The specific return, the part that "
            f"is the formula's own, was {100 * a['mean_specific']:.1f} percent a year."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(foot))
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
                 ylabel=r"cumulative return, \%", xticks=[], yticks=[lo, 0, hi], font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        c1 = curve(ax, x, tot, IC_C, stroke_width=3)
        c2 = curve(ax, x, fac, FAC_C, stroke_width=3)
        c3 = curve(ax, x, spec, SPEC_C, stroke_width=3)
        leg = legend([(IC_C, r"the book"), (FAC_C, r"its factor part"), (SPEC_C, r"its specific part")], font_size=17)
        leg.to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        fit_right(leg)
        st = VGroup(label(rf"Sharpe of the book: {a['sharpe_total']:.2f}", font_size=17, color=IC_C),
                    label(rf"Sharpe of the specific part: {a['sharpe_specific']:.2f}", font_size=17, color=SPEC_C),
                    label(rf"factor share of variance: {100 * a['var_share_factor']:.0f}\%", font_size=17, color=FAC_C))
        st.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        fit_right(st)
        with self.voiceover(
            "Day by day. <bookmark mark='a'/> The book, and its factor part, which tracks it almost exactly. "
            "<bookmark mark='b'/> And the specific part, which rose for a while and then gave almost all of it back. <bookmark mark='c'/> The book's Sharpe ratio "
            f"was {a['sharpe_total']:.2f}; its specific part's, {a['sharpe_specific']:.2f}. Factors carried "
            f"{100 * a['var_share_factor']:.0f} percent of its variance."
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
            desk_question(r"what the search found", r"a new way to be short volatile coins: the low-volatility factor, "
                          r"repackaged as a formula", width=12.4, font_size=19),
            desk_question(r"why it matters", r"a factor can be bought cheaply and sized deliberately; paying a mining "
                          r"budget, a trial count and a stock picker's fee for it is paying twice", width=12.4, font_size=19),
            desk_question(r"the remedy", r"mine on residuals: neutralise each candidate to the risk model's factors before "
                          r"scoring it, so only specific skill is rewarded", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What attribution teaches. <bookmark mark='a'/> The search of Part twenty-nine found a new way to be short "
            "volatile coins: the low-volatility factor, repackaged as a formula. <bookmark mark='b'/> A factor can be "
            "held cheaply and sized deliberately; paying a mining budget and a trial count for it is paying twice. "
            "<bookmark mark='c'/> The remedy is to mine on residuals: neutralise every candidate to the risk model's "
            "factors before scoring it, so that only skill the factors cannot explain is rewarded."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def timing(self):
        rows = [cmath(r"\tfrac1T\textstyle\sum_t e_{k,t}\,f_{k,t+1}", r"=", r"\bar e_k\,\bar f_k + "
                      r"\widehat{\operatorname{Cov}}(e_{k,t},\,f_{k,t+1})", font_size=34),
                cmath(r"\bar e_k\,\bar f_k", r":", r"\text{static exposure, the factor's premium}", font_size=30,
                      colors={r"\bar e_k\,\bar f_k": FAC_C}),
                cmath(r"\operatorname{Cov}", r":", r"\text{timing: more exposure before good factor days}", font_size=30,
                      colors={r"\operatorname{Cov}": HURDLE})]
        whys = [why(r"the average contribution of factor $k$, with exposure $e_{k,t} = (h_t^\top X_t)_k$, splits exactly"),
                why(r"the part a constant exposure would have earned"),
                why(r"the part that comes from varying the exposure at the right times: a claim of skill in timing")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "One more split. <bookmark mark='a'/> A factor's average contribution is the average exposure times the "
            "average factor return, plus the covariance between them. <bookmark mark='b'/> The first part is what a "
            "constant exposure would have earned: a premium, cheaply replicated. <bookmark mark='c'/> The second is "
            "timing: having more exposure just before the factor's good days. A manager who claims to time factors "
            "should show it in that term."
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
                why(r"by factor: the exposure times the covariance of the factor with the whole book"),
                why(r"a contribution can be negative: a position that hedges the rest of the book")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Return is attributed; so is risk. <bookmark mark='a'/> Volatility is homogeneous of degree one in the "
            "holdings, so Euler's theorem splits it exactly into contributions that add up: each holding times its "
            "marginal risk. Part thirty's risk parity used the same split. <bookmark mark='b'/> Group the terms by "
            "factor, and each factor's share is the book's exposure to it times its covariance with the whole book. "
            "<bookmark mark='c'/> A contribution can be negative: that position hedges the rest. The daily risk report "
            "is this table, next to the return attribution."
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
