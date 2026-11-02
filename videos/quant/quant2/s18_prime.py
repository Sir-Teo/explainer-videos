from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import CASH, GAIN, LOSS, PART, TRADE, load, node

C_ = {r"\lambda": LOSS, r"q": TRADE, r"L_j": LOSS}


def row(*parts, fs=36):
    return cmath(*parts, colors=C_, font_size=fs)


class Prime(VoiceoverScene):
    def construct(self):
        fs = load("fire_sale")
        self.card()
        self.trs()
        self.race(fs)
        self.game(fs)
        self.archegos()

    def card(self):
        c = chapter_card(13, r"Prime brokers and the race to sell", r"Why does a client's default become a race?",
                         lit=(2021,), part=PART)
        with self.voiceover("Chapter thirteen. Prime brokers, and the race to sell."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def trs(self):
        fund, bank, mkt = node(r"hedge fund", TRADE, width=2.4), node(r"prime broker", CASH, width=2.6), \
            node(r"the stock", GREY_B, width=2.2)
        VGroup(fund, bank, mkt).arrange(RIGHT, buff=2.4).shift(UP * 1.6)
        a1 = Arrow(bank.get_left() + UP * 0.2, fund.get_right() + UP * 0.2, buff=0.1, color=GAIN, stroke_width=3)
        a2 = Arrow(fund.get_right() + DOWN * 0.2, bank.get_left() + DOWN * 0.2, buff=0.1, color=LOSS, stroke_width=3)
        a3 = Arrow(bank.get_right(), mkt.get_left(), buff=0.1, color=GREY_B, stroke_width=3)
        l1 = label(r"$\Delta S$ + dividends", font_size=20, color=GAIN).next_to(a1, UP, buff=0.06)
        l2 = label(r"$(r + s_f)\,S\,\Delta t$ + losses", font_size=20, color=LOSS).next_to(a2, DOWN, buff=0.06)
        l3 = label(r"the bank owns the hedge", font_size=20, color=GREY_B).next_to(a3, UP, buff=0.06)
        svc = VGroup(
            label(r"A prime broker lends the fund cash and securities, holds its assets, clears its trades,", font_size=21),
            label(r"and nets its margin across everything held there (cross-margining).", font_size=21),
            label(r"A total return swap is a synthetic long with financing: the fund gets the stock's return", font_size=21),
            label(r"and pays a funding rate; the bank holds the shares as its hedge. Swaps are not reported", font_size=21),
            label(r"as ownership in 13F filings: no lender saw how big the client was everywhere else.", font_size=21,
                  color=QC.IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.5)
        if svc.width > 13.0:
            svc.scale_to_fit_width(13.0)
        with self.voiceover(
            "Hedge funds borrow through prime brokers: divisions of large banks that lend them cash and securities, hold their "
            "assets, clear their trades, and net margin across everything they hold there. <bookmark mark='a'/> Much of the "
            "exposure is synthetic. In a total return swap the fund receives the stock's price change and dividends and pays "
            "a financing rate, and the bank buys the stock to hedge itself. <bookmark mark='b'/> The fund owns nothing, so it "
            "doesn't appear in the quarterly filings that report large shareholders. It can run the same trade with five banks "
            "at once, and none of them sees the whole."
        ) as vo:
            self.play(FadeIn(fund), FadeIn(bank), FadeIn(mkt), FadeIn(svc[:2]))
            vo.wait_until("a")
            self.play(GrowArrow(a1), FadeIn(l1), GrowArrow(a2), FadeIn(l2), GrowArrow(a3), FadeIn(l3), FadeIn(svc[2:4]))
            vo.wait_until("b")
            self.play(FadeIn(svc[4]))
        self.wait(0.4)
        self.clear_scene()

    def race(self, fs):
        K, q, lam = 4, 1.0, 1.0
        losses = np.asarray(fs["linear4"], float)
        g = axes([0, 4.2], [-4.6, 0.2], x_length=4.2, y_length=4.6, ylabel=r"price, in units of $\lambda q$",
                 yticks=[-4, -2, 0], font_size=16).to_edge(LEFT, buff=0.9).shift(DOWN * 0.2)
        ax = g.ax
        cols = [QC.IDEA, TRADE, CASH, QC.GAMMA]
        banks = VGroup()
        for j in range(K):
            b = VGroup(*[Square(0.3, stroke_width=0, fill_color=cols[j], fill_opacity=0.85) for _ in range(4)])
            b.arrange(UP, buff=0.04).move_to([1.2 + 1.0 * j, -1.6, 0])
            banks.add(VGroup(b, label(rf"bank {j + 1}", font_size=18, color=cols[j]).next_to(b, DOWN, buff=0.1)))
        price = ValueTracker(0.0)
        tick = always_redraw(lambda: VGroup(
            Line(ax.c2p(0, price.get_value()), ax.c2p(4.2, price.get_value()), color=LOSS, stroke_width=3),
            MathTex(r"P", font_size=26, color=LOSS).next_to(ax.c2p(4.2, price.get_value()), RIGHT, buff=0.08)))
        lbars = VGroup()
        for j in range(K):
            lbars.add(Rectangle(width=0.5, height=0.35 * losses[j], stroke_width=0, fill_color=cols[j], fill_opacity=0.8)
                      .move_to([1.2 + 1.0 * j, 1.0 + 0.35 * losses[j] / 2, 0]))
        lt = label(r"loss per bank", font_size=20, color=GREY_A).next_to(lbars, UP, buff=0.2)
        rows = [
            row(r"P_j", r"=", r"P_0 - \lambda\big((j-1)q + \tfrac q2\big)"),
            row(r"L_j", r"=", r"\lambda q^2\,(j - \tfrac12)"),
            row(r"\frac{L_K}{L_1}", r"=", r"2K - 1"),
        ]
        whys = [why(r"the $j$-th seller's average price: the earlier sales already moved it", font_size=19),
                why(r"its loss against the starting price", font_size=19),
                why(r"with four banks the last loses seven times the first", font_size=19)]
        for r_ in rows:
            r_.scale(0.85)
        step = ladder(self, rows, whys, keep=3, top=2.9, x=3.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "When such a client defaults, every bank holds the same shares as its hedge, and every bank must sell. Here are "
            "four banks, each with a block of q shares, and a price that falls by lambda for every share sold. "
            "<bookmark mark='a'/> The first bank sells into an untouched market. The second sells after the first has pushed "
            "the price down; the third, lower still. <bookmark mark='b'/> The j-th seller's average price is the start less "
            "everything sold before it, plus half its own block. Its loss is lambda q squared times j minus a half: it grows in "
            "a straight line with its place in the queue, and the last of K sellers loses two K minus one times what the first "
            "does. With four banks, seven times."
        ) as vo:
            self.play(FadeIn(g), FadeIn(banks))
            self.add(tick)
            vo.wait_until("a")
            for j in range(K):
                self.play(banks[j][0].animate.shift(LEFT * (1.2 + 1.0 * j)).set_opacity(0.15),
                          price.animate.set_value(-(j + 1) * lam * q), GrowFromEdge(lbars[j], DOWN), run_time=1.0)
            self.play(FadeIn(lt))
            vo.wait_until("b")
            step(0)
            step(1)
            step(2)
        tick.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def game(self, fs):
        br = fs["by_rank"]
        Ks = fs["K"]
        g = axes([0.5, 8.5], [0, 3.0], x_length=5.4, y_length=3.4, xlabel=r"place in the selling queue",
                 ylabel=r"loss per share, $\sqrt{\ }$ impact", xticks=[1, 4, 8], yticks=[0, 1, 2, 3], font_size=16)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        ax = g.ax
        lines = VGroup()
        for K in Ks:
            arr = np.asarray(br[str(K)], float)
            xs = np.arange(1, K + 1)
            lines.add(seed_band(ax, xs, arr, interpolate_color(ManimColor(QC.IDEA), ManimColor(LOSS), (K - 2) / 6),
                                stroke_width=2))
        pay = fs["payoff"]
        cells = VGroup()
        txt = {("SS", 0, 0): pay["SS"], ("SH", 0, 1): pay["SH"], ("HS", 1, 0): pay["HS"], ("HH", 1, 1): pay["HH"]}
        for (key, i, j), v in txt.items():
            other = {"SS": "SS", "SH": "HS", "HS": "SH", "HH": "HH"}[key]
            sq = Square(1.5, stroke_color=GREY_B, stroke_width=1.5).move_to([3.0 + 1.5 * j, 0.6 - 1.5 * i, 0])
            cells.add(VGroup(sq, MathTex(rf"{v:.2f},\ {pay[other]:.2f}", font_size=26).move_to(sq)))
        heads = VGroup(label(r"bank B: sell now", font_size=18).next_to(cells[0], UP, buff=0.1),
                       label(r"wait", font_size=18).next_to(cells[1], UP, buff=0.1),
                       label(r"A: sell now", font_size=18).next_to(cells[0], LEFT, buff=0.1),
                       label(r"wait", font_size=18).next_to(cells[2], LEFT, buff=0.1))
        nash = SurroundingRectangle(cells[0], color=LOSS, buff=0.02, stroke_width=4)
        best = SurroundingRectangle(cells[3], color=GAIN, buff=0.02, stroke_width=3)
        cap = VGroup(label(r"losses of A, B in units of $\lambda q^2$; the standstill is an orderly sale with a "
                           r"quarter less impact (assumed)", font_size=17, color=GREY_A),
                     label(r"red: what each bank's best response gives; green: what they could have had",
                           font_size=17, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        cap.next_to(cells, DOWN, buff=0.3).align_to(cells, LEFT).shift(LEFT * 1.0)
        src = note(r"simulated: 2 to 8 banks, random block sizes and random order, square-root impact, 8 seeds",
                   font_size=16).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "With square-root impact and random sizes, two to eight banks, eight seeds, the picture holds: loss rises with "
            "your place in the queue. <bookmark mark='a'/> So two banks decide. Both wait and unwind in order: three quarters "
            "each. If the other waits, selling first costs a half; if the other sells, selling too costs one, not one and a "
            "half. <bookmark mark='b'/> Selling now is each bank's best response, so both sell and both lose more: a "
            "prisoner's dilemma, played in hours."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.2, run_time=3), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(heads), FadeIn(cap))
            self.play(Create(best))
            vo.wait_until("b")
            self.play(Create(nash))
        self.wait(0.4)
        self.clear_scene()

    def archegos(self):
        c = crisis_card(r"March 2021", r"Archegos Capital Management",
                        r"A family office with concentrated positions in a few stocks, built largely through total "
                        r"return swaps with several prime brokers. The SEC alleges it grew from about \$1.5 billion "
                        r"with \$10 billion of exposure in March 2020 to more than \$36 billion with \$160 billion at "
                        r"its peak in March 2021. When the stocks fell it missed margin calls; some banks sold early, "
                        r"and those that waited lost most. Bill Hwang was convicted in July 2024 and sentenced to 18 "
                        r"years on 20 November 2024.",
                        stats=[(r"\sim\$5.5\,\text{bn}", r"Credit Suisse's loss (its report)"),
                               (r"\sim\$2.9\,\text{bn}", r"Nomura's (reported, two fiscal years)")],
                        width=7.4, font_size=19).to_edge(LEFT, buff=0.3)
        d = wrapped_label(r"Duffie (2010), ``The failure mechanics of dealer banks'' (\textit{Journal of Economic "
                          r"Perspectives}): the run goes the other way too. When a dealer looks weak, its prime-brokerage "
                          r"clients pull their cash and securities, as at Bear Stearns and Lehman in 2008.", 5.2, 19,
                          GREY_A).to_edge(RIGHT, buff=0.35).shift(UP * 1.0)
        q = desk_question(r"You are a prime broker and hear first that a big client is in trouble. What do you do, "
                          r"and to whom?", width=5.2, font_size=20).next_to(d, DOWN, buff=0.4).align_to(d, LEFT)
        src = note(r"SEC press release 2022-70 (allegations); Credit Suisse report (July 2021); Nomura's results "
                   r"(April 2021) as reported", font_size=15).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "In March 2021 it was played for real. Archegos, a family office, built concentrated positions through swaps with "
            "several prime brokers; the SEC alleges it grew from about one and a half billion dollars, with ten billion of "
            "exposure, to over thirty-six billion with a hundred and sixty billion. <bookmark mark='a'/> When its stocks fell "
            "it missed margin calls. Banks that sold early lost little; Credit Suisse lost about five and a half billion and "
            "Nomura nearly three, as they reported. Its founder was convicted in 2024. <bookmark mark='b'/> Duffie describes "
            "the mirror image: clients run from a weak dealer, as from Bear Stearns and Lehman. Pause and predict: you hear "
            "first. What do you do?"
        ) as vo:
            self.play(FadeIn(c, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(d))
            self.play(FadeIn(q))
        self.wait(1.0)
        self.clear_scene()
