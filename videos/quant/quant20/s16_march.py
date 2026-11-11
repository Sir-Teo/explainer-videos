from __future__ import annotations

from videos.quant.quant20.common import lesson_cards

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, GOOD, PART, RISKY, SAFE, ask, fit_right, illustration, load


def _t(d):
    d = np.asarray(d)
    return (d // 100 % 100 - 1) * 30.5 + d % 100  # day of the year, roughly


class March(VoiceoverScene):
    def construct(self):
        m = load("march2020")
        self.card()
        self.etfs(m)
        self.spread(m)
        self.facilities()
        self.factors()
        self.feedback()

    def card(self):
        c = chapter_card(15, r"Corporate bonds and March 2020", r"Can the safest corporate bonds stop trading?",
                         lit=(2020,), part=PART)
        with self.voiceover("Chapter fifteen. Corporate bond markets, and three weeks in March 2020."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def etfs(self, m):
        g = axes([0, 182], [60, 110], x_length=8.0, y_length=4.4, xlabel=r"2020",
                 ylabel=r"price, as \% of 20 February", xticks=[], yticks=[70, 80, 90, 100], font_size=14
                 ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        months = VGroup(*[label(mn, font_size=16, color=GREY_B).next_to(ax.c2p(x, 60), DOWN, buff=0.15)
                          for mn, x in zip(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], [15, 46, 75, 106, 136, 167])])
        lines = VGroup()
        for tk, c_ in (("LQD", SAFE), ("HYG", BAD)):
            d, p = np.asarray(m[tk]["date"]), np.asarray(m[tk]["close"])
            base = p[np.searchsorted(d, 20200220)]
            lines.add(curve(ax, _t(d), 100 * p / base, c_, stroke_width=2.8))
        ev = VGroup()
        for d, txt in ((20200323, r"23 Mar: the Fed's corporate credit facilities"), (20200409, r"9 Apr: expanded")):
            x = _t(d)
            ev.add(VGroup(DashedLine(ax.c2p(x, 60), ax.c2p(x, 110), color=GREY_B, stroke_width=1.5),
                          label(txt, font_size=15, color=GREY_A).next_to(ax.c2p(x, 108), RIGHT, buff=0.08)))
        ev[1][1].next_to(ax.c2p(_t(20200409), 104), RIGHT, buff=0.08)
        lq, hy = m["LQD"], m["HYG"]
        side = VGroup(
            legend([(SAFE, r"LQD: investment-grade bond ETF"), (BAD, r"HYG: high-yield bond ETF")], font_size=17),
            MathTex(rf"\text{{LQD}}: {100 * lq['drawdown']:.0f}\%\ \text{{by {lq['low']['date'] % 100} March}}", font_size=24,
                    color=SAFE),
            MathTex(rf"\text{{HYG}}: {100 * hy['drawdown']:.0f}\%\ \text{{by {hy['low']['date'] % 100} March}}", font_size=24,
                    color=BAD),
            wrapped_label('ETF shares and underlying bonds have different observation clocks and liquidity. A discount to a reported NAV does not by itself identify which price is executable or the source of the gap', 3.6, 17,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"These are unadjusted exchange closing prices, rebased for the selected March twenty twenty window, not total returns including distributions. <bookmark mark='a'/> The saved investment-grade ETF price drawdown is {abs(100 * lq['drawdown']):.0f} percent and the high-yield ETF's {abs(100 * hy['drawdown']):.0f} percent under that window's convention. Trading prices can differ from published fund NAV when underlying bond quotes are stale or costly to execute. <bookmark mark='b'/> The Federal Reserve announced corporate-credit facilities on March twenty-third. The April ninth expansion covered certain recently downgraded issuers and high-yield ETFs, not unrestricted purchases of all high-yield bonds. Event studies examine announcement effects and eligibility, but this price chart alone cannot separate those effects from pandemic news and other policy responses."
        ) as vo:
            self.play(FadeIn(g), FadeIn(months), FadeIn(side[0]))
            self.play(Create(lines), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(ev))
        self.add(illustration(r"Yahoo Finance closes; Federal Reserve press releases, 23 March and 9 April 2020"))
        self.wait(0.4)
        self.clear_scene()

    def spread(self, m):
        d, v = np.asarray(m["baa"]["date"]), np.asarray(m["baa"]["v"])
        g = axes([0, 182], [1.5, 4.6], x_length=8.0, y_length=4.2, xlabel=r"2020", ylabel=r"Baa minus 10-year Treasury, \%",
                 xticks=[], yticks=[2, 3, 4], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        months = VGroup(*[label(mn, font_size=16, color=GREY_B).next_to(ax.c2p(x, 1.5), DOWN, buff=0.15)
                          for mn, x in zip(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], [15, 46, 75, 106, 136, 167])])
        line = curve(ax, _t(d), v, RISKY, stroke_width=3)
        k = int(np.argmax(v))
        k0 = int(np.searchsorted(d, 20200220))
        top = Dot(ax.c2p(_t(d[k]), v[k]), color=BAD)
        mark = DashedLine(ax.c2p(_t(20200323), 1.5), ax.c2p(_t(20200323), 4.6), color=GREY_B, stroke_width=1.5)
        side = VGroup(
            MathTex(rf"{v[k0]:.2f}\% \to {v[k]:.2f}\%", font_size=30, color=BAD),
            label(rf"20 February to {d[k] % 100} March", font_size=18, color=GREY_A),
            MathTex(rf"\text{{30 June: }} {v[-1]:.2f}\%", font_size=26),
            wrapped_label('spread movements and policy announcements share this timeline. The chart describes co-movement; it does not identify a causal effect or separate credit risk from liquidity', 3.4, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"The Baa-minus-ten-year-Treasury series rises from {v[k0]:.2f} percent at the selected February twentieth observation to {v[k]:.2f} percent at its March peak, then ends this June window at {v[-1]:.2f}. <bookmark mark='a'/> This is a broad yield gap, with credit premia, liquidity and maturity differences as well as expected loss. <bookmark mark='b'/> Its decline coincides with support measures and changing economic expectations. The chart does not show that defaults alone were priced in, or identify what fraction the backstop removed. A causal policy estimate needs an identification strategy and comparison assets, rather than a before-and-after line."
        ) as vo:
            self.play(FadeIn(g), FadeIn(months), Create(mark))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(top), FadeIn(side[0]), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def facilities(self):
        rows = [cmath(r"\text{PMCCF} + \text{SMCCF}", r"\to", r"\text{the Fed as buyer of last resort for corporate credit}",
                      font_size=32, colors={r"\text{PMCCF} + \text{SMCCF}": GOOD}),
                cmath(r"\Delta s", r"\not\equiv", r"\Delta s_{\text{policy}}", font_size=36,
                      colors={r"\Delta s": RISKY})]
        whys = [why('23 March announcements included investment-grade ETF support; 9 April expanded eligibility for specified fallen angels and high-yield ETFs. Announcement, eligibility and actual purchase dates are different'),
                why('Haddad, Moreira and Muir (2021) study the announcement and eligibility effects. A backstop is one interpretation; this chart alone cannot identify the unique credit, liquidity or policy channel')]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "The primary facility supported eligible new corporate issuance and the secondary facility supported eligible outstanding bonds and ETFs. Eligibility, maturity and rating rules limited the scope. The secondary facility's eventual holdings were modest relative to the overall corporate market. <bookmark mark='a'/> The literature studies the announcements, eligibility boundaries and subsequent purchases to distinguish channels. A backstop can affect liquidity and tail expectations before large purchases occur. Calling it an option is an economic analogy, not a literal freely exercisable guarantee for every bond. Its causal effect is not estimated by the descriptive figures in this lecture."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def factors(self):
        cards = VGroup(
            desk_question(r"credit factors", 'corporate-bond factor studies depend on data cleaning, return measurement and model specification. Bai, Bali and Wen (2019) and Dickerson, Mueller and Robotti (2023) address different measurements and tests', width=12.0,
                          font_size=21),
            desk_question(r"the distress puzzle", 'Campbell, Hilscher and Szilagyi (2008) document a study-specific distress-return puzzle. Physical failure probability alone does not determine expected returns; priced covariance, selection and measurement matter', width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Two research debates return later. Corporate-bond factor findings depend on pricing, return construction, liquidity filters and the comparison model; the cited papers study different specifications and data issues. <bookmark mark='a'/> The distress-return puzzle asks why high predicted failure risk has sometimes accompanied low subsequent equity returns in particular historical samples. A high physical default probability alone does not imply a high expected return: priced covariance, investor constraints, selection and measurement matter. These are literature results, not new forecast trials in this review. Part twenty-five examines the evidence and competing interpretations."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        q = ask(r"an ETF trades 5\% below the value its sponsor reports for its bonds. Which price is wrong?")
        with self.voiceover("A bond fund trades five percent below the value its sponsor reports for its bonds. Which "
                            "price is wrong?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def feedback(self):
        title = wrapped_label('Answer: NAV and execution prices can use different information', 12.4, 32, QC.IDEA).to_edge(UP, buff=.6)
        answer = wrapped_label('A discount alone does not identify which price is wrong. Check timestamps, stale bond quotes, bid-ask costs, creation/redemption and executable portfolio value.', 11.8, 27, GREY_A).move_to(ORIGIN)
        with self.voiceover('A five percent discount to published NAV does not by itself identify the wrong price. Check the valuation timestamps, stale underlying quotes, bid-ask costs, creation and redemption constraints, and what the bond portfolio could actually be sold for. The ETF can contribute price discovery while its own price also reflects liquidity and financing conditions.') as vo:
            self.play(FadeIn(title), FadeIn(answer))
        self.wait(.5)
        self.clear_scene()
