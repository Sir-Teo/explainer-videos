from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant40.common import ladder, pause_card, desk_question
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
        self.euler()
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
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(Indicate(tab[1], scale_factor=1.01), FadeIn(tab[2]))
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
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def var_fails(self):
        cards = VGroup(
            desk_question(r"VaR satisfies three", r"translation, scaling and monotonicity hold for any quantile", width=12.4,
                          font_size=19),
            desk_question(r"and fails the fourth", 'for skewed, discrete or very heavy-tailed losses, as the bonds just showed; for jointly elliptical linear losses with finite means and a nonnegative quantile coefficient, it holds', width=12.4,
                          font_size=19),
            desk_question(r"why it matters", r"a desk can lower its reported VaR by splitting a position, or by selling "
                          r"tail risk just beyond the quantile: the measure rewards hiding risk where it does not look",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "VaR satisfies translation, nonnegative scaling and monotonicity. <bookmark mark='a'/> Quantiles preserve those properties. <bookmark mark='b'/> Subadditivity fails in examples such as the independent default bonds. It holds for linear losses from a jointly elliptical family when the scale coefficient is nonnegative and the means exist; merely fitting separate normal or t marginals is insufficient. <bookmark mark='c'/> Splitting a book can then reduce summed reported VaRs without reducing the underlying joint loss distribution."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
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
                why('a supremum of linear functionals is subadditive: so ES is coherent, on integrable losses')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Expected shortfall uses an integrable loss and the integrated-quantile definition. <bookmark mark='a'/> It averages all upper quantiles, splitting any atom at the cutoff. <bookmark mark='b'/> Its dual takes a supremum over probability measures absolutely continuous with respect to the reference measure, with nonnegative density integrating to one and bounded by one over one minus alpha. <bookmark mark='c'/> Each expectation is linear and the same density class applies to both positions, so the supremum is subadditive. Translation, homogeneity and monotonicity follow too."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def es_formula(self):
        rows = [cmath(r"\text{normal}", r":", r"\text{ES}_\alpha = \mu + \sigma\,\frac{\varphi(z_\alpha)}{1 - \alpha}", font_size=38),
                cmath(r"\alpha = 99\%", r":", r"\text{ES} = 2.67\,\sigma,\quad \text{VaR} = 2.33\,\sigma", font_size=38),
                cmath(r"\alpha = 97.5\%", r":", r"\text{ES} = 2.34\,\sigma", font_size=38, colors={r"\alpha = 97.5\%": HURDLE})]
        whys = [why(r"for a normal loss: the mean plus the density at the quantile over the tail probability"),
                why('zero-mean normal coefficient comparison; a different distribution requires its own mean, scale and tail calculation'),
                why("so the 97.5\\% ES that Basel's FRTB adopted is close to, not exactly equal to, zero-mean normal 99\\% VaR; heavier-tail comparisons depend on the distribution")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "For a normal loss, ES is its mean plus sigma times the normal density at the quantile divided by tail probability. <bookmark mark='a'/> At ninety-nine percent the zero-mean coefficient is about two point six six five, versus two point three two six for VaR. <bookmark mark='b'/> At ninety-seven and a half percent the ES coefficient is about two point three three eight. <bookmark mark='c'/> That is close to ninety-nine percent normal VaR, not identical. A universal inequality across different confidence levels does not follow merely from calling a distribution fat tailed."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
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
                if k: vo.wait_until(m_)
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
                why('under the relevant dual-representation and lower-semicontinuity assumptions, use penalized scenario expectations'),
                why(r"the entropic risk measure, with the relative entropy as the penalty: Part 8's exponential utility")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Convex monetary risk measures relax positive homogeneity while retaining monotonicity and cash translation. <bookmark mark='a'/> Convexity rewards mixing; scaling up a position can raise risk more than proportionally. <bookmark mark='b'/> On a specified function space with the appropriate lower-semicontinuity or Fatou property, a dual representation uses scenario expectations minus a penalty. <bookmark mark='c'/> Entropic risk is one example when the exponential moment exists; its penalty is relative entropy divided by risk aversion. These domain and regularity conditions matter."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def euler(self, unused=None):
        head=label('Euler allocation: a chosen Gaussian example',font_size=29).to_edge(UP,buff=0.35)
        cards=VGroup(
            desk_question('differentiability matters','For an integrable linear loss with a smooth unique tail quantile: $\\mathrm{ES}(w)=\\sum_i w_i\\partial_i\\mathrm{ES}(w)$.',width=12.0,font_size=23),
            desk_question('chosen covariance, zero means','$\\Sigma=\\left(\\begin{smallmatrix}1&0.5\\\\0.5&4\\end{smallmatrix}\\right)10^{-4},\\ w=(1,1)$; $\\sigma_P^2=0.0006$.',width=12.0,font_size=23),
            desk_question('contributions from the same model','$w_i(\\Sigma w)_i/(w^\\top\\Sigma w)$ gives 25\\%,75\\% of Gaussian ES. Atoms or nonsmooth books require boundary allocation or subgradients.',width=12.0,font_size=23)
        ).arrange(DOWN,buff=0.28).next_to(head,DOWN,buff=0.35)
        with self.voiceover("Euler allocation requires conditions. Degree-one homogeneity plus differentiability gives risk equal to the sum of position times marginal risk; coherence alone does not guarantee derivatives. <bookmark mark='a'/> In a chosen zero-mean Gaussian two-factor example, use the displayed positive-definite covariance and unit weights. Portfolio variance is nought point nought nought nought six. <bookmark mark='b'/> Marginal ES shares are twenty-five and seventy-five percent, from each weighted covariance divided by portfolio variance. Both contributions use this same chosen book. The omitted historical extra output is not replaced by another fit; atoms and nondifferentiable books need appropriate boundary weights or subgradients.") as vo:
            self.play(FadeIn(head),FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.wait(0.5)
        self.clear_scene()

    def which(self):
        cards = VGroup(
            desk_question(r"VaR", r"easy to explain and to backtest, as Chapter 3 shows; blind beyond its line; not "
                          r"subadditive", width=12.4, font_size=19),
            desk_question(r"expected shortfall", 'coherent and sensitive to the tail, but harder to estimate, and, as the research chapter proves, not elicitable alone on this rich class; calibration tests and joint scoring remain possible', width=12.4, font_size=19),
            desk_question(r"in practice", 'the Basel 2016 standard specified 97.5\\% ES, with later revisions and jurisdiction-specific implementation; banks still report and backtest VaR beside it', width=12.4, font_size=19, ),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Which measure serves which task? <bookmark mark='a'/> VaR is a quantile with direct exception diagnostics, but is not generally subadditive. <bookmark mark='b'/> Integrated-tail ES is coherent for integrable losses and sensitive to severity. Non-elicitability alone means no strictly consistent standalone score on the class considered; it does not rule out backtesting. <bookmark mark='c'/> Basel's twenty-sixteen standard specified ninety-seven-and-a-half percent ES and retained VaR diagnostics. Later revisions and local implementation differ; this is historical methodology, not a current compliance certification."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
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
        self.wait(6.0)
        self.clear_scene()
