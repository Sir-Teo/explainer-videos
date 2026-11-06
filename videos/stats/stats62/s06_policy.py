from __future__ import annotations

import numpy as np

from videos.stats.stats62.common import *  # noqa: F403


class Policy(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter five. Policy learning: whom should we treat, and how good is the rule we learned?", 5,
                            r"Policy learning", r"From effects to decisions", lit=(2018,))
        self.problem()
        self.ewm()
        self.scores()
        self.chart()
        self.curse()
        self.ope()
        self.board()
        self.winners()
        self.regret()

    def problem(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Part thirty-six estimated how effects vary with covariates. A decision-maker needs "
            "something else: a rule saying whom to treat. <bookmark mark='b'/> A policy pi maps covariates to a treatment. "
            "Its value is the mean outcome if everyone followed it. <bookmark mark='c'/> The best policy in a class "
            "maximizes the value, and the regret of a learned policy is how much value it gives up. <bookmark mark='d'/> "
            "Plugging in an estimate of the effect function and treating where it is positive can be far from optimal if "
            "the class of rules is restricted, say to rules a clinic can follow.",
            [(r"\text{policy}", r":", r"\pi: x \mapsto \{0, 1\}", 40),
             (r"\text{value}", r":", r"V(\pi) = E[Y(\pi(X))]", 40),
             (r"\text{regret}", r":", r"\max_{\pi' \in \Pi} V(\pi') - V(\hat\pi)", 40),
             (r"\text{constraint}", r":", r"\Pi \text{ simple, \ interpretable}", 40)],
            [r"a decision", r"the welfare", r"the target", r"thresholds, \ trees"],
            colors=[(2, IDC)])

    def ewm(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Toru Kitagawa and Aleksey Tetenov's empirical welfare maximization, in 2018: choose the "
            "rule in the class that maximizes an estimate of its value. <bookmark mark='b'/> With known propensities, an "
            "inverse-weighting estimate works, and the regret shrinks like root of the class's VC dimension over n, Part "
            "fifty-four's rate. <bookmark mark='c'/> Susan Athey and Stefan Wager, in 2021, replaced it by doubly robust "
            "scores, with cross-fitted nuisance estimates, so the same rate holds in observational data with estimated "
            "propensities. <bookmark mark='d'/> Maximizing over a class is a weighted classification problem: treat where "
            "the score is positive, as far as the class allows.",
            [(r"\text{EWM}", r":", r"\hat\pi = \arg\max_{\pi \in \Pi} \tfrac1n\sum_i \Gamma_i\,\pi(X_i)", 40),
             (r"\text{regret}", r"\lesssim", r"\sqrt{\mathrm{VC}(\Pi)/n}", 40),
             (r"\Gamma_i", r"=", r"\hat\mu_1 - \hat\mu_0 + \frac{A(Y - \hat\mu_1)}{\hat e} - \frac{(1 - A)(Y - \hat\mu_0)}{1 - \hat e}", 34),
             (r"\text{so}", r":", r"\text{weighted classification}", 40)],
            [r"Kitagawa \& Tetenov (2018)", r"Part 54", r"Athey \& Wager (2021)", r"a reduction"],
            colors=[(0, IDC)])

    def scores(self):
        d = load("policy")
        self.lad_voiceover(
            f"<bookmark mark='a'/> A simulation where the right answer is known. A covariate x uniform on minus one to one; a "
            f"randomized treatment; an effect of a quarter of x minus a tenth. <bookmark mark='b'/> The best rule treats "
            f"only when x exceeds 0.4, and gains {say(d['best'], 4)} over treating no one: a small effect, as real ones often "
            f"are. <bookmark mark='c'/> With four hundred units, the doubly robust scores are noisy. <bookmark mark='d'/> "
            f"The class is threshold rules: treat when x is above, or below, some cut.",
            [(r"\text{model}", r":", r"Y = X + A(0.25X - 0.1) + \varepsilon, \ \ X \sim U(-1, 1)", 38),
             (r"\text{best rule}", r":", rf"\text{{treat iff }} X > 0.4; \ \ \text{{gain}} \ {d['best']:.4f}", 40),
             (r"n = 400", r":", r"\text{noisy scores}", 40),
             (r"\Pi", r":", r"\text{threshold rules, \ either direction}", 40)],
            [r"randomized", r"the oracle", r"signal $\ll$ noise", r"a simple class"],
            colors=[(1, GOLDC)])

    def chart(self):
        d = load("policy")
        x, G = np.asarray(d["x"]), np.asarray(d["G"])
        o = np.argsort(x)
        cs = np.cumsum(G[o][::-1])[::-1] / len(x)  # value of treating x >= x_(k)
        lo_y = float(min(cs.min(), -0.1)) - 0.02
        A = axes([-1, 1], [lo_y, 0.12], x_length=7.4, y_length=4.4, xlabel=r"cut $c$: \ treat if $x \ge c$", ylabel=r"estimated gain over treating no one",
                 xticks=[-1, -0.5, 0, 0.5, 1], yticks=[-0.1, -0.05, 0, 0.05, 0.1], center=[-2.5, 0.2, 0])
        ax = A.ax
        est = polyline(ax, x[o], cs, TRTC, 2.5)
        xs = np.linspace(-1, 1, 200)
        tv = np.array([np.mean((0.25 * np.linspace(-1, 1, 4001) - 0.1) * (np.linspace(-1, 1, 4001) >= c)) for c in xs])
        tru = curve(ax, xs, tv, GOLDC, 3.5)
        cut = DashedLine(ax.c2p(d["rule_c"], lo_y), ax.c2p(d["rule_c"], 0.12), color=TRTC, stroke_width=2)
        zero = DashedLine(ax.c2p(-1, 0), ax.c2p(1, 0), color=GREY_B, stroke_width=1.2)
        side = side_groups([
            [(r"gold: \ the true value of each cut", GOLDC), (rf"best at 0.4: \ {d['best']:.4f}", GOLDC)],
            [(r"orange: \ the estimate from one sample", TRTC)],
            [(rf"EWM picks $c = {d['rule_c']:.2f}$", TRTC), (rf"estimated gain {d['value_est']:.4f}", TRTC), (rf"true gain {d['value_true']:.4f}", GOLDC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> For rules that treat everyone above a cut, the gold curve is each cut's true value: it "
            f"peaks at 0.4. <bookmark mark='b'/> The orange curve is one sample's estimate, the running sum of the scores: "
            f"jagged, because each score is noisy. <bookmark mark='c'/> EWM picks the cut where the orange curve is highest, "
            f"{say(d['rule_c'], 2)}. Its estimated gain is {say(d['value_est'], 4)}; its true gain, {say(d['value_true'], 4)}. The "
            f"maximum of a noisy curve is biased upward."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(Create(tru), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(est), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(cut), FadeIn(side[2]))
        self.clear_scene()

    def curse(self):
        d = load("policy")
        self.lad_voiceover(
            f"<bookmark mark='a'/> That upward bias is the winner's curse of Part fifty-six, in a new place. <bookmark "
            f"mark='b'/> Over {d['reps']} samples, the in-sample estimate of the chosen rule's value exceeds its true value "
            f"by {say(d['gap_naive'], 3)} on average, three times the best possible gain. <bookmark mark='c'/> The fix is the "
            f"one from Part fifty-six: learn the rule on one half of the data, and evaluate it on the other half, which "
            f"played no part in choosing it. <bookmark mark='d'/> The honest estimate's average error is "
            f"{say(d['gap_split'], 4)}.",
            [(r"\text{in-sample}", r":", r"\hat V(\hat\pi) \text{ biased upward}", 40),
             (r"\text{bias}", r":", rf"+{d['gap_naive']:.3f} \ \text{{on average}}", 40),
             (r"\text{fix}", r":", r"\text{learn on one half, \ evaluate on the other}", 40),
             (r"\text{honest error}", r":", rf"{d['gap_split']:+.4f}", 40)],
            [r"Part 56's winner's curse", rf"{d['reps']} samples", r"sample splitting", r"unbiased"],
            colors=[(1, NAIVEC), (3, IDC)])

    def board(self):
        br = load("board")["rows"]
        show_board(self, board_rows("in-sample", "one half"),
                   f"<bookmark mark='a'/> On the Board: the ninety-five percent interval for the learned rule's value, computed "
                   f"on the data that chose it, covers {100 * br[2]['achieved']:.1f} percent of the time: broken. <bookmark "
                   f"mark='b'/> Learned on one half and evaluated on the other, it covers {100 * br[3]['achieved']:.1f} percent: "
                   f"kept.", [("a", [0]), ("b", [1])])

    def regret(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Beyond thresholds. <bookmark mark='b'/> Policy trees, of fixed depth, give rules a clinic "
            "can read: Athey and Wager's method finds the best tree for the doubly robust scores exactly. <bookmark "
            "mark='c'/> Constraints, such as a budget on how many can be treated, or fairness requirements, change the class "
            "but not the method. <bookmark mark='d'/> And with adaptive data, from Part fifty-eight's bandits, the scores "
            "must be reweighted, or the value estimates inherit the adaptivity's bias.",
            [(r"\text{policy trees}", r":", r"\text{readable, \ exactly optimized}", 40),
             (r"\text{constraints}", r":", r"\text{budgets, \ fairness}", 40),
             (r"\text{same method}", r":", r"\text{a different class}", 40),
             (r"\text{adaptive data}", r":", r"\text{reweighted scores}", 40)],
            [r"Athey \& Wager", r"Part 63", r"weighted classification", r"Part 58"],
            colors=[(0, IDC)])

    def ope(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Evaluating a policy without deploying it is off-policy evaluation. <bookmark mark='b'/> "
            "The doubly robust scores already do it: the average score of those a new policy would treat estimates its "
            "gain, from data collected under another policy. <bookmark mark='c'/> It needs overlap: the old policy must "
            "sometimes have done what the new one would do. A deterministic old policy cannot evaluate any other. <bookmark "
            "mark='d'/> Recommender systems and online platforms evaluate new rules this way, from logs of randomized or "
            "bandit decisions, Part fifty-eight's adaptive experiments.",
            [(r"\text{off-policy}", r":", r"\hat V(\pi) \text{ from data under } \pi_0", 40),
             (r"\text{estimator}", r":", r"\text{doubly robust scores}", 40),
             (r"\text{needs}", r":", r"\pi_0(a \mid x) > 0 \text{ wherever } \pi(x) = a", 40),
             (r"\text{used}", r":", r"\text{recommender systems, \ platforms}", 40)],
            [r"no deployment", r"Dud\'ik et al. (2011)", r"overlap", r"Part 58"],
            colors=[(2, NAIVEC)])

    def winners(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Splitting costs half the data. Part fifty-six offers alternatives. <bookmark mark='b'/> "
            "Isaiah Andrews, Toru Kitagawa and Adam McCloskey's inference on winners, from 2024, gives intervals for the "
            "value of the selected option using all the data, by conditioning on the selection event or by a hybrid "
            "projection. <bookmark mark='c'/> For a finite class of candidate policies, the learned policy is exactly a "
            "winner among them. <bookmark mark='d'/> Cross-fitting, rotating the roles of the halves and averaging, recovers "
            "most of the efficiency, though its intervals need care, because the folds' rules differ.",
            [(r"\text{splitting}", r":", r"\text{honest, \ but half the data}", 40),
             (r"\text{inference on winners}", r":", r"\text{condition on the selection}", 40),
             (r"\text{finite class}", r":", r"\text{the learned rule is a winner}", 40),
             (r"\text{cross-fitting}", r":", r"\text{efficiency, \ with care}", 40)],
            [r"the price", r"Andrews, \ Kitagawa \& McCloskey (2024)", r"Part 56", r"rotate and average"],
            colors=[(1, IDC)])
