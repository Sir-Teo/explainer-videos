from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import deep as D
from videos.quant.quant17.common import (BAD, GOOD, IV, NET, OPT, PART, REF, ask, grid_fn, house_lab, illustration,
                                         load, surf3d_axes)


class Calibrate(VoiceoverScene, ThreeDScene):
    def construct(self):
        c = load("calib")
        t = load("calib_trace")
        self.card()
        self.derive(c, t)
        self.morph(t)
        self.starts(t)
        self.lab(t)
        self.surface(c)
        self.wall()

    def card(self):
        c = chapter_card(4, r"Calibrating through the network", r"Why is it fast, and where is it blind?", part=PART)
        with self.voiceover("Chapter four. The neural calibrator, part two: calibrating through the network."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self, c, t):
        n_it = len(t["traces"]) * (200 + 100)
        rows = [cmath(r"\vartheta(u)", r"=", r"\ell + (h - \ell)\,\tfrac{1 + \tanh u}{2}", font_size=40,
                      colors={r"\vartheta(u)": GOOD}),
                cmath(r"\nabla_u L", r"=", r"\nabla_\vartheta L \odot (h - \ell)\,\tfrac{1 - \tanh^2 u}{2}", font_size=40,
                      colors={r"\nabla_u L": BAD}),
                cmath(r"\nabla_\vartheta L", r"=", r"2\textstyle\sum_i w_i\,(\hat F_i - \sigma_i)\,\nabla_\vartheta \hat F_i",
                      font_size=40, colors={r"\nabla_\vartheta L": NET}),
                cmath(r"\text{cost}", r"\approx", rf"{n_it:,}".replace(",", "{,}") + rf"\times {1e3 * c['t_net_surface']:.1f}"
                      r"\,\text{ms}\ \ \text{vs}\ \ " + rf"{n_it:,}".replace(",", "{,}")
                      + rf"\times {c['t_mc_surface']:.1f}\,\text{{s}}", font_size=36, colors={r"\text{cost}": OPT})]
        whys = [why(r"optimize an unconstrained $u$ and map it into the training box $[\ell, h]$: every iterate is a "
                    r"parameter set the network has seen around"),
                why(r"the chain rule through the map: its slope $(1 - \tanh^2 u)/2$ goes to zero at the walls. A parameter "
                    r"pushed against a wall stops moving and stays there"),
                why(r"the gradient of the fit through the network is exact, by automatic differentiation. Through Monte "
                    r"Carlo, each gradient would need extra simulations for five parameters, all of them noisy"),
                why(rf"{len(t['traces'])} starts of 200 Adam steps and up to 100 L-BFGS steps each: through the network, "
                    r"seconds; by simulation, at this cost per surface, hours, before the extra simulations each gradient "
                    r"would need")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.62, edge=6.9)
        with self.voiceover(
            "Calibration is now an optimization over five numbers. First, keep the parameters where the network was "
            "trained: squash a free variable into the training box with a hyperbolic tangent. <bookmark mark='a'/> By "
            "the chain rule the gradient picks up the tangent's slope, which vanishes at the walls: a parameter pushed "
            "against a wall stops there, without complaint. <bookmark mark='b'/> Second, the gradient is exact, by "
            "automatic differentiation; by Monte Carlo it would cost more simulations, and be noisy. "
            "<bookmark mark='c'/> Third, the cost. Twelve starts, a few hundred steps each: through "
            f"the network a pass costs {1e3 * c['t_net_surface']:.1f} milliseconds, by simulation "
            f"{c['t_mc_surface']:.1f} seconds. Seconds against hours, before counting the extra simulations every "
            "Monte Carlo gradient would need."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def morph(self, t):
        kk, TT = np.asarray(t["kk"]), np.asarray(t["TT"])
        Q = t["quotes"]
        k, T, iv = (np.asarray(Q[x]) for x in ("k", "T", "iv"))
        m = (k >= kk[0]) & (k <= kk[-1]) & (T <= TT[-1]) & (T >= TT[0])
        ax = surf3d_axes([kk[0], kk[-1], 0.2], [0, TT[-1], 0.1], [0.3, 1.1, 0.2]).shift(DOWN * 0.3)
        dots = smile_points3d(ax, k[m], T[m], np.clip(iv[m], 0.3, 1.1), radius=0.04)
        tr = t["traces"][t["best"]]
        picks = list(t["picks"])

        def surf(i):
            f = grid_fn(kk, TT, np.clip(np.asarray(t["surfs"][i]), 0.3, 1.1))
            return Surface(lambda u, v: ax.c2p(u, v, f(u, v)), u_range=(kk[0], kk[-1]), v_range=(TT[0], TT[-1]),
                           resolution=(20, 12), fill_color=NET, fill_opacity=0.55, stroke_width=0.4,
                           stroke_color=WHITE, checkerboard_colors=False)
        s = surf(0)
        names = ["H", "eta", "rho", "vol0", "vol1"]
        tex = [r"H", r"\eta", r"\rho", r"\xi_0^{1/2}", r"\xi_1^{1/2}"]

        def panel(i):
            p = tr["params"][picks[i]]
            rows = VGroup(*[MathTex(rf"{tx} = {v:.3f}", font_size=26, color=GOOD) for tx, v in zip(tex, p)],
                          MathTex(rf"\text{{fit}} = {tr['rmse'][picks[i]]:.2f}\ \text{{vol pts}}", font_size=26, color=NET),
                          label(rf"step {tr['step'][picks[i]] if picks[i] < len(tr['step']) - 1 else 'final'}",
                                font_size=20, color=GREY_B))
            return rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.4)
        pan = panel(0)
        hint = label(r"log-moneyness (across), expiry (back), implied vol (up); dots: the Surface's quotes", font_size=19,
                     color=GREY_A).to_corner(UL, buff=0.35)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-62 * DEGREES, zoom=0.92)
        self.add_fixed_in_frame_mobjects(hint, pan)
        self.remove(hint, pan)
        fin = tr["params"][-1]
        with self.voiceover(
            "Here it is happening. The dots are the Surface's quotes, over log-moneyness and expiry, with implied "
            "volatility as height. The sheet is the network's implied-volatility surface at the first iterate of the "
            "best start: wrong, nearly flat. <bookmark mark='a'/> Now let the optimizer run. With every step the five "
            "parameters move, the network redraws the whole surface, and the sheet settles onto the dots: the skew "
            f"steepens, the short end rises. It finishes at a Hurst exponent of {fin[0]:.3f}, a volatility of volatility "
            f"of {fin[1]:.2f} and a correlation of {fin[2]:.2f}, {t['rmse']:.2f} vol points from the quotes."
        ) as vo:
            self.play(Create(ax), FadeIn(hint), FadeIn(dots), run_time=2)
            self.play(Create(s), FadeIn(pan))
            vo.wait_until("a")
            per = max(vo.remaining(1.5), 6) / (len(picks) - 1)
            for i in range(1, len(picks)):
                new = panel(i)
                self.add_fixed_in_frame_mobjects(new)
                self.remove(new)
                self.play(Transform(s, surf(i)), FadeOut(pan), FadeIn(new), run_time=per * 0.75)
                pan = new
                self.move_camera(theta=(-62 + 4 * i) * DEGREES, run_time=per * 0.25)
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, s, dots)), FadeOut(hint),
                                                                  FadeOut(pan)], run_time=1.2)
        self.clear_scene()

    def starts(self, t):
        trs = t["traces"]
        g = axes([0, 200], [-0.5, 1.5], x_length=7.0, y_length=4.2, xlabel=r"Adam step", ylabel=r"fit (vol points)",
                 xticks=[0, 100, 200], yticks=[0, 1], yfmt=lambda v: f"10^{{{v:.0f}}}", font_size=14,
                 ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        lines = VGroup()
        for i, tr in enumerate(trs):
            st = np.asarray(tr["step"][:-1], float)
            y = np.log10(np.clip(np.asarray(tr["rmse"][:-1]), 10 ** -0.5, 10 ** 1.5))
            lines.add(curve(g.ax, st, y, NET if i == t["best"] else GREY_B, stroke_width=4 if i == t["best"] else 1.5))
        finals = sorted(tr["rmse"][-1] for tr in trs)
        Hs = [tr["params"][-1][0] for tr in trs]
        near = sum(f < finals[0] + 0.1 for f in finals)
        side = wrapped_label(rf"{len(trs)} random starts. After L-BFGS, fits from {finals[0]:.2f} to {finals[-1]:.2f} vol "
                             rf"points; {near} of them within 0.1 of the best, with $H$ from {min(Hs):.3f} to "
                             rf"{max(Hs):.3f}: the fit is not unique, which is why a desk starts from many points",
                             4.4, 19, GREY_A).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            f"That was one start. Here are all {len(trs)}, from random points in the box: the fit, step by step. "
            f"<bookmark mark='a'/> After the final polish they end between {finals[0]:.2f} and {finals[-1]:.2f} vol "
            f"points, {near} of them within a tenth of the best. Several different parameter sets fit almost equally "
            "well. The surface pins down some combinations of the parameters better than others, and a calibrator "
            "that starts from one point would never know."
        ) as vo:
            self.play(FadeIn(g))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.15, run_time=4))
            vo.wait_until("a")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def lab(self, t):
        card = house_lab(r"calibrate through the network", D.calibrate_neural, "def model(u):", 5,
                         extra=[(D.calibrate_neural, "opt = torch.optim.Adam([u], lr=0.05)", 7)])
        card.to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.6)
        p = t["params"]
        outs = [f"H = {p['H']:.3f}   eta = {p['eta']:.2f}   rho = {p['rho']:.2f}",
                f"fit {t['rmse']:.2f} vol points, {len(t['traces'])} starts, {t['seconds']:.1f} s"]
        with self.voiceover(
            "The House's code. The model: the tanh map into the box, the features, one pass of the network. The loop: "
            "the vega-weighted squared error, a gradient step on the free variable, two hundred times, then L-BFGS to "
            "polish. <bookmark mark='a'/> Run on the Surface, it returns the parameters, the fit, and the time it took."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs)
        self.wait(0.5)
        self.clear_scene()

    def surface(self, c):
        s = c["surface"]
        p = s["params"]
        p14 = c["part14"]
        sl = c["slices"]
        groups = VGroup()
        for d in sl:
            k, iv, mc = np.asarray(d["k"]), np.asarray(d["iv"]), np.asarray(d["mc"])
            kk, net = np.asarray(d["kk"]), np.asarray(d["net"])
            ylo, yhi = float(np.nanmin(np.r_[iv, net])) - 0.03, float(np.nanmax(np.r_[iv, net])) + 0.03
            yt = [v / 100 for v in range(int(np.ceil(ylo * 10)) * 10, int(yhi * 100) + 1, 10)]
            g = axes([kk[0], kk[-1]], [ylo, yhi], x_length=3.7, y_length=2.8, xlabel=r"log-moneyness $k$",
                     ylabel=r"implied volatility" if not groups else "",
                     xticks=[round(kk[0] / 2, 1), 0, round(kk[-1] / 2, 1)], yticks=yt,
                     yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=13)
            ax = g.ax
            dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=IV) for a, b in zip(k, iv)])
            chk = VGroup(*[Cross(scale_factor=0.06, stroke_color=REF, stroke_width=2).move_to(ax.c2p(a, b))
                           for a, b in zip(k, mc) if np.isfinite(b) and ylo < b < yhi])
            ln = curve(ax, kk, np.clip(net, ylo, yhi), NET, stroke_width=3)
            ttl = label(rf"{d['T'] * 365:.0f} days", font_size=20).next_to(g, UP, buff=0.1)
            groups.add(VGroup(g, dots, ln, chk, ttl))
        groups.arrange(RIGHT, buff=0.45).to_edge(UP, buff=0.9)
        leg = legend([(IV, r"the Surface (Part 13)"), (NET, r"rough Bergomi through the network"),
                      (REF, r"$\times$ fresh Monte Carlo at the same parameters")], font_size=16)
        leg.next_to(groups, DOWN, buff=0.3).to_edge(LEFT, buff=0.8)
        res = VGroup(
            MathTex(rf"H = {p['H']:.2f},\ \eta = {p['eta']:.1f},\ \rho = {p['rho']:.2f}", font_size=30, color=NET),
            label(rf"error {s['net_rmse']:.2f} vol points through the network, {s['mc_rmse']:.2f} by fresh Monte Carlo; "
                  rf"{s['n']} quotes", font_size=19, color=GREY_A),
            label(rf"calibrated in {s['seconds']:.1f} s; one network pass over the surface: "
                  rf"{1e3 * c['t_net_surface']:.1f} ms, against {c['t_mc_surface']:.0f} s of Monte Carlo", font_size=19,
                  color=GREY_A),
            label(rf"Part 14's direct Monte Carlo fit: $H = {p14['params']['H']:.2f}$, error {p14['rmse']:.2f}",
                  font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(leg, DOWN, buff=0.3).to_edge(LEFT, buff=0.8)
        with self.voiceover(
            "Now the check that matters. Three expiries of the Surface: the market in orange, the network's smile in "
            "purple. <bookmark mark='a'/> The crosses are fresh Monte Carlo at the same parameters. "
            f"The fit is {s['net_rmse']:.2f} vol points through the network and {s['mc_rmse']:.2f} "
            f"by simulation, with Hurst exponent {p['H']:.2f}. <bookmark mark='b'/> A pass of the network over the whole "
            f"surface takes {1e3 * c['t_net_surface']:.1f} milliseconds, against {c['t_mc_surface']:.0f} seconds of Monte "
            f"Carlo. Part fourteen's direct fit found H of {p14['params']['H']:.2f}. Calibration that took minutes now "
            "takes seconds, so it can be done every week for two years, which is the next chapter."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(VGroup(gg[0], gg[1], gg[4])) for gg in groups], lag_ratio=0.3),
                      FadeIn(leg[0]))
            self.play(*[Create(gg[2]) for gg in groups], FadeIn(leg[1]))
            vo.wait_until("a")
            self.play(*[FadeIn(gg[3]) for gg in groups], FadeIn(leg[2]), FadeIn(res[0]), FadeIn(res[1]))
            vo.wait_until("b")
            self.play(FadeIn(res[2]), FadeIn(res[3]))
        self.wait(0.5)
        self.clear_scene()

    def wall(self):
        q = ask(r"today's market wants $H = 0.01$, below the box's floor of 0.02. What does the calibrator report?")
        with self.voiceover(
            "A question for the next chapter. Suppose the market wants a Hurst exponent of 0.01, below the floor of "
            "the training box. What does the calibrator report, and does it warn you?"
        ):
            self.play(FadeIn(q))
        self.wait(0.6)
        self.clear_scene()
