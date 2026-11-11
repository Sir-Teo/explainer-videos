from __future__ import annotations

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, GOOD, IV, OPT, PART, SPOT, VEGA, illustration, load, axes, data_range, pause_card


class Cliquet(VoiceoverScene, ThreeDScene):
    def construct(self):
        c = load("cliquet")
        self.card()
        self.resets()
        self.derive()
        self.ridge(c)
        self.variants(c)

    def card(self):
        c = chapter_card(12, r"Cliquets: the risk vega cannot see", r"Can a product have no vega and still be all about "
                         r"volatility?", part=PART)
        with self.voiceover("Chapter twelve. Cliquets, and the risk that vega cannot see."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def resets(self):
        g = np.random.default_rng(12)
        n_m, d = 12, 21
        z = g.standard_normal(n_m * d) * 0.22 * np.sqrt(1 / 252)
        x = np.concatenate([[0], np.cumsum(z - 0.5 * 0.22 ** 2 / 252)])
        S = 100 * np.exp(x)
        t = np.arange(len(S)) / d
        ax_ = axes([0, 12], [float(S.min()) - 4, float(S.max()) + 4], x_length=6.4, y_length=2.8, xlabel=r"months",
                   ylabel=r"index", xticks=[0, 3, 6, 9, 12], yticks=[], font_size=15).to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.5)
        ax = ax_.ax
        tr = ValueTracker(0)
        path = tracing(ax, t, S, tr, SPOT, stroke_width=2.5)
        cap, flo = 0.03, -0.03
        r = S[d::d] / S[:-1:d] - 1
        clip = np.clip(r, flo, cap)
        bands = VGroup()
        for m in range(n_m):
            s0 = S[m * d]
            bands.add(Rectangle(width=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, s0 * (1 + cap))[1] -
                                ax.c2p(0, s0 * (1 + flo))[1], stroke_width=0, fill_color=GOOD, fill_opacity=0.15)
                      .move_to([ax.c2p(m + 0.5, 0)[0], ax.c2p(0, s0)[1], 0]))
        bars = VGroup()
        run = np.cumsum(clip)
        # the axis covers the running sum, which can fall well below one month's floor
        ylo = min(-0.04, float(np.floor((min(run.min(), clip.min()) - 0.01) / 0.03) * 0.03))
        yhi = max(0.06, float(np.ceil((max(run.max(), clip.max()) + 0.01) / 0.03) * 0.03))
        bx = axes([0, 12], [ylo, yhi], x_length=6.4, y_length=2.1, xlabel=r"month", ylabel=r"clipped return, summed",
                  xticks=[0, 6, 12], yticks=[v for v in np.arange(-0.3, 0.31, 0.03 if yhi - ylo < 0.16 else 0.06)
                                             if ylo <= v <= yhi + 1e-9],
                  yfmt=lambda u: f"{int(round(100 * u))}\\%", font_size=14).next_to(ax_, DOWN, buff=0.25).align_to(ax_, LEFT)
        for m in range(n_m):
            y0, y1 = bx.ax.c2p(m + 0.5, 0)[1], bx.ax.c2p(m + 0.5, clip[m])[1]
            bars.add(Rectangle(width=0.4, height=max(abs(y1 - y0), 0.01), stroke_width=0,
                               fill_color=GOOD if clip[m] >= 0 else BAD, fill_opacity=0.85)
                     .move_to([bx.ax.c2p(m + 0.5, 0)[0], (y0 + y1) / 2, 0]))
        runl = curve(bx.ax, np.arange(n_m) + 1, run, OPT, stroke_width=3)
        pay = max(run[-1], 0.0)
        side = VGroup(
            wrapped_label(r"a cliquet: each month the strike resets to the current level; that month's return counts, "
                          r"clipped to a local floor and cap ($-3\%$, $+3\%$ here); the clipped returns are summed, and "
                          r"the sum has a global floor of zero", 4.0, 18, GREY_A),
            MathTex(r"\text{payoff} = \max\Big(\textstyle\sum_i \min(\max(r_i, -3\%), 3\%),\ 0\Big)",
                    font_size=26, color=OPT),
            MathTex(rf"= {100 * pay:.1f}\%\ \ \text{{on this path}}", font_size=26, color=OPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        src = illustration(r"one simulated year at 22\% volatility")
        with self.voiceover(
            "A cliquet is a ratchet. Every month the strike resets to wherever the index is, and only that month's "
            "return counts, clipped between a local floor and cap. <bookmark mark='a'/> Watch a year: each month a "
            "new band, and the clipped return drops into the running sum below. "
            "<bookmark mark='b'/> At the end, the sum is paid, with a global floor of zero, so the buyer gets the "
            f"sum of clipped monthly returns, or nothing: here, {100 * pay:.1f} percent. Cliquets were sold as "
            "capital-protected equity exposure, and they are where model risk hides best."
        ) as vo:
            self.play(FadeIn(ax_), FadeIn(bx), FadeIn(side[0]), FadeIn(src))
            self.add(path)
            vo.wait_until("a")
            for m in range(n_m):
                self.play(FadeIn(bands[m]), tr.animate.set_value((m + 1) * d), GrowFromEdge(bars[m], DOWN),
                          run_time=0.5, rate_func=linear)
            self.play(Create(runl))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"FS_0", r"=", r"\mathbb E\big[e^{-rt_2}(S_{t_2} - \alpha S_{t_1})^+\big] = S_0 e^{-qt_1}\,"
                  r"C^{BS}\big(1, \alpha, t_2 - t_1\big)", font_size=32, colors={r"FS_0": OPT}),
            cmath(r"V_{\text{cliquet}}", r"=", r"\mathbb E\Big[\max\Big(\textstyle\sum_i \min\big(\max(r_i, f), c\big),\ "
                  r"F\Big)\Big]", font_size=32, colors={r"V_{\text{cliquet}}": OPT}),
            cmath(r"\frac{\partial V}{\partial\sigma}", r"=", r"0\ \ \text{on the ridge, yet}\ \ "
                  r"\frac{\partial^2 V}{\partial\sigma^2} \le 0", font_size=34,
                  colors={r"\frac{\partial V}{\partial\sigma}": VEGA}),
            cmath(r"\mathbb E\big[V(\bar\sigma+\varepsilon)\big]", r"\approx", r"V(\bar\sigma)+\tfrac12 V^{\prime\prime}(\bar\sigma)\operatorname{Var}(\varepsilon)", font_size=36,
                  colors={r"\mathbb E\big[V(\bar\sigma+\varepsilon)\big]": BAD}),
        ]
        whys = [why(r"a forward-start option: homogeneity of degree one and independent increments; it depends only on "
                    r"the forward volatility between $t_1$ and $t_2$"),
                why(r"a strip of capped and floored forward returns; the global floor $F$ makes it more than a sum of "
                    r"forward-starts"),
                why(r"at a smooth interior maximum vega is zero; strict concavity requires more than the maximum condition "
                    r"(negative volga)"),
                why(r"local Taylor illustration for a small mean-zero random constant volatility; Jensen needs concavity on the full support. This is not a general stochastic-volatility "
                    r"comparison")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.0, buff=0.8, edge=6.9)
        with self.voiceover(
            "Under constant-parameter Black-Scholes, homogeneity and independent increments price a forward-start option through a normalized call over the remaining interval. The displayed formula assumes the stated constant dividend yield. <bookmark mark='a'/> Our cliquet is a sum of capped and floored returns with a global floor. The numerical cliquet examples use zero rates and dividends; the displayed expectation then needs no discount factor. <bookmark mark='b'/> Near an interior smooth price maximum in constant volatility, aggregate vega is zero. That alone does not imply strictly negative volga or zero bucketed forward-volatility risk. <bookmark mark='c'/> For a small, mean-zero random constant-volatility perturbation, Taylor's expansion introduces the volga term shown. Jensen requires concavity over the entire perturbation support. A general stochastic-volatility process changes joint return laws and is not automatically this mixture. Zero first-order vega can still leave substantial higher-order and dynamic-model risk."
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

    def ridge(self, c):
        vols = np.asarray(c["vols"])
        caps = np.asarray(c["caps"])
        G = np.asarray(c["grid"])  # (caps, vols)
        f = RegularGridInterpolator((caps, vols), G, bounds_error=False, fill_value=None)
        zmax = float(G.max()) * 1.1
        ax = ThreeDAxes(x_range=[0.05, 0.5, 0.15], y_range=[0.01, 0.06, 0.01], z_range=[0, zmax, zmax / 3],
                        x_length=6.8, y_length=4.6, z_length=3.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2}).shift(DOWN * 0.6)
        surf = Surface(lambda u, w: ax.c2p(u, w, float(f((w, u)))), u_range=[0.05, 0.5], v_range=[0.01, 0.06],
                       resolution=(30, 20), fill_opacity=0.85, stroke_width=0.3, stroke_color=GREY_D)
        surf.set_fill_by_value(axes=ax, colorscale=[(SPOT, 0), (OPT, zmax * 0.5), ("#F7A8D8", zmax)], axis=2)
        # the ridge: the volatility that maximises the price at each cap (interior maxima only)
        cg = np.linspace(0.01, 0.06, 26)
        vg = np.linspace(0.05, 0.5, 91)
        rp = []
        for cc in cg:
            row = np.array([float(f((cc, v))) for v in vg])
            k = int(np.argmax(row))
            if 0 < k < len(vg) - 1:
                rp.append(ax.c2p(vg[k], cc, row[k] + zmax * 0.01))
        ridge = VMobject(stroke_color=WHITE, stroke_width=5).set_points_smoothly(rp) if len(rp) > 2 else VGroup()
        i3 = int(np.argmin(np.abs(caps - 0.03)))
        row3 = G[i3]
        hint = VGroup(label(r"volatility, 5\% to 50\%", font_size=21, color=IV),
                      label(r"local cap, 1\% to 6\% (local floor $-3\%$, global floor 0)", font_size=21, color=GREY_A),
                      label(r"price of the 12-month cliquet", font_size=21, color=OPT),
                      label(r"white: interpolated grid maxima; not exact vega roots", font_size=21, color=WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-125 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint)
        self.remove(hint)
        with self.voiceover(
            f"This is the zero-rate Black-Scholes cliquet value over volatility and local cap, estimated with two hundred thousand paths and common random numbers. <bookmark mark='a'/> The low-cap rows decline on the sampled grid; high-cap rows tend to rise. Intermediate rows have grid maxima tracing the white ridge. Linear interpolation and a finite volatility mesh do not certify an exact zero of vega. <bookmark mark='b'/> At a three-percent cap the largest sampled value occurs at {100 * c['peak_vol']:.0f} percent volatility, worth {100 * c['peak']:.2f} percent of notional. The twenty and thirty percent values are {100 * row3[3]:.2f} and {100 * row3[5]:.2f}. A small aggregate vega is not a reason to hold no options: separate forward-volatility buckets, volga and smile dynamics still matter. This coupon payoff alone does not provide principal protection."
        ) as vo:
            self.play(FadeIn(hint[:3]), Create(ax), Create(surf), run_time=3)
            vo.wait_until("a")
            self.move_camera(theta=-70 * DEGREES, phi=68 * DEGREES, run_time=3)
            self.play(Create(ridge), FadeIn(hint[3]))
            vo.wait_until("b")
            self.move_camera(theta=-170 * DEGREES, phi=55 * DEGREES, run_time=max(vo.remaining(1.0) - 1.0, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, surf, ridge)), FadeOut(hint)],
                         run_time=1.2)
        self.clear_scene(run_time=0.1)

    def variants(self, c):
        vols = np.asarray(c["vols"])
        nf = np.asarray(c["nofloor"])
        rv = np.asarray(c["reverse"])
        g1 = axes([0.05, 0.5], [0, 0.016], x_length=5.4, y_length=3.4, xlabel=r"volatility",
                  ylabel=r"capped at 2\%, no local floor", xticks=[0.1, 0.3, 0.5], yticks=[0, 0.008, 0.016],
                  font_size=14)
        g2 = axes([0.05, 0.5], [0, 0.25], x_length=5.4, y_length=3.4, xlabel=r"volatility",
                  ylabel=r"reverse cliquet, $C = 30\%$", xticks=[0.1, 0.3, 0.5], yticks=[0, 0.1, 0.2], font_size=14)
        VGroup(g1, g2).arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.9)
        l1 = curve(g1.ax, vols, nf, BAD, stroke_width=3)
        l2 = curve(g2.ax, vols, rv, BAD, stroke_width=3)
        q = c["q13_spread"]
        foot = VGroup(
            MathTex(r"\text{reverse cliquet} = \max\Big(C + \textstyle\sum_i \min(r_i, 0),\ 0\Big)", font_size=30,
                    color=OPT),
            wrapped_label((rf"Part 13 priced one cliquet under five models fitted to the same Surface: they disagreed by "
                           rf"{100 * q:.1f}\%. " if q is not None else "") +
                          r"A Napoleon pays a fixed coupon plus the worst monthly return of the year: short volatility "
                          r"too", 11.6, 20, GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Other members of the family lean one way. A cliquet capped at two percent with no local floor only "
            f"loses value as volatility rises, from {100 * nf[0]:.2f} percent of notional at five percent volatility "
            f"to {100 * nf[-1]:.2f} at fifty. <bookmark mark='a'/> The reverse cliquet starts with a coupon, thirty "
            "percent here, and subtracts every negative monthly return. It is steeply short volatility: worth "
            f"{100 * rv[0]:.1f} percent at five percent volatility and {100 * rv[-1]:.1f} at fifty. "
            "<bookmark mark='b'/> And the model risk: Part "
            "thirteen priced one cliquet under five models, all fitted to the same Surface, and found them "
            f"{100 * (q or 0):.1f} percent apart, on a product whose Black–Scholes vega can be zero."
            " If the models disagree, price the worst case. Next: uncertain volatility."
        ) as vo:
            self.play(FadeIn(g1), Create(l1))
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(l2), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
        self.wait(0.4)
        self.clear_scene()
