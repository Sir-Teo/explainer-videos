from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import (BAD, IV, MODEL_COL, NAMES, OPT, PART, RV, SPOT, VAR, illustration, load, pause,
                                         real_data)

SMALL = ("Heston", "Bates", "Merton", "VG", "NIG", "CGMY_inf")


class Skew(VoiceoverScene):
    def construct(self):
        c = load("calibrate")
        sm = load("skew_more")
        self.card()
        self.multiples(sm)
        self.termstructure(sm)
        self.derive(c)
        self.cards(c)

    def card(self):
        c = chapter_card(10, r"The skew across maturities", r"What does each model's skew do as expiry nears?",
                         part=PART)
        with self.voiceover("Chapter ten. The skew across maturities: one picture that sorts every model."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c), run_time=0.35)

    def multiples(self, sm):
        Tm = np.asarray(sm["Tm"])
        z = np.asarray(sm["z"])

        def panel(name, j):
            iv = np.asarray(sm["small"][name][j])
            a = axes([-2.6, 2.6], [0, 0.85], x_length=3.4, y_length=2.0, xticks=[-2, 0, 2], yticks=[0, 0.4, 0.8],
                     yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=12)
            ln = curve(a.ax, z, iv, MODEL_COL[name], stroke_width=3)
            t = label(NAMES[name], font_size=18, color=MODEL_COL[name]).next_to(a, UP, buff=0.05)
            return VGroup(a, ln, t)

        def grid(j):
            G = VGroup(*[panel(n, j) for n in SMALL]).arrange_in_grid(rows=2, cols=3, buff=(0.5, 0.45))
            return G.to_edge(UP, buff=0.7)

        cur = grid(0)
        days = lambda j: Tm[j] * 365  # noqa: E731
        readout_ = VGroup(label(r"expiry", font_size=22, color=GREY_A),
                          MathTex(f"{days(0):.0f}", font_size=34)).arrange(RIGHT, buff=0.2)
        readout_.to_edge(DOWN, buff=0.9)
        cap = wrapped_label(r"each model's smile against standardized moneyness $k / (\tfrac12\sqrt{T})$, as expiry shrinks "
                            r"from a year to two days", 7.4, 19, GREY_B).to_corner(DL, buff=0.35)  # the source takes DR
        src = real_data(r"every model as fitted to the Surface", corner=DR)
        with self.voiceover(
            (
            "Ask every fitted model one question: what happens to your smile as expiry nears? Six of them, each smile "
            "drawn against moneyness scaled by root time. Shrink the expiry from a year. <bookmark mark='a'/> Heston's "
            "shape barely changes: a diffusion's skew tends to a constant. <bookmark mark='b'/> The pure-jump models "
            "twist harder and harder, into cliffs at a few days. Merton's rare crashes show only in the far put wing; "
            "Bates and CGMY sit between."
        )
        ) as vo:
            self.play(FadeIn(cur), FadeIn(readout_), FadeIn(cap), FadeIn(src))
            per = max((vo.remaining(2.0) - 1.0) / (len(Tm) - 1), 0.4)
            for j in range(1, len(Tm)):
                new = grid(j)
                num = MathTex(f"{days(j):.0f}", font_size=34).move_to(readout_[1])
                self.play(Transform(cur, new), Transform(readout_[1], num), run_time=per)
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def termstructure(self, sm):
        T = np.asarray(sm["T"])
        mk = sm["market"]
        g = axes([np.log10(2 / 365), 0], [-1.75, 0.8], x_length=6.6, y_length=4.4, xlabel=r"years to expiry (log scale)",
                 ylabel=r"at-the-money skew $|\partial_k \sigma|$ (log scale)",
                 xticks=[np.log10(x) for x in (3 / 365, 10 / 365, 30 / 365, 0.25, 1.0)],
                 xfmt=lambda u: {0: "1y"}.get(round(u, 3), f"{365 * 10 ** u:.0f}d"), log_x=True, font_size=15)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        for v in (0.05, 0.1, 0.3, 1, 3):
            g.add(label(f"{v:g}", font_size=15, color=GREY_B).next_to(ax.c2p(np.log10(2 / 365), np.log10(v)), LEFT, buff=0.12))
        lx = np.log10(T)
        order = ("Heston", "Bates", "Merton", "Kou", "VG", "NIG", "CGMY_inf")
        lines = VGroup(*[curve(ax, lx, np.log10(np.abs(np.asarray(sm["models"][n])) + 1e-9),
                               MODEL_COL[n], stroke_width=2.5) for n in order])
        dots = VGroup(*[Dot(ax.c2p(np.log10(r["T"]), np.log10(abs(r["skew"]))), radius=0.07, color=WHITE) for r in mk
                        if abs(r["skew"]) > 0.02])
        sab = VGroup(*[Square(0.12, stroke_width=0, fill_color=MODEL_COL["SABR"], fill_opacity=1).move_to(
            ax.c2p(np.log10(r["T"]), np.log10(abs(r["skew"])))) for r in sm["sabr"] if abs(r["skew"]) > 0.02])
        sl = sm["slopes"]
        rows = [(r"\text{market}", sl["market"]["short"], sl["market"]["long"], WHITE)]
        rows += [(rf"\text{{{NAMES[n]}}}", sl[n]["short"], sl[n]["long"], MODEL_COL[n]) for n in order]
        cells = VGroup(MathTex(r"\text{local slope}", font_size=22, color=GREY_A),
                       MathTex(r"2\text{--}14\text{d}", font_size=22, color=GREY_A),
                       MathTex(r"60\text{--}365\text{d}", font_size=22, color=GREY_A))
        for a, b, c_, col in rows:
            cells.add(MathTex(a, font_size=24, color=col), MathTex(f"{b:+.2f}", font_size=24, color=col),
                      MathTex(f"{c_:+.2f}", font_size=24, color=col))
        tab = cells.arrange_in_grid(rows=len(rows) + 1, cols=3, buff=(0.35, 0.12), col_alignments="lrr")
        tab.to_edge(RIGHT, buff=0.35).shift(DOWN * 0.1)
        h, vg, ni, me, ko, cg = (sl[n] for n in ("Heston", "VG", "NIG", "Merton", "Kou", "CGMY_inf"))
        mkt = sl["market"]
        Y = load("levy_fits")["fits"]["CGMY_inf"]["params"]["Y"]
        cgmy_s = (f"Only CGMY, with Y of {Y:.2f}, infinite-variation jumps that behave almost like a diffusion, comes "
                  f"close to the market at the short end: {cg['short']:.2f}." if abs(cg["short"] - mkt["short"]) < 0.2 else
                  f"CGMY's short-end slope is {cg['short']:.2f}.")
        between = (h["short"] > mkt["short"] > vg["short"])
        end_s = ("So at the short end the market sits between the diffusions and the pure-jump models. No model in this "
                 "part gets its power right at every horizon, and the overall slope of about minus one half is where "
                 "Part fourteen begins." if between else
                 "The market does not sit neatly between the families here; Part fourteen takes up the power law that "
                 "summarises it.")
        with self.voiceover(
            f"""The powers in this table are regressions over finite maturity ranges. White points come from the fitted Surface; green squares from per-expiry SABR, which approximates the quoted slices. <bookmark mark='a'/> The market proxy's overall slope is {mkt['all']:.2f}; its short and long fits are {mkt['short']:.2f} and {mkt['long']:.2f}. <bookmark mark='b'/> Heston gives {h['short']:.2f} and {h['long']:.2f}. Variance gamma gives {vg['short']:.2f} and {vg['long']:.2f}; NIG gives {ni['short']:.2f} and {ni['long']:.2f}. Merton and Kou's short-window fits are {me['short']:.2f} and {ko['short']:.2f}. CGMY with Y equal to {Y:.2f} gives {cg['short']:.2f}. <bookmark mark='c'/> These numbers describe this calibration and grid. They do not identify a universal jump-family exponent or prove the market's asymptotic law. Part fourteen examines those distinctions."""
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.1), FadeIn(sab),
                      run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab[:6])))  # header and the market row
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3, run_time=4), FadeIn(VGroup(*tab[6:])))
            vo.wait_until("c")
            self.play(Indicate(VGroup(*tab[3:6]), color=WHITE))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def derive(self, c):
        rows = [cmath(r"\kappa_n(T)", r"=", r"\kappa_n(1)\,T", font_size=38, colors={r"\kappa_n(T)": OPT}),
                cmath(r"\gamma_1(T)", r"=", r"\frac{\kappa_3(T)}{\kappa_2(T)^{3/2}} = \frac{\gamma_1(1)}{\sqrt{T}}",
                      font_size=38, colors={r"\gamma_1(T)": OPT}),
                cmath(r"\partial_k\sigma\big|_0", r"\propto", r"\frac{\gamma_1(T)}{\sqrt T}\ \propto\ \frac1T",
                      font_size=38, colors={r"\partial_k\sigma\big|_0": IV}),
                cmath(r"\partial_k\sigma\big|_0", r"\to", r"\frac{\rho\xi}{4\sqrt{v_0}}\quad(T\to0,\ v_0>0)", font_size=34,
                      colors={r"\partial_k\sigma\big|_0": IV})]
        whys = [why(r"an exponential L\'evy model has independent, stationary increments: every cumulant of $\ln S_T$ grows "
                    r"linearly in $T$", 20),
                why(r"so the skewness of the log return dies like $1/\sqrt T$", 20),
                why('Near-Gaussian heuristic: $\\partial_k\\sigma\\approx\\gamma_1/(6\\sqrt T)$; its validity generally fails in the short-time jump limit.', 20),
                why('Regular Heston with positive initial variance: finite short-time ATM limit. Finite-maturity damping is model dependent.', 20)]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.0, buff=0.6, edge=6.9)  # the pause card takes the corner
        pp = pause(r"A model's skew is constant as $T \to 0$. Can it fit a 3-day expiry?", width=4.4).to_corner(DL, buff=0.3)  # the rows sit right of centre
        with self.voiceover(
            (
            f"""Here is a useful heuristic, with its regime stated. For a Lévy process with the required finite cumulants, stationary independent increments make each cumulant proportional to time. <bookmark mark='a'/> Standardized skewness therefore scales as one over root T. <bookmark mark='b'/> In a leading near-Gaussian Gram–Charlier approximation, the absolute implied-volatility slope is skewness divided by six root T, suggesting one over T. The near-Gaussian approximation generally breaks down as maturity tends to zero, so this is not a universal short-time Lévy theorem. <bookmark mark='c'/> Smooth Heston dynamics with positive initial variance instead have the finite ATM skew limit derived in chapter four. <bookmark mark='d'/> In this particular fit xi is {c['fits']['Heston']['params']['xi']:.1f}. Finite-expiry skew, rough models and other jump regimes require their own analysis."""
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
            self.play(FadeIn(pp))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def cards(self, c):
        x = c["fits"]["Heston"]["params"]
        c1 = history_card(2007, r"Carr, Geman, Madan and Yor, \textit{Math.\ Finance}",
                          r"``Self-decomposability and option pricing'': additive (Sato) processes, whose increments are "
                          r"independent but not stationary, repair the L\'evy term structure (Cont and Tankov, ch.\ 14).",
                          color=QC.IDEA, width=5.6)
        c2 = history_card(2023, r"Abi Jaber and De Carvalho, ``Reconciling rough volatility with jumps''",
                          rf"With very fast mean reversion and a huge vol of vol, Heston imitates jumps. Our fit, "
                          rf"$\kappa = {x['kappa']:.1f}$ and $\xi = {x['xi']:.1f}$, already leans that way (chapter 18).",
                          color=QC.IDEA, width=5.6)
        G = VGroup(c1, c2).arrange(RIGHT, buff=0.4, aligned_edge=UP)
        with self.voiceover(
            (
            "Two repairs. Carr, Geman, Madan and Yor's additive processes, with independent but non-identical "
            "increments, fix the Lévy term structure. <bookmark mark='a'/> And Abi Jaber and De Carvalho showed that "
            "Heston with very fast mean reversion imitates jumps; chapter eighteen pushes our fit that way."
            " No single model fits every maturity. Next: combining stochastic and local volatility."
        )
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(c2, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

