from __future__ import annotations

from videos.psychology.psych29.common import *  # noqa: F403

PROBLEMS = [
    r"Show that double-centring the squared distances, \ $B = -\tfrac12 J D^{(2)} J$ with $J = I - \tfrac1n "
    r"\mathbf{1}\mathbf{1}^\top$, \ gives $B = X X^\top$ for centred points $X$. \ Why are its top eigenvectors the "
    r"best $k$-dimensional map?",
    r"Show that the rotation $R$ maximizing $\mathrm{tr}(R^\top X^\top Y)$ is $U V^\top$, \ where $X^\top Y = U "
    r"\Sigma V^\top$.",
    r"In the attribution model, \ arousal $a \sim N(s + c, \sigma^2)$ with an exponential prior of mean $m$ on $s "
    r"\geq 0$. \ Show that the posterior of $s$ is a normal with mean $a - c - \sigma^2/m$, \ truncated at 0.",
    r"For $h(t) = I e^{-t/\tau}$, \ show that a forecaster with time constant $\tau_p$ overstates the total extra "
    r"happiness by the factor $\tau_p / \tau$, \ and find when the forecast is twice the experience.",
    r"With the meta-analysis table \ (\texttt{opendata.coles\_2019}), \ recompute $\hat\tau^2$, \ $I^2$ and the "
    r"PET intercept. \ What does PET assume about small studies?",
    r"In a world where a share $q$ of people stop gaining above $x^*$ \ (and sit below the rest), \ show that the "
    r"mean's slope above $x^*$ falls to $(1 - q)$ of its value, \ and that the 10th percentile flattens only if "
    r"$q > 0.1$.",
    r"$\star$ \ Design a study that the constructed-emotion account and the basic-emotion account predict "
    r"differently, \ and say what each predicts.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.your_forecast()
        self.recap()
        self.score()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def your_forecast(self):
        head = heading(r"Your forecast, \ checked")
        rows = rows_of([
            (r"in chapter ten you guessed how much happier a hoped-for event would make you, \ a month and a "
             r"year later", YOU),
            (r"if your year-later number was close to your month-later number, \ you forecast like most people: "
             r"the impact bias", UNPL),
            (r"the evidence says the event will matter, \ in the direction you expect, \ and for less long than "
             r"you expect", COG),
            (r"write the forecast down, \ and check it next year: \ it is the cheapest experiment in this series",
             PLEAS),
        ], 12.2, 26, 0.42).move_to([0, -0.2, 0])
        with self.voiceover(
            "First, your forecast. <bookmark mark='a'/> In chapter ten you guessed how much happier something you "
            "are hoping for would make you, a month later and a year later. <bookmark mark='b'/> If your year-later "
            "number was close to your month-later number, you forecast like most people, with the impact bias. "
            "<bookmark mark='c'/> The evidence says the event will matter, in the direction you expect, and for "
            "less long than you expect. <bookmark mark='d'/> Write the forecast down, and check it next year. It's "
            "the cheapest experiment in this series."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def recap(self):
        items = [
            (r"James: \ the feeling is the body, \ perceived; \ Cannon: \ the body is too slow and too alike", BODY),
            (r"two factors, \ as inference: \ unexplained arousal gets a cause; \ the strong version failed", COG),
            (r"six faces, \ recognized with a list to choose from, \ and less without one", FACE),
            (r"a map of feelings: \ two dimensions, \ from 1962 data, \ and from you", PLEAS),
            (r"constructed emotion: \ categories built from core affect and concepts", COG),
            (r"a pen in the teeth: \ 0.82 points, \ then 0.03 in seventeen laboratories, \ and $d \approx 0.2$ "
             r"across 286 effects", UNPL),
            (r"appraisal: \ an emotion as an evaluation of an event, \ computed", COG),
            (r"two roads to the amygdala; \ S.\,M., \ without fear of the world, \ but not of suffocation", FEAR),
            (r"reappraise early; \ we misjudge how long feelings last; \ money plateaus for the unhappiest", PLEAS),
            (r"a ratio from fluid dynamics, \ withdrawn after a student checked the mathematics", LOST),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=30, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 29, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part twenty-nine in ten lines. <bookmark mark='a'/> James said the feeling is the body, perceived, and "
            "Cannon answered that the body is too slow and too much alike across emotions. The two-factor theory, "
            "read as inference, gives unexplained arousal a cause, and its strong version failed. Six faces are "
            "recognized around the world when people have a list to choose from, and less without one. A map of "
            "feelings, with two dimensions, came out of data from 1962, and out of your own judgments. Constructed "
            "emotion builds the categories from core affect and concepts. A pen in the teeth made cartoons 0.82 "
            "points funnier, then 0.03 in seventeen laboratories, and about 0.2 standard deviations across two "
            "hundred and eighty-six effects. Appraisal treats an emotion as an evaluation of an event, and we "
            "computed one. There are two roads to the amygdala, and a woman without amygdalae who feared nothing "
            "in the world, but panicked at suffocation. Reappraise early; we misjudge how long our feelings last; "
            "and money stops helping only the unhappiest. And a ratio borrowed from fluid dynamics was withdrawn "
            "after a student checked the mathematics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=45.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"scaling, \ Bayes and appraisal: \ a map of feelings recovered and an emotion computed",
             STATUS_COLOR["replicated"]),
            (r"injections, \ seventeen laboratories, \ and an adversarial collaboration", STATUS_COLOR["replicated"]),
            (r"feelings are known by report: \ the reports work, \ but forecasts of them fail, \ and the way of "
             r"asking moves them", STATUS_COLOR["contested"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "multidimensional scaling, Bayes's rule and an appraisal model: a map of feelings recovered from "
            "judgments, and an emotion computed from an event. <bookmark mark='b'/> The second, that the mind "
            "can't be experimented on, met injections of adrenaline, seventeen laboratories testing one pen, and "
            "rivals who reanalysed the same data together. <bookmark mark='c'/> The third, that introspection "
            "disturbs what it observes, struck closest here, because feelings are known mainly by report. The "
            "reports are consistent, but people's forecasts of their own feelings fail, and the way a question is "
            "asked moves the answer. Amber."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"fear and sadness as disorders", [40]),
            (r"reappraisal as therapy, \ tested", [42]),
            (r"scaling judgments into maps", [46]),
            (r"emotion as the brain's prediction of the body", [58]),
            (r"machines that read and describe feelings", [60]),
        ], font_size=28)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Fear and sadness as disorders are Part 40. Reappraisal as "
            "therapy is tested in Part 42. Scaling judgments into maps returns in Part 46. Emotion as the brain's "
            "prediction of the body is part of Part 58, and machines that read and describe feelings are Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=8.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=22)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One derives classical "
            "scaling. One finds the best rotation for comparing two maps. One solves the attribution model. One "
            "measures the forecaster's error. One recomputes the facial-feedback meta-analysis from the open data. "
            "One shows why a plateau for some people can hide in an average. And the last, with the star, asks you "
            "to design a study that the constructed and basic accounts of emotion would predict differently. Pause "
            "here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"W. James, \emph{What is an emotion?}, \ Mind (1884)",
             r"L. F. Barrett, \emph{How Emotions Are Made} (2017)",
             r"J. LeDoux, \emph{The Emotional Brain} (1996)"],
            [r"W. B. Cannon (1927); \ S. Schachter \& J. E. Singer (1962); \ R. Reisenzein (1983)",
             r"P. Ekman \& W. V. Friesen (1971); \ J. A. Russell (1980, \ 1994); \ L. F. Barrett et al.\ (2019)",
             r"F. Strack, \ L. L. Martin \& S. Stepper (1988); \ E.-J. Wagenmakers et al.\ (2016); \ N. A. Coles et "
             r"al.\ (2019, \ 2022)",
             r"R. S. Lazarus (1991); \ C. A. Smith \& P. C. Ellsworth (1985)",
             r"J. S. Feinstein et al.\ (2011, \ 2013); \ J. J. Gross (1998)",
             r"D. T. Gilbert et al.\ (1998); \ P. Brickman, \ D. Coates \& R. Janoff-Bulman (1978)",
             r"M. A. Killingsworth, \ D. Kahneman \& B. Mellers (2023)",
             r"N. J. L. Brown, \ A. D. Sokal \& H. L. Friedman (2013)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. James's essay of 1884 is "
            "short and still lively; Barrett's How Emotions Are Made is the case for construction, from its author; "
            "and LeDoux's The Emotional Brain is the case for circuits, from his."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act VI \ complete: \ feeling and wanting", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 30", font_size=32, color=GREY_B), label(r"The Infant Mind", font_size=40),
                     wrapped_label(r"What does a baby know, \ and how can you find out?", 6.0, 28, GREY_A)).arrange(
            DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "That completes Act Six, on feeling and wanting. <bookmark mark='a'/> Act Seven asks where a mind comes "
            "from. <bookmark mark='b'/> Jean Piaget watched his own three children and concluded that a baby does "
            "not know that a hidden toy still exists. Checking him meant solving a problem this part never had: "
            "his subjects could not answer questions. The answer was to time how long they look. It's Part 30: the "
            "infant mind."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
