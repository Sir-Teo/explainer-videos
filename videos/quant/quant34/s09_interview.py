from __future__ import annotations

import math
from fractions import Fraction

from explainer.quant import *  # noqa: F403
from explainer.quant.house import systematic as SY
from videos.quant.quant34.common import BAD, FIRM_C, GOOD, HURDLE, PART, PM_C, house_lab


class Interview(VoiceoverScene):
    def construct(self):
        self.card()
        self.what()
        self.dice()
        self.market()
        self.informed()
        self.petersburg()
        self.kelly()
        self.code()
        self.fermi()
        self.prepare()
        self.question()

    def card(self):
        c = chapter_card(8, r"The interview", r"What do quant firms test, and why those things?", part=PART)
        self.add(c)
        with self.voiceover("Chapter eight. Quant firms hire by testing, and the tests are public knowledge: probability, "
                            "expected value, estimation under pressure, making markets, and code. Each tests a skill the "
                            "job uses every day. Here is a mock interview, with the answers computed."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def what(self):
        rows = [cmath(r"\text{probability}", r":", r"\text{exact answers, quickly, by symmetry}", font_size=32,
                      colors={r"\text{probability}": PM_C}),
                cmath(r"\text{expected value}", r":", r"\text{prices are expectations; bets are sized}", font_size=32,
                      colors={r"\text{expected value}": PM_C}),
                cmath(r"\text{markets}", r":", r"\text{quote, update on the trade, manage the position}", font_size=32,
                      colors={r"\text{markets}": PM_C}),
                cmath(r"\text{code}", r":", r"\text{correct, then fast}", font_size=32, colors={r"\text{code}": PM_C})]
        whys = [why(r"the language of every model in this series"),
                why(r"a trader prices in expectations and sizes by Kelly (Part 8)"),
                why(r"the market-making game: the interview's version of Part 38"),
                why(r"the research platform of Chapter 6 is code; so is every limit")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "What is tested. <bookmark mark='a'/> Probability, answered exactly and quickly, usually by symmetry. "
            "<bookmark mark='b'/> Expected value and sizing, because prices are expectations and bets are sized. "
            "<bookmark mark='c'/> Making markets: quoting, updating on the trade, managing what you end up holding. "
            "<bookmark mark='d'/> And code, correct first and then fast."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def dice(self):
        e = sum(Fraction(k * (2 * k - 1), 36) for k in range(1, 7))
        rows = [cmath(r"\Pr(\max = k)", r"=", r"\frac{k^2 - (k-1)^2}{36} = \frac{2k - 1}{36}", font_size=36),
                cmath(r"\mathbb E[\max]", r"=", rf"\sum_k k\,\frac{{2k-1}}{{36}} = \frac{{{e.numerator}}}{{{e.denominator}}} "
                      rf"\approx {float(e):.2f}", font_size=36, colors={r"\mathbb E[\max]": GOOD}),
                cmath(r"\text{check}", r":", '\\text{between } 3.5 \\text{ and } 6,\\ \\text{nearer } 3.5', font_size=32)]
        whys = [why(r"the maximum is at most $k$ when both dice are: $(k/6)^2$; difference the cumulative probabilities"),
                why(r"the expectation, as an exact fraction"),
                why(r"a sanity check an interviewer wants to hear: the answer must exceed one die's 3.5")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        fe = float(e)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Question one. Roll two dice; what is the expected value of the larger? <bookmark mark='a'/> The maximum is "
            "at most k when both dice are, so its distribution is a difference of squares. <bookmark mark='b'/> The "
            f"expectation is one hundred and sixty-one over thirty-six, about {fe:.2f}. <bookmark mark='c'/> And the "
            "check: more than one die's three and a half, less than six. The interviewer is listening for the method and "
            "the check, not the arithmetic."
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

    def market(self):
        sd = math.sqrt(3 * 35 / 12)
        rows = [cmath(r"\mathbb E[\text{sum of 3 dice}]", r"=", r"3 \times 3.5 = 10.5", font_size=36),
                cmath(r"\sigma", r"=", rf"\sqrt{{3 \times 35/12}} = {sd:.2f}", font_size=36),
                cmath(r"\text{quote}", r":", r"10 \text{ bid},\ 11 \text{ offer}", font_size=36, colors={r"\text{quote}": PM_C})]
        whys = [why(r"make a market on the sum of three dice about to be rolled: start from the fair value"),
                why(r"the uncertainty, which sets how much size you can bear"),
                why(r"a spread around fair value: you earn half the spread from anyone who trades without information")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            f"""Question two uses independent fair dice, a risk-neutral payoff and one unit without fees or inventory costs. <bookmark mark='a'/> The sum of three dice has expectation ten and a half. <bookmark mark='b'/> Its standard deviation is {sd:.2f}; risk tolerance and wealth would determine size. <bookmark mark='c'/> At ten bid and eleven offered, either side has expected half-point revenue only if trade direction conveys no information about the dice. Information changes the conditional fair value."""
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

    def informed(self):
        rows = [cmath(r"\text{they saw one die: } 6", r"\Rightarrow", r"\mathbb E[\text{sum}] = 6 + 7 = 13", font_size=34,
                      colors={r"\text{they saw one die: } 6": BAD}),
                cmath(r"\text{they lift your 11 offer}", r"\Rightarrow", r"\text{you lose } 2 \text{ in expectation}",
                      font_size=32),
                cmath(r"\text{after a buy}", r":", '\\text{update using a specified information model}',
                      font_size=30, colors={r"\text{after a buy}": GOOD})]
        whys = [why(r"the interviewer reveals that the counterparty has seen one of the dice"),
                why(r"adverse selection: the informed trade only when your quote is wrong"),
                why(r"the trade itself is information: Glosten and Milgrom's model, in Part 38")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Now suppose it is revealed that one specified die is six and the other two remain independent and fair. <bookmark mark='a'/> Conditional expected payoff is thirteen. <bookmark mark='b'/> Selling at eleven then loses two in conditional expectation. This illustrates adverse selection. <bookmark mark='c'/> A buy without that revelation requires a model of informed and uninformed order flow before it determines a posterior price or spread. Raising quotes after every buy is not a model-free theorem."
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

    def petersburg(self):
        cap = 2 ** 30
        ev = sum(Fraction(1, 2 ** n) * min(2 ** n, cap) for n in range(1, 61)) + Fraction(1, 2 ** 60) * cap
        rows = [cmath(r"\text{pay } 2^n", r":", r"n = \text{the toss of the first head}", font_size=34),
                cmath(r"\mathbb E", r"=", r"\textstyle\sum_n 2^{-n}\, 2^n = 1 + 1 + \dots = \infty", font_size=34,
                      colors={r"\infty": BAD}),
                cmath(r"\text{capped at } 2^{30} \approx \$1\text{bn}", r"\Rightarrow", rf"\mathbb E = {float(ev):.0f}",
                      font_size=32, colors={r"\mathbb E \approx": GOOD})]
        whys = [why(r"the St. Petersburg game: how much would you pay to play?"),
                why(r"each toss adds one to the expectation, forever"),
                why(r"no counterparty can pay more than it has: with a billion-dollar cap the fair price is about \$31, "
                    r"which is why the answer an interviewer wants is about counterparties, not infinity")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        evf = float(ev)
        self.add(rows[0], whys[0])
        with self.voiceover(
            f"""Question three uses a fair independent coin. <bookmark mark='a'/> First head on toss n pays two to the n. <bookmark mark='b'/> Each possible n contributes one dollar, so the uncapped expectation diverges. <bookmark mark='c'/> Cap the payoff at exactly two to the thirty, about one point zero seven four billion dollars. The first thirty terms contribute thirty dollars and the remaining tail one, giving exactly {evf:.0f} dollars. That is a risk-neutral expectation for an enforceable specified payoff, not a utility-based ticket price or a guarantee that a counterparty can pay."""
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

    def kelly(self):
        p = 0.6
        f = 2 * p - 1
        g = p * math.log(1 + f) + (1 - p) * math.log(1 - f)
        g2 = p * math.log(1 + 2 * f) + (1 - p) * math.log(1 - 2 * f)
        rows = [cmath(r"f^*", r"=", rf"2p - 1 = {f:.1f}", font_size=36, colors={r"f^*": GOOD}),
                cmath(r"g(f^*)", r"=", rf"p\ln(1+f) + (1-p)\ln(1-f) = {g:.4f}", font_size=32),
                cmath(r"g(2f^*)", r"=", rf"{g2:.4f}", font_size=36, colors={r"g(2f^*)": BAD})]
        whys = [why(r"a coin that wins 60\% of even-money bets: bet the Kelly fraction of your wealth (Part 8)"),
                why(r"the growth rate per bet, about two percent"),
                why('at twice Kelly the known-iid model has negative log growth; wealth tends to zero asymptotically, not finite-time exact ruin')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            f"""Question four assumes a known iid win probability point six, even-money payoffs and a fixed fraction of current positive wealth. <bookmark mark='a'/> Maximizing expected log growth gives Kelly fraction {f:.1f}. <bookmark mark='b'/> Its log growth is {g:.5f} per bet. <bookmark mark='c'/> At twice Kelly, the fraction is point four and log growth is {g2:.5f}. By the law of large numbers, wealth tends to zero asymptotically in this model. Each finite-time multiplier remains positive, so this is not exact finite-time ruin. Uncertain odds, constraints and other risks require separate sizing judgments."""
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

    def fermi(self):
        shares = 12e9
        share_mm = 0.2
        avg_trade = 100
        trades = shares * share_mm / avg_trade
        trades_m = trades / 1e6
        rows = [cmath(r"\text{US equity volume}", r"\approx", '12\\times10^9\\ \\text{shares a day, stipulated}', font_size=34),
                cmath(r"\text{one firm's share}", r"\approx", r"20\%,\quad \text{about 100 shares a trade}", font_size=32),
                cmath(r"\text{trades a day}", r"\approx", rf"{trades / 1e6:.0f}\ \text{{million}}", font_size=36,
                      colors={r"\text{trades a day}": GOOD})]
        whys = [why(r"an order of magnitude is enough: US exchanges and off-exchange venues trade around ten billion shares "
                    r"on a typical day"),
                why(r"a large wholesaler or market maker in a fifth of it, at the small average trade size of electronic "
                    r"markets"),
                why("trade count does not identify independence, effective breadth, profit magnitudes or the actual firm's Sharpe ratio")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            f"""Question six is an explicit order-of-magnitude illustration. <bookmark mark='a'/> Choose twelve billion shares per day; this is an input assumption, not a measured current volume. <bookmark mark='b'/> Choose one firm's share as one fifth and one hundred shares per trade. <bookmark mark='c'/> Division gives {trades_m:.0f} million trades per day. Changing those inputs changes the answer. A count says nothing by itself about independence or effective breadth, so this estimate cannot verify a disclosed Sharpe ratio."""
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

    def code(self):
        card = house_lab(r"Question five: the maximum drawdown in one pass", SY.max_drawdown, "def max_drawdown", 8,
                         width=10.6)
        card.move_to(ORIGIN)
        self.add(card)
        with self.voiceover(
            'Question five, code. Compute maximum drawdown from cumulative simple-return wealth in one pass. The displayed unchanged function compounds returns, keeps the running wealth peak, and finds the worst proportional fall. It requires a meaningful positive wealth path for this interpretation. This differs from the arithmetic cumulative-return drawdown used by the research stop in Chapter ten; the two conventions must not be interchanged.'
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def prepare(self):
        cards = VGroup(
            desk_question(r"the classics", r"Mosteller's \textit{Fifty Challenging Problems in Probability} (1965); "
                          r"Crack's \textit{Heard on the Street}; Zhou's \textit{A Practical Guide to Quantitative Finance "
                          r"Interviews} (2008)", width=12.4, font_size=26),
            desk_question(r"how to answer", r"say the approach, compute, then check the answer against a bound or a "
                          r"special case; in a market game, say what each trade tells you", width=12.4, font_size=26),
            desk_question(r"what is really tested", r"calm reasoning under uncertainty with a clock running, which is "
                          r"also the job", width=12.4, font_size=26),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "How to prepare. <bookmark mark='a'/> The classic books: Mosteller's fifty challenging problems, Crack's "
            "Heard on the Street, and Zhou's practical guide. <bookmark mark='b'/> Say the approach, compute, then check "
            "against a bound or a special case; in a market game, say what each trade tells you. "
            "<bookmark mark='c'/> What is really tested is calm reasoning under uncertainty with a clock running, which "
            "is also the job."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card('Use the stated assumptions; derive the result and check its units and denominator.')
        working = MathTex('V_2=\\mathbb E[D]=3.5,\\quad V_1=\\mathbb E[\\max(D,V_2)],\\quad D\\sim\\mathrm{Unif}\\{1,\\ldots,6\\}', font_size=32).move_to(UP*0.9)
        if working.width > 12.1:
            working.scale_to_fit_width(12.1)
        setup_note = wrapped_label('A fair independent reroll, no fee, risk-neutral payoff; the second result must be kept. Decide after observing the first roll.', 11.7, 23).move_to(DOWN*0.8)
        self.add(working, setup_note, q)
        with self.voiceover('Pause and predict. Roll a fair die and optionally reroll once, keeping the independent second result. With no fee and a risk-neutral payoff, derive the optimal threshold and expected payoff.'):
            self.wait(0.5)
        self.wait(0.5)
        self.clear_scene()
