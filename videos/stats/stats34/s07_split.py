from __future__ import annotations

import numpy as np

from videos.stats.stats34.common import *  # noqa: F403


class Split(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.exchange()
        self.ladder_demo()
        self.ranks()
        self.lemma()
        self.recipe()
        self.beta()
        self.income()
        self.by_age()
        self.board()
        self.impossible()

    def card(self):
        card = chapter_card(6, r"Split conformal", r"A guarantee from ranks alone", lit=(2005,), part=PART)
        with self.voiceover("Chapter six. Split conformal prediction."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def history(self):
        rows = fit_rows(VGroup(
            label(r"Vladimir Vovk, \ Alex Gammerman \& Glenn Shafer, \ \emph{Algorithmic Learning in a Random World} (2005)", font_size=24),
            label(r"from Kolmogorov's algorithmic randomness: \ how strange is a new case among the old ones?", font_size=24, color=GREY_A),
            label(r"split (inductive) conformal: \ Papadopoulos, \ Proedrou, \ Vovk \& Gammerman (2002)", font_size=24, color=CALC),
            label(r"brought to statistics: \ Lei, \ G'Sell, \ Rinaldo, \ Tibshirani \& Wasserman (2018)", font_size=24, color=PREDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Conformal prediction was developed by Vladimir Vovk, Alex Gammerman and Glenn Shafer, and "
            "set out in their 2005 book, Algorithmic Learning in a Random World. <bookmark mark='b'/> Vovk had been a "
            "student of Kolmogorov, and the idea grew out of algorithmic randomness: to predict a new case, ask how "
            "strange each possible answer would make it look among the cases already seen. <bookmark mark='c'/> The "
            "computationally cheap version, which splits the data once, came from Harris Papadopoulos and colleagues in "
            "2002. <bookmark mark='d'/> It reached mainstream statistics through Jing Lei, Max G'Sell, Alessandro "
            "Rinaldo, Ryan Tibshirani and Larry Wasserman in 2018, and is now everywhere. Its guarantee rests on one "
            "simple fact about ranks."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def exchange(self):
        rows = [
            cmath(r"(Z_1, \ldots, Z_{n+1})", r"\overset{d}{=}", r"(Z_{\pi(1)}, \ldots, Z_{\pi(n+1)}) \ \ \text{for every } \pi", font_size=30),
            cmath(r"S_i", r"=", r"s(Z_i) \ \text{exchangeable too}", font_size=32),
            cmath(r"P\big(\mathrm{rank}(S_{n+1}) = r\big)", r"=", r"\tfrac{1}{n+1}, \ \ r = 1, \ldots, n+1", font_size=30),
            cmath(r"\text{needs}", r":", r"\text{no model, \ no distribution, \ no } n \to \infty", font_size=30),
        ]
        rows[2][-1].set_color(CALC)
        whys = [why(r"exchangeable: \ order carries no information"), why(r"a fixed score function"),
                why(r"no ties; \ by symmetry"), why(r"Part 16's permutation logic")]
        with self.voiceover(
            "<bookmark mark='a'/> Suppose the n calibration cases and the new case are exchangeable: their joint "
            "distribution does not change if we shuffle them. Independent and identically distributed cases are "
            "exchangeable, but so are many dependent ones. <bookmark mark='b'/> Apply any fixed score function to "
            "each case, say how far its response is from a model's prediction. The scores are exchangeable too. "
            "<bookmark mark='c'/> With no ties, symmetry makes its rank uniform. Ties require randomization for "
            "equality; the unrandomized coverage lower bound still holds. <bookmark mark='d'/> No parametric "
            "distribution or large-sample approximation, but exchangeability is essential. It is Part 16's "
            "permutation argument, pointed at the future."
        ) as vo:
            intro=label('Exchangeable continuous scores have uniform marginal ranks',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ladder_demo(self):
        d = load("lemma")
        lad = ScoreLadder(d["scores"], alpha=0.1, width=8.4, height=3.6, center=[-1.6, 0.0, 0])
        thr = lad.threshold(CALC)
        rung = lad.rung(color=CALC)
        kept = lad.kept(BANDC)
        qlab = label(rf"$q = S_{{(18)}} = {d['q']:.1f}$", font_size=22, color=CALC).next_to(thr, UP, buff=0.1).align_to(thr, LEFT)
        side = fit_rows(VGroup(
            label(r"19 calibration scores, \ sorted", font_size=22),
            label(r"$\alpha = 0.1$: \ $k = \lceil 20 \times 0.9 \rceil = 18$", font_size=22, color=CALC),
            label(r"threshold: \ the 18th smallest", font_size=22, color=CALC),
            label(r"a new score below it: \ 18 of 20 slots", font_size=22, color=BANDC),
        ), 3.8, 0.42, [5.0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> This part's instrument is a score ladder. Here are nineteen calibration scores, "
            "sorted from smallest to largest. <bookmark mark='b'/> We want ninety percent coverage, so alpha is a "
            "tenth, and we take k as the ceiling of twenty times point nine: eighteen. <bookmark mark='c'/> The "
            "threshold q is the eighteenth smallest score. <bookmark mark='d'/> Across fresh continuous calibration "
            "sets and a new score jointly, each of the twenty ranks is equally likely. The gaps in this particular "
            "displayed, rounded ladder are not conditionally equally likely. In eighteen of the twenty it lands at or"
            " below the threshold. So the chance that a new score is at most q is exactly eighteen in twenty: ninety "
            "percent."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(lad), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(rung), Create(thr), FadeIn(qlab), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(kept), FadeIn(side[3]))
            self.bring_to_front(rung)
            g = np.random.default_rng(7)
            for s_new in (3.1, 15.0, 26.0, 6.5):
                b = lad.new_slot(s_new, MISSC if s_new > d["q"] else PREDC)
                self.play(FadeIn(b, shift=DOWN * 0.4), run_time=0.6)
                self.play(FadeOut(b), run_time=0.4)
        self.clear_scene()

    def ranks(self):
        d = load("lemma")
        r = np.asarray(d["ranks"], float)
        A = axes([0, 20], [0, 0.08], x_length=7.4, y_length=4.0, xlabel=r"rank of the new score among 20",
                 ylabel=r"share", xticks=[1, 10, 20], yticks=[0, 0.05], center=[-2.0, 0.2, 0])
        ax = A.ax
        bars = bars_at(ax, np.arange(20) + 0.5, r / r.sum(), 0.8, PREDC)
        flat = DashedLine(ax.c2p(0, 0.05), ax.c2p(20, 0.05), color=CALC, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(r"4,000 fresh sets of 20 scores", font_size=22),
            label(r"the new one's rank: \ flat at $1/20$", font_size=22, color=CALC),
            label(rf"coverage, \ simulated: \ {100 * d['sim_cover']:.2f}\%", font_size=22, color=BANDC),
            label(r"exact: \ $18/20 = 90\%$", font_size=22, color=BANDC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Check it by simulation: four thousand fresh sets of twenty scores, recording where the "
            "twentieth falls among the other nineteen. <bookmark mark='b'/> Every rank comes up about one time in twenty: "
            "the histogram is flat. <bookmark mark='c'/> Over twenty thousand repetitions, the new score falls at or below "
            "the eighteenth smallest " + say(100 * d["sim_cover"], 2) + " percent of the time, <bookmark mark='d'/> where "
            "the exact answer is eighteen twentieths, ninety percent. The scores here were absolute values of normals, but "
            "nothing depended on that."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), Create(flat), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def lemma(self):
        rows = [
            cmath(r"k", r"=", r"\lceil (n+1)(1-\alpha) \rceil, \ \ \hat q = S_{(k)}", font_size=32),
            cmath(r"P\big(S_{n+1} \le \hat q\big)", r"=", r"P\big(\mathrm{rank}(S_{n+1}) \le k\big) = \tfrac{k}{n+1}", font_size=30),
            cmath(r"1 - \alpha", r"\le", r"P\big(S_{n+1} \le \hat q\big) \le 1 - \alpha + \tfrac{1}{n+1}", font_size=30),
            cmath(r"k > n", r"\Rightarrow", r"\hat q = \infty: \ \text{too few scores}", font_size=32),
        ]
        rows[2][-1].set_color(CALC)
        whys = [why(r"the quantile lemma"), why(r"$S_{n+1} \le S_{(k)}$ iff its rank is at most $k$"),
                why(r"$k/(n+1)$ rounds $1 - \alpha$ up by less than $\frac{1}{n+1}$"), why(r"e.g. $n < 9$ at $\alpha = 0.1$")]
        with self.voiceover(
            "<bookmark mark='a'/> In general: with n calibration scores, take k as the ceiling of n plus one times one "
            "minus alpha, and the threshold q hat as the k-th smallest score. <bookmark mark='b'/> The new score is at most "
            "q hat exactly when its rank among the n plus one is at most k, which has probability k over n plus one. "
            "<bookmark mark='c'/> Since k over n plus one rounds one minus alpha up by less than one over n plus one, the "
            "coverage is at least one minus alpha, and, with no ties, at most one minus alpha plus one over n plus one. "
            "This is the quantile lemma. <bookmark mark='d'/> If k exceeds n, there are too few scores for the requested "
            "level, and the honest threshold is infinite."
        ) as vo:
            intro=label('A finite-sample rank correction gives a coverage lower bound',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def recipe(self):
        rows = [
            cmath(r"\text{1. train}", r":", r"\text{any model } \hat\mu \text{ on one part of the data}", font_size=30),
            cmath(r"\text{2. calibrate}", r":", r"S_i = |y_i - \hat\mu(x_i)| \ \text{on the other } n", font_size=30),
            cmath(r"\text{3. predict}", r":", r"C(x) = \big[\hat\mu(x) - \hat q, \ \hat\mu(x) + \hat q\big]", font_size=32),
            cmath(r"P\big(Y_{n+1} \in C(X_{n+1})\big)", r"\ge", r"1 - \alpha", font_size=32),
        ]
        rows[3][-1].set_color(BANDC)
        whys = [why(r"a forest, \ a network, \ anything"), why(r"the model never saw these"),
                why(r"$\hat q$ from the quantile lemma"), why(r"exchangeable scores; model fitted on separate data")]
        with self.voiceover(
            "<bookmark mark='a'/> Split conformal prediction turns this into intervals for any model. Train the "
            "model, any model at all, on one part of the data. <bookmark mark='b'/> On the other part, the "
            "calibration set, score each case by its absolute residual. Conditional on the fitted score function, the"
            " calibration and new cases must be exchangeable. Keeping model fitting separate is necessary but does "
            "not alone establish this assumption. <bookmark mark='c'/> The prediction interval is the model's "
            "prediction plus or minus q hat. <bookmark mark='d'/> The new response falls inside with probability at "
            "least one minus alpha. Finite sample, any distribution, any model, however wrong. A bad model gives wide"
            " intervals, not dishonest ones."
        ) as vo:
            intro=label('Split conformal requires exchangeability given the fitted score',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def beta(self):
        d = load("lemma")
        bt = d["beta"]
        A = axes([0.6, 1.0], [0, 50], x_length=7.4, y_length=4.2, xlabel=r"coverage given the calibration set",
                 ylabel=r"density", xticks=[0.7, 0.8, 0.9, 1.0], yticks=[0, 25, 50], xfmt=lambda v: rf"{v:.1f}",
                 center=[-2.0, 0.2, 0])
        ax = A.ax
        cols = {"19": MISSC, "99": PREDC, "999": BANDC}
        cs = {k: clip_curve(ax, v["xs"], v["pdf"], cols[k], 3) for k, v in bt.items()}
        nine = DashedLine(ax.c2p(0.9, 0), ax.c2p(0.9, 50), color=CALC, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"$F(\hat q) \sim \mathrm{Beta}(k, \, n + 1 - k)$", font_size=22, color=CALC),
            label(rf"$n = 19$: \ 90\% between {bt['19']['q05']:.2f} and {bt['19']['q95']:.2f}", font_size=22, color=MISSC),
            label(rf"$n = 99$: \ {bt['99']['q05']:.2f} to {bt['99']['q95']:.2f}", font_size=22, color=PREDC),
            label(rf"$n = 999$: \ {bt['999']['q05']:.3f} to {bt['999']['q95']:.3f}", font_size=22, color=BANDC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One subtlety. The ninety percent is an average over calibration sets as well as over "
            "the new case. Given one particular calibration set, the coverage is a random number, the score "
            "distribution function evaluated at q hat, and, for independent identically distributed continuous scores given the fitted model, it follows a beta distribution with "
            "parameters k and n plus one minus k. <bookmark mark='b'/> With nineteen calibration cases, the coverage you "
            "actually get lies between " + say(bt["19"]["q05"]) + " and " + say(bt["19"]["q95"]) + " in ninety percent of "
            "calibration sets. <bookmark mark='c'/> With ninety-nine, between " + say(bt["99"]["q05"]) + " and "
            + say(bt["99"]["q95"]) + ". <bookmark mark='d'/> With nine hundred and ninety-nine, within about one and a "
            "half points of ninety. This quantifies variation over calibration sets; it is not input-conditional coverage for your "
            "interval."
        ) as vo:
            self.play(FadeIn(A), Create(nine), FadeIn(side[0]))
            for m_, k, r in (("b", "19", 1), ("c", "99", 2), ("d", "999", 3)):
                vo.wait_until(m_)
                self.play(Create(cs[k]), FadeIn(side[r]))
        self.clear_scene()

    def income(self):
        d = load("split")
        ages = np.asarray(d["ages"], float)
        m = np.asarray(d["m"], float)
        q = d["q"]
        A = axes([18, 96], [0, 250], x_length=7.6, y_length=4.6, xlabel=r"age", ylabel=r"income (\$1{,}000s)",
                 xticks=[20, 40, 60, 80], yticks=[0, 100, 200], center=[-2.0, 0.2, 0])
        ax = A.ax
        pa, py = np.asarray(d["pts_a"], float), np.asarray(d["pts_y"], float)
        jit = np.random.default_rng(3).uniform(-0.4, 0.4, len(pa))
        dots = VGroup(*[Dot(ax.c2p(a + j, b), radius=0.02, color=LABC, fill_opacity=0.5) for a, b, j in zip(pa, py, jit)])
        ok = np.isfinite(m)
        mean = polyline(ax, ages[ok], m[ok], PREDC, 3.5)
        bd = band(ax, ages[ok], np.maximum(m[ok] - q, 0), np.minimum(m[ok] + q, 250), BANDC, 0.25)
        side = fit_rows(VGroup(
            label(r"World incomes; \ display capped at 250; bands cropped", font_size=22),
            label(r"$\hat\mu$: \ a cubic in age, \ with a step at 67", font_size=22, color=PREDC),
            label(rf"$\hat q = {q:.1f}$: \ the band $\hat\mu \pm \hat q$", font_size=22, color=BANDC),
            label(rf"20,000 new adults: \ {100 * d['cover_split']:.1f}\% inside", font_size=22, color=BANDC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A real-sized test, on the World. Predict an adult's income from their age. <bookmark "
            "mark='b'/> The model is a cubic in age with a step at the retirement age, fitted by least squares to a "
            "thousand adults. <bookmark mark='c'/> On another thousand, the calibration set, the absolute residuals "
            "give q hat of about forty-four thousand dollars, so the band is the fitted curve plus or minus that. "
            "<bookmark mark='d'/> On twenty thousand new adults, " + say(100 * d["cover_split"], 1) + " percent fall "
            "inside. Exactly as promised, from a model that is certainly wrong: incomes are skewed, with a Pareto tail, and "
            "their spread changes with age."
        ) as vo:
            self.add(income_tag())
            self.play(FadeIn(A), FadeIn(dots), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(mean), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bd), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def by_age(self):
        d = load("split")
        g = d["by_group"]
        A = axes([0, 6], [0.75, 1.0], x_length=7.4, y_length=4.2, xlabel=r"age group", ylabel=r"coverage",
                 xticks=[], yticks=[0.8, 0.9, 1.0], yfmt=lambda v: rf"{100 * v:.0f}\%", center=[-2.0, 0.3, 0])
        ax = A.ax
        cov = [x["split"] for x in g]
        dots = VGroup(*[Dot(ax.c2p(i + 0.5, c), radius=0.09, color=MISSC if c < 0.88 else BANDC) for i, c in enumerate(cov)])
        stems = VGroup(*[Line(ax.c2p(i + 0.5, 0.75), ax.c2p(i + 0.5, c), color=GREY_C, stroke_width=2) for i, c in enumerate(cov)])
        labs = VGroup(*[label(x["group"].replace("-", "--"), font_size=18, color=GREY_A).next_to(ax.c2p(i + 0.5, 0.75), DOWN, buff=0.15)
                        for i, x in enumerate(g)])
        nine = DashedLine(ax.c2p(0, 0.9), ax.c2p(6, 0.9), color=CALC, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"the same band, \ by age", font_size=22),
            label(rf"18--24: \ {100 * cov[0]:.0f}\% \ (too wide)", font_size=22, color=BANDC),
            label(rf"55--66: \ {100 * cov[4]:.0f}\% \ (too narrow)", font_size=22, color=MISSC),
            label(r"marginal: \ 90\% on average over everyone", font_size=22, color=CALC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> But look at the coverage within age groups. <bookmark mark='b'/> For the young, whose "
            "incomes vary least, the band covers " + f"{100 * cov[0]:.0f}" + " percent: it is wider than they need. "
            "<bookmark mark='c'/> For those aged fifty-five to sixty-six, at the peak of their careers and the widest "
            "spread, it covers only " + f"{100 * cov[4]:.0f}" + ". <bookmark mark='d'/> The guarantee is marginal: ninety "
            "percent on average over everyone, which is not ninety percent for each kind of person. A band of constant "
            "width cannot be right everywhere when the spread is not constant."
        ) as vo:
            self.add(income_tag())
            self.play(FadeIn(A), FadeIn(labs), Create(nine), FadeIn(side[0]))
            self.play(FadeIn(stems), FadeIn(dots))
            vo.wait_until("b")
            self.play(Indicate(dots[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Indicate(dots[4], color=MISSC), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def board(self):
        rows = board_rows("split conformal, \\ 90")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board: split conformal on the World's incomes, with five hundred "
                   "calibration cases, over three hundred fresh draws of the data. Kept, within a hair of ninety percent, "
                   "as the quantile lemma says it must be.",
                   [("a", [0])])

    def impossible(self):
        rows = [
            cmath(r"\text{wanted}", r":", r"P\big(Y \in C(X) \mid X = x\big) \ge 1 - \alpha \ \text{for every } x", font_size=28),
            cmath(r"\text{for all distributions}", r"\Rightarrow", r"\text{no finite expected length at non-atomic }x", font_size=28),
            cmath(r"\text{what survives}", r":", r"\text{coverage within groups chosen in advance}", font_size=28),
            cmath(r"\text{or}", r":", r"\text{better scores: \ bands that adapt}", font_size=32),
        ]
        rows[1][-1].set_color(MISSC)
        whys = [why(r"conditional coverage"), why(r"Vovk (2012); \ Lei \& Wasserman (2014); \ Barber et al. (2021)"),
                why(r"Mondrian conformal, \ chapter 9"), why(r"the next chapter")]
        with self.voiceover(
            "<bookmark mark='a'/> Could we have coverage at every x, conditional on the inputs, without assumptions? "
            "<bookmark mark='b'/> No. Vovk in 2012, Lei and Wasserman in 2014, and Rina Foygel Barber and colleagues in "
            "2021 proved versions of the same impossibility: any procedure with distribution-free conditional coverage "
            "cannot have finite expected interval length at non-atomic input values over an unrestricted response class. <bookmark mark='c'/> What "
            "survives is coverage within a few groups fixed in advance, which chapter nine will build. <bookmark mark='d'/> "
            "Or we can change the score so that the band breathes with the data, which is the next chapter. Part 57 returns "
            "to the impossibility theorems and proves them."
        ) as vo:
            intro=label('Unrestricted conditional coverage prevents finite expected length',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
