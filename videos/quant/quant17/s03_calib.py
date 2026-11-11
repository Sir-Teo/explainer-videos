from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import axes, data_range
from videos.quant.quant17.common import BAD, GOOD, IV, NET, OPT, PART, REF, ask, comma, illustration, load


class Calibrator(VoiceoverScene):
    def construct(self):
        c = load("calib")
        self.card()
        self.idea(c)
        self.pipeline(c)
        self.training(c, load("calib_ckpt"))
        self.noise(c, load("calib_noise"))

    def card(self):
        c = chapter_card(3, r"The neural calibrator: learning the map", r"How do you calibrate a model with no formula, "
                         r"every day?", lit=(2016,), part=PART)
        with self.voiceover("Chapter three. The neural calibrator, part one: learning the map."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def idea(self, c):
        npts = f"{c['n_train'] + c['n_held']:,}".replace(",", "{,}")
        rows = [cmath(r"\sigma_{\text{imp}}", r"\approx", r"\mathcal{N}_w\big(H, \eta, \rho, \xi_0, \xi_1;\ T, k\big)",
                      font_size=40, colors={r"\sigma_{\text{imp}}": IV}),
                cmath(r"\hat\theta", r"=", r"\arg\min_\theta \sum_i w_i\,\big(\mathcal{N}_w(\theta; T_i, k_i) - "
                      r"\sigma_i^{\text{mkt}}\big)^2", font_size=36, colors={r"\hat\theta": GOOD})]
        whys = [why(rf"Horvath, Muguruza and Tomas (2021): learn the map from rough Bergomi's parameters and an option's "
                    rf"expiry and moneyness to its implied volatility, offline, from Monte Carlo: here "
                    rf"{npts} prices from 12{{,}}000 parameter sets"),
                why(r"then calibrate online by gradient descent through the network, which is smooth and differentiable: "
                    r"simulation moves offline; fresh engine checks and retraining remain necessary")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.6, buff=1.0, edge=6.9)
        with self.voiceover(
            "Part fourteen compared rough Bergomi and Heston on one frozen option surface. The slow engine uses simulation inside calibration. Neural calibration moves much of that work offline, following research including Horvath, Muguruza and Tomas. <bookmark mark='a'/> Here a pointwise surrogate learns implied volatility from five parameters, maturity and log-moneyness. Its labels come from twelve thousand parameter sets. Online optimization differentiates this fitted surrogate. Simulation is still needed for independent checks, new parameter regions and retraining; paying once does not remove numerical bias or model risk."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def pipeline(self, c):
        n_pts = c["n_train"] + c["n_held"]
        off = RoundedRectangle(width=6.0, height=3.2, corner_radius=0.15, stroke_color=GREY_B, stroke_width=1.5)
        on = RoundedRectangle(width=5.6, height=3.2, corner_radius=0.15, stroke_color=NET, stroke_width=1.5)
        VGroup(off, on).arrange(RIGHT, buff=0.8).shift(UP * 0.9)
        t_off = label(r"offline, once: hours", font_size=22, color=GREY_A).next_to(off, UP, buff=0.1)
        t_on = label(r"online, every day: seconds", font_size=22, color=NET).next_to(on, UP, buff=0.1)
        rng = np.random.default_rng(0)
        cloud = VGroup(*[Dot(off.get_center() + np.array([rng.uniform(-2.6, 2.6), rng.uniform(-0.5, 1.0), 0]),
                             radius=0.025, color=IV) for _ in range(160)])
        bar_bg = Rectangle(width=5.2, height=0.22, stroke_color=GREY_C, stroke_width=1).move_to(off.get_bottom() + UP * 0.45)
        bar = Rectangle(width=5.2, height=0.22, stroke_width=0, fill_color=IV, fill_opacity=0.8).move_to(bar_bg)
        bar.stretch(0.01, 0, about_edge=LEFT)
        cap = label(rf"12{{,}}000 parameter sets $\to$ Monte Carlo $\to$ {comma(n_pts)} labels $\to$ network",
                    font_size=17, color=GREY_A).next_to(bar_bg, UP, buff=0.12)
        flow = VGroup(label(r"today's quotes", font_size=21, color=IV), MathTex(r"\downarrow", font_size=30),
                      label(r"gradient descent through the network", font_size=21, color=NET),
                      MathTex(r"\downarrow", font_size=30), label(r"$(H, \eta, \rho, \xi_0, \xi_1)$", font_size=24,
                                                                   color=GOOD)).arrange(DOWN, buff=0.08).move_to(on)
        lin = VGroup(*[history_card(y, w, t, color=QC.IDEA, width=6.2, font_size=16) for y, w, t in (
            (2016, r"Hernandez, \textit{Risk}", r"a network learns the inverse map, quotes to parameters, for Hull--White"),
            (2018, r"Bayer and Stemper, arXiv", r"neural calibration of rough stochastic volatility"),
            (2019, r"Liu, Oosterlee and Bohte, \textit{Risks}", r"networks for prices and implied volatilities"),
            (2021, r"Horvath, Muguruza and Tomas, \textit{Quantitative Finance}",
             r"the forward map on a grid, for rough volatility"))]
        ).arrange_in_grid(rows=2, cols=2, buff=(0.25, 0.15)).to_edge(DOWN, buff=0.25)
        if lin.width > 13.4:
            lin.scale_to_fit_width(13.4)
        with self.voiceover(
            f"Offline, draw twelve thousand parameter sets and retain {n_pts:,} finite implied-volatility labels, then train the surrogate. Many option labels share the same simulated paths, so this is not that many independent observations. <bookmark mark='a'/> Online, fit the five parameters through the surrogate. These recorded CPU times describe different workloads and do not prove equal accuracy. <bookmark mark='b'/> The history includes Hernandez's inverse calibration, Bayer and Stemper's neural calibration, Liu, Oosterlee and Bohte's pricing and implied-volatility networks, and Horvath, Muguruza and Tomas's rough-volatility calibration. Our pointwise implementation is an illustration within this literature."
        ) as vo:
            self.play(Create(off), FadeIn(t_off), FadeIn(bar_bg), FadeIn(bar), FadeIn(cap))
            self.play(LaggedStart(*[FadeIn(d) for d in cloud], lag_ratio=0.01),
                      bar.animate.stretch(100, 0, about_edge=LEFT), run_time=4)
            vo.wait_until("a")
            self.play(Create(on), FadeIn(t_on), LaggedStart(*[FadeIn(f_) for f_ in flow], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.2) for card in lin], lag_ratio=0.5, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def training(self, c, k):
        h0, h1 = c["history"], k["history"]
        ep = np.array([r["epoch"] for r in h0])
        L = np.array([[r["val_rmse"] for r in h0], [r["val_rmse"] for r in h1]])
        sl = c["slices"]
        cks = ["0", "1", "5", "10", "20", "40"]
        yr = data_range(*[d["iv"] for d in sl],
                        *[k["snaps"][c][j] for c in cks for j in range(len(sl))])

        def frame(i):
            panels = VGroup()
            for j, d in enumerate(sl):
                kk = np.asarray(d["kk"])
                iv = np.asarray(d["iv"])
                y = np.asarray(k["snaps"][cks[i]][j])
                ylo, yhi = yr
                g = axes([kk[0], kk[-1]], [ylo, yhi], x_length=1.75, y_length=2.4, xlabel=rf"{d['T'] * 365:.0f} days",
                         ylabel=r"implied vol" if j == 0 else "", xticks=[], yticks=[0.4, 0.7, 1.0] if j == 0 else [],
                         yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=12)
                dots = VGroup(*[Dot(g.ax.c2p(a, b_), radius=0.03, color=IV) for a, b_ in zip(d["k"], iv)
                                if kk[0] <= a <= kk[-1] and np.isfinite(b_)])
                panels.add(VGroup(g, dots, curve(g.ax, kk, y, NET, stroke_width=3)))
            panels.arrange(RIGHT, buff=0.15)
            return VGroup(panels, label(rf"after epoch {cks[i]}: the Surface's smiles at the calibrated parameters",
                                        font_size=16, color=NET).next_to(panels, DOWN, buff=0.15))
        rp = TrainingReplay(ep, L, frame, checkpoints=[1, 2, 5, 10, 20, 40], ylabel=r"held-out error (vol points)",
                            xlabel=r"epoch")
        leg = legend([(IV, r"the Surface's quotes"), (NET, r"what the network (seed 1) says rough Bergomi gives"),
                      (QC.Q, r"two-seed min--max; held-out parameter sets; not a confidence interval")], font_size=16).to_edge(UP, buff=0.3)
        e0, e1 = h0[-1]["val_rmse"], h1[-1]["val_rmse"]
        src = illustration(rf"4 layers of 96 units; 40 epochs of the {comma(c['n_train'])} training labels; "
                           rf"about {c['train_seconds'] / 60:.0f} recorded shared-CPU minutes for the base seed")
        with self.voiceover(
            "Here is the network learning, from two random starts. On the right, its error on parameter sets it never "
            "saw. On the left, what it believes rough Bergomi gives at the parameters we will calibrate in the next "
            "chapter, at three expiries, against the market's quotes. <bookmark mark='a'/> At the start, flat lines. "
            "After one pass, a level. After five, the skew appears, and it sharpens epoch by epoch. Both seeds end "
            f"near {min(e0, e1):.1f} to {max(e0, e1):.1f} vol points."
        ) as vo:
            self.play(FadeIn(rp), FadeIn(leg), FadeIn(src))
            vo.wait_until("a")
            rp.play(self, run_time=max(vo.remaining(0.5), 4))
        self.wait(0.4)
        self.clear_scene()

    def noise(self, c, nz):
        a, b, d = nz["net_label"], nz["net_fresh"], nz["label_fresh"]
        s10 = d["rmse"] / np.sqrt(1.5)
        rows = [cmath(r"\mathbb{E}(\hat F - y)^2", r"=", r"\mathbb{E}(\hat F - F)^2 + s^2", font_size=40,
                      colors={r"\mathbb{E}(\hat F - y)^2": NET}),
                cmath(r"\mathbb{E}(y_{10k} - y_{20k})^2", r"=", r"s_{10k}^2 + s_{20k}^2 \approx 1.5\, s_{10k}^2", font_size=40,
                      colors={r"\mathbb{E}(y_{10k} - y_{20k})^2": BAD}),
                cmath(r"s_{10k}", r"\approx", rf"{d['rmse']:.2f} / \sqrt{{1.5}} = {s10:.2f}", font_size=40,
                      colors={r"s_{10k}": BAD})]
        whys = [why(r"a label $y$ is the true implied vol $F$ plus Monte Carlo noise of variance $s^2$, independent of the "
                    r"network: this identity assumes conditionally unbiased label noise, independent of the fitted network; it concerns expected squared error, not every finite sample"),
                why(r"two independent simulations of the same parameters, with 10{,}000 and 20{,}000 paths: Monte Carlo "
                    r"price-estimator variance scales as $1/n$; the $1.5$ implied-vol approximation also needs local linearization and comparable biases"),
                why(r"dividing the gap by $\sqrt{1.5}$ is a diagnostic, not an exact noise estimate; implied-vol inversion, finite-IV selection and common time-grid bias remain")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.4, buff=0.7, edge=6.9)
        with self.voiceover(
            f"An ideal variance decomposition first: conditionally unbiased independent validation noise adds to the network's expected squared error. It is not a lower bound for every measured finite-sample error. Implied-volatility labels need extra care: inversion is nonlinear and can be biased. <bookmark mark='a'/> The saved diagnostic repeats {nz['n_sets']} held-out parameter sets with twenty thousand paths, comparing them with the ten-thousand-path labels. A one-and-a-half variance factor is only a local linear approximation; both engines also share time-discretization bias. <bookmark mark='b'/> Dividing the gap by square root of one point five gives {s10:.2f} vol points as an illustrative noise diagnostic, not a certified noise floor or a true-model error."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()
        names = [(r"network vs held-out labels (10k paths)", a, NET), (r"network vs fresh simulation (20k paths)", b, GOOD),
                 (r"label vs fresh simulation", d, BAD)]
        mx = max(x["rmse"] for _, x, _ in names) * 1.25
        g = axes([-0.5, 2.5], [0, mx], x_length=6.6, y_length=4.0, ylabel=r"vol points", xticks=[], yticks=[0, 1, 2],
                 font_size=14).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        bars = VGroup()
        for i, (nm, x, col) in enumerate(names):
            p0, p1 = g.ax.c2p(i - 0.3, 0), g.ax.c2p(i + 0.3, x["rmse"])
            r_ = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                           fill_opacity=0.8).move_to((p0 + p1) / 2)
            m_ = DashedLine(g.ax.c2p(i - 0.3, x["median_abs"]), g.ax.c2p(i + 0.3, x["median_abs"]), stroke_color=WHITE,
                            stroke_width=2)
            bars.add(VGroup(r_, m_, MathTex(f"{x['rmse']:.2f}", font_size=28, color=col).next_to(r_, UP, buff=0.1),
                            wrapped_label(nm, 2.0, 15, col).next_to(g.ax.c2p(i, 0), DOWN, buff=0.15)))
        closer = b["rmse"] < d["rmse"]
        if closer:
            verdict = "the network is closer to the fresh simulation than these held-out labels are"
        else:
            verdict = "the network is no closer to the fresh simulation than these held-out labels are"
        side = wrapped_label(rf"bars: root-mean-square; white lines: median absolute ({b['median_abs']:.2f}, "
                             rf"{d['median_abs']:.2f}). {nz['n_points']:,} points on {nz['n_sets']} parameter sets the "
                             r"network never saw. The variance split is not exact (implied-vol noise has heavy tails), so "
                             r"no single 'true error' is claimed".replace(",", "{,}", 1), 4.4, 18,
                             GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            f"Compare the saved finite-implied-volatility subset. Network against held-out ten-thousand-path labels: {a['rmse']:.2f} vol points. <bookmark mark='a'/> Those labels against fresh simulation: {d['rmse']:.2f}. <bookmark mark='b'/> Network against fresh simulation: {b['rmse']:.2f}. Here {verdict}. These statistics mix parameter sets with correlated option errors and exclude non-finite fresh implied volatilities. The comparison can suggest smoothing of label noise; it does not uniquely identify the surrogate's bias, variance or continuous-time pricing error."
        ) as vo:
            self.play(FadeIn(g), FadeIn(bars[0]))
            vo.wait_until("a")
            self.play(FadeIn(bars[2]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1]), FadeIn(side))
        q = ask(r"train on labels with twice the noise. Does the held-out error double?")
        with self.voiceover(
            "A question: train on labels with twice the noise. Does the error against the fresh simulation double? "
            "Think about what averaging does before you answer; it is one of the problems in the notes."
            " Far less than double. Each label is noisier, but the network averages over thousands of them, so its own error grows much more slowly than the noise: you need more data, not a new method. Next: calibrating the Surface through the network."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
