from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import (CNF_C, DATA, FLOW, NOISE, PART, Plane, band, curve, load, node_box, take_away)

EXACT, HUTCH = CNF_C, "#7FD3FF"


class NeuralODE(VoiceoverScene):
    def construct(self):
        self.card()
        self.resnet()
        self.trace()
        self.hutchinson()
        self.training()
        self.particles()

    def card(self):
        card = chapter_card(10, r"Neural ODEs and continuous flows", r"What if the layers were infinitely thin?",
                            lit=(), part=PART)
        with self.voiceover("Chapter ten. Neural ODEs and continuous flows."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def resnet(self):
        rows = VGroup(
            cmath(r"h_{k+1}", r"=", r"h_k + f(h_k)", font_size=38),
            cmath(r"h(t + \Delta t)", r"=", r"h(t) + \Delta t\, f(h(t), t)", font_size=38),
            cmath(r"\frac{dh}{dt}", r"=", r"f_\theta(h(t), t)", font_size=40),
        ).arrange(DOWN, buff=0.55).move_to([-2.6, 0.6, 0])
        whys = VGroup(why(r"a residual block (Part 9)"), why(r"one Euler step of size $\Delta t$"),
                      why(r"$\Delta t \to 0$: \ an ODE")).arrange(DOWN, buff=0.95, aligned_edge=LEFT)
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.5).set_y(r.get_y())
        rows[2][2].set_color(CNF_C)
        card = history_card(2018, r"Chen, Rubanova, Bettencourt \& Duvenaud", r"\textit{Neural Ordinary Differential "
                            r"Equations}: \ best paper, NeurIPS 2018", width=6.0, font_size=20).to_edge(DOWN, buff=0.4)
        pros = label(r"depth becomes time; \ any ODE solver; \ run it backwards to invert", font_size=22,
                     color=GREY_A).next_to(rows, DOWN, buff=0.45)
        with self.voiceover(
            "A residual network, from Part 9, updates its state a little at each layer: h plus f of h. <bookmark "
            "mark='a'/> Read that as one step of Euler's method for an ordinary differential equation, with a "
            "step of size one. <bookmark mark='b'/> Shrink the step to zero and the layers become continuous: the "
            "state flows along a velocity field that a network defines. <bookmark mark='c'/> Ricky Chen, Yulia "
            "Rubanova, Jesse Bettencourt and David Duvenaud called these neural ODEs, in a paper that won best "
            "paper at NeurIPS in 2018. Depth becomes time, any solver can integrate them, and running the "
            "solver backwards inverts them: a flow, with no coupling layers needed."
        ) as vo:
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("a")
            self.play(Write(rows[1]), FadeIn(whys[1]))
            vo.wait_until("b")
            self.play(Write(rows[2]), FadeIn(whys[2]))
            vo.wait_until("c")
            self.play(FadeIn(card, shift=UP * 0.1), FadeIn(pros))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trace(self):
        rows = [
            cmath(r"\log p(z(t + \Delta t))", r"=", r"\log p(z(t))", r"-", r"\log \big|\det\big(I + \Delta t\, "
                  r"\tfrac{\partial f}{\partial z}\big)\big|", font_size=32),
            cmath(r"\log \det (I + \Delta t\, A)", r"=", r"\Delta t\, \mathrm{tr}\, A", r"+", r"O(\Delta t^2)",
                  font_size=32),
            cmath(r"\frac{d \log p(z(t))}{dt}", r"=", r"-\,\mathrm{tr}\Big(\frac{\partial f}{\partial z(t)}\Big)",
                  font_size=36),
            cmath(r"\log p(x)", r"=", r"\log p(z(0))", r"-", r"\int_0^1 \mathrm{tr}\Big(\frac{\partial f}"
                  r"{\partial z}\Big)\, dt", font_size=34),
        ]
        rows[2][2].set_color(CNF_C)
        rows[3][4].set_color(CNF_C)
        whys = [why(r"change of variables, \ one small step"), why(r"$\det(I + \epsilon A) = 1 + \epsilon\, "
                                                                 r"\mathrm{tr} A + \dots$"),
                why(r"the instantaneous change of variables"), why(r"integrate along the path")]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-1.4, buff=0.5, edge=6.9)
        cost = label(r"a trace needs only the diagonal: \ $d$ backward passes, \ not $d^3$ operations", font_size=22,
                     color=C.BITS).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How does the density change along the flow? Over one small step, by the change of variables of the "
            "last chapter: minus the log-determinant of the step's Jacobian, the identity plus delta t times the "
            "field's Jacobian. <bookmark mark='a'/> For a small step, the determinant of the identity plus a small "
            "matrix is one plus the trace, to first order. <bookmark mark='b'/> In the limit: the log-density "
            "changes at a rate of minus the trace of the field's Jacobian, its divergence. Where the flow spreads "
            "out, density falls. <bookmark mark='c'/> Integrate along the path and you have the exact "
            "log-likelihood of a continuous flow, with no restriction at all on the network. <bookmark mark='d'/> "
            "The determinant has become a trace, which needs only the diagonal of the Jacobian. But even the "
            "diagonal costs one backward pass per dimension."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(cost))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hutchinson(self):
        c = load("cnf")
        rows = [
            cmath(r"\mathbb E\big[\varepsilon^\top A\, \varepsilon\big]", r"=", r"\sum_{i, j} A_{ij}\, \mathbb E"
                  r"[\varepsilon_i \varepsilon_j]", font_size=34),
            cmath(r"\mathbb E\big[\varepsilon^\top A\, \varepsilon\big]", r"=", r"\sum_i A_{ii}", r"=",
                  r"\mathrm{tr}\, A", font_size=34),
        ]
        rows[1][4].set_color(CNF_C)
        whys = [why(r"expand the quadratic form"), why(r"if $\mathbb E[\varepsilon \varepsilon^\top] = I$")]
        step = ladder(self, rows, whys, keep=2, top=3.2, x=-2.2, buff=0.45, edge=6.9)
        var = VGroup(label(r"its variance, \ for $A$'s symmetric part $S$:", font_size=22, color=GREY_A),
                     MathTex(r"\text{Gaussian } \varepsilon: \ 2\, \|S\|_F^2 \qquad \text{Rademacher } \varepsilon "
                             r"= \pm 1: \ 2\big(\|S\|_F^2 - \textstyle\sum_i S_{ii}^2\big)", font_size=28))
        var.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-2.2, 0.6, 0])
        mg, tg_ = np.asarray(c["hv_gauss_measured"]), np.asarray(c["hv_gauss_theory"])
        mr, tr_ = np.asarray(c["hv_rad_measured"]), np.asarray(c["hv_rad_theory"])
        top = float(np.percentile(np.r_[tg_, mg], 99)) * 1.1
        g = axes([0, top], [0, top], x_length=3.4, y_length=3.0, xlabel=r"formula", ylabel=r"measured variance",
                 xticks=[0], yticks=[0], center=[-3.6, -2.0, 0])
        g.scale(0.85)
        keep = (tg_ < top) & (mg < top)
        dg = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.03, color=HUTCH) for a, b in zip(tg_[keep], mg[keep])])
        keep2 = (tr_ < top) & (mr < top)
        dr = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.03, color=C.BITS) for a, b in zip(tr_[keep2], mr[keep2])])
        diag = DashedLine(g.ax.c2p(0, 0), g.ax.c2p(top, top), color=GREY_C, stroke_width=1.5)
        lg = legend([(HUTCH, r"Gaussian probes"), (C.BITS, r"Rademacher probes")], font_size=18).next_to(g, RIGHT,
                                                                                                         buff=0.2)
        ratio = float(np.mean(mr) / max(np.mean(mg), 1e-12))
        rel_err = float(np.median(np.abs(mg - tg_) / np.maximum(tg_, 1e-12)))
        d_ = int(c["big_dim"])
        tr_ratio = float(c["big_time_ratio"])
        ex = np.asarray(c["big_exact"])
        hm, hs = np.asarray(c["big_hutch_mean"]), np.asarray(c["big_hutch_sd"])
        big = VGroup(
            label(rf"in ${d_}$ dimensions \ (a random network):", font_size=22, color=GREY_A),
            label(rf"exact trace: \ ${d_}$ backward passes; \ one probe: \ $1$", font_size=22, color=CNF_C),
            label(rf"measured here: \ one probe is ${tr_ratio:.0f}\times$ faster", font_size=22, color=CNF_C),
            label(rf"its spread, \ one probe: \ $\pm {np.median(hs):.1f}$ \ around a trace of about "
                  rf"${np.median(np.abs(ex)):.1f}$", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.4, -1.0, 0])
        cite_ = cite(r"Hutchinson (1989); \ Grathwohl et al., \textit{FFJORD} (2019)", corner=DR)
        with self.voiceover(
            "The way out is a trick from 1989, for estimating the trace of a huge matrix you can only multiply by. "
            "Draw a random vector epsilon whose entries have mean zero and variance one, and compute epsilon "
            "transpose A epsilon. <bookmark mark='a'/> Its average is the sum of A's entries times the averages of "
            "epsilon i times epsilon j, which are one on the diagonal and zero off it: the trace. One random "
            "probe, one backward pass, an unbiased estimate. That is Hutchinson's estimator. <bookmark mark='b'/> "
            "Its variance depends on the probe. For random signs it is smaller than for Gaussians, because the "
            "diagonal terms never vary. We measured both, at four hundred points of a trained flow, against the "
            f"formulas: they agree to within {100 * rel_err:.0f} percent, and the random signs' variance is "
            f"{ratio:.2f} times the Gaussians'. <bookmark mark='c'/> Will Grathwohl and colleagues built FFJORD "
            f"on it in 2019. The saving grows with dimension: in {d_} dimensions, one probe is {tr_ratio:.0f} "
            "times faster than the exact trace, here."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(var))
            self.play(FadeIn(g), Create(diag), FadeIn(dg), FadeIn(dr), FadeIn(lg))
            vo.wait_until("c")
            self.play(FadeIn(big, shift=UP * 0.1), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def training(self):
        c, t = load("cnf"), load("toys")
        E = np.array([np.asarray(c[f"exact_s{s}_curve"]) for s in range(3)])
        H = np.array([np.asarray(c[f"hutch_s{s}_curve"]) for s in range(3)])
        S = E[0, :, 0]
        h = float(t["moons_entropy"])
        top = float(math.ceil(max(E[:, :, 1].max(), H[:, :, 1].max()) * 2) / 2)
        g = axes([0, S[-1]], [h - 0.2, top], x_length=6.0, y_length=3.6, xlabel=r"training step",
                 ylabel=r"held-out NLL (nats), \ exact divergence", xticks=[0, S[-1]], yticks=[round(h, 2), top],
                 center=[-2.2, -0.3, 0])
        be = band(g.ax, S, E[:, :, 1].min(0), E[:, :, 1].max(0), EXACT, 0.25)
        bh = band(g.ax, S, H[:, :, 1].min(0), H[:, :, 1].max(0), HUTCH, 0.25)
        le, lh = curve(g.ax, S, E[:, :, 1].mean(0), EXACT, 3), curve(g.ax, S, H[:, :, 1].mean(0), HUTCH, 3)
        fl = DashedLine(g.ax.c2p(0, h), g.ax.c2p(S[-1], h), color=DATA, stroke_width=1.5)
        lg = legend([(EXACT, r"trained with the exact trace"), (HUTCH, r"trained with one Hutchinson probe"),
                     (DATA, r"the floor")], font_size=20).next_to(g, RIGHT, buff=0.3)
        fe, fh = float(E[:, -1, 1].mean()), float(H[:, -1, 1].mean())
        te = float(np.mean([c[f"exact_s{s}_secs"] for s in range(3)]))
        th = float(np.mean([c[f"hutch_s{s}_secs"] for s in range(3)]))
        gap = fh - fe
        ag = abs(gap)
        if ag < 0.05:
            verdict = (f"The two end within {ag:.2f} nats of each other: the noisy estimate trains the flow as well "
                       "as the exact trace.")
        elif gap > 0:
            verdict = f"The noisy estimate costs {ag:.2f} nats by the end."
        else:
            verdict = f"The noisy estimate even ends {ag:.2f} nats ahead."
        tg = note(r"computed: \ the moons, \ three seeds each, \ bands: \ min to max").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Here is a continuous flow trained on the two moons, both ways, three seeds each: once with the exact "
            "trace, once with a single random-sign probe per path. Both are judged the same way, with the exact "
            f"trace, on held-out points. <bookmark mark='a'/> {verdict} In two dimensions the exact trace is "
            f"cheap anyway: a run took {te:.0f} seconds with it, {th:.0f} with the estimate. In a thousand "
            "dimensions, only the estimate is affordable."
        ) as vo:
            self.play(FadeIn(g), Create(fl), FadeIn(tg), FadeIn(lg))
            self.play(FadeIn(be), Create(le), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(bh), Create(lh), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def particles(self):
        c = load("cnf")
        P = np.asarray(c["paths"])  # 41 x 1500 x 2
        D = np.asarray(c["dens_t"])  # 5 x 48 x 48
        pl = Plane(5.4, center=[-2.4, -0.1, 0])
        imgs = [pl.image(d, CNF_C, gamma=0.5) for d in D]
        for im in imgs:
            im.set_opacity(0.55)
        n = 700
        dots = VGroup(*[Dot(q, radius=0.022, color=WHITE, fill_opacity=0.85) for q in pl.pts(np.clip(P[0][:n],
                                                                                                    -2.95, 2.95))])
        t = ValueTracker(0.0)
        tv = DecimalNumber(0.0, num_decimal_places=2, font_size=34, color=CNF_C)
        tl = VGroup(MathTex(r"t =", font_size=34, color=CNF_C), tv).arrange(RIGHT, buff=0.15).move_to([3.6, 2.4, 0])
        tv.add_updater(lambda m: m.set_value(t.get_value()))

        def upd(g):
            v = t.get_value() * (len(P) - 1)
            k = min(int(v), len(P) - 2)
            a = v - k
            Q = (1 - a) * P[k][:n] + a * P[k + 1][:n]
            for d_, q in zip(g, pl.pts(np.clip(Q, -2.95, 2.95))):
                d_.move_to(q)

        expl = VGroup(label(r"dots: \ $700$ points of noise, \ carried by the learned field", font_size=20),
                      label(r"glow: \ the density at that time, \ $\log p_t$ by the trace integral", font_size=20,
                            color=CNF_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.7, 1.0, 0])
        tk = take_away(r"Next: \ Part 21's flow matching trains such a field without ever solving the ODE in "
                       r"training.", font_size=24)
        with self.voiceover(
            "And here is the flow itself. Seven hundred points of Gaussian noise at time zero, carried along by the "
            "learned field to time one; underneath, the density at each moment, computed with the trace integral. "
            "<bookmark mark='a'/> The cloud stretches, splits and curls into two moons, the density following it, "
            "conserved all the way. <bookmark mark='b'/> One cost remains: training needs the ODE solved, forward "
            "and back, at every step. Part 21 shows how to learn the same kind of field without that, by "
            "regression: flow matching."
        ) as vo:
            self.play(FadeIn(pl), FadeIn(imgs[0]), FadeIn(dots), FadeIn(tl), FadeIn(expl))
            vo.wait_until("a")
            dots.add_updater(upd)
            cur = imgs[0]
            seg = max(1.0, (vo.until("b") - 0.5) / 4)
            for k in range(1, 5):
                self.play(t.animate.set_value(k / 4), FadeTransform(cur, imgs[k]), run_time=seg, rate_func=linear)
                cur = imgs[k]
            dots.clear_updaters()
            vo.wait_until("b")
            self.play(FadeIn(tk))
        self.wait(0.3)
        self.clear_scene()
