from __future__ import annotations

from videos.psychology.psych3.common import *  # noqa: F403

PROBLEMS = [
    r"Which of these sentences still say something after a permitted change of scale, and why? \ (a) ``It is "
    r"twice as hot today, $20^\circ$C against $10^\circ$C.'' \ (b) ``Her reaction time is twice his.'' \ (c) ``The "
    r"median rating was 4.'' \ (d) ``The mean rating rose from 3.0 to 3.5, half as much again as last year's rise.''",
    r"Two classes rate a course from 1 to 5. \ Class A's answers are in the shares 0, 0.2, 0.6, 0.2, 0; class B's "
    r"are 0.3, 0.1, 0.1, 0.1, 0.4. \ Compare the means. \ Then show from the cumulative shares that an increasing "
    r"recoding of the five answers can reverse the comparison, and find one.",
    r"Two forms of a test give $X = T + E$ and $X' = T + E'$, with errors of equal variance that are unrelated to "
    r"$T$ and to each other. \ Show that $\mathrm{corr}(X, X') = \mathrm{Var}(T)/\mathrm{Var}(X)$.",
    r"A 10-item test has reliability 0.70. \ How many items of the same kind are needed for 0.90? \ State the "
    r"assumption the formula makes, and one way in which lengthening a real test can break it.",
    r"Two measures with reliabilities 0.60 and 0.70 correlate 0.30. \ Estimate the correlation between the true "
    r"scores. \ Why can this estimate exceed 1 in a small sample although no correlation can?",
    r"With \texttt{explainer.psychology.measure} and the Pool: build a 20-item test from 10 items of "
    r"\texttt{conscientious} and 10 of \texttt{extravert}. \ Compute alpha and the correlation of the two halves. "
    r"\ What does each number tell you, and what does alpha not?",
    r"$\star$ \ You have each person's answers to each item, with error. \ Devise a test of whether an additive "
    r"scale lies behind them that fails when there is none and passes when there is one.",
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
        d, ts = archive.STEVENS_1946.data, load("truescore")
        items = [
            (rf"{d['final_report']}: \ a committee cannot agree whether a sensation can be measured", KANT),
            (r"Stevens: \ ask what a number survives; \ four kinds of scale", SCALE["interval"]),
            (r"an order with enough structure gives a scale, \ with nothing added to anything", SCALE["ordinal"]),
            (r"``it fits me'' proves nothing: \ a measure has to tell people apart", P.ACCENT),
            (rf"$X = T + E$; \ reliability is the true share of the variance, \ {r2(ts['reliability'])} for our "
             r"ten questions", TRUE),
            (r"error shrinks correlations; \ Spearman's correction restores them, at a price", OBS),
            (r"longer tests are better; \ alpha is a lower bound, and not a test of one dimension", "#F2A65A"),
            (r"validity is an argument: \ agree with other methods, differ from other traits", "#B48EF0"),
            (r"a new name is not a new thing; \ a construct may be a hidden cause or a tangle", GRIT),
            (r"people can report what, not why; \ and the best experiments make poor tests", "#7BD88F"),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=32, color=c) for i, (t, c) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        head = label(r"Part 3, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part three in ten lines. <bookmark mark='a'/> A committee of physicists and psychologists couldn't "
            "agree whether a sensation can be measured. Stevens replied by asking what a number survives, and "
            "got four kinds of scale. An order with enough structure yields a scale with nothing added to "
            "anything. A description that fits you proves nothing, because a measure has to tell people apart. "
            "A score is a true score plus error, and reliability is the share of the variance that's true. "
            "Error shrinks every correlation, and Spearman's correction restores it, at a price in noise. Longer "
            "tests are better tests, and alpha is a lower bound, not a certificate that one thing is being "
            "measured. Validity is an argument: agree with other methods, and differ from other traits. A new "
            "name isn't a new thing, and the thing may be a hidden cause or a tangle of causes. And people can "
            "tell you what, but not why; while the tasks that never fail make poor tests of a person."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.75), run_time=42.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"numbers with a stated scale, a stated error, and an argument for what they measure",
             STATUS_COLOR["replicated"]),
            (r"minds can be compared fairly: \ a control, a shuffle, a balanced order", STATUS_COLOR["replicated"]),
            (r"a blind where one can be kept; \ and the person's own report counted as a measurement, with limits",
             P.ACCENT),
        ))
        with self.voiceover(
            "And Kant's wager. <bookmark mark='a'/> His first objection, no mathematics, came back today in a "
            "sharper form: you have numbers, but are they measurements? The reply is no longer a list of "
            "formulas. It's a discipline. A number attached to a mind comes with its kind of scale, its error, "
            "and an argument for what it measures, or it isn't worth much. Whether these numbers are quantities "
            "in the physicist's sense is still open, and Kant may keep a corner of this one. "
            "<bookmark mark='b'/> The second stands as Part 2 left it. <bookmark mark='c'/> And the third "
            "gained something. The observer who disturbs includes the person observing themselves. We now know "
            "roughly what that observer can deliver: what, and not why. There's one observer left that we "
            "haven't examined. The scientist, looking at the data and hoping. That's next."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r.objection) for r in board.rows])
            for mark, r in zip("abc", board.rows):
                vo.wait_until(mark)
                self.play(FadeIn(r.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"flexible analysis, and what counts as evidence", [4]),
            (r"thresholds: \ what an observer can report", [11]),
            (r"grit, and what it adds", [28]),
            (r"factor analysis: \ the hidden-cause picture", [32]),
            (r"symptoms as a network", [39]),
            (r"which picture of a construct is right?", [44]),
            (r"scales you can test: \ the modern theory of items", [46]),
            (r"the reliability paradox, put to work", [59]),
        ], font_size=30)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Flexibility in analysis is the next part. What an "
            "observer can report is Part 11. Grit returns in Part 28. The hidden-cause picture becomes factor "
            "analysis in Part 32, the network picture arrives in Part 39, and the two meet in Part 44. The "
            "scale you can test becomes the modern theory of test items in Part 46. And the reliability paradox "
            "is put to work in Part 59."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.4), run_time=9.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=24)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One sorts sentences "
            "into those that mean something and those that don't. One asks you to reverse a comparison of means "
            "by respacing a rating scale. Three are short derivations: the reliability of a test from its twin, "
            "the length a test needs, and the correction for attenuation. One uses the measurement code to catch "
            "alpha misleading you. And the last, with the star, is the open problem from the frontier. Pause "
            "here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=6.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"F. M. Lord \& M. R. Novick, \emph{Statistical Theories of Mental Test Scores} (1968)",
             r"L. J. Cronbach, G. C. Gleser, H. Nanda \& N. Rajaratnam, \emph{The Dependability of Behavioral "
             r"Measurements} (1972)",
             r"J. Michell, \emph{Measurement in Psychology} (1999); \ D. Borsboom, \emph{Measuring the Mind} (2005)"],
            [r"S. S. Stevens (1946); \ C. Spearman (1904, 1910); \ W. Brown (1910); \ L. J. Cronbach (1951); \ "
             r"J. Cohen (1960)",
             r"L. J. Cronbach \& P. E. Meehl (1955); \ D. T. Campbell \& D. W. Fiske (1959); \ R. D. Luce \& "
             r"J. W. Tukey (1964)",
             r"B. R. Forer (1949); \ D. H. Dickson \& I. W. Kelly (1985); \ R. E. Nisbett \& T. D. Wilson (1977); \ "
             r"P. Johansson et al.\ (2005); \ L. Hall et al.\ (2010)",
             r"M. Cred\'e, M. C. Tynan \& P. D. Harms (2017); \ C. Hedge, G. Powell \& P. Sumner (2018); \ "
             r"J. K. Flake \& E. I. Fried (2020)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Stevens's paper is four "
            "pages long, and Spearman's of 1904 reads as if it had been written last year. Both are worth an "
            "evening."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=1, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"the ruler is made; \ one faculty begun", font_size=26, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        nxt = VGroup(label(r"Part 4", font_size=32, color=GREY_B), label(r"The Evidence", font_size=54),
                     wrapped_label(r"2011. \ A leading journal publishes nine experiments that appear to show people "
                                   r"responding to events that have not happened yet.", 6.0, 28, GREY_A)).arrange(
            DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "That's the ruler. <bookmark mark='a'/> We can compare minds fairly, and we know what the numbers "
            "we compare are worth. One thing is still missing: how to decide, from a set of numbers, that "
            "something is really there. <bookmark mark='b'/> In 2011 a leading journal of social psychology "
            "published nine experiments that appeared to show people responding to events that hadn't "
            "happened yet. The experiments were run by the book. The statistics were the field's own. Either "
            "the future reaches back into the present, or something was wrong with the book. What it was, and "
            "what the field did about it, is Part 4: the evidence."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
