from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import BAD, GOOD, PART, RP_C, fit_right
from videos.quant.quant32.illustrations import covariance_case, group_euler_case


class RiskParity(VoiceoverScene):
    def construct(self):
        self.card()
        self.capital()
        self.weights()
        self.groups(group_euler_case())
        self.scale()
        self.correlation()
        self.financing()
        self.duration_example()
        self.firm()
        self.regimes()
        self.question()

    def card(self):
        c = chapter_card(4, r"Risk parity and correlation", r"What risk is balanced, under which covariance?", part=PART)
        with self.voiceover(
            "Chapter four. Part thirty introduced risk budgeting. Across asset classes the question remains: "
            "which contributions are balanced, using which covariance forecast? Capital weights, standalone "
            "budgets and covariance-aware Euler contributions differ. We will calculate those distinctions "
            "on chosen inputs before discussing leverage."
        ):
            self.play(FadeIn(c[0]), FadeIn(c[1]))
        self.play(FadeOut(c))

    def capital(self):
        a = covariance_case()
        w, cov = a["sixty_forty"], a["covariance"]
        fraction = w * (cov @ w) / (w @ cov @ w)
        rows = VGroup(
            MathTex(r"\sigma=(20\%,10\%),\quad \rho=-0.2,\quad w=(0.6,0.4)", font_size=34),
            MathTex(rf"\sigma_p={100 * a['balanced_risk']:.2f}\%", font_size=40),
            MathTex(rf"\text{{Euler fractions}}=({100 * fraction[0]:.1f}\%,{100 * fraction[1]:.1f}\%)", font_size=34),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"chosen annual covariance and fully invested long weights; no observed stock-bond portfolio",
                             12.2, 18, GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Choose two assets with annual standard deviations twenty and ten percent, correlation minus "
            "one fifth, and capital weights sixty and forty percent. "
            f"<bookmark mark='a'/> Portfolio volatility is {100 * a['balanced_risk']:.2f} percent. "
            f"<bookmark mark='b'/> Its Euler variance fractions are {100 * fraction[0]:.1f} and "
            f"{100 * fraction[1]:.1f} percent. The proportional volatility contributions have the same "
            "fractions. Sixty percent of the dollars is not sixty percent of the risk. The concentration "
            "depends on covariance, so a universal ninety-four-percent equity-risk figure does not follow "
            "from the label sixty-forty."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def weights(self):
        a = covariance_case()
        rows = VGroup(
            MathTex(r"w_i\propto1/\sigma_i\quad\Longrightarrow\quad w=(1/3,2/3)", font_size=36),
            MathTex(r"w_1\sigma_1=w_2\sigma_2", font_size=38),
            MathTex(rf"\sigma_p={100 * a['base_risk']:.2f}\%,\qquad \text{{Euler fractions}}=(50\%,50\%)",
                    font_size=32),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"two-asset special case, long weights, positive SDs and nonzero portfolio risk; "
                             r"not a general multi-asset ERC solution", 12.2, 18,
                             GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Inverse-volatility weights give one third to the twenty-percent asset and two thirds to "
            "the ten-percent asset. Weighted standalone volatilities are equal. "
            "<bookmark mark='a'/> For exactly two long assets, cross-covariance enters both Euler "
            "contributions symmetrically. Equal standalone budgets therefore also equalise Euler "
            "fractions, provided portfolio risk is nonzero. "
            f"<bookmark mark='b'/> The chosen base risk is {100 * a['base_risk']:.2f} percent. "
            "This special identity does not make inverse volatility a general equal-risk-contribution "
            "solution for three or more assets. Equal risk does not itself specify expected returns "
            "or establish an investment premium."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def groups(self, a):
        matrix = MathTex(r"C=\begin{pmatrix}1&0.8&0\\0.8&1&0.1\\0&0.1&1\end{pmatrix}",
                         font_size=35).shift(UP * 1.5)
        assumption = label(r"three chosen groups: SD 10\% each, weights 1/3 each", font_size=26)
        fractions = MathTex(rf"\text{{Euler fractions}}=({100 * a['Euler_fraction'][0]:.2f}\%,"
                            rf"{100 * a['Euler_fraction'][1]:.2f}\%,{100 * a['Euler_fraction'][2]:.2f}\%)",
                            font_size=32).shift(DOWN * 1.3)
        foot = wrapped_label(r"fixed positive-definite correlation matrix; equal standalone budgets do not equalise "
                             r"covariance-aware contributions", 12.2, 18,
                             GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(matrix), FadeIn(assumption), FadeIn(foot))
        with self.voiceover(
            "Choose three groups with ten percent volatility and one third of capital each. Their "
            "correlation matrix is positive definite: A and B correlate at point eight, B and C "
            "at point one, and A and C at zero. "
            "<bookmark mark='a'/> Standalone budgets are equal, but Euler fractions are "
            f"{100 * a['Euler_fraction'][0]:.2f}, {100 * a['Euler_fraction'][1]:.2f} and "
            f"{100 * a['Euler_fraction'][2]:.2f} percent. Shared covariance changes the contributions. "
            "<bookmark mark='b'/> The House's hierarchical rule uses inverse-volatility weights within "
            "groups, then inverse group standalone volatility, followed by overall risk scaling. "
            "It does not solve the general equal group Euler-risk equations. That difference belongs "
            "in the model's definition, rather than being explained away by a return comparison."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(fractions))
            vo.wait_until("b")
            self.wait(0.2)
        self.clear_scene()

    def scale(self):
        a = covariance_case()
        rows = VGroup(
            MathTex(r"\sigma^*=10\%,\qquad L=\min\left(\frac{\sigma^*}{\hat\sigma_p},4\right)", font_size=38),
            MathTex(rf"\hat\sigma_p={100 * a['base_risk']:.2f}\%\quad\Longrightarrow\quad L={a['leverage']:.3f}",
                    font_size=36),
            label(r"fixed covariance: a common scale preserves Euler risk fractions", font_size=26, color=RP_C),
        ).arrange(DOWN, buff=0.7)
        foot = wrapped_label(r"chosen fully invested long base; gross leverage cap 4; future risk and financing "
                             r"remain separate", 12.2, 18, GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Risk scaling is a second step. For a fully invested long base portfolio, multiply weights "
            "by target over forecast volatility, subject to a chosen gross cap of four. "
            f"<bookmark mark='a'/> Base risk {100 * a['base_risk']:.2f} percent gives leverage "
            f"{a['leverage']:.3f} for a ten percent target. "
            "<bookmark mark='b'/> At fixed covariance, the common scale changes contributions "
            "proportionally and preserves their fractions. It cannot turn unequal fractions into "
            "equal ones. A different covariance forecast or binding limit changes the calculation. "
            "Very low estimated risk can imply extreme leverage, motivating a cap alongside "
            "independent liquidity and financing constraints."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def correlation(self):
        a, b = covariance_case(), covariance_case(0.6)
        rho = np.linspace(-0.9, 0.9, 121)
        w = a["target_weights"]
        risk = np.sqrt((w[0] * 0.2) ** 2 + (w[1] * 0.1) ** 2
                       + 2 * w[0] * w[1] * 0.2 * 0.1 * rho)
        changed = float(np.sqrt(w @ b["covariance"] @ w))
        g = axes([-1, 1], [0, 17], x_length=8.2, y_length=4.2,
                 xlabel=r"chosen correlation $\rho$", ylabel=r"fixed-weights annual SD, \%",
                 xticks=[-0.9, -0.2, 0.6, 0.9], yticks=[0, 10, 15], font_size=16).move_to(LEFT * 1.3)
        line = curve(g.ax, rho, 100 * risk, RP_C, stroke_width=3)
        point = Dot(g.ax.c2p(0.6, 100 * changed), color=BAD, radius=0.08)
        text = wrapped_label(rf"same positions: $\rho=-0.2$ gives $10\%$; $\rho=0.6$ gives "
                             rf"{100 * changed:.2f}\%", 3.3, 22, BAD).to_edge(RIGHT, buff=0.35)
        fit_right(text)
        foot = wrapped_label(r"chosen covariance stress; SDs and old positions fixed; no historical correlation "
                             r"estimate or strategy outcome", 12.2, 18,
                             GREY_A).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(g), Create(line), FadeIn(foot))
        with self.voiceover(
            "Hold those positions fixed and vary only correlation. Every point is a chosen covariance "
            "calculation, with both standalone volatilities unchanged. "
            "<bookmark mark='a'/> The old weights had ten percent risk at correlation minus point two. "
            f"At plus point six, the same positions have {100 * changed:.2f} percent risk. "
            "<bookmark mark='b'/> Re-estimation and rebalancing may change desired exposure later, "
            "but cannot change positions already held during a shock. Risk parity does not require "
            "permanently negative correlation to be defined. Forecasts, stress assumptions and "
            "limits still matter; one scenario cannot establish protection in every regime."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(point), FadeIn(text))
            vo.wait_until("b")
            self.wait(0.2)
        self.clear_scene()

    def financing(self):
        rows = VGroup(
            MathTex(r"\mu_L=L\mu-(L-1)s,\qquad \sigma_L=L\sigma,\quad L\geq1", font_size=33),
            MathTex(r"S_L=\frac{\mu}{\sigma}-\frac{L-1}{L}\frac{s}{\sigma}", font_size=38),
            MathTex(r"L=2,\ \mu=3\%,\ \sigma=5\%,\ s=0.5\%:\quad S_L=0.55", font_size=30),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"chosen one-period excess-return model; extra spread on borrowing above initial "
                             r"capital; no default, other fees or dynamic rebalancing", 12.2, 18,
                             GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "A gross Sharpe is preserved by leverage only in a costless linear scaling convention. "
            "Choose base expected excess return mu and volatility sigma, and leverage at least one. "
            "Charge spread s on borrowing above initial capital. "
            "<bookmark mark='a'/> Mean is L mu minus L minus one times s, while volatility is L sigma. "
            "The ratio loses the borrowing-spread term shown here. "
            "<bookmark mark='b'/> At leverage two, base expected excess return three percent, volatility "
            "five percent and half-percent spread, the gross ratio point six becomes point five five. "
            "This fixed arithmetic omits other fees, default and dynamic trading. Actual collateral "
            "and financing agreements require their own cash-flow specification."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def duration_example(self):
        rows = VGroup(
            MathTex(r"r_{\rm bond}\approx y/252-D_{\rm mod}\Delta y", font_size=38),
            MathTex(r"y=3\%,\quad D_{\rm mod}=8,\quad \Delta y=0.005", font_size=36),
            MathTex(r"r_{\rm bond}\approx0.03/252-8(0.005)\approx-3.99\%", font_size=34),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"chosen one-day first-order duration/carry approximation; decimal yield change; "
                             r"omits convexity, coupon timing and roll", 12.2, 18,
                             GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "A bond label does not remove price risk. A first-order approximation combines carry "
            "with modified duration times the negative yield change. "
            "<bookmark mark='a'/> Choose yield three percent, modified duration eight years, and "
            "a one-day yield rise of half a percentage point, written as point zero zero five. "
            "<bookmark mark='b'/> Carry is about three percent over two hundred fifty-two, and "
            "the duration term minus four percent, giving about minus three point nine nine percent. "
            "Convexity, coupon timing and rolling exposures are omitted. This local chosen calculation "
            "is not a Treasury-index reconstruction or a promise that bonds offset equity losses."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def firm(self):
        c = firm_card(r"All Weather", r"Bridgewater describes its approach through growth and inflation "
                      r"environments. The House's simplified hierarchical rule does not reconstruct "
                      r"its holdings, constraints or investment results.",
                      source=r"Bridgewater, The All Weather Story", width=11.8, font_size=22)
        self.play(FadeIn(c))
        with self.voiceover(
            "Bridgewater describes All Weather through growth and inflation environments and dates "
            "its launch to 1996. That firm history differs from our simplified allocation rule. "
            "Actual holdings, instruments, hedges and constraints are not reconstructed here. "
            "An institutional idea can motivate questions about exposures without making a simple "
            "inverse-volatility illustration an empirical replica or identifying the cause of "
            "a particular fund return."
        ):
            self.wait(0.2)
        self.clear_scene()

    def regimes(self):
        cards = VGroup(
            desk_question(r"growth news", r"cash-flow and discount-rate channels affect equities and bonds "
                          r"differently; responses depend on what news changes", width=12.2, font_size=20),
            desk_question(r"inflation news", r"nominal cash flows, policy expectations and real activity can "
                          r"move together; bond-equity covariance is not fixed", width=12.2, font_size=20),
            desk_question(r"design", r"hypothesised regime exposures need instruments, estimated sensitivities "
                          r"and stress limits, not just quadrant labels", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "Growth news can affect cash flows and discount rates differently. Inflation news can "
            "change nominal purchasing power, expected policy and real activity together. "
            "<bookmark mark='a'/> Campbell, Sunderam and Viceira analyse links between nominal-bond "
            "risk and inflation news. Such mechanisms depend on model and period; a quadrant "
            "label does not fix the sign of every asset's return. "
            "<bookmark mark='b'/> Spanning several environments still needs specified instruments, "
            "measured sensitivities, financing and stress limits. Nominal bonds, inflation-linked "
            "bonds and commodities carry distinct risks. Equalising one forecast budget does not "
            "guarantee equal protection against every shock."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def question(self):
        panel = VGroup(
            MathTex('w=(1/3,2/3),\\quad L=2.5', font_size=34),
            MathTex('r=(-20\\%,-10\\%),\\quad r_f=0', font_size=34),
            MathTex('r_p=Lw^\\top r+(1-L)r_f', font_size=34),
        ).arrange(DOWN, buff=0.6).shift(UP * 0.3)
        self.play(FadeIn(panel))
        q = pause_card(r"Chosen risky weights $(1/3,2/3)$, leverage $2.5$, returns $(-20\%,-10\%)$, "
                       r"zero cash rate and costs: what is the one-period portfolio return?")
        with self.voiceover(
            "Pause and predict. Use risky weights one third and two thirds, multiplied by leverage "
            "two point five, and choose one-period returns minus twenty and minus ten percent. "
            "Cash rate and costs are zero. What is the portfolio return? Explain why saying only "
            "mostly bonds would not have supplied enough information."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
