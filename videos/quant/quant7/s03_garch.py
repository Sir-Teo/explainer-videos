from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data, predict


class Garch(VoiceoverScene, ThreeDScene):
    def construct(self):
        g = load("garch")
        gl = load("garch_lik")
        self.card()
        self.bucket(gl)
        self.derive()
        self.lab(g)
        self.surface(gl, load("garch_persist"))

    def card(self):
        c = chapter_card(6, r"ARCH and GARCH by maximum likelihood", r"How does volatility remember?", lit=(1982,),
                         part=PART)
        with self.voiceover("Chapter six. ARCH and GARCH, by maximum likelihood."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def bucket(self, gl):
        h, r = np.asarray(gl["bucket_h"]), np.asarray(gl["bucket_r"])
        w, a, b = gl["us"]
        w, n = w * 1e4, len(h)
        hist = history_card(1982, r"Robert Engle", r"ARCH, to model the uncertainty of UK inflation: the "
                            r"variance of today's surprise depends on yesterday's", color=QC.IDEA, width=5.0, font_size=19)
        hist.to_corner(UL, buff=0.3)
        H = 3.4
        top = 1.6
        box = VGroup(Line([-5.6, top, 0], [-5.6, top - H, 0]), Line([-5.6, top - H, 0], [-3.6, top - H, 0]),
                     Line([-3.6, top - H, 0], [-3.6, top, 0])).set_stroke(GREY_B, 4).shift(DOWN * 0.6)
        floor = top - H - 0.6
        scale = H / (1.05 * max(h.max(), w / (1 - a - b)))
        tr = ValueTracker(0)
        water = always_redraw(lambda: Rectangle(width=1.92, height=max(scale * h[int(tr.get_value())], 0.01), stroke_width=0,
                                                fill_color=VOL, fill_opacity=0.7).move_to([-4.6, floor + scale * h[int(tr.get_value())] / 2, 0]))
        bar_lr = scale * w / (1 - a - b)
        lr = DashedLine([-5.8, floor + bar_lr, 0], [-3.4, floor + bar_lr, 0], color=GOOD, stroke_width=3)
        lrl = label(r"long-run level $\omega/(1-\alpha-\beta)$", font_size=17, color=GOOD).next_to(lr, RIGHT, buff=0.1)
        tap = VGroup(Line([-5.2, top + 0.2, 0], [-5.2, top - 0.6, 0], color=GOOD, stroke_width=6),
                     label(r"tap $\omega$", font_size=18, color=GOOD).move_to([-5.2, top + 0.45, 0]))
        tap.shift(DOWN * 0.6)
        leak = VGroup(Arrow([-3.55, floor + 0.3, 0], [-2.9, floor - 0.1, 0], buff=0, color=BAD, stroke_width=3),
                      label(r"leak: keeps $\beta$", font_size=18, color=BAD).move_to([-2.6, floor - 0.35, 0]))
        splash = label(r"splash $\alpha r_t^2$", font_size=18, color=RET).move_to([-4.6, top + 0.15, 0])
        rmax = 1.05 * float(np.max(np.abs(r)))
        g = axes([0, n], [-rmax, rmax], x_length=7.2, y_length=3.0, xticks=[], yticks=[-4, 0, 4], font_size=14,
                 ylabel=r"each day's return, drawn with size $\propto\sqrt{\text{level}}$ (simulated, US parameters)")
        g.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.6)
        bars = VGroup(*[Line(g.ax.c2p(i, 0), g.ax.c2p(i, r[i]), stroke_width=1.6, color=RET)
                        for i in range(n)])
        with self.voiceover(
            "Robert Engle, on a sabbatical at the London School of Economics, wanted to model how uncertain British "
            "inflation was. His answer, published in 1982: the variance of today's surprise depends on yesterday's "
            "surprise. That is ARCH. "
            "<bookmark mark='a'/> Picture the variance as water in a bucket. A tap pours in a steady trickle, omega. "
            "Each night it keeps a fraction beta and leaks the rest. <bookmark mark='b'/> Each "
            "day a return is drawn, its size in proportion to the square root of the water level, and it splashes "
            "alpha times its square back in. <bookmark mark='c'/> Run it. A high level makes big returns, big returns "
            "make big splashes, and clusters appear by themselves. With positive omega, nonnegative coefficients and alpha plus beta below one, the conditional expected level reverts to the finite long-run variance; individual paths keep receiving shocks."
        ) as vo:
            self.play(FadeIn(hist))
            vo.wait_until("a")
            self.play(Create(box), FadeIn(tap), FadeIn(leak), FadeIn(g))
            self.add(water)
            vo.wait_until("b")
            self.play(FadeIn(splash))
            vo.wait_until("c")
            self.play(tr.animate.set_value(n - 1), LaggedStart(*[Create(b) for b in bars], lag_ratio=1.0),
                      run_time=max(vo.remaining(1.0) - 1.5, 4), rate_func=linear)
            self.play(Create(lr), FadeIn(lrl))
        water.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"r_t = \sigma_t z_t", r",", r"\ \sigma_t^2 = \omega + \alpha r_{t-1}^2 + \beta\sigma_{t-1}^2", font_size=36),
            cmath(r"\bar\sigma^2", r"=", r"\omega + (\alpha + \beta)\bar\sigma^2 \ \Rightarrow\ \bar\sigma^2 = \frac{\omega}{1 - \alpha - \beta}",
                  font_size=36),
            cmath(r"\sigma_t^2", r"=", r"\frac{\omega}{1-\beta} + \alpha\sum_{k\ge1}\beta^{k-1}r_{t-k}^2", font_size=36),
            cmath(r"\ell(\theta)", r"=", r"-\tfrac12\sum_t\Big[\ln 2\pi + \ln\sigma_t^2 + \frac{r_t^2}{\sigma_t^2}\Big]", font_size=36),
            cmath(r"\mathbb{E}_t\sigma_{t+h}^2", r"=", r"\bar\sigma^2 + (\alpha + \beta)^{h-1}(\sigma_{t+1}^2 - \bar\sigma^2)",
                  font_size=36),
            cmath(r"r_t^2", r"=", r"\omega + (\alpha + \beta)r_{t-1}^2 + \nu_t - \beta\nu_{t-1},\quad \nu_t = r_t^2 - \sigma_t^2",
                  font_size=36),
        ]
        whys = [why(r"the definition: Bollerslev (1986) added yesterday's variance to Engle's ARCH"),
                why(r"$\omega>0$, $\alpha,\beta\ge0$, $\alpha+\beta<1$, $\mathbb{E}_{t-1}z_t^2=1$: take expectations"),
                why(r"unroll: an exponentially weighted average of past squares, above a floor"),
                why(r"Gaussian densities multiplied day by day: the prediction-error decomposition"),
                why(r"the tower property: deviations from the long run decay at the rate $\alpha + \beta$"),
                why(r"substitute $\sigma^2=r^2-\nu$; covariance-ARMA interpretation also needs finite fourth moments")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-2.0, buff=0.5, edge=6.9)
        with self.voiceover(
            "The equations behind the bucket. Today's return is the volatility times a standard shock, and in 1986 Tim "
            "Bollerslev let the variance remember itself as well as yesterday's squared return: GARCH. <bookmark "
            "mark='a'/> Take expectations, and the long-run level is omega over one minus alpha minus beta. "
            "<bookmark mark='b'/> Unroll the recursion: the variance is an exponentially weighted average of all past "
            "squared returns, sitting above a floor. <bookmark mark='c'/> To fit it, write the Gaussian density of "
            "each day's return given its variance and multiply across days: the likelihood if shocks are normal, a quasi-likelihood otherwise. <bookmark mark='d'/> "
            "Forecasts revert to the long run at the rate alpha plus beta, <bookmark mark='e'/> and rewritten, GARCH "
            "has an ARMA identity for squared returns, with finite fourth moments needed for a covariance-ARMA interpretation. This helps explain why the last chapter's Ljung-Box test on squares failed so "
            "badly."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            vo.wait_until("e")
            step(5)
        self.wait(0.3)
        self.clear_scene()

    def lab(self, g):
        us = g["us"]
        w, a, b = us["garch"]["params"]
        card = lab_card(r"the GARCH filter and its likelihood", [
            "def garch_filter(params, r):",
            "    w, a, b = params",
            "    h = np.empty(len(r)); h[0] = np.var(r)",
            "    for t in range(1, len(r)):",
            "        h[t] = w + a * r[t-1]**2 + b * h[t-1]",
            "    return h",
            "def nll(params, r):",
            "    h = garch_filter(params, r)",
            "    return 0.5 * np.sum(np.log(2*np.pi*h) + r**2 / h)",
        ], source="explainer/quant/house/vol.py", width=6.6).to_corner(UL, buff=0.3)
        t, v, ab = np.asarray(g["t"]), np.asarray(g["vol_ann"]), np.asarray(g["absr_ann"])
        vmax = 1.05 * float(max(v.max(), ab.max()))
        gr = axes([1926, 2021], [0, vmax], x_length=6.4, y_length=2.8, ylabel=r"US market volatility, annualised",
                  xticks=[1930, 1960, 1990, 2020], xfmt=lambda u: f"{int(u)}", yticks=[0, 0.5, 1.0],
                  yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15).to_corner(DR, buff=0.4)
        dots = curve(gr.ax, t, ab, RET, stroke_width=1).set_stroke(opacity=0.3)
        tr = ValueTracker(0)
        line = tracing(gr.ax, t, v, tr, VOL, stroke_width=2.5)
        pc = predict(rf"$\alpha + \beta = {us['garch']['persistence']:.3f}$. After a shock, how many days until "
                        r"half of it is gone?", width=5.4, font_size=21).to_corner(UR, buff=0.3)
        with self.voiceover(
            "Lab. The House's GARCH is five lines of recursion and one line of likelihood; the optimiser does the "
            f"rest. <bookmark mark='a'/> On {g['n']:,} days of the American market, alpha comes out at about a tenth "
            "and beta at about nine tenths. <bookmark mark='b'/> Pause and predict: alpha plus beta is "
            f"{us['garch']['persistence']:.3f}. After a shock, how many days until half of it is gone? <bookmark "
            f"mark='c'/> {us['garch']['half_life']:.0f} trading days, about three months. And here is the fitted "
            "volatility, drawn day by day through the century."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, [">>> garch_fit(r)",
                                 f"omega = {w:.2e}, alpha = {a:.3f}, beta = {b:.3f}",
                                 f"log-likelihood = {us['garch']['loglik']:,.0f}"], run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(pc))
            vo.wait_until("c")
            self.play(FadeOut(pc), FadeIn(gr), FadeIn(dots))
            self.add(line)
            self.play(tr.animate.set_value(len(t) - 1), run_time=max(vo.remaining(1.0) - 0.3, 3), rate_func=linear)
        self.wait(0.3)
        self.clear_scene()

    def surface(self, gl, gp):
        # drawn over (alpha, persistence alpha + beta): every point is stationary, and the surface ends at
        # persistence one, where RiskMetrics sits
        from scipy.interpolate import RegularGridInterpolator
        A, Pp = np.asarray(gp["A"]), np.asarray(gp["P"])
        G = np.asarray(gp["grid"], float)
        top = float(np.nanmax(G))
        Z = np.clip(G - top, -4000, 0) / 1000.0
        f_ = RegularGridInterpolator((Pp, A), Z, bounds_error=False, fill_value=-4.0)
        lo_p, hi_p = float(Pp[0]), float(Pp[-1])

        def f(a, p_):
            return float(f_([[p_, a]])[0])

        ax3 = ThreeDAxes(x_range=[0.02, 0.22, 0.05], y_range=[lo_p, hi_p, 0.04], z_range=[-4, 0.5, 1], x_length=6.4,
                         y_length=6.4, z_length=2.5, axis_config={"stroke_color": GREY_C, "include_ticks": False})
        surf = loss_surface(ax3, f, (0.02, 0.22), (lo_p, hi_p), resolution=(28, 28), z_lo=-4, z_hi=0)
        alabs = VGroup(label(r"$\alpha$", font_size=26, color=GREY_B).move_to(ax3.c2p(0.245, lo_p, 0)),
                       label(r"persistence $\alpha + \beta$", font_size=20, color=GREY_B).move_to(ax3.c2p(0.02, hi_p + 0.03, 0)))
        P = np.asarray(gl["path"])
        LL = np.asarray(gl["path_ll"])
        Q = np.clip(np.column_stack([P[:, 0], P[:, 0] + P[:, 1]]), [0.02, lo_p], [0.22, hi_p])
        path = surface_path(ax3, f, Q, color=YELLOW)
        ball = surface_ball(ax3, f, *Q[0])
        k = ValueTracker(0)
        ro = always_redraw(lambda: MathTex(rf"\alpha = {P[int(k.get_value())][0]:.3f},\ \beta = {P[int(k.get_value())][1]:.3f},"
                                           rf"\ \ \log L = {LL[int(k.get_value())]:,.0f}".replace(",", "{,}"), font_size=28,
                                           color=YELLOW).to_corner(UL, buff=0.35))
        tag = label(r"relative log likelihood / 1000, floor $-4$; iterates projected to grid; readout uses actual iterates",
                    font_size=19, color=GREY_A).to_edge(DOWN, buff=0.3)
        ewma = wrapped_label("RiskMetrics' EWMA is GARCH with $\\omega=0$, $\\alpha+\\beta=1$: no fixed variance-reversion target (Technical Document, 4th ed., 1996, sec.\\ 5.2)",
                             5.2, 19, ALT).to_corner(UR, buff=0.3)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-125 * DEGREES, zoom=0.7)
        self.add_fixed_in_frame_mobjects(tag)
        self.add_fixed_orientation_mobjects(*alabs)
        for m in (tag, *alabs):
            m.set_opacity(0)
        with self.voiceover(
            "What did the optimiser do? Fix omega by matching the long-run variance to the sample's, and the "
            "likelihood becomes a landscape over two numbers: alpha, the splash, and the persistence, alpha plus beta, "
            "which must stay below one. "
            "<bookmark mark='a'/> Start from a poor guess and let a simplex search climb. It races up the steep "
            f"persistence slope, then crawls across alpha, through {gl['n_iter']} iterations, to the peak at alpha "
            f"{P[-1][0]:.3f} and beta {P[-1][1]:.3f}. <bookmark mark='b'/> The hill is steep across persistence and "
            "broad along alpha: the geometry shows different sensitivities in these coordinates. A precision ratio would require a curvature or robust covariance calculation. <bookmark mark='c'/> And "
            "J.P. Morgan's RiskMetrics exponential average sits at the far edge of the landscape: persistence "
            "exactly one, no tap and no net expected leak, so it never reverts to a long-run level."
            " Next: GARCH's many children."
        ) as vo:
            self.play(Create(ax3), FadeIn(surf), *[m.animate.set_opacity(1) for m in (tag, *alabs)], run_time=2)
            vo.wait_until("a")
            self.add(ball)
            self.add_fixed_in_frame_mobjects(ro)
            n = len(P)
            self.play(Create(path), MoveAlongPath(ball, path), k.animate.set_value(n - 1), run_time=5, rate_func=linear)
            vo.wait_until("b")
            self.move_camera(theta=-80 * DEGREES, phi=70 * DEGREES, run_time=3)
            vo.wait_until("c")
            self.add_fixed_in_frame_mobjects(ewma)
            self.play(FadeIn(ewma))
        ro.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1)
