from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, GOOD, IV, NET, OPT, PART, REF, illustration, load


class Calibrator(VoiceoverScene):
    def construct(self):
        c = load("calib")
        self.card()
        self.idea(c)
        self.training(c)
        self.surface(c)

    def card(self):
        c = chapter_card(2, r"The neural calibrator", r"How do you calibrate a model with no formula, every day?", part=PART)
        with self.voiceover("Chapter two. The neural calibrator."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def idea(self, c):
        rows = [cmath(r"\sigma_{\text{imp}}", r"\approx", r"\mathcal{N}_w\big(H, \eta, \rho, \xi_0, \xi_1;\ T, k\big)",
                      font_size=40, colors={r"\sigma_{\text{imp}}": IV}),
                cmath(r"\hat\theta", r"=", r"\arg\min_\theta \sum_i w_i\,\big(\mathcal{N}_w(\theta; T_i, k_i) - "
                      r"\sigma_i^{\text{mkt}}\big)^2", font_size=36, colors={r"\hat\theta": GOOD})]
        whys = [why(rf"Horvath, Muguruza and Tomas (2021): learn the map from rough Bergomi's parameters and an option's "
                    rf"expiry and moneyness to its implied volatility, offline, from Monte Carlo: here "
                    rf"{c['n_train'] + c['n_held']:,} prices from 12{{,}}000 parameter sets".replace(",", "{,}", 1)),
                why(r"then calibrate online by gradient descent through the network, which is smooth and differentiable: "
                    r"the slow simulation is paid once, not at every step of every calibration")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.6, buff=1.0, edge=6.9)
        with self.voiceover(
            "Part fourteen found that rough Bergomi fits the Surface better than Heston, but it has no formula: "
            "each calibration ran Monte Carlo inside an optimizer, for minutes. Blanka Horvath, Aitor Muguruza and "
            "Mehdi Tomas split the work in two. <bookmark mark='a'/> Offline, a network learns the model's implied "
            "volatility from its parameters, an expiry and a strike, trained on Monte Carlo prices from twelve thousand "
            "random parameter sets. Online, calibration runs through the network, which is smooth and can be "
            "differentiated. The slow simulation is paid once."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def training(self, c):
        h = c["history"]
        ep = np.array([r["epoch"] for r in h])
        tr = np.array([r["train_rmse"] for r in h])
        va = np.array([r["val_rmse"] for r in h])
        top = float(max(tr[1:].max(), va[1:].max()) * 1.3)
        g = axes([0, ep.max()], [0, top], x_length=6.6, y_length=4.2, xlabel=r"epoch",
                 ylabel=r"error in implied volatility (vol points)", xticks=[0, 10, 20, 30, 40],
                 yticks=[round(v, 1) for v in np.linspace(0, top, 4)[1:]], font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        l1 = curve(ax, ep, np.minimum(tr, top), GREY_B, stroke_width=2.5)
        l2 = curve(ax, ep, np.minimum(va, top), NET, stroke_width=3.5)
        nz = DashedLine(ax.c2p(0, c["label_noise_rmse"]), ax.c2p(ep.max(), c["label_noise_rmse"]), stroke_color=BAD,
                        stroke_width=2)
        leg = legend([(GREY_B, r"training sets"), (NET, r"parameter sets never seen"),
                      (BAD, r"Monte Carlo noise in the labels themselves")], font_size=16)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        q = c["held_err_q"]
        side = wrapped_label(rf"held out: {c['held_rmse']:.2f} vol points (median {q[0]:.2f}, 99th percentile {q[2]:.2f}). "
                             rf"Simulating the same parameters again with fresh random numbers moves the labels by "
                             rf"{c['label_noise_rmse']:.2f}: the network's error is below the noise in its own labels, "
                             r"because fitting thousands of them averages that noise out", 4.3, 19, GREY_A).to_edge(RIGHT, buff=0.4)
        src = illustration(rf"{c['train_seconds'] / 60:.0f} minutes of training on a CPU; 4 layers of 96 units")
        with self.voiceover(
            "Training, epoch by epoch. Grey is the error on the training data, purple on parameter sets the network "
            f"never saw. <bookmark mark='a'/> It ends at {c['held_rmse']:.2f} vol points. For scale: simulating the same "
            f"parameters again with fresh random numbers moves the labels themselves by {c['label_noise_rmse']:.2f}. The "
            "network's error is below the noise in its own training data: fitting thousands of noisy labels averages "
            "the noise out."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(l1), FadeIn(leg[0]), Create(l2), FadeIn(leg[1]), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(nz), FadeIn(leg[2]), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def surface(self, c):
        s = c["surface"]
        p = s["params"]
        p14 = c["part14"]
        sl = c["slices"]
        groups = VGroup()
        for d in sl:
            k, iv, mc = np.asarray(d["k"]), np.asarray(d["iv"]), np.asarray(d["mc"])
            kk, net = np.asarray(d["kk"]), np.asarray(d["net"])
            ylo, yhi = float(np.nanmin(np.r_[iv, net])) - 0.03, float(np.nanmax(np.r_[iv, net])) + 0.03
            yt = [v / 100 for v in range(int(np.ceil(ylo * 10)) * 10, int(yhi * 100) + 1, 10)]
            g = axes([kk[0], kk[-1]], [ylo, yhi], x_length=3.7, y_length=2.8, xlabel=r"log-moneyness $k$",
                     ylabel=r"implied volatility" if not groups else "",
                     xticks=[round(kk[0] / 2, 1), 0, round(kk[-1] / 2, 1)], yticks=yt,
                     yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=13)
            ax = g.ax
            dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=IV) for a, b in zip(k, iv)])
            chk = VGroup(*[Cross(scale_factor=0.06, stroke_color=REF, stroke_width=2).move_to(ax.c2p(a, b))
                           for a, b in zip(k, mc) if np.isfinite(b) and ylo < b < yhi])
            ln = curve(ax, kk, np.clip(net, ylo, yhi), NET, stroke_width=3)
            ttl = label(rf"{d['T'] * 365:.0f} days", font_size=20).next_to(g, UP, buff=0.1)
            groups.add(VGroup(g, dots, ln, chk, ttl))
        groups.arrange(RIGHT, buff=0.45).to_edge(UP, buff=0.9)
        leg = legend([(IV, r"the Surface (Part 13)"), (NET, r"rough Bergomi through the network"),
                      (REF, r"$\times$ fresh Monte Carlo at the same parameters")], font_size=16)
        leg.next_to(groups, DOWN, buff=0.3).to_edge(LEFT, buff=0.8)
        res = VGroup(
            MathTex(rf"H = {p['H']:.2f},\ \eta = {p['eta']:.1f},\ \rho = {p['rho']:.2f}", font_size=30, color=NET),
            label(rf"error {s['net_rmse']:.2f} vol points through the network, {s['mc_rmse']:.2f} by fresh Monte Carlo; "
                  rf"{s['n']} quotes", font_size=19, color=GREY_A),
            label(rf"calibrated in {s['seconds']:.1f} s; one network pass over the surface: "
                  rf"{1e3 * c['t_net_surface']:.1f} ms, against {c['t_mc_surface']:.0f} s of Monte Carlo", font_size=19,
                  color=GREY_A),
            label(rf"Part 14's direct Monte Carlo fit: $H = {p14['params']['H']:.2f}$, error {p14['rmse']:.2f}",
                  font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(leg, DOWN, buff=0.3).to_edge(LEFT, buff=0.8)
        with self.voiceover(
            "Now the Surface, calibrated through the network. Three expiries: the market in orange, the network's smile "
            "in purple. <bookmark mark='a'/> The crosses check it: fresh Monte Carlo at the calibrated parameters, never "
            f"touched by the network. The fit is {s['net_rmse']:.2f} vol points through the network and {s['mc_rmse']:.2f} "
            f"by simulation, with Hurst exponent {p['H']:.2f}. <bookmark mark='b'/> A pass of the network over the whole "
            f"surface takes {1e3 * c['t_net_surface']:.1f} milliseconds, against {c['t_mc_surface']:.0f} seconds of Monte "
            f"Carlo. Part fourteen's direct fit found H of {p14['params']['H']:.2f}. Calibration that took minutes now "
            "takes seconds, so it can be done every day, which is the next chapter."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(VGroup(gg[0], gg[1], gg[4])) for gg in groups], lag_ratio=0.3),
                      FadeIn(leg[0]))
            self.play(*[Create(gg[2]) for gg in groups], FadeIn(leg[1]))
            vo.wait_until("a")
            self.play(*[FadeIn(gg[3]) for gg in groups], FadeIn(leg[2]), FadeIn(res[0]), FadeIn(res[1]))
            vo.wait_until("b")
            self.play(FadeIn(res[2]), FadeIn(res[3]))
        self.wait(0.5)
        self.clear_scene()
