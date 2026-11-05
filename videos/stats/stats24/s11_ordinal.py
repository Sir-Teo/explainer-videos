from __future__ import annotations

import numpy as np

from videos.stats.stats24.common import *  # noqa: F403

CATS = [r"under", r"normal", r"over", r"obese"]
CCOL = [TEAL, BLUE, PATH, RED]


class Ordinal(VoiceoverScene):
    def construct(self):
        self.card()
        self.multinomial()
        self.po()
        self.fit()
        self.stack()
        self.check()
        self.others()

    def card(self):
        card = chapter_card(10, r"Multinomial and ordinal", r"More than two outcomes", lit=(1980,), part=PART)
        with self.voiceover("Chapter ten. Multinomial and ordinal models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def multinomial(self):
        rows = [
            cmath(r"P(y = j \mid x)", r"=", r"\dfrac{e^{x^\top\beta_j}}{\sum_k e^{x^\top\beta_k}}, \ \ \beta_0 = 0", font_size=30),
            cmath(r"\log\dfrac{P(y = j)}{P(y = 0)}", r"=", r"x^\top\beta_j", font_size=30),
            cmath(r"\text{parameters}", r":", r"(K - 1) \times p", font_size=30),
            cmath(r"\text{IIA}", r":", r"\text{the odds of } j \text{ vs } k \text{ ignore every other option}", font_size=28),
        ]
        rows[0][2].set_color(MODEL)
        whys = [why(r"baseline-category logits: \ the softmax"), why(r"each category against the baseline"),
                why(r"one coefficient vector per extra category"), why(r"the red bus and the blue bus")]
        with self.voiceover(
            "<bookmark mark='a'/> With more than two unordered outcomes, the multinomial logit gives each category its own "
            "linear predictor and turns them into probabilities with the softmax, one category serving as the baseline. "
            "<bookmark mark='b'/> Each coefficient vector is a log odds of that category against the baseline. "
            "<bookmark mark='c'/> With K categories and p covariates there are K minus one times p coefficients, which adds up "
            "quickly. <bookmark mark='d'/> And it assumes the independence of irrelevant alternatives: the odds of choosing "
            "the car over the red bus don't change when a blue bus, identical but for colour, is added. Daniel McFadden's "
            "famous example shows how odd that can be."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def po(self):
        rows = [
            cmath(r"y^*", r"=", r"x^\top\beta + \varepsilon, \ \ \varepsilon \sim \text{logistic}", font_size=30),
            cmath(r"y = j", r"\iff", r"\theta_{j-1} < y^* \le \theta_j", font_size=30),
            cmath(r"\text{logit}\, P(y \le j \mid x)", r"=", r"\theta_j - x^\top\beta", font_size=30),
            cmath(r"\text{proportional odds}", r":", r"\text{one } \beta \text{ for every cut-point}", font_size=30),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"a latent continuous scale"), why(r"cut-points chop it into categories"),
                why(r"McCullagh (1980)"), why(r"the odds ratio is the same at every cut")]
        with self.voiceover(
            "<bookmark mark='a'/> When categories are ordered, underweight, normal, overweight, obese, use the order. Imagine "
            "a continuous latent scale, a linear predictor plus logistic noise, <bookmark mark='b'/> chopped into categories "
            "by cut-points. <bookmark mark='c'/> Then the log odds of being at or below category j is theta j minus x "
            "transpose beta: Peter McCullagh's proportional-odds model, from 1980. <bookmark mark='d'/> A single coefficient "
            "vector serves every cut-point, so each covariate has one odds ratio, whichever way the categories are split."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fit(self):
        d = load("ordinal")
        c = np.asarray(d["counts"])
        b, se = d["beta"], d["se_beta"]
        rows = [
            cmath(r"\text{data}", r":", rf"{d['n']:,} \text{{ adults: \ }} {c[0]}, \ {c[1]:,}, \ {c[2]:,}, \ {c[3]}", font_size=30),
            cmath(r"\hat\beta_{\text{age}}", r"=", rf"{b[0]:.3f} \ (\mathrm{{SE}} \ {se[0]:.3f}) \ \text{{per 10 years}}", font_size=30),
            cmath(r"\text{odds ratio}", r"=", rf"e^{{{b[0]:.3f}}} = {np.exp(b[0]):.2f}", font_size=30),
            cmath(r"\hat\beta_{\text{female}}", r"=", rf"{b[1]:.3f} \ (\mathrm{{SE}} \ {se[1]:.3f})", font_size=30),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"BMI categories of the World's adults"), why(r"the latent scale rises with age"),
                why(r"heavier categories, \ at every cut"), why(r"no sex difference: \ as the World was built")]
        with self.voiceover(
            "<bookmark mark='a'/> Three thousand of the World's adults, classified by body mass index: eighty-two "
            "underweight, a thousand normal, a thousand and forty-five overweight, eight hundred and seventy-three obese. "
            "<bookmark mark='b'/> In the proportional-odds model, ten years of age move the latent scale up by point one "
            "seven three. <bookmark mark='c'/> So the odds of being in a heavier category, at any cut, are one point one "
            "nine times higher per decade. <bookmark mark='d'/> Sex makes no difference, which is right: the World's body "
            "mass index doesn't depend on sex."
        ) as vo:
            self.add(simulated_tag())
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def stack(self):
        d = load("ordinal")
        ages = np.asarray(d["ages"], float)
        P = np.asarray(d["probs"]["0"])
        A = axes([18, 85], [0, 1], x_length=8.0, y_length=4.4, xlabel=r"age", ylabel=r"fitted probability",
                 xticks=[20, 30, 40, 50, 60, 70, 80], yticks=[0, 0.25, 0.5, 0.75, 1], center=[-1.6, 0.3, 0])
        ax = A.ax
        cum = np.cumsum(P, axis=1)
        bands = VGroup()
        for j in range(4):
            lo = cum[:, j - 1] if j else np.zeros(len(ages))
            hi = cum[:, j]
            pts = [ax.c2p(a, b) for a, b in zip(ages, lo)] + [ax.c2p(a, b) for a, b in zip(ages[::-1], hi[::-1])]
            bands.add(Polygon(*pts, stroke_width=0, fill_color=CCOL[j], fill_opacity=0.6))
        rows = fit_rows(VGroup(
            *[label(name, font_size=22, color=c) for name, c in zip(CATS, CCOL)],
            label(r"one latent shift, \ four probabilities", font_size=22, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are the fitted probabilities of the four categories across age, stacked. "
            "<bookmark mark='b'/> As the latent scale moves up with age, probability flows from underweight and normal into "
            "overweight and obese, all governed by one coefficient."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bands], lag_ratio=0.3), LaggedStart(*[FadeIn(r) for r in rows[:4]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(rows[4]))
        self.wait(2.0)
        self.clear_scene()


    def others(self):
        rows = [
            cmath(r"\text{cumulative}", r":", r"\text{logit } P(y \le j) = \theta_j - x^\top\beta", font_size=30),
            cmath(r"\text{adjacent categories}", r":", r"\log\dfrac{P(y = j + 1)}{P(y = j)} = \alpha_j + x^\top\beta", font_size=30),
            cmath(r"\text{continuation ratio}", r":", r"\text{logit } P(y > j \mid y \ge j) = \alpha_j + x^\top\beta", font_size=30),
            cmath(r"\text{links}", r":", r"\text{probit, \ cloglog: \ the latent noise changes}", font_size=30),
        ]
        rows[2][-1].set_color(PATH)
        whys = [why(r"this chapter's model"), why(r"neighbouring steps"), why(r"stages passed in order: \ grades, \ survival"),
                why(r"cloglog: \ a grouped proportional-hazards model")]
        with self.voiceover(
            "<bookmark mark='a'/> The cumulative logit is one of several ordinal models. <bookmark mark='b'/> Adjacent-"
            "category logits compare each category with the next. <bookmark mark='c'/> Continuation ratios model the "
            "chance of going beyond a category given that you reached it, natural for stages passed in order, like school "
            "grades or survival through intervals. <bookmark mark='d'/> And the latent noise need not be logistic: a probit "
            "gives the ordered probit, and a complementary log-log gives a grouped version of Part 40's proportional-hazards "
            "model."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def check(self):
        d = load("ordinal")
        sep = d["separate"]
        hdr = [r"\textbf{cut}", r"\textbf{age slope}", r"\textbf{SE}"]
        names = [r"under $|$ normal+", r"$\le$ normal $|$ over+", r"$\le$ over $|$ obese"]
        body = [[n, f"{s['coef'][1]:.3f}", f"{s['se'][1]:.3f}"] for n, s in zip(names, sep)]
        body.append([r"proportional odds", f"{d['beta'][0]:.3f}", f"{d['se_beta'][0]:.3f}"])
        t = table_rows([hdr] + body, font_size=26, col_buff=0.8, row_buff=0.3, colors=[GREY_A, TEAL, BLUE, PATH, MODEL])
        t.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"separate logistic regressions at each cut: \ the slopes should agree", font_size=22),
            label(r"the first is twice the others: \ age matters more at the bottom", font_size=22, color=RES),
            label(r"remedies: \ partial proportional odds, \ or the multinomial", font_size=22, color=GREY_A),
        ), 12.0, 0.25, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Is one coefficient enough? Fit a separate logistic regression at each cut: underweight "
            "against the rest, normal or less against overweight or more, and so on. If the odds were proportional, the "
            "slopes would agree. <bookmark mark='b'/> They don't quite: at the bottom cut the age slope is point three one, "
            "nearly twice the others, so age matters more for leaving underweight than for crossing into obesity. "
            "<bookmark mark='c'/> A partial proportional-odds model lets that one slope differ; or fall back on the "
            "multinomial, at the price of many more parameters."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(t[0]), FadeIn(foot[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in t[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()
