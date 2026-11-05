from __future__ import annotations

import math

from explainer.quant import *  # noqa: F403
from videos.quant.quant34.common import BAD, FIRM_C, GOOD, HURDLE, LAW_C, PART, PLAT_C, PM_C, STOP_C, fit_right


class Risk(VoiceoverScene):
    def construct(self):
        self.card()
        self.layers()
        self.limits()
        self.liquidity()
        self.stress()
        self.crisis_corr()
        self.knight()
        self.controls()
        self.archegos()
        self.question()

    def card(self):
        c = chapter_card(5, r"Risk at the level of the firm", r"What can a firm lose in a day, and who can stop it?",
                         part=PART)
        with self.voiceover("Chapter five. A desk's risk model, from Part thirty-one, measures a book. A firm's risk "
                            "function has a harder job: to add up every book, to find the losses no model sees, and to be "
                            "able to stop trading in seconds."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def layers(self):
        rows = [cmath(r"\text{pre-trade}", r":", r"\text{size, price and rate checks on every order}", font_size=32,
                      colors={r"\text{pre-trade}": STOP_C}),
                cmath(r"\text{intraday}", r":", r"\text{positions, P\&L and exposures, live}", font_size=32,
                      colors={r"\text{intraday}": HURDLE}),
                cmath(r"\text{end of day}", r":", r"\text{factor risk, stress, liquidity, limits}", font_size=32,
                      colors={r"\text{end of day}": PLAT_C}),
                cmath(r"\text{governance}", r":", r"\text{who may override, and who is told}", font_size=32,
                      colors={r"\text{governance}": FIRM_C})]
        whys = [why(r"in microseconds, before an order leaves the firm: the layer that would have saved Knight Capital"),
                why(r"every desk's positions and profit in one place, so the firm sees a loss before the desk explains it"),
                why(r"Part 31's model on the whole firm, plus the scenarios no model covers"),
                why(r"limits mean nothing unless someone independent of the trader can enforce them")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "Four layers. <bookmark mark='a'/> Pre-trade checks on every order, in microseconds, before it leaves the "
            "firm. <bookmark mark='b'/> Intraday: every desk's positions and profit in one place, live. "
            "<bookmark mark='c'/> End of day: Part thirty-one's factor model on the whole firm, plus stress tests and "
            "liquidity. <bookmark mark='d'/> And governance: who may override a limit, and who must be told. Limits mean "
            "nothing without someone independent of the trader to enforce them."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def limits(self):
        hx = [-3.6, 2.2]
        head = VGroup(label(r"limit", font_size=18, color=GREY_B), label(r"what it caps", font_size=18, color=GREY_B))
        data = [(r"volatility budget", r"the book's forecast volatility, from the risk model"),
                (r"gross and net", r"leverage, and the market exposure left after hedges"),
                (r"factor exposures", r"market, sector, style betas: what a pod is not paid to hold"),
                (r"concentration", r"any one name, issuer or counterparty"),
                (r"liquidity", r"days to exit at a fraction of normal volume"),
                (r"drawdown", r"the loss from the peak that halves or ends a book (Chapter 3)")]
        tab = VGroup(head)
        for a, b in data:
            tab.add(VGroup(label(a, font_size=19, color=PM_C), label(b, font_size=17)))
        for j, row in enumerate(tab):
            row[0].move_to([hx[0], 2.4 - 0.7 * j, 0])
            row[1].move_to([hx[1], 2.4 - 0.7 * j, 0])
        with self.voiceover(
            "The limits a desk lives under. <bookmark mark='a'/> A volatility budget from the risk model; gross and net "
            "exposure; factor betas, the risks a pod is not paid to hold; concentration in any one name or counterparty; "
            "liquidity, in days to exit; and the drawdown rule of Chapter three. Each is a number the trader can see "
            "and the risk desk can enforce."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab[1:]], lag_ratio=0.4, run_time=5))
        self.wait(0.4)
        self.clear_scene()

    def liquidity(self):
        pos, adv, part = 50e6, 20e6, 0.10
        days = pos / (part * adv)
        sig = 0.02
        cost = sig * math.sqrt(part) * 1.0
        rows = [cmath(r"\text{days to exit}", r"=", r"\frac{\text{position}}{\text{participation} \times \text{ADV}}",
                      font_size=36, colors={r"\text{days to exit}": HURDLE}),
                cmath(r"\$50\text{m},\ \text{ADV } \$20\text{m},\ 10\%", r"\Rightarrow", rf"{days:.0f}\ \text{{days}}",
                      font_size=32),
                cmath(r"\text{cost}", r"\approx", rf"\sigma\sqrt{{\text{{participation}}}} = {1e4 * cost:.0f}\ \text{{bp}}",
                      font_size=34, colors={r"\text{cost}": BAD})]
        whys = [why(r"the time to sell a position without being more than a set share of the market's volume"),
                why(r"a position of two and a half days' volume, sold at a tenth of the volume each day"),
                why(r"Part 31's square-root law with a 2\% daily volatility: and in a crisis volume falls and volatility "
                    r"rises, so both numbers get worse together")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Liquidity is a limit measured in time. <bookmark mark='a'/> Days to exit: the position over the share of "
            "daily volume the firm allows itself. <bookmark mark='b'/> Fifty million dollars in a stock that trades "
            f"twenty million a day, at a tenth of the volume, takes {days:.0f} days. <bookmark mark='c'/> And by Part "
            f"thirty-one's square-root law it costs about {1e4 * cost:.0f} basis points. In a crisis volume falls and "
            "volatility rises, so both get worse at once, which is why the limit is set for the crisis, not the average day."
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

    def stress(self):
        cards = VGroup(
            desk_question(r"historical scenarios", r"October 1987, August 2007 (Part 33), autumn 2008, March 2020 (Part "
                          r"32), 2022's bonds: replay today's book through each", width=12.4, font_size=19),
            desk_question(r"hypothetical scenarios", r"a factor moving five standard deviations, correlations going to "
                          r"one, a counterparty failing, an exchange closing", width=12.4, font_size=19),
            desk_question(r"reverse stress tests", r"start from the loss that would end the firm, and ask what would have "
                          r"to happen to cause it; then check it is not too likely", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Stress tests find the losses the model does not. <bookmark mark='a'/> Historical: replay today's book "
            "through 1987, August 2007, the autumn of 2008, March 2020 and 2022. <bookmark mark='b'/> Hypothetical: a "
            "factor moving five deviations, correlations going to one, a counterparty failing. "
            "<bookmark mark='c'/> And reverse: start from the loss that would end the firm, and ask what would have to "
            "happen to cause it."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def crisis_corr(self):
        n, rho_calm, rho_crisis = 50, 0.05, 0.4
        div_calm = math.sqrt(rho_calm + (1 - rho_calm) / n)
        div_crisis = math.sqrt(rho_crisis + (1 - rho_crisis) / n)
        rows = [cmath(r"\sigma_{\text{firm}}", r"=", r"\sigma\sqrt{\rho + (1 - \rho)/N}", font_size=36,
                      colors={r"\sigma_{\text{firm}}": PLAT_C}),
                cmath(rf"N = {n},\ \rho = {rho_calm}", r":", rf"\sigma_{{\text{{firm}}}} = {div_calm:.2f}\,\sigma",
                      font_size=34),
                cmath(rf"\rho = {rho_crisis}", r":", rf"\sigma_{{\text{{firm}}}} = {div_crisis:.2f}\,\sigma\quad "
                      rf"(\times {div_crisis / div_calm:.1f})", font_size=34, colors={r"\times": BAD})]
        whys = [why(r"$N$ desks of equal volatility $\sigma$ and average correlation $\rho$"),
                why(r"in calm markets, fifty nearly independent desks diversify the firm's risk to a quarter of one desk's"),
                why(r"in a crisis the correlations rise together, and the firm's volatility rises about two and a half times, with no change "
                    r"in any desk's position")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        r = div_crisis / div_calm
        with self.voiceover(
            "Why firm risk is not the sum of desk risks, until it is. <bookmark mark='a'/> With N desks of equal "
            "volatility and average correlation rho, the firm's volatility is this. <bookmark mark='b'/> Fifty desks "
            f"with a correlation of five hundredths diversify to {div_calm:.2f} of one desk's risk. "
            f"<bookmark mark='c'/> In a crisis, correlations rise together: at point four, {div_crisis:.2f}, about "
            f"{r:.1f} times as much, with no desk changing a single position. Limits set on calm correlations are "
            "breached by the market, not by the traders."
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

    def knight(self):
        card = crisis_card(r"1 August 2012", r"Knight Capital", body=r"a deployment left old, unused code active on one of eight "
                           r"servers; when markets opened it sent millions of unintended orders, and in about 45 minutes "
                           r"the firm accumulated positions that cost it more than \$460 million; the SEC's 2013 order "
                           r"found its controls inadequate under the market access rule, and the firm was taken over",
                           width=10.6, font_size=22).move_to(UP * 0.3)
        with self.voiceover(
            "The case every risk desk studies. <bookmark mark='a'/> On the first of August 2012, a software deployment "
            "at Knight Capital left old, unused code active on one of eight servers. When the market opened it sent "
            "millions of unintended orders, and in about forty-five minutes the firm built positions that cost it more "
            "than four hundred and sixty million dollars, according to the SEC's order, which found its controls "
            "inadequate under the market access rule. Within days the firm needed rescue capital, and it was later taken "
            "over."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card))
        self.wait(0.4)
        self.clear_scene()

    def controls(self):
        rows = [cmath(r"\text{price}", r":", r"\text{reject orders far from the market}", font_size=34),
                cmath(r"\text{size and rate}", r":", r"\text{cap shares per order, orders per second}", font_size=34),
                cmath(r"\text{credit}", r":", r"\text{cap the gross exposure an algorithm may build}", font_size=34),
                cmath(r"\text{kill switch}", r":", r"\text{one action cancels everything and stops sending}",
                      font_size=34, colors={r"\text{kill switch}": STOP_C})]
        whys = [why(r"fat-finger checks: the first line against a broken algorithm"),
                why(r"a runaway loop shows up as an impossible rate before it shows up as a loss"),
                why(r"the market access rule (SEC Rule 15c3-5, 2010) requires brokers to control the exposure of every "
                    r"client and of themselves"),
                why(r"and someone with the authority, and the habit, to press it")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "What would have stopped it. <bookmark mark='a'/> Price checks reject orders far from the market. "
            "<bookmark mark='b'/> Size and rate limits catch a runaway loop, which shows up as an impossible order rate "
            "before it shows up as a loss. <bookmark mark='c'/> Credit limits cap what any algorithm may build, as the "
            "SEC's market access rule of 2010 requires. <bookmark mark='d'/> And a kill switch, with someone who has the "
            "authority, and the habit, to press it."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def archegos(self):
        card = crisis_card(r"March 2021", r"Archegos", body=r"a family office held very large, concentrated stock positions "
                           r"through total-return swaps with several banks, none of which saw the whole; when the stocks "
                           r"fell it could not meet margin calls, and the banks that sold slowest lost the most: Credit "
                           r"Suisse reported a loss of about \$5.5 billion",
                           width=10.6, font_size=22).move_to(UP * 0.3)
        with self.voiceover(
            "The other side of the trade. <bookmark mark='a'/> In March 2021 the family office Archegos held very "
            "large, concentrated stock positions through swaps with several banks, and none of them saw the whole. When "
            "the stocks fell it could not meet its margin calls, and the banks that sold slowest lost the most; Credit "
            "Suisse reported a loss of about five and a half billion dollars. A firm's risk includes its "
            "counterparties' concentration, which it cannot see, only ask about."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a book holds 5 days of a stock's volume. In a crisis volume halves and volatility doubles. How "
                       r"do its days to exit and its square-root cost change?")
        with self.voiceover(
            "Pause and predict. A book holds five days of a stock's volume. In a crisis, volume halves and volatility "
            "doubles. How do its days to exit and its square-root cost change?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
