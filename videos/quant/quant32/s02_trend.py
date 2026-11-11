from __future__ import annotations

import math
import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import BAD, GOOD, PART, TREND_C, fit_right
from videos.quant.quant32.illustrations import trend_paths


class Trend(VoiceoverScene):
    def construct(self):
        self.card()
        self.universe()
        self.rule()
        self.paths(trend_paths())
        self.choices()
        self.breadth()
        self.evidence()
        self.firms()
        self.business()
        self.horizons()
        self.question()

    def card(self):
        c = chapter_card(1, r"Trend following", r"What does the rule know, and when does it trade?", part=PART)
        with self.voiceover(
            "Chapter one. A trend rule uses a market's own earlier returns to decide its exposure. A positive past "
            "return can lead to a long position, and a negative one to a short position. That specifies a decision "
            "rule. Whether it earns a premium after trading and financing is an empirical question, and the timing "
            "of its information is part of that question."
        ):
            self.play(FadeIn(c[0]), FadeIn(c[1]))
        self.play(FadeOut(c))

    def universe(self):
        cards = VGroup(
            desk_question(r"instruments", r"equity indices, bonds, credit, commodities and currencies; futures, "
                          r"funds and spot assets have different cash flows", width=12.2, font_size=20),
            desk_question(r"信息集" if zh() else r"information", r"signal and volatility observed by a specified close; the position "
                          r"earns the following period's return", width=12.2, font_size=20),
            desk_question(r"sample", r"membership, available history, dividends, missing observations and data "
                          r"revisions affect interpretation", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "Begin with the instruments. Futures and forwards express long and short views across asset classes, "
            "while a fund has its own collateral, expenses and mandate. Its return is not simply a spot price change. "
            "<bookmark mark='a'/> Next specify the information set. A close can enter a signal applied to the next "
            "period; it cannot support a claim of execution before that close. "
            "<bookmark mark='b'/> Finally specify the sample. Funds selected today and revised adjusted prices do "
            "not reconstruct the choices available to an earlier investor. Missing observations and changing "
            "membership also alter the markets sharing the risk budget."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def rule(self):
        rows = [
            cmath(r"s_{i,t}", r"=", r"\operatorname{sign}\!\left(\sum_{j=0}^{L-1}r_{i,t-j}\right)", font_size=36),
            cmath(r"x_{i,t}", r"=", r"s_{i,t}\frac{\sigma^*_{\rm asset}}{\hat\sigma_{i,t}}", font_size=36),
            cmath(r"p_{t+1}", r"=", r"\frac1{N_t}\sum_i x_{i,t}r_{i,t+1}", font_size=36),
        ]
        whys = [
            why(r"the House implementation sums daily excess returns; this differs from compounding a trailing total return"),
            why(r"chosen forecast budget 40\%, forecast SD 20\%: coefficient 2 before averaging across markets"),
            why(r"prior-close coefficients and a specified active count; separate lagged book-risk scaling"),
        ]
        step = ladder(self, rows, whys, keep=3, top=2.5, x=-0.25, buff=0.6, edge=6.8)
        with self.voiceover(
            "Time-series momentum compares each market with its own past, rather than ranking it against other "
            "markets. <bookmark mark='a'/> Here the stated signal is the sign of a sum of daily excess returns. "
            "A compounded trailing return is a different statistic. "
            "<bookmark mark='b'/> Divide a chosen risk budget by an available volatility forecast. Forty percent "
            "over twenty percent gives two before the coefficients are averaged across markets. These are forecast "
            "units, not a guarantee of realised risk. "
            "<bookmark mark='c'/> The prior close's coefficients multiply next-period returns. The original House "
            "design rebalances signals monthly and separately scales its preliminary book using lagged EWMA risk, "
            "with that multiplier capped at ten. Missing-return and active-count conventions, portfolio drift, "
            "financing and costs still matter for an executable account."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.clear_scene()

    def paths(self, data):
        g = axes([0, 4], [-0.5, 4.5], x_length=7.0, y_length=4.2,
                 xlabel=r"chosen period", ylabel=r"cumulative increment units",
                 xticks=[0, 1, 2, 3, 4], yticks=[0, 2, 4], font_size=16).move_to(LEFT * 2.1)
        names = list(data)
        colors = [TREND_C, BAD, QC.OPTION, QC.DELTA]
        lines = VGroup(*[curve(g.ax, np.arange(5), data[n]["path"], c, stroke_width=3)
                         for n, c in zip(names, colors)])
        leg = legend(list(zip(colors, names)), font_size=16).to_edge(RIGHT, buff=0.35).shift(UP * 1.4)
        fit_right(leg)
        stats = VGroup(*[label(rf"$S={data[n]['S']:.0f},\ Q={data[n]['Q']:.0f},\ P={data[n]['P']:.0f}$",
                              font_size=19, color=c) for n, c in zip(names, colors)])
        stats.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        fit_right(stats)
        foot = wrapped_label(r"four stipulated paths; linear within-block positions equal prior cumulative increments; "
                             r"PnL in squared increment units, without capital normalisation or costs",
                             12.2, 18, GREY_A).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(g), Create(lines[0]), FadeIn(leg), FadeIn(foot))
        with self.voiceover(
            "Compare the four chosen paths. The persistent rise builds position before later positive increments, "
            "giving profit six in squared increment units. "
            "<bookmark mark='a'/> Alternation and the rise followed by reversal finish at zero. Each has sum of "
            "squares four, and the linear rule loses two. Intermediate positions differ even though this block "
            "identity gives the same final profit. "
            "<bookmark mark='b'/> One final jump reaches the same total of four as the persistent rise, but profit "
            "is zero: earlier movement did not build a position. Its sum of squares is sixteen. A large terminal "
            "move alone therefore does not establish a trend gain. These paths isolate arithmetic. Converting "
            "their profits into portfolio returns would require a capital and risk normalisation, plus costs."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(lines[1]), Create(lines[2]))
            vo.wait_until("b")
            self.play(Create(lines[3]), FadeIn(stats))
        self.clear_scene()

    def choices(self):
        cards = VGroup(
            desk_question(r"lookback", r"21, 63 or 252 observations are design choices, with different response "
                          r"speeds and availability requirements", width=12.2, font_size=20),
            desk_question(r"signal shape", r"sign discards magnitude; a linear score retains it and needs a scaling "
                          r"and clipping convention", width=12.2, font_size=20),
            desk_question(r"accounting", r"three lookbacks times two shapes gives six specifications; dependence "
                          r"does not erase selection", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "A rule contains choices. Twenty-one, sixty-three and two hundred fifty-two observations are three "
            "lookbacks, not evidence that one horizon is universally best. "
            "<bookmark mark='a'/> A sign signal drops magnitude. A linear score keeps it and adds a scaling "
            "convention; the House's alternative clips its normalised signal at two in absolute value. "
            "<bookmark mark='b'/> Three lookbacks and two shapes give six specifications. Their overlap makes "
            "their outcomes dependent, but trying related choices still matters when reporting selection. "
            "Predefining the comparison and retaining unsuccessful choices makes a research history more "
            "interpretable. We have not selected a winning specification from these arithmetic examples."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def breadth(self):
        equation = MathTex(r"\sigma_p=\sigma\sqrt{\frac{1+(N-1)\rho}{N}}", font_size=40).shift(UP * 1.7)
        cases = [(0.0, 0.05), (0.5, 0.10 * math.sqrt(2.5 / 4)), (1.0, 0.10)]
        rows = VGroup(*[label(rf"$N=4,\ \sigma=10\%,\ \rho={rho:g}:\quad \sigma_p={100 * risk:.2f}\%$",
                              font_size=27, color=TREND_C) for rho, risk in cases])
        rows.arrange(DOWN, buff=0.4).move_to(DOWN * 0.15)
        foot = wrapped_label(r"chosen equal weights, equal SDs and feasible common correlations; "
                             r"covariance identities, not observed class returns",
                             12.2, 18, GREY_A).to_edge(DOWN, buff=0.4)
        self.play(Write(equation), FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Why trade several markets? In a fixed equal-weight, equal-volatility model, risk depends on common "
            "correlation. Four markets with ten percent standalone volatility give five percent portfolio "
            "volatility when their correlations are zero. "
            "<bookmark mark='a'/> Choose correlation one half instead: risk is about seven point nine one percent. "
            "Choose correlation one and it is ten percent. These are covariance assumptions, not historical books. "
            "<bookmark mark='b'/> Different labels do not ensure independent signals, positions or returns. "
            "Contracts can share currency, duration, inflation or financing exposures, and correlations can change "
            "during liquidation. Breadth must be defined for the exposures and horizon being diversified."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.wait(0.2)
        self.clear_scene()

    def evidence(self):
        cards = VGroup(
            desk_question(r"studies", r"Moskowitz, Ooi and Pedersen (2012): futures and forwards; Hurst, Ooi and "
                          r"Pedersen (2017) and Lemp\'eri\`ere et al. (2014): long historical reconstructions",
                          width=12.2, font_size=20),
            desk_question(r"comparison", r"markets, dates, signals, risk scaling, financing and costs differ "
                          r"between published indices and funds", width=12.2, font_size=20),
            desk_question(r"inference", r"conditional historical evidence motivates a mechanism and another test; "
                          r"it does not guarantee a future premium or every crisis hedge", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "Specified empirical studies motivate the mechanism. Moskowitz, Ooi and Pedersen examine time-series "
            "momentum on futures and forwards. Hurst, Ooi and Pedersen reconstruct a longer history, while "
            "Lemperiere and coauthors examine trend behaviour across horizons. "
            "<bookmark mark='a'/> A published index, a managed fund and an ETF implementation can have different "
            "markets, scaling and costs. Their Sharpe ratios alone do not identify a unique cause of a difference. "
            "<bookmark mark='b'/> Long histories expose more regimes but also require reconstruction assumptions "
            "about availability, contracts and execution. The appropriate conclusion is conditional evidence "
            "about a named design and sample, followed by a clearly specified independent test."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def firms(self):
        cards = VGroup(
            firm_card(r"AHL and Man", r"AHL was founded in 1987 by Michael Adam, David Harding and Martin Lueck "
                      r"and became part of Man Group.", source=r"Man Group company history and annual reports",
                      width=6.1, font_size=20),
            firm_card(r"Winton", r"David Harding founded Winton in 1997; published descriptions document a "
                      r"changing strategy mix.", source=r"Winton company history and published descriptions",
                      width=6.1, font_size=20),
        ).arrange(RIGHT, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "The firm files give an institutional setting. Michael Adam, David Harding and Martin Lueck founded "
            "AHL in 1987; it became part of Man Group. Harding founded Winton in 1997. "
            "<bookmark mark='a'/> Company histories describe businesses, not controlled comparisons of identical "
            "rules. Changes in markets, signals, execution technology or client terms can change a product. "
            "Explaining why a firm changed course needs evidence beyond the observation that a difficult "
            "performance period occurred nearby."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
        self.clear_scene()

    def business(self):
        equation = MathTex(r"g=5\%,\quad m=2\%,\quad p=20\%", font_size=38).shift(UP * 1.4)
        result = MathTex(r"(g-m)(1-p)=3\%\times0.8=2.4\%", font_size=40).shift(DOWN * 0.25)
        foot = wrapped_label(r"chosen one-year fee convention: performance fee on positive profit after the "
                             r"management fee; no hurdle, high-water mark, cash-flow timing or other expense",
                             12.2, 18, GREY_A).to_edge(DOWN, buff=0.45)
        self.play(Write(equation), FadeIn(foot))
        with self.voiceover(
            "Implementation is a business. Futures require margin and liquidity reserves; notional exposure "
            "differs from cash posted. Shorting and rolling can incur spreads, impact and funding constraints. "
            "<bookmark mark='a'/> Choose one year's gross excess profit at five percent, a management fee of two "
            "percent of starting capital, and a performance fee of twenty percent of the positive remainder. "
            "Three percent remains before that performance fee and two point four percent after it. "
            "<bookmark mark='b'/> Actual terms can include hurdles, high-water marks and cash-flow conventions. "
            "The example explains why terms matter without assuming every fund charges the same fees or "
            "promising a constant investor return."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(result))
            vo.wait_until("b")
            self.wait(0.2)
        self.clear_scene()

    def horizons(self):
        cards = VGroup(
            desk_question(r"faster", r"can adjust sooner, but can trade more in response to transient moves",
                          width=12.2, font_size=20),
            desk_question(r"slower", r"retains a longer history, and can remain exposed to the previous direction "
                          r"during a sharp reversal", width=12.2, font_size=20),
            desk_question(r"blended", r"another portfolio design: joint risk, offsetting orders and combined costs "
                          r"matter; improvement is not automatic", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "Horizon changes the response. A faster signal can turn sooner after new observations but also "
            "trade more in response to transient changes. "
            "<bookmark mark='a'/> A slower signal retains a longer history and can stay pointed in the old "
            "direction through a sharp reversal. Whether that tradeoff helps depends on the return process "
            "and execution. <bookmark mark='b'/> Combining speeds adds a portfolio design: correlated signals "
            "are not independent bets, and some orders can offset before trading. Evaluate the combined book's "
            "risk and costs, preserve the choices, and use appropriate independent evidence."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def question(self):
        panel = VGroup(
            MathTex('N=4,\\quad \\sigma=20\\%,\\quad \\sigma_p=10\\%', font_size=34),
            MathTex('\\sigma_p^2=\\sigma^2\\,\\frac{1+3\\rho}{4}', font_size=34),
            MathTex('\\rho=?', font_size=34),
        ).arrange(DOWN, buff=0.6).shift(UP * 0.3)
        self.play(FadeIn(panel))
        q = pause_card(r"Four equally weighted markets have 20\% SD and a common correlation. "
                       r"If the book has 10\% SD, what correlation is implied under those assumptions?")
        with self.voiceover(
            "Pause and predict. Four equally weighted markets each have twenty percent standard deviation, "
            "with the same correlation for every pair. The portfolio has ten percent standard deviation. "
            "What correlation is implied? State the equal-weight and equal-volatility assumptions before "
            "interpreting the result as a statement about breadth."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
