from __future__ import annotations

import numpy as np

from videos.stats.stats49.common import *  # noqa: F403


class Bounds(VoiceoverScene):
    def construct(self):
        self.card()
        self.convolution()
        self.leastfav()
        self.lam()
        self.chart()
        self.models()
        self.ate()

    def card(self):
        card = chapter_card(3, r"Efficiency bounds", r"The hardest one-dimensional submodel", part=PART)
        with self.voiceover("Chapter three. Efficiency bounds: the hardest one-dimensional submodel."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def convolution(self):
        rows = [
            cmath(r"T_n \text{ regular in } \mathcal P", r":", r"\sqrt n(T_n - \psi(P_{t/\sqrt n})) \rightsquigarrow L \ \text{along every submodel}", font_size=30),
            cmath(r"\Rightarrow", r"\;", r"L = N(0, E\,\phi^{*2}) * M: \ \text{the convolution theorem}", font_size=34),
            cmath(r"T_n \text{ asymptotically linear}", r":", r"\sqrt n(T_n - \psi) = \tfrac{1}{\sqrt n}\textstyle\sum \phi(X_i) + o_P(1), \ \phi \text{ a gradient}", font_size=30),
            cmath(r"\mathrm{Var}\,\phi", r"=", r"\|\phi^*\|^2 + \|\phi - \phi^*\|^2 \ \ge \ \|\phi^*\|^2", font_size=34),
        ]
        rows[1][-1].set_color(EFFC)
        rows[3][-1].set_color(TANC)
        whys = [why(r"no superefficiency, \ Part 47"), why(r"Hájek, \ for semiparametric models"), why(r"regular asymptotically linear estimators"), why(r"Pythagoras")]
        heading = label('Regular local limits contain the efficient Gaussian noise', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Part forty-seven's convolution theorem carries over. Call an estimator regular if its limit law is the same along every submodel's local alternatives. <bookmark mark='b'/> Under regular differentiable submodels and a square-integrable canonical gradient, the limit law is a normal with variance the squared length of the efficient influence function, convolved with something else. This lower-bounds the covariance of the limiting law when that covariance exists. Passing to finite-sample asymptotic risks requires additional moment control. <bookmark mark='c'/> For regular asymptotically linear estimators, the picture is even simpler: the estimator's influence function is some gradient. <bookmark mark='d'/> And by Pythagoras its variance is the efficient one plus the squared distance from the gradient to its projection. Efficiency means that distance is zero."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def leastfav(self):
        rows = [
            cmath(r"\text{a submodel with score } s", r":", r"\text{a parametric problem: \ Cram\'er--Rao bound } \frac{\langle \phi^*, s\rangle^2}{\langle s, s\rangle}", font_size=30),
            cmath(r"\sup_{s \in \dot{\mathcal P}} \frac{\langle \phi^*, s\rangle^2}{\langle s, s\rangle}", r"=", r"\|\phi^*\|^2, \ \text{supremum in the closure at }s\propto\phi^*", font_size=32),
            cmath(r"\text{the semiparametric bound}", r"=", r"\text{the bound of the hardest submodel}", font_size=32),
            cmath(r"s^* \propto \phi^*", r":", r"\text{the least favourable submodel}", font_size=34),
        ]
        rows[1][-1].set_color(EFFC)
        rows[3][-1].set_color(NUIC)
        whys = [why(r"one parameter $t$: \ Part 45"), why(r"Cauchy--Schwarz"), why(r"Stein (1956)'s idea"), why(r"TMLE walks along it, \ chapter 6")]
        heading = label('The hardest smooth submodels approach the canonical gradient', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> There is a second way to see the bound, and it is Stein's original idea. Any one-dimensional submodel is a parametric problem, and psi along it has a Cramér–Rao bound: the squared inner product of the efficient influence function with the score, over the score's squared length. <bookmark mark='b'/> By Cauchy–Schwarz, the largest of these over all submodels is the squared length of the efficient influence function, attained in the closed tangent space when the score points along it. A single actual submodel need not attain that direction; a sequence of smooth submodels can approach the supremum. <bookmark mark='c'/> So the semiparametric problem is exactly as hard as its hardest one-dimensional sub-problem. <bookmark mark='d'/> When such a path exists it is called a least favourable submodel, and chapter six's targeted estimator moves along it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lam(self):
        rows = [
            cmath(r"\text{any estimator } T_n", r":", r"\lim_{c \to \infty} \liminf_n \sup_{|h|\le c}nE_{P_{h/\sqrt n}}(T_n-\psi(P_{h/\sqrt n}))^2 \ \ge \ \|\phi^*\|^2", font_size=30),
            cmath(r"\text{regular or not}", r":", r"\text{Part 47's LAM theorem, \ in the hardest submodel}", font_size=32),
            cmath(r"\text{Hodges-type tricks}", r":", r"\text{superefficient at a point, \ never uniformly}", font_size=32),
            cmath(r"\text{so}", r":", r"\|\phi^*\|^2 \ \text{is the honest benchmark for every method}", font_size=34),
        ]
        rows[0][-1].set_color(EFFC)
        rows[3][-1].set_color(TANC)
        whys = [why(r"local asymptotic minimax"), why(r"one-dimensional reduction"), why(r"Part 47's chapter 9"), why(r"no estimator escapes it")]
        heading = label('Take the local large-sample limit before expanding the shift range', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The bound holds for every estimator, not just regular ones, in the local minimax sense of Part forty-seven: first take the large-sample limit over local shifts bounded by c, then let c tend to infinity; the resulting worst scaled risk is at least the efficient variance under the LAN and loss conditions. <bookmark mark='b'/> The proof applies Part forty-seven's theorem to the least favourable submodel, which is an ordinary one-dimensional parametric model. <bookmark mark='c'/> Hodges-type estimators can beat the bound at a point but cannot improve the limiting worst risk as these local shift ranges expand. <bookmark mark='d'/> So the efficient variance is an honest benchmark: any method, however modern, can be judged against it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("bounds")
        ang = np.degrees(np.asarray(d["ang"]))
        A = axes([0, 180], [0, 0.11], x_length=7.4, y_length=4.4, xlabel=r"direction of the submodel's score in the tangent plane (degrees)",
                 ylabel=r"Cram\'er--Rao bound along it", xticks=[0, 45, 90, 135, 180], yticks=[0, 0.05, 0.0972], center=[-2.5, 0.2, 0])
        ax = A.ax
        c = polyline(ax, ang, d["bound"], GRADC, 4)
        top = DashedLine(ax.c2p(0, d["max"]), ax.c2p(180, d["max"]), color=EFFC, stroke_width=2.5)
        b = np.degrees(d["best"])
        dot = Dot(ax.c2p(b, d["max"]), radius=0.1, color=NUIC)
        side = fit_rows(VGroup(
            label(r"the 2 $\times$ 2 table: \ every 1-D submodel of independence", font_size=22),
            label(r"blue: \ its bound for $\psi = P(\text{cell } 11)$", font_size=22, color=GRADC),
            label(rf"gold: \ the semiparametric bound {d['max']:.4f}", font_size=22, color=EFFC),
            label(rf"red: \ the least favourable direction, \ {b:.0f}$^\circ$", font_size=22, color=NUIC),
            label(r"other directions: \ easier problems", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Back to the two by two table. Each direction in its tangent plane is a one-dimensional "
            f"submodel. <bookmark mark='b'/> In blue, the parametric bound for the top-left cell along each direction. "
            f"<bookmark mark='c'/> The highest is the semiparametric bound, {say(d['max'], 4)}, <bookmark mark='d'/> reached "
            f"in exactly one direction, along the efficient influence function. <bookmark mark='e'/> Along any other path, "
            f"knowing the path would make the problem easier. Not knowing which path nature took is what costs us; the bound "
            f"is the cost of the worst case."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(top), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(dot), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def models(self):
        d = load("geometry")
        rows = [[r"model for the 2 $\times$ 2 table", r"tangent space", r"bound for $P(\text{cell } 11)$", r"efficient estimator"],
                [r"nonparametric", r"3 dimensions", f"{d['bound_np']:.4f}", r"the cell frequency"],
                [r"independence", r"2 dimensions", f"{d['bound']:.4f}", r"$\hat p_1 \hat q_1$"],
                [r"independence, \ $q_1 = 0.6$ known", r"1 dimension", f"{d['bound_known']:.4f}", r"$0.6\, \hat p_1$"]]
        tab = table_rows(rows, font_size=28, col_buff=0.7, row_buff=0.4, colors=[GREY_B, None, TANC, EFFC])
        if tab.width > 12.6:
            tab.width = 12.6
        tab.move_to([0, 0.8, 0])
        foot = label(r"smaller model $\Rightarrow$ smaller tangent space $\Rightarrow$ shorter projection $\Rightarrow$ smaller bound", font_size=24, color=GREY_A).move_to([0, -1.4, 0])
        foot2 = label(r"assumptions buy precision, \ at the price of being wrong when they fail", font_size=24, color=NUIC).move_to([0, -2.2, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The same estimand in three nested models. Assuming nothing, the bound is {say(d['bound_np'], 4)}, and the cell frequency attains it. Assuming independence, the tangent space loses a dimension and the bound falls to {say(d['bound'], 4)}. Knowing one margin as well leaves a single free direction, and the bound falls again, to {say(d['bound_known'], 4)}. <bookmark mark='b'/> Each assumption shrinks the tangent space, shortens the projection, and lowers the bound. But the efficient estimator of a smaller model can become biased when its assumption fails, which is the trade-off semiparametric models are designed to manage: assume only what you are willing to defend."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(exact_tag(r"exact")))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def ate(self):
        d = load("ate")
        rows = [[r"estimator", r"$n \times$ variance", r"how"],
                [r"efficiency bound $E\,\phi^{*2}$", f"{d['bound']:.2f}", r"quadrature"],
                [r"one-step, \ true nuisances", f"{d['sim_os']:.2f}", r"simulated"],
                [r"Hajek IPW, \ true propensity", f"{d['sim_hajek']:.2f}", r"simulated"],
                [r"Horvitz--Thompson IPW", f"{d['sim_ht']:.2f}", rf"simulated \ (theory {d['ht']:.2f})"]]
        tab = table_rows(rows, font_size=30, col_buff=0.9, row_buff=0.36, colors=[GREY_B, EFFC, OSC, None, NUIC])
        tab.move_to([0, 0.8, 0])
        foot = label(rf"the ATE in a smooth world: \ $e(x) = 0.2 + 0.6x_1$, \ $n = {d['n']}$, \ {d['reps']:,} samples", font_size=24, color=GREY_A).move_to([0, -1.6, 0])
        foot2 = label(r"weighting alone ignores the outcome's predictability: \ the bound uses it", font_size=24, color=EFFC).move_to([0, -2.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A preview of chapter four's main example, the average treatment effect, in a smooth simulated world with a known propensity. The efficiency bound, computed by quadrature, is {say(d['bound'], 2)} per observation. The one-step estimator with the true nuisance functions is close in this finite simulation, at {say(d['sim_os'], 2)}. Inverse probability weighting with the true propensity is much worse: {say(d['sim_hajek'], 2)} normalized, and {say(d['sim_ht'], 1)} unnormalized. <bookmark mark='b'/> Weighting alone ignores how predictable the outcome is from the covariates; the efficient influence function uses it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(simulated_tag(r"simulated; \ bound by quadrature")))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()
