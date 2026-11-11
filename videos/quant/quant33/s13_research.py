from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant33.common import BAD, COST_C, GOOD, HURDLE, OU_C, PART, RES_C, SPREAD_C, fit_right, illustration, load

CCOL = {"0.1": QC.REALIZED, "0.3": QC.DELTA, "0.5": QC.LOSS}


class Research(VoiceoverScene):
    def construct(self):
        t = load("theory")
        self.card()
        self.setup_()
        self.renewal()
        self.dynkin()
        self.solution()
        self.theorem()
        self.times(t)
        self.rates(t)
        self.universal(t)
        self.frictionless(t)
        self.cuberoot(load("smallc"))
        self.cubetable(load("smallc"))
        self.example()
        self.sims(t)
        self.data(load("pca"))
        self.related()
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"The optimal band for a mean-reverting spread", r"Where should a trader enter, given the "
                          r"costs?", part=PART)
        with self.voiceover("For the researcher. Every stat-arb book chooses bands, usually by habit: one and a quarter "
                            "deviations, or two. This chapter derives the profit rate of a band rule exactly, and the band "
                            "that maximises it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"dX_t", r"=", r"-\kappa X_t\,dt + \sigma\,dW_t", font_size=38, colors={r"\kappa": OU_C}),
                cmath(r"\text{rule}", r":", r"\text{flat at } 0;\ \text{enter one unit against } X \text{ when } |X| = m;\ "
                      r"\text{exit at } 0", font_size=28),
                cmath(r"\text{reward}", r"=", r"m - c\ \ \text{per round trip}", font_size=36, colors={r"c": COST_C})]
        whys = [why(r"a spread measured from its mean; its equilibrium deviation is $s_{\text{eq}} = \sigma/\sqrt{2\kappa}$"),
                why(r"the band rule: wait at the mean, bet on reversion when the spread reaches the band, close at the mean"),
                why(r"each round trip gains the band's width and pays a cost $c$, in the spread's own units")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The setup fixes a known Ornstein-Uhlenbeck process with positive kappa and sigma, centered at zero. <bookmark mark='a'/> Parameters are constant and the path is monitored continuously. <bookmark mark='b'/> While flat, wait until either band at distance m is reached; then hold one unit against the displacement and exit at zero. <bookmark mark='c'/> A completed cycle earns m minus a fixed round-trip cost c in spread units. We maximize long-run expected profit per time within this family. This is not a Sharpe objective, a return on committed capital, or a solution with financing, stops, breaks or a risk budget."
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

    def renewal(self):
        rows = [cmath(r"\text{cycle}", r"=", r"\underbrace{0 \to \pm m}_{\text{waiting}}\ \ \underbrace{\pm m \to 0}_{"
                      r"\text{holding}}", font_size=34),
                cmath(r"R(m)", r"=", r"\lim_{t\to\infty}\frac{\text{profit by } t}{t} = \frac{\mathbb E[\text{reward per "
                      r"cycle}]}{\mathbb E[\text{cycle length}]}", font_size=30, colors={r"R(m)": GOOD}),
                cmath(r"R(m)", r"=", r"\frac{m - c}{\mathbb E_0[\tau_m] + \mathbb E_{-m}[T_0]}", font_size=38)]
        whys = [why(r"the strong Markov property: each cycle starts afresh at the mean, so cycles are independent and "
                    r"identically distributed; by symmetry entering at $+m$ or $-m$ takes the same time back"),
                why(r"the renewal-reward theorem: long-run profit per unit time is the expected reward per cycle over the "
                    r"expected cycle length"),
                why(r"$\tau_m$: the first time $|X|$ reaches $m$ from 0; $T_0$: the first time $X$ reaches 0 from $-m$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Lemma one, the renewal-reward theorem. <bookmark mark='a'/> Each cycle has two legs: waiting at the mean "
            "until the spread reaches the band, then holding until it returns. By the strong Markov property every cycle "
            "starts afresh at the mean, so the cycles are independent and identical. <bookmark mark='b'/> Then the "
            "long-run profit per unit time is the expected reward per cycle over the expected length of a cycle. "
            "<bookmark mark='c'/> So everything reduces to two expected first-passage times."
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

    def dynkin(self):
        rows = [cmath(r"f(x)", r"=", r"\mathbb E_x[T]", font_size=36),
                cmath(r"\tfrac{\sigma^2}{2} f''(x) - \kappa x f'(x)", r"=", r"-1", font_size=36, colors={r"-1": HURDLE}),
                cmath(r"\big(e^{-\kappa x^2/\sigma^2} f'(x)\big)'", r"=", r"-\frac{2}{\sigma^2}e^{-\kappa x^2/\sigma^2}",
                      font_size=34)]
        whys = [why(r"the expected time to reach a boundary, as a function of the start"),
                why(r"Dynkin's formula: the generator of the OU process applied to $f$ is minus one inside the interval, "
                    r"with $f = 0$ on the boundary (Part 8's Feynman--Kac, with a constant running cost)"),
                why(r"multiply by the integrating factor $e^{-\kappa x^2/\sigma^2}$: the left side becomes an exact "
                    r"derivative, and the equation integrates twice")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Lemma two, the first-passage times. <bookmark mark='a'/> Let f of x be the expected time to reach the "
            "boundary from x. <bookmark mark='b'/> By Dynkin's formula, the OU generator applied to f is minus one, "
            "with f zero on the boundary: Part eight's Feynman-Kac, with a running cost of one per unit time. "
            "<bookmark mark='c'/> Multiply by the integrating factor, and the left side becomes an exact derivative. "
            "The equation integrates twice."
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

    def solution(self):
        rows = [cmath(r"\mathbb E_{-m}[T_0]", r"=", r"\frac{2}{\sigma^2}\int_{-m}^{0} e^{\kappa y^2/\sigma^2}\int_{-\infty}^{y}"
                      r"e^{-\kappa z^2/\sigma^2}dz\,dy", font_size=30, colors={r"\mathbb E_{-m}[T_0]": OU_C}),
                cmath(r"\mathbb E_{0}[\tau_m]", r"=", r"\frac{2}{\sigma^2}\int_{0}^{m} e^{\kappa y^2/\sigma^2}\int_{0}^{y}"
                      r"e^{-\kappa z^2/\sigma^2}dz\,dy", font_size=30, colors={r"\mathbb E_{0}[\tau_m]": SPREAD_C}),
                cmath(r"\int e^{-\kappa z^2/\sigma^2}dz", r"=", r"\frac{\sigma}{\sqrt\kappa}\frac{\sqrt\pi}{2}\operatorname{erf}"
                      r"\Big(\frac{\sqrt\kappa\, z}{\sigma}\Big)", font_size=30)]
        whys = [why(r"from $-m$ to the mean: the boundary condition at $-\infty$ is that $f'$ stays bounded, which fixes "
                    r"the inner integral's lower limit"),
                why(r"from the mean to either band: by symmetry $f'(0) = 0$, so the inner integral starts at 0"),
                why(r"the inner integrals are error functions; the outer ones are computed by quadrature in the House's "
                    r"\texttt{ou\_time\_to\_mean} and \texttt{ou\_time\_to\_band}")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The two solutions. <bookmark mark='a'/> From minus m to the mean, the condition far away is that the slope "
            "stays bounded, which starts the inner integral at minus infinity. <bookmark mark='b'/> From the mean to "
            "either band, symmetry makes the slope zero at the mean, which starts it at zero. <bookmark mark='c'/> The "
            "inner integrals are error functions, and the outer ones a one-dimensional quadrature."
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

    def theorem(self):
        st = VGroup(
            MathTex(r"u=m/s_{\rm eq},\ d=c/s_{\rm eq},\quad I(u)=\int_0^u e^{z^2/2}dz", font_size=30),
            MathTex(r"R=\frac{\kappa s_{\rm eq}}{\sqrt{\pi/2}}\frac{u-d}{I(u)},\qquad I(u^*)=(u^*-d)e^{u^{*2}/2}", font_size=30),
            wrapped_label(r"Known parameters; continuous monitoring; one unit; fixed round-trip cost. Unique $u^*>d$ for $d>0$. At $d=0$, a supremum as $u\downarrow0$, not an attained positive band.", 9.6, 20)
        ).arrange(DOWN, buff=0.35)
        card = theorem_card(r"The band rule's profit rate", st, r"this part; after Bertram (2010)", width=11.8, font_size=22)
        self.add(card)
        with self.voiceover(
            "The theorem is about this fixed policy family. <bookmark mark='a'/> The two expected passage times sum, after scaling, to the square root of half pi times the integral from zero to u of exp z squared over two, divided by kappa. Here u is m over equilibrium width and d is c over that width. <bookmark mark='b'/> Differentiating the reward rate gives the equation I of u equals u minus d times exp u squared over two. For positive cost it has exactly one solution above d: the derivative changes sign there. At zero cost the best rate is only a supremum as the positive band shrinks to zero. Speed scales the rate when width and dimensionless cost are held fixed."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def times(self, t):
        ms = np.asarray(t["ms"], float)
        tm, tb = np.asarray(t["times"]["to_mean"], float), np.asarray(t["times"]["to_band"], float)
        hi = float(np.ceil(max(tm.max(), tb.max())))
        g = axes([0, 2.5], [0, hi], x_length=7.2, y_length=4.2, xlabel=r"band $m$, in equilibrium deviations",
                 ylabel=r"expected time, in units of $1/\kappa$", xticks=[0, 1, 2], yticks=[0, hi / 2, hi],
                 yfmt=lambda v: f"{v:.1f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        c1 = curve(ax, ms, tm, OU_C, stroke_width=3)
        c2 = curve(ax, ms, tb, SPREAD_C, stroke_width=3)
        leg = legend([(OU_C, r"holding: from the band to the mean"), (SPREAD_C, r"waiting: from the mean to the band")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.8)
        fit_right(leg)
        self.add(g, c1, leg)
        with self.voiceover(
            "The two times. <bookmark mark='a'/> Holding, from the band back to the mean, grows slowly with the band: "
            "the further out, the stronger the pull back. <bookmark mark='b'/> Waiting, from the mean to the band, "
            "starts at zero and grows explosively, because reaching a distant band against the pull is rare. Wide "
            "bands are paid for in waiting."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(c1))
            vo.wait_until("b")
            self.play(Create(c2))
        self.wait(0.4)
        self.clear_scene()

    def rates(self, t):
        ms = np.asarray(t["ms"], float)
        g = axes([0, 2.5], [0, 0.7], x_length=7.2, y_length=4.2, xlabel=r"band $m$, in equilibrium deviations",
                 ylabel=r"profit rate $R(m)$, in $s_{\text{eq}}\kappa$", xticks=[0, 1, 2], yticks=[0, 0.3, 0.6],
                 yfmt=lambda v: f"{v:.1f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        lines, stars = VGroup(), VGroup()
        for c, col in CCOL.items():
            r = np.asarray(t["rates"][c], float)
            ok = np.isfinite(r) & (r > 0)
            lines.add(curve(ax, ms[ok], r[ok], col, stroke_width=3))
            best = [x for x in t["curve"] if abs(x["c"] - float(c)) < 1e-9][0]
            stars.add(Dot(ax.c2p(best["m"], best["R"]), radius=0.08, color=col))
        leg = legend([(col, rf"$c = {c}\,s_{{\text{{eq}}}}$") for c, col in CCOL.items()], font_size=16)
        leg.to_edge(RIGHT, buff=0.4).shift(UP * 1.8)
        fit_right(leg)
        b3 = [x for x in t["curve"] if abs(x["c"] - 0.3) < 1e-9][0]
        self.add(g, lines[0], leg)
        with self.voiceover(
            "The profit rate, for three costs. <bookmark mark='a'/> Each curve rises from zero at the cost, peaks, and "
            "falls as waiting takes over. <bookmark mark='b'/> The dots are the optima: higher costs push the best band "
            f"outward. At a cost of three tenths of a deviation, the best band is {b3['m']:.2f} deviations: close to "
            "Avellaneda and Lee's one and a quarter, which corresponds to a cost of roughly half a deviation."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(*[Create(l_) for l_ in lines], run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_, scale=1.5) for s_ in stars], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def universal(self, t):
        cv = t["curve"]
        cs = np.array([x["c"] for x in cv])
        ms = np.array([x["m"] for x in cv])
        g = axes([0, 1.05], [0, 2.0], x_length=7.0, y_length=4.2, xlabel=r"cost per round trip, $c/s_{\text{eq}}$",
                 ylabel=r"optimal band, $m^*/s_{\text{eq}}$", xticks=[0, 0.5, 1.0], yticks=[0, 1, 2],
                 xfmt=lambda v: f"{v:.1f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        line = curve(ax, cs, ms, OU_C, stroke_width=4, smooth=True)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=OU_C) for a, b in zip(cs, ms)])
        al = DashedLine(ax.c2p(0, 1.25), ax.c2p(1.05, 1.25), color=GREY_C, stroke_width=1.5)
        all_ = label(r"Avellaneda--Lee's 1.25", font_size=15, color=GREY_B).next_to(ax.c2p(1.05, 1.25), UP, buff=0.08).shift(LEFT * 1.0)
        txt = wrapped_label(r"one curve for every OU spread: the speed of reversion does not move it. Small costs move the "
                            r"band a lot: it grows roughly like the cube root of the cost near zero", 3.8, 16,
                            GREY_A).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        fit_right(txt)
        self.add(g, line, dots, al, all_)
        with self.voiceover(
            "The dimensionless optimum is a function of cost in equilibrium-width units. <bookmark mark='a'/> The displayed points are bounded numerical searches, not symbolic exact optimizers. The zero-cost grid point has a positive minimum band, whereas the mathematical optimum is a limiting supremum at zero. <bookmark mark='b'/> For small positive cost the true band grows asymptotically as the cube root of three times that cost. This shares an exponent with Part thirty-one's holdings band under quadratic risk, but the objective and derivation differ. A fixed one-and-a-quarter threshold corresponds to just one dimensionless cost within this particular OU model."
        ) as vo:
            self.play(FadeIn(g), Create(al), FadeIn(all_))
            vo.wait_until("a")
            self.play(Create(line), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(txt))
        self.wait(0.4)
        self.clear_scene()

    def frictionless(self, t):
        rows = [cmath(r"\mathbb E_{-m}[T_0]", r"\approx", r"\frac{m\sqrt\pi}{\sigma\sqrt\kappa},\qquad \mathbb E_0[\tau_m] \approx "
                      r"\frac{m^2}{\sigma^2}", font_size=32),
                cmath(r"R(m)", r"\to", r"\frac{m}{m\sqrt\pi/(\sigma\sqrt\kappa)} = \sigma\sqrt{\frac{\kappa}{\pi}}", font_size=34,
                      colors={r"\sigma\sqrt{\frac{\kappa}{\pi}}": GOOD}),
                cmath(r"\kappa = 1,\ s_{\text{eq}} = 1", r":", rf"R(0^+) = \sqrt{{2/\pi}} = {t['frictionless']:.4f}",
                      font_size=32)]
        whys = [why(r"for a small band: the holding time is linear in $m$ (from $-m$ the spread is pulled back by the mean "
                    r"reversion of its far excursions), the waiting time quadratic, like Brownian motion"),
                why(r"so with no costs the rate tends to a finite limit, not infinity: trading infinitely often does not "
                    r"earn infinitely fast"),
                why(r"the frictionless supremum is a limit; the optimizer's positive minimum band only approximates it")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A corollary that surprises people. <bookmark mark='a'/> For a tiny band, the holding time is linear in the "
            "band, and the waiting time quadratic. <bookmark mark='b'/> So with no costs the profit rate tends to a "
            "finite limit, sigma times the root of kappa over pi, not to infinity: trading infinitely often does not "
            f"earn infinitely fast. <bookmark mark='c'/> In the curve's units, the root of two over pi, {t['frictionless']:.3f}. "
            "Costs then decide how far from that limit the best band must retreat."
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

    def cuberoot(self, sc):
        rows = [cmath(r"\mathbb E_{-m}[T_0]", r"=", r"\frac{1}{\kappa}\Big(a\tilde m - \frac{\tilde m^2}{2} + "
                      r"\frac{a\tilde m^3}{6}\Big) + O(\tilde m^4)", font_size=30),
                cmath(r"\mathbb E_0[\tau_m]", r"=", r"\frac{1}{\kappa}\Big(\frac{\tilde m^2}{2} + \frac{\tilde m^4}{12}\Big)"
                      r" + O(\tilde m^6)", font_size=30),
                cmath(r"R(m)", r"\approx", r"\frac{\kappa s_{\text{eq}}}{a}\,\frac{\tilde m - \tilde c}{\tilde m + \tilde m^3/6}\ "
                      r"\Rightarrow\ \tilde m^{*3} \approx 3\tilde c", font_size=30, colors={r"3\tilde c": GOOD}),
                cmath(r"\frac{m^*}{s_{\text{eq}}}", r"\approx", r"\Big(\frac{3c}{s_{\text{eq}}}\Big)^{1/3},\quad "
                      r"\frac{R(m^*)}{R(0^+)} \approx 1 - \tfrac12\Big(\frac{3c}{s_{\text{eq}}}\Big)^{2/3}", font_size=30,
                      colors={r"\frac{m^*}{s_{\text{eq}}}": HURDLE})]
        whys = [why(r"expand the Dynkin integrals in $\tilde m = m/s_{\text{eq}}$, with $a = \sqrt{\pi/2}$: the holding "
                    r"time has a negative quadratic term"),
                why(r"the waiting time's quadratic term is exactly the opposite: in the cycle length, the $\tilde m^2$ "
                    r"terms cancel"),
                why(r"so the first correction is cubic; set the derivative to zero and keep the leading terms"),
                why(r"the small-cost law, with no free constant and no dependence on the speed $\kappa$; the profit lost to "
                    r"costs grows like $c^{2/3}$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "The cube root has a precise small-cost asymptotic derivation. <bookmark mark='a'/> Expand the two passage times for a small band, "
            "measured in equilibrium deviations. The time back to the mean has a negative quadratic term. "
            "<bookmark mark='b'/> The time out to the band has exactly the opposite one. In the length of a cycle, "
            "they cancel. <bookmark mark='c'/> So the first correction to the linear term is cubic, and setting the "
            "derivative of the profit rate to zero gives: to leading order the band cubed is three times the cost. "
            "<bookmark mark='d'/> The small-cost law. The best band is the cube root of three times the cost, in "
            "equilibrium deviations, with no free constant and no dependence on the speed. And the fraction of the "
            "frictionless profit lost to costs grows like the cost to the power two thirds."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def cubetable(self, sc):
        rows = sc["rows"]
        hx = [-3.6, -1.2, 1.2, 3.6]
        head = VGroup(label(r"cost $c/s_{\text{eq}}$", font_size=17, color=GREY_B),
                      label(r"numerical band", font_size=17, color=OU_C), label(r"$(3c)^{1/3}$", font_size=17, color=HURDLE),
                      label(r"ratio", font_size=17, color=GREY_B))
        tab = VGroup(head)
        for r in rows:
            tab.add(VGroup(MathTex(f"{r['c']:g}", font_size=24), MathTex(f"{r['m']:.3f}", font_size=24),
                           MathTex(f"{r['law']:.3f}", font_size=24), MathTex(f"{r['ratio']:.3f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.4 - 0.62 * j, 0])
        foot = wrapped_label(r"the numerical band from \texttt{statarb.optimal\_band} (Dynkin integrals, Simpson's rule); the law "
                             r"from the expansion; Part 31's no-trade band for quadratic risk has the same cube root", 11.4,
                             16, GREY_A).to_edge(DOWN, buff=0.4)
        r1, r3 = rows[2], rows[-1]
        e1 = 100 * abs(r1["ratio"] - 1)
        e3 = 100 * abs(r3["ratio"] - 1)
        self.add(tab[0], tab[1], foot)
        with self.voiceover(
            "Checked against the numerical optimum. <bookmark mark='a'/> At a cost of a hundredth of a deviation the law is "
            f"within {e1:.1f} percent of the numerical band; at a cost of {r3['c']:g} deviations, already a large cost, it is "
            f"within {e3:.0f} percent. <bookmark mark='b'/> It is the same cube root as Part thirty-one's no-trade band, "
            "for a different reason: there the cost was traded against quadratic risk, here against the time a cycle "
            "takes."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(Indicate(VGroup(*[r_[3] for r_ in tab[1:]]), color=GOOD, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    def example(self):
        from explainer.quant.house import statarb as SA
        s_eq, hl, cost = 0.02, 8.0, 0.002
        kappa = math.log(2) / hl
        sigma = s_eq * math.sqrt(2 * kappa)
        m, r = SA.optimal_band(kappa, sigma, cost)
        cyc = SA.ou_time_to_mean(m, kappa, sigma) + SA.ou_time_to_band(m, kappa, sigma)
        law = (3 * cost / s_eq) ** (1 / 3)
        rows = [cmath(r"s_{\text{eq}} = 2\%,\ \ \text{half-life } 8\ \text{days},\ \ c = 0.2\%", r"\Rightarrow",
                      rf"c/s_{{\text{{eq}}}} = {cost / s_eq:.2f}", font_size=30),
                cmath(r"m^*", r"=", rf"{100 * m:.2f}\%\ =\ {m / s_eq:.2f}\, s_{{\text{{eq}}}}\quad "
                      rf"(\text{{law: }} {law:.2f})", font_size=32, colors={r"m^*": HURDLE}),
                cmath(r"\text{a cycle}", r"\approx", rf"{cyc:.0f}\ \text{{days}},\quad R = {1e4 * r:.1f}\ "
                      rf"\text{{bp a day per unit}}", font_size=30, colors={r"\text{a cycle}": OU_C})]
        whys = [why(r"a chosen mathematical spread: two percent wide, an eight-day half-life, and a round trip of 20 bp "
                    r"on both legs"),
                why(r"a numerical optimizer from the House's functions, and the small-cost law beside it"),
                why(r"the expected time from the mean out to the band and back, and the profit rate it implies")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        mb, ms, ra = 100 * m, m / s_eq, 1e4 * r
        with self.voiceover(
            "A worked example. <bookmark mark='a'/> A residual two percent wide, with an eight-day half-life, and a "
            "round trip costing twenty basis points on both legs: a cost of a tenth of a deviation. "
            f"<bookmark mark='b'/> The best band is {mb:.2f} percent, {ms:.2f} deviations, and the small-cost law gives "
            f"{law:.2f}. <bookmark mark='c'/> A cycle takes about {cyc:.0f} days, and the rule earns {ra:.1f} basis points "
            "a day for each unit held. Avellaneda and Lee's habit of one and a quarter deviations would be nearly twice "
            "as wide."
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

    def sims(self, t):
        rows = t["sims"]
        hx = [-4.8, -2.8, -0.8, 1.4, 3.6, 5.6]
        head = VGroup(label(r"$c$", font_size=17, color=GREY_B), label(r"$m$", font_size=17, color=GREY_B),
                      label(r"theorem", font_size=17, color=GOOD), label(r"grid $\Delta t=0.0005$", font_size=17,
                                                                         color=OU_C),
                      label(r"$2R_{\rm fine}-R_{\rm coarse}$", font_size=17, color=OU_C), label(r"trades", font_size=17,
                                                                                   color=GREY_B))
        tab = VGroup(head)
        for r in rows:
            tab.add(VGroup(MathTex(f"{r['c']:.1f}", font_size=22), MathTex(f"{r['m']:.2f}", font_size=22),
                           MathTex(f"{r['theory']:.3f}", font_size=22), MathTex(f"{r['sim']:.3f}", font_size=22),
                           MathTex(f"{r['sim_extrap']:.3f}", font_size=22), MathTex(f"{r['trades']}", font_size=22)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.7 - 0.52 * j, 0])
        foot = wrapped_label(r"exact OU simulation over 4{,}000 units of time; each trade booked at the band and the mean; "
                             r"discrete monitoring detects crossings late, so the heuristic $2R_{\rm fine}-R_{\rm coarse}$ uses steps of 0.002 "
                             r"and 0.0005; no execution overshoots or error bars", 11.8, 15, GREY_A).to_edge(DOWN, buff=0.25)
        self.add(tab[0], tab[1], foot)
        with self.voiceover(
            "The stored simulation is a timing illustration on a grid, at half, once, and one point six times each numerical optimum. <bookmark mark='a'/> Exact OU transitions connect grid dates, but crossings between dates are missed. Every completed trade is credited at the band and mean, not the actual overshoot execution prices. Thus it does not simulate an executable grid-trading cash account. <bookmark mark='b'/> The final column combines a fine step of point zero zero zero five and a coarse step four times larger as twice fine minus coarse, assuming a leading square-root-step bias. This extrapolation is heuristic. Equal seeds do not create coupled Brownian paths, and this table has no Monte Carlo error bars or guaranteed ranking."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[:4])) for r_ in tab[1:]], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[4:])) for r_ in tab[1:]], lag_ratio=0.1))
        self.wait(0.4)
        self.clear_scene()

    def data(self, p):
        cf = p["configs"]
        th, al = cf["5f/60d/theory"], cf["5f/60d/1.25"]
        hx = [-3.6, -1.0, 1.4, 3.8]
        head = VGroup(label(r"rule, 1994--2020", font_size=17, color=GREY_B), label(r"Sharpe, gross", font_size=17,
                                                                                   color=GREY_B),
                      label(r"Sharpe, net of 5 bp", font_size=17, color=GREY_B), label(r"daily turnover", font_size=17,
                                                                                     color=GREY_B))
        tab = VGroup(head)
        for nm, r, col in ((r"Avellaneda--Lee bands", al, RES_C), (r"the theorem's band", th, OU_C)):
            tab.add(VGroup(label(nm, font_size=20, color=col), MathTex(f"{r['gross']['sharpe']:.2f}", font_size=26),
                           MathTex(f"{r['sharpe']:.2f}", font_size=26), MathTex(rf"{100 * r['turnover']:.0f}\%",
                                                                                 font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.2 - 0.9 * j, 0])
        foot = wrapped_label(r"same research sample, synthetic residual P\&L and incomplete cost accounting; bands use a finite cost lookup with endpoint clipping; no independent performance verdict", 11.6, 15, GREY_A).to_edge(DOWN, buff=0.4)
        self.add(tab[0], tab[1], foot)
        with self.voiceover(
            f"The stored industry comparison is a research illustration of two proxy policies. <bookmark mark='a'/> Fixed thresholds have synthetic gross Sharpe {al['gross']['sharpe']:.2f}, and charged proxy Sharpe {al['sharpe']:.2f}. <bookmark mark='b'/> The mathematical-band configuration has {th['gross']['sharpe']:.2f} and {th['sharpe']:.2f}, with discrete-signal turnover {100 * th['turnover']:.0f} percent versus {100 * al['turnover']:.0f}. Bands are interpolated from thirty-one cost points with endpoint clipping. Known-parameter OU theory does not validate fitted bridges or omitted cash flows. All these comparisons reuse research data and incomplete trading-cost accounting; Chapter ten specifies what a fuller evaluation would require."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
        self.wait(0.4)
        self.clear_scene()

    def related(self):
        cards = VGroup(
            desk_question(r"Bertram (2010)", r"the same renewal argument for an entry level and an exit level, "
                          r"maximising the expected return per unit time, with first-passage times from the OU's known "
                          r"series", width=12.4, font_size=18),
            desk_question(r"Leung and Li (2015)", r"entry and exit as optimal stopping problems with discounting and a "
                          r"stop-loss: free boundaries instead of a fixed cycle", width=12.4, font_size=18),
            desk_question(r"Part 31's no-trade band", r"a cost against quadratic risk gives a band in holdings, also "
                          r"growing like the cube root of the cost: two problems, one exponent", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        self.add(cards[0])
        with self.voiceover(
            "Where the theorem sits. <bookmark mark='a'/> William Bertram used the same renewal argument for an entry level and "
            "an exit level, with the passage times from the process's known series. <bookmark mark='b'/> Tim Leung and Xin Li "
            "treat entry and exit as optimal stopping problems with discounting and a stop-loss, whose answer is a pair "
            "of free boundaries rather than a fixed cycle. <bookmark mark='c'/> And Part thirty-one's no-trade band, a "
            "cost traded against quadratic risk, grows with the same cube root: two different problems, one exponent."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: estimated parameters", r"the band depends on $\kappa$ and $s_{\text{eq}}$, which are "
                          r"estimated with Kendall's bias (Chapter 4); the optimal band under parameter uncertainty, and "
                          r"learning while trading, are not solved here", width=12.4, font_size=18),
            desk_question(r"open: breaks and stop-losses", r"a spread whose tie breaks is not OU; Leung and Li add a "
                          r"stop-loss, but the joint problem of detecting a break and trading the band needs a specified joint model",
                          width=12.4, font_size=18),
            desk_question(r"open: many spreads at once", r"a book of correlated residuals with a risk budget and "
                          r"square-root impact is a multi-dimensional free-boundary problem not solved in this chapter",
                          width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        self.add(cards[0])
        with self.voiceover(
            "Three extensions require additional modeling. <bookmark mark='a'/> Uncertain parameters and learning while trading change the known-parameter optimum; this chapter supplies no general solution. <bookmark mark='b'/> Structural breaks and a stop-loss change the cycle and objective. Existing optimal-stopping literature treats specified versions, but does not make our fixed-band formula universal. <bookmark mark='c'/> Correlated spreads, financing, a portfolio risk budget and nonlinear impact create a joint control problem. These are directions for further work, not claims that no related solution exists anywhere in the literature."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"two spreads have the same $s_{\text{eq}}$ and cost; one reverts twice as fast. How do their "
                       r"optimal bands and profit rates compare?")
        working = MathTex('s_1=s_2,\\ c_1=c_2,\\ \\kappa_2=2\\kappa_1,\\qquad u^*=h(c/s),\\quad R=\\kappa s\\,g(u,c/s)', font_size=32).move_to(UP * 0.8)
        if working.width > 12.1:
            working.scale_to_fit_width(12.1)
        setup_note = wrapped_label('Known OU parameters, one unit and continuous monitoring. Equilibrium width stays fixed, so sigma changes with the square root of kappa.', 11.7, 23).move_to(DOWN * 0.9)
        self.add(working, setup_note, q)
        with self.voiceover(
            "Pause and predict. Two spreads have the same equilibrium deviation and the same cost, but one reverts "
            "twice as fast. How do their optimal bands and their profit rates compare?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
