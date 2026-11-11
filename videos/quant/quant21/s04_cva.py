from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, CVA_C, DVA_C, EXPO, GOOD, NEG, PART, ask, fit_right, illustration, load


class CVA(VoiceoverScene):
    def construct(self):
        v = load("cva")
        e = load("exposure")
        self.card()
        self.derive()
        self.compute(v, e)
        self.dva(v)
        r = load("cvarisk")
        self.hedge(r)
        self.incremental(r)
        self.accuracy(load("convergence"), load("modelrisk"))
        self.losses()

    def card(self):
        c = chapter_card(3, r"CVA and DVA", r"What is the chance of default worth, in dollars?", lit=(2008,), part=PART)
        with self.voiceover("Chapter three. The credit valuation adjustment, and its mirror image."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"V_{\text{risky}}", r"=", 'V_{\\text{clean}} - \\text{CVA}_{bil} + \\text{DVA}_{bil}', font_size=40,
                      colors={r"V_{\text{risky}}": WHITE}),
                cmath(r"\text{CVA}", r"=", '-(1 - R)\\int_0^T \\text{EE}(t)\\,P(0,t)\\,dQ_c(t)', font_size=40,
                      colors={r"\text{CVA}": CVA_C}),
                cmath(r"\text{CVA}", r"\approx", r"(1 - R)\sum_i \text{EE}(t_i)\,P(0, t_i)\,\big[Q_c(t_{i-1}) - Q_c(t_i)\big]",
                      font_size=36, colors={r"\text{CVA}": CVA_C}),
                cmath(r"\text{DVA}", r"=", r"-(1 - R_b)\sum_i \text{ENE}(t_i)\,P(0, t_i)\,\big[Q_b(t_{i-1}) - Q_b(t_i)\big]",
                      font_size=34, colors={r"\text{DVA}": DVA_C})]
        whys = [why(r"the value of a trade with a risky counterparty: the risk-free value, less the expected loss from "
                    r"its default, plus the expected gain from your own"),
                why('Unilateral clean-closeout approximation: $Q_c$ is survival, so $-dQ_c$ is positive. Here discounting is deterministic and exposure is independent of default.'),
                why(r"on the exposure grid: each bucket's expected exposure, discounted, times the chance of default in "
                    r"that bucket (independence of exposure and default assumed, for now)"),
                why(r"the mirror: what the bank would not have to pay if it defaulted itself, using its own CDS curve")]
        step = ladder(self, rows, whys, keep=4, top=3.25, x=-1.0, buff=0.3, edge=6.9)
        with self.voiceover(
            "Under a specified clean closeout, bilateral value subtracts loss when the counterparty defaults first and adds the own-default adjustment. <bookmark mark='a'/> Here start with unilateral CVA: loss given default, times discounted expected positive exposure, integrated against minus the survival decrement. The sign matters. We use a pricing-measure exposure model, independent default and deterministic discounting. With stochastic rates, discount and exposure belong inside one joint expectation. <bookmark mark='b'/> On a monthly grid the integral becomes a bucket approximation, with a positive survival decrement. <bookmark mark='c'/> DVA is the mirror for negative exposure. Bilateral versions also require survival of the other party and a consistent closeout convention."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def compute(self, v, e):
        t = np.asarray(v["times"])
        contrib = np.asarray(v["contrib"]) * 1e3
        EE = np.asarray(e["net"]["EE"])
        g1 = axes([0, 10], [0, 7], x_length=5.6, y_length=3.4, xlabel=r"years", ylabel=r"EE, \$m", xticks=[0, 5, 10],
                  yticks=[0, 3, 6], font_size=13)
        g2 = axes([0, 10], [0, max(contrib) * 1.2], x_length=5.6, y_length=3.4, xlabel=r"years",
                  ylabel=r"CVA by month, \$ thousand", xticks=[0, 5, 10], yticks=[], font_size=13)
        VGroup(g1, g2).arrange(RIGHT, buff=0.9).shift(DOWN * 0.5)
        l1 = curve(g1.ax, np.r_[0, t], np.r_[0, EE], EXPO, stroke_width=3)
        bars = VGroup(*[Rectangle(width=max(g2.ax.c2p(t[1] - t[0], 0)[0] - g2.ax.c2p(0, 0)[0] - 0.005, 0.01),
                                  height=max(g2.ax.c2p(0, c_)[1] - g2.ax.c2p(0, 0)[1], 0.005), stroke_width=0,
                                  fill_color=CVA_C, fill_opacity=0.8).move_to(
            [g2.ax.c2p(x_, 0)[0], (g2.ax.c2p(0, c_)[1] + g2.ax.c2p(0, 0)[1]) / 2, 0]) for x_, c_ in zip(t, contrib)])
        head = VGroup(
            MathTex(rf"\text{{CVA}} = \${1e3 * v['cva']:,.0f}\text{{k}}".replace(",", "{,}"), font_size=32, color=CVA_C),
            label(rf"counterparty BBB-like: CDS 80--170 bp; recovery 40\%; the netting set of chapter 1", font_size=18,
                  color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.45)
        foot = wrapped_label(f"about {v['cva_bp_running']:.1f} bp a year on a 100 million reference notional, the charge a desk adds to the price; the contributions peak where expected exposure and the default density are both large", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"Use the illustrative CDS quotes and the same three-swap netting set. <bookmark mark='a'/> The left curve is expected positive exposure; the bars are monthly deterministic-discount CVA contributions under independent default. <bookmark mark='b'/> The sum is {1e3 * v['cva']:,.0f} thousand dollars. The running-spread conversion is {v['cva_bp_running']:.1f} basis points on a one-hundred-million reference notional, not on the book's two-hundred-million gross notional. The conversion is a quoting convention; it does not change the dollar loss estimate."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), Create(l1))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.01, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(head), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def dva(self, v):
        mult = np.asarray(v["mult"])
        d_ = np.asarray(v["dva_by_spread"]) * 1e3
        g = axes([0.5, 6.5], [0, 800], x_length=6.8, y_length=4.2, xlabel=r"the bank's own CDS, multiple of today's",
                 ylabel=r"DVA, \$ thousand", xticks=[1, 2, 3, 4, 6], yticks=[0, 200, 400, 600, 800], font_size=14
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = VGroup(curve(ax, mult, d_, DVA_C, stroke_width=3.5), *[Dot(ax.c2p(a, b), color=DVA_C) for a, b in zip(mult, d_)])
        side = VGroup(
            MathTex(rf"\text{{bilateral CVA}} = {1e3 * v['cva_bilateral']:.0f}\text{{k}}", font_size=26, color=CVA_C),
            MathTex(rf"\text{{DVA}} = {1e3 * v['dva']:.0f}\text{{k}}", font_size=26, color=DVA_C),
            MathTex(rf"\text{{BCVA}} = \text{{CVA}} - \text{{DVA}} = {1e3 * v['bcva']:.0f}\text{{k}}", font_size=26),
            wrapped_label("bilateral: each default counts only if it comes first. DVA rises as the bank's own credit worsens: a gain recorded when the bank is closer to failing. Accounting standards (IFRS 13) require non-performance risk in fair value; own-credit effects receive prudential adjustments. A DVA gain is not freely available cash",
                          3.8, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"In this bucket approximation, each default counts only while the other party survives. <bookmark mark='a'/> Bilateral CVA is {1e3 * v['cva_bilateral']:.0f} thousand, and DVA {1e3 * v['dva']:.0f}. <bookmark mark='b'/> Widening the bank's own spreads raises this DVA. Dealers reported own-credit gains in the financial crisis, but accounting recognition does not turn them into spendable income. Realization, hedging and prudential treatment depend on the instrument and rules; it is misleading to treat a deterioration in the bank's credit as operating profit."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(line), FadeIn(side[3]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def hedge(self, r):
        m, pth = np.asarray(r["mults"]), np.asarray(r["path"]) * 1e3
        g = axes([0, 4.5], [0, 1400], x_length=6.8, y_length=4.2, xlabel=r"counterparty's CDS, multiple of today's",
                 ylabel=r"CVA, \$ thousand", xticks=[0, 1, 2, 3, 4], yticks=[0, 400, 800, 1200], font_size=14
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = VGroup(curve(ax, np.r_[0, m], np.r_[0, pth], CVA_C, stroke_width=3.5),
                      *[Dot(ax.c2p(a, b), color=CVA_C) for a, b in zip(m, pth)])
        side = VGroup(
            MathTex(rf"\text{{CS01}} = \${1e6 * r['cs01']:,.0f}\ \text{{per bp}}".replace(",", "{,}"), font_size=26,
                    color=CVA_C),
            MathTex(rf"\text{{hedge: buy}}\ \${r['cds_hedge_notional']:.1f}\text{{m of 5-year CDS}}", font_size=26,
                    color=GOOD),
            wrapped_label(r"CVA is a short position in the counterparty's credit: it grows as the spread widens, less "
                          r"than in proportion because a likelier default comes sooner and the trades are worth less by "
                          r"then. Buying protection on the counterparty offsets the spread risk; the exposure moves with "
                          r"rates, so the rate risk is hedged with swaps", 3.8, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Once CVA is on the books, it is a position, and positions are hedged. <bookmark mark='a'/> Double the "
            f"counterparty's spreads and the CVA goes from {pth[1]:.0f} to {pth[3]:.0f} thousand; quadruple them and it "
            f"reaches {pth[-1]:,.0f}. It is short the counterparty's credit, and curves over because a likelier "
            "default comes sooner, before the exposure has grown. <bookmark mark='b'/> One basis point on the "
            f"counterparty's curve moves the CVA by about {1e6 * r['cs01']:,.0f} dollars, so the desk buys about "
            f"{r['cds_hedge_notional']:.1f} million of five-year protection on that name. The exposure itself moves "
            "with interest rates, and that part is hedged with swaps. The CVA desk is a trading desk, with the "
            "bank's own counterparties as its underlyings."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x_) for x_ in side], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def incremental(self, r):
        inc = r["incremental"]
        rows = [cmath(r"\Delta\text{CVA}_{\text{new}}", r"=", r"\text{CVA}(\text{book} + \text{new}) - \text{CVA}(\text{book})",
                      font_size=36, colors={r"\Delta\text{CVA}_{\text{new}}": CVA_C})]
        whys = [why(r"exposure is a property of the netting set, so a new trade's price is the change it makes to the "
                    r"set's CVA, not its own")]
        step = ladder(self, rows, whys, keep=1, top=2.6, x=-0.4, buff=0.8, edge=6.9)
        hx = [-3.4, 0.4, 3.6]
        heads = [r"new 5-year swap, \$50m", r"CVA alone", r"CVA it adds to the book"]
        tab = VGroup(VGroup(*[label(h_, font_size=19, color=GREY_A).move_to([x, 0.2, 0]) for h_, x in zip(heads, hx)]))
        for i, (nm, k) in enumerate(((r"receiver (offsets the 10-year payer)", "receiver"),
                                     (r"payer (adds to it)", "payer"))):
            y = -0.55 - 0.65 * i
            a, b = 1e3 * inc[k]["alone"], 1e3 * inc[k]["incremental"]
            tab.add(VGroup(label(nm, font_size=19).move_to([hx[0], y, 0]),
                           MathTex(rf"{a:.1f}\text{{k}}", font_size=28).move_to([hx[1], y, 0]),
                           MathTex(rf"{b:+.1f}\text{{k}}", font_size=28, color=GOOD if b < 0 else CVA_C).move_to([hx[2], y, 0])))
        foot = wrapped_label(r"the same counterparty, the same day, two quotes: the trade that reduces the book's exposure "
                             r"earns the client a credit; the one that adds to it pays less than it would alone, because "
                             r"its exposure is not perfectly aligned with the book's", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.4)
        rv, py = inc["receiver"], inc["payer"]
        with self.voiceover(
            "Because exposure belongs to the netting set, so does the price. A new trade is charged the change it "
            "makes to the set's CVA. <bookmark mark='a'/> A new five-year receiver swap, which partly offsets the "
            f"book's ten-year payer, would carry {1e3 * rv['alone']:.0f} thousand of CVA on its own; added to this "
            f"book it reduces the CVA by {abs(1e3 * rv['incremental']):.0f} thousand, so the desk can pay the client "
            f"to do it. A new payer swap would cost {1e3 * py['alone']:.0f} thousand alone and adds "
            f"{1e3 * py['incremental']:.0f}. Two clients asking for the same swap can get different prices, and both "
            "can be right."
        ) as vo:
            step(0)
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x_) for x_ in tab[1:]], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def accuracy(self, cv, mr):
        rows = cv["rows"]
        n = np.array([r_["n"] for r_ in rows], float)
        sd = np.array([r_["sd"] for r_ in rows]) * 1e3
        g = axes([2, 4.5], [0, 30], x_length=5.4, y_length=3.6, xlabel=r"paths ($\log_{10}$)",
                 ylabel=r"CVA's std.\ error, \$k", xticks=[2.5, 3, 3.5, 4], yticks=[0, 10, 20, 30], font_size=13
                 ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.4)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(np.log10(a), b), color=CVA_C, radius=0.07) for a, b in zip(n, sd)])
        ref = curve(ax, np.linspace(2.3, 4.3, 50), sd[0] * np.sqrt(n[0] / 10 ** np.linspace(2.3, 4.3, 50)), GREY_B,
                    stroke_width=2)
        mrows = mr["rows"]
        hx = [2.4, 4.4, 6.0]
        heads = [r"mean reversion $a$", r"$\sigma$, bp", r"CVA, \$k"]
        tab = VGroup(VGroup(*[label(h_, font_size=17, color=GREY_A).move_to([x, 2.0, 0]) for h_, x in zip(heads, hx)]))
        for i, r_ in enumerate(mrows):
            y = 1.45 - 0.5 * i
            tab.add(VGroup(MathTex(f"{r_['a']:.3g}", font_size=24).move_to([hx[0], y, 0]),
                           MathTex(f"{1e4 * r_['sigma']:.0f}", font_size=24).move_to([hx[1], y, 0]),
                           MathTex(f"{1e3 * r_['cva']:.0f}", font_size=24).move_to([hx[2], y, 0])))
        cvas = [1e3 * r_["cva"] for r_ in mrows]
        tnote = wrapped_label(r"each model re-fitted to the same 10-year yield volatility, on the same random numbers",
                              5.0, 16, GREY_A).next_to(tab, DOWN, buff=0.25)
        title = label(r"Two kinds of error", font_size=28).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Distinguish simulation error from a model sensitivity exercise. <bookmark mark='a'/> Across twenty fixed-law independent runs, the standard deviation is {sd[0]:.0f} thousand at two hundred fifty paths and {sd[-1]:.1f} at sixteen thousand. The inverse-square-root rule is an asymptotic sampling principle, not a guarantee for every realized run. <bookmark mark='b'/> Vary mean reversion and rescale volatility to the same historical ten-year-yield proxy. This example's CVA ranges from {min(cvas):.0f} to {max(cvas):.0f} thousand. That narrow range does not validate the model: option-price calibration, multiple factors, past fixings, discount-exposure dependence and closeout assumptions remain outside this test."
        ) as vo:
            self.play(FadeIn(title), FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.3), Create(ref))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(tnote))
        self.wait(0.4)
        self.clear_scene()

    def losses(self):
        rows = [cmath(r"\Delta\text{CVA}", r"\gg", r"\text{actual default losses}\ \ (2007\text{--}09)", font_size=36,
                      colors={r"\Delta\text{CVA}": CVA_C})]
        whys = [why(r"the Basel Committee's finding: roughly two thirds of the counterparty credit losses in the crisis "
                    r"came from CVA losses, the marks on counterparties that had not defaulted, and only a third from "
                    r"actual defaults. Basel III added a capital charge for CVA's volatility (chapter 12)")]
        step = ladder(self, rows, whys, keep=1, top=2.0, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "CVA is not only a price; it is a position that moves. As counterparties' spreads widened in 2007 and "
            "2008, the adjustments on trades with them grew, and those changes were marked as losses. The Basel "
            "Committee found that about two thirds of banks' counterparty losses in the crisis came that way, from "
            "counterparties that had not defaulted, and only a third from those that did. So Basel the Third charged "
            "capital for the volatility of CVA itself."
        ) as vo:
            step(0)
        q = ask(r"a bank's DVA rises when its own credit spread widens. Is that profit real? Who would pay it, and "
                r"when?")
        with self.voiceover("A bank's DVA rises as its own credit gets worse. Is that profit real? Who would pay it, and "
                            "when?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
