from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant23.common import BAD, FRONT, GOOD, MKT, PART, SDF, TAN, fit_right, load

T1, T2, PR = MKT, FRONT, BAD


class Research(VoiceoverScene):
    def construct(self):
        t = load("speculation_theory")
        self.card()
        self.model()
        self.example(t)
        self.why_more()
        self.sweep(t)
        self.sx()
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Speculative bubbles from disagreement", r"Can a price exceed what every single investor thinks "
                          r"the asset is worth?", part=PART)
        with self.voiceover("For the researcher: Chapter 12's rational bubbles needed an infinite horizon and a price "
                            "growing at the interest rate. Here is a different kind: investors who agree to disagree, who "
                            "cannot sell short, and who pay for the right to sell to someone more optimistic later. The "
                            "price ends up above every investor's own valuation."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"V_i(s)", r"=", r"\sum_{t \ge 1}\beta^t\,\big(Q_i^t d\big)(s)", font_size=32, colors={r"V_i(s)": T1}),
                cmath(r"P(s)", r"=", r"\beta\,\max_i\ \big(Q_i(d + P)\big)(s)", font_size=34, colors={r"P(s)": PR}),
                cmath(r"P", r"\ge", '\\max_i V_i',
                      font_size=28, colors={r"P": PR})]
        whys = [why(r"each type $i$ believes the dividend state follows the Markov chain $Q_i$: its own value of holding "
                    r"for ever, buy-and-hold"),
                why("no short sales and many investors of each type: the asset sits with whoever values it most, next period's dividend plus the resale price. A fixed point, a contraction for $\\beta < 1$"),
                why('since $P \\ge \\beta Q_i(d + P)$ for every $i$, iterating gives $P \\ge V_i$; changing strict optimists with suitable reachability give strict inequalities; ties alone do not: the excess is the value of the option to resell')]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        thm = theorem_card(r"Speculative behaviour", wrapped_label(
            r"with heterogeneous expectations and no short sales, the equilibrium price can exceed what any investor would "
            r"pay to hold the asset for ever; investors buy in order to resell, and the price contains a speculative "
            r"premium", 10.6, 20, GREY_A), who=r"Harrison and Kreps (1978), \textit{Quarterly Journal of Economics} 92",
            width=11.6, font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Michael Harrison and David Kreps wrote the model down in 1978. <bookmark mark='a'/> Each type of investor has its own view of how the dividend moves, and its own buy-and-hold value. <bookmark mark='b'/> Nobody can sell short, and there are many investors of each type, so the asset sits with whoever values it most: next period's dividend plus the price at which it can be sold tomorrow. <bookmark mark='c'/> Iterate, and the price is at least every type's buy-and-hold value, with strictness under changing strict optimists and suitable reachability, as in the positive transition matrices of this fixed example. Merely changing an arbitrary tie-break does not establish a strict premium. <bookmark mark='d'/> The excess is the value of the option to resell."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(thm))
        self.wait(0.5)
        self.clear_scene()

    def example(self, t):
        h = t["hk"]
        hx = [-3.6, 0.0, 2.4, 4.8]
        head = VGroup(label(r"Harrison and Kreps's example, $\beta = 3/4$", font_size=18, color=GREY_B),
                      label(r"state 0", font_size=20), label(r"state 1", font_size=20), label(r"", font_size=20))
        rows = [(r"type 1, buy and hold", h["V1"], T1), (r"type 2, buy and hold", h["V2"], T2),
                (r"the market price", h["P"], PR), (r"speculative premium over the best", h["premium"], GOOD)]
        tab = VGroup(head)
        for name, v, col in rows:
            tab.add(VGroup(label(name, font_size=19, color=col), MathTex(rf"{v[0]:.3f}", font_size=28),
                           MathTex(rf"{v[1]:.3f}", font_size=28), VectorizedPoint()))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.9 - 0.75 * j, 0])
            row[0].align_to(np.array([hx[0] - 2.8, 0, 0]), LEFT)
        hold = MathTex(r"\text{holder: type }" + rf"{int(h['holder'][0]) + 1}" + r"\text{ in state 0, type }"
                       + rf"{int(h['holder'][1]) + 1}" + r"\text{ in state 1}", font_size=26, color=GREY_A).next_to(tab, DOWN,
                                                                                                         buff=0.4)
        foot = wrapped_label(r"dividend 0 or 1; type 1 believes $Q_1 = \begin{pmatrix}1/2 & 1/2\\ 2/3 & 1/3\end{pmatrix}$, type 2 "
                             r"$Q_2 = \begin{pmatrix}2/3 & 1/3\\ 1/4 & 3/4\end{pmatrix}$. The prices are exactly $24/13$ and "
                             r"$27/13$, as in the 1978 paper", 11.6, 16, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Their own example: a dividend of zero or one, two types, a discount factor of three quarters. "
            "<bookmark mark='a'/> Type 1 values the asset at one point three three or one point two two, by state; "
            "type 2 at one point four five or one point nine one. <bookmark mark='b'/> The market price is one point "
            "eight five and two point oh eight, exactly twenty-four and twenty-seven thirteenths: above both types' "
            "valuations, in both states. <bookmark mark='c'/> Type 1 holds in state zero, type 2 in state one, and each "
            "pays for the right to hand the asset to the other when the state turns."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
            vo.wait_until("c")
            self.play(FadeIn(hold))
        self.wait(0.4)
        self.clear_scene()

    def why_more(self):
        rows = [cmath(r"P", r"=", r"\beta Q_{h(s)}(d + P)\ \ \ge\ \ \beta Q_i(d + P)\quad\text{for every } i", font_size=30,
                      colors={r"P": PR}),
                cmath(r"P - V_i", r"\ge", r"\beta Q_i(P - V_i)\ \ \Rightarrow\ \ P - V_i \ge 0", font_size=30,
                      colors={r"P - V_i": GOOD}),
                cmath(r"\text{short sales allowed}", r"\Rightarrow", '\\text{pessimists can supply; price now needs wealth, risk preferences and shorting limits}', font_size=28, colors={r"\text{short sales allowed}": T2})]
        whys = [why(r"the holder in state $s$ is the type $h(s)$ with the highest continuation value"),
                why(r"subtract $V_i = \beta Q_i(d + V_i)$: the gap satisfies a positive linear inequality, and since $\beta Q_i$ "
                    r"is a contraction with nonnegative entries, the gap is nonnegative"),
                why(r"the short-sale constraint is essential: with it, only optimists' views enter the price (Miller 1977); "
                    r"without it, pessimists' do too")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Why must the price be at least every valuation? <bookmark mark='a'/> In each state the holder is the type with the highest continuation value, so the price is at least what any type would pay. <bookmark mark='b'/> Subtract that type's own buy-and-hold equation: the gap satisfies a positive linear inequality, and since the type's discounted transition matrix is a contraction with nonnegative entries, the gap cannot be negative. <bookmark mark='c'/> The short-sale constraint is essential: with it only the optimists' views enter the price, as Edward Miller argued in 1977; allowing pessimists to sell changes supply and the equilibrium problem. With risk-neutral investors and unlimited capital and shorts, an equilibrium may fail to exist; a unique lower price does not follow without additional wealth or risk constraints."
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

    def sweep(self, t):
        rows = t["sweep"]
        lam = np.array([r_["lam"] for r_ in rows])
        bub = np.array([r_["bubble_vs_true"] for r_ in rows])
        prem = np.array([r_["premium"] for r_ in rows])
        g = axes([0, 1.0], [0, 0.6], x_length=8.0, y_length=4.0, xlabel=r"disagreement $\lambda$ (beliefs $\bar Q \pm \lambda\Delta$)",
                 ylabel=r"price above a valuation, stationary average", xticks=[0, 0.25, 0.5, 0.75, 1.0],
                 yticks=[0, 0.2, 0.4, 0.6], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        c1 = curve(ax, lam, bub, PR, stroke_width=3.5)
        c2 = curve(ax, lam, prem, GOOD, stroke_width=3)
        leg = legend([(PR, 'above value under chosen $\\bar Q$ (reference gap)'), (GOOD, r"above the most optimistic buy-and-hold")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        v0 = rows[0]["Vtrue"]
        side = wrapped_label(f"$\\lambda = 1$ is Harrison and Kreps's pair; $\\lambda = 0$, agreement. Value under the chosen reference chain $\\bar Q$ is {np.dot(t['pi'], v0):.2f}; at full disagreement the price is {100 * bub[-1] / np.dot(t['pi'], v0):.0f}\\% above it. Here ownership changes hands every time the state changes, {100 * rows[-1]['turnover']:.0f}\\% of periods", 3.3, 14, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"Now turn disagreement up from zero, keeping the average transition matrix fixed. That matrix is a chosen illustrative reference, not an estimated true probability law, and its buy-and-hold value is not the average of the two nonlinear valuation functions. <bookmark mark='a'/> With agreement there is no bubble. As beliefs spread apart, the price rises above the value under the average belief, almost linearly, to {100 * bub[-1] / np.dot(t['pi'], v0):.0f} percent at Harrison and Kreps's pair. <bookmark mark='b'/> And above even the most optimistic investor's buy-and-hold value: the pure resale premium. This is a fixed numerical model comparison, not a market estimate. Turnover is computed under the chosen reference chain; it does not establish that trading volume rises continuously with disagreement."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(leg[1]), run_time=1.3)
        self.wait(0.4)
        self.clear_scene()

    def sx(self):
        cards = VGroup(
            desk_question(r"overconfidence as the source", r"Scheinkman and Xiong (2003): two groups each overweight their "
                          r"own signal; their disagreement follows a mean-reverting diffusion, and the bubble is a "
                          r"perpetual American option on it, priced in closed form", width=12.4, font_size=19),
            desk_question(r"three predictions", r"the bubble rises with overconfidence and with the volatility of "
                          r"disagreement; it comes with heavy trading, turnover far above fundamentals' needs; and a "
                          r"transaction cost cuts trading a lot and the bubble only a little", width=12.4, font_size=19),
            desk_question(r"the evidence", r"Xiong and Yu (2011): deep out-of-the-money Chinese put warrants that were "
                          r"almost surely worthless traded at substantial prices with enormous turnover, as the theory "
                          r"predicts when short sales are banned", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "José Scheinkman and Wei Xiong gave the idea its modern form in 2003. <bookmark mark='a'/> Two groups each overweight their own signal; their disagreement wanders like a mean-reverting diffusion, and the bubble is a perpetual American option on it, priced in closed form. <bookmark mark='b'/> It predicts that the bubble grows with overconfidence and with the volatility of disagreement, that it comes with very heavy trading, and that a trading cost cuts the trading a lot but the bubble only a little. <bookmark mark='c'/> And Wei Xiong and Jialin Yu reported evidence consistent with the mechanism, not unique identification: Chinese put warrants, almost surely worthless, trading at substantial prices with enormous turnover, in a market without short selling."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: where does disagreement come from?", r"overconfidence, different models, or different "
                          r"information; the bubble's predictions differ, and the data rarely separate them", width=12.4,
                          font_size=18),
            desk_question(r"open: bubbles with limited short sales", r"real markets allow costly, limited shorting; how "
                          r"the premium scales with borrowing fees and recall risk is only partly measured", width=12.4,
                          font_size=18),
            desk_question(r"open: welfare and policy", r"if investors agree to disagree, whose beliefs should judge "
                          r"welfare? Brunnermeier, Simsek and Xiong (2014) proposed a belief-neutral criterion; whether "
                          r"policy should lean against such bubbles is unsettled", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> Where does disagreement come from: overconfidence, different "
            "models, different information? The bubble's predictions differ, and data rarely separate them. "
            "<bookmark mark='b'/> Real markets allow costly, limited shorting, and how the premium scales with "
            "borrowing fees and recall risk is only partly measured. <bookmark mark='c'/> And welfare: if investors "
            "agree to disagree, whose beliefs judge it? Markus Brunnermeier, Alp Simsek and Wei Xiong proposed a "
            "belief-neutral criterion in 2014; whether policy should lean against such bubbles is unsettled."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card('if both types had the same beliefs $Q$, what would the price be? And if type 2 alone could buy, would state-0 price exceed, equal or fall below $16/11 \\approx 1.455$?')
        with self.voiceover(
            'Pause and predict. If both types shared a common transition matrix Q, what would the price be? If only type two could buy, would the state-zero price exceed, equal or fall below sixteen elevenths, about one point four five five?'
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

        answer = VGroup(
            label(r"With common beliefs: $P=\beta Q(d+P)=V_Q$", font_size=28),
            label(r"Only type 2: $P=V_2$; state 0 is exactly $16/11\approx1.455$", font_size=25),
            wrapped_label(r"The answer is equality, not a forced above/below choice. The resale option disappears when only one belief can buy.", 11.6, 21, GREY_A),
        ).arrange(DOWN, buff=0.4)
        with self.voiceover("The answer: under common beliefs, price equals the unique buy-and-hold value for that transition matrix. If only type two can buy, price equals type two's value. In state zero it is exactly sixteen elevenths, about one point four five five, so the answer is equality. There is no option to resell to a different belief type."):
            self.play(FadeIn(answer))
        self.wait(0.5)
        self.clear_scene()
