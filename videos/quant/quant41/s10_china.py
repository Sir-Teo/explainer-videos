from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant41.common import (BAD, FUND_C, GOOD, HURDLE, LEV_C, PART, PRICE_C, SAFE_C, SPIRAL_C, comma, load)


def _t(d):
    d = np.array([int(str(x).replace("-", "")[:8]) for x in d])
    return (d // 10000) + ((d // 100) % 100 - 1) / 12 + (d % 100) / 365


class China(VoiceoverScene):
    def construct(self):
        x = load("china")
        self.card(x)
        self.index(x)
        self.margin()
        self.rescue()
        self.breaker(x)
        self.magnet()
        self.question()

    def card(self, x):
        c = chapter_card(9, r"2015: a leveraged boom in Shanghai", r"What happens when the margin lenders are everywhere and "
                         r"the exit is a single door?", part=PART)
        with self.voiceover(
            f"Chapter nine, and the answer to the pause: from a peak of {x['peak']:,.0f} on the twelfth of June twenty "
            f"fifteen, the Shanghai Composite fell {100 * -x['fall']:.0f} percent in eleven weeks, to {x['low']:,.0f} on "
            "the twenty-sixth of August. Much of the way up had been bought on margin; much of the way down was margin "
            "calls."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def index(self, x):
        t = _t(x["d"])
        c = np.asarray(x["c"], float)
        g = axes([2014.4, 2016.3], [1800, 5400], x_length=9.4, y_length=4.4, xlabel=r"June 2014 to March 2016",
                 ylabel=r"Shanghai Composite", xticks=[2015, 2016], yticks=[2000, 3000, 4000, 5000],
                 yfmt=lambda u: comma(u), font_size=15).move_to(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, c, PRICE_C, stroke_width=2.5)
        pk_t = float(_t([x["peak_day"]])[0])
        lo_t = float(_t([x["low_day"]])[0])
        d1 = Dot(ax.c2p(pk_t, x["peak"]), color=BAD, radius=0.07)
        d2 = Dot(ax.c2p(lo_t, x["low"]), color=BAD, radius=0.07)
        l1 = label(rf"12 Jun 2015: {comma(x['peak'])}", font_size=17, color=BAD).next_to(d1, UP, buff=0.12)
        l2 = label(rf"26 Aug: {comma(x['low'])}", font_size=17, color=BAD).next_to(d2, DOWN + RIGHT, buff=0.1)
        cb = x["cb"]
        r1 = 100 * cb["20160104"]
        r2 = 100 * cb["20160107"]
        l3 = label(rf"Jan 2016: {r1:.1f}\%, {r2:.1f}\%", font_size=17, color=SPIRAL_C)
        l3.next_to(ax.c2p(2016.02, 3000), UP + LEFT, buff=0.15)
        with self.voiceover(
            "The index, from public data. <bookmark mark='a'/> From about "
            f"{x['start']:,.0f} in July twenty fourteen it rose {100 * x['rise']:.0f} percent in eleven months. "
            "<bookmark mark='b'/> Then it fell by more than four tenths in under three months, with days of eight percent "
            "falls. <bookmark mark='c'/> And in the first week of twenty sixteen, two more: "
            f"{r1:.1f} and {r2:.1f} percent, the days of the circuit breaker."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), run_time=3)
            self.play(FadeIn(d1), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(d2), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(l3))
        self.wait(0.4)
        self.clear_scene()

    def margin(self):
        rows = [cmath(r"\text{brokers' margin loans}", r":", r"\text{over 2 trillion yuan at the peak}", font_size=36,
                      colors={r"\text{brokers' margin loans}": LEV_C}),
                cmath(r"\text{grey-market margin}", r":", r"\text{umbrella trusts and peer lenders, up to } 5\text{--}10\times",
                      font_size=34, colors={r"\text{grey-market margin}": SPIRAL_C}),
                cmath(r"\text{the trigger}", r":", r"\text{the regulator curbs grey margin, June 2015}", font_size=34),
                cmath(r"\text{the spiral}", r":", r"\text{forced sales} \to \text{limit-down} \to \text{more forced sales}",
                      font_size=34, colors={r"\text{the spiral}": SPIRAL_C})]
        whys = [why(r"official margin financing on the two exchanges, as reported in June 2015"),
                why(r"off-exchange lending to retail investors through account-splitting software, with automatic "
                    r"liquidation; Bian, He, Shue and Zhou study it with account data"),
                why(r"tighter rules on the off-exchange channel, the deleveraging that began the fall, as reported"),
                why(r"a 10\% daily limit meant a forced seller often could not sell at all, so the selling moved to other "
                    r"stocks and to the next day: Chapter 3's fire sale with a lock on the door")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "How the boom was financed. <bookmark mark='a'/> Brokers' margin loans passed two trillion yuan. "
            "<bookmark mark='b'/> And around them a grey market: umbrella trusts and lending platforms that gave retail "
            "investors five or ten times leverage, with automatic liquidation. Bian, He, Shue and Zhou later traced it "
            "account by account. <bookmark mark='c'/> In June the regulator moved to curb the grey channel. "
            "<bookmark mark='d'/> The rest was Chapter three, with a lock on the door: forced sales hit the ten percent "
            "daily limit, a seller who could not sell one stock sold another, and the selling spread."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def rescue(self):
        cards = VGroup(
            desk_question(r"a national team", r"a state-backed fund, financed by the central bank through the securities "
                          r"finance company, bought shares directly, as reported", width=12.4, font_size=19),
            desk_question(r"selling made difficult", r"large shareholders were barred from selling for six months; new "
                          r"listings were suspended", width=12.4, font_size=19),
            desk_question(r"half the market stopped", r"in early July, around half the listed companies had "
                          r"suspended trading in their own shares, as reported", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The response, as reported. <bookmark mark='a'/> A national team: state-backed buyers financed through the "
            "securities finance company, with central-bank money. <bookmark mark='b'/> Large shareholders were barred "
            "from selling, and new listings stopped. <bookmark mark='c'/> And in early July around half the listed companies "
            "suspended trading in their own shares. If you cannot sell what you hold, Chapter three says you sell what "
            "you can: the stocks that stayed open, and markets abroad."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def breaker(self, x):
        cb = x["cb"]
        r1 = 100 * cb["20160104"]
        r2 = 100 * cb["20160107"]
        rows = [cmath(r"\text{rule}", r":", r"\text{CSI 300 down } 5\% \Rightarrow 15\text{-minute halt}", font_size=38,
                      colors={r"\text{rule}": FUND_C}),
                cmath(r"", r"", r"\text{down } 7\% \Rightarrow \text{closed for the day}", font_size=38),
                cmath(r"\text{4 January}", r":", rf"\text{{Shanghai }} {r1:.1f}\%,\ \text{{halted early afternoon}}", font_size=36,
                      colors={r"\text{4 January}": BAD}),
                cmath(r"\text{7 January}", r":", rf"\text{{Shanghai }} {r2:.1f}\%,\ \text{{closed within half an hour}}",
                      font_size=36, colors={r"\text{7 January}": BAD})]
        whys = [why(r"a market-wide circuit breaker, in force from the first trading day of 2016"),
                why(r"the two thresholds only two percentage points apart"),
                why(r"the first threshold was hit, the halt ended, and the second came minutes later"),
                why(r"the rule was suspended that night, four days after it began")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "And the circuit breaker. <bookmark mark='a'/> From the first trading day of twenty sixteen: if the CSI three "
            "hundred fell five percent, trading halted for fifteen minutes; <bookmark mark='b'/> at seven percent, it "
            "closed for the day. <bookmark mark='c'/> On the fourth of January both thresholds were hit, minutes apart. "
            "<bookmark mark='d'/> On the seventh, the market closed within half an hour of opening, and that night the "
            "rule was suspended."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def magnet(self):
        rows = [cmath(r"\text{a halt at } b", r":", r"\text{after it, you cannot sell}", font_size=40, colors={r"\text{a halt at } b": FUND_C}),
                cmath(r"\text{so near } b", r":", r"\text{sell now, before the door closes}", font_size=40,
                      colors={r"\text{so near } b": SPIRAL_C}),
                cmath(r"\Rightarrow", r"", r"\text{prices accelerate toward the threshold}", font_size=40),
                cmath(r"\text{the fix}", r":", r"\text{thresholds far apart, a pause, not a closing}", font_size=36,
                      colors={r"\text{the fix}": SAFE_C})]
        whys = [why(r"a trader who expects to need liquidity values it most just before it disappears"),
                why(r"the option to trade later is worth less as the price nears the barrier"),
                why(r"the magnet effect: Subrahmanyam's 1994 model; Chen, Petukhov and Wang's ``dark side of circuit "
                    r"breakers'', with China's 2016 episode as the example"),
                why(r"US breakers sit at 7, 13 and 20\% of the S\&P 500, and only the last closes the market")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Why a breaker can pull prices toward itself. <bookmark mark='a'/> After a halt you cannot sell. "
            "<bookmark mark='b'/> So as the price nears the threshold, a trader who might need to sell should sell now, "
            "before the door closes. <bookmark mark='c'/> And their selling moves the price toward the threshold: the "
            "magnet effect, modelled by Subrahmanyam in nineteen ninety-four, and by Chen, Petukhov and Wang with China's "
            "episode in mind. <bookmark mark='d'/> The design lesson: thresholds far apart, and a pause rather than a "
            "closing. America's breakers sit at seven, thirteen and twenty percent."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        q = pause_card(r"in 2022 the Fed raised rates faster than at any time in forty years. A bank's long bonds, on its books "
                       r"at 100, are now worth 85; it owes depositors 90. What happens if they leave?")
        with self.voiceover(
            "Pause and predict. In twenty twenty-two the Federal Reserve raised rates faster than at any time in forty "
            "years. A bank's long bonds, on its books at a hundred, are now worth eighty-five, and it owes its depositors "
            "ninety. What happens if they leave?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
