from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import HIST, MEAS, TEST, TRAIN, chapter, curve, load, log_axes

SPIKE, ISO = C.INTERVAL, C.SURPRISE


class Benign(VoiceoverScene):
    def construct(self):
        chapter(self, 14, r"Benign overfitting", r"When is fitting the noise harmless?",
                "Chapter fourteen. Benign overfitting.")
        self.picture()
        self.measure()
        self.why()

    # ------------------------------------------------------------------
    def picture(self):
        g = np.random.default_rng(5)
        xs = np.sort(g.uniform(-2.6, 2.6, 18))
        f = lambda x: 0.6 * np.sin(1.3 * x) + 0.15 * x  # noqa: E731
        ys = f(xs) + 0.35 * g.normal(size=len(xs))
        ax = Axes(x_range=[-3, 3, 1], y_range=[-1.8, 1.8, 1], x_length=10.0, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([0, -0.6, 0])
        smooth = ax.plot(f, x_range=[-3, 3], color=MEAS, stroke_width=4)
        grid = np.linspace(-3, 3, 1600)
        # Nearby spikes overlap. Solve for their coefficients so the pictured
        # interpolant actually reaches every label, as the narration claims.
        gram = np.exp(-((xs[:, None] - xs[None, :]) / 0.025) ** 2)
        coefficients = np.linalg.solve(gram, ys - f(xs))

        def spiky(x):
            return f(x) + sum(c * np.exp(-((x - a) / 0.025) ** 2) for a, c in zip(xs, coefficients))

        assert np.allclose(spiky(xs), ys, rtol=0, atol=1e-10)
        sp = VMobject(color=C.BITS, stroke_width=2.5).set_points_as_corners([ax.c2p(x, spiky(x)) for x in grid])
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=WHITE) for a, b in zip(xs, ys)])
        cw = np.polyfit(xs, ys, 11)
        wild = ax.plot(lambda x: float(np.clip(np.polyval(cw, x), -1.75, 1.75)), x_range=[-2.7, 2.7], color=C.SURPRISE,
                       stroke_width=2.5)
        cap = VGroup(label(r"harmful: \ the fit bends everywhere to reach the noise", font_size=24, color=C.SURPRISE),
                     label(r"benign: \ smooth almost everywhere, \ a thin spike at each training point", font_size=24,
                           color=C.BITS)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(UP, buff=0.35)
        tag = note(r"schematic").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Double descent showed fits that pass through every noisy label and still do well. How can fitting "
            "noise exactly be harmless? <bookmark mark='a'/> One way to chase noisy labels is to bend the whole curve; "
            "that spoils predictions elsewhere. <bookmark mark='b'/> Another is to follow the "
            "smooth truth almost everywhere, and reach each noisy label with a thin spike that touches almost no "
            "other input. That fit has zero training error, and on new data it's nearly as good as the truth. "
            "In high dimensions, the spikes come for free."
        ) as vo:
            self.play(Create(ax), FadeIn(dots), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(wild), FadeIn(cap[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(wild.animate.set_stroke(opacity=0.25), Create(smooth), run_time=1.0)
            self.play(Create(sp), FadeIn(cap[1]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measure(self):
        b = load("benign")
        Ds = np.asarray(b["Ds"], float)
        sp, iso = np.asarray(b["spiked"]), np.asarray(b["iso"])
        spq, isq = np.asarray(b["spiked_q"]), np.asarray(b["iso_q"])
        n, s, noise = int(b["n"]), int(b["s"]), float(b["noise"])
        G = log_axes((2, math.log10(Ds[-1])), (-2, 1), x_length=7.0, y_length=4.4, xticks=[2, 3, 4],
                     yticks=[-2, -1, 0, 1], xlabel=r"$D$: \ extra directions", ylabel=r"excess error on new data",
                     center=(-2.2, -0.6, 0))
        ax = G.ax
        lx = np.log10(Ds)

        def ly(v):
            return np.clip(np.log10(np.maximum(v, 1e-2)), -2, 1)

        bs = band(ax, lx, ly(spq[:, 0]), ly(spq[:, 1]), SPIKE, 0.18)
        bi = band(ax, lx, ly(isq[:, 0]), ly(isq[:, 1]), ISO, 0.18)
        cs = curve(ax, lx, ly(sp), SPIKE, 4)
        ci = curve(ax, lx, ly(iso), ISO, 4)
        nl = DashedLine(ax.c2p(2, math.log10(noise)), ax.c2p(lx[-1], math.log10(noise)), color=GREY_B, stroke_width=2)
        nll = label(rf"the noise itself, \ ${noise:g}$", font_size=20, color=GREY_B).next_to(nl.get_end(), UP, buff=0.05)
        nll.align_to(nl, RIGHT)
        setup = VGroup(
            label(rf"$n = {n}$ noisy examples; \ the signal in ${s}$ strong directions", font_size=22),
            label(rf"plus $D$ weak ones, \ of total variance ${b['tail']:g}$", font_size=22, color=SPIKE),
            label(r"or plus $D$ as strong as the signal's", font_size=22, color=ISO),
            label(rf"the minimum-norm fit: \ every label fit, \ residual $< {sci(max(b['max_train'], 1e-15), 0)}$",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_corner(UR, buff=0.3)
        with self.voiceover(
            "Bartlett, Long, Lugosi and Tsigler made this exact in 2020, for linear regression. Take a hundred "
            "noisy examples whose signal lives in five strong directions, and fit them exactly with the minimum-"
            "norm solution. <bookmark mark='a'/> Add D weak directions that together have a small total variance: "
            f"as D grows, the excess error falls, to {sp[-1]:.3f} with {int(Ds[-1]):,} of them, "
            f"{100 * sp[-1] / noise:.0f} percent of the noise level, though the fit reproduces every noisy label. Benign. <bookmark mark='b'/> Add instead D "
            f"directions as strong as the signal's, and the excess error climbs to {iso[-1]:.1f}: the fit spreads "
            "its weight over directions that matter, and loses the signal. Harmful."
        ) as vo:
            self.play(FadeIn(G), FadeIn(setup[0]), FadeIn(setup[3]), Create(nl), FadeIn(nll))
            vo.wait_until("a")
            self.play(FadeIn(setup[1]), FadeIn(bs), Create(cs), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(setup[2]), FadeIn(bi), Create(ci), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        b = load("benign")
        rows = [
            cmath(r"\text{excess}", r"\approx", r"\text{bias} + \sigma^2 \Big(\frac{k}{n} + \frac{n}{R_k}\Big)",
                  font_size=34),
            cmath(r"R_k", r"=", r"\frac{\big(\sum_{i > k} \lambda_i\big)^2}{\sum_{i > k} \lambda_i^2}", font_size=34),
            cmath(r"\text{bias}", r"\approx", r"\text{ridge with } \lambda_{\text{eff}} = \tfrac1n \textstyle\sum_{i > k} "
                  r"\lambda_i", font_size=34),
        ]
        whys = [why(r"$k$ strong directions, \ the rest a tail"),
                why(r"the tail's effective rank: \ how many directions share its variance"),
                why(r"the tail soaks up the noise, \ and acts as a ridge on the rest")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-2.4, buff=0.55, edge=6.9)
        cond = VGroup(
            label(r"benign when: \ $k \ll n$, \ $R_k \gg n$, \ and the tail's total variance $\ll n$", font_size=26,
                  color=SPIKE),
            label(rf"here: \ $k/n = {b['s'] / b['n']:.2f}$, \ $n/R_k = {b['n'] / b['Ds'][-1]:.4f}$, \ "
                  rf"$\lambda_{{\mathrm{{eff}}}} = {b['tail'] / b['n']:.2f}$", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=1.75)
        hist = history_card(2020, r"P.~Bartlett, P.~Long, G.~Lugosi \& A.~Tsigler", r"\textit{Benign Overfitting in "
                            r"Linear Regression}", width=6.6, font_size=17, color=HIST).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Their theorem splits the excess error into a bias, and a variance that's the noise times two terms. "
            "<bookmark mark='a'/> The first counts the strong directions against the examples. "
            "<bookmark mark='b'/> The second compares n with the effective rank of the tail: how many directions "
            "share the weak variance. Many small directions can each absorb a little of the noise without moving "
            "predictions much: those are the spikes. <bookmark mark='c'/> And the tail as a whole acts like a ridge "
            "penalty on the strong directions, costing a little bias. <bookmark mark='d'/> So interpolation is "
            "benign when the signal is low-dimensional and the rest is a long tail of tiny directions, the kind of "
            "spectrum real data and wide networks tend to have. For real networks the picture is more often in "
            "between: Mallinar and colleagues in 2022 called it tempered."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=WHITE, scale_factor=1.03))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(cond, shift=UP * 0.1))
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
