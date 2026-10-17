from __future__ import annotations


import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import (AUSTEN, DICKENS, X_RANGE, Y_RANGE, crop_to_axes, line_in_box, load,
                                  page_dots, page_plane, region_image)

SIG = C.MODEL_Q


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


class Logistic(VoiceoverScene, ThreeDScene):
    def construct(self):
        p = load("pages")
        self.X2, self.y, self.test = np.asarray(p["X2"]), np.asarray(p["y"]), np.asarray(p["test"], bool)
        self.lg = load("logistic")
        self.card()
        self.score()
        self.sheet()
        self.descend()
        self.result()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(2, r"Logistic regression", r"How do you turn a line into a probability?", part=5)
        with self.voiceover("Chapter two. Logistic regression."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def score(self):
        w, b = np.asarray(self.lg["w"]), float(self.lg["b"])
        plane = page_plane(x_length=6.4, y_length=4.4, center=[-3.4, -0.2, 0])
        ax = plane[0]
        tr = np.nonzero(~self.test)[0]
        dots = page_dots(ax, self.X2, self.y, idx=tr, jitter=0.4, radius=0.045)
        bl = line_in_box(ax, w, b)
        colors = {r"w_1": SIG, r"w_2": SIG, r"b": SIG}
        sc = cmath(r"s", "=", r"w_1", r"\,x_{\text{the}}", "+", r"w_2", r"\,x_{\text{not}}", "+", r"b", colors=colors,
                   font_size=40).move_to([3.4, 2.6, 0])
        side = VGroup(label(r"$s > 0$: \ Dickens", font_size=26, color=DICKENS),
                      label(r"$s < 0$: \ Austen", font_size=26, color=AUSTEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        side.next_to(sc, DOWN, buff=0.25)
        # the sigmoid
        sax = Axes(x_range=[-6, 6, 2], y_range=[0, 1, 0.5], x_length=5.2, y_length=2.2, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([3.4, -1.6, 0])
        zs = np.linspace(-6, 6, 120)
        sg = VMobject(stroke_width=4).set_points_smoothly([sax.c2p(z, sigmoid(z)) for z in zs])
        sg.set_color([AUSTEN, DICKENS])
        sf = cmath(r"\sigma(s) = \frac{1}{1 + e^{-s}}", font_size=34).next_to(sax, UP, buff=0.35).align_to(sax, RIGHT)
        sl = VGroup(MathTex(r"s", font_size=26, color=GREY_A).next_to(sax.x_axis, RIGHT, buff=0.1),
                    label(r"$P(\text{Dickens})$", font_size=22, color=GREY_A).next_to(sax.y_axis.get_top(), LEFT, buff=0.12))
        with self.voiceover(
            "The simplest classifier draws a straight line. Give every page a score: a weighted sum of its two "
            "rates, plus a constant. <bookmark mark='a'/> Positive means Dickens, negative means Austen, and the "
            "line is where the score is exactly zero. <bookmark mark='b'/> But a score isn't a probability. Squash "
            "it with the sigmoid: large positive scores go to one, large negative scores to zero, and zero to a half."
        ) as vo:
            self.play(Create(ax), FadeIn(plane[1:]), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.003),
                      Write(sc), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(bl), FadeIn(side))
            vo.wait_until("b")
            self.play(Create(sax), FadeIn(sl), Write(sf))
            self.play(Create(sg), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sheet(self):
        w, b = np.asarray(self.lg["w"]), float(self.lg["b"])
        axes = ThreeDAxes(x_range=[*X_RANGE, 10], y_range=[*Y_RANGE, 4], z_range=[0, 1, 0.5], x_length=7.0, y_length=4.6,
                          z_length=2.6, axis_config={"stroke_color": GREY_C, "include_ticks": False, "include_tip": False})
        axes.shift(DOWN * 0.4)

        def P(x, v):
            return float(sigmoid(w[0] * x + w[1] * v + b))

        surf = Surface(lambda u, v: axes.c2p(u, v, P(u, v)), u_range=list(X_RANGE), v_range=list(Y_RANGE),
                       resolution=(36, 24), fill_opacity=0.55, stroke_width=0.3, stroke_color="#0E1117",
                       checkerboard_colors=False)
        surf.set_fill_by_value(axes=axes, colorscale=[(AUSTEN, 0.0), ("#8B7FB8", 0.5), (DICKENS, 1.0)], axis=2)
        g = np.random.default_rng(3)
        tr = np.nonzero(~self.test)[0]
        pick = g.choice(tr, size=260, replace=False)
        pts = VGroup()
        for i in pick:
            x, v = self.X2[i]
            if X_RANGE[0] <= x <= X_RANGE[1] and Y_RANGE[0] <= v <= Y_RANGE[1]:
                jx, jy = g.uniform(-0.4, 0.4, 2)
                pts.add(Dot(axes.c2p(x + jx, v + jy, float(self.y[i])), radius=0.04,
                            color=AUSTEN if self.y[i] == 0 else DICKENS))
        head = label(r"The probability of Dickens, \ over every page", font_size=32).to_edge(UP, buff=0.35)
        colors = {r"y_i": WHITE, r"q_i": SIG}
        loss = cmath(r"\mathcal{L}", "=", r"-\frac{1}{n}\sum_i", r"\big[", r"y_i", r"\log_2", r"q_i", "+",
                     r"(1-y_i)", r"\log_2", r"(1-q_i)", r"\big]", colors=colors, font_size=34)
        loss.to_corner(DL, buff=0.4)
        ln = label(rf"Part 1's cross-entropy: \ ${self.lg['loss_bits']:.2f}$ bits per page at the best sheet",
                   font_size=24, color=GREY_A).next_to(loss, UP, buff=0.15).align_to(loss, LEFT)
        lift = label(r"each page lifted to $0$ (Austen) or $1$ (Dickens)", font_size=24, color=GREY_A)
        lift.to_corner(UR, buff=0.4).shift(DOWN * 0.6)
        for m in (head, loss, ln, lift):
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-115 * DEGREES, zoom=0.85)
        with self.voiceover(
            "Over the whole plane, that makes a sheet: the probability of Dickens, rising from Austen's side to "
            "Dickens's. <bookmark mark='a'/> Lift each training page to the height of its true answer: zero for "
            "Austen, one for Dickens. The sheet should pass close to them. <bookmark mark='b'/> Fitting it means "
            "minimizing the average surprise, part one's cross-entropy, by part three's gradient descent. The best "
            "sheet leaves about half a bit of surprise per page."
        ) as vo:
            self.play(Create(axes), FadeIn(surf), FadeIn(head), run_time=1.6)
            self.begin_ambient_camera_rotation(rate=0.06)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in pts], lag_ratio=0.005), FadeIn(lift), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(loss), FadeIn(ln))
        self.stop_ambient_camera_rotation()
        self.wait(0.3)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

    # ------------------------------------------------------------------
    def result(self):
        lg = self.lg
        plane = page_plane(x_length=7.0, y_length=4.6, center=[-2.6, -0.3, 0])
        ax = plane[0]
        prob, xs, ys = crop_to_axes(lg["prob"], lg["xs"], lg["ys"])
        img = region_image(prob, xs, ys, ax, opacity=0.4)
        te = np.nonzero(self.test)[0]
        dots = page_dots(ax, self.X2, self.y, idx=te, jitter=0.4, radius=0.055)
        bl = line_in_box(ax, np.asarray(lg["w"]), float(lg["b"]))
        n_te = int(self.test.sum())
        a2 = label(rf"held-out pages, \ $2$ rates: \ ${100 * lg['acc2']:.1f}\%$ right", font_size=30, color=WHITE)
        a70 = label(rf"all $70$ rates: \ ${round(lg['acc70'] * n_te)}$ of ${n_te}$, \ ${100 * lg['acc70']:.1f}\%$",
                    font_size=30, color=C.BITS)
        VGroup(a2, a70).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.0, 0.6, 0])
        note_ = label(r"seventy small words \\ are a fingerprint", font_size=28, color=GREY_A).next_to(a70, DOWN, buff=0.6)
        note_.align_to(a70, LEFT)
        with self.voiceover(
            rf"Now the test: pages the method never saw. With two rates, the line gets {100 * lg['acc2']:.0f} "
            "percent of them right. <bookmark mark='a'/> Give it all seventy rates instead, and the same method gets "
            f"{round(lg['acc70'] * n_te)} of the {n_te} test pages right. A handful of small words, counted, are a "
            "fingerprint."
        ) as vo:
            self.play(Create(ax), FadeIn(plane[1:]), FadeIn(img), Create(bl))
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01), FadeIn(a2), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(a70))
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def descend(self):
        """How it is fitted: gradient descent, the line swinging into place as the loss falls."""
        import math

        lg = self.lg
        P = np.asarray(lg["path"])  # iteration, w1, w2, b (original units), loss in bits
        cv = np.asarray(lg["curve"])
        # the loss at every step the picture shows, and every fifth one besides: the fall is in the first few steps
        cv = np.array(sorted({**{float(a): float(b) for a, b in cv if a >= 1}, **{float(r[0]): float(r[4]) for r in P if r[0] >= 1}}.items()))
        plane = page_plane(x_length=6.4, y_length=4.4, center=[-3.0, -0.3, 0])
        ax = plane[0]
        tr = np.nonzero(~self.test)[0]
        dots = page_dots(ax, self.X2, self.y, idx=tr, jitter=0.4, radius=0.045)
        lines = [line_in_box(ax, P[k, 1:3], float(P[k, 3])) for k in range(1, len(P))]
        bx = CornerAxes(x_range=[0, math.log10(cv[-1, 0]), 1], y_range=[0, 1.05, 0.5], x_length=4.4, y_length=2.8, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.9, -0.3, 0])
        xt = VGroup(*[MathTex(t_, font_size=20, color=GREY_B).next_to(bx.c2p(math.log10(v), 0), DOWN, buff=0.08)
                      for v, t_ in ((1, "1"), (10, "10"), (100, "100"), (1000, "1{,}000"))])
        xn = label(r"steps of gradient descent \ (log scale)", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yn = label(r"cross-entropy on the training pages, \ bits", font_size=20, color=GREY_A).next_to(bx, UP, buff=0.12).align_to(bx, LEFT)
        t = ValueTracker(1)
        dot = always_redraw(lambda: Dot(bx.c2p(math.log10(t.get_value()), float(np.interp(t.get_value(), cv[:, 0], cv[:, 1]))),
                                        radius=0.07, color=C.BITS))
        cnt = always_redraw(lambda: MathTex(rf"\text{{step }}{int(round(t.get_value())):,}".replace(",", "{,}"), font_size=28,
                                            color=C.BITS).next_to(ax, UP, buff=0.2))
        settle = int(next((P[k, 0] for k in range(1, len(P)) if abs(P[k, 4] - P[-1, 4]) < 0.005), P[-1, 0]))
        # convex: one bowl, one bottom; an egg-crate has many, and where you stop depends on where you start
        bx_ = np.linspace(-1.0, 1.0, 60)
        bowl_c = VMobject(stroke_color=GREY_B, stroke_width=3).set_points_smoothly(
            [np.array([u, 0.6 * u * u, 0]) for u in bx_])
        crate_c = VMobject(stroke_color=GREY_B, stroke_width=3).set_points_smoothly(
            [np.array([u, 0.3 * u * u + 0.15 * math.cos(9.5 * u), 0]) for u in bx_])
        bowl_g = VGroup(bowl_c, Dot([0, 0, 0], radius=0.07, color=C.BITS),
                        label(r"convex: \ one bottom", font_size=24, color=C.BITS).next_to(bowl_c, DOWN, buff=0.12))
        lows = [k * 2 * math.pi / 9.5 + math.pi / 9.5 for k in (-2, -1, 0, 1)]  # the crate's dips, near cos = -1
        crate_g = VGroup(crate_c, *[Dot([u, 0.3 * u * u - 0.15, 0], radius=0.06, color=C.PENALTY) for u in lows],
                         label(r"not convex: \ many bottoms", font_size=24, color=C.PENALTY).next_to(crate_c, DOWN, buff=0.12))
        convex = gloss(r"convex", r"shaped like one bowl:\\ every downhill path ends at the same bottom",
                       picture=VGroup(bowl_g, crate_g).arrange(RIGHT, buff=0.5, aligned_edge=DOWN), corner=UR, width=4.4)
        with self.voiceover(
            "How is that line found? By gradient descent on the cross-entropy, the same recipe as every model in "
            "this series. <bookmark mark='a'/> It starts with every weight at zero: a coin flip for every page. "
            "Each step nudges the weights against the gradient: <bookmark mark='b'/> the line swings toward the gap "
            f"between the two authors, the loss falls, and by about step {settle} it has settled. "
            "<bookmark mark='c'/> A convex loss is shaped like a single bowl: it has one bottom, and every downhill "
            "path ends there, so where it settles doesn't depend on where it started."
        ) as vo:
            self.play(Create(ax), FadeIn(plane[1:]), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.005),
                      Create(bx), FadeIn(xt), FadeIn(xn), FadeIn(yn), run_time=1.5)
            self.add(dot, cnt)
            vo.wait_until("a")
            cur = lines[0]
            self.play(Create(cur))
            vo.wait_until("b")
            for k in range(2, len(P)):
                seg = [bx.c2p(math.log10(a), b) for a, b in cv if P[k - 1, 0] <= a <= P[k, 0]]
                anims = [Transform(cur, lines[k - 1]), t.animate.set_value(P[k, 0])]
                if len(seg) > 1:
                    anims.append(Create(VMobject(color=SIG, stroke_width=3).set_points_as_corners(seg)))
                self.play(*anims, run_time=0.5 if P[k, 0] < 200 else 0.35)
            vo.wait_until("c")
            self.play(FadeIn(convex))
        self.wait(0.3)
        self.remove(dot, cnt)
        self.clear_scene()
