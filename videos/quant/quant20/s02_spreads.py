from __future__ import annotations

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
                          rf"2020). End of 2025: {s['end']:.2f}\%. The spread widens before and during every recession",
                          3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Moody's has published the yields of seasoned corporate bonds since 1919. Here is the gap over the "
            "ten-year Treasury, month by month since 1953, for the safest grade, Aaa, and the lowest investment "
            "grade, Baa. <bookmark mark='a'/> The grey bands are recessions. The spread widens before and during "
            f"every one, and Baa's averaged {s['mean_baa']:.1f} percent. <bookmark mark='b'/> Its daily peaks: "
            f"{pk['2008']['v']:.2f} percent in December 2008, and {pk['2020']['v']:.2f} on the twenty-third of March "
            "2020, the day the Federal Reserve said it would buy corporate bonds."
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
            wrapped_label(r"both are investment grade, both are long corporate bonds: the gap prices only the step "
                          r"down in quality, without the Treasury market's own quirks. It widens in every recession, "
                          r"most of all in 1980--82 and 2008", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "A cleaner measure of default risk alone is the gap between the two grades: both are corporate bonds, "
            "both long, both investment grade, so the Treasury market's own quirks cancel. <bookmark mark='a'/> It "
            f"averaged {gap.mean():.2f} percent and reached {gap[k]:.2f} at the end of {int(t[k])}. The price of one "
            "step down in quality is small in calm years and widens in every recession, most of all in the early "
            "eighties and in 2008."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def anatomy(self):
        rows = [cmath(r"y_{\text{risky}} - y_{\text{safe}}", r"=", r"\underbrace{\lambda\,(1 - R)}_{\text{expected loss}} + "
                      r"\underbrace{\text{risk premium}}_{\text{bad times}} + \underbrace{\text{liquidity}}_{\text{hard to "
                      r"sell}}", font_size=34, colors={r"y_{\text{risky}} - y_{\text{safe}}": RISKY}),
                cmath(r"s", r"\approx", r"\lambda\,(1 - R)", font_size=40, colors={r"s": RISKY})]
        whys = [why(r"a spread pays for three things: the losses you expect, the fact that defaults cluster in "
                    r"recessions, when losses hurt most, and the cost of selling a bond that rarely trades"),
                why(r"the credit triangle: a spread is a default rate $\lambda$ times the loss given default $1 - R$; "
                    r"with recovery 40\%, a 100 bp spread implies about 1.7\% a year")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "What does that extra yield pay for? Three things. The losses you expect: how often borrowers like this "
            "default, times how much is lost when they do. A premium for when those losses arrive, bunched in "
            "recessions, when everything else is falling too. And liquidity: a corporate bond can take days to sell. "
            "<bookmark mark='a'/> The first part has a rule of thumb, the credit triangle: the spread is the default "
            "rate times the fraction lost. With forty percent recovered, a spread of one hundred basis points implies "
            "a default rate of about one point seven percent a year."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def puzzle(self):
        cards = VGroup(
            desk_question(r"Huang and Huang (2012)", r"calibrate structural models to historical default and recovery "
                          r"rates: for investment-grade bonds they explain only a small part of the spread; for junk "
                          r"bonds, most of it. The rest of an investment-grade spread is risk premium and liquidity",
                          width=12.0, font_size=22),
            desk_question(r"Longstaff, Mithal and Neis (2005)", r"use credit default swaps, which isolate default: the "
                          r"default component is the majority of corporate spreads, and the remainder moves with "
                          r"measures of bond-market liquidity", width=12.0, font_size=22),
            desk_question(r"Collin-Dufresne, Goldstein and Martin (2001)", r"changes in spreads are driven mostly by one "
                          r"common factor that firm-level variables (leverage, volatility, rates) do not explain",
                          width=12.0, font_size=22),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "How big is each part? This is the credit spread puzzle. Jing-Zhi Huang and Ming Huang calibrated models "
            "to how often firms actually default and how much they repay: for investment-grade bonds, expected losses "
            "explain only a small part of the spread. <bookmark mark='a'/> Using credit default swaps, which strip "
            "out the bond itself, Longstaff, Mithal and Neis found default to be the larger share, with the remainder "
            "moving with liquidity. <bookmark mark='b'/> And Collin-Dufresne, Goldstein and Martin found that spreads "
            "move together, driven by a common factor that the companies' own numbers do not explain. A spread is a "
            "price of default risk, and of much else."
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
        with self.voiceover("A Baa bond yields two percent over Treasuries. Suppose issuers like it default a third of a "
                            "percent a year and lose sixty percent. What is the rest paying for?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
