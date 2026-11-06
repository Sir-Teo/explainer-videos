from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import (ALT, ARB, CALL, FWD, PART, PUT, Q_C, FullRangeReplay, answer_under, load, pause_at, real_data)

SPEC_COL = {"svi": Q_C, "spline": QC.IMPLIED, "mix2": CALL, "mix3": FWD}
SPEC_NAME = {"svi": r"SVI", "spline": r"spline: positive part only (invalid fit)", "mix2": r"two log-normals", "mix3": r"three log-normals"}


class DensitySurface(VoiceoverScene, ThreeDScene):
    def construct(self):
        fit, term, specs = load("density_fit"), load("density_term"), load("density_specs")
        self.card()
        self.replay(fit)
        self.conditions()
        self.ridges(term)
        self.specs(specs)
        self.predict()

    def card(self):
        c = chapter_card(13, r"The density on the Surface", r"How much of the density do option prices really pin "
                         r"down?", lit=(2004,), part=PART)
        with self.voiceover("Chapter thirteen. The density on the Surface."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def replay(self, fit):
        steps = np.array([s["nfev"] for s in fit["steps"]], float)
        rmse = np.array([s["rmse"] for s in fit["steps"]])
        kq, ivq = np.asarray(fit["k"]), np.asarray(fit["iv"])
        kk = np.asarray(fit["kk"])
        Kg = np.asarray(fit["Kg"])
        F = fit["F"]
        cks = [1, 2, 4, 8, 16, 25, 200]
        idx = [int(np.where(steps == c)[0][0]) for c in cks]
        dmax = max(np.max(s["dens"]) for s in fit["steps"][3:])

        def frame(i):
            s = fit["steps"][idx[i]]
            g1 = axes([-0.7, 0.6], [0.3, 1.0], x_length=4.8, y_length=2.0, ylabel=r"implied volatility",
                      xticks=[-0.5, 0, 0.5], yticks=[0.4, 0.6, 0.8, 1.0], yfmt=lambda u: f"{100 * u:.0f}\\%",
                      font_size=13)
            g2 = axes([0.4 * F, 1.9 * F], [0, dmax * 1.1], x_length=4.8, y_length=1.7, ylabel=r"its density",
                      xlabel=r"bitcoin at expiry", xticks=[50000, 100000, 150000], xfmt=lambda u: f"{u / 1000:.0f}k",
                      yticks=[], font_size=13)
            VGroup(g1, g2).arrange(DOWN, buff=0.35)
            dots = VGroup(*[Dot(g1.ax.c2p(a, b), radius=0.03, color=WHITE) for a, b in zip(kq, ivq)
                            if -0.7 <= a <= 0.6 and 0.3 <= b <= 1.0])  # only the quotes inside the axes
            fitc = curve(g1.ax, kk, s["iv"], Q_C, stroke_width=3)
            ok = (Kg > 0.4 * F) & (Kg < 1.9 * F)
            dc = curve(g2.ax, Kg[ok], np.asarray(s["dens"])[ok], Q_C, stroke_width=3)
            return VGroup(g1, g2, dots, fitc, dc)

        rp = FullRangeReplay(steps, rmse, frame, cks, ylabel=r"vega-weighted error, vol points",
                            xlabel=r"function-evaluation budget", log_y=True, color=Q_C, left=LEFT * 3.5 + DOWN * 0.2,
                            right=RIGHT * 3.4 + DOWN * 0.2)
        head = label(rf"fitting SVI to the {fit['T'] * 365:.0f}-day expiry, {fit['expiry']}", font_size=26).to_edge(UP,
                                                                                                             buff=0.3)
        src = real_data(r"the Surface; \texttt{least\_squares} rerun with a growing budget")
        with self.voiceover(
            f"The density is only as good as the smile it comes from, so watch the House fit one. White dots: the Surface's implied volatilities {fit['T'] * 365:.0f} days out; purple: Gatheral's SVI smile from a rough guess; below, the density it implies. <bookmark mark='a'/> In the first steps the smile swings, and the density with it, lopsided, double-humped. <bookmark mark='b'/> Within about twenty-five evaluations the error settles at {rmse[-1]:.2f} vol points and the density stops moving. It inherits every wobble of the fit. The five parameters are a level, a slope, a skew, a shift and a curvature: five numbers that compress the whole expiry. Each point is a fresh fit from the same initialization with a larger evaluation budget; after convergence the solver may use fewer evaluations than that cap. The replay is indexed by budget."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rp), FadeIn(src))
            vo.wait_until("a")
            rp.play(self, run_time=max(vo.until("b") - 0.5, 5.0))
        self.wait(0.5)
        self.clear_scene()

    def conditions(self):
        rows = [cmath(r"w(k)", r"=", r"\sigma_{BS}^2(k)\, T,\qquad k = \ln K/F", font_size=34, colors={r"w(k)": Q_C}),
                cmath(r"w(k)", r"=", r"a + b\big(\rho(k - m) + \sqrt{(k - m)^2 + s^2}\big)", font_size=34,
                      colors={r"w(k)": Q_C}),
                cmath(r"q", r"=", r"\partial_{KK}\, C\big(F, K, \sqrt{w/T}\big)", font_size=34, colors={r"q": Q_C}),
                cmath(r"w(k, T_2)", r"\ge", r"w(k, T_1)\quad (T_2 > T_1)", font_size=34),
                cmath(r"b\,(1 + |\rho|)", r"\le", r"2", font_size=34)]
        whys = [why(r"total implied variance against log-moneyness: the natural coordinates of a smile", 21),
                why(r"raw SVI (Gatheral 2004): five parameters, linear wings", 21),
                why(r"price every strike with Black's formula on the fitted smile, then differentiate twice (chapter 12)", 21),
                why(r"no calendar arbitrage: at fixed moneyness, a later call spread on the forward is worth more", 21),
                why(r"Lee's moment formula bounds the wings' slope; Part 12 derives it", 21)]
        step = ladder(self, rows, whys, keep=5, top=3.2, x=-0.8, buff=0.5, edge=6.9)
        with self.voiceover(
            "The coordinates: total implied variance against log-moneyness. <bookmark mark='a'/> SVI is a hyperbola there, five parameters. <bookmark mark='b'/> Price every strike on the smile and differentiate twice. <bookmark mark='c'/> Across expiries, total variance must not fall with maturity, or a calendar spread is free. <bookmark mark='d'/> And Lee's bound limits the wings. Part twelve proves both. Raw SVI can still allow a butterfly arbitrage in the wings; Gatheral and Jacquier's surface version, SSVI, has parameter restrictions that can rule out both kinds, and Part twelve fits it. Calendar monotonicity here is at fixed forward moneyness under deterministic carry and the normalization used. Lee wing slopes are necessary constraints, not a full butterfly certificate. SSVI parameter restrictions can ensure both types of no arbitrage; arbitrary raw SVI parameters cannot."
        ) as vo:
            step(0, run_time=0.15)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.3)
        self.clear_scene()

    def ridges(self, term):
        x = np.asarray(term["x"])
        R = term["ridges"]
        Tmax = max(r["T"] for r in R) * 365
        ax = ThreeDAxes(x_range=[0.4, 1.8, 0.2], y_range=[0, 300, 50], z_range=[0, 1.1, 0.5], x_length=8.0,
                        y_length=6.0, z_length=3.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.4)
        ridges, floors = VGroup(), VGroup()
        last_lab = -1e9
        for i, r in enumerate(R):
            d = np.asarray(r["dens"])
            d = d / d.max()
            Td = r["T"] * 365
            col = interpolate_color(ManimColor(ALT), ManimColor(Q_C), i / max(len(R) - 1, 1))
            pts = [ax.c2p(a, Td, b) for a, b in zip(x[::2], d[::2])]
            poly = Polygon(ax.c2p(x[0], Td, 0), *pts, ax.c2p(x[-2], Td, 0), stroke_color=col, stroke_width=2.5,
                           fill_color=col, fill_opacity=0.35)
            ridges.add(poly)
            lab_ = MathTex(rf"{Td:.0f}\text{{d}}", font_size=22, color=col).move_to(ax.c2p(1.86, Td, 0))
            if Td - last_lab < 12:  # expiries a week apart would print on top of each other: label the first only
                lab_.set_opacity(0)
            else:
                last_lab = Td
            floors.add(lab_)
        names = VGroup(label(r"$x$: bitcoin at expiry, over today's price", font_size=22, color=GREY_A),
                       label(r"$y$: days to expiry", font_size=22, color=GREY_A),
                       label(r"$z$: density, each ridge scaled to its peak", font_size=22, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        cal = term["calendar"]
        info = VGroup(label(rf"{len(R)} expiries, {R[0]['T'] * 365:.0f} to {Tmax:.0f} days", font_size=22, color=Q_C),
                      label(rf"calendar check: {term['calendar_total']} violations across {term['n_pairs']} pairs",
                            font_size=22, color=CALL if term["calendar_total"] == 0 else ARB)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UR, buff=0.35)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-70 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(names, info)
        self.remove(names, info)
        k0, k1 = R[0]["skew"], R[-1]["skew"]
        lean = (f"And their shape turns: the shortest leans left, a skewness of {k0:.2f}, the market paying for "
                f"protection against falls; the longest leans right, {k1:.2f}, as a spreading log-normal does, "
                f"since a price can fall only to zero but rise without limit." if k0 < 0 < k1 else
                f"Their skewness goes from {k0:.2f} at the shortest to {k1:.2f} at the longest.")
        verdict = ("and the checker flags no violation at the sampled moneyness points between neighboring expiries."
                   if term["calendar_total"] == 0 else
                   f"and the checker flags {term['calendar_total']} calendar violations, which the House repairs first.")
        with self.voiceover(
            f"Now every expiry of the Surface at once: {len(R)} of them, from {R[0]['T'] * 365:.0f} days to {Tmax:.0f}, each fitted and differentiated, standing in three dimensions. <bookmark mark='a'/> Walk along maturity. The ridges widen, because uncertainty grows with time: the standard deviation goes from {100 * R[0]['sd']:.0f} percent of today's price to {100 * R[-1]['sd']:.0f}. {lean} <bookmark mark='b'/> Total variance rises with maturity at the checked moneyness points, {verdict} Each ridge is separately normalized to its own peak, so heights are not comparable densities. These are sampled calendar checks, not a global certificate of every wing and maturity."
        ) as vo:
            self.play(Create(ax), FadeIn(names), run_time=1.5)
            self.play(LaggedStart(*[Create(r_) for r_ in ridges], lag_ratio=0.3), FadeIn(floors), run_time=3)
            vo.wait_until("a")
            self.move_camera(theta=-35 * DEGREES, phi=68 * DEGREES, run_time=max(vo.until("b") - 0.3, 3.0))
            self.play(FadeIn(info))
            self.move_camera(theta=-55 * DEGREES, run_time=max(vo.remaining(1.0) - 0.5, 1.5))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0,
                         added_anims=[FadeOut(VGroup(ax, ridges, floors)), FadeOut(names), FadeOut(info)], run_time=0.5)
        self.clear_scene()

    def specs(self, sp):
        Kg = np.asarray(sp["Kg"])
        F = sp["F"]
        ok = (Kg > 0.35 * F) & (Kg < 1.9 * F)
        top = max(np.asarray(s["dens"])[ok].max() for s in sp["specs"]) * 1.1
        valid = [s for s in sp["specs"] if s["neg_mass"] <= 1e-4]
        spread = max(s["down30"] for s in valid) - min(s["down30"] for s in valid)
        g = axes([0.35 * F, 1.9 * F], [0, top], x_length=7.0, y_length=4.4, xlabel=r"bitcoin at expiry (\$)",
                 ylabel=r"risk-neutral density", xticks=[50000, 100000, 150000], xfmt=lambda u: f"{u / 1000:.0f}k",
                 yticks=[], font_size=16)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        cv = VGroup(*[curve(ax, Kg[ok], np.asarray(s["dens"])[ok], SPEC_COL[s["name"]], stroke_width=3)
                      for s in sp["specs"]])
        cut = DashedLine(ax.c2p(0.7 * F, 0), ax.c2p(0.7 * F, top), color=ARB, stroke_width=2)
        cl = label(r"30\% below the forward", font_size=17, color=ARB).next_to(ax.c2p(0.7 * F, top), DOWN, buff=0.1)
        rows = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.35, color=SPEC_COL[s["name"]], stroke_width=5),
                               label(SPEC_NAME[s["name"]], font_size=19, color=SPEC_COL[s["name"]]),
                               MathTex(rf"{s['rmse']:.2f}\ \text{{RMSE pts}},\ \ I(\text{{down }}30\%) = "
                                       rf"{100 * s['down30']:.1f}\%", font_size=22, color=SPEC_COL[s["name"]])).arrange(
            RIGHT, buff=0.15) for s in sp["specs"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        neg = [s for s in sp["specs"] if s["neg_mass"] > 1e-4]
        side = VGroup(
            rows,
            wrapped_label(rf"weighted RMSEs are at most {sp['rmse_max']:.1f} vol points; valid-fit tail "
                          rf"integrals span {100 * spread:.1f} percentage points", 5.0, 20, WHITE),
            wrapped_label((rf"the spline's density goes negative ({100 * neg[0]['neg_mass']:.1f}\% of mass): it fails "
                           rf"the checker" if neg else r"all four have no negative curvature on the checked grid"), 5.0, 20, ARB if neg else CALL),
            wrapped_label(r"Shikhman et al.\ (2026): in their conditioning analysis, 95 of 126 pricing directions are "
                          r"numerically null: very different densities give the same prices", 5.0, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3)
        src = real_data(rf"the Surface, {sp['expiry']}; each specification fitted to the same quotes")
        neg_line = (" The spline's density even dips below zero, so the checker rejects it." if neg else "")
        with self.voiceover(
            f"""How much of a density do the quotes pin down? Fit the same {sp['T'] * 365:.0f}-day observations with SVI, a volatility spline, and mixtures of two and three lognormals. <bookmark mark='a'/> Their vega-weighted RMSEs are at most {sp['rmse_max']:.1f} volatility points; that is not a maximum error for every quote. <bookmark mark='b'/> The spline has negative curvature, so it is not a probability density. Its plotted curve is only the stored positive part, and its tail integral is not a valid probability. Among the other fitted candidates, the thirty-percent downside integrals span {100 * spread:.2f} percentage points on the finite integration grid. <bookmark mark='c'/> Shikhman and coauthors' 2026 numerical conditioning analysis illustrates why accurate option prices need not identify a latent density. Finite quotes, numerical integration and extrapolation leave specification uncertainty; this illustration does not certify any fit globally."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), LaggedStart(*[Create(c_) for c_ in cv], lag_ratio=0.3), FadeIn(rows),
                      run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(cut), FadeIn(cl), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def predict(self):
        card = pause_at(r"Four fits have small weighted RMSE. Must their crash probabilities agree?")
        with self.voiceover(
            """Pause and predict. Four fits have small weighted quote RMSE. Must their crash probabilities agree? <bookmark mark='a'/> No. Finite quotes and a weighted average error do not identify a unique tail. Extrapolation matters, and any fit with negative density must be rejected rather than assigned a crash probability. These are Q candidates, not physical crash forecasts."""
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"no: finite quotes and extrapolation leave tail uncertainty; reject negative densities before comparing probabilities")))
        self.wait(0.4)
        self.clear_scene()
