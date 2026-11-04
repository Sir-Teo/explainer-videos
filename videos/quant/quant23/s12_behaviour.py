from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant23.common import BAD, CONS, GOOD, MKT, PART, SDF, TAN, ask, fit_right, illustration, load


class Behaviour(VoiceoverScene):
    def construct(self):
        lim = load("limits")
        self.card()
        self.two_pillars()
        self.palm()
        self.sv(lim)
        self.chart(lim)
        self.prospect()
        self.disposition()
        self.biases()

    def prospect(self):
        g1 = axes([-1, 1], [-2.4, 1.2], x_length=5.0, y_length=4.0, xlabel=r"gain or loss", ylabel=r"value",
                  xticks=[-1, 0, 1], yticks=[-2, -1, 0, 1], font_size=13).to_edge(LEFT, buff=0.5).shift(DOWN * 0.4)
        g2 = axes([0, 1], [0, 1], x_length=4.4, y_length=4.0, xlabel=r"probability", ylabel=r"decision weight",
                  xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], font_size=13).next_to(g1, RIGHT, buff=1.0)
        x = np.linspace(-1, 1, 201)
        v = np.where(x >= 0, np.abs(x) ** 0.88, -2.25 * np.abs(x) ** 0.88)
        pp = np.linspace(0.001, 0.999, 300)
        gm = 0.61
        wp = pp ** gm / (pp ** gm + (1 - pp) ** gm) ** (1 / gm)
        c1 = curve(g1.ax, x, v, BAD, stroke_width=3.5)
        c2 = curve(g2.ax, pp, wp, SDF, stroke_width=3.5)
        d2 = DashedLine(g2.ax.c2p(0, 0), g2.ax.c2p(1, 1), color=GREY_B, stroke_width=1.5)
        w01 = 0.01 ** gm / (0.01 ** gm + 0.99 ** gm) ** (1 / gm)
        cap = VGroup(
            MathTex(r"v(x) = x^{0.88},\ \ v(-x) = -2.25\,x^{0.88}", font_size=24),
            MathTex(rf"w(1\%) \approx {100 * w01:.1f}\%", font_size=26, color=SDF),
        ).arrange(RIGHT, buff=1.2).to_edge(UP, buff=0.5)
        foot = wrapped_label(r"Tversky and Kahneman's (1992) estimates. Losses weigh 2.25 times gains; a 1\% chance is "
                             r"felt as about 5\%. Barberis and Huang (2008): investors who weigh probabilities this way "
                             r"overpay for stocks with a small chance of a huge gain, which then earn less", 12.4, 16,
                             GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Prospect theory, in two curves. <bookmark mark='a'/> On the left, how a gain or loss feels. Amos Tversky "
            "and Daniel Kahneman estimated that losses weigh about two and a quarter times as much as equal gains, and "
            "that the curve flattens on both sides: the second thousand dollars lost hurts less than the first. "
            "<bookmark mark='b'/> On the right, how a probability is weighed. Small chances are overweighted: a one "
            "percent chance is felt as about five and a half; large ones are underweighted. <bookmark mark='c'/> Put "
            "those in a market and investors overpay for lottery tickets, stocks with a small chance of an enormous "
            "gain. Nicholas Barberis and Ming Huang showed that such stocks should then earn less, and the most "
            "skewed stocks, new issues and penny stocks among them, have."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(cap[0]))
            vo.wait_until("a")
            self.play(Create(c1), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(d2), Create(c2), FadeIn(cap[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def disposition(self):
        rows = [cmath(r"\text{PGR}", r"=", r"\frac{\text{gains realised}}{\text{gains realised} + \text{paper gains}} = 0.148",
                      font_size=36, colors={r"\text{PGR}": GOOD}),
                cmath(r"\text{PLR}", r"=", r"\frac{\text{losses realised}}{\text{losses realised} + \text{paper losses}} = "
                      r"0.098", font_size=36, colors={r"\text{PLR}": BAD})]
        whys = [why(r"Odean (1998), 10,000 accounts at a discount broker, 1987--93: on each day an investor sold "
                    r"anything, the share of the winners in the account that were sold"),
                why(r"and of the losers: winners were sold about one and a half times as readily. The stocks sold went on "
                    r"to beat the losers kept, by about 3.4 points over the next year. The disposition effect, predicted "
                    r"by prospect theory's kink at the purchase price")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Prospect theory leaves a fingerprint in trading records. Terrance Odean studied ten thousand accounts at "
            "a discount broker. On every day an investor sold something, Odean asked what fraction of the winners in the "
            "account were sold. <bookmark mark='a'/> And what fraction of the losers. Winners were sold about one and a "
            "half times as readily, even though the winners sold went on to beat the losers kept. Investors measure "
            "gains and losses from the price they paid, and hate to make a paper loss real: the disposition effect."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def card(self):
        c = chapter_card(11, r"Behaviour and the limits of arbitrage", r"Why don't smart investors correct every price?",
                         lit=(2000,), part=PART)
        with self.voiceover("Chapter eleven. Behavioural finance, and why arbitrage cannot always fix what behaviour "
                            "breaks."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def two_pillars(self):
        cards = VGroup(
            desk_question(r"limits to arbitrage", r"correcting a mispricing is risky and costly: the price can move further "
                          r"away before it comes back, short selling costs money, and capital is finite", width=12.0,
                          font_size=21),
            desk_question(r"psychology", r"investors overextrapolate recent returns, are overconfident, feel losses more "
                          r"than gains, and hold losers too long: the systematic errors that create the mispricing",
                          width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Nicholas Barberis and Richard Thaler described behavioural finance as resting on two pillars. "
            "<bookmark mark='a'/> The first is the limits of arbitrage: correcting a mispriced asset is itself risky "
            "and costly. The price can move further away before it comes back, borrowing a stock to short it costs "
            "money, and the arbitrageur's capital is finite. <bookmark mark='b'/> The second is psychology: systematic "
            "errors, such as extrapolating recent returns, overconfidence, and feeling losses more than gains, which "
            "create mispricing in the first place. Either alone is not enough. Errors that arbitrage could fix would be "
            "fixed; limits without errors would have nothing to limit."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def palm(self):
        cc = crisis_card(r"2 March 2000", r"3Com and Palm",
                         r"3Com sold 5\% of its Palm subsidiary to the public and announced it would distribute the rest "
                         r"to its own shareholders: 1.5 Palm shares for every 3Com share. On the first day of trading, Palm "
                         r"closed so high that 3Com, which still owned 95\% of it, was worth less than its Palm stake: the "
                         r"rest of 3Com was valued at about minus \$22 billion (Lamont and Thaler, 2003)",
                         stats=[(r"-\$22\,\text{bn}", r"the implied value of 3Com's other businesses"),
                                (r"\approx 1.5", r"Palm shares per 3Com share, to come")], width=8.8,
                         font_size=19).move_to(UP * 0.3)
        foot = wrapped_label(r"the arbitrage, short Palm and buy 3Com, was obvious and widely reported; it was limited by "
                             r"how few Palm shares could be borrowed, and the cost of borrowing them. Later work argues the "
                             r"lending fees explain much of the gap", 11.8, 17, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The cleanest example came at the peak of the dot-com bubble. In March 2000 3Com sold five percent of its "
            "Palm subsidiary to the public and promised to hand the rest to its shareholders, about one and a half Palm "
            "shares for each 3Com share. <bookmark mark='a'/> On Palm's first day, the market valued 3Com at less than "
            "the Palm shares it owned: the rest of the company, Owen Lamont and Richard Thaler calculated, at about "
            "minus twenty-two billion dollars. The arbitrage was obvious, and in the newspapers. It was limited by how "
            "few Palm shares could be borrowed to sell short, and what it cost to borrow them."
        ) as vo:
            self.play(FadeIn(cc))
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.add(illustration(r"Lamont and Thaler, Journal of Political Economy (2003)"))
        self.wait(0.4)
        self.clear_scene()

    def sv(self, lim):
        rows = [cmath(r"p_1", r"=", r"V - S_1 + F_1", font_size=40, colors={r"p_1": MKT}),
                cmath(r"F_2", r"=", r"F_1 + a\,F_1\Big(\frac{p_2}{p_1} - 1\Big),\quad a > 1", font_size=38,
                      colors={r"F_2": BAD}),
                cmath(r"p_2", r"=", r"\frac{V - S_2 + F_1(1 - a)}{1 - a F_1/p_1}", font_size=40, colors={r"p_2": BAD})]
        whys = [why(r"Shleifer and Vishny (1997): noise traders depress the price by $S$; arbitrageurs with funds $F$ buy, "
                    r"and the price is the fundamental $V$ less what they cannot absorb"),
                why(r"but they manage other people's money, and investors judge them on returns: after a loss, money is "
                    r"withdrawn. Performance-based arbitrage"),
                why(r"so when the mispricing deepens, arbitrageurs lose capital exactly when the opportunity is best, and "
                    r"the price falls further than the shock alone would push it")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "Andrei Shleifer and Robert Vishny made the limit precise. Noise traders push a price below its value; "
            "arbitrageurs buy with whatever funds they have, and the price is the value less what they cannot absorb. "
            "<bookmark mark='a'/> But arbitrageurs invest other people's money, and investors judge them by recent "
            "returns. After a loss, money is withdrawn. <bookmark mark='b'/> So if the mispricing deepens, the "
            "arbitrageurs lose capital exactly when the opportunity has improved, and the price falls further than the "
            "noise traders alone would push it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def chart(self, lim):
        a, p2 = np.asarray(lim["a"]), np.asarray(lim["p2"])
        g = axes([0, 3], [0.5, 0.9], x_length=7.2, y_length=4.2, xlabel=r"sensitivity of withdrawals to losses, $a$",
                 ylabel=r"price after the second shock", xticks=[0, 1, 2, 3], yticks=[0.6, 0.7, 0.8, 0.9], font_size=14
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, a, p2, BAD, stroke_width=3.5)
        nw = DashedLine(ax.c2p(0, lim["nw"]), ax.c2p(3, lim["nw"]), color=GREY_B, stroke_width=1.5)
        p1 = DashedLine(ax.c2p(0, lim["p1"]), ax.c2p(3, lim["p1"]), color=MKT, stroke_width=1.5)
        side = VGroup(
            legend([(MKT, rf"after the first shock: {lim['p1']:.2f}"), (GREY_B, rf"second shock, no withdrawals: "
                                                                               rf"{lim['nw']:.2f}"),
                    (BAD, r"with withdrawals")], font_size=16),
            wrapped_label(r"fundamental value 1, noise-trader pessimism 0.3 then 0.4, arbitrage funds 0.2; illustrative. "
                          r"At $a$ = 3 the price falls to 0.6: half again the shock's direct effect", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "In numbers: a stock worth one dollar, noise traders pessimistic by thirty cents and then by forty, "
            "arbitrage funds of twenty. <bookmark mark='a'/> After the first shock the price is ninety cents. Without "
            "withdrawals, the second shock would take it to eighty. <bookmark mark='b'/> The more investors pull money "
            "after losses, the lower it goes; at a withdrawal sensitivity of three, to sixty cents. Arbitrage is least "
            "effective exactly when it is most needed: this is how hedge funds failed in 1998 and how bases widened in "
            "2008 and March 2020."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(p1), Create(nw))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(side[1]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def biases(self):
        cards = VGroup(
            desk_question(r"noise-trader risk", r"De Long, Shleifer, Summers and Waldmann (1990): if pessimists can get "
                          r"more pessimistic before the price recovers, a short-horizon arbitrageur faces risk even with "
                          r"no fundamental risk at all", width=12.0, font_size=20),
            desk_question(r"extrapolation", r"investors' expected returns, measured in surveys, are high after high returns: "
                          r"the opposite of what Campbell--Shiller says rational expectations should be (Greenwood and "
                          r"Shleifer, 2014)", width=12.0, font_size=20),
            desk_question(r"prospect theory", r"Kahneman and Tversky: losses weigh about twice as much as gains, and small "
                          r"probabilities are overweighted, which can price lottery-like stocks too high", width=12.0,
                          font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Three ideas recur on the psychological side. <bookmark mark='a'/> Noise-trader risk: if pessimists can grow "
            "more pessimistic before the price recovers, an arbitrageur with a short horizon faces risk even when the "
            "asset itself has none. <bookmark mark='b'/> Extrapolation: surveys show investors expect high returns "
            "after high returns, the opposite of what chapter eight says rational expectations should be. "
            "<bookmark mark='c'/> And prospect theory, as the curves showed: losses weigh about twice as much as gains, and "
            "small chances are overweighted, which can make lottery-like stocks expensive. Each predicts patterns Part twenty-four will "
            "test as factors."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"you run an arbitrage fund and a position you are sure of loses 20\% in a month. Your investors can "
                r"withdraw monthly. What do you do, and what does everyone like you do to the price?")
        with self.voiceover("You run an arbitrage fund, and a position you are sure of loses twenty percent in a month. "
                            "Your investors can withdraw monthly. What do you do, and what does everyone like you do to "
                            "the price?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
