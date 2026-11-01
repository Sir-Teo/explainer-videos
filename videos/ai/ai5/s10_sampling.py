from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, MODEL, MONO, PART, curve, hist_shape, load

ALPHA27 = " abcdefghijklmnopqrstuvwxyz"
ACC, REJ = "#5BD17A", C.SURPRISE
GUM = "#B39DDB"  # Gumbel noise and its picks


def normal_scatter_scale(points, radius=2.04):
    """Fit the actual finite cohort, preserving every point and coordinate unit."""
    points = np.asarray(points, float)
    if (points.ndim != 2 or points.shape[1] != 2 or not len(points)
            or not np.isfinite(points).all() or not math.isfinite(radius) or radius <= 0):
        raise ValueError("finite nonempty two-coordinate points and positive radius required")
    extent = max(2.5, math.ceil((float(np.abs(points).max()) + 0.1) * 2) / 2)
    return radius / extent


class Sampling(VoiceoverScene):
    def construct(self):
        self.card()
        self.stick()
        self.continuous()
        self.box_muller()
        self.gumbel()
        self.relax()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(8, r"Rolling loaded dice", r"How does a computer draw from a distribution?", part=PART)
        with self.voiceover("Chapter eight. Rolling loaded dice."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def stick(self):
        freq = np.asarray(load("markov")["freq"])
        assert abs(freq.sum() - 1) < 1e-9
        W, y0, h = 12.4, 0.9, 0.7
        edges = np.concatenate([[0], np.cumsum(freq)])
        palette = [ManimColor(DATA), ManimColor("#7C7FE0"), ManimColor(C.INTERVAL), ManimColor(MODEL)]
        segs, labs = VGroup(), VGroup()
        for i, ch in enumerate(ALPHA27):
            a, b = edges[i], edges[i + 1]
            r = Rectangle(width=W * (b - a), height=h, stroke_width=1, stroke_color=BACKGROUND,
                          fill_color=palette[i % 4], fill_opacity=0.55).move_to([-W / 2 + W * (a + b) / 2, y0, 0])
            segs.add(r)
            if W * (b - a) > 0.3:
                labs.add(Text("␣" if ch == " " else ch, font=MONO, font_size=22).move_to(r))
        # the same probabilities first as bars, standing up
        bw = 0.34
        stand = VGroup(*[Rectangle(width=bw, height=max(9.0 * f, 0.02), stroke_width=0, fill_color=palette[i % 4],
                                   fill_opacity=0.55) for i, f in enumerate(freq)])
        for i, r in enumerate(stand):
            r.move_to([-(27 * (bw + 0.08)) / 2 + i * (bw + 0.08) + bw / 2, -2.2 + r.height / 2, 0])
        stand_l = VGroup(*[Text("␣" if c == " " else c, font=MONO, font_size=18, color=GREY_A)
                           .next_to(stand[i], DOWN, buff=0.1).set_y(-2.45) for i, c in enumerate(ALPHA27)])
        dist_l = label(r"a model's output: \ a probability for every letter", font_size=28, color=GREY_A)
        dist_l.next_to(stand, UP, buff=0.4)
        z0 = MathTex("0", font_size=28, color=GREY_B).next_to(segs, LEFT, buff=0.15)
        z1 = MathTex("1", font_size=28, color=GREY_B).next_to(segs, RIGHT, buff=0.15)
        head = label(r"Every letter gets a stretch of $[0, 1)$ as long as its probability", font_size=30)
        head.to_edge(UP, buff=0.5)
        u = ValueTracker(0.5)
        needle = always_redraw(lambda: VGroup(
            Line([-W / 2 + W * u.get_value(), y0 + h / 2 + 0.55, 0], [-W / 2 + W * u.get_value(), y0 - h / 2 - 0.05, 0],
                 color=WHITE, stroke_width=3),
            Triangle(color=WHITE, fill_opacity=1, stroke_width=0).scale(0.09).rotate(PI)
            .move_to([-W / 2 + W * u.get_value(), y0 + h / 2 + 0.6, 0])))
        uv = DecimalNumber(0.5, num_decimal_places=3, font_size=30)
        uv.add_updater(lambda m: m.set_value(u.get_value()).next_to([-W / 2 + W * u.get_value(), y0 + h / 2 + 0.85, 0],
                                                                       UP, buff=0.0))
        g = np.random.default_rng(4)
        draws = g.random(16)
        out_l = label(r"drawn:", font_size=30, color=GREY_A).move_to([-5.4, -1.0, 0])
        out = VGroup()
        rule = label(r"a uniform random number $u$; \ the letter whose stretch contains it", font_size=28, color=C.BITS)
        rule.to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "A model never hands us a word, only a distribution, and to write anything we must roll loaded dice. "
            "<bookmark mark='a'/> Lay the probabilities end to end from zero to one, so each letter owns a stretch as "
            "long as its probability. <bookmark mark='b'/> Pick a uniform random point and take the letter it lands "
            "in: the inverse of the cumulative distribution. <bookmark mark='c'/> These are drawn from part one's "
            "letter frequencies."
        ) as vo:
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in stand], lag_ratio=0.03), FadeIn(stand_l),
                      FadeIn(dist_l), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeOut(dist_l), FadeOut(stand_l), FadeIn(head),
                      LaggedStart(*[ReplacementTransform(r, sg) for r, sg in zip(stand, segs)], lag_ratio=0.03),
                      run_time=2.2)
            self.play(FadeIn(labs), FadeIn(z0), FadeIn(z1))
            vo.wait_until("b")
            self.play(FadeIn(needle), FadeIn(uv), FadeIn(rule))
            vo.wait_until("c")
            self.play(FadeIn(out_l))
            for j, r in enumerate(draws):
                i = int(np.searchsorted(edges, r, side="right") - 1)
                ch = ALPHA27[i]
                t = Text("␣" if ch == " " else ch, font=MONO, font_size=30, color=palette[i % 4])
                t.move_to([-4.6 + 0.42 * j, -1.0, 0])
                self.play(u.animate.set_value(r), run_time=0.45 if j < 4 else 0.25)
                self.play(Indicate(segs[i], color=WHITE, scale_factor=1.0), TransformFromCopy(segs[i], t),
                          run_time=0.45 if j < 4 else 0.25)
                out.add(t)
        needle.clear_updaters()
        uv.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def continuous(self):
        d = load("draws")
        from scipy.stats import beta as beta_

        # left: inverse CDF for the exponential
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 1, 0.5], x_length=5.4, y_length=2.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-3.5, 1.2, 0])
        xs = np.linspace(0, 4, 200)
        F = curve(ax, xs, 1 - np.exp(-xs), color=DATA, stroke_width=3.5)
        Fl = label(r"$F(x) = 1 - e^{-x}$", font_size=22, color=DATA).next_to(ax.c2p(3.0, 0.9), DOWN, buff=0.25)
        us = [0.25, 0.6, 0.88]
        arrows = VGroup()
        for u in us:
            x = -math.log(1 - u)
            arrows.add(VGroup(Line(ax.c2p(0, u), ax.c2p(x, u), color=C.BITS, stroke_width=2.5),
                              Arrow(ax.c2p(x, u), ax.c2p(x, 0), buff=0, color=C.BITS, stroke_width=2.5,
                                    max_tip_length_to_length_ratio=0.12)))
        rule1 = label(r"$x = F^{-1}(u) = -\ln(1 - u)$", font_size=24, color=C.BITS).next_to(ax, UP, buff=0.12)
        hx = Axes(x_range=[0, 5, 1], y_range=[0, 1.05, 0.5], x_length=5.4, y_length=2.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.5, -2.2, 0])
        h = np.asarray(d["ex_hist"], float)
        e = np.linspace(0, 5, len(h) + 1)
        eh = hist_shape(hx, e, h / h.sum() / (e[1] - e[0]), color=DATA, opacity=0.4)
        ec = curve(hx, xs, np.exp(-xs), color=MODEL, stroke_width=3)
        el = label(rf"$20{{,}}000$ draws; \ largest CDF gap ${float(d['ks_exp']):.3f}$", font_size=20, color=GREY_A)
        el.next_to(hx, UP, buff=0.08)
        # right: rejection sampling of Beta(2, 5)
        M, rate = float(d["M"]), float(d["rate"])
        bx = Axes(x_range=[0, 1, 0.5], y_range=[0, 2.7, 1], x_length=5.4, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.4, -0.6, 0])
        xb = np.linspace(0, 1, 200)
        pb = curve(bx, xb, beta_.pdf(xb, 2, 5), color=MODEL, stroke_width=3.5)
        box = Rectangle(width=bx.x_length, height=bx.y_length * M / 2.7, stroke_color=GREY_B, stroke_width=2,
                        fill_opacity=0).move_to(bx.c2p(0.5, M / 2))
        xp, up_, acc = np.asarray(d["xp"]), np.asarray(d["up"]), np.asarray(d["acc"], bool)
        pts = VGroup(*[Dot(bx.c2p(a, b), radius=0.03, color=ACC if ok else REJ, fill_opacity=0.85)
                       for a, b, ok in zip(xp, up_, acc)])
        bl = label(r"rejection: \ keep the points under the curve", font_size=22, color=GREY_A).next_to(bx, UP, buff=0.12)
        rl = label(rf"kept ${100 * rate:.1f}\%$; \ predicted $1/M = {100 / M:.1f}\%$", font_size=22, color=ACC)
        rl.next_to(bx, DOWN, buff=0.15)
        cite_ = cite(r"J.~von Neumann, \textit{Various techniques used in connection with random digits} (1951)", corner=DR)
        with self.voiceover(
            "The same trick works for continuous distributions. <bookmark mark='a'/> For the exponential, x is minus "
            "the log of one minus u: twenty thousand draws match the density, with a largest CDF gap of "
            f"{float(d['ks_exp']):.3f}. <bookmark mark='b'/> When the inverse is hard to compute, John von Neumann's "
            "rejection method of 1951 needs only the density: scatter points uniformly in a box over the curve, and "
            "keep the ones under it. <bookmark mark='c'/> The kept points follow the density. The price is waste: "
            f"{100 * rate:.1f} percent are kept, one over the box's height, as predicted, and in many dimensions that "
            "share collapses."
        ) as vo:
            self.play(Create(ax), Create(F), FadeIn(Fl))
            vo.wait_until("a")
            self.play(FadeIn(rule1), LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.4), run_time=1.5)
            self.play(Create(hx), FadeIn(eh), Create(ec), FadeIn(el))
            vo.wait_until("b")
            self.play(Create(bx), Create(pb), Create(box), FadeIn(bl), FadeIn(cite_))
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.004), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def box_muller(self):
        d = load("draws")
        U, Z = np.asarray(d["bm_u"]), np.asarray(d["bm_z"])
        rows = [
            cmath(r"p(z_1, z_2)", "=", r"\tfrac{1}{2\pi}\, e^{-(z_1^2 + z_2^2)/2}", font_size=32),
            cmath(r"p(z_1, z_2)\,dz_1\,dz_2", "=", r"\frac{d\theta}{2\pi} \cdot e^{-r^2/2}\, r\, dr", font_size=32),
            cmath(r"(\theta,\, r)", "=", r"\big(2\pi u_2,\; \sqrt{-2\ln(1 - u_1)}\big)", font_size=32),
        ]
        whys = [why(r"two independent bells", font_size=22), why(r"polar coordinates: \ the angle is uniform",
                                                                 font_size=22),
                why(r"$r^2/2$ is exponential: \ inverse CDF", font_size=22)]
        step = ladder(self, rows, whys, keep=3, top=3.3, x=-1.8, buff=0.32, edge=6.8)
        S = normal_scatter_scale(Z)
        sq = Square(2.4, color=GREY_B, stroke_width=2).move_to([-3.6, -1.6, 0])
        ud = VGroup(*[Dot(sq.get_corner(DL) + 2.4 * np.array([a, b, 0]), radius=0.025, color=C.BITS) for a, b in U])
        c0 = np.array([3.0, -1.6, 0])
        zd = VGroup(*[Dot(c0 + S * np.array([a, b, 0]), radius=0.025, color=C.BITS) for a, b in Z])
        ring = VGroup(Circle(radius=S, color=MODEL, stroke_width=2), Circle(radius=2 * S, color=MODEL,
                                                                            stroke_width=1.5).set_stroke(opacity=0.5)).move_to(c0)
        ul = label(r"$(u_1, u_2)$, \ uniform", font_size=22, color=GREY_A).next_to(sq, DOWN, buff=0.12)
        zl = label(rf"$(z_1, z_2)$: \ independent bells \ (full-sample CDF gap ${float(d['ks_bm']):.4f}$)", font_size=22,
                   color=GREY_A).next_to(c0 + DOWN * 2.1, DOWN, buff=0.0)
        view_note = label(rf"${len(Z)}$ actual draws; \ circles at radii $1$ and $2$", font_size=20,
                          color=GREY_A).move_to(c0 + UP * 2.2)
        arr = Arrow(sq.get_right() + RIGHT * 0.2, c0 + LEFT * 2.3, buff=0.1, color=GREY_B, stroke_width=3)
        cite_ = cite(r"G.~E.~P.~Box \& M.~E.~Muller (1958)", corner=UR)
        with self.voiceover(
            "The bell itself has no simple inverse CDF, but a pair of bells does, in polar coordinates. "
            "<bookmark mark='a'/> Two independent bells have a density that depends only on the distance from the "
            "centre. <bookmark mark='b'/> So the angle is uniform, and the squared radius, halved, is exponential, "
            "which we just learned to draw. <bookmark mark='c'/> Two uniform numbers in, two independent bells out: "
            "the Box-Muller transform of 1958."
        ) as vo:
            self.play(Create(sq), FadeIn(ud), FadeIn(ul), FadeIn(cite_))
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1, transform=False)
            self.play(GrowArrow(arr), TransformFromCopy(ud, zd), Create(ring), FadeIn(zl), FadeIn(view_note), run_time=2.0)
            vo.wait_until("c")
            step(2, transform=False)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gumbel(self):
        d = load("draws")
        z, p, freq = np.asarray(d["scores"]), np.asarray(d["p"]), np.asarray(d["freq"])
        N, chi2 = int(d["N"]), float(d["chi2"])
        g = np.random.default_rng(1954)  # Gumbel, 1954 (illustrative draws for the animation)
        G = -np.log(-np.log(g.random((6, 6))))
        lb = LiveBars(z + 1.5, max_value=6.0, height=3.4, bar_width=0.5, gap=0.25, colors=GUM,
                      labels=[r"$1$", r"$2$", r"$3$", r"$4$", r"$5$", r"$6$"], label_font=24)
        lb.place(-2.2, x=-3.6)
        lt = label(r"score $+$ Gumbel noise \ (shifted up by $1.5$)", font_size=22, color=GREY_A).move_to([-3.6, 1.7, 0])
        crown = Triangle(color=C.BITS, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI)

        def crown_at(i, vals):
            return crown.copy().move_to([lb._cx(i) - 3.6, -2.2 + 3.4 * vals[i] / 6.0 + 0.25, 0])

        rows = [
            cmath(r"i^\star", "=", r"\arg\max_i \;(z_i + G_i)", font_size=34),
            cmath(r"P(i^\star = i)", "=", r"\frac{e^{z_i}}{\sum_j e^{z_j}}", font_size=34, colors={r"\frac{e^{z_i}}{\sum_j e^{z_j}}": MODEL}),
        ]
        whys = [why(r"$G_i = -\log(-\log U_i)$: \ Gumbel noise", font_size=22), why(r"exactly the softmax", font_size=22)]
        step = ladder(self, rows, whys, keep=2, top=3.2, x=1.6, buff=0.5, edge=6.8)
        cmp = VGroup()
        for i in range(6):
            cmp.add(VGroup(Rectangle(width=0.3, height=4.5 * p[i], stroke_width=0, fill_color=MODEL, fill_opacity=0.8),
                           Rectangle(width=0.3, height=4.5 * freq[i], stroke_width=0, fill_color=GUM, fill_opacity=0.8))
                    .arrange(RIGHT, buff=0.03, aligned_edge=DOWN))
        cmp.arrange(RIGHT, buff=0.35, aligned_edge=DOWN).move_to([3.3, -1.6, 0])
        cl = VGroup(label(r"softmax", font_size=20, color=MODEL), label(rf"argmax picks, ${N:,}$ draws".replace(",", "{,}"),
                                                                       font_size=20, color=GUM)).arrange(RIGHT, buff=0.3)
        cl.next_to(cmp, DOWN, buff=0.2)
        ok = chi2 < 20
        verdict = (f"they agree, with a chi-squared of {chi2:.1f} on five degrees of freedom, just what chance gives." if ok
                   else f"chi-squared is {chi2:.1f}, more than chance should give.")
        cite_ = cite(r"E.~J.~Gumbel (1954); \ R.~D.~Luce (1959); \ J.~I.~Yellott (1977); \ C.~Maddison et al.\ (2014)",
                     corner=DL)
        with self.voiceover(
            "One more trick, used constantly in machine learning. To pick option i with the softmax of its score, add "
            "independent Gumbel noise to each score, minus the log of minus the log of a uniform number, <bookmark "
            "mark='a'/> and take the largest. <bookmark mark='b'/> The winner follows the softmax exactly: the Gumbel "
            f"is the shape of maxima. <bookmark mark='c'/> Two hundred thousand picks against the softmax: {verdict} "
            "It needs only the scores, never the normalizer, and turns sampling into maximization."
        ) as vo:
            self.play(FadeIn(lb), FadeIn(lt))
            for k in range(3):
                vals = z + 1.5 + G[k]
                i = int(np.argmax(vals))
                c_ = crown_at(i, vals)
                self.play(*lb.to(vals), run_time=0.6)
                self.play(FadeIn(c_), run_time=0.3)
                self.play(FadeOut(c_), run_time=0.2)
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in cmp], lag_ratio=0.1), FadeIn(cl), FadeIn(cite_))
        lb.freeze()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def relax(self):
        d = load("draws")
        taus, onehot = [float(t) for t in d["taus"]], np.asarray(d["onehot"])
        f = cmath(r"y", "=", r"\operatorname{softmax}\big((z + G)\,/\,", r"\tau", r"\big)", font_size=40,
                  colors={r"\tau": C.SURPRISE}).to_edge(UP, buff=0.45)
        fn = label(r"a smooth stand-in for the one-hot pick: \ gradients flow through it", font_size=24, color=GREY_A)
        fn.next_to(f, DOWN, buff=0.2)
        panels = VGroup()
        for tau in (0.1, 1.0, 5.0):
            ys = np.asarray(d[f"y{tau}"])
            rows = VGroup()
            for y in ys:
                rows.add(VGroup(*[Rectangle(width=0.3, height=max(1.3 * v, 0.01), stroke_width=0, fill_color=GUM,
                                            fill_opacity=0.85) for v in y]).arrange(RIGHT, buff=0.06, aligned_edge=DOWN))
            rows.arrange(RIGHT, buff=0.6, aligned_edge=DOWN)
            j = taus.index(tau)
            panels.add(VGroup(rows, label(rf"$\tau = {tau:g}$: \ largest entry ${onehot[j]:.2f}$ on average", font_size=22,
                                          color=C.SURPRISE).next_to(rows, DOWN, buff=0.15)))
        panels.arrange(DOWN, buff=0.4).move_to(DOWN * 0.9)
        tag = note(r"three draws at each temperature").to_corner(DR, buff=0.25)
        cite_ = cite(r"E.~Jang, S.~Gu \& B.~Poole; \ C.~Maddison, A.~Mnih \& Y.~W.~Teh (both 2017)", corner=DL)
        with self.voiceover(
            "Sampling can't be differentiated: a pick is a pick. In 2017 two groups proposed relaxing it. Replace the "
            "argmax by a softmax with a temperature, tau: the Gumbel-softmax. <bookmark mark='a'/> Cold, at a tenth, "
            f"each draw is nearly a one-hot pick, its largest entry {onehot[0]:.2f} on average. <bookmark mark='b'/> "
            f"At one it is softer, <bookmark mark='c'/> and at five it is a blur, {onehot[-1]:.2f}. The temperature "
            "trades faithfulness for smooth gradients; it trained the discrete codes of the first DALL-E."
        ) as vo:
            self.play(Write(f), FadeIn(fn), FadeIn(cite_), FadeIn(tag), FadeIn(panels[0]))
            for k, mk in enumerate("bc", start=1):
                vo.wait_until(mk)
                self.play(FadeIn(panels[k], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
