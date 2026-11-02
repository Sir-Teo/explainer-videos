from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, pause

PCOL, QCOL = QC.P, QC.Q


class Girsanov(VoiceoverScene):
    def construct(self):
        g = load("girsanov_paths")
        self.card()
        self.reweight(g)
        self.proof()
        self.collapse(g)

    def card(self):
        c = chapter_card(8, r"Girsanov: re-weighting paths", r"Is drift just a change of measure?", part=PART)
        with self.voiceover("Chapter eight. Girsanov's theorem: re-weighting paths."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def _hist(self, ax, edges, h, color, x0):
        w = edges[1] - edges[0]
        hmax = 0.5
        return VGroup(*[Rectangle(width=max(1.3 * v / hmax, 0.002), height=ax.c2p(0, w)[1] - ax.c2p(0, 0)[1] - 0.005,
                                  stroke_width=0, fill_color=color, fill_opacity=0.75)
                        .move_to([x0 + 1.3 * v / hmax / 2, ax.c2p(0, e + w / 2)[1], 0])
                        for e, v in zip(edges[:-1], np.minimum(h, hmax)) if e + w / 2 > -3 and e + w / 2 < 4])

    def reweight(self, g):
        W = np.asarray(g["W"])
        Z = np.asarray(g["Z"])
        t = np.linspace(0, 1, W.shape[1])
        th = g["theta"]
        e = np.asarray(g["edges"])
        g1 = axes([0, 1], [-3, 4], x_length=4.6, y_length=4.4, xlabel=r"time", ylabel=r"the same 300 paths, re-weighted",
                  xticks=[0, 1], yticks=[-2, 0, 2, 4], font_size=15)
        g2 = axes([0, 1], [-3, 4], x_length=4.6, y_length=4.4, xlabel=r"time", ylabel=r"300 paths, moved: $W_t + \theta t$",
                  xticks=[0, 1], yticks=[-2, 0, 2, 4], font_size=15)
        VGroup(g1, g2).arrange(RIGHT, buff=2.4).to_edge(LEFT, buff=0.5).shift(DOWN * 0.4)
        a1, a2 = g1.ax, g2.ax
        paths = VGroup(*[VMobject(stroke_width=1.2, stroke_color=PCOL, stroke_opacity=0.35).set_points_as_corners(
            [a1.c2p(x, np.clip(y, -3, 4)) for x, y in zip(t, row)]) for row in W])
        wn = Z / Z.max()
        moved = VGroup(*[VMobject(stroke_width=1.2, stroke_color=QCOL, stroke_opacity=0.35).set_points_as_corners(
            [a2.c2p(x, np.clip(y + th * x, -3, 4)) for x, y in zip(t, row)]) for row in W])
        x1 = a1.get_right()[0] + 0.1
        x2 = a2.get_right()[0] + 0.1
        hp = self._hist(a1, e, np.asarray(g["h_p"]), PCOL, x1)
        hq = self._hist(a1, e, np.asarray(g["h_q"]), QCOL, x1)
        hm = self._hist(a2, e, np.asarray(g["h_moved"]), QCOL, x2)
        z = MathTex(r"Z_T = e^{\theta W_T - \theta^2 T/2}", font_size=32, color=QCOL).to_corner(UL, buff=0.35)
        tk = ValueTracker(0)
        thr = always_redraw(lambda: MathTex(rf"\theta = {tk.get_value():.2f}", font_size=30, color=QCOL)
                            .next_to(z, RIGHT, buff=0.6))
        res = MathTex(rf"\textstyle\sum Z\,W_T / \sum Z = {g['wmean']:.3f} \quad (\theta T = {th:.0f})", font_size=28,
                      color=QCOL).to_corner(UR, buff=0.35)
        with self.voiceover(
            "Here is the theorem as a picture. Three hundred Brownian paths with no drift, in amber, the colour of the "
            "real-world measure P. Their endpoints stand in a histogram on the right: a Gaussian centred at zero. "
            "<bookmark mark='a'/> Now turn a dial theta from zero to one. The paths do not move. Instead each path's "
            "weight becomes Z: the exponential of theta times its endpoint, minus a half theta squared. Paths that "
            "ended high get heavier and turn violet, the colour of the new measure Q; paths that ended low fade. "
            "<bookmark mark='b'/> The weighted histogram slides to the right, to a Gaussian centred at theta. "
            f"Over two hundred thousand paths, the weighted mean endpoint is {g['wmean']:.3f}. <bookmark mark='c'/> "
            "On the right, the honest way to get drift: move every path up by theta t. Its histogram is the same "
            "Gaussian. Moving paths and re-weighting them give the same distribution. Under Q, the original, "
            "unmoved paths are a Brownian motion with drift theta."
        ) as vo:
            self.play(FadeIn(g1), LaggedStart(*[Create(p) for p in paths], lag_ratio=0.003, run_time=3), FadeIn(z))
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in hp], lag_ratio=0.03))
            vo.wait_until("a")
            self.add(thr)
            anims = [p.animate.set_stroke(color=interpolate_color(ManimColor(PCOL), ManimColor(QCOL), float(min(w * 3, 1))),
                                          opacity=float(0.04 + 0.9 * w)) for p, w in zip(paths, wn)]
            self.play(tk.animate.set_value(th), *anims, run_time=4)
            vo.wait_until("b")
            self.play(ReplacementTransform(hp, hq), FadeIn(res), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(g2), LaggedStart(*[Create(p) for p in moved], lag_ratio=0.003, run_time=3))
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in hm], lag_ratio=0.03))
        thr.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        rows = [cmath(r"\frac{dQ}{dP}", r"=", r"\prod_k \frac{q(\Delta W_k)}{p(\Delta W_k)} = \exp\Big(\sum_k \theta\,\Delta W_k - "
                      r"\tfrac12 \theta^2 \Delta t_k\Big)", font_size=30),
                cmath(r"Z_t", r"=", r"\exp\Big(\int_0^t \theta\,dW - \tfrac12\int_0^t \theta^2\,ds\Big), \quad dZ = \theta Z\,dW",
                      font_size=30, colors={r"dZ = \theta Z\,dW": QCOL}),
                cmath(r"d(Z\widetilde W)", r"=", r"Z\,d\widetilde W + \widetilde W\,dZ + d\langle Z, \widetilde W\rangle "
                      r"= Z(1 + \theta\widetilde W)\,dW", font_size=30),
                cmath(r"\widetilde W = W - \int_0^\cdot \theta\,ds", r"\text{ is a }", r"Q\text{-Brownian motion}",
                      font_size=32, colors={r"Q\text{-Brownian motion}": QCOL}),
                cmath(r"\mathbb{E}\,e^{\frac12 \int_0^T \theta^2\,dt} < \infty", r"\Rightarrow", r"\mathbb{E}\,Z_T = 1",
                      font_size=32)]
        whys = [why(r"Part 4's coin: the ratio of two Gaussian densities; complete the square"),
                why(r"the continuous limit; by the lemma, $Z$ is the stochastic exponential of $\int \theta\,dW$"),
                why(r"the product rule: $-Z\theta\,dt$ from $d\widetilde W$ cancels $+\theta Z\,dt$ from the covariation"),
                why(r"so $Z\widetilde W$ is a $P$-martingale, i.e.\ $\widetilde W$ a $Q$-martingale (Bayes); "
                    r"$\langle \widetilde W\rangle_t = t$; by L\'evy's characterization, a Brownian motion"),
                why(r"Novikov (1972); without it $Z$ is only a supermartingale, and $Q$ loses mass")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-1.3, buff=0.55, edge=6.9)
        th = theorem_card(r"Cameron--Martin and Girsanov", r"Cameron and Martin (1944): shifting Wiener measure by a "
                          r"smooth deterministic path $h$ multiplies it by $e^{\int h'\,dW - \frac12\int h'^2}$. "
                          r"Girsanov (1960): the same for an adapted drift $\theta_t$.", color=QCOL, width=6.0,
                          font_size=19).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The proof starts where Part four left off, with a coin. On a grid, the likelihood ratio of a drifting "
            "Brownian path against a driftless one is a product of ratios of Gaussian densities; completing the square "
            "gives an exponential of theta times the increments, minus a half theta squared times the steps. "
            "<bookmark mark='a'/> In the limit that is Z, and by the lemma it solves d Z equals theta Z d W: a "
            "stochastic exponential, a martingale. Cameron and Martin had this in 1944 for deterministic shifts. "
            "<bookmark mark='b'/> Girsanov's step: subtract the drift from W and multiply by Z. By the product rule, "
            "the drift from the subtraction cancels the drift from the covariation exactly. <bookmark mark='c'/> So "
            "Z times W tilde is a martingale under P, which by Bayes's rule means W tilde is a martingale under Q; its "
            "quadratic variation is still t, and by Lévy's characterization it is a Brownian motion. "
            "<bookmark mark='d'/> One condition: Z must have mean one. Novikov's condition guarantees it. Without it, "
            "Z can be a strict supermartingale and Q is not a probability at all."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            self.play(FadeIn(th))
            vo.wait_until("b")
            self.play(FadeOut(th))
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.5)
        self.clear_scene()

    def collapse(self, g):
        ess = g["ess"]
        bars_ax = axes([-0.6, 3.6], [-8, 0.3], x_length=6.0, y_length=4.0, xlabel=r"horizon $T$",
                       ylabel=r"effective sample size, share of $10^5$ (log scale)", xticks=[0, 1, 2, 3],
                       xfmt=lambda u: str([1, 4, 16, 64][int(u)]), yticks=[-8, -6, -4, -2, 0],
                       yfmt=lambda u: rf"10^{{{int(u)}}}" if u else "1", font_size=16).to_edge(LEFT, buff=0.6)
        bars_ax.shift(DOWN * 0.3)
        ax = bars_ax.ax
        meas = VGroup(*[Dot(ax.c2p(i, np.log10(max(e["ess"], 1e-8))), radius=0.09, color=QCOL) for i, e in enumerate(ess)])
        theo = curve(ax, np.linspace(0, 3, 50), np.log10(np.exp(-0.25 * 4 ** np.linspace(0, 3, 50))), GREY_A,
                     stroke_width=2.5)
        floor = DashedLine(ax.c2p(-0.6, -5), ax.c2p(3.6, -5), color=JUMP, stroke_width=1.5)
        fl = label(r"one path in $10^5$", font_size=16, color=JUMP).next_to(ax.c2p(3.6, -5), UP, buff=0.05).align_to(
            ax.c2p(3.6, -5), RIGHT)
        rows = VGroup(*[MathTex(rf"T = {e['T']}:\ \ \text{{ESS}} = {e['ess']:.3g},\ \ \textstyle\frac1N\sum Z = "
                                rf"{e['mean_w']:.3f}", font_size=24, color=GREY_A) for e in ess])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        side = VGroup(MathTex(r"\text{ESS} = \frac{(\sum Z)^2}{\sum Z^2} \approx N e^{-\theta^2 T}", font_size=30,
                              color=QCOL), rows,
                      wrapped_label(r"on $[0, \infty)$, $P$ and $Q$ are singular: $W_t / t \to 0$ under $P$ and "
                                    r"$\to \theta$ under $Q$, an event of probability one for one and zero for the other",
                                    5.0, 19, JUMP)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        pc, ans = pause(r"Under $P$, what is $\mathbb{E}[Z_T]$?", rf"1, if Novikov holds. Measured at $T = 1$: "
                        rf"{g['EZ']:.4f}; at $T = 64$ with $\theta = 0.5$: {ess[-1]['mean_w']:.2f}.", width=5.6,
                        font_size=21)
        pc.to_corner(UL, buff=0.3)
        ans.next_to(pc, DOWN, buff=0.15).align_to(pc, LEFT)
        with self.voiceover(
            "When does it fail? A pause first: under P, what is the expected value of Z? <bookmark mark='a'/> One, "
            f"when Novikov's condition holds, and a hundred thousand samples at T equals one give {g['EZ']:.4f}. "
            "<bookmark mark='b'/> But let the horizon grow, with theta a half. The effective sample size, the number "
            "of paths that really carry weight, falls like e to the minus theta squared T. "
            f"At T equals sixteen, {100 * ess[2]['ess']:.1f} percent of the paths carry the weight. At sixty-four, "
            "theory says a ten-millionth, fewer than one path in our sample: the measured weights no longer even "
            f"average one, but {ess[-1]['mean_w']:.2f}. <bookmark mark='c'/> On an infinite horizon the two "
            "measures are singular: under P the average slope of the path goes to zero, under Q to theta, and a "
            "single infinitely long path tells you which world you are in. Girsanov works on finite horizons, which "
            "is all pricing needs, and the next chapter puts it to work."
        ) as vo:
            self.play(FadeIn(pc))
            vo.wait_until("a")
            self.play(FadeIn(ans))
            vo.wait_until("b")
            self.play(FadeIn(bars_ax), Create(theo), Create(floor), FadeIn(fl), FadeIn(side[0]))
            for i in range(len(ess)):
                self.play(FadeIn(meas[i], scale=1.5), FadeIn(rows[i]), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
