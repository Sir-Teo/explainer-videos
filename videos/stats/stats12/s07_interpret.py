from __future__ import annotations

import numpy as np

from videos.stats.stats12.common import *  # noqa: F403


class Interpret(VoiceoverScene):
    def construct(self):
        self.card()
        self.dummies()
        self.regions()
        self.interaction()
        self.standardized()
        self.logs()
        self.curves()
        self.extrapolation()

    def card(self):
        card = chapter_card(6, r"Interpreting coefficients", r"Units, \ dummies, \ interactions, \ curves", part=PART)
        with self.voiceover("Chapter six. Interpreting coefficients."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def dummies(self):
        d = load("dummies")
        mid, son, y = np.asarray(d["mid"]), np.asarray(d["son"]), np.asarray(d["y"])
        A = axes([155, 185], [145, 200], x_length=6.4, y_length=5.0, xlabel=r"mid-parent height (cm)", ylabel=r"child's height (cm)",
                 xticks=[160, 170, 180], yticks=[150, 170, 190], center=[-3.0, -0.3, 0])
        ax = A.ax
        keep = (mid > 155) & (mid < 185) & (y > 145) & (y < 200)
        ds = VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=S.CTRL if s_ else S.TREAT, fill_opacity=0.7) for a, b, s_ in zip(mid[keep], y[keep], son[keep])])
        m1, m2 = d["m1"], d["m2"]
        l1 = fit_line(ax, m1[0], m1[1], 155, 185, GREY_A)
        ld = fit_line(ax, m2[0], m2[1], 155, 185, S.TREAT)
        ls = fit_line(ax, m2[0] + m2[2], m2[1], 155, 185, S.CTRL)
        rows = fit_rows(VGroup(
            MathTex(rf"\text{{one line: }} R^2 = {d['r2'][0]:.2f}", font_size=26, color=GREY_A),
            MathTex(r"y = \beta_0 + \beta_1\,\text{mid} + \beta_2\,\mathbf 1\{\text{son}\}", font_size=26),
            MathTex(rf"\hat\beta_2 = {m2[2]:.1f}\ \text{{cm}},\quad R^2 = {d['r2'][1]:.2f}", font_size=28, color=S.CTRL),
            label(r"a dummy shifts the intercept: \ two parallel lines", font_size=24, color=OBS),
            label(r"sons are 12.8 cm taller, \ at the same parents' height", font_size=22, color=GREY_A),
        ), 5.0, 0.32, [4.0, -0.2, 0])
        tag = simulated_tag(r"the World: \ 400 families", corner=DR)
        with self.voiceover(
            "Coefficients carry units, and their meaning depends on what's in the model. <bookmark mark='a'/> Four hundred of "
            "the World's families, now in centimetres: sons in blue, daughters in red. <bookmark mark='b'/> One line through "
            "everyone explains only ten percent of the variation, because it ignores the biggest fact about height. "
            "<bookmark mark='c'/> Add a dummy variable, one for a son and zero for a daughter. <bookmark mark='d'/> Its "
            "coefficient, twelve point eight centimetres, is the difference between sons and daughters with the same "
            "parents' height, and R squared jumps to sixty percent. <bookmark mark='e'/> Geometrically, a dummy gives each "
            "group its own intercept: two parallel lines."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in ds], lag_ratio=0.003), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(l1), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeOut(l1), Create(ld), Create(ls), FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def interaction(self):
        d = load("dummies")
        m3, se = d["m3"], d["se3"]
        rows = [
            cmath(r"y", r"=", r"\beta_0 + \beta_1\,\text{mid} + \beta_2\,\text{son} + \beta_3\,(\text{mid} \times \text{son})", font_size=30),
            cmath(r"\text{daughters' slope}", r"=", rf"\beta_1 = {m3[1]:.3f}", font_size=32),
            cmath(r"\text{sons' slope}", r"=", rf"\beta_1 + \beta_3 = {m3[1] + m3[3]:.3f}", font_size=32),
            cmath(r"\hat\beta_3", r"=", rf"{m3[3]:.3f} \pm {se[3]:.3f}\ \text{{(1 SE)}},\quad p = {d['p_int']:.2f}", font_size=32),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"an interaction: \ the slope may differ by group"), why(r"the slope for the reference group"),
                why(r"the interaction adds to it"), why(r"no evidence the slopes differ; \ and $\hat\beta_2$ now means ``at mid $= 0$''")]
        with self.voiceover(
            "<bookmark mark='a'/> To let the slopes differ too, add an interaction: the product of the dummy and mid-parent "
            "height. <bookmark mark='b'/> Then the daughters' slope is beta-one, <bookmark mark='c'/> and the sons' slope is "
            "beta-one plus beta-three. <bookmark mark='d'/> Here the interaction is small and its p-value is point four six: no "
            "evidence that sons and daughters regress differently, which is how the World was built. Beware one trap: with an "
            "interaction in the model, the son coefficient means the difference at a mid-parent height of zero centimetres, a "
            "meaningless extrapolation. Centring the predictor fixes that."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def logs(self):
        rows = [
            cmath(r"\log y", r"=", r"\beta_0 + \beta_1 x", r"\quad e^{\beta_1} - 1 \approx \beta_1 \text{ per unit of } x", font_size=32),
            cmath(r"y", r"=", r"\beta_0 + \beta_1\log x", r"\quad \beta_1/100 \text{ per 1\% of } x", font_size=32),
            cmath(r"\log y", r"=", r"\beta_0 + \beta_1\log x", r"\quad \beta_1 = \text{an elasticity: \% per \%}", font_size=32),
        ]
        whys = [why(r"multiplicative effects: \ a 0.05 slope is about $+5\%$"), why(r"diminishing returns"),
                why(r"the economists' favourite: \ scale-free")]
        intro = label('Logarithms change the scale of the association', font_size=36)
        with self.voiceover(
            "Logarithms change the meaning of a coefficient, usefully. <bookmark mark='a'/> With log y on the left, a slope of "
            "point zero five means each unit of x is associated with about five percent higher conditional geometric mean y: effects become proportional, which is "
            "how incomes and prices behave. <bookmark mark='b'/> With log x on the right, each one percent increase in x adds approximately "
            "beta over a hundred to y: diminishing returns. <bookmark mark='c'/> With logs on both sides, the slope is an "
            "elasticity: the percentage change in y per percentage change in x, a number with no units at all."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.2, x=-1.2, buff=1.0, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def curves(self):
        d = load("poly")
        age, y, grid = np.asarray(d["age"]), np.asarray(d["y"]), np.asarray(d["grid"])
        A = axes([18, 100], [7.5, 12], x_length=7.4, y_length=4.6, xlabel=r"age", ylabel=r"log income", xticks=[20, 40, 60, 80, 100],
                 yticks=[8, 9, 10, 11, 12], center=[-2.0, -0.3, 0])
        ax = A.ax
        keep = (y > 7.5) & (y < 12)
        pts = scatter(ax, age[keep], y[keep], radius=0.035, opacity=0.5)
        lin = clip_curve(ax, grid, d["lin"], GREY_A, 3)
        quad = clip_curve(ax, grid, d["quad"], S.POST, 3)
        spl = clip_curve(ax, grid, d["spline"], FIT, 3.5)
        truth = DashedVMobject(polyline(ax, d["true_age"], d["true_mean"], EXACT, 2.5), num_dashes=40)
        leg = legend([(GREY_A, rf"linear: \ $R^2 = {d['r2'][0]:.3f}$"), (S.POST, rf"quadratic: \ $R^2 = {d['r2'][1]:.3f}$"),
                      (FIT, rf"linear spline, \ knots 30, 45, 60, 67: \ $R^2 = {d['r2'][2]:.3f}$"), (EXACT, r"the World's mean log income (3-year bins)")],
                     font_size=20).move_to([4.6, 1.8, 0])
        rows = fit_rows(VGroup(
            label(r"still \emph{linear} regression: \ linear in the coefficients, \ not in age", font_size=22, color=OBS),
            label(r"columns $1, a, (a-30)_+, (a-45)_+, \dots$: \ a broken line", font_size=22, color=GREY_A),
            label(r"the drop at 67 is retirement", font_size=22, color=GREY_A),
        ), 4.6, 0.3, [4.6, -1.0, 0])
        tag = simulated_tag(r"the World: \ 600 adults", corner=DR)
        with self.voiceover(
            "Linear regression can fit curves. <bookmark mark='a'/> Six hundred of the World's adults: log income against age. "
            "<bookmark mark='b'/> A straight line explains one percent of the variation; it can't follow a career. "
            "<bookmark mark='c'/> A quadratic, with age and age squared as two columns, rises and falls: twelve percent. "
            "<bookmark mark='d'/> A linear spline, a broken line with knots at thirty, forty-five, sixty and sixty-seven, built "
            "from columns like age minus thirty where positive, does better still and catches the drop at retirement. "
            "<bookmark mark='e'/> The dashed curve is the World's mean log income in three-year age bins. All three are still linear regression: "
            "linear in the coefficients, not in age. Part 29 does this with smoothing."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(pts, lag_ratio=0.002), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lin), FadeIn(leg[0]))
            vo.wait_until("c")
            self.play(Create(quad), FadeIn(leg[1]), FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(Create(spl), FadeIn(leg[2]), FadeIn(rows[1:]))
            vo.wait_until("e")
            self.play(Create(truth), FadeIn(leg[3]))
        self.clear_scene()

    def extrapolation(self):
        d = load("poly")
        e = d["extrap"]
        rows = fit_rows(VGroup(
            label(r"the fitted quadratic, \ asked about ages it never saw:", font_size=28),
            MathTex(rf"\text{{age 120}}:\ e^{{{e['120']:.2f}}} \approx {np.exp(e['120']):,.0f}".replace(",", "{,}"), font_size=32),
            MathTex(rf"\text{{age 150}}:\ e^{{{e['150']:.2f}}} \approx {np.exp(e['150']):,.0f}".replace(",", "{,}"), font_size=32, color=RES),
            label(r"a curve is only checked where there are data; \ beyond them it is pure assumption", font_size=26, color=OBS),
            label(r"Mark Twain, \ \emph{Life on the Mississippi} (1883): \ the river has shortened 242 miles in 176 years, \ so a million "
                  r"years ago it stuck out over the Gulf like a fishing rod", font_size=22, color=GREY_A),
        ), 12.6, 0.4, [0, 0.0, 0])
        intro = label('Extrapolation depends on an unchecked model', font_size=36)
        with self.voiceover(
            "A warning about curves. <bookmark mark='a'/> Ask the fitted quadratic about ages it never saw. "
            "<bookmark mark='b'/> At a hundred and twenty, an exponentiated fitted log income of about three thousand two hundred, a geometric-scale prediction rather than the arithmetic mean. "
            "<bookmark mark='c'/> At a hundred and fifty, a hundred and sixty. The parabola has kept falling, as parabolas do. "
            "<bookmark mark='d'/> A fitted curve is checked only where there are data; beyond them it's pure assumption. "
            "<bookmark mark='e'/> Mark Twain made the point in 1883: the lower Mississippi had shortened by two hundred and "
            "forty-two miles in a hundred and seventy-six years, so a million years earlier it must have stuck out over the "
            "Gulf of Mexico like a fishing rod."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def standardized(self):
        rows = [
            cmath(r"y", r"=", r"\beta_0 + \beta_1 x", r"\quad \beta_1 \text{ in units of } y \text{ per unit of } x", font_size=32),
            cmath(r"x \to 100\,x\ \ (\text{m} \to \text{cm})", r"\Rightarrow", r"\beta_1 \to \beta_1/100", r"\quad t,\ p,\ R^2 \text{ unchanged}", font_size=30),
            cmath(r"\beta^{\mathrm{std}}_1", r"=", r"\beta_1\,\frac{s_x}{s_y}", r"\quad\text{per SD of } x, \text{ in SDs of } y", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"a slope always carries units"), why(r"rescaling a predictor rescales its coefficient, \ nothing else"),
                why(r"unit-free, \ sample-dependent; \ not a measure of causal importance")]
        with self.voiceover(
            "<bookmark mark='a'/> A slope always carries units: units of y per unit of x. <bookmark mark='b'/> Measure x in "
            "centimetres instead of metres, and the coefficient shrinks a hundredfold, while its t statistic, its p-value and "
            "R squared don't change at all. A coefficient's size tells you nothing until you know its units. "
            "<bookmark mark='c'/> Standardized coefficients, per standard deviation of x in standard deviations of y, remove "
            "the units, but do not make predictors comparable in causal importance. But they depend on how spread out x happened to be in this sample, "
            "the same weakness as R squared."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.6, buff=0.9, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def regions(self):
        from explainer.stats.kit import ols as O
        from explainer.stats.world import World

        W = World()
        g = np.random.Generator(np.random.PCG64(4))
        idx = g.choice(np.flatnonzero(W.adult & W.male), 300, replace=False)
        reg, h = W.region[idx], W.height[idx]
        r = O.fit(O.design(*[(reg == k).astype(float) for k in range(1, 10)]), h)
        f = r.f_test(O.fit(np.ones((300, 1)), h))
        rows = [
            cmath(r"\text{height} \sim \mathbf 1\{\text{region 1}\} + \dots + \mathbf 1\{\text{region 9}\}", r"\ ", r"", font_size=30),
            cmath(r"\hat\beta_0", r"=", rf"{r.coef[0]:.1f}\ \text{{cm}}", r"\quad\text{the reference region, 0}", font_size=32),
            cmath(r"\hat\beta_k", r"=", r"\text{region } k \text{ minus region 0}", font_size=32),
            cmath(r"F_{9,\,290}", r"=", rf"{f['F']:.2f},\ \ p = {f['p']:.2f}", r"\quad\text{no evidence the regions differ}", font_size=32),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"ten regions: \ nine dummies and an intercept"), why(r"all ten dummies plus an intercept would be collinear"),
                why(r"every coefficient is a comparison with the reference"),
                why(r"one $F$-test for the whole factor: \ the one-way ANOVA (Part 13)")]
        tag = simulated_tag(r"the World: \ 300 men", corner=UR)
        intro = label('Represent a factor with an intercept and nine dummies', font_size=36)
        with self.voiceover(
            "A variable with many categories needs one dummy fewer than it has levels. <bookmark mark='a'/> Three hundred of "
            "the World's men, and their region, one of ten: nine dummies plus an intercept. <bookmark mark='b'/> All ten dummies "
            "plus an intercept would be exactly collinear, since the dummies add up to the ones column. So one region is left "
            "out as the reference, and the intercept is its mean, a hundred and seventy-six centimetres. "
            "<bookmark mark='c'/> Every other coefficient is a difference from the reference. <bookmark mark='d'/> To ask whether "
            "region matters at all, test all nine together with one F-test: F of point nine, p of point five two. No evidence "
            "the regions differ, which is how the World was built. That test is the one-way analysis of variance of Part 13."
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(tag))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.2, buff=0.65, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()
