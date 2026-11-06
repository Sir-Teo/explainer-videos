from __future__ import annotations

import numpy as np

from videos.stats.stats34.common import *  # noqa: F403


def short(name: str) -> str:
    return name.replace("_", " ")


class Explain(VoiceoverScene):
    def construct(self):
        self.card()
        self.shmueli()
        self.epe()
        self.wrong_wins()
        self.trees()
        self.roots()
        self.pairs()
        self.rashomon_set()
        self.lesson()

    def card(self):
        card = chapter_card(1, r"Explain or predict?", r"The Rashomon effect", lit=(2010,), part=PART)
        with self.voiceover("Chapter one. Explain, or predict?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def shmueli(self):
        left = VGroup(label(r"\textbf{explanatory}", font_size=28, color=TRUEC),
                      label(r"a causal theory $\to$ a model $f$", font_size=22),
                      label(r"goal: \ the right $f$, \ unbiased $\hat\beta$", font_size=22),
                      label(r"judged by: \ fit, \ tests, \ theory", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        right = VGroup(label(r"\textbf{predictive}", font_size=28, color=PREDC),
                       label(r"any $\hat f$ that maps $x$ to $y$", font_size=22),
                       label(r"goal: \ small error on new $x$", font_size=22),
                       label(r"judged by: \ held-out accuracy", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        cols = VGroup(left, right).arrange(RIGHT, buff=1.6, aligned_edge=UP).move_to([0, 0.6, 0])
        bar = Line(cols.get_top() + DOWN * 0.1, cols.get_bottom() + DOWN * 0.1, color=GREY_D).move_to(cols)
        foot = label(r"Galit Shmueli, \ \emph{To Explain or to Predict?} \ (2010)", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "<bookmark mark='a'/> Galit Shmueli made the distinction precise in 2010, in a paper called To Explain or to "
            "Predict? Explanatory modelling starts from a causal theory, translates it into a statistical model, and "
            "wants the right model with unbiased coefficients, so that each coefficient means what the theory says. It "
            "is judged by fit, by tests, and by whether it agrees with theory. <bookmark mark='b'/> Predictive modelling "
            "wants any function that maps new inputs to accurate outputs. It is judged only by its error on data it has "
            "not seen. <bookmark mark='c'/> Shmueli's point was that these are different goals, which can call for "
            "different models fitted to the same data, and that a field which only does one of them is missing half "
            "its science."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(bar), FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def epe(self):
        rows = [
            cmath(r"\mathrm{EPE}(x_0)", r"=", r"E\big[(Y - \hat f(x_0))^2\big]", font_size=32),
            cmath(r"", r"=", r"\sigma^2 + \big(f(x_0) - E\hat f(x_0)\big)^2 + \mathrm{Var}\,\hat f(x_0)", font_size=30),
            cmath(r"\text{explanation}", r":", r"\text{drive the bias to } 0", font_size=32),
            cmath(r"\text{prediction}", r":", r"\text{trade bias for variance}", font_size=32),
        ]
        rows[1][-1].set_color(PREDC)
        whys = [why(r"expected prediction error"), why(r"noise $+$ bias$^2$ $+$ variance"),
                why(r"the coefficients must be right"), why(r"Part 19's tradeoff")]
        with self.voiceover(
            "<bookmark mark='a'/> The difference shows in the expected prediction error at a point x nought. <bookmark "
            "mark='b'/> It splits, as in Part 19, into the noise sigma squared, the squared bias of the fitted function, "
            "and its variance. <bookmark mark='c'/> Explanation cares about the bias: a coefficient that is wrong on "
            "average answers the scientific question wrongly, however small its variance. <bookmark mark='d'/> "
            "Prediction cares about the sum, and will happily accept some bias to buy a larger fall in variance."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def wrong_wins(self):
        rows = [
            cmath(r"y", r"=", r"\beta_1 x_1 + \beta_2 x_2 + \varepsilon, \ \ \beta_2 \text{ small}", font_size=30),
            cmath(r"\text{full model}", r":", r"\mathrm{EPE} = \sigma^2 (1 + 2/n)", font_size=30),
            cmath(r"\text{drop } x_2", r":", r"\mathrm{EPE} \approx \sigma^2(1 + 1/n) + \beta_2^2 \mathrm{Var}(x_2)", font_size=30),
            cmath(r"\text{wrong wins if}", r":", r"\beta_2^2 \mathrm{Var}(x_2) < \sigma^2 / n", font_size=30),
        ]
        rows[3][-1].set_color(PREDC)
        whys = [why(r"the true model has both"), why(r"unbiased, \ two coefficients"), why(r"biased, \ one coefficient"),
                why(r"a standard result; \ Shmueli (2010)")]
        with self.voiceover(
            "<bookmark mark='a'/> A small example makes it concrete. Suppose the truth has two predictors, and the second "
            "has a small coefficient. <bookmark mark='b'/> The correct model is unbiased and, with independent "
            "standardized predictors, has expected prediction error about sigma squared times one plus two over n. "
            "<bookmark mark='c'/> The wrong model, which drops x two, has one fewer coefficient to estimate but carries "
            "the bias beta two squared times the variance of x two. <bookmark mark='d'/> So the wrong model predicts "
            "better whenever that bias is smaller than sigma squared over n: when the effect is smaller than the noise "
            "can resolve. The model that explains correctly is not always the one that predicts best."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def trees(self):
        d = load("rashomon")
        ft = d["first_trees"]
        rows = [[r"tree", r"root split", r"test accuracy"]] + [[rf"{k + 1}", short(t["root"]), rf"{100 * t['acc']:.1f}\%"] for k, t in enumerate(ft)]
        tab = table_rows(rows, font_size=24, col_buff=0.7, row_buff=0.22,
                         colors=[GREY_A] + [TREEC] * len(ft)).move_to([-2.2, 0.2, 0])
        side = fit_rows(VGroup(
            label(r"50 bootstrap samples \ of the 400 training cases", font_size=22),
            label(r"a depth-3 tree on each", font_size=22, color=TREEC),
            label(rf"accuracy: \ {100 * d['acc_mean']:.1f}\% $\pm$ {100 * d['acc_sd']:.1f}", font_size=22, color=PREDC),
            label(r"the story at the root keeps changing", font_size=22, color=CALC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Breiman's Rashomon effect is easy to see on the breast cancer data. Take fifty "
            "bootstrap samples of the four hundred training biopsies, <bookmark mark='b'/> and grow a tree three levels "
            "deep on each. <bookmark mark='c'/> On the hundred and sixty-nine held-out cases they are all about as good: "
            "ninety-three percent correct, give or take two. <bookmark mark='d'/> But the first split, the one a doctor "
            "would read as the most important feature, changes from tree to tree: the worst radius, the worst perimeter, "
            "the worst area, the mean concave points."
        ) as vo:
            self.add(bc_tag())
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def roots(self):
        d = load("rashomon")
        order = [int(i) for i in d["order"][:5]]
        cnt = [d["root_counts"][i] for i in order]
        names = [short(d["names"][i]) for i in order]
        A = axes([0, 5], [0, 24], x_length=7.2, y_length=4.2, xlabel=r"", ylabel=r"trees (of 50)",
                 xticks=[], yticks=[0, 10, 20], center=[-2.0, 0.2, 0])
        ax = A.ax
        bars = bars_at(ax, np.arange(5) + 0.5, cnt, 0.7, TREEC)
        labs = VGroup(*[label(n, font_size=16, color=GREY_A).rotate(PI / 7).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.25)
                        for i, n in enumerate(names)])
        nums = VGroup(*[label(rf"{c}", font_size=20, color=TREEC).next_to(b, UP, buff=0.08) for c, b in zip(cnt, bars)])
        side = fit_rows(VGroup(
            label(rf"{d['n_distinct_roots']} different root features", font_size=22, color=TREEC),
            label(rf"{d['distinct_top3']} different `top three' sets \ in 50 trees", font_size=22, color=CALC),
            label(r"radius, \ perimeter, \ area: \ correlated 0.94--0.998", font_size=22),
            label(r"the data cannot say which one matters", font_size=22, color=MISSC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Over all fifty trees, five different features appear at the root. The worst concave "
            "points wins twenty-one times, the mean concave points eleven, the worst perimeter ten. <bookmark mark='b'/> "
            "And if we list each tree's three most important features, we get thirty-nine different lists from fifty "
            "trees. <bookmark mark='c'/> The reason is no mystery. The radius, perimeter and area of a nucleus are "
            "essentially the same measurement, correlated between point nine four and point nine nine eight, and the concavity features move together "
            "too. <bookmark mark='d'/> The data cannot say which of them matters, because any of them predicts as well "
            "as any other. A tree picks one, almost by chance."
        ) as vo:
            self.add(bc_tag())
            self.play(FadeIn(A), FadeIn(labs))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), FadeIn(nums), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def pairs(self):
        d = load("rashomon")
        rows = [[r"model", r"features", r"coefficients", r"accuracy"]]
        for k, p in enumerate(d["pairs"]):
            rows.append([rf"{k + 1}", short(p["features"][0]) + r" \ + \ " + short(p["features"][1]),
                         rf"{p['coef'][0]:.1f}, \ {p['coef'][1]:.1f}", rf"{100 * p['acc']:.1f}\%"])
        tab = table_rows(rows, font_size=24, col_buff=0.6, row_buff=0.3, colors=[GREY_A, TRUEC, TRUEC, TRUEC]).move_to([0, 1.2, 0])
        if tab.width > 12.6:
            tab.width = 12.6
        foot = fit_rows(VGroup(
            label(r"three logistic regressions on disjoint pairs of features", font_size=24),
            label(r"each `explains' the diagnosis with different variables", font_size=24, color=CALC),
            label(r"each coefficient is significant; \ none is the mechanism", font_size=24, color=MISSC),
        ), 12.4, 0.4, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The same happens with a data model. Here are three logistic regressions, each on two "
            "standardized features, with no feature in common. <bookmark mark='b'/> The first uses the mean concave points "
            "and the worst perimeter; the second, the worst concave points and worst radius; the third, the worst area and "
            "worst texture. Their accuracies are ninety-five, ninety-five and ninety-three percent. <bookmark mark='c'/> "
            "Each would make a respectable paper: two highly significant predictors of malignancy, with a biological "
            "story. <bookmark mark='d'/> None of them is the mechanism. They are three witnesses to one crime, each "
            "telling the story from where it stood."
        ) as vo:
            self.add(bc_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def rashomon_set(self):
        rows = [
            cmath(r"\mathcal R(\epsilon)", r"=", r"\{f \in \mathcal F: \ L(f) \le L(f^\star) + \epsilon\}", font_size=32),
            cmath(r"\text{model reliance}", r":", r"\mathrm{MR}(f) = L(f \text{ with } x_j \text{ scrambled}) / L(f)", font_size=28),
            cmath(r"\text{report}", r":", r"\big[\min_{\mathcal R} \mathrm{MR}, \ \max_{\mathcal R} \mathrm{MR}\big]", font_size=32),
            cmath(r"\text{large } \mathcal R", r"\Rightarrow", r"\text{a simple model may be as good}", font_size=30),
        ]
        rows[2][-1].set_color(CALC)
        whys = [why(r"the Rashomon set"), why(r"how much one model uses $x_j$"),
                why(r"Fisher, \ Rudin \& Dominici (2019)"), why(r"Semenova, \ Rudin \& Parr (2022)")]
        with self.voiceover(
            "<bookmark mark='a'/> Cynthia Rudin and her colleagues turned the effect into an object. The Rashomon set is "
            "every model in a class whose loss is within epsilon of the best. <bookmark mark='b'/> For one model, the "
            "reliance on feature j is how much its loss grows when that feature is scrambled. <bookmark mark='c'/> "
            "Instead of reporting one model's reliance, Aaron Fisher, Rudin and Francesca Dominici proposed reporting its "
            "range over the whole Rashomon set: the least and the most any good model needs the feature. A feature that "
            "every good model needs is important; one that some good models ignore is not, whatever a single forest says. "
            "<bookmark mark='d'/> And when the Rashomon set is large, it is likely to contain a simple, interpretable "
            "model as accurate as the black box, which is Rudin's argument for using one in high-stakes decisions."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"a good predictor is not an explanation", font_size=26, color=PREDC),
            label(r"many models, \ one accuracy: \ the data do not choose between them", font_size=26, color=TREEC),
            label(r"but prediction is a statistical problem too: \ it has estimands, \ errors, \ guarantees", font_size=26, color=CALC),
            label(r"next: \ the forest as an estimator", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So the first lesson: a good predictor is not an explanation. <bookmark mark='b'/> When "
            "many models predict equally well, the data simply do not choose between their stories. <bookmark mark='c'/> "
            "But Breiman's culture is not outside statistics. A predictor is an estimator of something; its error is a "
            "random variable; and we can ask for guarantees about it. <bookmark mark='d'/> We start with the forest "
            "itself."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
