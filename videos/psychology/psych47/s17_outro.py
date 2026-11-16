from __future__ import annotations

from videos.psychology.psych47.common import *  # noqa: F403

PROBLEMS = [
    r"A by-participant test gives $F_1 = 6.0$ on (1, 29) df and a by-item test $F_2 = 2.0$ on (1, 18). \ Find min "
    r"$F'$ and its denominator degrees of freedom.",
    r"A person's own slope is 1.0 with sampling variance 0.09; \ people's slopes have mean 0.5 and variance 0.09. \ "
    r"Find the multilevel estimate.",
    r"A person averages $\bar x_p = 4$; \ today $x = 6$. \ With $\beta_W = 0.6$ and $\beta_B = -1$, \ split today's "
    r"predicted value into its within and between parts.",
    r"True inertia 0.5, \ 25 occasions per person. \ Roughly what will the average estimate be?",
    r"Ten items per condition, \ items vary with SD 0.5, \ effect 0.4. \ With unlimited participants, \ what is the "
    r"standard error of the effect?",
    r"An AR(1) mood with $\phi = 0.4$ and shocks of SD 1. \ What is its variance?",
    r"$\star$ \ Design a diary study of whether poor sleep raises next-day anxiety within persons: \ occasions, \ lag, "
    r"\ centring, \ model, \ and power at both levels.",
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
        f, s, e, i = load("fpr"), load("simpson"), load("ergodic"), load("inertia")
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for k, q, ans, col in (
                (r"1", r"false positives, \ by participants only", rf"{100 * f['F1']:.0f}\%", AUTH),
                (r"2", r"one person's y when their x rises", rf"rises: \ slope {s['within']:+.2f}", PERSON),
                (r"3", r"people whose own correlation is near the group's", rf"{100 * e['share_near']:.0f}\%", MODEL),
                (r"4", r"inertia 0.4, \ estimated from 20 days", rf"{i['mean_est'][1]:.2f}", GOOD)):
            rows.add(VGroup(label(k, font_size=30, color=col), wrapped_label(q, 6.4, 22, WHITE),
                            label(ans, font_size=24, color=col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"the level of the data must match the level of the claim: \ items, \ persons, \ or "
                             r"moments", 12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> Analysed by participants only, about half the studies of "
            "nothing came out significant. In the cloud, one person's y rises when their x does, though across "
            "people it falls. Fewer than one person in ten showed the group's correlation within themselves. And "
            "twenty days turn a true inertia of zero point four into about zero point three. <bookmark mark='b'/> The "
            "level of the data must match the level of the claim: items, persons, or moments."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=9.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"stimuli are a sample: \ ignore them and false positives soar", WHITE),
            (r"averaging over trials throws away structure", PERSON),
            (r"multilevel models: \ regressions within regressions", MODEL),
            (r"partial pooling describes each person better", MODEL),
            (r"participants and items crossed; \ maximal or parsimonious", SYMP),
            (r"power comes from stimuli too", SYMP),
            (r"split predictors into person means and departures", GOOD),
            (r"a relation can reverse within a person", AUTH),
            (r"ergodicity rarely holds; \ groups may describe no one", AUTH),
            (r"diaries make each person a time series; \ inertia is biased", PERSON),
            (r"cause over time needs within-person change", MODEL),
            (r"tipping points slow down first, \ but diaries see it poorly", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 47, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part forty-seven in twelve lines. <bookmark mark='a'/> Stimuli are a sample, and ignoring them sends "
            "false positives soaring. Averaging over trials throws away structure. Multilevel models are regressions "
            "within regressions, and partial pooling describes each person better. Participants and items are "
            "crossed, and the model can be maximal or parsimonious. Power comes from stimuli too. Split predictors "
            "into person means and departures, because a relation can reverse within a person. Ergodicity rarely "
            "holds, so groups may describe no one. Diaries make each person a time series, and inertia's estimate is "
            "biased. Cause over time needs within-person change. And tipping points slow down first, though diaries "
            "see it poorly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=40.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"multilevel models, \ min $F'$, \ ergodicity and critical slowing down, \ simulated and fitted",
             STATUS_COLOR["replicated"]),
            (r"within-person experiments: \ single cases and micro-randomized trials", STATUS_COLOR["replicated"]),
            (r"diaries are self-reports, \ many times a day: \ less recall, \ still introspection",
             STATUS_COLOR["contested"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection met multilevel models, min F prime, ergodicity "
            "and critical slowing down, simulated and fitted. Green. <bookmark mark='b'/> The second, that the mind "
            "can't be experimented on, met within-person experiments: single cases and micro-randomized trials. "
            "Green. <bookmark mark='c'/> And the third, about introspection. Diaries are self-reports many times a "
            "day: less reliance on memory, but still introspection. Amber."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"models of behaviour, \ fitted person by person", [48]),
            (r"the brain's data, \ with subjects and voxels", [49]),
            (r"the weight of evidence across studies", [50]),
            (r"computational psychiatry, \ one person at a time", [59]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Models of behaviour, fitted person by person, are next, in "
            "Part 48. The brain's data, with subjects and voxels as levels, are Part 49. The weight of evidence across "
            "studies is Part 50. And computational psychiatry, one person at a time, is Part 59."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=7.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One computes min F "
            "prime. One shrinks a slope. One splits a prediction into within and between. One predicts inertia's "
            "bias. One finds the limit that items put on precision. One finds a mood's variance. And the last, with "
            "the star, asks you to design a diary study of sleep and anxiety within persons. Pause here if you'd like "
            "to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"N. Bolger \& J.-P. Laurenceau, \ \emph{Intensive Longitudinal Methods} (2013)",
             r"A. Gelman \& J. Hill, \ \emph{Data Analysis Using Regression and Multilevel Models} (2007)",
             r"T. A. B. Snijders \& R. J. Bosker, \ \emph{Multilevel Analysis} (2nd edition, \ 2012)"],
            [r"H. H. Clark (1973); \ R. H. Baayen, \ D. J. Davidson \& D. M. Bates (2008)",
             r"D. J. Barr et al.\ (2013); \ H. Matuschek et al.\ (2017)",
             r"C. M. Judd, \ J. Westfall \& D. A. Kenny (2012); \ T. Yarkoni (2022)",
             r"P. C. M. Molenaar (2004); \ A. J. Fisher et al.\ (2018); \ W. S. Robinson (1950)",
             r"P. Kuppens et al.\ (2010); \ E. Dejonckheere et al.\ (2019)",
             r"M. Scheffer et al.\ (2009); \ I. A. van de Leemput et al.\ (2014)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Niall Bolger and "
            "Jean-Philippe Laurenceau's book teaches diary data; Gelman and Hill teach multilevel models by example; "
            "and Snijders and Bosker is the standard reference."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act XI: \ the graduate toolkit, \ 4 of 7", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 48", font_size=32, color=GREY_B),
                     label(r"Modelling Behaviour", font_size=36),
                     wrapped_label(r"When is a computational model of the mind more than a curve fit?", 6.0, 26,
                                   GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Four parts of the graduate toolkit done. <bookmark mark='a'/> This one matched the level of the data to "
            "the level of the claim. <bookmark mark='b'/> Next, the models themselves. When is a computational model "
            "of the mind more than a curve fit? Part 48: modelling behaviour."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
