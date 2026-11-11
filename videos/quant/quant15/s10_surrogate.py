from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, GOOD, IV, OPT, PART, SPOT, illustration, load, axes, data_range, pause_card


class Surrogate(VoiceoverScene):
    def construct(self):
        s = load("surrogate")
        r = load("surrogate_replay")
        self.card()
        self.lab(r)
        self.replay(r)
        self.baseline(r)
        self.net(s)

    def card(self):
        c = chapter_card(16, r"A neural pricer for the book, trained on screen", r"How do you reprice ten thousand notes "
                         r"every second, and do you need a network to do it?", part=PART)
        with self.voiceover("Chapter sixteen. A neural pricer for the book, trained on screen."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def lab(self, r):
        card = lab_card(r"training the surrogate", [
            "net = Sequential(Linear(3, 64), SiLU(), Linear(64, 64), SiLU(),",
            "                 Linear(64, 1))",
            "opt = torch.optim.Adam(net.parameters(), lr=3e-3)",
            "for step in range(4000):",
            "    idx = torch.randint(0, len(xt), (256,))",
            "    loss = torch.mean((net(xt[idx]) - yt[idx]) ** 2)",
            "    opt.zero_grad()",
            "    loss.backward()",
            "    opt.step()",
        ], source="videos/quant/quant15/compute.py: compute_surrogate", width=7.8, font_size=17).to_corner(UL, buff=0.35)
        f = r["final"]
        outs = [f"3,000 Monte Carlo labels (3,000 paths each); inputs: log spot, months / 24, knocked in",
                f"test RMSE after 4,000 steps, seeds 0, 1, 2: {f[0]:.3f}, {f[1]:.3f}, {f[2]:.3f}"]
        with self.voiceover(
            f"Our proxy prices one fixed-parameter contract, not an arbitrary snowball book. Inputs are relative spot, age and knock-in state; volatility, carry and coupon remain fixed. Two hidden layers have sixty-four units each. <bookmark mark='a'/> Three thousand synthetic price labels use three thousand paths apiece. Four thousand fixed optimization steps fit random batches of two hundred fifty-six. <bookmark mark='b'/> The three seed runs have RMSE {f[0]:.3f}, {f[1]:.3f} and {f[2]:.3f} against a hundred fifty higher-path numerical references. Test input examples are held out, but the replay inspects this same set repeatedly; the pricing seed formula is predefined. This is an in-model numerical benchmark, not future-market validation or an untouched final market holdout."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(Indicate(card.code[3:], color=QC.HOUSE, scale_factor=1.02))
            vo.wait_until("b")
            lab_run(self, card, outs, font_size=16)
        self.wait(0.4)
        self.clear_scene()

    def replay(self, r):
        steps = np.asarray(r["steps"], float)
        L = np.asarray(r["rmse"], float)
        ck = r["checkpoints"]
        sg = np.asarray(r["spots"])
        ds = np.asarray(r["dot_spots"])
        dots = {k: np.asarray(v) for k, v in r["dots"].items()}

        def frame(i):
            a = axes([0.6, 1.2], data_range(*[v for c in r["curves"].values() for v in c.values()], *dots.values()), x_length=4.8, y_length=3.4, xlabel=r"index / start, month 6",
                     ylabel=r"note value", xticks=[0.75, 1.0], yticks=[0.6, 1.0, 1.3], font_size=13)
            c = r["curves"][str(ck[i])]
            g = VGroup(a)
            for fl, col in (("0", OPT), ("1", BAD)):
                # a note still alive below the knock-in level does not exist: draw that state only above it
                keep = sg >= 0.75 if fl == "0" else np.ones_like(sg, bool)
                g.add(curve(a.ax, sg[keep], np.asarray(c[fl])[keep], col, stroke_width=3))
                g.add(VGroup(*[Dot(a.ax.c2p(x, y), radius=0.04, color=WHITE) for x, y in zip(ds, dots[fl])
                               if fl == "1" or x >= 0.75]))
            return g  # the replay prints the step above the loss curve
        rp = TrainingReplay(steps, L, frame, ck, ylabel=r"synthetic test RMSE, log scale (3 seeds)", log_y=True)
        leg = legend([(OPT, r"the network, not knocked in"), (BAD, r"knocked in"), (WHITE, r"Monte Carlo, 40{,}000 paths")],
                     font_size=16).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The replay shows all saved predictions and the full RMSE history without clipping initial errors. The right axis is logarithmic. Its band spans three network seeds, not a confidence interval. On the left, month-six predictions are compared with forty-thousand-path reference dots. <bookmark mark='a'/> The not-yet-knocked-in state is drawn only where admissible. Training learns the broad shape, but coarse sampling near observation boundaries, label noise and limited function approximation leave residual error. The plotted state comparison does not establish a universal price discontinuity at a continuously monitored barrier. Nor does fitting values establish accurate Greeks, monotonicity or absence of arbitrage."
        ) as vo:
            self.play(FadeIn(rp), FadeIn(leg))
            vo.wait_until("a")
            rp.play(self, run_time=max(vo.remaining(0.5), 6.0))
        self.wait(0.4)
        self.clear_scene()

    def baseline(self, r):
        f = r["final"]
        poly = r["poly_rmse"]
        noise = r["label_noise"]
        items = [(rf"network, seed {i}", v, OPT) for i, v in enumerate(f)] + [
            (r"degree-4 polynomial, same 3{,}000 labels", poly, GOOD),
            (r"noise of one 3{,}000-path label", noise, GREY_B)]
        top = max(v for _, v, _ in items) * 1.25
        rows = VGroup()
        for nm, v, col in items:
            bar = Rectangle(width=6.0 * v / top, height=0.38, stroke_width=0, fill_color=col, fill_opacity=0.85)
            rows.add(VGroup(label(nm, font_size=20, color=col), bar, MathTex(f"{v:.4f}", font_size=26, color=col)))
        for r_ in rows:
            r_[1].next_to(r_[0], RIGHT, buff=0.3)
            r_[2].next_to(r_[1], RIGHT, buff=0.2)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.8)
        for r_ in rows:
            r_[1].align_to(rows[3][1], LEFT)
            r_[1].shift(RIGHT * (rows[3][0].get_right()[0] + 0.3 - r_[1].get_left()[0]))
            r_[2].next_to(r_[1], RIGHT, buff=0.2)
        wins = poly < min(f)
        verdict = (f"The polynomial wins: {poly:.4f}, below every seed of the network. With three inputs, a smooth "
                   "fixed basis fitted by least squares is hard to beat, and its coefficients come from a linear least-squares solve."
                   if wins else
                   f"The network wins: its best seed reaches {min(f):.4f} against the polynomial's {poly:.4f}.")
        foot = wrapped_label(r"the network's case is many inputs: a worst-of on three assets with the vol surface as input, "
                             r"where a polynomial's terms explode (Sharma et al.\ 2024 report pricing three-asset "
                             r"autocallables about 250 times faster than Monte Carlo)", 11.6, 19, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            f"Compare a degree-four polynomial in log spot and age, with separate coefficients by knock-in state, using the same labels. <bookmark mark='a'/> Its RMSE is {poly:.4f}; the network seeds reach {f[0]:.4f}, {f[1]:.4f} and {f[2]:.4f}. For this fixed problem the polynomial is competitive. The local repeated-label standard deviation is {noise:.4f}, measured at one specified state, not across the whole input domain. Our test errors exceed it; it is not a demonstrated global error floor. <bookmark mark='b'/> More input dimensions make a full polynomial basis large, but networks also require more parameters, labels and validation. Sharma and co-authors' multi-asset result is a different benchmark. It cannot validate this three-input proxy outside its trained contract and parameter range."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_[0]) for r_ in rows], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r_[1], LEFT) for r_ in rows], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(r_[2]) for r_ in rows], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def net(self, s):
        mc = np.asarray(s["test_mc"])
        nn = np.asarray(s["test_net"])
        lo, hi = data_range(mc, nn)
        g = axes([lo, hi], [lo, hi], x_length=4.6, y_length=4.6, xlabel=r"Monte Carlo, 40{,}000 paths",
                 ylabel=r"the network", xticks=[0.6, 0.8, 1.0, 1.2], yticks=[0.6, 0.8, 1.0, 1.2], font_size=15)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        diag = DashedLine(ax.c2p(lo, lo), ax.c2p(hi, hi), stroke_color=GREY_C, stroke_width=1.5)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=OPT)
                        for a, b in zip(mc, nn)])
        speed = s["t_mc"] / s["t_net"]
        side = VGroup(
            MathTex(rf"\text{{error}}\ {s['rmse']:.3f}\ \text{{per 1 of notional}}", font_size=30, color=OPT),
            MathTex(rf"{s['t_mc']:.1f}\ \text{{s}} \to {1e6 * s['t_net']:.1f}\ \mu\text{{s per price}}", font_size=30, color=GOOD),
            wrapped_label(rf"about {speed / 1e6:.0f} million times faster. The largest errors sit at the knock-in cliff, "
                          r"near observation/state boundaries. Batched CPU inference excludes label generation, training and Greek validation", 4.6,
                          19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        src = illustration(rf"{len(mc)} random test notes, never seen in training; CPU, one thread")
        with self.voiceover(
            f"Seed zero has RMSE {s['rmse']:.3f} per unit notional on these hundred fifty synthetic references. The scatter retains every saved prediction. <bookmark mark='a'/> This machine measured about {1e6 * s['t_net']:.2f} microseconds per output in repeated batches of a hundred fifty, versus {s['t_mc']:.3f} seconds for one forty-thousand-path Monte Carlo valuation. They have different accuracy and setup costs; this is not single-request latency or a full calibration benchmark. Original training-label generation took {s['t_data']:.1f} seconds and network optimization {s['t_train']:.1f}, excluding the separately generated test references. Fast values enabled the historical book reconstruction, but their approximation and Greek errors remain model risks. Next, valuation governance."
        ) as vo:
            self.play(FadeIn(g), Create(diag), FadeIn(src), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots],
                                                                        lag_ratio=0.01, run_time=2), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
