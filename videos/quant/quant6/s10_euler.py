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
            "The most famous moment condition in finance. An investor who can save one more dollar, in stocks or "
            "bills, is indifferent at the margin: the marginal utility given up today equals the discounted marginal "
            "utility of what the dollar buys tomorrow. So the discount factor m, patience beta times consumption growth to "
            "the power minus gamma, times the return, averages one. Gamma is risk aversion. <bookmark mark='a'/> It holds "
            "given anything known today, so by the tower property, multiply the error by today's instruments, a constant, "
            "last quarter's consumption growth and market return, and the products average zero too. Two assets times "
            "three instruments: six moments, two parameters, four left to test. <bookmark mark='b'/> And for an excess "
            "return the condition says the premium is minus the covariance of m with the return: a premium must be "
            "earned by covarying with consumption. Hansen and Kenneth Singleton estimated this in 1982."
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
            "The House's two-step GMM: minimise with the identity weight; from that estimate build S with Bartlett "
            "weights; reweight by S inverse and minimise again; the Jacobian gives standard errors, the leftover gives "
            "J. <bookmark mark='a'/> On seventy-three years of American consumption, stocks and bills: patience "
            f"{g['beta']:.3f}, risk aversion {g['gamma']:.1f} with a standard error of {g['se'][1]:.1f}, and J of "
            f"{g['J']:.0f} on {g['df']} degrees of freedom, a p-value of {g['p_J']:.4f}. Rejected."
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
            "Why is gamma so uncertain? Look at the objective. <bookmark mark='a'/> Across beta it is a steep valley: "
            "the bill pins patience down. Along gamma the floor is almost flat, a ridge, in pink. "
            "<bookmark mark='b'/> Let the optimiser roll a ball: it finds the valley in a few steps, then wanders along "
            "the floor. <bookmark mark='c'/> Weak identification, as James Stock and Jonathan Wright called it in 2000: "
            "the data barely know gamma, and the usual normal approximation fails on a ridge."
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
                                                                  FadeOut(hint), FadeOut(note_)], run_time=0.6)
        self.clear_scene(run_time=0.1)

    def montecarlo(self, mc, g):
        gh = np.asarray(mc["gamma_hat"])
        q = mc["q"]
        gax = axes([-60, 60], [0, 0.10], x_length=6.0, y_length=3.8, xlabel=r"$\hat\gamma$ in a simulated economy "
                   r"(true $\gamma = 2$)", ylabel=r"density, full Monte Carlo sample", xticks=[-50, -25, 0, 25, 50], yticks=[], font_size=16).to_edge(LEFT, buff=0.6)
        gax.shift(DOWN * 0.2)
        ax = gax.ax
        edges = np.linspace(-60, 60, 49)
        n = ValueTracker(1)
        hb = always_redraw(lambda: hist_bars(ax, gh[:max(int(n.get_value()), 1)], edges, EST, density=True, total=len(gh)))
        cnt = always_redraw(lambda: MathTex(rf"\text{{economies revealed: }} {int(n.get_value())}/{len(gh)}", font_size=26,
                                            color=GREY_A).next_to(gax, UP, buff=0.05).align_to(gax, RIGHT))
        truth = DashedLine(ax.c2p(2, 0), ax.c2p(2, 0.10), color=GOOD, stroke_width=3)
        side = VGroup(
            label(r"400 economies where the model is true", font_size=23, color=WHITE),
            wrapped_label(rf"$\beta = 1$, $\gamma = 2$, lognormal consumption and returns with the data's volatilities "
                          rf"and correlation; {mc['n']} quarters each", 5.6, 19, GREY_B),
            MathTex(rf"\hat\gamma:\ 5\%\text{{--}}95\%\ \text{{range}}\ {q[0]:.0f}\ \text{{to}}\ {q[4]:.0f}", font_size=28,
                    color=EST),
            MathTex(rf"\text{{95\% intervals cover }} \gamma:\ {100 * mc['cover_gamma']:.0f}\%", font_size=28, color=GOOD),
            MathTex(rf"J > \chi^2_{{4, 0.95}}:\ {100 * mc['rej_J']:.1f}\%\ \text{{of economies}}", font_size=28,
                    color=ALT),
            MathTex(rf"\text{{largest simulated }} J: {max(mc['J']):.1f};\ \ \text{{the data's: }} {g['J']:.1f}",
                    font_size=28, color=BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        if side.width > 6.0:  # the column must clear the histogram on the left
            side.scale_to_fit_width(6.0)
        side.to_edge(RIGHT, buff=0.35)
        beyond = ("beyond every one of them. This is strong evidence against the joint moment restrictions in this specification, subject to the sampling and estimation assumptions." if g["J"] > max(mc["J"])
                  else "large, but not beyond what a true model sometimes produces.")
        with self.voiceover(
            "How bad at our sample size? Build four hundred economies where the model is exactly true, gamma two, with "
            f"the data's volatilities and correlation, {mc['n']} quarters each, and estimate each one. "
            f"<bookmark mark='a'/> The estimates of gamma spread from {q[0]:.0f} to {q[4]:.0f} in the middle ninety "
            f"percent. Our {g['gamma']:.1f} is no surprise. <bookmark mark='b'/> But J is informative: in true worlds it "
            f"exceeds its five percent critical value {100 * mc['rej_J']:.1f} percent of the time and never passes "
            f"{max(mc['J']):.0f}. The data's J is {g['J']:.0f}, {beyond}"
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
            f"Why it fails. Stocks earned about {100 * g['equity_premium_q']:.0f} percent a quarter over bills; "
            "consumption is smooth, about one percent a quarter, and barely moves with stocks: correlation "
            f"{g['corr_g_rm']:.2f}. Risk aversion would need to be about {g['hj_gamma']:.0f}: Mehra and Prescott's equity "
            "premium puzzle, 1985. <bookmark mark='a'/> Pause and predict: with only the T-bill's moments, is gamma "
            "identified? <bookmark mark='b'/> Barely. The bill pins patience; risk aversion needs the risky asset's "
            "covariance with consumption, and it is tiny."
            " From the economy's average investor to single news days. Next: event studies."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.5, run_time=4))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
        self.wait(0.4)
        self.clear_scene()
