from __future__ import annotations

from videos.psychology.psych14.common import *  # noqa: F403

PROBLEMS = [
    r"Multiply a normal prior $N(\mu_0, \sigma_0^2)$ by a normal likelihood $N(x, \sigma^2)$ \ and show the posterior "
    r"is normal, \ with precision $1/\sigma_0^2 + 1/\sigma^2$, \ and mean the precision-weighted average.",
    r"Vision's $\sigma$ is 2 mm and touch's 4 mm. \ Find the weights and the combined $\sigma$. \ If the seen bar is "
    r"3 mm taller than the standard and the felt bar 3 mm shorter, \ where does the combined percept fall?",
    r"With the eyes 6.3 cm apart, \ find the disparity, \ in seconds of arc, \ of 1 cm of depth at 0.5 m and at 5 m. "
    r"\ Could an observer with a 10$''$ threshold see the second?",
    r"A person 1.8 m tall stands 10 m away. \ What angle do they subtend? \ If the visual system takes them to be "
    r"5 m away, \ how tall do they look?",
    r"An edge with unit normal $\mathbf{n}$ moving at velocity $\mathbf{v}$ shows only $\mathbf{n}\cdot\mathbf{v}$. "
    r"\ For two edges, \ find the MAP velocity under a prior $N(\mathbf{0}, \sigma_p^2 I)$ and noise $\sigma$, \ and "
    r"show it tends to the intersection of constraints as $\sigma \to 0$.",
    r"With \texttt{explainer.psychology.psyche.infer}: \ train \texttt{TinyConvNet} on sets in which a fraction $q$ of "
    r"images carry their shape's own texture, \ and find the $q$ at which half the conflict answers follow texture.",
    r"$\star$ \ Design an experiment that could tell whether a perceptual prior is learned in a lifetime or present "
    r"at birth, \ and say what result would decide it.",
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
            (r"two squares send equal light, \ and look different: \ you saw the surfaces", YOU),
            (r"every image fits many scenes: \ seeing must add assumptions", LIKE),
            (r"grouping, \ illusory edges and figure-ground: \ the Gestalt laws as priors", PRIOR),
            (r"two eyes give disparity, \ falling with the square of distance", LIKE),
            (r"constancy multiplies by seen distance; \ misapplied, \ it makes illusions", WORLD),
            (r"Bayes: \ precisions add, \ and means are precision-weighted", POST),
            (r"cues combined by reliability: \ predicted in advance, \ and nearly met", POST),
            (r"priors you can see: \ light from above, \ and slow motion", PRIOR),
            (r"objects need invariance; \ faces are seen as wholes, \ in their own cortex", WHITE),
            (r"deep networks predict the brain, \ and still see by texture", MODEL),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=30, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 14, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part fourteen in ten lines. <bookmark mark='a'/> Two squares sent your eye the same light and looked "
            "different, because you saw the surfaces, with the shadow taken out. Every image fits many scenes, so "
            "seeing must add assumptions. Grouping, illusory edges and the choice of figure over ground are the first "
            "of them, and the Gestalt laws read best as priors. Two eyes give disparity, which falls with the square "
            "of distance. Constancy multiplies an image's size by its seen distance, and misapplied to a page, it "
            "makes illusions. Bayes's rule for perception says precisions add, and means are weighted by precision. "
            "Cues are combined by reliability, as predicted in advance from each cue alone, and people nearly meet "
            "the prediction. Some priors you can see for yourself: light from above, and things that move slowly. "
            "Recognizing objects needs invariance, faces are seen as wholes and have cortex of their own, and deep "
            "networks predict the brain's responses, and still see by texture."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=44.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"a threshold counted in quanta; \ colour predicted by a matrix. \ Whether a sensation has a size: \ still "
             r"argued", STATUS_COLOR["replicated"]),
            (r"experiments by the dozen: \ assignment by lot, \ lesions, \ twins, \ a cave",
             STATUS_COLOR["replicated"]),
            (r"cue weights read from choices, \ never from reports; \ and illusions that knowing does not undo",
             STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> Today the third objection, that watching a mental state changes it, "
            "met two replies. Ernst and Banks never asked anyone how much they relied on vision. The weights were "
            "read from where their choices fell when the senses disagreed, a method that doesn't depend on looking "
            "inward. <bookmark mark='b'/> And the two squares still look different now that you know they're the "
            "same. Seeing doesn't change when you watch it, or when you know better. Whether the same holds for "
            "thought and feeling is a question for later parts."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows], FadeIn(board.rows[0].reply),
                      FadeIn(board.rows[1].reply))
            vo.wait_until("a")
            self.play(Indicate(board.rows[2].objection, color=KANT), FadeIn(board.rows[2].reply, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the other senses, \ and combining them", [15]),
            (r"priors and prediction errors in learning", [17]),
            (r"attention, \ and seeing what you expect", [18]),
            (r"what infants know before they learn", [30]),
            (r"displays, \ headsets and the human in the loop", [51]),
            (r"the predictive brain", [58]),
            (r"deep networks as models of minds", [60]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> The other senses, and how they're combined, are Part 15. "
            "Priors and prediction errors in learning, Part 17. Attention, and seeing what you expect, Part 18. What "
            "infants know before they've learned anything, Part 30. Displays, headsets and the human in the loop, "
            "Part 51. The predictive brain, Part 58. And deep networks as models of minds, Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=13.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One derives the normal "
            "posterior. One combines vision and touch, with a conflict. One works out when two eyes stop helping. One "
            "makes a giant out of a misjudged distance. One solves the aperture problem with a prior. One uses "
            "Psyche's inference module to find when a network's diet tips it from shape to texture. And the last, "
            "with the star, is the frontier's problem. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"S. E. Palmer, \emph{Vision Science: Photons to Phenomenology} (1999)",
             r"J. P. Frisby \& J. V. Stone, \emph{Seeing} (2nd ed., 2010)",
             r"D. Marr, \emph{Vision} (1982); \ D. C. Knill \& W. Richards (eds.), \emph{Perception as Bayesian "
             r"Inference} (1996)"],
            [r"M. Wertheimer (1923); \ G. Kanizsa (1955); \ R. von der Heydt et al.\ (1984); \ H. Zhou et al.\ (2000)",
             r"C. Wheatstone (1838); \ B. Julesz (1960); \ R. L. Gregory (1963); \ M. H. Segall et al.\ (1966)",
             r"M. O. Ernst \& M. S. Banks (2002); \ D. Alais \& D. Burr (2004); \ D. Rahnev \& R. N. Denison (2018)",
             r"P. Thompson (1982); \ Y. Weiss, E. P. Simoncelli \& E. H. Adelson (2002); \ W. J. Adams et al.\ (2004)",
             r"E. H. Land \& J. J. McCann (1971); \ E. H. Adelson (1995); \ A. L. Gilchrist (1977)",
             r"I. Biederman (1987); \ S. Thorpe et al.\ (1996); \ R. K. Yin (1969); \ N. Kanwisher et al.\ (1997)",
             r"D. L. K. Yamins et al.\ (2014); \ R. Geirhos et al.\ (2019); \ W. K. Vong et al.\ (2024)",
             r"R. Held et al.\ (2011); \ D. Amir \& C. Firestone (2025); \ J. J. Gibson (1979)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Palmer's Vision Science is the "
            "place to start, and Knill and Richards's collection is where the Bayesian view was set out."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act III: \ the senses", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 15", font_size=32, color=GREY_B), label(r"The Other Senses", font_size=50),
                     wrapped_label(r"A cochlea that does a Fourier transform, \ a nose with four hundred receptors, \ "
                                   r"and a sense of where your own body is.", 6.0, 28, GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "So seeing is a bet, made fast, with assumptions learned from a world in which they're usually true. "
            "<bookmark mark='a'/> But vision is one sense of many. <bookmark mark='b'/> Next time: an ear whose "
            "cochlea splits sound into frequencies, a nose with about four hundred kinds of receptor, touch and pain, "
            "and the sense you never notice, of where your own body is. Each has its own code, and the same "
            "mathematics of combination. It's Part 15: the other senses."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
