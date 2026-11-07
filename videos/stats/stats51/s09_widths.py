from __future__ import annotations

import math

import numpy as np

from videos.stats.stats51.common import *  # noqa: F403


class Widths(VoiceoverScene):
    def construct(self):
        self.card()
        self.width()
        self.table()
        self.recovery()
        self.picture()
        self.mesh()

    def card(self):
        card = chapter_card(8, r"Gaussian widths and the escape through the mesh", r"When does a random subspace miss a set?", lit=(1985,), part=PART)
        with self.voiceover("Chapter eight. Gaussian widths and the escape through the mesh: when does a random subspace miss a set?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def width(self):
        rows = [
            cmath(r"w(T)", r"=", r"E\sup_{t \in T} \langle g, t\rangle, \ \ g \sim N(0, I_p)", font_size=36),
            cmath(r"\text{geometrically}", r":", r"\text{the average half-width of } T \text{ in a random direction, } \times E\chi_p\sim\sqrt p", font_size=30),
            cmath(r"w(B_2^p) \approx \sqrt p", r",", r"\ w(B_1^p) \approx \sqrt{2\log 2p}", font_size=36),
            cmath(r"\text{the effective dimension}", r":", r"w(T \cap S^{p-1})^2: \ \text{how many dimensions } T \text{ really uses}", font_size=30),
        ]
        rows[2][-1].set_color(SPHC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"a Gaussian supremum"), why(r"the mean width"), why(r"the cross-polytope is thin"), why(r"a cone's 'dimension'")]
        heading = label('Gaussian width measures an average support function', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The Gaussian width of a set T is the expected supremum of the Gaussian process indexed by T: the largest inner product of a random Gaussian direction with a point of T. Everything in the last two chapters applies to it. <bookmark mark='b'/> Geometrically, it is the average half-width of T measured along a random direction, scaled by the mean length of a standard Gaussian vector, asymptotic to root p. <bookmark mark='c'/> The Euclidean ball has width about root p. The l-one ball, the cross-polytope, has width only about the root of two log two p, because a random direction is nearly orthogonal to all of its corners at once. <bookmark mark='d'/> For a cone, the squared width of its intersection with the sphere acts as its effective dimension: how many dimensions the cone really occupies."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("widths")
        rows = [[r"dimension $p$"] + [f"{p:,}" for p in d["ps"]],
                [r"$w(B_2^p) = E\|g\|$"] + [f"{v:.1f}" for v in d["l2"]],
                [r"$w(B_1^p) = E\max_i |g_i|$"] + [f"{v:.2f}" for v in d["l1"]],
                [r"$\sqrt{2\log 2p}$"] + [f"{v:.2f}" for v in d["sqrt2log"]]]
        tab = table_rows(rows, font_size=26, col_buff=0.5, row_buff=0.4, colors=[GREY_B, GAUSSC, SPHC, EXACTC])
        if tab.width > 12.8:
            tab.width = 12.8
        tab.move_to([0, 0.9, 0])
        foot = label(r"the ball's width grows like $\sqrt p$; \ the cross-polytope's like $\sqrt{\log p}$", font_size=24, color=GREY_A).move_to([0, -1.2, 0])
        foot2 = label(r"in 10,000 dimensions the $\ell_1$ ball is 25 times thinner than the $\ell_2$ ball, \ on average", font_size=24, color=SPHC).move_to([0, -2.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Exact widths, by quadrature. The Euclidean ball's grows like root p: "
            f"{say(d['l2'][0], 1)} in ten dimensions, a hundred in ten thousand. The cross-polytope's grows only like the root "
            f"of log p: {say(d['l1'][-1], 1)} in ten thousand dimensions, a little under the root of two log two p. "
            f"<bookmark mark='b'/> That is the geometric fact under all of sparse recovery. <bookmark mark='c'/> In ten "
            f"thousand dimensions, the l-one ball is, on average over directions, about twenty-five times thinner than the "
            f"Euclidean ball it sits inside, though both reach the same distance along the coordinate axes."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(exact_tag(r"exact, \ by quadrature")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def recovery(self):
        rows = [
            cmath(r"y = Ax_0, \ \ A \in \mathbb R^{m \times p}", r":", r"m < p \text{ Gaussian measurements of an } s\text{-sparse } x_0", font_size=30),
            cmath(r"\hat x", r"=", r"\arg\min \{\|x\|_1 : Ax = y\}: \ \text{basis pursuit (Part 32)}", font_size=32),
            cmath(r"\hat x = x_0", r"\iff", r"\ker A \cap D(x_0) = \{0\}", font_size=36),
            cmath(r"D(x_0)", r"=", r"\{h: \|x_0 + \varepsilon h\|_1 \le \|x_0\|_1 \text{ for some } \varepsilon > 0\}", font_size=30),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(SPHC)
        whys = [why(r"fewer equations than unknowns"), why(r"a linear program"), why(r"the null space misses a cone"), why(r"the descent cone")]
        heading = label('Unique basis pursuit requires the null space to miss the descent cone', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The question the widths answer. We take m Gaussian measurements of a p-dimensional vector "
            "with only s non-zero entries, with fewer measurements than unknowns. <bookmark mark='b'/> Basis pursuit, from Part "
            "thirty-two, returns the solution of the equations with the smallest l-one norm. <bookmark mark='c'/> It recovers "
            "the truth exactly if and only if the null space of A meets the descent cone only at zero. <bookmark mark='d'/> The "
            "descent cone is the set of directions in which the l-one norm does not increase from the truth. If some null-space "
            "direction lay in it, moving along it would keep the equations satisfied and not increase the norm, and the truth "
            "would not be the unique minimizer."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        sh = SphereShell(center=(-3.0, -0.2, 0.0), radius=2.4)
        c = sh.c
        circ = sh.circle()
        # the descent cone at x0 = (1, 0) for the l1 diamond: directions h with h_1 <= -|h_2|
        ang = math.radians(45)
        cone_pts = [c] + [c + sh.r * np.array([math.cos(u), math.sin(u), 0.0]) for u in np.linspace(math.pi - ang, math.pi + ang, 40)] + [c]
        cone = VMobject(fill_color=SPHC, fill_opacity=0.35, stroke_color=SPHC, stroke_width=2)
        cone.set_points_as_corners(cone_pts)
        cap_pts = [c + sh.r * np.array([math.cos(u), math.sin(u), 0.0]) for u in np.linspace(math.pi - ang, math.pi + ang, 40)]
        cap = VMobject(stroke_color=SPHC, stroke_width=7)
        cap.set_points_as_corners(cap_pts)

        def line(theta, color):
            v = np.array([math.cos(theta), math.sin(theta), 0.0]) * sh.r * 1.12
            return Line(c - v, c + v, color=color, stroke_width=4)

        miss = line(math.radians(70), GOODC)
        hit = line(math.radians(160), BADC)
        side = fit_rows(VGroup(
            label(r"gold: \ the descent cone, \ cut by the sphere", font_size=22, color=SPHC),
            label(r"a random null space: \ a random subspace", font_size=22),
            label(r"green: \ it misses the cone: \ exact recovery", font_size=22, color=GOODC),
            label(r"red: \ it hits the cone: \ failure", font_size=22, color=BADC),
            label(r"in $\mathbb R^p$: \ dimension $p - m$, \ and the cap is tiny", font_size=22, color=GREY_A),
        ), 4.8, 0.45, [3.6, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The picture, drawn in the plane with the SphereShell. The gold region is the descent cone, "
            "and its intersection with the sphere is a cap. <bookmark mark='b'/> The null space of a Gaussian matrix is a "
            "uniformly random subspace. <bookmark mark='c'/> If it passes the cone by, basis pursuit recovers the vector "
            "exactly. <bookmark mark='d'/> If it cuts through, recovery fails. <bookmark mark='e'/> In two dimensions a random "
            "line hits a quarter-circle cone half the time. In high dimensions the cap is an exponentially small part of the "
            "sphere, chapter two's geometry again, and the question becomes how large the subspace can be and still miss it."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(circ), FadeIn(cone), Create(cap), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(miss), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(hit), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def mesh(self):
        rows = [
            cmath(r"T \subset S^{p-1}\text{ compact}, \ \ E \text{ uniform, codim } m", r":", r"\text{Gordon's escape through the mesh (1988)}", font_size=30),
            cmath(r"w(T)<a_m:=E\chi_m", r"\Rightarrow", r"P(E \cap T = \emptyset) \ge 1-e^{-(a_m-w(T))^2/2}", font_size=32),
            cmath(r"T = D(x_0) \cap S^{p-1}", r":", r"w^2 \lesssim 2s\log(p/s) \ \Rightarrow \ m \gtrsim 2s\log(p/s) \text{ suffice}", font_size=30),
            cmath(r"\text{closed convex cones only}", r":", r"m \ll w^2 \Rightarrow \text{failure away from the transition window}", font_size=32),
        ]
        rows[1][-1].set_color(GOODC)
        rows[2][-1].set_color(SPHC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"from his min--max comparison"), why(r"an explicit probability"), why(r"Chandrasekaran et al. (2012)"), why(r"a sharp threshold, \ chapter 9")]
        heading = label('A positive Gaussian-width gap controls the escape probability', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Yehoram Gordon answered it in 1988 with his min-max comparison: the escape through the mesh. <bookmark mark='b'/> For a compact subset T of the sphere, a uniformly random subspace of codimension m misses T with high probability when its width lies sufficiently below the mean length of an m-dimensional Gaussian vector. The gap sets the probability bound. <bookmark mark='c'/> For the descent cone of the l-one norm at an s-sparse vector, the squared width is at most about two s log of p over s, so that many measurements suffice, as Venkat Chandrasekaran, Benjamin Recht, Pablo Parrilo and Alan Willsky showed in 2012. <bookmark mark='d'/> For closed convex descent cones, the next chapter supplies a converse with a finite-dimensional transition window. There is no such converse for every arbitrary subset of the sphere."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
