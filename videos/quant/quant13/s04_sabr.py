from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import stochvol as sv
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, illustration, load, pause, real_data


class SABR(VoiceoverScene, ThreeDScene):
    def construct(self):
        c = load("calibrate")
        s = load("sabr")
        r = load("sabr_replay")
        self.card()
        self.model(c)
        self.derive(r)
        self.replay(r, c)
        self.ribbon(c)
        self.backbone(s)

    def card(self):
        c = chapter_card(6, r"SABR I: Hagan's formula and the backbone", r"What do traders write on the smile, expiry by expiry?",
                         lit=(2002,), part=PART)
        with self.voiceover("Chapter six. SABR: Hagan's formula, and the backbone."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self, c):
        rows = [cmath(r"dF_t", r"=", r"\alpha_t F_t^{\beta}\,dW^1_t,\qquad d\alpha_t = \nu\,\alpha_t\,dW^2_t,\quad "
                      r"dW^1 dW^2 = \rho\,dt", font_size=34, colors={r"dF_t": SPOT}),
                cmath(r"\sigma_B(K)", r"\approx", r"\alpha\,\frac{z}{x(z)}\Big[1 + \big(\tfrac14\rho\nu\alpha + "
                      r"\tfrac{2 - 3\rho^2}{24}\nu^2\big)T\Big],\quad z = \frac{\nu}{\alpha}\ln\frac{F}{K}", font_size=32,
                      colors={r"\sigma_B(K)": IV}),
                cmath(r"x(z)", r"=", r"\ln\frac{\sqrt{1 - 2\rho z + z^2} + z - \rho}{1 - \rho}", font_size=34,
                      colors={r"x(z)": IV})]
        whys = [why(r"Hagan, Kumar, Lesniewski and Woodward (2002): a lognormal volatility $\alpha$ for the forward, a "
                    r"backbone exponent $\beta$, a vol of vol $\nu$ and a correlation $\rho$, for one expiry at a time; "
                    r"$\beta = 0$ and $\nu = 0$ is Bachelier, $\nu = 0$ alone is CEV"),
                why(r"singular perturbation theory, shown here for $\beta = 1$: the implied vol is the volatility along the "
                    r"most likely path from $F$ to $K$, corrected to first order in $T$"),
                why(r"the function that bends the smile: $z/x(z)$ equals 1 at the money")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.4, buff=0.85, edge=6.9)
        with self.voiceover(
            (
            (
            "Rates and FX desks wanted a smile they could fit one expiry at a time, in a few numbers. In 2002 Hagan, "
            "Kumar, Lesniewski and Woodward gave them SABR: the forward moves with volatility alpha raised to a "
            "backbone power beta, and alpha is itself lognormal, with vol of vol nu and correlation rho. With nu zero "
            "it is the constant-elasticity model; with beta zero as well, Bachelier. In practice beta is fixed by "
            "convention, often one half for rates and one for FX and crypto, and the other three are fitted. "
            "<bookmark mark='a'/> Singular perturbation theory gives the implied volatility directly: roughly the "
            "volatility along the most likely path to the strike, corrected in time. <bookmark mark='b'/> All the "
            "bending lives in z over x of z."
        )
        )
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def derive(self, r):
        sl = next(z for z in r["slices"] if z["days"] == 51)
        a, rho, nu = sl["x"]
        rows = [cmath(r"\frac{z}{x(z)}", r"=", r"1 - \frac{\rho}{2}\,z + \frac{2 - 3\rho^2}{12}\,z^2 + O(z^3)", font_size=36,
                      colors={r"\frac{z}{x(z)}": IV}),
                cmath(r"\partial_k\sigma_B\big|_0", r"\approx", r"\frac{\rho\,\nu}{2}", font_size=38,
                      colors={r"\partial_k\sigma_B\big|_0": IV}),
                cmath(r"\partial^2_k\sigma_B\big|_0", r"\approx", r"\frac{(2 - 3\rho^2)\,\nu^2}{6\,\alpha}", font_size=38,
                      colors={r"\partial^2_k\sigma_B\big|_0": IV}),
                cmath(r"\sigma_{\text{ATM}}(F)", r"\approx", r"\alpha\,F^{\beta - 1}", font_size=38,
                      colors={r"\sigma_{\text{ATM}}(F)": SPOT})]
        whys = [why(r"expand $x(z)$ around $z = 0$ and divide", 20),
                why(r"with $k = \ln(K/F)$, $z = -\nu k/\alpha$: the skew is the correlation times the vol of vol", 20),
                why(r"the curvature comes from $\nu^2$; even with $\rho = 0$ the smile curves", 20),
                why(r"at the money ($K = F$) the leading term for general $\beta$: the backbone", 20)]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.2, buff=0.55, edge=6.9)
        res = VGroup(
            MathTex(rf"51\ \text{{days:}}\ \alpha = {a:.3f},\ \rho = {rho:.2f},\ \nu = {nu:.2f}", font_size=28, color=GREY_A),
            MathTex(rf"\tfrac12\rho\nu \times (1 + O(T)) = {sl['skew_formula']:.3f}\ \ \text{{vs the formula's slope}}\ "
                    rf"{sl['skew_num']:.3f}", font_size=28, color=IV)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            (
            "Term by term: expand x of z at zero, and z over x of z is one, minus rho z over two, plus a quadratic. "
            "<bookmark mark='a'/> Since z is minus nu k over alpha, the at-the-money slope is rho nu over two: skew is "
            "correlation times vol of vol. <bookmark mark='b'/> The curvature is proportional to nu squared over "
            "alpha. <bookmark mark='c'/> And at the money, alpha times F to the beta minus one: the backbone. "
            f"<bookmark mark='d'/> On the 51-day slice, the formula's slope is {sl['skew_formula']:.3f}. Four "
            "readable numbers: that is why traders speak SABR."
        )
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def replay(self, r, c):
        S = r["slices"]
        days = np.array([z["days"] for z in S])
        lx = np.log10(days)
        main = axes([-0.45, 0.45], [0.3, 1.1], x_length=5.6, y_length=4.2, xlabel=r"log-moneyness",
                    ylabel=r"implied volatility", xticks=[-0.4, -0.2, 0, 0.2, 0.4], yticks=[0.4, 0.6, 0.8, 1.0],
                    yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        mini = []
        for nm, lo, hi, tk in ((r"$\alpha$", 0.3, 0.6, [0.4, 0.5]), (r"$\rho$", -0.5, 0.0, [-0.4, -0.2, 0]),
                               (r"$\nu$ (log scale)", np.log10(0.5), np.log10(10), [0, 1])):
            g = axes([0.3, 2.6], [lo, hi], x_length=3.6, y_length=1.45, ylabel=nm, xticks=[np.log10(3), 1, 2],
                     xfmt=lambda u: f"{10 ** u:.0f}d", yticks=tk, yfmt=(lambda u: f"{10 ** u:g}") if "log" in nm else None,
                     font_size=12)
            mini.append(g)
        M = VGroup(*mini).arrange(DOWN, buff=0.38).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.2)
        src = real_data(r"the Surface: SABR ($\beta = 1$) by least squares, slice by slice, every evaluation recorded")

        def view(z, j):
            kk = np.asarray(z["kk"])
            c_ = curve(main.ax, kk, np.clip(np.asarray(z["curves"][j]), 0.3, 1.1), MODEL_COL["SABR"], stroke_width=3.5)
            return c_

        nu_dots = VGroup()
        with self.voiceover(
            (
            "Fit it slice by slice and watch: each expiry's smile moves from its starting guess onto the quotes, and "
            "its three numbers land on the right. <bookmark mark='a'/> Alpha barely moves; rho stays near minus a "
            f"third. <bookmark mark='b'/> But nu falls steadily, along a line on log scales: like T to the "
            f"{c['sabr_nu_power']:.2f}. Fitted per slice, SABR misses by only {c['sabr_rmse']:.2f} points, with "
            f"{3 * len(c['sabr'])} numbers. One global nu would underfit the short skew, the same diagnosis as "
            "Heston's; the square-root law is Part fourteen's clue."
        )
        ) as vo:
            self.play(FadeIn(main), FadeIn(M), FadeIn(src))
            per = max((vo.until("b") + 4.0) / len(S), 1.0)
            cur = None
            for i, z in enumerate(S):
                kq, iv = np.asarray(z["k"]), np.asarray(z["iv"])
                dts = VGroup(*[Dot(main.ax.c2p(a_, np.clip(b_, 0.3, 1.1)), radius=0.045, color=WHITE)
                               for a_, b_ in zip(kq, iv) if abs(a_) <= 0.45])
                tag = label(rf"{z['days']} days", font_size=22, color=GREY_A).next_to(main, UP, buff=0.05).align_to(main, RIGHT)
                first = view(z, 0)
                anims = [FadeIn(dts), FadeIn(tag)]
                if cur is None:
                    cur = first
                    anims.append(Create(cur))
                else:
                    anims.append(Transform(cur, first))
                self.play(*anims, run_time=per * 0.25)
                for j in range(1, len(z["curves"])):
                    self.play(Transform(cur, view(z, j)), run_time=per * 0.45 / (len(z["curves"]) - 1))
                a_, rh_, nu_ = z["x"]
                d3 = VGroup(Dot(mini[0].ax.c2p(lx[i], a_), radius=0.05, color=MODEL_COL["SABR"]),
                            Dot(mini[1].ax.c2p(lx[i], rh_), radius=0.05, color=MODEL_COL["SABR"]),
                            Dot(mini[2].ax.c2p(lx[i], np.log10(nu_)), radius=0.05, color=MODEL_COL["SABR"]))
                nu_dots.add(d3)
                self.play(FadeIn(d3, scale=1.5), FadeOut(dts), FadeOut(tag), run_time=per * 0.3)
        self.wait(0.3)
        self.clear_scene()

    def ribbon(self, c):
        sab = c["sabr"]
        days = np.array(sorted(int(d) for d in sab))
        kk = np.linspace(-0.35, 0.35, 29)
        lD = np.log10(days)
        G = np.array([sv.sabr_iv(1.0, np.exp(kk), d / 365, sab[str(d)]["alpha"], 1.0, sab[str(d)]["rho"], sab[str(d)]["nu"])
                      for d in days])
        G = np.clip(G, 0.3, 1.1)
        ax = ThreeDAxes(x_range=[-0.35, 0.35, 0.1], y_range=[lD[0], lD[-1], 0.5], z_range=[0.3, 1.1, 0.2], x_length=6.4,
                        y_length=5.4, z_length=3.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.3)

        def f(x, y):
            j = np.clip(np.searchsorted(lD, y) - 1, 0, len(lD) - 2)
            w = (y - lD[j]) / (lD[j + 1] - lD[j])
            return float(np.interp(x, kk, (1 - w) * G[j] + w * G[j + 1]))

        surf = price_surface(ax, f, [-0.35, 0.35], [lD[0], lD[-1]], resolution=(20, 16), z_lo=0.4, z_hi=1.0, opacity=0.55)
        lines = VGroup(*[VMobject(stroke_color=MODEL_COL["SABR"], stroke_width=4).set_points_as_corners(
            [ax.c2p(x, l_, z) for x, z in zip(kk, g_)]) for l_, g_ in zip(lD, G)])
        hint = label(r"nine SABR smiles, one per expiry (3 to 289 days, log), assembled into a surface", font_size=21,
                     color=GREY_A).to_corner(UL, buff=0.35)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-120 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint)
        self.remove(hint)
        with self.voiceover(
            (
            "Assemble the nine smiles into a surface. <bookmark mark='a'/> The short end is a deep narrow valley, the "
            "long end nearly flat. Nothing in SABR links one slice to the next: a model per expiry, not of time."
        )
        ) as vo:
            self.play(Create(ax), FadeIn(hint), run_time=1.2)
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(surf), run_time=1.5)
            self.move_camera(theta=-60 * DEGREES, phi=68 * DEGREES, run_time=max(vo.remaining(1.0) - 0.3, 1.5))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, surf, lines)), FadeOut(hint)],
                         run_time=1.5)
        self.clear_scene()

    def backbone(self, s):
        Fs = np.asarray(s["Fs"])
        g = axes([0.7, 1.3], [0.25, 0.7], x_length=6.2, y_length=4.0, xlabel=r"forward, relative to today",
                 ylabel=r"at-the-money implied vol", xticks=[0.8, 1.0, 1.2], yticks=[0.3, 0.4, 0.5, 0.6],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        cols = {"0.0": BAD, "0.5": IV, "1.0": RV}
        lines = VGroup(*[curve(ax, Fs, np.clip(np.asarray(s["backbone"][b]), 0.25, 0.7), cols[b], stroke_width=3)
                         for b in ("0.0", "0.5", "1.0")])
        leg = legend([(BAD, r"$\beta = 0$: normal, vol falls as the price rises"), (IV, r"$\beta = \tfrac12$"),
                      (RV, r"$\beta = 1$: lognormal, the smile moves with the price")], font_size=17).next_to(
            g, UP, buff=0.15).align_to(g, LEFT)
        side = wrapped_label(r"$\beta$ barely changes today's fit (vol of vol and $\rho$ can mimic it), but it decides how "
                             r"the smile moves when the price moves, and so the delta. Part 12's sticky test found that "
                             r"bitcoin's smile moved with the price: $\beta$ near 1", 4.6, 20, GREY_A).to_edge(RIGHT, buff=0.4)
        src = illustration(r"SABR with the 51-day slice's $\rho$ and $\nu$, $\alpha$ set to match today's at-the-money vol")
        with self.voiceover(
            (
            "Beta is the backbone: how at-the-money volatility moves with the forward. With beta one the smile slides "
            "with the price. <bookmark mark='a'/> With beta zero, volatility falls as the price rises, which suits "
            "rates. Today's fit barely sees beta; the hedge does. Bitcoin's smile moved with the price in Part "
            "twelve's test: beta near one. And it is why Hagan wrote the paper: local volatility predicts the smile "
            "moves the wrong way, and its deltas were worse than Black–Scholes's."
            " But Hagan's formula has a flaw. Next."
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(lines[2]), FadeIn(leg[2]))
            vo.wait_until("a")
            self.play(Create(lines[0]), Create(lines[1]), FadeIn(leg[0]), FadeIn(leg[1]), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.clear_scene()
