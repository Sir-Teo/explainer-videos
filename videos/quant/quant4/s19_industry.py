from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, LOSS, MART, P_C, PART, Q_C, load


class Industry(VoiceoverScene):
    def construct(self):
        ca = load("casino")
        b = load("beliefs")
        self.card()
        self.casino(ca)
        self.azuma(ca)
        self.players()
        self.books()
        self.markets(b)
        self.testing()

    def card(self):
        c = chapter_card(17, r"The house, the book and the market", r"Who lives on martingales with a drift?",
                         lit=(1962,), part=PART)
        disc = note(r"Public record only. Nothing in this chapter is gambling or investment advice.", font_size=18,
                    color=GREY_C).to_edge(DOWN, buff=0.3)
        with self.voiceover("Chapter seventeen. The house, the book, and the market."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]), FadeIn(disc))
        self.play(FadeOut(c), FadeOut(disc))

    def casino(self, ca):
        card = firm_card(r"The casino: a portfolio of martingales with a drift",
                         r"Every bet is a supermartingale for the player. Nevada's statewide roulette \textit{hold}, "
                         r"what the tables keep of the cash exchanged for chips, was 17.34\% in 2024, against an edge of "
                         r"5.26\% per spin on a double-zero wheel: chips are bet again and again. Table limits keep the "
                         r"bets bounded, which is when optional stopping holds.",
                         numbers=[(r"17.34\%", r"Nevada roulette hold, 2024"),
                                  (r"18.84\%", r"monthly average, 2004--Feb.\ 2026"),
                                  (r"3.15", r"its monthly s.d., points"),
                                  (r"14.30\%", r"blackjack hold, 2024")],
                         source=r"UNLV Center for Gaming Research, \textit{Nevada Table Games: Historical Hold "
                                r"Percentage Variations}, March 2026", width=11.4)
        card.to_edge(UP, buff=0.3)
        calc = VGroup(
            MathTex(r"\text{hold} \approx \text{edge} \times \frac{\text{amount wagered}}{\text{chips bought}}",
                    font_size=32),
            MathTex(rf"\frac{{17.34\%}}{{5.26\%}} \approx {ca['turnover']:.1f}\ \text{{bets per dollar of chips}}",
                    font_size=32, color=QC.IDEA),
        ).arrange(DOWN, buff=0.2).next_to(card, DOWN, buff=0.35)
        pred = desk_question(r"Roulette's edge is 5.26\%. Why do Nevada's tables report a hold near 17\%?",
                             rf"Chips are re-bet: about {ca['turnover']:.1f} times per dollar bought, at 5.26\% each.",
                             width=7.6, font_size=20).next_to(calc, DOWN, buff=0.3)
        with self.voiceover(
            "A casino is a portfolio of martingales with a drift in its favour. <bookmark mark='a'/> Nevada's "
            "roulette tables kept seventeen point three four percent of the cash exchanged for chips in 2024, by the "
            "University of Nevada's figures. <bookmark mark='b'/> Yet a double-zero wheel's edge is five point two "
            "six percent. The gap is chapter four's tax per unit staked: the edge times how often each dollar of "
            f"chips is bet, about {ca['turnover']:.1f} times. <bookmark mark='c'/> Table limits keep the bets bounded, "
            "so optional stopping holds."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(calc[0]))
            self.play(FadeIn(calc[1]))
            vo.wait_until("c")
            self.play(FadeIn(pred, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def azuma(self, ca):
        rows = ca["rows"]
        Ns = [r_["N"] for r_ in rows]
        g = axes([1.5, 5.5], [-18, 0], x_length=6.4, y_length=4.2, xlabel=r"even-money bets $N$ (log scale)",
                 ylabel=r"P(the house is behind after $N$ bets)", xticks=[2, 3, 4, 5], xfmt=lambda v: rf"10^{{{int(v)}}}",
                 yticks=[-15, -10, -5, 0], yfmt=lambda u: rf"10^{{{int(u)}}}" if u else "1", font_size=16)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        x = np.log10(Ns)

        def line(key, col):
            ys = np.log10([max(r_[key], 1e-18) for r_ in rows])
            return VGroup(curve(ax, x, ys, col, stroke_width=3),
                          *[Dot(ax.c2p(a, b_), radius=0.06, color=col) for a, b_ in zip(x, ys)])

        ex, nm, az = line("exact", MART), line("normal", P_C), line("azuma", LOSS)
        leg = legend([(MART, r"exact (binomial)"), (P_C, r"normal approximation"),
                      (LOSS, r"Azuma: $e^{-(N/37)^2/(2N)} = e^{-N/2738}$")], font_size=19)
        r4 = next(r_ for r_ in rows if r_["N"] == 10000)
        side = VGroup(
            leg,
            MathTex(r"P(\text{loss}) \le \exp\!\Big(-\frac{(\text{edge}\cdot N)^2}{2N}\Big)", font_size=30),
            MathTex(rf"N = 10^4:\ {r4['exact']:.4f}\ (\text{{simulated }} {ca['sims']['10000']:.4f})", font_size=26,
                    color=MART),
            wrapped_label(r"Azuma (1967): a martingale with bounded steps rarely strays far; the bound is loose, but it "
                          r"needs nothing beyond the bound on each bet", 4.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        spread = VGroup(
            label(rf"luck alone would give the observed 3.15-point monthly s.d.\ only if a month had about "
                  rf"{ca['need_even']:,.0f} equal even-money bets".replace(",", "{,}"), font_size=19, color=GREY_B),
        ).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "How sure is the house? Azuma's inequality of 1967 bounds how far a martingale with bounded steps strays. "
            "<bookmark mark='a'/> On even-money bets the house is behind after a hundred bets about "
            f"{100 * rows[0]['exact']:.0f} percent of the time, after ten thousand {100 * r4['exact']:.2f} percent, "
            "after a hundred thousand essentially never. <bookmark mark='b'/> Yet monthly hold swings by three "
            f"points; luck alone would need a month of only about {ca['need_even']:,.0f} equal bets, so unequal bets "
            "and high rollers drive it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(ex), FadeIn(leg[0]))
            self.play(Create(nm), FadeIn(leg[1]))
            self.play(Create(az), FadeIn(leg[2]), FadeIn(side[2:]))
            vo.wait_until("b")
            self.play(FadeIn(spread))
        self.wait(0.4)
        self.clear_scene()

    def players(self):
        cards = VGroup(
            history_card(1962, r"Edward Thorp, \textit{Beat the Dealer}",
                         r"blackjack is not i.i.d.: the deck remembers. Counting cards changes the filtration, and at "
                         r"times the player's drift turns positive", width=11.0),
            history_card(1982, r"\textit{Uston v.\ Resorts International}, 89 N.J.\ 163, 445 A.2d 370",
                         r"New Jersey's Supreme Court held that the Casino Control Act left rules on card counting to "
                         r"the Casino Control Commission, so the casino could not exclude Ken Uston for counting on its "
                         r"own", width=11.0),
            history_card(2017, r"\textit{Ivey v Genting Casinos}, [2017] UKSC 67",
                         r"edge sorting, chapter 11's change of filtration, was held to be cheating", width=11.0),
        ).arrange(DOWN, buff=0.35).move_to(ORIGIN)
        with self.voiceover(
            "The house's enemies change the filtration. Edward Thorp showed in 1962 that the blackjack deck remembers, "
            "and a counter sometimes faces a positive drift. <bookmark mark='a'/> In 1982 New Jersey's Supreme Court "
            "held in Ken Uston's case that card counting was for the Casino Control Commission to regulate, so a "
            "casino could not exclude a counter on its own. <bookmark mark='b'/> In Britain, edge sorting was held to "
            "be cheating."
        ) as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.wait(0.4)
        self.clear_scene()

    def books(self):
        k = firm_card(r"Beating the bookmakers, on the record",
                      r"Kaunitz, Zhong and Kreiner (2017) took the average of many bookmakers' odds as the probability "
                      r"(the market as the martingale) and bet where one bookmaker's odds were better. A ten-year "
                      r"backtest: 56{,}435 bets, a 3.5\% return. Five months with real money: 265 bets of \$50, "
                      r"\$957.50 profit. Then the bookmakers ``started to severely limit'' their accounts.",
                      numbers=[(r"3.5\%", r"backtest return, 2005--15"), (r"8.5\%", r"live return, 265 bets")],
                      source=r"arXiv:1710.02824", width=6.4, font_size=21)
        f = firm_card(r"The book's side: FanDuel",
                      r"A sportsbook sets odds with a margin and, like a casino, limits the customers whose drift "
                      r"points the other way. Flutter Entertainment's US segment reported its sportsbook net revenue "
                      r"margin, revenue as a share of amounts staked.",
                      numbers=[(r"7.9\%", r"US sportsbook margin, 2024 (7.5\% in 2023)"),
                               (r"\$50.9\text{bn}", r"US amounts staked, 2024")],
                      source=r"Flutter Entertainment plc, Form 10-K for fiscal 2024", width=6.0, font_size=21)
        VGroup(k, f).arrange(RIGHT, buff=0.4, aligned_edge=UP).to_edge(UP, buff=0.4)
        benter = wrapped_label(r"Bill Benter: a Hong Kong racing syndicate combining a fundamental model with the "
                               r"public's odds (Benter 1994, in Hausch, Lo and Ziemba, eds.); ``close to a billion "
                               r"dollars'', as reported by Bloomberg Businessweek (2018)", 12.4, 19, GREY_A)
        benter.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Bookmakers run the same business on sport. In 2017 Kaunitz, Zhong and Kreiner took the average of many "
            "bookmakers' odds as the probability and bet where one book offered better: a three and a half percent "
            "return over fifty-six thousand backtested bets, and a profit with real money, until the bookmakers "
            "began, in their words, to severely limit their accounts. <bookmark mark='a'/> Flutter reports that its "
            "American sportsbook kept seven point nine percent of fifty-one billion dollars staked in 2024. "
            "<bookmark mark='b'/> Bill Benter's racing syndicate blended a model with the public's odds and, as "
            "reported by Bloomberg Businessweek, made close to a billion dollars."
        ) as vo:
            self.play(FadeIn(k, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(f, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(benter))
        self.wait(0.4)
        self.clear_scene()

    def markets(self, b):
        cards = VGroup(
            history_card(2024, r"\textit{KalshiEX v.\ CFTC} (D.D.C., Judge Jia Cobb)",
                         r"the CFTC exceeded its authority in barring contracts on control of Congress; the appeals "
                         r"court declined to stay the ruling", width=6.6),
            history_card(2024, r"Polymarket, US presidential election",
                         r"nearly \$3.7bn traded, as reported by The Block; one trader's net profit about \$79m, as "
                         r"estimated by Chainalysis", width=6.6),
        ).arrange(DOWN, buff=0.25).to_corner(UL, buff=0.35)
        rows = [cmath(r"\mathbb{E}\sum_t (\pi_{t+1} - \pi_t)^2", r"=", r"\mathbb{E}\big[\pi_0(1 - \pi_0) - \pi_T(1 - \pi_T)\big]",
                      font_size=30)]
        eq = rows[0].next_to(cards, RIGHT, buff=0.4).align_to(cards, UP)
        if eq.get_right()[0] > 6.9:
            eq.scale_to_fit_width(6.9 - eq.get_left()[0])
        eqn = wrapped_label(r"a Bayesian's belief is a martingale, so its squared movement must equal the uncertainty it "
                            r"resolves (Augenblick and Rabin, \textit{QJE} 2021; chapter 11's $\langle M \rangle$)", 5.8,
                            19, GREY_A).next_to(eq, DOWN, buff=0.15).align_to(eq, LEFT)
        g = axes([0, 2], [0, 1.6], x_length=4.6, y_length=2.6, ylabel=r"movement $\div$ uncertainty resolved",
                 xticks=[], yticks=[0, 1.0, 1.5], font_size=15).next_to(eqn, DOWN, buff=0.45).align_to(eq, LEFT)
        ax = g.ax
        bw = ax.c2p(0.6, 0)[0] - ax.c2p(0, 0)[0]
        bars = VGroup()
        for i, (v, se, col, nm) in enumerate(((b["bayes"], b["bayes_se"], MART, r"Bayesian"),
                                              (b["over"], b["over_se"], LOSS, r"overreacts 30\%"))):
            top, bot = ax.c2p(i + 0.5, v), ax.c2p(i + 0.5, 0)
            bars.add(VGroup(Rectangle(width=bw, height=top[1] - bot[1], stroke_width=0, fill_color=col, fill_opacity=0.85)
                            .move_to((top + bot) / 2),
                            MathTex(rf"{v:.2f}", font_size=24, color=col).next_to(top, UP, buff=0.08),
                            label(nm, font_size=17, color=col).next_to(bot, DOWN, buff=0.1)))
        one = DashedLine(ax.c2p(0, 1), ax.c2p(2, 1), color=GREY_B, stroke_width=1.5)
        find = wrapped_label(r"on 11 million Betfair transactions, Augenblick and Rabin find consistent excess "
                             r"movement; Kalshi's prices sharpen near the close and show a favourite--longshot bias, "
                             r"stronger for takers (B\"urgi, Deng and Whelan, CESifo WP 12122)", 6.4, 18, GREY_B)
        find.next_to(cards, DOWN, buff=0.3).align_to(cards, LEFT)
        with self.voiceover(
            "Prediction markets sell the martingale directly: a contract paying one dollar if an event happens, its "
            "price read as a probability. In 2024 Judge Jia Cobb held that the CFTC had exceeded its authority in "
            "barring Kalshi's contracts on control of Congress, and the appeals court declined to stay her ruling. "
            "Polymarket's presidential market traded nearly three point seven billion dollars, as reported by The "
            "Block. <bookmark mark='a'/> Is such a price a martingale? Ned Augenblick and Matthew Rabin turned "
            "chapter eleven into a test: for a Bayesian, expected squared movement equals the uncertainty resolved. "
            f"<bookmark mark='b'/> On chapter three's forecasts the ratio is {b['bayes']:.2f}, as it must be; a "
            f"forecaster who overreacts by thirty percent scores {b['over']:.2f}. <bookmark mark='c'/> On eleven "
            "million Betfair trades they found consistent excess movement. On Kalshi, Bürgi, Deng and Whelan find "
            "prices that sharpen near the close, and a favourite-longshot bias, stronger for those who take "
            "liquidity."
        ) as vo:
            self.play(FadeIn(cards[0]))
            self.play(FadeIn(cards[1]))
            vo.wait_until("a")
            self.play(FadeIn(eq), FadeIn(eqn))
            vo.wait_until("b")
            self.play(FadeIn(g), Create(one), LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.5))
            vo.wait_until("c")
            self.play(FadeIn(find))
        self.wait(0.4)
        self.clear_scene()

    def testing(self):
        cards = VGroup(
            history_card(1945, r"Abraham Wald, sequential probability ratio test",
                         r"test while the data arrive, stop as soon as the evidence suffices: the likelihood ratio of "
                         r"chapter 12, watched", width=11.0),
            history_card(2022, r"Johari, Koomen, Pekelis and Walsh, \textit{Operations Research}",
                         r"always-valid p-values for A/B tests that are watched continuously (Optimizely)", width=11.0),
            history_card(2022, r"Lindon, Sanden and Shirikian, KDD 2022",
                         r"anytime-valid tests for canary releases at Netflix", width=11.0),
        ).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.4)
        desk = wrapped_label(r"on trading desks, watching a strategy's decay with sequential tests (CUSUM, e-processes) "
                             r"is standard practice; no firm-specific method is on the public record", 11.0, 21, GREY_A)
        desk.to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Testing while you watch is old, and now industrial. Abraham Wald's sequential probability ratio test, "
            "from the war years, watched chapter twelve's likelihood ratio and stopped as soon as the evidence "
            "sufficed. <bookmark mark='a'/> Optimizely's always-valid p-values serve website experiments that people "
            "check every hour, and Netflix uses anytime-valid tests to decide, while a new version rolls out, whether "
            "it is safe. <bookmark mark='b'/> On trading desks, watching a strategy for decay with sequential tests is "
            "standard practice, though no firm has published its own method."
        ) as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]), FadeIn(cards[2]))
            vo.wait_until("b")
            self.play(FadeIn(desk))
        self.wait(0.4)
        self.clear_scene()
