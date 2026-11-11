from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import axes, data_range
from explainer.quant.house import deep as D
from videos.quant.quant17.common import (BAD, DELTA, GOOD, NET, OPT, PART, REF, ask, grid_fn, house_lab, illustration,
                                         load, surf3d_axes, flat_camera)

CK = ["0", "20", "40", "80", "120", "200"]


class HLP(VoiceoverScene, ThreeDScene):
    def construct(self):
        h = load("hlp")
        r = load("hlp_replay")
        self.card()
        self.idea(h)
        self.replay(r)
        self.surface(r)
        self.lab(r)
        self.hedge(h, r)

    def card(self):
        c = chapter_card(1, r"Learning a pricing formula", r"Can a network learn Black--Scholes from prices alone?",
                         lit=(1994,), part=PART)
        with self.voiceover("Chapter one. Learning a pricing formula."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def idea(self, h):
        rows = [cmath(r"C(S, K, \tau)", r"=", r"K\,c\!\left(\tfrac{S}{K},\ \tau\right)", font_size=40,
                      colors={r"C(S, K, \tau)": OPT}),
                cmath(r"\sup_{x \in \mathcal{K}}\big|c(x) - \hat c_\theta(x)\big|", r"<", r"\varepsilon", font_size=38,
                      colors={r"<": WHITE}),
                cmath(r"\hat\Delta", r"=", r"\partial_S\big(K \hat c_\theta(S/K, \tau)\big) = \partial_1 \hat c_\theta",
                      font_size=38, colors={r"\hat\Delta": NET}),
                cmath(r"e", r"=", r"\hat C_0 + \textstyle\sum_k \hat\Delta_k\,(S_{k+1} - S_k) - (S_T - K)^+", font_size=36,
                      colors={r"e": BAD})]
        whys = [why(r"Hutchinson, Lo and Poggio (1994): geometric Brownian motion scales, so multiplying the price and the "
                    r"strike by $\lambda$ multiplies the call by $\lambda$ (Merton's homogeneity): fixed volatility, rates and dividends here; positive strike; two varying inputs"),
                why(r"the universal approximation theorem (Cybenko 1989; Hornik 1991): one hidden layer, wide enough, "
                    r"approximates any continuous function on a compact set $\mathcal{K}$, under the usual continuity and non-polynomial-activation conditions. It says a network exists, not that training finds it, nor how many prices it needs"),
                why(r"autograd differentiates the fitted function; accurate values alone do not guarantee accurate Greeks"),
                why(r"and the test is the hedge, not the fit: the tracking error of a daily rebalanced hedge, which even "
                    r"the true delta cannot drive to zero (Part 10: its spread falls like one over the square root of "
                    r"the number of rebalances)")]
        step = ladder(self, rows, whys, keep=3, top=3.2, x=-0.6, buff=0.42, edge=6.9)
        n = h["n_train"]
        with self.voiceover(
            f"Hutchinson, Lo and Poggio asked whether a network could learn an option price. In this modern illustration volatility, rates and dividends are fixed. For positive strike, homogeneity reduces the varying inputs to moneyness and maturity. <bookmark mark='a'/> A universal approximation theorem gives existence on a compact set under activation conditions. It does not guarantee successful optimization, finite sample accuracy, or accurate derivatives. <bookmark mark='b'/> Differentiate the fitted network to obtain a candidate delta; that operation still costs work. <bookmark mark='c'/> Then test it. Even the true delta leaves discrete hedging error. The saved training set contains {n:,} Black–Scholes-labelled prices from ten simulated two-year paths, with overlapping options; these are not independent market observations or a literal replication of the original paper."
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

    def replay(self, r):
        seeds = [r["seeds"][s] for s in ("0", "1", "2")]
        ep = np.array([c[0] for c in seeds[0]["curve"]])
        L = np.array([[c[1] * 100 for c in s["curve"]] for s in seeds])  # (10 C/K)^2 -> (100 C/K)^2, in (% of K)^2
        xs = np.asarray(r["xs"])
        bsl = np.asarray(r["bs_slice"])

        yr = data_range(bsl, *[seeds[0]["snaps"][k] for k in CK], zero=True)

        def frame(i):
            g = axes([0.8, 1.2], yr, x_length=5.0, y_length=3.6, xlabel=r"moneyness $S/K$",
                     ylabel=r"$C/K$, six weeks to expiry", xticks=[0.8, 1.0, 1.2], yticks=[0, 0.1, 0.2], font_size=14)
            y = np.asarray(seeds[0]["snaps"][CK[i]])
            err = float(np.max(np.abs(np.asarray(seeds[0]["snaps"][CK[i]]) - bsl))) * 100
            return VGroup(g, DashedVMobject(curve(g.ax, xs, bsl, REF, stroke_width=2.5), num_dashes=36),
                          curve(g.ax, xs, y, NET, stroke_width=4),
                          label(rf"epoch {CK[i]}: largest error {err:.2f}\% of the strike", font_size=18,
                                color=NET).next_to(g, DOWN, buff=0.15))
        rp = TrainingReplay(ep, L, frame, checkpoints=[1, 20, 40, 80, 120, 200], ylabel=r"squared error, $(\%K)^2$",
                            xlabel=r"epoch", log_y=True)
        fin = [float(np.sqrt(s["curve"][-1][1]) * 10) for s in seeds]
        leg = legend([(REF, r"Black--Scholes, never shown to the network"), (NET, r"the network (seed 0)"),
                      (QC.Q, r"min--max of three seeds, not a confidence interval")], font_size=16).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is the training. On the right, the error over the sixty-six thousand prices, epoch by epoch, for "
            "three networks started from different random weights: the band is their spread. On the left, what the "
            "first network believes the call is worth six weeks before expiry, against the formula it never saw. "
            "<bookmark mark='a'/> At first it is a flat guess. Within twenty passes it has the hockey stick's bend; by "
            f"the end the three seeds sit at a root-mean-square error of {min(fin):.2f} to {max(fin):.2f} percent of the "
            "strike, and the curve lies on the formula."
        ) as vo:
            self.play(FadeIn(rp), FadeIn(leg))
            vo.wait_until("a")
            rp.play(self, run_time=max(vo.remaining(0.5), 4))
        self.wait(0.4)
        self.clear_scene()

    def surface(self, r):
        s0 = r["seeds"]["0"]
        gx, gT = np.asarray(r["grid_x"]), np.asarray(r["grid_T"])
        Z, E = np.asarray(s0["surf"]), np.asarray(s0["surf_err"]) * 100
        f, fe = grid_fn(gx, gT, Z), grid_fn(gx, gT, E)
        ax = surf3d_axes([0.8, 1.2, 0.1], [0, 0.25, 0.05], [*data_range(Z, zero=True), 0.05]).shift(DOWN * 0.6 + RIGHT * 1.2)  # clear of the key
        surf = Surface(lambda u, v: ax.c2p(u, v, f(u, v)), u_range=(0.8, 1.2), v_range=(gT[0], 0.25),
                       resolution=(30, 20), fill_opacity=0.9, stroke_width=0.3, stroke_color="#0E1117",
                       checkerboard_colors=False)
        thr = 0.1
        for face in surf:
            u, v, _ = ax.p2c(face.get_center())
            e = abs(fe(u, v))
            face.set_fill(interpolate_color(ManimColor("#6366F1"), ManimColor(BAD), min(e / thr, 1.0)), opacity=0.9)
        payoff = VMobject(stroke_color=WHITE, stroke_width=3).set_points_as_corners(
            [ax.c2p(x, gT[0], max(x - 1, 0)) for x in np.linspace(0.8, 1.2, 41)])
        big = float(np.mean(np.abs(E) > thr)) * 100
        worst = float(np.abs(E).max())
        hint = VGroup(label(r"moneyness $S/K$ (across), time to expiry (back), $C/K$ (up)", font_size=20),
                      legend([("#6366F1", r"error below 0.1\% of the strike"), (BAD, r"colour saturates at 0.1\%")],
                             font_size=17),
                      label(rf"{big:.0f}\% of the grid above 0.1\%; worst {worst:.2f}\%", font_size=20, color=GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.35)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-60 * DEGREES, zoom=0.95)
        self.add_fixed_in_frame_mobjects(hint)
        self.remove(hint)
        with self.voiceover(
            "Now the whole function at once: the learned price over moneyness and time to expiry, coloured by its "
            "error. Blue is within a tenth of a percent of the strike. <bookmark mark='a'/> The red is where you would "
            "expect it: the shortest expiries, near the money, where the true price bends sharply into the payoff and "
            f"a smooth network has to bend with it. The worst point is off by {worst:.2f} percent. A desk would see "
            "that red patch as the place not to trust this network, and it is exactly where gamma, the curvature, is "
            "largest."
        ) as vo:
            self.play(Create(ax), Create(payoff), FadeIn(hint[0]))
            self.play(Create(surf), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(hint[1]), FadeIn(hint[2]))
            self.move_camera(theta=-30 * DEGREES, phi=60 * DEGREES, run_time=max(vo.remaining(0.5), 2))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, added_anims=[FadeOut(VGroup(ax, surf, payoff)), FadeOut(hint)],
                         run_time=1.2)
        flat_camera(self)
        self.clear_scene()

    def lab(self, r):
        card = house_lab(r"train a pricing network", D.train_mlp_regressor, "for _ in range(epochs)", 9)
        card.to_edge(UP, buff=0.4).to_edge(LEFT, buff=0.6)
        outs = [f"n_train = {r['n_train']:,}"]
        for s in ("0", "1", "2"):
            q = r["seeds"][s]
            outs.append(f"seed {s}: training rms {10 * np.sqrt(q['curve'][-1][1]):.3f}% of K   at the money "
                        f"{q['slice_err_atm']:.3f}% of K")
        with self.voiceover(
            "An excerpt from the House's training loop: shuffle, batch, measure squared error and step the optimizer. The scheduler lowers the learning rate. <bookmark mark='a'/> Three fixed random starts give three fitted sets of weights; they do not establish a sampling distribution or prove successful optimization."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs)
        self.wait(0.5)
        self.clear_scene()

    def hedge(self, h, r):
        fst = r["seeds"]["0"]["first"]
        S = np.asarray(fst["S"])
        n = len(S) - 1
        t = np.arange(n + 1)
        vn, vb, opt = np.asarray(fst["val_net"]), np.asarray(fst["val_bs"]), np.asarray(fst["opt"])
        lo, hi = float(min(vn.min(), vb.min(), opt.min())) - 0.3, float(max(vn.max(), vb.max(), opt.max())) + 0.3
        g = axes([0, n], [lo, hi], x_length=6.4, y_length=3.8, xlabel=r"trading day", ylabel=r"value",
                 xticks=[0, 21, 42, 63], yticks=[round(v, 1) for v in np.linspace(lo + 0.2, hi - 0.2, 3)],
                 font_size=14).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        tr = ValueTracker(0)

        def upto(y, col, w):
            def f():
                k = max(int(tr.get_value()), 1)
                return curve(ax, t[:k + 1], y[:k + 1], col, stroke_width=w)
            return f
        lines = [always_redraw(upto(opt, OPT, 2.5)), always_redraw(upto(vb, REF, 2.5)), always_redraw(upto(vn, NET, 3.5))]
        leg = legend([(OPT, r"the option (Black--Scholes value)"), (REF, r"hedge portfolio, true delta"),
                      (NET, r"hedge portfolio, the network's delta")], font_size=16).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        rms = [r["seeds"][s]["tracking"] for s in ("0", "1", "2")]
        net_r = [x["net"] for x in rms]
        bs_r = rms[0]["bs"]
        inside = min(net_r) <= bs_r <= max(net_r)
        if inside:
            verdict = "the reference RMS lies inside this three-seed range"
        elif min(net_r) > bs_r:
            verdict = "the networks' errors sit consistently above the true delta's"
        else:
            verdict = "the networks' errors sit consistently below the true delta's"
        side = VGroup(
            label(r"tracking error over 200 fresh options (RMS)", font_size=21),
            MathTex(rf"\text{{true delta}}\ {bs_r:.3f}", font_size=30, color=REF),
            MathTex(rf"\text{{network, three seeds}}\ {min(net_r):.3f}\text{{--}}{max(net_r):.3f}", font_size=30, color=NET),
            wrapped_label(verdict, 4.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            f"Here is a separate evaluation on two hundred fresh simulated options, struck at the money and hedged daily for sixty-three trading days. The plot selects the first saved option; each network and the true delta use the same evaluation paths. <bookmark mark='a'/> Their portfolio values track closely in this example. <bookmark mark='b'/> The true delta has RMS tracking error {bs_r:.3f}; the three training seeds give {min(net_r):.3f} to {max(net_r):.3f}: {verdict}. This range measures three training outcomes on reused paths, not a confidence interval or a significance test. It compares discrete hedges within a fixed Black–Scholes model; it does not establish performance on other models or real markets."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            self.add(*lines)
            self.play(tr.animate.set_value(n), run_time=6, rate_func=linear)
            vo.wait_until("a")
            for m in lines:
                m.clear_updaters()
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in side], lag_ratio=0.4))
        q = ask(r"the network never saw a delta. Will its derivative hedge a short straddle's gamma risk as well? "
                r"Chapter 2 asks which networks can even represent gamma.")
        with self.voiceover(
            "But a network judged on prices is not automatically good at derivatives of prices. Will its second "
            "derivative, the gamma, be right too? That depends on a choice made before training even starts."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
