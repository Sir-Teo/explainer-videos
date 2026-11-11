from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import BAD, COIN, GOOD, HURDLE, LINEAR, MKT, NET, PART, TREE, ask, fit_right, load

COLS = {"linear betas": LINEAR, "CA1": TREE, "CA2": NET}


class Autoencoder(VoiceoverScene):
    def construct(self):
        a = load("autoenc")
        self.card()
        self.model()
        self.ipca()
        self.picture()
        self.fit(a["rows"])
        self.predict(a["rows"])
        self.question()

    def card(self):
        c = chapter_card(7, r"Autoencoder asset pricing", r"Which few factors move all coins, and do their betas say "
                         r"which will earn more?", part=PART)
        with self.voiceover("Chapter seven. From forecasting returns one asset at a time to explaining them all at "
                            "once: factor models, learned."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"r_{i,t+1}", r"=", r"\beta(z_{i,t})^{\top} f_{t+1} + \varepsilon_{i,t+1}", font_size=34,
                      colors={r"r_{i,t+1}": COIN}),
                cmath(r"x_{t+1}", r"=", r"\tfrac{1}{N_t}\,[\mathbf 1, Z_t]^{\top} r_{t+1}", font_size=34,
                      colors={r"x_{t+1}": HURDLE}),
                cmath(r"f_{t+1}", r"=", r"W\, x_{t+1}", font_size=34, colors={r"f_{t+1}": HURDLE}),
                cmath(r"\min_{\beta(\cdot),\,W}", r"\ ", r"\textstyle\sum_{t, i}\big(r_{i,t+1} - \beta(z_{i,t})^{\top} W x_{t+1}"
                      r"\big)^2", font_size=34, colors={r"\min_{\beta(\cdot),\,W}": NET})]
        whys = [why(r"a conditional factor model: $K$ common factors, and each coin's exposures are a function of its "
                    r"characteristics last week (Part 24's betas, now changing with the coin)"),
                why(r"characteristic-managed portfolios: the market, and for each characteristic a portfolio long the "
                    r"coins that rank high on it; 16 returns a week"),
                why('The factor arm combines contemporaneous managed returns. Tradability requires additional execution and portfolio restrictions.'),
                why(r"Gu, Kelly and Xiu (2021): fit both arms together. The beta arm is a network of $z$; the factor arm "
                    r"is linear. An autoencoder: returns in, a $K$-dimensional bottleneck, returns out")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "A conditional factor model separates exposures and common realised factors. <bookmark mark='a'/> Characteristics determine each asset's exposures through a shared map. <bookmark mark='b'/> The original forms sixteen managed-return summaries from current returns and past ranked characteristics. These algebraic portfolios do not by themselves establish executable trading rules. <bookmark mark='c'/> A restricted linear arm maps those summaries into factor returns. <bookmark mark='d'/> Training jointly minimises reconstruction error. Factor rotations and scales require identifying normalisations. The architecture is inspired by conditional autoencoder asset pricing; its implementation and evaluation are smaller and more restricted than the cited paper."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def ipca(self):
        rows=[cmath(r"\beta(z)",r"=",r"\Gamma^\top z",font_size=32),cmath(r"f_t",r"=",r"(\Gamma^\top Z_t^\top Z_t\Gamma)^{-1}\Gamma^\top Z_t^\top r_t",font_size=30),cmath(r"\operatorname{vec}(\Gamma)",r"=",r"[\sum_t(f_tf_t^\top)\otimes(Z_t^\top Z_t)]^{-1}\sum_t(f_t\otimes Z_t^\top)r_t",font_size=27),cmath(r"Z_t^\top Z_t=cI",r"\Rightarrow",r"\text{global loading space: top eigenspace of }\sum_t Z_t^\top r_tr_t^\top Z_t",font_size=27)]
        whys=[why(r"Unrestricted linear-beta factor model, with identification and invertibility conditions"),why(r"For fixed loadings: unrestricted period factors from cross-sectional least squares"),why(r"For fixed factors: pooled least squares with column-major vectorisation; alternate, without a global one-step guarantee"),why(r"Equal orthonormalisation and loading normalisation give a global eigenproblem. The implemented managed-factor arm is restricted and gradient-fitted.")]
        step=ladder(self,rows,whys,keep=3,top=2.8,x=-.4,buff=.5,edge=6.8)
        with self.voiceover("Distinguish a theoretical linear factor model from our restricted implementation. <bookmark mark='a'/> Linear betas use a loading matrix with identification normalisations. <bookmark mark='b'/> Fixing that matrix gives unrestricted per-period least-squares factors. <bookmark mark='c'/> Fixing the factors gives a pooled normal equation; alternating these steps need not reach a global solution in one iteration. <bookmark mark='d'/> Under equal orthonormalisation, a globally optimal loading space follows from an eigenproblem. Our autoencoder instead gradient-fits a restricted managed-portfolio factor arm, with possible beta biases; it is inspired by IPCA rather than identical to unrestricted alternating least squares.") as vo:
            step(0);vo.wait_until("a");self.wait(.1)
            vo.wait_until("b");step(1)
            vo.wait_until("c");step(2)
            vo.wait_until("d");step(3)
        self.clear_scene()

    def picture(self):
        def stack(n, col, h=0.22):
            return VGroup(*[Circle(radius=h / 2, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.3)
                            for _ in range(n)]).arrange(DOWN, buff=0.08)
        z_in = stack(8, COIN)
        hid = stack(6, NET)
        beta = stack(3, LINEAR)
        x_in = stack(8, HURDLE)
        fac = stack(3, HURDLE)
        out = stack(1, GOOD, h=0.4)
        left = VGroup(z_in, hid, beta).arrange(RIGHT, buff=1.0)
        right = VGroup(x_in, fac).arrange(RIGHT, buff=1.0)
        arms = VGroup(left, right).arrange(DOWN, buff=0.9).move_to(LEFT * 1.6)
        out.next_to(arms, RIGHT, buff=1.5)

        def connect(a, b, col):
            return VGroup(*[Line(p.get_center(), q.get_center(), stroke_width=0.6, color=col, stroke_opacity=0.4)
                            for p in a for q in b])
        lines = VGroup(connect(z_in, hid, NET), connect(hid, beta, NET), connect(x_in, fac, HURDLE),
                       *[Line(b_.get_center(), out.get_center(), stroke_width=1.2, color=GREY_B) for b_ in beta],
                       *[Line(f_.get_center(), out.get_center(), stroke_width=1.2, color=GREY_B) for f_ in fac])
        labs = VGroup(label(r"characteristics $z_{i,t}$", font_size=22, color=COIN).next_to(z_in, LEFT, buff=0.2),
                      label(r"betas $\beta(z_{i,t})$", font_size=22, color=LINEAR).next_to(beta, UP, buff=0.15),
                      label(r"managed portfolios $x_{t+1}$", font_size=22, color=HURDLE).next_to(x_in, LEFT, buff=0.2),
                      label(r"factors $f_{t+1}$", font_size=22, color=HURDLE).next_to(fac, DOWN, buff=0.15),
                      label(r"$\hat r_{i,t+1} = \beta^{\top} f$", font_size=20, color=GOOD).next_to(out, RIGHT, buff=0.2))
        for l_ in labs:
            fit_right(l_)
        with self.voiceover(
            "Read the two arms carefully. <bookmark mark='a'/> Past characteristics enter the beta network to produce exposures. <bookmark mark='b'/> Contemporaneous managed returns enter a restricted linear factor arm. <bookmark mark='c'/> Their inner product reconstructs a contemporaneous asset return. The linear-beta, one-hidden-layer and two-hidden-layer versions differ in their beta maps. The linear-beta implementation is not unrestricted IPCA, and feeding realised returns into factor extraction does not forecast those returns."
        ) as vo:
            self.add(left,labs[0],labs[1])
            vo.wait_until("a")
            self.play(Create(lines[0]),Create(lines[1]))
            vo.wait_until("b")
            self.play(FadeIn(right), Create(lines[2]), FadeIn(labs[2]), FadeIn(labs[3]))
            vo.wait_until("c")
            self.play(FadeIn(out), Create(VGroup(*lines[3:])), FadeIn(labs[4]))
        self.wait(0.4)
        self.clear_scene()

    def _plot(self, rows, key, lo, hi, ylabel, yticks):
        values=[r[key] for r in rows]
        pad=max(.01,(max(values)-min(values))*.15)
        lo=min(0,min(values))-pad;hi=max(0,max(values))+pad;yticks=list(np.linspace(lo,hi,5))
        g = axes([0.6, 5.4], [lo, hi], x_length=7.0, y_length=4.0, xlabel=r"factors $K$", ylabel=ylabel,
                 xticks=[1, 2, 3, 4, 5], yticks=yticks, yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=14).move_to(
            LEFT * 1.8 + DOWN * 0.3)
        ax = g.ax
        lines = VGroup()
        for nm, col in COLS.items():
            ks = [r["K"] for r in rows if r["model"] == nm]
            vs = [r[key] for r in rows if r["model"] == nm]
            lines.add(VGroup(curve(ax, ks, vs, col, stroke_width=3),
                             *[Dot(ax.c2p(k, v), radius=0.06, color=col) for k, v in zip(ks, vs)]))
        leg = legend([(c, n) for n, c in COLS.items()], font_size=18).to_edge(RIGHT, buff=0.4).shift(UP * 1.5)
        fit_right(leg)
        return g, lines, leg

    def fit(self, rows):
        g, lines, leg = self._plot(rows, "total", 0.3, 0.6, r"total $R^2$ on 2020, weekly", [0.3, 0.4, 0.5, 0.6])
        best = max(rows, key=lambda r: r["total"])
        one = [r["total"] for r in rows if r["K"] == 1]
        side = VGroup(
            MathTex(rf"K = 1:\ {100 * min(one):.0f}\text{{--}}{100 * max(one):.0f}\%", font_size=24, color=MKT),
            MathTex(rf"\text{{best}}:\ {100 * best['total']:.1f}\%\ ({best['model']}, K = {best['K']})".replace(
                "linear betas", r"\text{linear}"), font_size=24),
            wrapped_label(r"total $R^2 = 1 - \sum (r - \hat\beta^{\top}\hat f_t)^2 / \sum r^2$: how much of each week's "
                          r"returns the factors of that same week explain. Fitted on mid-2018 to mid-2019, tuned on the "
                          r"second half of 2019", 3.4, 22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(leg, DOWN, buff=0.4)
        fit_right(side)
        with self.voiceover(
            f"Total fit uses contemporaneous test-week returns in the factor arm. <bookmark mark='a'/> Parameters were trained earlier, but these factor inputs are realised in the evaluation week, so this is reconstruction rather than a forecast. For one factor the saved total R squared ranges from {100*min(one):.1f} to {100*max(one):.1f} percent. <bookmark mark='b'/> The largest saved total fit is {100*best['total']:.1f} percent for {best['model']} with {best['K']} factors. We have not identified a particular factor as the market or isolated why nonlinear versions differ. Zero-benchmark reconstruction R squared is also not literally a variance fraction."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3, run_time=2))
            self.play(FadeIn(side[0]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def predict(self, rows):
        g, lines, leg = self._plot(rows, "pred", -0.03, 0.01, r"predictive $R^2$ on 2020", [-0.03, -0.02, -0.01, 0, 0.01])
        ax = g[0]
        zero = DashedLine(ax.c2p(0.6, 0), ax.c2p(5.4, 0), color=GREY_B, stroke_width=1.5)
        eq = MathTex(r"R^2_{\text{pred}} = 1 - \frac{\sum (r_{i,t+1} - \hat\beta(z_{i,t})^{\top}\hat\lambda)^2}{\sum r_{i,t+1}^2},"
                     r"\quad \hat\lambda = \overline{\hat f}", font_size=26).to_edge(UP, buff=0.3)
        side = wrapped_label('Prediction uses mean fitted factors from training plus validation. Changing premia, beta error, estimation and model restrictions are possible contributors; these outputs do not uniquely identify a cause.', 3.4, 15,
                             GREY_A).next_to(leg, DOWN, buff=0.4)
        fit_right(side)
        with self.voiceover(
            f"Forecasting is a different calculation. <bookmark mark='a'/> The original substitutes mean fitted factors from training plus validation for contemporaneous factors. <bookmark mark='b'/> Saved predictive R squared ranges from {100*min(r['pred'] for r in rows):.2f} to {100*max(r['pred'] for r in rows):.2f} percent. <bookmark mark='c'/> Changing premia, exposure error, estimation and model restrictions can all contribute. The saved outputs do not uniquely identify the cause. Describing co-movement can support risk management, but is not the same task as predicting expected returns."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3, run_time=2))
            vo.wait_until("c")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a factor model's total $R^2$ is 50\% but its predictive $R^2$ is negative. Name two ways to estimate "
                r"the premia $\lambda$ better, and what each assumes.")
        with self.voiceover(
            "Pause and predict. A factor model explains half the variance of returns but forecasts worse than zero. "
            "Name two ways to estimate the factor premia better, and say what each one assumes."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
