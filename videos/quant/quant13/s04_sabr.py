from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, illustration, load, real_data


class SABR(VoiceoverScene):
    def construct(self):
        c = load("calibrate")
        s = load("sabr")
        self.card()
        self.model(c)
        self.slices(c)
        self.backbone(s)
        self.density(s)

    def card(self):
        c = chapter_card(3, r"SABR", r"What do traders write on the smile, expiry by expiry?", lit=(2002,), part=PART)
        with self.voiceover("Chapter three. SABR."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self, c):
        rows = [cmath(r"dF_t", r"=", r"\alpha_t F_t^{\beta}\,dW^1_t,\qquad d\alpha_t = \nu\,\alpha_t\,dW^2_t,\quad "
                      r"dW^1 dW^2 = \rho\,dt", font_size=34, colors={r"dF_t": SPOT}),
                cmath(r"\sigma_B(K)", r"\approx", r"\frac{\alpha}{(FK)^{(1-\beta)/2}}\cdot\frac{z}{x(z)}\cdot"
                      r"\Big[1 + O(T)\Big],\quad z = \frac{\nu}{\alpha}(FK)^{(1-\beta)/2}\ln\frac{F}{K}", font_size=32,
                      colors={r"\sigma_B(K)": IV})]
        whys = [why(r"Hagan, Kumar, Lesniewski and Woodward (2002): a lognormal volatility $\alpha$ for the forward, a "
                    r"backbone exponent $\beta$, a vol of vol $\nu$ and a correlation $\rho$, for one expiry at a time"),
                why(r"a singular-perturbation expansion gives the implied volatility directly, with no Fourier integral; "
                    r"it became the rates desks' common language")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=-1.6, buff=1.0, edge=6.9)
        with self.voiceover(
            "Rates and foreign-exchange desks needed something different: a smile they could fit one expiry at a "
            "time, and talk about in a few numbers. In 2002 Patrick Hagan and his co-authors gave them SABR. The "
            "forward moves with a volatility alpha, raised to a backbone power beta, and alpha itself is lognormal, "
            "with its own volatility nu and a correlation rho. <bookmark mark='a'/> Its gift is an expansion: the "
            "implied volatility at each strike, written out directly. No integral, no simulation. Traders quote and "
            "risk-manage smiles in its four numbers to this day."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def slices(self, c):
        sab = c["sabr"]
        days = np.array(sorted(int(d) for d in sab))
        nu = np.array([sab[str(d)]["nu"] for d in days])
        g = axes([np.log10(2), np.log10(400)], [np.log10(0.4), np.log10(10)], x_length=6.2, y_length=4.0,
                 xlabel=r"days to expiry", ylabel=r"SABR's vol of vol $\nu$", xticks=[np.log10(x) for x in (3, 10, 30, 100, 300)],
                 xfmt=lambda u: f"{10 ** u:.0f}", log_x=True, font_size=16).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        # the y axis is log too: place points by hand
        yl = lambda v: np.log10(v)  # noqa: E731
        for v in (0.5, 1, 2, 5, 10):
            g.add(label(f"{v:g}", font_size=16, color=GREY_B).next_to(ax.c2p(np.log10(2), yl(v)), LEFT, buff=0.12))
        dots = VGroup(*[Dot(ax.c2p(np.log10(d), yl(n)), radius=0.07, color=MODEL_COL["SABR"]) for d, n in zip(days, nu)])
        a = c["sabr_nu_power"]
        b0 = np.polyfit(np.log10(days / 365), np.log10(nu), 1)[1]
        xs = np.linspace(np.log10(2.5), np.log10(350), 40)
        fitl = curve(ax, xs, (b0 + a * (xs - np.log10(365))), GREY_A, stroke_width=2)
        side = VGroup(
            MathTex(rf"\text{{error}}\ {c['sabr_rmse']:.2f}\ \text{{vol points}}", font_size=30, color=MODEL_COL["SABR"]),
            wrapped_label(rf"SABR fitted to each of the Surface's {len(days)} expiries on its own ($\beta = 1$): three "
                          rf"numbers per expiry, {3 * len(days)} in all, against Heston's five for everything", 4.6, 19,
                          GREY_A),
            MathTex(rf"\nu \propto T^{{{a:.2f}}}", font_size=40, color=WHITE),
            wrapped_label(r"the vol of vol each expiry needs falls like one over the square root of its maturity. No "
                          r"model in this part produces that; Part 14's rough volatility does", 4.6, 19, VAR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = real_data(r"the Surface, 10 December 2025; log scales")
        with self.voiceover(
            "Fit SABR to the Surface expiry by expiry, and it nails every one: "
            f"{c['sabr_rmse']:.1f} of a volatility point overall. But it uses three numbers per expiry, "
            f"{3 * len(days)} in all. <bookmark mark='a'/> Now plot the vol of vol each expiry asked for, against "
            "the expiry, on log scales. It falls on a line. The slope is "
            f"{a:.2f}: the vol of vol needed falls like one over the square root of maturity. <bookmark mark='b'/> "
            "Remember that number. No model in this part produces it, and in Part fourteen it will turn out to be "
            "a clue that volatility is rough."
        ) as vo:
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(g), LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.15, run_time=2))
            self.play(Create(fitl), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
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
            "The exponent beta is the backbone: how the at-the-money volatility moves when the forward moves. With "
            "beta equal to one, the smile slides along with the price. <bookmark mark='a'/> With beta zero, "
            "volatility falls as the price rises, like a normal model, which suits interest rates. Today's fit "
            "barely cares about beta, because rho and the vol of vol can imitate it. But it decides the dynamics, "
            "and so the hedge. Part twelve's test found that Bitcoin's smile moved with the price: beta near one."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(lines[2]), FadeIn(leg[2]))
            vo.wait_until("a")
            self.play(Create(lines[0]), Create(lines[1]), FadeIn(leg[0]), FadeIn(leg[1]), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def density(self, s):
        d10 = s["density"]["10"]
        d1 = s["density"]["1"]
        p = s["density_params"]
        K = np.asarray(d10["K"])
        g = axes([0, 0.09], [-40, 40], x_length=7.0, y_length=4.0, xlabel=r"strike (rate)", ylabel=r"implied density",
                 xticks=[0, 0.03, 0.06, 0.09], xfmt=lambda u: f"{100 * u:.0f}\\%", yticks=[-40, -20, 0, 20, 40],
                 font_size=16).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        l1 = curve(ax, K, np.clip(np.asarray(d1["pdf"]), -40, 40), RV, stroke_width=2.5)
        l10 = curve(ax, K, np.clip(np.asarray(d10["pdf"]), -40, 40), BAD, stroke_width=3)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0.09, 0), stroke_color=GREY_C, stroke_width=1.5)
        leg = legend([(RV, r"1 year"), (BAD, r"10 years")], font_size=17).next_to(g, UP, buff=0.15).align_to(g, LEFT)
        side = VGroup(
            wrapped_label(rf"below a strike of {100 * d10['neg_below']:.1f}\% the 10-year density is negative, and it "
                          rf"integrates to {d10['mass']:.2f}, not 1: Hagan's formula is an expansion in $\nu^2 T$, and at "
                          r"long expiries and low rates it prices a butterfly below zero", 4.6, 20, WHITE),
            wrapped_label(r"the fixes: solve SABR's effective PDE for the density (Hagan, Kumar, Lesniewski and Woodward "
                          r"2014), or price it exactly near zero (Antonov, Konikov and Spector 2015); the House runs Part "
                          r"9's checker on every SABR slice it quotes", 4.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = illustration(rf"a rates-like smile: forward {100 * p['F']:.0f}\%, $\beta = \tfrac12$, $\rho = {p['rho']}$, "
                           rf"$\nu = {p['nu']}$; at-the-money vol {100 * p['atm']:.0f}\%")
        with self.voiceover(
            "SABR's formula is an expansion, and expansions break. Here is a rates-like smile: a three percent "
            "forward rate, beta one half. At one year, the density implied by Hagan's formula is a fine "
            "distribution. <bookmark mark='a'/> At ten years, it goes negative at low strikes, and the total "
            f"probability comes to {d10['mass']:.2f} instead of one. A butterfly there has a negative price: an "
            "arbitrage, generated by the formula, not the market. When rates sat near zero in the 2010s this was a "
            "daily problem. <bookmark mark='b'/> The fixes solve SABR's equation for the density itself, or price it "
            "exactly near zero, and the House simply runs Part nine's checker on every slice it quotes."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(zero), Create(l1), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(l10), FadeIn(leg[1]), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()
