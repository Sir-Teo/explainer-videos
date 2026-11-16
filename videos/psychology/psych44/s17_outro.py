from __future__ import annotations

from videos.psychology.psych44.common import *  # noqa: F403

PROBLEMS = [
    r"X causes M with standardized path 0.5, \ and M causes Y with path 0.6. \ Use Wright's tracing rules to find the "
    r"correlation of X and Y.",
    r"Nine tests, \ three factors, \ each test loading on one factor, \ a marker loading fixed for each factor. \ "
    r"Count the free parameters and the degrees of freedom.",
    r"$\chi^2 = 85.3$ on 24 df with $n = 301$. \ Compute the RMSEA.",
    r"Two sum scores each have reliability 0.63 and correlate 0.32. \ Correct the correlation for attenuation.",
    r"Metric invariance gives $\chi^2 = 124.0$ on 54 df; \ scalar, \ 164.1 on 60. \ Test the intercepts at 5\%.",
    r"Three variables, \ edges X--M and M--Y. \ Of the four ways to direct the two edges, \ which fit identically, "
    r"\ and why?",
    r"$\star$ \ For chapter 12's invented abstract, \ draw two diagrams that fit equally well, \ and design a study "
    r"that would tell them apart.",
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
        h, a, m = load("hs"), load("attenuation"), load("mediation")
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for n, q, ans, col in (
                (r"1", r"does the three-factor model pass the exact-fit test?",
                 rf"no: \ $\chi^2 = {h['t3_T']:.1f}$ on {h['t3_df']:.0f} df", PERSON),
                (r"2", r"the sum scores' correlation, \ when the traits correlate 0.5", rf"{a['sum_r']:.2f}", MODEL),
                (r"3", r"can mediation be found when there is none?",
                 rf"yes: \ {m['indirect']:.2f}, \ [{m['lo']:.2f}, {m['hi']:.2f}]", SYMP),
                (r"4", r"diagrams that fit exactly as well as the true one", r"here two; \ often many", GOOD)):
            rows.add(VGroup(label(n, font_size=30, color=col), wrapped_label(q, 6.4, 22, WHITE),
                            label(ans, font_size=24, color=col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"a model can be rejected and useful, \ corrected and still wrong, \ significant and false, "
                             r"\ and never the only one", 12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> The three-factor model fails the exact-fit test, with a "
            "chi-square of eighty-five on twenty-four degrees of freedom. The sum scores correlate about zero point "
            "three, when the traits correlate zero point five. Mediation can be found when there is none: zero point "
            "one seven, with an interval clear of zero. And two other diagrams fit exactly as well as the true one "
            "here; in published models, often many more. <bookmark mark='b'/> A model can be rejected and useful, "
            "corrected and still wrong, significant and false, and never the only one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=9.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"a correlation is a sum over the paths that join two variables", WHITE),
            (r"a factor model is a diagram: \ $\Sigma = \Lambda\Phi\Lambda^\top + \Theta$", MODEL),
            (r"identification: \ fix a scale, \ count parameters against moments", MODEL),
            (r"maximum likelihood fits the diagram to the covariances", MODEL),
            (r"$\chi^2$ rejects every model in time; \ fixed cut-offs pass wrong ones", AUTH),
            (r"modelled measurement undoes attenuation", GOOD),
            (r"compare means only with scalar invariance", SYMP),
            (r"a randomized X does not randomize the mediator", AUTH),
            (r"equivalent models fit identically; \ arrows come from design", PERSON),
            (r"the cross-lag confuses stable people with change", PERSON),
            (r"factors and networks can imply the same data", GOOD),
            (r"eight questions for reading a path diagram", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 44, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part forty-four in twelve lines. <bookmark mark='a'/> A correlation is a sum over the paths that join two "
            "variables. A factor model is a diagram, written as a matrix equation. Identification fixes a scale and "
            "counts parameters against moments. Maximum likelihood fits the diagram to the covariances. The "
            "chi-square test rejects every model in time, and fixed cut-offs pass wrong ones. Modelled measurement "
            "undoes attenuation. Compare means only with scalar invariance. A randomized treatment doesn't randomize "
            "the mediator. Equivalent models fit identically, so arrows come from design. The cross-lagged panel "
            "confuses stable people with change. Factors and networks can imply the same data. And eight questions "
            "for reading a path diagram."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=38.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"Wright's rules, \ maximum likelihood, \ fit and invariance, \ computed and checked against lavaan",
             STATUS_COLOR["replicated"]),
            (r"the arrows of a model are claims an experiment must test; \ the fit cannot", STATUS_COLOR["contested"]),
            (r"the indicators are mostly questionnaires: \ the model handles their error, \ not their bias",
             STATUS_COLOR["contested"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "Wright's rules, maximum likelihood, fit and invariance, all computed and checked against a reference "
            "implementation. <bookmark mark='b'/> The second, that the mind can't be experimented on: the arrows of a "
            "model are claims an experiment must test, and the fit can't. Amber. <bookmark mark='c'/> And the third, "
            "about introspection: the indicators are mostly questionnaires. The model handles their random error, not "
            "their bias. Amber."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"a latent trait behind each single item", [45]),
            (r"within-person models over time", [47]),
            (r"models of behaviour, \ fitted and compared", [48]),
            (r"the weight of evidence across studies", [50]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> A latent trait behind each single item is next, in Part 45. "
            "Within-person models over time are Part 47. Models of behaviour, fitted and compared, are Part 48. And "
            "the weight of evidence across studies is Part 50."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=7.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One traces paths. One "
            "counts parameters and degrees of freedom. One computes an RMSEA. One corrects for attenuation. One tests "
            "invariance. One finds equivalent models. And the last, with the star, asks you to redraw an abstract two "
            "ways and design the study that would tell them apart. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"R. B. Kline, \ \emph{Principles and Practice of Structural Equation Modeling}",
             r"K. A. Bollen, \ \emph{Structural Equations with Latent Variables} (1989)",
             r"J. M. Rohrer, \ Thinking clearly about correlations and causation (2018)"],
            [r"S. Wright (1921); \ K. G. Jöreskog (1969); \ K. J. Holzinger \& F. F. Swineford (1939)",
             r"L. Hu \& P. M. Bentler (1999); \ D. McNeish \& M. G. Wolf (2023)",
             r"R. C. MacCallum et al.\ (1993); \ W. Meredith (1993)",
             r"R. M. Baron \& D. A. Kenny (1986); \ J. G. Bullock, \ D. P. Green \& S. E. Ha (2010)",
             r"E. L. Hamaker, \ R. M. Kuiper \& R. P. P. P. Grasman (2015)",
             r"D. Borsboom \& A. O. J. Cramer (2013); \ J. Kruis \& G. Maris (2016)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Rex Kline's textbook is the "
            "standard course; Kenneth Bollen's is the mathematics; and Julia Rohrer's short paper on correlation and "
            "causation is the best first read on what a diagram can and can't claim."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act XI: \ the graduate toolkit, \ 1 of 7", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 45", font_size=32, color=GREY_B),
                     label(r"Item Response Theory", font_size=36),
                     wrapped_label(r"How can two people who took different questions be put on the same scale?", 6.0,
                                   26, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "The graduate toolkit has begun. <bookmark mark='a'/> This part modelled what no one observes, and showed "
            "what the fit can and can't say. <bookmark mark='b'/> Next, the single encounter of one person with one "
            "question. How can two people who took different questions be put on the same scale? Part 45: item "
            "response theory."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
