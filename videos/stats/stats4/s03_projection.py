from __future__ import annotations

import numpy as np

from videos.stats.stats4.common import *  # noqa: F403


class Projection(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.lab()
        self.gram_schmidt()
        self.eigen()
        self.anova()
        self.leverage()

    def card(self):
        card = chapter_card(2, r"Projections", r"The closest point in a subspace", lit=(1805,), part=PART)
        with self.voiceover("Chapter two. Projections."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def derive(self):
        rows = [
            cmath(r"P\mathbf y", r"=", r"A\mathbf b", r"\quad \text{for some } \mathbf b", font_size=34),
            cmath(r"A^\top(\mathbf y - A\mathbf b)", r"=", r"\mathbf 0", font_size=36),
            cmath(r"\mathbf b", r"=", r"(A^\top A)^{-1} A^\top \mathbf y", font_size=36),
            cmath(r"P", r"=", r"A (A^\top A)^{-1} A^\top", font_size=40),
        ]
        rows[3][0].set_color(FIT)
        whys = [why(r"the projection lies in the column space"), why(r"the residual is $\perp$ every column"),
                why(r"the normal equations; \ $A$ of full column rank"), why(r"so $P^2 = P$ and $P^\top = P$")]
        dfn = definition_card(r"Orthogonal projection", r"a matrix $P$ with $P^2 = P$ and $P^\top = P$: \ it sends "
                              r"$\mathbf y$ to the closest point of its column space", color=FIT, width=5.4,
                              font_size=22).to_corner(DR, buff=0.35)
        with self.voiceover(
            "Projecting onto a line is the simplest case. Statistics needs projections onto any subspace, spanned "
            "by the columns of a matrix A. <bookmark mark='a'/> The projection of y has to lie in the column space, "
            "so it's A times some vector b. <bookmark mark='b'/> And the residual has to be at right angles to every "
            "column, which is A transpose times the residual equal to zero. <bookmark mark='c'/> Solve: b is A "
            "transpose A inverse, A transpose y. These are the normal equations of least squares, named for the "
            "normal, the perpendicular. <bookmark mark='d'/> So the projection matrix is A, A transpose A inverse, A "
            "transpose: the hat matrix again. Multiply it by itself and the middle cancels, so it's idempotent; and "
            "it's symmetric. Those two properties define an orthogonal projection."
        ) as vo:
            self.play(FadeIn(dfn))
            step = ladder(self, rows, whys, keep=4, top=2.4, x=-1.6, buff=0.55)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                step(k, transform=k in (2,))
        self.clear_scene()

    def lab(self):
        d = load("projection")
        A, y = np.asarray(d["A"]), np.asarray(d["y"])
        lab = ProjectionLab(A, y, scale=0.62, center=(-3.0, -0.7, 0), axis_len=5.0)
        ns = lab.ns
        Py, r = lab.Py, lab.r
        info = VGroup(MathTex(r"A = " + mat_tex(A, "{:.0f}"), font_size=30, color=SPACE),
                      MathTex(r"\mathbf y = " + mat_tex(y[:, None], "{:.0f}"), font_size=30, color=DATA),
                      MathTex(r"P\mathbf y = " + mat_tex(Py[:, None], "{:.2f}"), font_size=30, color=FIT))
        info.arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.35).shift(RIGHT * 2.0)
        again = MathTex(r"P(P\mathbf y) = P\mathbf y", r",\qquad P\mathbf r = \mathbf 0", font_size=34).move_to([3.6, -0.4, 0])
        again[0].set_color(FIT)
        again[1].set_color(RES)
        perp = MathTex(rf"\langle \mathbf r, P\mathbf y\rangle = {float(r @ Py):.1e}", font_size=28, color=GREY_A)
        perp.next_to(again, DOWN, buff=0.4)
        pyth = MathTex(r"\|\mathbf y\|^2", r"=", r"\|P\mathbf y\|^2", r"+", r"\|\mathbf r\|^2", font_size=34)
        pyth[2].set_color(FIT)
        pyth[4].set_color(RES)
        pyth.next_to(perp, DOWN, buff=0.4)
        nums = MathTex(rf"{y @ y:.2f} = {Py @ Py:.2f} + {r @ r:.2f}", font_size=28).next_to(pyth, DOWN, buff=0.2)
        with self.voiceover(
            "Here's the projection lab, the build of this part. <bookmark mark='a'/> The green plane is the column "
            "space of a three-by-two matrix A: every combination of its two columns. <bookmark mark='b'/> The white "
            "vector is the data, y. <bookmark mark='c'/> Its projection, blue, is the closest point of the plane, "
            "<bookmark mark='d'/> and the residual, red, stands at right angles to the plane. Turn the space and you "
            "can see the right angle from every side. <bookmark mark='e'/> Project the projection again, and nothing "
            "moves: it's already in the plane. Project the residual, and it vanishes. <bookmark mark='f'/> And "
            "because the angle is right, Pythagoras splits the squared length of the data into fitted and residual "
            "parts: the decomposition behind every analysis of variance."
        ) as vo:
            self.add(ns)
            self.play(FadeIn(info))
            vo.wait_until("a")
            self.add(lab.space)
            self.play(NSpace.reveal(lab.space))
            vo.wait_until("b")
            self.add(lab.vy)
            self.play(NSpace.reveal(lab.vy))
            vo.wait_until("c")
            self.add(lab.vfit)
            self.play(NSpace.reveal(lab.vfit))
            vo.wait_until("d")
            self.add(lab.vres, lab.angle_mark)
            self.play(NSpace.reveal(lab.vres, lab.angle_mark))
            self.play(ns.turn(1.0, run_time=5.0))
            vo.wait_until("e")
            self.play(Write(again), Indicate(lab.vfit, color=FIT))
            self.play(FadeIn(perp))
            vo.wait_until("f")
            self.play(Write(pyth), FadeIn(nums), ns.turn(-0.6, run_time=3.0))
        lab.stop()
        self.clear_scene()

    def gram_schmidt(self):
        d = load("projection")
        A = np.asarray(d["A"])
        q1, q2 = np.asarray(d["q1"]), np.asarray(d["q2"])
        ns = NSpace(scale=0.62, center=[-3.0, -1.4, 0], angle=-0.6, tilt=0.38, axis_len=6.0)
        a1 = ns.vector(A[:, 0], color=GREY_A)
        a2 = ns.vector(A[:, 1], color=GREY_A)
        comp = ns.vector((A[:, 1] @ q1) * q1, color=GREY_C, stroke_width=3)
        perp_v = ns.vector(A[:, 1] - (A[:, 1] @ q1) * q1, color=EIG, origin=(A[:, 1] @ q1) * q1)
        v1 = ns.vector(q1 * 2, color=SPACE)
        v2 = ns.vector(q2 * 2, color=SPACE)
        rows = [
            cmath(r"\mathbf q_1", r"=", r"\frac{\mathbf a_1}{\|\mathbf a_1\|}", font_size=32),
            cmath(r"\mathbf q_2", r"=", r"\frac{\mathbf a_2 - \langle \mathbf a_2, \mathbf q_1\rangle \mathbf q_1}"
                  r"{\|\mathbf a_2 - \langle \mathbf a_2, \mathbf q_1\rangle \mathbf q_1\|}", font_size=30),
            cmath(r"A", r"=", r"QR", font_size=36),
            cmath(r"P", r"=", r"QQ^\top", font_size=36),
        ]
        whys = [why(r"normalize"), why(r"remove the part along $\mathbf q_1$"), why(r"$R$ upper triangular"),
                why(r"no inverse needed")]
        hc = note(r"Laplace (1812), Gram (1883), Schmidt (1907)").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Projections are easiest with orthonormal columns, and Gram–Schmidt makes them. <bookmark mark='a'/> "
            "Normalize the first column. <bookmark mark='b'/> From the second, subtract its projection onto the "
            "first, leaving the yellow part at right angles, and normalize that. <bookmark mark='c'/> The result is "
            "a factorization: A equals Q, with orthonormal columns, times R, upper triangular. "
            "<bookmark mark='d'/> With orthonormal columns the projection is just Q Q transpose: no inverse at all. "
            "That's not only elegant; chapter twelve shows it's how a computer should actually do least squares."
        ) as vo:
            self.add(ns, a1, a2)
            self.play(NSpace.reveal(a1, a2), FadeIn(hc))
            step = ladder(self, rows, whys, keep=4, top=2.9, x=3.0, buff=0.45, edge=6.9)
            vo.wait_until("a")
            self.add(v1)
            self.play(NSpace.reveal(v1))
            step(0, transform=False)
            vo.wait_until("b")
            self.add(comp, perp_v)
            self.play(NSpace.reveal(comp, perp_v))
            self.add(v2)
            self.play(NSpace.reveal(v2))
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
            vo.wait_until("d")
            step(3, transform=False)
            self.play(ns.turn(0.8, run_time=4.0))
        for m in (a1, a2, comp, perp_v, v1, v2):
            m.clear_updaters()
        self.clear_scene()

    def eigen(self):
        d = load("projection")
        rows = VGroup(
            MathTex(r"P\mathbf v = \mathbf v \quad \text{for } \mathbf v \text{ in the plane}", font_size=32, color=SPACE),
            MathTex(r"P\mathbf n = \mathbf 0 \quad \text{for } \mathbf n \perp \text{the plane}", font_size=32, color=RES),
            MathTex(rf"\text{{eigenvalues: }} {', '.join(f'{v:.0f}' for v in np.round(d['eig']))},\qquad "
                    rf"\operatorname{{rank}} P = \operatorname{{tr}} P = {d['trace']:.0f}", font_size=32, color=EIG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.6, 0])
        take = label(r"a projection is decided by its eigenvalues: \ ones on the subspace, \ zeros off it", font_size=28,
                     color=S.ACCENT).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The eigenvalues of a projection now make geometric sense. <bookmark mark='a'/> Every vector already in "
            "the plane is left alone: eigenvalue one. <bookmark mark='b'/> Every vector at right angles to the plane "
            "is sent to zero: eigenvalue zero. <bookmark mark='c'/> So this projection's eigenvalues are one, one and "
            "zero, and its rank, the dimension of the plane, equals its trace. Ones on the subspace, zeros off it: "
            "that's all a projection is."
        ) as vo:
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
            self.play(FadeIn(take))
        self.clear_scene()

    def anova(self):
        e = load("extras")["anova"]
        rows = [
            cmath(r"I", r"=", r"P_{\mathbf 1}", r"+", r"(P_X - P_{\mathbf 1})", r"+", r"(I - P_X)", font_size=38),
            cmath(r"\|\mathbf y - \bar y\mathbf 1\|^2", r"=", r"\|(P_X - P_{\mathbf 1})\mathbf y\|^2", r"+", r"\|(I - P_X)\mathbf y\|^2",
                  font_size=34),
            cmath(r"\text{SS}_{\text{total}}", r"=", r"\text{SS}_{\text{regression}}", r"+", r"\text{SS}_{\text{residual}}", font_size=36),
        ]
        for r in rows[1:]:
            r[2].set_color(FIT)
            r[4].set_color(RES)
        rows[0][4].set_color(FIT)
        rows[0][6].set_color(RES)
        whys = [why(r"three projections, \ mutually $\perp$"), why(r"Pythagoras, \ twice"), why(r"the analysis of variance")]
        nums = VGroup(
            MathTex(rf"{e['tot']:.0f}", r"=", rf"{e['reg']:.0f}", r"+", rf"{e['res']:.0f}", font_size=36),
            MathTex(rf"\text{{ranks: }}\ 1,\ \ {e['tr'][1]:.0f},\ \ {e['tr'][2]:.0f}", r"\qquad",
                    rf"R^2 = \tfrac{{\text{{SS}}_{{\text{{reg}}}}}}{{\text{{SS}}_{{\text{{tot}}}}}} = {e['r2']:.3f}", font_size=30),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.5)
        nums[0][2].set_color(FIT)
        nums[0][4].set_color(RES)
        tag = simulated_tag(r"simulated: the hook's 40 families", corner=UR)
        with self.voiceover(
            "Projections onto nested subspaces give the analysis of variance its shape. <bookmark mark='a'/> For "
            "the hook's forty families, split the identity into three projections: onto the ones vector; onto the "
            "part of the column space of X perpendicular to it; and onto everything perpendicular to X. They're "
            "mutually perpendicular, and their ranks are one, one and thirty-eight. <bookmark mark='b'/> Apply them "
            "to the centred data, and Pythagoras splits its squared length in two: the part the regression line "
            "explains, and the residual. <bookmark mark='c'/> Those are the sums of squares of every ANOVA table. "
            f"<bookmark mark='d'/> For the families, {e['tot']:.0f} equals {e['reg']:.0f} plus {e['res']:.0f}, and "
            f"the share explained, R squared, is {e['r2']:.2f}: parents' heights explain about a quarter of the "
            "variation in children's."
        ) as vo:
            self.play(FadeIn(tag))
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.6, buff=0.55, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=k == 2)
            vo.wait_until("d")
            self.play(FadeIn(nums, shift=UP * 0.2))
        self.clear_scene()

    def leverage(self):
        e = load("extras2")["lev"]
        x, y, h = np.asarray(e["x"]), np.asarray(e["y"]), np.asarray(e["h"])
        A = axes([150, 190], [0, 0.2], x_length=6.8, y_length=4.0, xlabel=r"mid-parent height (cm)", ylabel=r"leverage $h_{ii}$",
                 xticks=[150, 160, 170, 180, 190], yticks=[0, 0.1, 0.2], center=[-2.6, -0.6, 0])
        ax = A.ax
        bars = VGroup(*[Line(ax.c2p(a, 0), ax.c2p(a, hh), color=EIG, stroke_width=4) for a, hh in zip(x, h)])
        tops = VGroup(*[Dot(ax.c2p(a, hh), radius=0.05, color=EIG) for a, hh in zip(x, h)])
        avg = DashedLine(ax.c2p(150, 2 / 40), ax.c2p(190, 2 / 40), color=GREY_B, stroke_width=2)
        al = MathTex(r"p/n", font_size=24, color=GREY_B).next_to(ax.c2p(190, 2 / 40), RIGHT, buff=0.1)
        rows = VGroup(
            MathTex(r"\hat y_i = \sum_j H_{ij}\, y_j", r",\quad h_{ii} = H_{ii}", font_size=30),
            MathTex(r"0 \le h_{ii} \le 1", r",\quad \sum_i h_{ii} = \operatorname{tr} H = p", font_size=30),
            MathTex(r"h_{ii} = \frac1n + \frac{(x_i - \bar x)^2}{\sum_j (x_j - \bar x)^2}", font_size=30, color=EIG),
            label(r"far from the centre of the $x$'s, \ a point pulls the line toward itself", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.8, 1.4, 0])
        for r in rows:
            if r.width > 6.0:
                r.width = 6.0
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.8, 1.4, 0])  # re-align after clamping
        tag = simulated_tag(r"simulated: the hook's 40 families")
        with self.voiceover(
            "The diagonal of the hat matrix has a meaning of its own. <bookmark mark='a'/> The i-th fitted value "
            "puts weight h i i on its own observation: that's its leverage. <bookmark mark='b'/> Because H is a "
            "projection, every leverage lies between zero and one, and they add up to the trace, p, so they "
            "average p over n. <bookmark mark='c'/> For a straight line, the leverage is one over n plus the squared "
            "distance from the average x, as a share of the total. <bookmark mark='d'/> Families whose parents are "
            "unusually short or tall have the most leverage: they pull the fitted line toward themselves. Part 30 "
            "makes leverage and influence precise."
        ) as vo:
            self.play(FadeIn(A), Create(avg), FadeIn(al), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[Create(b) for b in bars], lag_ratio=0.02), FadeIn(tops))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Indicate(tops[e["i_max"]], color=RES, scale_factor=2.0))
        self.clear_scene()
