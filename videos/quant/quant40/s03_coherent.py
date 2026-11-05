from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant40.common import BAD, ES_C, HURDLE, PART, VAR_C, load


class Coherent(VoiceoverScene):
    def construct(self):
        c = load("coherent")
        self.card(c)
        self.bonds(c)
        self.axioms()
        self.var_fails()
        self.es_holds(c)
        self.es_formula()
        self.spectral()
        self.convex()
        self.euler(load("extra"))
        self.which()
        self.question()

    def card(self, c):
        b = c["both"]
        cd = chapter_card(2, r"Coherent risk measures", r"Should the risk of two positions ever exceed the sum of their "
                          r"risks?", part=PART)
        with self.voiceover(
            f"Chapter two, and the answer to the pause: {b['var']:.0f} dollars. The chance that at least one bond "
            f"defaults is {100 * b['p_any']:.2f} percent, more than five, so the portfolio's VaR is a full default, while "
            "each bond alone shows zero. Diversifying made the reported risk appear from nothing."
        ):
            self.play(FadeIn(cd[0], shift=UP * 0.2), FadeIn(cd[1]))
        self.play(FadeOut(cd))

    def bonds(self, c):
        s, b = c["single"], c["both"]
        hx = [-3.4, 0.0, 3.4]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"", r"VaR 95\%", r"ES 95\%")])
        rows = [(r"bond A", s["var"], s["es"]), (r"bond B", s["var"], s["es"]), (r"A + B, as the sum", 2 * s["var"],
                                                                                   2 * s["es"]),
                (r"A + B, held together", b["var"], b["es"])]
        tab = VGroup(head)
        for nm, v, e in rows:
            tab.add(VGroup(label(nm, font_size=20), MathTex(f"{v:.0f}", font_size=30, color=VAR_C),
                           MathTex(f"{e:.1f}", font_size=30, color=ES_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.85 * j, 0])
        with self.voiceover(
            "The numbers. <bookmark mark='a'/> Each bond alone: a VaR of zero, because a default is rarer than one day in "
            f"twenty; an expected shortfall of {s['es']:.0f}. <bookmark mark='b'/> Added up, a VaR of zero. "
            f"<bookmark mark='c'/> Held together, a VaR of {b['var']:.0f}. Expected shortfall goes the other way: "
            f"{b['es']:.1f} together, less than the {2 * s['es']:.0f} of the sum. One measure punishes diversification; "
            "the other rewards it."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]))
            vo.wait_until("c")
            self.play(FadeIn(tab[4]), Indicate(tab[4][1], color=BAD))
        self.wait(0.4)
        self.clear_scene()

    def axioms(self):
        rows = [cmath(r"\rho(L + c)", r"=", r"\rho(L) + c", font_size=40),
                cmath(r"\rho(\lambda L)", r"=", r"\lambda\,\rho(L),\ \lambda \ge 0", font_size=40),
                cmath(r"L_1 \le L_2", r"\Rightarrow", r"\rho(L_1) \le \rho(L_2)", font_size=40),
                cmath(r"\rho(L_1 + L_2)", r"\le", r"\rho(L_1) + \rho(L_2)", font_size=40, colors={r"\le": HURDLE})]
        whys = [why(r"translation invariance: adding a sure loss of $c$ adds $c$ of capital"),
                why(r"positive homogeneity: twice the position, twice the risk"),
                why(r"monotonicity: a position that always loses more is riskier"),
                why(r"subadditivity: merging never creates risk, so a firm's capital is at most the sum of its desks'")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Philippe Artzner, Freddy Delbaen, Jean-Marc Eber and David Heath asked what a risk measure should satisfy, "
            "and called the answer coherence. <bookmark mark='a'/> A sure extra loss adds exactly that much capital. "
            "<bookmark mark='b'/> Twice the position, twice the risk. <bookmark mark='c'/> A position that always loses "
            "more is riskier. <bookmark mark='d'/> And merging never creates risk: the firm's capital is at most the sum "
            "of its desks'."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def var_fails(self):
        cards = VGroup(
            desk_question(r"VaR satisfies three", r"translation, scaling and monotonicity hold for any quantile", width=12.4,
                          font_size=19),
            desk_question(r"and fails the fourth", r"for skewed, discrete or very heavy-tailed losses, as the bonds just "
                          r"showed; for elliptical distributions, normal or $t$, it happens to hold", width=12.4,
                          font_size=19),
            desk_question(r"why it matters", r"a desk can lower its reported VaR by splitting a position, or by selling "
                          r"tail risk just beyond the quantile: the measure rewards hiding risk where it does not look",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "VaR's record. <bookmark mark='a'/> It satisfies the first three: any quantile does. <bookmark mark='b'/> It "
            "fails the fourth for skewed, discrete or very heavy-tailed losses, as the bonds showed; for normal or t "
            "distributions it happens to hold. <bookmark mark='c'/> And the failure matters: a desk can lower its reported "
            "VaR by splitting a position, or by selling risk just beyond the quantile, where the measure does not look."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def es_holds(self, c):
        rows = [cmath(r"\text{ES}_\alpha(L)", r"=", r"\frac{1}{1 - \alpha}\int_\alpha^1 \text{VaR}_u(L)\,du", font_size=40,
                      colors={r"\text{ES}_\alpha(L)": ES_C}),
                cmath(r"", r"=", r"\sup_{Q \in \mathcal Q_\alpha} \mathbb E_Q[L],\quad \frac{dQ}{dP} \le \frac{1}{1 - \alpha}",
                      font_size=36),
                cmath(r"\sup (f + g)", r"\le", r"\sup f + \sup g", font_size=40, colors={r"\le": HURDLE})]
        whys = [why(r"expected shortfall averages the quantiles beyond $\alpha$ (Acerbi and Tasche 2002)"),
                why(r"equivalently, the worst expected loss over every reweighting of the probabilities that inflates "
                    r"no state by more than $1/(1 - \alpha)$"),
                why(r"a supremum of linear functionals is subadditive: so ES is coherent, for every distribution")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Expected shortfall passes. <bookmark mark='a'/> It averages all the quantiles beyond alpha. "
            "<bookmark mark='b'/> Equivalently, it is the worst expected loss over every reweighting of the "
            "probabilities that inflates no state by more than one over one minus alpha: a set of stress scenarios. "
            "<bookmark mark='c'/> And a supremum of expectations is subadditive. So expected shortfall is coherent, for "
            "every distribution."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def es_formula(self):
        rows = [cmath(r"\text{normal}", r":", r"\text{ES}_\alpha = \mu + \sigma\,\frac{\varphi(z_\alpha)}{1 - \alpha}", font_size=38),
                cmath(r"\alpha = 99\%", r":", r"\text{ES} = 2.67\,\sigma,\quad \text{VaR} = 2.33\,\sigma", font_size=38),
                cmath(r"\alpha = 97.5\%", r":", r"\text{ES} = 2.34\,\sigma", font_size=38, colors={r"\alpha = 97.5\%": HURDLE})]
        whys = [why(r"for a normal loss: the mean plus the density at the quantile over the tail probability"),
                why(r"at 99\%, ES is only 15\% above VaR for a normal; for fat tails, much more"),
                why(r"so the 97.5\% ES that Basel's FRTB adopted equals the 99\% VaR for a normal, and exceeds it when the "
                    r"tail is fat (Chapter 9)")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "In numbers. <bookmark mark='a'/> For a normal loss, expected shortfall is the mean plus sigma times the "
            "density at the quantile over the tail probability. <bookmark mark='b'/> At ninety-nine percent, two point "
            "six seven sigma, against VaR's two point three three. <bookmark mark='c'/> And at ninety-seven and a half, "
            "two point three four: the same as the ninety-nine percent VaR for a normal, and larger whenever the tail is "
            "fat. That equivalence is why regulators chose it."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def spectral(self):
        rows = [cmath(r"\rho_\phi(L)", r"=", r"\int_0^1 \phi(u)\,\text{VaR}_u(L)\,du", font_size=42, colors={r"\rho_\phi(L)": ES_C}),
                cmath(r"\phi", r":", r"\text{non-negative, increasing, } \int\phi = 1", font_size=38),
                cmath(r"\text{ES}_\alpha", r":", r"\phi = \tfrac{1}{1 - \alpha}\mathbf 1_{u > \alpha}", font_size=38)]
        whys = [why(r"Acerbi's spectral measures: a weighted average of quantiles, with weights $\phi$"),
                why(r"coherent exactly when the weights rise toward the worst outcomes: a risk-aversion function"),
                why(r"ES puts equal weight on the tail and none elsewhere; VaR, a point mass, is not spectral")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The family behind it. <bookmark mark='a'/> Carlo Acerbi's spectral measures weight every quantile. "
            "<bookmark mark='b'/> They are coherent exactly when the weights rise toward the worst outcomes, a risk "
            "aversion written as a function. <bookmark mark='c'/> Expected shortfall weights the tail equally and ignores "
            "the rest; VaR, a single point, is not in the family at all."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def convex(self):
        rows = [cmath(r"\rho(\lambda L_1 + (1 - \lambda) L_2)", r"\le", r"\lambda\rho(L_1) + (1 - \lambda)\rho(L_2)",
                      font_size=34),
                cmath(r"\rho(L)", r"=", r"\sup_Q\bigl(\mathbb E_Q[L] - \gamma(Q)\bigr)", font_size=38),
                cmath(r"\text{entropic}", r":", r"\tfrac1\theta \log \mathbb E\,e^{\theta L}", font_size=38)]
        whys = [why(r"Föllmer and Schied's convex measures drop positive homogeneity: doubling a position may more than "
                    r"double its risk, which is what illiquidity does"),
                why(r"every such measure is a worst expected loss over scenarios $Q$, each charged a penalty $\gamma(Q)$"),
                why(r"the entropic risk measure, with the relative entropy as the penalty: Part 8's exponential utility")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "And beyond. <bookmark mark='a'/> Hans Föllmer and Alexander Schied relaxed homogeneity to convexity: doubling a "
            "position may more than double its risk, which is what illiquidity does. <bookmark mark='b'/> Every such "
            "measure is a worst expected loss over scenarios, each charged a penalty for implausibility. "
            "<bookmark mark='c'/> With relative entropy as the penalty, it is the entropic risk measure, Part eight's "
            "exponential utility in disguise."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def euler(self, x):
        eu = x["euler"]
        rows = [cmath(r"\text{ES}(w)", r"=", r"\textstyle\sum_i w_i\,\frac{\partial\,\text{ES}}{\partial w_i}", font_size=40,
                      colors={r"\text{ES}(w)": ES_C}),
                cmath(r"w_i\,\frac{\partial\,\text{ES}}{\partial w_i}", r"=", r"-w_i\,\mathbb E[x_i \mid L \ge \text{VaR}]",
                      font_size=38),
                cmath(r"\text{market, SMB, HML}", r":", rf"{100 * eu['share'][0]:.0f}\%,\ {100 * eu['share'][1]:.1f}\%,\ "
                      rf"{100 * eu['share'][2]:.1f}\%", font_size=36, colors={r"\text{market, SMB, HML}": HURDLE}),
                cmath(r"\text{variance shares}", r":", rf"{100 * eu['sd_share'][0]:.0f}\%,\ {100 * eu['sd_share'][1]:.1f}\%,\ "
                      rf"{100 * eu['sd_share'][2]:.1f}\%", font_size=36)]
        whys = [why(r"positive homogeneity gives Euler's theorem: a coherent measure splits exactly into each position's "
                    r"marginal contribution, a capital allocation (Tasche)"),
                why(r"for ES, each position's average loss on the days beyond VaR"),
                why(r"Chapter 6's portfolio, at 97.5\% since 1990: the market carries most of the tail"),
                why(r"value carries more of the tail than of the variance: it falls with the market on the worst days")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Coherence also tells a firm how to split its capital. <bookmark mark='a'/> Positive homogeneity gives "
            "Euler's theorem: the risk is exactly the sum of each position times its marginal risk. "
            "<bookmark mark='b'/> For expected shortfall, each position's average loss on the days beyond VaR. "
            "<bookmark mark='c'/> On a portfolio of the market with tilts to small and value stocks, the market carries "
            f"{100 * eu['share'][0]:.0f} percent of the shortfall. <bookmark mark='d'/> Value carries "
            f"{100 * eu['share'][2]:.1f} percent of the tail against {100 * eu['sd_share'][2]:.1f} percent of the "
            "variance: on the worst days it falls with the market."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def which(self):
        cards = VGroup(
            desk_question(r"VaR", r"easy to explain and to backtest, as Chapter 3 shows; blind beyond its line; not "
                          r"subadditive", width=12.4, font_size=19),
            desk_question(r"expected shortfall", r"coherent and sensitive to the tail, but harder to estimate, and, as "
                          r"the research chapter proves, impossible to backtest on its own", width=12.4, font_size=19),
            desk_question(r"in practice", r"regulators moved trading-book capital to 97.5\% ES in 2016; banks still "
                          r"report and backtest VaR beside it", width=12.4, font_size=19, ),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "So which? <bookmark mark='a'/> VaR is easy to explain and to backtest, blind beyond its line, and not "
            "subadditive. <bookmark mark='b'/> Expected shortfall is coherent and sees the tail, but is harder to "
            "estimate, and, as the research chapter proves, cannot be backtested on its own. <bookmark mark='c'/> "
            "Regulators moved trading-book capital to ninety-seven and a half percent ES in twenty sixteen, and banks "
            "still backtest VaR beside it."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a 99\% VaR model was used for 250 days and exceeded on 7 of them. Is the model wrong? How would "
                       r"you decide, and what else would you look at besides the count?")
        with self.voiceover(
            "Pause and predict. A ninety-nine percent VaR model was used for two hundred and fifty days and exceeded on "
            "seven of them. Is the model wrong? How would you decide, and what would you look at besides the count?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
