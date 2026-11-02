from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
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
            return float((1 - kind.get_value()) * np.exp(-KAP * x) + kind.get_value() * min(x ** (H0 - 0.5) / 2.5, 3.0))

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
        dot = always_redraw(lambda: Dot(g.ax.c2p(np.log10(T.get_value()), np.clip(np.log10(
            ((1 - kind.get_value()) * _vol_exp(T.get_value()) + kind.get_value() * _vol_power(T.get_value()))
            / T.get_value() ** 2), -1.6, 1.2)), radius=0.08, color=YELLOW))
        Tr = readout(r"T =", lambda: 365 * T.get_value(), digits=0, font_size=30, color=YELLOW,
                     unit=r"\ \text{days}").next_to(hint, DOWN, buff=0.25).align_to(hint, LEFT)
        fixed = VGroup(hint, g, leg, Tr)
        src = illustration(r"the first-order skew formula, flat forward variance", corner=DL)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-130 * DEGREES, zoom=0.9)
        self.add_fixed_in_frame_mobjects(fixed, dot, src)
        self.remove(fixed, dot, src)
        with self.voiceover(
            "Why should the skew be a power law at all? Here is the picture behind the answer. On the floor, a "
            "triangle: all pairs of times, t before u, up to the expiry T. Above each pair, the kernel: how much a "
            "shock to volatility at time t still moves the variance expected at the later time u. "
            "<bookmark mark='a'/> To first order in the vol of vol, the skew is the volume under this roof, divided "
            "by T squared. Start with a classical kernel, an exponential, as in Heston or Bergomi: the roof is almost "
            "flat. Shrink the expiry. The volume shrinks like T squared, so the ratio stays put: the skew of a "
            "one-factor Markov model is flat at short expiries. <bookmark mark='b'/> Now the rough kernel, the "
            "power law. The roof becomes a ridge that shoots up along the diagonal, where the lag is small. Shrink "
            "the expiry again, and the volume falls more slowly than T squared, because the ridge never flattens. "
            "<bookmark mark='c'/> The ratio grows like T to the power H minus a half: the power law, straight "
            "out of the shape of the kernel."
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
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"d\langle \ln S, \xi^u\rangle_t", r"=", r"\rho\,\sigma_t\,\xi_t(u)\,K(u - t)\,dt", font_size=36,
                  colors={r"d\langle \ln S, \xi^u\rangle_t": OPT}),
            cmath(r"\psi(T)", r"\approx", r"\frac{\rho}{2\sigma_0^3 T^2}\int_0^T\!\!\int_t^T \sigma_0\,\xi_0(u)\,K(u - t)"
                  r"\,du\,dt", font_size=36, colors={r"\psi(T)": IV}),
            cmath(r"\int_0^T\!\!\int_t^T e^{-\kappa(u - t)}", r"=", r"\frac{T}{\kappa} - \frac{1 - e^{-\kappa T}}{\kappa^2}",
                  font_size=36, colors={r"\int_0^T\!\!\int_t^T e^{-\kappa(u - t)}": VAR}),
            cmath(r"\int_0^T\!\!\int_t^T (u - t)^{H - \frac12}", r"=", r"\frac{T^{H + 3/2}}{(H + \frac12)(H + \frac32)}",
                  font_size=36, colors={r"\int_0^T\!\!\int_t^T (u - t)^{H - \frac12}": ROUGH}),
            cmath(r"\psi_{\rm rBergomi}(T)", r"\approx", r"\frac{\rho\,\eta\sqrt{2H}}{2(H + \frac12)(H + \frac32)}\,"
                  r"T^{H - 1/2}", font_size=36, colors={r"\psi_{\rm rBergomi}(T)": ROUGH}),
        ]
        whys = [why(r"a forward variance model: $\xi_t(u)$ is the variance expected at $u$; Itô's covariance with the spot"),
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
            "triangle, divided by twice sigma cubed T squared. A check: with a lognormal vol of vol, this gives "
            "SABR's well-known short skew, rho times nu over two. <bookmark mark='b'/> For an exponential kernel the "
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
                            r"Given a power law of the at-the-money skew in an option market, a continuous price with "
                            r"non-rough volatility admits an arbitrage. Non-rough models are inconsistent with a power-law "
                            r"skew; if the power law is real, volatility must be rough.", color=QC.IDEA, width=8.6,
                            font_size=24).move_to(UP * 0.6)
        sev = wrapped_label(r"and several exponentials, at time scales spread over decades, imitate a power law over the "
                            r"range they span: chapters 10 and 12", 9.0, 22, GREY_A).next_to(card, DOWN, buff=0.5)
        with self.voiceover(
            "Masaaki Fukasawa turned this into a theorem in 2021, with a title that says it all: volatility has to "
            "be rough. If the skew really follows a power law as expiry goes to zero, then a continuous price whose "
            "volatility is not rough admits an arbitrage. <bookmark mark='a'/> The escape hatch is the word "
            "really. Several exponentials, with time scales spread over decades, imitate a power law over the range "
            "they span, and no market quotes a zero-day option at the limit. Chapters ten and twelve walk through "
            "that hatch."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(sev))
        self.wait(0.4)
        self.clear_scene()

    def models(self, m):
        g = loglog_skew_axes(x_length=6.6, y_length=4.4, t_lo=2 / 365, y_range=(-2.0, 0.6)).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        mk = m["market"]
        dots = VGroup(*[Dot(ax.c2p(np.log10(a), np.log10(abs(b))), radius=0.07, color=WHITE)
                        for a, b in zip(mk["T"], mk["skew"]) if abs(b) > 0.01 and a >= 2 / 365])
        cols = {"Heston": MODEL_COL["Heston"], "jumps": BAD, "Bates": QC.DELTA, "rBergomi": MODEL_COL["rBergomi"],
                "rough Heston": MODEL_COL["rough Heston"]}
        names = {"Heston": r"Heston (Part 13's fit)", "jumps": r"jumps only (Bates' jumps)", "Bates": r"Bates: Heston + jumps",
                 "rBergomi": r"rough Bergomi (chapter 5)", "rough Heston": r"rough Heston, $H = 0.1$"}
        curves = VGroup()
        for k in ("Heston", "jumps", "Bates", "rBergomi", "rough Heston"):
            T = m[k]["T"] if "T" in m[k] else m["T"]
            curves.add(loglog_curve(ax, T, m[k]["skew"], cols[k], y_range=(-2.0, 0.6)))
        fm = m["formula"]
        form = DashedVMobject(loglog_curve(ax, fm["T"], fm["skew"], MODEL_COL["rBergomi"], y_range=(-2.0, 0.6),
                                           stroke_width=2), num_dashes=40)
        hdr = VGroup(label(r"", font_size=17), label(r"2--14 days", font_size=17, color=GREY_A),
                     label(r"2 months and longer", font_size=17, color=GREY_A))
        tab = VGroup()
        for k in ("market", "Heston", "jumps", "Bates", "rBergomi", "rough Heston"):
            c = WHITE if k == "market" else cols[k]
            nm = r"the Surface" if k == "market" else names[k]
            tab.add(VGroup(label(nm, font_size=16, color=c), MathTex(f"{m[k]['short']:.2f}", font_size=22, color=c),
                           MathTex(f"{m[k]['long']:.2f}", font_size=22, color=c)))
        grid = VGroup(hdr, *tab).arrange_in_grid(rows=7, cols=3, buff=(0.3, 0.14), col_alignments="lcc")
        cap = label(r"local exponent $a$ in $\psi \propto T^{-a}$", font_size=17, color=GREY_A)
        side = VGroup(cap, grid).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(g, RIGHT, buff=0.35).align_to(g, UP)
        if side.get_right()[0] > 6.9:
            side.scale_to_fit_width(6.9 - side.get_left()[0])
        hs, js = m["Heston"], m["jumps"]
        fnote = wrapped_label(rf"dashed: the first-order formula for rough Bergomi at its fitted $\eta = 2$: the right slope, "
                              rf"{m['ratio_formula_mc']:.1f} times too high, since a vol of vol that large is far from "
                              r"first order", 6.0, 17, GREY_A).next_to(side, DOWN, buff=0.3).align_to(side, LEFT)
        q = pause(r"Heston's mean reversion is $\kappa = 2$ a year. Over which expiries is its skew flat?", width=6.4,
                  font_size=22).to_corner(UR, buff=0.3)
        src = real_data(r"models priced by COS (Part 13) or Monte Carlo; the Surface, 10 December 2025", corner=DL)
        with self.voiceover(
            "Now the models themselves, priced exactly, with their skews against maturity on the same log scales "
            "as the market's. Pause and predict: a Heston model whose mean reversion is two a year. Over which "
            "expiries is its skew flat? <bookmark mark='a'/> Over everything well under six months. Part thirteen's "
            f"Heston fit has a local exponent of {hs['short']:.2f} between two days and two weeks: flat. "
            "<bookmark mark='b'/> Jumps alone go the other way: their skew falls like one over maturity, an "
            f"exponent of {js['short']:.2f}, too steep. Heston with jumps sits in between, by mixing the two. "
            "<bookmark mark='c'/> The rough models produce the power law from the kernel itself. The dashed line is "
            "the first-order formula for rough Bergomi: the right slope, but too high, because the fitted vol of "
            "vol is far from small. <bookmark mark='d'/> The market's own short-end exponent is "
            f"{m['market']['short']:.2f}. One factor with one time scale cannot make a power law; a kernel with all "
            "time scales can."
        ) as vo:
            self.play(FadeIn(g), FadeIn(dots), FadeIn(src), FadeIn(q))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(hdr), FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(Create(curves[1]), Create(curves[2]), FadeIn(tab[2]), FadeIn(tab[3]), FadeOut(q))
            vo.wait_until("c")
            self.play(Create(curves[3]), Create(curves[4]), FadeIn(tab[4]), FadeIn(tab[5]), Create(form), FadeIn(fnote))
            vo.wait_until("d")
            self.play(Indicate(tab[0], color=YELLOW))
        self.wait(0.4)
        self.clear_scene()
