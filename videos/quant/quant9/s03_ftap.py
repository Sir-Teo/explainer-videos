from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import arbitrage as A
from videos.quant.quant9.common import ALT, ARB, CALL, FWD, PART, Q_C


class FTAP(VoiceoverScene):
    def construct(self):
        self.card()
        self.cone()
        self.state_prices()

    def card(self):
        c = chapter_card(2, r"The fundamental theorem, in one period", r"Why must a price lie inside a cone?",
                         lit=(1979,), part=PART)
        with self.voiceover("Chapter two. The fundamental theorem of asset pricing, in one period."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def cone(self):
        S = np.array([80.0, 100.0, 125.0])
        D = np.vstack([np.ones(3), S])
        g = axes([0, 1.4], [0, 150], x_length=5.6, y_length=5.0, xlabel=r"pays in bonds", ylabel=r"the stock pays", xticks=[0, 0.5, 1.0], yticks=[0, 50, 100, 150], font_size=17)
        g.to_edge(LEFT, buff=0.9).shift(DOWN * 0.2)
        ax = g.ax
        o = ax.c2p(0, 0)
        cone = Polygon(o, ax.c2p(1.4, 80 * 1.4), ax.c2p(150 / 125, 150), stroke_width=0, fill_color=Q_C,
                       fill_opacity=0.18)
        arrows = VGroup(*[Arrow(o, ax.c2p(1, s), buff=0, color=FWD, stroke_width=4, max_tip_length_to_length_ratio=0.06)
                          for s in S])
        slabs = VGroup(*[label(rf"state {i + 1}: stock {s:.0f}", font_size=18, color=FWD).next_to(ax.c2p(1, s), RIGHT,
                                                                                                 buff=0.1)
                         for i, s in enumerate(S)])
        p_ok = Dot(ax.c2p(1, 100), radius=0.09, color=CALL)
        ok_l = label(r"price: 100", font_size=19, color=CALL).next_to(p_ok, LEFT, buff=0.35).shift(DOWN * 0.15)
        bad = A.ftap(D, [1.0, 130.0])
        th = bad["theta"]
        p_bad = Dot(ax.c2p(1, 130), radius=0.09, color=ARB)
        bad_l = label(r"price: 130", font_size=19, color=ARB).next_to(p_bad, LEFT, buff=0.35).shift(UP * 0.1)
        # a strictly separating line through the origin, between the cone's upper edge (slope 125) and the price
        # (slope 130); the LP's portfolio is its normal, up to scale
        slope = 127.5
        sep = Line(o, ax.c2p(150 / slope, 150), color=ARB, stroke_width=4)
        sep_l = label(r"separating hyperplane", font_size=18, color=ARB).next_to(ax.c2p(150 / slope, 150), RIGHT,
                                                                                buff=0.1)
        side = VGroup(
            MathTex(r"p = \sum_j \psi_j\, d_j,\quad \psi_j > 0", font_size=34, color=Q_C),
            wrapped_label(r"no arbitrage $\iff$ the price vector lies inside the cone spanned by the states' payoff "
                          r"vectors (Farkas 1902; Harrison and Kreps 1979)", 4.6, 21, GREY_A),
            wrapped_label(r"outside it, a hyperplane separates the price from every payoff: its normal is a portfolio "
                          r"with negative cost and non-negative payoff in every state", 4.6, 21, ARB),
            MathTex(rf"\theta = ({th[0]:+.2f}\ \text{{bonds}},\ {th[1]:+.4f}\ \text{{stock}})", font_size=28,
                    color=ARB),
            MathTex(rf"\text{{cost }} {bad['cost']:+.3f},\ \text{{payoffs }} " + ",\\ ".join(f"{abs(v) if abs(v) < 5e-3 else v:.2f}"
                                                                                         for v in bad["payoff"]),
                    font_size=26, color=ARB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Here is the whole theorem in one picture. One period, three possible states tomorrow, two assets: a "
            "bond that pays one in every state, and a stock that pays eighty, a hundred or a hundred and twenty-five. "
            "Each state is an arrow: what the two assets pay in it. <bookmark mark='a'/> Any combination of the "
            "arrows with positive weights lies in this cone. If today's prices are inside it, they can be written as "
            "a positive sum of the states' payoffs, and the weights are prices of a dollar in each state. "
            "<bookmark mark='b'/> Now price the stock at a hundred and thirty, more than it can ever pay. The price "
            "is outside the cone, and then, by a theorem of Gyula Farkas from 1902, there is a line that separates "
            "it from every arrow. <bookmark mark='c'/> The line's normal is a portfolio: here, short the stock and "
            "hold bonds. It costs less than nothing today and pays at least zero in every state: an arbitrage. "
            "Michael Harrison and David Kreps put it this way in 1979: no arbitrage, if and only if positive state "
            "prices exist. The House's checker finds one or the other by linear programming."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), FadeIn(slabs),
                      run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(cone), FadeIn(p_ok), FadeIn(ok_l), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(p_bad), FadeIn(bad_l), Create(sep), FadeIn(sep_l))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def state_prices(self):
        rows = [cmath(r"p", r"=", r"\sum_j \psi_j\, d_j", font_size=38, colors={r"p": FWD}),
                cmath(r"p", r"=", r"\mathbb{E}^P\!\left[m\, d\right],\qquad m_j = \psi_j / \pi_j", font_size=36,
                      colors={r"m_j = \psi_j / \pi_j": ALT}),
                cmath(r"p", r"=", r"\frac{1}{1 + r}\,\mathbb{E}^Q[d],\qquad Q_j = (1 + r)\,\psi_j", font_size=36,
                      colors={r"Q_j = (1 + r)\,\psi_j": Q_C})]
        whys = [why(r"state prices: the price of one dollar paid only in state $j$ (Arrow 1964; Debreu 1959)"),
                why(r"divide by the real probabilities $\pi_j$: the stochastic discount factor, high in bad states "
                    r"(Part 23 builds asset pricing on it)"),
                why(r"rescale to sum to one: the risk-neutral measure $Q$; prices are discounted expectations under $Q$ "
                    r"(Ross 1978). $Q$ is not a forecast; it is $P$ reweighted by $m$")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-0.8, buff=0.8, edge=6.9)
        with self.voiceover(
            "The weights deserve names. A state price is the price today of a dollar paid only in one state, the "
            "Arrow-Debreu security. <bookmark mark='a'/> Divide each by the state's real probability, and you get "
            "the stochastic discount factor: prices are expectations of payoffs times this factor, which is large in "
            "the states people fear. Part twenty-three builds all of asset pricing on it. <bookmark mark='b'/> Or "
            "rescale the state prices to sum to one. They become a probability measure, Q, the risk-neutral measure, "
            "and every price is the discounted expectation of its payoff under Q. Stephen Ross wrote this down in "
            "1978. Q is not anyone's forecast. It is the real probability, reweighted by the discount factor: the "
            "states people fear count more."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()
