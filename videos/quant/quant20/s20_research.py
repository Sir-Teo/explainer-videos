from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, GOOD, HAZ, PART, RISKY, SAFE, load

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

    def card(self):
        c = research_card(r"The granularity adjustment", r"How wrong is Basel's large-pool formula for a portfolio of "
                          r"real size?", part=PART)
        with self.voiceover("For the researcher: Chapter 10 derived Vasicek's large-pool distribution, the formula "
                            "behind bank capital, and noted that it assumes infinitely many tiny loans. Real books have "
                            "a hundred names, or a thousand. Here is the exact loss distribution for a finite pool, and "
                            "the one-term correction, Gordy's granularity adjustment, that fixes the formula."):
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
            "Take N equal loans. <bookmark mark='a'/> Given the common factor, each defaults with Vasicek's conditional "
            "probability. <bookmark mark='b'/> Given the factor, defaults are independent, so their number is "
            "binomial. <bookmark mark='c'/> So the exact loss distribution is a one-dimensional integral of binomial "
            "probabilities over the factor: computable to any precision, no simulation needed. <bookmark mark='d'/> As "
            "the pool grows, the binomial collapses onto its mean, and the quantile becomes the conditional default "
            "rate in the bad state: the large-pool formula that sets bank capital."
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
                why(r"Gordy (2003): a closed-form, portfolio-level add-on, proportional to $1/N$ for equal loans (to the "
                    r"Herfindahl index of exposures in general)")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        thm = theorem_card(r"The granularity adjustment", wrapped_label(
            r"in a one-factor model the loss quantile of a finite portfolio is the asymptotic (ASRF) quantile plus a term "
            r"of order $1/N$, given in closed form by the second-order expansion of the quantile; the ASRF formula is "
            r"exact only in the infinitely granular limit", 10.6, 20, GREY_A),
            who=r"Gordy (2003), \textit{J. Financial Intermediation} 12; Martin and Wilde (2002); Gordy and L\"utkebohmert (2013)",
            width=11.6, font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now the correction. <bookmark mark='a'/> Write the loss as the large-pool loss plus idiosyncratic noise, "
            "whose conditional variance falls like one over N. <bookmark mark='b'/> A quantile perturbed by small noise "
            "shifts by a term with the noise's variance, the factor's density, and the slope of the conditional loss: "
            "a second-order expansion due to Christian Gourieroux, Jean-Paul Laurent and Olivier Scaillet. "
            "<bookmark mark='c'/> For equal loans the shift is a constant over N. <bookmark mark='d'/> Michael Gordy "
            "turned this into the granularity adjustment in 2003; for unequal loans, N is replaced by the inverse "
            "Herfindahl index of the exposures."
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
            "For Vasicek's model the adjustment is fully explicit. <bookmark mark='a'/> The conditional default rate's "
            "first derivative is a normal density times the chain rule, and its second derivative brings down minus z. "
            "<bookmark mark='b'/> Expand the derivative in the formula, using the fact that the normal density's "
            f"derivative is minus y times itself, and three explicit terms remain. At a one percent default probability "
            f"and twelve percent correlation the bracket is {c['ga_unit']:.2f}, so the add-on is about two over N: two "
            "percentage points of the book for a hundred loans."
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
        leg = legend([(EX, r"exact (the binomial integral)"), (ASRF, r"large-pool formula (ASRF)"),
                      (GA, r"ASRF + granularity adjustment"), (HAZ, r"Monte Carlo, 400{,}000 scenarios")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"PD 1\%, asset correlation {c['rho']:g}, full loss given default; the exact quantile "
                             r"interpolated between its steps of $1/N$. The ASRF line is what Basel's formula charges",
                             3.3, 14, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        r100 = [r_ for r_ in c["rows"] if r_["N"] == 100][0]
        with self.voiceover(
            "Here is the 99.9 percent loss quantile, for loans with a one percent default probability and an asset "
            "correlation of twelve percent. <bookmark mark='a'/> The large-pool formula says "
            f"{100 * c['asrf']:.1f} percent of the book, whatever the size. <bookmark mark='b'/> The exact answer is "
            f"higher for any finite pool: {100 * r100['smooth']:.1f} percent for a hundred loans, a sixth more capital; "
            "the squares, Monte Carlo, agree. <bookmark mark='c'/> Add Gordy's adjustment, and the formula tracks the "
            "exact curve from about two hundred and fifty loans on. For very small pools it overcorrects: a "
            "second-order expansion cannot capture twenty-five loans."
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
                      label(r"exact, $N = 100$", font_size=20, color=EX), label(r"exact, $N = 1{,}000$", font_size=20, color=EX),
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
        foot = wrapped_label(r"the adjustment is largest, relative to the quantile, for low correlation: when the common "
                             r"factor explains little, idiosyncratic noise is a larger share of the tail. Basel's Pillar 1 "
                             r"capital has no granularity term; concentration is left to supervisors (Pillar 2)", 11.6, 16,
                             GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Across three portfolios. <bookmark mark='a'/> The adjustment matters most, relative to the capital, when "
            "the correlation is low: the common factor explains little, and idiosyncratic noise is a larger share of the "
            "tail. <bookmark mark='b'/> Basel's first-pillar capital formula has no granularity term at all; "
            "concentration is left to supervisors' judgement under the second pillar."
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
                (r"500 equal loans, exact", rf"{100 * lp['q_equal500']:.1f}\%"),
                (r"ASRF + granularity adjustment at $N = 1/\mathrm{HHI}$", rf"{100 * lp['asrf_ga']:.1f}\%"),
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
            "Real books are lumpy. Take five hundred loans whose sizes fall like one over their rank. "
            f"<bookmark mark='a'/> The largest is {100 * lp['largest']:.0f} percent of the book, and the inverse "
            f"Herfindahl index says the book behaves like {lp['n_eff']:.0f} equal loans, not five hundred. "
            f"<bookmark mark='b'/> The large-pool formula charges {100 * lp['asrf']:.1f} percent. Simulation says the "
            f"99.9 percent loss is {100 * lp['q_mc']:.1f} percent: more than double. The granularity adjustment, "
            f"applied at the effective size, gets most of the way, to {100 * lp['asrf_ga']:.1f}; at so few effective "
            "names the expansion is stretched."
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
                    r"correlation, so a bank's capital is a sum over loans. Gordy (2003) showed that only the "
                    r"asymptotic single-factor model has this property"),
                why(r"granularity breaks it: the add-on depends on the whole book's concentration, so it cannot be "
                    r"computed loan by loan, which is why Basel left it out of the formula")]
        step = ladder(self, rows, whys, keep=2, top=2.2, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Why does Basel use the limit at all? <bookmark mark='a'/> Because in the large-pool limit each loan's "
            "capital depends only on its own default probability and correlation, so a bank's capital is a simple sum "
            "over its loans, and a loan costs the same capital in any bank. Gordy proved in 2003 that only the "
            "asymptotic single-factor model has this property. <bookmark mark='b'/> Granularity breaks it: the "
            "adjustment depends on the whole book's concentration, and cannot be computed loan by loan. Basel chose "
            "simplicity, and left concentration to judgement."
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
            desk_question(r"open: small and lumpy books", r"the expansion fails for a few large exposures, as here at 25 "
                          r"loans; exact methods for lumpy, heterogeneous books at the 99.9\% level are costly", width=12.4,
                          font_size=18),
            desk_question(r"open: estimation risk in the inputs", r"$\rho$ and PD are estimated from short histories "
                          r"(Chapter 7's seventeen years); their uncertainty moves the quantile more than granularity "
                          r"does, and combining the two is unsettled", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> With sector and country factors the analytic adjustment needs "
            "multifactor conditional moments; methods exist, but guarantees in the far tail are partial. "
            "<bookmark mark='b'/> The expansion fails for a few large exposures, as at twenty-five loans here, and exact "
            "methods for lumpy books at the ninety-nine point nine percent level are costly. <bookmark mark='c'/> And "
            "the correlation and the default probability are themselves estimated from short histories, like Chapter "
            "7's seventeen years; their uncertainty moves the quantile more than granularity does."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
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
