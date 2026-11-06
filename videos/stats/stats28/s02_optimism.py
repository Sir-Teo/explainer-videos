from __future__ import annotations

import numpy as np

from videos.stats.stats28.common import *  # noqa: F403


class Optimism(VoiceoverScene):
    def construct(self):
        self.card()
        self.fits()
        self.curves()
        self.decomp()
        self.theory()
        self.df()
        self.lasso()

    def card(self):
        card = chapter_card(1, r"Optimism", r"Training error flatters", lit=(1986,), part=PART)
        with self.voiceover("Chapter one. Optimism."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def fits(self):
        d = load("optimism")
        x, y, xx = np.asarray(d["x"]), np.asarray(d["y"]), np.asarray(d["xx"])
        A = axes([-1.6, 1.6], [-2.5, 2.5], x_length=7.2, y_length=4.4, xlabel=r"$x$", ylabel=r"$y$", xticks=[-1, 0, 1],
                 yticks=[-2, 0, 2], center=[-2.0, 0.3, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=WHITE) for a, b in zip(x, y)])
        truth = DashedVMobject(curve(ax, xx, d["truth"], TRUE, 2.5), num_dashes=50)
        cs = {k: clip_curve(ax, xx, np.asarray(d["fits"][k]), c, 3, ymin=-2.5, ymax=2.5) for k, c in (("1", AICC), ("3", HIT), ("10", RES))}
        rows = fit_rows(VGroup(
            label(rf"30 points, \ noise SD {d['sigma']}", font_size=22),
            label(r"gold dashed: \ the truth", font_size=22, color=TRUE),
            label(r"blue: \ degree 1", font_size=22, color=AICC),
            label(r"green: \ degree 3", font_size=22, color=HIT),
            label(r"red: \ degree 10: \ closest to these points", font_size=22, color=RES),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The phenomenon in miniature. Thirty noisy points from a smooth curve, <bookmark mark='b'/> "
            "the truth dashed in gold. <bookmark mark='c'/> A straight line misses the bend. <bookmark mark='d'/> A cubic "
            "follows it. <bookmark mark='e'/> A degree-ten polynomial follows the points best of all, chasing their noise, "
            "and its training error is the smallest of the three."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in dots], lag_ratio=0.03), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(rows[1]))
            for k, (key, m_) in enumerate((("1", "c"), ("3", "d"), ("10", "e"))):
                vo.wait_until(m_)
                self.play(Create(cs[key]), FadeIn(rows[k + 2]))
        self.clear_scene()

    def curves(self):
        d = load("optimism")
        degs = np.asarray(d["degs"])
        tr, te = np.asarray(d["train"]), np.asarray(d["test"])
        A = axes([-0.5, 12.5], [0, 1.2], x_length=7.4, y_length=4.4, xlabel=r"polynomial degree", ylabel=r"mean squared error",
                 xticks=[0, 3, 6, 9, 12], yticks=[0, 0.25, 0.5, 1], center=[-2.0, 0.3, 0])
        ax = A.ax
        lt = polyline(ax, degs, tr, TRAIN, 3)
        le = polyline(ax, degs, te, TEST, 3)
        dt = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=TRAIN) for a, b in zip(degs, tr)])
        de = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=TEST) for a, b in zip(degs, te)])
        noise = DashedLine(ax.c2p(-0.5, d["sigma"] ** 2), ax.c2p(12.5, d["sigma"] ** 2), color=GREY_B, stroke_width=1.5)
        rows = fit_rows(VGroup(
            label(r"averaged over 600 data sets", font_size=22),
            label(r"teal: \ training error: \ always falls", font_size=22, color=TRAIN),
            label(r"red: \ error on new $y$ at the same $x$", font_size=22, color=TEST),
            label(r"grey: \ the noise variance, \ 0.25", font_size=22, color=GREY_B),
            label(r"test error: \ about 0.30 from degree 3 to 6, \ then rises", font_size=22, color=TEST),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Average over six hundred data sets. <bookmark mark='b'/> Training error falls with every "
            "added degree, below even the noise variance. <bookmark mark='c'/> Error on new responses at the same x values "
            "falls, <bookmark mark='d'/> bottoms out a little above the noise floor, <bookmark mark='e'/> flat at about point "
            "three from degree three to six, and then climbs as the polynomial starts fitting noise. The gap between the two curves is the optimism of the training error."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(noise))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(lt), FadeIn(dt), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(le), FadeIn(de), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def theory(self):
        d = load("optimism")
        degs = np.asarray(d["degs"])
        gap, th = np.asarray(d["gap"]), np.asarray(d["theory"])
        rows = [
            cmath(r"\text{optimism}", r"=", r"E\,\text{err}_{\text{in}} - E\,\overline{\text{err}}", font_size=30),
            cmath(r"", r"=", r"\dfrac{2}{n}\textstyle\sum_i \mathrm{Cov}(\hat y_i, y_i)", font_size=30),
            cmath(r"\text{linear fit, } d \text{ parameters}", r":", r"2\sigma^2 d/n", font_size=30),
            cmath(r"\text{degree 3}", r":", rf"\text{{simulated }} {gap[3]:.3f}, \ \text{{formula }} {th[3]:.3f}", font_size=30),
        ]
        rows[2][2].set_color(HIT)
        whys = [why(r"new $y$ at the same $x$, \ minus training error"), why(r"Efron (1986): \ fits that copy $y$ are optimistic"),
                why(r"$\sum \mathrm{Cov} = \sigma^2 \mathrm{tr}\,H = \sigma^2 d$"), why(r"every degree matches")]
        with self.voiceover(
            "<bookmark mark='a'/> Bradley Efron made the gap precise. The optimism is the expected in-sample prediction "
            "error minus the expected training error. <bookmark mark='b'/> It equals two over n times the sum of the "
            "covariances between each fitted value and its own observation: a fit that copies its data looks good on that "
            "data. <bookmark mark='c'/> For a linear fit with d parameters, the covariances sum to sigma squared times d, so "
            "the optimism is two sigma squared d over n. <bookmark mark='d'/> At degree three, four parameters, the simulated "
            "gap is point oh six seven, as the formula says, and the same holds at every degree."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def df(self):
        rows = [
            cmath(r"\mathrm{df}(\hat y)", r"=", r"\dfrac{1}{\sigma^2}\textstyle\sum_i \mathrm{Cov}(\hat y_i, y_i)", font_size=32),
            cmath(r"\text{linear smoother } \hat y = Sy", r":", r"\mathrm{df} = \mathrm{tr}\, S", font_size=30),
            cmath(r"\text{Stein's lemma}", r":", r"\mathrm{df} = E\,\textstyle\sum_i \partial \hat y_i/\partial y_i", font_size=30),
            cmath(r"\text{any procedure}", r":", r"\text{simulate, \ and measure the covariance}", font_size=30),
        ]
        rows[0][2].set_color(HIT)
        whys = [why(r"Efron (2004): \ degrees of freedom, \ defined"), why(r"ridge, \ splines, \ kernels: \ Part 29"),
                why(r"Part 25's lemma: \ the divergence of the fit"), why(r"stepwise, \ trees, \ anything")]
        with self.voiceover(
            "<bookmark mark='a'/> That suggests a definition. A procedure's degrees of freedom are the summed covariances "
            "between fitted and observed values, divided by sigma squared: how hard the fit copies the data. "
            "<bookmark mark='b'/> For any linear smoother, a fit of the form S times y, it is the trace of S, the effective "
            "number of parameters of a ridge regression or a spline, Part 29. <bookmark mark='c'/> By Stein's lemma from "
            "Part 25 it is also the expected divergence of the fit. <bookmark mark='d'/> And for any procedure at all, stepwise "
            "selection included, it can be measured by simulation."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lasso(self):
        d = load("lassodf")
        hdr = [r"\textbf{lasso penalty} $\lambda$", r"\textbf{df, \ simulated}", r"\textbf{1 + E(nonzero coefficients)}"]
        body = [[f"{r['lam']:g}", f"{r['df_mc']:.2f}", f"{r['mean_nonzero']:.2f}"] for r in d["rows"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.32, colors=[GREY_A] + [None] * 4)
        for r in tb[1:]:
            r[1].set_color(HIT)
            r[2].set_color(AICC)
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"Stamey's prostate predictors, \ 600 simulated responses at each $\lambda$", font_size=22),
            label(r"Zou, Hastie \& Tibshirani (2007): \ the lasso's df is its number of nonzero coefficients", font_size=22, color=HIT),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A surprising example. Fit the lasso of Part 19 to responses simulated around the prostate "
            "data's eight predictors, at four penalties, and measure its degrees of freedom by the covariance. "
            "<bookmark mark='b'/> They match, to simulation error, one plus the average number of nonzero coefficients. Hui "
            "Zou, Trevor Hastie and Robert Tibshirani proved it: the lasso's search for which coefficients to use costs "
            "nothing extra, because its shrinkage exactly offsets the selection. Best-subset selection, by contrast, costs "
            "more than its count of coefficients."
        ) as vo:
            self.add(prostate_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb[1:]], lag_ratio=0.3), FadeIn(foot[1]))
        self.wait(1.0)
        self.clear_scene()

    def decomp(self):
        rows = [
            cmath(r"E(y_0 - \hat f(x_0))^2", r"=", r"\sigma^2 + \text{bias}^2(x_0) + \mathrm{Var}\,\hat f(x_0)", font_size=30),
            cmath(r"\text{averaged over the } x_i", r":", r"\sigma^2 + \overline{\text{bias}^2} + \sigma^2 d/n", font_size=30),
            cmath(r"\text{training error}", r":", r"\sigma^2 + \overline{\text{bias}^2} - \sigma^2 d/n", font_size=30),
            cmath(r"\text{gap}", r"=", r"2\sigma^2 d/n", font_size=34),
        ]
        rows[3][2].set_color(HIT)
        whys = [why(r"noise, \ bias, \ variance: \ Part 9"), why(r"least squares with $d$ coefficients"),
                why(r"the fit absorbs $d$ dimensions of noise"), why(r"the next scene, \ in general")]
        with self.voiceover(
            "<bookmark mark='a'/> The shape has a simple anatomy. The error of a prediction at a new point is the noise, plus "
            "the squared bias of the fit there, plus its variance, Part 9's decomposition. <bookmark mark='b'/> For least "
            "squares with d coefficients, averaged over the design points, the variance term is sigma squared d over n: it "
            "grows with every coefficient, while the bias falls. <bookmark mark='c'/> The training error has the same noise "
            "and bias, but the fit has absorbed d dimensions of the noise, so it sits sigma squared d over n below the noise "
            "level instead of above. <bookmark mark='d'/> The gap is two sigma squared d over n."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
