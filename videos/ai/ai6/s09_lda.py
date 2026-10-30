from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import AUSTEN, BOUNDARY, DICKENS, HIST, HL, MONO, chapter, load, sci_tex

U = 0.95  # screen units per standard deviation


class LDA(VoiceoverScene):
    def construct(self):
        chapter(self, 8, r"Fisher's direction", r"Which way do the two authors look most different?",
                "Chapter eight. Fisher's discriminant.")
        self.fisher()
        self.eigen()

    # ------------------------------------------------------------------
    def fisher(self):
        p = load("pages")
        X2, y, test = np.asarray(p["X2"]), np.asarray(p["y"]), np.asarray(p["test"], bool)
        mu, sd = X2[~test].mean(0), X2[~test].std(0)
        Z = (X2 - mu) / sd  # each rate in its own standard deviations, so directions look like directions
        tr = np.nonzero(~test)[0]
        A, D = Z[tr][y[tr] == 0], Z[tr][y[tr] == 1]

        def J(th):
            u = np.array([math.cos(th), math.sin(th)])
            pa, pd = A @ u, D @ u
            return (pd.mean() - pa.mean()) ** 2 / (pa.var() + pd.var())

        Sw = np.cov(A.T) * (len(A) - 1) + np.cov(D.T) * (len(D) - 1)
        wbest = np.linalg.solve(Sw, D.mean(0) - A.mean(0))
        best = math.atan2(wbest[1], wbest[0]) % math.pi
        ths = np.linspace(0, math.pi, 181)
        Js = np.array([J(t) for t in ths])
        assert abs(ths[np.argmax(Js)] - best) < 0.03
        u_b = wbest / np.linalg.norm(wbest)  # pointing from Austen towards Dickens (the angle above is only mod pi)
        c = 0.5 * ((A @ u_b).mean() + (D @ u_b).mean())
        acc = float((((Z[test] @ u_b) > c) == y[test]).mean())
        assert abs(acc - load("lda")["acc2"]) < 1e-9
        C0 = np.array([-3.3, -0.2, 0])

        def S(z):
            return C0 + U * np.array([z[0], z[1], 0])

        g = np.random.default_rng(2)
        jit = g.uniform(-0.04, 0.04, Z.shape)
        dots = VGroup(*[Dot(S(Z[i] + jit[i]), radius=0.04, color=AUSTEN if y[i] == 0 else DICKENS, fill_opacity=0.75)
                        for i in tr if np.abs(Z[i]).max() < 3.4])
        axes_l = VGroup(Line(S([-3.4, 0]), S([3.4, 0]), color=GREY_D), Line(S([0, -3.4]), S([0, 3.4]), color=GREY_D))
        names = VGroup(label(r"``the''", font_size=22, color=GREY_A).next_to(S([3.4, 0]), DOWN, buff=0.1),
                       label(r"``not''", font_size=22, color=GREY_A).next_to(S([0, 3.4]), LEFT, buff=0.1))
        unit = label(r"each rate in its own standard deviations", font_size=20, color=GREY_B).next_to(S([0, -3.4]), DOWN, buff=0.12)
        th = ValueTracker(0.15)

        def direction():
            t = th.get_value()
            u = np.array([math.cos(t), math.sin(t)])
            return VGroup(Line(S(-3.6 * u), S(3.6 * u), color=WHITE, stroke_width=3),
                          Arrow(S(np.zeros(2)), S(1.2 * u), buff=0, color=WHITE, stroke_width=5))

        # the piles: histograms of the projections, on their own axis
        hx0, hy0, HW = 1.2, -2.2, 5.4
        edges = np.linspace(-3.5, 3.5, 36)

        def piles():
            t = th.get_value()
            u = np.array([math.cos(t), math.sin(t)])
            out = VGroup(Line([hx0, hy0, 0], [hx0 + HW, hy0, 0], color=GREY_C, stroke_width=2))
            for P, col in ((A, AUSTEN), (D, DICKENS)):
                h, _ = np.histogram(P @ u, bins=edges, density=True)
                pts = [np.array([hx0, hy0, 0])]
                for k, v in enumerate(h):
                    xa = hx0 + HW * (edges[k] + 3.5) / 7
                    xb = hx0 + HW * (edges[k + 1] + 3.5) / 7
                    pts += [np.array([xa, hy0 + 2.0 * v, 0]), np.array([xb, hy0 + 2.0 * v, 0])]
                pts.append(np.array([hx0 + HW, hy0, 0]))
                out.add(Polygon(*pts, color=col, stroke_width=2, fill_color=col, fill_opacity=0.3))
            return out

        pile_l = label(r"every page, squashed onto the direction", font_size=22, color=GREY_A).move_to([hx0 + HW / 2, hy0 - 0.35, 0])
        # Fisher's score against the angle
        jax = Axes(x_range=[0, 180, 45], y_range=[0, float(Js.max()) * 1.15, 1], x_length=4.6, y_length=1.9, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([3.9, 0.7, 0])
        jcurve = VMobject(color=C.BITS, stroke_width=3).set_points_smoothly(
            [jax.c2p(math.degrees(t), v) for t, v in zip(ths, Js)])
        jdot = always_redraw(lambda: Dot(jax.c2p(math.degrees(th.get_value()), J(th.get_value())), radius=0.07, color=WHITE))
        colors = {r"\mu_D": DICKENS, r"\mu_A": AUSTEN}
        jf = cmath(r"\text{score} =", r"\frac{(\text{gap between the centres})^2}{\text{spread} + \text{spread}}",
                   font_size=30).next_to(jax, UP, buff=0.2)
        jl = label(r"direction's angle", font_size=20, color=GREY_A).next_to(jax.x_axis, DOWN, buff=0.1)
        wf = cmath(r"\mathbf{w}", r"\propto", r"S_W^{-1}", r"(", r"\mu_D", "-", r"\mu_A", r")", colors=colors, font_size=40)
        wf.move_to([3.9, 1.6, 0])
        wn = label(r"$S_W$: \ the spread within each author", font_size=22, color=GREY_A).next_to(wf, DOWN, buff=0.15)
        res = label(rf"cut halfway: \ ${100 * acc:.1f}\%$ of test pages right", font_size=28, color=BOUNDARY)
        res.next_to(wn, DOWN, buff=0.4)
        cite_ = cite(r"R.~A.~Fisher, \textit{The Use of Multiple Measurements in Taxonomic Problems} (1936)", corner=UL)
        pl = always_redraw(piles)
        dl = always_redraw(direction)
        # S_W^-1, pictured: stretch the space until each author's cloud is round, then point from centre to centre
        frame_ = Rectangle(width=3.6, height=1.7, stroke_opacity=0)

        def two_clouds(round_):
            if round_:
                ca, cd = np.array([-1.0, -0.15, 0]), np.array([1.0, 0.15, 0])
                shapes = [Circle(radius=0.42).move_to(c_) for c_ in (ca, cd)]
            else:
                ca, cd = np.array([-0.35, -0.3, 0]), np.array([0.35, 0.3, 0])
                shapes = [Ellipse(width=2.2, height=0.42).rotate(-20 * DEGREES).move_to(c_) for c_ in (ca, cd)]
            for sh, col in zip(shapes, (AUSTEN, DICKENS)):
                sh.set_stroke(col, 2.5).set_fill(col, 0.25)
            return VGroup(*shapes, Dot(ca, radius=0.06, color=AUSTEN), Dot(cd, radius=0.06, color=DICKENS),
                          Arrow(ca, cd, buff=0.08, color=WHITE, stroke_width=4, max_tip_length_to_length_ratio=0.2))

        before = two_clouds(False)
        before[4].set_opacity(0)
        swc = gloss(r"$S_W^{-1}$", r"stretch the space until each author's cloud is round,\\ then point from one "
                    r"centre to the other", picture=VGroup(frame_, before), width=4.6)
        swc.move_to([3.9, -1.3, 0])
        sp = swc[1][-1]  # the card's copy of (frame, clouds)
        after = VGroup(frame_.copy(), two_clouds(True))
        after.scale(sp[0].width / frame_.width).move_to(sp[0])
        with self.voiceover(
            "In 1936, Ronald Fisher, separating species of iris by the sizes of their petals, asked a different question. Along which direction do the two groups look most "
            "different? <bookmark mark='a'/> Pick a direction, and squash every page onto it. Each author becomes a "
            "pile. <bookmark mark='b'/> Turn the direction, and the piles slide together, or apart. Fisher's score "
            "is the gap between the piles' centres, squared, divided by how spread out they are."
        ) as vo:
            self.play(FadeIn(axes_l), FadeIn(names), FadeIn(unit), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.003),
                      FadeIn(cite_), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(dl), FadeIn(pl), FadeIn(pile_l))
            vo.wait_until("b")
            self.play(Create(jax), FadeIn(jl), Write(jf), Create(jcurve), FadeIn(jdot))
            self.play(th.animate.set_value(math.pi * 0.97), run_time=5.0, rate_func=smooth)
        like_lr = (", the same as logistic regression." if abs(acc - load("logistic")["acc2"]) < 0.006 else ".")
        with self.voiceover(
            "The best direction has a formula: the difference between the two centres, corrected by the inverse of "
            "the spread within each author. <bookmark mark='w'/> That correction means: stretch the space until each "
            "author's cloud is round, then point from one centre to the other. <bookmark mark='a'/> Here, it leans mostly on 'not'. "
            "<bookmark mark='b'/> Cut halfway between the piles, and you have a classifier. It gets "
            f"{100 * acc:.0f} percent of the test pages right{like_lr} <bookmark mark='c'/> When each group is a bell "
            "of the same shape, this cut is exactly the best one possible."
        ) as vo:
            self.play(th.animate.set_value(best), run_time=2.0)
            self.play(FadeOut(jf), FadeOut(jax), FadeOut(jcurve), FadeOut(jdot), FadeOut(jl), FadeIn(wf), FadeIn(wn))
            vo.wait_until("w")
            self.play(FadeIn(swc))
            self.play(Transform(sp[1], after[1]), run_time=1.6)
            vo.wait_until("a")
            self.play(FadeOut(swc), Indicate(dl, color=C.BITS))
            vo.wait_until("b")
            ub = u_b
            perp = np.array([-ub[1], ub[0]])
            boundary = Line(S(c * ub - 3.4 * perp), S(c * ub + 3.4 * perp), color=BOUNDARY, stroke_width=4)
            hcut = DashedLine([hx0 + HW * (c + 3.5) / 7, hy0, 0], [hx0 + HW * (c + 3.5) / 7, hy0 + 1.7, 0], color=BOUNDARY)
            self.play(Create(boundary), Create(hcut), FadeIn(res))
        for m in (pl, dl, jdot):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def eigen(self):
        ld = load("lda")
        colors = {r"S_B": HL, r"S_W": GREY_A}
        rows = [
            cmath(r"J(\mathbf{w})", "=", r"\frac{\big(\mathbf{w}^{\top}(\boldsymbol\mu_D - \boldsymbol\mu_A)\big)^2}"
                  r"{\mathbf{w}^{\top}S_W\,\mathbf{w}} = \frac{\mathbf{w}^{\top}S_B\,\mathbf{w}}{\mathbf{w}^{\top}S_W\,\mathbf{w}}",
                  font_size=34, colors=colors),
            cmath(r"\nabla J = 0", r"\;\Longleftrightarrow\;", r"S_B\,\mathbf{w} = J(\mathbf{w})\, S_W\,\mathbf{w}",
                  font_size=34, colors=colors),
            cmath(r"S_B\,\mathbf{w}", r"\;\propto\;", r"\boldsymbol\mu_D - \boldsymbol\mu_A", font_size=34, colors=colors),
            cmath(r"\mathbf{w}", r"\;\propto\;", r"S_W^{-1}(\boldsymbol\mu_D - \boldsymbol\mu_A)", font_size=34,
                  colors=colors),
        ]
        whys = [why(r"$S_B = \Delta\boldsymbol\mu\,\Delta\boldsymbol\mu^{\top}$: \\ between the authors"),
                why(r"the quotient rule: \\ a generalized eigenproblem"), why(r"$S_B$ has rank one"),
                why(r"Fisher's direction")]
        step = ladder(self, rows, whys, keep=4, top=3.3, x=-2.0, buff=0.36, edge=6.8)
        ev = ld["eigvals"]
        top = ld["top"]
        sg = ld["top_signs"]
        checks = VGroup(
            label(r"all $70$ standardized rates:", font_size=26, color=GREY_A),
            label(rf"generalized eigenvalues: \ ${ev[0]:.4f}$, \ then ${sci_tex(abs(ev[1]), 0)}$ \ (rank ${ld['rank_SB']}$)",
                  font_size=26, color=GREY_A),
            label(rf"eigenvector against the formula: \ cosine ${ld['cos_eig']:.6f}$", font_size=26, color=HL),
            label(rf"against least squares on a $0/1$ target: \ cosine ${ld['cos_ls']:.6f}$", font_size=26, color=HL),
            label(rf"held-out pages: \ ${100 * ld['acc70']:.1f}\%$", font_size=26, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DL, buff=0.35)
        words = VGroup(label(r"heaviest words", font_size=22, color=GREY_A),
                       *[data_text(w, font=MONO, font_size=22, color=DICKENS if s_ > 0 else AUSTEN)
                         for w, s_ in zip(top, sg)]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DR, buff=0.4)
        same = ld["cos_ls"] > 0.9999

        def heat(M, title):
            M = np.asarray(M, float)
            v = np.abs(M) / np.abs(M).max()
            v = v ** 0.5
            col = np.array(ManimColor(HL).to_rgb())
            rgb = (v[..., None] * col[None, None] + (1 - v[..., None]) * np.array([0.07, 0.09, 0.13]))
            img = ImageMobject((np.concatenate([rgb, np.ones(v.shape + (1,))], -1) * 255).astype(np.uint8))
            img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
            img.scale_to_fit_width(1.9)
            return Group(img, SurroundingRectangle(img, buff=0, color=GREY_C, stroke_width=1),
                         label(title, font_size=20, color=GREY_A).next_to(img, DOWN, buff=0.1))

        hb = heat(ld["SB"], r"$S_B$: \ rank $1$")
        hw = heat(ld["SW"], r"$S_W$: \ full rank")
        mats = Group(hb, hw).arrange(RIGHT, buff=0.4).to_corner(DR, buff=0.5).shift(UP * 0.2)
        mats_t = label(r"the two $70 \times 70$ scatter matrices \ (size of each entry)", font_size=20,
                       color=GREY_B).next_to(mats, UP, buff=0.15)
        names = ", ".join(f"'{w}'" for w in top[:3])
        also = ("It also agrees with least squares on a zero-one target: with two classes, the two are the same line."
                if same else "And least squares on a zero-one target points the same way.")
        with self.voiceover(
            "Where does the formula come from? <bookmark mark='a'/> Fisher's score is a ratio of two quadratic forms: "
            "the spread between the authors over the spread within them. <bookmark mark='b'/> Set its gradient to "
            "zero, and you get a generalized eigenproblem: S B w equals J times S W w. <bookmark mark='c'/> But S B "
            "has rank one: it only ever points along the difference of the means. <bookmark mark='d'/> So the "
            "answer is S W inverse times that difference. <bookmark mark='e'/> On all seventy rates, the eigensolver "
            f"finds one nonzero eigenvalue, and its eigenvector agrees with the formula to {ld['cos_eig']:.6f}. {also}"
            f"<bookmark mark='f'/> It leans hardest on {names}, and gets {100 * ld['acc70']:.0f} percent of the "
            "held-out pages right."
        ) as vo:
            vo.wait_until("a")
            step(0)
            self.play(FadeIn(mats), FadeIn(mats_t))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(Indicate(hb, color=HL, scale_factor=1.05), FadeIn(checks[0]), FadeIn(checks[1]))
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(FadeIn(checks[2]))
            self.play(FadeIn(checks[3]))
            vo.wait_until("f")
            self.play(FadeOut(mats), FadeOut(mats_t))
            self.play(FadeIn(checks[4]), FadeIn(words))
        self.wait(0.3)
        self.clear_scene()
