from __future__ import annotations

import numpy as np

from videos.stats.stats49.common import *  # noqa: F403


class Pathwise(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.projection()
        self.check()
        self.numbers()
        self.lesson()

    def card(self):
        card = chapter_card(2, r"Pathwise differentiability", r"The efficient influence function as a projection", part=PART)
        with self.voiceover("Chapter two. Pathwise differentiability: the efficient influence function as a projection."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"\tfrac{d}{dt}\, \psi(P_t)\big|_{t=0}", r"=", r"E_P[\phi(X)\, s(X)] \ \ \text{for every submodel with score } s", font_size=32),
            cmath(r"\phi", r":", r"\text{a gradient: \ any such function in } L_2^0(P)", font_size=32),
            cmath(r"\phi + h, \ h \perp \dot{\mathcal P}", r":", r"\text{also a gradient: \ many gradients, \ one per complement}", font_size=30),
            cmath(r"\phi^* = \Pi(\phi \mid \dot{\mathcal P})", r":", r"\text{the canonical gradient: \ the efficient influence function}", font_size=30),
        ]
        rows[1][-1].set_color(GRADC)
        rows[3][-1].set_color(EFFC)
        whys = [why(r"Koshevnik \& Levit (1976); \ Pfanzagl (1982)"), why(r"Riesz: \ a derivative as an inner product"),
                why(r"only $\langle \phi, s \rangle$ on scores matters"), why(r"the unique gradient in the tangent space")]
        heading = label('An orthogonal projection identifies the efficient part', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The quantity of interest psi is pathwise differentiable at P if, along every smooth path "
            "through P, its derivative is the inner product of a fixed function phi with the path's score. <bookmark "
            "mark='b'/> Such a phi is called a gradient, or an influence function: it is a derivative of psi written as a "
            "function of the data. <bookmark mark='c'/> But it is only pinned down by its inner products with scores. Add "
            "anything orthogonal to the tangent space and the derivatives do not change. A large tangent space leaves little "
            "freedom; a small one leaves a lot. <bookmark mark='d'/> Among all gradients there is exactly one inside the "
            "tangent space: the projection of any gradient onto it. That is the efficient influence function."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def projection(self):
        d = load("geometry")
        sc = 5.0
        v = np.asarray(d["c_phi"]) * sc
        T = TangentSpace(origin=(-2.6, -1.4, 0.0), scale=1.6)
        box = T.plane(extent=2.6, color=GREY_D, opacity=0.05)
        pl = T.plane(extent=2.0, color=TANC, opacity=0.2)
        a = T.arrow(v, color=GRADC)
        dr = T.drop(v, [[1, 0, 0], [0, 1, 0]], color=EFFC)
        side = fit_rows(VGroup(
            label(r"the 2 $\times$ 2 table under independence", font_size=22),
            label(r"blue: \ $\phi = \mathbf 1\{\text{cell } 11\} - 0.18$", font_size=22, color=GRADC),
            label(r"the cell frequency's influence function", font_size=22, color=GRADC),
            label(r"gold: \ its projection on the green plane: \ $\phi^*$", font_size=22, color=EFFC),
            label(r"dashed: \ the interaction part, \ discarded", font_size=22, color=GREY_B),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the two by two table, the space is exactly three-dimensional and we can draw it to scale. <bookmark mark='b'/> The natural estimator of the top-left cell's probability is the fraction of observations in it. Its influence function, the indicator of the cell minus point one eight, is a gradient, <bookmark mark='c'/> because differentiating the cell probability gives the inner product with that centred indicator. Consistency alone would not prove it is a gradient. <bookmark mark='d'/> Project it onto the tangent plane of the independence model: the gold arrow, the efficient influence function. <bookmark mark='e'/> The dashed segment is its interaction component, the part that independence makes irrelevant, and discarding it can only reduce the variance."
        ) as vo:
            self.play(FadeIn(box), FadeIn(pl), FadeIn(exact_tag(r"exact: \ coordinates in an orthonormal basis of $L_2^0(P)$")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowArrow(a), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(dr[0]), GrowArrow(dr[1]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), Indicate(dr[0]))
        self.clear_scene()

    def check(self):
        d = load("geometry")
        names = {"row": r"change the row margin", "column": r"change the column margin", "both": r"change both"}
        rows = [[r"path inside independence", r"$\tfrac{d}{dt}\psi(P_t)$", r"$\langle \phi, s\rangle$", r"$\langle \phi^*, s\rangle$"]]
        for r in d["paths"]:
            rows.append([names[r["name"]], f"{r['deriv']:+.4f}", f"{r['ip_phi']:+.4f}", f"{r['ip_eff']:+.4f}"])
        tab = table_rows(rows, font_size=30, col_buff=0.9, row_buff=0.4, colors=[GREY_B, None, None, None])
        tab.move_to([0, 0.8, 0])
        for i in range(1, 4):
            tab[i][2].set_color(GRADC)
            tab[i][3].set_color(EFFC)
        foot = label(r"numerical derivatives along three submodels: \ both $\phi$ and $\phi^*$ are gradients", font_size=24, color=GREY_A).move_to([0, -1.4, 0])
        foot2 = label(r"they differ only off the plane, \ where no path of the model goes", font_size=24, color=TANC).move_to([0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A numerical check of the definition. Move the law along three paths that keep the "
            "variables independent: change the row margin, change the column margin, or both. Along each, the derivative of "
            "psi, computed numerically, equals the inner product of the score with the cell's influence function, and also "
            "with its projection. <bookmark mark='b'/> Both are gradients, because they agree on every direction the model "
            "can move in. They differ only in the interaction direction, where no path of the model goes."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(exact_tag(r"exact: \ numerical derivatives")))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def numbers(self):
        d = load("geometry")
        rows = [
            cmath(r"\|\phi\|^2 = 0.18 \times 0.82", r"=", rf"{d['bound_np']:.4f}: \ \text{{the cell frequency, \ any model}}", font_size=32),
            cmath(r"\|\phi^*\|^2 = q_1^2\, p_1(1-p_1) + p_1^2\, q_1(1-q_1)", r"=", rf"{d['bound']:.4f}: \ \text{{under independence}}", font_size=30),
            cmath(r"\hat\psi = \hat p_1\, \hat q_1", r":", r"\text{the product of the margins: \ its influence function is } \phi^*", font_size=30),
            cmath(rf"n = {d['n']}, \ {d['reps']:,} \text{{ samples}}", r":", rf"n\,\mathrm{{Var}} = {d['sim_cell']:.4f} \ \text{{and}} \ {d['sim_prod']:.4f}", font_size=32),
        ]
        rows[1][-1].set_color(EFFC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"the nonparametric bound"), why(r"the efficient bound"), why(r"an efficient estimator"), why(r"simulated")]
        heading = label('The efficient influence function reduces the asymptotic variance', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            f"<bookmark mark='a'/> In numbers. The cell frequency's influence function has squared length point one eight times point eight two, {say(d['bound_np'], 4)}: that is the best possible variance when nothing is assumed. <bookmark mark='b'/> Its projection has squared length {say(d['bound'], 4)}: the bound under independence, a third smaller. <bookmark mark='c'/> And an estimator attains it: the product of the two marginal frequencies, whose influence function, by the delta method, is exactly the projection. <bookmark mark='d'/> Simulated with four hundred observations, the two estimators have n times variance {say(d['sim_cell'], 4)} and {say(d['sim_prod'], 4)}. The efficient variance is about one third smaller, equivalent to needing about one third fewer observations for the same asymptotic precision."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"the recipe, \ in any model:", font_size=28, color=GREY_A),
            label(r"1. \ find one gradient \ (often: the nonparametric influence function of a natural estimator)", font_size=26, color=GRADC),
            label(r"2. \ project it on the model's tangent space", font_size=26, color=TANC),
            label(r"3. \ the projection is $\phi^*$; \ its variance is the bound \ (chapter 3)", font_size=26, color=EFFC),
            label(r"nonparametric model: \ nothing to project: \ every regular estimator has the same $\phi$", font_size=26, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So the recipe, in any model, is three steps. <bookmark mark='b'/> Find one gradient; often "
            "the influence function of a natural estimator that is consistent without the model's restrictions. <bookmark "
            "mark='c'/> Project it onto the model's tangent space. <bookmark mark='d'/> The projection is the efficient "
            "influence function, and its variance is the bound, as chapter three proves. <bookmark mark='e'/> In the "
            "nonparametric model the tangent space is everything and there is nothing to project: all regular, asymptotically "
            "linear estimators of a quantity share one influence function, and so one asymptotic variance."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
