from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.stochastic.common import (PathBundle, boxed, gauss_pdf, hist_shape, label, load, mtex, note, num, pdf_curve,
                                      polyline, tw_axes)


def sci(x: float, digits=2) -> str:
    m, e = f"{x:.{digits}e}".split("e")
    return rf"{m} \times 10^{{{int(e)}}}"


class Girsanov(VoiceoverScene):
    def construct(self):
        self.reweight()
        self.derive()
        self.risk_neutral()
        self.rare()

    # ------------------------------------------------------------------
    def reweight(self):
        d = load("girsanov")
        P = d["paths"]
        m, n1 = P.shape
        ts = np.linspace(0, 1, n1)
        W1 = P[:, -1]
        ax = tw_axes(x_length=7.6, y_range=(-3.2, 3.6, 1), y_length=5.4).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        hax = Axes(x_range=[0, 0.6, 0.2], y_range=[-3.2, 3.6, 1], x_length=2.4, y_length=5.4, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": False}).next_to(ax, RIGHT, buff=0.2)
        hax.x_axis.set_opacity(0)
        theta = ValueTracker(0.0)
        reveal = ValueTracker(0.0)
        bundle = PathBundle(ax, ts, P, (0, 1), (-3.2, 3.6))

        def weights():
            th = theta.get_value()
            return np.exp(th * W1 - 0.5 * th * th)

        def draw(_):
            w = weights()
            op = np.clip(0.11 * w / np.mean(w), 0.0, 0.85) + 0.01
            op[np.arange(m) >= reveal.get_value() * m] = 0.0
            return bundle.rgba(op)

        curves = bundle.raster(draw, [theta, reveal])

        def mean_path():
            w = weights()
            return polyline(ax, ts, (w[:, None] * P).sum(axis=0) / w.sum(), color=C.WEIGHT, stroke_width=4)

        edges = np.linspace(-3.2, 3.6, 35)
        ys = np.linspace(-3.2, 3.6, 200)

        def hist():
            w = weights()
            h, _ = np.histogram(W1, bins=edges, weights=w)
            h = h / (w.sum() * np.diff(edges))
            return hist_shape(hax, edges, np.minimum(h, 0.6), sideways=True, color=C.WEIGHT, fill_opacity=0.35)

        def bell():
            return pdf_curve(hax, ys, gauss_pdf(ys, theta.get_value(), 1.0), sideways=True, color=WHITE, stroke_width=2)

        mp, hs, bl = always_redraw(mean_path), always_redraw(hist), always_redraw(bell)
        th_val = DecimalNumber(0, num_decimal_places=2, font_size=36, color=C.WEIGHT)
        th_val.add_updater(lambda v: v.set_value(theta.get_value()))
        th_lab = VGroup(MathTex(r"\theta =", font_size=36, color=C.WEIGHT), th_val).arrange(RIGHT, buff=0.12)
        Z = MathTex(r"Z", r"=", r"e^{\,\theta W_1 - \frac12\theta^2}", font_size=40)
        Z[0].set_color(C.WEIGHT)
        Z[2].set_color(C.WEIGHT)
        side = VGroup(Z, th_lab).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UR, buff=0.5)
        rule = label(r"each path drawn with\\opacity $\propto$ its weight $Z$", font_size=24, color=GREY_B,
                     tex_environment="flushleft")
        rule.next_to(side, DOWN, buff=0.3).align_to(side, LEFT)
        meanl = label(r"weighted average path", font_size=24, color=C.WEIGHT).next_to(rule, DOWN, buff=0.25).align_to(side, LEFT)
        slope = label(r"$\to$ the line $\theta\, t$", font_size=24, color=C.WEIGHT).next_to(meanl, DOWN, buff=0.1).align_to(side, LEFT)
        histl = label(r"weighted histogram\\of $W_1$: \ $\mathcal N(\theta, 1)$", font_size=24, color=GREY_A,
                      tex_environment="flushleft")
        histl.next_to(slope, DOWN, buff=0.25).align_to(side, LEFT)
        textcol = VGroup(side, rule, meanl, slope, histl)
        textcol.shift(RIGHT * (hax.get_right()[0] + 0.35 - textcol.get_left()[0]))
        sim = note(r"2{,}000 simulated paths").to_corner(DR, buff=0.3)
        # the weighted mean of W_1 tracks theta (asserted in compute.py, with the effective sample size)

        with self.voiceover(
            "One last idea, and it's a strange one: change the probabilities, not the paths. <bookmark mark='p'/> Here "
            "are two thousand Brownian paths, all equally likely. <bookmark mark='w'/> Now give each path a weight, Z, "
            "equal to e to the theta W at time one, minus one half theta squared, and draw it with opacity proportional "
            "to its weight."
        ) as vo:
            self.play(Create(ax), FadeIn(ax.x_labels))
            vo.wait_until("p")
            self.play(FadeIn(sim))
            self.add(curves)
            self.play(reveal.animate.set_value(1.0), run_time=2, rate_func=linear)
            vo.wait_until("w")
            self.play(Write(Z), FadeIn(th_lab), FadeIn(rule))
        with self.voiceover(
            "Turn up theta. <bookmark mark='u'/> Paths that end high get heavier; paths that end low fade away. "
            "<bookmark mark='m'/> The weighted average path tilts up into a straight line of slope theta, "
            "<bookmark mark='h'/> and the weighted distribution of where the paths end slides over to a bell curve "
            "centered at theta. <bookmark mark='d'/> Under the new weights, W looks exactly like Brownian motion with drift "
            "theta. Turn theta negative, and the drift goes down."
        ) as vo:
            vo.wait_until("u")
            self.play(theta.animate.set_value(0.8), run_time=vo.until("m"), rate_func=smooth)
            self.add(mp)
            self.play(FadeIn(meanl), FadeIn(slope), theta.animate.set_value(1.0), run_time=vo.until("h"))
            self.add(hs, bl)
            self.play(FadeIn(histl), Create(hax.y_axis), theta.animate.set_value(1.2), run_time=vo.until("d"))
            self.play(theta.animate.set_value(-1.0), run_time=vo.remaining() + 0.5, rate_func=smooth)
            self.play(theta.animate.set_value(1.0), run_time=1.5, rate_func=smooth)
        self.wait(0.3)
        th_val.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        l1 = MathTex(r"\frac{\text{density of } \Delta W \text{ with drift } \theta}{\text{density of } \Delta W \text{ without}}",
                     r"=", r"\frac{e^{-(\Delta W - \theta\Delta t)^2 / 2\Delta t}}{e^{-(\Delta W)^2 / 2\Delta t}}", r"=",
                     r"e^{\,\theta\,\Delta W - \frac12\theta^2\,\Delta t}", font_size=36)
        l1[4].set_color(C.WEIGHT)
        l2 = MathTex(r"\prod_i e^{\,\theta\,\Delta W_i - \frac12\theta^2\,\Delta t}", r"=", r"e^{\,\theta W_T - \frac12\theta^2 T}",
                     r"=", r"Z_T", font_size=40)
        l2[2].set_color(C.WEIGHT)
        l2[4].set_color(C.WEIGHT)
        n2 = label(r"independent steps: the ratios multiply", font_size=24, color=GREY_B)
        l3 = MathTex(r"dZ", r"=", r"\big(-\tfrac12\theta^2 + \tfrac12\theta^2\big)\,Z\,dt", r"+", r"\theta Z\,dW", r"=",
                     r"\theta Z\,dW", font_size=38)
        l3[2].set_color(C.QV)
        l3[6].set_color(C.WEIGHT)
        n3 = label(r"It\^o: the $-\tfrac12\theta^2$ exactly cancels the curvature term, so $Z$ is a martingale with mean 1",
                   font_size=24, color=GREY_B)
        col = VGroup(l1, VGroup(l2, n2).arrange(DOWN, buff=0.1), VGroup(l3, n3).arrange(DOWN, buff=0.1)).arrange(DOWN, buff=0.5)
        col.to_edge(UP, buff=0.4)
        thm = label(r"\textbf{Girsanov's theorem:} \ reweight probabilities by $Z_T$, \ and \ $\widetilde W_t = W_t - \theta t$ \ "
                    r"is a Brownian motion.", font_size=30)
        thb = boxed(thm, color=C.WEIGHT, buff=0.25).to_edge(DOWN, buff=0.6)
        cred = note(r"Cameron and Martin (1944); Girsanov (1960), for drifts that change with the path").next_to(thb, DOWN, buff=0.12)
        with self.voiceover(
            "Where does that weight come from? <bookmark mark='a'/> Compare the bell curve for one step with drift theta "
            "to the one without. Their ratio is e to the theta delta W, minus one half theta squared delta t. "
            "<bookmark mark='b'/> The steps are independent, so for a whole path the ratios multiply, and the exponents "
            "add up to theta W at time T minus one half theta squared T."
        ) as vo:
            self.play(Write(l1), run_time=3)
            vo.wait_until("b")
            self.play(Write(l2), FadeIn(n2))
        with self.voiceover(
            "And that minus one half theta squared is Itô's correction yet again. <bookmark mark='c'/> Apply Itô's lemma to "
            "Z: the minus one half theta squared from the time derivative exactly cancels the plus one half theta squared "
            "from the curvature, so Z has no drift. It's a martingale, with average one, which makes it a legitimate way "
            "to reweight probabilities."
        ) as vo:
            vo.wait_until("c")
            self.play(Write(l3), FadeIn(n3))
        with self.voiceover(
            "That's Girsanov's theorem: <bookmark mark='t'/> reweighting by Z turns W into a Brownian motion with drift "
            "theta, or, equivalently, W minus theta t into a standard Brownian motion. Changing the drift is the same as "
            "changing the odds."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(thm), Create(thb[0]), FadeIn(cred))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def risk_neutral(self):
        real = MathTex(r"dS", r"=", r"\mu S\,dt", r"+", r"\sigma S\,dW", font_size=42)
        real[2].set_color(C.DRIFT)
        real[4].set_color(C.BROWNIAN)
        sub = MathTex(r"W_t", r"=", r"\widetilde W_t", r"+", r"\theta t", r",\qquad", r"\theta = \frac{r - \mu}{\sigma}",
                      font_size=38)
        sub[4].set_color(C.WEIGHT)
        sub[6].set_color(C.WEIGHT)
        rn = MathTex(r"dS", r"=", r"r S\,dt", r"+", r"\sigma S\,d\widetilde W", font_size=42)
        rn[2].set_color(C.DRIFT)
        rn[4].set_color(C.BROWNIAN)
        col = VGroup(VGroup(label(r"the real world:", font_size=28, color=GREY_A), real).arrange(RIGHT, buff=0.4),
                     sub,
                     VGroup(label(r"reweighted:", font_size=28, color=GREY_A), rn).arrange(RIGHT, buff=0.4))
        col.arrange(DOWN, buff=0.55).move_to(UP * 0.5)
        msg = label(r"Black--Scholes' ``as if the stock grew at $r$'' is a change of measure", font_size=30, color=C.OPTION)
        msg.next_to(col, DOWN, buff=0.6)
        mpr = note(r"$-\theta = (\mu - r)/\sigma$ is the market price of risk").next_to(msg, DOWN, buff=0.2)
        with self.voiceover(
            "This explains the strangest step in Black–Scholes. <bookmark mark='a'/> In the real world, the stock drifts "
            "at mu. <bookmark mark='b'/> Reweight with theta equal to r minus mu, over sigma, <bookmark mark='c'/> and "
            "under the new probabilities, the stock drifts at exactly the risk-free rate. <bookmark mark='d'/> That's the "
            "risk-neutral world, where the option price is a plain discounted average. It isn't an assumption about "
            "investors: it's Girsanov's theorem."
        ) as vo:
            self.play(FadeIn(col[0]))
            vo.wait_until("b")
            self.play(Write(sub))
            vo.wait_until("c")
            self.play(FadeIn(col[2]))
            vo.wait_until("d")
            self.play(FadeIn(msg), FadeIn(mpr))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rare(self):
        exact, hits, plain, est, se = (float(x) for x in load("girsanov")["is_stats"])
        assert int(hits) == 1 and round(exact * 1e5, 2) == 3.17 and round(est * 1e5, 2) == 3.24
        ax = Axes(x_range=[-4, 8, 2], y_range=[0, 0.45, 0.1], x_length=10.5, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(DOWN * 1.3)
        ticks = VGroup(*[MathTex(f"{v}", font_size=24).next_to(ax.c2p(v, 0), DOWN, buff=0.1) for v in (-4, 0, 4, 8)])
        xs = np.linspace(-4, 8, 400)
        p0 = ax.plot_line_graph(xs, gauss_pdf(xs, 0, 1), add_vertex_dots=False, line_color=C.BROWNIAN, stroke_width=3)
        p4 = ax.plot_line_graph(xs, gauss_pdf(xs, 4, 1), add_vertex_dots=False, line_color=C.WEIGHT, stroke_width=3)
        cut = DashedLine(ax.c2p(4, 0), ax.c2p(4, 0.45), color=C.QV, stroke_width=2.5)
        cutl = MathTex(r"W_1 > 4", font_size=30, color=C.QV).next_to(ax.c2p(4, 0.45), UP, buff=0.08)
        tail = ax.get_area(ax.plot(lambda x: gauss_pdf(x, 4, 1), x_range=[4, 8]), x_range=[4, 8], color=C.WEIGHT, opacity=0.35)
        rows = VGroup(
            MathTex(r"\text{exact: }", r"P(W_1 > 4) = " + sci(exact), font_size=34),
            MathTex(r"\text{plain Monte Carlo, } 100{,}000 \text{ paths: }", r"1 \text{ hit} \;\Rightarrow\; " + sci(plain, 1),
                    font_size=34),
            MathTex(r"\text{tilted by } \theta = 4,\ 10{,}000 \text{ paths, reweighted: }", sci(est) + r" \pm " + sci(se, 1),
                    font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(UP, buff=0.5)
        rows[1][1].set_color(C.BROWNIAN)
        rows[2][1].set_color(C.WEIGHT)
        wl = label(r"weight per path: $e^{-4 W_1 + 8}$", font_size=26, color=C.WEIGHT).next_to(ax.c2p(6.2, 0.3), UP, buff=0.0)
        with self.voiceover(
            "Changing the odds is also a practical tool. Suppose you need the probability of a rare event: "
            "<bookmark mark='e'/> say, Brownian motion ending above four at time one. The exact answer is about three in a "
            "hundred thousand. <bookmark mark='p'/> Simulate a hundred thousand paths, and you'll see it about three "
            "times. We saw it once: an estimate off by a factor of three."
        ) as vo:
            self.play(Create(ax), FadeIn(ticks), Create(p0))
            vo.wait_until("e")
            self.play(FadeIn(rows[0]), Create(cut), FadeIn(cutl))
            vo.wait_until("p")
            self.play(FadeIn(rows[1]))
        with self.voiceover(
            "Instead, <bookmark mark='t'/> simulate with a drift of four, so half the paths land in the rare region, "
            "<bookmark mark='w'/> and undo the change by weighting each path with Girsanov's factor. <bookmark mark='r'/> "
            "Ten thousand tilted paths give 3.24 times ten to the minus five, within about two percent of the truth. This is "
            "importance sampling, and it's how banks and engineers estimate the probability of disasters."
        ) as vo:
            vo.wait_until("t")
            self.play(Create(p4), FadeIn(tail))
            vo.wait_until("w")
            self.play(FadeIn(wl))
            vo.wait_until("r")
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()
