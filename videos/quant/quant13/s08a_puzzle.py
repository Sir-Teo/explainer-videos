from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, load, pause, real_data, simulated, yr


class Puzzle(VoiceoverScene):
    def construct(self):
        vp = load("vol_puzzle")
        f = load("facts")
        self.card()
        self.history()
        self.rivers(vp, f)
        self.derive()
        self.jensen(vp)
        self.smile(vp)

    def card(self):
        c = chapter_card(15, 'A volatility-index challenge: Bitcoin illustration', r"Can one model price options and options on volatility?",
                         lit=(2008, 2020), part=PART)
        with self.voiceover("""Chapter fifteen. A Bitcoin illustration of a volatility-index calibration challenge."""):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c), run_time=0.35)

    def history(self):
        h0 = history_card(2004, r"Cboe Futures Exchange", r"VIX futures list on 26 March 2004; VIX options on 24 February "
                          r"2006. Volatility becomes a traded asset, with a smile of its own.", color=QC.FIRM, width=4.1)
        h1 = history_card(2008, r"Gatheral, Bachelier Congress",
                          r"A model fitted to S\&P options also predicts VIX options. A diffusion with two variance factors "
                          r"fits both, but only approximately.", color=QC.IDEA, width=4.1)
        h2 = history_card(2020, r"Guyon, \textit{Risk}", 'Guyon (2020): a specific nonparametric discrete-time joint-calibration construction. Common continuous models exhibit a skew/index-volatility tension.', color=QC.IDEA, width=4.1)
        G = VGroup(h0, h1, h2).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        if G.width > 13.2:
            G.scale_to_fit_width(13.2)
        c4 = label(r"Cont and Kokholm (2013): jumps in both the index and its variance decouple the two smiles",
                   font_size=20, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            (
            """VIX futures began trading in 2004 and VIX options in 2006. A model for S&P prices must also predict the distribution of its future volatility index. <bookmark mark='a'/> Gatheral examined joint fitting with two variance factors in 2008. <bookmark mark='b'/> Guyon's 2020 work describes the tension in common continuous models between steep short SPX skew and high implied volatility of VIX options, and supplies a particular nonparametric discrete-time construction. Jumps and other richer dynamics offer further approaches. The Bitcoin exercise here compares a fitted model index with historical DVOL. We do not have a Bitcoin volatility-option surface in this calculation, so this is an illustration, not a measured joint-calibration test."""
        )
        ) as vo:
            self.play(FadeIn(h0, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(h1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(h2, shift=UP * 0.2), FadeIn(c4))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def rivers(self, vp, f):
        h = vp["models"]["Heston"]
        path = np.asarray(h["path"])
        td = yr(f["dvol_t"])
        dv = np.asarray(f["dvol"])
        n = min(len(path), len(dv))
        t0 = td[-n:]
        g = axes([t0[0], t0[-1]], [0.2, 1.6], x_length=8.0, y_length=4.2, ylabel=r"30-day volatility index",
                 xticks=[2022, 2023, 2024, 2025], yticks=[0.4, 0.8, 1.2, 1.6], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=15).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ld = curve(g.ax, t0, np.clip(dv[-n:], 0.2, 1.6), IV, stroke_width=2)
        lm = curve(g.ax, t0, np.clip(path[:n], 0.2, 1.6), MODEL_COL["Heston"], stroke_width=2)
        leg = legend([(IV, r"DVOL, the real index"), (MODEL_COL["Heston"], r"the fitted Heston's own index, simulated")],
                     font_size=17).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        E = np.asarray(vp["edges"])
        x = 0.5 * (E[1:] + E[:-1])
        hg = axes([-0.4, 0.4], [0, 0.25], x_length=3.6, y_length=2.6, xlabel=r"daily change in log index",
                  xticks=[-0.3, 0, 0.3], yticks=[], font_size=13).to_edge(RIGHT, buff=0.5).shift(UP * 0.9)

        def hist(vals, col):
            return VGroup(*[Rectangle(width=abs(hg.ax.c2p(E[1], 0)[0] - hg.ax.c2p(E[0], 0)[0]) * 0.9,
                                      height=max(abs(hg.ax.c2p(0, min(p, 0.25))[1] - hg.ax.c2p(0, 0)[1]), 1e-3),
                                      stroke_width=0, fill_color=col, fill_opacity=0.55).move_to(hg.ax.c2p(a, min(p, 0.25) / 2))
                            for a, p in zip(x, vals)])

        hd, hm = hist(vp["dvol_hist"], IV), hist(h["hist"], MODEL_COL["Heston"])
        nums = VGroup(MathTex(rf"\text{{DVOL: vol of vol}}\ {100 * vp['dvol_volvol']:.0f}\%,\ \rho = {vp['dvol_corr']:+.2f}",
                              font_size=24, color=IV),
                      MathTex(rf"\text{{Heston's index:}}\ {100 * h['volvol_median']:.0f}\%,\ \rho = {h['corr_median']:+.2f}",
                              font_size=24, color=MODEL_COL["Heston"])).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        nums.next_to(hg, DOWN, buff=0.5).align_to(hg, LEFT)
        src = simulated(r"the fitted Heston simulated for four years, 200 paths, its index $\sqrt{\mathrm{VIX}^2(v_t)}$; "
                        r"DVOL 2021--2025", corner=DL)
        r_ = vp["ratio"]
        with self.voiceover(
            (
            f"""The fitted Heston implies a thirty-day index from expected future variance. Compare a four-year pricing-measure simulation with observed DVOL. <bookmark mark='a'/> Its floor and variability depend on this calibration. These are independent paths aligned for illustration, not historical path predictions. <bookmark mark='b'/> The simulated median log-index vol of vol is {100 * h['volvol_median']:.0f} percent, versus {100 * vp['dvol_volvol']:.0f} historically, a ratio of {r_:.1f}. Correlations are {h['corr_median']:+.2f} and {vp['dvol_corr']:+.2f}. The two hundred simulated paths describe sampling dispersion under Q. Differences from P history also involve drift, state occupancy and index construction; they cannot by themselves establish a failure to price Bitcoin volatility options."""
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg[0]), Create(ld), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(leg[1]), Create(lm), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(hg), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in hd], lag_ratio=0.02),
                      LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in hm], lag_ratio=0.02), FadeIn(nums), run_time=2.5)
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def derive(self):
        rows = [cmath(r"\mathrm{VIX}^2_T", r"=", r"\mathbb{E}_T\Big[\tfrac1\tau\!\int_T^{T+\tau}\! v_s\,ds\Big] = \theta + (v_T - "
                      r"\theta)\,\frac{1 - e^{-\kappa\tau}}{\kappa\tau}", font_size=32, colors={r"\mathrm{VIX}^2_T": IV}),
                cmath(r"\mathbb{E}\big[\mathrm{VIX}_T\big]", r"\le", r"\sqrt{\mathbb{E}\big[\mathrm{VIX}^2_T\big]}", font_size=36,
                      colors={r"\mathbb{E}\big[\mathrm{VIX}_T\big]": IV}),
                cmath(r"\sqrt{\mathbb{E}\big[\mathrm{VIX}^2_T\big]} - \mathbb{E}\big[\mathrm{VIX}_T\big]", r"\approx",
                      r"\frac{\operatorname{Var}\big(\mathrm{VIX}_T\big)}{2\,\mathbb{E}\big[\mathrm{VIX}_T\big]}", font_size=34,
                      colors={r"\sqrt{\mathbb{E}\big[\mathrm{VIX}^2_T\big]} - \mathbb{E}\big[\mathrm{VIX}_T\big]": BAD}),
                cmath(r"dQ/dP", r":", r"d\langle X\rangle_t = a(X_t,t)\,dt\quad (P\text{ and }Q)",
                      font_size=34, colors={r"dQ/dP": VAR})]
        whys = [why(r"Heston is affine: integrate its forward variance curve (chapter 13) over the next $\tau$ = 30 days", 20),
                why('Jensen under the same $Q$, index definition, reset date and forward variance window.', 20),
                why(r"the gap is the variance of the index: VIX futures and options price the vol of vol directly", 20),
                why('Girsanov preserves conditional instantaneous diffusion at a state, not unconditional daily or stationary statistics.', 20)]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.8, buff=0.6, edge=6.9)
        with self.voiceover(
            (
            """Heston's squared model index is its thirty-day forward variance averaged over the index window. <bookmark mark='a'/> Jensen bounds the Q expectation of the index by the square root of the Q expectation of its square, using the same date, window and index definition. This is a matched forward-variance comparison, not any spot-start variance swap. <bookmark mark='b'/> For small dispersion, the gap is approximately index variance over twice its mean. <bookmark mark='c'/> An equivalent Girsanov measure change preserves conditional instantaneous quadratic variation at the same state; it changes drifts. It need not preserve unconditional daily return variance, the stationary state distribution, or statistics of a filtered index. A historical check therefore needs a specified P model and comparable observations."""
        )
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def jensen(self, vp):
        h = vp["models"]["Heston"]
        q = np.sort(np.asarray(h["vix2_q"]))
        s = h["smiles"]["30"]
        g = axes([0, 2.0], [0, 1.45], x_length=6.4, y_length=4.2, xlabel=r"$\mathrm{VIX}^2$ in 30 days (variance)",
                 ylabel=r"$\mathrm{VIX}$ (volatility)", xticks=[0, 0.5, 1.0, 1.5, 2.0], yticks=[0, 0.5, 1.0],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15).to_edge(LEFT, buff=0.7)
        ax = g.ax
        xs = np.linspace(0, 2.0, 200)
        sq = curve(ax, xs, np.sqrt(xs), WHITE, stroke_width=3)
        qq = q[q <= 2.0][::8]
        rug = VGroup(*[Line(ax.c2p(v, 0), ax.c2p(v, 0.06), color=VAR, stroke_width=2) for v in qq])
        m2 = float(np.mean(q))
        fut, vs = s["future"], s["var_swap_vol"]
        chord = DashedLine(ax.c2p(m2, 0), ax.c2p(m2, vs), stroke_color=IV, stroke_width=2)
        p1 = Dot(ax.c2p(m2, vs), color=IV)
        p2 = Dot(ax.c2p(m2, fut), color=BAD)
        side = VGroup(
            MathTex(rf"\sqrt{{\mathbb{{E}}[\mathrm{{VIX}}^2]}} = {100 * vs:.1f}\%", font_size=30, color=IV),
            MathTex(rf"\mathbb{{E}}[\mathrm{{VIX}}] = {100 * fut:.1f}\%", font_size=30, color=BAD),
            MathTex(rf"\text{{floor}}\ \sqrt{{\theta(1 - b)}} = {100 * h['floor']:.1f}\%", font_size=28, color=GREY_A),
            wrapped_label(r"purple ticks: the law of $\mathrm{VIX}^2$ in 30 days under the fitted model; the wider it is, "
                          r"the further the future falls below the variance-swap vol", 4.2, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            (
            f"""Draw the square root against the model's squared index in thirty days. <bookmark mark='a'/> For the matching Q distribution, root mean square is {100 * vs:.1f} percent and the index future is {100 * fut:.1f}. <bookmark mark='b'/> This Heston fit also has an index floor near {100 * h['floor']:.0f} percent. The Jensen upper bound applies to the matching forward window and index definition. Comparing a differently timed swap, a different index, or market quotes with frictions is a different question."""
        )
        ) as vo:
            self.play(FadeIn(g), Create(sq), LaggedStart(*[FadeIn(r_) for r_ in rug], lag_ratio=0.02), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(chord), FadeIn(p1), FadeIn(p2), FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def smile(self, vp):
        H, B = vp["models"]["Heston"], vp["models"]["Bates"]
        g = axes([0.75, 1.55], [0.3, 1.6], x_length=6.4, y_length=4.2, xlabel=r"strike $/$ the index future",
                 ylabel=r"implied vol of options on the index", xticks=[0.8, 1.0, 1.2, 1.4], yticks=[0.4, 0.8, 1.2, 1.6],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15).to_edge(LEFT, buff=0.7)
        ax = g.ax

        def ln(d, col, sw=3):
            return VGroup(curve(ax, d["m"], np.clip(d["iv"], 0.3, 1.6), col, stroke_width=sw),
                          *[Dot(ax.c2p(a, min(b, 1.6)), radius=0.05, color=col) for a, b in zip(d["m"], d["iv"])])

        h30, h90, b30 = ln(H["smiles"]["30"], MODEL_COL["Heston"]), ln(H["smiles"]["90"], IV), ln(B["smiles"]["30"], MODEL_COL["Bates"])
        leg = legend([(MODEL_COL["Heston"], r"Heston, 30 days"), (IV, r"Heston, 90 days"), (MODEL_COL["Bates"], r"Bates, 30 days")],
                     font_size=17).next_to(g, UP, buff=0.12).align_to(g, LEFT)
        a30 = H["smiles"]["30"]["iv"][2]
        a90 = H["smiles"]["90"]["iv"][2]
        side = VGroup(
            MathTex(rf"\text{{ATM, 30 days:}}\ {100 * a30:.0f}\%", font_size=30, color=MODEL_COL["Heston"]),
            MathTex(rf"\text{{ATM, 90 days:}}\ {100 * a90:.0f}\%", font_size=30, color=IV),
            MathTex(rf"\text{{Bates:}}\ {100 * B['volvol_median']:.0f}\%\ \text{{vol of vol}}", font_size=28,
                    color=MODEL_COL["Bates"]),
            MathTex(rf"\text{{DVOL realized:}}\ {100 * vp['dvol_volvol']:.0f}\%", font_size=28, color=WHITE),
            wrapped_label('Model-index predictions under $Q$; no observed Bitcoin index-option quotes or joint calibration test here.', 4.4, 17, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        verdict = (f"Bates, with its jumps, does no better: its index has a vol of vol of {100 * B['volvol_median']:.0f} "
                   "percent, because its diffusion part had to fit the same skew." if B["volvol_median"] > 1.5 * vp["dvol_volvol"]
                   else f"Bates's jumps relieve the diffusion: its index has a vol of vol of {100 * B['volvol_median']:.0f} "
                   "percent, closer to DVOL's.")
        src = simulated(r"options on the fitted Heston's 30-day index, priced by quadrature over the law of $v_T$")
        with self.voiceover(
            (
            f"""Model-index option ATM implied volatility is {100 * a30:.0f} percent at thirty days and {100 * a90:.0f} at ninety, with an upward smile on this grid. <bookmark mark='a'/> Bates's simulated index vol of vol is {100 * B['volvol_median']:.0f} percent under this fit. These are calibration-specific predictions. <bookmark mark='b'/> There are no observed Bitcoin index-option prices here to compare them with. Nor does Girsanov make these Q simulations directly comparable to unconditional P statistics. The exercise motivates a joint market test and explicit P dynamics; it does not estimate a volatility risk premium. Next, calibration stability."""
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg[0]), Create(h30[0]), FadeIn(h30[1:]), FadeIn(side[0]))
            self.play(FadeIn(leg[1]), Create(h90[0]), FadeIn(h90[1:]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(FadeIn(leg[2]), Create(b30[0]), FadeIn(b30[1:]), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)
