from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant23.common import BAD, CONS, GOOD, MKT, PART, SDF, TAN, ask, fit_right, illustration, load


class Puzzle(VoiceoverScene):
    def construct(self):
        p = load("puzzle")
        self.card()
        self.numbers(p)
        self.mehra()
        self.habit()
        self.lrr()
        self.disasters(load("disaster"))
        self.verdict()

    def card(self):
        c = chapter_card(7, r"The equity premium puzzle", r"Why do stocks pay so much more than bills?", lit=(1985,),
                         part=PART)
        with self.voiceover("Chapter seven. The equity premium puzzle, and three answers to it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def numbers(self, p):
        rows = [cmath(r"\gamma", r"\approx", r"\frac{\mathbb{E}[R^m - R^f]}{\text{cov}(\Delta c, r^m)} = "
                      rf"\frac{{{p['prem']:.4f}}}{{{p['cov']:.6f}}} \approx "
                      rf"{p['gamma_implied']:.0f}", font_size=36, colors={r"\gamma": BAD})]
        whys = [why(r"the premium is 8.8 points a year (real, 1948--2024); the covariance of consumption with the market "
                    r"is tiny because consumption is so smooth. To make the two meet, investors would have to be "
                    r"implausibly averse to risk")]
        step = ladder(self, rows, whys, keep=1, top=2.3, x=-0.4, buff=0.8, edge=6.9)
        gam = p["gamma_implied"]
        ce = (0.5 * 1.1 ** (1 - gam) + 0.5 * 0.9 ** (1 - gam)) ** (1 / (1 - gam))
        pay = 100 * (1 - ce)
        box = VGroup(
            label(rf"what $\gamma = {gam:.0f}$ means", font_size=22, color=BAD),
            wrapped_label(f'if the same CRRA utility directly applied to wealth, a fair bet winning or losing 10\\% of wealth, such a person would pay {pay:.1f}\\% of wealth to avoid it, almost the downside. Mapping wealth gambles to consumption risk aversion requires additional assumptions', 11.0, 19, GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            f"Put chapter six's numbers into the premium formula. The market paid {100 * p['prem']:.1f} points a year over bills, after inflation. The saved sample covariance with consumption log growth and the market log return is {p['cov']:.6f}; this mixed simple-return and log-return formula is an approximation. <bookmark mark='a'/> To reconcile them, gamma must be about {p['gamma_implied']:.0f}. If that same CRRA coefficient applied directly to wealth, a person would pay {pay:.0f} percent of their wealth to avoid a fair bet that wins or loses ten: almost the whole downside, to escape a coin toss. Relating this wealth gamble to consumption risk aversion requires an additional mapping; it is not a direct empirical measurement of consumption preferences."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(box))
        self.wait(0.4)
        self.clear_scene()

    def mehra(self):
        cc = crisis_card(r"1985", r"Mehra and Prescott",
                         r"in 'The equity premium: a puzzle', a calibrated Lucas economy with risk aversion up to 10 "
                         r"could produce an equity premium of at most 0.35 points a year, against the 6 points observed "
                         r"in US data from 1889 to 1978; raising risk aversion to close the gap made the riskless rate far "
                         r"too high",
                         stats=[(r"0.35\%", r"the model's largest premium"), (r"6\%", r"observed, 1889--1978")],
                         width=8.8, font_size=19).move_to(UP * 0.3)
        with self.voiceover(
            "Rajnish Mehra and Edward Prescott put the puzzle in its classic form in 1985. A carefully calibrated version "
            "of Lucas's economy, with risk aversion up to ten, could produce an equity premium of at most a third of a "
            "percent a year. The data showed six. And raising risk aversion to close the gap sent the riskless rate "
            "through the roof. Forty years of research since has been, in large part, an attempt to answer them. Here "
            "are the three most important answers."
        ) as vo:
            self.play(FadeIn(cc))
        self.wait(0.4)
        self.clear_scene()

    def habit(self):
        rows = [cmath(r"u", r"=", r"\frac{(C_t - X_t)^{1-\gamma}}{1-\gamma},\quad S_t = \frac{C_t - X_t}{C_t}", font_size=38,
                      colors={r"u": CONS}),
                cmath(r"\text{local risk aversion}", r"=", r"\frac{\gamma}{S_t}", font_size=40,
                      colors={r"\text{local risk aversion}": BAD})]
        whys = [why(r"Campbell and Cochrane (1999): utility depends on consumption above a habit $X_t$ that follows past "
                    r"consumption slowly; $S$ is the surplus"),
                why(r"in a recession consumption falls toward the habit, the surplus shrinks, and effective risk aversion "
                    r"soars: investors demand most compensation exactly when stocks have fallen, so prices are volatile "
                    r"and returns predictable")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "First, habits. John Campbell and John Cochrane let utility depend on consumption above a habit level that "
            "follows past consumption slowly. <bookmark mark='a'/> When a recession pushes consumption down toward the "
            "habit, the surplus shrinks and effective risk aversion soars. Investors then demand a large premium exactly "
            "when stocks have already fallen, which makes prices volatile and returns predictable, as chapter eight will "
            "find them to be, with a modest gamma at the core."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def lrr(self):
        rows = [cmath(r"\Delta c_{t+1}", r"=", r"\mu + x_t + \sigma_t\,\eta_{t+1},\quad x_{t+1} = \rho x_t + \varphi_e\sigma_t "
                      r"e_{t+1},\ \rho \approx 0.98", font_size=32, colors={r"\Delta c_{t+1}": CONS})]
        whys = [why(r"Bansal and Yaron (2004): a small, persistent component $x_t$ in growth, hard to see in the data, and "
                    r"slowly changing volatility; with Epstein--Zin preferences investors care about such news about the "
                    r"long run, and stocks, whose dividends load on it, pay a large premium for it")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "Second, long-run risk. Ravi Bansal and Amir Yaron suggested that consumption growth contains a small, very "
            "persistent component, almost invisible year by year, plus slowly changing volatility. With preferences "
            "that care about the timing of uncertainty, investors fear news about the long run, and stocks, whose "
            "dividends are exposed to it, must pay a large premium. The difficulty is that the key ingredient is, by "
            "construction, hard to measure."
        ) as vo:
            step(0)
        self.wait(0.4)
        self.clear_scene()

    def disasters(self, d):
        g_ = np.asarray(d["gams"])
        p29, p40, base = (100 * np.asarray(d["prem"]["0.29"]), 100 * np.asarray(d["prem"]["0.4"]),
                          100 * np.asarray(d["base"]))
        g = axes([1, 10], [0, 120], x_length=7.2, y_length=4.4, xlabel=r"risk aversion $\gamma$",
                 ylabel=r"equity premium, \% a year", xticks=[2, 4, 6, 8, 10], yticks=[0, 30, 60, 90, 120], font_size=14).to_edge(
            LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        l0 = curve(ax, g_, base, GREY_B, stroke_width=2.5)
        l1 = curve(ax, g_, p29, TAN, stroke_width=3)
        l2 = curve(ax, g_, p40, BAD, stroke_width=3)
        k4 = int(np.argmin(np.abs(g_ - 4)))
        side = VGroup(
            legend([(GREY_B, r"no disasters"), (TAN, r"disasters, $b$ = 0.29"), (BAD, r"disasters, $b$ = 0.40")],
                   font_size=17),
            MathTex(rf"\gamma = 4:\ {base[k4]:.2f}\%,\ {p29[k4]:.1f}\%,\ {p40[k4]:.1f}\%", font_size=24),
            wrapped_label("premium $\\approx \\gamma\\sigma^2 + p\\,\\mathbb{E}[b(1-b)^{-\\gamma}]$ with $\\sigma$ = 2\\% and $p$ = 1.7\\% a year, Barro's (2006) estimate from twentieth-century depressions in 35 countries (mean contraction 0.29); fixed-loss toy approximation; Jensen gives a lower bound only for a convex loss term under the same probability law and mean, not for the full Barro economy",
                          3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"Third, disasters. Thomas Rietz in 1988 and Robert Barro in 2006 argued that the data from calm countries miss the rare catastrophes: wars, depressions, revolutions. Barro counted them across thirty-five countries in the twentieth century: a contraction of fifteen percent or more in output, with a probability of about one point seven percent a year, averaging twenty-nine percent. <bookmark mark='a'/> Without disasters, a risk aversion of four gives a premium of a sixth of a point. <bookmark mark='b'/> With them, about {p29[k4]:.0f} percent; if the average disaster is forty percent deep, {p40[k4]:.0f}. This fixed-loss approximation illustrates a mechanism, not the full calibrated Barro economy. The full displayed range reaches about one hundred and thirteen percent at gamma ten for the forty-percent loss; no tail is clipped. A Jensen lower-bound argument applies only under the same probability law and mean with a convex loss term."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(l0), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(l1), Create(l2), FadeIn(side[1]), FadeIn(side[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def verdict(self):
        cards = VGroup(
            desk_question('the risk-based interpretation', 'in these models, the premium compensates bad-state risk; the historical mean alone does not establish the cause; consumption measured quarterly is too smooth to show those times; something with fatter tails or slower dynamics is needed', width=12.0, font_size=21),
            desk_question(r"what is not", r"which something: habits, long-run risk and disasters fit the same average "
                          r"premium and differ in what they predict for volatility, predictability and options",
                          width=12.0, font_size=21),
            desk_question(r"for an investor", 'if crash risk is the mechanism, expected compensation is conditional; holding through a crash guarantees neither recovery nor a positive realised premium (Part 22, chapter 3)', width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Where does that leave us? <bookmark mark='a'/> In these risk-based models, the premium compensates exposure to bad states. Smooth measured consumption challenges the simplest specification; the historical premium alone does not prove the risk-based explanation. <bookmark mark='b'/> Habits, long-run risk and disasters all fit the average premium; they differ in what they predict for volatility, predictability, and the prices of options on the market, which is where they are tested now. <bookmark mark='c'/> If crash risk is the mechanism, expected compensation is conditional and realised losses can still be permanent. Holding through a crash guarantees neither recovery nor a positive realised premium."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"in a disaster model with $p$ = 2\% a year and $b$ = 30\%, how would the price of deep out-of-the-money "
                r"index puts differ from a model without disasters?")
        with self.voiceover("In a disaster model with a two percent yearly chance of a thirty percent fall, how would deep "
                            "out-of-the-money index puts be priced, compared with a model without disasters?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
