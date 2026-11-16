from __future__ import annotations

from videos.psychology.psych46.common import *  # noqa: F403

PROBLEMS = [
    r"Under Thurstone's Case V, \ 84\% prefer $j$ to $i$. \ How far apart are they, \ in units of $\sigma$?",
    r"Luce strengths $v = (1, 2, 4)$. \ Find $P(2 \succ 1)$, \ the shares from the menu $\{1, 2, 3\}$, \ and check "
    r"that the odds of 2 over 1 are the same in both.",
    r"A logit with utilities $0$, $\ln 2$ and $\ln 3$. \ Find the choice shares.",
    r"Car and red bus are equally liked. \ Add an identical blue bus. \ Give the logit's car share and the true one.",
    r"A conjoint gives $-0.6$ per \$100 of price and $0.5$ for a great camera. \ What is the camera worth?",
    r"400 customers: \ 30\% promoters, \ 25\% detractors. \ Find the NPS and its standard error.",
    r"$\star$ \ Design a split-ballot survey that measures support for a policy and estimates the effect of its "
    r"wording and of question order, \ with balanced keys.",
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
        v, dc, a, n = load("veg"), load("decoy"), load("acq"), load("nps")
        se200 = float(n["se_nps"][list(n["ns"]).index(200)])
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for k, q, ans, col in (
                (r"1", r"share preferring corn to turnips", rf"{100 * v['P'][8, 0]:.0f}\%", PERSON),
                (r"2", r"the first option's share, \ with a decoy beneath it",
                 rf"{100 * dc['decoy_A_5'][0]:.0f}\% to {100 * dc['decoy_A_40'][0]:.0f}\%, \ by deliberation", AUTH),
                (r"3", r"unrelated scales, \ one-way keys, \ acquiescence", rf"$r = {a['pos_4']:.2f}$", MODEL),
                (r"4", r"the NPS's margin of error from 200 customers", rf"$\pm${1.96 * se200:.0f} points", GOOD)):
            rows.add(VGroup(label(k, font_size=30, color=col), wrapped_label(q, 6.4, 22, WHITE),
                            label(ans, font_size=24, color=col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"choices have structure, \ menus bend them, \ and answers carry the instrument's "
                             r"fingerprints", 12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> Ninety-three percent preferred corn to turnips. With a "
            "decoy beneath it, Psyche's first option kept half the choices after brief deliberation, and about three "
            "quarters after long. Unrelated scales keyed one way correlated about zero point two five, through "
            "acquiescence alone. And a net promoter score from two hundred customers has a margin of error of about "
            "eleven points. <bookmark mark='b'/> Choices have structure, menus bend them, and answers carry the "
            "fingerprints of the instrument."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=9.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"inconsistent comparisons carry the information", WHITE),
            (r"Thurstone: \ normal impressions; \ proportions become distances", MODEL),
            (r"Luce: \ one axiom gives a ratio scale; \ Bradley-Terry by MM", MODEL),
            (r"random utility with Gumbel noise gives the logit", PERSON),
            (r"similar options break the axiom: \ red bus, \ blue bus", AUTH),
            (r"decoys and compromises: \ the menu bends the choice", AUTH),
            (r"a comparing chooser produces both, \ more with time", SYMP),
            (r"conjoint prices attributes from choices", GOOD),
            (r"comprehend, \ retrieve, \ judge, \ report", PERSON),
            (r"wording, \ order, \ styles and satisficing", AUTH),
            (r"careless answers can manufacture correlations", AUTH),
            (r"one number is still a number with an error", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 46, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part forty-six in twelve lines. <bookmark mark='a'/> Inconsistent comparisons carry the information. "
            "Thurstone turned proportions into distances between normal impressions. Luce derived a ratio scale from "
            "one axiom, fitted by a climbing algorithm. Random utility with Gumbel noise gives the logit. Similar "
            "options break the axiom. Decoys and compromises show the menu bending the choice, and a comparing "
            "chooser produces both, more with time. Conjoint prices attributes from choices. Answering a survey "
            "means comprehending, retrieving, judging and reporting. Wording, order, styles and satisficing all leave "
            "marks. Careless answers can manufacture correlations. And one number is still a number with an error."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=40.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"Case V, \ Bradley-Terry, \ the logit and conjoint, \ fitted and checked", STATUS_COLOR["replicated"]),
            (r"split-ballot experiments on wording and order; \ menus varied by design", STATUS_COLOR["replicated"]),
            (r"comparisons ask less of introspection than ratings do; \ survey answers are reports, \ with their "
             r"known distortions", STATUS_COLOR["contested"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "Thurstone's law, Bradley-Terry, the logit and conjoint, fitted and checked. Green. "
            "<bookmark mark='b'/> The second, that the mind can't be experimented on, met split-ballot experiments on "
            "wording and order, and menus varied by design. Green. <bookmark mark='c'/> And the third, about "
            "introspection. Comparisons ask less of it than ratings do, but survey answers are reports, with known "
            "distortions. Amber."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"people over time, \ and within one person", [47]),
            (r"fitting and comparing models of behaviour", [48]),
            (r"the weight of evidence across studies", [50]),
            (r"language models as participants", [60]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> People over time, and within one person, are next, in Part "
            "47. Fitting and comparing models of behaviour, including models of choice, is Part 48. The weight of "
            "evidence across studies is Part 50. And language models as participants are Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=7.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One applies Thurstone's "
            "law. One checks Luce's axiom. One computes logit shares. One redoes the red bus. One prices a camera. One "
            "finds a net promoter score and its error. And the last, with the star, asks you to design a survey that "
            "measures its own wording and order effects. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"K. E. Train, \ \emph{Discrete Choice Methods with Simulation} (2nd edition, \ 2009)",
             r"R. Tourangeau, \ L. J. Rips \& K. Rasinski, \ \emph{The Psychology of Survey Response} (2000)",
             r"H. Schuman \& S. Presser, \ \emph{Questions and Answers in Attitude Surveys} (1981)"],
            [r"L. L. Thurstone (1927); \ R. D. Luce (1959); \ R. A. Bradley \& M. E. Terry (1952)",
             r"D. McFadden (1974); \ D. R. Hunter (2004); \ A. Tversky (1972)",
             r"J. Huber, \ J. W. Payne \& C. Puto (1982); \ I. Simonson (1989)",
             r"P. E. Green \& V. Srinivasan (1990); \ J. Hainmueller et al.\ (2014)",
             r"R. Likert (1932); \ J. A. Krosnick (1991); \ L. J. Cronbach (1946)",
             r"F. F. Reichheld (2003); \ T. L. Keiningham et al.\ (2007)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Kenneth Train's book is the "
            "standard on discrete choice, free online; Tourangeau, Rips and Rasinski's is the psychology of answering "
            "surveys; and Schuman and Presser's experiments are still the best demonstration of question effects."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act XI: \ the graduate toolkit, \ 3 of 7", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 47", font_size=32, color=GREY_B),
                     label(r"People over Time", font_size=36),
                     wrapped_label(r"When is a finding about people a finding about a person?", 6.0, 26, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Three parts of the graduate toolkit done. <bookmark mark='a'/> This one turned preferences and answers "
            "into numbers, and showed where those numbers bend. <bookmark mark='b'/> Next, time and the individual. "
            "When is a finding about people a finding about a person? Part 47: people over time."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
