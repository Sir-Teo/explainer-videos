from __future__ import annotations

import numpy as np

from videos.stats.stats25.common import *  # noqa: F403


class Fixed(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_views()
        self.picture()
        self.mundlak()
        self.numbers()
        self.hausman()
        self.advice()

    def card(self):
        card = chapter_card(9, r"Fixed or random?", r"When the groups are correlated with $x$", lit=(1978,), part=PART)
        with self.voiceover("Chapter nine. Fixed effects or random effects?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def two_views(self):
        rows = [
            cmath(r"\text{fixed}", r":", r"y_{gi} = \alpha_g + \beta x_{gi} + \varepsilon_{gi}, \ \text{one } \alpha_g \text{ per school}", font_size=28),
            cmath(r"\text{random}", r":", r"\alpha_g = \mu + u_g, \ \ u_g \sim N(0, \tau^2) \ \text{independent of } x", font_size=28),
            cmath(r"\text{fixed uses}", r":", r"\text{only the variation of } x \text{ within schools}", font_size=28),
            cmath(r"\text{random uses}", r":", r"\text{within and between, \ weighted}", font_size=28),
        ]
        rows[1][2].set_color(RES)
        whys = [why(r"the within estimator: \ demean each school"), why(r"the assumption that matters"),
                why(r"additive intercepts removed; \ strict exogeneity still needed"), why(r"more efficient, \ if the assumption holds")]
        intro = label('Fixed effects control additive group intercepts under exogeneity', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Economists and statisticians argued about this for decades. A fixed-effects model "
            "gives every school its own intercept, a dummy variable each, which is the same as subtracting each "
            "school's mean from everything. <bookmark mark='b'/> A random-effects model draws the intercepts from a "
            "normal distribution, and, crucially, assumes they are independent of the predictors. <bookmark "
            "mark='c'/> Fixed effects use only variation within schools, so it removes additive, constant school "
            "intercepts. A common slope and strict conditional mean-zero pupil errors are still needed; causality "
            "needs further identification. <bookmark mark='d'/> Random effects use the within and between variation "
            "together, weighted, and are more efficient, if their assumption holds."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        d = load("mundlak")
        mx, my = np.asarray(d["school_ses"]), np.asarray(d["school_y"])
        b1, b0 = d["between"]
        A = axes([-1.6, 1.3], [370, 700], x_length=7.4, y_length=4.8, xlabel=r"school's mean home background (SES)",
                 ylabel=r"school's mean score", xticks=[-1, 0, 1], yticks=[400, 500, 600, 700], center=[-2.0, 0.2, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.03, color=GREY_B, fill_opacity=0.6) for a, b in zip(mx, my)])
        between = Line(ax.c2p(-1.5, b0 - 1.5 * b1), ax.c2p(1.2, b0 + 1.2 * b1), color=PATH, stroke_width=4)
        w = d["fe"]
        within = VGroup()
        for k in d["show"]:
            x0, y0 = mx[k], my[k]
            within.add(Line(ax.c2p(x0 - 0.35, y0 - 0.35 * w), ax.c2p(x0 + 0.35, y0 + 0.35 * w), color=SHRUNK, stroke_width=4))
        rows = fit_rows(VGroup(
            label(r"grey: \ the World's 400 schools", font_size=22),
            label(rf"yellow: \ unweighted between-school slope {b1:.1f}", font_size=22, color=PATH),
            label(rf"green: \ within schools, \ slope {w:.1f}", font_size=22, color=SHRUNK),
            label(r"richer schools are better than their pupils' SES alone predicts", font_size=20, color=GREY_A),
        ), 4.6, 0.42, [4.4, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is why it matters. Each grey dot is one of the World's schools: its pupils' "
            "average home background against its average score. <bookmark mark='b'/> The unweighted descriptive "
            "between-school slope is about forty points per unit of background. <bookmark mark='c'/> Within a school,"
            " comparing pupils with each other, the slope is twenty-nine. <bookmark mark='d'/> The World built it "
            "that way: a school full of advantaged pupils does better than their individual backgrounds predict, a "
            "contextual effect. So the school effects are correlated with SES, and the random-effects assumption "
            "fails."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.003), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(between), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(x) for x in within], lag_ratio=0.2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def mundlak(self):
        rows = [
            cmath(r"y_{gi}", r"=", r"\mu + \beta_W x_{gi} + \gamma\,\bar x_g + u_g + \varepsilon_{gi}", font_size=32),
            cmath(r"\hat\beta_W", r"=", r"\text{the fixed-effects estimate, \ exactly}", font_size=30),
            cmath(r"\gamma", r"=", r"\beta_B - \beta_W: \ \text{the contextual effect}", font_size=30),
            cmath(r"\gamma = 0", r":", r"\text{no linear association with included group means}", font_size=30),
        ]
        rows[0][2].set_color(SHRUNK)
        whys = [why(r"Mundlak (1978): \ add the school mean of $x$"), why(r"the between part is absorbed by $\bar x_g$"),
                why(r"between minus within"), why(r"a test of the assumption")]
        intro = label('Group predictor means separate within and between associations', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Yair Mundlak's 1978 resolution: keep the random effects, but add each school's mean"
            " of the predictor as a further predictor. <bookmark mark='b'/> Then the coefficient on the pupil's own "
            "SES is exactly the fixed-effects estimate here, with common within-school variance and the relevant "
            "group means included, <bookmark mark='c'/> and the coefficient on the school mean is the contextual "
            "effect, the between slope minus the within slope. <bookmark mark='d'/> Testing it probes a linear "
            "conditional-mean association with those group means. A zero coefficient cannot establish independence or"
            " rule out omitted nonlinear context. One model gives both answers, and keeps random effects' ability to "
            "predict for a new school."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def numbers(self):
        d = load("mundlak")
        se = d["mundlak_se"]
        hdr = [r"\textbf{model}", r"\textbf{SES within}", r"\textbf{SE}", r"\textbf{contextual}", r"\textbf{SE}"]
        body = [[r"random effects", f"{d['re']:.2f}", f"{d['re_se']:.2f}", r"---", r""],
                [r"fixed effects", f"{d['fe']:.2f}", f"{d['fe_se']:.2f}", r"---", r""],
                [r"Mundlak", f"{d['mundlak_within']:.2f}", f"{se[1]:.2f}", f"{d['mundlak_context']:.1f}", f"{se[2]:.1f}"],
                [r"the World", f"{d['truth_within']:.0f}", r"", f"{d['truth_context']:.0f}", r""]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.75, row_buff=0.3, colors=[GREY_A, RAW, POOLED, SHRUNK, TRUE])
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"60 pupils a school: \ random effects already lean on the within information", font_size=22, color=GREY_A),
            label(r"the contextual effect: \ real, \ and estimated from 400 schools, \ not 24,000 pupils", font_size=22, color=HIT),
        ), 12.0, 0.25, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The numbers. <bookmark mark='b'/> Random effects say twenty-nine point four, "
            "<bookmark mark='c'/> fixed effects twenty-nine point two. Close, because with sixty pupils a school the "
            "shrinkage factor is near one and random effects already lean mostly on the within-school comparison. "
            "<bookmark mark='d'/> Mundlak's model reproduces the fixed-effects slope exactly, and estimates a "
            "contextual effect of ten point six with a standard error of four. <bookmark mark='e'/> The World uses "
            "thirty within school and fifteen for latent school SES. Our estimated contextual regressor is the "
            "observed sample mean, so the targets are only approximately the same. The contextual effect is the "
            "noisier number, because it is learned from four hundred schools, not twenty-four thousand pupils."
        ) as vo:
            self.add(simulated_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tb[k + 1]))
                if k == 1:
                    self.play(FadeIn(foot[0]))
            vo.wait_until("e")
            self.play(FadeIn(tb[4]), FadeIn(foot[1]))
        self.clear_scene()

    def hausman(self):
        d = load("mundlak")
        rows = [
            cmath(r"H", r"=", r"\dfrac{(\hat\beta_{FE} - \hat\beta_{RE})^2}{\mathrm{Var}\,\hat\beta_{FE} - \mathrm{Var}\,\hat\beta_{RE}}", font_size=30),
            cmath(r"\text{why the difference}", r":", r"\mathrm{Cov}(\hat\beta_{RE}, \hat\beta_{FE} - \hat\beta_{RE}) = 0 \ \text{under } H_0", font_size=28),
            cmath(r"H", r"=", rf"\dfrac{{({d['fe']:.2f} - {d['re']:.2f})^2}}{{{d['fe_se']:.3f}^2 - {d['re_se']:.3f}^2}} = {d['hausman']:.2f}", font_size=30),
            cmath(r"p", r"=", rf"{d['p_hausman']:.3f} \ \text{{from }} \chi^2_1", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"Hausman (1978)"), why(r"the efficient estimator is uncorrelated with its gap"),
                why(r"a tiny gap, \ but tinier noise"), why(r"reject: \ the school effects are correlated with SES")]
        intro = label('Hausman compares estimators under an efficiency null', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Jerry Hausman's test of 1978 compares the two estimates directly: their squared difference, "
            "over the difference of their variances. <bookmark mark='b'/> That denominator is right because, when random "
            "effects are valid and efficient, the efficient estimator is uncorrelated with its difference from any other "
            "consistent one. <bookmark mark='c'/> Here the gap is only point two three, but the two estimates are so "
            "precise and so similar that the gap's own noise is smaller still: H is six point five six. "
            "<bookmark mark='d'/> A p-value of point oh one: reject, the school effects are correlated with SES, as built."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def advice(self):
        rows = fit_rows(VGroup(
            label(r"`random' is not about the groups being random: \ it is the assumption $u_g \perp x$", font_size=24, color=RES),
            label(r"within effects: \ additive group control + strict exogeneity; \ FE or Mundlak", font_size=24),
            label(r"new groups or group-level effects need between-group assumptions; \ RE is one option", font_size=24, color=SHRUNK),
            label(r"Mundlak's model gives both; \ the Hausman test checks the gap", font_size=24, color=HIT),
            label(r"Part 37: \ fixed effects as a causal design for panels", font_size=24, color=GREY_A),
        ), 12.6, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So the choice is not about whether schools are, philosophically, random. It is "
            "about the assumption that the school effects are unrelated to the predictors. <bookmark mark='b'/> If "
            "you want a within-school effect controlling additive constant school effects under strict exogeneity, "
            "use fixed effects, or Mundlak. <bookmark mark='c'/> If you want to predict for a new school, or to "
            "estimate an effect of something that varies only between schools, like the programme, you need "
            "additional restrictions or a design for between-school comparisons. Random effects are one option; "
            "school fixed effects absorb that programme variable. <bookmark mark='d'/> Mundlak's model delivers both."
            " <bookmark mark='e'/> And Part 37 returns to fixed effects as a causal design for panel data."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
