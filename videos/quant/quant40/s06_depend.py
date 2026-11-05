from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.quant import *  # noqa: F403
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
        self.copula_var(load("extra"))
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
        with self.voiceover(
            "Paul Embrechts, Alexander McNeil and Daniel Straumann's pitfalls of correlation. <bookmark mark='a'/> Zero "
            "correlation is not independence. <bookmark mark='b'/> Not every correlation is possible: for lognormal "
            "marginals with very different volatilities, the attainable range is narrow. <bookmark mark='c'/> And "
            "correlation does not fix the tail: the same marginals and the same correlation can give very different "
            "chances of crashing together."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
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
                why(r"the $t$ copula, with the same correlation but joint extremes")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Separate the two. <bookmark mark='a'/> Abe Sklar's theorem: any joint distribution is its marginals glued "
            "together by a copula. <bookmark mark='b'/> The copula is the dependence with the marginals removed. "
            "<bookmark mark='c'/> The Gaussian copula, Part twenty's credit model. <bookmark mark='d'/> And the Student t "
            "copula, with the same correlation parameter but a tendency to produce extremes together."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
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
            "Seen as points, with uniform marginals. <bookmark mark='a'/> A Gaussian copula with correlation nought point "
            "seven: the cloud thins toward the corners. <bookmark mark='b'/> A t copula with the same correlation and "
            "three degrees of freedom: the corners fill. Count the points where both fall in their worst five percent."
        ) as vo:
            vo.wait_until("a")
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
                why(r"the Gaussian copula is asymptotically independent: extreme joint crashes become impossibly rare"),
                why(r"the $t$ copula keeps a positive limit; with $\rho = 0.8$ and $\nu = 4$ it is about one half")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The measure of joint crashes. <bookmark mark='a'/> Tail dependence: given one variable is in its extreme "
            "tail, the chance the other is too, in the limit. <bookmark mark='b'/> For the Gaussian copula it is zero, at "
            "any correlation below one: joint extremes become impossibly rare. <bookmark mark='c'/> For the t copula it "
            "stays positive: about a half with correlation nought point eight and four degrees of freedom."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
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
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3:]))
        self.wait(0.4)
        self.clear_scene()

    def copula_var(self, x):
        c = x["copula"]
        hx = [-3.6, -0.8, 1.8, 4.4]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"two assets, same marginals", r"copula",
                                                                         r"VaR / ES 99\%", r"VaR / ES 99.9\%")])
        tab = VGroup(head)
        for nm, key, col in ((r"Student-$t_3$ marginals", "gauss", MODEL_C), (r"$\rho = 0.8$", "t4", TAIL_C)):
            v = c[key]
            tab.add(VGroup(label(nm, font_size=18), label(r"Gaussian" if key == "gauss" else r"$t_4$", font_size=18, color=col),
                           MathTex(rf"{100 * v['var'][0]:.2f} / {100 * v['var'][1]:.2f}", font_size=24, color=col),
                           MathTex(rf"{100 * v['var999'][0]:.2f} / {100 * v['var999'][1]:.2f}", font_size=24, color=col)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.4 - 1.0 * j, 0])
        g, t = c["gauss"], c["t4"]
        foot = wrapped_label(r"400,000 simulated days of the sum of two assets with 1\% daily volatility each; the only "
                             r"difference between the rows is the copula", 11.4, 16, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "What the copula does to a portfolio's risk. Two assets with the same fat-tailed marginals and the same "
            "correlation, combined two ways. <bookmark mark='a'/> At ninety-nine percent, the VaR barely changes: "
            f"{100 * g['var'][0]:.2f} against {100 * t['var'][0]:.2f} percent. <bookmark mark='b'/> But the shortfall "
            f"beyond ninety-nine point nine rises from {100 * g['var999'][1]:.1f} to {100 * t['var999'][1]:.1f}. The copula "
            "lives in the deep tail, exactly where a ninety-nine percent VaR does not look."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(Indicate(VGroup(tab[1][3], tab[2][3]), color=BAD))
        self.wait(0.4)
        self.clear_scene()

    def conditional(self, d):
        rows = [cmath(r"\bar\rho\ \text{(49 industries, all days)}", r"=", rf"{d['avg_all']:.2f}", font_size=36),
                cmath(r"\bar\rho\ \text{(the market's worst 5\% of days)}", r"=", rf"{d['avg_bad']:.2f}", font_size=36,
                      colors={rf"{d['avg_bad']:.2f}": BAD}),
                cmath(r"\text{conditioning}", r"\Rightarrow", r"\text{biased correlation}", font_size=38)]
        whys = [why(r"the average pairwise correlation of the industries' daily returns"),
                why(r"measured only on crash days, it looks lower, the opposite of every crash's experience"),
                why(r"selecting days on the outcome truncates their range: Boyer, Gibson and Loretan (1997), Forbes and "
                    r"Rigobon (2002); tail dependence is the right question")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "A trap. <bookmark mark='a'/> The forty-nine industries' average correlation, over all days, is "
            f"{d['avg_all']:.2f}. <bookmark mark='b'/> On the market's worst five percent of days, it is {d['avg_bad']:.2f}: "
            "lower, against every trader's experience that everything falls together. <bookmark mark='c'/> It is a "
            "statistical artefact: choosing days by their outcome truncates the range, and correlation within a "
            "truncated sample is biased. Tail dependence asks the right question; conditional correlation does not."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def li(self):
        cards = VGroup(
            desk_question(r"one parameter for a whole market", r"David Li's Gaussian copula priced CDO tranches from a "
                          r"single correlation between default times (Part 20)", width=12.4, font_size=19),
            desk_question(r"no joint extremes", r"with zero tail dependence, it made the senior tranches look almost "
                          r"riskless", width=12.4, font_size=19),
            desk_question(r"2007--08", r"defaults came together, as they do; the formula was later blamed, as reported, "
                          r"though its users had chosen to ignore what it left out", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "This is not academic. <bookmark mark='a'/> David Li's Gaussian copula priced collateralised debt tranches "
            "from one correlation, Part twenty's model. <bookmark mark='b'/> With zero tail dependence, it made senior "
            "tranches look almost riskless. <bookmark mark='c'/> In twenty oh seven and oh eight defaults came together, "
            "as they do; the formula was later blamed, as reported, though its users had chosen to ignore what it left "
            "out."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
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
                vo.wait_until(m_)
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
        self.wait(0.5)
        self.clear_scene()
