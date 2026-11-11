from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import axes, data_range, skew_range
from videos.quant.quant14.common import (BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, VAR, illustration, load,
                                         loglog_curve, loglog_skew_axes, pause, real_data)

H0, KAP = 0.1, 2.0


def _vol_power(T, H=H0):
    return T ** (H + 1.5) / ((H + 0.5) * (H + 1.5))


def _vol_exp(T, k=KAP):
    return T / k - (1 - np.exp(-k * T)) / k ** 2


class SkewMath(VoiceoverScene, ThreeDScene):
    def construct(self):
        m = load("skew_models")
        self.card()
        self.triangle()
        self.derive()
        self.models(m)

    def card(self):
        c = chapter_card(2, r"Why a power law: the skew from the kernel",
                         r"Which models can make the skew explode, and why?", part=PART)
        with self.voiceover("Chapter two. Why a power law: the skew from the kernel."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def triangle(self):
        ax = ThreeDAxes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], z_range=[0, 3, 1], x_length=5.0, y_length=5.0,
                        z_length=3.0, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False})
        ax.shift(LEFT * 2.2 + DOWN * 0.4)
        T = ValueTracker(1.0)
        kind = ValueTracker(0.0)   # 0: exponential kernel, 1: power kernel

        def K(x):
            x = max(x, 1e-4)
            return float((1 - kind.get_value()) * np.exp(-KAP * x) + kind.get_value() * min(x ** (H0 - 0.5) / 2.5, 2.2))

        def surf():
            TT = T.get_value()
            s = Surface(lambda u, v: ax.c2p(u * v * TT, v * TT, K(v * TT * (1 - u))), u_range=[0, 1], v_range=[0, 1],
                        resolution=(10, 12), fill_opacity=0.75, stroke_width=0.3, stroke_color=GREY_D)
            s.set_fill(interpolate_color(ManimColor(VAR), ManimColor(ROUGH), kind.get_value()), opacity=0.75)
            return s

        sf = always_redraw(surf)
        floor = always_redraw(lambda: Polygon(ax.c2p(0, 0, 0), ax.c2p(0, T.get_value(), 0),
                                              ax.c2p(T.get_value(), T.get_value(), 0), stroke_color=YELLOW,
                                              stroke_width=2, fill_color=YELLOW, fill_opacity=0.15))
        hint = VGroup(label(r"floor: the triangle $0 < t < u < T$", font_size=20, color=YELLOW),
                      label(r"height: the kernel $K(u - t)$", font_size=20, color=GREY_A),
                      label(r"volume $\div\, T^2$: the skew (to first order)", font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).to_corner(UL, buff=0.3)
        g = loglog_skew_axes(x_length=4.4, y_length=3.4, t_lo=1 / 365, y_range=(-1.6, 1.2), font_size=13,
                             ylabel=r"volume$/T^2$ (log)").to_corner(DR, buff=0.4)
        Tg = np.exp(np.linspace(np.log(1 / 365), 0, 60))
        ce = loglog_curve(g.ax, Tg, _vol_exp(Tg) / Tg ** 2, VAR, y_range=(-1.6, 1.2))
        cp = loglog_curve(g.ax, Tg, _vol_power(Tg) / Tg ** 2, ROUGH, y_range=(-1.6, 1.2))
        leg = legend([(VAR, rf"exponential $e^{{-{KAP:g}\tau}}$: flat, then $1/T$"),
                      (ROUGH, rf"power $\tau^{{H - 1/2}}$, $H = {H0:g}$: $T^{{H - 1/2}}$")], font_size=15).next_to(
            g, UP, buff=0.15)
        def dot_at():
            return g.ax.c2p(np.log10(T.get_value()), np.clip(np.log10(
                ((1 - kind.get_value()) * _vol_exp(T.get_value()) + kind.get_value() * _vol_power(T.get_value()))
                / T.get_value() ** 2), -1.6, 1.2))
        dot = Dot(dot_at(), radius=0.08, color=YELLOW)  # one dot, moved: it stays pinned to the frame
        dot.add_updater(lambda m: m.move_to(dot_at()))
        Tr = readout(r"T =", lambda: 365 * T.get_value(), digits=0, font_size=30, color=YELLOW,
                     unit=r"\ \text{days}").next_to(hint, DOWN, buff=0.25).align_to(hint, LEFT)
        fixed = VGroup(hint, g, leg, Tr)
        src = illustration(r"the first-order skew formula, flat forward variance", corner=DL)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-130 * DEGREES, zoom=0.9)
        self.add_fixed_in_frame_mobjects(fixed, dot, src, ce, cp)
        self.remove(fixed, dot, src, ce, cp)
        cam = self.renderer.camera
        Tr[1].add_updater(lambda m: cam.add_fixed_in_frame_mobjects(m))  # the number rebuilds itself: pin it again
        with self.voiceover(
            """Why can a rough kernel produce a power-law skew? The floor contains all pairs t before u before expiry T. The height illustrates a forward-variance response to a shock. <bookmark mark='a'/> For flat initial forward variance and small volatility of volatility, the leading signed skew is proportional to the kernel integral over this triangle, divided by T squared. An exponential kernel is locally bounded: at maturities far below its decay time, that ratio approaches a constant. <bookmark mark='b'/> The ideal power kernel has an integrable diagonal singularity. Its uncapped integral scales as T to H plus three halves. The displayed roof is divided by two point five and capped for visibility; it is not the literal volume used by the curve on the right. <bookmark mark='c'/> Dividing the analytical integral by T squared gives T to H minus a half. These are leading-order model statements, with amplitudes and validity depending on the model."""
        ) as vo:
            self.play(Create(ax), FadeIn(sf), FadeIn(floor), FadeIn(hint), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(leg[0]), FadeIn(Tr), FadeIn(dot), Create(ce))
            self.play(T.animate.set_value(3 / 365), run_time=5, rate_func=smooth)
            vo.wait_until("b")
            self.play(T.animate.set_value(1.0), run_time=1.5)
            self.play(kind.animate.set_value(1.0), run_time=2)
            self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES, run_time=2)
            vo.wait_until("c")
            self.play(Create(cp), FadeIn(leg[1]))
            self.play(T.animate.set_value(3 / 365), run_time=5, rate_func=smooth)
        for m in (sf, floor, dot, Tr):
            m.clear_updaters()
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0,
                         added_anims=[FadeOut(VGroup(ax, sf, floor)), FadeOut(fixed), FadeOut(dot), FadeOut(src),
                                      FadeOut(VGroup(ce, cp))], run_time=1.2)
        self.clear_scene(run_time=0.1)

    def derive(self):
        rows = [
            cmath(r"d\langle \ln S, \xi^u\rangle_t", r"=", r"\rho\,\sigma_t\,\xi_t(u)\,K(u - t)\,dt", font_size=36,
                  colors={r"d\langle \ln S, \xi^u\rangle_t": OPT}),
            cmath(r"s(T)", r"\approx", r"\frac{\rho}{2\sigma_0^3 T^2}\int_0^T\!\!\int_t^T \sigma_0\,\xi_0(u)\,K(u - t)"
                  r"\,du\,dt", font_size=36, colors={r"s(T)": IV}),
            cmath(r"\int_0^T\!\!\int_t^T e^{-\kappa(u - t)}", r"=", r"\frac{T}{\kappa} - \frac{1 - e^{-\kappa T}}{\kappa^2}",
                  font_size=36, colors={r"\int_0^T\!\!\int_t^T e^{-\kappa(u - t)}": VAR}),
            cmath(r"\int_0^T\!\!\int_t^T (u - t)^{H - \frac12}", r"=", r"\frac{T^{H + 3/2}}{(H + \frac12)(H + \frac32)}",
                  font_size=36, colors={r"\int_0^T\!\!\int_t^T (u - t)^{H - \frac12}": ROUGH}),
            cmath(r"s_{\rm rBergomi}(T)", r"\approx", r"\frac{\rho\,\eta\sqrt{2H}}{2(H + \frac12)(H + \frac32)}\,"
                  r"T^{H - 1/2}", font_size=36, colors={r"s_{\rm rBergomi}(T)": ROUGH}),
        ]
        whys = [why('signed skew $s=\\partial_k\\sigma_{\\rm imp}(0,T)$; plotted magnitude $\\psi=|s|$'),
                why(r"to first order in vol of vol, the skew is the integrated spot--variance covariance (Bergomi and "
                    r"Guyon 2012); check: lognormal vol of vol $\nu$ gives SABR's short skew $\rho\nu/2$"),
                why(r"$\approx T^2/2$ for $T \ll 1/\kappa$: a flat skew; $\approx T/\kappa$ for $T \gg 1/\kappa$: a skew "
                    r"falling like $1/T$"),
                why(r"integrate twice: the skew grows like $T^{H - 1/2}$ (Al\`os, Le\'on and Vives 2007; Fukasawa 2011)"),
                why(r"rough Bergomi's kernel is $\eta\sqrt{2H}\,\tau^{H - 1/2}$ (Bayer, Friz and Gatheral 2016)")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "Now the algebra behind the picture. In a forward variance model, the variance expected at a later "
            "time u moves with the spot: their covariance is rho, times the volatility, times the forward "
            "variance, times the kernel at lag u minus t. <bookmark mark='a'/> To first order in the vol of vol, "
            "Lorenzo Bergomi and Julien Guyon showed, the at-the-money skew is that covariance integrated over the "
            "triangle, divided by twice sigma cubed T squared. <bookmark mark='b'/> For an exponential kernel the "
            "double integral is T over kappa minus a correction: about T squared over two at short expiries, so a "
            "flat skew; about T over kappa at long ones, so a skew that falls like one over T. "
            "<bookmark mark='c'/> For the power kernel, integrate twice: T to the H plus three halves. Divide by T "
            "squared: T to the H minus a half. <bookmark mark='d'/> And with rough Bergomi's own kernel, the "
            "constant in front is explicit."
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
        self.wait(0.4)
        self.clear_scene()
        card = history_card(2021, r"Fukasawa: ``Volatility has to be rough'' (Quantitative Finance 21(1))",
                            'For a positive continuous It\\^o price with positive $H_0$-H\\"older instantaneous variance, a persistent-sign near-ATM $H$-power law as expiry tends to a fixed date gives arbitrage when $0<H<H_0$ and $H<1/2$, under the paper\\textquotesingle s frictionless option-market assumptions. Finite-window magnitude fits do not verify these hypotheses.', color=QC.IDEA, width=8.6,
                            font_size=24).move_to(UP * 0.6)
        sev = wrapped_label(r"and several exponentials, at time scales spread over decades, imitate a power law over the "
                            r"range they span: chapters 10 and 12", 9.0, 22, GREY_A).next_to(card, DOWN, buff=0.5)
        with self.voiceover(
            """Fukasawa's 2021 theorem concerns a precise limiting market. Prices are positive continuous Itô processes, instantaneous variance is positive and locally Hölder regular, and frictionless options are available near a fixed expiry. A persistent-sign near-at-the-money power law with exponent H below one half conflicts with variance regularity strictly above H. <bookmark mark='a'/> Our finite-maturity magnitude fits, including sign changes, do not verify those assumptions. Regularized kernels and several exponentials can imitate a power law over a finite interval. The theorem distinguishes limiting behavior, not the winner of this finite-data comparison."""
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(sev))
        self.wait(0.4)
        self.clear_scene()

    def models(self, m):
        yr = skew_range(*[v["skew"] for v in m.values() if isinstance(v, dict) and "skew" in v])
        g = loglog_skew_axes(x_length=6.6, y_length=4.4, t_lo=2 / 365, y_range=yr).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        mk = m["market"]
        dots = VGroup(*[Dot(ax.c2p(np.log10(a), np.log10(abs(b))), radius=0.07, color=WHITE)
                        for a, b in zip(mk["T"], mk["skew"]) if np.isfinite(b) and abs(b) > 0 and a >= 2 / 365])
        cols = {"Heston": MODEL_COL["Heston"], "jumps": BAD, "Bates": QC.DELTA, "rBergomi": MODEL_COL["rBergomi"],
                "rough Heston": MODEL_COL["rough Heston"]}
        names = {"Heston": r"Heston (Part 13's fit)", "jumps": 'constant vol + Bates jump parameters', "Bates": r"Bates: Heston + jumps",
                 "rBergomi": r"rough Bergomi (chapter 5)", "rough Heston": r"rough Heston, $H = 0.1$"}
        curves = VGroup()
        for k in ("Heston", "jumps", "Bates", "rBergomi", "rough Heston"):
            T = m[k]["T"] if "T" in m[k] else m["T"]
            curves.add(loglog_curve(ax, T, m[k]["skew"], cols[k], y_range=yr))
        fm = m["formula"]
        form = DashedVMobject(loglog_curve(ax, fm["T"], fm["skew"], MODEL_COL["rBergomi"], y_range=yr,
                                           stroke_width=2), num_dashes=40)
        hdr = VGroup(label(r"", font_size=17), label('short window*', font_size=17, color=GREY_A),
                     label('long window*', font_size=17, color=GREY_A))
        tab = VGroup()
        for k in ("market", "Heston", "jumps", "Bates", "rBergomi", "rough Heston"):
            c = WHITE if k == "market" else cols[k]
            nm = r"the Surface" if k == "market" else names[k]
            tab.add(VGroup(label(nm, font_size=16, color=c), MathTex(f"{m[k]['short']:.2f}", font_size=22, color=c),
                           MathTex(f"{m[k]['long']:.2f}", font_size=22, color=c)))
        # lay out the cells themselves (hdr and the rows keep pointing at them, so the fades below still work)
        VGroup(*hdr, *[c for row in tab for c in row]).arrange_in_grid(rows=len(tab) + 1, cols=3, buff=(0.3, 0.14),
                                                                        col_alignments="lcc")
        grid = VGroup(hdr, *tab)
        cap = label(r"local exponent $a$ in $\psi \propto T^{-a}$", font_size=17, color=GREY_A)
        side = VGroup(cap, grid).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(g, RIGHT, buff=0.35).align_to(g, UP)
        if side.get_right()[0] > 6.9:
            side.scale_to_fit_width(6.9 - side.get_left()[0])
        hs, js = m["Heston"], m["jumps"]
        fnote = wrapped_label('dashed: leading flat-curve/small-$\\eta$ formula; finite-grid Monte Carlo need not match its slope or level. *Windows and skew stencils differ; see notes.', 6.0, 17, GREY_A).next_to(side, DOWN, buff=0.3).align_to(side, LEFT)
        q = pause(r"Heston's mean reversion is $\kappa = 2$ a year. Over which expiries is its skew flat?", width=6.4,
                  font_size=22).to_corner(UR, buff=0.3)
        src = real_data(r"models priced by COS (Part 13) or Monte Carlo; the Surface, 10 December 2025", corner=DL)
        with self.voiceover(
            f"""Now finite-grid numerical prices. First consider the illustrative exponential decay rate of two per year. Its leading-order skew is approximately flat only well below six months, with other model scales also relevant. <bookmark mark='a'/> The plotted Heston curve instead uses Part thirteen's fitted decay rate, about fourteen point eight. Its fitted short-window exponent is {hs['short']:.2f}. <bookmark mark='b'/> The red curve combines constant diffusion with Bates' fitted jump parameters. Its finite-difference exponent is {js['short']:.2f}; this is not a universal jump-model asymptotic. Bates mixes diffusion variance dynamics and jumps. <bookmark mark='c'/> Rough-model curves and the dashed leading formula also differ on these grids. Small-volatility-of-volatility theory is not an exact finite-grid prediction. <bookmark mark='d'/> The market's short-window exponent is {m['market']['short']:.2f}. Model fits mostly use two to fourteen and sixty to three hundred sixty-five days; the market and rough Bergomi use different windows. Skew stencils differ too. These scores describe the recorded calculations; they do not establish that one kernel class is necessary. Next: measuring roughness."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(dots), FadeIn(src), FadeIn(q))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(hdr), FadeIn(tab[0]), FadeIn(tab[1]), FadeOut(q))  # the table takes its place
            vo.wait_until("b")
            self.play(Create(curves[1]), Create(curves[2]), FadeIn(tab[2]), FadeIn(tab[3]))
            vo.wait_until("c")
            self.play(Create(curves[3]), Create(curves[4]), FadeIn(tab[4]), FadeIn(tab[5]), Create(form), FadeIn(fnote))
            vo.wait_until("d")
            self.play(Indicate(tab[0], color=YELLOW))
        self.wait(0.4)
        self.clear_scene()
