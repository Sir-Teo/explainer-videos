from __future__ import annotations

import numpy as np

from videos.stats.stats62.common import *  # noqa: F403
from videos.stats.stats62.compute import _true_value


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
            "<bookmark mark='a'/> Empirical welfare maximization selects a rule with high estimated gain within a specified class. <bookmark mark='b'/> Regret bounds involving the square root of VC dimension over sample size require boundedness or suitable tails, overlap and other theorem conditions. <bookmark mark='c'/> Doubly robust, cross-fitted scores extend the approach when nuisance estimates satisfy appropriate rates and the causal assumptions hold. Cross-fitting does not repair hidden confounding or missing action support. <bookmark mark='d'/> Maximizing score-weighted treatment choices can be formulated as weighted classification under the policy constraints.",
            [(r"\text{EWM}", r":", r"\hat\pi = \arg\max_{\pi \in \Pi} \tfrac1n\sum_i \Gamma_i\,\pi(X_i)", 40),
             (r"\text{regret}", r"\lesssim", r"\sqrt{\mathrm{VC}(\Pi)/n}", 40),
             (r"\Gamma_i", r"=", r"\hat\mu_1 - \hat\mu_0 + \frac{A(Y - \hat\mu_1)}{\hat e} - \frac{(1 - A)(Y - \hat\mu_0)}{1 - \hat e}", 34),
             (r"\text{so}", r":", r"\text{weighted classification}", 40)],
            [r"Kitagawa \& Tetenov (2018)", r"Part 54", r"Athey \& Wager (2021)", r"a reduction"],
            colors=[(0, IDC)])

    def scores(self):
        d = load("policy")
        self.lad_voiceover(
            "<bookmark mark='a'/> In this randomized simulation X is uniform between minus one and one, with treatment effect a quarter X minus a tenth. <bookmark mark='b'/> The optimal upper-threshold rule treats above point four and has exact gain zero point zero two two five relative to treating nobody. <bookmark mark='c'/> Each run uses four hundred policy observations plus an independent auxiliary sample of four hundred outcomes for nuisance fitting. Treatment propensity is known to be one half. This prevents policy learning from seeing evaluation outcomes through nuisance estimates. <bookmark mark='d'/> The coverage comparison optimizes upper and lower threshold rules. The representative chart shows only the upper-threshold subfamily, so its marked cut actually maximizes the curve shown.",
            [(r"\text{model}", r":", r"Y = X + A(0.25X - 0.1) + \varepsilon, \ \ X \sim U(-1, 1)", 38),
             (r"\text{best rule}", r":", rf"\text{{treat iff }} X > 0.4; \ \ \text{{gain}} \ {d['best']:.4f}", 40),
             (r"n = 400", r":", r"\text{policy data + 400 independent nuisance-training outcomes}", 40),
             (r"\Pi", r":", r"\text{threshold rules, \ either direction}", 40)],
            [r"randomized", r"the oracle", r"signal $\ll$ noise", r"a simple class"],
            colors=[(1, GOLDC)])

    def chart(self):
        d = load("policy")
        x, G = np.asarray(d["x"]), np.asarray(d["G"])
        o = np.argsort(x)
        cs = np.cumsum(G[o][::-1])[::-1] / len(x)  # value of treating x >= x_(k)
        lo_y = float(min(cs.min(), -0.1)) - 0.02
        hi_y=float(max(cs.max(),.12))+.02
        A = axes([-1, 1], [lo_y, hi_y], x_length=7.4, y_length=4.4, xlabel=r"cut $c$: \ treat if $x \ge c$", ylabel=r"estimated gain over treating no one",
                 xticks=[-1, -0.5, 0, 0.5, 1], yticks=[-0.1, -0.05, 0, 0.05, 0.1], center=[-2.5, 0.2, 0])
        ax = A.ax
        est = polyline(ax, x[o], cs, TRTC, 2.5)
        xs = np.linspace(-1, 1, 200)
        tv = np.array([_true_value({"c":c,"s":1}) for c in xs])
        tru = curve(ax, xs, tv, GOLDC, 3.5)
        cut = DashedLine(ax.c2p(d["rule_c"], lo_y), ax.c2p(d["rule_c"], hi_y), color=TRTC, stroke_width=2)
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
            "<bookmark mark='a'/> Selecting and evaluating the same noisy maximum creates optimism. <bookmark mark='b'/> The displayed Monte Carlo comparison estimates both that optimism and coverage for the randomly learned rule's own population gain. <bookmark mark='c'/> For the split version, learn on half of the policy observations and evaluate on the other half, using nuisances fitted on the independent auxiliary sample. Ordinary two-fold nuisance fitting alone would leak evaluation outcomes into the learning scores in this design. <bookmark mark='d'/> The split estimate's average error is recorded with its Monte Carlo uncertainty. Its Wald interval is an approximation under this simulation, not a universal finite-sample guarantee.",
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
            "<bookmark mark='a'/> More complex policy classes can improve flexibility while increasing optimization and statistical difficulty. <bookmark mark='b'/> Shallow policy trees can be optimized exactly for specified finite search spaces, but general tree optimization is computationally difficult; fixed depth alone does not make every search cheap. <bookmark mark='c'/> Budget and fairness constraints alter the feasible policies and the available algorithms. <bookmark mark='d'/> Adaptive logging requires correct action probabilities, support and inference appropriate to the dependence. Reweighting alone does not guarantee a valid interval.",
            [(r"\text{policy trees}", r":", r"\text{readable; \ optimization cost depends on the search class}", 40),
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
            "sometimes have done what the new one would do. A deterministic logging policy cannot identify a new action where it supplied zero probability; policies agreeing on the observed action support are a different case. <bookmark "
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
