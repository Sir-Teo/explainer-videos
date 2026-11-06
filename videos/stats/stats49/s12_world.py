from __future__ import annotations

from videos.stats.stats49.common import *  # noqa: F403


class WorldTest(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_world()
        self.table()
        self.board()
        self.why()
        self.practice()

    def card(self):
        card = chapter_card(11, r"The World test", r"Plug-in, \ one-step and TMLE, \ on the World", part=PART)
        with self.voiceover("Chapter eleven. The World test: plug-in, one-step and targeted estimators, on the World."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def setup_world(self):
        rows = fit_rows(VGroup(
            label(r"Part 36's observational world: \ 2,000 patients, \ doctors choose who gets the drug", font_size=26),
            label(r"more often for higher pressure, \ age and BMI: \ confounding \ (propensities 0.2 to 0.98)", font_size=26, color=NUIC),
            label(r"the true ATE: \ known, \ from the World's science table", font_size=26, color=TANC),
            label(r"outcomes by 15-nearest neighbours: \ flexible, \ slow, \ biased; \ propensity by logistic regression", font_size=26, color=GRADC),
            label(r"300 samples; \ nominal 90\% intervals; \ the influence-function SE throughout", font_size=26, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The final test uses Part thirty-six's observational world: two thousand patients, and "
            "doctors who decide who gets the blood-pressure drug. <bookmark mark='b'/> They prescribe more often for higher "
            "pressure, greater age and higher body mass, which also predict the outcome: confounding. Here the doctors are "
            "a little gentler than in Part thirty-six, so that propensities stay between about point two and point nine "
            "eight. <bookmark mark='c'/> The World knows every patient's effect, so the true average treatment effect is "
            "known. <bookmark mark='d'/> The outcome regressions are estimated by fifteen nearest neighbours, a deliberately "
            "crude learner: flexible, slow and biased, like machine learning in a hurry. The propensity is fitted by logistic "
            "regression. <bookmark mark='e'/> Three hundred samples, ninety percent intervals, and the influence-function "
            "standard error for every method."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def table(self):
        d = load("board")
        names = [r"plug-in", r"IPW, \ logistic", r"one-step, \ cross-fitted", r"TMLE, \ cross-fitted", r"one-step, \ $k$-NN propensity too"]
        rows = [[r"estimator \ ($k$-NN nuisances)", r"90\% coverage", r"verdict"]]
        for nm, r in zip(names, d["rows"]):
            rows.append([nm, f"{100 * r['achieved']:.1f}\\%", r["verdict"]])
        tab = table_rows(rows, font_size=30, col_buff=1.0, row_buff=0.36, colors=[GREY_B, PLUGC, None, OSC, TMLEC, NUIC])
        tab.move_to([0, 0.7, 0])
        r = d["rows"]
        b, sd = d["bias"], d["sd"]
        with self.voiceover(
            f"<bookmark mark='a'/> The results. The plug-in covers {100 * r[0]['achieved']:.0f} percent: the nearest-neighbour "
            f"regressions are biased, and the plug-in passes their bias straight through, about {say(b['plugin'], 1)} millimetres "
            f"of mercury, several of its standard errors. Inverse probability weighting with the logistic propensity covers "
            f"{100 * r[1]['achieved']:.0f} percent: valid, because the propensity model happens to be right, but its interval "
            f"is the widest. The cross-fitted one-step and targeted estimators cover {100 * r[2]['achieved']:.0f} and "
            f"{100 * r[3]['achieved']:.0f} percent, with biases of {say(b['os'], 2)} and {say(b['tmle'], 2)}. And when the "
            f"propensity is also estimated by nearest neighbours, the product of two slow errors is no longer small: the "
            f"one-step estimator's bias grows to {say(b['os_knn'], 2)} and its coverage falls to {100 * r[4]['achieved']:.0f} percent."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"the World: \ 300 samples")))
        self.wait(2.0)
        self.clear_scene()

    def board(self):
        rows = board_rows("doctors choose")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Coverage Board. The plug-in, broken by its first-order bias, and inverse "
                   "probability weighting, which keeps its promise conservatively because its single nuisance is right. "
                   "<bookmark mark='b'/> The efficient estimators, cross-fitted, which need only the product of two errors to be "
                   "small, and keep the promise. <bookmark mark='c'/> And the same efficient estimator with both nuisances crude: "
                   "double robustness cannot rescue two slow errors.",
                   [("a", [0, 1]), ("b", [2, 3]), ("c", [4])])

    def why(self):
        d = load("board")
        b, sd = d["bias"], d["sd"]
        rows = [
            cmath(r"\text{plug-in}", r":", rf"\text{{bias }} {b['plugin']:+.2f}, \ \text{{SD }} {sd['plugin']:.2f}: \ \text{{first order in }} \|\hat\mu - \mu\|", font_size=30),
            cmath(r"\text{one-step}", r":", rf"\text{{bias }} {b['os']:+.2f}, \ \text{{SD }} {sd['os']:.2f}: \ \|\hat e - e\| \cdot \|\hat\mu - \mu\|", font_size=30),
            cmath(r"\text{TMLE}", r":", rf"\text{{bias }} {b['tmle']:+.2f}, \ \text{{SD }} {sd['tmle']:.2f}: \ \text{{the same product, \ a plug-in}}", font_size=30),
            cmath(r"k\text{-NN for both}", r":", rf"\text{{bias }} {b['os_knn']:+.2f}: \ \text{{the product of two slow errors}}", font_size=30),
        ]
        rows[1][-1].set_color(OSC)
        rows[2][-1].set_color(TMLEC)
        rows[3][-1].set_color(NUIC)
        whys = [why(r"chapter 6: \ the plug-in's bias"), why(r"chapter 7: \ a product"), why(r"chapter 6: \ targeting"), why(r"chapter 8: \ $a + b < 1/2$")]
        with self.voiceover(
            f"<bookmark mark='a'/> Each result is a chapter of this part. The plug-in's bias, {say(b['plugin'], 2)}, is the "
            f"first-order error of its regressions, chapter six's warning. <bookmark mark='b'/> The one-step estimator's bias, "
            f"{say(b['os'], 2)}, is a product of the regressions' error and the propensity's, and the logistic propensity's "
            f"error is small: chapter seven. <bookmark mark='c'/> The targeted estimator has the same structure and, here, a "
            f"slightly smaller spread, {say(sd['tmle'], 2)} against {say(sd['os'], 2)}. <bookmark mark='d'/> And with two "
            f"crude nuisances the product is no longer negligible: chapter eight's product-rate condition, failing in front "
            f"of us."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def practice(self):
        rows = fit_rows(VGroup(
            label(r"in practice:", font_size=28, color=GREY_A),
            label(r"1. \ write down $\phi^*$ for your estimand \ (or look it up: \ Kennedy 2022)", font_size=26, color=EFFC),
            label(r"2. \ estimate every nuisance in it, \ as well as you can, \ with cross-fitting", font_size=26, color=GRADC),
            label(r"3. \ one-step or TMLE; \ SE from the empirical variance of $\hat\phi^*$", font_size=26, color=OSC),
            label(r"4. \ check overlap: \ the bound has $1/e$ in it, \ and no method escapes it", font_size=26, color=NUIC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The practical recipe that falls out of the theory. <bookmark mark='b'/> Write down the "
            "efficient influence function for the quantity you want, or look it up; Edward Kennedy's 2022 review collects "
            "many. <bookmark mark='c'/> Estimate every nuisance function in it as well as you can, with cross-fitting. "
            "<bookmark mark='d'/> Use the one-step or the targeted estimator, with the standard error from the empirical "
            "variance of the estimated influence function. <bookmark mark='e'/> And check overlap first: the bound has one "
            "over the propensity in it, and no estimator, however clever, can escape it."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
