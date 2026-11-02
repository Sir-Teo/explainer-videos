from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import (BAD, IV, LV, OPT, PART, RV, SPOT, axes3, fixed, grid_fn, illustration, load,
                                         real_data, surf3)

KG = np.linspace(-0.4, 0.4, 17)
TG = np.array([7, 14, 30, 60, 90, 180]) / 365


class Learning(VoiceoverScene, ThreeDScene):
    def construct(self):
        v = load("vae")
        n = load("neural_surface")
        self.card()
        self.vae_replay(v)
        self.latent(v)
        self.walk(v)
        self.derive()
        self.net_replay(n)
        self.compare(n)

    def card(self):
        c = chapter_card(17, r"Learning surfaces", r"Can a network learn what a surface may look like?", part=PART)
        with self.voiceover("Chapter seventeen. Learning surfaces."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def vae_replay(self, v):
        L = np.asarray(v["losses"])
        steps = np.asarray(v["ck_steps"])
        ck = np.asarray(v["ck_show"])
        true = np.asarray(v["show_true"]).reshape(len(TG), len(KG))
        rows, cols = (0, 2, 5), (BAD, IV, LV)
        pick = [0, 1, 2, 4, 8, 15, len(steps) - 1]

        def frame(i):
            g = axes([-0.4, 0.4], [0.3, 1.6], x_length=5.0, y_length=3.4, xlabel=r"log-moneyness", ylabel=r"implied vol",
                     xticks=[-0.4, 0, 0.4], yticks=[0.5, 1.0, 1.5], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15)
            rec = ck[pick[i]].reshape(len(TG), len(KG))
            out = VGroup(g)
            for r, c in zip(rows, cols):
                out.add(VGroup(*[Dot(g.ax.c2p(a, float(np.clip(b, 0.3, 1.6))), radius=0.03, color=c) for a, b in
                                 zip(KG, true[r])]))
                out.add(curve(g.ax, KG, np.clip(rec[r], 0.3, 1.6), c, stroke_width=3))
            return out
        rp = TrainingReplay(steps, L, frame, [int(steps[p]) for p in pick], ylabel=r"reconstruction RMSE (vol points)")
        leg = legend([(BAD, r"7 days"), (IV, r"30 days"), (LV, r"180 days")], font_size=16).to_corner(UL, buff=0.35)
        head = label(rf"the week of {v['show_day']} (FTX), rebuilt from two numbers; dots: its surface", font_size=19,
                     color=GREY_A).to_edge(UP, buff=0.3).shift(RIGHT * 1.5)
        src = real_data(rf"{v['n']} weekly surfaces, 2021--2025; five seeds (band); trained here on a CPU")
        r0 = v["recon_rmse_volpts"]
        rs = v["recon_seeds"]
        pc = v["pca2_rmse"]
        with self.voiceover(
            "Can a network find its own coordinates? A variational autoencoder squeezes each week's surface, a "
            "hundred and two volatilities, through two numbers and rebuilds it. Here it trains on every week since "
            "April 2021: left, the week FTX collapsed, rebuilt at each checkpoint; right, the error, five seeds as a "
            "band. <bookmark mark='a'/> At first the rebuilt smiles are a "
            "blur near the average; within a few hundred steps they find the level, and then the shape. "
            f"<bookmark mark='b'/> After three thousand steps the error is {r0:.1f} volatility points, and the five "
            f"seeds agree to within {max(rs) - min(rs):.2f}. The fair baseline, two principal components of the same "
            f"grids, the best linear two-number summary, gets {pc:.1f}."
        ) as vo:
            self.play(FadeIn(rp), FadeIn(leg), FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            rp.play(self, run_time=10)
            vo.wait_until("b")
        self.wait(0.4)
        self.clear_scene()

    def latent(self, v):
        z = np.asarray(v["latent"])
        atm = np.asarray(v["atm"])
        lev = int(np.argmax(np.abs(v["corr_atm"])))
        oth = 1 - lev
        g = axes([-3, 3], [-3, 3], x_length=4.8, y_length=4.8, xlabel=r"$z_1$", ylabel=r"$z_2$", xticks=[-2, 0, 2],
                 yticks=[-2, 0, 2], font_size=17).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        lo, hi = atm.min(), atm.max()
        dots = VGroup(*[Dot(g.ax.c2p(*np.clip(p, -3, 3)), radius=0.05,
                            color=interpolate_color(ManimColor(QC.SPOT), ManimColor(BAD), float((a - lo) / (hi - lo))))
                        for p, a in zip(z, atm)])
        cbar = label(rf"colour: 30-day ATM vol, {100 * lo:.0f}\% (blue) to {100 * hi:.0f}\% (red)", font_size=17,
                     color=GREY_B).next_to(g, DOWN, buff=0.15)
        side = VGroup(
            wrapped_label(r"each dot is one week; the network was never told the at-the-money level or the skew", 4.6,
                          20, GREY_A),
            MathTex(rf"\text{{corr}}(z_{lev + 1}, \text{{ATM level}}) = {v['corr_atm'][lev]:+.2f}", font_size=30, color=IV),
            MathTex(rf"\text{{corr}}(z_{oth + 1}, \text{{skew}}) = {v['corr_skew'][oth]:+.2f}", font_size=30, color=BAD),
            wrapped_label(r"Bergeron, Fung, Hull and Poulos (2022) did this for currency and equity surfaces", 4.6, 19,
                          GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = real_data(r"weekly surfaces, 2021--2025")
        ca, cs = v["corr_atm"][lev], v["corr_skew"][oth]
        with self.voiceover(
            "Where did each week land in the two-number space? Every dot is a week, coloured by its at-the-money "
            "volatility, from blue to red. <bookmark mark='a'/> The colours sort themselves along one direction. The "
            "network was never told what a level is, but one of its two numbers tracks at-the-money volatility with a "
            f"correlation of {ca:+.2f}. The other carries part of the skew: {cs:+.2f}. Maxime Bergeron, Nicholas Fung, "
            "John Hull and Zissis Poulos showed the same for currency and equity surfaces in 2022."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]))
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.004, run_time=2.5), FadeIn(cbar))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def walk(self, v):
        lev = int(np.argmax(np.abs(v["corr_atm"])))
        W = np.asarray(v["walk"][f"z{lev + 1}"])  # (5, 6, 17)
        W2 = np.asarray(v["walk"][f"z{2 - lev}"])
        ax = axes3([-0.4, 0.4, 0.2], [0, 0.5, 0.1], [0.2, 1.4, 0.2], x_length=7.0, y_length=4.6, z_length=3.0)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-58 * DEGREES, zoom=0.85)

        def s(grid):
            return surf3(ax, grid_fn(KG, TG, grid), (-0.4, 0.4), (TG[0], TG[-1]), 0.2, 1.4, resolution=(18, 10))
        cur = s(W[2])
        t1 = label(rf"walk $z_{lev + 1}$ from $-2$ to $+2$: the whole surface lifts", font_size=22, color=IV).to_corner(UL, buff=0.35)
        t2 = label(rf"walk $z_{2 - lev}$: the shape changes instead", font_size=22, color=BAD).to_corner(UL, buff=0.35)
        foot = label(r"surfaces that never happened, but could have: scenarios for risk (Part 40)", font_size=20,
                     color=GREY_A).to_edge(DOWN, buff=0.3)
        fixed(self, t1, t2, foot)
        with self.voiceover(
            "Now walk through the space the network learned, decoding each point back into a surface. Move the level "
            "number from minus two to plus two, and the whole surface rises: a calm market becomes a frightened one. "
            "<bookmark mark='a'/> Move the other number, and the shape changes instead of the height. "
            "<bookmark mark='b'/> These are surfaces that never happened but could have: scenarios for risk "
            "management, and a smooth way to fill in missing quotes. One caution: the network knows nothing about "
            "arbitrage unless it is taught."
        ) as vo:
            self.play(Create(ax), FadeIn(cur), FadeIn(t1))
            for i in (0, 4, 2):
                self.play(Transform(cur, s(W[i])), run_time=1.6)
            vo.wait_until("a")
            self.play(FadeOut(t1), FadeIn(t2))
            for i in (0, 4, 2):
                self.play(Transform(cur, s(W2[i])), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, cur)), FadeOut(t2), FadeOut(foot)],
                         run_time=1)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\text{ELBO}", r"=", r"\mathbb{E}_q[\ln p(x \mid z)] - \text{KL}\big(q(z \mid x)\,\|\,N(0, I)\big)",
                      font_size=36, colors={r"\text{ELBO}": LV}),
                cmath(r"w_\theta(k, T)", r"=", r"T\cdot\text{softplus}\big(\text{net}_\theta(k, \sqrt T)\big)", font_size=38,
                      colors={r"w_\theta(k, T)": IV}),
                cmath(r"\mathcal{L}(\theta)", r"=", r"\sum_i(\hat\sigma_i - \sigma_i)^2 + \lambda\Big[\overline{(-g)^+} + "
                      r"\overline{(-\partial_T w)^+}\Big]", font_size=36, colors={r"\mathcal{L}(\theta)": OPT})]
        whys = [why(r"the autoencoder's objective: rebuild well, keep the code close to a standard normal (AI, Built)"),
                why(r"a small network for total variance, positive by construction; derivatives in $k$ and $T$ by "
                    r"automatic differentiation"),
                why(r"Ackerer, Tagasovska and Vatter (2020): fit the quotes, and penalize Chapter 3's two conditions on a "
                    r"grid of points where there are no quotes")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "The autoencoder maximizes the evidence lower bound: rebuild well, keep the codes near a standard normal. "
            "<bookmark mark='a'/> Teaching arbitrage is the second idea. Let a small network be the total variance "
            "itself, its derivatives from automatic differentiation. <bookmark mark='b'/> Then add Chapter three's two "
            "conditions as penalties on a grid of points with no quotes at all: the recipe of Ackerer, Tagasovska and "
            "Vatter, from 2020."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def net_replay(self, n):
        R = n["runs"]
        pen = [R[f"{s}_1"] for s in range(3)]
        r0 = R["0_1"]
        steps = np.asarray(r0["step"])
        loss = np.array([np.asarray(p["test"]) for p in pen])
        surf = np.asarray(r0["surf"])  # (checkpoints, nT, nk)
        flags = np.asarray(r0["g_flags"])
        gk, gT = np.asarray(n["gk"]), np.asarray(n["gT"])
        ck_k, ck_T = np.asarray(n["colloc_k"]), np.asarray(n["colloc_T"])
        k, T, iv = np.asarray(n["k"]), np.asarray(n["T"]), np.asarray(n["iv"])
        pick = [0, 1, 2, 4, 8, 15, len(steps) - 1]
        j30 = int(np.argmin(np.abs(gT - 30 / 365)))
        j90 = int(np.argmin(np.abs(gT - 0.25)))
        m30 = np.abs(T - gT[j30]) < 12 / 365
        m90 = np.abs(T - gT[j90]) < 20 / 365

        def frame(i):
            c = pick[i]
            g = axes([-0.6, 0.6], [0.3, 0.9], x_length=4.2, y_length=2.4, ylabel=r"implied vol", xticks=[-0.5, 0, 0.5],
                     yticks=[0.4, 0.6, 0.8], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=13)
            out = VGroup(g)
            for m_, j, col in ((m30, j30, IV), (m90, j90, LV)):
                out.add(VGroup(*[Dot(g.ax.c2p(a, float(np.clip(b, 0.3, 0.9))), radius=0.025, color=col)
                                 for a, b in zip(k[m_], iv[m_]) if abs(a) <= 0.6]))
                out.add(curve(g.ax, gk, np.clip(surf[c, j], 0.3, 0.9), col, stroke_width=3))
            h = axes([-1, 1], [0, 0.8], x_length=4.2, y_length=1.6, xlabel=r"collocation grid: $k$ across, $T$ up",
                     xticks=[], yticks=[], font_size=12)
            bad = flags[c].astype(bool)
            pts = VGroup(*[Dot(h.ax.c2p(a, b), radius=0.022, color=BAD if f else GREY_D) for a, b, f in
                           zip(ck_k[::2], ck_T[::2], bad[::2])])
            return VGroup(out, VGroup(h, pts)).arrange(DOWN, buff=0.3)
        rp = TrainingReplay(steps, loss, frame, [int(steps[p]) for p in pick], ylabel=r"held-out RMSE (vol points)")
        head = label(r"the penalized network on the Surface: 30 and 90 days, and where $g < 0$ (red)", font_size=19,
                     color=GREY_A).to_edge(UP, buff=0.2)
        src = real_data(r"the Surface, 80\% of quotes to train, 20\% held out; three seeds (band)")
        g0 = float(r0["g_neg"][0])
        with self.voiceover(
            "Watch it train on the Surface. Eighty percent of the quotes train it, twenty percent are held out. Left, "
            "its thirty and ninety day smiles against the quotes, and below them the collocation grid, red wherever g "
            f"is negative. At the start {100 * g0:.0f} percent of the grid is red. <bookmark mark='a'/> The smiles bend "
            "toward the quotes; the red points go dark one by one as the penalty bites. On the right, the error on the "
            "held-out quotes, three seeds as a band."
        ) as vo:
            self.play(FadeIn(rp), FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            rp.play(self, run_time=11)
        self.wait(0.4)
        self.clear_scene()

    def compare(self, n):
        pt, rt, st = (np.asarray(n[x]) for x in ("pen_test", "raw_test", "ssvi_test"))
        pg, rg = np.asarray(n["pen_g"]), np.asarray(n["raw_g"])
        pc, rc = np.asarray(n["pen_cal"]), np.asarray(n["raw_cal"])
        tab = VGroup(
            label(r"held-out RMSE (vol points), three splits \quad butterfly violations \quad calendar violations",
                  font_size=20, color=GREY_A),
            label(rf"penalized network: {pt[0]:.2f}, {pt[1]:.2f}, {pt[2]:.2f} \quad {100 * pg.max():.1f}\% \quad "
                  rf"{100 * pc.max():.1f}\%", font_size=24, color=IV),
            label(rf"same network, no penalty: {rt[0]:.2f}, {rt[1]:.2f}, {rt[2]:.2f} \quad {100 * rg.mean():.1f}\% \quad "
                  rf"{100 * rc.mean():.1f}\%", font_size=24, color=BAD),
            label(rf"SSVI on the same splits: {st[0]:.2f}, {st[1]:.2f}, {st[2]:.2f} \quad 0 by construction", font_size=24,
                  color=LV),
            label(rf"vega-weighted, network against SSVI: {np.mean(n['pen_test_vw']):.2f} against "
                  rf"{np.mean(n['ssvi_test_vw']):.2f}", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.9)
        note_ = label(r"violations: share of a $201 \times 60$ grid ($|k| \le 1$, 3 days to 0.8 years) with $g < 0$ or "
                      r"$\partial_T w < 0$; unweighted RMSE", font_size=17, color=GREY_B).next_to(tab, DOWN, buff=0.3)
        wins = bool(np.mean(pt) < np.mean(st))
        verdict = (r"the network beats SSVI out of sample here, at the cost of a closed form, provable extrapolation and "
                   r"speed" if wins else r"SSVI is as good or better out of sample here, and it comes with proofs")
        foot = VGroup(wrapped_label(verdict, 11.6, 21, QC.HOUSE),
                      wrapped_label(r"pause and predict: the network fits better. Why might a desk still quote SSVI?", 11.6,
                                    21, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.6)
        a, b, c = float(np.mean(pt)), float(np.mean(rt)), float(np.mean(st))
        rgm = 100 * float(np.mean(rg))
        branch = ("So the penalized network beats SSVI on quotes it never saw. " if wins else
                  "So SSVI holds its own on quotes it never saw. ")
        pv, sv = float(np.mean(n["pen_test_vw"])), float(np.mean(n["ssvi_test_vw"]))
        branch2 = ("Weighted by vega, as a desk would weigh them, the network still wins. " if pv < sv else
                   "But weight the errors by vega, as a desk would, and the order flips: SSVI wins, because the "
                   "network's gains are in the far wings, where options are cheap. ")
        with self.voiceover(
            f"The scores. On held-out quotes the penalized network misses by {a:.2f} volatility points on average over "
            f"three splits, and has no arbitrage anywhere on a fine grid. The same network without the penalty fits "
            f"the held-out quotes better, {b:.2f}, but {rgm:.0f} percent of the grid has a negative density: it buys "
            "accuracy with arbitrage. SSVI, refitted on the same training quotes, misses by "
            f"{c:.2f}. {branch}<bookmark mark='a'/> {branch2}Pause and predict: if the network fits better, why might a "
            "desk still quote SSVI? Because SSVI extrapolates with a guarantee, fits in milliseconds, moves smoothly "
            "from one day to the next, and its parameters mean something to a trader."
            " Next: who builds surfaces, and who sells them."
        ) as vo:
            self.play(FadeIn(tab), FadeIn(note_))
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
