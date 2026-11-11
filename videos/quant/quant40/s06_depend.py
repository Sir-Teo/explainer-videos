from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.quant import *  # noqa: F403
from videos.quant.quant40.common import ladder, pause_card, desk_question
from videos.quant.quant40.common import (
    BAD,
    DATA_C,
    MODEL_C,
    PART,
    TAIL_C,
    load,
)


class Depend(VoiceoverScene):
    def construct(self):
        d = load("depend")
        self.card(d)
        self.pitfalls()
        self.sklar()
        self.scatter()
        self.lambda_()
        self.table(d)
        self.copula_var()
        self.conditional(d)
        self.li()
        self.lessons()
        self.question()

    def card(self, d):
        p = d["pairs"][0]
        c = chapter_card(5, r"Dependence and copulas", r"What does correlation miss when everything falls together?",
                         part=PART)
        with self.voiceover(
            f"Chapter five, and the answer to the pause: {100 * p['emp']['0.01']:.0f} percent. On banks' worst days, "
            f"insurers had their own worst day {100 * p['emp']['0.01']:.0f} percent of the time, where a Gaussian model "
            f"with the same correlation says {100 * p['gauss']['0.01']:.0f}. The model gets the average relationship right "
            "and the crashes wrong."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def pitfalls(self):
        cards = VGroup(
            desk_question(r"correlation is not dependence", r"zero correlation does not mean independence: $X$ and $X^2$ are "
                          r"uncorrelated for a symmetric $X$", width=12.4, font_size=19),
            desk_question(r"not every correlation is possible", r"for lognormal marginals with very different "
                          r"volatilities, the attainable correlations form a narrow interval, far inside $[-1, 1]$",
                          width=12.4, font_size=19),
            desk_question(r"correlation does not fix the tail", r"two models with the same marginals and the same "
                          r"correlation can have very different chances of joint crashes", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label(r"Embrechts, McNeil and Straumann: pitfalls of correlation", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Paul Embrechts, Alexander McNeil and Daniel Straumann's pitfalls of correlation. <bookmark mark='a'/> Zero "
            "correlation is not independence. <bookmark mark='b'/> Not every correlation is possible: for lognormal "
            "marginals with very different volatilities, the attainable range is narrow. <bookmark mark='c'/> And "
            "correlation does not fix the tail: the same marginals and the same correlation can give very different "
            "chances of crashing together."
        ) as vo:
            self.play(FadeIn(head))
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def sklar(self):
        rows = [cmath(r"F(x, y)", r"=", r"C\bigl(F_X(x), F_Y(y)\bigr)", font_size=44, colors={r"C": TAIL_C}),
                cmath(r"C", r":", r"[0, 1]^2 \to [0, 1],\ \text{uniform marginals}", font_size=38),
                cmath(r"\text{Gaussian}", r":", r"C = \Phi_\rho(\Phi^{-1}(u), \Phi^{-1}(v))", font_size=38, colors={r"\text{Gaussian}": MODEL_C}),
                cmath(r"\text{Student } t", r":", r"C = t_{\rho,\nu}(t_\nu^{-1}(u), t_\nu^{-1}(v))", font_size=38,
                      colors={r"\text{Student } t": TAIL_C})]
        whys = [why(r"Sklar (1959): any joint distribution is its marginals glued by a copula"),
                why(r"the copula is the dependence, with the marginals stripped away"),
                why(r"the Gaussian copula of Part 20's credit models, made famous by Li (2000)"),
                why('the t copula with the same latent correlation parameter; transformed Pearson correlations need not match')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Separate the two. <bookmark mark='a'/> Abe Sklar's theorem: any joint distribution is its marginals glued "
            "together by a copula. <bookmark mark='b'/> The copula is the dependence with the marginals removed. "
            "<bookmark mark='c'/> The Gaussian copula, Part twenty's credit model. <bookmark mark='d'/> And the Student t "
            "copula, with the same correlation parameter but a tendency to produce extremes together."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def scatter(self):
        rng = np.random.default_rng(5)
        rho, n = 0.7, 900
        L = np.linalg.cholesky([[1, rho], [rho, 1]])
        z = rng.standard_normal((n, 2)) @ L.T
        w = np.sqrt(3.0 / rng.chisquare(3.0, n))[:, None]
        tt = z * w
        u_g = stats.norm.cdf(z)
        u_t = stats.t.cdf(tt, 3.0)
        panels = VGroup()
        for k, (U, nm, col) in enumerate(((u_g, r"Gaussian copula, $\rho = 0.7$", MODEL_C),
                                          (u_t, r"$t$ copula, $\rho = 0.7$, $\nu = 3$", TAIL_C))):
            g = axes([0, 1], [0, 1], x_length=4.6, y_length=4.6, xticks=[0, 1], yticks=[0, 1], font_size=14)
            ax = g.ax
            dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.018, color=col, fill_opacity=0.6) for a, b in U])
            box = Rectangle(width=ax.c2p(0.05, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 0.05)[1] - ax.c2p(0, 0)[1],
                            stroke_color=BAD, stroke_width=2.5).move_to(ax.c2p(0.025, 0.025))
            joint = int(((U[:, 0] < 0.05) & (U[:, 1] < 0.05)).sum())
            t = label(nm, font_size=18, color=col).next_to(g, UP, buff=0.15)
            c = label(rf"{joint} points in the red corner", font_size=17, color=BAD).next_to(g, DOWN, buff=0.2)
            panels.add(VGroup(g, dots, box, t, c))
        panels.arrange(RIGHT, buff=1.2).move_to(DOWN * 0.1)
        with self.voiceover(
            "A chosen finite sample with uniform marginals. <bookmark mark='a'/> Nine hundred Gaussian-copula points use latent correlation nought point seven. <bookmark mark='b'/> The t-copula points use the same latent correlation and three degrees of freedom. Count the observed five-percent red-corner points: this particular seed has nineteen Gaussian and seventeen t points. That finite random ordering does not contradict the distinct asymptotic tail coefficients, and the illustration does not estimate an expected joint frequency precisely. It would be wrong to claim this sample must contain more t-copula corner points."
        ) as vo:
            self.play(FadeIn(panels[0][0]), FadeIn(panels[0][3]), LaggedStart(*[FadeIn(d_) for d_ in panels[0][1]],
                                                                              lag_ratio=0.0005, run_time=2))
            self.play(Create(panels[0][2]), FadeIn(panels[0][4]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1][0]), FadeIn(panels[1][3]), LaggedStart(*[FadeIn(d_) for d_ in panels[1][1]],
                                                                              lag_ratio=0.0005, run_time=2))
            self.play(Create(panels[1][2]), FadeIn(panels[1][4]))
        self.wait(0.4)
        self.clear_scene()

    def lambda_(self):
        rows = [cmath(r"\lambda_L", r"=", r"\lim_{q \to 0} P\bigl(U < q \mid V < q\bigr)", font_size=42, colors={r"\lambda_L": TAIL_C}),
                cmath(r"\text{Gaussian}", r":", r"\lambda_L = 0\ \ \text{for any } \rho < 1", font_size=38, colors={r"\text{Gaussian}": MODEL_C}),
                cmath(r"t_\nu", r":", r"\lambda_L = 2\,t_{\nu+1}\Bigl(-\sqrt{\tfrac{(\nu + 1)(1 - \rho)}{1 + \rho}}\Bigr)", font_size=36,
                      colors={r"t_\nu": TAIL_C})]
        whys = [why(r"tail dependence: given one is in its extreme tail, the chance the other is too, in the limit"),
                why('the Gaussian copula is asymptotically independent: the conditional probability tends to zero; finite-threshold joint events can still be substantial'),
                why(r"the $t$ copula keeps a positive limit; with $\rho = 0.8$ and $\nu = 4$ it is about one half")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Tail dependence is a limiting conditional probability. <bookmark mark='a'/> Given one uniformized variable lies below q, ask the chance the other does too as q tends to zero. <bookmark mark='b'/> For a nonsingular Gaussian copula with correlation strictly between minus one and one, this limit is zero. That does not make finite-threshold joint extremes impossible. <bookmark mark='c'/> A t copula with finite degrees of freedom has the displayed positive limit. A one-percent empirical conditional frequency is a finite-threshold statistic, not an estimate known to have reached that limit."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def table(self, d):
        hx = [-4.4, -2.0, 0.2, 2.4, 4.8]
        head = VGroup(*[label(t, font_size=15, color=GREY_B) for t in (r"industries, daily 1969--2020", r"correlation",
                                                                         r"joint worst 1\%: data", r"Gaussian",
                                                                         r"$t_4$ limit")])
        tab = VGroup(head)
        for p in d["pairs"]:
            tab.add(VGroup(label(rf"{p['a']} and {p['b']}", font_size=18), MathTex(f"{p['rho']:.2f}", font_size=26),
                           MathTex(f"{p['emp']['0.01']:.2f}", font_size=26, color=DATA_C),
                           MathTex(f"{p['gauss']['0.01']:.2f}", font_size=26, color=MODEL_C),
                           MathTex(f"{p['t4']:.2f}", font_size=26, color=TAIL_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.85 * j, 0])
        p0, p1 = d["pairs"][0], d["pairs"][1]
        with self.voiceover(
            "In the data: Kenneth French's industries, every day the forty-nine all trade, from nineteen sixty-nine. "
            f"<bookmark mark='a'/> Banks and insurers: {p0['emp']['0.01']:.2f} in the data against the Gaussian's "
            f"{p0['gauss']['0.01']:.2f}. <bookmark mark='b'/> Oil and mining: {p1['emp']['0.01']:.2f} against "
            f"{p1['gauss']['0.01']:.2f}, less than half. <bookmark mark='c'/> In every pair, joint crashes are more common "
            "than the Gaussian copula allows; the t copula's limit is closer, though a finite sample at one percent is not "
            "yet the limit."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(Indicate(tab[1], scale_factor=1.01))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3:]))
        self.wait(0.4)
        self.clear_scene()

    def copula_var(self, unused=None):
        head=label('Copula sensitivity: what is held fixed?',font_size=29).to_edge(UP,buff=0.35)
        cards=VGroup(
            desk_question('marginals','Hold each asset distribution, units, weights and confidence level fixed before comparing joint models.',width=12.0,font_size=23),
            desk_question('latent correlation','The same copula correlation parameter need not preserve Pearson correlation after nonlinear marginal transforms.',width=12.0,font_size=23),
            desk_question('tail comparison','A finite-threshold portfolio ES comparison differs from asymptotic tail dependence. No omitted extra-output simulation is reused.',width=12.0,font_size=23)
        ).arrange(DOWN,buff=0.28).next_to(head,DOWN,buff=0.35)
        with self.voiceover("A copula sensitivity exercise must say what is held fixed. Match marginal distributions, units, portfolio weights and confidence. <bookmark mark='a'/> A Gaussian and a t copula can use the same latent correlation parameter without yielding the same Pearson correlation after nonlinear marginal transformations. <bookmark mark='b'/> A finite-threshold portfolio expected shortfall is also different from an asymptotic conditional tail limit. The combined extra output was not approved, so its simulated portfolio comparison is omitted rather than reconstructed from another historical fit or simulation.") as vo:
            self.play(FadeIn(head),FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.wait(0.5)
        self.clear_scene()

    def conditional(self, d):
        rows = [cmath(r"\bar\rho\ \text{(49 industries, all days)}", r"=", rf"{d['avg_all']:.2f}", font_size=36),
                cmath(r"\bar\rho\ \text{(the market's worst 5\% of days)}", r"=", rf"{d['avg_bad']:.2f}", font_size=36,
                      colors={rf"{d['avg_bad']:.2f}": BAD}),
                cmath(r"\text{conditioning}", r"\Rightarrow", '\\text{a different conditional estimand}', font_size=38)]
        whys = [why(r"the average pairwise correlation of the industries' daily returns"),
                why('measured on selected crash days; lower here, without identifying a causal selection decomposition'),
                why('outcome selection changes the conditional population; this descriptive gap does not identify its structural or selection components')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            f"Conditioning changes the population being measured. <bookmark mark='a'/> Average pairwise industry correlation is {d['avg_all']:.2f} over all eligible days. <bookmark mark='b'/> On selected worst-market-five-percent days it is {d['avg_bad']:.2f}. <bookmark mark='c'/> That conditional correlation estimates a different, truncated population. Selection can change correlation even with fixed structural dependence, but these two numbers do not identify the entire gap as bias or prove a structural change. Conditional correlation and finite-threshold joint-tail frequencies answer different questions."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def li(self):
        cards = VGroup(
            desk_question(r"one parameter for a whole market", r"David Li's Gaussian copula priced CDO tranches from a "
                          r"single correlation between default times (Part 20)", width=12.4, font_size=19),
            desk_question('finite-threshold risk remains', 'zero asymptotic tail dependence does not imply zero tranche loss; probabilities, recovery, correlation and structure all matter', width=12.4, font_size=19),
            desk_question(r"2007--08", r"defaults came together, as they do; the formula was later blamed, as reported, "
                          r"though its users had chosen to ignore what it left out", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The credit application illustrates model scope. <bookmark mark='a'/> A one-factor Gaussian default construction often uses a latent correlation parameter, not simply the Pearson correlation of default times. <bookmark mark='b'/> Zero asymptotic tail dependence does not imply riskless senior tranches: finite default probabilities, recovery, correlation, concentrations and tranche attachment all matter. <bookmark mark='c'/> A crisis narrative cannot be attributed to one asymptotic coefficient. The practical task is to examine joint-loss assumptions and stress alternative dependence structures."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"model the tail of the joint", r"choose copulas with tail dependence for risk, and test them "
                          r"on joint exceedances, not on correlations", width=12.4, font_size=19),
            desk_question(r"diversification fails when needed", r"the benefit measured on all days is smaller on the days "
                          r"it is wanted", width=12.4, font_size=19),
            desk_question(r"and the dependence is uncertain", r"Chapter 7 asks how bad VaR can be if nothing is known about "
                          r"the copula at all", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons. <bookmark mark='a'/> Model the tail of the joint distribution, and test it on joint "
            "exceedances, not on correlations. <bookmark mark='b'/> Diversification measured on all days is smaller on "
            "the days it is wanted. <bookmark mark='c'/> And dependence is itself uncertain: Chapter seven asks how bad "
            "VaR can get when nothing is known about it."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a portfolio's daily volatility is \$1.2m. What is the most plausible move of its risk factors that "
                       r"would cost it \$10m in a day, and how many standard deviations away is it?")
        with self.voiceover(
            "Pause and predict. A portfolio's daily volatility is one point two million dollars. What is the most "
            "plausible move of its risk factors that would cost it ten million in a day, and how many standard "
            "deviations away is that move?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
