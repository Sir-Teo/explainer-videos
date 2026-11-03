from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import volsurface as V
from videos.quant.quant12.common import (BAD, IV, LV, OPT, PART, RV, SPOT, axes3, fixed, load, real_data, surf3)


def _iv_from(pv, Ts):
    rho, eta, gam, th = pv[0], pv[1], pv[2], np.asarray(pv[3:])
    fit = {"rho": rho, "eta": eta, "gamma": gam, "theta": th, "T": Ts}
    return lambda k, T: float(np.sqrt(max(V.ssvi_surface_w(fit, k, T), 1e-8) / T))


class SSVI(VoiceoverScene, ThreeDScene):
    def construct(self):
        r = load("ssvi_replay")
        s = load("surface")
        self.card()
        self.build(s)
        self.lab(r)
        self.replay(r)
        self.theorems(r)
        self.price(r)

    def card(self):
        c = chapter_card(5, r"SSVI: the whole surface in one formula", r"Can a surface be arbitrage-free by construction?",
                         lit=(2014,), part=PART)
        with self.voiceover("Chapter five. SSVI: the whole surface in one formula."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def build(self, s):
        fit = s["ssvi"]
        zmax = max(float(V.ssvi_surface_w(fit, k_, T_)) for k_ in (-0.4, 0.0, 0.4) for T_ in (0.4, 0.8))
        zmax = float(np.ceil(zmax / 0.04) * 0.04)  # the whole surface fits: no flat-topped plateau
        ax = axes3([-0.4, 0.4, 0.2], [0, 0.8, 0.2], [0, zmax, 0.04], x_length=7.0, y_length=5.0, z_length=3.0)
        Ts = np.asarray(fit["T"])
        th = np.asarray(fit["theta"])
        self.set_camera_orientation(phi=66 * DEGREES, theta=-58 * DEGREES, zoom=0.85)
        floor = VMobject(color=LV, stroke_width=4).set_points_smoothly([ax.c2p(-0.4, t, float(x)) for t, x in zip(Ts, th)
                                                                       if x <= zmax])
        thdots = VGroup(*[Dot3D(ax.c2p(-0.4, t, float(x)), radius=0.05, color=LV, resolution=(4, 4)) for t, x in zip(Ts, th)
                          if x <= zmax])
        kk = np.linspace(-0.4, 0.4, 41)
        slices = VGroup()
        for t, x in zip(Ts, th):
            w = V.ssvi_w(kk, x, fit["rho"], fit["eta"], fit["gamma"])
            if w.max() > zmax:
                continue
            slices.add(VMobject(color=IV, stroke_width=3).set_points_smoothly([ax.c2p(a, t, float(b)) for a, b in zip(kk, w)]))
        sf = surf3(ax, lambda k, T: float(V.ssvi_surface_w(fit, k, T)), (-0.4, 0.4), (0.01, 0.8), 0.0, zmax,
                   colors=[(QC.SPOT, 0.0), (IV, 0.4 * zmax), (QC.LOSS, zmax)], resolution=(24, 14), opacity=0.6)
        t1 = label(r"$\theta_T$: at-the-money total variance, rising with $T$", font_size=22, color=LV).to_corner(UL, buff=0.35)
        t2 = label(r"one smile shape for every $\theta$, scaled by $\varphi(\theta)$", font_size=22, color=IV).next_to(t1, DOWN,
                                                                                                             aligned_edge=LEFT)
        hint = VGroup(label(r"across: log-moneyness", font_size=18, color=GREY_B), label(r"depth: years", font_size=18,
                                                                                          color=GREY_B),
                      label(r"up: total variance $w$", font_size=18, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.08).to_corner(UR, buff=0.35)
        fixed(self, t1, t2, hint)
        with self.voiceover(
            "SVI fits one expiry. Gatheral and Antoine Jacquier's surface SVI, from 2014, fits them all at once. Start "
            "with one number per expiry: theta, the at-the-money total variance, which must rise with maturity. Here "
            "it is, climbing along the left wall. <bookmark mark='a'/> Then hang the same smile over every theta, its "
            "width set by one function, phi of theta, and its tilt by one correlation, rho. <bookmark mark='b'/> "
            "Sweep the slices together and you have a surface with only three shape parameters, plus the thetas."
        ) as vo:
            self.play(Create(ax), FadeIn(hint), FadeIn(t1), Create(floor), FadeIn(thdots))
            vo.wait_until("a")
            self.play(FadeIn(t2), LaggedStart(*[Create(x) for x in slices], lag_ratio=0.2, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(sf), run_time=1.5)
            self.move_camera(theta=-30 * DEGREES, run_time=max(vo.remaining(0.5) - 0.5, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, floor, thdots, slices, sf)),
                                                                  FadeOut(t1), FadeOut(t2), FadeOut(hint)], run_time=1)
        self.clear_scene()

    def lab(self, r):
        card = lab_card(r"fitting SSVI to the Surface", [
            "def unpack(x):",
            "    rho, eta, gam = np.tanh(x[0]), np.exp(x[1]), 1 / (1 + np.exp(-x[2]))",
            "    eta = min(eta, 2 / (1 + abs(rho)))",
            "    theta = np.cumsum(np.exp(x[3:]))",
            "    return rho, eta, gam, theta",
            "",
            "def resid(x):",
            "    rho, eta, gam, theta = unpack(x)",
            "    th = theta[np.searchsorted(Ts, T)]",
            "    return np.sqrt(wt) * (ssvi_w(k, th, rho, eta, gam) - w)",
            "",
            "r = optimize.least_squares(resid, x0, max_nfev=5000)",
        ], source="explainer/quant/house/volsurface.py", width=8.4).to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.5)
        f = r["fit"]
        th = np.asarray(r["theta"])
        rm = r["rmse"]
        with self.voiceover(
            "The House's fitter is a dozen lines, and the trick is the unpacking: the optimizer searches freely, and "
            "every constraint lives in the map to the model's parameters. A hyperbolic tangent keeps rho inside minus "
            "one and one, eta is clipped to the butterfly bound, and the thetas are sums of exponentials, so they "
            "can only rise. "
            f"<bookmark mark='a'/> On the Surface's quotes, weighted by vega: rho {f['rho']:.2f}, eta {f['eta']:.2f}, "
            f"gamma {f['gamma']:.2f}, and an error of {rm:.2f} volatility points."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, [f"rho={f['rho']:.3f}  eta={f['eta']:.3f}  gamma={f['gamma']:.3f}",
                                 "theta=" + " ".join(f"{x:.4f}" for x in th[:5]) + " ...",
                                 f"vega-weighted rmse {rm:.2f} vol points;  eta(1+|rho|) = {r['eta_rho']:.3f} <= 2"])
        self.wait(0.6)
        self.clear_scene()

    def replay(self, r):
        runs = r["runs"]
        Ts = np.asarray(r["Ts"])
        j = int(np.argmax([x["loss"][0] for x in runs]))
        run = runs[j]
        frames, fi = np.asarray(run["frames"]), list(run["frames_i"])
        k, T, iv = np.asarray(r["k"]), np.asarray(r["T"]), np.asarray(r["iv"])
        ax = axes3([-0.4, 0.4, 0.2], [0, 0.8, 0.2], [0.3, 0.9, 0.1], x_length=6.2, y_length=4.4, z_length=2.8,
                   shift=LEFT * 2.2 + DOWN * 0.5)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-58 * DEGREES, zoom=0.85)
        m = (np.abs(k) <= 0.4) & (T <= 0.8) & (iv >= 0.3) & (iv <= 0.9)
        dots = VGroup(*[Dot3D(ax.c2p(a, b, c), radius=0.03, color=WHITE, resolution=(4, 4)) for a, b, c in
                        zip(k[m], T[m], iv[m])])
        pick = [0, 2, 4, 7, 11, 16, 22, len(frames) - 1]
        pick = sorted(set(min(p, len(frames) - 1) for p in pick))

        def surf(i):
            return surf3(ax, _iv_from(frames[i], Ts), (-0.4, 0.4), (0.02, 0.8), 0.3, 0.9, resolution=(18, 10), opacity=0.7)
        cur = surf(pick[0])
        # the loss panel, fixed in frame: every start as a faint line, the replayed one bright
        Lmax = max(len(x["loss"]) for x in runs)
        lo = np.log10(max(min(min(x["loss"]) for x in runs), 1e-3))
        hi = np.log10(max(x["loss"][0] for x in runs) * 1.2)
        g = axes([0, Lmax], [lo, hi], x_length=4.6, y_length=3.2, xlabel=r"residual evaluations",
                 ylabel=r"vega-weighted RMSE (log)", xticks=[0, Lmax], yticks=[round(lo, 1), round(hi, 1)],
                 yfmt=lambda u: f"10^{{{u:.1f}}}", font_size=14).to_corner(UR, buff=0.4).shift(DOWN * 0.3)
        faint = VGroup(*[curve(g.ax, np.arange(len(x["loss"])), np.clip(np.log10(x["loss"]), lo, hi), GREY_C, stroke_width=1.5)
                         for x in runs])
        bright = [curve(g.ax, np.arange(fi[a], fi[b] + 1), np.clip(np.log10(np.asarray(run["loss"])[fi[a]:fi[b] + 1]), lo, hi),
                        QC.Q, stroke_width=3) for a, b in zip(pick, pick[1:])]
        cnt = label(r"one SSVI fit, replayed: the surface after each step of the search", font_size=20,
                    color=GREY_A).to_edge(UP, buff=0.25).shift(LEFT * 2)
        src = real_data(r"the Surface's 254 quotes (white); five random starts")
        fixed(self, g, faint, *bright, cnt, src)
        finals = r["finals"]
        start = run["loss"][0]
        nr = len(runs)
        with self.voiceover(
            f"Now watch it fit, in three dimensions. White dots are the quotes. This start is the worst of {nr}, about "
            f"{start:.0f} volatility points off. On the right, the error after every evaluation, the replayed start "
            "in violet, the others in grey. <bookmark mark='a'/> The surface lifts, tilts and folds onto the dots, "
            "the camera circling as it goes. <bookmark mark='b'/> Every start ends within "
            f"{max(finals) - min(finals):.4f} of the same error, {min(finals):.2f} points. A twelve-parameter fit of "
            "two hundred and fifty quotes, with no arbitrage allowed at any step."
        ) as vo:
            self.play(Create(ax), FadeIn(dots), FadeIn(cur), FadeIn(g), FadeIn(faint), FadeIn(cnt), FadeIn(src))
            vo.wait_until("a")
            for a, (i, seg) in enumerate(zip(pick[1:], bright)):
                self.play(Transform(cur, surf(i)), Create(seg), run_time=1.3)
                if a == 2:
                    self.move_camera(theta=-35 * DEGREES, run_time=1.2)
            vo.wait_until("b")
            self.move_camera(theta=-60 * DEGREES, run_time=max(vo.remaining(0.5) - 0.5, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, dots, cur))], run_time=1)
        self.clear_scene()

    def theorems(self, r):
        f = r["fit"]
        rows = [cmath(r"w(k, \theta_T)", r"=", r"\frac{\theta_T}{2}\Big(1 + \rho\varphi k + \sqrt{(\varphi k + \rho)^2 + 1 - "
                      r"\rho^2}\Big),\quad \varphi = \frac{\eta}{\theta^\gamma(1 + \theta)^{1 - \gamma}}", font_size=32,
                      colors={r"w(k, \theta_T)": IV}),
                cmath(r"\text{no calendar arbitrage}", r"\iff", r"\partial_T\theta_T \ge 0,\ \ 0 \le \partial_\theta(\theta\varphi)"
                      r" \le \frac{1 + \sqrt{1 - \rho^2}}{\rho^2}\,\varphi", font_size=32),
                cmath(r"\text{no butterfly arbitrage}", r"\Leftarrow", r"\theta\varphi(1 + |\rho|) < 4,\ \ "
                      r"\theta\varphi^2(1 + |\rho|) \le 4", font_size=32),
                cmath(r"\theta\varphi^2(1 + |\rho|)", r"=", r"\eta^2(1 + |\rho|)\,\theta^{1 - 2\gamma}(1 + \theta)^{2\gamma - 2}",
                      font_size=34, colors={r"\theta\varphi^2(1 + |\rho|)": BAD})]
        whys = [why(r"Gatheral and Jacquier (2014): SVI's shape, written in $\theta$"),
                why(r"Theorem 4.1; for the power law, $\theta\varphi$ rises and the bound holds for every $|\rho| < 1$ "
                    r"(Problem 3)"),
                why(r"Theorem 4.2: sufficient, not necessary"),
                why(rf"bounded as $\theta \to 0$ only if $\gamma \le \tfrac12$; the Surface's fit has $\gamma = "
                    rf"{f['gamma']:.3f}$")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.8, buff=0.65, edge=6.9)
        bound = r["bound"]
        tmin = r["theta_min"]
        ok_all = f["gamma"] <= 0.5
        verdict = (r"the sufficient condition holds for every $\theta$: provably free of butterflies" if ok_all else
                   rf"so it holds for $\theta > {bound:.1e}$, at every quoted expiry (smallest $\theta = {tmin:.4f}$), "
                   r"but not for all $\theta$; the measured $g_{\min}$ is " + f"{r['g_min']:.2f}")
        foot = wrapped_label(verdict, 12.0, 21, QC.HOUSE).to_edge(DOWN, buff=0.35)
        gm = f["gamma"]
        branch = ("So the fit is provably free of butterflies at every maturity. " if ok_all else
                  "And here an honest caveat. The fitted gamma is above one half, so the sufficient condition fails for "
                  "tiny theta: it holds only above about one ten-millionth, which covers every expiry actually quoted, "
                  "but not every theta in principle. Checked directly, the smallest g on the fitted slices is still "
                  "comfortably positive. ")
        with self.voiceover(
            "The theorems. Here is SSVI, with the power-law phi. <bookmark mark='a'/> Gatheral and Jacquier proved that "
            "it is free of calendar arbitrage exactly when theta rises and theta times phi stays in a band; for the "
            "power law the band always holds. <bookmark mark='b'/> For butterflies they gave a sufficient condition: "
            "two inequalities in theta and phi. <bookmark mark='c'/> Plug in the power law. The second inequality "
            "stays bounded as theta goes to zero only if gamma is at most one half. On the Surface, gamma is "
            f"{gm:.3f}. {branch}"
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def price(self, r):
        pr = r["per_rmse"]
        n = len(pr)
        hi = float(min(max(max(x["ssvi"], x["svi"]) for x in pr) * 1.1, 9))
        g = axes([0, n], [0, hi], x_length=8.0, y_length=3.8, ylabel=r"RMSE against the quotes (vol points)",
                 yticks=[0, round(hi / 2), round(hi)], font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        ax = g.ax
        bars = VGroup()
        for i, x in enumerate(pr):
            for j, (key, col) in enumerate((("svi", LV), ("ssvi", IV))):
                h = min(x[key], hi)
                bars.add(Rectangle(width=0.28, height=max(ax.c2p(0, h)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                   fill_color=col, fill_opacity=0.85).move_to(ax.c2p(i + 0.35 + 0.3 * j, h / 2)))
        ticks = VGroup(*[label(f"{x['days']:.0f}", font_size=15, color=GREY_B).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.1)
                         for i, x in enumerate(pr)])
        xl = label(r"days to expiry", font_size=17, color=GREY_A).next_to(ticks, DOWN, buff=0.15)
        leg = legend([(LV, rf"SVI per expiry: {r['n_par_svi']} parameters"), (IV, rf"SSVI: {r['n_par_ssvi']} parameters")],
                     font_size=17).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = VGroup(
            wrapped_label(r"the price of global consistency is paid at the short end, where one smile shape cannot "
                          r"match the first few days", 3.8, 19, GREY_A),
            wrapped_label(r"eSSVI (Hendriks and Martini 2019; Martini and Mingone 2022) lets $\rho$ vary with maturity and keeps the "
                          r"surface arbitrage-free", 3.8, 19, GREY_B),
            wrapped_label(r"pause and predict: which fits better in sample, and which would you quote from?", 3.8, 19,
                          QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = real_data(r"the Surface: unweighted RMSE per expiry, quotes within $|k| < 0.6$")
        a0, b0 = pr[0]["svi"], pr[0]["ssvi"]
        a1, b1 = pr[-1]["svi"], pr[-1]["ssvi"]
        nsvi = r["n_par_svi"]
        with self.voiceover(
            "What does consistency cost? Expiry by expiry, the error of SVI fitted to that expiry alone, in gold, "
            f"against one SSVI for all, in orange. <bookmark mark='a'/> At the first expiry SVI misses by {a0:.1f} "
            f"points and SSVI by {b0:.1f}; at the last, {a1:.1f} against {b1:.1f}. The {nsvi} free parameters "
            "always fit better in sample. But they cross each other, as Chapter three showed, and they cannot be "
            "trusted between expiries. A desk quotes from the surface that cannot be arbitraged, and pays for it in "
            "the first few days, where one smile shape cannot follow the quotes; beyond a month the gap is a fraction "
            "of a point. Extensions such as eSSVI let the tilt vary with maturity and close part of the gap."
            " A fitted surface is a price list. Next: the model hiding inside it, Dupire's local volatility."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg), FadeIn(ticks), FadeIn(xl))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.05, run_time=3))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in side], lag_ratio=0.5, run_time=3))
        self.wait(0.4)
        self.clear_scene()
