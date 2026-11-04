from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant23.common import SDF as SDFC, BAD, CONS, GOOD, MKT, PART, TAN, ask, fit_right, illustration, load


class SDF(VoiceoverScene):
    def construct(self):
        h = load("hj")
        self.card()
        self.one_equation()
        self.special_cases()
        self.qmeasure()
        self.hj_derive()
        self.hj_numbers(h)
        self.hj_cup(h)

    def card(self):
        c = chapter_card(4, r"One price equation", r"What do all asset pricing models have in common?", lit=(1991,),
                         part=PART)
        with self.voiceover("Chapter four. The single equation behind every model of risk and return."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def one_equation(self):
        rows = [cmath(r"p_t", r"=", r"\mathbb{E}_t\big[m_{t+1}\,x_{t+1}\big]", font_size=48, colors={r"p_t": SDFC}),
                cmath(r"1", r"=", r"\mathbb{E}[m R],\qquad 0 = \mathbb{E}[m R^e]", font_size=44),
                cmath(r"\mathbb{E}[R^e]", r"=", r"-\frac{\text{cov}(m, R^e)}{\mathbb{E}[m]}", font_size=44,
                      colors={r"\mathbb{E}[R^e]": MKT})]
        whys = [why(r"a price is the expected payoff weighted by $m$, the stochastic discount factor: positive, and high "
                    r"in the states where an extra dollar is worth most. It exists whenever there is no arbitrage (Part 9)"),
                why(r"for a gross return the price is 1; for an excess return (long one asset, short another) it is 0"),
                why(r"so expected excess returns are set by covariance with $m$: an asset that pays off when $m$ is high, "
                    r"in bad times, is insurance and earns less; one that pays off in good times must earn more")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "Here is the equation. The price of any payoff is the expectation of that payoff times a random discount "
            "factor, m, which is large in the states of the world where an extra dollar is worth most. Part nine showed "
            "that such an m exists whenever there is no arbitrage. <bookmark mark='a'/> For a return, the price is one; "
            "for an excess return, zero. <bookmark mark='b'/> And so the expected excess return of anything is minus its "
            "covariance with the discount factor. An asset that pays when times are bad, when m is high, is insurance, "
            "and earns less. One that pays in good times must offer more. Risk premia are about when you get paid, not "
            "how much the payoff varies."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def special_cases(self):
        cards = VGroup(
            desk_question(r"$m = a - b\,R^m$", r"the CAPM: the discount factor is linear in the market's return",
                          width=12.0, font_size=21),
            desk_question(r"$m = \beta\,(C_{t+1}/C_t)^{-\gamma}$", r"the consumption model (chapter 6): dollars are worth "
                          r"most when consumption falls", width=12.0, font_size=21),
            desk_question(r"$m = a - b^\top f$", r"any linear factor model, Fama and French's included (Part 24)",
                          width=12.0, font_size=21),
            desk_question(r"$m = $ the intermediary's marginal value of wealth",
                          r"chapter 9: when dealers' capital is scarce, every dollar they have is worth more", width=12.0,
                          font_size=21),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Every model in this part is a choice of m. <bookmark mark='a'/> If m is linear in the market's return, you "
            "have the CAPM. <bookmark mark='b'/> If it is the growth of consumption raised to a power, the consumption "
            "model. <bookmark mark='c'/> If it is linear in some factors, a factor model of the kind Part twenty-four "
            "studies. <bookmark mark='d'/> And if it is the value of a dollar to the dealers who make markets, the "
            "intermediary models of chapter nine. The equation is always the same; the economics is in m."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c", "d")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def qmeasure(self):
        rows = [cmath(r"p", r"=", r"\mathbb{E}[m\,x] = \frac{1}{R^f}\,\mathbb{E}\Big[\frac{m}{\mathbb{E}[m]}\,x\Big]"
                      r" = \frac{1}{R^f}\,\mathbb{E}^{\mathbb{Q}}[x]", font_size=38, colors={r"p": SDFC}),
                cmath(r"\frac{d\mathbb{Q}}{d\mathbb{P}}", r"=", r"m\,R^f", font_size=42),
                cmath(r"\mathbb{E}[R^e]", r"=", r"\mathbb{E}^{\mathbb{P}}[R^e] - \mathbb{E}^{\mathbb{Q}}[R^e]", font_size=40,
                      colors={r"\mathbb{E}[R^e]": MKT})]
        whys = [why(r"since $\mathbb{E}[m] = 1/R^f$, normalising $m$ by its mean gives a probability density: the "
                    r"risk-neutral measure of Parts 4 and 9, under which every price is a discounted expectation"),
                why(r"the discount factor and the risk-neutral density are the same object: $\mathbb{Q}$ puts more "
                    r"weight than $\mathbb{P}$ on the states where $m$ is high"),
                why(r"so a risk premium is the gap between real-world and risk-neutral expectations: option prices "
                    r"reveal $\mathbb{Q}$, history estimates $\mathbb{P}$, and the premium is the difference")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "This equation is an old friend in new clothes. The expected discount factor is one over the riskless "
            "return, so divide m by its mean and you have a probability density. <bookmark mark='a'/> Weighting the "
            "real-world probabilities by it gives the risk-neutral measure of Parts four and nine, under which every "
            "price is a discounted expectation. The derivatives desk and the research desk use the same object: one "
            "calls it Q, the other m. Q simply tilts the probabilities toward the states where a dollar is worth most. "
            "<bookmark mark='b'/> And so a risk premium is the gap between two expectations, the real-world one and "
            "the risk-neutral one. Option prices reveal the second; history estimates the first. Part twelve's "
            "variance risk premium was exactly that gap, measured for volatility."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def hj_derive(self):
        rows = [cmath(r"0", r"=", r"\mathbb{E}[m]\,\mathbb{E}[R^e] + \rho_{m,R^e}\,\sigma(m)\,\sigma(R^e)", font_size=40),
                cmath(r"\frac{\sigma(m)}{\mathbb{E}[m]}", r"\geq", r"\frac{|\mathbb{E}[R^e]|}{\sigma(R^e)}", font_size=44,
                      colors={r"\frac{\sigma(m)}{\mathbb{E}[m]}": SDFC})]
        whys = [why(r"write $0 = \mathbb{E}[m R^e]$ as the product of means plus the covariance, and the covariance as "
                    r"a correlation times two volatilities"),
                why(r"since $|\rho| \le 1$: Hansen and Jagannathan (1991). Any discount factor that prices a set of "
                    r"returns must be at least as volatile, relative to its mean, as the best Sharpe ratio they offer")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "The equation has a powerful consequence. Write the excess-return version as the product of means plus a "
            "covariance, and the covariance as a correlation times two volatilities. <bookmark mark='a'/> The "
            "correlation is at most one, so the discount factor's volatility, relative to its mean, must be at least "
            "the Sharpe ratio. Lars Hansen and Ravi Jagannathan used this in 1991 to test whole classes of models at "
            "once: whatever your m is, it has to be at least this volatile."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def hj_numbers(self, h):
        rows = [(r"the market alone", h["sr_mkt"], MKT), (r"ten industries", h["sr_ind"], TAN),
                (r"25 size and value portfolios, in sample", h["sr_ff25"], BAD),
                (r"the same, fitted before 1994 and held after", h["sr_ff25_oos"], GOOD)]
        g = axes([0, 1.5], [-0.6, len(rows) - 0.4], x_length=6.0, y_length=3.6, xlabel=r"largest Sharpe ratio, a year",
                 ylabel=r"", xticks=[0, 0.5, 1.0, 1.5], yticks=[], font_size=14).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, (nm, v, c_) in enumerate(rows):
            y = len(rows) - 1 - i
            x0, x1 = ax.c2p(0, 0)[0], ax.c2p(v, 0)[0]
            b_ = Rectangle(width=x1 - x0, height=0.5, stroke_width=0, fill_color=c_, fill_opacity=0.85).move_to(
                [(x0 + x1) / 2, ax.c2p(0, y)[1], 0])
            bars.add(VGroup(b_, MathTex(f"{v:.2f}", font_size=22).next_to(b_, RIGHT, buff=0.08),
                            label(nm, font_size=16).next_to([x0 - 0.15, ax.c2p(0, y)[1], 0], LEFT, buff=0)))
        foot = wrapped_label(r"monthly 1963--2020, annualised. The bound for any model that prices these assets: its "
                             r"discount factor must have $\sigma(m)/E(m)$ at least this large, about 0.5 a year for the "
                             r"market and far more for the cross-section", 12.4, 17, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "So how volatile must m be? <bookmark mark='a'/> The market alone has had a Sharpe ratio of about "
            f"{h['sr_mkt']:.2f} a year since 1963. Ten industries combined optimally, {h['sr_ind']:.2f}. Twenty-five "
            f"portfolios sorted on size and value, in sample, {h['sr_ff25']:.2f}; fitted on the first half and held in "
            f"the second, still {h['sr_ff25_oos']:.2f}. <bookmark mark='b'/> Any model that prices these assets needs a "
            "discount factor whose volatility is at least half its mean every year, and more like its whole mean. "
            "That is a very volatile marginal value of a dollar."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def hj_cup(self, h):
        Em, bd = np.asarray(h["Em"]), np.asarray(h["bound"])
        g = axes([0.5, 1.02], [0, 0.9], x_length=7.2, y_length=4.4, xlabel=r"$E(m)$", ylabel=r"$\sigma(m)$",
                 xticks=[0.6, 0.7, 0.8, 0.9, 1.0], yticks=[0, 0.2, 0.4, 0.6, 0.8], font_size=14).to_edge(
            LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        ok = (Em >= 0.5)
        cup = curve(ax, Em[ok], np.minimum(bd[ok], 0.9), SDFC, stroke_width=3.5)
        pts = VGroup(*[VGroup(Dot(ax.c2p(p_["Em"], p_["sd"]), color=CONS, radius=0.07),
                              MathTex(rf"\gamma={p_['gamma']}", font_size=18, color=CONS).next_to(
                                  ax.c2p(p_["Em"], p_["sd"]), RIGHT, buff=0.06))
                       for p_ in h["pts"] if p_["sd"] <= 0.85])
        side = VGroup(
            legend([(SDFC, r"the Hansen--Jagannathan bound"), (CONS, r"power utility, $\beta$ = 0.98")], font_size=17),
            wrapped_label(r"annual real returns of the market and the bill, 1948--2025: the bound is the cup, and an "
                          r"admissible discount factor must lie above it. Consumption's own volatility is small, so power "
                          r"utility reaches the cup only at a risk aversion above 20, where its mean has fallen far "
                          r"below one: interest rates would have to be very high", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "With gross returns the bound becomes a cup: for each possible mean of the discount factor, the least "
            "volatility it can have. <bookmark mark='a'/> Now try the most natural discount factor of all, consumption "
            "growth raised to a power of minus gamma. <bookmark mark='b'/> With low risk aversion it sits far below the "
            "cup: consumption barely moves, so neither does m. It reaches the cup only above a gamma of about twenty, "
            "and by then its mean has fallen well below one, which would imply interest rates far higher than any we "
            "have seen. That is the equity premium puzzle, drawn as a picture, and chapters six and seven take it apart."
        ) as vo:
            self.play(FadeIn(g), Create(cup), FadeIn(side[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.3), FadeIn(side[1]))
        q = ask(r"an asset has a Sharpe ratio of 2. What does Hansen--Jagannathan say about any model that prices it, and "
                r"what would you suspect first?")
        with self.voiceover("An asset shows a Sharpe ratio of two. What does the bound say about any model that prices it, "
                            "and what would you suspect first?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
