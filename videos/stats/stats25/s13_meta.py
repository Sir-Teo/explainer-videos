from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats25.common import *  # noqa: F403


class Meta(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.forest()
        self.heterogeneity()
        self.shrunk()
        self.hk()
        self.board()
        self.cautions()

    def card(self):
        card = chapter_card(12, r"Meta-analysis", r"Studies as a sample of studies", lit=(1986,), part=PART)
        with self.voiceover("Chapter twelve. Meta-analysis."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def model(self):
        rows = [
            cmath(r"y_k", r"\sim", r"N(\theta_k, v_k), \ \ v_k \text{ known from study } k", font_size=30),
            cmath(r"\text{common effect}", r":", r"\theta_k = \mu: \ \hat\mu = \textstyle\sum w_k y_k / \sum w_k, \ w_k = 1/v_k", font_size=28),
            cmath(r"\text{random effects}", r":", r"\theta_k \sim N(\mu, \tau^2): \ w_k = 1/(v_k + \tau^2)", font_size=28),
            cmath(r"\hat\tau^2_{DL}", r"=", r"\max\Bigl\{0, \ \dfrac{Q - (K - 1)}{\sum w_k - \sum w_k^2/\sum w_k}\Bigr\}", font_size=28),
        ]
        rows[2][2].set_color(SHRUNK)
        whys = [why(r"each study reports an estimate and its SE"), why(r"inverse-variance weights"),
                why(r"Fay--Herriot again, \ with studies for towns"), why(r"DerSimonian \& Laird (1986): \ moments of Cochran's $Q$")]
        intro = label('A working probability model states the assumptions behind shrinkage', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Meta-analysis combines studies, each reporting an estimate and its standard error. "
            "<bookmark mark='b'/> If every study estimates the same effect, the best combination weights each by its inverse "
            "variance. <bookmark mark='c'/> But studies differ in their populations and protocols, so their true effects "
            "vary around a mean with variance tau squared: the random-effects model, which is Fay–Herriot with studies in "
            "place of towns. <bookmark mark='d'/> Rebecca DerSimonian and Nan Laird's 1986 estimator of tau squared matches "
            "Cochran's heterogeneity statistic Q to its expectation, a method of moments."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def forest(self):
        d = load("meta")
        y, v, r = np.asarray(d["y"]), np.asarray(d["v"]), d["res"]
        K = len(y)
        A = axes([-0.8, 1.0], [-2.2, K + 0.6], x_length=7.6, y_length=5.0, xlabel=r"effect", ylabel=r"",
                 xticks=[-0.5, 0, 0.5, 1.0], yticks=[], center=[-1.4, 0.0, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(0, -2.2), ax.c2p(0, K + 0.6), color=GREY_C, stroke_width=1.5)
        studies = VGroup()
        names = VGroup()
        w = 1 / v
        for k in range(K):
            yy = K - k
            se = np.sqrt(v[k])
            ln = Line(ax.c2p(y[k] - 1.96 * se, yy), ax.c2p(y[k] + 1.96 * se, yy), color=RAW, stroke_width=3)
            sq = Square(side_length=0.12 + 0.25 * np.sqrt(w[k] / w.max()), stroke_width=0, fill_color=RAW, fill_opacity=1).move_to(ax.c2p(y[k], yy))
            studies.add(VGroup(ln, sq))
            names.add(label(rf"study {k + 1}", font_size=20, color=GREY_A).next_to(ax.c2p(-0.8, yy), LEFT, buff=0.2))

        def diamond(mu, lo, hi, yy, col):
            return Polygon(ax.c2p(lo, yy), ax.c2p(mu, yy + 0.25), ax.c2p(hi, yy), ax.c2p(mu, yy - 0.25), stroke_width=0, fill_color=col, fill_opacity=0.9)

        fe = diamond(r["mu_fe"], r["mu_fe"] - 1.96 * r["se_fe"], r["mu_fe"] + 1.96 * r["se_fe"], -0.3, POOLED)
        dl = diamond(r["mu"], r["ci_dl"][0], r["ci_dl"][1], -1.0, SHRUNK)
        hk = diamond(r["mu"], r["ci_hk"][0], r["ci_hk"][1], -1.7, PATH)
        dn = VGroup(label(r"common", font_size=20, color=POOLED).next_to(ax.c2p(-0.8, -0.3), LEFT, buff=0.2),
                    label(r"DL", font_size=20, color=SHRUNK).next_to(ax.c2p(-0.8, -1.0), LEFT, buff=0.2),
                    label(r"HK", font_size=20, color=PATH).next_to(ax.c2p(-0.8, -1.7), LEFT, buff=0.2))
        truth = DashedLine(ax.c2p(d["truth"], -2.2), ax.c2p(d["truth"], K + 0.6), color=TRUE, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"five simulated trials, \ 95\% intervals", font_size=22, color=RAW),
            label(rf"common effect: \ {r['mu_fe']:.3f} $\pm$ {1.96 * r['se_fe']:.3f}", font_size=22, color=POOLED),
            label(rf"random effects: \ {r['mu']:.3f}, \ [{r['ci_dl'][0]:.2f}, {r['ci_dl'][1]:.2f}]", font_size=22, color=SHRUNK),
            label(rf"Hartung--Knapp: \ [{r['ci_hk'][0]:.2f}, {r['ci_hk'][1]:.2f}]", font_size=22, color=PATH),
            label(rf"gold: \ the true mean effect, \ {d['truth']}", font_size=22, color=TRUE),
        ), 4.0, 0.42, [4.8, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A forest plot of five simulated trials, each square sized by its weight. One study points "
            "the other way. <bookmark mark='b'/> The common-effect estimate is point one one four with a narrow interval. "
            "<bookmark mark='c'/> Allowing heterogeneity, the random-effects estimate is point one three seven, and its "
            "DerSimonian–Laird interval, from minus point one three to point four, is far wider: the trials disagree more "
            "than their standard errors allow. <bookmark mark='d'/> The Hartung–Knapp interval, coming next, is wider still. "
            "<bookmark mark='e'/> The simulation's true mean effect is point three, inside both random-effects intervals but "
            "outside the common-effect one."
        ) as vo:
            self.add(simulated_tag(r"simulated: \ a seeded example"))
            self.play(FadeIn(A), Create(zero), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in studies], lag_ratio=0.2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(fe), FadeIn(dn[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(dl), FadeIn(dn[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(hk), FadeIn(dn[2]), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(Create(truth), FadeIn(rows[4]))
        self.clear_scene()

    def heterogeneity(self):
        d = load("meta")
        r = d["res"]
        K = len(d["y"])
        rows = [
            cmath(r"Q", r"=", rf"\textstyle\sum w_k (y_k - \hat\mu_{{FE}})^2 = {r['Q']:.2f}, \ \ E\,Q = K - 1 = {K - 1} \text{{ if }} \tau = 0", font_size=28),
            cmath(r"\hat\tau^2", r"=", rf"{r['tau2']:.3f}: \ \hat\tau = {np.sqrt(r['tau2']):.2f} \ \ (\text{{truth }} {d['tau']})", font_size=30),
            cmath(r"I^2", r"=", rf"\max\{{0,(Q-K+1)/Q\}} = {r['I2']:.2f}", font_size=30),
            cmath(r"\text{prediction interval}", r":", r"\hat\mu\pm t_{K-2}\sqrt{\hat\tau^2+\mathrm{SE}^2}:\ \text{approximate, next latent effect}", font_size=28),
        ]
        rows[2][2].set_color(SHRUNK)
        whys = [why(r"Cochran (1954)"), why(r"five studies: \ $\tau$ is barely estimable"),
                why(r"Higgins \& Thompson (2002): \ relative heterogeneity of study estimates"), why(r"Higgins, Thompson \& Spiegelhalter (2009)")]
        intro = label('Study heterogeneity and individual-outcome variation are different', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Cochran's Q sums the weighted squared deviations from the common estimate: "
            "seventeen, against four expected if all the studies shared one effect. <bookmark mark='b'/> The "
            "DerSimonian–Laird estimate of tau is point two six, against a true point one five: from five studies, "
            "tau is barely estimable. <bookmark mark='c'/> I squared estimates the relative contribution of "
            "between-study heterogeneity to study-estimate variation, seventy-seven percent here. It is not a share "
            "of individual-outcome variance. <bookmark mark='d'/> And the most useful summary for practice is often "
            "the prediction interval: where the effect in the next study, or the next hospital, might fall under the "
            "same exchangeable study model. With five studies, this plug-in prediction interval is a rough "
            "approximation."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def hk(self):
        rows = [
            cmath(r"\text{DL}", r":", r"\hat\mu \pm 1.96\,\bigl(\textstyle\sum \hat w_k\bigr)^{-1/2}", font_size=30),
            cmath(r"\text{trouble}", r":", r"\hat\tau^2 \text{ is noisy, \ and treated as known}", font_size=30),
            cmath(r"\text{HK}", r":", r"\hat\mu \pm t_{K - 1}\,\sqrt{\tfrac{\sum \hat w_k (y_k - \hat\mu)^2}{(K - 1)\sum \hat w_k}}", font_size=30),
            cmath(r"\text{why}", r":", r"\text{the spread of the studies rescales the SE; \ } t \text{ pays for it}", font_size=28),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"a $z$ interval"), why(r"chapter six's problem: \ few groups"),
                why(r"Hartung \& Knapp (2001); \ Sidik \& Jonkman (2002)"), why(r"Satterthwaite's idea, \ for studies")]
        intro = label('Hartung-Knapp uses a residual scale and a t reference', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The DerSimonian–Laird interval is a z interval with the estimated weights. "
            "<bookmark mark='b'/> Its trouble is chapter six's: with few studies, tau squared is noisy, and the "
            "interval treats it as known. <bookmark mark='c'/> Joachim Hartung and Guido Knapp's interval rescales "
            "the standard error by how much the studies actually scatter around the estimate, and uses a t with K "
            "minus one degrees of freedom. <bookmark mark='d'/> It is chapter six's lesson for studies. Unmodified "
            "Hartung–Knapp can still be narrower than a z interval when residual heterogeneity is small; it does not "
            "guarantee coverage in every setting."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=25) if r.part == 25][0:2]
        b = coverage_board(rows, lit_part=25, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> The Board: a thousand meta-analyses of five studies each, with real heterogeneity. The "
            "DerSimonian–Laird interval, still the default in much software, covers the true mean effect eighty-nine percent "
            "of the time: broken. <bookmark mark='b'/> Hartung–Knapp's covers ninety-four: kept. Methodologists, Cochrane's "
            "among them, now advise against relying on DerSimonian–Laird alone when the studies are few."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            for k, m_ in enumerate("ab"):
                vo.wait_until(m_)
                self.play(FadeIn(b.body[k]))
        self.wait(1.0)
        self.clear_scene()

    def cautions(self):
        rows = fit_rows(VGroup(
            label(r"publication bias: \ studies that found nothing stay in drawers", font_size=24, color=RES),
            label(r"the funnel plot: \ small studies should scatter symmetrically", font_size=24),
            label(r"garbage in: \ combining biased studies gives a precise biased answer", font_size=24, color=RES),
            label(r"each study's own effect: \ shrunk towards $\hat\mu$, \ as the hitters were", font_size=24, color=SHRUNK),
            label(r"Part 26: \ the eight schools, \ a meta-analysis done the Bayesian way", font_size=24, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two cautions. Studies that found nothing are less often published, so the "
            "literature overstates effects. <bookmark mark='b'/> Under a common effect and suitable sampling "
            "conditions a funnel plot should be roughly symmetric. Asymmetry can reflect selection, heterogeneity or "
            "other small-study effects; it does not diagnose publication bias alone. <bookmark mark='c'/> And "
            "combining biased studies only produces a precise biased answer. <bookmark mark='d'/> The model also "
            "shrinks each study's own effect towards the mean, as Efron and Morris shrank the hitters. <bookmark "
            "mark='e'/> Part 26 begins with exactly such a meta-analysis, the eight schools, done the Bayesian way."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def shrunk(self):
        d = load("meta")
        y, v, r = np.asarray(d["y"]), np.asarray(d["v"]), d["res"]
        lam = r["tau2"] / (r["tau2"] + v)
        bl = r["mu"] + lam * (y - r["mu"])
        P = ShrinkagePlot(y, bl, None, x_range=(-0.4, 0.5), width=10.4, center=[0.6, 0.6, 0], gap=1.8,
                          labels={"raw": "each study", "shrunk": "shrunk"}, ticks=[-0.4, -0.2, 0, 0.2, 0.4],
                          fmt=lambda v_: f"{v_:.1f}", colors={"raw": RAW, "shrunk": SHRUNK, "truth": TRUE})
        rows = fit_rows(VGroup(
            label(rf"$\lambda_k = \hat\tau^2/(\hat\tau^2 + v_k)$: \ from {lam.min():.2f} to {lam.max():.2f}", font_size=22, color=SHRUNK),
            label(r"precise studies move little; \ the outlier moves most", font_size=22, color=GREY_A),
        ), 12.0, 0.22, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The random-effects model also says what each study's own effect probably was. Each is "
            "shrunk towards the overall mean by its own factor, the heterogeneity over itself plus the study's sampling "
            "variance, here between point six three and point eight five. <bookmark mark='b'/> Precise studies move little, and "
            "the study that pointed the other way is pulled the furthest: Efron and Morris's hitters, as clinical trials."
        ) as vo:
            self.add(simulated_tag(r"simulated: \ a seeded example"))
            self.play(FadeIn(P.lines), FadeIn(P.names), FadeIn(P.ticks), FadeIn(P.raw))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(a) for a in P.arrows], lag_ratio=0.1), LaggedStart(*[FadeIn(x) for x in P.shrunk], lag_ratio=0.1),
                      FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
        self.clear_scene()
