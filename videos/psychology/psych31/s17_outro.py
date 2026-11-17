from __future__ import annotations

from videos.psychology.psych31.common import *  # noqa: F403

PROBLEMS = [
    r"Show that with linear effects, \ $(a, p, c)$ and $(a + k, p - k, c + k)$ give identical predictions for every "
    r"person, \ and that only $a - c$ and $p + c$ are identified.",
    r"In a cross-section taken in one year, \ a cohort gain of $g$ per year of birth and no ageing at all produce an "
    r"apparent ageing slope. \ What is it? \ What does a longitudinal study of one cohort show in the same world?",
    r"For the growth model, \ show that a child's BLUP slope shrinks its own least-squares slope toward $\beta_1$ by "
    r"a factor that grows with the noise and falls with the number of visits \ (take the intercept as known).",
    r"Under the ACE model, \ derive $h^2 = 2(r_{MZ} - r_{DZ})$ and $c^2 = 2r_{DZ} - r_{MZ}$, \ and say why the "
    r"correlation of adoptive siblings is a direct estimate of $c^2$.",
    r"Derive Levin's population attributable fraction from $P(D) = P(D \mid \bar E)\,(1 + p(\mathrm{RR} - 1))$, \ "
    r"and show that for independent factors the combined fraction is $1 - \prod_i (1 - \mathrm{PAF}_i)$.",
    r"A test was normed 18 years ago, \ and scores have drifted up 2.8 points a decade. \ What is the expected "
    r"score of an average person today, \ and what share of people now score below 70, \ against 2.3\% at norming?",
    r"$\star$ \ Design a study that could tell whether retirement speeds cognitive decline, \ and say which "
    r"clock, \ and which assumption, \ each part of your design relies on.",
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
        head = heading(r"Your three graphs, \ checked")
        rows = rows_of([
            (r"most people call graph 1 ageing, \ because every cross-section in it slopes down", YOU),
            (r"it was cohort: \ the lines moved up between years, \ and nobody aged", COHORT),
            (r"chapter two's simulation made the same mistake on purpose: \ a cross-section of a world with "
             r"rising cohorts shows decline from the twenties", PERIOD),
            (r"the cure is never more data of the same shape; \ it is a design, \ and an assumption, \ chosen "
             r"in advance", AGE),
        ], 12.2, 26, 0.42).move_to([0, -0.2, 0])
        with self.voiceover(
            "First, your three graphs. <bookmark mark='a'/> Most people call graph one ageing, because every "
            "cross-section in it slopes down. <bookmark mark='b'/> It was cohort: the lines moved up between the "
            "years, and nobody aged at all. <bookmark mark='c'/> Chapter two's simulation made the same mistake on "
            "purpose: a cross-section of a world with rising cohorts shows a decline from the twenties. "
            "<bookmark mark='d'/> The cure is never more data of the same shape. It's a design, and an assumption, "
            "chosen in advance."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def recap(self):
        items = [
            (r"Bucharest's lottery: \ foster care raised IQ, \ most for the youngest", GOOD),
            (r"age, \ period and cohort: \ any two fix the third, \ so every answer needs an assumption", AGE),
            (r"three designs: \ cross-sections see cohorts, \ panels see practice and drop-out", COHORT),
            (r"growth curves: \ a mixed model, \ and each child's line shrunk toward the fan", CHILD),
            (r"windows: \ sharp in vision, \ blurrier in grammar, \ six months for care", AGE),
            (r"adolescence: \ risk with peers, \ two timetables, \ a late clock", PERIOD),
            (r"parents: \ shared environment fades; \ birth order touches IQ slightly, \ personality not at all",
             CARE),
            (r"programmes: \ fade-out, \ then adult effects, \ smaller after many outcomes are counted", CARE),
            (r"moral stages, \ and a sex difference that was not there", COHORT),
            (r"ageing: \ speed down, \ knowledge up, \ feelings better; \ reserve, \ and fractions that assume "
             r"causes", OLD),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        head = label(r"Part 31, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part thirty-one in ten lines. <bookmark mark='a'/> Bucharest's lottery showed foster care raising IQ, "
            "most for the children placed youngest. Age, period and cohort are tied by an identity, so every answer "
            "needs an assumption. Cross-sectional studies see cohorts, and panels see practice and drop-out. Growth "
            "curves are a mixed model, with each child's line shrunk toward the fan. Windows are sharp in vision, "
            "blurrier in grammar, and about six months for institutional care. Adolescence brings risk with peers, "
            "two timetables and a late body clock. A family's shared environment fades with age, and birth order "
            "touches IQ slightly and personality not at all. Early programmes fade on tests and reappear in adult "
            "lives, smaller once many outcomes are counted. Kohlberg's stages showed a sex difference that wasn't "
            "there. And ageing brings slower speed, more knowledge and better feelings, with reserve, and "
            "attributable fractions that assume their causes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=45.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"an identity, \ a mixed model, \ ACE algebra and attributable fractions: \ the lifespan written as "
             r"mathematics", STATUS_COLOR["replicated"]),
            (r"a lottery in Bucharest, \ natural experiments, \ and designs that separate the clocks",
             STATUS_COLOR["replicated"]),
            (r"memory of one's own past is unreliable, \ so development is measured, \ not recalled: \ a lifetime "
             r"cannot be introspected", STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "an identity, a mixed model, the algebra of twins and adoptees, and attributable fractions: the lifespan "
            "written as mathematics. <bookmark mark='b'/> The second, that the mind can't be experimented on, met a "
            "lottery in Bucharest, natural experiments, and designs that separate the clocks. "
            "<bookmark mark='c'/> And the third, about introspection: nobody can introspect a lifetime, so "
            "development is measured, not recalled. Green on all three, with the assumptions written down."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"cohorts, \ the Flynn effect and what IQ measures", [32]),
            (r"temperament and personality across life", [33]),
            (r"development that goes differently", [41]),
            (r"growth curves and people over time", [47]),
            (r"early programmes and schools", [54]),
            (r"ages in law", [56]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Cohorts, the Flynn effect and what IQ measures are next, "
            "in Part 32. Personality across life is Part 33. Development that goes differently is Part 41. Growth "
            "curves and people over time are Part 47. Early programmes and schools are Part 54, and ages in law are "
            "Part 56."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=8.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=22)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One proves the "
            "age-period-cohort identity. One finds the slope a cross-section invents from cohorts. One derives how "
            "much a growth model shrinks each child. One derives heritability and the shared environment from twin "
            "and adoption correlations. One derives the attributable fraction and its combination. One works out "
            "what old norms do near an IQ cutoff. And the last, with the star, asks you to design a study of "
            "retirement and cognitive decline, naming the clock and the assumption behind each part. Pause here if "
            "you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"C. A. Nelson, \ N. A. Fox \& C. H. Zeanah, \emph{Romania's Abandoned Children} (2014)",
             r"K. W. Schaie, \emph{Developmental Influences on Adult Intelligence} (2005)",
             r"P. B. Baltes, \emph{Theoretical propositions of life-span developmental psychology}, \ Developmental "
             r"Psychology (1987)"],
            [r"N. B. Ryder (1965); \ T. A. Salthouse (2009)",
             r"L. Steinberg (2008); \ M. Gardner \& L. Steinberg (2005)",
             r"R. Plomin \& D. Daniels (1987); \ J. R. Harris, \emph{The Nurture Assumption} (1998)",
             r"J. J. Heckman (2006); \ M. L. Anderson (2008)",
             r"L. Kohlberg (1958); \ C. Gilligan (1982); \ L. J. Walker (1984)",
             r"L. L. Carstensen (2006); \ Y. Stern (2012)",
             r"G. Livingston et al.\ (2024); \ J. R. Flynn (1987)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Romania's Abandoned Children, "
            "by Nelson, Fox and Zeanah, tells the story of the Bucharest project; Schaie's book reports the Seattle "
            "study; and Paul Baltes's 1987 paper sets out the propositions of lifespan psychology, including that "
            "development is gain and loss at every age."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act VII \ complete: \ growing", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 32", font_size=32, color=GREY_B), label(r"Intelligence", font_size=40),
                     wrapped_label(r"Is there one thing that the word ``intelligence'' measures?", 6.0, 28,
                                   GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "That completes Act Seven, on growing. <bookmark mark='a'/> Act Eight is about how people differ. "
            "<bookmark mark='b'/> In 1904 Charles Spearman noticed that schoolchildren good at one thing tend to be "
            "good at everything, and invented factor analysis to explain it. The same year, the French government "
            "asked Alfred Binet for a practical test. It's Part 32: intelligence."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
