from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant34.common import BAD, FIRM_C, GOOD, HURDLE, PART, PNL_C, STOP_C, fit_right, load

RULES = ["10%/3m", "10%/12m", "15%/3m", "15%/12m", "20%/3m", "20%/12m"]


class Stops(VoiceoverScene):
    def construct(self):
        s = load("stops")
        self.card()
        self.setup_()
        self.null()
        self.table(s)
        self.heat(s)
        self.why_(s)
        self.trials(s)
        self.question()

    def card(self):
        c = chapter_card(10, r"Do drawdown stops help?", r"On real premia, does cutting a losing strategy pay?", part=PART)
        self.add(c)
        with self.voiceover('Chapter ten revisits an existing research calculation on six Kenneth French factors and six stop rules. No new market trial is run. We compare the cached research sample with a descriptive shuffle reference and an iid mathematical calculation. Neither establishes a universal stop benefit, a causal mechanism or a deployable after-cost strategy.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"x_t", r"=", r"\frac{10\%/\sqrt{12}}{\hat\sigma_{t,36}}\, f_t", font_size=36, colors={r"x_t": PNL_C}),
                cmath(r"\text{stop}", r":", r"\text{drawdown} > D \Rightarrow \text{flat for } w \text{ months, then restart}",
                      font_size=30, colors={r"\text{stop}": STOP_C}),
                cmath(r"D \in \{10, 15, 20\}\%,\ w \in \{3, 12\}", r":", r"\text{six rules, six factors}", font_size=30)]
        whys = [why(r"each factor (market, size, value, profitability, investment, momentum) scaled to 10\% volatility "
                    r"with the trailing three years' volatility, from 1966 to 2020"),
                why('when arithmetic drawdown strictly exceeds $D$, include that return, skip the next $w$ observations, then reset the peak'),
                why(r"stops one to two volatilities deep, and short or long time-outs: 36 combinations")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Read the exact convention. <bookmark mark='a'/> Six factor proxies use thirty-six prior finite monthly observations for volatility scaling; removing missing values can compress the clock. The research sample begins July 1966 and ends December 2020, with uncapped leverage and no trading, funding or borrowing costs. <bookmark mark='b'/> Drawdown is in arithmetic cumulative returns. The whole breach-period loss is included; exactly the next w observations are skipped with zero cash return, then the peak restarts. This differs from a compounded-wealth drawdown. <bookmark mark='c'/> Six rules across six factors reuse one sample: thirty-six dependent research comparisons."
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

    def null(self):
        rows = [cmath(r"Y=ZR,\quad p=\Pr(Z=1)", r":", r"Z\text{ predictable, independent of current iid }R", font_size=27),
                cmath(r"\operatorname{Var}(Y)", r"=", r"p\sigma^2+p(1-p)\mu^2", font_size=33),
                cmath(r"s_Y", r"=", r"\frac{\sqrt p\,s_R}{\sqrt{1+(1-p)s_R^2}}\approx\sqrt p\,s_R", font_size=33)]
        whys = [why(r"zero-return cash; mean $p\mu$; $s_R=\mu/\sigma$ is the per-period ratio"),
                why(r"the extra variance term comes from variation between cash and invested periods"),
                why(r"the approximation needs small per-period mean/noise; serial exposure dependence can affect long-run variance")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover("The iid exposure calculation has an extra variance term. <bookmark mark='a'/> Let a predictable on-off indicator be independent of the current iid return, with stationary on probability p, and assign cash zero return. Mean becomes p mu. <bookmark mark='b'/> Variance is p sigma squared plus p times one minus p times mu squared. <bookmark mark='c'/> The exact marginal per-period ratio is root p times the original ratio, divided by root one plus one minus p times the original ratio squared. Root p alone is a low-mean approximation. It lowers a positive ratio; a negative one becomes less negative. Serial exposure dependence can alter long-run variance, so annualization needs more care. Shuffling the already scaled factor is a descriptive reference, not a general calibrated iid experiment.") as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.clear_scene()

    def table(self, s):
        hx = [-4.4, -2.0, 0.4, 2.8, 5.0]
        head = VGroup(label(r"factor", font_size=17, color=GREY_B), label(r"no stop", font_size=17, color=GREY_B),
                      label(r"15\%, 12 months", font_size=17, color=STOP_C), label(r"shuffled", font_size=17,
                                                                                   color=HURDLE),
                      label(r"stops taken", font_size=17, color=GREY_B))
        tab = VGroup(head)
        for n, r in zip(s["names"], s["rows"]):
            q = r["15%/12m"]
            tab.add(VGroup(label(n, font_size=20), MathTex(f"{r['none']['sharpe']:.2f}", font_size=26),
                           MathTex(f"{q['sharpe']:.2f}", font_size=26),
                           MathTex(rf"{r['none']['sharpe'] + q['null_change']:.2f} \pm {q['null_sd']:.2f}", font_size=24),
                           MathTex(f"{q['stops']}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.4 - 0.65 * j, 0])
        start = s["start"]
        foot = wrapped_label(rf"monthly, {start // 100}-{start % 100:02d} to 2020-12; Sharpe ratios include the months "
                             r"spent flat; shuffled: the rule on 200 shuffles, mean $\pm$ sd", 11.4, 15,
                             GREY_A).to_edge(DOWN, buff=0.5)
        rv = dict(zip(s["names"], s["rows"]))
        hml, umd = rv["HML"], rv["UMD"]
        h0, h1 = hml["none"]["sharpe"], hml["15%/12m"]["sharpe"]
        u0, u1 = umd["none"]["sharpe"], umd["15%/12m"]["sharpe"]
        self.add(tab[0], tab[1], foot)
        with self.voiceover(
            f"""One existing rule uses an arithmetic fifteen-percent barrier and twelve observations out. <bookmark mark='a'/> Value's sample ratio changes from {h0:.2f} to {h1:.2f}; momentum changes from {u0:.2f} to {u1:.2f}. <bookmark mark='b'/> The shuffled column is baseline ratio plus the mean change across two hundred shuffles, with their standard deviation. That spread is not a confidence interval for future performance. Shared data, scaling, the chosen rule, finite shuffles and omitted costs limit what we can conclude."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1], r_[2], r_[4])) for r_ in tab[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_[3]) for r_ in tab[1:]], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def heat(self, s):
        Z = np.array([[r[k]["change"] - r[k]["null_change"] for k in RULES] for r in s["rows"]])
        sd = np.array([[r[k]["null_sd"] for k in RULES] for r in s["rows"]])
        cells = VGroup()
        for i, n in enumerate(s["names"]):
            for j, k in enumerate(RULES):
                z = Z[i, j]
                t = float(np.clip((z + 0.25) / 0.5, 0, 1))
                sq = Rectangle(width=1.5, height=0.62, fill_color=interpolate_color(ManimColor(RED_D), ManimColor(GREEN_D), t),
                               fill_opacity=0.85, stroke_color=GREY_D, stroke_width=1)
                sq.move_to([-3.2 + 1.55 * j, 1.8 - 0.67 * i, 0])
                star = r"^{*}" if abs(z) > 2 * sd[i, j] else ""
                cells.add(VGroup(sq, MathTex(rf"{z:+.2f}{star}", font_size=22).move_to(sq)))
        rl = VGroup(*[label(n, font_size=18).move_to([-5.3, 1.8 - 0.67 * i, 0]) for i, n in enumerate(s["names"])])
        cl = VGroup(*[label(k.replace("%", r"\%"), font_size=15, color=GREY_B).move_to([-3.2 + 1.55 * j, 2.45, 0])
                      for j, k in enumerate(RULES)])
        foot = wrapped_label('stop change less mean shuffle change; star: beyond two shuffle SDs, descriptive only; no selection adjustment', 11.0, 15, GREY_A).to_edge(DOWN, buff=0.45)
        n_pos = int(np.sum(Z > 2 * sd))
        n_neg = int(np.sum(Z < -2 * sd))
        self.add(rl, cl, cells[0], foot)
        with self.voiceover(
            f"""The heatmap shows all thirty-six dependent research comparisons. <bookmark mark='a'/> Each cell subtracts the average shuffle change from the observed stop change. {n_pos} exceed two shuffle standard deviations positively and {n_neg} negatively. <bookmark mark='b'/> The star is a descriptive threshold, not a calibrated or multiple-testing-adjusted p-value. Patterns across factors suggest questions about timing and dependence; this display does not prove persistent losses caused the difference or establish a universal stop policy."""
        ) as vo:
            self.play(FadeIn(rl), FadeIn(cl), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.03))
            vo.wait_until("b")
            focus = SurroundingRectangle(VGroup(*cells[-6:]), color=WHITE, buff=0.07)
            self.play(Create(focus))
            self.play(FadeOut(focus))
        self.wait(0.4)
        self.clear_scene()

    def why_(self, s):
        cards = VGroup(
            desk_question(r"value and profitability: slow drawdowns", 'their losses come in long episodes (value in 1998--2000 and 2018--2020), a possible timing explanation to investigate, without a causal or future-performance conclusion', width=12.4, font_size=26),
            desk_question(r"momentum: crash and rebound", r"momentum's worst losses are sudden reversals that recover "
                          r"(2009, Part 24); a stop sells at the bottom and sits out the recovery", width=12.4,
                          font_size=26),
            desk_question(r"what a stop really bets on", 'whether past losses forecast future opportunities after costs; the research comparison does not establish that', width=12.4, font_size=26),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "Possible mechanisms require further evidence. <bookmark mark='a'/> Slow drawdown episodes in value or profitability could make a delayed exit useful during some periods. This reused sample does not prove conditional predictability. <bookmark mark='b'/> Sudden momentum reversals and rebounds can make exits miss recoveries; costs and timing matter. <bookmark mark='c'/> A stop changes exposure based on the past. Whether that helps future investor outcomes depends on return dependence, financing, costs, objectives and selection. The cached comparison alone cannot settle that question."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def trials(self, s):
        rows = [cmath(r"36\ \text{combinations}", r"\Rightarrow", r"\text{the best one is flattered}", font_size=32,
                      colors={r"36\ \text{combinations}": BAD}),
                cmath(r"\text{for a platform}", r":", r"\text{stops are about unknown skill, not premia}", font_size=30,
                      colors={r"\text{for a platform}": FIRM_C}),
                cmath(r"\text{not registered}", r":", r"\text{a finding about factors, with its trials stated}", font_size=30)]
        whys = [why(r"choosing the best stop for each factor after seeing these results would be Part 26's mistake"),
                why('platform hiring and factor timing are different questions; neither latent manager skill nor a future premium is known from these comparisons'),
                why(r"the House records it as research with 36 trials; no stop rule is added to any registered book")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Selection remains. <bookmark mark='a'/> Choosing each factor's best stop after examining thirty-six results would add selection bias. Dependence means thirty-six is not an effective independent test count. <bookmark mark='b'/> A known latent skill in a simulation differs from an uncertain future factor premium in data. Neither is guaranteed in practice. <bookmark mark='c'/> The historical registration metadata already includes this research. This review performs no new market trial, updates no registry, opens no sealed strategy result and adds no stop to an approved live book."
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
        q = pause_card('Use the stated assumptions; derive the result and check its units and denominator.')
        working = MathTex('Y_t=Z_tR_t,\\quad p=0.75,\\quad s_Y=\\frac{\\sqrt p\\,s_R}{\\sqrt{1+(1-p)s_R^2}}', font_size=32).move_to(UP*0.9)
        if working.width > 12.1:
            working.scale_to_fit_width(12.1)
        setup_note = wrapped_label('Current iid return independent of predictable exposure, stationary on probability p, zero cash return. Use the low-mean approximation for annual S=0.6; annualization has additional dependence assumptions.', 11.7, 23).move_to(DOWN*0.8)
        self.add(working, setup_note, q)
        with self.voiceover('Pause and predict. With annual Sharpe point six and a stationary on fraction three quarters, apply the low-mean iid exposure approximation. Then identify the extra term in the exact marginal per-period formula and the assumptions needed to annualize.'):
            self.wait(0.5)
        self.wait(0.5)
        self.clear_scene()
