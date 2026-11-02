from __future__ import annotations

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, hist_bars, load, predict, real_data, show_card

GMM_CODE = [
    "# condensed from econ.gmm: two steps",
    "obj = lambda th, W: g(th).mean(0) @ W @ g(th).mean(0)",
    "th1 = minimize(obj, th0, args=(I,)).x          # step 1: identity weight",
    "G = g(th1) - g(th1).mean(0); S = G.T @ G / n   # + Bartlett-weighted lags",
    "th = minimize(obj, th1, args=(inv(S),)).x      # step 2: efficient weight",
    "D = jacobian(lambda t: g(t).mean(0), th)",
    "V = inv(D.T @ inv(S) @ D) / n                  # se = sqrt(diag(V))",
    "J = n * obj(th, inv(S))                        # ~ chi2(q - p)",
]


class Euler(VoiceoverScene, ThreeDScene):
    def construct(self):
        g = load("gmm")
        sf = load("gmm_surface")
        mc = load("gmm_mc")
        self.card()
        self.derive(g)
        self.lab(g)
        self.surface(sf, g)
        self.montecarlo(mc, g)
        self.puzzle(g)

    def card(self):
        c = chapter_card(9, r"The Euler equation, estimated and rejected", r"Can a model of investors explain returns?",
                         lit=(1982,), part=PART)
        with self.voiceover("Chapter nine. The consumption Euler equation, estimated and rejected."):
            show_card(self, c)
        self.play(FadeOut(c))

    def derive(self, g):
        C_ = {r"\gamma": EST, r"\beta": EST, r"z_t": ALT}
        rows = [cmath(r"\mathbb{E}_t\big[m_{t+1} R_{t+1}\big] = 1", r",", r"\ m_{t+1} = \beta \Big(\frac{C_{t+1}}{C_t}"
                      r"\Big)^{-\gamma}", font_size=36, colors=C_),
                cmath(r"\mathbb{E}\big[(m_{t+1} R_{t+1} - 1) \otimes z_t\big]", r"=", r"0", font_size=36, colors=C_),
                cmath(r"\mathbb{E}[R^e]", r"=", r"-\frac{\mathrm{cov}(m, R^e)}{\mathbb{E}[m]} \approx \gamma\,"
                      r"\mathrm{cov}(\Delta c, R^e)", font_size=36, colors=C_)]
        whys = [why(r"the first-order condition for saving one more dollar: marginal utility given up today equals "
                    r"the discounted marginal utility of what it buys"),
                why(r"tower property: anything known at $t$ (instruments $z_t$) times the error averages to zero; "
                    r"2 assets $\times$ 3 instruments = 6 moments for 2 parameters"),
                why(r"for an excess return $\mathbb{E}[m R^e] = 0$; log-linearise $m$: the premium must be paid by a "
                    r"covariance with consumption")]
        step = ladder(self, rows, whys, keep=3, top=2.5, x=-0.6, buff=1.0, edge=6.8)
        with self.voiceover(
            "Here is the most famous moment condition in finance. An investor who can save one more dollar, in "
            "stocks or in bills, is indifferent at the margin: the stochastic discount factor m, patience beta "
            "times the growth of consumption to the power minus gamma, times the return, averages one. Gamma is "
            "risk aversion. <bookmark mark='a'/> The condition holds given anything known today, so multiply the "
            "error by instruments known today: a constant, last quarter's consumption growth and market return. "
            "Two assets times three instruments: six moments for two parameters, four left over to test. "
            "<bookmark mark='b'/> And it says how a premium must be earned: by covarying with consumption. Lars "
            "Hansen and Kenneth Singleton estimated exactly this by GMM in 1982."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def lab(self, g):
        card = lab_card(r"two-step GMM in the House", GMM_CODE, source="explainer/quant/house/econ.py (condensed)",
                        width=8.6, font_size=18).to_corner(UL, buff=0.35)
        outs = [f"beta  = {g['beta']:.3f}  (se {g['se'][0]:.3f})",
                f"gamma = {g['gamma']:.1f}    (se {g['se'][1]:.1f})",
                f"J = {g['J']:.1f}, {g['df']} df, p = {g['p_J']:.4f}"]
        src = real_data(r"FRED: real PCE per capita (A794RX0Q048SBEA), CPI; French: market and T-bill; quarterly "
                        r"1947--2020")
        with self.voiceover(
            "The House's GMM in eight lines. The objective is the moments' length in the weight W. Step one uses "
            "the identity. From that estimate, build the moments' long-run covariance S, with chapter two's "
            "Bartlett weights. Step two reweights by S inverse and minimises again. The Jacobian gives the "
            "standard errors, and the leftover gives J. <bookmark mark='a'/> Run it on seventy-three years of "
            "American data: real consumption per person from the national accounts, the stock market and the "
            f"Treasury bill. Patience: {g['beta']:.3f}. Risk aversion: {g['gamma']:.1f}, with a standard error of "
            f"{g['se'][1]:.1f}. And J is {g['J']:.0f} on {g['df']} degrees of freedom: a p-value of "
            f"{g['p_J']:.4f}. The model is rejected."
        ) as vo:
            self.play(FadeIn(card), FadeIn(src))
            vo.wait_until("a")
            lab_run(self, card, outs, run_time=2.4)
        self.wait(0.4)
        self.clear_scene()

    def surface(self, sf, g):
        bs, gs, J = np.asarray(sf["beta"]), np.asarray(sf["gamma"]), np.asarray(sf["J"])
        Z = np.log10(J)
        itp = RegularGridInterpolator((gs, bs), Z)
        zlo, zhi = float(Z.min()), float(np.percentile(Z, 97))
        f = lambda b, gg: float(min(itp([[np.clip(gg, gs[0], gs[-1]), np.clip(b, bs[0], bs[-1])]])[0], zhi))  # noqa: E731
        ax = ThreeDAxes(x_range=[bs[0], bs[-1], 0.02], y_range=[gs[0], gs[-1], 10], z_range=[zlo, zhi, 1], x_length=7,
                        y_length=6, z_length=3, tips=False, axis_config={"stroke_color": GREY_D,
                                                                          "include_ticks": False, "stroke_width": 1.5})
        surf = loss_surface(ax, f, (bs[0], bs[-1]), (gs[0], gs[-1]), resolution=(30, 30), z_lo=zlo, z_hi=zhi)
        path = [(float(np.clip(b, bs[0], bs[-1])), float(np.clip(gg, gs[0], gs[-1]))) for b, gg in sf["path"]]
        k = ValueTracker(0)
        ball = always_redraw(lambda: surface_ball(ax, f, *path[int(k.get_value())], color=YELLOW, radius=0.12))
        trail = always_redraw(lambda: surface_path(ax, f, path[:int(k.get_value()) + 1] + [path[int(k.get_value())]],
                                                   color=YELLOW, stroke_width=4))
        ridge = surface_path(ax, f, [(b, r) for b, r in zip(bs, sf["ridge"]) if gs[0] <= r <= gs[-1]], color=ALT,
                             stroke_width=4, lift=0.06)
        hint = VGroup(
            label(r"the GMM objective $J(\beta, \gamma)$, log scale", font_size=22, color=WHITE),
            label(r"across: patience $\beta$ (0.96 to 1.04); depth: risk aversion $\gamma$ ($-10$ to 40)",
                  font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        note_ = wrapped_label(r"a valley sharp in $\beta$, an almost flat ridge in $\gamma$: weak identification "
                              r"(Stock and Wright 2000)", 5.0, 21, ALT).to_corner(DR, buff=0.4)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-115 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint, note_)
        self.remove(hint, note_)
        with self.voiceover(
            "Why is the standard error on gamma so large? Look at the objective itself, over patience and risk "
            "aversion. <bookmark mark='a'/> Across beta it is a steep-walled valley: the T-bill pins patience down "
            "almost exactly. Along gamma, the valley floor is nearly flat, a long ridge in orange. "
            "<bookmark mark='b'/> Drop a ball and let the optimiser roll it. It finds the valley in a few steps, "
            "then wanders along the floor, where moving gamma by ten barely changes the fit. "
            "<bookmark mark='c'/> This is weak identification, as James Stock and Jonathan Wright called it in "
            "2000: the data barely know gamma, and on a ridge like this the usual normal approximation for its "
            "standard error is unreliable."
        ) as vo:
            self.play(FadeIn(hint), Create(ax), run_time=1.2)
            vo.wait_until("a")
            self.play(Create(surf), run_time=2.5)
            self.play(Create(ridge))
            vo.wait_until("b")
            self.add(trail, ball)
            self.play(k.animate.set_value(len(path) - 1), run_time=vo.until("c"), rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(note_))
            self.move_camera(theta=-150 * DEGREES, run_time=max(vo.remaining(1.0) - 0.5, 1.0))
        for x in (ball, trail):
            x.clear_updaters()
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, surf, ball, trail, ridge)),
                                                                  FadeOut(hint), FadeOut(note_)], run_time=1.2)
        self.clear_scene()

    def montecarlo(self, mc, g):
        gh = np.asarray(mc["gamma_hat"])
        q = mc["q"]
        gax = axes([-60, 60], [0, 0.04], x_length=6.8, y_length=3.8, xlabel=r"$\hat\gamma$ in a simulated economy "
                   r"(true $\gamma = 2$)", xticks=[-50, -25, 0, 25, 50], yticks=[], font_size=16).to_edge(LEFT, buff=0.6)
        gax.shift(DOWN * 0.2)
        ax = gax.ax
        edges = np.linspace(-60, 60, 49)
        n = ValueTracker(1)
        hb = always_redraw(lambda: hist_bars(ax, gh[:max(int(n.get_value()), 1)], edges, EST, density=True, cap=0.04))
        cnt = always_redraw(lambda: MathTex(rf"\text{{economies: }} {int(n.get_value())}", font_size=26,
                                            color=GREY_A).next_to(gax, UP, buff=0.05).align_to(gax, RIGHT))
        truth = DashedLine(ax.c2p(2, 0), ax.c2p(2, 0.04), color=GOOD, stroke_width=3)
        side = VGroup(
            label(r"400 economies where the model is true", font_size=23, color=WHITE),
            label(rf"$\beta = 1$, $\gamma = 2$, lognormal consumption and returns with the data's volatilities and "
                  rf"correlation; {mc['n']} quarters each", font_size=19, color=GREY_B),
            MathTex(rf"\hat\gamma:\ 5\%\text{{--}}95\%\ \text{{range}}\ {q[0]:.0f}\ \text{{to}}\ {q[4]:.0f}", font_size=28,
                    color=EST),
            MathTex(rf"\text{{95\% intervals cover }} \gamma:\ {100 * mc['cover_gamma']:.0f}\%", font_size=28, color=GOOD),
            MathTex(rf"J > \chi^2_{{4, 0.95}}:\ {100 * mc['rej_J']:.1f}\%\ \text{{of economies}}", font_size=28,
                    color=ALT),
            MathTex(rf"\text{{largest simulated }} J: {max(mc['J']):.1f};\ \ \text{{the data's: }} {g['J']:.1f}",
                    font_size=28, color=BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        side[1].scale_to_fit_width(min(side[1].width, 5.6))
        beyond = ("beyond every one of them. The model is not just imprecise; it is wrong." if g["J"] > max(mc["J"])
                  else "large, but not beyond what a true model sometimes produces.")
        with self.voiceover(
            "How bad is it at our sample size? Build four hundred economies in which the model is exactly true, "
            "with patience one and risk aversion two, and consumption and stock returns as volatile and as weakly "
            f"correlated as in the data, each {mc['n']} quarters long. Estimate each one the same way. "
            "<bookmark mark='a'/> The estimates of gamma pile up around the truth, but the pile is enormous: from "
            f"{q[0]:.0f} to {q[4]:.0f} in the middle ninety percent. Our estimate of {g['gamma']:.1f} is no surprise "
            "in a world where gamma is two. <bookmark mark='b'/> The J test, though, is informative: in these true "
            f"worlds it exceeds its five percent critical value only {100 * mc['rej_J']:.1f} percent of the time, "
            f"and never reaches more than {max(mc['J']):.0f}. The real data's J is {g['J']:.0f}, "
            + beyond
        ) as vo:
            self.play(FadeIn(gax), Create(truth), FadeIn(side[0]), FadeIn(side[1]))
            self.add(hb, cnt)
            vo.wait_until("a")
            self.play(n.animate.set_value(len(gh)), run_time=4, rate_func=rate_functions.ease_in_quad)
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[4]))
            self.play(FadeIn(side[5]))
        hb.clear_updaters()
        cnt.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def puzzle(self, g):
        rows = VGroup(
            label(r"Why it fails", font_size=32),
            MathTex(rf"\text{{equity premium: }} {100 * g['equity_premium_q']:.1f}\% \text{{ a quarter}}", font_size=30),
            MathTex(rf"\text{{consumption growth: sd }} {100 * g['sd_g']:.1f}\%,\ \text{{corr. with stocks }} "
                    rf"{g['corr_g_rm']:.2f}", font_size=30),
            MathTex(rf"\gamma \approx \frac{{\mathbb{{E}}[R^e]}}{{\mathrm{{cov}}(\Delta c, R^e)}} \approx "
                    rf"{g['hj_gamma']:.0f}", font_size=36, color=BAD),
            label(r"the equity premium puzzle (Mehra and Prescott 1985); Hansen--Jagannathan bounds, habits and long-run "
                  r"risk in Part 23", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.7)
        q = predict(r"Use only the T-bill's moments. Can $\gamma$ be identified?").next_to(rows, DOWN, buff=0.5)
        with self.voiceover(
            "The reason is simple to see. Stocks have earned about "
            f"{100 * g['equity_premium_q']:.0f} percent a quarter more than bills, but consumption is smooth, with a "
            f"standard deviation of about one percent a quarter, and barely moves with the stock market: a "
            f"correlation of {g['corr_g_rm']:.2f}. From the last line of the derivation, risk aversion would have to "
            f"be about {g['hj_gamma']:.0f}. Rajnish Mehra and Edward Prescott called it the equity premium puzzle in "
            "1985. <bookmark mark='a'/> Pause and predict: with only the T-bill's moments, can gamma be identified? "
            "<bookmark mark='b'/> Barely. The bill pins down patience; it is the risky asset's covariance with "
            "consumption that carries information about risk aversion, and that covariance is tiny."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.5, run_time=4))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
        self.wait(0.4)
        self.clear_scene()
