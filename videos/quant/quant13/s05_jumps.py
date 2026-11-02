from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, load, real_data

NAMES = {"BS": r"Black--Scholes", "Heston": r"Heston", "Bates": r"Bates", "VG": r"variance gamma", "NIG": r"NIG",
         "SABR": r"SABR, per expiry"}


class Jumps(VoiceoverScene):
    def construct(self):
        c = load("calibrate")
        s = load("skew")
        self.card()
        self.models()
        self.levy()
        self.scores(c)
        self.slices(c)
        self.skew(s)

    def card(self):
        c = chapter_card(4, r"Jumps and L\'evy models", r"What if prices do not move continuously?", part=PART)
        with self.voiceover("Chapter four. Jumps, and Lévy models."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def models(self):
        rows = [cmath(r"\frac{dS}{S_-}", r"=", r"\sigma\,dW_t + (e^{J} - 1)\,dN_t - \lambda\bar k\,dt", font_size=36,
                      colors={r"\frac{dS}{S_-}": SPOT}),
                cmath(r"J", r"\sim", r"\mathcal{N}(\mu_J, \sigma_J^2)\ \ \text{(Merton)}\quad\text{or}\quad "
                      r"\text{two exponentials (Kou)}", font_size=34, colors={r"J": BAD}),
                cmath(r"\text{Bates}", r"=", r"\text{Heston} + \text{Merton's jumps}", font_size=36,
                      colors={r"\text{Bates}": MODEL_COL["Bates"]})]
        whys = [why(r"Merton (1976): Poisson-timed jumps $N_t$ at rate $\lambda$ on top of the diffusion; the last term "
                    r"keeps the forward a martingale"),
                why(r"Merton's jumps are log-normal; Kou's (2002) are exponential up and down, with fatter tails and "
                    r"closed-form barrier prices"),
                why(r"Bates (1996): stochastic volatility for the long end, jumps for the short end, after the crash of "
                    r"1987 made short-dated puts dear")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.6, buff=0.85, edge=6.9)
        with self.voiceover(
            "A diffusion cannot gap. Robert Merton added jumps in 1976: on top of the Brownian motion, a Poisson clock "
            "rings at rate lambda, and each ring multiplies the price by a random factor. The last term pays for the "
            "jumps, so the forward stays fair. <bookmark mark='a'/> Merton's jumps are log-normal. Steven Kou's, in "
            "2002, are exponential, with fatter tails and closed-form prices for barriers. <bookmark mark='b'/> David "
            "Bates, studying the market after 1987, put the two ideas together: Heston's variance for the long end, "
            "Merton's jumps for the short end, where a sudden crash is all a three-day put is really about."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def levy(self):
        rows = [cmath(r"X_t", r"=", r"\theta\,G_t + \sigma\,W_{G_t},\qquad G_t \sim \text{Gamma}(t/\nu,\ \nu)",
                      font_size=36, colors={r"X_t": SPOT}),
                cmath(r"\mathbb{E}\,e^{iuX_t}", r"=", r"e^{t\,\psi(u)}", font_size=38,
                      colors={r"\mathbb{E}\,e^{iuX_t}": OPT}),
                cmath(r"X_t", r"=", r"L_{\tau_t},\qquad \tau_t = \int_0^t v_s\,ds", font_size=38, colors={r"X_t": SPOT})]
        whys = [why(r"variance gamma (Madan, Carr and Chang 1998): Brownian motion run on a random gamma clock, so business "
                    r"time speeds up and slows down; infinitely many tiny jumps, no diffusion at all"),
                why(r"every L\'evy process has independent, stationary increments and a characteristic exponent $\psi$: the "
                    r"COS method prices it like Heston. NIG and CGMY (Carr, Geman, Madan and Yor 2002) are cousins"),
                why(r"Carr and Wu (2004): run a L\'evy process on a stochastic clock, and volatility clusters: jumps and "
                    r"stochastic volatility in one frame")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.0, buff=0.85, edge=6.9)
        with self.voiceover(
            "Go further, and drop the diffusion altogether. Variance gamma, from Dilip Madan, Peter Carr and Eric "
            "Chang, runs a Brownian motion on a random clock. Business time speeds up in busy markets and slows in "
            "quiet ones, and the price moves by infinitely many tiny jumps. <bookmark mark='a'/> It belongs to the "
            "Lévy family: independent, stationary increments, and a characteristic function that is a simple "
            "exponential, so the same Fourier machinery prices it. The normal inverse Gaussian and CGMY are its "
            "cousins. <bookmark mark='b'/> And Carr and Liuren Wu showed in 2004 how to unify everything: run a Lévy "
            "process on a stochastic clock, and you get jumps and clustering volatility in one model."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def scores(self, c):
        names = ["BS", "VG", "NIG", "Heston", "Bates", "SABR"]
        vals = [c["fits"][n]["rmse"] if n != "SABR" else c["sabr_rmse"] for n in names]
        npar = [1, 3, 3, 5, 8, 3 * len(c["sabr"])]
        g = axes([0, 4.5], [-0.5, len(names) - 0.5], x_length=6.4, y_length=4.2, xlabel=r"fit error (vol points, vega-weighted)",
                 xticks=[0, 1, 2, 3, 4], yticks=[], font_size=16).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        bars, labs = VGroup(), VGroup()
        for i, (n, v, k) in enumerate(zip(names, vals, npar)):
            y = len(names) - 1 - i
            bars.add(Rectangle(width=abs(ax.c2p(v, 0)[0] - ax.c2p(0, 0)[0]), height=0.45, stroke_width=0,
                               fill_color=MODEL_COL[n], fill_opacity=0.85).move_to(ax.c2p(v / 2, y)))
            labs.add(VGroup(label(NAMES[n], font_size=20, color=MODEL_COL[n]),
                            label(rf"{k} parameter" + ("s" if k > 1 else ""), font_size=16, color=GREY_B)).arrange(DOWN, aligned_edge=RIGHT,
                                                                                          buff=0.05)
                     .next_to(ax.c2p(0, y), LEFT, buff=0.2))
            labs[-1].add(MathTex(f"{v:.2f}", font_size=22).next_to(bars[-1], RIGHT, buff=0.12))
        b = c["fits"]["Bates"]["params"]
        side = VGroup(
            wrapped_label(rf"every model fitted to the same {c['n']} quotes by the same calibrator", 4.4, 19, GREY_A),
            wrapped_label(r"the L\'evy models, with no stochastic volatility, cannot hold the term structure: their "
                          r"smiles flatten too fast with maturity", 4.4, 19, MODEL_COL["VG"]),
            wrapped_label(rf"Bates's jumps add almost nothing: the optimizer pushed them to the edge of what we allowed, "
                          rf"{b['lam']:.0f} a year of {100 * b['mj']:.0f}\% each, a second diffusion. On this calm day, "
                          r"the Surface priced no crash", 4.4, 19, MODEL_COL["Bates"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=0.5)
        src = real_data(r"the Surface, 10 December 2025; the House's calibrator, COS pricing")
        with self.voiceover(
            f"Fit them all to the same {c['n']} quotes, with the same calibrator. Black–Scholes, one number, misses by "
            f"{c['fits']['BS']['rmse']:.1f} points. <bookmark mark='a'/> Variance gamma and NIG, three numbers each, "
            "do better but not well: with no stochastic volatility, their smiles flatten too fast as maturity grows. "
            f"Heston gets to {c['fits']['Heston']['rmse']:.1f}. <bookmark mark='b'/> Bates, with eight numbers, adds "
            f"almost nothing. The optimizer turned its jumps into a flurry of small ones, {c['fits']['Bates']['params']['lam']:.0f} a year: a second "
            "diffusion, not a crash. On this calm December day the Surface was not pricing a crash. "
            f"<bookmark mark='c'/> And SABR, fitted expiry by expiry, is best of all, with {3 * len(c['sabr'])} numbers. "
            "Every extra parameter buys fit. The question this part keeps asking is what it buys beyond that."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]),
                      *[AnimationGroup(GrowFromEdge(bars[i], LEFT), FadeIn(labs[i])) for i in range(1)])
            vo.wait_until("a")
            self.play(*[AnimationGroup(GrowFromEdge(bars[i], LEFT), FadeIn(labs[i])) for i in range(1, 4)], FadeIn(side[1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[4], LEFT), FadeIn(labs[4]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[5], LEFT), FadeIn(labs[5]))
        self.wait(0.4)
        self.clear_scene()

    def slices(self, c):
        panels = VGroup()
        anims = []
        for sl in c["shown"]:
            k, iv = np.asarray(sl["k"]), np.asarray(sl["iv"])
            kk = np.asarray(sl["kk"])
            lo, hi = 0.35, 0.8
            g = axes([kk.min(), kk.max()], [lo, hi], x_length=3.9, y_length=3.2, xlabel=r"log-moneyness",
                     yticks=[0.4, 0.6, 0.8], yfmt=lambda u: f"{100 * u:.0f}\\%",
                     xticks=[round(kk.min() + 0.05, 1), 0, round(kk.max() - 0.05, 1)], font_size=14)
            ttl = label(rf"{sl['days']} days", font_size=20).next_to(g, UP, buff=0.1)
            dots = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.05, color=WHITE) for a, b in zip(k, iv) if lo <= b <= hi])
            lines = VGroup(*[curve(g.ax, kk, np.clip(np.asarray(sl["curves"][n]), lo, hi), MODEL_COL[n], stroke_width=2.2)
                             for n in ("VG", "NIG", "Heston", "Bates")])
            panels.add(VGroup(g, ttl, dots, lines))
        panels.arrange(RIGHT, buff=0.55).to_edge(UP, buff=0.9)
        leg = legend([(WHITE, r"the Surface's quotes")] + [(MODEL_COL[n], NAMES[n]) for n in ("Heston", "Bates", "VG", "NIG")],
                     font_size=17)
        leg.arrange(RIGHT, buff=0.4).next_to(panels, DOWN, buff=0.45)
        foot = wrapped_label(r"at 9 days every model bends; at 198 days the L\'evy models' smiles have gone nearly flat, while "
                             r"the market's has not: their skew dies too fast with maturity", 11.0, 20, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here are three expiries, with each model's smile over the quotes. At nine days, everything can bend. "
            "<bookmark mark='a'/> At fifty-one days, the Lévy models start to miss the wings. <bookmark mark='b'/> At "
            "a hundred and ninety-eight days, their smiles have gone nearly flat, and the market's has not. With "
            "independent increments, a Lévy model's skew must die away as maturity grows. Stochastic volatility "
            "keeps it alive."
        ) as vo:
            self.play(FadeIn(panels[0][:3]), FadeIn(leg), LaggedStart(*[Create(l_) for l_ in panels[0][3]], lag_ratio=0.2),
                      run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(panels[1][:3]), LaggedStart(*[Create(l_) for l_ in panels[1][3]], lag_ratio=0.2), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(panels[2][:3]), LaggedStart(*[Create(l_) for l_ in panels[2][3]], lag_ratio=0.2),
                      FadeIn(foot), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def skew(self, s):
        T = np.asarray(s["T"])
        mk = s["market"]
        g = axes([np.log10(2 / 365), 0], [-1.6, 0.8], x_length=7.0, y_length=4.4, xlabel=r"years to expiry (log scale)",
                 ylabel=r"at-the-money skew $|\partial_k \sigma|$ (log scale)",
                 xticks=[np.log10(x) for x in (3 / 365, 10 / 365, 30 / 365, 0.25, 1.0)],
                 xfmt=lambda u: {0: "1y"}.get(round(u, 3), f"{365 * 10 ** u:.0f}d"), log_x=True, font_size=15)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        for v in (0.05, 0.1, 0.3, 1, 3):
            g.add(label(f"{v:g}", font_size=15, color=GREY_B).next_to(ax.c2p(np.log10(2 / 365), np.log10(v)), LEFT, buff=0.12))
        lx = np.log10(T)
        lines = VGroup(*[curve(ax, lx, np.clip(np.log10(np.abs(np.asarray(s["models"][n]))), -1.6, 0.8), MODEL_COL[n],
                               stroke_width=2.5) for n in ("Heston", "Bates", "VG", "NIG")])
        dots = VGroup(*[Dot(ax.c2p(np.log10(r["T"]), np.log10(abs(r["skew"]))), radius=0.07, color=WHITE) for r in mk
                        if abs(r["skew"]) > 0.02])
        leg = legend([(WHITE, r"the Surface")] + [(MODEL_COL[n], NAMES[n]) for n in ("Heston", "Bates", "VG", "NIG")],
                     font_size=16).next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        side = VGroup(
            MathTex(rf"|\partial_k\sigma| \propto T^{{{s['power']:.2f}}}", font_size=36, color=WHITE),
            wrapped_label(r"diffusions (Heston) flatten toward a constant as $T \to 0$; jumps and L\'evy models blow up "
                          r"like $1/T$; the market sits between, close to $1/\sqrt{T}$, the same law as SABR's vol of vol",
                          4.0, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        with self.voiceover(
            "One picture sums up the chapter. Take the at-the-money skew, how fast implied volatility changes with the "
            "strike, and plot it against maturity, both on log scales. The Surface's expiries fall on a line. "
            f"<bookmark mark='a'/> Its slope is {s['power']:.2f}: the skew grows like one over the square root of "
            "maturity as expiry approaches. <bookmark mark='b'/> Heston's skew flattens toward a constant at short "
            "maturities: a diffusion cannot move far enough in three days. The jump and Lévy models go the other way, "
            "exploding like one over maturity. The market sits between them, close to one over the square root, the "
            "same law as SABR's vol of vol. Neither family produces it. That is the doorway to Part fourteen."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg[0]), LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.1,
                                                             run_time=2))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3, run_time=3), FadeIn(leg[1:]),
                      FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()
