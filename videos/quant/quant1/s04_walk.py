from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import GAIN, GAUSS, LOSS, PART, REAL

C_ = {r"P_t": REAL, r"P_{t+1}": REAL, r"X": QC.IDEA, r"\mathbb E_t": GREY_A, r"\mathbb E_{t+1}": GREY_A}


def row(*parts, fs=42):
    return cmath(*parts, colors=C_, font_size=fs)


class Walk(VoiceoverScene):
    def construct(self):
        self.card()
        self.people()
        self.proof()
        self.coins()
        self.nuance()

    def card(self):
        c = chapter_card(3, r"The random walk", r"If prices are fair, why are they unpredictable?",
                         lit=(1933, 1953, 1959, 1965), part=PART)
        with self.voiceover("Chapter three. The random walk."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def people(self):
        c1 = history_card(1933, r"Alfred Cowles, \textit{Econometrica}",
                          r"``Can stock market forecasters forecast?'': the forecasting services and publications he "
                          r"followed from 1928 to 1932 did, as a group, worse than chance", width=6.2, font_size=22)
        c2 = history_card(1953, r"Maurice Kendall, \textit{JRSS}",
                          r"22 weekly price series: ``as if once a week the Demon of Chance drew a random number'' and "
                          r"added it to the price", width=6.2, font_size=22)
        c3 = history_card(1959, r"M.\ F.\ M.\ Osborne, \textit{Operations Research}",
                          r"a physicist: the \emph{logarithm} of price moves like a particle in Brownian motion",
                          width=6.2, font_size=22)
        c4 = history_card(1965, r"Paul Samuelson, \textit{Industrial Management Review}",
                          r"``Proof that properly anticipated prices fluctuate randomly''", width=6.2, font_size=22)
        cards = VGroup(c1, c2, c3, c4).arrange_in_grid(2, 2, buff=(0.45, 0.45)).move_to(ORIGIN)
        with self.voiceover(
            "By the middle of the century the evidence was piling up. In 1933 Alfred Cowles, who had paid for "
            "market forecasts himself, checked them: the forecasting services and publications he followed through "
            "the crash did, as a group, worse than chance. <bookmark mark='a'/> In 1953 Maurice Kendall studied "
            "twenty-two weekly price series and found nothing to predict, as if, he wrote, once a week the Demon of "
            "Chance drew a random number and added it to the price. <bookmark mark='b'/> In 1959 the physicist "
            "Maury Osborne argued that it is the logarithm of the price that wanders like a particle in Brownian "
            "motion: log returns, the sums of the last chapter. <bookmark mark='c'/> Economists found this "
            "unsettling. Did it mean markets were irrational? In 1965 Samuelson showed the opposite: randomness is "
            "what a well-working market should produce."
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c3, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(c4, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        rows = [
            row(r"P_t", r"=", r"\mathbb E_t", r"[\,", r"X", r"\,]"),
            row(r"\mathbb E_t", r"[\,", r"P_{t+1}", r"\,]", r"=", r"\mathbb E_t", r"\big[\,", r"\mathbb E_{t+1}",
                r"[\,", r"X", r"\,]", r"\,\big]"),
            row(r"\mathbb E_t", r"[\,", r"P_{t+1}", r"\,]", r"=", r"\mathbb E_t", r"[\,", r"X", r"\,]", r"=", r"P_t"),
            row(r"\mathbb E_t", r"[\,", r"P_{t+1} - P_t", r"\,]", r"=", r"0"),
        ]
        rows[2][2].set_color(REAL)
        rows[3][2].set_color(REAL)
        whys = [why(r"the price is the expected value of what the asset will pay, given what is known now"),
                why(r"tomorrow's price is tomorrow's expectation"),
                why(r"tower property: you can't expect to change your own expectation"),
                why(r"so the expected price change is zero: a martingale")]
        # align on the first '='
        idx = [1, 4, 4, 4]
        top = 2.8
        for i, (r_, w_) in enumerate(zip(rows, whys)):
            r_.shift((-1.6 - r_[idx[i]].get_center()[0]) * RIGHT)
            r_.set_y(top - 1.35 * i)
            w_.next_to(r_, DOWN, buff=0.15).align_to(r_, LEFT)
        thm = theorem_card(r"Samuelson (1965)", r"If the price is the expectation of a fixed future value, given "
                           r"everything known today, then price changes cannot be predicted from anything known today.",
                           width=10.5, font_size=24).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The proof fits in four lines. Suppose an asset will one day be worth X, and today's price is the best "
            "estimate of X, given everything known today: the expectation of X conditional on today's "
            "information. <bookmark mark='a'/> Then tomorrow's price is tomorrow's expectation of X. What do we "
            "expect it to be, today? <bookmark mark='b'/> The expectation, today, of tomorrow's expectation is just "
            "today's expectation. That is the tower property of conditional expectation, and it says something "
            "obvious once heard: you cannot expect to change your own mind. If you could, you would already have "
            "changed it. <bookmark mark='c'/> So the expected price change is zero. Any predictable part of "
            "tomorrow's move would already be in today's price. <bookmark mark='d'/> A sequence with this property "
            "is called a martingale, and it is the mathematical form of a fair game."
        ) as vo:
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("a")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            vo.wait_until("d")
            self.play(FadeIn(thm, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def coins(self):
        n = 20
        rng = np.random.default_rng(1965)
        flips = rng.integers(0, 2, n)
        heads = np.concatenate([[0], np.cumsum(flips)])
        price = heads + (n - np.arange(n + 1)) / 2.0
        lo, hi = float(np.floor(price.min()) - 1), float(np.ceil(price.max()) + 1)
        g = axes([0, n], [lo, hi], x_length=8.4, y_length=4.4, xlabel=r"coins tossed so far",
                 ylabel=r"the price: expected number of heads", xticks=[0, 5, 10, 15, 20],
                 yticks=list(range(int(lo) + 1, int(hi), 2)),
                 font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.4)
        ax = g.ax
        setup = VGroup(label(r"A contract pays \$1 for every head in 20 tosses of a fair coin.", font_size=26),
                       MathTex(r"P_t = \underbrace{H_t}_{\text{heads so far}} + \underbrace{\tfrac12(20 - t)}_{"
                               r"\text{expected from the rest}}", font_size=34, color=REAL)
                       ).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.3)
        coins = VGroup()
        for i, f in enumerate(flips):
            c = Circle(radius=0.17, stroke_color=GAIN if f else LOSS, stroke_width=2, fill_color=GAIN if f else LOSS,
                       fill_opacity=0.25)
            t = MathTex("H" if f else "T", font_size=20, color=GAIN if f else LOSS).move_to(c)
            coins.add(VGroup(c, t))
        coins.arrange_in_grid(4, 5, buff=0.12).to_edge(RIGHT, buff=0.8).shift(UP * 0.2)
        steps = VGroup()
        dots = VGroup(Dot(ax.c2p(0, price[0]), radius=0.06, color=REAL))
        for i in range(n):
            steps.add(Line(ax.c2p(i, price[i]), ax.c2p(i + 1, price[i + 1]), color=REAL, stroke_width=3.5))
            dots.add(Dot(ax.c2p(i + 1, price[i + 1]), radius=0.06, color=REAL))
        move = wrapped_label(r"each toss moves the price by $\pm\tfrac12$, equally likely", 3.6, 24, GREY_A)
        move.next_to(coins, DOWN, buff=0.4)
        end = MathTex(rf"P_{{20}} = X = {heads[-1]}", font_size=34, color=QC.IDEA).next_to(move, DOWN, buff=0.35)
        with self.voiceover(
            "Here is a fair price at work. A contract pays a dollar for every head in twenty tosses of a fair coin. "
            "Before any toss, its fair price is ten dollars. After some tosses, it is the heads so far, plus half "
            "of the tosses still to come. <bookmark mark='a'/> Watch the price as the coins land. Each head adds "
            "half a dollar, each tail takes half a dollar away, with equal chances. The price wanders, and by the "
            "end it has found the true value. At no point could anyone predict its next step, and that is not "
            "because the market is foolish: it is because the price already contains everything that can be known. "
            "Information arrives at random, so the price moves at random."
        ) as vo:
            self.play(FadeIn(setup), FadeIn(g), FadeIn(dots[0]))
            vo.wait_until("a")
            per = max(vo.remaining(2.0) / n, 0.35)
            for i in range(n):
                self.play(FadeIn(coins[i], scale=1.3), Create(steps[i]), FadeIn(dots[i + 1]), run_time=per)
                if i == 2:
                    self.play(FadeIn(move), run_time=0.4)
            self.play(FadeIn(end))
        self.wait(0.4)
        self.clear_scene()

    def nuance(self):
        dm = definition_card(r"Martingale", r"$\mathbb E_t[P_{t+1}] = P_t$: the expected next value is the current "
                             r"one. The \emph{size} of the moves may change over time, and they need not be "
                             r"independent; they only cannot be predicted in direction.", width=6.2, color=REAL)
        dr = definition_card(r"Random walk", r"$P_{t+1} = P_t + \varepsilon_{t+1}$, the $\varepsilon$ independent "
                             r"and identically distributed: a stricter claim. Every day is the same kind of day.",
                             width=6.2, color=GAUSS, kind=r"Definition")
        pair = VGroup(dm, dr).arrange(RIGHT, buff=0.45, aligned_edge=UP).shift(UP * 1.3)
        caveats = VGroup(
            label(r"Two refinements the series will need:", font_size=26, color=GREY_A),
            label(r"1. Stocks earn a premium: the martingale is the price after adjusting for its expected return "
                  r"(Parts 4, 9, 23)", font_size=23),
            label(r"2. ``Fair'' is a claim about expectations, not about risk: the moves can be wild (chapters 5--8)",
                  font_size=23),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(pair, DOWN, buff=0.55)
        if caveats.width > 13.0:
            caveats.scale_to_fit_width(13.0)
        with self.voiceover(
            "Two words are easy to confuse, and the difference is the rest of this part. A martingale only says the "
            "expected next value is today's value. The size of the moves can change, calm weeks and wild weeks, and "
            "moves can depend on each other in every way except direction. <bookmark mark='a'/> A random walk is a "
            "stronger claim: every move independent, and drawn from the same distribution, so every day is the "
            "same kind of day. Samuelson proved the first, not the second. <bookmark mark='b'/> Two refinements "
            "will follow us. Stocks are expected to rise, because holding them is risky, so the fair game is the "
            "price after allowing for that expected return; making that precise takes Parts four, nine and "
            "twenty-three. And fair is a statement about averages, not about safety. The next chapters measure how "
            "wild a fair game can be."
        ) as vo:
            self.play(FadeIn(dm, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(dr, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in caveats], lag_ratio=0.5, run_time=3))
        self.wait(0.4)
        self.clear_scene()
