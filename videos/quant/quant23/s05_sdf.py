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
            "Here is the equation. The price of any payoff is the expectation of that payoff times a random discount factor, m, which is large in the states of the world where an extra dollar is worth most. Part nine showed that such an m exists whenever there is no arbitrage. <bookmark mark='a'/> For a return, the price is one; for an excess return, zero. <bookmark mark='b'/> And so the expected excess return of anything is minus its covariance with the discount factor, divided by the discount factor's positive mean. An asset that pays when times are bad, when m is high, is insurance, and earns less. One that pays in good times must offer more. Risk premia are about when you get paid, not how much the payoff varies."
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
            "Every model in this part is a choice of m. <bookmark mark='a'/> If m is linear in the market's return, you have the CAPM. <bookmark mark='b'/> If it is the growth of consumption raised to a power, the consumption model. <bookmark mark='c'/> If it is linear in some factors, a factor model of the kind Part twenty-four studies. <bookmark mark='d'/> And if it is the value of a dollar to the dealers who make markets, the intermediary models of chapter nine. The equation is the same; the economics is in m. Linear factor pricing projections can be negative, so those projections are not automatically positive discount factors or probability densities."
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
        whys = [why('since $\\mathbb{E}[m] = 1/R^f$, for a strictly positive $m$ and a known one-period gross $R^f$, normalising $m$ gives a probability density: the risk-neutral measure of Parts 4 and 9, under which every price is a discounted expectation'),
                why(r"the discount factor and the risk-neutral density are the same object: $\mathbb{Q}$ puts more "
                    r"weight than $\mathbb{P}$ on the states where $m$ is high"),
                why(r"so a risk premium is the gap between real-world and risk-neutral expectations: option prices "
                    r"reveal $\mathbb{Q}$, history estimates $\mathbb{P}$, and the premium is the difference")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "This equation is an old friend in new clothes. Use a strictly positive discount factor and a known one-period gross risk-free return, with conditional expectations if rates vary by state. The expected discount factor is then one over that risk-free return, so divide m by its mean and you have a probability density. <bookmark mark='a'/> Weighting the real-world probabilities by it gives the risk-neutral measure of Parts four and nine, under which every price is a discounted expectation. The derivatives desk and the research desk use the same object: one calls it Q, the other m. Q simply tilts the probabilities toward the states where a dollar is worth most. <bookmark mark='b'/> And so a risk premium is the gap between two expectations, the real-world one and the risk-neutral one. Option prices constrain risk-neutral expectations for the traded payoffs; a limited option surface need not identify every state price. History estimates physical expectations with uncertainty. Part twelve's variance risk premium was exactly that gap, measured for volatility."
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
        foot = wrapped_label('1963--2020 monthly returns. Bars are monthly Sharpe ratios times $\\sqrt{12}$; divide by $\\sqrt{12}$ for the monthly HJ coefficient-of-variation bound. These are not annual SDF bounds', 12.4, 17, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            f"So how volatile must m be? <bookmark mark='a'/> The market alone has had a Sharpe ratio of about {h['sr_mkt']:.2f} a year since 1963. Ten industries combined optimally, {h['sr_ind']:.2f}. Twenty-five portfolios sorted on size and value, in sample, {h['sr_ff25']:.2f}; fitted on the first half and held in the second, still {h['sr_ff25_oos']:.2f}. <bookmark mark='b'/> These bars annualise monthly Sharpe ratios by multiplying by the square root of twelve. Divide each bar by that factor to obtain the necessary coefficient-of-variation bound for a monthly discount factor. They do not measure an annual discount factor's volatility. The fitted portfolios are retrospective, and the later window rebalances the fixed fitted exposures without costs."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def hj_cup(self, h):
        audit = load("hj_display_audit")
        Em, bd = np.asarray(audit["Em"]), np.asarray(audit["bound"])
        g = axes([0.5, 1.02], [0, 22], x_length=6.8, y_length=4.3, xlabel=r"$E(m)$", ylabel=r"$\sigma(m)$",
                 xticks=[0.5, 0.7, 0.9, 1.0], yticks=[0, 5, 10, 15, 20], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        cup = curve(g.ax, Em, bd, SDFC, stroke_width=3)
        pts = VGroup(*[Dot(g.ax.c2p(p["Em"], p["sd"]), color=CONS, radius=0.055) for p in audit["points"]])
        rows = [label(r"$\gamma$       $E(m)$     $\sigma(m)$      bound", font_size=19)]
        rows += [MathTex(rf"{p['gamma']:2d}\quad {p['Em']:.3f}\quad {p['sd']:.3f}\quad {p['lower_bound']:.2f}", font_size=20, color=CONS)
                 for p in audit["points"]]
        side = VGroup(*rows).arrange(DOWN, buff=0.18, aligned_edge=LEFT).to_edge(RIGHT, buff=0.45).shift(UP * 0.35)
        foot = wrapped_label(r"1948--2024 annual real market and ex-post-deflated nominal bills; latter have inflation risk. Fixed grid, original sample moments. Necessary L2 bound, without positivity. All seven CRRA points fail at their own means.", 12.2, 17, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover("The gross-return bound depends on the discount factor's mean. The original chart covered only a narrow mean interval and clipped its height. This explicitly named display audit applies the unchanged formula to the same 1948 to 2024 sample moments on a fixed wider grid. <bookmark mark='a'/> The green points use the seven original consumption-model risk aversions and beta of point nine eight. <bookmark mark='b'/> The table compares each point at its own mean. All seven lie below the necessary bound, including gamma twenty and fifty. We therefore cannot claim that gamma twenty reaches the curve. The bound uses real market returns and nominal bills deflated after the fact; those bills have inflation risk. It is a sample lower bound without a positivity restriction, and being above it would still not establish that a positive factor prices all assets. An inverse mean would price a hypothetical known real risk-free payoff, not the inflation-risky bill shown here.") as vo:
            self.play(FadeIn(g), Create(cup), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(pts))
            vo.wait_until("b")
            self.play(FadeIn(side))
        q = ask(r"a monthly asset Sharpe ratio is 2. What monthly HJ bound follows, and what if 2 was an annualised monthly ratio?")
        with self.voiceover('A monthly asset Sharpe ratio is two. What monthly bound follows? How does the answer change if two was an annualised monthly ratio?'):
            self.play(FadeOut(foot), FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
