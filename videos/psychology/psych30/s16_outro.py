from __future__ import annotations

from videos.psychology.psych30.common import *  # noqa: F403

PROBLEMS = [
    r"For a Dirichlet$(\alpha)$-multinomial learner with $k$ outcomes, \ show that the predictive probability of an "
    r"outcome seen $c$ times in $n$ events is $(c + \alpha)/(n + k\alpha)$, \ and give its surprisal in bits.",
    r"If a number $n$ is represented as a normal with mean $n$ and standard deviation $w n$, \ show that "
    r"$P(\text{correct}) = \Phi\big(|n_1 - n_2| / (w\sqrt{n_1^2 + n_2^2})\big)$, \ and that it depends only on the ratio.",
    r"From a box with a share $p$ of white balls, \ show that four red and one white is $\big(p/(1 - p)\big)^3$ times "
    r"less probable than four white and one red.",
    r"With the ManyBabies table \ (\texttt{opendata.manybabies\_2020}), \ refit the meta-regression with age alone. "
    r"\ How much does the age slope change, \ and why?",
    r"In a field with no interactions, \ a cue of strength $A$ at B decays as $A e^{-t/\tau}$ while a memory "
    r"trace $c\,m$ sits at A. \ Show that the reach goes to A after $t^* = \tau \ln(A / c\,m)$.",
    r"Infants who have seen too little of a display prefer the familiar one. \ Show how a familiarity preference "
    r"could produce longer looks at the 180-degree drawbridge without any knowledge of the box.",
    r"$\star$ \ Design a study that core knowledge and rational constructivism predict differently, \ and say "
    r"what each predicts.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.your_guesses()
        self.recap()
        self.score()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def your_guesses(self):
        head = heading(r"Your six guesses, \ checked")
        rows = rows_of([
            (r"most people guess all six reported results, \ because each makes a good story", YOU),
            (r"the strongest evidence: \ infant-directed speech, \ and the large-ratio number result; \ the "
             r"drawbridge's looking pattern repeats in its laboratory", GOOD),
            (r"arithmetic and false belief at fifteen months are contested", LOST),
            (r"a good guess about where a baby looks is not the same as knowing what the baby knows", LOOK),
        ], 12.2, 26, 0.42).move_to([0, -0.2, 0])
        with self.voiceover(
            "First, your six guesses. <bookmark mark='a'/> Most people guess all six reported results, because each "
            "makes a good story. <bookmark mark='b'/> Of the six, the evidence is strongest for infant-directed "
            "speech and for the large-ratio number result, and the drawbridge's looking pattern repeats in its "
            "laboratory. <bookmark mark='c'/> Arithmetic, and false belief at fifteen months, are contested. "
            "<bookmark mark='d'/> And a good guess about where a baby looks is not the same as knowing what the "
            "baby knows."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def recap(self):
        items = [
            (r"A-not-B: \ reaching back to where the toy was found", A_COL),
            (r"Piaget: \ a mind built by acting, \ in stages", OBJ),
            (r"looking time: \ habituation, \ surprise, \ and the Goldilocks middle", LOOK),
            (r"ManyBabies: \ $d = 0.35$ in 65 laboratories, \ with age, \ method and language as moderators", NUM),
            (r"objects and arithmetic by looking: \ patterns that repeat, \ readings that are argued", OBJ),
            (r"number by ratio: \ Weber's law, \ sharpening with age", NUM),
            (r"infants as statisticians: \ samples judged against populations", MODEL),
            (r"A-not-B as a field: \ an error from dynamics, \ outgrown by a parameter", B_COL),
            (r"false belief at four, \ robust; \ at fifteen months, \ contested", MIND),
            (r"attachment, \ temperament and copying: \ modest predictions, \ faithful learners", CARE),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=30, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 30, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part thirty in ten lines. <bookmark mark='a'/> Infants of eight to twelve months reach back to where a "
            "toy was found, not where they saw it go. Piaget saw a mind built by acting, in stages. Looking time "
            "replaced asking, through habituation, surprise, and attention to the Goldilocks middle. ManyBabies "
            "measured one effect in sixty-five laboratories, a d of 0.35, with age, method and language as "
            "moderators, and we recomputed it. Knowledge of objects and arithmetic by looking gives patterns that "
            "repeat and readings that are argued. Number is judged by ratio, under Weber's law, sharpening with age. "
            "Infants judge samples against populations, like small statisticians. The A-not-B error falls out of a "
            "dynamic field, and is outgrown by a change in one parameter. False belief at four is robust; at fifteen "
            "months it's contested. And attachment, temperament and copying make modest predictions about faithful "
            "learners."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=45.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"Weber's law, \ Bayes and a neural field: \ number, \ samples and an error written as mathematics",
             STATUS_COLOR["replicated"]),
            (r"looking times, \ habituation, \ and an effect tested in 65 laboratories", STATUS_COLOR["replicated"]),
            (r"infants cannot report at all: \ every finding is an inference from behaviour, \ and the rich "
             r"inferences are where findings fail", STATUS_COLOR["contested"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "Weber's law, Bayes's rule and a neural field: number, samples and an error, written as mathematics. "
            "<bookmark mark='b'/> The second, that the mind can't be experimented on, met looking times, "
            "habituation, and one effect tested in sixty-five laboratories at once. <bookmark mark='c'/> The third, "
            "about introspection, takes a new form here: infants can't report anything, so every finding is an "
            "inference from behaviour, and the rich inferences are where findings fail. Amber."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"development across the whole life", [31]),
            (r"temperament grown up: \ personality", [33]),
            (r"autism and development", [41]),
            (r"a replication run end to end", [43]),
            (r"learning in schools", [54]),
            (r"machines tested like infants", [60]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Development across the whole life is next, in Part 31. "
            "Temperament grown up is personality, in Part 33. Autism and development are in Part 41. A replication "
            "run end to end is Part 43's capstone. Learning in schools is Part 54, and machines tested like infants "
            "are Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=8.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=22)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One derives the ideal "
            "learner's surprisal. One derives the number system's accuracy and shows it depends only on the ratio. "
            "One works out the box of balls. One refits the ManyBabies meta-regression from the open data. One "
            "finds when the field's memory wins. One shows how a preference for the familiar could fake knowledge "
            "of objects. And the last, with the star, asks you to design a study that core knowledge and rational "
            "constructivism would predict differently. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"J. Piaget, \emph{The Construction of Reality in the Child} (1954)",
             r"A. Gopnik, \ A. N. Meltzoff \& P. K. Kuhl, \emph{The Scientist in the Crib} (1999)",
             r"E. S. Spelke \& K. D. Kinzler, \emph{Core knowledge}, \ Developmental Science (2007)"],
            [r"R. L. Fantz (1961); \ C. Kidd, \ S. T. Piantadosi \& R. N. Aslin (2012)",
             r"ManyBabies Consortium (2020)",
             r"R. Baillargeon, \ E. S. Spelke \& S. Wasserman (1985); \ R. S. Bogartz et al.\ (2000)",
             r"K. Wynn (1992); \ F. Xu \& E. S. Spelke (2000); \ F. Xu \& V. Garcia (2008)",
             r"E. Thelen, \ G. Sch\"oner, \ C. Scheier \& L. B. Smith (2001)",
             r"H. Wimmer \& J. Perner (1983); \ K. H. Onishi \& R. Baillargeon (2005); \ L. Kulke et al.\ (2018)",
             r"A. N. Meltzoff \& M. K. Moore (1977); \ J. Oostenbroek et al.\ (2016)",
             r"H. F. Harlow (1958); \ M. D. S. Ainsworth et al.\ (1978); \ R. M. P. Fearon et al.\ (2010)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Piaget's The Construction of "
            "Reality in the Child is where the A-not-B error begins; The Scientist in the Crib, by Alison Gopnik, "
            "Andrew Meltzoff and Patricia Kuhl, is the case for infants as learners; and Spelke and Kinzler's short "
            "review sets out core knowledge."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act VII \ begun: \ growing", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 31", font_size=32, color=GREY_B), label(r"The Lifespan", font_size=40),
                     wrapped_label(r"What, \ in a life, \ is set early, \ and what stays open?", 6.0, 28,
                                   GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "That's the first part of Act Seven, on growing. <bookmark mark='a'/> The next part follows the whole "
            "life. <bookmark mark='b'/> In 2000 in Bucharest, with too few foster homes for the children in the "
            "city's institutions, placement was decided by lottery. It made a randomized experiment on early care, "
            "and the children have been followed ever since. It's Part 31: the lifespan."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
