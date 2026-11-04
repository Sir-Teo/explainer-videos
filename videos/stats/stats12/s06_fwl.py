from __future__ import annotations

import numpy as np

from videos.stats.stats12.common import *  # noqa: F403


class FWL(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.demo()
        self.ovb()
        self.ovb_sim()
        self.simpson()
        self.lesson()

    def card(self):
        card = chapter_card(5, r"Controlling for", r"What a coefficient in a multiple regression means", part=PART)
        with self.voiceover("Chapter five. Controlling for."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorem(self):
        tc = theorem_card(r"Frisch--Waugh--Lovell", r"In $y = X_1\beta_1 + X_2\beta_2 + \varepsilon$, \ the least squares $\hat\beta_1$ equals the "
                          r"slope from regressing \ (the residuals of $y$ on $X_2$) \ on \ (the residuals of $X_1$ on $X_2$).",
                          who=r"R. Frisch \& F. Waugh (1933); \ M. Lovell (1963)", color=FIT, width=10.4, font_size=26).move_to([0, 1.4, 0])
        rows = fit_rows(VGroup(
            label(r"``controlling for $X_2$'' means: \ remove from both $y$ and $X_1$ whatever $X_2$ predicts, \ then compare what is left",
                  font_size=24, color=OBS),
            label(r"geometry: \ project everything onto the space perpendicular to $X_2$ (Part 4's Schur complement)", font_size=24,
                  color=GREY_A),
        ), 12.6, 0.34, [0, -1.7, 0])
        with self.voiceover(
            "What does a coefficient mean when there are several predictors? <bookmark mark='a'/> The Frisch–Waugh–Lovell "
            "theorem, from Ragnar Frisch and Frederick Waugh in 1933, the year Frisch founded econometrics, and Michael "
            "Lovell in 1963, answers exactly. The coefficient on x1 in a multiple regression equals the slope you get by "
            "first removing from y everything x2 can predict, removing from x1 everything x2 can predict, and regressing "
            "the first leftover on the second. <bookmark mark='b'/> That's what controlling for x2 means: compare y and x1 "
            "after taking out whatever x2 explains in each. <bookmark mark='c'/> In the geometry of chapter two, project "
            "everything onto the space perpendicular to x2, and fit there."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def demo(self):
        d = load("fwl")
        ra, ry = np.asarray(d["ra"]), np.asarray(d["ry"])
        A = axes([-3, 3], [-3, 3], x_length=5.6, y_length=5.0, xlabel=r"father's height, \ residual on mother's", ylabel=r"child, \ residual on mother's",
                 xticks=[-2, 0, 2], yticks=[-2, 0, 2], center=[-3.2, -0.3, 0])
        ax = A.ax
        pts = scatter(ax, np.clip(ra, -3, 3), np.clip(ry, -3, 3), radius=0.045, opacity=0.7)
        ln = fit_line(ax, 0, d["fwl"][0], -3, 3)
        rows = fit_rows(VGroup(
            label(r"200 of the World's families, \ standard units", font_size=22, color=GREY_A),
            MathTex(rf"\text{{child}} \sim \text{{father}} + \text{{mother}}:\ \ \hat\beta_{{\text{{father}}}} = {d['full'][1]:.4f}", font_size=28),
            MathTex(rf"\text{{residual on residual}}:\ \ {d['fwl'][0]:.4f}", font_size=28, color=FIT),
            MathTex(rf"\text{{child}} \sim \text{{father alone}}:\ \ {d['simple'][1]:.4f}", font_size=28, color=GREY_A),
            label(rf"parents' heights correlate {d['corr_ab']:.2f} (assortative mating), \ so the two answers differ", font_size=22, color=GREY_A),
        ), 5.8, 0.34, [3.6, -0.2, 0])
        tag = simulated_tag(r"the World: \ families", corner=DR)
        with self.voiceover(
            "Let's check it on the World. <bookmark mark='a'/> Two hundred families. Regress the child's height on both "
            "parents' heights: the father's coefficient is point four three five four. <bookmark mark='b'/> Now do it the long "
            "way. Remove from the father's height whatever the mother's predicts, and the same from the child's, and plot the "
            "two leftovers. <bookmark mark='c'/> The slope through this cloud is point four three five four again, to every "
            "digit. <bookmark mark='d'/> Regressing on the father alone gives point four eight three: larger, because tall "
            "fathers tend to have tall partners, and without controlling for the mother, the father's coefficient picks up "
            "part of her effect."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.005), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(ln), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def ovb(self):
        rows = [
            cmath(r"y", r"=", r"\beta_0 + \beta_1 x_1 + \gamma\,x_2 + \varepsilon", r"\quad\text{the truth}", font_size=32),
            cmath(r"x_2", r"=", r"\delta_0 + \delta\,x_1 + u", r"\quad\text{how the omitted variable tracks } x_1", font_size=32),
            cmath(r"E\,\hat\beta_1^{\text{short}}", r"=", r"\beta_1 + \gamma\,\delta", r"\quad\text{omitted-variable bias}", font_size=34),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"but $x_2$ is left out of the regression"), why(r"the auxiliary regression of $x_2$ on $x_1$"),
                why(r"bias = (effect of the omitted) $\times$ (its association with the included)")]
        with self.voiceover(
            "That's a special case of the most important formula in applied regression. <bookmark mark='a'/> Suppose the "
            "truth involves x1 and x2, but x2 is left out. <bookmark mark='b'/> Write how the omitted variable tracks the "
            "included one, with slope delta. <bookmark mark='c'/> Then the short regression's coefficient on x1 is biased by "
            "gamma times delta: the omitted variable's effect, times its association with the included one. Both must be "
            "non-zero for bias, and the sign of the bias is the product of their signs."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.6, buff=0.9, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ovb_sim(self):
        d = load("ovb")
        bars = VGroup()
        specs = [(r"true return to a year of school", d["true"], EXACT), (r"wage on schooling and ability", d["long"], FIT),
                 (r"wage on schooling alone", d["short"], RES), (r"formula: \ $0.08 + 0.10 \times 0.30$", d["formula"], GREY_A)]
        for i, (t, v, c) in enumerate(specs):
            y = 1.6 - 1.0 * i
            bars.add(VGroup(label(t, font_size=24, color=c).move_to([-3.6, y, 0]),
                            Rectangle(width=v * 40, height=0.45, stroke_width=0, fill_color=c, fill_opacity=0.8).move_to([0.2, y, 0], aligned_edge=LEFT),
                            MathTex(f"{v:.3f}", font_size=30, color=c).move_to([0.2 + v * 40 + 0.7, y, 0])))
        for b in bars:
            if b[0].width > 5.6:
                b[0].width = 5.6
            b[0].align_to([0.0, 0, 0], RIGHT)
        foot = label(r"ability raises wages ($\gamma = 0.10$) \ and schooling ($\delta = 0.30$): \ the short regression credits school with both",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.6)
        if foot.width > 12.6:
            foot.width = 12.6
        tag = simulated_tag(r"simulated: \ 4,000 samples of 500", corner=UR)
        with self.voiceover(
            "The economists' classic case. <bookmark mark='a'/> In a simulated population, each year of schooling raises the "
            "log wage by point zero eight. <bookmark mark='b'/> Regress wages on schooling and ability, and you recover point "
            "zero eight. <bookmark mark='c'/> But ability is rarely measured. Leave it out, and the coefficient on schooling "
            "becomes point one one: a thirty-eight percent overstatement. <bookmark mark='d'/> The formula predicts it "
            "exactly: ability's effect, point one, times its association with schooling, point three, added to the truth. "
            "Able people both earn more and stay in school longer, and the short regression credits school with both."
        ) as vo:
            self.play(FadeIn(tag))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(bars[k][0]), GrowFromEdge(bars[k][1], LEFT), FadeIn(bars[k][2]))
            self.play(FadeIn(foot))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"a regression coefficient answers a comparison, \ not an intervention", font_size=30, color=OBS),
            label(r"``among people with the same $X_2$, \ those with one more unit of $X_1$ have $\hat\beta_1$ more $y$, \ on average''",
                  font_size=24),
            label(r"it is causal only if nothing that affects $y$ and tracks $X_1$ has been left out", font_size=24),
            label(r"you can never be sure of that from the data alone: \ hence experiments (Part 13), \ and Parts 35--37", font_size=24,
                  color=GREY_A),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So a regression coefficient answers a question about comparison, not intervention. "
            "<bookmark mark='b'/> It says: among people with the same values of the other variables, those with one more "
            "unit of x1 have, on average, beta-one-hat more y. <bookmark mark='c'/> It's the effect of changing x1 only if "
            "nothing that affects y and tracks x1 has been left out. <bookmark mark='d'/> And no amount of data can prove "
            "that nothing has been left out. That's why the next part is about designing the data instead, and why Parts 35 "
            "to 37 exist."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def simpson(self):
        from explainer.stats.kit import ols as O
        from explainer.stats.world import World

        c = World().clinic
        t, s_, r = (c[k].astype(float) for k in ("treated", "severe", "recovered"))
        short = O.fit(O.design(t), r).coef
        long = O.fit(O.design(t, s_), r).coef
        delta = O.fit(O.design(t), s_).coef[1]
        rows = [
            cmath(r"\text{recovered} \sim \text{treated}", r":", rf"\hat\beta = {short[1]:+.3f}", r"\quad\text{treatment looks harmful}", font_size=32),
            cmath(r"\text{recovered} \sim \text{treated} + \text{severe}", r":", rf"\hat\beta = {long[1]:+.3f},\ \ \hat\gamma = {long[2]:+.3f}", font_size=32),
            cmath(r"\gamma\,\delta", r"=", rf"({long[2]:+.3f}) \times ({delta:+.3f}) = {long[2] * delta:+.3f}", font_size=32),
            cmath(r"\text{short}", r"=", rf"\text{{long}} + \gamma\delta:\ \ {long[1]:+.3f} {long[2] * delta:+.3f} = {short[1]:+.3f}", font_size=32),
        ]
        rows[1][2].set_color(FIT)
        rows[3][2].set_color(OBS)
        whys = [why(r"20,000 of the World's patients: \ a linear probability model"), why(r"control for severity: \ the sign flips (Part 5's Simpson)"),
                why(r"severity hurts, \ and the treated are sicker ($\delta$ = share severe, treated minus untreated)"),
                why(r"the omitted-variable formula holds exactly, \ in-sample")]
        with self.voiceover(
            "Part 5's Simpson's paradox is the same formula. <bookmark mark='a'/> Regress recovery on treatment, across all "
            "twenty thousand of the World's clinic patients: treatment seems to lower the chance of recovery by eleven points. "
            "<bookmark mark='b'/> Control for severity, and the treatment coefficient becomes positive: plus eight points, while "
            "severe illness lowers recovery by forty. <bookmark mark='c'/> The bias is gamma times delta: severity's effect "
            "times how much more often the treated are severe, about minus nineteen points. <bookmark mark='d'/> And the short "
            "coefficient is exactly the long one plus that bias. The paradox was omitted-variable bias all along."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.2, buff=0.65, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
