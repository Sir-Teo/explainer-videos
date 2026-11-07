from __future__ import annotations

import numpy as np

from videos.stats.stats49.common import *  # noqa: F403


class Tangent(VoiceoverScene):
    def construct(self):
        self.card()
        self.submodels()
        self.paths()
        self.picture()
        self.examples()
        self.independence()

    def card(self):
        card = chapter_card(1, r"Models and tangent spaces", r"The directions in which a model can move", part=PART)
        with self.voiceover("Chapter one. Models and tangent spaces: the directions in which a model can move."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def submodels(self):
        rows = [
            cmath(r"\mathcal P", r"=", r"\text{the model: \ a set of laws, \ possibly infinite dimensional}", font_size=32),
            cmath(r"\{P_t : t \in (-\varepsilon, \varepsilon)\} \subset \mathcal P, \ P_0 = P", r":", r"\text{a one-dimensional submodel through } P", font_size=30),
            cmath(r"s = \tfrac{\partial}{\partial t} \log p_t \big|_{t=0}", r":", r"\text{its score: } \ E_P\, s = 0, \ \ E_P\, s^2 < \infty", font_size=32),
            cmath(r"\dot{\mathcal P}_P", r"=", r"\overline{\text{span}}\{\text{scores of all smooth submodels}\} \subset L_2^0(P)", font_size=32),
        ]
        rows[3][-1].set_color(TANC)
        whys = [why(r"what we are willing to assume"), why(r"a path through the model"), why(r"a direction, \ as a function"), why(r"the tangent space")]
        heading = label('A tangent space collects the scores of regular smooth paths', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> A statistical model is a set of possible distributions, and in semiparametric problems it is infinite dimensional. <bookmark mark='b'/> To do calculus on it, look at one-dimensional paths through the true distribution P that stay inside the model, indexed by t, passing through P at t equal to zero. <bookmark mark='c'/> For differentiability-in-quadratic-mean paths, a square-integrable score describes the first-order change. Formally it is the derivative of its log-density at zero. A score is a function of the data with mean zero and finite variance, an element of L two zero of P. <bookmark mark='d'/> The tangent space is the closed linear span of all those scores: every direction in which the model can move away from P, written as functions."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def paths(self):
        rows = [
            cmath(r"p_t = p\,(1 + t\,s), \ s \text{ bounded}", r":", r"\text{score } s: \ \text{the linear path}", font_size=34),
            cmath(r"p_t = p\, e^{t s} / E_p\, e^{t s}", r":", r"\text{score } s - E\,s = s: \ \text{exponential tilting}", font_size=34),
            cmath(r"p_t = (1 - t)\, p + t\, q\quad(t\ge0)", r":", r"q\ll p,\ q/p-1\in L_2(P):\ \text{one-sided contamination}", font_size=34),
            cmath(r"\text{every mean-zero } s \in L_2(P)", r":", r"\text{a limit of such scores: \ the closure}", font_size=34),
        ]
        rows[1][-1].set_color(GRADC)
        rows[2][-1].set_color(GRADC)
        rows[3][-1].set_color(TANC)
        whys = [why(r"stays a density for small $t$"), why(r"Part 43's tilting, \ Part 47's saddlepoints"), why(r"contamination, \ as in Huber's model"), why(r"why the tangent space is closed")]
        heading = label('Smooth paths require valid densities and square-integrable scores', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Three standard ways to build paths. The linear path multiplies the density by one plus t times a bounded mean-zero function s; for small t it is still a density, and its score is s itself. <bookmark mark='b'/> Exponential tilting, from Parts forty-three and forty-seven, multiplies by e to the t s and renormalizes; when its moment-generating function exists around zero, its score is again s. <bookmark mark='c'/> For q absolutely continuous with respect to P, a one-sided contamination path has score q over p minus one when it is square integrable. A continuous model contaminated by a point mass is not such a dominated smooth path; the point-mass influence calculation is a separate formal device. <bookmark mark='d'/> Any mean-zero function with finite variance is a limit of bounded ones, so taking the closure makes the nonparametric tangent space all of L two zero."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        T = TangentSpace(origin=(-1.6, -1.0, 0.0), scale=1.7)
        box = T.plane(extent=2.4, color=GREY_D, opacity=0.06)
        pl = T.plane(extent=1.7, color=TANC, opacity=0.2)
        up = T.arrow((0, 0, 1.8), color=GREY_C, stroke_width=3)
        s1 = T.arrow((1.4, 0.3, 0), color=GRADC)
        s2 = T.arrow((-0.4, 1.3, 0), color=GRADC)
        s3 = T.arrow((0.9, -0.9, 0), color=GRADC)
        side = fit_rows(VGroup(
            label(r"grey sheet: \ $L_2^0(P)$, \ every mean-zero function", font_size=22, color=GREY_B),
            label(r"blue arrows: \ scores of submodels", font_size=22, color=GRADC),
            label(r"green: \ their span, \ the tangent space $\dot{\mathcal P}_P$", font_size=22, color=TANC),
            label(r"grey: \ a direction the model forbids", font_size=22, color=GREY_C),
            label(r"nonparametric model: \ the plane is all of $L_2^0$", font_size=22, color=EFFC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A picture helps, with the infinite-dimensional space of mean-zero functions drawn as three-dimensional space. <bookmark mark='b'/> Each smooth path through P contributes one score, an arrow. <bookmark mark='c'/> Their span is the tangent space, here a plane. <bookmark mark='d'/> Directions out of the plane are moves the model forbids: if we assume, say, symmetry or independence, the scores that would break it are excluded. <bookmark mark='e'/> If the model assumes nothing at all, the closure of bounded scores contains every mean-zero square-integrable function, and the tangent space is the whole space. The smaller the model, the smaller its tangent space, and, as we will see, the easier the estimation."
        ) as vo:
            self.play(FadeIn(box), FadeIn(exact_tag(r"a schematic: \ three of infinitely many dimensions")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowArrow(s1), GrowArrow(s2), GrowArrow(s3), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(pl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(GrowArrow(up), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def examples(self):
        rows = [
            cmath(r"\text{nonparametric}", r":", r"\dot{\mathcal P} = L_2^0(P): \ \ p_t = p\,(1 + t\, s), \ s \text{ bounded}", font_size=32),
            cmath(r"\text{parametric } \{p_\theta\}", r":", r"\dot{\mathcal P} = \text{span}\{\dot\ell_\theta\}: \ k \text{ dimensions}", font_size=32),
            cmath(r"\text{symmetric about } \theta", r":", r"\operatorname{span}\{\dot\ell_\theta\}+\{\text{mean-zero even }L_2(P)\text{ functions}\}", font_size=30),
            cmath(r"X_1 \perp X_2", r":", r"\{a(x_1) + b(x_2)\}: \ \text{no interactions}", font_size=32),
        ]
        rows[0][-1].set_color(TANC)
        rows[2][-1].set_color(EFFC)
        rows[3][-1].set_color(GRADC)
        whys = [why(r"every direction allowed"), why(r"Part 22's scores"), why(r"the hook's model"), why(r"chapter 2's example")]
        heading = label('Model restrictions remove directions from the tangent space', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Four examples. In the nonparametric model, any bounded mean-zero s gives a path p times one plus t s, so the tangent space is everything. <bookmark mark='b'/> In a parametric model the tangent space is spanned by the parameter scores; its dimension is k when the information is nonsingular. <bookmark mark='c'/> For the symmetric location model of the hook, moving theta gives the location score, and changing the shape while keeping it symmetric gives the mean-zero square-integrable even functions of x minus theta, under regular location assumptions. <bookmark mark='d'/> And if two variables are assumed independent, a change of either margin is allowed but a change in their joint structure is not: the tangent space is sums of a function of the first and a function of the second."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def independence(self):
        d = load("geometry")
        P = np.asarray(d["P"]).reshape(2, 2)
        cells = VGroup()
        for i in range(2):
            for j in range(2):
                sq = Square(side_length=1.3, stroke_color=GREY_B, stroke_width=2, fill_color=GRADC, fill_opacity=0.15 + 0.8 * P[i, j])
                sq.move_to([-4.2 + 1.35 * j, 1.0 - 1.35 * i, 0])
                cells.add(VGroup(sq, label(rf"{P[i, j]:.2f}", font_size=28).move_to(sq)))
        heads = VGroup(label(r"$X_2 = 1$", font_size=24).move_to([-4.2, 2.0, 0]), label(r"$X_2 = 2$", font_size=24).move_to([-2.85, 2.0, 0]),
                       label(r"$X_1 = 1$", font_size=24).move_to([-5.5, 1.0, 0]), label(r"$X_1 = 2$", font_size=24).move_to([-5.5, -0.35, 0]))
        side = fit_rows(VGroup(
            label(r"$P = (0.3, 0.7) \otimes (0.6, 0.4)$: \ 4 cells", font_size=24),
            label(r"$L_2^0(P)$: \ 3 dimensions \ (4 values, \ mean 0)", font_size=24, color=GREY_B),
            label(r"independence: \ $a(x_1) + b(x_2)$: \ 2 dimensions", font_size=24, color=TANC),
            label(r"the forbidden direction: \ the interaction", font_size=24, color=NUIC),
            label(r"estimand: \ $\psi = P(X_1 = 1, X_2 = 1) = 0.18$", font_size=24, color=EFFC),
        ), 6.0, 0.45, [2.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A concrete model we can compute everything in. Two binary variables, assumed independent, "
            "with margins point three and point six, so four cells. <bookmark mark='b'/> Functions on four cells with mean "
            "zero form a three-dimensional space. <bookmark mark='c'/> Under independence, the tangent space is the "
            "two-dimensional plane of row effects plus column effects. <bookmark mark='d'/> The missing direction is the "
            "interaction, a change that would make the variables dependent. <bookmark mark='e'/> We will estimate the "
            "probability of the top-left cell, point one eight, and ask how much knowing independence helps."
        ) as vo:
            self.play(FadeIn(cells), FadeIn(heads), FadeIn(exact_tag(r"exact")))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k], shift=RIGHT * 0.2))
        self.clear_scene()
