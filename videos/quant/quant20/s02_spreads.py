from __future__ import annotations

from videos.quant.quant20.common import lesson_cards

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, PART, RISKY, SAFE, ZERO, ask, fit_right, illustration, load


class Spreads(VoiceoverScene):
    def construct(self):
        s = load("spreads")
        self.card()
        self.history(s)
        self.quality(s)
        self.anatomy()
        self.puzzle()
        self.feedback()

    def card(self):
        c = chapter_card(1, r"What a credit spread measures", r"Why does a risky bond yield more?", part=PART)
        with self.voiceover("Chapter one. The credit spread: what the extra yield on a risky bond pays for."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def history(self, s):
        t, b, a = np.asarray(s["t"]), np.asarray(s["baa"]), np.asarray(s["aaa"])
        rt, rv = np.asarray(s["rec_t"]), np.asarray(s["rec"])
        g = axes([1953, 2026], [-1, 7], x_length=8.8, y_length=4.4, xlabel=r"year",
                 ylabel=r"yield minus the 10-year Treasury, \%", xticks=[1960, 1970, 1980, 1990, 2000, 2010, 2020],
                 yticks=[0, 2, 4, 6], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        bands = VGroup()
        on = None
        for x_, r_ in zip(rt, rv):
            if r_ > 0.5 and on is None:
                on = x_
            if r_ < 0.5 and on is not None:
                bands.add(Rectangle(width=ax.c2p(x_, 0)[0] - ax.c2p(on, 0)[0], height=ax.c2p(0, 7)[1] - ax.c2p(0, -1)[1],
                                    stroke_width=0, fill_color=GREY_B, fill_opacity=0.18).move_to(
                    [(ax.c2p(on, 0)[0] + ax.c2p(x_, 0)[0]) / 2, (ax.c2p(0, 7)[1] + ax.c2p(0, -1)[1]) / 2, 0]))
                on = None
        lb = curve(ax, t, b, RISKY, stroke_width=2.2)
        la = curve(ax, t, a, SAFE, stroke_width=2.2)
        zero = Line(ax.c2p(1953, 0), ax.c2p(2026, 0), color=GREY_C, stroke_width=1)
        pk = s["peaks"]
        side = VGroup(
            legend([(RISKY, r"Moody's Baa"), (SAFE, r"Moody's Aaa"), (GREY_B, r"recessions (NBER)")], font_size=17),
            MathTex(rf"\text{{average: Baa }} {s['mean_baa']:.2f}\%,\ \text{{Aaa }} {s['mean_aaa']:.2f}\%", font_size=24),
            wrapped_label(rf"daily peaks: {pk['2008']['v']:.2f}\% (December 2008), {pk['2020']['v']:.2f}\% (23 March "
                          rf"2020). End of 2025: {s['end']:.2f}\%. Descriptive sample; Treasury maturity, duration and liquidity differences remain",
                          3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"Moody's seasoned Aaa and Baa yields are broad corporate yield measures. This chart subtracts a ten-year Treasury yield; it is not a duration-matched option-adjusted credit spread. <bookmark mark='a'/> The grey bands mark recessions. Spreads often widen in stressed periods, but the chart alone does not establish a recession forecast. The sample average Baa gap is {s['mean_baa']:.1f} percent. <bookmark mark='b'/> The saved daily series reaches {pk['2008']['v']:.2f} percent in December twenty oh eight and {pk['2020']['v']:.2f} on March twenty-third, twenty twenty. The latter coincides with the Federal Reserve's corporate-credit announcement; coincidence in this chart does not identify the causal announcement effect."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(bands), FadeIn(side[0]))
            self.play(Create(lb), Create(la), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.add(illustration(r"FRED: BAA, AAA, GS10 (monthly), BAA10Y (daily), USREC"))
        self.wait(0.4)
        self.clear_scene()

    def quality(self, s):
        t, gap = np.asarray(s["t"]), np.asarray(s["baa"]) - np.asarray(s["aaa"])
        g = axes([1953, 2026], [0, 3.6], x_length=8.6, y_length=4.2, xlabel=r"year", ylabel=r"Baa minus Aaa, \%",
                 xticks=[1960, 1970, 1980, 1990, 2000, 2010, 2020], yticks=[0, 1, 2, 3], font_size=14).to_edge(
            LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, gap, BAD, stroke_width=2.4)
        k = int(np.argmax(gap))
        side = VGroup(
            MathTex(rf"\text{{average}} = {gap.mean():.2f}\%", font_size=28),
            MathTex(rf"\max = {gap[k]:.2f}\%\ (\text{{{int(t[k])}}})", font_size=28, color=BAD),
            wrapped_label(r"both are investment grade, both are long corporate bonds: the gap compares a step "
                          r"down in quality, with duration, liquidity and composition differences still present. It widened "
                          r"most of all in 1980--82 and 2008", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"The Baa-minus-Aaa yield gap removes a common Treasury benchmark, but it is not pure default risk. The bond groups can still differ in duration, liquidity, embedded options, composition and risk premia. <bookmark mark='a'/> In the saved sample the gap averages {gap.mean():.2f} percent and reaches {gap[k]:.2f} in {int(t[k])}. It is a descriptive credit-quality comparison. Identifying expected losses alone requires a model, matched instruments and assumptions about recovery and the pricing measure."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def anatomy(self):
        rows = [cmath(r"y_{\text{risky}} - y_{\text{safe}}", r"\approx", r"\underbrace{\lambda^{P}\,(1 - R)}_{\text{physical expected loss}} + "
                      r"\underbrace{\text{risk premium}}_{\text{bad times}} + \underbrace{\text{liquidity}}_{\text{hard to "
                      r"sell}}", font_size=34, colors={r"y_{\text{risky}} - y_{\text{safe}}": RISKY}),
                cmath(r"s_{\mathrm{CDS}}", r"\approx", r"\lambda^{Q}\,(1 - R)", font_size=40, colors={r"s_{\mathrm{CDS}}": RISKY})]
        whys = [why(r"heuristic decomposition: physical expected loss, compensation for priced credit risk, and differences in "
                    r"liquidity, contracts, duration and composition; these terms are not separately identified here"),
                why(r"flat continuous-premium CDS triangle: risk-neutral intensity $\lambda^Q$ times loss given default $1-R$; "
                    r"with recovery 40\%, a 100 bp spread gives pricing intensity about 1.67\% per year, not physical PD")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "A broad corporate yield gap can reflect physical expected losses, compensation for priced credit risk and liquidity or instrument differences. The first line is a heuristic decomposition, not a separately identified accounting identity. <bookmark mark='a'/> Keep the probability measure explicit. Physical intensity times loss given default approximates physical expected annual loss. By contrast, the credit triangle relates a CDS par spread to risk-neutral intensity under flat continuous-premium assumptions. A one hundred basis point CDS spread with forty percent recovery implies pricing intensity of about one point six six seven percent per year, not a physical default forecast. Finite-horizon probability is one minus exponential survival; exact traded prices require contract and curve conventions."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def puzzle(self):
        cards = VGroup(
            desk_question(r"Huang and Huang (2012)", 'Structural models calibrated to historical defaults and recovery explain a limited share of investment-grade spreads in their study. Credit-risk pricing includes more than physical expected loss.',
                          width=12.0, font_size=22),
            desk_question(r"Longstaff, Mithal and Neis (2005)", 'CDS-based estimation finds a larger default-related component in their sample; contract, liquidity, counterparty and identification assumptions still matter.', width=12.0, font_size=22),
            desk_question(r"Collin-Dufresne, Goldstein and Martin (2001)", 'Residual spread changes contain a substantial common component beyond their explanatory variables; this is a sample finding, not a complete decomposition.',
                          width=12.0, font_size=22),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "The credit-spread puzzle depends on model and measurement choices. Huang and Huang calibrate structural models to historical default and recovery evidence; their estimated credit-risk component explains a limited portion of investment-grade spreads. That component includes pricing for credit risk, rather than only physical expected loss. <bookmark mark='a'/> Longstaff, Mithal and Neis use CDS to estimate default and nondefault components and obtain a larger default-related share in their sample. CDS still have contractual, liquidity and counterparty effects, so the study is not a frictionless decomposition valid for every bond. <bookmark mark='b'/> Collin-Dufresne, Goldstein and Martin find a substantial common component in residual spread changes beyond their explanatory variables. These studies ask related questions using different samples, contracts and identification assumptions; they do not uniquely identify the components of our broad yield-gap chart."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a Baa bond yields 2\% over Treasuries. Suppose issuers like it default 0.3\% a year and lose 60\%. What "
                r"is the rest of the 2\% paying for?")
        with self.voiceover('A Baa bond yields two percent over Treasuries. Suppose issuers like it have a physical annual event rate of point three percent and lose sixty percent on default. What is the rest paying for?'):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def feedback(self):
        title = wrapped_label('Answer: a spread is not a physical default frequency', 12.4, 32, QC.IDEA).to_edge(UP, buff=.6)
        answer = wrapped_label('First-order physical expected loss is 18 bp. The remaining 182 bp of a 200 bp yield gap combines premia, liquidity and instrument differences; it is not a uniquely identified component.', 11.8, 27, GREY_A).move_to(ORIGIN)
        with self.voiceover('Using the supplied physical annual event rate of point three percent and loss given default of sixty percent, first-order expected annual loss is eighteen basis points. Subtracting this from a two hundred basis point yield gap leaves one hundred eighty-two basis points arithmetically. That is not a uniquely identified risk premium: liquidity, duration, instrument differences and the approximation can also contribute. The credit triangle itself is a pricing relation under stated recovery and payment conventions.') as vo:
            self.play(FadeIn(title), FadeIn(answer))
        self.wait(.5)
        self.clear_scene()
