from __future__ import annotations

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, load, pause, real_data

PNAME = {"v0": r"v_0", "kappa": r"\kappa", "theta": r"\theta", "xi": r"\xi", "rho": r"\rho"}


class HestonFit(VoiceoverScene, ThreeDScene):
    def construct(self):
        c = load("calibrate")
        sl = load("heston_sliders")
        rp = load("heston_replay")
        self.card()
        self.sliders(sl, rp)
        self.replay(rp)
        self.fit(c)
        self.skew(sl)

    def card(self):
        c = chapter_card(4, r"Heston II: what each parameter does", r"How do five numbers bend a whole surface?",
                         lit=(1993,), part=PART)
        with self.voiceover("Chapter four. What each of Heston's parameters does, and the fit."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sliders(self, sl, rp):
        k = np.asarray(sl["k"])
        lT = np.log10(np.asarray(sl["T"]) * 365)
        ax = ThreeDAxes(x_range=[-0.4, 0.4, 0.2], y_range=[lT[0], lT[-1], 0.5], z_range=[0.2, 1.3, 0.2], x_length=6.4,
                        y_length=5.0, z_length=3.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.4)

        def surf(grid):
            G = np.clip(np.asarray(grid, float), 0.2, 1.3)
            f = RegularGridInterpolator((lT, k), G)
            return price_surface(ax, lambda x, y: float(f((y, x))), [-0.4, 0.4], [lT[0], lT[-1]], resolution=(18, 12),
                                 z_lo=0.3, z_hi=1.1, opacity=0.75)

        names = ("v0", "kappa", "theta", "xi", "rho")
        base = sl["grids"]["v0"][2]
        S0 = surf(base)
        Q = rp["quotes"]
        qk, qT, qv = np.asarray(Q["k"]), np.asarray(Q["T"]) * 365, np.asarray(Q["iv"])
        m = (np.abs(qk) <= 0.4) & (qT >= 3) & (qT <= 289)
        dots = smile_points3d(ax, qk[m], np.log10(qT[m]), np.clip(qv[m], 0.2, 1.3), color=WHITE, radius=0.03)
        hint = VGroup(label(r"the fitted Heston's implied vol over (log-moneyness, expiry 3 to 289 days, log)",
                            font_size=20, color=GREY_A),
                      label(r"white: the Surface's quotes", font_size=20, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        vals = sl["vals"]
        tags = {n: MathTex(PNAME[n] + r":\ " + r"\to ".join(f"{v:.2g}" for v in vals[n]), font_size=30, color=VAR)
                .to_corner(UR, buff=0.4) for n in names}
        self.set_camera_orientation(phi=64 * DEGREES, theta=-125 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint, *tags.values())
        self.remove(hint, *tags.values())
        cur = S0
        marks = {n: n for n in names}
        with self.voiceover(
            "Five numbers bend a whole surface. Here is the fitted Heston's implied volatility over strike and "
            "expiry, with the Surface's quotes as white dots. Move one parameter at a time, from low to high, and "
            "watch what it does. <bookmark mark='v0'/> Today's variance, v nought, lifts the short end: the near "
            "expiries feel today's level. <bookmark mark='theta'/> The long-run level, theta, lifts the long end. "
            "<bookmark mark='kappa'/> Mean reversion, kappa, decides how fast the one becomes the other: slow, and "
            "today's level lingers for months; fast, and the surface is flat in expiry after a few weeks. "
            "<bookmark mark='rho'/> The correlation, rho, rotates every smile: negative tilts it toward puts, "
            "positive toward calls. <bookmark mark='xi'/> And the vol of vol, xi, bends every smile, most of all at "
            "the short end, where it is the only thing that can produce curvature quickly. Five dials, each with one "
            "job. The calibrator's work is to set all five at once."
        ) as vo:
            self.play(Create(ax), FadeIn(hint), run_time=1.5)
            self.play(Create(cur), FadeIn(dots), run_time=2.5)
            for n in ("v0", "theta", "kappa", "rho", "xi"):
                vo.wait_until(marks[n])
                self.play(FadeIn(tags[n]), run_time=0.3)
                for g_ in (sl["grids"][n][0], sl["grids"][n][-1], base):
                    self.play(Transform(cur, surf(g_)), run_time=1.1)
                self.play(FadeOut(tags[n]), run_time=0.3)
            self.move_camera(theta=-70 * DEGREES, run_time=2)
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, cur, dots)), FadeOut(hint)],
                         run_time=1.5)
        self.clear_scene()

    def replay(self, rp):
        runs = rp["runs"]
        fr = rp["frames"]
        Ts = np.asarray(rp["T"])
        k = np.asarray(rp["k"])
        Q = rp["quotes"]
        qk, qT, qv = np.asarray(Q["k"]), np.asarray(Q["T"]), np.asarray(Q["iv"])
        n_max = max(int(r["trace"]["eval"][-1]) for r in runs)
        steps = np.arange(0, n_max + 1)
        L = np.array([np.interp(steps, r["trace"]["eval"], np.minimum(r["trace"]["best"], 8.0)) for r in runs])
        L = np.array([np.where(steps <= r["trace"]["eval"][-1], l_, l_[np.searchsorted(steps, r["trace"]["eval"][-1])])
                      for l_, r in zip(L, runs)])
        pick = [int(np.argmin(np.abs(Ts * 365 - d))) for d in (9, 51, 198)]
        cks = sorted({int(runs[0]["trace"]["eval"][f["i"]]) for f in fr})
        frames = [f for f in fr]
        frames = [next(f for f in frames if int(runs[0]["trace"]["eval"][f["i"]]) == c_) for c_ in cks]

        def frame(i):
            f = frames[i]
            G = np.asarray(f["grid"])
            panels = VGroup()
            for j in pick:
                a = axes([-0.4, 0.4], [0.3, 0.9], x_length=1.9, y_length=2.6, xticks=[-0.3, 0.3], yticks=[0.4, 0.6, 0.8],
                         yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=12)
                mq = (qT == Ts[j]) & (np.abs(qk) <= 0.4)
                d_ = VGroup(*[Dot(a.ax.c2p(x_, np.clip(y_, 0.3, 0.9)), radius=0.035, color=WHITE)
                              for x_, y_ in zip(qk[mq], qv[mq])])
                c_ = curve(a.ax, k, np.clip(G[j], 0.3, 0.9), MODEL_COL["Heston"], stroke_width=3)
                t_ = label(rf"{round(Ts[j] * 365)} days", font_size=16, color=GREY_A).next_to(a, UP, buff=0.05)
                panels.add(VGroup(a, d_, c_, t_))
            panels.arrange(RIGHT, buff=0.25)
            x = f["x"]
            par = MathTex(rf"\kappa = {x[1]:.1f},\ \xi = {x[3]:.2f},\ \rho = {x[4]:.2f}", font_size=24, color=GREY_A)
            err = MathTex(rf"\text{{implied-vol error}}\ {f['iv_rmse']:.2f}", font_size=24, color=MODEL_COL["Heston"])
            return VGroup(panels, par, err).arrange(DOWN, buff=0.2)

        rpl = TrainingReplay(steps, L, frame, checkpoints=cks, ylabel=r"calibrator loss, best so far",
                             xlabel=r"model evaluations", color=MODEL_COL["Heston"], left=LEFT * 3.2 + DOWN * 0.2,
                             right=RIGHT * 3.6 + DOWN * 0.2, x_length=4.8, y_length=3.4)
        r0, r1, r2 = runs
        cap = label(r"three starts: the default and two random; band = their spread", font_size=18, color=GREY_B)
        cap.to_edge(UP, buff=0.3)
        src = real_data(r"the Surface, 10 December 2025; the House's calibrator, every evaluation recorded")
        with self.voiceover(
            "Now watch it set them. The calibrator prices all of the Surface's quotes by Fourier, compares them with "
            "the market, and asks a least-squares optimizer for a better set of five. Every evaluation is recorded, "
            "so we can replay the fit. On the right, the loss, best so far, from three starting points: the band is "
            "their spread. On the left, the model's smiles at three expiries, rebuilt at checkpoints. "
            "<bookmark mark='a'/> From the default start the smiles are too flat and the loss is "
            f"{r0['trace']['best'][0]:.1f}. The optimizer first raises the vol of vol and tilts the correlation, and "
            "the smiles start to bend. <bookmark mark='b'/> Then a long stretch where it trades mean reversion "
            "against vol of vol, sliding along a valley we will map in chapter sixteen, until it settles at kappa "
            f"{r0['x'][1]:.1f} and xi {r0['x'][3]:.1f}. <bookmark mark='c'/> The two random starts begin far worse, "
            f"at {r1['trace']['best'][0]:.0f} and {r2['trace']['best'][0]:.0f}, and all three end at the same loss, "
            f"{r0['rmse']:.3f}, after {r0['n_eval']}, {r1['n_eval']} and {r2['n_eval']} evaluations. One caution about "
            "units: the optimizer's loss is a price error divided by vega, a fast stand-in for the implied-volatility "
            f"error, which at the end is {frames[-1]['iv_rmse']:.2f} points."
        ) as vo:
            self.play(FadeIn(rpl), FadeIn(cap), FadeIn(src))
            vo.wait_until("a")
            rpl.play(self, run_time=max(vo.until("c") - 0.5, 4))
            vo.wait_until("c")
        self.wait(0.4)
        self.clear_scene()

    def fit(self, c):
        h = c["fits"]["Heston"]
        p = h["params"]
        days = sorted(int(d) for d in h["by_expiry"])
        bsx = [c["fits"]["BS"]["by_expiry"][str(d)] for d in days]
        hsx = [h["by_expiry"][str(d)] for d in days]
        g = axes([-0.6, len(days) - 0.4], [0, 8], x_length=6.6, y_length=3.6, xlabel=r"expiry (days)",
                 ylabel=r"fit error (vol points)", xticks=list(range(len(days))), xfmt=lambda u: str(days[int(round(u))]),
                 yticks=[0, 2, 4, 6, 8], font_size=16).to_edge(LEFT, buff=0.7).shift(DOWN * 0.4)
        ax = g.ax
        w = 0.32

        def bar(i, v, dx, col):
            return Rectangle(width=w, height=max(abs(ax.c2p(0, min(v, 8))[1] - ax.c2p(0, 0)[1]), 1e-3), stroke_width=0,
                             fill_color=col, fill_opacity=0.85).move_to(ax.c2p(i + dx, min(v, 8) / 2))

        b1 = VGroup(*[bar(i, v, -0.18, MODEL_COL["BS"]) for i, v in enumerate(bsx)])
        b2 = VGroup(*[bar(i, v, 0.18, MODEL_COL["Heston"]) for i, v in enumerate(hsx)])
        leg = legend([(MODEL_COL["BS"], rf"Black--Scholes, one vol: {c['fits']['BS']['rmse']:.1f} overall"),
                      (MODEL_COL["Heston"], rf"Heston, five numbers: {h['rmse']:.2f} overall")], font_size=17).next_to(
            g, UP, buff=0.15).align_to(g, LEFT)
        tab = VGroup(*[MathTex(s, font_size=28) for s in (
            rf"\sqrt{{v_0}} = {100 * np.sqrt(p['v0']):.0f}\%,\ \ \sqrt{{\theta}} = {100 * np.sqrt(p['theta']):.0f}\%",
            rf"\kappa = {p['kappa']:.1f}\ \ (\text{{half-life}}\ {365 * np.log(2) / p['kappa']:.0f}\ \text{{days}})",
            rf"\xi = {p['xi']:.1f},\ \ \rho = {p['rho']:.2f}",
            rf"2\kappa\theta / \xi^2 = {c['feller']:.2f} < 1")]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        tab[3].set_color(BAD)
        note_ = wrapped_label(r"a vol of vol of several hundred percent: Heston fits the Surface only by making its "
                              r"variance violent; the 3-day options are still missed by several points", 4.6, 19, GREY_A)
        side = VGroup(tab, note_).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        src = real_data(rf"the Surface: {c['n']} quotes, vega-weighted implied-vol error")
        d3 = h["by_expiry"][str(days[0])]
        with self.voiceover(
            "Here is where it landed, expiry by expiry. A single Black–Scholes volatility misses by "
            f"{c['fits']['BS']['rmse']:.1f} points. <bookmark mark='a'/> Heston misses by {h['rmse']:.1f}. "
            "<bookmark mark='b'/> But look at what it took. Mean reversion with a half-life of "
            f"{365 * np.log(2) / p['kappa']:.0f} days. A volatility of volatility of {100 * p['xi']:.0f} percent. "
            f"Feller's ratio is {c['feller']:.2f}, far below one. And the shortest expiry, {days[0]} days, is still "
            f"missed by {d3:.1f} points. Heston can bend its smile only so fast, and the next derivation says why."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg[0]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in b1],
                                                                          lag_ratio=0.1, run_time=1.5))
            vo.wait_until("a")
            self.play(FadeIn(leg[1]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in b2], lag_ratio=0.1, run_time=1.5))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=2.5), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def skew(self, sl):
        rows = [cmath(r"\sigma^2_{\text{imp}}(k)", r"\approx", r"\Big(\int_0^1 \frac{ds}{\sigma_{\text{loc}}(sk)}\Big)^{-2}"
                      r"\ \approx\ \int_0^1 \sigma^2_{\text{loc}}(sk)\,ds", font_size=32,
                      colors={r"\sigma^2_{\text{imp}}(k)": IV}),
                cmath(r"\sigma^2_{\text{loc}}(x)", r"=", r"\mathbb{E}\big[v \mid x\big] \approx v_0 + \rho\xi\,x", font_size=34,
                      colors={r"\sigma^2_{\text{loc}}(x)": MODEL_COL["LV"]}),
                cmath(r"\sigma^2_{\text{imp}}(k)", r"\approx", r"v_0 + \tfrac12\rho\xi\,k", font_size=34,
                      colors={r"\sigma^2_{\text{imp}}(k)": IV}),
                cmath(r"\partial_k\sigma_{\text{imp}}\big|_{k=0}", r"\approx", r"\frac{\rho\,\xi}{4\sqrt{v_0}}", font_size=36,
                      colors={r"\partial_k\sigma_{\text{imp}}\big|_{k=0}": IV})]
        whys = [why(r"Berestycki, Busca and Florent (2002): as $T \to 0$ the implied vol is the harmonic mean of local vol "
                    r"along the straight line to $k$; to first order in $k$, the arithmetic mean of local variance", 20),
                why(r"Gy\"ongy (Part 12): local variance is the expected variance given the price; over a short time "
                    r"$v - v_0 \approx \xi\sqrt{v_0}W^2$, $x \approx \sqrt{v_0}W^1$: a Gaussian regression", 20),
                why(r"average a straight line over $sk$, $s \in [0, 1]$: half its slope", 20),
                why(r"differentiate the square root at $v_0$: the short-maturity skew of Heston is a constant", 20)]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.2, buff=0.6, edge=6.9)
        res = VGroup(MathTex(rf"\frac{{\rho\xi}}{{4\sqrt{{v_0}}}} = {sl['skew_formula']:.3f}", font_size=34, color=IV),
                     MathTex(rf"\text{{model, 2 days:}}\ {sl['skew_2d']:.3f}", font_size=34, color=MODEL_COL["Heston"])
                     ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.5)
        pp = pause(r"Make $\rho$ positive. What happens to the 3-day skew?", width=4.4).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Where does the limit come from? Derive the skew at very short maturity. Berestycki, Busca and Florent "
            "showed that as expiry goes to zero, the implied volatility at log-strike k is the harmonic mean of "
            "local volatility along the straight line from the money to k; to first order, the average local "
            "variance. <bookmark mark='a'/> By Gyöngy's theorem from Part twelve, local variance is the expected "
            "variance given the price. Over a short time both are Gaussian, the variance moving by xi root v nought "
            "times one Brownian motion and the log price by root v nought times the other, so the regression of one "
            "on the other has slope rho xi. <bookmark mark='b'/> Average that straight line from zero to k: you get "
            "half its slope. <bookmark mark='c'/> Take the square root and differentiate. The short-maturity skew is "
            "rho xi over four root v nought: a constant, set by correlation times vol of vol. <bookmark mark='d'/> On "
            f"our fit the formula gives {sl['skew_formula']:.3f}, and the model itself, priced at two days, gives "
            f"{sl['skew_2d']:.3f}. So to match the market's steep three-day skew, Heston has no choice but an "
            "enormous xi, and that is exactly what the calibrator found. The curvature, likewise, grows with xi "
            "squared. <bookmark mark='e'/> Pause and predict: make rho positive. The three-day skew flips sign, a "
            "call skew. For Bitcoin in 2023's rally, that was not absurd."
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
            vo.wait_until("e")
            self.play(FadeIn(pp))
        self.wait(0.4)
        self.clear_scene()
