from __future__ import annotations

from videos.psychology.psych32.common import *  # noqa: F403

PROBLEMS = [
    r"Under one factor, \ $r_{ij} = \lambda_i \lambda_j$ for $i \neq j$. \ Show that every tetrad difference "
    r"$r_{ik} r_{jl} - r_{il} r_{jk}$ is zero, \ and that $\lambda_i^2 = r_{ij} r_{ik} / r_{jk}$.",
    r"From Spearman's table, \ $r_{CF} = .83$, \ $r_{CE} = .78$ and $r_{FE} = .67$. \ Estimate the loadings of "
    r"Classics, \ French and English, \ and say why three tests give one answer but four test the model.",
    r"Derive Thorndike's correction for direct range restriction, \ $r_c = (r/u) / \sqrt{1 - r^2 + r^2/u^2}$, \ "
    r"and apply it to $r = .28$, \ $u = .51$.",
    r"Why does a ratio IQ give a 40-year-old with a mental age of 16 a score of 40? \ Give the deviation IQ of a "
    r"raw score of 42 when the age group's mean is 34 and its SD is 6.",
    r"With true scores normal and $X = T + E$, \ show that $E[T \mid X] = \mu + \rho\,(X - \mu)$, \ with $\rho$ "
    r"the reliability. \ Estimate the true score behind 130 at $\rho = 0.9$.",
    r"For a standard normal test $X$ and criterion $Y$ with correlation $r$, \ show that $E[Y \mid X > z] = "
    r"r\,\phi(z) / (1 - \Phi(z))$. \ What do the top 20\% average at $r = 0.4$?",
    r"$\star$ \ Design an experiment that could tell a common cause from mutualism, \ and say what each world "
    r"predicts for every test when one ability is trained.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.your_matrices()
        self.recap()
        self.score()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def your_matrices(self):
        d = load("matrices")
        head = heading(r"Your three matrices, \ checked")
        rows = rows_of([
            (r"if one of them stopped you, \ it was probably the third: \ three rules to find, \ and to hold at once",
             YOU),
            (rf"Psyche's population got {pct(d['acc_pop'][1])} of one-rule items and {pct(d['acc_pop'][3])} of "
             rf"three-rule items: \ chapter eight's solver ran out of room, \ not of logic", MODEL),
            (r"and three items are a poor test: \ with so few, \ the error of chapter six would swamp any score", G),
            (r"which is why a real test has dozens of items, \ is normed on thousands of people, \ and still "
             r"reports a band, \ not a point", VERB),
        ], 12.2, 25, 0.42).move_to([0, -0.2, 0])
        with self.voiceover(
            "First, your three matrices. <bookmark mark='a'/> If one of them stopped you, it was probably the third: "
            "three rules to find, and to hold at once. <bookmark mark='b'/> Psyche's population got "
            f"{spct(d['acc_pop'][1])} of one-rule items right, and {spct(d['acc_pop'][3])} of three-rule items. "
            "Chapter eight's solver ran out of room, not of logic. <bookmark mark='c'/> And three items are a poor "
            "test. With so few, the error of chapter six would swamp any score. <bookmark mark='d'/> That's why a "
            "real test has dozens of items, is normed on thousands of people, and still reports a band, not a point."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def recap(self):
        items = [
            (r"1904: \ Spearman's one factor and Binet's practical scale", G),
            (r"the positive manifold, \ in Spearman's table and in 301 children's nine tests", G),
            (r"the factor model: \ loadings, \ tetrads, \ one factor too few, \ three enough, \ and $g$ above them",
             MODEL),
            (r"a common cause, \ sampling and mutualism: \ one pattern of correlations, \ three worlds", MODEL),
            (r"the scale: \ ratio, \ then deviation IQs, \ and a band of error around every score", VERB),
            (r"validity: \ school strongly, \ jobs moderately, \ and range restriction in between", GOOD),
            (r"matrices: \ difficulty from rules held at once", VIS),
            (r"genes, \ school and generations: \ heritable, \ and still changeable", COHORT),
            (r"group differences: \ overlap, \ invariance, \ and Lewontin's two fields", VERB),
            (r"harm, \ fraud and a checked critic; \ and intelligences that turned out to correlate", HARM),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        head = label(r"Part 32, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part thirty-two in ten lines. <bookmark mark='a'/> In 1904 Spearman proposed one general factor, and "
            "Binet built a practical scale. The positive manifold appeared in Spearman's table and in three hundred "
            "and one children's nine tests. The factor model gave loadings and tetrads, and showed one factor too "
            "few and three enough, with g above them. A common cause, sampling and mutualism make one pattern of "
            "correlations in three different worlds. The scale went from ratio to deviation IQs, with a band of "
            "error around every score. Scores predict school strongly and jobs moderately, with range restriction "
            "in between. Matrix items are hard in proportion to the rules held at once. Scores are heritable, and "
            "still changeable, by school and across generations. Group differences need overlap, invariance and "
            "Lewontin's two fields. And the history includes harm, fraud, a critic who needed checking, and "
            "intelligences that turned out to correlate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=42.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"a correlation matrix factored, \ tetrads, \ standard errors and Brogden's gain: \ ability written as "
             r"mathematics", STATUS_COLOR["replicated"]),
            (r"school-leaving laws, \ entry cutoffs and siblings compared: \ natural experiments on the causes of "
             r"scores", STATUS_COLOR["replicated"]),
            (r"nobody can see their own IQ from the inside: \ it is a comparison with other people, \ measured",
             STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met a "
            "factored correlation matrix, tetrads, standard errors and Brogden's gain: ability written as "
            "mathematics. <bookmark mark='b'/> The second, that the mind can't be experimented on, met "
            "school-leaving laws, school-entry cutoffs and siblings compared: natural experiments on the causes of "
            "scores. <bookmark mark='c'/> And the third, about introspection: nobody can see their own IQ from the "
            "inside, because it's a comparison with other people, and it has to be measured. Green on all three, "
            "and the history is a reminder of what a measurement can be used for."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"factor analysis on personality", [33]),
            (r"stereotype threat's full record", [36]),
            (r"intellectual disability and development", [41]),
            (r"latent variables and measurement invariance", [44]),
            (r"item response theory and adaptive tests", [45]),
            (r"selection at work", [53]),
            (r"schools, \ courts and machines", [54, 56, 60]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Factor analysis meets personality next, in Part 33. "
            "Stereotype threat's full record is Part 36. Intellectual disability and development are Part 41. Latent "
            "variables and measurement invariance are Part 44, and item response theory, with adaptive tests, Part "
            "45. Selection at work is Part 53, and schools, courts and machines are Parts 54, 56 and 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=8.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=22)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One proves that a single "
            "factor makes every tetrad vanish. One estimates loadings from three of Spearman's correlations. One "
            "derives Thorndike's correction. One explains why ratio IQs failed for adults. One derives Kelley's "
            "estimate of a true score. One derives Brogden's gain from selection. And the last, with the star, asks "
            "you to design the experiment that could tell a common cause from mutualism. Pause here if you'd like "
            "to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"I. J. Deary, \emph{Intelligence: A Very Short Introduction} (2nd ed., \ 2020)",
             r"J. B. Carroll, \emph{Human Cognitive Abilities} (1993)",
             r"J. R. Flynn, \emph{What Is Intelligence?} (2007)"],
            [r"C. Spearman (1904); \ A. Binet \& T. Simon (1905); \ G. H. Thomson (1916)",
             r"K. J. Holzinger \& F. Swineford (1939); \ L. L. Thurstone (1938)",
             r"H. L. J. van der Maas et al.\ (2006); \ K.-J. Kan et al.\ (2019)",
             r"F. L. Schmidt \& J. E. Hunter (1998); \ P. R. Sackett et al.\ (2022)",
             r"P. A. Carpenter, \ M. A. Just \& P. Shell (1990)",
             r"J. R. Flynn (1987); \ S. J. Ritchie \& E. M. Tucker-Drob (2018)",
             r"J. M. Wicherts et al.\ (2004); \ J. E. Lewis et al.\ (2011)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Ian Deary's short "
            "introduction is the clearest overview of the evidence; John Carroll's survey is the reference for the "
            "structure of abilities; and James Flynn's What Is Intelligence? asks what the rise in scores across "
            "generations means."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act VIII \ begun: \ how people differ", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 33", font_size=32, color=GREY_B), label(r"Personality", font_size=40),
                     wrapped_label(r"Is there a ``you'' that stays the same across situations and years?", 6.0, 28,
                                   GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "That begins Act Eight, on how people differ. <bookmark mark='a'/> Intelligence is one way. "
            "<bookmark mark='b'/> In 1936 Gordon Allport and Henry Odbert went through Webster's New International "
            "Dictionary and copied out every word they could find that describes a person, nearly eighteen thousand of them. Fifty "
            "years of factor analysis reduced them to five. It's Part 33: personality."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
