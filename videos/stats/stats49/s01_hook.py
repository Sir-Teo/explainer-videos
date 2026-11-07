from __future__ import annotations

import numpy as np

from videos.stats.stats49.common import *  # noqa: F403

NAMES = {"normal": r"normal", "logistic": r"logistic", "laplace": r"Laplace", "t3": r"$t_3$", "mixture": r"bimodal mixture"}


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.table()
        self.chart()
        self.question()
        self.upgrades()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1956, 1982)).to_edge(UP, buff=0.35)
        rows = fit_rows(VGroup(
            label(r"the centre $\theta$ of a symmetric law with an \emph{unknown} shape $f$", font_size=28),
            label(r"if $f$ were known: \ regular MLE, \ asymptotic variance $1/(n I_f)$, \ $I_f = \int (f'/f)^2 f$", font_size=26, color=GRADC),
            label(r"1956: \ Stein asks: \ can we do as well \emph{without} knowing $f$?", font_size=26, color=GREY_A),
            label(r"1975: \ Stone: \ yes, \ by estimating the score $-f'/f$ from the data", font_size=26, color=EFFC),
            label(r"1982: \ Bickel: \ when, \ and why: \ knowing nothing can cost nothing", font_size=26, color=TANC),
        ), 12.4, 0.55, [0, -0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is a question that sounds impossible. Data come from a symmetric distribution centred at theta, but the shape of the distribution is unknown: it might be normal, or logistic, or heavy tailed, or bimodal. <bookmark mark='b'/> If the shape f were known, the maximum likelihood estimator under suitable regularity would have asymptotic variance one over n times the Fisher information of f, and nothing regular could do better. <bookmark mark='c'/> In 1956 Charles Stein asked whether the same accuracy can be had without knowing f. <bookmark mark='d'/> In 1975 Charles Stone showed that it can: estimate the shape's score function from the data themselves, and use it. <bookmark mark='e'/> And in 1982 Peter Bickel explained when and why this works. Sometimes, knowing nothing about an infinite-dimensional nuisance costs nothing at all."
        ) as vo:
            self.play(FadeIn(tl))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def table(self):
        d = load("hook")
        rows = [[r"law", r"mean", r"median", r"Hodges--Lehmann", r"adaptive", r"bound $1/I_f$"]]
        for r in d["rows"]:
            rows.append([NAMES[r["law"]], f"{r['mean']:.2f}", f"{r['median']:.2f}", f"{r['hl']:.2f}", f"{r['adaptive']:.2f}", f"{r['bound']:.2f}"])
        tab = table_rows(rows, font_size=28, col_buff=0.7, row_buff=0.34, colors=[GREY_B] + [None] * 5)
        if tab.width > 12.6:
            tab.width = 12.6
        tab.move_to([0, 0.8, 0])
        # gold the adaptive column, green the bound column
        for i in range(1, 6):
            tab[i][4].set_color(EFFC)
            tab[i][5].set_color(TANC)
        foot = label(rf"$n \times$ variance, \ $n = {d['n']}$, \ {d['reps']} samples per law; \ smaller is better", font_size=24, color=GREY_A).move_to([0, -1.7, 0])
        foot2 = label(r"one estimator, \ never told the law, \ within about a third of the bound in every row", font_size=24, color=EFFC).move_to([0, -2.5, 0])
        r = {x["law"]: x for x in d["rows"]}
        with self.voiceover(
            f"<bookmark mark='a'/> Five symmetric laws, four hundred observations each, and n times the variance of four estimators of the centre. The mean is best for normal data but poor for heavy tails: {say(r['t3']['mean'], 2)} for t with three degrees of freedom, against a bound of {say(r['t3']['bound'], 1)}. The median is good for the Laplace and poor for the normal. The Hodges–Lehmann estimator is a strong compromise. <bookmark mark='b'/> The illustrative density-score estimator, which is never told the law, is within about a third of the bound in every row, and it is the only one that is: {say(r['t3']['adaptive'], 2)} for t three, {say(r['laplace']['adaptive'], 2)} for the Laplace against one, and {say(r['mixture']['adaptive'], 2)} for the bimodal mixture, where every other estimator is at least {say(min(r['mixture']['mean'], r['mixture']['median'], r['mixture']['hl']), 1)}. In some rows a fixed estimator does slightly better; none does well in all of them."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("b")
            self.play(FadeIn(foot2), Indicate(VGroup(*[tab[i][4] for i in range(1, 6)]), color=EFFC))
        self.clear_scene()

    def chart(self):
        d = load("hook")
        ns = np.log10([r["n"] for r in d["by_n"]])
        eff = [r["eff"] for r in d["by_n"]]
        A = axes([1.8, 3.4], [0, 1.1], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"efficiency $= (1/I_f)\,/\,(n\,\mathrm{Var})$",
                 xticks=[2, np.log10(400), np.log10(1600)], xfmt=lambda v: f"{10 ** v:,.0f}", yticks=[0, 0.5, 0.8, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        one = DashedLine(ax.c2p(1.8, 1), ax.c2p(3.4, 1), color=TANC, stroke_width=2.5)
        c = VGroup(polyline(ax, ns, eff, EFFC, 4), *[Dot(ax.c2p(a, b), radius=0.09, color=EFFC) for a, b in zip(ns, eff)])
        side = fit_rows(VGroup(
            label(r"$t_3$ data: \ $1/I_f = 1.5$", font_size=22),
            label(r"gold: \ the adaptive estimator's efficiency", font_size=22, color=EFFC),
            label(rf"{eff[0]:.2f} at 100, \ {eff[1]:.2f} at 400, \ {eff[2]:.2f} at 1,600", font_size=22, color=EFFC),
            label(r"green: \ theoretical adaptive-efficiency benchmark", font_size=22, color=TANC),
            label(r"illustrative KDE one-step; \ fixed score trimming", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The adaptation is asymptotic. For t three data the bound is one point five. <bookmark mark='b'/> The adaptive estimator's efficiency, the bound divided by its actual variance, <bookmark mark='c'/> is {say(eff[0], 2)} at a hundred observations, {say(eff[1], 2)} at four hundred and {say(eff[2], 2)} at sixteen hundred, <bookmark mark='d'/> improving across these sample sizes. This finite-sample KDE one-step uses fixed tail trimming; the adaptation theorem requires additional tuning and score-consistency conditions, and is not proved by this simulation. <bookmark mark='e'/> Not knowing the shape costs something in finite samples, but the cost vanishes to first order. Why that is possible, and when it is not, is what this part is about."
        ) as vo:
            self.play(FadeIn(A), Create(one), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def question(self):
        rows = fit_rows(VGroup(
            label(r"a semiparametric model: \ a number of interest $\psi(P)$, \ and the rest of $P$ unrestricted, \ or nearly", font_size=26),
            label(r"the question: \ how well can $\psi$ be estimated, \ by anyone? \ and by what?", font_size=28, color=EFFC),
            label(r"the answer: \ one function, \ the efficient influence function $\phi^*$; \ the bound is $E\,\phi^{*2}$", font_size=26, color=TANC),
            label(r"and it explains: \ AIPW, \ double robustness, \ DML, \ TMLE, \ missing-data estimators", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The symmetric-centre problem is a semiparametric model: a finite-dimensional quantity of "
            "interest, and everything else about the distribution left unknown and infinite dimensional. <bookmark "
            "mark='b'/> The question of this part: how well can such a quantity be estimated, by any regular estimator, and "
            "which estimators achieve it? <bookmark mark='c'/> The answer is a single function, the efficient influence "
            "function, whose variance is the bound. <bookmark mark='d'/> And that one function explains the estimators "
            "Part thirty-six used on trust: augmented inverse probability weighting, double robustness, double machine "
            "learning, targeted maximum likelihood, and the estimators for missing data. The theory has a reputation for "
            "abstraction, but its central object is concrete: a function of one observation, which you can write down, "
            "estimate and average. Most of this part is about finding that function, and about what to do with it once it "
            "is found, when the nuisance parts of the model are estimated by flexible, imperfect machine learning."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def upgrades(self):
        cards = [
            upgrade_card(36, r"AIPW and DML: \ doubly robust, \ root-$n$ with machine learning", r"their optimality and their robustness, \ on trust",
                         r"chapters 5--8: \ efficient influence functions, \ double robustness, \ the product rate"),
            upgrade_card(47, r"the convolution theorem, \ for parametric models", r"a finite-dimensional model",
                         r"chapters 1--3: \ tangent spaces, \ pathwise derivatives, \ the semiparametric bound"),
            upgrade_card(48, r"a plug-in's cost is its footprint", r"a simple nuisance",
                         r"chapters 4--5: \ the nuisance tangent space, \ the efficient score, \ orthogonality"),
        ]
        for c in cards:
            c.scale(0.86)
        VGroup(*cards).arrange(DOWN, buff=0.25).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Three promises are due. Part thirty-six used augmented inverse probability weighting and double machine learning, and said they were doubly robust and root n consistent with machine-learned nuisances under adequate product rates and regularity; chapters five to eight explain those conditions. <bookmark mark='b'/> Part forty-seven proved the convolution theorem for parametric models; chapters one to three extend it to models with infinite-dimensional parts. <bookmark mark='c'/> And Part forty-eight found that a plugged-in nuisance costs its footprint; chapters four and five turn that observation into geometry."
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 49", font_size=34, color=GREY_B), label(r"Semiparametric Efficiency", font_size=48)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"models and tangent spaces; \ pathwise derivatives; \ the efficient influence function as a projection",
            r"semiparametric efficiency bounds; \ worked influence functions: \ the mean, \ the ATE, \ the partially linear model",
            r"the nuisance tangent space and the efficient score; \ one-step estimators and TMLE",
            r"double robustness; \ DML theory and the product rate; \ missing data; \ higher-order influence functions",
        ], color=EFFC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 36, \ 47, \ 48").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.semipar}, \ the tangent-space picture").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part forty-nine: semiparametric efficiency. <bookmark mark='b'/> We'll define tangent "
            "spaces and pathwise derivatives, and find the efficient influence function as a projection, drawn in a picture "
            "of the space of scores; derive the bound and work out the influence functions of the mean, the average "
            "treatment effect and the partially linear model; project out nuisances to get the efficient score; build "
            "one-step and targeted estimators; and then explain double robustness, the product-rate condition behind "
            "double machine learning, missing data, and what lies beyond the first order."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
