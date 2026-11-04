from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, OPT, PART, RV, SPOT, VAR, load

LEFT_C, RIGHT_C, LEE_C = BAD, RV, QC.IDEA


class Research(VoiceoverScene):
    def construct(self):
        t = load("moments_theory")
        self.card()
        self.riccati()
        self.tstar_plot(t)
        self.sample(t)
        self.lee()
        self.wing(t)
        self.btc(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Moment explosions and the wings", r"When do a model's moments become infinite, and what does "
                          r"that say about its smile far from the money?", part=PART)
        with self.voiceover("For the researcher: Chapter 5 warned in passing that in stochastic volatility models a "
                            "moment of the price can become infinite at a finite time. Here is when exactly, why it "
                            "matters for simulation, and the theorem that turns it into the slope of the smile's wings."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def riccati(self):
        rows = [cmath(r"\mathbb E\,e^{pX_T}", r"=", r"\exp\big(\phi(T) + \psi(T)\,v_0\big),\qquad X = \log S/F", font_size=30,
                      colors={r"\mathbb E\,e^{pX_T}": VAR}),
                cmath(r"\psi'", r"=", r"\tfrac12\xi^2\psi^2 + (\rho\xi p - \kappa)\,\psi + \tfrac12(p^2 - p),\quad \psi(0) = 0",
                      font_size=30, colors={r"\psi'": VAR}),
                cmath(r"T^*(p)", r"=", r"\frac{2}{\sqrt{-\Delta}}\Big(\frac{\pi}{2} - \arctan\frac{\rho\xi p - \kappa}{\sqrt{-\Delta}}"
                      r"\Big),\quad \Delta = (\rho\xi p - \kappa)^2 - \xi^2(p^2 - p)", font_size=26, colors={r"T^*(p)": BAD})]
        whys = [why(r"Heston is affine (Chapter 3): the moment generating function is exponential-affine in the "
                    r"starting variance"),
                why(r"the variance coefficient solves a Riccati equation with constant coefficients; for $p > 1$ or "
                    r"$p < 0$ the constant term is positive and pushes it up"),
                why(r"when the quadratic has no real root ($\Delta < 0$), $\psi$ is a shifted tangent and reaches infinity "
                    r"at this time; with real roots it explodes only if $\rho\xi p - \kappa > 0$, and then at "
                    r"$\log\frac{b + \sqrt\Delta}{b - \sqrt\Delta}/\sqrt\Delta$")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        thm = theorem_card(r"Moment explosions", wrapped_label(
            r"in the Heston model $\mathbb E[S_T^p] < \infty$ exactly when $T < T^*(p)$, the blow-up time of $\psi$; "
            r"after it, the moment is infinite, however the model is simulated", 10.6, 20, GREY_A),
            who=r"Andersen and Piterbarg (2007), \textit{Finance and Stochastics} 11", width=11.6,
            font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Heston is affine. <bookmark mark='a'/> So the moment generating function of the log price is an "
            "exponential, affine in the starting variance. <bookmark mark='b'/> The variance coefficient psi solves a "
            "Riccati equation. For p above one, or below zero, its constant term is positive and pushes psi up, and "
            "the quadratic term can make it run away. <bookmark mark='c'/> When the quadratic has no real root, psi "
            "is a shifted tangent, and reaches infinity at this time. <bookmark mark='d'/> Leif Andersen and Vladimir "
            "Piterbarg showed in 2007 that this is exactly when the p-th moment of the price becomes infinite."
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

    def tstar_plot(self, t):
        g = axes([-10, 16], [0, 10], x_length=8.4, y_length=4.2, xlabel=r"moment $p$ of the price, $\mathbb E[S_T^p]$",
                 ylabel=r"explosion time $T^*(p)$, years", xticks=[-10, -5, 0, 1, 5, 10, 15], yticks=[0, 2, 4, 6, 8, 10],
                 font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        pn, tn = np.asarray(t["p_neg"]), np.asarray(t["tstar_neg"], float)
        ok = np.isfinite(tn) & (tn <= 10)
        left = curve(ax, pn[ok], tn[ok], LEFT_C, stroke_width=3)
        pp, tp = np.asarray(t["p_pos"]), np.asarray(t["tstar_pos"], float)
        okp = np.isfinite(tp) & (tp <= 10)
        right = curve(ax, pp[okp], tp[okp], RIGHT_C, stroke_width=3) if okp.sum() > 2 else VGroup()
        dots = VGroup(*[Dot(ax.c2p(c["p"], c["ode"]), radius=0.07, color=WHITE) for c in t["ode_check"]
                        if c["ode"] and c["ode"] <= 10])
        band = Rectangle(width=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 10)[1] - ax.c2p(0, 0)[1],
                         stroke_width=0, fill_color=GREY_D, fill_opacity=0.5).move_to(ax.c2p(0.5, 5))
        blab = label(r"$0 \le p \le 1$: always finite", font_size=14, color=GREY_B).next_to(band, UP, buff=0.05)
        tb = t["textbook"]
        leg = legend([(LEFT_C, r"negative moments: the crash side"), (RIGHT_C, r"$p > 1$: the upper tail"),
                      (WHITE, r"an ODE solver's blow-up time")], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"a textbook Heston: $\kappa = {tb['kappa']:g}$, $\theta = {tb['theta']:g}$, "
                             rf"$\xi = {tb['xi']:g}$, $\rho = {tb['rho']:g}$. With $\rho < 0$, $\rho\xi p - \kappa < 0$, and the "
                             r"roots stay real up to $p \approx 8.4$: those moments are finite for ever", 3.3, 14,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        c3 = [c for c in t["ode_check"] if c["p"] == -3.0][0]
        with self.voiceover(
            "The explosion times for a textbook Heston with strong negative correlation. <bookmark mark='a'/> "
            "Between zero and one, every moment is finite, always. <bookmark mark='b'/> Negative moments, the crash "
            f"side, explode, and sooner the more negative: the minus third moment at {c3['formula']:.2f} years. The "
            "white dots are an ODE solver's blow-up times; they agree to seven digits. <bookmark mark='c'/> On the "
            "right, negative correlation keeps every moment up to about the eighth finite for ever; beyond it they "
            "explode too, but later. The upper tail is thinner than the lower."
        ) as vo:
            self.play(FadeIn(g), FadeIn(band), FadeIn(blab), FadeIn(side))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Create(left), FadeIn(leg[0]), FadeIn(dots), FadeIn(leg[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(leg[1]), FadeIn(right))
        self.wait(0.4)
        self.clear_scene()

    def sample(self, t):
        sm = t["sample_moment"]
        g = axes([2, 5.4], [0, 10], x_length=8.2, y_length=4.0, xlabel=r"number of simulated paths",
                 ylabel=r"running sample mean of $S_T^{-3}$", xticks=[2, 3, 4, 5], yticks=[0, 2, 4, 6, 8, 10],
                 xfmt=lambda v: f"10^{{{int(v)}}}", font_size=15, log_x=True).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        cols = {"before": RIGHT_C, "after": LEFT_C}
        lines = VGroup()
        for k in ("before", "after"):
            r = sm["runs"][k]
            y = np.clip(np.asarray(r["running_mean"]), 0, 10)
            lines.add(curve(ax, np.log10(r["n"]), y, cols[k], stroke_width=3))
        b, a = sm["runs"]["before"], sm["runs"]["after"]
        leg = legend([(cols["before"], rf"$T = {b['T']:.2f}$, before $T^*$"), (cols["after"], rf"$T = {a['T']:.2f}$, after")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"Andersen's QE scheme (Chapter 5), 200{{,}}000 paths; $T^*(-3) = {sm['tstar']:.2f}$. After "
                             rf"it, the single largest path is {100 * a['max_share']:.0f}\% of the whole sum; before it, "
                             rf"{100 * b['max_share']:.1f}\%", 3.3, 14, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Why it matters for simulation. Estimate the minus third moment by Monte Carlo. <bookmark mark='a'/> At "
            "half the explosion time the running mean settles, as the law of large numbers promises. "
            "<bookmark mark='b'/> At one and a half times it, it never settles: it jumps whenever a path hits a deep "
            f"crash, and the single largest path is {100 * a['max_share']:.0f} percent of the whole sum. The estimator "
            "is not slow; its target is infinite. Any payoff that grows like an inverse power of the price, such as a "
            "variance swap in a crash or a put struck far out, inherits this."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines[1]), FadeIn(leg[1]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def lee(self):
        rows = [cmath(r"\tilde q", r"=", r"\sup\{q : \mathbb E[S_T^{-q}] < \infty\}", font_size=32, colors={r"\tilde q": LEFT_C}),
                cmath(r"\limsup_{k \to -\infty} \frac{\sigma^2(k)\,T}{|k|}", r"=", r"2 - 4\big(\sqrt{\tilde q^2 + \tilde q} - "
                      r"\tilde q\big)", font_size=32, colors={r"\limsup_{k \to -\infty} \frac{\sigma^2(k)\,T}{|k|}": LEE_C}),
                cmath(r"\tilde q = -p^*(T)", r"\Rightarrow", r"\text{the wings follow from } T^*(p)", font_size=30,
                      colors={r"\tilde q = -p^*(T)": BAD})]
        whys = [why(r"the left critical moment: how many inverse powers of the price have a finite mean"),
                why(r"Lee (2004): the total implied variance grows at most linearly in log-moneyness (Part 12), and its "
                    r"slope is fixed by the critical moment; fat tails, $\tilde q \to 0$, give the maximum slope 2; thin "
                    r"tails, $\tilde q \to \infty$, a flat wing"),
                why(r"at maturity $T$ the critical moment is where $T^*(p) = T$; for Heston the lim sup is a limit (Benaim "
                    r"and Friz 2008), so the explosion times are the wings' slopes")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Now connect the moments to the smile. <bookmark mark='a'/> Define the left critical moment: how many "
            "inverse powers of the price still have a finite mean. <bookmark mark='b'/> Roger Lee's moment formula of "
            "2004, which Part 12 used as a no-arbitrage bound, is sharper than a bound: the slope of the total implied "
            "variance in the far wing is fixed by the critical moment. Fat tails give the maximum slope, two; thin tails "
            "a flat wing. <bookmark mark='c'/> At maturity T the critical moment is where the explosion time equals T. "
            "Shalom Benaim and Peter Friz showed that for Heston the limit exists. So the explosion times are the "
            "slopes of the wings, in closed form."
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

    def wing(self, t):
        w = t["wing"]
        k = np.asarray(w["k"])
        g = axes([0, 8.2], [0.14, 0.24], x_length=8.2, y_length=4.0, xlabel=r"distance into the left wing, $|k| = "
                 r"-\log(K/F)$", ylabel=r"slope of total implied variance", xticks=[0, 2, 4, 6, 8],
                 yticks=[0.14, 0.16, 0.18, 0.2, 0.22, 0.24], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        a1 = curve(ax, k, np.clip(w["w_over_k"], 0.14, 0.24), IV, stroke_width=3)
        a2 = curve(ax, k[1:], np.asarray(w["dw_dk"])[1:], VAR, stroke_width=3)
        lee = DashedLine(ax.c2p(0, w["lee"]), ax.c2p(8.2, w["lee"]), color=LEE_C, stroke_width=2.5)
        leg = legend([(IV, r"$w(k)/|k|$"), (VAR, r"$dw/d|k|$"), (LEE_C, rf"Lee's limit, {w['lee']:.3f}")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"the textbook Heston at $T = {w['T']:g}$, priced by COS out to $K = e^{{-8}}F$; "
                             rf"$p^*(1) = {w['p_crit']:.2f}$. The approach is slow, like $|k|^{{-1/2}}$ (Gulisashvili and "
                             r"Stein 2010; Friz, Gerhold, Gulisashvili and Sturm 2011)", 3.3, 14, GREY_A).next_to(
            leg, DOWN, buff=0.3)
        fit_right(side)
        dk = np.asarray(w["dw_dk"])
        with self.voiceover(
            "Check it on the model's own smile, priced far into the left wing. <bookmark mark='a'/> Lee's limit from "
            f"the critical moment: {w['lee']:.3f}. <bookmark mark='b'/> The local slope of the total variance comes down "
            f"towards it, {dk[4]:.3f} at one and a quarter, {dk[-1]:.3f} at eight, and the average slope more slowly. "
            "The convergence is slow, like one over the square root of the distance, which is why a smile observed "
            "out to a few strikes says less about the true tail than it seems."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(lee), FadeIn(leg[2]))
            vo.wait_until("b")
            self.play(Create(a2), FadeIn(leg[1]), Create(a1), FadeIn(leg[0]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def btc(self, t):
        rows = t["btc"]["rows"]
        hx = [-4.8, -2.6, -0.4, 1.8, 4.0, 5.9]
        head = VGroup(label(r"expiry", font_size=18, color=GREY_B), label(r"$T$", font_size=20),
                      label(r"observed slope", font_size=18, color=IV), label(r"Lee, Heston fit", font_size=18, color=LEE_C),
                      label(r"fit's $p^*$", font_size=18, color=BAD), label(r"implied $\tilde q$", font_size=18, color=SPOT))
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(label(r_["expiry"], font_size=18),
                                                 MathTex(rf"{r_['T']:.2f}", font_size=24),
                                                 MathTex(rf"{r_['slope_left']:.3f}", font_size=24),
                                                 MathTex(rf"{r_['lee_left']:.3f}", font_size=24),
                                                 MathTex(rf"{r_['p_left']:.2f}", font_size=24),
                                                 MathTex(rf"{r_['implied_q_left']:.1f}", font_size=24)) for r_ in rows]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.0 - 0.62 * j, 0])
            tab.add(row)
        fit = t["btc"]["fit"]
        foot = wrapped_label(rf"the Surface, 10 December 2025, left wing: the slope of total variance on the outer quarter of "
                             rf"each expiry's put strikes; the Heston fit of Chapter 3 ($\xi = {fit['xi']:.1f}$, $\rho = "
                             rf"{fit['rho']:.2f}$) saw these quotes, so agreement is consistency, not a test. Implied "
                             r"$\tilde q$: Lee's formula inverted, $\tilde q = (2 - \beta)^2/(8\beta)$", 11.8, 15,
                             GREY_A).to_edge(DOWN, buff=0.4)
        last = rows[-1]
        with self.voiceover(
            "And Bitcoin. Take the Heston fit of Chapter 3, with its huge volatility of volatility, and compute its "
            "critical moments at each listed expiry. <bookmark mark='a'/> Lee's slopes from those moments sit close "
            "to the slopes of the Surface's outer put wings. That is consistency, not a test: the fit saw these "
            "quotes. <bookmark mark='b'/> But read the other way, Lee's formula inverted turns a wing into a tail: the "
            "market prices Bitcoin as if the inverse moments of its price were finite only up to about "
            f"{rows[0]['implied_q_left']:.0f} at six weeks and about {last['implied_q_left']:.0f} at nine months."
        ) as vo:
            self.play(FadeIn(VGroup(*[r_[:5] for r_ in tab])), FadeIn(foot))
            vo.wait_until("a")
            self.play(*[Indicate(VGroup(r_[2], r_[3]), color=LEE_C) for r_ in tab[1:]])
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*[r_[5] for r_ in tab])))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: explosions beyond affine models", r"for rough volatility (Part 14) and for stochastic "
                          r"local volatility, critical moments have no Riccati equation; bounds exist (Gerhold, Gerstenecker "
                          r"and Pinter 2019 for rough Heston) but exact wings are mostly open", width=12.4, font_size=18),
            desk_question(r"open: the rate of convergence in practice", r"the second-order terms that make $w(k)/|k|$ "
                          r"approach Lee's slope slowly are known for Heston; using them to extrapolate a market smile "
                          r"robustly from a few strikes is unsettled", width=12.4, font_size=18),
            desk_question(r"open: tails under P and under Q", r"the risk-neutral tail implied by the wings and the "
                          r"real-world tail of returns (Part 1's cubic law) need not match; their gap is a price of crash "
                          r"risk that is hard to measure", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> Beyond affine models, for rough volatility or stochastic local "
            "volatility, there is no Riccati equation; bounds exist, but exact wings are mostly open. "
            "<bookmark mark='b'/> The second-order terms that make the convergence slow are known for Heston; using "
            "them to extrapolate a market smile from a few strikes is unsettled. <bookmark mark='c'/> And the "
            "risk-neutral tail implied by the wings need not match the real-world tail of returns, Part 1's cubic law. "
            "The gap between them is a price of crash risk, and it is hard to measure."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"with Lee's formula, what wing slope does a critical moment $\tilde q = 2$ give? What happens as "
                       r"$\tilde q \to 0$, and as $\tilde q \to \infty$?")
        with self.voiceover(
            "Pause and predict. Using Lee's formula, what wing slope does a critical moment of two give? And what "
            "happens as it goes to zero, and to infinity?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
