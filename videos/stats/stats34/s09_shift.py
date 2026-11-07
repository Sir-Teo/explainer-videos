from __future__ import annotations

import numpy as np

from videos.stats.stats34.common import *  # noqa: F403


class Shift(VoiceoverScene):
    def construct(self):
        self.card()
        self.covariate()
        self.ages()
        self.unweighted()
        self.weighted()
        self.result()
        self.board()
        self.unknown()
        self.stream()
        self.aci_rule()
        self.aci_chart()
        self.aci_bound()

    def card(self):
        card = chapter_card(8, r"Under shift", r"When the future is not exchangeable with the past", lit=(2019, 2021), part=PART)
        with self.voiceover("Chapter eight. Conformal prediction under shift."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def covariate(self):
        rows = [
            cmath(r"\text{calibration}", r":", r"(X_i, Y_i) \sim P_X \times P_{Y \mid X}", font_size=32),
            cmath(r"\text{test}", r":", r"(X, Y) \sim \tilde P_X \times P_{Y \mid X}", font_size=32),
            cmath(r"w(x)", r"=", r"d\tilde P_X / dP_X \ (x)", font_size=32),
            cmath(r"\text{exchangeability}", r":", r"\text{gone}", font_size=32),
        ]
        rows[2][-1].set_color(CALC)
        whys = [why(r"where the model was checked"), why(r"the same rule, \ different inputs"),
                why(r"the likelihood ratio"), why(r"so the quantile lemma no longer applies")]
        with self.voiceover(
            "<bookmark mark='a'/> Everything so far rested on exchangeability: the new case looks like a random draw from "
            "the same population as the calibration cases. That fails all the time. A model calibrated on one hospital's "
            "patients is used at another, with older patients. <bookmark mark='b'/> The simplest failure is covariate "
            "shift: the relationship between x and y is unchanged, but the inputs come from a different distribution. "
            "<bookmark mark='c'/> The shift is described by the likelihood ratio w of x, how much more common such inputs "
            "are in the test population than in calibration. <bookmark mark='d'/> Once w is not constant, a new case is no "
            "longer exchangeable with the old ones, and the quantile lemma no longer applies."
        ) as vo:
            intro=label('Covariate shift changes input frequencies while preserving response laws',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ages(self):
        d = load("shift")
        ag = np.asarray(d["ages"], float)
        A = axes([18, 96], [0, 0.06], x_length=7.4, y_length=4.2, xlabel=r"age", ylabel=r"share", xticks=[20, 40, 60, 80],
                 yticks=[0, 0.03, 0.06], center=[-2.0, 0.2, 0])
        ax = A.ax
        pop = density(ax, ag, np.asarray(d["pop"], float), PREDC, fill=0.3)
        sh = density(ax, ag, np.asarray(d["shifted"], float), CALC, fill=0.3)
        side = fit_rows(VGroup(
            label(r"calibration: \ all the World's adults", font_size=22, color=PREDC),
            label(r"test: \ a clinic for ages 40--60, \ mostly", font_size=22, color=CALC),
            label(r"$w(\mathrm{age})$ known: \ how the test group was drawn", font_size=22),
            label(r"incomes vary most in mid-career", font_size=22, color=MISSC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the World: the income model of chapter six, calibrated on adults of all ages. "
            "<bookmark mark='b'/> Now use it on a population tilted heavily towards ages forty to sixty, say the clients of "
            "a financial adviser. <bookmark mark='c'/> We know the tilt exactly, because we drew the test population with "
            "it. <bookmark mark='d'/> The shift matters because these are exactly the ages at which incomes vary most."
        ) as vo:
            self.add(income_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(pop), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(sh), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def unweighted(self):
        d = load("shift")
        rows = fit_rows(VGroup(
            label(r"split conformal, \ calibrated on everyone, \ used on the tilted group", font_size=26),
            label(rf"coverage: \ {100 * d['unweighted']:.1f}\% \ (promised 90\%)", font_size=26, color=MISSC),
            label(r"the threshold was set by a population with more young and old people", font_size=26, color=GREY_A),
            label(r"the fix: \ make the calibration cases look like the test population", font_size=26, color=CALC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Use the ordinary split conformal band, calibrated on everyone, on the tilted group, over "
            "two hundred repetitions. <bookmark mark='b'/> It covers " + say(100 * d["unweighted"], 1) + " percent, not "
            "ninety. <bookmark mark='c'/> The threshold was set by a population full of young adults and pensioners, whose "
            "incomes are easier to predict. <bookmark mark='d'/> The repair is to reweight the calibration cases so that, "
            "in effect, they come from the test population."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def weighted(self):
        rows = [
            cmath(r"p_i(x)", r"=", r"\dfrac{w(X_i)}{\sum_{j=1}^n w(X_j) + w(x)}, \ \ p_{n+1}(x) = \dfrac{w(x)}{\sum_j w(X_j) + w(x)}", font_size=26),
            cmath(r"\hat q(x)", r"=", r"\text{the } 1 - \alpha \text{ quantile of } \textstyle\sum_i p_i(x)\, \delta_{S_i} + p_{n+1}(x)\, \delta_{+\infty}", font_size=26),
            cmath(r"P\big(Y \in C(X)\big)", r"\ge", r"1 - \alpha \ \ \text{under the shift}", font_size=30),
            cmath(r"w \equiv 1", r"\Rightarrow", r"\text{ordinary split conformal}", font_size=30),
        ]
        rows[2][-1].set_color(BANDC)
        whys = [why(r"the test point's own weight goes at infinity"), why(r"a weighted quantile lemma"),
                why(r"Tibshirani, \ Barber, \ Cand\`es \& Ramdas (2019)"), why(r"the special case")]
        with self.voiceover(
            "<bookmark mark='a'/> Ryan Tibshirani, Barber, Candès and Ramdas showed how in 2019. Give each "
            "calibration score a weight proportional to the likelihood ratio at its x, and give the new point its own"
            " weight, <bookmark mark='b'/> placed at infinity. Take the one minus alpha quantile of this weighted "
            "distribution of scores. <bookmark mark='c'/> They proved a weighted version of the quantile lemma: the "
            "resulting band covers at least one minus alpha under the shift. <bookmark mark='d'/> When all the "
            "weights are equal, it is ordinary split conformal. The threshold now depends on x, through the new "
            "point's weight: a point with a larger target-to-calibration density ratio can require a higher "
            "threshold, possibly infinity."
        ) as vo:
            intro=label('Known density ratios reweight scores and the test-point mass',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def result(self):
        d = load("shift")
        rows = fit_rows(VGroup(
            label(rf"unweighted: \ $\hat q = {d['q']:.1f}$, \ coverage {100 * d['unweighted']:.1f}\%", font_size=26, color=MISSC),
            label(rf"weighted: \ $\hat q \approx {d['qw']:.1f}$, \ coverage {100 * d['weighted']:.1f}\%", font_size=26, color=BANDC),
            label(r"the weights raise the threshold to match the harder population", font_size=26),
        ), 12.4, 0.6, [0, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The unweighted threshold was about " + say(d["q"], 1) + " thousand dollars, and covered "
            + say(100 * d["unweighted"], 1) + " percent. <bookmark mark='b'/> The weighted threshold rises to about "
            + say(d["qw"], 1) + " thousand, and covers " + say(100 * d["weighted"], 1) + " percent. <bookmark mark='c'/> The "
            "weights simply let the calibration cases from mid-career, the ones that resemble the test population, set "
            "the threshold."
        ) as vo:
            self.add(income_tag())
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = board_rows("test ages shifted")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board, with three hundred fresh draws. Unweighted split conformal under the "
                   "shift: broken. <bookmark mark='b'/> Weighted conformal: kept.",
                   [("a", [0]), ("b", [1])])

    def unknown(self):
        rows = fit_rows(VGroup(
            label(r"$w$ unknown? \ estimate it: \ a classifier telling calibration from test inputs", font_size=26),
            label(r"$\hat w(x) = \hat P(\text{test} \mid x) / \hat P(\text{calibration} \mid x)$, \ times a constant", font_size=26, color=CALC),
            label(r"the guarantee then holds only approximately", font_size=26, color=GREY_A),
            label(r"general drift: \ coverage $\ge 1 - \alpha - \sum_i \tilde w_i\, d_{TV}(Z, Z^{(i)})$ \ (Barber et al. 2023)", font_size=26, color=PREDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Usually the likelihood ratio is unknown. It can be estimated by training a classifier to "
            "tell calibration inputs from test inputs, <bookmark mark='b'/> since the odds it assigns to test are "
            "proportional to the likelihood ratio. <bookmark mark='c'/> The guarantee then holds only as well as the "
            "classifier. <bookmark mark='d'/> For slower, general drift, Barber, Candès, Ramdas and Tibshirani showed in "
            "2023 that weighting recent cases more heavily loses coverage only in proportion to how far the data have "
            "drifted, measured in total variation. And when the drift never stops, there is another approach."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def stream(self):
        d = load("aci")
        t = np.asarray(d["scores_t"], float)
        s = np.asarray(d["scores"], float)
        A = axes([0, 3000], [0, max(10,float(s.max())*1.05)], x_length=11.0, y_length=3.6, xlabel=r"time $t$", ylabel=r"score $|y_t - \hat\mu_t|$",
                 xticks=[0, 1000, 2000, 3000], yticks=[0, 5, 10], center=[0, 0.4, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.015, color=LABC, fill_opacity=0.6) for a, b in zip(t, s)])
        sq = DashedLine(ax.c2p(300, d["static_q"]), ax.c2p(3000, d["static_q"]), color=MISSC, stroke_width=2.5)
        cal = Rectangle(width=ax.c2p(300, 0)[0] - ax.c2p(0, 0)[0], height=3.6, stroke_width=0, fill_color=CALC,
                        fill_opacity=0.12).move_to(ax.c2p(150, 5))
        foot = fit_rows(VGroup(
            label(r"a stream of scores: \ the noise triples from $t = 1{,}000$ to $2{,}000$", font_size=22),
            label(rf"static split conformal, \ calibrated on the first 300: \ $\hat q = {d['static_q']:.2f}$", font_size=22, color=MISSC),
            label(rf"coverage during the storm: \ {100 * d['static_mid']:.0f}\%", font_size=22, color=MISSC),
        ), 12.0, 0.25, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is a stream of scores, one per time step, from a forecaster whose errors suddenly "
            "triple in size at time one thousand and calm down again at two thousand: a volatile period in a market, or a "
            "new sensor that fails. <bookmark mark='b'/> A static split conformal threshold, calibrated on the first three "
            "hundred steps, <bookmark mark='c'/> covers only " + f"{100 * d['static_mid']:.0f}" + " percent of the time "
            "during the storm. No fixed threshold can be right both before and during it."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), FadeIn(dots, run_time=2.0))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(cal), Create(sq), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def aci_rule(self):
        rows = [
            cmath(r"\text{at time } t", r":", r"\hat q_t = \text{the } 1 - \alpha_t \text{ quantile of recent scores}", font_size=30),
            cmath(r"\mathrm{err}_t", r"=", r"\mathbf 1\{S_t > \hat q_t\}", font_size=32),
            cmath(r"\alpha_{t+1}", r"=", r"\alpha_t + \gamma\,(\alpha - \mathrm{err}_t)", font_size=34),
            cmath(r"\text{a miss}", r"\Rightarrow", r"\alpha_t \text{ falls: \ the next band is wider}", font_size=30),
        ]
        rows[2][-1].set_color(BANDC)
        whys = [why(r"a sliding window"), why(r"did we miss?"), why(r"Gibbs \& Cand\`es (2021)"),
                why(r"a hit nudges it back up a little")]
        with self.voiceover(
            "<bookmark mark='a'/> Isaac Gibbs and Candès proposed adaptive conformal inference in 2021. At each time,"
            " use the one minus alpha t quantile of recent scores, where alpha t is a level we keep adjusting. "
            "<bookmark mark='b'/> Record whether this step's score exceeded the threshold: a miss. <bookmark "
            "mark='c'/> Then update alpha t by a small step gamma times alpha minus the miss indicator. <bookmark "
            "mark='d'/> A miss lowers alpha t by gamma times one minus alpha, so the next band is wider; a hit raises"
            " it by gamma alpha, one ninth as much at alpha point one, so the band slowly narrows. It is the simplest"
            " feedback controller there is."
        ) as vo:
            intro=label('Adaptive conformal updates the target quantile after each miss',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def aci_chart(self):
        d = load("aci")
        rt = np.asarray(d["roll_t"], float)
        A = axes([0, 3000], [0, 1.0], x_length=11.0, y_length=3.8, xlabel=r"time $t$", ylabel=r"coverage, \ last 100",
                 xticks=[0, 1000, 2000, 3000], yticks=[0.4, 0.6, 0.8, 0.9, 1.0], yfmt=lambda v: rf"{100 * v:.0f}\%",
                 center=[0, 0.5, 0])
        ax = A.ax
        st = polyline(ax, rt, d["roll_static"], MISSC, 2.5)
        ac = polyline(ax, rt, d["roll_aci"], BANDC, 3)
        nine = DashedLine(ax.c2p(0, 0.9), ax.c2p(3000, 0.9), color=CALC, stroke_width=2)
        foot = fit_rows(VGroup(
            label(rf"static: \ {100 * d['static_cover']:.1f}\% overall, \ {100 * d['static_mid']:.0f}\% in the storm", font_size=22, color=MISSC),
            label(rf"ACI, \ $\gamma = 0.01$: \ {100 * d['aci_cover']:.1f}\% overall, \ {100 * d['aci_mid']:.1f}\% in the storm", font_size=22, color=BANDC),
        ), 12.0, 0.25, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The coverage over the last hundred steps, for both methods. <bookmark mark='b'/> The "
            "static threshold collapses to about half when the storm begins, and recovers only when it ends. <bookmark mark='c'/> Adaptive "
            "conformal dips briefly at each change, then climbs back to ninety percent within a hundred or so steps, "
            "because the misses push alpha t down until the band is wide enough. Overall it covers "
            + say(100 * d["aci_cover"], 1) + " percent."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(nine))
            vo.wait_until("b")
            self.play(Create(st), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(Create(ac), FadeIn(foot[1]))
        self.clear_scene()

    def aci_bound(self):
        rows = [
            cmath(r"\Big|\tfrac1T \textstyle\sum_{t=1}^T \mathrm{err}_t - \alpha\Big|", r"\le", r"\dfrac{\max(\alpha_1, 1 - \alpha_1) + \gamma}{\gamma\, T}", font_size=30),
            cmath(r"\text{for}", r":", r"\text{every sequence, \ even an adversary's}", font_size=30),
            cmath(r"\text{the catch}", r":", r"\text{a long-run average, \ not a probability}", font_size=30),
            cmath(r"\gamma", r":", r"\text{fast adaptation vs. a steady band}", font_size=32),
        ]
        rows[0][-1].set_color(BANDC)
        whys = [why(r"Gibbs \& Cand\`es (2021), \ Prop. 4.1"), why(r"no probability model at all"),
                why(r"the misses could bunch together"), why(r"Part 58 meets this tradeoff again")]
        with self.voiceover(
            "<bookmark mark='a'/> The guarantee is of an unusual kind. Over T steps, the miss rate is within a constant "
            "over gamma T of alpha, <bookmark mark='b'/> with infinite and empty interval conventions, for every finite-score sequence, including one chosen by an "
            "adversary who knows the method. The proof is a few lines: alpha t stays in a bounded interval, and its total "
            "movement is gamma times the sum of alpha minus the misses. <bookmark mark='c'/> The catch is that this is a "
            "long-run frequency, not a probability for any single step; misses can bunch together. <bookmark mark='d'/> "
            "And gamma trades fast adaptation against a jittery band. Part 57 develops these guarantees, and Part 58's "
            "anytime-valid inference shares their spirit."
        ) as vo:
            intro=label('Bounded level updates control long-run miss frequency',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
