from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import (BAD, IV, MODEL_COL, NAMES, OPT, PART, RV, SPOT, VAR, illustration, load, pause,
                                         real_data)

LAB_VG = [
    "def vg_cf(u, T, sigma, nu, th):",
    "    w = np.log(1 - th*nu - 0.5*sigma*sigma*nu) / nu",
    "    return (1 - 1j*u*th*nu + 0.5*sigma*sigma*nu*u*u) \\",
    "        ** (-T / nu) * np.exp(1j * u * w * T)",
    "",
    "def vg_paths(S0, sigma, nu, th, T, n, n_paths, seed=0):",
    "    dt = T / n",
    "    w = np.log(1 - th*nu - 0.5*sigma*sigma*nu) / nu",
    "    G = rng.gamma(dt / nu, nu, (n, n_paths))     # the clock",
    "    dX = th*G + sigma*np.sqrt(G)*rng.standard_normal(G.shape) + w*dt",
    "    return S0 * np.exp(cumsum(dX))",
]


class Levy(VoiceoverScene):
    def construct(self):
        v = load("lab_vg")
        lf = load("levy_fits")
        self.card()
        self.clock(v)
        self.derive()
        self.fine(v)
        self.lab(v)
        self.race(lf)

    def card(self):
        c = chapter_card(9, r"L\'evy models and time changes", r"What if the market's clock runs at a random speed?",
                         lit=(2002, 2004), part=PART)
        with self.voiceover("Chapter nine. Lévy models, and changing the clock."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def clock(self, v):
        ck = v["clock"]
        t = np.asarray(ck["t"])
        G = np.asarray(ck["G"])
        X = np.asarray(ck["X"])
        Tm = float(t[-1])
        top = axes([0, Tm * 1.05], [-0.25, 0.25], x_length=10.0, y_length=2.6, ylabel=r"log price", xticks=[0, Tm],
                   xfmt=lambda u: "0" if u == 0 else r"3\ \text{months}", yticks=[-0.2, 0, 0.2], font_size=15)
        bot = axes([0, Tm * 1.05], [0, Tm * 1.15], x_length=10.0, y_length=2.2, xlabel=r"calendar time",
                   ylabel=r"business time: the gamma clock $G_t$", xticks=[0, Tm], xfmt=lambda u: "0" if u == 0 else r"3\ \text{months}",
                   yticks=[0, Tm], yfmt=lambda u: "0" if u == 0 else r"3\ \text{m}", font_size=15)
        VGroup(top, bot).arrange(DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
        lam = ValueTracker(0.0)  # 0: plotted against business time; 1: against calendar time

        def path():
            w = lam.get_value()
            xs = (1 - w) * G + w * t
            return VMobject(stroke_color=SPOT, stroke_width=2.5).set_points_as_corners(
                [top.ax.c2p(a, b) for a, b in zip(xs, np.clip(X, -0.25, 0.25))])

        p = always_redraw(path)
        stair = VMobject(stroke_color=VAR, stroke_width=3).set_points_as_corners(
            [bot.ax.c2p(a, b) for a, b in zip(np.repeat(t, 2)[1:], np.repeat(G, 2)[:-1])])
        diag = DashedLine(bot.ax.c2p(0, 0), bot.ax.c2p(Tm, Tm), stroke_color=GREY_C, stroke_width=1.5)
        tag = always_redraw(lambda: label(r"plotted against business time" if lam.get_value() < 0.5 else
                                          r"plotted against calendar time: a variance gamma path", font_size=20,
                                          color=SPOT).next_to(top, UP, buff=0.05).align_to(top, RIGHT))
        src = illustration(rf"$\nu = {ck['nu']}$, $\sigma = {100 * ck['sigma']:.0f}\%$, {len(t) - 1} steps")
        nu_fit = v["params"][1]
        with self.voiceover(
            "Here is a different way to make a smile: keep the Brownian motion, but change the clock. On top, an "
            "ordinary Brownian path, plotted against business time: the time the market experiences. "
            "<bookmark mark='a'/> Below, the clock that converts calendar time into business time. It is a gamma "
            "process: it only goes forward, and it goes forward in random lurches. Where the purple staircase "
            "climbs steeply, a lot of business time passed in a little calendar time: a burst of trading. Where it "
            "is flat, the market slept. <bookmark mark='b'/> Now replot the very same path against calendar time. "
            "Stretches of business time that passed in an instant collapse into jumps. Quiet stretches flatten out. "
            "The result has no diffusion at all: it moves only by jumps, infinitely many of them, mostly tiny. That "
            "is the variance gamma process of Dilip Madan and Eugene Seneta, 1990, put to work on options by Madan, "
            "Peter Carr and Eric Chang in 1998. <bookmark mark='c'/> The clock's randomness is one number, nu, the "
            f"variance of the clock per unit time. On the Surface, the fitted nu is only {nu_fit:.3f}: the options "
            "ask for a nearly regular clock and a strong drift, which is how variance gamma makes its skew."
        ) as vo:
            self.play(FadeIn(top), FadeIn(src), FadeIn(tag))
            self.add(p)
            vo.wait_until("a")
            self.play(FadeIn(bot), Create(diag), Create(stair), run_time=2.5)
            vo.wait_until("b")
            self.play(lam.animate.set_value(1.0), run_time=4)
        p.clear_updaters()
        tag.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"X_t", r"=", r"\theta\,G_t + \sigma\,W_{G_t},\qquad G_t \sim \Gamma\big(\text{shape } t/\nu,\ "
                      r"\text{scale } \nu\big)", font_size=32, colors={r"X_t": SPOT}),
                cmath(r"\mathbb{E}\big[e^{iuX_t} \mid G_t\big]", r"=", r"e^{\,G_t\,(iu\theta - \frac12\sigma^2u^2)}",
                      font_size=34, colors={r"\mathbb{E}\big[e^{iuX_t} \mid G_t\big]": OPT}),
                cmath(r"\varphi(u)", r"=", r"\mathbb{E}\big[e^{sG_t}\big]_{s = iu\theta - \sigma^2u^2/2} = "
                      r"\big(1 - iu\theta\nu + \tfrac12\sigma^2\nu u^2\big)^{-t/\nu}", font_size=32,
                      colors={r"\varphi(u)": OPT}),
                cmath(r"\omega", r"=", r"\tfrac1\nu\ln\big(1 - \theta\nu - \tfrac12\sigma^2\nu\big)", font_size=34,
                      colors={r"\omega": VAR}),
                cmath(r"\psi_{\text{CGMY}}(u)", r"=", r"C\,\Gamma(-Y)\big[(M - iu)^Y - M^Y + (G + iu)^Y - G^Y\big]",
                      font_size=32, colors={r"\psi_{\text{CGMY}}(u)": OPT}),
                cmath(r"\mathbb{E}\big[e^{iuL_{\tau_t}}\big]", r"=", r"\mathbb{E}\big[e^{\tau_t\,\psi_L(u)}\big],\quad "
                      r"\tau_t = \int_0^t v_s\,ds", font_size=34, colors={r"\mathbb{E}\big[e^{iuL_{\tau_t}}\big]": OPT})]
        whys = [why(r"Brownian motion with drift $\theta$, run on a gamma clock with mean $t$ and variance $\nu t$ "
                    r"(Madan and Seneta 1990)", 20),
                why(r"given the clock, the price is Gaussian: the mean and variance are proportional to $G_t$", 20),
                why(r"tower property, then the gamma law's moment generating function $(1 - \nu s)^{-t/\nu}$", 20),
                why(r"add $\omega t$ to the drift so that $\varphi(-i) = 1$: the forward is a martingale", 20),
                why(r"integrate $e^{iux} - 1$ against the L\'evy density $C e^{-G|x|}/|x|^{1+Y}$ (and $M$ on the right); VG is "
                    r"$Y = 0$, $C = 1/\nu$ (Carr, Geman, Madan and Yor 2002)", 20),
                why(r"run any L\'evy process on a CIR clock: its characteristic function is the clock's Laplace transform, "
                    r"Heston's affine formula again (Carr and Wu 2004)", 20)]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.0, buff=0.8, edge=6.9)
        with self.voiceover(
            "The characteristic function falls out in three lines. Write the log price as a drift theta and a "
            "Brownian motion, both run on the gamma clock. <bookmark mark='a'/> Given the clock, the price is "
            "Gaussian, with mean and variance proportional to the business time elapsed. <bookmark mark='b'/> Take "
            "the expectation over the clock with the tower property: it is the gamma distribution's moment "
            "generating function, evaluated at a complex argument. One minus i u theta nu plus a half sigma "
            "squared nu u squared, to the power minus t over nu. <bookmark mark='c'/> A constant drift correction, "
            "omega, keeps the forward fair. <bookmark mark='d'/> Carr, Geman, Madan and Yor generalised the jump "
            "density to C e to the minus G x over x to the one plus Y, and integrated it in closed form. The exponent "
            "Y is the fine structure: below zero, finitely many jumps; between zero and one, infinitely many but "
            "summable; above one, so many that the path has infinite variation, like a diffusion. "
            "<bookmark mark='e'/> And Carr and Liuren Wu closed the circle in 2004: run any Lévy process on a "
            "random clock whose speed is a CIR variance, and the characteristic function is the clock's Laplace "
            "transform. That is Heston's affine formula again: stochastic volatility is a random clock."
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
            vo.wait_until("e")
            step(5)
        self.wait(0.4)
        self.clear_scene()

    def fine(self, v):
        cg = v["cgmy"]
        Ys = ["-0.5", "0.5", "1.5"]
        cols = {"-0.5": BAD, "0.5": OPT, "1.5": RV}
        xs = np.linspace(0.02, 0.6, 120)
        dens = axes([0, 0.6], [0, 4], x_length=4.2, y_length=3.0, xlabel=r"jump size $|x|$",
                    ylabel=r"L\'evy density (log scale)", xticks=[0, 0.3, 0.6], yticks=[0, 2, 4],
                    yfmt=lambda u: f"10^{{{u:.0f}}}", font_size=14)
        paths = VGroup()
        for Y in Ys:
            X = np.asarray(cg[Y]["X"])
            tt = np.linspace(0, 1, len(X))
            a = axes([0, 1], [-0.8, 0.8], x_length=7.6, y_length=1.55, yticks=[-0.5, 0, 0.5], font_size=12)
            ln = curve(a.ax, tt, np.clip(X - X[0], -0.8, 0.8), cols[Y], stroke_width=2)
            t_ = MathTex(rf"Y = {Y}", font_size=26, color=cols[Y]).next_to(a, LEFT, buff=0.2)
            paths.add(VGroup(a, ln, t_))
        paths.arrange(DOWN, buff=0.25).to_edge(RIGHT, buff=0.4)
        dens.to_edge(LEFT, buff=0.6).shift(UP * 0.3)
        lines = VGroup(*[curve(dens.ax, xs, np.clip(np.log10(cg[Y]["C"] * np.exp(-5 * xs) / xs ** (1 + float(Y))), 0, 4),
                               cols[Y], stroke_width=3) for Y in Ys])
        cap = wrapped_label(r"$C e^{-5|x|}/|x|^{1+Y}$, with $C$ set so every process has the same yearly variance; "
                            r"right: one year of each, simulated (small jumps as their Gaussian limit)", 4.6, 18, GREY_B)
        cap.next_to(dens, DOWN, buff=0.35).align_to(dens, LEFT)
        src = illustration(r"CGMY with $G = M = 5$, annual variance 0.25")
        with self.voiceover(
            "Here is the fine structure, as pictures. On the left, the density of jumps by size, for three values of "
            "Y, scaled so that all three processes have the same total variance. On the right, one year of each. "
            "<bookmark mark='a'/> With Y minus one half, the density is finite: a handful of jumps a year, and "
            f"flat stretches between them; about {cg['-0.5']['lam_eps']:.0f} jumps here. <bookmark mark='b'/> With "
            "Y one half, the density blows up at zero but its total size stays finite: a swarm of small jumps "
            f"with some big ones, {cg['0.5']['lam_eps']:.0f} of them above a tenth of a percent. "
            "<bookmark mark='c'/> With Y one and a half, there are so many tiny jumps that the path looks like a "
            f"diffusion, {cg['1.5']['lam_eps']:.0f} above a tenth of a percent in the year, with occasional big "
            "ones on top. Pause and predict: variance gamma has no Brownian part. Can its paths look continuous? On "
            "a chart, yes: infinitely many small jumps are indistinguishable from a diffusion at any resolution you "
            "can see."
        ) as vo:
            self.play(FadeIn(dens), FadeIn(src), FadeIn(cap), Create(lines[0]), FadeIn(paths[0][0]), FadeIn(paths[0][2]),
                      Create(paths[0][1]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(lines[1]), FadeIn(paths[1][0]), FadeIn(paths[1][2]), Create(paths[1][1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(lines[2]), FadeIn(paths[2][0]), FadeIn(paths[2][2]), Create(paths[2][1]), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def lab(self, v):
        card = lab_card(r"variance gamma, two ways", LAB_VG, source="explainer/quant/house/stochvol.py", width=8.8)
        card.to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.4)
        s, nu, th = v["params"]
        z = (v["mc"] - v["cos"]) / v["se"]
        outs = [f"fitted VG: sigma {s:.3f}, nu {nu:.4f}, theta {th:.3f}",
                f"30-day ATM call by COS:          {v['cos']:.5f}",
                f"by {v['n']:,} simulated paths:  {v['mc']:.5f} +/- {v['se']:.5f}",
                f"difference: {z:+.1f} standard errors"]
        verdict = (f"The two agree within {abs(z):.1f} standard errors." if abs(z) < 2 else
                   f"They differ by {abs(z):.1f} standard errors: more paths, or a finer clock, are needed.")
        with self.voiceover(
            "In the House it is a few lines each: the characteristic function with its drift correction, and the "
            "simulator, which draws gamma clock increments and then a Gaussian scaled by their square root. "
            "<bookmark mark='a'/> Run both on the fitted variance gamma: price a thirty-day at-the-money call by "
            f"Fourier, and by simulation. {verdict}"
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            lab_run(self, card, outs, run_time=3)
        self.wait(0.6)
        self.clear_scene()

    def race(self, lf):
        F = lf["fits"]
        tags = ("VG", "NIG", "CGMY", "CGMY_inf")
        cols = {"VG": MODEL_COL["VG"], "NIG": MODEL_COL["NIG"], "CGMY": GREY_A, "CGMY_inf": MODEL_COL["CGMY"]}
        n_max = max(F[t]["trace"]["eval"][-1] for t in tags)
        g = axes([0, n_max], [0, 8], x_length=6.4, y_length=4.0, xlabel=r"evaluations", ylabel=r"calibrator loss, best so far",
                 xticks=[0, n_max], yticks=[0, 2, 4, 6, 8], font_size=15).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        tr = ValueTracker(0)

        def series(tg):
            ev, b = np.asarray(F[tg]["trace"]["eval"]), np.clip(np.asarray(F[tg]["trace"]["best"]), 0, 8)

            def mk():
                k = max(int(np.searchsorted(ev, tr.get_value(), side="right")), 2)
                return VMobject(stroke_color=cols[tg], stroke_width=3).set_points_as_corners(
                    [g.ax.c2p(a, c_) for a, c_ in zip(ev[:k], b[:k])])
            return always_redraw(mk)

        lines = VGroup(*[series(t_) for t_ in tags])
        lab = {"VG": r"variance gamma", "NIG": r"NIG", "CGMY": r"CGMY, $Y < 1$", "CGMY_inf": r"CGMY, $1 < Y < 2$"}
        leg = legend([(cols[t_], lab[t_]) for t_ in tags], font_size=17).next_to(g, UP, buff=0.12).align_to(g, LEFT)
        c1, c2 = F["CGMY"]["params"], F["CGMY_inf"]["params"]
        side = VGroup(*[MathTex(rf"\text{{{lab_}}}:\ {F[t_]['rmse_iv']:.2f}", font_size=28, color=cols[t_])
                        for t_, lab_ in (("VG", "VG"), ("NIG", "NIG"), ("CGMY", "CGMY, Y<1"), ("CGMY_inf", "CGMY, Y>1"))])
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        hit = c1["Y"] > 0.94
        inf_better = F["CGMY_inf"]["rmse_iv"] < F["CGMY"]["rmse_iv"]
        yv = MathTex(rf"Y = {c2['Y']:.2f}", font_size=36, color=MODEL_COL["CGMY"])
        note_ = wrapped_label(r"implied-vol error, vol points; Carr--Wu: the same L\'evy process on a stochastic clock is "
                              r"stochastic volatility with jumps", 4.4, 18, GREY_A)
        S = VGroup(side, yv, note_).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        v1 = (f"Fitted with Y below one, CGMY runs to the edge, {c1['Y']:.2f}." if hit else
              f"Fitted with Y below one, CGMY stops at {c1['Y']:.2f}.")
        v2 = (f"Allowed above one, it settles at Y equal to {c2['Y']:.2f} and fits better: the Surface asks for infinite "
              "variation, jumps so small and so many that they act like a diffusion." if inf_better else
              f"Allowed above one, it reaches {c2['Y']:.2f} but fits no better: finite variation is enough.")
        hes = load("calibrate")["fits"]["Heston"]["rmse"]
        src = real_data(r"the Surface; the House's calibrator, every evaluation recorded")
        with self.voiceover(
            "Now race the pure-jump models on the Surface: variance gamma, NIG, which runs Brownian motion on an "
            "inverse Gaussian clock as Ole Barndorff-Nielsen proposed in 1997, and CGMY, fitted twice, with its Y "
            "confined below one and above one. <bookmark mark='a'/> All four fall fast and then flatten well "
            f"above Heston's {hes:.1f}. {v1} <bookmark mark='v'/> {v2} <bookmark mark='b'/> None of them can match stochastic "
            "volatility, and the next chapter shows the reason in one picture: what each model's skew does as "
            "maturity changes."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(src))
            self.add(lines)
            self.play(tr.animate.set_value(n_max), run_time=max(vo.until("a") + 3, 4), rate_func=linear)
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(yv), FadeIn(note_))
        for l_ in lines:
            l_.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
