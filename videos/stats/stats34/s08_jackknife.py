from __future__ import annotations

import numpy as np

from videos.stats.stats34.common import *  # noqa: F403

METH = {"naive": (r"in-sample residuals", MISSC), "jack": (r"jackknife", CALC), "jplus": (r"jackknife+", BANDC),
        "split": (r"split", PREDC)}


class Jackknife(VoiceoverScene):
    def construct(self):
        self.card()
        self.waste()
        self.naive()
        self.jplus()
        self.coverage()
        self.widths()
        self.cvplus()
        self.diabetes()
        self.cqr()
        self.cqr_band()
        self.cqr_age()
        self.board()

    def card(self):
        card = chapter_card(7, r"Jackknife+ and CQR", r"Using all the data; \ bands that breathe", lit=(2021,), part=PART)
        with self.voiceover("Chapter seven. The jackknife plus, and conformalized quantile regression."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def waste(self):
        rows = fit_rows(VGroup(
            label(r"split conformal spends half the data on calibration", font_size=26),
            label(r"full conformal: \ refit with each candidate $y$ added, \ keep those that conform", font_size=26, color=GREY_A),
            label(r"exact, \ uses every case, \ but one refit per candidate per new point", font_size=26, color=GREY_A),
            label(r"in between: \ leave-one-out", font_size=26, color=CALC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Split conformal has a cost: the model is trained on only part of the data, and the "
            "calibration cases are used for nothing else. With small data sets that hurts. <bookmark mark='b'/> Full "
            "conformal prediction, Vovk's original, uses every case. For each candidate value y of the new response, "
            "add the new case with that y to the data, refit, and keep y if the new case's score does not stand out "
            "among all n plus one. <bookmark mark='c'/> It is exact, but needs a refit for every candidate value at every "
            "new point, which is affordable only for special models such as ridge regression. <bookmark mark='d'/> The "
            "natural compromise is to leave one case out at a time."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def naive(self):
        rows = [
            cmath(r"\text{in-sample}", r":", r"\hat\mu(x) \pm \hat q\{|y_i - \hat\mu(x_i)|\}", font_size=30),
            cmath(r"\text{jackknife}", r":", r"\hat\mu(x) \pm \hat q\{R_i\}, \ \ R_i = |y_i - \hat\mu_{-i}(x_i)|", font_size=30),
            cmath(r"\text{trouble}", r":", r"\hat\mu \text{ and the } \hat\mu_{-i} \text{ can differ a lot}", font_size=30),
            cmath(r"\text{no guarantee}", r":", r"\text{coverage can fall to } 0", font_size=32),
        ]
        rows[3][-1].set_color(MISSC)
        whys = [why(r"residuals of points it was fitted to"), why(r"leave-one-out residuals"),
                why(r"an unstable fit"), why(r"Barber et al. (2021), \ Theorem 2")]
        with self.voiceover(
            "<bookmark mark='a'/> The crudest interval uses the residuals of the fitted model on its own training data. "
            "Those are too small, since the model was fitted to make them small. <bookmark mark='b'/> The jackknife uses "
            "leave-one-out residuals instead: refit without case i, and see how far off it is for case i. Then it centres "
            "the interval on the full model's prediction. <bookmark mark='c'/> The trouble is that mixture. The "
            "leave-one-out residuals describe models fitted without one case; the centre is the model fitted with all of "
            "them. When the fit is unstable, these can be very different. <bookmark mark='d'/> Rina Foygel Barber, "
            "Emmanuel Candès, Aaditya Ramdas and Ryan Tibshirani showed in 2021 that the jackknife has no coverage "
            "guarantee at all: for some fitting methods its coverage can be driven to zero."
        ) as vo:
            intro=label('Leave-one-out residuals alone need not validate a full-fit interval',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def jplus(self):
        rows = [
            cmath(r"\text{lower}", r":", r"\hat q^{-}_{\alpha}\big\{\hat\mu_{-i}(x) - R_i\big\}", font_size=32),
            cmath(r"\text{upper}", r":", r"\hat q^{+}_{\alpha}\big\{\hat\mu_{-i}(x) + R_i\big\}", font_size=32),
            cmath(r"P\big(Y_{n+1} \in C(X_{n+1})\big)", r"\ge", r"1 - 2\alpha \ \ \text{under exchangeability and symmetric fitting}", font_size=30),
            cmath(r"\text{in practice}", r":", r"\approx 1 - \alpha", font_size=32),
        ]
        rows[2][-1].set_color(BANDC)
        whys = [why(r"the $\lfloor \alpha(n+1) \rfloor$-th smallest"), why(r"the $\lceil (1-\alpha)(n+1) \rceil$-th smallest"),
                why(r"for any algorithm treating cases symmetrically"), why(r"stability can improve the bound; finite-sample slack remains")]
        with self.voiceover(
            "<bookmark mark='a'/> Their fix, the jackknife plus, is small and decisive: use the leave-one-out models "
            "for the centre too. For each i, the model without case i makes a prediction at the new x, and we shift "
            "it down by case i's own residual. The lower end is a low quantile of these n numbers. <bookmark "
            "mark='b'/> The upper end is a high quantile of the predictions shifted up. <bookmark mark='c'/> They "
            "proved that this interval covers with probability at least one minus two alpha, for any distribution and"
            " any fitting algorithm that treats the cases symmetrically, however unstable. <bookmark mark='d'/> The "
            "factor of two is the price of the worst case; in practice, stability conditions can yield stronger "
            "approximate bounds with finite-sample slack. At alpha point one the general jackknife-plus guarantee is "
            "eighty percent, not ninety."
        ) as vo:
            intro=label('Jackknife+ pairs each residual with its own fitted prediction',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def coverage(self):
        d = load("jack")
        ps = np.asarray(d["ps"], float)
        A = axes([0, 210], [0, 1.0], x_length=7.4, y_length=4.4, xlabel=r"number of predictors $p$ \ ($n = 100$)",
                 ylabel=r"coverage", xticks=[0, 50, 100, 150, 200], yticks=[0, 0.5, 0.9],
                 yfmt=lambda v: rf"{100 * v:.0f}\%", center=[-2.0, 0.2, 0])
        ax = A.ax
        nine = DashedLine(ax.c2p(0, 0.9), ax.c2p(210, 0.9), color=GREY_B, stroke_width=2)
        pn = DashedLine(ax.c2p(100, 0), ax.c2p(100, 1.0), color=GREY_D, stroke_width=1.5)
        lines = {}
        for k, (nm, c) in METH.items():
            ys = [d["res"][str(int(p))][k]["cover"] for p in ps]
            lines[k] = VGroup(polyline(ax, ps, ys, c, 3), *[Dot(ax.c2p(a, b), radius=0.05, color=c) for a, b in zip(ps, ys)])
        r100 = d["res"]["100"]
        side = fit_rows(VGroup(
            label(r"least squares, \ minimum-norm past $p = n$", font_size=22),
            label(rf"in-sample: \ {100 * r100['naive']['cover']:.0f}\% at $p = n$", font_size=22, color=MISSC),
            label(rf"jackknife: \ {100 * r100['jack']['cover']:.0f}\% at $p = n$", font_size=22, color=CALC),
            label(rf"jackknife+: \ {100 * r100['jplus']['cover']:.0f}\%; \ split: \ {100 * r100['split']['cover']:.0f}\%", font_size=22, color=BANDC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Barber and colleagues' own experiment, repeated. A hundred training points, p "
            "Gaussian predictors, and least squares, taking the minimum-norm solution once p exceeds n, where the fit"
            " interpolates the data. Sixty data sets at each p. <bookmark mark='b'/> The in-sample method collapses "
            "as p grows: at p equal to n the fit passes through every training point, the residuals are all zero, and"
            " the interval has no width. <bookmark mark='c'/> The jackknife holds up for small p but fails near the "
            "interpolation threshold, where leaving one point out changes the fit violently. <bookmark mark='d'/> The"
            " jackknife plus stays near ninety percent in this experiment, above its eighty percent general lower "
            "bound; at p equal to n it covers ninety-five. Split conformal is valid too, though it dips at p equal to"
            " fifty, where its own fit, on only half the data, is the one interpolating; with sixty data sets per "
            "point, some wobble is expected."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(nine), Create(pn), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lines["naive"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(lines["jack"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(lines["jplus"]), Create(lines["split"]), FadeIn(side[3]))
        self.clear_scene()

    def widths(self):
        d = load("jack")
        ps = [20, 50, 80, 90, 100, 110, 150, 200]
        rows = [[r"$p$"] + [rf"{p}" for p in ps]]
        for k in ("jack", "jplus", "split"):
            rows.append([METH[k][0]] + [rf"{d['res'][str(p)][k]['width']:.0f}" for p in ps])
        tab = table_rows(rows, font_size=24, col_buff=0.45, row_buff=0.3,
                         colors=[GREY_A, CALC, BANDC, PREDC]).move_to([0, 0.9, 0])
        if tab.width > 12.6:
            tab.width = 12.6
        foot = fit_rows(VGroup(
            label(r"median interval widths; \ the noise alone needs about 3.3", font_size=24),
            label(r"near $p = n$ the honest answer is: \ very uncertain", font_size=24, color=BANDC),
            label(r"jackknife+ is narrower than split for small $p$: \ it trains on $n-1$", font_size=24, color=CALC),
        ), 12.4, 0.35, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The widths tell the rest. The noise alone, with standard deviation one, needs an "
            "interval about three point three wide. <bookmark mark='b'/> Near p equal to n, the jackknife plus gives "
            "very wide intervals, because a least squares fit that has just enough parameters to interpolate predicts "
            "wildly. The jackknife's intervals are wide there too, but they are centred on the full model's wild "
            "prediction, and miss half the time. <bookmark mark='c'/> For small p, the "
            "jackknife plus is narrower than split conformal, because its models are trained on all but one case rather "
            "than half of them."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def cvplus(self):
        rows = [
            cmath(r"\text{CV+}", r":", r"K \text{ folds instead of } n: \ \hat\mu_{-k(i)} \text{ in place of } \hat\mu_{-i}", font_size=30),
            cmath(r"\text{cost}", r":", r"K \text{ fits, \ not } n", font_size=32),
            cmath(r"\text{coverage}", r"\ge", r"1 - 2\alpha - \text{a term of order } \sqrt{1/n}", font_size=30),
            cmath(r"\text{jackknife+-after-bootstrap}", r":", r"\text{reuse a forest's out-of-bag trees}", font_size=28),
        ]
        rows[0][-1].set_color(BANDC)
        whys = [why(r"Barber et al. (2021)"), why(r"$K = 10$: \ ten forests"), why(r"Theorem 4"),
                why(r"Kim, \ Xu \& Barber (2020)")]
        with self.voiceover(
            "<bookmark mark='a'/> Refitting n times is expensive for a forest or a network. CV plus does the same with K "
            "folds: each case's residual comes from the model trained without its fold, and the same model makes that "
            "case's shifted prediction at the new point. <bookmark mark='b'/> Ten folds, ten fits. <bookmark mark='c'/> "
            "Its bound includes a fold-dependent correction under the theorem’s symmetry and fold-size conditions. Nominal ninety percent is not a universal CV-plus guarantee. <bookmark mark='d'/> And for bagged models "
            "there is a free version: Byol Kim, Chen Xu and Barber's jackknife plus after bootstrap uses, for each case, "
            "the trees that never saw it, exactly the out-of-bag idea of chapter two."
        ) as vo:
            intro=label('CV+ saves fits but has its own finite-sample correction',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def diabetes(self):
        d = load("diab")
        f = d["first"]
        n = len(f["y"])
        A = axes([0, n + 1], [0, 360], x_length=7.4, y_length=4.4, xlabel=r"test patient", ylabel=r"progression",
                 xticks=[1, 6, 12], yticks=[0, 100, 200, 300], center=[-2.0, 0.2, 0])
        ax = A.ax
        bars = VGroup()
        for k, (lo, hi, y) in enumerate(zip(f["lo"], f["hi"], f["y"])):
            ok = lo <= y <= hi
            bars.add(VGroup(Line(ax.c2p(k + 1, max(lo, 0)), ax.c2p(k + 1, min(hi, 360)), color=BANDC if ok else MISSC, stroke_width=6, stroke_opacity=0.7),
                            Dot(ax.c2p(k + 1, y), radius=0.06, color=WHITE)))
        side = fit_rows(VGroup(
            label(r"442 diabetes patients, \ 10 baseline measures", font_size=22),
            label(r"a forest, \ CV+ with $K = 10$, \ 90\%", font_size=22, color=TREEC),
            label(rf"coverage {100 * d['cvplus_cover']:.1f}\%, \ width {d['cvplus_width']:.0f}", font_size=22, color=BANDC),
            label(rf"split: \ {100 * d['split_cover']:.1f}\%, \ width {d['split_width']:.0f}", font_size=22, color=PREDC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On real data: the diabetes study of Part 32, four hundred and forty-two patients, ten "
            "baseline measurements, and disease progression a year later. <bookmark mark='b'/> A random forest wrapped in "
            "ten-fold CV plus, at ninety percent, on ten random splits into training and test patients. Here are twelve "
            "test patients: white dots are their outcomes, bars their intervals. <bookmark mark='c'/> Over all the test "
            "patients, the coverage is " + say(100 * d["cvplus_cover"], 1) + " percent, <bookmark mark='d'/> and split "
            "conformal, training the forest on half the data, gives " + say(100 * d["split_cover"], 1) + " percent with "
            "intervals of similar width. Both are wide, about two hundred units, because a year's progression of diabetes "
            "is hard to predict from ten measurements: the intervals say so honestly."
        ) as vo:
            self.add(diab_tag())
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.15), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def cqr(self):
        rows = [
            cmath(r"\hat q_{lo}(x), \ \hat q_{hi}(x)", r":", r"\text{quantile regressions at } \alpha/2, \ 1 - \alpha/2", font_size=28),
            cmath(r"E_i", r"=", r"\max\big\{\hat q_{lo}(x_i) - y_i, \ y_i - \hat q_{hi}(x_i)\big\}", font_size=30),
            cmath(r"C(x)", r"=", r"\big[\hat q_{lo}(x) - \hat Q, \ \hat q_{hi}(x) + \hat Q\big]", font_size=32),
            cmath(r"\hat Q", r"=", r"\text{the conformal quantile of the } E_i", font_size=32),
        ]
        rows[2][-1].set_color(BANDC)
        whys = [why(r"quantile regression (Parts 21, 23), \ on the training part"), why(r"how far outside the band; \ negative if inside"),
                why(r"widen, \ or narrow if $\hat Q < 0$"), why(r"Romano, \ Patterson \& Cand\`es (2019)")]
        with self.voiceover(
            "<bookmark mark='a'/> Now the fixed width. Yaniv Romano, Evan Patterson and Emmanuel Candès proposed in 2019 to "
            "start from a band that already adapts: quantile regressions, from Parts 21 and 23, at alpha over two and one minus "
            "alpha over two, fitted on the training part. <bookmark mark='b'/> On the calibration cases, the score measures "
            "how far each response falls outside its band, negative if inside. <bookmark mark='c'/> Then widen both ends of "
            "the band by Q hat, <bookmark mark='d'/> the conformal quantile of those scores; if the quantile regressions "
            "were too generous, Q hat is negative and the band shrinks. The guarantee is the quantile lemma's, unchanged, "
            "and the width now follows the data."
        ) as vo:
            intro=label('Conformal quantile scores can adapt a band to input-dependent spread',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cqr_band(self):
        d = load("split")
        ages = np.asarray(d["ages"], float)
        m = np.asarray(d["m"], float)
        lo, hi = np.asarray(d["cqr_lo"], float), np.asarray(d["cqr_hi"], float)
        q = d["q"]
        A = axes([18, 96], [0, 250], x_length=7.6, y_length=4.6, xlabel=r"age", ylabel=r"income (\$1{,}000s)",
                 xticks=[20, 40, 60, 80], yticks=[0, 100, 200], center=[-2.0, 0.2, 0])
        ax = A.ax
        pa, py = np.asarray(d["pts_a"], float), np.asarray(d["pts_y"], float)
        jit = np.random.default_rng(3).uniform(-0.4, 0.4, len(pa))
        dots = VGroup(*[Dot(ax.c2p(a + j, b), radius=0.02, color=LABC, fill_opacity=0.5) for a, b, j in zip(pa, py, jit)])
        ok = np.isfinite(m) & np.isfinite(lo) & np.isfinite(hi)
        sb = band(ax, ages[ok], np.maximum(m[ok] - q, 0), np.minimum(m[ok] + q, 250), PREDC, 0.15)
        cb = band(ax, ages[ok], np.maximum(lo[ok], 0), np.minimum(hi[ok], 250), BANDC, 0.35)
        side = fit_rows(VGroup(
            label(r"faint blue: \ split conformal, \ fixed width", font_size=22, color=PREDC),
            label(r"green: \ CQR, \ 5\% and 95\% quantile fits", font_size=22, color=BANDC),
            label(rf"$\hat Q = {d['cqr_q']:.2f}$: \ the fits were nearly right", font_size=22, color=CALC),
            label(rf"coverage {100 * d['cover_cqr']:.1f}\%; \ width {d['width_cqr']:.0f} \ vs \ {d['width_split']:.0f}", font_size=22, color=BANDC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the World's incomes, the split conformal band of the last chapter, of fixed width. "
            "<bookmark mark='b'/> And the conformalized quantile regression band, built from linear quantile regressions at "
            "five and ninety-five percent on the same cubic in age. It is narrow for the young, wide in mid-career, and "
            "narrower again after retirement. <bookmark mark='c'/> Its correction Q hat is almost zero: the quantile "
            "regressions were already about right. <bookmark mark='d'/> Overall coverage " + say(100 * d["cover_cqr"], 1)
            + " percent. Its average width is a little larger here, because it reaches up into the long right tail where "
            "the incomes really are."
        ) as vo:
            self.add(income_tag())
            self.play(FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(sb), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(cb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def cqr_age(self):
        d = load("split")
        g = d["by_group"]
        A = axes([0, 6], [0.75, 1.0], x_length=7.4, y_length=4.2, xlabel=r"age group", ylabel=r"coverage",
                 xticks=[], yticks=[0.8, 0.9, 1.0], yfmt=lambda v: rf"{100 * v:.0f}\%", center=[-2.0, 0.3, 0])
        ax = A.ax
        s_d = VGroup(*[Dot(ax.c2p(i + 0.38, x["split"]), radius=0.08, color=PREDC) for i, x in enumerate(g)])
        c_d = VGroup(*[Dot(ax.c2p(i + 0.62, x["cqr"]), radius=0.08, color=BANDC) for i, x in enumerate(g)])
        labs = VGroup(*[label(x["group"].replace("-", "--"), font_size=18, color=GREY_A).next_to(ax.c2p(i + 0.5, 0.75), DOWN, buff=0.15)
                        for i, x in enumerate(g)])
        nine = DashedLine(ax.c2p(0, 0.9), ax.c2p(6, 0.9), color=CALC, stroke_width=2)
        rng_s = (min(x["split"] for x in g), max(x["split"] for x in g))
        rng_c = (min(x["cqr"] for x in g), max(x["cqr"] for x in g))
        side = fit_rows(VGroup(
            label(rf"split: \ {100 * rng_s[0]:.0f}\% to {100 * rng_s[1]:.0f}\% by age", font_size=22, color=PREDC),
            label(rf"CQR: \ {100 * rng_c[0]:.0f}\% to {100 * rng_c[1]:.0f}\%", font_size=22, color=BANDC),
            label(r"closer to conditional, \ still only promised marginally", font_size=22, color=CALC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> By age group, the fixed band ranged from " + f"{100 * rng_s[0]:.0f}" + " to "
            + f"{100 * rng_s[1]:.0f}" + " percent. <bookmark mark='b'/> The adaptive band ranges only from "
            + f"{100 * rng_c[0]:.0f}" + " to " + f"{100 * rng_c[1]:.0f}" + ". <bookmark mark='c'/> It is much closer to "
            "conditional coverage, because the quantile regressions model how the spread changes with age. But only the "
            "marginal ninety percent is guaranteed; the rest depends on how good the quantile regressions are."
        ) as vo:
            self.add(income_tag())
            self.play(FadeIn(A), FadeIn(labs), Create(nine))
            vo.wait_until("a")
            self.play(FadeIn(s_d), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(c_d), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def board(self):
        rows = board_rows("CQR", "in-sample", "jackknife+")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board. Conformalized quantile regression on the World's incomes: kept. "
                   "<bookmark mark='b'/> In-sample residuals for least squares with p equal to n: broken, never covering "
                   "at all. The jackknife plus in the same setting: kept, at about ninety percent, comfortably above its "
                   "worst-case promise of eighty.",
                   [("a", [0]), ("b", [1, 2])])
