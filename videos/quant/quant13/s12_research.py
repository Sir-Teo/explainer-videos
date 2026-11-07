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
        self.play(FadeOut(c), run_time=0.35)

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
        self.clear_scene(run_time=0.35)

    def tstar_plot(self, t):
        g = axes([-10, 16], [0, 12], x_length=8.4, y_length=4.2, xlabel=r"moment $p$ of the price, $\mathbb E[S_T^p]$",
                 ylabel=r"explosion time $T^*(p)$, years", xticks=[-10, -5, 0, 1, 5, 10, 15], yticks=[0, 3, 6, 9, 12],
                 font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        pn, tn = np.asarray(t["p_neg"]), np.asarray(t["tstar_neg"], float)
        ok = np.isfinite(tn)
        left = curve(ax, pn[ok], tn[ok], LEFT_C, stroke_width=3)
        pp, tp = np.asarray(t["p_pos"]), np.asarray(t["tstar_pos"], float)
        okp = np.isfinite(tp)
        right = curve(ax, pp[okp], tp[okp], RIGHT_C, stroke_width=3) if okp.sum() > 2 else VGroup()
        dots = VGroup(*[Dot(ax.c2p(c["p"], c["ode"]), radius=0.07, color=WHITE) for c in t["ode_check"]
                        if c["ode"] and c["ode"] <= 12])
        band = Rectangle(width=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 12)[1] - ax.c2p(0, 0)[1],
                         stroke_width=0, fill_color=GREY_D, fill_opacity=0.5).move_to(ax.c2p(0.5, 6))
        blab = label(r"$0 \le p \le 1$: always finite", font_size=14, color=GREY_B).next_to(band, UP, buff=0.05)
        tb = t["textbook"]
        leg = legend([(LEFT_C, r"negative moments: the crash side"), (RIGHT_C, r"$p > 1$: the upper tail"),
                      (WHITE, r"an ODE solver's blow-up time")], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label('Textbook Heston: $\\kappa=2$, $\\theta=0.04$, $\\xi=1$, $\\rho=-0.7$. For positive $p>1$, moments up to about 8.4 remain finite at all times. All finite saved explosion times are shown; other regions have $T^*=\\infty$.', 3.3, 14,
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
        self.clear_scene(run_time=0.35)

    def sample(self, t):
        sm = t["sample_moment"]
        g = axes([2, 5.4], [0, 40], x_length=8.2, y_length=4.0, xlabel=r"number of simulated paths",
                 ylabel=r"running sample mean of $S_T^{-3}$", xticks=[2, 3, 4, 5], yticks=[0, 10, 20, 30, 40],
                 xfmt=lambda v: f"10^{{{int(v)}}}", font_size=15, log_x=True).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        cols = {"before": RIGHT_C, "after": LEFT_C}
        lines = VGroup()
        for k in ("before", "after"):
            r = sm["runs"][k]
            y = np.asarray(r["running_mean"])
            lines.add(curve(ax, np.log10(r["n"]), y, cols[k], stroke_width=3))
        b, a = sm["runs"]["before"], sm["runs"]["after"]
        leg = legend([(cols["before"], rf"$T = {b['T']:.2f}$, before $T^*$"), (cols["after"], rf"$T = {a['T']:.2f}$, after")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label('Finite QE experiment, 200{,}000 paths. Curves use $0.5T^*$ and $1.6T^*$. Analytic continuous-model integrability is not determined by this sample.', 3.3, 14, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"""Consider the inverse-cube payoff, S to the minus three. Its continuous-time Heston expectation is finite before the analytic explosion time and infinite afterwards. <bookmark mark='a'/> The first saved running mean uses half that time. <bookmark mark='b'/> The second uses one point six times it, with large jumps and a largest-path share of {100 * a['max_share']:.0f} percent. These are finite, time-discretized QE samples; an unstable-looking sample is not a proof of an infinite expectation, nor does apparent stability prove finiteness. The analytic moment result supplies the conclusion about the continuous model. A bounded far-out put does not inherit an inverse-power explosion. Nor may a variance swap or log payoff be classified as an inverse power without a separate integrability argument."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(side), Create(lines[0]), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(lines[0]))
            vo.wait_until("b")
            self.play(Create(lines[1]), FadeIn(leg[1]), run_time=2)
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def lee(self):
        rows = [cmath(r"\tilde q", r"=", r"\sup\{q : \mathbb E[S_T^{-q}] < \infty\}", font_size=32, colors={r"\tilde q": LEFT_C}),
                cmath(r"\limsup_{k \to -\infty} \frac{\sigma^2(k)\,T}{|k|}", r"=", r"2 - 4\big(\sqrt{\tilde q^2 + \tilde q} - "
                      r"\tilde q\big)", font_size=32, colors={r"\limsup_{k \to -\infty} \frac{\sigma^2(k)\,T}{|k|}": LEE_C}),
                cmath(r"\tilde q = -p^*(T)", r"\Rightarrow", r"\text{the wings follow from } T^*(p)", font_size=30,
                      colors={r"\tilde q = -p^*(T)": BAD})]
        whys = [why(r"the left critical moment: how many inverse powers of the price have a finite mean"),
                why('Lee (2004): a limsup ratio $w(k)/|k|$, not a general local-derivative limit. Critical exponents alone do not settle boundary integrability.'),
                why('Heston critical moments follow its Riccati boundary; regular tail asymptotics justify an actual ratio limit and derivative behavior.')]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            """Connect integrability to an asymptotic wing. <bookmark mark='a'/> The critical inverse moment is the supremum of q for which the inverse-power expectation is finite; it does not alone settle finiteness at the boundary. <bookmark mark='b'/> Lee's formula gives the limsup of total implied variance divided by absolute log strike. It is not, in general, a statement that a local derivative converges. As the critical moment approaches zero this ratio bound approaches two; as it tends to infinity it approaches zero. <bookmark mark='c'/> Heston's Riccati explosion boundary identifies the critical exponent. Stronger Heston tail asymptotics justify a true ratio limit and the corresponding derivative behavior. Those extra conclusions should not be transferred to arbitrary models."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene(run_time=0.35)

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
        side = wrapped_label("Textbook Heston at $T=1$, COS prices through $K=e^{-8}F$. The ratio and derivative need stronger tail asymptotics than Lee's general limsup formula.", 3.3, 14, GREY_A).next_to(
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
            self.play(FadeIn(g), FadeIn(side), Create(lee), FadeIn(leg[2]))
            vo.wait_until("a")
            self.play(Indicate(lee))
            vo.wait_until("b")
            self.play(Create(a2), FadeIn(leg[1]), Create(a1), FadeIn(leg[0]), run_time=2)
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def btc(self, t):
        rows = t["btc"]["rows"]
        hx = [-4.8, -2.6, -0.4, 1.8, 4.0, 5.9]
        head = VGroup(label(r"expiry", font_size=18, color=GREY_B), label(r"$T$", font_size=20),
                      label(r"observed slope", font_size=18, color=IV), label(r"Lee, Heston fit", font_size=18, color=LEE_C),
                      label(r"fit's $p^*$", font_size=18, color=BAD), label('extrapolated $q$ proxy', font_size=18, color=SPOT))
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
        foot = wrapped_label('Outer-quarter finite-strike slopes from pooled marks, 10 December 2025. Inverting Lee requires extrapolating them as asymptotic slopes: $q=(2-\\beta)^2/(8\\beta)$. These are proxies, not identified market moments.', 11.8, 15,
                             GREY_A).to_edge(DOWN, buff=0.4)
        last = rows[-1]
        with self.voiceover(
            f"""Compare finite quoted wings with a fitted model's asymptotic prediction. <bookmark mark='a'/> Heston saw these input marks, so proximity is an in-sample consistency observation. More fundamentally, the observed outer-quarter slope is at finite strikes, while Lee's relation concerns infinite log-strike distance. <bookmark mark='b'/> Inverting that finite slope gives proxy q values of {rows[0]['implied_q_left']:.0f} and {last['implied_q_left']:.0f} at the short and long displayed expiries, only if one extrapolates it as an asymptotic slope. Many tails can agree on the observed interval. These proxies do not identify the market's true critical moments or establish which inverse-power payoffs have finite expectations."""
        ) as vo:
            self.play(FadeIn(VGroup(*[r_[:5] for r_ in tab])), FadeIn(foot))
            vo.wait_until("a")
            self.play(*[Indicate(VGroup(r_[2], r_[3]), color=LEE_C) for r_ in tab[1:]])
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*[r_[5] for r_ in tab])))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: explosions beyond affine models", 'Rough Heston has a fractional/Volterra Riccati equation; sharp tail results for broader rough and SLV models remain difficult.', width=12.4, font_size=18),
            desk_question(r"open: the rate of convergence in practice", r"the second-order terms that make $w(k)/|k|$ "
                          r"approach Lee's slope slowly are known for Heston; using them to extrapolate a market smile "
                          r"robustly from a few strikes is unsettled", width=12.4, font_size=18),
            desk_question(r"open: tails under P and under Q", '$Q$ and $P$ tails can differ; observed differences do not isolate a crash-risk premium without further assumptions.', width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            """Three further questions. <bookmark mark='a'/> Rough Heston has a fractional, or Volterra, Riccati equation. Extending sharp critical-moment and wing results to broader rough and stochastic-local models remains difficult. <bookmark mark='b'/> Heston's second-order tail corrections are known, but robustly extrapolating a sparse market smile still needs assumptions and uncertainty analysis. <bookmark mark='c'/> Pricing-measure and physical tails need not match. Their difference can reflect risk compensation, changing states and model error; a single fitted wing and a historical tail estimate do not isolate a crash-risk premium."""
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def question(self):
        q = pause_card(r"with Lee's formula, what wing slope does a critical moment $\tilde q = 2$ give? What happens as "
                       r"$\tilde q \to 0$, and as $\tilde q \to \infty$?")
        with self.voiceover(
            "Pause and predict. Using Lee's formula, what wing slope does a critical moment of two give? And what "
            "happens as it goes to zero, and to infinity?"
        ):
            self.play(FadeIn(q))
        self.wait(3.0)
        answer = MathTex(r"\beta(2)=2-4(\sqrt6-2)\approx0.202,\quad \beta(0^+)=2,\quad \beta(\infty)=0", font_size=32, color=LEE_C)
        answer.to_edge(DOWN, buff=1.2)
        with self.voiceover('For q equal to two, the slope is two minus four times root six minus two, about zero point two zero two. As q decreases to zero the ratio tends to two; as q grows without bound it tends to zero. These are asymptotic total-variance ratios.'):
            self.play(FadeIn(answer))
        self.wait(0.5)
        self.clear_scene(run_time=0.35)
