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
        with self.voiceover('For the researcher: exact false-discovery results require explicit null and dependence assumptions. Estimating the share of nulls and local densities adds a mixture model and further uncertainty. We preserve the numerical diagnostics while distinguishing model-conditional statements from identified facts about published anomalies.'):
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
                why('for independent p-values with uniform true-null marginals, each true null contributes q/m exactly. Super-uniform nulls give an upper bound; plug-in null-share estimation needs additional assumptions')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "First state an exact theorem. <bookmark mark='a'/> Apply BH at level q to a fixed family. Assume independent p-values and exactly uniform true-null p-values. <bookmark mark='b'/> Write the expected false-rejection fraction as a sum over true nulls and possible rejection counts, with zero fraction when there are no rejections. <bookmark mark='c'/> Each true null then contributes q over m, giving pi zero times q exactly. Merely valid super-uniform p-values give an upper bound rather than equality. Appropriate positive regression dependence permits a bound, not arbitrary correlation or arbitrary dependence."
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
                why('untruncated expectation bound for uniform nulls, fixed lambda; neither a realised bound nor a clipped-estimator guarantee')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Storey's estimator needs another careful distinction. <bookmark mark='a'/> Under uniform true-null p-values, each null exceeds a fixed lambda with probability one minus lambda. <bookmark mark='b'/> Divide the total count above lambda by m times one minus lambda. For this untruncated estimator the expectation is at least pi zero, because alternatives add nonnegative tail mass. <bookmark mark='c'/> This is an expectation bound, not a guarantee that each realised estimate exceeds truth. Capping at one can change that bound. The saved empirical calculation caps the estimator, and using q over an estimated pi zero does not automatically retain finite-sample FDR control."
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
        head = VGroup(label(r"true share of nulls", font_size=18, color=GREY_B), label('mean FDP over simulations', font_size=19, color=FALSE),
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
            "The preserved simulation uses four hundred replications per row and two hundred and eight independent tests. Non-null effects are gamma distributed, with independent normal observation noise. <bookmark mark='a'/> The average realised false-rejection fraction is close to pi zero times q, with finite simulation error. <bookmark mark='b'/> The displayed untruncated Storey estimates have averages above the generating null shares; their reported spread is across replications. This checks the stated toy model, not dependence-valid error control for published return predictors."
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
                                                            ("p_post_hist", 'post-publication $t$: published universe', TRUE, 60,
                                                             [0, 30, 60]))):
            h = np.asarray(t[key], float)
            g = axes([0, 1], [0, top], x_length=5.2, y_length=3.0, xlabel=r"one-sided p-value", ylabel=title,
                     xticks=[0, 0.5, 1], yticks=ticks, font_size=14)
            ax = g.ax
            bars = VGroup()
            for i, c in enumerate(h):
                p0, p1 = ax.c2p(i / 20, 0), ax.c2p((i + 1) / 20, c)
                bars.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.00001), stroke_width=0, fill_color=col,
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
            "The in-sample histogram inherits significance and publication selection. <bookmark mark='a'/> Applying a uniform-null mixture mechanically produces a very low fitted null share, which is not identified truth. <bookmark mark='b'/> The post-publication returns were not selected on this exact statistic by the original paper, but the predictors, directions, available histories and modern release remain selected. Normal tail probabilities from iid mean t values are not automatically uniform under the null. The capped estimate varies strongly with lambda; it does not prove that a majority of predictors retain real premia."
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
            "The lambda curve is a sensitivity diagnostic. <bookmark mark='a'/> With uniform true nulls and alternatives concentrated near zero, a flat region may be informative. <bookmark mark='b'/> Here the saved capped estimate falls substantially across lambda. Null misspecification, dependence, direction selection, weak effects and finite noise can affect this shape. <bookmark mark='c'/> No realised point is certified to exceed the true null share, and choosing a convenient lambda after seeing the curve introduces another choice. The figure cannot identify a guaranteed minimum fraction of real anomalies."
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
                cmath('\\sum_i\\Pr(H_{1i}\\mid z_i)', r"=", r"\sum_i \big(1 - \operatorname{lfdr}(z_i)\big)", font_size=32,
                      colors={'\\sum_i\\Pr(H_{1i}\\mid z_i)': TRUE})]
        whys = [why(r"Efron's two-group model: each $t$-statistic $z$ is a null (standard normal) or a real effect, with "
                    r"unknown density $f_1$; the mixture $f$ is estimated directly from the data"),
                why(r"Bayes's rule: the posterior probability that this particular anomaly is a null"),
                why('model-conditional expected count for a correctly specified mixture; fitted clipped ratios are heuristic diagnostics')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The two-group mixture is a conditional statistical model. <bookmark mark='a'/> Suppose the null density is standard normal and the mixture density and null share are correctly specified. <bookmark mark='b'/> Bayes's formula then gives the local null probability. The saved example instead plugs in a kernel density and a capped estimated null share, and clips local ratios at one. These plug-ins need not define a coherent identified mixture. <bookmark mark='c'/> Summing one minus the fitted ratios is a model diagnostic; without those assumptions it is not a certified expected count of real economic effects."
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
        g = axes([-4, 10.2], [0, 0.36], x_length=8.2, y_length=4.2, xlabel=r"post-publication $t$-statistic, in the published "
                 r"direction", ylabel=r"density", xticks=[-4, 0, 4, 8, 10], yticks=[0, 0.1, 0.2, 0.3], font_size=15).move_to(
            LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        f = curve(ax, z, t["density_f"], WHITE, stroke_width=3)
        n0 = curve(ax, z, t["density_null"], NOISE, stroke_width=3)
        tp = np.asarray(t["t_post"])
        lf = np.asarray(t["lfdr"])
        rug = VGroup(*[Line(ax.c2p(x, 0), ax.c2p(x, 0.015), color=TRUE if l_ < 0.2 else FALSE, stroke_width=1.5)
                       for x, l_ in zip(tp, lf)])
        leg = legend([(WHITE, r"mixture $f$, kernel estimate"), (NOISE, r"$\hat\pi_0\,\varphi$: the nulls' share"),
                      (TRUE, r"anomalies with $\operatorname{lfdr} < 0.2$"), (FALSE, r"the rest")], font_size=16).to_edge(
            RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(f"{t['n_lfdr_02']} of {t['m']} anomalies have a local false discovery rate below 0.2; the heuristic fitted sum is {t['expected_true']:.0f}; the strongest after publication: {t['best'][0]['name']}, {t['best'][1]['name']}, {t['best'][2]['name']}", 3.3, 14,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Read the density plot as a model-dependent diagnostic. <bookmark mark='a'/> White is the fitted mixture and grey is the estimated null share times a standard-normal density. <bookmark mark='b'/> The coloured rug uses clipped fitted local ratios. The displayed count and sum depend on kernel smoothing, the assumed normal null, the capped null share and the selected published universe. They do not establish how many anomalies are real or what a future implementation will earn."
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
                ('heuristic fitted sum, $\\sum(1-\\widehat{\\operatorname{lfdr}})$', rf"{t['expected_true']:.0f}")]
        tab = VGroup()
        for j, (a_, v) in enumerate(rows):
            r_ = VGroup(label(a_, font_size=20, color=GREY_A), MathTex(v, font_size=30, color=TRUE if j else WHITE))
            r_[0].move_to([-1.6, 1.9 - 0.75 * j, 0]).align_to(np.array([-6.2, 0, 0]), LEFT)
            r_[1].move_to([5.0, 1.9 - 0.75 * j, 0])
            tab.add(r_)
        foot = wrapped_label('different model-dependent diagnostics; selected published universe, approximate nulls, adaptive and kernel plug-ins; no certified count of true effects or future earnings', 11.4, 16, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "These saved numbers answer different conditional questions. <bookmark mark='a'/> BH uses approximate normal p-values, while the adaptive row replaces q with q over a capped estimated null share. That plug-in does not inherit the same finite-sample guarantee automatically. <bookmark mark='b'/> Local-ratio counts and their summed complements additionally depend on a kernel mixture model. <bookmark mark='c'/> Report them as sensitivity diagnostics on a selected published universe. None identifies a certified majority of real factors, controls portfolio loss, or proves an implementable future premium."
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
            desk_question(r"open: dependence", 'anomalies share stocks and factors; BH needs valid nulls and independence or PRDS; arbitrary positive correlation is insufficient, but $\\hat\\pi_0$ and lfdr estimates become noisier, and their standard errors under realistic dependence are not settled', width=12.4, font_size=18),
            desk_question(r"open: decay versus falsehood", r"a post-publication $t$ near zero may mean the anomaly was never "
                          r"real or was arbitraged away (McLean and Pontiff 2016); the two-group model cannot tell them "
                          r"apart", width=12.4, font_size=18),
            desk_question(r"open: discoveries that matter economically", 'a statistically nonzero 1 bp monthly effect may be outweighed by implementation costs; prespecified economic thresholds and capacity matter', width=12.4,
                          font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> Shared stocks create dependence. BH has a bound under valid null p-values and appropriate positive regression dependence, not arbitrary positive correlations. Adaptive null-share and local-density methods need further assumptions. <bookmark mark='b'/> A small post-publication statistic cannot by itself distinguish no original effect from economic decay, changed risk, noise or data revision. <bookmark mark='c'/> Finally, statistical nonzero means are not net economic opportunities. Costs, funding, constraints and a meaningful economic null matter."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card('of 1{,}000 tests, 380 p-values exceed 0.5. Estimate $\\pi_0$. If BH rejects 120 at 10\\%, why is $0.76(0.1)(120)\\approx9$ only a heuristic, not a realised guarantee?')
        with self.voiceover(
            'Pause and predict. Of a thousand p-values, three hundred and eighty exceed one half. Compute the untruncated Storey plug-in estimate. If BH at ten percent rejects one hundred and twenty, multiplying point seven six times point one times one hundred and twenty gives about nine. Explain why that is only a heuristic under an assumed stable mixture, not a realised false-discovery count or a consequence of FDR alone.'
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
