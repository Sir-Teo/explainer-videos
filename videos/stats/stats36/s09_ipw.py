from __future__ import annotations

from videos.stats.stats36.common import *  # noqa: F403


class IPW(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.estimators()
        self.balance()
        self.numbers()
        self.weights()
        self.board()

    def card(self):
        card = chapter_card(8, r"Weighting", r"Rebuild the population the coin would have made", lit=(1952, 1983), part=PART)
        with self.voiceover("Chapter eight. Inverse probability weighting."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = fit_rows(VGroup(
            label(r"a treated patient with $e(x) = 0.2$ is one of five similar patients, \ the others untreated", font_size=26),
            label(r"let them stand for all five: \ weight $1/e(x) = 5$", font_size=26, color=Y1C),
            label(r"an untreated patient with $e(x) = 0.2$: \ weight $1/(1 - e(x)) = 1.25$", font_size=26, color=Y0C),
            label(r"the weighted arms each resemble the whole population: \ a pseudo-randomized trial", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Weighting uses the propensity score differently. A treated patient whose propensity is "
            "point two is, in effect, one of five similar patients, four of whom were not treated. <bookmark mark='b'/> Let "
            "that patient stand for all five, with a weight of one over e, which is five. <bookmark mark='c'/> An untreated "
            "patient with the same propensity stands for one point two five. <bookmark mark='d'/> Then each weighted arm "
            "resembles the whole population in its covariates, as if a coin had assigned treatment: a pseudo-randomized "
            "trial built from observational data. It is Part 18's Horvitz–Thompson estimator, with treatment in place of "
            "being sampled."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def estimators(self):
        rows = [
            cmath(r"\hat\tau_{HT}", r"=", r"\tfrac1n \textstyle\sum_i \Big(\dfrac{T_i Y_i}{\hat e(x_i)} - \dfrac{(1 - T_i) Y_i}{1 - \hat e(x_i)}\Big)", font_size=28),
            cmath(r"E\Big[\dfrac{T Y}{e(X)}\Big]", r"=", r"E\Big[\dfrac{E[T \mid X]\, E[Y(1) \mid X]}{e(X)}\Big] = E[Y(1)]", font_size=28),
            cmath(r"\hat\tau_{\rm Hajek}", r":", r"\text{normalize the weights to sum to } n \text{ in each arm}", font_size=28),
            cmath(r"\text{ATT}", r":", r"\text{treated weight } 1; \ \text{untreated } \hat e/(1 - \hat e)", font_size=30),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"Horvitz \& Thompson (1952), \ Part 18"), why(r"unconfoundedness inside"),
                why(r"more stable; \ a ratio estimator"), why(r"reweight the untreated to look treated")]
        with self.voiceover(
            "<bookmark mark='a'/> The inverse probability weighted estimator averages treated outcomes divided by the "
            "propensity, minus untreated outcomes divided by one minus it. <bookmark mark='b'/> Why it works: the expected "
            "treated term, given X, is the probability of treatment times the average treated outcome, divided by the "
            "probability of treatment, by unconfoundedness. The propensities cancel, leaving the mean treated outcome. "
            "<bookmark mark='c'/> In practice one normalizes the weights to sum to n in each arm, Hajek's version, which is "
            "more stable. <bookmark mark='d'/> For the effect on the treated, the treated get weight one, and the untreated "
            "are reweighted by the odds e over one minus e, to look like the treated."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def balance(self):
        d = load("obs")
        bal = d["balance"]
        A = axes([0, 1.5], [0, 4], x_length=6.0, y_length=3.6, xlabel=r"$|$standardized mean difference$|$", ylabel=r"",
                 xticks=[0, 0.1, 0.5, 1.0, 1.5], yticks=[], xfmt=lambda v: rf"{v:g}", center=[-1.0, 0.2, 0])
        ax = A.ax
        dots = VGroup()
        labs = VGroup()
        for k, b in enumerate(bal):
            yy = 3.5 - k
            dots.add(VGroup(Dot(ax.c2p(abs(b["before"]), yy), radius=0.09, color=MISSC),
                            Dot(ax.c2p(abs(b["after"]), yy), radius=0.09, color=BANDC),
                            Line(ax.c2p(abs(b["before"]), yy), ax.c2p(abs(b["after"]), yy), color=GREY_C, stroke_width=2)))
            labs.add(label(b["name"], font_size=20, color=GREY_A).next_to(ax.c2p(0, yy), LEFT, buff=0.25))
        tenth = DashedLine(ax.c2p(0.1, 0), ax.c2p(0.1, 4), color=TAUC, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"red: \ before weighting", font_size=22, color=MISSC),
            label(r"green: \ after", font_size=22, color=BANDC),
            label(r"dashed: \ 0.1, \ a common rule of thumb", font_size=22, color=TAUC),
        ), 3.2, 0.42, [5.4, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Check balance, the way a trial would. For each covariate, the standardized difference in "
            "means between the arms. <bookmark mark='b'/> Before weighting, the treated have baseline pressures over a "
            "standard deviation higher, and are much older. <bookmark mark='c'/> After weighting, the differences shrink "
            "towards zero, though baseline pressure is still above the conventional threshold of a tenth. The propensity model "
            "here is exactly the right one; what remains is the work of a few enormous weights at the edges of overlap."
        ) as vo:
            self.add(obs_tag())
            self.play(FadeIn(A), FadeIn(labs), Create(tenth), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(*[FadeIn(dg[0]) for dg in dots], FadeIn(side[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(dg[1:]) for dg in dots], FadeIn(side[1]))
        self.clear_scene()

    def numbers(self):
        d = load("obs")
        ip = d["ipw"]
        rows = fit_rows(VGroup(
            label(rf"IPW (Hajek): \ ${ip['est']:.2f}$ \ [{ip['lo']:.1f}, \ {ip['hi']:.1f}]", font_size=26, color=PSC),
            label(rf"the truth: \ ${d['ate']:.2f}$", font_size=26, color=TRUEC),
            label(rf"largest weight {ip['max_weight']:.0f}; \ effective sizes {ip['ess1']:,.0f} and {ip['ess0']:,.0f} of about 1,500 each", font_size=26, color=MISSC),
            label(r"a few patients far from overlap carry much of the answer", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The weighted estimate is minus " + say(-ip["est"], 1) + ", <bookmark mark='b'/> against the "
            "true minus " + say(-d["ate"], 1) + ": much better than the naive comparison, but in this sample its interval "
            "misses the truth. <bookmark mark='c'/> The largest weight is " + f"{ip['max_weight']:.0f}" + ", and the weights "
            "are so uneven that each arm's fifteen hundred patients count as about seven hundred. <bookmark mark='d'/> A few "
            "patients at the edges of overlap carry much of the answer, which is IPW's characteristic weakness."
        ) as vo:
            self.add(obs_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def weights(self):
        rows = fit_rows(VGroup(
            label(r"remedies for extreme weights:", font_size=26),
            label(r"trim the sample to overlap \ (Crump et al. 2009): \ a different estimand", font_size=26, color=TAUC),
            label(r"truncate the weights: \ less variance, \ some bias", font_size=26, color=GREY_A),
            label(r"overlap weights $e(1 - e)$ \ (Li, \ Morgan \& Zaslavsky 2018): \ the effect where both treatments happen", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> There are standard remedies for extreme weights. <bookmark mark='b'/> Trim the sample to "
            "the region of good overlap, as Richard Crump and colleagues proposed in 2009, accepting that the estimate then "
            "describes that region only. <bookmark mark='c'/> Truncate the largest weights, trading variance for some bias. "
            "<bookmark mark='d'/> Or use overlap weights, proportional to e times one minus e, which Fan Li, Kari Lock Morgan "
            "and Alan Zaslavsky showed in 2018 target the effect in the population where both treatments are plausible, and "
            "balance the covariate means exactly."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = board_rows("naive difference in means", "IPW, \\ logistic")
        b = load("board")["rows"]
        ipw = next(r for r in b if r["method"].startswith("IPW"))
        verdict = ipw["verdict"]
        text = ("<bookmark mark='a'/> On the Board, over five hundred observational studies of two thousand patients each. "
                "The naive difference in means: broken. <bookmark mark='b'/> IPW with a logistic propensity score covers "
                + f"{100 * ipw['achieved']:.0f}" + " percent of the time: " + verdict + ".")
        if verdict != "kept":
            text += " Even with a correctly specified propensity model, its variance estimate struggles with the extreme weights."
        show_board(self, rows, text, [("a", [0]), ("b", [1])])
