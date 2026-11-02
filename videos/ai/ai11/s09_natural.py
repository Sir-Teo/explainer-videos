from __future__ import annotations


import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import OPT_COLORS, OPT_NAMES, PART, SAY, growing, load, takeaway_card
from videos.ai.ai11.s04_sgd import loss_axes

GDC, NGC, KF, AD = OPT_COLORS["gd"], OPT_COLORS["ng"], OPT_COLORS["kfac"], OPT_COLORS["adam"]


class Natural(VoiceoverScene):
    def construct(self):
        self.card()
        self.rulers()
        self.fisher()
        self.kfac()
        self.race()
        self.takeaway()

    def card(self):
        c = chapter_card(8, r"The natural gradient and K-FAC", r"Steepest, \ measured how?", part=PART)
        with self.voiceover("Chapter eight. The natural gradient, and K-FAC."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def rulers(self):
        n = load("natgrad")
        d = load("noise")
        ax, cont, star = loss_axes(d, center=(-3.3, 0.0), width=5.8)
        p1 = VMobject(color=GDC, stroke_width=3).set_points_as_corners([ax.c2p(*p) for p in np.asarray(n["path_gd_1"])])
        p4 = VMobject(color=C.SURPRISE, stroke_width=3).set_points_as_corners([ax.c2p(*p) for p in np.asarray(n["path_gd_0.25"])])
        lg = VGroup(label(r"gradient descent on $(w_1, w_2)$", font_size=20, color=GDC),
                    label(r"gradient descent on $(w_1, 4w_2)$: \ the same loss", font_size=20, color=C.SURPRISE))
        lg.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax, DOWN, buff=0.15)
        rows = [
            cmath(r"\Delta^*", "=", r"\arg\min_{\|\Delta\|_M \le \epsilon}\; g^\top \Delta", font_size=34),
            cmath(r"\Delta^*", r"\propto", r"-M^{-1} g", r",\quad \|\Delta\|_M^2 = \Delta^\top M \Delta", font_size=34),
        ]
        whys = [why(r"the steepest step, \ under some ruler $M$"), why(r"Lagrange: \ $g + 2\lambda M\Delta = 0$")]
        for r_ in rows:
            r_.shift(RIGHT * 3.0)
        step = ladder(self, rows, whys, keep=2, top=2.4, x=3.2, buff=0.9, edge=6.9)
        mi = label(r"plain gradient descent: \ $M = I$, \ whatever the weights mean", font_size=22, color=GDC).move_to([3.3, -1.5, 0])
        keep_in_frame(mi)
        with self.voiceover(
            "Gradient descent has a hidden assumption. <bookmark mark='a'/> Take Chapter three's two-weight loss, and "
            "write the second weight four times as large: the same model, the same loss, a new label on one axis. "
            "Gradient descent now takes a different path, because the steepest direction depends on how you measure "
            "a step. <bookmark mark='b'/> In general, the steepest step under a ruler M is minus M inverse times "
            "the gradient. <bookmark mark='c'/> Gradient descent is the choice M equals the identity: every weight "
            "counts the same, whatever it means."
        ) as vo:
            self.play(Create(cont), FadeIn(star))
            vo.wait_until("a")
            self.play(Create(p1), FadeIn(lg[0]), run_time=1.5)
            self.play(Create(p4), FadeIn(lg[1]), run_time=1.5)
            vo.wait_until("b")
            step(0)
            step(1)
            vo.wait_until("c")
            self.play(FadeIn(mi))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fisher(self):
        n = load("natgrad")
        d = load("noise")
        hist = history_card(1998, r"Shun-ichi Amari", r"\textit{Natural Gradient Works Efficiently in Learning}: \ measure "
                            r"a step by how much it changes the model's predictions", width=5.6).to_corner(UL, buff=0.35)
        rows = VGroup(
            cmath(r"\mathrm{KL}\big(p_\theta \,\|\, p_{\theta + \Delta}\big)", r"\approx", r"\tfrac12\, \Delta^\top F \Delta",
                  font_size=32),
            cmath(r"F", "=", r"\mathbb{E}_{x,\; y \sim p_\theta}\big[\nabla \log p_\theta(y|x)\, \nabla \log p_\theta(y|x)^\top\big]",
                  font_size=30, colors={r"F": NGC}),
            cmath(r"\Delta", "=", r"-\eta\, F^{-1} g", font_size=36, colors={r"-\eta\, F^{-1} g": NGC}),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(hist, DOWN, buff=0.45).align_to(hist, LEFT)
        notes = VGroup(label(r"Part 1's KL, \ to second order", font_size=20, color=GREY_A),
                       label(r"the Fisher information", font_size=20, color=NGC),
                       label(r"the natural gradient", font_size=20, color=NGC))
        for n_, r_ in zip(notes, rows):
            n_.next_to(r_, RIGHT, buff=0.3)
            keep_in_frame(n_)
        ax, cont, star = loss_axes(d, center=(3.6, 1.0), width=4.4)
        q1 = VMobject(color=NGC, stroke_width=5).set_points_as_corners([ax.c2p(*p) for p in np.asarray(n["path_ng_1"])])
        q4 = DashedVMobject(VMobject(color=WHITE, stroke_width=2.5).set_points_as_corners(
            [ax.c2p(*p) for p in np.asarray(n["path_ng_0.25"])]), num_dashes=30)
        same = float(np.abs(np.asarray(n["path_ng_1"]) - np.asarray(n["path_ng_0.25"])).max())
        lg = VGroup(label(r"natural gradient, \ both ways of writing the weights", font_size=18, color=NGC),
                    label(r"largest gap between the two paths: \ $" + (sci(same, 0) if same > 0 else "0") + "$",
                          font_size=18, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        lg.next_to(ax, DOWN, buff=0.12)
        keep_in_frame(lg)
        with self.voiceover(
            "In 1998 Shun-ichi Amari proposed the ruler that doesn't care about labels: measure a step by how much "
            "it changes the model's predictions. <bookmark mark='a'/> For a small step, part one's KL divergence "
            "between the old and new predictions is a quadratic form, <bookmark mark='b'/> and its matrix is the "
            "Fisher information: the covariance of the model's own score, with the labels drawn from its own "
            "predictions. <bookmark mark='c'/> The steepest step in that ruler is the natural gradient, minus eta F "
            "inverse g. <bookmark mark='d'/> On our two-weight loss, written both ways, its two paths are one path. "
            "It sees the model, not the coordinates."
        ) as vo:
            self.play(FadeIn(hist, shift=RIGHT * 0.2), Create(cont), FadeIn(star))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(Write(rows[k]), FadeIn(notes[k]))
            vo.wait_until("d")
            self.play(Create(q1), Create(q4), FadeIn(lg), run_time=2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kfac(self):
        n = load("natgrad")
        P = int(n["P"])
        head = label(r"one layer, \ $s = W a$: \ inputs $a$, \ output gradients $\delta = \partial \ell / \partial s$",
                     font_size=28).to_edge(UP, buff=0.3)
        rows = [
            cmath(r"\nabla_W \ell", "=", r"\delta\, a^\top", font_size=34),
            cmath(r"F_W", "=", r"\mathbb{E}\big[(a a^\top) \otimes (\delta \delta^\top)\big]", font_size=34),
            cmath(r"F_W", r"\approx", r"A \otimes G", r",\quad A = \mathbb{E}\,a a^\top,\ G = \mathbb{E}\,\delta\delta^\top", font_size=34,
                  colors={r"A \otimes G": OPT_COLORS["kfac"]}),
            cmath(r"F_W^{-1}\,\mathrm{vec}(\nabla_W)", r"\approx", r"\mathrm{vec}\big(G^{-1}\, \nabla_W\, A^{-1}\big)", font_size=34,
                  colors={r"\mathrm{vec}\big(G^{-1}\, \nabla_W\, A^{-1}\big)": OPT_COLORS["kfac"]}),
        ]
        whys = [why(r"backpropagation (Part 9)"), why(r"the Fisher block of this layer"),
                why(r"pretend inputs and gradients are independent"), why(r"$(A \otimes G)^{-1} = A^{-1} \otimes G^{-1}$")]
        step = ladder(self, rows, whys, keep=4, top=2.3, x=-1.4, buff=0.45, edge=6.9)
        cost = label(rf"our tiny net: \ ${P}$ weights, \ $F$ is ${P} \times {P}$; \ a billion weights: \ $10^{{18}}$ entries",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.9)
        cite_ = cite(r"J.~Martens \& R.~Grosse, \textit{K-FAC} (2015)", corner=DR)
        kf = label(r"two small matrices per layer, \ inverted: \ K-FAC", font_size=24, color=OPT_COLORS["kfac"]).next_to(cost, DOWN, buff=0.2)
        with self.voiceover(
            "The catch is size. The Fisher has one row and one column per weight: for our tiny spiral network, "
            f"{P} by {P}, for a billion-weight model, a billion billion entries. <bookmark mark='a'/> In 2015 James "
            "Martens and Roger Grosse found a shortcut. A layer's weight gradient is an outer product, the "
            "gradient at its output times its input. <bookmark mark='b'/> So its block of the Fisher is the "
            "expected Kronecker product of the two outer products. <bookmark mark='c'/> Pretend the inputs and the "
            "gradients are independent, and it factors into a Kronecker product of two small matrices: the inputs' "
            "second moment A and the output gradients' G. <bookmark mark='d'/> A Kronecker product inverts factor "
            "by factor, so the natural gradient of a layer becomes G inverse, times its gradient, times A inverse. "
            "That is K-FAC: Kronecker-factored approximate curvature."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cost), FadeIn(cite_))
            step(0)
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                step(k + 1)
            self.play(FadeIn(kf))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def race(self):
        n = load("natgrad")
        opts = ["gd", "adam", "kfac", "ng"]
        curves = {o: np.asarray(n[f"curves_{o}"]) for o in opts}  # seed x step x (t, loss, acc)
        T = curves["gd"].shape[1] - 1
        # Show the complete stored positive loss range; a display floor is not a measured plateau.
        log_losses = {}
        for o, c in curves.items():
            losses = c[:, :, 1]
            if not np.all(np.isfinite(losses) & (losses > 0)):
                raise ValueError("Natural race requires finite positive cached losses for the log display")
            log_losses[o] = np.log10(losses)
        lo = float(4 * np.floor(min(L.min() for L in log_losses.values()) / 4))
        hi = float(max(lo + 4, np.ceil(max(L.max() for L in log_losses.values()))))
        tick_exponents = sorted(set([int(lo), int(hi), *range(int(lo), int(hi) + 1, 4)]))
        ax = CornerAxes(x_range=[0, T, 100], y_range=[lo, hi, 1], x_length=6.2, y_length=4.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-3.1, -0.5, 0])
        xt = VGroup(*[MathTex(str(k), font_size=20, color=GREY_B).next_to(ax.c2p(k, lo), DOWN, buff=0.08) for k in range(0, T + 1, 100)])
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=18, color=GREY_B).next_to(ax.c2p(0, k), LEFT, buff=0.08)
                      for k in tick_exponents])
        xn = label(r"full-batch steps", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yn = label(r"training loss \ (nats, log scale)", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        t = ValueTracker(0)
        live, bands = [], VGroup()
        for o in opts:
            c = curves[o]
            L = log_losses[o]
            med = np.median(L, 0)
            ts = c[0, :, 0]
            bands.add(band(ax, ts, L.min(0), L.max(0), OPT_COLORS[o], 0.15))
            live.append(growing(ax, ts, med, t, OPT_COLORS[o], 3))
        race_names = dict(OPT_NAMES, ng=r"natural gradient (damped)", kfac=r"K-FAC (damped)")
        lab = VGroup(*[label(rf"{race_names[o]}: \ $\eta = {n[f'best_{o}']:g}$", font_size=20, color=OPT_COLORS[o]) for o in opts])
        lab.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.45, -1.7, 0])
        # decision maps: gradient descent against the natural gradient, through training
        snaps = list(n["snap_steps"])
        X, y = np.asarray(n["X"]), np.asarray(n["y"])
        P, N = int(n["P"]), len(y)

        def dmap(o, k, center, size=2.3):
            p = np.asarray(n[f"snaps_{o}"])[k].reshape(41, 41)[::-1]  # image rows run top to bottom
            c0, c1 = np.array(ManimColor(C.TRUE_P).to_rgb()), np.array(ManimColor(C.MODEL_Q).to_rgb())
            rgb = (255 * (c0[None, None] * (1 - p[..., None]) + c1[None, None] * p[..., None])).astype(np.uint8)
            img = ImageMobject(np.concatenate([rgb, np.full((41, 41, 1), 230, np.uint8)], 2)).set_height(size).move_to(center)
            pts = VGroup(*[Dot(center + np.array([x_[0], x_[1], 0]) * size / 7.2, radius=0.012,
                               color=WHITE if yy else BLACK) for x_, yy in zip(X[::3], y[::3])])
            return Group(img, pts)

        cg, cn = np.array([1.9, 1.3, 0]), np.array([5.0, 1.3, 0])
        maps = {o: [dmap(o, k, c_) for k in range(len(snaps))] for o, c_ in (("gd", cg), ("ng", cn))}
        mh = VGroup(label(OPT_NAMES["gd"], font_size=20, color=GDC).next_to(maps["gd"][0], UP, buff=0.08),
                    label(OPT_NAMES["ng"], font_size=20, color=NGC).next_to(maps["ng"][0], UP, buff=0.08))
        stp = Integer(0, font_size=24, color=WHITE)
        sl = VGroup(label(r"step", font_size=22, color=GREY_A), stp).arrange(RIGHT, buff=0.12).move_to([3.45, -0.3, 0])
        med = {o: float(np.median(curves[o][:, -1, 1])) for o in opts}
        k100 = 100
        at100 = {o: float(np.median(curves[o][:, k100, 1])) for o in opts}
        order = sorted(opts, key=lambda o: at100[o])
        tag = note(r"Part 9's spirals; \ a $2$--$24$--$24$--$2$ network; \ each at its best of $5$ rates, \ $3$ seeds "
                   r"(band: \ min to max)\\NG: full Fisher + damping; \ K-FAC: sampled model-label factors + factor damping").to_corner(DL, buff=0.15)
        edges = [o for o in opts if bool(n[f"edge_{o}"])]
        ecomment = (f" {SAY[edges[0]].capitalize()}'s best rate was at the end of its grid, so it may do a little better "
                    "still." if edges else "")
        said1 = ("The natural gradient carves out the two spirals almost at once. "
            if order[0] == "ng" else "")
        with self.voiceover(
            "Race them on part nine's spirals: gradient descent, Adam, damped K-FAC and a damped full-Fisher natural gradient, each at "
            "its best of five learning rates, three seeds each. <bookmark mark='a'/> After a hundred steps, the "
            f"order is {SAY[order[0]]}, then {SAY[order[1]]}, {SAY[order[2]]} and {SAY[order[3]]}. "
            f"<bookmark mark='b'/> On the right, what the network believes, as it trains: gradient descent's map "
            "and the natural gradient's, at the same steps. "
            + said1
            + f"<bookmark mark='c'/> The full Fisher acts on {P} parameters. Here a Woodbury identity computes the "
            f"damped direction through a smaller system of {N} equations, one per training example. At scale, even "
            "full-Fisher geometry is costly, so K-FAC uses layer factors. Next chapter's Shampoo uses a related "
            "Kronecker idea." + ecomment
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), FadeIn(lab), FadeIn(tag))
            self.play(FadeIn(bands))
            self.add(*live)
            self.play(FadeIn(maps["gd"][0]), FadeIn(maps["ng"][0]), FadeIn(mh), FadeIn(sl))
            vo.wait_until("a")
            # Replay cached snapshots in chronological order. The old sequence
            # advanced the curve alone to 100, then rewound it to snapshot 10.
            # Keep the original 3.0 + 4 * 1.2 seconds of replay animation.
            split = snaps.index(k100)

            def advance(k, duration):
                self.play(t.animate.set_value(snaps[k]), FadeOut(maps["gd"][k - 1]), FadeIn(maps["gd"][k]),
                          FadeOut(maps["ng"][k - 1]), FadeIn(maps["ng"][k]), ChangeDecimalToValue(stp, snaps[k]),
                          run_time=duration, rate_func=linear)

            for k in range(1, split + 1):
                advance(k, 3.0 / split)
            vo.wait_until("b")
            for k in range(split + 1, len(snaps)):
                advance(k, 1.2 * (len(snaps) - 1) / (len(snaps) - 1 - split))
            self.play(t.animate.set_value(T), run_time=1.0)
            for m_ in live:
                m_.clear_updaters()
            vo.wait_until("c")
        self.wait(0.3)
        self.clear_scene()

    def takeaway(self):
        t = takeaway_card(r"The right ruler is the model's own",
                          r"The ideal natural-gradient direction $-\eta F^{-1} g$ measures local prediction change, \ "
                          r"independent of smooth invertible coordinates. \ K-FAC approximates it with two small "
                          r"Kronecker factors per layer.",
                          r"Next: \ Shampoo's Kronecker factors, \ from the gradient alone")
        with self.voiceover(
            "So the natural gradient measures a step by what it does to the model, and K-FAC makes that affordable "
            "with two small matrices per layer. Next, Shampoo, which gets its two matrices from the gradient alone."
        ):
            self.play(FadeIn(t[0], shift=UP * 0.2))
            self.play(FadeIn(t[1]))
        self.wait(0.3)
        self.clear_scene()
