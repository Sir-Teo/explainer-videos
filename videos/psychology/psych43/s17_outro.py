from __future__ import annotations

from videos.psychology.psych43.common import *  # noqa: F403

PROBLEMS = [
    r"Using the normal approximation, \ find $d_{33}$ for an original study with 20 people per group.",
    r"An original study has 23 and 24 people. \ Find its power, \ two-sided at 5\%, \ for $d = 0.2$.",
    r"How many people per group does one study need for 95\% power at $d = 0.1$? \ Use the normal approximation.",
    r"An original reports $d = 0.68$ (SE 0.30); \ a replication finds $d = 0.04$ (SE 0.055). \ Compute the "
    r"replication Bayes factor in its normal form.",
    r"Lab A: \ 30 of 60 correct after describing, \ 40 of 60 without; \ lab B: \ 50 of 100 and 62 of 100. \ Pool the "
    r"risk differences with fixed-effect weights.",
    r"A multiverse has 3 estimators, \ 4 exclusion rules and 5 subsets of labs. \ How many analyses? \ If each had an "
    r"independent 5\% false-positive rate, \ how likely is at least one significant result?",
    r"$\star$ \ Write a preregistration for a Stroop replication run on the course site: \ hypothesis, \ smallest "
    r"effect of interest, \ sample size, \ exclusions and analysis.",
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
        c, p = load("confirm"), load("plans")
        head = heading(r"Your four predictions, \ checked")
        fewer = f"{-100 * c['vo_est']:.0f}"
        rows = VGroup()
        for n, q, ans, col in (
                (r"1", r"fewer correct picks per 100 after describing a face", fewer, PERSON),
                (r"2", r"ego depletion in 23 labs", rf"$g = {c['ed_est']:.2f}$: \ no", AUTH),
                (r"3", r"people per group for 95\% power at $d = 0.1$", num(p["ed_n95"]), MODEL),
                (r"4", r"the original's power for $d = 0.2$", rf"{100 * p['ed_power_orig']:.0f}\%", GOOD)):
            rows.add(VGroup(label(n, font_size=30, color=col), wrapped_label(q, 6.8, 23, WHITE),
                            label(ans, font_size=28, color=col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"one effect held, \ smaller; \ one did not; \ and the plan said in advance what each "
                             r"result would mean", 12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            f"First, your four predictions. <bookmark mark='a'/> Describing a face cost {fewer} correct picks per "
            f"hundred. Ego depletion, in twenty-three labs: no. One study would need about two thousand six hundred "
            f"people per group for ninety-five percent power at an effect of zero point one. And the original "
            f"depletion study had about ten percent power for an effect of zero point two. <bookmark mark='b'/> One "
            f"effect held, smaller; one did not; and the plan said in advance what each result would mean."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=8.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"a good target is important, \ uncertain and feasible", WHITE),
            (r"a direct replication repeats procedure, \ materials and analysis", SYMP),
            (r"the smallest effect of interest sets the sample size", MODEL),
            (r"$d_{33}$: \ the effect the original could have seen", MODEL),
            (r"the plan is code, \ run on simulated data before any real data", PERSON),
            (r"trial strips, \ counterbalancing, \ checks, \ consent and debriefing", PERSON),
            (r"open multi-lab data: \ 22 and 23 laboratories", GOOD),
            (r"verbal overshadowing held, \ smaller; \ ego depletion did not", GOOD),
            (r"three criteria and a Bayes factor can disagree", AUTH),
            (r"exploration is labelled, \ and makes hypotheses, \ not findings", AUTH),
            (r"the report is registered, \ and its data and code are open", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 43, \ in eleven lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part forty-three in eleven lines. <bookmark mark='a'/> A good target is important, uncertain and "
            "feasible. A direct replication repeats the procedure, the materials and the analysis. The smallest effect "
            "of interest sets the sample size. D thirty-three is the effect the original could have seen. The plan is "
            "code, run on simulated data before any real data. Trial strips, counterbalancing, checks, consent and "
            "debriefing make the experiment. Open multi-lab data came from twenty-two and twenty-three laboratories. "
            "Verbal overshadowing held, smaller; ego depletion did not. Three criteria and a Bayes factor can "
            "disagree. Exploration is labelled, and makes hypotheses, not findings. And the report is registered, with "
            "its data and code open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=40.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"power, \ $d_{33}$, \ random effects, \ a replication Bayes factor and a multiverse, \ computed",
             STATUS_COLOR["replicated"]),
            (r"two registered replications in 45 laboratories, \ and the viewer as a participant",
             STATUS_COLOR["replicated"]),
            (r"the outcomes here are behaviour, \ not reports; \ the objection is met where the measure allows",
             STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager, at the end of the degree. <bookmark mark='a'/> The first objection, that mathematics can't "
            "apply to the mind, met power, d thirty-three, random effects, a replication Bayes factor and a "
            "multiverse, all computed. <bookmark mark='b'/> The second, that the mind can't be experimented on, met "
            "two registered replications in forty-five laboratories, and you as a participant. <bookmark mark='c'/> "
            "And the third, about introspection: the outcomes here are behaviour, a line-up choice and response "
            "times, not reports. Where the measure allows, the objection is met. Green."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"latent variables: \ what a questionnaire measures", [44]),
            (r"people over time", [47]),
            (r"the weight of evidence: \ reading a literature", [50]),
            (r"the dissertation", [62]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Act Eleven starts next, with latent variables, in Part 44. "
            "People over time are Part 47. Reading a whole literature is Part 50. And the series ends with a "
            "dissertation, Part 62, built the way this part was."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=7.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One finds d thirty-three. "
            "One finds an original study's power. One sizes a single study. One computes a replication Bayes factor. "
            "One pools two labs. One counts a multiverse and its false positives. And the last, with the star, asks "
            "you to write a preregistration for the Stroop study on the site. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"C. D. Chambers, \ \emph{The Seven Deadly Sins of Psychology} (2017)",
             r"D. Lakens, \ \emph{Improving Your Statistical Inferences} (online book)",
             r"the Many Labs and Registered Replication Report protocols, \ published with their data"],
            [r"U. Simonsohn (2015); \ J. Verhagen \& E.-J. Wagenmakers (2014)",
             r"M. J. Brandt et al.\ (2014); \ R. A. Zwaan et al.\ (2018); \ D. Lakens (2022)",
             r"V. K. Alogna et al.\ (2014); \ M. S. Hagger et al.\ (2016)",
             r"B. A. Nosek \& T. M. Errington (2020); \ C. D. Chambers \& L. Tzavella (2022)",
             r"C. Allen \& D. M. A. Mehler (2019); \ A. M. Scheel et al.\ (2021)",
             r"J. J. Van Bavel et al.\ (2016); \ R. A. Klein et al.\ (2018)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Chris Chambers's The Seven "
            "Deadly Sins of Psychology tells why the reforms were needed; Daniel Lakens's online book teaches the "
            "statistics of this part; and the published protocols of the multi-lab replications are models of how to "
            "plan a study."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"the degree, \ complete", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 44", font_size=32, color=GREY_B),
                     label(r"Latent Variables", font_size=36),
                     wrapped_label(r"What does a questionnaire measure, \ and how would you know?", 6.0, 26, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "The degree is complete. <bookmark mark='a'/> Forty-three parts, from Kant's wager to a study that "
            "deserves to be believed. <bookmark mark='b'/> Act Eleven begins the graduate toolkit, with the question "
            "under every questionnaire in the series: what does it measure, and how would you know? Part 44: latent "
            "variables."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
