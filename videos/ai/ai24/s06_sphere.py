from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai24.common import (DIGIT, NEG, PART, POS, SIMCLR, Hypersphere, axes, bars_chart, curve, load, pct,
                                   take_away)

TAUS = ["0.05", "0.1", "0.2", "0.5", "1"]
TAU_KEY = {"0.05": "0.05", "0.1": "0.1", "0.2": "0.2", "0.5": "0.5", "1": "1.0"}
ALIGN = "#5BD17A"
UNIF = "#58A6FF"


class Sphere(VoiceoverScene):
    def construct(self):
        self.card()
        self.replay()
        self.centroids()
        self.derive()
        self.sweep()
        self.hardness()

    def card(self):
        card = chapter_card(5, r"Alignment and uniformity", r"What does the contrastive loss do on the sphere?",
                            lit=(), part=PART)
        with self.voiceover("Chapter five. Alignment and uniformity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def replay(self):
        sp = load("sphere")
        Z = np.asarray(sp["simclr_z"])
        lab = np.asarray(sp["labels"]).astype(int)
        steps = np.asarray(sp["rec_steps"])
        al, un = np.asarray(sp["simclr_align"]), np.asarray(sp["simclr_unif"])
        n = len(steps)
        hs = Hypersphere(Z, [DIGIT[c] for c in lab], radius=2.7, center=[-3.0, -0.3, 0], dot=0.045)
        hs.angle.set_value(0.4)
        idx = lambda: float(np.clip(hs.t.get_value(), 0, n - 1))  # noqa: E731
        ax = axes([0, n - 1], [-4.0, 2.0], x_length=4.6, y_length=3.2, xlabel=r"snapshot", yticks=[-4, -2, 0, 2],
                  center=[3.7, -0.4, 0])
        A = ax.ax
        ca = always_redraw(lambda: curve(A, np.arange(int(idx()) + 1), al[:int(idx()) + 1], ALIGN, 3)
                           if idx() >= 1 else VectorizedPoint(A.c2p(0, al[0])))
        cu = always_redraw(lambda: curve(A, np.arange(int(idx()) + 1), un[:int(idx()) + 1], UNIF, 3)
                           if idx() >= 1 else VectorizedPoint(A.c2p(0, un[0])))
        ra = always_redraw(lambda: label(rf"$\mathcal L_{{\rm align}} = {np.interp(idx(), np.arange(n), al):.2f}$",
                                         font_size=26, color=ALIGN).move_to([3.0, 2.6, 0]))
        ru = always_redraw(lambda: label(rf"$\mathcal L_{{\rm uniform}} = {np.interp(idx(), np.arange(n), un):.2f}$",
                                         font_size=26, color=UNIF).move_to([5.2, 2.6, 0]))
        st = always_redraw(lambda: label(rf"step ${int(round(np.interp(idx(), np.arange(n), steps)))}$", font_size=22,
                                         color=GREY_A).move_to([-3.0, 3.2, 0]))
        d1 = label(r"two views of a digit: \ how far apart", font_size=20, color=ALIGN)
        d2 = label(r"all pairs: \ how bunched up", font_size=20, color=UNIF)
        VGroup(d1, d2).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax, DOWN, buff=0.15)
        tg = tag(r"computed: \ SimCLR with three output numbers, \ $\tau = 0.2$")
        with self.voiceover(
            "Watch the contrastive loss work on a sphere. This is a SimCLR network whose output has only three "
            "numbers, so every digit is a point we can see. <bookmark mark='a'/> Two quantities tell the story. "
            "Alignment: how far apart the two views of the same digit land. Uniformity: how bunched up all the "
            "points are, measured so that lower means more evenly spread. <bookmark mark='b'/> Both fall. The "
            "views of each digit come together, and the digits spread over the whole sphere, as far from each "
            f"other as they can get. <bookmark mark='c'/> By the end, alignment is {al[-1]:.2f} and uniformity "
            f"{un[-1]:.2f}; and because the network cannot spread all the fives apart without also separating "
            "them from their own views, the fives end up together."
        ) as vo:
            self.play(FadeIn(hs), FadeIn(st), FadeIn(tg))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(ra), FadeIn(ru), FadeIn(d1), FadeIn(d2), FadeIn(ca), FadeIn(cu))
            vo.wait_until("b")
            self.play(hs.t.animate.set_value(n - 1), hs.angle.animate.set_value(3.6),
                      run_time=max(4.0, vo.until("c") - 0.2), rate_func=lambda u: u ** 0.7)
            vo.wait_until("c")
            self.play(hs.angle.animate.set_value(4.8), run_time=max(1.0, vo.remaining()), rate_func=linear)
        hs.freeze()
        for m in (ca, cu, ra, ru, st):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def centroids(self):
        sp = load("sphere")
        Z = np.asarray(sp["simclr_z"])[-1]
        Z = Z / np.linalg.norm(Z, axis=1, keepdims=True)
        lab = np.asarray(sp["labels"]).astype(int)
        cen = np.array([Z[lab == c].mean(0) for c in range(10)])
        tight = np.linalg.norm(cen, axis=1)  # 1 when a digit's points coincide, 0 when spread all over
        cen = cen / np.linalg.norm(cen, axis=1, keepdims=True)
        ang = np.degrees(np.arccos(np.clip(cen @ cen.T, -1, 1)))
        iu = [(a, b) for a in range(10) for b in range(a + 1, 10)]
        pairs = sorted(iu, key=lambda ab: ang[ab])
        (a1, b1), (a2, b2) = pairs[0], pairs[1]
        far = pairs[-1]
        hs = Hypersphere(Z, [DIGIT[c] for c in lab], radius=2.5, center=[-3.2, -0.3, 0], dot=0.03)
        for d in hs.dots:
            d.set_opacity(0.35)
        hs.angle.set_value(4.8)
        cl = VGroup()

        def mk(c):
            def f():
                q = hs._rot(cen[c][None])[0]
                p = hs.c + hs.R * np.array([q[0], q[1], 0.0])
                return VGroup(Dot(p, radius=0.09, color=DIGIT[c]).set_stroke(WHITE, 1.5),
                              MathTex(str(c), font_size=30, color=DIGIT[c]).next_to(p, UR, buff=0.04)).set_opacity(
                    0.45 + 0.55 * (q[2] + 1) / 2)
            return f

        for c in range(10):
            cl.add(always_redraw(mk(c)))
        tab = VGroup(label(r"closest digits on the sphere", font_size=24, color=GREY_A),
                     MathTex(rf"{a1} \leftrightarrow {b1}:\ {ang[a1, b1]:.0f}^\circ", font_size=34, color=WHITE),
                     MathTex(rf"{a2} \leftrightarrow {b2}:\ {ang[a2, b2]:.0f}^\circ", font_size=34, color=WHITE),
                     label(r"farthest", font_size=24, color=GREY_A),
                     MathTex(rf"{far[0]} \leftrightarrow {far[1]}:\ {ang[far]:.0f}^\circ", font_size=34, color=WHITE))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, 0.4, 0])
        tg = tag(r"computed: \ the mean direction of each digit's test points")
        loose = int(np.argmin(tight))
        with self.voiceover(
            "Where did the digits land? Take each digit's average direction on the sphere. <bookmark mark='a'/> The "
            f"closest pair is {a1} and {b1}, {ang[a1, b1]:.0f} degrees apart, then {a2} and {b2}. <bookmark "
            f"mark='b'/> The farthest apart are {far[0]} and {far[1]}. Nobody told the network that some digits are "
            f"written alike; the geometry of the sphere records it. <bookmark mark='c'/> The loosest cluster is the "
            f"digit {loose}: its points are the most spread out."
        ) as vo:
            self.play(FadeIn(hs), FadeIn(tg))
            vo.wait_until("a")
            self.play(FadeIn(cl), FadeIn(tab[:3]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3:]))
            self.play(hs.angle.animate.set_value(6.4), run_time=max(1.0, vo.until("c")), rate_func=linear)
            vo.wait_until("c")
            self.play(hs.angle.animate.set_value(7.4), run_time=max(1.0, vo.remaining()), rate_func=linear)
        hs.freeze()
        for m in cl:
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        cols = {r"\tfrac{1}{2\tau}\,\|z - z^+\|^2": ALIGN, r"\log \mathbb E_{z^-} e^{z \cdot z^- / \tau}": UNIF}
        rows = [
            cmath(r"\ell", r"=", r"-\tfrac{1}{\tau}\, z \cdot z^+", r"+", r"\log \sum_{j=1}^{N} e^{z \cdot z_j / \tau}",
                  font_size=36, colors=cols),
            cmath(r"\ell - \log N", r"\to", r"-\tfrac{1}{\tau}\, z \cdot z^+", r"+",
                  r"\log \mathbb E_{z^-} e^{z \cdot z^- / \tau}", font_size=36, colors=cols),
            cmath(r"\ell - \log N", r"\to", r"\tfrac{1}{2\tau}\,\|z - z^+\|^2", r"+",
                  r"\log \mathbb E_{z^-} e^{z \cdot z^- / \tau}", r"-\tfrac{1}{\tau}", font_size=36, colors=cols),
        ]
        whys = [why(r"one view's loss, \ unit vectors $z$"), why(r"$N \to \infty$: \ a sum of $N$ becomes $N$ times a mean"),
                why(r"on the sphere: \ $z \cdot z^+ = 1 - \tfrac12 \|z - z^+\|^2$")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.6, buff=0.55, edge=6.9)
        defs = VGroup(
            cmath(r"\mathcal L_{\rm align}", r"=", r"\mathbb E\,\|f(x) - f(x^+)\|^2", font_size=34),
            cmath(r"\mathcal L_{\rm uniform}", r"=", r"\log \mathbb E\, e^{-2\|f(x) - f(y)\|^2}", font_size=34),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(DOWN, buff=0.9)
        defs[0][0].set_color(ALIGN)
        defs[1][0].set_color(UNIF)
        ul = label(r"smallest when the points are spread uniformly over the sphere", font_size=22,
                   color=GREY_A).next_to(defs, DOWN, buff=0.2)
        src = cite(r"Wang \& Isola (2020)", corner=DR)
        with self.voiceover(
            "Tongzhou Wang and Phillip Isola showed why, in 2020. Write one view's loss with unit vectors: a pull "
            "toward its partner, and a log-sum over everyone. <bookmark mark='a'/> With many negatives, the sum "
            "becomes N times an average. <bookmark mark='b'/> On the sphere, the dot product with the partner is one "
            "minus half their squared distance. So the loss splits in two: <bookmark mark='c'/> an alignment term, "
            "the distance between views, and a uniformity term, smallest when the points spread evenly over the "
            "sphere. Contrastive learning is these two forces, and the temperature sets their balance."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(defs, shift=UP * 0.1), FadeIn(ul), FadeIn(src))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sweep(self):
        s = load("simclr")
        runs, keys = s["runs"], s["keys"]
        lin = [np.array([runs[k]["final"]["linear"] for k in keys[TAU_KEY[t]]]) for t in TAUS]
        al = [np.mean([runs[k]["final"]["align_z"] for k in keys[TAU_KEY[t]]]) for t in TAUS]
        un = [np.mean([runs[k]["final"]["unif_z"] for k in keys[TAU_KEY[t]]]) for t in TAUS]
        means = np.array([x.mean() for x in lin])
        lo = float(np.floor((min(x.min() for x in lin) - 0.01) * 100) / 100)
        ch = bars_chart(means, [SIMCLR] * 5, [rf"$\tau = {t}$" for t in TAUS], height=3.0, bar_w=0.7, gap=0.35,
                        vmin=lo, vmax=1.0, spread=[(x.min(), x.max()) for x in lin], digits=1,
                        value_fmt=lambda v: pct(v), font_size=20)
        ch.move_to([-3.4, -0.6, 0])
        chl = label(rf"linear probe, \% \ (axis from ${pct(lo, 0)}$)", font_size=20, color=GREY_A).next_to(ch, UP,
                                                                                                        buff=0.3)
        ax = axes([min(un) - 0.3, max(un) + 0.3], [0, max(al) * 1.2], x_length=4.4, y_length=3.2,
                  xlabel=r"$\mathcal L_{\rm uniform}$ \ (lower: more spread)", ylabel=r"$\mathcal L_{\rm align}$",
                  center=[3.5, -0.4, 0])
        pts = VGroup()
        for t, a_, u_ in zip(TAUS, al, un):
            d = Dot(ax.ax.c2p(u_, a_), radius=0.08, color=SIMCLR)
            pts.add(VGroup(d, MathTex(rf"\tau = {t}", font_size=22, color=GREY_A).next_to(d, UR, buff=0.06)))
        best = int(np.argmax(means))
        worst = int(np.argmin(means))
        n_seed = [len(keys[TAU_KEY[t]]) for t in TAUS]
        ends_bad = means[0] < means[best] - 0.003 and means[-1] < means[best] - 0.003
        line = (f"Accuracy peaks in the middle, at tau {TAUS[best]}, with {pct(means[best])} percent, and falls off "
                f"at both ends: {pct(means[0])} at tau {TAUS[0]}, {pct(means[-1])} at tau {TAUS[-1]}."
                if ends_bad and 0 < best < 4 else
                f"The best is tau {TAUS[best]}, with {pct(means[best])} percent; the worst, tau {TAUS[worst]}, with "
                f"{pct(means[worst])}.")
        low_t_unif = un[0] < un[-1]
        geo = ("Low temperatures spread the points most evenly, and pay for it in alignment; high temperatures "
               "align the views and leave the points bunched." if low_t_unif and al[0] > al[-1] else
               "The temperature moves each run along the trade between the two terms.")
        tg = tag(rf"computed: \ ${n_seed[2]}$ seeds at $\tau = 0.2$, \ ${n_seed[0]}$ at the others")
        with self.voiceover(
            "We trained SimCLR at five temperatures, from 0.05 to 1. <bookmark mark='a'/> "
            f"{line} <bookmark mark='b'/> On the right, each temperature's final alignment and uniformity. {geo}"
        ) as vo:
            self.play(FadeIn(chl), FadeIn(ch[0]), FadeIn(ch.names), FadeIn(tg))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in ch.bars], lag_ratio=0.15), FadeIn(ch.whiskers),
                      FadeIn(ch.vals), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(ax), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hardness(self):
        s = load("simclr")
        runs, keys = s["runs"], s["keys"]
        lo_t, hi_t = TAUS[0], TAUS[-1]
        W_lo, W_hi = np.asarray(s[f"wsorted_{lo_t}"]), np.asarray(s[f"wsorted_{hi_t}"])
        top_lo = np.mean([runs[k]["extra"]["top10"] for k in keys[TAU_KEY[lo_t]]])
        top_hi = np.mean([runs[k]["extra"]["top10"] for k in keys[TAU_KEY[hi_t]]])
        n_neg = 510

        def panel(W, t, center, col):
            m = 30
            ax = axes([0, m], [0, float(max(W_lo[0], W_hi[0])) * 1.1], x_length=4.6, y_length=2.6,
                      xlabel=r"negatives, \ hardest first", center=center)
            bars = VGroup(*[Rectangle(width=4.6 / m * 0.8, height=max(ax.ax.c2p(0, float(w))[1] - ax.ax.c2p(0, 0)[1],
                                                                       0.005),
                                      stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                ax.ax.c2p(i + 0.5, float(w) / 2)) for i, w in enumerate(W[:m])])
            t_ = label(rf"$\tau = {t}$", font_size=28, color=col).next_to(ax, UP, buff=0.1)
            return VGroup(ax, bars, t_)

        p1 = panel(W_lo, lo_t, [-3.4, 0.2, 0], NEG)
        p2 = panel(W_hi, hi_t, [3.4, 0.2, 0], SIMCLR)
        s1 = label(rf"ten hardest: \ ${pct(top_lo, 0)}\%$ of the push", font_size=24, color=NEG).next_to(p1, DOWN,
                                                                                                     buff=0.35)
        s2 = label(rf"ten hardest: \ ${pct(top_hi, 0)}\%$ of the push", font_size=24, color=SIMCLR).next_to(p2, DOWN,
                                                                                                        buff=0.35)
        head = label(rf"Where the push goes: \ each view's weights on its ${n_neg}$ negatives", font_size=30)
        head.to_edge(UP, buff=0.4)
        src = cite(r"Wang \& Liu (2021): \ the uniformity--tolerance dilemma")
        tk = take_away(r"the temperature sets how hard the loss pushes on the most similar other digits")
        with self.voiceover(
            "The temperature has a second effect. In the softmax, every negative pushes in proportion to its "
            "weight, and the weights depend on how similar it already is. <bookmark mark='a'/> At tau "
            f"{lo_t}, the ten most similar negatives of each view take {pct(top_lo, 0)} percent of the push: the "
            f"loss fights over the hardest cases. <bookmark mark='b'/> At tau {hi_t}, they take {pct(top_hi, 0)} "
            "percent; the push is spread over everything. <bookmark mark='c'/> But a hard negative is often just "
            "another five that looks like this five. Pushing it away tears a class apart; ignoring it leaves the "
            "sphere bunched. Feng Wang and Huaping Liu called this the uniformity-tolerance dilemma."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(p1[0]), FadeIn(p1[2]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in p1[1]],
                                                                 lag_ratio=0.03), FadeIn(s1), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(p2[0]), FadeIn(p2[2]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in p2[1]],
                                                                 lag_ratio=0.03), FadeIn(s2), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(tk, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
