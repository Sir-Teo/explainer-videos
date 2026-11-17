from __future__ import annotations

from videos.psychology.psych45.common import *  # noqa: F403

PROBLEMS = [
    r"Under the Rasch model, \ a person with $\theta = 1$ meets an item with $b = 0.5$. \ Find the probability of a "
    r"right answer.",
    r"An item has $a = 2$, \ $b = 0$. \ Find its information at $\theta = 0$ and at $\theta = 1$.",
    r"Ten items, \ each with $a = 1.5$, \ all at difficulty equal to a person's ability. \ Find the test information "
    r"and the standard error.",
    r"Rasch items with $b_1 = 0$ and $b_2 = 1$. \ Given a score of 1, \ find the probability that the right answer "
    r"was item 1, \ and show it does not depend on $\theta$.",
    r"The anchors' difficulties have mean 0 and SD 0.8 on this year's scale, \ mean 0.4 and SD 1.0 on last year's. "
    r"\ Find $A$ and $B$, \ and put a new item with $b = 1$ on last year's scale.",
    r"Knowledge tracing with $L_0 = 0.2$, \ $T = 0.15$, \ $G = 0.2$, \ $S = 0.1$. \ A student answers right. \ Find "
    r"P(known) after the update and after the learning step.",
    r"$\star$ \ Design an adaptive anxiety questionnaire: \ its bank, \ its stopping rule, \ its exposure control, "
    r"\ and the check that it works the same in two languages.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.your_numbers()
        self.recap()
        self.score()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def your_numbers(self):
        c, l, d = load("cat"), load("lsat"), load("dif")
        k_match = int(c["lengths"][np.argmax(c["fixed_best"] <= c["cat_rmse"] + 0.002)])
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for n, q, ans, col in (
                (r"1", r"items an adaptive test gives, \ stopping at SE 0.3", rf"about {c['mean_items']:.0f}", PERSON),
                (r"2", r"items the best fixed form needs for the same accuracy", rf"about {k_match}", MODEL),
                (r"3", r"is the Rasch model enough for the LSAT's five items?",
                 rf"yes: \ LR {l['lr']:.2f} on 4 df", SYMP),
                (r"4", r"the gap on a fair item between groups 0.8 SD apart",
                 rf"{100 * d['gap_none']:.0f} points: \ impact, \ not bias", GOOD)):
            rows.add(VGroup(label(n, font_size=30, color=col), wrapped_label(q, 6.4, 22, WHITE),
                            label(ans, font_size=24, color=col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"put the items on one scale first, \ and tests can be shorter, \ fairer and comparable "
                             r"across years", 12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> The adaptive test gave about seventeen items. The best "
            "fixed form needed about thirty-five for the same accuracy. For the law-school items, the Rasch model is "
            "enough: the extra slopes bought half a point of likelihood. And on a perfectly fair item, groups zero "
            "point eight apart differ by about fifteen points: impact, not bias. <bookmark mark='b'/> Put the items "
            "on one scale first, and tests can be shorter, fairer, and comparable across years."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=9.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"classical difficulty depends on the sample, \ and scores on the test", WHITE),
            (r"Rasch: \ the log-odds of success is ability minus difficulty", MODEL),
            (r"specific objectivity, \ and the sum score is sufficient", MODEL),
            (r"discrimination and guessing: \ two and three parameters", PERSON),
            (r"information adds; \ the standard error is one over its root", PERSON),
            (r"marginal maximum likelihood by EM; \ EAP and ML abilities", SYMP),
            (r"an adaptive test: \ the same precision with half the items", GOOD),
            (r"graded responses for rating scales", GOOD),
            (r"DIF compares people of equal ability; \ a gap is not a bias", AUTH),
            (r"anchors link this year's scale to last year's", AUTH),
            (r"surveys report populations with plausible values", YOU),
            (r"knowledge tracing follows ability as it changes", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 45, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part forty-five in twelve lines. <bookmark mark='a'/> Classical difficulty depends on the sample, and "
            "scores on the test. In Rasch's model, the log-odds of success is ability minus difficulty. That gives "
            "specific objectivity, and a sufficient sum score. Discrimination and guessing add two more parameters. "
            "Information adds across items, and the standard error is one over its square root. Items are estimated "
            "by marginal maximum likelihood, and abilities by the posterior. An adaptive test reaches the same "
            "precision with about half the items. Graded responses model rating scales. Fairness compares people of "
            "equal ability, because a gap is not a bias. Anchors link this year's scale to last year's. Surveys report "
            "populations with plausible values. And knowledge tracing follows ability as it changes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=40.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"the Rasch and graded response models fitted to real tests, \ matching published fits; \ an adaptive "
             r"test built", STATUS_COLOR["replicated"]),
            (r"items are calibrated by experiment: \ pre-tested, \ checked for DIF, \ linked", STATUS_COLOR["replicated"]),
            (r"answers to questions, \ not reports of inner states, \ for ability; \ attitude items still rest on "
             r"self-report", STATUS_COLOR["contested"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "the Rasch and graded response models fitted to real tests, matching the published fits, and an adaptive "
            "test built from scratch. Green. <bookmark mark='b'/> The second, that the mind can't be experimented on: "
            "items are calibrated by experiment, pre-tested, checked for bias and linked. Green. "
            "<bookmark mark='c'/> And the third, about introspection: ability is measured by answers, not reports of "
            "inner states, but attitude items still rest on self-report. Amber."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"what happens between a question and its answer", [46]),
            (r"ability and learning over time", [47]),
            (r"fitting models of behaviour", [48]),
            (r"a whole literature as evidence", [50]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> What happens between a question and its answer is next, in "
            "Part 46. Ability and learning over time are Part 47. Fitting models of behaviour is Part 48. And reading a "
            "whole literature as evidence is Part 50."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=7.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One computes a Rasch "
            "probability. One finds an item's information. One finds a test's standard error. One checks sufficiency "
            "by hand. One links two forms. One runs a step of knowledge tracing. And the last, with the star, asks you "
            "to design an adaptive questionnaire that works the same in two languages. Pause here if you'd like to "
            "try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"S. E. Embretson \& S. P. Reise, \ \emph{Item Response Theory for Psychologists} (2000)",
             r"F. M. Lord, \ \emph{Applications of Item Response Theory to Practical Testing Problems} (1980)",
             r"W. J. van der Linden (ed.), \ \emph{Handbook of Item Response Theory}"],
            [r"G. Rasch (1960); \ F. M. Lord \& M. R. Novick (1968)",
             r"R. D. Bock \& R. Lieberman (1970); \ R. D. Bock \& M. Aitkin (1981)",
             r"F. Samejima (1969); \ G. N. Masters (1982)",
             r"P. W. Holland \& D. T. Thayer (1988); \ M. J. Kolen \& R. L. Brennan (2014)",
             r"R. J. Mislevy (1991); \ D. J. Weiss (1982); \ H. Wainer (2000)",
             r"A. T. Corbett \& J. R. Anderson (1995); \ C. Piech et al.\ (2015)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Susan Embretson and Steven "
            "Reise's book is the friendliest introduction for psychologists; Frederic Lord's is the classic; and van "
            "der Linden's handbook covers every model in this part and many more."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act XI: \ the graduate toolkit, \ 2 of 7", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 46", font_size=32, color=GREY_B),
                     label(r"Scaling, \ Surveys and Choice", font_size=36),
                     wrapped_label(r"How do you turn ``I prefer this one'' into a number?", 6.0, 26, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Two parts of the graduate toolkit done. <bookmark mark='a'/> This one put people who answered different "
            "questions on one scale. <bookmark mark='b'/> Next, the answer itself. How do you turn I prefer this one "
            "into a number, and what happens between a question and its answer? Part 46: scaling, surveys and choice."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
