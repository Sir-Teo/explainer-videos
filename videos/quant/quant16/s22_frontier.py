from __future__ import annotations

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, fixed, illustration, load, loglog, polyline, predict, sci, axes, data_range, pause_card, flat_camera


class Frontier(VoiceoverScene, ThreeDScene):
    def construct(self):
        ch = load("cheb")
        rq = load("rqmc_median")
        race = load("race")
        self.card()
        self.chebyshev(ch)
        self.speed(ch, race)
        self.median(rq)
        self.papers()

    def card(self):
        c = chapter_card(19, r"Frontier: interpolation and selected research", r"Where is computational pricing research now?",
                         lit=(2024,), part=PART)
        with self.voiceover('Chapter nineteen. Interpolation, randomized integration, and selected research.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def chebyshev(self, ch):
        (x0, x1), (y0, y1) = ch["box"]
        xs, ys = np.asarray(ch["xs"]), np.asarray(ch["ys"])
        zr = data_range(*[r["err_surface"] for r in ch["rows"]])
        ax = ThreeDAxes(x_range=[x0, x1, 15], y_range=[y0, y1, 0.02], z_range=[*zr, 2], x_length=6.6, y_length=5.0,
                        z_length=3.0, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False,
                                                               "stroke_width": 2})
        ax.shift(DOWN * 0.4)
        rows = ch["rows"]

        def surf(r):
            f = RegularGridInterpolator((xs, ys), np.asarray(r["err_surface"]))
            sf = Surface(lambda u, v: ax.c2p(u, v, float(f((u, v)))), u_range=[x0, x1], v_range=[y0, y1],
                         resolution=(24, 24), fill_opacity=0.85, stroke_width=0.3, stroke_color="#0E1117",
                         checkerboard_colors=False)
            sf.set_fill_by_value(axes=ax, colorscale=[(QC.GAIN, zr[0]), (QC.DELTA, sum(zr) / 2), (QC.LOSS, zr[1])], axis=2)
            return sf

        def nodes(r):
            return VGroup(*[Dot3D(ax.c2p(a, b, zr[0]), radius=0.03, color=GREY_A, resolution=(4, 4))
                            for a in r["x"] for b in r["y"]])

        show = [r for r in rows if r["n"] in (4, 8, 16, 32)]
        hint = VGroup(label(r"across: spot $S_0$ (70 to 130)", font_size=21, color=GREY_A),
                      label(r"back: initial variance $v_0$ (0.01 to 0.09)", font_size=21, color=GREY_A),
                      label(r"up: log discrepancy; cached floor $10^{-12}$", font_size=21, color=GREY_A),
                      label(r"surface: 25 by 25 test grid; floor: COS nodes", font_size=21, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        tags = [VGroup(MathTex(rf"{r['n']}\times{r['n']}\ \text{{nodes}}", font_size=28, color=OPT),
                       wrapped_label(rf"maximum at 200 fixed test sites: ${sci(r['max_err'], 1)}$", 5.0, 22, OPT))
                .arrange(DOWN, aligned_edge=RIGHT, buff=0.15).to_corner(UR, buff=0.4) for r in show]
        self.set_camera_orientation(phi=64 * DEGREES, theta=-58 * DEGREES, zoom=0.85)
        fixed(self, hint, *tags)
        s = surf(show[0])
        nd = nodes(show[0])
        with self.voiceover(
            f"Build a Chebyshev interpolant over this fixed two-parameter box: initial spot and initial variance, with the remaining contract and model parameters fixed. Labels come from a five-hundred-and-twelve-term COS calculation, so they have numerical error too. The surface compares on a separate twenty-five-by-twenty-five grid; saved log discrepancies below one trillionth are censored at that level. <bookmark mark='a'/> Four, eight, sixteen and thirty-two nodes per direction improve this example. The headline maximum is over two hundred fixed random test sites, not the supremum over the entire box. <bookmark mark='b'/> At thirty-two nodes per direction that sampled maximum is {show[-1]['max_err']:.3g}. Analytic interpolation theory requires regularity in a complex neighbourhood and appropriate bounds. Finite tests provide no extrapolation, Greek-accuracy or arbitrage certificate."
        ) as vo:
            self.play(Create(ax), FadeIn(hint), FadeIn(nd), Create(s), FadeIn(tags[0]), run_time=2)
            vo.wait_until("a")
            for k in range(1, len(show)):
                s2, nd2 = surf(show[k]), nodes(show[k])
                self.play(ReplacementTransform(s, s2), ReplacementTransform(nd, nd2), FadeOut(tags[k - 1]), FadeIn(tags[k]),
                          run_time=1.8)
                s, nd = s2, nd2
                self.wait(0.4)
            vo.wait_until("b")
            self.move_camera(theta=-25 * DEGREES, run_time=max(vo.remaining(0.5), 2))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(Group(*[m for m in self.mobjects]))], run_time=1.5)
        self.clear_scene()
        # back to the flat camera for the rest of the chapter, whatever the animated move left behind
        flat_camera(self)

    def speed(self, ch, race):
        rows = ch["rows"]
        last = rows[-1]
        mc = min((q for q in race["points"] if q["method"].startswith("Monte Carlo")), key=lambda q: q["err"])
        items = [(r"Chebyshev interpolant, one query", ch["t_cheb"], GOOD),
                 (r"COS, one price (512 terms)", ch["t_cos"], OPT),
                 (rf"MC: one sampling s.e. {mc['err']:.3f}", mc["time"], BAD)]
        xr = data_range([np.log10(t) for _, t, _ in items])
        baseline = xr[0]
        g = axes(xr, [0, 4], x_length=7.0, y_length=3.0, xlabel=r"seconds per price (log)",
                 xticks=[-4, -2, 0], xfmt=lambda v: f"10^{{{int(v)}}}", font_size=15).to_edge(LEFT, buff=3.2).shift(UP * 0.5)
        ax = g.ax
        bars = VGroup()
        for i, (nm, t, col) in enumerate(items):
            y = 3 - i
            x1 = np.log10(t)
            bars.add(VGroup(Rectangle(width=max(ax.c2p(x1, 0)[0] - ax.c2p(baseline, 0)[0], 0.02), height=0.5, stroke_width=0,
                                      fill_color=col, fill_opacity=0.85).move_to(ax.c2p(baseline, y), aligned_edge=LEFT),
                            label(nm, font_size=17, color=col).next_to(ax.c2p(baseline, y), LEFT, buff=0.15),
                            MathTex(rf"{t * 1e3:.3g}\,\text{{ms}}", font_size=20, color=GREY_A).next_to(ax.c2p(x1, y), RIGHT,
                                                                                                   buff=0.1)))
        build = last["t_build"]
        saving = ch["t_cos"] - ch["t_cheb"]
        break_even = build / saving if saving > 0 else float("inf")
        q = predict(rf"The pricer needs {last['calls']:,} COS prices to build. When does it pay?".replace(",", "{,}"),
                    width=6.0, font_size=21).to_edge(DOWN, buff=0.4)
        note_ = wrapped_label(r"low-rank tensor formats (Glau, Kressner and Statti 2020) take the idea to many parameters; "
                              r"Part 17's networks are the learned version", 10.0, 18, GREY_A).next_to(q, UP, buff=0.3)
        with self.voiceover(
            f"The final interpolant uses {last['calls']:,} COS labels and has recorded build time {build:.3f} seconds. A fixed query takes {ch['t_cheb'] * 1000:.3f} milliseconds, versus {ch['t_cos'] * 1000:.3f} for the timed COS implementation. This is a shared-CPU, single-query comparison; batching and parameters can change it. The MC row reports one sampling standard error and is not accuracy-matched to these deterministic diagnostics. <bookmark mark='a'/> Break-even against repeated COS queries is build time divided by COS-query time minus interpolation-query time, provided that difference is positive. Here that is about {break_even:.0f} queries. Building the interpolant consumes work; it does not disappear. Low-rank tensor methods exploit additional structure to address some higher-dimensional parameter spaces. They do not remove every dimensionality or accuracy problem."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.4, run_time=2.5))
            vo.wait_until("a")
            self.play(FadeIn(q), FadeIn(note_))
        self.wait(0.5)
        self.clear_scene()

    def median(self, rq):
        ns = np.log10(rq["ns"])
        g = loglog(*data_range(ns), *data_range(np.log10(rq["mean"]), np.log10(rq["median"])), r"points per scrambled Sobol set", r"RMSE of $\int_0^1 e^u\,du$", x_length=6.4,
                   y_length=4.2, xt=[1, 2, 3], yt=[-10, -8, -6, -4, -2]).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        lm = polyline(ax, ns, np.log10(rq["mean"]), QC.THETA)
        ld = polyline(ax, ns, np.log10(rq["median"]), GOOD)
        leg = legend([(QC.THETA, r"mean of 11 scramblings"), (GOOD, r"median of 11 scramblings")], font_size=17)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        k = 3
        side = VGroup(
            MathTex(rf"n = {rq['ns'][k]:,}".replace(",", "{,}"), font_size=26, color=GOOD),
            MathTex(rf"\text{{mean}} = {sci(rq['mean'][k], 1)}", font_size=24, color=QC.THETA),
            MathTex(rf"\text{{median}} = {sci(rq['median'][k], 1)}", font_size=24, color=GOOD),
            wrapped_label(r"Pan and Owen (\textit{Math.\ Comp.}\ 2023): the median of independent randomisations of "
                          r"nets: conditional super-polynomial results require analytic derivative bounds and growing repetition count. "
                          r"Here 11 fixed repeats and 30 experiments use 30-bit grids; plateau near $8\times10^{-10}$ is consistent with grid bias, not double precision.", 4.6, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            f"This example compares the mean and median of eleven independently scrambled Sobol estimates of the exponential integral. RMSE uses thirty experiments. The full saved values are plotted. <bookmark mark='a'/> At the displayed thousand-point scale, the empirical RMSE ratio is {rq['mean'][k] / rq['median'][k]:.0f}. Pan and Owen's one-dimensional theorem assumes analytic derivative bounds and a repetition count growing with log sample size. Eleven fixed repeats do not meet that asymptotic condition, and this plot is not proof of a universal rate. The mean has no universal minus-three-halves ceiling for every integrand. Our SciPy construction uses a thirty-bit grid. Its uniform-grid leading bias for this integral is about minus eight times ten to minus ten, consistent with the median plateau. That plateau is far above double-precision machine epsilon."
        ) as vo:
            self.play(FadeIn(g), Create(lm), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(ld), FadeIn(leg[1]), FadeIn(side))
        self.wait(0.5)
        self.clear_scene()

    def papers(self):
        cards = [
            (2023, r"Pan and Owen, \textit{Math.\ Comp.}", r"medians of independently randomized net estimates: super-polynomial accuracy "
             r"under analytic and repetition-growth conditions; a multivariate follow-up (arXiv 2208.05078)."),
            (2024, r"Junike, \textit{Numerische Mathematik}", r"how many terms the COS method needs for a given error, "
             r"building on Junike and Pankrashkin's truncation range (2022)."),
            (2025, r"Bayer, Pelizzari, Schoenmakers (arXiv 2312.03444v2)", r"Longstaff--Schwartz and the dual bound with "
             r"signature features, for non-Markovian (rough) models: chapters 8--9 generalised (Part 14)."),
            (2024, r"Stamatopoulos and Zeng, \textit{Quantum}", r"derivative pricing by quantum signal processing: "
             r"a specified resource scenario, separating T-count and T-depth (chapter 18)."),
            (2025, r"Dalzell et al.\ (arXiv 2310.03011v2; Cambridge book)", r"a survey of quantum algorithms with end-to-end costs; its "
             r"finance section is the sober accounting of chapter 18."),
            (2018, r"Ga{\ss}, Glau, Mahlstedt, Mair; Glau, Kressner, Statti (2020)", r"Chebyshev and low-rank tensor "
             r"pricers: the offline--online split behind fast calibration."),
        ]
        g = VGroup(*[history_card(y, w, t, color=QC.IDEA, width=4.3, font_size=20) for y, w, t in cards])
        g.arrange_in_grid(rows=2, cols=3, buff=0.25)
        if g.height > 7.2:
            g.scale_to_fit_height(7.2)
        if g.width > 13.4:
            g.scale_to_fit_width(13.4)
        g.move_to(ORIGIN)
        with self.voiceover(
            "Selected reading, with assumptions and versions attached. Pan and Owen give analytic-integrand and repetition-growth conditions for median estimators. Junike's COS error control requires its density regularity, tail and derivative bounds; it does not turn any cumulant rule into an unconditional guarantee. <bookmark mark='a'/> Bayer, Pelizzari and Schoenmakers's signature-based primal and dual stopping paper was revised in twenty-twenty-five. It develops non-Markovian approximation and convergence under its stated assumptions. The twenty-twenty-four quantum signal-processing paper is a particular resource analysis, without a claim here that it remains globally cheapest. <bookmark mark='b'/> Dalzell and colleagues' end-to-end survey has a twenty-twenty-five revision and Cambridge book edition. Chebyshev and tensor methods illustrate how offline work may support faster later queries when smoothness and low-rank structure are available."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in g[:2]], lag_ratio=0.4))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in g[2:4]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in g[4:]], lag_ratio=0.4))
        self.wait(0.5)
        self.clear_scene()
