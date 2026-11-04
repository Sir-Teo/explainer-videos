from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant24.common import BAD, CMA, GOOD, HML, MKT, PART, RMW, SMB, ask, fit_right, illustration, load


class Profit(VoiceoverScene):
    def construct(self):
        p = load("profit")
        self.card()
        self.ddm(p)
        self.numbers(p)
        self.novy()
        self.factors(p)
        self.redundant(p)
        self.qfactors(p)
        self.contest()

    def card(self):
        c = chapter_card(5, r"Profitability, investment, five factors and q", r"What does a firm's balance sheet say about "
                         r"its expected return?", lit=(2015,), part=PART)
        with self.voiceover("Chapter five. Two more factors, profitability and investment, and two rival models built "
                            "from them."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def ddm(self, p):
        rows = [cmath(r"M_t", r"=", r"\textstyle\sum_{\tau \ge 1} \frac{\mathbb{E}_t[Y_{t+\tau} - dB_{t+\tau}]}{(1 + r)^\tau}",
                      font_size=40, colors={r"M_t": MKT}),
                cmath(r"\frac{M_t}{B_t}", r"=", r"\textstyle\sum_{\tau \ge 1} \frac{(\text{ROE} - g)(1 + g)^{\tau - 1}}"
                      r"{(1 + r)^\tau}", font_size=40),
                cmath(r"r\ \uparrow", r"\iff", r"B/M\ \uparrow,\ \ \text{ROE}\ \uparrow\ \text{(given } B/M),\ \ g\ "
                      r"\downarrow\ \text{(given } B/M)", font_size=34, colors={r"r\ \uparrow": GOOD})]
        whys = [why(r"Fama and French (2006): a firm's market value is its expected earnings $Y$ less the investment $dB$ "
                    r"needed to grow its book, discounted at its expected return $r$"),
                why(r"with book equity growing at $g$ and a steady return on equity: divide by book, and the ratio depends "
                    r"on three things only"),
                why(r"so, holding the others fixed, a higher expected return shows up as a higher book-to-market, higher "
                    r"profitability, or lower investment: value, profitability and investment are three windows on $r$")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "Start from the dividend discount model, as Fama and French did. A firm's market value is the discounted "
            "stream of what it can pay out: earnings, less the investment it needs to grow its book equity. "
            "<bookmark mark='a'/> Divide by book equity. With a steady return on equity and steady growth, the ratio "
            "of market to book depends on just three things: profitability, investment, and the discount rate. "
            "<bookmark mark='b'/> Turn it around. Holding two fixed, a higher expected return appears as a higher "
            "book-to-market, or as higher profitability, or as lower investment. Value, profitability and investment "
            "are three windows onto the same unobserved discount rate."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def numbers(self, p):
        d = p["ddm"]
        hx = [-3.6, -0.4, 2.2, 4.8]
        heads = [r"firm", r"ROE, growth, $r$", r"book-to-market", r""]
        cases = [(r"a base case", r"12\%,\ 5\%,\ 9\%", d["base"], r""),
                 (r"less profitable", r"8\%,\ 5\%,\ 9\%", d["low_roe"], r"looks like value"),
                 (r"investing more", r"12\%,\ 7\%,\ 9\%", d["high_inv"], r"looks like growth"),
                 (r"riskier", r"12\%,\ 5\%,\ 11\%", d["high_r"], r"looks like value")]
        tab = VGroup(VGroup(*[label(h_, font_size=18, color=GREY_A).move_to([x, 2.1, 0]) for h_, x in zip(heads, hx)]))
        for i, (a, b, c_, e) in enumerate(cases):
            y = 1.4 - 0.62 * i
            tab.add(VGroup(label(a, font_size=19).move_to([hx[0], y, 0]), MathTex(b, font_size=24).move_to([hx[1], y, 0]),
                           MathTex(f"{c_:.2f}", font_size=26, color=HML).move_to([hx[2], y, 0]),
                           label(e, font_size=17, color=GREY_A).move_to([hx[3], y, 0])))
        foot = wrapped_label(r"the House's \texttt{factors.ddm\_bm}, two hundred years of payouts. A high B/M can mean a high "
                             r"discount rate, or just low profitability or low growth: value alone confounds them, which "
                             r"is why profitability and investment are needed beside it", 12.0, 17, GREY_A).to_edge(
            DOWN, buff=0.5)
        with self.voiceover(
            "In numbers. A firm earning twelve percent on its book, growing five percent a year, discounted at nine, "
            "trades at a book-to-market of about six tenths. <bookmark mark='a'/> Make it less profitable and its "
            "book-to-market more than doubles: it looks like a value stock with no change in risk. Make it invest "
            "more, and it looks like growth. Make it riskier, and it looks like value again. <bookmark mark='b'/> So a "
            "cheap stock may be cheap because it is risky, or because it is a poor business. Only by controlling for "
            "profitability and investment can value measure the discount rate."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab[2:]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def novy(self):
        rows = [cmath(r"GP/A", r"=", r"\frac{\text{revenue} - \text{cost of goods sold}}{\text{total assets}}", font_size=42,
                      colors={r"GP/A": RMW})]
        whys = [why(r"Novy-Marx (2013), 'The other side of value': gross profits, the cleanest measure of economic "
                    r"profitability before accounting choices, predict returns about as strongly as book-to-market, and "
                    r"profitable firms tend to be growth firms, so a profitability strategy hedges value")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "The evidence came first, as usual. Robert Novy-Marx measured profitability as gross profits, revenue less "
            "the cost of the goods sold, over total assets: a number that comes before most accounting choices. "
            "Profitable firms earned more, about as reliably as cheap ones did. And because profitable firms tend to "
            "be expensive, a profitability strategy tends to be long growth stocks, a natural hedge for value. He "
            "called it the other side of value."
        ) as vo:
            step(0)
        self.wait(0.4)
        self.clear_scene()

    def factors(self, p):
        hx = [-4.4, -1.6, 0.8, 3.0, 5.2]
        heads = [r"factor", r"mean, a year", r"volatility", r"Sharpe", r"$t$"]
        tab = VGroup(VGroup(*[label(h_, font_size=18, color=GREY_A).move_to([x, 2.1, 0]) for h_, x in zip(heads, hx)]))
        for i, (k, nm, col) in enumerate((("HML", r"HML: value", HML), ("RMW", r"RMW: robust minus weak profitability", RMW),
                                          ("CMA", r"CMA: conservative minus aggressive", CMA))):
            s = p[k]
            y = 1.4 - 0.7 * i
            tab.add(VGroup(label(nm, font_size=17, color=col).move_to([hx[0], y, 0]),
                           MathTex(rf"{100 * s['mean']:.1f}\%", font_size=26).move_to([hx[1], y, 0]),
                           MathTex(rf"{100 * s['vol']:.1f}\%", font_size=26).move_to([hx[2], y, 0]),
                           MathTex(f"{s['sharpe']:.2f}", font_size=26).move_to([hx[3], y, 0]),
                           MathTex(f"{s['t']:.1f}", font_size=26).move_to([hx[4], y, 0])))
        foot = wrapped_label(r"July 1963 to December 2020. RMW sorts on operating profitability (revenue less costs and "
                             r"interest, over book equity), CMA on asset growth, each in the same 2 x 3 way as HML. The new "
                             rf"two are as rewarding as value, and less volatile. CMA and HML are correlated "
                             rf"{p['corr_hml_cma']:.2f}", 12.0, 17, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In 2015 Fama and French added two factors. Robust minus weak, on operating profitability, and conservative "
            "minus aggressive, on the growth of total assets: firms that invest little against firms that invest a "
            "lot. <bookmark mark='a'/> Since 1963 each has earned about three percent a year, like value, with less "
            "volatility and higher t-statistics. And investment is strongly correlated with value, about seven tenths: "
            "cheap firms are usually the ones not growing."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def redundant(self, p):
        rows = [cmath(r"HML_t", r"=", r"\alpha + b\,MKT_t + s\,SMB_t + r\,RMW_t + c\,CMA_t + e_t", font_size=40,
                      colors={r"HML_t": HML})]
        whys = [why(r"a spanning test: if a factor's return is explained by the others, its alpha is zero and it adds "
                    r"nothing to the best Sharpe ratio the model can reach")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        s3, s5 = p["span3"], p["span"]
        res = VGroup(
            MathTex(rf"\text{{on the market and size}}:\ \alpha = {100 * s3['alpha']:+.1f}\%\ (t = {s3['t']:.1f})",
                    font_size=30),
            MathTex(rf"\text{{adding RMW and CMA}}:\ \alpha = {100 * s5['alpha']:+.1f}\%\ (t = {s5['t']:.1f}),\ R^2 = "
                    rf"{s5['r2']:.2f}", font_size=30, color=BAD),
            wrapped_label(r"1963--2020, Newey--West $t$. Fama and French found the same in 2015: in the five-factor model "
                          r"value is redundant, its average return explained by its exposures to profitability and, above "
                          r"all, investment", 11.0, 17, GREY_A),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Now a striking test. Regress value's return on the other four factors. <bookmark mark='a'/> On the "
            "market and size alone, value has an alpha of almost four percent a year. <bookmark mark='b'/> Add "
            "profitability and investment, and the alpha disappears, to about minus one percent with a t of minus "
            "eight tenths. Fama and French reported it themselves: in their own five-factor model, value, the factor "
            "they made famous, is redundant. Its premium is explained by its tilt toward firms that invest little."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(res[0]))
            vo.wait_until("b")
            self.play(FadeIn(res[1]), FadeIn(res[2]))
        self.wait(0.4)
        self.clear_scene()

    def qfactors(self, p):
        rows = [cmath(r"\mathbb{E}[r^S_{i,t+1}]", r"=", r"\frac{\mathbb{E}_t[\Pi_{i,t+1}]}{1 + a\,(I_{it}/A_{it})}",
                      font_size=40, colors={r"\mathbb{E}[r^S_{i,t+1}]": GOOD})]
        whys = [why(r"Hou, Xue and Zhang (2015): the investment CAPM. A firm invests until the marginal cost of investing, "
                    r"$1 + a(I/A)$, equals the discounted marginal profit. So expected returns rise with expected "
                    r"profitability and fall with investment: the q-factors are investment (IA) and return on equity "
                    r"(ROE), and the q5 model adds expected growth (EG, 2021)")]
        step = ladder(self, rows, whys, keep=1, top=2.6, x=-0.4, buff=0.8, edge=6.9)
        q = p["q"]
        hx = [-3.6, -0.6, 2.0, 4.4]
        tab = VGroup(VGroup(*[label(h_, font_size=17, color=GREY_A).move_to([x, -0.4, 0]) for h_, x in
                              zip((r"q-factor", r"mean, a year", r"Sharpe", r"$t$"), hx)]))
        for i, (k, nm) in enumerate((("R_ME", r"ME: size"), ("R_IA", r"IA: investment"), ("R_ROE", r"ROE: profitability"),
                                      ("R_EG", r"EG: expected growth"))):
            s = q[k]
            y = -0.9 - 0.45 * i
            tab.add(VGroup(label(nm, font_size=17).move_to([hx[0], y, 0]),
                           MathTex(rf"{100 * s['mean']:.1f}\%", font_size=22).move_to([hx[1], y, 0]),
                           MathTex(f"{s['sharpe']:.2f}", font_size=22).move_to([hx[2], y, 0]),
                           MathTex(f"{s['t']:.1f}", font_size=22).move_to([hx[3], y, 0])))
        foot = label(rf"global-q.org, 1967--2020; IA and CMA correlated {p['corr']['IA_CMA']:.2f}; HML's alpha on the q "
                     rf"model: {100 * p['q_span_hml']['alpha']:.1f}\%", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A rival model arrived the same year, from the other direction. Kewei Hou, Chen Xue and Lu Zhang started "
            "from the firm's decision to invest. A firm invests until the marginal cost of one more unit of capital "
            "equals the discounted profit it will bring. Rearranged, expected returns rise with expected profitability "
            "and fall with investment. No investor psychology, no consumption, only the firm's first-order "
            "condition. <bookmark mark='a'/> Their factors, from 1967: investment and profitability earn about four "
            "and six percent a year, and their later expected-growth factor nearly ten, with a t-statistic above "
            "ten. Value, again, has no alpha against them."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.25), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def contest(self):
        cards = VGroup(
            desk_question(r"which model?", r"Barillas and Shanken (2018): compare models by the squared Sharpe ratio "
                          r"their factors reach. Both FF5 and q beat FF3; adding momentum helps either; there is no clean "
                          r"winner", width=12.0, font_size=20),
            desk_question(r"which reason?", r"Fama and French read the factors as risk; Hou, Xue and Zhang as the "
                          r"firm's optimal investment, whatever the cause of the discount rate; Stambaugh and Yuan (2017) "
                          r"as mispricing", width=12.0, font_size=20),
            desk_question(r"a caution", r"EG is built from a forecast of investment growth fitted on the same data: a "
                          r"$t$ of ten needs the trial count of Part 25 beside it", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Which model wins? <bookmark mark='a'/> Francisco Barillas and Jay Shanken showed how to compare them: by "
            "the best squared Sharpe ratio their factors can reach. Both the five-factor and the q models beat three "
            "factors, and adding momentum helps either; there is no clean winner. <bookmark mark='b'/> They also "
            "disagree about why: Fama and French read the factors as risk, Hou, Xue and Zhang as the firm's optimal "
            "investment whatever drives the discount rate, and Robert Stambaugh and Yu Yuan as mispricing. "
            "<bookmark mark='c'/> And a caution: the expected-growth factor uses a forecast fitted on the same data it "
            "is tested on. A t-statistic of ten deserves the scrutiny of Part twenty-five."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"in the five-factor model HML has no alpha. Should an investor who holds RMW and CMA still hold value? "
                r"What would change your answer?")
        with self.voiceover("In the five-factor model value has no alpha. Should an investor who holds profitability and "
                            "investment still hold value? What would change your answer?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
