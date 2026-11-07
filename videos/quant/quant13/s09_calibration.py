from __future__ import annotations

from datetime import date

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, load, pause, real_data

LAB_REG = [
    "def calibrate_reg(name, quotes, x_prev, lam, W=None, x0=None):",
    "    spec, pre = MODELS[name], _pre(quotes)",
    "    W = 1 / np.maximum(np.abs(x_prev), 0.05) if W is None else W",
    "    s = np.sqrt(lam * len(quotes['K']))",
    "    def fun(p):  # the fit's residuals, then the pull toward last week",
    "        return np.concatenate([residuals(name, p, quotes, pre),",
    "                               s * W * (p - x_prev)])",
    "    r = least_squares(fun, x_prev, bounds=(spec['lo'], spec['hi']),",
    "                      x_scale='jac')",
    "    return r.x",
]


def _t(s):
    d = date.fromisoformat(s)
    return d.year + (d.timetuple().tm_yday - 1) / 365


class Calibration(VoiceoverScene, ThreeDScene):
    def construct(self):
        L = load("landscape")
        h = load("history")
        hs = load("hessian")
        hr = load("history_reg")
        self.card()
        self.landscape(L, hs)
        self.derive(hs)
        self.history(h)
        self.wander(h)
        self.regularised(hr)

    def card(self):
        c = chapter_card(16, r"Calibration: valleys, identifiability, instability", r"Which parameters did the market mean?",
                         part=PART)
        with self.voiceover("Chapter sixteen. Calibration, as an inverse problem."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c), run_time=0.35)

    def landscape(self, Ld, hs):
        ka, xi = np.log10(np.asarray(Ld["kappa"])), np.log10(np.asarray(Ld["xi"]))
        loss = np.asarray(Ld["loss"])
        f = RegularGridInterpolator((ka, xi), loss)
        ax = ThreeDAxes(x_range=[ka[0], ka[-1], 0.5], y_range=[xi[0], xi[-1], 0.5], z_range=[1.0, 6.0, 1.0],
                        x_length=7.0, y_length=5.0, z_length=3.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.5)
        surf = Surface(lambda u, v: ax.c2p(u, v, float(f((u, v)))), u_range=[ka[0], ka[-1]], v_range=[xi[0], xi[-1]],
                       resolution=(28, 28), fill_opacity=0.85, stroke_width=0.3, stroke_color=GREY_D)
        surf.set_fill_by_value(axes=ax, colorscale=[(RV, 1.3), (IV, 2.2), (BAD, 3.5)], axis=2)
        floor = np.asarray(Ld["loss"]).argmin(axis=1)
        valley = VMobject(stroke_color=WHITE, stroke_width=4).set_points_smoothly(
            [ax.c2p(ka[i], xi[j], loss[i, j] + 0.03) for i, j in enumerate(floor)])
        best = Ld["best"]
        star = Dot3D(ax.c2p(np.log10(best[1]), np.log10(best[3]), loss.min() + 0.05), radius=0.09, color=YELLOW)
        V = np.asarray(hs["profile_vecs"])  # columns: eigenvectors over (log kappa, log xi), natural logs
        ev = np.asarray(hs["profile_eig"])
        c0 = np.array([np.log10(best[1]), np.log10(best[3])])
        arrows = VGroup()
        for j, col in ((0, WHITE), (1, BAD)):
            d = V[:, j] / np.linalg.norm(V[:, j]) * (0.55 if j == 0 else 0.55 * np.sqrt(ev[0] / ev[1]) * 3)
            for sgn in (1, -1):
                a3 = Arrow3D(ax.c2p(*c0, loss.min() + 0.05), ax.c2p(*(c0 + sgn * d), loss.min() + 0.05), color=col,
                             thickness=0.015)
                arrows.add(a3)
        hint = VGroup(label(r"mean reversion $\kappa$, 0.5 to 30 (log)", font_size=22, color=GREY_A),
                      label(r"vol of vol $\xi$, 0.3 to 8 (log)", font_size=22, color=GREY_A),
                      label(r"height: the best fit error with $v_0, \theta, \rho$ re-optimized", font_size=22,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.4)
        Lm = np.asarray(Ld["loss"])
        i0 = int(np.argmin(np.abs(np.asarray(Ld["kappa"]) - 5.0)))
        along = Lm[i0, floor[i0]]
        txt = VGroup(MathTex(rf"\min = {Lm.min():.2f}\ \text{{at}}\ \kappa = {best[1]:.0f},\ \xi = {best[3]:.1f}",
                             font_size=26, color=YELLOW),
                     MathTex(rf"\kappa = {Ld['kappa'][i0]:.0f}:\ \ {along:.2f}", font_size=26, color=WHITE),
                     label(rf"12 random starts: all 12 end at the same minimum", font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DR, buff=0.4)
        src = real_data(r"Heston on the Surface: 225 fits on a 15 by 15 grid", corner=DL)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-130 * DEGREES, zoom=0.72)  # below the caption
        self.add_fixed_in_frame_mobjects(hint, txt, src)
        self.remove(hint, txt, src)
        with self.voiceover(
            (
            "Calibration is an optimization; look at its landscape. Fix Heston's mean reversion and vol of vol, refit "
            "the other three, record the error, over a grid. <bookmark mark='a'/> The minimum is the yellow star, at "
            "the end of a long curved valley where faster mean reversion trades against higher vol of vol: the valley "
            f"chapter four's replay slid along. At kappa {Ld['kappa'][i0]:.0f} instead of {best[1]:.0f}, the error "
            f"rises only from {Lm.min():.2f} to {along:.2f}. <bookmark mark='b'/> Twelve random starts all end at "
            "the star; but the data pin a combination of the two, not each one."
        )
        ) as vo:
            self.play(FadeIn(hint), FadeIn(src), Create(ax), Create(surf), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(star), Create(valley), run_time=2)
            self.move_camera(theta=-70 * DEGREES, phi=58 * DEGREES, run_time=max(vo.remaining(1.0) - 6, 2))
            vo.wait_until("b")
            self.play(FadeIn(txt))
        with self.voiceover(
            (
            f"""Approximate the local loss curvature using Gauss–Newton, J transpose J. The first four parameter coordinates are logarithmic and rho is untransformed. Profiling out the other three coordinates uses a Schur complement. <bookmark mark='a'/> In this coordinate system the across-valley curvature is {hs['profile_cond']:.0f} times the along-valley curvature. This describes local sensitivity of the fitted objective, not a coordinate-independent measure of information."""
        )
        ) as vo:
            self.play(*[FadeIn(a_) for a_ in arrows[:2]], run_time=1.2)
            vo.wait_until("a")
            self.play(*[FadeIn(a_) for a_ in arrows[2:]], run_time=1.2)
            self.move_camera(theta=-95 * DEGREES, phi=30 * DEGREES, run_time=max(vo.remaining(1.0) - 0.3, 1.5))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, added_anims=[FadeOut(VGroup(ax, surf, valley, star, arrows)), FadeOut(hint),
                                                                  FadeOut(txt), FadeOut(src)], run_time=0.8)
        self.clear_scene(run_time=0.35)

    def history(self, h):
        rows = h["rows"]
        t = np.array([_t(r["day"]) for r in rows])
        X = np.array([r["x"] for r in rows])
        xt = [2024, 2024.5, 2025, 2025.5, 2026]
        fmt = lambda u: {0: "Jan 24", 1: "Jul 24", 2: "Jan 25", 3: "Jul 25", 4: "Jan 26"}[round((u - 2024) * 2)]  # noqa: E731
        g1 = axes([2024, 2026], [0, 22], x_length=6.2, y_length=1.65, ylabel=r"$\kappa$", xticks=xt, xfmt=fmt,
                  yticks=[0, 10, 20], font_size=15)
        g2 = axes([2024, 2026], [0, 6.5], x_length=6.2, y_length=1.65, ylabel=r"$\xi$", xticks=xt, xfmt=fmt,
                  yticks=[0, 2, 4, 6], font_size=15)
        g3 = axes([2024, 2026], [-0.5, 0.3], x_length=6.2, y_length=1.65, ylabel=r"$\rho$", xticks=xt, xfmt=fmt,
                  yticks=[-0.4, 0, 0.2], font_size=15)
        G = VGroup(g1, g2, g3).arrange(DOWN, buff=0.22).to_edge(LEFT, buff=0.7)
        if G.height > 7.4:  # three charts and their tick labels inside the frame
            G.scale_to_fit_height(7.4).to_edge(LEFT, buff=0.7)
        l1 = curve(g1.ax, t, X[:, 1], VAR, stroke_width=2.2)
        l2 = curve(g2.ax, t, X[:, 3], OPT, stroke_width=2.2)
        l3 = curve(g3.ax, t, X[:, 4], IV, stroke_width=2.2)
        z3 = DashedLine(g3.ax.c2p(2024, 0), g3.ax.c2p(2026, 0), stroke_color=GREY_C, stroke_width=1.2)
        kb = float((X[:, 1] > 19.9).mean())
        fe = float((2 * X[:, 1] * X[:, 2] / X[:, 3] ** 2 < 1).mean())
        rp = float((X[:, 4] > 0).mean())
        side = VGroup(
            wrapped_label('100 weekly pooled-mark fits, maturities above 6 days; single-day fits use above 2 days. These are different quote universes.', 4.6, 19, GREY_A),
            MathTex(rf"\kappa\ \text{{moves}}\ {100 * h['median_weekly_change']['kappa']:.0f}\%\ \text{{a week (median)}}",
                    font_size=26, color=VAR),
            label(rf"and sits at its bound of 20 in {100 * kb:.0f}\% of weeks", font_size=20, color=GREY_A),
            MathTex(rf"\text{{Feller fails in}}\ {100 * fe:.0f}\%\ \text{{of weeks}}", font_size=26, color=BAD),
            MathTex(rf"\rho > 0\ \text{{in}}\ {100 * rp:.0f}\%\ \text{{of weeks}}", font_size=26, color=IV),
            wrapped_label('Changing inputs and weak identifiability both affect fitted parameters; hedge improvement is not measured by this stability exercise.', 4.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35)
        src = real_data(r"100 weekly pooled Deribit option-mark surfaces, 2024--2025")
        with self.voiceover(
            (
            f"""Recalibrate on a hundred weekly pooled-mark surfaces. Single-day fits use maturities above two days; weekly fits use above six, so their universes differ. The fitted kappa changes by {100 * h['median_weekly_change']['kappa']:.0f} percent in a median week and reaches its bound in {100 * kb:.0f} percent of weeks. <bookmark mark='a'/> The strict-positive CIR Feller condition fails in {100 * fe:.0f} percent; this permits reaching zero rather than invalidating Heston. <bookmark mark='b'/> Fitted rho is positive in {100 * rp:.0f} percent. <bookmark mark='c'/> Parameter drift can reflect changing surfaces, risk premia, sparse data, model error, optimizer behavior and weak identifiability. These fits do not establish immutable physical constants. Their consequences for exotics and hedges require further calculation."""
        )
        ) as vo:
            self.play(FadeIn(G[0]), Create(l1), FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]), FadeIn(src), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(G[1]), Create(l2), FadeIn(side[3]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(G[2]), Create(z3), Create(l3), FadeIn(side[4]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def derive(self, hs):
        rows = [cmath(r"\hat x", r"=", r"\arg\min_x\ \tfrac12\,\|r(x)\|^2,\qquad H \approx J^\top J", font_size=36,
                      colors={r"\hat x": VAR}),
                cmath(r"\delta L", r"\approx", r"\tfrac12\,\delta x^\top H\,\delta x = \tfrac12\sum_j \lambda_j\,(e_j^\top\delta x)^2",
                      font_size=36, colors={r"\delta L": VAR}),
                cmath(r"\operatorname{Cov}(\hat x)", r"\approx", r"\hat\sigma^2\,H^{-1}", font_size=36,
                      colors={r"\operatorname{Cov}(\hat x)": VAR}),
                cmath(r"\min_p", r"\ ", r"\tfrac12\|r(p)\|^2 + \tfrac{N\lambda}{2}\,\big\|W(p - p_{\text{prev}})\big\|^2"
                      r"\ \Rightarrow\ H_p \to H_p + N\lambda W^\top W", font_size=32, colors={r"\min_p": OPT})]
        whys = [why('Price-over-vega residuals; reported vega-weighted IV RMSE is a different statistic. $J^\\top J$ is a Gauss--Newton approximation.', 20),
                why(r"near the optimum the loss is a bowl; a small eigenvalue $\lambda_j$ is a flat direction $e_j$: the "
                    r"data pin the combination $e_j^\top\delta x$ only weakly", 20),
                why('Illustrative standard errors require independent, correctly scaled quote errors and an adequate model; unverified here.', 20),
                why('Raw residual convention: add $N\\lambda W^\\top W$, with quote count $N$. Normalizing the objective by $N$ gives $\\lambda W^\\top W$. Nonuniform for relative weights.', 20)]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.8, buff=0.6, edge=6.9)  # the eigenvalue readout takes the bottom
        se = np.asarray(hs["se"])
        ev = np.asarray(hs["eig"])
        tab = VGroup(
            MathTex(rf"\text{{eigenvalues of }}H:\ " + r",\ ".join(f"{v:.0f}" for v in ev) +
                    rf"\quad \text{{condition}}\ {hs['cond']:.0f}", font_size=26, color=GREY_A),
            MathTex(rf"\text{{s.e.:}}\ \kappa\ \pm{100 * se[1]:.0f}\%,\ \ \xi\ \pm{100 * se[3]:.0f}\%,\ \ v_0\ \pm{100 * se[0]:.0f}\%,"
                    rf"\ \ \theta\ \pm{100 * se[2]:.0f}\%,\ \ \rho\ \pm{se[4]:.2f}", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            (
            f"The optimizer minimizes squared price errors divided by quote vega. This approximates IV errors locally, while the reported vega-weighted IV RMSE is a different statistic. <bookmark mark='a'/> Gauss–Newton curvature identifies locally flat directions in the chosen coordinates. <bookmark mark='b'/> The displayed covariance formula additionally assumes correctly scaled independent errors and an adequate model. Its illustrative kappa standard error is {100 * se[1]:.0f} percent, with condition number {hs['cond']:.0f}; these assumptions are unverified for pooled option marks and a misspecified model. It is not an empirical confidence interval. <bookmark mark='c'/> For the raw residuals used here, the relative penalty adds quote count times lambda W transpose W. Dividing the whole objective by quote count gives the normalized convention. This penalty formula uses raw parameters; the log-coordinate diagnostic above requires transforming its weights. It does not increase every eigenvalue by a uniform amount unless W is identity. This imposes stability information; it does not recover missing market information automatically."
        )
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeIn(tab))
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def wander(self, h):
        rows = h["rows"]
        X = np.array([r["x"] for r in rows])
        lk, lxi = np.log10(np.clip(X[:, 1], 0.05, 25)), np.log10(np.clip(X[:, 3], 0.05, 8))
        rm = np.array([r["rmse"] for r in rows])
        g = axes([np.log10(0.05), np.log10(25)], [np.log10(0.05), np.log10(8)], x_length=6.0, y_length=4.6,
                 xlabel=r"mean reversion $\kappa$ (log)", ylabel=r"vol of vol $\xi$ (log)",
                 xticks=[np.log10(v) for v in (0.1, 1, 10)], yticks=[np.log10(v) for v in (0.1, 1, 5)],
                 xfmt=lambda u: f"{10 ** u:g}", yfmt=lambda u: f"{10 ** u:g}", font_size=15).to_edge(LEFT, buff=0.7)
        gr = axes([0, len(rows) - 1], [0, 7], x_length=4.6, y_length=2.4, xlabel=r"week", ylabel=r"fit error (vol pts)",
                  xticks=[0, len(rows) - 1], yticks=[0, 3, 6], font_size=13).to_edge(RIGHT, buff=0.5).shift(UP * 1.0)
        w = ValueTracker(0)

        def trail():
            k = int(w.get_value())
            pts = [g.ax.c2p(a, b) for a, b in zip(lk[:k + 1], lxi[:k + 1])]
            m = VMobject(stroke_color=VAR, stroke_width=1.5, stroke_opacity=0.6)
            if len(pts) > 1:
                m.set_points_as_corners(pts)
            return m

        tr = always_redraw(trail)
        dot = always_redraw(lambda: Dot(g.ax.c2p(lk[int(w.get_value())], lxi[int(w.get_value())]), radius=0.08, color=YELLOW))
        err = always_redraw(lambda: VMobject(stroke_color=MODEL_COL["Heston"], stroke_width=2.5).set_points_as_corners(
            [gr.ax.c2p(i, v) for i, v in enumerate(rm[:max(int(w.get_value()) + 1, 2)])]))
        day = always_redraw(lambda: label(rows[int(w.get_value())]["day"], font_size=22, color=GREY_A).next_to(g, UP, buff=0.1)
                            .align_to(g, RIGHT))
        corr = float(np.corrcoef(lk, lxi)[0, 1])
        side = wrapped_label(rf"each yellow dot is one Wednesday's fit; across {len(rows)} weeks $\log\kappa$ and $\log\xi$ "
                             rf"move together, correlation {corr:+.2f}: the fits slide along the valley, while the error "
                             rf"stays near {h['rmse_median']:.1f}", 4.6, 18, GREY_A).next_to(gr, DOWN, buff=0.5).align_to(gr, LEFT)
        src = real_data(r"100 weekly pooled Deribit option-mark surfaces, 2024--2025")
        with self.voiceover(
            f"""Replay the hundred weekly fits across log kappa and log xi. <bookmark mark='a'/> They often move together, with correlation {corr:+.2f} in these coordinates. The right panel retains the full fit-error range. This resembles the local calibration valley, but a time series across changing market inputs is not the same experiment as perturbing parameters against a fixed surface. Both weak identifiability and changing inputs can contribute."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(gr), FadeIn(src))
            self.add(tr, dot, err, day)
            self.play(w.animate.set_value(len(rows) - 1), run_time=max(vo.remaining(2.0) - 2.0, 6), rate_func=linear)
            self.play(FadeIn(side))
        for m in (tr, dot, err, day):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def regularised(self, hr):
        fr = hr["frontier"]
        days = hr["days"]
        # the three settings differ by little: zoom the axes to them (the ticks keep the scale honest)
        xs_ = np.array([f_["median_change_all"] for f_ in fr]); ys_ = np.array([f_["rmse_median"] for f_ in fr])
        x0, x1 = float(np.floor(xs_.min() * 50 - 1) / 50), float(np.ceil(xs_.max() * 50 + 1) / 50)
        y0, y1 = float(np.floor(ys_.min() * 50 - 1) / 50), float(np.ceil(ys_.max() * 50 + 1) / 50)
        g = axes([x0, x1], [y0, y1], x_length=5.4, y_length=3.6, xlabel=r"median weekly change in the parameters",
                 ylabel=r"median fit error (vol points)", xticks=list(np.round(np.linspace(x0, x1, 3), 3)),
                 xfmt=lambda u: f"{100 * u:.0f}\\%", yticks=list(np.round(np.linspace(y0, y1, 3), 3)),
                 yfmt=lambda u: f"{u:.2f}", font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.6)
        ax = g.ax
        cols = [BAD, OPT, RV]
        pts = VGroup()
        for f_, c_, d_ in zip(fr, cols, (UP, DOWN, LEFT)):  # the first two settings nearly coincide
            x_, y_ = f_["median_change_all"], f_["rmse_median"]
            pts.add(VGroup(Dot(ax.c2p(x_, y_), radius=0.09, color=c_),
                           MathTex(rf"\lambda = {f_['lam']:g}", font_size=24, color=c_).next_to(ax.c2p(x_, y_), d_, buff=0.12)))
        link = VMobject(stroke_color=GREY_B, stroke_width=2).set_points_as_corners(
            [ax.c2p(f_["median_change_all"], f_["rmse_median"]) for f_ in fr])
        card = lab_card(r"regularised calibration", LAB_REG, source="explainer/quant/house/stochvol.py: calibrate_reg",
                        width=7.2, font_size=16).to_edge(UP, buff=0.3).to_edge(RIGHT, buff=0.3)
        outs = [f"lam={f_['lam']:<5g} weekly change {100 * f_['median_change_all']:5.1f}%   "
                f"kappa {100 * f_['median_change']['kappa']:5.1f}%   error {f_['rmse_median']:.2f}" for f_ in fr]
        a, b = fr[0], fr[-1]
        cut = a["median_change_all"] / max(b["median_change_all"], 1e-9)
        cost = b["rmse_median"] - a["rmse_median"]
        verdict = (f"The strongest pull cuts the typical weekly change by a factor of {cut:.0f} and costs "
                   f"{cost:.2f} vol points of median fit error." if cut > 2 else
                   f"Even the strongest pull cuts the weekly change only by a factor of {cut:.1f}, for {cost:.2f} vol "
                   "points of fit: the instability is not only noise.")
        pp = pause(r"Overnight $\kappa$ jumped from 3 to 20 and the fit barely moved. Which prices changed?", width=5.2)
        pp.to_corner(DR, buff=0.3)  # the chart takes the left
        with self.voiceover(
            f"""The House stacks price-over-vega residuals with a penalty on relative parameter changes from last week. <bookmark mark='a'/> Rerun the same hundred dates with two penalty strengths and compare median parameter change with median fit error. <bookmark mark='b'/> {verdict} <bookmark mark='c'/> This measures a stability–fit trade-off, not an observed improvement in hedging. Pause: if kappa jumps from three to twenty while fit error barely changes, what follows? Vanilla prices may remain close; forward-starts, cliquets and hedge ratios can change, but neither their direction nor their size follows from kappa alone. All other fitted parameters and the payoff matter. Next, evaluating a hedge."""
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(g))
            vo.wait_until("a")
            lab_run(self, card, outs, run_time=2.5, font_size=16)
            vo.wait_until("b")
            self.play(Create(link), LaggedStart(*[FadeIn(p_, scale=1.4) for p_ in pts], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(pp))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)
