from __future__ import annotations

from videos.psychology.psych48.common import *  # noqa: F403

PROBLEMS = [
    r"A softmax chooser with $\beta = 5$ values two arms at 0.6 and 0.4. \ Find the probability of choosing the first.",
    r"A Q-learner with $\alpha = 0.3$ values an arm at 0.5, \ chooses it, \ and is rewarded. \ Find the new value.",
    r"A model gave a person's three choices probabilities 0.7, \ 0.6 and 0.8. \ Find the log-likelihood.",
    r"Two models of 200 choices: \ log-likelihood $-60$ with 2 parameters, \ $-58$ with 3. \ Which does BIC prefer?",
    r"Learners jump from 10\% to 90\% correct with probability 0.1 per trial. \ What does the average curve show on "
    r"trial 10?",
    r"A person's log-odds learning rate is $-1.5$ with variance 0.5; \ the population's mean is $-0.7$ with "
    r"variance 0.25. \ Find the hierarchical estimate.",
    r"$\star$ \ Plan the checks for a new model of a new task: \ simulations, \ recovery, \ model recovery, \ a "
    r"posterior predictive check, \ and the number of trials.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.your_numbers()
        self.recap()
        self.score()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def your_numbers(self):
        r, c, p, g = load("recovery"), load("confusion"), load("practice"), load("group")
        m = np.isclose(r["true_alpha"], 0.4)
        err = float(np.median(np.abs(r["est_alpha"][m] - 0.4)))
        M = np.asarray(c["confusion"])
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for k, q, ans, col in (
                (r"1", r"a learning rate of 0.4 from 200 choices", rf"typically within {err:.2f}", PERSON),
                (r"2", r"perseverating learners identified correctly", rf"{100 * M[3, 3]:.0f}\%", MODEL),
                (r"3", r"the curve that fits the average of exponential learners", r"a power law", AUTH),
                (r"4", r"error in each learning rate, \ alone and as a population",
                 rf"{g['rmse_ml']:.2f} $\to$ {g['rmse_eb']:.2f}", GOOD)):
            rows.add(VGroup(label(k, font_size=30, color=col), wrapped_label(q, 6.4, 22, WHITE),
                            label(ans, font_size=24, color=col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"a model earns trust by the checks it passes, \ not by its fit", 12.0, 22,
                             YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> A learning rate of zero point four, from two hundred "
            "choices, is typically recovered within a few hundredths. Model comparison identified more than nine in "
            "ten perseverating learners. The average of exponential learners is best fitted by a power law. And "
            "fitting thirty people as a population cut the error in each learning rate by almost half. "
            "<bookmark mark='b'/> A model earns trust by the checks it passes, not by its fit."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=9.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"an average can describe no one: \ Estes's jumping learners", WHITE),
            (r"a cognitive model is a program from parameters to behaviour", MODEL),
            (r"maximum likelihood, \ with restarts and bounds", MODEL),
            (r"recover parameters from simulations before trusting them", PERSON),
            (r"some parameters trade off along a ridge", PERSON),
            (r"compare models by penalized fit or prediction", SYMP),
            (r"check that comparison can recover the true model", SYMP),
            (r"a good fit can be bad: \ ask what the model rules out", AUTH),
            (r"posterior predictive checks: \ does it make the effect?", AUTH),
            (r"hierarchical fits borrow strength across people", GOOD),
            (r"rational analysis asks why; \ networks ask how", GOOD),
            (r"prediction is not yet explanation", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 48, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part forty-eight in twelve lines. <bookmark mark='a'/> An average can describe no one. A cognitive model "
            "is a program from parameters to behaviour, fitted by maximum likelihood with restarts and bounds. "
            "Recover parameters from simulations before trusting them, and watch for parameters that trade off along "
            "a ridge. Compare models by penalized fit or by prediction, and check that the comparison can recover the "
            "true model. A good fit can be bad, so ask what the model rules out, and whether it makes the effect. "
            "Hierarchical fits borrow strength across people. Rational analysis asks why, networks ask how. And "
            "prediction is not yet explanation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=38.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"likelihoods, \ recovery, \ model comparison and hierarchy, \ all run in the open",
             STATUS_COLOR["replicated"]),
            (r"models tested by the effects they must produce, \ on data they did not see", STATUS_COLOR["replicated"]),
            (r"models of choices, \ not of reports: \ the objection does not arise here", STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection met likelihoods, recovery, model comparison and "
            "hierarchy, all run in the open. Green. <bookmark mark='b'/> The second met models tested by the effects "
            "they must produce, on data they didn't see. Green. <bookmark mark='c'/> And the third, about "
            "introspection: these are models of choices, not of reports, so the objection doesn't arise. Green."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"models of the brain's data", [49]),
            (r"the weight of evidence across studies", [50]),
            (r"computational psychiatry, \ with recovery first", [59]),
            (r"language models as minds", [60]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Models of the brain's data are next, in Part 49. The weight of "
            "evidence across studies is Part 50. Computational psychiatry, with recovery first, is Part 59. And "
            "language models as minds are Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=7.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One computes a softmax "
            "choice. One updates a value. One computes a log-likelihood. One compares two models by BIC. One averages "
            "jumping learners. One shrinks a learning rate. And the last, with the star, asks you to plan every check "
            "for a new model of a new task. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"S. Farrell \& S. Lewandowsky, \ \emph{Computational Modeling of Cognition and Behavior} (2018)",
             r"M. D. Lee \& E.-J. Wagenmakers, \ \emph{Bayesian Cognitive Modeling} (2013)",
             r"R. C. Wilson \& A. G. E. Collins, \ Ten simple rules for the computational modeling of behavioral data "
             r"(2019)"],
            [r"W. K. Estes (1956); \ A. Newell \& P. S. Rosenbloom (1981); \ A. Heathcote et al.\ (2000)",
             r"S. Roberts \& H. Pashler (2000); \ M. A. Pitt \& I. J. Myung (2002)",
             r"S. Palminteri, \ V. Wyart \& E. Koechlin (2017)",
             r"J. R. Anderson (1990); \ F. Lieder \& T. L. Griffiths (2020)",
             r"D. E. Rumelhart, \ J. L. McClelland \& the PDP Group (1986)",
             r"M. Binz \& E. Schulz (2023); \ M. K. Eckstein et al.\ (2022)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Farrell and Lewandowsky's book "
            "teaches the craft; Lee and Wagenmakers teach the Bayesian version; and Wilson and Collins's ten rules fit "
            "on a page and should be read before any fit."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act XI: \ the graduate toolkit, \ 5 of 7", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 49", font_size=32, color=GREY_B),
                     label(r"Modelling the Brain's Data", font_size=36),
                     wrapped_label(r"What must be true for a brain map to be evidence?", 6.0, 26, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Five parts of the graduate toolkit done. <bookmark mark='a'/> This one opened the fitting harness the "
            "whole series has used. <bookmark mark='b'/> Next, the brain. Seventy teams were given one brain-imaging "
            "dataset and reached different answers. What must be true for a brain map to be evidence? Part 49: "
            "modelling the brain's data."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
