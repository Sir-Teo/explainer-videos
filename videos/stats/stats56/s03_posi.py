from __future__ import annotations

import numpy as np

from videos.stats.stats56.common import *  # noqa: F403


class PoSI(VoiceoverScene):
    def construct(self):
        self.card()
        self.target()
        self.constant()
        self.chart()
        self.bounds()
        self.practice()
        self.verdict()

    def card(self):
        card = chapter_card(2, r"PoSI", r"Cover every model you might have chosen", lit=(2013,), part=PART)
        with self.voiceover("Chapter two. Post-selection inference, PoSI: cover every model you might have chosen."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def target(self):
        rows = [
            cmath(r"\text{a submodel } M \subseteq \{1, \dots, p\}", r":", r"\beta_M = X_M^+\,\mu = \arg\min_b \|\mu - X_M b\|^2", font_size=32),
            cmath(r"\beta_{j\cdot M}", r":", r"\text{the coefficient of } x_j \text{ adjusted for the others in } M", font_size=32),
            cmath(r"\text{not}", r":", r"\text{the true model's coefficient: \ no model need be true}", font_size=34),
            cmath(r"\hat M = \hat M(Y)", r"\Rightarrow", r"\text{the target } \beta_{j\cdot\hat M} \text{ is itself random}", font_size=34),
        ]
        rows[0][-1].set_color(SIMC)
        rows[3][-1].set_color(SELC)
        whys = [why(r"$\mu = E Y$: \ the projection"), why(r"meaning changes with $M$"), why(r"Berk, \ Brown, \ Buja, \ Zhang \& Zhao"), why(r"a moving target")]
        with self.voiceover(
            "<bookmark mark='a'/> Richard Berk, Lawrence Brown, Andreas Buja, Kai Zhang and Linda Zhao, at Wharton, began "
            "with the target. For any submodel M, a set of columns, define beta M as the projection of the mean of Y onto "
            "those columns. <bookmark mark='b'/> Its j-th entry is the coefficient of x j adjusted for the other variables "
            "in M; it means something different in every submodel. <bookmark mark='c'/> It is not the coefficient of some "
            "true model; no model need be true. <bookmark mark='d'/> When the submodel is chosen from the data, the target "
            "itself is random, and that is the source of the trouble."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def constant(self):
        rows = [
            cmath(r"t_{j\cdot M}", r"=", r"\frac{\hat\beta_{j\cdot M} - \beta_{j\cdot M}}{\sigma\,\|l_{j\cdot M}\|}, \ \ l_{j\cdot M}' = e_j' X_M^+", font_size=34),
            cmath(r"K", r":", r"P\Big(\max_{M}\max_{j \in M}|t_{j\cdot M}| \le K\Big) = 1 - \alpha", font_size=36),
            cmath(r"\Rightarrow", r"\;", r"P\big(\beta_{j\cdot\hat M} \in \hat\beta_{j\cdot\hat M} \pm K\sigma\|l_{j\cdot\hat M}\|\ \ \forall j \in \hat M\big) \ge 1 - \alpha", font_size=32),
            cmath(r"\text{for any}", r":", r"\text{rule: \ lasso, \ stepwise, \ a human}", font_size=32),
        ]
        rows[1][-1].set_color(SIMC)
        rows[3][-1].set_color(HYBC)
        whys = [why(r"each a normal contrast of $Y$"), why(r"the PoSI constant"), why(r"$\hat M$ is one of the $M$'s"), why(r"its strength")]
        with self.voiceover(
            "<bookmark mark='a'/> For each submodel and each coefficient in it, the standardized estimate is a normal "
            "contrast of Y, with the contrast vector l j dot M. <bookmark mark='b'/> The PoSI constant K is the one minus "
            "alpha quantile of the largest of these t-statistics, over every submodel and every coefficient in it. "
            "<bookmark mark='c'/> Then intervals of half-width K standard errors cover every coefficient of the selected "
            "model, simultaneously, because the selected model is one of the models in the maximum. <bookmark mark='d'/> "
            "And that holds for any selection rule at all: the lasso, stepwise regression, or a human looking at plots and "
            "trying things until something works."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("posi")
        rows = d["rows"]
        ps = [r["p"] for r in rows]
        A = axes([1.5, 10.5], [1.5, 4.7], x_length=7.4, y_length=4.4, xlabel=rf"$p$ variables, \ $n = {d['n']}$, \ all $p 2^{{p-1}}$ coefficients",
                 ylabel=r"the constant $K$", xticks=[2, 4, 6, 8, 10], yticks=[2, 3, 4], center=[-2.5, 0.2, 0])
        ax = A.ax

        def ln(key, col, dash=False):
            c = VGroup(polyline(ax, ps, [r[key] for r in rows], col, 4), *[Dot(ax.c2p(p, r[key]), radius=0.06, color=col) for p, r in zip(ps, rows)])
            return c

        z = DashedLine(ax.c2p(1.5, 1.96), ax.c2p(10.5, 1.96), color=NAIVEC, stroke_width=2)
        co, cc = ln("orth", HYBC), ln("corr", SIMC)
        cb, cs = ln("bonf", GREY_B), ln("scheffe", WHITE)
        r10 = rows[-1]
        side = fit_rows(VGroup(
            label(r"red dashed: \ 1.96, \ no correction", font_size=22, color=NAIVEC),
            label(rf"green: \ orthogonal design: \ {r10['orth']:.2f} at $p = 10$", font_size=22, color=HYBC),
            label(rf"purple: \ correlated ($\rho = 0.5$): \ {r10['corr']:.2f}", font_size=22, color=SIMC),
            label(rf"grey: \ Bonferroni over {r10['n_contrasts']:,} contrasts: \ {r10['bonf']:.2f}", font_size=22, color=GREY_B),
            label(rf"white: \ Scheff\'e, \ $\sqrt{{\chi^2_p}}$: \ {r10['scheffe']:.2f}", font_size=22, color=WHITE),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The PoSI constant by simulation, against the number of variables. Without correction, one "
            f"point nine six. <bookmark mark='b'/> For an orthogonal design, the constant grows slowly, to {say(r10['orth'], 2)} "
            f"with ten variables. <bookmark mark='c'/> For correlated variables it grows faster, to {say(r10['corr'], 2)}, "
            f"because coefficients mean very different things in different submodels. <bookmark mark='d'/> A Bonferroni "
            f"correction over all {r10['n_contrasts']:,} coefficients would need {say(r10['bonf'], 2)}, <bookmark mark='e'/> "
            f"and Scheffé's method, which covers every linear contrast, {say(r10['scheffe'], 2)}. PoSI sits between the "
            f"naive and the universal."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated, \ 4,000 draws per point")))
            vo.wait_until("a")
            self.play(Create(z), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(co), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cc), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cb), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(cs), FadeIn(side[4]))
        self.clear_scene()

    def bounds(self):
        rows = [
            cmath(r"\text{always}", r":", r"K \le K_{\text{Scheff\'e}} = \sqrt{\chi^2_{p, 1 - \alpha}} \asymp \sqrt p", font_size=36),
            cmath(r"\text{orthogonal } X", r":", r"K \asymp \sqrt{2\log p}: \ \text{the max of } p \text{ normals}", font_size=34),
            cmath(r"\text{worst designs}", r":", r"K \asymp \sqrt p \ \ (\text{Berk et al. 2013})", font_size=34),
            cmath(r"\text{so}", r":", r"\text{the price of covering every model is up to } \sqrt p", font_size=34),
        ]
        rows[1][-1].set_color(HYBC)
        rows[2][-1].set_color(NAIVEC)
        whys = [why(r"all contrasts in a $p$-space"), why(r"each $t_{j\cdot M}$ is the same for all $M$"), why(r"the gap is real"), why(r"affordable for small $p$")]
        with self.voiceover(
            "<bookmark mark='a'/> How large can K get? Never larger than Scheffé's constant, the root of a chi-squared "
            "quantile, of order root p. <bookmark mark='b'/> For an orthogonal design every submodel's coefficients are the "
            "same, so K is the maximum of p normals, of order root two log p. <bookmark mark='c'/> And there are designs, "
            "constructed by Berk and colleagues, where K really is of order root p. <bookmark mark='d'/> So the price of covering every model you might have chosen "
            "can be as large as root p: affordable for a handful of variables, ruinous for thousands."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def practice(self):
        rows = [
            cmath(r"\text{compute } K", r":", r"\text{simulate } \max_{M, j}|l_{j\cdot M}'Z|, \ Z \sim N(0, I): \ p\,2^{p-1} \text{ contrasts}", font_size=30),
            cmath(r"\text{restrict}", r":", r"\text{submodels of size} \le m: \ \text{fewer contrasts, \ a smaller } K", font_size=32),
            cmath(r"\sigma \text{ unknown}", r":", r"\text{use } \hat\sigma \text{ from the full model and a } t\text{-type constant}", font_size=32),
            cmath(r"\text{target}", r":", r"\text{report what } \beta_{j\cdot\hat M} \text{ means: \ the effect adjusted for } \hat M", font_size=32),
        ]
        rows[1][-1].set_color(SIMC)
        whys = [why(r"Monte Carlo, \ as on the chart"), why(r"a smaller search space"), why(r"a $t$ maximum"), why(r"interpretation matters")]
        with self.voiceover(
            "<bookmark mark='a'/> In practice the constant is computed by simulation: draw standard normal vectors and "
            "take the largest absolute contrast over all p times two to the p minus one coefficients, as we did for "
            "the chart. <bookmark mark='b'/> If only submodels up to some size m will ever be considered, the maximum "
            "runs over fewer contrasts and the constant shrinks. <bookmark mark='c'/> With sigma unknown, estimate it "
            "from the full model and use a t-type constant. <bookmark mark='d'/> And report what the target means: the "
            "effect of x j adjusted for the other selected variables, which can differ in size and even sign from its "
            "effect in another model."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def verdict(self):
        rows = fit_rows(VGroup(
            label(r"PoSI's strengths:", font_size=28, color=GREY_A),
            label(r"valid for any selection, \ including informal snooping a paper never reports", font_size=26, color=HYBC),
            label(r"needs no model of how the selection was made", font_size=26, color=HYBC),
            label(r"its weaknesses:", font_size=28, color=GREY_A),
            label(r"conservative for any one rule; \ computing $K$ exactly is exponential in $p$", font_size=26, color=NAIVEC),
            label(r"next: \ condition on the rule actually used, \ and pay only for it", font_size=26, color=CONDC),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> PoSI's strengths. <bookmark mark='b'/> It is valid for any selection, including the "
            "informal snooping that a paper never reports. <bookmark mark='c'/> And it needs no model of how the selection "
            "was made. <bookmark mark='d'/> Its weaknesses. <bookmark mark='e'/> For any one selection rule it is "
            "conservative, and computing the constant exactly requires every one of the two to the p submodels. <bookmark "
            "mark='f'/> The next chapter takes the opposite approach: condition on the rule that was actually used, and pay "
            "only for that."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
