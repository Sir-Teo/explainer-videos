from __future__ import annotations

from videos.psychology.psych17.common import *  # noqa: F403

PROBLEMS = [
    r"With $\gamma = 0.9$ and one reward of 1 three steps after a cue, \ find the value of each step after the cue, \ "
    r"and the TD error at the cue once learning is complete.",
    r"Derive the TD error from the Bellman equation, \ and show that its expected value is zero when $V$ is correct.",
    r"On a delay line with $\alpha = 1$, \ show that the error moves back one step per trial, \ and find how many "
    r"trials it takes to reach a cue 15 steps before the reward.",
    r"Write the log-likelihood of a choice sequence under Q-learning with a softmax, \ and say why $\beta$ is hard "
    r"to recover when it is large.",
    r"Compute the successor matrix $M = (I - \gamma T)^{-1}$ for a three-state chain, \ and show how $V = Mr$ "
    r"handles a reward change but not a transition change.",
    r"With \texttt{explainer.psychology.psyche.rl}: \ run the two-step task with $w$ from 0 to 1, \ and plot the "
    r"interaction in the stay probabilities against $w$.",
    r"$\star$ \ Design an experiment that tells a dopamine ramp that is a TD error under uncertainty from one that "
    r"encodes value.",
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
            (r"dopamine neurons fire at surprise: \ unpredicted reward, \ a predicting cue, \ a dip at omission", DELTA),
            (r"credit over time: \ learn a prediction from the next prediction", CUE),
            (r"TD learning, \ derived from the Bellman equation: \ $\delta = r + \gamma V' - V$", VALUE),
            (r"on Pavlov's task the error moves to the cue; \ an artificial error teaches", DELTA),
            (r"actor and critic, \ Q-learning, \ Go and NoGo; \ Parkinson's on and off medication", MB),
            (r"bandits: \ a learning rate read from choices, \ checked by recovery; \ directed exploration", REWARD),
            (r"maps: \ latent learning, \ place and grid cells", VALUE),
            (r"habits and plans: \ devaluation, \ the two-step task, \ the successor representation, \ replay", MB),
            (r"dopamine is more than an error: \ ramps, \ movement, \ a distributional code", CUE),
            (r"a drug that fakes the error; \ recommenders; \ a medicine's side effect", INHIB),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=30, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 17, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part seventeen in ten lines. <bookmark mark='a'/> Dopamine neurons fire at surprise: at unpredicted "
            "reward, at a cue that predicts reward, and they dip when a promised reward fails. Credit over time is "
            "solved by learning each prediction from the next one. Temporal-difference learning follows from the "
            "Bellman equation, and its error is reward plus discounted next value minus current value. On Pavlov's "
            "task that error moves to the cue, and an artificial error teaches as a real one does. Actor and critic, "
            "Q-learning, and the Go and NoGo pathways turn errors into actions. A learning rate can be read from "
            "choices, if you check that it can be recovered, and good explorers direct their exploring. Animals "
            "learn maps without reward, and the brain contains place and grid cells. Habits and plans can be told "
            "apart, by devaluation, the two-step task and revaluation, with replay in between. Dopamine is more "
            "than one error. And a drug can fake it, a recommender can exploit it, and a medicine can derail it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=48.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"a threshold counted in quanta; \ colour a matrix; \ a neuron that computes $\delta$",
             STATUS_COLOR["replicated"]),
            (r"experiments by the dozen: \ lots, \ lesions, \ twins, \ a cave, \ light-switched neurons",
             STATUS_COLOR["replicated"]),
            (r"cue weights read from choices, \ never from reports; \ and illusions that knowing does not undo",
             STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "its strongest answer yet: a single neuron whose firing follows a term in an equation from computer "
            "science. <bookmark mark='b'/> And the second, that the mind can't be experimented on, met an experiment "
            "that switched a learning signal on with light and watched the learning change."
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
            (r"attention, \ and what is worth learning about", [18]),
            (r"memory, \ replay and consolidation", [21]),
            (r"decisions, \ value and risk", [26]),
            (r"motivation: \ wanting and liking", [28]),
            (r"addiction", [41]),
            (r"products designed around habits", [52]),
            (r"the predictive brain, \ and learning to learn", [58]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Attention, and what's worth learning about, is next, Part 18. "
            "Memory, replay and consolidation are Part 21. Decisions, value and risk are Part 26. Motivation, and the "
            "difference between wanting and liking, is Part 28. Addiction is Part 41, products designed around habits "
            "Part 52, and the predictive brain, with learning to learn, Part 58."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=12.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One computes values on a "
            "short chain by hand. One derives the TD error. One times the error's journey back to the cue. One "
            "writes the likelihood of a bandit player's choices. One builds a successor matrix. One uses Psyche to "
            "trace the two-step signature as planning increases. And the last, with the star, asks how to tell what "
            "a dopamine ramp means. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"R. S. Sutton \& A. G. Barto, \emph{Reinforcement Learning: An Introduction} (2nd ed., 2018)",
             r"Y. Niv, \ Reinforcement learning in the brain (2009); \ P. Dayan \& N. D. Daw (2008)",
             r"E. C. Tolman, \ Cognitive maps in rats and men (1948)"],
            [r"W. Schultz, \ P. Dayan \& P. R. Montague (1997); \ E. E. Steinberg et al.\ (2013)",
             r"R. S. Sutton (1988); \ C. J. C. H. Watkins (1989); \ A. G. Barto et al.\ (1983)",
             r"M. J. Frank, \ L. C. Seeberger \& R. C. O'Reilly (2004); \ R. C. Wilson et al.\ (2014)",
             r"E. C. Tolman \& C. H. Honzik (1930); \ J. O'Keefe \& J. Dostrovsky (1971); \ T. Hafting et al.\ (2005)",
             r"C. D. Adams \& A. Dickinson (1981); \ N. D. Daw et al.\ (2011); \ C. Feher da Silva \& T. A. Hare (2020)",
             r"P. Dayan (1993); \ I. Momennejad et al.\ (2017); \ M. A. Wilson \& B. L. McNaughton (1994)",
             r"M. W. Howe et al.\ (2013); \ W. Dabney et al.\ (2020); \ A. D. Redish (2004)",
             r"L. Li et al.\ (2010); \ D. Weintraub et al.\ (2010); \ J. X. Wang et al.\ (2018)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Sutton and Barto's "
            "Reinforcement Learning, especially its chapters on psychology and neuroscience, is the place to start."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act IV: \ learning and memory", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 18", font_size=32, color=GREY_B), label(r"Attention", font_size=50),
                     wrapped_label(r"A gorilla walks through a basketball game, \ and half the audience misses it.",
                                   6.0, 28, GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Learning needs something to learn about, and the world offers far more than any brain can take in. "
            "<bookmark mark='a'/> Mackintosh and Pearce and Hall argued that attention itself is learned. "
            "<bookmark mark='b'/> Next time, attention in its own right: why a gorilla can walk through a "
            "basketball game unseen by half the people watching it, and what a brain does with the rest. It's "
            "Part 18: attention."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
