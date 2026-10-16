from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import ALPHA27, letter, load, plain_axes, polyline


def slivers(p, h, W=11.0, y0=-2.5, scale=0.3, order=None, color=C.SURPRISE, opacity=0.8) -> VGroup:
    """Rectangles of width W p[i] and height scale * h[i], laid out in ``order``; ``g[i]`` is symbol i's."""
    order = list(range(len(p))) if order is None else list(order)
    rects, cum = {}, 0.0
    for i in order:
        r = Rectangle(width=max(W * p[i], 0.003), height=max(scale * h[i], 0.003), stroke_width=0.8,
                      stroke_color=BACKGROUND, fill_color=color, fill_opacity=opacity)
        r.move_to([-W / 2 + (cum + p[i] / 2) * W, y0 + scale * h[i] / 2, 0])
        rects[i] = r
        cum += p[i]
    return VGroup(*[rects[i] for i in range(len(p))])


def heat_image(Z, cmap_stops, vmin, vmax, width, height) -> ImageMobject:
    """A heatmap of Z (rows = y from bottom to top) as an image, log-scaled between vmin and vmax."""
    t = np.clip((np.log(Z) - math.log(vmin)) / (math.log(vmax) - math.log(vmin)), 0, 1)
    cols = np.array([ManimColor(c).to_rgb() for c in cmap_stops])
    pos = np.linspace(0, 1, len(cols))
    rgb = np.stack([np.interp(t, pos, cols[:, k]) for k in range(3)], -1)
    img = (rgb[::-1] * 255).astype(np.uint8)
    img = np.repeat(np.repeat(img, 6, 0), 6, 1)
    m = ImageMobject(img)
    m.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    m.stretch_to_fit_width(width).stretch_to_fit_height(height)
    return m


