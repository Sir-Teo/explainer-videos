from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, COLL, CVA_C, EXPO, PART, ask, fit_right, illustration, load


class Capital(VoiceoverScene):
    def construct(self):
        s = load("saccr")
        self.card()
        self.formula()
        self.numbers(s)
        self.multiplier(s)
        self.bacva(s)
        self.balance()

    def card(self):
        c = chapter_card(12, r"Capital for counterparty risk", r"Why did balance sheets become expensive?", part=PART)
        with self.voiceover("Chapter twelve. Capital: what regulators charge for counterparty risk, and what it changed."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def formula(self):
        rows = [cmath(r"\text{EAD}", r"=", r"1.4\,\big(\text{RC} + \text{multiplier}\times\text{AddOn}\big)", font_size=40,
                      colors={r"\text{EAD}": EXPO}),
                cmath(r"\text{AddOn}_{\text{IR}}", r"=", r"0.5\%\times\sqrt{D_1^2 + D_2^2 + D_3^2 + 1.4 D_1D_2 + 1.4 D_2D_3 + "
                      r"0.6 D_1D_3}", font_size=30, colors={r"\text{AddOn}_{\text{IR}}": EXPO}),
                cmath(r"D_k", r"=", r"\textstyle\sum_{i \in k} \delta_i\,N_i\,\frac{e^{-0.05 S_i} - e^{-0.05 E_i}}{0.05}\,"
                      r"\text{MF}_i", font_size=32, colors={r"D_k": EXPO})]
        whys = [why(r"SA-CCR (Basel, 2014): exposure at default is the replacement cost today plus a potential future "
                    r"exposure add-on, scaled by 1.4"),
                why(r"for interest-rate swaps in one currency: supervisory factor 0.5\%, and three maturity buckets "
                    r"(under 1 year, 1--5, over 5) that net partly with each other"),
                why(r"each trade's notional times a supervisory duration, with sign $\delta$ (long or short) and a "
                    r"maturity factor that is smaller when the trade is margined")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.0, buff=0.6, edge=6.9)
        with self.voiceover(
            "Regulators require capital against counterparty exposure, measured by a standard formula, SA-CCR. "
            "<bookmark mark='a'/> Exposure at default is what the trades would cost to replace today, plus an "
            "add-on for what they might become, times one point four. <bookmark mark='b'/> For interest-rate swaps, "
            "the add-on is half a percent of an effective notional: each trade's notional times a supervisory "
            "duration, signed long or short, grouped by maturity, with partial netting between the groups, and a "
            "smaller factor for margined trades."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def numbers(self, s):
        vals = s["alone"] + [s["sum_alone"], s["net"]["EAD"], s["margined"]["EAD"]]
        names = [r"10y payer alone", r"5y receiver alone", r"3y payer alone", r"sum of the three", r"one netting set",
                 r"netting set, margined"]
        cols = [GREY_B, GREY_B, GREY_B, BAD, EXPO, COLL]
        g = axes([0.4, 6.6], [0, 9], x_length=7.6, y_length=4.2, xlabel=r"", ylabel=r"exposure at default, \$ million",
                 xticks=[], yticks=[0, 3, 6, 9], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, (v, n_, c_) in enumerate(zip(vals, names, cols)):
            b_ = Rectangle(width=0.6, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0, fill_color=c_,
                           fill_opacity=0.8).move_to([ax.c2p(i + 1, 0)[0], (ax.c2p(0, v)[1] + ax.c2p(0, 0)[1]) / 2, 0])
            bars.add(VGroup(b_, MathTex(f"{v:.1f}", font_size=22).next_to(b_, UP, buff=0.08),
                            wrapped_label(n_, 1.15, 14, GREY_A).next_to(ax.c2p(i + 1, 0), DOWN, buff=0.15)))
        side = VGroup(
            MathTex(rf"\text{{capital at 8\% of a 100\% risk weight}}: \${s['capital_8pct_rw100']:.2f}\text{{m}}", font_size=22),
            wrapped_label(r"at today's par rates the replacement cost is zero, so the add-on is all of it. Netting and "
                          r"margin cut the charge by two thirds and then by more: the regulation's incentive to clear, "
                          r"collateralise and offset", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The netting set's three swaps. <bookmark mark='a'/> Each alone has an exposure at default; summed, "
            f"{s['sum_alone']:.1f} million. <bookmark mark='b'/> As one netting set, with offsetting directions, "
            f"{s['net']['EAD']:.1f}; margined, {s['margined']['EAD']:.1f}. The formula rewards exactly what the "
            "lessons of 2008 recommended: netting, collateral, and clearing."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars[:4]], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(bars[4]), FadeIn(bars[5]), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def multiplier(self, s):
        rows = [cmath(r"\text{mult}", r"=", r"\min\Big\{1,\ 0.05 + 0.95\,\exp\Big(\frac{V - C}{2 \times 0.95 \times "
                      r"\text{AddOn}}\Big)\Big\}", font_size=34, colors={r"\text{mult}": EXPO})]
        whys = [why(r"the add-on is scaled down when the netting set is out of the money or over-collateralised ($V - C "
                    r"< 0$): a trade deep against the counterparty is unlikely to become an exposure soon. The floor of "
                    r"5\% means no amount of collateral removes the charge entirely")]
        step = ladder(self, rows, whys, keep=1, top=2.8, x=-0.4, buff=0.8, edge=6.9)
        z = np.linspace(-6, 1, 200)
        m = np.minimum(1, 0.05 + 0.95 * np.exp(z / (2 * 0.95)))
        g = axes([-6, 1], [0, 1.1], x_length=6.4, y_length=2.8, xlabel=r"$(V - C)/\text{AddOn}$", ylabel=r"multiplier",
                 xticks=[-6, -4, -2, 0], yticks=[0, 0.5, 1.0], font_size=13).to_edge(DOWN, buff=0.5).shift(LEFT * 2.4)
        ax = g.ax
        line = curve(ax, z, m, EXPO, stroke_width=3.5)
        floor = DashedLine(ax.c2p(-6, 0.05), ax.c2p(1, 0.05), color=GREY_B, stroke_width=1.5)
        ex = [(-1.0, r"out of the money by one add-on"), (-3.0, r"by three")]
        dots = VGroup()
        for zz, t_ in ex:
            mm = float(np.minimum(1, 0.05 + 0.95 * np.exp(zz / 1.9)))
            dots.add(VGroup(Dot(ax.c2p(zz, mm), color=BAD), label(rf"{t_}: {mm:.2f}", font_size=15, color=BAD).next_to(
                ax.c2p(zz, mm), UR, buff=0.08)))
        side = wrapped_label(rf"for the margined netting set, the add-on is \${s['margined']['AddOn']:.2f}m: posting "
                             r"collateral beyond the exposure lowers the charge, but never below the floor", 4.6, 16,
                             GREY_A).to_edge(RIGHT, buff=0.4).to_edge(DOWN, buff=0.7)
        fit_right(side, 6.85)
        with self.voiceover(
            "One more piece of the formula rewards collateral beyond what is owed. <bookmark mark='a'/> The add-on "
            "is multiplied by a factor that falls when the netting set is out of the money, or when the bank holds "
            "more collateral than the trades are worth. <bookmark mark='b'/> One add-on out of the money, and the "
            "multiplier is about point six; three, and about a quarter. It never goes below five percent: however "
            "much collateral there is, some charge remains, because the market can always move further than the "
            "collateral covers."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(g), Create(floor), Create(line), FadeIn(side), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.5))
        self.wait(0.4)
        self.clear_scene()

    def bacva(self, s):
        rows = [cmath(r"\text{SCVA}_c", r"=", r"\tfrac{1}{\alpha}\,RW_c\,M_c\,\text{EAD}_c\,\text{DF}_c,\quad "
                      r"\text{DF} = \tfrac{1 - e^{-0.05M}}{0.05M}", font_size=32, colors={r"\text{SCVA}_c": CVA_C}),
                cmath(r"K", r"=", r"0.65\sqrt{\big(\rho\textstyle\sum_c \text{SCVA}_c\big)^2 + (1 - \rho^2)\textstyle\sum_c "
                      r"\text{SCVA}_c^2},\quad \rho = 0.5", font_size=30, colors={r"K": CVA_C})]
        whys = [why(r"Basel's basic approach to CVA capital (2020): each counterparty's stand-alone charge from its "
                    r"exposure, maturity and a risk weight set by sector and rating"),
                why(r"a single common factor with correlation 0.5: part of every counterparty's spread moves together "
                    r"and cannot be diversified away")]
        step = ladder(self, rows, whys, keep=2, top=2.9, x=-0.6, buff=0.7, edge=6.9)
        ead, M, rw = s["net"]["EAD"], 6.0, 0.05
        df = (1 - np.exp(-0.05 * M)) / (0.05 * M)
        sc = rw * M * ead * df / 1.4
        ns = np.arange(1, 101)
        per = np.sqrt((0.5 * ns) ** 2 + 0.75 * ns) / ns
        g = axes([0, 100], [0, 1.05], x_length=5.2, y_length=2.4, xlabel=r"identical counterparties",
                 ylabel=r"capital per name, $\times$ one", xticks=[1, 25, 50, 75, 100], yticks=[0, 0.5, 1.0], font_size=12
                 ).to_edge(DOWN, buff=0.5).shift(LEFT * 3.0)
        ax = g.ax
        line = curve(ax, ns, per, CVA_C, stroke_width=3)
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(100, 0.5), color=GREY_B, stroke_width=1.5)
        side = VGroup(
            MathTex(rf"\text{{one name}}: K = 0.65 \times {1e3 * sc:.0f}\text{{k}} = \${0.65 * 1e3 * sc:.0f}\text{{k}}",
                    font_size=24, color=CVA_C),
            wrapped_label(rf"the netting set's SA-CCR EAD \${ead:.1f}m, an assumed effective maturity of {M:g} years and a "
                          rf"{100 * rw:g}\% risk weight. Across many names the charge per name falls toward half: "
                          r"the common factor stays", 5.0, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4).to_edge(DOWN, buff=0.6)
        fit_right(side, 6.85)
        with self.voiceover(
            "The charge for CVA's own volatility has a formula too, Basel's basic approach since 2020. "
            "<bookmark mark='a'/> Each counterparty's stand-alone charge scales with its exposure at default, its "
            "maturity, and a risk weight set by its sector and rating. <bookmark mark='b'/> Then they are combined "
            "as if every spread had one common factor, with correlation one half. <bookmark mark='c'/> For our "
            f"netting set alone, with a five percent risk weight, the charge is about {0.65 * 1e3 * sc:.0f} thousand "
            "dollars of capital. Spread the same exposure over a hundred counterparties, and the charge per name "
            "falls only to about half: the part of credit spreads that moves together cannot be diversified away, "
            "which is exactly what happened in 2008."
        ) as vo:
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(FadeIn(g), Create(half), Create(line), FadeIn(side), run_time=2)
        self.add(illustration(r"Basel Framework MAR50; inputs illustrative", UR))
        self.wait(0.4)
        self.clear_scene()

    def balance(self):
        cards = VGroup(
            desk_question(r"CVA capital", r"a separate charge for the volatility of CVA itself (chapter 3's two thirds), "
                          r"revised in 2020 into standardised and basic approaches", width=12.0, font_size=21),
            desk_question(r"the leverage ratio", r"capital of at least 3\% of total exposure, whatever its risk: "
                          r"derivatives, repo and even Treasuries count, so low-risk, low-margin business became "
                          r"expensive", width=12.0, font_size=21),
            desk_question(r"the consequence", r"dealers charge for balance sheet: swap spreads below Treasuries (Part "
                          r"18), wider covered-interest-parity gaps and a costlier basis trade (Part 22), and KVA in every "
                          r"quote (chapter 5)", width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "So capital is charged twice for one counterparty: for its default, and for the volatility of its CVA, "
            "where most of the crisis losses came from. <bookmark mark='a'/> And then the leverage ratio: capital of at "
            "least three percent of all exposures, whatever their risk, so even Treasuries and repo use capital. "
            "<bookmark mark='b'/> The consequence runs through the series: dealers now charge for their balance "
            "sheets, which is why swap spreads went below Treasury yields in Part eighteen, why the gaps in Part "
            "twenty-two's currency markets persist, and why every quote carries KVA."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"under a leverage ratio, a dealer holds a riskless Treasury position financed in repo. Why does it "
                r"still cost the dealer money?")
        with self.voiceover("Under a leverage ratio, a dealer holds a riskless Treasury position financed in repo. Why "
                            "does it still cost money?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
