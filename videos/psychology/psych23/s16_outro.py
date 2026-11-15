from __future__ import annotations

from videos.psychology.psych23.common import *  # noqa: F403

PROBLEMS = [
    r"A reader holds a probability over analyses $T$. \ Show that $D_{\mathrm{KL}}(P(T \mid w_{\le t}) \,\|\, "
    r"P(T \mid w_{<t})) = -\log P(w_t \mid w_{<t})$ when each analysis fixes the words.",
    r"In a stream of four three-syllable words with no word repeated twice running, \ show that transitional "
    r"probabilities are 1 inside words and $\tfrac{1}{3}$ across boundaries.",
    r"Under Zipf's law with exponent 1 and $N$ word types, \ show that the $k$ commonest words cover about "
    r"$\ln k / \ln N$ of all tokens.",
    r"For one unit of the interactive activation model with constant net input $n > 0$, \ find its steady "
    r"activation, \ and say how decay and the ceiling share the work.",
    r"Sketch why no learner can identify every language in a family that contains all finite languages and one "
    r"infinite one, \ from examples alone.",
    r"With \texttt{explainer.psychology.opendata}: \ add the surprisal of the word two back to the reading-time "
    r"regression. \ Does the cost spill over further?",
    r"$\star$ \ Design a nonce-verb study \ (\emph{spling}, \ \emph{plip}) \ whose results a words-and-rules "
    r"account and a single-network account must predict differently.",
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
            (r"knowing a language is productive at every level: \ wugs, \ new sentences", WORD),
            (r"words follow Zipf's law, \ and so does a typing monkey", STAT),
            (r"common words are found faster; \ a spoken word narrows a cohort", WORD),
            (r"words feed back into letters: \ the interactive activation model", MODEL),
            (r"readers commit as they go; \ garden paths make them pay", RULE),
            (r"reading time grows with surprisal, \ in ten stories and many corpora", STAT),
            (r"infants and Psyche find words by transitional probabilities", SOUND),
            (r"one network gives a U-shaped past tense; \ whether rules exist is argued", RULE),
            (r"learning a language gets harder with the age of starting, \ late into the teens", WORD),
            (r"language has a network of its own; \ claims that it reshapes other abilities mostly failed", LOST),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=30, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 23, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part twenty-three in ten lines. <bookmark mark='a'/> Knowing a language is productive at every level, "
            "from wugs to sentences never heard before. Words follow Zipf's law, and so does a monkey at a "
            "typewriter, which is a warning. Common words are found faster, and a spoken word narrows a cohort as it "
            "arrives. Knowledge of words feeds back into the seeing of letters. Readers commit to an analysis as they "
            "go, and garden paths make them pay. Reading time grows with surprisal, in ten stories and in many "
            "corpora. Infants, and Psyche, find words in a stream by transitional probabilities. A single network "
            "gives a U-shaped past tense, and whether the mind uses rules is still argued. Learning a language gets "
            "harder with the age of starting, late into the teens. And language has a network of its own in the "
            "brain, while claims that it reshapes other abilities have mostly failed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=45.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"surprisal fitted to ten thousand words' reading times; \ a network that reads and one that learns the "
             r"past tense",
             STATUS_COLOR["replicated"]),
            (r"two minutes of a made-up language, \ and infants learn its words",
             STATUS_COLOR["replicated"]),
            (r"reading times, \ eye movements and brain waves, \ measured as a sentence unfolds, \ never asked",
             STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "surprisal fitted to the reading times of ten thousand words, and networks that read and learn. "
            "<bookmark mark='b'/> The second, that the mind can't be experimented on, met two minutes of a made-up "
            "language, from which infants learn the words. <bookmark mark='c'/> And the third, that looking inward "
            "disturbs what you look at, met reading times, eye movements and brain waves, measured while a sentence "
            "unfolds, without ever asking the reader what they think they are doing."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"reasoning: \ rules again, \ in logic", [24]),
            (r"the infant mind: \ how early language begins", [30]),
            (r"modelling behaviour: \ comparing models of reading", [48]),
            (r"modelling the brain's data: \ encoding models of language", [49]),
            (r"designing for minds: \ readable interfaces", [52]),
            (r"the science of learning: \ teaching reading", [54]),
            (r"minds and machines: \ what language models know", [60]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Reasoning, and rules again, is the next part. How early "
            "language begins is Part 30. Comparing models of reading is Part 48, and encoding models of the brain's "
            "response to language are Part 49. Readable interfaces are Part 52, teaching reading is Part 54, and what "
            "language models know is Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=12.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One derives Levy's "
            "result that surprisal is a change of belief. One works out the transitional probabilities of the "
            "stream. One finds how much of a text its commonest words cover. One finds the steady state of a unit in "
            "the reading network. One sketches Gold's argument. One extends the reading-time regression on the open "
            "data. And the last, with the star, asks you to design a study with made-up verbs that the two accounts "
            "of the past tense must predict differently. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"S. Pinker, \emph{The Language Instinct} (1994) \ and \emph{Words and Rules} (1999)",
             r"M. J. Traxler, \emph{Introduction to Psycholinguistics} (2012)",
             r"M. H. Christiansen \& N. Chater, \emph{The Language Game} (2022)"],
            [r"N. Chomsky (1957, \ 1959); \ J. Berko (1958); \ G. A. Miller (1957)",
             r"G. M. Reicher (1969); \ J. L. McClelland \& D. E. Rumelhart (1981); \ W. D. Marslen-Wilson (1987)",
             r"T. G. Bever (1970); \ L. Frazier \& K. Rayner (1982); \ J. Hale (2001); \ R. Levy (2008)",
             r"N. J. Smith \& R. Levy (2013); \ R. Futrell et al.\ (2021); \ B.-D. Oh \& W. Schuler (2023)",
             r"J. R. Saffran, \ R. N. Aslin \& E. L. Newport (1996); \ E. M. Gold (1967)",
             r"D. E. Rumelhart \& J. L. McClelland (1986); \ S. Pinker \& A. Prince (1988); \ G. F. Marcus et al.\ (1992)",
             r"J. S. Johnson \& E. L. Newport (1989); \ J. K. Hartshorne et al.\ (2018); \ E. Fedorenko et al.\ (2011)",
             r"J. Winawer et al.\ (2007); \ M. C. Frank et al.\ (2008); \ M. Lehtonen et al.\ (2018)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Steven Pinker's The Language "
            "Instinct makes the case for an innate grammar, and Morten Christiansen and Nick Chater's The Language "
            "Game makes the case against it. Read both."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act V: \ thinking", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 24", font_size=32, color=GREY_B), label(r"Reasoning and Problem Solving",
                                                                         font_size=40),
                     wrapped_label(r"Four cards, \ one rule, \ and most people turn the wrong ones. \ Are we "
                                   r"illogical, \ or is logic the wrong yardstick?", 6.0, 28, GREY_A)
                     ).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Today the mind learned words and grammar from what it heard. <bookmark mark='a'/> Next time, it reasons "
            "with them. <bookmark mark='b'/> Four cards, one rule, and most people turn over the wrong ones. Are we "
            "illogical, or is logic the wrong yardstick for a mind? It's Part 24: reasoning and problem solving."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
