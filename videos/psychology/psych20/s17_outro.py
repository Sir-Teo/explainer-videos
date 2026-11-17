from __future__ import annotations

from videos.psychology.psych20.common import *  # noqa: F403

PROBLEMS = [
    r"Ebbinghaus took 1,156 s to learn a list and 780 s to relearn it a day later. \ What is the saving, \ and what "
    r"does his formula predict for 24 hours?",
    r"For the recall sequence 16, \ 15, \ 14, \ 1, \ 2, \ 9 of a 16-word list, \ count the actual and possible "
    r"transitions at lags $+1$ and $-1$, \ and give both CRPs.",
    r"Show that for orthogonal inputs the drift keeps $\|\mathbf{c}\| = 1$ with $\rho = \sqrt{1 - \beta^2}$, \ and "
    r"that $\mathbf{c}_i \cdot \mathbf{c}_j \to \rho^{|i-j|}$ for a long list.",
    r"Show that a choice rule $a_i^{1/\tau} / \sum_k a_k^{1/\tau}$ is unchanged when every $a_i$ is multiplied by "
    r"the same constant, \ and use it to explain long-term recency.",
    r"Prove that an asynchronous update of a Hopfield network with symmetric weights and zero diagonal never "
    r"raises $E = -\tfrac{1}{2}\mathbf{s}^\top W \mathbf{s}$.",
    r"With \texttt{explainer.psychology.opendata}: \ redo Murre's sign-flip test, \ then find the power to detect "
    r"a context effect of 4 words with 16 divers and his spread.",
    r"$\star$ \ Design an experiment that could tell a single-system account of priming and recognition from a "
    r"two-system account, \ and say what each predicts.",
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
            (r"savings show memory that recall can't; \ forgetting is fast, \ then slow, \ like the odds of need", WORD),
            (r"recall favours the first and the last, \ and starts at the end", WORD),
            (r"one word brings back its neighbour, \ forward more than back, \ in almost everyone", CTX),
            (r"what you do at study, \ and the match at test, \ decide what comes back", CUE),
            (r"context helps a little; \ the famous divers did not replicate", LOST),
            (r"SAM's buffer gives both ends, \ but symmetric contiguity and no long-term recency", SAM),
            (r"a drifting context gives recency, \ contiguity and its forward lean, \ and why a delay ends recency",
             MODEL),
            (r"fitted by maximum likelihood, \ it predicts each next word far better than position alone", MODEL),
            (r"a Hopfield network completes a memory from a part, \ up to about $0.14N$ memories", CTX),
            (r"memory has systems, \ or one system tested many ways; \ the hippocampus indexes and separates", WORD),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=30, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 20, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part twenty in ten lines. <bookmark mark='a'/> Savings show memory that recall cannot, and forgetting "
            "is fast and then ever slower, like the odds that a memory will be needed. Recall favours the first and "
            "the last words of a list, and starts at the end. One word brings back its neighbour, forward more than "
            "backward, in almost every person. What you do while studying, and how well the test matches it, decide "
            "what comes back. Context helps a little, and the famous divers did not replicate. SAM's buffer gives "
            "both ends of the curve, but symmetric contiguity and no long-term recency. A drifting context gives "
            "recency, contiguity and its forward lean, and explains why a delay ends recency. Fitted by maximum "
            "likelihood, it predicts each next word far better than position alone, and fails one test that tells "
            "us what it lacks. A Hopfield network completes a memory from a part of "
            "it, up to about 0.14 memories per unit. And memory has systems, or one system tested in many ways, "
            "with the hippocampus as the index that separates and binds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=45.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"attention as a multiplication; \ a limit fitted trial by trial; \ a memory search fitted recall by "
             r"recall",
             STATUS_COLOR["replicated"]),
            (r"experiments by the dozen: \ lots, \ lesions, \ twins, \ a gorilla, \ divers on land and under water",
             STATUS_COLOR["replicated"]),
            (r"cue weights read from choices, \ never from reports; \ and illusions that knowing does not undo",
             STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met a "
            "model of memory search with nine parameters, fitted to every recall of three and a half thousand "
            "lists, and checked on lists it had never seen. <bookmark mark='b'/> And the second, that the mind can't "
            "be experimented on, met divers on a beach and under the sea, and then, forty-six years later, the "
            "experiment done again."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows], FadeIn(board.rows[2].reply))
            vo.wait_until("a")
            self.play(Indicate(board.rows[0].objection, color=KANT), FadeIn(board.rows[0].reply, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(Indicate(board.rows[1].objection, color=KANT), FadeIn(board.rows[1].reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"forgetting, \ consolidation, \ false memories", [21]),
            (r"semantic memory and concepts", [22]),
            (r"memory across the lifespan", [31]),
            (r"model fitting and model comparison", [48]),
            (r"learning: \ spacing, \ testing, \ the classroom", [54]),
            (r"witnesses and interviews", [56]),
            (r"memory in machines", [60]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Forgetting, consolidation and false memories are Part 21. "
            "Semantic memory and concepts are Part 22. Memory across the lifespan is Part 31. Fitting and comparing "
            "models like the ones today is Part 48. Spacing, testing and the classroom are Part 54. Witnesses and "
            "interviews are Part 56. And memory in machines is Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=12.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One computes a saving. "
            "One works a lag-CRP by hand. One derives the drift of context. One shows why a choice rule ignores a "
            "common factor, and what that says about recency. One proves that a Hopfield network must settle. One "
            "redoes the divers' test and asks how much power it had. And the last, with the star, asks you to design "
            "the experiment that could settle one memory against many. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"M. J. Kahana, \emph{Foundations of Human Memory} (2012)",
             r"A. Baddeley, \ M. W. Eysenck \& M. C. Anderson, \emph{Memory} (3rd ed., \ 2020)",
             r"M. K. Healey, \ N. M. Long \& M. J. Kahana, \ Contiguity in episodic memory (2019)"],
            [r"H. Ebbinghaus (1885); \ J. R. Anderson \& L. J. Schooler (1991); \ B. B. Murdock (1962)",
             r"M. Glanzer \& A. R. Cunitz (1966); \ R. A. Bjork \& W. B. Whitten (1974); \ M. J. Kahana (1996)",
             r"F. I. M. Craik \& E. Tulving (1975); \ N. J. Slamecka \& P. Graf (1978); \ M. Dresler et al.\ (2017)",
             r"E. Tulving \& D. M. Thomson (1973); \ D. R. Godden \& A. D. Baddeley (1975); \ J. M. J. Murre (2021)",
             r"J. G. W. Raaijmakers \& R. M. Shiffrin (1981); \ M. W. Howard \& M. J. Kahana (2002)",
             r"S. M. Polyn, \ K. A. Norman \& M. J. Kahana (2009); \ J. J. Hopfield (1982); \ D. J. Amit et al.\ (1985)",
             r"L. R. Squire (2004); \ P. Graf, \ L. R. Squire \& G. Mandler (1984); \ A. P. Yonelinas (1994)",
             r"T. J. Teyler \& P. DiScenna (1986); \ J. R. Manning et al.\ (2011); \ L. Ji-An et al.\ (2024)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Michael Kahana's Foundations "
            "of Human Memory is the best single book on the models of this part; Baddeley, Eysenck and Anderson's "
            "Memory is the broadest introduction."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act V: \ thinking", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 21", font_size=32, color=GREY_B), label(r"Memory II: \ Forgetting and Inventing",
                                                                           font_size=40),
                     wrapped_label(r"1974: \ ``smashed'' or ``hit''? \ One word in a question, \ and a week later "
                                   r"people remember broken glass.", 6.0, 28, GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Today memory was a search, and a good one. <bookmark mark='a'/> But a search that reconstructs can "
            "also invent. <bookmark mark='b'/> In 1974 Elizabeth Loftus showed people a film of a car crash and "
            "asked how fast the cars were going when they hit each other, or when they smashed into each other. A "
            "week later, those who heard smashed were more likely to remember broken glass. There was none. It's "
            "Part 21: memory, forgetting and inventing."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
