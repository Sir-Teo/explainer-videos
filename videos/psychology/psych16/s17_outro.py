from __future__ import annotations

from videos.psychology.psych16.common import *  # noqa: F403

PROBLEMS = [
    r"Under Rescorla-Wagner with $\alpha\beta = 0.2$ and $\lambda = 1$, \ find $V$ after $n$ reinforced trials from "
    r"$V = 0$, \ and the number of trials to reach 0.9.",
    r"Show that the rule is gradient descent on $\tfrac12(\lambda - \sum_i x_i V_i)^2$, \ and say what step size "
    r"$\alpha\beta$ plays.",
    r"Solve for the asymptotes of $V_C$ and $V_X$ when trials with the cue occur with probability $q$, \ and show "
    r"that $V_X = \Delta P$ for every $q$.",
    r"In an overexpectation design, \ A and B each reach $V = 1$ alone. \ Find where they end after many AB$+$ "
    r"trials, \ and why.",
    r"Show that melioration on two variable-interval keys stops where $R_L/B_L = R_R/B_R$, \ and that this is the "
    r"matching law.",
    r"With \texttt{explainer.psychology.psyche.conditioning}: \ run renewal in the AAA, \ ABA, \ ABC and AAB designs, "
    r"\ and change the model so that AAB is weaker than ABC.",
    r"$\star$ \ Design an experiment that tells Mackintosh's attention from Pearce and Hall's, \ and say what each "
    r"predicts.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.score()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def recap(self):
        items = [
            (r"a response that comes, \ goes, \ and comes back", YOU),
            (r"Pavlov: \ signals come to predict; \ the response prepares, \ it does not substitute", CS),
            (r"Thorndike and Skinner: \ consequences shape action; \ schedules leave signatures", CR),
            (r"Little Albert: \ a demonstration, \ retold larger than it was", GREY_A),
            (r"contingency, \ not pairing: \ Rescorla's random control, \ and $\Delta P$", US),
            (r"blocking: \ learning is driven by surprise", CUE_A),
            (r"Rescorla-Wagner: \ gradient descent on a prediction error, \ with its asymptote at $\Delta P$", CR),
            (r"extinction is new learning bound to context: \ renewal, \ recovery, \ relapse", INHIB),
            (r"attention, \ time and choice: \ learned $\alpha$, \ scalar timing, \ matching by melioration", CONTEXT),
            (r"biology sets limits: \ taste and sickness, \ instinctive drift, \ learning by watching", US),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=30, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 16, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part sixteen in ten lines. <bookmark mark='a'/> A conditioned response comes, goes in extinction, and "
            "comes back. Pavlov's signals come to predict, and the response prepares the animal for what's coming. "
            "Thorndike and Skinner showed consequences shaping action, and schedules of reward leaving their "
            "signatures. Little Albert was a demonstration, retold larger than it was. Rescorla showed that "
            "learning follows contingency, not pairing, and Kamin that it is driven by surprise. The Rescorla-Wagner "
            "rule is gradient descent on a prediction error, and its asymptote is the contingency. Extinction is new "
            "learning tied to its context, which is why fears return. Attention is learned, time is measured on a "
            "scale of its own, and choices match their rewards by melioration. And biology sets limits: taste goes "
            "with sickness, animals drift back to instinct, and people learn by watching."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=44.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"a threshold counted in quanta; \ colour a matrix; \ learning as gradient descent on surprise",
             STATUS_COLOR["replicated"]),
            (r"experiments by the dozen: \ lots, \ lesions, \ twins, \ a cave, \ a random control",
             STATUS_COLOR["replicated"]),
            (r"cue weights read from choices, \ never from reports; \ and illusions that knowing does not undo",
             STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> Today the first objection, that mathematics can't apply to the mind, "
            "lost more ground than in any part so far. One line of algebra, a gradient on a squared error, predicts "
            "blocking, inhibition, overexpectation and Rescorla's ten groups. <bookmark mark='b'/> And the second "
            "objection, that the mind can't be experimented on, met Rescorla's random control: a design that "
            "separates pairing from prediction, which no amount of watching could have done."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows], FadeIn(board.rows[1].reply),
                      FadeIn(board.rows[2].reply))
            vo.wait_until("a")
            self.play(Indicate(board.rows[0].objection, color=KANT), FadeIn(board.rows[0].reply, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(Indicate(board.rows[1].objection, color=KANT))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"prediction errors in dopamine neurons", [17]),
            (r"attention learned from prediction", [18]),
            (r"memory, \ rewritten when it is used", [21]),
            (r"choices over time", [26]),
            (r"fear, \ exposure and relapse", [40]),
            (r"addiction", [41]),
            (r"products designed around habits", [52]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Prediction errors in the firing of dopamine neurons are "
            "next time, Part 17. Attention learned from prediction is Part 18. Memories rewritten each time they're "
            "used are Part 21. Choices over time are Part 26. Fear, exposure and relapse are Part 40, addiction is "
            "Part 41, and products designed around our habits are Part 52."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=12.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One runs the rule by "
            "hand. One derives it as gradient descent. One proves that its asymptote is the contingency. One works "
            "out overexpectation. One derives the matching law from melioration. One uses Psyche to fix the model's "
            "mistake about renewal. And the last, with the star, asks you to design the experiment that separates the "
            "two theories of attention. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"M. E. Bouton, \emph{Learning and Behavior: A Contemporary Synthesis} (2nd ed., 2016)",
             r"I. P. Pavlov, \emph{Conditioned Reflexes} (1927); \ D. P. Todes, \emph{Ivan Pavlov} (2014)",
             r"R. A. Rescorla, \ Pavlovian conditioning: \ it's not what you think it is (1988)"],
            [r"E. L. Thorndike (1898); \ J. B. Watson \& R. Rayner (1920); \ B. Harris (1979)",
             r"B. F. Skinner (1938); \ C. B. Ferster \& B. F. Skinner (1957)",
             r"R. A. Rescorla (1968); \ L. J. Kamin (1969); \ R. A. Rescorla \& A. R. Wagner (1972)",
             r"R. E. Lubow \& A. U. Moore (1959); \ M. E. Bouton \& R. C. Bolles (1979); \ E. F. Kremer (1978)",
             r"N. J. Mackintosh (1975); \ J. M. Pearce \& G. Hall (1980); \ C. R. Gallistel \& J. Gibbon (2000)",
             r"R. J. Herrnstein (1961); \ W. M. Baum (1979); \ R. J. Herrnstein \& D. Prelec (1991)",
             r"J. Garcia \& R. A. Koelling (1966); \ K. \& M. Breland (1961); \ A. Bandura et al.\ (1961)",
             r"T. Maes et al.\ (2016); \ C. J. Mitchell et al.\ (2009); \ S. J. Gershman et al.\ (2010)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Mark Bouton's Learning and "
            "Behavior is the place to start."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act IV begins: \ learning and memory", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 17", font_size=32, color=GREY_B), label(r"Reward and Prediction", font_size=50),
                     wrapped_label(r"A monkey, \ a drop of juice, \ and a neuron that fires at surprise.", 6.0, 28,
                                   GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "That opens Act Four, on learning and memory. <bookmark mark='a'/> Rescorla and Wagner wrote their rule "
            "for trials, as if nothing happened between the start of a signal and the reward. "
            "<bookmark mark='b'/> Next time we let time back in, and the same idea, learning from errors in "
            "prediction, becomes temporal-difference learning. In the 1990s it turned up in the firing of single "
            "dopamine neurons in a monkey's brain. It's Part 17: reward and prediction."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
