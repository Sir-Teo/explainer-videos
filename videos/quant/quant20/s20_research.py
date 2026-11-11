from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, GOOD, HAZ, PART, RISKY, SAFE, load, lesson_cards

EX, ASRF, GA = WHITE, BAD, GOOD


class Research(VoiceoverScene):
    def construct(self):
        t = load("granularity_theory")
        self.card()
        self.exact()
        self.ga()
        self.explicit(t)
        self.plot(t)
        self.table(t)
        self.lumpy(t)
        self.invariance()
        self.open_problems()
        self.question()
        self.answer()

    def card(self):
        c = research_card(r"The granularity adjustment", r"How wrong is Basel's large-pool formula for a portfolio of "
                          r"real size?", part=PART)
        with self.voiceover('For the researcher: the finite portfolio and the granularity approximation. We derive an exact binomial-mixture distribution under the homogeneous conditional-independence model, evaluate it numerically and compare a formal small-noise quantile expansion. The distinction between a discrete quantile and an interpolated CDF is essential; an adjustment is not a universal repair for concentrated books.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def exact(self):
        rows = [cmath(r"p(y)", r"=", r"\Phi\Big(\frac{\Phi^{-1}(\mathrm{PD}) + \sqrt\rho\,y}{\sqrt{1 - \rho}}\Big)", font_size=32,
                      colors={r"p(y)": RISKY}),
                cmath(r"N L \mid y", r"\sim", r"\operatorname{Binomial}\big(N, p(y)\big)", font_size=32,
                      colors={r"N L \mid y": HAZ}),
                cmath(r"\Pr\Big(L \le \tfrac kN\Big)", r"=", r"\int \operatorname{Bin}\big(k; N, p(y)\big)\,\varphi(y)\,dy",
                      font_size=32, colors={r"\Pr\Big(L \le \tfrac kN\Big)": SAFE}),
                cmath(r"N \to \infty:\ \ q_\alpha(L)", r"\to", r"p\big(\Phi^{-1}(\alpha)\big)", font_size=32,
                      colors={r"N \to \infty:\ \ q_\alpha(L)": ASRF})]
        whys = [why(r"Chapter 10: the default probability of every loan, given the common factor $y$ (large $y$ is the bad "
                    r"state), for equal loans with full loss given default"),
                why(r"given the factor, defaults are independent: the number of defaults is binomial"),
                why(r"so the exact distribution of the loss fraction is a one-dimensional integral: no simulation needed"),
                why(r"as the pool grows the binomial concentrates at its mean, and the loss quantile becomes the "
                    r"conditional default rate in the bad state: Vasicek's formula, Basel's ASRF")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.44, edge=6.9)
        with self.voiceover(
            "Take N equal loans with full loss given default, a homogeneous Gaussian one-factor law and increasing bad-state factor y. <bookmark mark='a'/> Conditional default probability is p of y. <bookmark mark='b'/> Conditional independence makes the default count binomial. <bookmark mark='c'/> Integrating its cumulative probability over the factor gives the exact model CDF, a discrete distribution on multiples of one over N. Evaluating the integral still needs numerical error control; the saved example uses a finite factor grid and quadrature. <bookmark mark='d'/> Conditional concentration gives the large-pool distribution. Quantile convergence additionally needs continuity and a uniquely identified limit quantile. The limit concerns default loss under these assumptions, not a complete regulatory capital calculation."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def ga(self):
        rows = [cmath(r"L", r"=", r"\mu(y) + U,\qquad \mu(y) = p(y),\ \ \operatorname{Var}(U \mid y) = \frac{p(1 - p)}{N}",
                      font_size=30, colors={r"L": HAZ}),
                cmath(r"q_\alpha(L)", r"\approx", r"q_\alpha(\mu) - \frac{1}{2\varphi(y)}\frac{d}{dy}\Big[\frac{\varphi(y)\,"
                      r"\operatorname{Var}(U \mid y)}{\mu'(y)}\Big]_{y = \Phi^{-1}(\alpha)}", font_size=28,
                      colors={r"q_\alpha(L)": GA}),
                cmath(r"\mathrm{GA}", r"=", r"\frac{c(\mathrm{PD}, \rho, \alpha)}{N}", font_size=34, colors={r"\mathrm{GA}": GA})]
        whys = [why(r"the loss is the large-pool loss plus idiosyncratic noise whose conditional variance falls like $1/N$"),
                why(r"Gourieroux, Laurent and Scaillet (2000): the second-order expansion of a quantile under a small "
                    r"perturbation; $\varphi$ is the factor's density, $\mu'$ the slope of the conditional loss"),
                why("Gordy's granularity expansion is a formal small-exposure approximation. Equal homogeneous loans give $1/N$ scaling; exposure Herfindahl shortcuts need additional homogeneity conditions")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        thm = theorem_card(r"The granularity adjustment", wrapped_label(
            r"formal smooth-quantile expansion: locally smooth monotone conditional mean, nonzero slope, "
            r"positive density and controlled moments. The discrete quantile has $O(1/N)$ lattice error; "
            r"a few large exposures can invalidate the approximation.", 10.6, 20, GREY_A),
            who=r"Gordy (2003), \textit{J. Financial Intermediation} 12; Martin and Wilde (2002); Gordy and L\"utkebohmert (2013)",
            width=11.6, font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now consider a formal small-noise expansion around a smooth conditional mean. <bookmark mark='a'/> Idiosyncratic loss noise has conditional mean zero and, for equal loans, variance p times one minus p divided by N. <bookmark mark='b'/> A second-order quantile expansion requires a locally smooth mean map with nonzero derivative, positive factor density at the quantile, suitable moment control and a differentiable CDF approximation. <bookmark mark='c'/> It gives a leading correction proportional to one over N for the homogeneous granular case. <bookmark mark='d'/> The raw finite loss is discrete. Its quantile has lattice rounding of order one over N, the same order as the proposed correction; the smooth expansion does not automatically give a smaller remainder for that raw quantile. For unequal exposures, replacing N by an inverse Herfindahl index is a useful homogeneous small-exposure approximation, not a theorem for every portfolio."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.clear_scene()
            thm.move_to(ORIGIN)
            self.play(FadeIn(thm))
        self.wait(0.5)
        self.clear_scene()

    def explicit(self, t):
        rows = [cmath(r"p'(y) = b\,\varphi(z),\ \ p''(y)", r"=", r"-z\,b^2\varphi(z),\qquad z = \frac{\Phi^{-1}(\mathrm{PD}) + "
                      r"\sqrt\rho\,y}{\sqrt{1 - \rho}},\ b = \sqrt{\frac{\rho}{1 - \rho}}", font_size=26,
                      colors={r"p'(y) = b\,\varphi(z),\ \ p''(y)": RISKY}),
                cmath(r"N\cdot\mathrm{GA}", r"=", r"\frac12\Big[\frac{y\,p(1 - p)}{b\,\varphi(z)} - (1 - 2p) - "
                      r"\frac{z\,p(1 - p)}{\varphi(z)}\Big]_{y = \Phi^{-1}(\alpha)}", font_size=30,
                      colors={r"N\cdot\mathrm{GA}": GA})]
        c = t["cases"]["0.01_0.12"]
        whys = [why(r"differentiate Vasicek's conditional default rate: a normal density times the chain rule"),
                why(rf"expand the derivative of $\varphi\,p(1 - p)/p'$ using $\varphi'(y) = -y\varphi(y)$: three terms, all "
                    rf"explicit. At PD 1\%, $\rho = 0.12$, $\alpha = 99.9\%$ the bracket is {c['ga_unit']:.2f}, matching the "
                    r"numerical derivative to four digits")]
        step = ladder(self, rows, whys, keep=2, top=2.3, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            f"For the smooth Vasicek approximation the leading coefficient can be written explicitly. <bookmark mark='a'/> Differentiate the conditional normal probability to obtain its first and second derivatives, with the sign convention that larger y is worse. <bookmark mark='b'/> Expanding the derivative in the correction gives the displayed three-term expression. At one percent PD, point twelve latent correlation and the ninety-nine point nine percent quantile, the saved finite-grid derivative gives coefficient {c['ga_unit']:.3f}. Dividing by one hundred suggests about two percentage points for a hundred equal loans. Numerical agreement checks algebra in this example; it does not validate an error bound, remove lattice effects or justify using the expansion for a large single exposure."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def plot(self, t):
        c = t["cases"]["0.01_0.12"]
        N = np.array([r_["N"] for r_ in c["rows"]], float)
        x = np.log10(N)
        sm = 100 * np.array([r_["smooth"] for r_ in c["rows"]])
        ga = 100 * np.array([r_["asrf_ga"] for r_ in c["rows"]])
        g = axes([1.3, 4.1], [8, 18], x_length=8.0, y_length=4.2, xlabel=r"number of equal loans, $N$",
                 ylabel=r"99.9\% loss quantile, \% of the book", xticks=[np.log10(v) for v in (25, 100, 1000, 10000)],
                 yticks=[8, 10, 12, 14, 16, 18], xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), font_size=15,
                 log_x=True).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        asrf = DashedLine(ax.c2p(1.3, 100 * c["asrf"]), ax.c2p(4.1, 100 * c["asrf"]), color=ASRF, stroke_width=2.5)
        ex = VGroup(curve(ax, x, sm, EX, stroke_width=3), *[Dot(ax.c2p(a_, b_), radius=0.06, color=EX) for a_, b_ in zip(x, sm)])
        gac = VGroup(curve(ax, x, ga, GA, stroke_width=3), *[Dot(ax.c2p(a_, b_), radius=0.05, color=GA) for a_, b_ in zip(x, ga)])
        mc = VGroup(*[Square(side_length=0.16, color=HAZ, stroke_width=2.5).move_to(ax.c2p(np.log10(r_["N"]), 100 * r_["mc"]))
                      for r_ in c["rows"] if r_["mc"] is not None])
        leg = legend([(EX, r"interpolated numerical CDF quantile"), (ASRF, r"large-pool formula (ASRF)"),
                      (GA, r"ASRF + granularity adjustment"), (HAZ, r"Monte Carlo, 400{,}000 scenarios")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"PD 1\%, asset correlation {c['rho']:g}, full loss given default; the numerical CDF quantile "
                             r"interpolated between its steps of $1/N$. full LGD default-loss quantile; not complete regulatory capital",
                             3.3, 14, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        r100 = [r_ for r_ in c["rows"] if r_["N"] == 100][0]
        with self.voiceover(
            f"Here the white curve is the quantile of a linearly interpolated numerical CDF, not the exact lattice-valued loss quantile. <bookmark mark='a'/> The large-pool default-loss fraction is {100 * c['asrf']:.1f} percent. <bookmark mark='b'/> At one hundred loans the displayed interpolated benchmark is {100 * r100['smooth']:.1f} percent. The actual discrete quantile rounds to a support point. Monte Carlo squares use four hundred thousand scenarios, leaving only about four hundred observations beyond a ninety-nine point nine percent threshold. They have tail sampling uncertainty and a lattice of their own. <bookmark mark='c'/> The green first-order correction is reasonably close to this interpolated benchmark for the larger sample sizes shown, but this plot establishes no uniform accuracy guarantee or exact remainder order. Small pools and concentrated exposures need direct validation."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(asrf), FadeIn(leg[1]))
            vo.wait_until("b")
            self.play(FadeIn(ex), FadeIn(leg[0]), FadeIn(mc), FadeIn(leg[3]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(gac), FadeIn(leg[2]), run_time=1.3)
        self.wait(0.4)
        self.clear_scene()

    def table(self, t):
        hx = [-4.4, -2.0, 0.2, 2.4, 4.6]
        head = VGroup(label(r"PD, $\rho$", font_size=18, color=GREY_B), label(r"ASRF", font_size=20, color=ASRF),
                      label(r"interpolated, $N = 100$", font_size=20, color=EX), label(r"interpolated, $N = 1{,}000$", font_size=20, color=EX),
                      label(r"$c$ in $\mathrm{GA} = c/N$", font_size=20, color=GA))
        tab = VGroup(head)
        for key in ("0.01_0.12", "0.01_0.24", "0.03_0.12"):
            c = t["cases"][key]
            r1 = [r_ for r_ in c["rows"] if r_["N"] == 100][0]
            r2 = [r_ for r_ in c["rows"] if r_["N"] == 1000][0]
            tab.add(VGroup(MathTex(rf"{100 * c['pd']:.0f}\%,\ {c['rho']:g}", font_size=24),
                           MathTex(rf"{100 * c['asrf']:.1f}\%", font_size=24),
                           MathTex(rf"{100 * r1['smooth']:.1f}\%", font_size=24),
                           MathTex(rf"{100 * r2['smooth']:.1f}\%", font_size=24),
                           MathTex(rf"{c['ga_unit']:.2f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.5 - 0.75 * j, 0])
        foot = wrapped_label('in these three cases the adjustment is largest relative to the full-loss quantile at low correlation. The stylized IRB formula omits name concentration; broader capital and concentration assessments remain necessary', 11.6, 16,
                             GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "These are three specified model portfolios. <bookmark mark='a'/> In these cases the formal adjustment is largest relative to the full-loss quantile when common-factor correlation is low. This is an approximation under small-exposure and regularity conditions, not a universal ordering of capital requirements. <bookmark mark='b'/> The stylized internal-ratings formula omits name concentration. Concentration needs separate assessment within the applicable supervisory and capital framework; this comparison is not a complete description of current bank rules."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def lumpy(self, t):
        lp = t["lumpy"]
        rows = [(r"loans in the book", rf"{lp['n']}"),
                (r"largest exposure, share of the book", rf"{100 * lp['largest']:.1f}\%"),
                (r"effective number, $1/\sum_i w_i^2$", rf"{lp['n_eff']:.0f}"),
                (r"large-pool formula (ASRF)", rf"{100 * lp['asrf']:.1f}\%"),
                (r"500 equal loans, interpolated CDF", rf"{100 * lp['q_equal500']:.1f}\%"),
                (r"homogeneous GA using $1/\mathrm{HHI}$ (heuristic)", rf"{100 * lp['asrf_ga']:.1f}\%"),
                (r"this book, Monte Carlo (400{,}000 scenarios)", rf"{100 * lp['q_mc']:.1f}\%")]
        tab = VGroup()
        for j, (a_, v) in enumerate(rows):
            col = BAD if j == 6 else GA if j == 5 else ASRF if j == 3 else WHITE
            r_ = VGroup(label(a_, font_size=19, color=GREY_A), MathTex(v, font_size=28, color=col))
            r_[0].move_to([-1.6, 2.2 - 0.6 * j, 0]).align_to(np.array([-6.4, 0, 0]), LEFT)
            r_[1].move_to([5.0, 2.2 - 0.6 * j, 0])
            tab.add(r_)
        foot = wrapped_label(r"500 loans with exposures proportional to $1/k$ for the $k$-th largest (a Zipf book), PD 1\%, "
                             r"$\rho = 0.12$; 99.9\% quantiles of the loss as a share of the book", 11.6, 16,
                             GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"Take five hundred loans with exposures proportional to one over rank. <bookmark mark='a'/> The largest is {100 * lp['largest']:.1f} percent of the book. The inverse exposure Herfindahl index is {lp['n_eff']:.1f}, a concentration statistic, not an exact distributional equivalent to that many equal loans. <bookmark mark='b'/> The large-pool value is {100 * lp['asrf']:.1f} percent; this fixed Monte Carlo estimates a quantile of {100 * lp['q_mc']:.1f} percent, with sampling uncertainty. Substituting the effective size in the homogeneous correction gives {100 * lp['asrf_ga']:.1f} percent. Its noticeable shortfall is a warning: a nearly fifteen-percent exposure violates the spirit of a small-exposure expansion. Direct conditional simulation, quadrature or another validated method is needed for a reliable concentrated-book tail."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[3:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def invariance(self):
        rows = [cmath(r"K_{\text{book}}", r"=", r"\sum_i w_i\,K(\mathrm{PD}_i, \rho_i)", font_size=34,
                      colors={r"K_{\text{book}}": ASRF}),
                cmath(r"K_{\text{book}}", r"=", r"\sum_i w_i\,K(\mathrm{PD}_i, \rho_i) + \mathrm{GA}\big(\{w_i\}\big)",
                      font_size=34, colors={r"K_{\text{book}}": GA})]
        whys = [why(r"portfolio invariance: in the large-pool limit, each loan's capital depends only on its own PD and "
                    r"correlation, so a bank's capital is a sum over loans. Gordy (2003) studies this under the "
                    r"asymptotic single-factor setting and its regularity conditions"),
                why(r"granularity breaks it: the add-on depends on the whole book's concentration, so it cannot be "
                    r"computed loan by loan, the displayed first-pillar formula needs additional concentration assessment")]
        step = ladder(self, rows, whys, keep=2, top=2.2, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Why use a granular single-factor limit? <bookmark mark='a'/> Under the asymptotic single-risk-factor framework and its regularity conditions, each loan's marginal capital contribution can depend on its own risk characteristics and a common factor quantile, rather than the rest of a particular portfolio. Gordy's portfolio-invariance result explains the appeal of that structure. It is not a theorem that every conceivable additive risk model must have exactly these assumptions. <bookmark mark='b'/> Finite-name concentration introduces portfolio-dependent terms, and multiple factors can introduce sector composition effects. The stylized first-pillar formula does not fully cover these risks; supervisors and internal capital assessments require broader concentration analysis. Numerical quantiles, expected-loss subtraction and regulatory adjustments must also be kept distinct."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: many factors", r"with sector and country factors the analytic adjustment needs the "
                          r"multifactor conditional moments; Pykhtin's and saddlepoint methods exist, accuracy guarantees "
                          r"in the far tail are partial", width=12.4, font_size=18),
            desk_question(r"open: small and lumpy books", 'a small or concentrated book can make the expansion inaccurate. Direct finite-pool methods need tail error control; there is no universal failure threshold at 25 loans', width=12.4,
                          font_size=18),
            desk_question(r"open: estimation risk in the inputs", r"$\rho$ and PD are estimated from short histories "
                          r"parameter uncertainty can materially move tail quantiles; its relative size "
                          r"must be assessed, not assumed", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three extensions and limitations. <bookmark mark='a'/> Multifactor portfolios require methods that preserve sector and country dependence; several approximations and numerical methods exist, with accuracy depending on the portfolio and tail region. <bookmark mark='b'/> A few large exposures can invalidate the granular expansion. Exact discrete methods, conditional integration, simulation and importance sampling offer alternatives, each with its own computational and error-control requirements. <bookmark mark='c'/> PD, dependence and recovery are themselves uncertain. Their contribution can exceed or fall below granularity depending on the case; we have not estimated their uncertainty from the unavailable filing count. Compare explicit parameter stresses and confidence assessments instead of asserting that one source of uncertainty is always largest."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a book has 400 loans: one is 50\% of the book, the other 399 share the rest equally. What is its "
                       r"effective $N$ (the inverse Herfindahl index), and what does that say?")
        with self.voiceover(
            "Pause and predict. A book has four hundred loans, but one of them is half the book and the other three "
            "hundred and ninety-nine share the rest equally. "
            "What is its effective number of loans, the inverse Herfindahl index, and what does that say about its "
            "capital?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def answer(self):
        title, cards = lesson_cards('Answer: 400 names can hide one dominant exposure', [
            ('Exposure Herfindahl', '$H=(1/2)^2+399(1/798)^2=0.25+0.25/399$'),
            ('Effective number', '$N_{eff}=1/H=3.99$ approximately; it measures concentration, not a full loss distribution'),
            ('Granularity condition fails', 'The largest exposure is 50\\%; it does not behave like many vanishing small names'),
            ('Implication', 'At PD 1\\% and full LGD, that name alone implies a 99.9\\% loss quantile of at least 50\\%'),
        ])
        with self.voiceover("The exposure Herfindahl is one quarter plus one quarter divided by three hundred ninety-nine. Its inverse is about three point nine nine. <bookmark mark='a'/> That does not turn the book into four equal loans. One name is half the book, so a small-exposure granularity assumption fails. The number of legal names disguises the concentration. <bookmark mark='b'/> Under the chapter's one percent marginal PD and full loss given default, the large name alone produces a loss of at least half the book with one percent probability. Therefore the ninety-nine point nine percent loss quantile is at least fifty percent, without knowing the other names' dependence. If the PD, loss given default or horizon changes, that numerical conclusion must be rechecked. The effective count alone never determines capital.") as vo:
            self.play(FadeIn(title), FadeIn(cards[0]))
            vo.wait_until('a'); self.play(FadeIn(cards[1]))
            vo.wait_until('b'); self.play(FadeIn(cards[2]))
            if len(cards) > 3: self.play(FadeIn(cards[3]))
        self.wait(0.5)
        self.clear_scene()
