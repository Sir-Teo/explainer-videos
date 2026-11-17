from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403

PROBLEMS = [
    r"An observed validity of 0.25 among hires, \ criterion reliability 0.5 among them, \ $u$ = 1.5. \ Correct for "
    r"both, \ in order.",
    r"Validity 0.3, \ top 10\% hired: \ $\bar z_x = \phi(1.28)/0.1$. \ With $SD_y$ = 15,000, \ 50 hires, \ 4 years, \ "
    r"find the gain before costs.",
    r"Selection rates 30\% and 20\%. \ Compute the impact ratio. \ Does it pass the four-fifths rule?",
    r"Two predictors, \ validities 0.3 and 0.4, \ correlated 0.3, \ equal weights. \ Find the composite's validity.",
    r"A structured interview's three raters each rate with reliability 0.5. \ Find the reliability of their mean "
    r"(Spearman-Brown).",
    r"Why does a concurrent study need little or no range-restriction correction? \ Give one case where it needs "
    r"some.",
    r"$\star$ \ Design a selection system for a role you know: \ job analysis, \ predictors, \ combination, \ adverse "
    r"impact, \ validation and a decision log.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.your_numbers()
        self.recap()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def your_numbers(self):
        s, tr = load("selection"), load("tr")
        k = int(np.where(np.isclose(tr["ratios"], 0.2))[0][0])
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for n_, q, ans, col in (
                (r"1", r"observed among the hired, \ true validity 0.5", rf"about {s['r_obs']:.2f}", PERSON),
                (r"2", r"the best method in the 2022 review", r"structured interview, \ about 0.42", MODEL),
                (r"3", r"hires who succeed, \ validity 0.3, \ top 20\%", rf"{100 * tr['success'][2][k]:.0f}\% (50\% by "
                                                                     rf"chance)", AUTH),
                (r"4", r"late pick-ups after a fine", r"roughly doubled", GOOD)):
            rows.add(VGroup(label(n_, font_size=30, color=col), wrapped_label(q, 5.8, 22, WHITE),
                            label(ans, font_size=24, color=col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"modest correlations, \ honestly corrected, \ are worth a great deal when applied to "
                             r"many decisions", 12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> A test with a true validity of zero point five shows about "
            "zero point one nine among the people it hired. The best single method in the 2022 review was the "
            "structured interview, at about zero point four two. With a validity of zero point three and the top "
            "fifth hired, sixty-seven percent of hires succeed, against fifty by chance. And the daycare fine roughly "
            "doubled late pick-ups. <bookmark mark='b'/> Modest correlations, honestly corrected, are worth a great "
            "deal when they're applied to many decisions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=9.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"Hawthorne's story outlived its data", WHITE),
            (r"validity is a correlation with a criterion", SYMP),
            (r"ratings are noisy, \ and the rater is half the rating", SYMP),
            (r"selection hides validity; \ corrections can restore it", MODEL),
            (r"the wrong correction overshoots", MODEL),
            (r"2022: \ structured interviews top, \ ability near 0.3", MODEL),
            (r"unstructured impressions dilute good predictors", PERSON),
            (r"Taylor-Russell and utility turn $r$ into outcomes", PERSON),
            (r"cuts magnify group differences; \ choose on the frontier", AUTH),
            (r"algorithms learn the criterion they are given", AUTH),
            (r"goals work; \ fines can become prices", GOOD),
            (r"satisfaction, \ safety and where people work, \ tested", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 53, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part fifty-three in twelve lines. <bookmark mark='a'/> Hawthorne's story outlived its data. Validity is a "
            "correlation with a criterion. Ratings are noisy, and the rater is half the rating. Selection hides "
            "validity, and corrections can restore it, but the wrong correction overshoots. In 2022, structured "
            "interviews came out on top and ability tests near zero point three. Unstructured impressions dilute "
            "good predictors. Taylor-Russell tables and utility turn a correlation into outcomes. Cuts magnify group "
            "differences, so choose on the frontier. Algorithms learn the criterion they're given. Goals work, and "
            "fines can become prices. And satisfaction, safety and where people work can all be tested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=34.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"learning, \ practice and training", [54]),
            (r"incentives, \ defaults and nudges at scale", [55]),
            (r"tests and judgements in court", [56]),
            (r"fairness in algorithms", [60]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Learning and training are Part 54. Incentives, defaults and "
            "nudges at scale are Part 55. Tests and judgements in court are Part 56. And fairness in algorithms "
            "returns in Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One corrects a validity "
            "twice. One computes utility. One applies the four-fifths rule. One finds a composite's validity. One uses "
            "Spearman-Brown on interview raters. One asks when a correction is needed. And the last, with the star, "
            "asks you to design a selection system for a role you know. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"L. J. Cronbach \& G. C. Gleser, \ \emph{Psychological Tests and Personnel Decisions} (1965)",
             r"F. L. Schmidt \& J. E. Hunter (1998); \ P. R. Sackett et al.\ (2022)",
             r"S. D. Levitt \& J. A. List (2011)"],
            [r"H. C. Taylor \& J. T. Russell (1939); \ R. L. Thorndike (1949)",
             r"M. A. McDaniel et al.\ (1994); \ J. Dana, \ R. Dawes \& N. Peterson (2013); \ S. Highhouse (2008)",
             r"S. E. Scullen, \ M. K. Mount \& M. Goff (2000)",
             r"F. De Corte, \ F. Lievens \& P. R. Sackett (2007)",
             r"E. A. Locke \& G. P. Latham (2002); \ E. P. Lazear (2000); \ U. Gneezy \& A. Rustichini (2000)",
             r"T. A. Judge et al.\ (2001); \ A. Edmondson (1999); \ N. Bloom et al.\ (2015)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Cronbach and Gleser's book turned "
            "selection into decision theory; Schmidt and Hunter, and Sackett and colleagues, are the two summaries to "
            "read side by side; and Levitt and List show how a famous story looks in its own data."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act XII: \ psychology at work, \ 3 of 7", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 54", font_size=32, color=GREY_B),
                     label(r"The Science of Learning", font_size=36),
                     wrapped_label(r"why do the study habits that feel best work worst?", 6.0, 26, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Three parts of Act Twelve are done. <bookmark mark='a'/> This one predicted who would do a job well, "
            "and found the honest numbers smaller than the stories. <bookmark mark='b'/> The next goes to school. Why "
            "do the study habits that feel best work worst? Part 54: the science of learning."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
