from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant25.common import FALSE, GOOD, HURDLE, NOISE, PART, TRUE, load


class Research(VoiceoverScene):
    def construct(self):
        t = load("discovery_theory")
        self.card()
        self.bh()
        self.proof()
        self.storey()
        self.sim(t)
        self.histograms(t)
        self.lam_curve(t)
        self.lfdr()
        self.density(t)
        self.verdict(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"How many anomalies are real?", r"Not which ones pass a test, but what share of the zoo is "
                          r"signal at all", part=PART)
        with self.voiceover("For the researcher: Chapter 2 controlled the false discovery rate with Benjamini and "
                            "Hochberg's rule. Two deeper questions remain: why that rule works, and how many of the "
                            "anomalies are real at all. The answer needs the p-values that were not selected for "
                            "significance, and the zoo has them."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def bh(self):
        rows = [cmath(r"\hat k", r"=", r"\max\{k : p_{(k)} \le qk/m\},\quad \text{reject } p_{(1)}, \dots, p_{(\hat k)}", font_size=30,
                      colors={r"\hat k": HURDLE}),
                cmath(r"\mathrm{FDR}", r"=", r"\mathbb E\Big[\frac{V}{\max(R, 1)}\Big] = \sum_{i \in H_0}\sum_k \frac1k\Pr\big(p_i "
                      r"\le \tfrac{qk}{m},\ R = k\big)", font_size=28, colors={r"\mathrm{FDR}": FALSE}),
                cmath(r"\mathrm{FDR}", r"=", r"\frac{m_0}{m}\,q = \pi_0\,q", font_size=34, colors={r"\mathrm{FDR}": FALSE})]
        whys = [why(r"Benjamini and Hochberg (1995): sort the $m$ p-values and reject up to the last one under the line "
                    r"$qk/m$"),
                why(r"write the false discovery proportion as a sum over true nulls $i$ and the number of rejections $k$"),
                why(r"for independent tests, conditioning on the other p-values, each null contributes exactly $q/m$, so "
                    r"the rate is $\pi_0 q$: below $q$ by the share of true nulls. Knowing $\pi_0$ would let one reject more")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "First, why the rule works. <bookmark mark='a'/> Sort the p-values and reject everything up to the last "
            "one below the line q k over m. <bookmark mark='b'/> Write the expected false discovery proportion as a "
            "sum over the true nulls and the number of rejections. <bookmark mark='c'/> For independent tests, "
            "conditioning on the others, each true null contributes exactly q over m. So the rate is the share of true "
            "nulls times q: below the target by exactly that share. If we knew the share, we could afford to reject "
            "more."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def proof(self):
        rows = [cmath(r"R^{(i)}", r"=", r"\text{the number BH rejects when } p_i \text{ is replaced by } 0", font_size=30,
                      colors={r"R^{(i)}": HURDLE}),
                cmath(r"\{p_i \le \tfrac{qk}{m},\ R = k\}", r"=", r"\{p_i \le \tfrac{qk}{m}\} \cap \{R^{(i)} = k\}", font_size=30,
                      colors={r"\{p_i \le \tfrac{qk}{m},\ R = k\}": FALSE}),
                cmath(r"\sum_k \frac1k \Pr(\cdot)", r"=", r"\sum_k \frac1k\,\frac{qk}{m}\Pr\big(R^{(i)} = k\big) = \frac{q}{m}",
                      font_size=30, colors={r"\sum_k \frac1k \Pr(\cdot)": FALSE})]
        whys = [why(r"a function of the other $m - 1$ p-values only, so independent of $p_i$"),
                why(r"if $p_i$ is rejected, setting it to zero changes nothing: the same $k$ hypotheses are rejected"),
                why(r"independence and $p_i \sim U(0,1)$ factor the probability; the $k$'s cancel and $\sum_k \Pr(R^{(i)} = k) = 1$. "
                    r"Summing over the $m_0$ nulls gives $\pi_0 q$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The key step deserves a line of its own. <bookmark mark='a'/> Let R i be the number of rejections when the "
            "i-th p-value is replaced by zero. It depends only on the other p-values, so it is independent of this one. "
            "<bookmark mark='b'/> If the i-th null is rejected with k rejections in all, then setting its p-value to zero "
            "changes nothing: the same k are rejected. So the event splits into two independent pieces. "
            "<bookmark mark='c'/> A uniform p-value falls below q k over m with probability q k over m. The k's cancel, "
            "the probabilities of R i sum to one, and each null contributes q over m. Sum over the nulls, and the rate "
            "is the null share times q. Under dependence the argument breaks at the factoring step, which is where "
            "Benjamini and Yekutieli's correction comes in."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def storey(self):
        rows = [cmath(r"p \mid H_0", r"\sim", r"U(0, 1),\qquad p \mid H_1\ \text{concentrated near } 0", font_size=30,
                      colors={r"p \mid H_0": NOISE}),
                cmath(r"\hat\pi_0(\lambda)", r"=", r"\frac{\#\{p_i > \lambda\}}{m(1 - \lambda)}", font_size=34,
                      colors={r"\hat\pi_0(\lambda)": HURDLE}),
                cmath(r"\mathbb E\,\hat\pi_0(\lambda)", r"\ge", r"\pi_0", font_size=34, colors={r"\mathbb E\,\hat\pi_0(\lambda)": HURDLE})]
        whys = [why(r"true nulls spread p-values evenly; real effects pile them up near zero"),
                why(r"Storey (2002): far from zero the histogram is mostly nulls, so count them there and scale by the "
                    r"width"),
                why(r"conservative: weak real effects also leave some p-values above $\lambda$, so the estimate errs high")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "How to estimate that share? <bookmark mark='a'/> True nulls spread their p-values evenly between zero and "
            "one; real effects pile theirs up near zero. <bookmark mark='b'/> John Storey's estimator, from 2002: count "
            "the p-values above some lambda, where nearly all are nulls, and scale by the width. <bookmark mark='c'/> "
            "It errs high, because weak real effects leave some p-values out there too: a conservative estimate."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def sim(self, t):
        hx = [-4.0, -1.4, 1.0, 3.4, 5.6]
        head = VGroup(label(r"true share of nulls", font_size=18, color=GREY_B), label(r"BH's FDR, realized", font_size=19, color=FALSE),
                      label(r"$\pi_0 q$", font_size=20), label(r"Storey's $\hat\pi_0$", font_size=19, color=HURDLE),
                      label(r"power", font_size=19, color=TRUE))
        tab = VGroup(head)
        for s_ in t["sims"]:
            tab.add(VGroup(MathTex(rf"{s_['pi0']:.1f}", font_size=26), MathTex(rf"{s_['fdr']:.3f}", font_size=26),
                           MathTex(rf"{s_['fdr_bound']:.3f}", font_size=26),
                           MathTex(rf"{s_['pi0_hat']:.2f} \pm {s_['pi0_hat_sd']:.2f}", font_size=26),
                           MathTex(rf"{100 * s_['power']:.0f}\%", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.4 - 0.75 * j, 0])
        foot = wrapped_label(rf"{t['m']} independent one-sided tests, 400 replications per row; real effects with mean "
                             r"$t$ drawn from a gamma (mean 2); BH at $q = 10\%$; Storey with $\lambda = \frac12$", 11.4, 16,
                             GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Check both on simulated zoos of the same size. <bookmark mark='a'/> Benjamini and Hochberg's realized false "
            "discovery rate lands on the share of nulls times q, row after row, as the theorem says. "
            "<bookmark mark='b'/> Storey's estimate sits above the truth each time, by four to fourteen points, more when "
            "real effects are many and weak: conservative, as promised, with a spread of six or seven points."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1], r_[2])) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[3], r_[4])) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def histograms(self, t):
        panels = VGroup()
        n_in = len(t["t_in"])
        for k, (key, title, col, top, ticks) in enumerate((("p_in_hist", r"in-sample $t$: selected for significance", FALSE,
                                                             200, [0, 100, 200]),
                                                            ("p_post_hist", r"post-publication $t$: not selected", TRUE, 60,
                                                             [0, 30, 60]))):
            h = np.asarray(t[key], float)
            g = axes([0, 1], [0, top], x_length=5.2, y_length=3.0, xlabel=r"one-sided p-value", ylabel=title,
                     xticks=[0, 0.5, 1], yticks=ticks, font_size=14)
            ax = g.ax
            bars = VGroup()
            for i, c in enumerate(h):
                p0, p1 = ax.c2p(i / 20, 0), ax.c2p((i + 1) / 20, max(min(c, top), 0.005 * top))
                bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                                   fill_opacity=0.85).move_to((p0 + p1) / 2))
            lev = t["m"] / 20 * t["pi0"] if k else n_in / 20 * t["pi0_in"]
            flat = DashedLine(ax.c2p(0, lev), ax.c2p(1, lev), color=HURDLE, stroke_width=2)
            panels.add(VGroup(g, bars, flat))
        panels.arrange(RIGHT, buff=0.8).move_to(UP * 0.4)
        foot = wrapped_label(rf"the zoo's anomalies (Chapter 3's open-source replication: {n_in} in sample, {t['m']} with a "
                             rf"post-publication record); dashed: the null level "
                             rf"implied by Storey's estimate, $\hat\pi_0 = {t['pi0_in']:.2f}$ in sample and {t['pi0']:.2f} after "
                             r"publication ($\lambda = \frac12$; across $\lambda$ from 0.05 to 0.9 the post-publication estimate "
                             r"runs from 0.75 to 0.14)", 11.6, 16, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Now the zoo. <bookmark mark='a'/> The in-sample p-values are useless for this: the anomalies were "
            "published because they were significant, so almost all sit below five percent, and Storey's estimate "
            f"would say only {100 * t['pi0_in']:.0f} percent are null. Selection did that. <bookmark mark='b'/> The "
            "post-publication p-values were never selected. Their histogram has a pile near zero and a flat right side, "
            f"and Storey's estimate of the share of nulls is about {100 * t['pi0']:.0f} percent. The estimate moves with "
            "lambda, falling as lambda rises, but it errs high at every lambda; so, by that count, at least six in ten "
            "published anomalies still earn something after publication."
        ) as vo:
            self.play(FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
        self.wait(0.4)
        self.clear_scene()

    def lam_curve(self, t):
        lam = np.asarray(t["lams"])
        pc = np.asarray(t["pi0_curve"])
        g = axes([0, 1], [0, 1], x_length=7.4, y_length=4.2, xlabel=r"$\lambda$, where the count starts",
                 ylabel=r"Storey's $\hat\pi_0(\lambda)$, post-publication $p$-values", xticks=[0, 0.25, 0.5, 0.75, 1],
                 yticks=[0, 0.25, 0.5, 0.75, 1], font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        c = curve(ax, lam, pc, HURDLE, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.05, color=HURDLE) for x, y in zip(lam, pc)])
        half = DashedLine(ax.c2p(0.5, 0), ax.c2p(0.5, t["pi0"]), color=GREY_B, stroke_width=2)
        side = VGroup(
            wrapped_label(r"if null $p$-values were exactly uniform, and every real effect sat near $p = 0$, the curve would "
                          r"flatten at $\pi_0$", 3.9, 16, GREY_A),
            wrapped_label(rf"instead it keeps falling: from {pc[0]:.2f} at $\lambda = 0.05$ to {pc[-1]:.2f} at 0.9. The far right "
                          r"($t < -1.3$ after publication) is thinner than uniform: many ``nulls'' may "
                          r"keep a small positive effect", 3.9,
                          16, GREY_A),
            wrapped_label(r"Storey and Tibshirani (2003) smooth the curve and read it near $\lambda = 1$; Storey, Taylor and "
                          r"Siegmund (2004) pick $\lambda$ by bootstrap. At the far right only a handful of $p$-values remain",
                          3.9, 16, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "The choice of lambda matters here. <bookmark mark='a'/> If the null p-values were exactly uniform, and all "
            "the real effects sat near zero, the estimate would flatten out at the true share as lambda grew. "
            f"<bookmark mark='b'/> Instead it keeps falling, from {pc[0]:.2f} near zero to {pc[-1]:.2f} at nine tenths. "
            "The far right of the histogram, anomalies that reversed after publication, is thinner than a uniform "
            "would give. That suggests the nulls are not all exact zeros: many decayed anomalies may keep a small positive "
            "effect. "
            "<bookmark mark='c'/> Storey and Tibshirani smooth the curve and read it near one; a bootstrap can choose "
            "lambda instead. Out at the far right, though, only a handful of p-values remain, so the half-way estimate "
            "is the safer one to report."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(dots), FadeIn(half), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def lfdr(self):
        rows = [cmath(r"f(z)", r"=", r"\pi_0\,\varphi(z) + (1 - \pi_0)\,f_1(z)", font_size=34, colors={r"f(z)": HURDLE}),
                cmath(r"\operatorname{lfdr}(z)", r"=", r"\Pr(H_0 \mid z) = \frac{\pi_0\,\varphi(z)}{f(z)}", font_size=34,
                      colors={r"\operatorname{lfdr}(z)": FALSE}),
                cmath(r"\mathbb E[\#\text{true effects}]", r"=", r"\sum_i \big(1 - \operatorname{lfdr}(z_i)\big)", font_size=32,
                      colors={r"\mathbb E[\#\text{true effects}]": TRUE})]
        whys = [why(r"Efron's two-group model: each $t$-statistic $z$ is a null (standard normal) or a real effect, with "
                    r"unknown density $f_1$; the mixture $f$ is estimated directly from the data"),
                why(r"Bayes's rule: the posterior probability that this particular anomaly is a null"),
                why(r"and the expected number of real effects in the zoo, without choosing any threshold")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Bradley Efron's two-group model goes one step further. <bookmark mark='a'/> Each t-statistic is either a "
            "null, standard normal, or a real effect with some unknown distribution; the mixture density is estimated "
            "directly from the data. <bookmark mark='b'/> By Bayes's rule, the probability that this particular anomaly "
            "is a null is the null share times the normal density, over the mixture density: the local false discovery "
            "rate. <bookmark mark='c'/> Summing one minus it counts the expected number of real effects, without any "
            "threshold at all."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def density(self, t):
        z = np.asarray(t["density_z"])
        g = axes([-4, 7], [0, 0.36], x_length=8.2, y_length=4.2, xlabel=r"post-publication $t$-statistic, in the published "
                 r"direction", ylabel=r"density", xticks=[-4, -2, 0, 2, 4, 6], yticks=[0, 0.1, 0.2, 0.3], font_size=15).move_to(
            LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        f = curve(ax, z, t["density_f"], WHITE, stroke_width=3)
        n0 = curve(ax, z, t["density_null"], NOISE, stroke_width=3)
        tp = np.asarray(t["t_post"])
        lf = np.asarray(t["lfdr"])
        rug = VGroup(*[Line(ax.c2p(x, 0), ax.c2p(x, 0.015), color=TRUE if l_ < 0.2 else FALSE, stroke_width=1.5)
                       for x, l_ in zip(tp, lf) if -4 < x < 7])
        leg = legend([(WHITE, r"mixture $f$, kernel estimate"), (NOISE, r"$\hat\pi_0\,\varphi$: the nulls' share"),
                      (TRUE, r"anomalies with $\operatorname{lfdr} < 0.2$"), (FALSE, r"the rest")], font_size=16).to_edge(
            RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"{t['n_lfdr_02']} of {t['m']} anomalies have a local false discovery rate below 0.2; the "
                             rf"expected number of real effects is {t['expected_true']:.0f}; the strongest after publication: "
                             rf"{t['best'][0]['name']}, {t['best'][1]['name']}, {t['best'][2]['name']}", 3.3, 14,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here is the zoo through that lens. <bookmark mark='a'/> The white curve is the estimated mixture of "
            "post-publication t-statistics; the grey one is the nulls' share of it. <bookmark mark='b'/> Where white "
            f"towers over grey, an anomaly is probably real: {t['n_lfdr_02']} of them have a local false discovery rate "
            f"below one in five. Summing over all of them, the expected number of real effects is about "
            f"{t['expected_true']:.0f}, most of them small, sitting in the overlap where no single test can pick them "
            "out."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(f), Create(n0), FadeIn(leg[0]), FadeIn(leg[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rug), FadeIn(leg[2]), FadeIn(leg[3]))
        self.wait(0.4)
        self.clear_scene()

    def verdict(self, t):
        rows = [(r"anomalies tested after publication", rf"{t['m']}"),
                (r"Benjamini--Hochberg at 10\%", rf"{t['bh10']}"),
                (r"the same, with Storey's $\hat\pi_0$ (rejecting at $q/\hat\pi_0$)", rf"{t['storey_bh10']}"),
                (r"local false discovery rate below 0.2", rf"{t['n_lfdr_02']}"),
                (r"expected number of real effects, $\sum(1 - \operatorname{lfdr})$", rf"{t['expected_true']:.0f}")]
        tab = VGroup()
        for j, (a_, v) in enumerate(rows):
            r_ = VGroup(label(a_, font_size=20, color=GREY_A), MathTex(v, font_size=30, color=TRUE if j else WHITE))
            r_[0].move_to([-1.6, 1.9 - 0.75 * j, 0]).align_to(np.array([-6.2, 0, 0]), LEFT)
            r_[1].move_to([5.0, 1.9 - 0.75 * j, 0])
            tab.add(r_)
        foot = wrapped_label(r"the counts answer different questions: which anomalies one would bet are real (BH, lfdr), and "
                             r"how many real effects the zoo contains (the sum). Jensen, Kelly and Pedersen (2023) read "
                             r"the evidence as most factors replicating; Harvey, Liu and Zhu (2016) as a call for "
                             r"higher hurdles. Both fit these numbers", 11.4, 16, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Put the numbers side by side. <bookmark mark='a'/> Benjamini and Hochberg at ten percent pick out "
            f"{t['bh10']}. Knowing that only about {100 * t['pi0']:.0f} percent are null lets the same guarantee pick "
            f"{t['storey_bh10']}. <bookmark mark='b'/> The local rule picks {t['n_lfdr_02']}, and the zoo as a whole "
            f"contains about {t['expected_true']:.0f} real effects. <bookmark mark='c'/> They answer different questions: "
            "which anomalies you would bet on, and how many real effects exist. Most of the zoo is probably real, and "
            "most of the real effects are small."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: dependence", r"anomalies share stocks and factors; BH remains valid under positive "
                          r"dependence (Benjamini and Yekutieli 2001), but $\hat\pi_0$ and lfdr estimates become noisier, and "
                          r"their standard errors under realistic dependence are not settled", width=12.4, font_size=18),
            desk_question(r"open: decay versus falsehood", r"a post-publication $t$ near zero may mean the anomaly was never "
                          r"real or was arbitraged away (McLean and Pontiff 2016); the two-group model cannot tell them "
                          r"apart", width=12.4, font_size=18),
            desk_question(r"open: discoveries that matter economically", r"a real effect of 1 bp a month is a discovery "
                          r"and worthless after costs; testing against an economically meaningful null is rare", width=12.4,
                          font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> Anomalies share stocks and factors. The step-up rule survives "
            "positive dependence, but the share-of-nulls and local estimates become noisier, and their standard errors "
            "under realistic dependence are not settled. <bookmark mark='b'/> A post-publication t near zero may mean "
            "the anomaly was never real, or that it was traded away; this model cannot tell the two apart. "
            "<bookmark mark='c'/> And a real effect of a basis point a month is a discovery and worthless after costs; "
            "testing against an economically meaningful null is rare."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"of 1{,}000 tests, 380 p-values exceed 0.5. Estimate $\pi_0$. If BH at 10\% rejects 120, about how "
                       r"many of those are false discoveries?")
        with self.voiceover(
            "Pause and predict. Of a thousand tests, three hundred and eighty p-values are above one half. Estimate the "
            "share of nulls. If the step-up rule at ten percent rejects a hundred and twenty, about how many of those "
            "are false?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
