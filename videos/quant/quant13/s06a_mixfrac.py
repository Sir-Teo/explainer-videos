from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, illustration, load, pause


class MixFrac(VoiceoverScene):
    def construct(self):
        ms = load("mixing_sweep")
        e = load("exotics")
        self.card()
        self.dial(ms, e)
        self.derive(ms)
        self.desks()

    def card(self):
        c = chapter_card(12, r"The mixing fraction", r"One dial moves every exotic. Which vanilla can see it?", part=PART)
        with self.voiceover("Chapter twelve. The mixing fraction: one dial between two worlds."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def dial(self, ms, e):
        runs = [r for r in ms["runs"] if r["seed"] == 7]
        runs.sort(key=lambda r: r["eta"])
        extra = [r for r in ms["runs"] if r["eta"] == 0.5]
        grid = np.asarray(ms["grid"])
        k = np.asarray(ms["k"])
        today = np.asarray(e["today"])
        cl_all = [r["cliquet"] for r in ms["runs"]]
        lo_c, hi_c = min(cl_all) * 0.97, max(cl_all) * 1.02
        gL = axes([-0.5, 0.5], [0.3, 2.4], x_length=3.8, y_length=2.8, xlabel=r"log-moneyness", ylabel=r"leverage at 60 days",
                  xticks=[-0.4, 0, 0.4], yticks=[0.5, 1, 1.5, 2], font_size=13)
        gF = axes([-0.25, 0.25], [0.35, 0.7], x_length=3.8, y_length=2.8, xlabel=r"log-moneyness, 30 days",
                  ylabel=r"forward smile in 60 days", xticks=[-0.2, 0, 0.2], yticks=[0.4, 0.5, 0.6],
                  yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=13)
        gC = axes([-0.6, 0.6], [lo_c, hi_c], x_length=1.8, y_length=2.8, ylabel=r"cliquet",
                  yticks=[round(lo_c, 3), round(hi_c, 3)], yfmt=lambda u: f"{100 * u:.1f}\\%", font_size=13)
        P = VGroup(gL, gF, gC).arrange(RIGHT, buff=0.7).to_edge(UP, buff=0.9)
        todayl = DashedVMobject(curve(gF.ax, k, today, WHITE, stroke_width=2), num_dashes=30)
        m = np.abs(grid) <= 0.5

        def frame(r):
            L = curve(gL.ax, grid[m], np.clip(np.asarray(r["L60"])[m], 0.3, 2.4), MODEL_COL["SLV"], stroke_width=3)
            F = curve(gF.ax, k, np.clip(np.asarray(r["fwd_iv"]), 0.35, 0.7), IV, stroke_width=3)
            hgt = abs(gC.ax.c2p(0, r["cliquet"])[1] - gC.ax.c2p(0, lo_c)[1])
            B = Rectangle(width=0.6, height=max(hgt, 1e-3), stroke_width=0, fill_color=OPT, fill_opacity=0.85).move_to(
                gC.ax.c2p(0, (r["cliquet"] + lo_c) / 2))
            Bv = MathTex(rf"{100 * r['cliquet']:.2f}\%", font_size=22).next_to(B, UP, buff=0.08)
            eta = MathTex(rf"\eta = {r['eta']:g}", font_size=40, color=VAR)
            rep = MathTex(rf"\text{{vanilla repricing error}}\ {np.mean(r['reprice']):.2f}\ \text{{vol pts}}", font_size=26,
                          color=GREY_A)
            sk = MathTex(rf"\text{{forward skew}}\ {100 * r['fwd_skew']:.1f}\ \text{{pts}}", font_size=26, color=IV)
            info = VGroup(eta, rep, sk).arrange(RIGHT, buff=0.6).next_to(P, DOWN, buff=0.6)
            return VGroup(L, F, B, Bv, info)

        cur = frame(runs[0])
        cls = [r["cliquet"] for r in runs]
        sks = [r["fwd_skew"] for r in runs]
        mono_c = all(np.diff(cls) <= 0) or all(np.diff(cls) >= 0)
        mono_s = all(np.diff(sks) >= 0) or all(np.diff(sks) <= 0)
        seeds_c = [r["cliquet"] for r in extra]
        sd_c = float(np.std(seeds_c))
        span = max(cls) - min(cls)
        v1 = (f"The cliquet moves steadily, from {100 * cls[0]:.2f} percent at eta zero to {100 * cls[-1]:.2f} at eta "
              "one." if mono_c else
              f"The cliquet moves from {100 * cls[0]:.2f} percent at eta zero to {100 * cls[-1]:.2f} at eta one, though "
              "not in a straight line.")
        v2 = (f"Across three seeds at eta one half, the cliquet varies by only {10000 * sd_c:.1f} basis points, so the "
              f"dial's effect, {10000 * span:.0f} basis points, is real." if sd_c < span / 3 else
              f"Across three seeds at eta one half, the cliquet varies by {10000 * sd_c:.1f} basis points, comparable to "
              "the dial's effect: more particles would be needed to rank the settings.")
        worst = max(np.mean(r["reprice"]) for r in runs)
        v0 = (f"It stays under {worst:.1f} vol points at every setting. That is the whole point: today's vanillas cannot "
              "see eta, and every exotic can." if worst < 1.5 else
              f"It reaches {worst:.1f} vol points at the worst setting, where the particles struggle; even so, the "
              "vanillas barely register the dial, and every exotic does.")
        foot = illustration(r"40{,}000 particles per setting, one seed (three at $\eta = \tfrac12$); white dashes: today's "
                            r"30-day smile", corner=DR)
        leg = label(r"$\eta = 0$: all the volatility from the leverage (local vol); $\eta = 1$: Heston's full vol of vol",
                    font_size=19, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The mixing fraction, eta, is the share of Heston's vol of vol the model keeps. At eta zero the variance "
            "is deterministic and the leverage does everything: that is local volatility, run through particles. At "
            "eta one it is Heston's full vol of vol, with a leverage that only corrects it. Run the particle method at "
            "five settings, forty thousand particles each, and watch three things: the leverage at sixty days, the "
            "thirty-day smile sixty days from now, and the price of the cliquet from the start of this part. "
            "<bookmark mark='a'/> Turn the dial up. The leverage flattens toward one, because more of the "
            "volatility now comes from the random variance. The forward smile steepens away from local "
            f"volatility's flat one: its skew goes from {100 * sks[0]:.1f} points to {100 * sks[-1]:.1f}. {v1} "
            f"<bookmark mark='b'/> And look at the vanilla repricing error, below. {v0} "
            f"<bookmark mark='c'/> {v2}"
        ) as vo:
            self.play(FadeIn(P), Create(todayl), FadeIn(cur), FadeIn(leg), FadeIn(foot))
            vo.wait_until("a")
            per = max((vo.until("b") - 0.5) / (len(runs) - 1), 0.8)
            for r in runs[1:]:
                self.play(Transform(cur, frame(r)), run_time=per)
            vo.wait_until("b")
            self.play(Indicate(cur[4][1], color=WHITE))
            vo.wait_until("c")
            dots = VGroup(*[Dot(gC.ax.c2p(0.4, c_), radius=0.05, color=WHITE) for c_ in seeds_c])
            self.play(Transform(cur, frame(next(r for r in runs if r["eta"] == 0.5))), FadeIn(dots))
        self.wait(0.4)
        self.clear_scene()

    def derive(self, ms):
        rows = [cmath(r"\xi_\eta", r"=", r"\eta\,\xi,\qquad L_\eta^2(S, t)\ \mathbb{E}_\eta\big[v_t \mid S_t = S\big] = "
                      r"\sigma^2_{\text{loc}}(S, t)\ \ \text{for every}\ \eta", font_size=32, colors={r"\xi_\eta": VAR}),
                cmath(r"\eta = 0", r"\Rightarrow", r"L = \sigma_{\text{loc}}/\sqrt{\bar v(t)}:\ \text{local volatility}",
                      font_size=34, colors={r"\eta = 0": MODEL_COL["LV"]}),
                cmath(r"\text{forward skew}", r"\propto", r"\operatorname{Cov}\big(d\ln S,\ d\sigma\big)\ \text{at}\ T_1\ "
                      r"\propto\ \rho\,\eta\,\xi", font_size=32, colors={r"\text{forward skew}": IV}),
                cmath(r"\text{cliquet}(\eta)", r"\approx", r"\text{cliquet}(0) + \eta\,\partial_\eta\text{cliquet}",
                      font_size=34, colors={r"\text{cliquet}(\eta)": OPT})]
        whys = [why(r"Gy\"ongy's condition holds at every $\eta$: each setting reprices every vanilla", 20),
                why(r"no vol of vol: a deterministic variance, so the leverage is all there is", 20),
                why(r"the smile at a future date is tilted by the spot--vol covariance then, which scales with the vol of "
                    r"vol the model keeps (chapter 2's tilt)", 20),
                why(r"so to first order an exotic that bets on the forward smile is monotone in $\eta$: checked above", 20)]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.0, buff=0.6, edge=6.9)
        with self.voiceover(
            "Why does a dial that vanillas cannot see move exotics? For every value of eta, the leverage is "
            "recomputed so that Gyöngy's condition holds: each setting is a different model with the same "
            "marginals. <bookmark mark='a'/> At eta zero there is no vol of vol, and the model is local volatility. "
            "<bookmark mark='b'/> A future smile's skew comes from the covariance between price and volatility at "
            "that future date, which, by chapter two's argument, scales with the vol of vol the model keeps. "
            "<bookmark mark='c'/> So to first order, anything that bets on future smiles, a forward start, a cliquet, "
            "moves monotonically with eta. Pause and predict: which is most sensitive to eta, a one-year European "
            "option, a forward-start, or a cliquet? The European, not at all: it is a vanilla. The forward-start "
            "and the cliquet, both."
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

    def desks(self):
        c1 = history_card(2011, r"Clark, \textit{Foreign Exchange Option Pricing}",
                          r"FX desks run local-stochastic volatility for barriers and no-touch options, and choose the "
                          r"mixing between the local and stochastic parts from the prices of those exotics, which are quoted "
                          r"in the interbank market.", color=QC.FIRM, width=5.8)
        c2 = history_card(2012, r"Guyon and Henry-Labord\`ere, \textit{Risk}",
                          r"``Being particular about calibration'': the particle method, so that any mixing fraction can be "
                          r"calibrated to the vanillas in one simulation.", color=QC.IDEA, width=5.8)
        G = VGroup(c1, c2).arrange(RIGHT, buff=0.4, aligned_edge=UP)
        with self.voiceover(
            "So how does a desk set the dial? Not from vanillas: they cannot see it. Foreign-exchange desks, where "
            "this model is widely used, set it from the exotics that are themselves quoted between "
            "banks, barrier and no-touch options, as Iain Clark's textbook describes. <bookmark mark='a'/> The "
            "particle method made that practical: any setting of the dial can be calibrated to the vanillas in a "
            "single simulation. Then the remaining exotics are priced in between. In crypto, with few liquid "
            "exotics, the dial is a modelling choice, and its range is model risk."
            " Next: a different state for the model, forward variance."
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(c2, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
