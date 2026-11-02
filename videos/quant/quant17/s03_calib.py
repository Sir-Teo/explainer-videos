from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
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

    def pipeline(self, c):
        n_pts = c["n_train"] + c["n_held"]
        off = RoundedRectangle(width=6.0, height=3.2, corner_radius=0.15, stroke_color=GREY_B, stroke_width=1.5)
        on = RoundedRectangle(width=5.6, height=3.2, corner_radius=0.15, stroke_color=NET, stroke_width=1.5)
        VGroup(off, on).arrange(RIGHT, buff=0.8).shift(UP * 0.9)
        t_off = label(r"offline, once: hours", font_size=22, color=GREY_A).next_to(off, UP, buff=0.1)
        t_on = label(r"online, every day: seconds", font_size=22, color=NET).next_to(on, UP, buff=0.1)
        rng = np.random.default_rng(0)
        cloud = VGroup(*[Dot(off.get_center() + np.array([rng.uniform(-2.6, 2.6), rng.uniform(-0.9, 0.5), 0]),
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
        lin = VGroup(
            firm_card(r"Hernandez (2016)", r"a network learns the inverse map, quotes to parameters, for Hull--White",
                      source=r"\textit{Risk}", width=3.1, font_size=16),
            firm_card(r"Bayer and Stemper (2018)", r"pointwise: one implied vol per $(\theta, T, k)$", source=r"arXiv",
                      width=3.1, font_size=16),
            firm_card(r"Liu, Oosterlee and Bohte (2019)", r"networks for prices and implied volatilities", source=r"\textit{Risks}",
                      width=3.1, font_size=16),
            firm_card(r"Horvath, Muguruza and Tomas (2021)", r"the forward map on a grid, for rough volatility",
                      source=r"\textit{Quantitative Finance}", width=3.1, font_size=16),
        ).arrange(RIGHT, buff=0.18).to_edge(DOWN, buff=0.3)
        for card in lin:
            card[0].set_stroke(GREY_C)
        with self.voiceover(
            "The work splits in two. Offline, once: draw twelve thousand random parameter sets, simulate each by "
            f"Monte Carlo, and keep {n_pts:,} implied volatilities as labels; then fit the network to them. That took "
            "hours, once. <bookmark mark='a'/> Online, every day: gradient descent on the five parameters, through the "
            "network, in seconds. <bookmark mark='b'/> In 2016 Andres Hernandez first mapped quotes straight to "
            "parameters. Christian Bayer and Benjamin Stemper made it pointwise, the form used here; Liu, Oosterlee "
            "and Bohte learned prices and implied volatilities; and Horvath, Muguruza and Tomas made it practical for "
            "rough volatility."
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

        def frame(i):
            panels = VGroup()
            for j, d in enumerate(sl):
                kk = np.asarray(d["kk"])
                iv = np.asarray(d["iv"])
                y = np.asarray(k["snaps"][cks[i]][j])
                ylo, yhi = 0.3, 1.0
                g = axes([kk[0], kk[-1]], [ylo, yhi], x_length=1.75, y_length=2.4, xlabel=rf"{d['T'] * 365:.0f} days",
                         ylabel=r"implied vol" if j == 0 else "", xticks=[], yticks=[0.4, 0.7, 1.0] if j == 0 else [],
                         yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=12)
                dots = VGroup(*[Dot(g.ax.c2p(a, b_), radius=0.03, color=IV) for a, b_ in zip(d["k"], iv)
                                if kk[0] <= a <= kk[-1] and ylo < b_ < yhi])
                panels.add(VGroup(g, dots, curve(g.ax, kk, np.clip(y, ylo, yhi), NET, stroke_width=3)))
            panels.arrange(RIGHT, buff=0.15)
            return VGroup(panels, label(rf"after epoch {cks[i]}: the Surface's smiles at the calibrated parameters",
                                        font_size=16, color=NET).next_to(panels, DOWN, buff=0.15))
        rp = TrainingReplay(ep, L, frame, checkpoints=[1, 2, 5, 10, 20, 40], ylabel=r"held-out error (vol points)",
                            xlabel=r"epoch")
        leg = legend([(IV, r"the Surface's quotes"), (NET, r"what the network (seed 1) says rough Bergomi gives"),
                      (QC.Q, r"band: seeds 0 and 1, error on parameter sets never seen")], font_size=16).to_edge(UP, buff=0.3)
        e0, e1 = h0[-1]["val_rmse"], h1[-1]["val_rmse"]
        src = illustration(rf"4 layers of 96 units; 40 epochs of the {comma(c['n_train'])} training labels; "
                           rf"about {c['train_seconds'] / 60:.0f} minutes a seed on a CPU")
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
                cmath(r"\mathbb{E}(y_{10k} - y_{20k})^2", r"=", r"s_{10k}^2 + s_{20k}^2 = 1.5\, s_{10k}^2", font_size=40,
                      colors={r"\mathbb{E}(y_{10k} - y_{20k})^2": BAD}),
                cmath(r"s_{10k}", r"\approx", rf"{d['rmse']:.2f} / \sqrt{{1.5}} = {s10:.2f}", font_size=40,
                      colors={r"s_{10k}": BAD})]
        whys = [why(r"a label $y$ is the true implied vol $F$ plus Monte Carlo noise of variance $s^2$, independent of the "
                    r"network: so a held-out error can never fall below the noise of the labels it is scored against"),
                why(r"two independent simulations of the same parameters, with 10{,}000 and 20{,}000 paths: Monte Carlo "
                    r"variance falls like one over the number of paths, so their gap has variance $1.5\,s_{10k}^2$"),
                why(r"so the label-against-fresh gap overstates the labels' own noise by $\sqrt{1.5}$; and the fair judge of "
                    r"the network is the fresher, less noisy simulation")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.4, buff=0.7, edge=6.9)
        with self.voiceover(
            "How good is that? The labels themselves are noisy: each is the true implied volatility plus Monte Carlo "
            "noise, so a held-out error can never fall below the noise of the labels it is scored against. "
            f"<bookmark mark='a'/> So we simulated {nz['n_sets']} held-out parameter sets again, with twenty thousand "
            "fresh paths. Two independent simulations differ by both their noises, one and a half times the label's "
            f"variance. <bookmark mark='b'/> So the labels' own noise is about {s10:.2f} vol points."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()
        names = [(r"network vs its own label (10k paths)", a, NET), (r"network vs fresh simulation (20k paths)", b, GOOD),
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
            verdict = "the network is closer to the fresh simulation than its own training labels are"
        else:
            verdict = "the network is no closer to the fresh simulation than its own labels are"
        side = wrapped_label(rf"bars: root-mean-square; white lines: median absolute ({b['median_abs']:.2f}, "
                             rf"{d['median_abs']:.2f}). {nz['n_points']:,} points on {nz['n_sets']} parameter sets the "
                             r"network never saw. The variance split is not exact (implied-vol noise has heavy tails), so "
                             r"no single 'true error' is claimed".replace(",", "{,}", 1), 4.4, 18,
                             GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Now the three comparisons side by side. The network against its own noisy label: "
            f"{a['rmse']:.2f} vol points. <bookmark mark='a'/> The same labels against the fresh simulation: "
            f"{d['rmse']:.2f}. <bookmark mark='b'/> And the network against the fresh simulation: {b['rmse']:.2f}. So "
            f"{verdict}. A smooth fit to hundreds of thousands of noisy labels averages much of their noise away."
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
