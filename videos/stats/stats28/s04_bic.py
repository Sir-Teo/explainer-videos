from __future__ import annotations

import numpy as np

from videos.stats.stats28.common import *  # noqa: F403


class BIC(VoiceoverScene):
    def construct(self):
        self.card()
        self.derivation()
        self.unit_info()
        self.bench()
        self.consistent()
        self.efficient()
        self.plateau()
        self.choose()

    def card(self):
        card = chapter_card(3, r"BIC", r"Consistency against efficiency", lit=(1978,), part=PART)
        with self.voiceover("Chapter three. The Bayesian information criterion."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def derivation(self):
        rows = [
            cmath(r"p(y \mid M)", r"=", r"\textstyle\int e^{\ell(\theta)}\, p(\theta)\, d\theta", font_size=30),
            cmath(r"", r"\approx", r"e^{\ell(\hat\theta)}\, p(\hat\theta)\, (2\pi)^{k/2} |I_n(\hat\theta)|^{-1/2}", font_size=30),
            cmath(r"|I_n|", r"=", r"n^k |I_1|: \ \ \log p(y \mid M) = \ell(\hat\theta) - \tfrac k2 \log n + O(1)", font_size=28),
            cmath(r"\text{BIC}", r"=", r"-2\ell(\hat\theta) + k \log n", font_size=34),
        ]
        rows[3][2].set_color(BICC)
        whys = [why(r"the evidence, \ Part 26"), why(r"Laplace's method at the MLE"), why(r"the information grows like $n$"),
                why(r"Schwarz (1978): \ drop the $O(1)$")]
        with self.voiceover(
            "<bookmark mark='a'/> BIC comes from Bayes, not from prediction. The evidence for a model, Part 26's marginal "
            "likelihood, is the likelihood integrated against the prior. <bookmark mark='b'/> Laplace's method at the "
            "maximum gives the maximized likelihood times the prior there times a volume factor, two pi to the k over two "
            "over the square root of the determinant of the information. <bookmark mark='c'/> The information grows like n, "
            "so its determinant grows like n to the k, and the log evidence is the maximized log likelihood minus k over two "
            "log n, plus terms that don't grow. <bookmark mark='d'/> Gideon Schwarz dropped those terms: minus twice it is "
            "BIC, whose penalty per parameter is log n rather than two."
        ) as vo:
            intro=label('Regular Laplace evidence has a leading dimension penalty',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bench(self):
        d = load("prostate")
        crit = d["crit"]
        n = d["n_train"]
        mis = [c["aic"] - 2 * (c["size"] + 2) for c in crit]
        k = [c["size"] + 2 for c in crit]
        Bn = CriterionBench(mis, k, [str(c["size"]) for c in crit], penalty_per_k=2.0, width=7.6, height=4.2,
                            center=[-2.0, 0.4, 0], y_max=70, colors={"misfit": TRAIN, "penalty": AICC, "total": PATH})
        nb = Bn.bars(float(np.log(n)))
        for b in nb.pen:
            b.set_fill(BICC)
        xl = label(r"predictors in the best subset of each size", font_size=22, color=GREY_A).next_to(Bn.names, DOWN, buff=0.2)
        ba, bb = crit[Bn.stack.best], crit[nb.best]
        rows = fit_rows(VGroup(
            label(rf"blue: \ AIC, \ 2 per parameter: \ chooses {ba['size']}", font_size=22, color=AICC),
            label(rf"purple: \ BIC, \ $\log {n} = {np.log(n):.2f}$ per parameter", font_size=22, color=BICC),
            label(rf"BIC chooses {bb['size']}: \ {', '.join(bb['subset'])}", font_size=22, color=PATH),
            label(r"the same data, \ two answers", font_size=22, color=RES),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Back on the bench, AIC chose seven predictors. <bookmark mark='b'/> With sixty-seven men, "
            "BIC charges log sixty-seven, four point two, per parameter, more than twice AIC's price. <bookmark mark='c'/> Its "
            "total is smallest at two predictors: cancer volume and prostate weight. <bookmark mark='d'/> The same data, two "
            "respectable criteria, and models of seven and two predictors. The difference is not a technicality: they are "
            "trying to do different things."
        ) as vo:
            self.add(prostate_tag())
            self.add(Bn, xl)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Transform(Bn.stack.pen, nb.pen), Transform(Bn.stack.dots, nb.dots), Transform(Bn.stack.ring, nb.ring),
                      FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(Bn.stack.ring, scale_factor=1.4), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def consistent(self):
        d = load("consistency")["select"]
        ns = np.asarray(d["ns"], float)
        A = axes([1, 3.6], [0, 1], x_length=7.4, y_length=4.2, xlabel=r"sample size $n$ \ (log scale)",
                 ylabel=r"P(choose the true degree, 2)", xticks=[1, 2, 3], yticks=[0, 0.5, 1], xfmt=lambda v: f"10^{{{int(v)}}}",
                 center=[-2.0, 0.3, 0])
        ax = A.ax
        lines = {c: polyline(ax, np.log10(ns), d[c], col, 3) for c, col in (("aic", AICC), ("bic", BICC))}
        dots = {c: VGroup(*[Dot(ax.c2p(np.log10(a), b), radius=0.06, color=col) for a, b in zip(ns, d[c])])
                for c, col in (("aic", AICC), ("bic", BICC))}
        rows = fit_rows(VGroup(
            label(r"truth: \ a quadratic; \ candidates: \ degrees 0--6", font_size=22),
            label(rf"BIC: \ {100 * d['bic'][-1]:.0f}\% right at $n = 3{{,}}000$: \ consistent", font_size=22, color=BICC),
            label(rf"AIC: \ stuck near {100 * np.mean(d['aic'][3:]):.0f}\%: \ overfits for ever", font_size=22, color=AICC),
            label(r"AIC's 2 is fixed; \ $\log n$ grows", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> First, when the truth is among the candidates: data from a quadratic, polynomials "
            "of degree zero to six, three hundred data sets at each sample size. <bookmark mark='b'/> BIC's chance of"
            " picking degree two climbs to ninety-nine percent: it is consistent. <bookmark mark='c'/> AIC's stalls "
            "around three quarters, however much data arrives: a quarter of the time it adds a superfluous term. "
            "<bookmark mark='d'/> Its fixed penalty of two is beaten, now and then, by noise; for a fixed regular "
            "candidate list containing the identifiable truth, BIC's growing penalty yields model-selection "
            "consistency."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(lines["bic"]), FadeIn(dots["bic"]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(lines["aic"]), FadeIn(dots["aic"]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def efficient(self):
        d = load("consistency")["risk"]
        hdr = [r"\textbf{$n$}", r"\textbf{risk, \ AIC's choice}", r"\textbf{AICc's}", r"\textbf{BIC's}"]
        body = [[f"{n:,}", f"{a:.4f}", f"{c:.4f}", f"{b:.4f}"] for n, a, c, b in zip(d["ns"], d["aic"], d["aicc"], d["bic"])]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.32, colors=[GREY_A] + [None] * 3)
        for r in tb[1:]:
            r[1].set_color(AICC)
            r[2].set_color(HIT)
            r[3].set_color(BICC)
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"truth: \ $\sin(2x)e^{0.3x}$, \ not a polynomial; \ candidates: \ degrees 0--12", font_size=22),
            label(r"this finite experiment: \ performance depends on sample size and approximation error", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Second, when no candidate is true: a smooth curve that is not a polynomial, "
            "approximated by polynomials up to degree twelve, and judged by prediction risk. <bookmark mark='b'/> "
            "With a thousand points, AIC's choices predict fifteen percent better than BIC's: this finite experiment "
            "favours AIC at that sample size. It does not establish an asymptotic efficiency theorem for the fixed "
            "list of degrees zero through twelve. <bookmark mark='c'/> With fifty points, plain AIC's licence to fit "
            "degree-twelve polynomials is a disaster, and AICc repairs most of it. Yuhong Yang studied a tradeoff "
            "between model-identification consistency and uniform risk adaptation. That result has a specific scope; "
            "it is not a ban on every criterion being both consistent and prediction-efficient in a finite regular "
            "candidate list."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tb[3]), FadeIn(tb[2]))
            vo.wait_until("c")
            self.play(FadeIn(tb[1]), FadeIn(foot[1]))
        self.clear_scene()

    def choose(self):
        rows = fit_rows(VGroup(
            label(r"want the true model, \ believe it is among the candidates: \ BIC", font_size=24, color=BICC),
            label(r"want predictions, \ truth more complex than any candidate: \ AIC or AICc, \ or CV", font_size=24, color=AICC),
            label(r"neither tells you the chosen model is right", font_size=24, color=RES),
            label(r"neither makes the chosen model's $p$-values honest \ (chapter nine)", font_size=24, color=RES),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So: if you want to identify the true model and believe it is among your candidates, BIC. "
            "<bookmark mark='b'/> If you want good predictions and suspect the truth is more complex than any candidate, as "
            "it usually is, AIC, AICc or cross-validation. <bookmark mark='c'/> Neither tells you the chosen model is right, "
            "<bookmark mark='d'/> and neither makes its p-values honest, Freedman's lesson, which chapter nine takes up."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def plateau(self):
        rows = [
            cmath(r"\text{AIC prefers } M_{k+1}", r"\iff", r"2(\ell_{k+1} - \ell_k) > 2", font_size=30),
            cmath(r"M_k \text{ true}", r":", r"2(\ell_{k+1} - \ell_k) \to \chi^2_1", font_size=30),
            cmath(r"P(\text{overfit by one})", r"\to", r"P(\chi^2_1 > 2) = 0.157", font_size=32),
            cmath(r"\text{BIC}", r":", r"P(\chi^2_1 > \log n) \to 0", font_size=32),
        ]
        rows[2][2].set_color(AICC)
        whys = [why(r"for nested models, \ one extra parameter"), why(r"Wilks, \ Part 22"),
                why(r"a likelihood-ratio test at level 0.157"), why(r"the threshold grows: \ consistency")]
        with self.voiceover(
            "<bookmark mark='a'/> Why AIC plateaus. For two nested models differing by one parameter, AIC prefers the larger "
            "exactly when twice the log likelihood gain exceeds two. <bookmark mark='b'/> If the smaller model is true, that "
            "statistic is, by Part 22's Wilks theorem, chi-squared with one degree of freedom. <bookmark mark='c'/> So AIC "
            "picks the superfluous parameter with probability tending to fifteen point seven percent, whatever n is: it is a "
            "likelihood-ratio test at level point one five seven. With several superfluous degrees on offer, Ritei Shibata "
            "computed the limiting chances, and they match the plateau. <bookmark mark='d'/> BIC's threshold is log n, which "
            "grows, so its chance of overfitting goes to zero."
        ) as vo:
            intro=label('A fixed pair of nested regular models gives a 0.157 limit',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def unit_info(self):
        rows = [
            cmath(r"\text{BIC's } O(1)", r":", r"\log p(\hat\theta) + \tfrac k2 \log 2\pi - \tfrac12 \log|I_1|", font_size=28),
            cmath(r"\theta \sim N(\hat\theta, I_1^{-1})", r":", r"\text{the unit-information prior}", font_size=30),
            cmath(r"\text{then}", r":", r"\log p(y \mid M) = -\tfrac12 \text{BIC} + O(n^{-1/2})", font_size=30),
            cmath(r"e^{-\Delta \text{BIC}/2}", r"\approx", r"\text{the Bayes factor}", font_size=32),
        ]
        rows[3][2].set_color(BICC)
        whys = [why(r"what Schwarz threw away"), why(r"a prior worth one observation"), why(r"Kass \& Wasserman (1995)"),
                why(r"under that prior, \ Part 26's evidence")]
        with self.voiceover(
            "<bookmark mark='a'/> What did Schwarz throw away? The dropped constant involves the prior at the "
            "estimate and the information per observation. <bookmark mark='b'/> Robert Kass and Larry Wasserman "
            "noticed that for one particular prior, a normal centred at the estimate with the information of a single"
            " observation, the unit-information prior, <bookmark mark='c'/> in a regular setting those leading "
            "constants cancel. Centering this illustrative prior at the estimate uses the data; it is not a uniquely "
            "prescribed fixed prior or an automatic Bayes-factor guarantee. <bookmark mark='d'/> So the exponentiated"
            " difference in BIC approximates a Bayes factor under a prior worth one data point: diffuse, and so, by "
            "Part 26's Lindley paradox, kind to small models."
        ) as vo:
            intro=label('Prior and curvature constants matter in a BIC approximation',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
