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
        self.fermi()
        self.code()
        self.prepare()
        self.question()

    def card(self):
        c = chapter_card(8, r"The interview", r"What do quant firms test, and why those things?", part=PART)
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
                cmath(r"\text{check}", r":", r"\text{between } 3.5 \text{ and } 6,\ \text{nearer } 6", font_size=32)]
        whys = [why(r"the maximum is at most $k$ when both dice are: $(k/6)^2$; difference the cumulative probabilities"),
                why(r"the expectation, as an exact fraction"),
                why(r"a sanity check an interviewer wants to hear: the answer must exceed one die's 3.5")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        fe = float(e)
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
        with self.voiceover(
            "Question two, the market-making game. Make a market on the sum of three dice about to be rolled. "
            "<bookmark mark='a'/> The fair value is ten and a half. <bookmark mark='b'/> The standard deviation is about "
            f"{sd:.1f}, which sets how much you can afford to hold. <bookmark mark='c'/> Quote ten bid, eleven offered: "
            "you earn half a point from anyone who trades without knowing more than you."
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
                cmath(r"\text{after a buy}", r":", r"\text{raise both quotes; widen if you suspect information}",
                      font_size=30, colors={r"\text{after a buy}": GOOD})]
        whys = [why(r"the interviewer reveals that the counterparty has seen one of the dice"),
                why(r"adverse selection: the informed trade only when your quote is wrong"),
                why(r"the trade itself is information: Glosten and Milgrom's model, in Part 38")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Then the twist. <bookmark mark='a'/> The interviewer says the other side has seen one die, and it was a "
            "six: their fair value is thirteen. <bookmark mark='b'/> If they buy at your eleven, you lose two in "
            "expectation. Informed traders trade only when your quote is wrong. <bookmark mark='c'/> So after a buy, "
            "raise both quotes, and widen them if you suspect information. The trade itself is information, which is "
            "the whole theory of Part thirty-eight in one exchange."
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
                cmath(r"\text{capped at } 2^{30} \approx \$1\text{bn}", r"\Rightarrow", rf"\mathbb E \approx {float(ev):.0f}",
                      font_size=32, colors={r"\mathbb E \approx": GOOD})]
        whys = [why(r"the St. Petersburg game: how much would you pay to play?"),
                why(r"each toss adds one to the expectation, forever"),
                why(r"no counterparty can pay more than it has: with a billion-dollar cap the fair price is about \$31, "
                    r"which is why the answer an interviewer wants is about counterparties, not infinity")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        evf = float(ev)
        with self.voiceover(
            "Question three, a classic. <bookmark mark='a'/> A coin is tossed until the first head; you are paid two to "
            "the power of the toss it came on. What would you pay to play? <bookmark mark='b'/> Each toss adds one "
            "dollar to the expectation, forever: infinite. <bookmark mark='c'/> But no one can pay more than they have. "
            f"Cap the payout at a billion dollars and the expectation is about {evf:.0f} dollars. The answer the "
            "interviewer wants is about the counterparty, not about infinity."
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
                why(r"bet twice Kelly and the growth rate is negative: you go broke with a winning coin")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Question four, sizing. A coin wins sixty percent of even-money bets. How much do you bet? "
            f"<bookmark mark='a'/> Kelly, from Part eight: twice the probability minus one, {f:.1f} of your wealth. "
            f"<bookmark mark='b'/> The growth rate is {g:.3f} per bet. <bookmark mark='c'/> Bet twice that and the "
            f"growth rate is {g2:.3f}: negative. With a winning coin, over-betting goes broke. Interviewers ask this "
            "because traders who over-size are the most common way a firm loses money."
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
        rows = [cmath(r"\text{US equity volume}", r"\approx", r"10^{10}\ \text{shares a day}", font_size=34),
                cmath(r"\text{one firm's share}", r"\approx", r"20\%,\quad \text{about 100 shares a trade}", font_size=32),
                cmath(r"\text{trades a day}", r"\approx", rf"{trades / 1e6:.0f}\ \text{{million}}", font_size=36,
                      colors={r"\text{trades a day}": GOOD})]
        whys = [why(r"an order of magnitude is enough: US exchanges and off-exchange venues trade around ten billion shares "
                    r"on a typical day"),
                why(r"a large wholesaler or market maker in a fifth of it, at the small average trade size of electronic "
                    r"markets"),
                why(r"millions of trades a day: Chapter 2's law of large numbers needs about $10^5$ independent ones, so "
                    r"the disclosed statistic is plausible")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Question six, an estimate. How many trades a day does a large American equity market maker do? "
            "<bookmark mark='a'/> Start from the market: around ten billion shares a day, order of magnitude. "
            "<bookmark mark='b'/> A large market maker in a fifth of it, at about a hundred shares a trade. "
            f"<bookmark mark='c'/> About {trades / 1e6:.0f} million trades a day. Chapter two's law of large numbers "
            "needed around a hundred thousand independent ones, so the disclosed statistic is plausible. Estimation "
            "questions test exactly this: a chain of rough numbers, each defended."
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
        with self.voiceover(
            "Question five, code. Compute a strategy's maximum drawdown. The quadratic answer compares every pair of "
            "days; the answer an interviewer wants keeps the running peak and the worst fall from it, in one pass. Here "
            "is the House's own version, the function behind every drawdown in this series."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def prepare(self):
        cards = VGroup(
            desk_question(r"the classics", r"Mosteller's \textit{Fifty Challenging Problems in Probability} (1965); "
                          r"Crack's \textit{Heard on the Street}; Zhou's \textit{A Practical Guide to Quantitative Finance "
                          r"Interviews} (2008)", width=12.4, font_size=19),
            desk_question(r"how to answer", r"say the approach, compute, then check the answer against a bound or a "
                          r"special case; in a market game, say what each trade tells you", width=12.4, font_size=19),
            desk_question(r"what is really tested", r"calm reasoning under uncertainty with a clock running, which is "
                          r"also the job", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
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
        q = pause_card(r"you roll a die and may re-roll once, keeping the second roll. With the best strategy, what is "
                       r"the expected value?")
        with self.voiceover(
            "Pause and predict. You roll a die and may re-roll once, keeping the second roll. With the best strategy, "
            "what is the expected value?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