class CrossEntropy(VoiceoverScene):
    def construct(self):
        self.card()
        self.wrong_code()
        self.decompose()
        self.gibbs()
        self.loss()
        self.asymmetry()
        self.landscape()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(5, r"Cross-entropy and KL: the price of a wrong model",
                            r"What does guessing with the wrong probabilities cost?", lit=(1948, 1951), part=1)
        with self.voiceover("Chapter five. What happens when your guesses are wrong?") as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def wrong_code(self):
        lt = load("letters")
        p = np.asarray(lt["p"])
        order = list(lt["order"])
        ie, iz = ALPHA27.index("e"), ALPHA27.index("z")
        q = p.copy()
        q[ie], q[iz] = p[iz], p[ie]  # a model that has e and z the wrong way round
        H = float(-(p * np.log2(p)).sum())
        CE = float(-(p * np.log2(q)).sum())
        KL = CE - H
        assert abs(H - 4.084) < 0.001 and abs(CE - 4.84) < 0.005 and abs(KL - 0.75) < 0.005, CE
        self.H, self.CE, self.KL = H, CE, KL
        head = mtex([r"H(p, q)", r"=", r"\sum_x p(x)\, \log_2 \frac{1}{q(x)}"], font_size=42).to_edge(UP, buff=0.4)
        head[0].set_color(C.MODEL_Q)
        sub = label(r"\textit{cross-entropy}: \ the data come from $p$, \ the code was built for $q$", font_size=26,
                    color=GREY_A).next_to(head, DOWN, buff=0.2)
        W, y0, sc = 11.0, -2.6, 0.27
        true = slivers(p, -np.log2(p), W=W, y0=y0, scale=sc, order=order, color=C.TRUE_P, opacity=0.75)
        wrong = slivers(p, -np.log2(q), W=W, y0=y0, scale=sc, order=order, color=C.MODEL_Q, opacity=0.18)
        wrong.set_stroke(C.MODEL_Q, width=2, opacity=1)
        base = Line([-W / 2, y0, 0], [W / 2, y0, 0], color=GREY_C, stroke_width=1.5)
        e_lab = letter("e", font_size=24, color=C.MODEL_Q).next_to(wrong[ie], UP, buff=0.08)
        z_lab = letter("z", font_size=24, color=C.MODEL_Q).next_to(wrong[iz], UP, buff=0.08)
        legend = VGroup(
            label(rf"coded for the true frequencies $p$: \ area $= H(p) = {H:.2f}$ bits", font_size=24, color=C.TRUE_P),
            label(rf"coded for a model $q$ that swaps \texttt{{e}} and \texttt{{z}}: \ area $= {CE:.2f}$ bits",
                  font_size=24, color=C.MODEL_Q),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-1.2, 1.15, 0])
        with self.voiceover(
            "Codes and guesses are the same thing. A code that spends l bits on a symbol is betting that the "
            "symbol has probability two to the minus l. So what if the bets are wrong? <bookmark mark='a'/> Say "
            "the data come from p, but the code was built for a model q. Each symbol costs log of one over q bits, "
            "and on average we pay the cross-entropy: the sum of p times log one over q."
        ) as vo:
            self.play(FadeIn(head[0]), FadeIn(head[1:]))
            vo.wait_until("a")
            self.play(FadeIn(sub))
        with self.voiceover(
            "Picture it as before. <bookmark mark='a'/> With the right probabilities, the area is the entropy, "
            "4.08 bits. <bookmark mark='b'/> Now use a model that has e and z the wrong way round. Every e, one "
            "symbol in ten, now costs almost eleven bits. The area grows to 4.84."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(base), FadeIn(true), FadeIn(legend[0]))
            vo.wait_until("b")
            self.play(FadeIn(wrong), FadeIn(legend[1]), FadeIn(e_lab), FadeIn(z_lab), run_time=1.5)
        self.parts = VGroup(head, sub, true, wrong, base, legend, e_lab, z_lab)

    # ------------------------------------------------------------------
    def decompose(self):
        lt = load("letters")
        H, CE, KL = self.H, self.CE, self.KL
        rows = [
            mtex([r"H(p, q)", r"=", r"\sum_x p(x) \log_2 \frac{1}{p(x)}", r"+", r"\sum_x p(x) \log_2 \frac{p(x)}{q(x)}"],
                 font_size=38),
            mtex([r"H(p, q)", r"=", r"H(p)", r"+", r"D_{\mathrm{KL}}(p \,\|\, q)"], font_size=44),
        ]
        for r in rows:
            r[0].set_color(C.MODEL_Q)
        rows[1][2].set_color(C.ENTROPY)
        rows[1][4].set_color(C.KL)
        g = VGroup(*rows).arrange(DOWN, buff=0.5).move_to(UP * 1.4)
        b1 = Brace(rows[1][2], DOWN, color=C.ENTROPY)
        b2 = Brace(rows[1][4], DOWN, color=C.KL)
        t1 = label(r"the price of the world's\\ own randomness", font_size=24, color=C.ENTROPY).next_to(b1, DOWN)
        t2 = label(r"the price of being wrong:\\ the Kullback--Leibler divergence", font_size=24, color=C.KL)
        t2.next_to(b2, DOWN)
        t1.shift(LEFT * max(0.0, t1.get_right()[0] - t2.get_left()[0] + 0.4))
        nums = VGroup(
            label(rf"swapped \texttt{{e}}, \texttt{{z}}: \ ${CE:.2f} = {H:.2f} + {KL:.2f}$", font_size=26),
            label(r"letters guessed uniformly: \ $4.75 = 4.07 + 0.69$ \ (the Falcon passage)", font_size=26),
            label(rf"letter frequencies of the $30$ books, used on the passage: \ $D_{{\mathrm{{KL}}}} = "
                  rf"{lt['KL_books']:.3f}$", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        assert abs(lt["H_passage"] - 4.066) < 0.001 and abs(lt["KL_uniform"] - 0.689) < 0.001
        assert abs(lt["KL_books"] - 0.009) < 0.001
        with self.voiceover(
            "Split the log in two, <bookmark mark='a'/> and the cross-entropy separates into two prices. The first "
            "is the entropy of p: the randomness of the world itself, which no code can remove. "
            "<bookmark mark='b'/> The second is the price of being wrong: the Kullback–Leibler divergence of q from "
            "p, introduced in 1951. <bookmark mark='c'/> Swapping e and z costs three quarters of a bit per symbol. Guessing "
            "letters uniformly costs 0.69. And the letter frequencies of our thirty books, used on the Falcon "
            "passage, are wrong by less than a hundredth of a bit."
        ) as vo:
            self.play(FadeOut(self.parts))
            self.play(Write(rows[0]))
            vo.wait_until("a")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]))
            self.play(GrowFromCenter(b1), FadeIn(t1))
            vo.wait_until("b")
            self.play(GrowFromCenter(b2), FadeIn(t2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.5), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gibbs(self):
        head = label(r"Gibbs' inequality: \ $D_{\mathrm{KL}}(p \,\|\, q) \ge 0$", font_size=38).to_edge(UP, buff=0.35)
        ax = plain_axes([0, 3, 1], [-2.5, 2, 1], 5.0, 3.8).shift(LEFT * 3.8 + DOWN * 0.15)
        xs = np.linspace(0.08, 3, 300)
        ln = polyline(ax, xs, np.log(xs), color=C.KL, stroke_width=4)
        tan = polyline(ax, np.linspace(0, 3, 2), np.linspace(0, 3, 2) - 1, color=GREY_A, stroke_width=3)
        lab_ln = MathTex(r"\ln x", font_size=30, color=C.KL).next_to(ax.c2p(3, math.log(3)), RIGHT, buff=0.1)
        lab_t = MathTex(r"x - 1", font_size=30, color=GREY_A).next_to(ax.c2p(2.9, 1.9), LEFT, buff=0.1)
        touch = Dot(ax.c2p(1, 0), radius=0.07, color=WHITE)
        touch_l = MathTex(r"x = 1", font_size=24, color=WHITE).next_to(touch, DOWN + RIGHT, buff=0.1)
        rows = [
            mtex([r"-D_{\mathrm{KL}}", r"=", r"\sum_x p(x)\, \ln \frac{q(x)}{p(x)}"], font_size=32),
            mtex([r"-D_{\mathrm{KL}}", r"\le", r"\sum_x p(x) \Big( \frac{q(x)}{p(x)} - 1 \Big)"], font_size=32),
            mtex([r"-D_{\mathrm{KL}}", r"\le", r"\sum_x q(x) - \sum_x p(x)"], font_size=32),
            mtex([r"-D_{\mathrm{KL}}", r"\le", r"1 - 1 = 0"], font_size=32),
        ]
        whys = [why(r"in nats (natural logs)"), why(r"$\ln x \le x - 1$"), why(r"multiply out"),
                why(r"both are distributions")]
        step = ladder(self, rows, whys, keep=3, top=2.45, x=2.6, buff=0.3)
        res = VGroup(
            label(r"equality only when $q = p$: \ the truth is the best code", font_size=28, color=C.BITS),
            label(r"so $H(p, q) \ge H(p)$, \ and $H(Y) - H(Y \mid X) = D_{\mathrm{KL}}\big(p(x, y) \,\|\, p(x)p(y)\big) "
                  r"\ge 0$", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.14)
        mi = label(r"(that last quantity is the \textit{mutual information} $I(X; Y)$: \ Chapter 10)", font_size=22,
                   color=GREY_B)
        VGroup(res, mi).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Is being wrong always a cost? Yes, and the proof rests on one fact: <bookmark mark='a'/> the natural "
            "log lies below its tangent line at one. ln x is at most x minus one. <bookmark mark='b'/> Write minus "
            "the divergence in natural logs, <bookmark mark='c'/> apply that inequality to each term, "
            "<bookmark mark='d'/> multiply out, <bookmark mark='e'/> and both sums are one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), Create(ln), Create(tan), FadeIn(lab_ln), FadeIn(lab_t), FadeIn(touch), FadeIn(touch_l))
            for k, mark in enumerate("bcde"):
                vo.wait_until(mark)
                step(k)
        with self.voiceover(
            "So the divergence is never negative, and it's zero only when q equals p. <bookmark mark='a'/> The "
            "truth is the best code. And this pays the debt from chapter three: <bookmark mark='b'/> the drop in "
            "entropy from knowing X is a divergence too, so it can't be negative. Knowing more never hurts, on "
            "average."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(res[0]))
            vo.wait_until("b")
            self.play(FadeIn(res[1]), FadeIn(mi))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def loss(self):
        head = label(r"Cross-entropy is how every language model is trained", font_size=36).to_edge(UP, buff=0.45)
        f = mtex(r"\mathcal{L}(\theta) = \frac{1}{N} \sum_{t=1}^{N} \log \frac{1}{q_\theta(x_t \mid x_{<t})}",
                 font_size=46).next_to(head, DOWN, buff=0.6)
        f[0][0:4].set_color(C.LOSS)
        rows = VGroup(
            label(r"$\approx H(p, q_\theta)$, \ measured on real text", font_size=30),
            label(r"$= H(p) + D_{\mathrm{KL}}(p \,\|\, q_\theta)$: \ only the second part can be trained away",
                  font_size=30),
            label(r"the floor is $H(p)$: \ the entropy of language itself", font_size=30, color=C.ENTROPY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(f, DOWN, buff=0.6)
        unit = note(r"papers report it in nats per token: \ $1$ nat $= 1/\ln 2 \approx 1.443$ bits", font_size=24)
        unit.to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is why all of this matters for AI. <bookmark mark='a'/> The loss that every large language model "
            "is trained to minimize is exactly this: the average of log one over q, for each token of real text, "
            "given the tokens before it. <bookmark mark='b'/> It's the cross-entropy between the world's text and the "
            "model. <bookmark mark='c'/> Training can only shrink the divergence part; <bookmark mark='d'/> the "
            "entropy of language itself is a floor no model can go below."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(unit))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def asymmetry(self):
        d = load("kl")
        x, p = np.asarray(d["x"]), np.asarray(d["p"])
        fwd, ra = np.asarray(d["fwd"]), np.asarray(d["rev_a"])
        assert abs(fwd[-1, 0] + 0.40) < 0.01 and abs(fwd[-1, 1] - 2.15) < 0.01
        assert abs(ra[-1, 0] + 1.99) < 0.01 and abs(ra[-1, 1] - 0.66) < 0.01
        head = label(r"$D_{\mathrm{KL}}$ is not symmetric", font_size=38).to_edge(UP, buff=0.35)
        axes, curves, qs, reads = [], [], [], []
        trackers = []
        for k, (title, path, col) in enumerate([
            (r"$\min_q D_{\mathrm{KL}}(p \,\|\, q)$: \ cover everything $p$ does", fwd, C.MODEL_Q),
            (r"$\min_q D_{\mathrm{KL}}(q \,\|\, p)$: \ go only where $p$ goes", ra, C.MODEL_Q),
        ]):
            ax = plain_axes([-6, 6, 2], [0, 0.7, 0.1], 6.0, 3.0).move_to([-3.5 + 7.0 * k, -0.75, 0])
            t = label(title, font_size=24, color=GREY_A).next_to(ax, UP, buff=0.35)
            pc = polyline(ax, x, p, color=C.TRUE_P, stroke_width=3.5)
            fill = ax.get_area(pc, x_range=[-6, 6], color=C.TRUE_P, opacity=0.25) if False else VGroup()
            m_t, s_t = ValueTracker(path[0, 0]), ValueTracker(path[0, 1])
            trackers.append((m_t, s_t, path))

            def qcurve(ax=ax, m_t=m_t, s_t=s_t):
                m, s = m_t.get_value(), s_t.get_value()
                y = np.exp(-0.5 * ((x - m) / s) ** 2) / (s * math.sqrt(2 * math.pi))
                return polyline(ax, x, np.minimum(y, 0.7), color=C.MODEL_Q, stroke_width=3.5)

            qc = always_redraw(qcurve)
            axes.append(VGroup(ax, t, pc, fill))
            qs.append(qc)
        lp = label(r"$p$: \ two peaks", font_size=26, color=C.TRUE_P)
        lq = label(r"$q$: \ one bell curve", font_size=26, color=C.MODEL_Q)
        VGroup(lp, lq).arrange(RIGHT, buff=1.0).next_to(head, DOWN, buff=0.3)
        res = VGroup(
            label(rf"$\mu = {fwd[-1, 0]:.2f},\ \sigma = {fwd[-1, 1]:.2f}$: \ matches $p$'s mean and spread", font_size=22,
                  color=C.MODEL_Q).move_to([-3.5, -2.85, 0]),
            label(rf"$\mu = {ra[-1, 0]:.2f},\ \sigma = {ra[-1, 1]:.2f}$: \ locks onto one peak", font_size=22,
                  color=C.MODEL_Q).move_to([3.5, -2.85, 0]),
        )
        why_ = VGroup(
            label(r"$p \log \frac{p}{q}$ explodes where $p > 0$ but $q \approx 0$", font_size=22, color=GREY_A),
            label(r"$q \log \frac{q}{p}$ explodes where $q > 0$ but $p \approx 0$", font_size=22, color=GREY_A),
        )
        why_[0].next_to(res[0], DOWN, buff=0.15)
        why_[1].next_to(res[1], DOWN, buff=0.15)
        with self.voiceover(
            "One more property, which will matter a lot later: the divergence is not symmetric. Suppose the truth p "
            "has two peaks, and our model q can only be a single bell curve. Which bell curve is best? It depends "
            "on which way round we measure. <bookmark mark='a'/> Minimizing the divergence of q from p, the "
            "training loss we just met, <bookmark mark='b'/> pulls q wide, to cover both peaks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axes[0]), FadeIn(axes[1]), FadeIn(lp), FadeIn(lq))
            self.add(*qs)
            vo.wait_until("a")
            self.wait(0.3)
            m_t, s_t, path = trackers[0]
            vo.wait_until("b")
            self.play(UpdateFromAlphaFunc(VGroup(), lambda mob, a: (
                m_t.set_value(np.interp(a, np.linspace(0, 1, len(path)), path[:, 0])),
                s_t.set_value(np.interp(a, np.linspace(0, 1, len(path)), path[:, 1])))), run_time=3.0,
                rate_func=linear)
            self.play(FadeIn(res[0]), FadeIn(why_[0]))
        with self.voiceover(
            "The other way round, <bookmark mark='a'/> q is punished for putting probability where p has none, so "
            "it squeezes into a single peak and ignores the other. <bookmark mark='b'/> Covering everything, or "
            "committing to one thing: that choice comes back in diffusion models, in part fourteen, and in "
            "reinforcement learning, in part seventeen."
        ) as vo:
            m_t, s_t, path = trackers[1]
            vo.wait_until("a")
            self.play(UpdateFromAlphaFunc(VGroup(), lambda mob, a: (
                m_t.set_value(np.interp(a, np.linspace(0, 1, len(path)), path[:, 0])),
                s_t.set_value(np.interp(a, np.linspace(0, 1, len(path)), path[:, 1])))), run_time=3.0,
                rate_func=linear)
            self.play(FadeIn(res[1]), FadeIn(why_[1]))
        for q in qs:
            q.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def landscape(self):
        d = load("kl")
        ms, ss = np.asarray(d["grid_m"]), np.asarray(d["grid_s"])
        F, R = np.asarray(d["F"]), np.asarray(d["R"])
        stops = ["#F7D154", "#FF6B8B", "#8E4E9E", "#2E4A78", "#121826"]
        head = label(r"The two losses, over every bell curve $(\mu, \sigma)$", font_size=34).to_edge(UP, buff=0.35)
        W, Hh = 5.6, 4.0
        panels = Group()
        for k, (Z, title, paths) in enumerate([
            (F, r"$D_{\mathrm{KL}}(p \,\|\, q)$: \ one valley", [d["fwd"]]),
            (R, r"$D_{\mathrm{KL}}(q \,\|\, p)$: \ two valleys", [d["rev_a"], d["rev_b"]]),
        ]):
            cx = -3.4 + 6.8 * k
            img = heat_image(Z, stops, 0.6, 12.0, W, Hh).move_to([cx, -0.5, 0])
            ax = Axes(x_range=[ms[0], ms[-1], 1], y_range=[ss[0], ss[-1], 1], x_length=W, y_length=Hh, tips=False,
                      axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(img)
            t = label(title, font_size=26, color=GREY_A).next_to(img, UP, buff=0.25)
            xl = MathTex(r"\mu", font_size=28, color=GREY_B).next_to(img, DOWN, buff=0.15)
            yl = MathTex(r"\sigma", font_size=28, color=GREY_B).next_to(img, LEFT, buff=0.15)
            trails = VGroup()
            for pth in paths:
                pth = np.asarray(pth)
                pts = [ax.c2p(float(m), float(s)) for m, s in pth[:, :2]]
                trail = VMobject(stroke_color=WHITE, stroke_width=3).set_points_as_corners(pts)
                trails.add(VGroup(trail, Dot(pts[0], radius=0.06, color=GREY_A), Dot(pts[-1], radius=0.09, color=WHITE)))
            panels.add(Group(img, t, xl, yl, trails))
        cap = label(r"brighter $=$ smaller divergence; \ white: gradient descent from a starting guess", font_size=22,
                    color=GREY_B).to_edge(DOWN, buff=0.35)
        tag = computed_tag()
        with self.voiceover(
            "Here are the two losses for every possible bell curve: its center across, its width up. "
            "<bookmark mark='a'/> Measured one way, there is a single valley, and gradient descent finds the wide "
            "curve from anywhere. <bookmark mark='b'/> Measured the other way, there are two valleys, one for each "
            "peak, and where you end up depends on where you start."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(panels[0][:4]))
            self.play(Create(panels[0][4]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(panels[1][:4]))
            self.play(Create(panels[1][4]), run_time=1.5)
        self.wait(0.5)
        self.clear_scene()
