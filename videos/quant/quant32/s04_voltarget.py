from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import BAD, GOOD, HURDLE, PART, SPY_C, VT_C, fit_right, load

SHOW = ["SPY", "IWM", "EEM", "VNQ", "TLT", "HYG", "GLD", "USO", "FXA"]


class VolTarget(VoiceoverScene):
    def construct(self):
        v = load("voltarget")
        self.card()
        self.rule()
        self.path(v)
        self.table(v)
        self.summary(v)
        self.leverage_effect()
        self.literature()
        self.crowded()
        self.why_macro()
        self.question()

    def card(self):
        c = chapter_card(3, r"Volatility targeting", r"Should you hold less of an asset when it is more volatile?",
                         part=PART)
        with self.voiceover("Chapter three. Every book in this part is scaled to a target volatility. Is that only risk "
                            "management, or does it also earn something?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rule(self):
        rows = [cmath(r"x_t", r"=", r"\min\Big(\frac{\sigma^*}{\hat\sigma_{t-1}},\ 3\Big)", font_size=40,
                      colors={r"x_t": VT_C}),
                cmath(r"r^{\text{VT}}_t", r"=", r"x_t\, r_t", font_size=38),
                cmath(r"\text{helps if}", r":", r"\frac{\mathbb E[r_t \mid \hat\sigma_{t-1}]}{\hat\sigma^2_{t-1}}\ \text{falls "
                      r"as } \hat\sigma_{t-1} \text{ rises}", font_size=30, colors={r"\text{helps if}": GOOD})]
        whys = [why(r"exposure inversely proportional to yesterday's volatility forecast, capped at three times: a 10\% "
                    r"target here"),
                why(r"the managed return"),
                why(r"Merton's rule, Part 8: the optimal exposure is expected return over variance. If expected returns "
                    r"do not rise with volatility, the asset is worth less when it is volatile")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The rule. <bookmark mark='a'/> Hold the target volatility divided by yesterday's forecast, capped at three "
            "times. <bookmark mark='b'/> Calm markets get more exposure, turbulent ones less. <bookmark mark='c'/> It "
            "earns something only if expected returns fail to keep pace with volatility. Merton's rule from Part eight "
            "says to hold expected return over variance; if the expected return is roughly constant while variance "
            "swings, the optimal exposure falls when volatility rises. Part eight tested it on the American market for "
            "ninety-four years. Here, across twenty-three assets."
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

    def path(self, v):
        d = np.asarray(v["spy_path"]["dates"], float)
        x = d // 10000 + ((d // 100) % 100 - 0.5) / 12
        e = np.asarray(v["spy_path"]["exposure"], float)
        vol = 100 * np.asarray(v["spy_path"]["vol"], float)
        top = axes([x[0], x[-1]], [0, 80], x_length=8.4, y_length=2.2, xlabel="", ylabel=r"SPY's volatility forecast, \%",
                   xticks=[], yticks=[0, 40, 80], font_size=14).move_to(UP * 1.6 + LEFT * 0.8)
        bot = axes([x[0], x[-1]], [0, 3.2], x_length=8.4, y_length=2.2, xlabel=r"2007--2020",
                   ylabel=r"exposure for a 15\% target", xticks=[2008, 2012, 2016, 2020], yticks=[0, 1, 3],
                   xfmt=lambda u: f"{u:.0f}", font_size=14).move_to(DOWN * 1.6 + LEFT * 0.8)
        c1 = curve(top.ax, x, np.minimum(vol, 80), BAD, stroke_width=2)
        c2 = curve(bot.ax, x, e, VT_C, stroke_width=2)
        txt = wrapped_label(rf"from {np.nanmin(e):.2f} in late 2008 to the cap of {np.nanmax(e):.0f} in the calm of 2017",
                            3.4, 16, GREY_A).to_edge(RIGHT, buff=0.3)
        fit_right(txt)
        with self.voiceover(
            "What it does, for American stocks at a fifteen percent target. <bookmark mark='a'/> The volatility forecast "
            "spikes in 2008, 2011 and 2020. <bookmark mark='b'/> The exposure is its mirror: cut to a fraction in the "
            "autumn of 2008, and at the cap of three times in the calm of 2017. Every rebalance is a trade, and these "
            "swings are why real funds cap leverage and smooth the forecast."
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot))
            vo.wait_until("a")
            self.play(Create(c1), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(txt), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    def table(self, v):
        rows = v["rows"]
        hx = [-5.0, -3.0, -1.2, 0.8, 2.8, 4.8]
        head = VGroup(label(r"fund", font_size=17, color=GREY_B), label(r"Sharpe, held", font_size=17, color=SPY_C),
                      label(r"Sharpe, targeted", font_size=17, color=VT_C), label(r"drawdown, held", font_size=17,
                                                                                  color=SPY_C),
                      label(r"drawdown, targeted", font_size=17, color=VT_C), label(r"class", font_size=17, color=GREY_B))
        tab = VGroup(head)
        for s in SHOW:
            r = rows[s]
            up = r["vt"]["sharpe"] > r["raw"]["sharpe"]
            tab.add(VGroup(label(r"\texttt{" + s + "}", font_size=19), MathTex(f"{r['raw']['sharpe']:.2f}", font_size=24),
                           MathTex(f"{r['vt']['sharpe']:.2f}", font_size=24, color=GOOD if up else BAD),
                           MathTex(rf"{100 * r['raw']['maxdd']:.0f}\%", font_size=24),
                           MathTex(rf"{100 * r['vt']['maxdd']:.0f}\%", font_size=24),
                           label(r["group"], font_size=16, color=GREY_A)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.8 - 0.55 * j, 0])
        foot = wrapped_label(r"2007--2020, daily excess returns; targeted: 10\% volatility, EWMA forecast (60-day centre of "
                             r"mass), exposure capped at 3; green where targeting raised the Sharpe ratio", 11.6, 15,
                             GREY_A).to_edge(DOWN, buff=0.3)
        s, u = rows["SPY"], rows["USO"]
        with self.voiceover(
            "Nine of the twenty-three. <bookmark mark='a'/> For American stocks, targeting raised the Sharpe ratio from "
            f"{s['raw']['sharpe']:.2f} to {s['vt']['sharpe']:.2f} and cut the worst drawdown from "
            f"{abs(100 * s['raw']['maxdd']):.0f} percent to {abs(100 * s['vt']['maxdd']):.0f}. Small caps and emerging "
            "markets got worse Sharpe ratios, though smaller drawdowns. <bookmark mark='b'/> For oil, the drawdown fell "
            f"from {abs(100 * u['raw']['maxdd']):.0f} percent to {abs(100 * u['vt']['maxdd']):.0f}, and the Sharpe ratio "
            "stayed negative: targeting manages risk, it does not create a premium where there is none."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:5]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[5:]], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def summary(self, v):
        n = v["n"]
        items = [(r"Sharpe ratio raised", v["better"], GOOD), (r"worst drawdown reduced", v["dd_better"], VT_C)]
        bars = VGroup()
        for j, (nm, k, col) in enumerate(items):
            full = Rectangle(width=8.0, height=0.6, stroke_color=GREY_D, stroke_width=1.5, fill_opacity=0)
            part = Rectangle(width=8.0 * k / n, height=0.6, fill_color=col, fill_opacity=0.8, stroke_width=0)
            part.align_to(full, LEFT)
            grp = VGroup(full, part).move_to([0.5, 0.9 - 1.3 * j, 0])
            bars.add(VGroup(grp, label(nm, font_size=22, color=col).next_to(grp, UP, buff=0.15).align_to(grp, LEFT),
                            MathTex(rf"{k}\ \text{{of}}\ {n}", font_size=28).next_to(grp, RIGHT, buff=0.25)))
        foot = wrapped_label(r"the funds whose worst drawdown fell were mostly the risky ones: equities, credit, commodities; "
                             r"for Treasuries and currencies, targeting mostly added leverage in calm years", 11.0, 18,
                             GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "In total. <bookmark mark='a'/> Targeting raised the Sharpe ratio for "
            f"{v['better']} of the {n} funds: no better than a coin. <bookmark mark='b'/> It reduced the worst drawdown for "
            f"{v['dd_better']}, mostly the risky ones: equities, credit and commodities, whose crashes come with high "
            "volatility. For Treasuries and currencies it mostly added leverage in calm years."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(bars[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def literature(self):
        cards = VGroup(
            desk_question(r"Moreira and Muir (2017)", r"volatility-managed factor portfolios earn large alphas against "
                          r"the unmanaged ones: the market, value, momentum, profitability, carry", width=12.4, font_size=19),
            desk_question(r"Cederburg, O'Doherty, Wang and Yan (2020)", r"across 103 strategies, the alphas do not survive "
                          r"as investable portfolios: combining managed and unmanaged in real time does not beat the "
                          r"unmanaged out of sample", width=12.4, font_size=19),
            desk_question(r"Harvey, Hoyle, Korgaonkar, Rattray, Sargaison and Van Hemert (2018)", r"for risk assets, "
                          r"targeting cuts the left tail and helps the Sharpe ratio a little; for bonds and currencies it "
                          r"does little", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The literature agrees with this table. <bookmark mark='a'/> Alan Moreira and Tyler Muir found large alphas "
            "for volatility-managed factors. <bookmark mark='b'/> Scott Cederburg and coauthors tested a hundred and "
            "three strategies and found that the alphas do not survive as portfolios an investor could have formed in "
            "real time. <bookmark mark='c'/> And Campbell Harvey and coauthors at Man Group found what we found: for "
            "risk assets, targeting cuts the left tail and helps a little; for bonds and currencies, it does little."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def why_macro(self):
        rows = [cmath(r"x_i", r"\propto", r"\frac{1}{\hat\sigma_i}", font_size=40, colors={r"x_i": VT_C}),
                cmath(r"\text{risk budget}", r"=", r"x_i\hat\sigma_i = \text{equal}", font_size=36),
                cmath(r"\text{leverage}", r"=", r"\textstyle\sum_i |x_i|\ \text{grows as the book's assets calm down}",
                      font_size=30, colors={r"\text{leverage}": BAD})]
        whys = [why(r"across markets, the same idea is risk budgeting: size each position by its volatility"),
                why(r"so a currency and natural gas contribute the same risk, and the book's return is not just its most "
                    r"volatile market"),
                why(r"the price: the calmer the assets, the more leverage the target requires, and leverage is what turns "
                    r"a correlation surprise into a loss (Chapter 4)")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Why macro books use it anyway. <bookmark mark='a'/> Across markets, scaling by volatility is risk "
            "budgeting. <bookmark mark='b'/> A currency and natural gas then contribute the same risk, and the book is "
            "not just its most volatile market. <bookmark mark='c'/> The price is leverage: the calmer the assets, the "
            "more of them the target requires. Chapter four shows what leverage does when calm assets stop being calm "
            "together."
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


    def leverage_effect(self):
        rows = [cmath(r"\operatorname{Corr}(r_t,\ \sigma_{t+1} - \sigma_t)", r"<", r"0\quad\text{for stocks}", font_size=34),
                cmath(r"\text{crash}", r"\Rightarrow", r"\hat\sigma\uparrow\ \Rightarrow\ x\downarrow\ \text{before the worst "
                      r"days}", font_size=32, colors={r"\text{crash}": BAD}),
                cmath(r"\text{bonds, currencies}", r":", r"\text{little leverage effect, little benefit}", font_size=32)]
        whys = [why(r"the leverage effect of Part 13: falling stock prices raise volatility, and volatility clusters"),
                why(r"so a targeted equity position shrinks during the first days of a sell-off, before the deepest losses, "
                    r"which is why the drawdowns shrank"),
                why(r"where volatility rises with prices as often as with falls, targeting mostly adds leverage in calm "
                    r"periods")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Why it helps risky assets in particular. <bookmark mark='a'/> For stocks, falling prices raise volatility: "
            "the leverage effect of Part thirteen, and volatility clusters. <bookmark mark='b'/> So a targeted equity "
            "position shrinks in the first days of a sell-off, before the worst of it; that is where the smaller "
            "drawdowns came from. <bookmark mark='c'/> For bonds and currencies, whose volatility rises with rallies as "
            "often as with falls, targeting mostly adds leverage when markets are calm."
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


    def crowded(self):
        cards = VGroup(
            desk_question(r"many hands on the same rule", r"volatility-control funds, risk-parity books and trend "
                          r"followers all cut exposure when volatility rises, and they measure it the same way", width=12.4,
                          font_size=19),
            desk_question(r"a feedback loop", r"selling into a rise in volatility can deepen the fall that raised it; "
                          r"supervisors and dealers have pointed to such rules in the selling of February 2018 and March "
                          r"2020, as reported", width=12.4, font_size=19),
            desk_question(r"the remedy", r"smoother forecasts, slower rebalancing and caps on daily changes in exposure: "
                          r"Part 31's partial trading, applied to risk", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "One more caution: many hands follow this rule. <bookmark mark='a'/> Volatility-control funds, risk-parity "
            "books and trend followers all cut exposure when volatility rises, and they measure it alike. "
            "<bookmark mark='b'/> Selling into a rise in volatility can deepen the fall that caused it; dealers and "
            "supervisors have pointed to such rules in the selling of February 2018 and March 2020. "
            "<bookmark mark='c'/> The remedies are Part thirty-one's: smoother forecasts, slower rebalancing, and limits "
            "on how fast exposure may change."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"an asset's expected return is proportional to its variance. Does volatility targeting help or "
                       r"hurt its Sharpe ratio?")
        with self.voiceover(
            "Pause and predict. Suppose an asset's expected return rises in proportion to its variance. Does volatility "
            "targeting help or hurt its Sharpe ratio?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
