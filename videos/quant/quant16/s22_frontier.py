from __future__ import annotations

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, fixed, illustration, load, loglog, polyline, predict


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
        c = chapter_card(19, r"Frontier: pricing faster, 2023--2026", r"Where is computational pricing research now?",
                         lit=(2024,), part=PART)
        with self.voiceover("Chapter nineteen. The frontier: pricing faster, from 2023 to 2026."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def chebyshev(self, ch):
        (x0, x1), (y0, y1) = ch["box"]
        xs, ys = np.asarray(ch["xs"]), np.asarray(ch["ys"])
        ax = ThreeDAxes(x_range=[x0, x1, 15], y_range=[y0, y1, 0.02], z_range=[-8, 0, 2], x_length=6.6, y_length=5.0,
                        z_length=3.0, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False,
                                                               "stroke_width": 2})
        ax.shift(DOWN * 0.4)
        rows = ch["rows"]

        def surf(r):
            f = RegularGridInterpolator((xs, ys), np.clip(np.asarray(r["err_surface"]), -8, 0))
            sf = Surface(lambda u, v: ax.c2p(u, v, float(f((u, v)))), u_range=[x0, x1], v_range=[y0, y1],
                         resolution=(24, 24), fill_opacity=0.85, stroke_width=0.3, stroke_color="#0E1117",
                         checkerboard_colors=False)
            sf.set_fill_by_value(axes=ax, colorscale=[(QC.GAIN, -7), (QC.DELTA, -4), (QC.LOSS, -1)], axis=2)
            return sf

        def nodes(r):
            return VGroup(*[Dot3D(ax.c2p(a, b, -8), radius=0.03, color=GREY_A, resolution=(4, 4))
                            for a in r["x"] for b in r["y"]])

        show = [r for r in rows if r["n"] in (4, 8, 16, 32)]
        hint = VGroup(label(r"across: spot $S_0$ (70 to 130)", font_size=21, color=GREY_A),
                      label(r"back: initial variance $v_0$ (0.01 to 0.09)", font_size=21, color=GREY_A),
                      label(r"up: $\log_{10}$ error of the interpolant", font_size=21, color=GREY_A),
                      label(r"floor: the Chebyshev nodes (COS prices)", font_size=21, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        tags = [MathTex(rf"{r['n']}\times{r['n']}\ \text{{nodes: max error}}\ {r['max_err']:.1e}", font_size=28,
                        color=OPT).to_corner(UR, buff=0.4) for r in show]
        self.set_camera_orientation(phi=64 * DEGREES, theta=-58 * DEGREES, zoom=0.85)
        fixed(self, hint, *tags)
        s = surf(show[0])
        nd = nodes(show[0])
        with self.voiceover(
            "First, a pricer that is trained, then used. Gaß, Glau, Mahlstedt and Mair proposed in 2018 to price an "
            "option at Chebyshev nodes over a box of parameters, here the spot and Heston's initial variance, and "
            "interpolate everywhere else. The floor shows the nodes, crowded toward the edges; the surface is the "
            "interpolant's error, on a log scale. <bookmark mark='a'/> Four by four nodes: errors near "
            f"{show[0]['max_err']:.1f}. Eight by eight, then sixteen, then thirty-two. <bookmark mark='b'/> The error "
            "surface collapses, a factor of ten for every few nodes added: the exponential convergence of polynomial "
            f"interpolation for analytic functions. At thirty-two by thirty-two the worst error over the whole box is "
            f"about {show[-1]['max_err'] * 1e6:.0f} in a million."
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

    def speed(self, ch, race):
        rows = ch["rows"]
        last = rows[-1]
        mc = min((q for q in race["points"] if q["method"].startswith("Monte Carlo")), key=lambda q: q["err"])
        items = [(r"Chebyshev interpolant, one query", ch["t_cheb"], GOOD),
                 (r"COS, one price (512 terms)", ch["t_cos"], OPT),
                 (rf"Monte Carlo, error {mc['err']:.3f}", mc["time"], BAD)]
        g = axes([-4.5, 1], [0, 4], x_length=7.0, y_length=3.0, xlabel=r"seconds per price (log)",
                 xticks=[-4, -2, 0], xfmt=lambda v: f"10^{{{int(v)}}}", font_size=15).to_edge(LEFT, buff=3.2).shift(UP * 0.5)
        ax = g.ax
        bars = VGroup()
        for i, (nm, t, col) in enumerate(items):
            y = 3 - i
            x1 = np.log10(t)
            bars.add(VGroup(Rectangle(width=max(ax.c2p(x1, 0)[0] - ax.c2p(-4.5, 0)[0], 0.02), height=0.5, stroke_width=0,
                                      fill_color=col, fill_opacity=0.85).move_to(ax.c2p(-4.5, y), aligned_edge=LEFT),
                            label(nm, font_size=17, color=col).next_to(ax.c2p(-4.5, y), LEFT, buff=0.15),
                            MathTex(rf"{t * 1e3:.3g}\,\text{{ms}}", font_size=20, color=GREY_A).next_to(ax.c2p(x1, y), RIGHT,
                                                                                                   buff=0.1)))
        build = last["calls"] * ch["t_cos"]
        q = predict(rf"The pricer needs {last['calls']:,} COS prices to build. When does it pay?".replace(",", "{,}"),
                    width=6.0, font_size=21).to_edge(DOWN, buff=0.4)
        note_ = wrapped_label(r"low-rank tensor formats (Glau, Kressner and Statti 2020) take the idea to many parameters; "
                              r"Part 17's networks are the learned version", 10.0, 18, GREY_A).next_to(q, UP, buff=0.3)
        with self.voiceover(
            f"The bill: {last['calls']:,} COS prices to build it, once. A query then costs "
            f"{ch['t_cheb'] * 1e3:.2f} milliseconds against {ch['t_cos'] * 1e3:.2f} for a COS price, "
            f"{ch['t_cos'] / ch['t_cheb']:.0f} times less, and against seconds for a simulation. "
            "<bookmark mark='a'/> Pause and predict: when does it pay? After roughly as many queries as it cost to "
            "build, which a calibration or a scenario run reaches in seconds; and far sooner when the pricer it "
            "replaces is slow. Low-rank tensors extend it to many parameters, and Part seventeen's networks are "
            "the learned version of the same idea."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.4, run_time=2.5))
            vo.wait_until("a")
            self.play(FadeIn(q), FadeIn(note_))
        self.wait(0.5)
        self.clear_scene()

    def median(self, rq):
        ns = np.log10(rq["ns"])
        g = loglog(1, 3.8, -10, -2, r"points per scrambled Sobol set", r"RMSE of $\int_0^1 e^u\,du$", x_length=6.4,
                   y_length=4.2, xt=[1, 2, 3], yt=[-10, -8, -6, -4, -2]).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        lm = polyline(ax, ns, np.clip(np.log10(rq["mean"]), -10, -2), QC.THETA)
        ld = polyline(ax, ns, np.clip(np.log10(rq["median"]), -10, -2), GOOD)
        leg = legend([(QC.THETA, r"mean of 11 scramblings"), (GOOD, r"median of 11 scramblings")], font_size=17)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        k = 3
        side = VGroup(
            MathTex(rf"n = {rq['ns'][k]:,}".replace(",", "{,}") + rf":\ \ \text{{mean}}\ {rq['mean'][k]:.1e},\ \ "
                    rf"\text{{median}}\ {rq['median'][k]:.1e}", font_size=26, color=GOOD),
            wrapped_label(r"Pan and Owen (\textit{Math.\ Comp.}\ 2023): the median of independent randomisations of a "
                          r"net converges super-polynomially for smooth integrands; the mean cannot beat $n^{-3/2}$. "
                          r"Here the median reaches double precision's floor by $n = 4{,}096$", 4.6, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Second, measured: an idea from Zexin Pan and Art Owen, published in 2023. Scramble a Sobol net eleven "
            "times. The usual estimate is the mean of the eleven. Take the median instead. "
            "<bookmark mark='a'/> On a smooth integral, the mean's error falls like n to the minus three halves, the "
            "best a scrambled net can do on average. The median falls faster than any power: at a thousand points it "
            f"is {rq['mean'][k] / rq['median'][k]:,.0f} times more accurate, and soon it hits the floor of double "
            "precision. One line of code changed."
        ) as vo:
            self.play(FadeIn(g), Create(lm), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(ld), FadeIn(leg[1]), FadeIn(side))
        self.wait(0.5)
        self.clear_scene()

    def papers(self):
        cards = [
            (2023, r"Pan and Owen, \textit{Math.\ Comp.}", r"median-of-means for randomized nets: super-polynomial accuracy "
             r"in one dimension; a multivariate follow-up (arXiv 2208.05078)."),
            (2024, r"Junike, \textit{Numerische Mathematik}", r"how many terms the COS method needs for a given error, "
             r"building on Junike and Pankrashkin's truncation range (2022)."),
            (2023, r"Bayer, Pelizzari, Schoenmakers (arXiv 2312.03444)", r"Longstaff--Schwartz and the dual bound with "
             r"signature features, for non-Markovian (rough) models: chapters 8--9 generalised (Part 14)."),
            (2024, r"Stamatopoulos and Zeng, \textit{Quantum}", r"derivative pricing by quantum signal processing: the "
             r"cheapest resource estimate so far (chapter 18)."),
            (2023, r"Dalzell et al.\ (arXiv 2310.03011)", r"a survey of quantum algorithms with end-to-end costs; its "
             r"finance section is the sober accounting of chapter 18."),
            (2018, r"Ga{\ss}, Glau, Mahlstedt, Mair; Glau, Kressner, Statti (2020)", r"Chebyshev and low-rank tensor "
             r"pricers: the offline--online split behind fast calibration."),
        ]
        g = VGroup(*[history_card(y, w, t, color=QC.IDEA, width=4.3, font_size=16) for y, w, t in cards])
        g.arrange_in_grid(rows=2, cols=3, buff=0.25)
        if g.height > 7.2:
            g.scale_to_fit_height(7.2)
        if g.width > 13.4:
            g.scale_to_fit_width(13.4)
        g.move_to(ORIGIN)
        with self.voiceover(
            "The reading list for the frontier. Pan and Owen's medians. Gero Junike's bound on how many cosine terms "
            "a target error needs, which turns chapter sixteen's rule of thumb into a guarantee. <bookmark mark='a'/> "
            "Christian Bayer, Luca Pelizzari and John Schoenmakers's Longstaff–Schwartz and dual bounds with "
            "signature features, for rough volatility, where the state is the whole path. Stamatopoulos and Zeng's "
            "quantum signal processing. <bookmark mark='b'/> A survey of quantum algorithms with end-to-end costs; "
            "and the Chebyshev and tensor pricers."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in g[:2]], lag_ratio=0.4))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in g[2:4]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in g[4:]], lag_ratio=0.4))
        self.wait(0.5)
        self.clear_scene()
