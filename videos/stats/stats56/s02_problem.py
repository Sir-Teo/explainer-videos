from __future__ import annotations

import numpy as np

from videos.stats.stats56.common import *  # noqa: F403


class Problem(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_rows()
        self.curse()
        self.shrink_link()
        self.goals()
        self.debate()
        self.snooping()
        self.fcr()
        self.board()

    def card(self):
        card = chapter_card(1, r"The selective-inference problem", r"Why a fixed-question interval fails a chosen question", lit=(2005,), part=PART)
        with self.voiceover("Chapter one. The selective-inference problem: why an interval built for a fixed question fails a chosen one."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def setup_rows(self):
        rows = [
            cmath(r"Y \sim P_\theta", r",", r"\text{many possible questions } \theta_1, \dots, \theta_K", font_size=36),
            cmath(r"\hat\jmath = S(Y)", r":", r"\text{the question chosen by looking at } Y", font_size=36),
            cmath(r"P(\theta_j \in C_j)", r"=", r"1 - \alpha \ \text{ for each fixed } j", font_size=36),
            cmath(r"P(\theta_{\hat\jmath} \in C_{\hat\jmath})", r"\ne", r"1 - \alpha \ \text{ in general}", font_size=30),
        ]
        rows[1][-1].set_color(SELC)
        rows[3][-1].set_color(NAIVEC)
        whys = [why(r"effects, \ coefficients, \ clusters"), why(r"a selection rule"), why(r"marginal coverage"), why(r"selection is part of the experiment")]
        head = label('Selection changes the question', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> The setting. Data Y, and many questions one might ask of it: K effects, coefficients or "
            "differences. <bookmark mark='b'/> A selection rule, S of Y, looks at the data and chooses which question to "
            "report: the largest effect, the variables a lasso keeps, the clusters an algorithm finds. <bookmark mark='c'/> "
            "For any fixed question, the usual interval covers with probability one minus alpha. <bookmark mark='d'/> For "
            "the chosen question it need not, because the interval was built for a question that nobody chose in advance. "
            "The selection is part of the experiment, and inference must account for it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def curse(self):
        d = load("winners")["curse"]
        lk = np.log10([r["K"] for r in d])
        A = axes([-0.1, 3.1], [-.15, 3.5], x_length=7.4, y_length=4.4, xlabel=r"$K$ candidates, \ all null \ (log scale)", ylabel=r"",
                 xticks=[0, 1, 2, 3], xfmt=lambda v: f"{10 ** v:,.0f}", yticks=[0, 1, 2, 3], center=[-2.5, 0.2, 0])
        ax = A.ax
        cb = VGroup(polyline(ax, lk, [r["bias"] for r in d], SELC, 4), *[Dot(ax.c2p(a, r["bias"]), radius=0.07, color=SELC) for a, r in zip(lk, d)])
        cc = VGroup(polyline(ax, lk, [3 * r["naive"] for r in d], NAIVEC, 4), *[Dot(ax.c2p(a, 3 * r["naive"]), radius=0.07, color=NAIVEC) for a, r in zip(lk, d)])
        nom = DashedLine(ax.c2p(-0.1, 3 * 0.95), ax.c2p(3.1, 3 * 0.95), color=GREY_B, stroke_width=2)
        k10 = [r for r in d if r["K"] == 10][0]
        k100 = [r for r in d if r["K"] == 100][0]
        side = fit_rows(VGroup(
            label(r"$K$ standard normals; \ report the largest", font_size=22),
            label(rf"gold: \ the bias: \ {k10['bias']:.2f} $(K = 10)$, \ {d[-1]['bias']:.2f} $(1{{,}}000)$", font_size=22, color=SELC),
            label(r"red: \ 3 times coverage of $\max \pm 1.96$ \ (95\% at 2.85)", font_size=22, color=NAIVEC),
            label(rf"{100 * k10['naive']:.0f}\% at $K = 10$, \ {100 * k100['naive']:.0f}\% at 100, \ {100 * d[-1]['naive']:.0f}\% at 1,000", font_size=22, color=NAIVEC),
            label(r"the bias grows like $\sqrt{2\log K}$: \ Part 51's maxima", font_size=22, color=GREY_A),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The simplest case. K independent standard normals, every true mean zero, and we report the largest. <bookmark mark='b'/> The reported value's average is its bias: {say(k10['bias'], 2)} with ten candidates and {say(d[-1]['bias'], 2)} with a thousand, growing like the root of two log K, the Gaussian maxima of Part fifty-one. <bookmark mark='c'/> In red, how often the usual interval, the maximum plus or minus one point nine six, covers the true value of zero. <bookmark mark='d'/> {100 * k10['naive']:.0f} percent with ten candidates, {100 * k100['naive']:.0f} with a hundred, and no hits in these four thousand draws with a thousand candidates; the exact probability is tiny and positive. <bookmark mark='e'/> Nothing is wrong with the interval; it is being asked a question it was not built for."
        ) as vo:
            self.play(FadeIn(A), FadeIn(nom), FadeIn(simulated_tag(r"simulated, \ 4,000 runs")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cc), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def shrink_link(self):
        rows = [
            cmath(r"\text{Bayes}", r":", r"\text{the posterior ignores selection}", font_size=32),
            cmath(r"\text{but}", r":", r"\text{only as good as the prior}", font_size=32),
            cmath(r"\text{empirical Bayes}", r":", r"E[\mu \mid z] = z + \sigma^2(\log f)'(z): \ \text{shrinks winners}", font_size=32),
            cmath(r"\text{Efron (2011)}", r":", r"\text{a correction learned from all } K", font_size=32),
        ]
        rows[2][-1].set_color(HYBC)
        whys = [why(r"Dawid (1994)"), why(r"the catch"), why(r"Part 25"), why(r"borrowing strength")]
        head = label('Shrink link', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> A Bayesian aside. Philip Dawid pointed out that a posterior for a selected mean is the same whether or not it was selected: selection does not change the likelihood of the data you condition on. <bookmark mark='b'/> But this is reassuring only if the prior is right; the selection effect is moved into the prior, not removed. <bookmark mark='c'/> Empirical Bayes makes it concrete. Tweedie's formula from Part twenty-five shrinks each estimate toward the bulk using the estimated density of all of them. The identity uses the true Gaussian marginal density; estimating its derivative introduces error and gives no individual confidence guarantee. Shrinkage need not always be largest at the winner. <bookmark mark='d'/> Bradley Efron proposed it in 2011 as a frequentist correction for the winner's curse, learned from all K estimates at once."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def goals(self):
        rows = [
            cmath(r"\text{simultaneous}", r":", r"P\big(\theta_j \in C_j \ \forall j\big) \ge 1 - \alpha \ \Rightarrow \ \text{any selection is covered}", font_size=32),
            cmath(r"\text{conditional}", r":", r"P\big(\theta_j \in C_j \mid \hat\jmath = j\big) \ge 1 - \alpha \ \text{ for every } j", font_size=32),
            cmath(r"\text{on average}", r":", r"\text{FCR} = E\Big[\frac{\#\text{selected intervals missing}}{\#\text{selected}\vee1}\Big] \le \alpha", font_size=32),
            cmath(r"\text{or}", r":", r"\text{use independent data for the two jobs}", font_size=34),
        ]
        rows[0][-1].set_color(SIMC)
        rows[1][-1].set_color(CONDC)
        rows[2][-1].set_color(HYBC)
        rows[3][-1].set_color(SPLITC)
        whys = [why(r"PoSI, \ projection: \ chapter 2"), why(r"Fithian, \ Sun \& Taylor: \ chapters 3, \ 8, \ 9"), why(r"Benjamini \& Yekutieli (2005), \ Part 33"), why(r"splitting, \ fission: \ chapters 4, \ 5")]
        head = label('Goals', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> What should a valid interval promise? Three answers. Simultaneous coverage: the intervals for all questions cover together, so whatever is selected is covered. <bookmark mark='b'/> Conditional coverage: given that question j was selected, its interval covers with probability one minus alpha, for every j. Conditional and simultaneous coverage are different guarantees: neither implies the other in general. Fithian, Sun and Taylor argue that conditioning matches what a reader of a selected finding wants. <bookmark mark='c'/> Coverage on average over the selected set: the false coverage rate of Yoav Benjamini and Daniel Yekutieli, from Part thirty-three. <bookmark mark='d'/> Or sidestep the problem, using independent pieces of data for selecting and for inferring."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def debate(self):
        rows = [
            cmath(r"\text{conditional}", r":", r"\text{valid for the question actually asked}", font_size=32),
            cmath(r"\text{unconditional}", r":", r"\text{valid on average over selections}", font_size=32),
            cmath(r"\text{a reader}", r":", r"\text{sees one finding: \ wants conditional}", font_size=34),
            cmath(r"\text{but}", r":", r"\text{conditioning can be costly}", font_size=34),
        ]
        rows[0][-1].set_color(CONDC)
        rows[1][-1].set_color(HYBC)
        whys = [why(r"Fithian, \ Sun \& Taylor"), why(r"Andrews, \ Kitagawa \& McCloskey's hybrid"), why(r"the argument for conditioning"), why(r"the argument against")]
        head = label('Debate', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> The choice between conditional and unconditional guarantees is a real debate. A "
            "conditional guarantee is valid for the question actually asked, whatever else might have been selected. "
            "<bookmark mark='b'/> An unconditional one is valid on average over all the selections that might have "
            "happened. <bookmark mark='c'/> The case for conditioning is the reader's view: someone reading a paper "
            "sees one selected finding, and wants an interval that is honest for that finding. <bookmark mark='d'/> "
            "The case against is cost: conditioning on a narrow selection can make intervals very long, and for many "
            "decisions an average guarantee is enough. Both answers appear in this part."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def snooping(self):
        rows = fit_rows(VGroup(
            label(r"selection is everywhere, \ and usually invisible:", font_size=28, color=GREY_A),
            label(r"stepwise regression, \ then the final model's $p$-values", font_size=26, color=NAIVEC),
            label(r"the lasso's variables, \ refitted by least squares, \ reported with OLS intervals", font_size=26, color=NAIVEC),
            label(r"clusters found in the data, \ then tested for differing means", font_size=26, color=NAIVEC),
            label(r"the best of several subgroups, \ outcomes or specifications \ (Part 33's forking paths)", font_size=26, color=NAIVEC),
            label(r"each needs a different correction; \ this part builds them", font_size=26, color=HYBC),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Selection is everywhere in practice, and usually invisible in the paper. <bookmark "
            "mark='b'/> Stepwise regression, followed by the final model's P-values. <bookmark mark='c'/> The variables a "
            "lasso keeps, refitted by least squares and reported with ordinary intervals. <bookmark mark='d'/> Clusters "
            "found in the data and then tested for differing means, which is guaranteed to look significant. <bookmark "
            "mark='e'/> And the best of several subgroups, outcomes or model specifications: the garden of forking paths of "
            "Part thirty-three. <bookmark mark='f'/> Each needs a different correction, and this part builds them."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def fcr(self):
        rows = [
            cmath(r"\text{select } \hat S \text{ by a simple rule}", r",", r"R = |\hat S|", font_size=36),
            cmath(r"C_j^{\text{FCR}}", r"=", r"\text{the marginal interval at level } 1 - \alpha R/K", font_size=36),
            cmath(r"\Rightarrow", r"\;", r"E\Big[\frac{\#\{j \in \hat S: \theta_j \notin C_j\}}{R \vee 1}\Big] \le \alpha \ \text{ for independent estimates and a simple rule}", font_size=30),
            cmath(r"\text{cost}", r":", r"\text{wide when few of many are selected}", font_size=32),
        ]
        rows[1][-1].set_color(HYBC)
        rows[2][-1].set_color(PROOFC)
        whys = [why(r"independent coordinates; \ simple selection rule"), why(r"Benjamini \& Yekutieli (2005)"), why(r"the false coverage rate"), why(r"the price of averaging")]
        head = label('False coverage rate: assumptions matter', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> The simplest correction, from Benjamini and Yekutieli in 2005, has this simple form for independent coordinate estimates and a simple selection rule. Simple means that varying one selected coordinate while keeping it selected leaves the number selected unchanged. Suppose R of the K questions are selected. <bookmark mark='b'/> Use a nested family of valid marginal intervals. Report each selected question's interval, but at level one minus alpha R over K instead of one minus alpha. <bookmark mark='c'/> For independent estimates, the expected fraction of the selected intervals that miss is then at most alpha: the false coverage rate. <bookmark mark='d'/> For arbitrary selection, replace R for each coordinate by the smallest possible selected size while that coordinate remains selected, as specified in their theorem. The cost is width: when few are selected out of many, each interval is as wide as a Bonferroni interval at alpha R over K."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        br = load("board")["rows"]
        show_board(self, board_rows("winner"),
                   f"<bookmark mark='a'/> On the Board: ten means, one of them truly one and the rest zero, and the usual "
                   f"interval around the largest observed. It covers the selected mean {100 * br[0]['achieved']:.1f} percent of "
                   f"the time: broken. Chapter eight will repair it.", [("a", [0])])
