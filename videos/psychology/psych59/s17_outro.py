from __future__ import annotations

from videos.psychology.psych59.common import *  # noqa: F403

PROBLEMS = [
    r"A task's retest reliability is 0.3 with 60 trials per condition. \ How many trials for 0.8?",
    r"A true correlation of 0.4; \ reliabilities 0.5 and 0.8. \ The expected observed correlation?",
    r"Features were chosen on all patients, \ then the model was cross-validated. \ Why is the estimate too high, "
    r"\ and how do you fix the pipeline?",
    r"Two halves of a sample give clusters that agree with an adjusted Rand index of 0.15. \ What do you conclude, "
    r"\ and what null would you compare against?",
    r"A choice rule's benefit is an interaction of size 0.2. \ About how many patients to detect it?",
    r"A phone feature correlates 0.6 with mood in 25 people. \ Give a 95\% interval for the correlation.",
    r"$\star$ \ Design a study to test whether model-based control is a treatment target: \ reliability, \ "
    r"intervention, \ mediation.",
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
        d = load("travel")
        b = load("biotypes")
        pai = load("pai")
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for n_, q, ans, col in (
                (r"1", r"trials for reliability 0.9, \ from 0.5 at 200", r"1{,}800", PERSON),
                (r"2", r"clusters with no types that differ in symptoms", rf"{int(np.sum(b['none_p'] < 0.05))} in 10",
                 MODEL),
                (r"3", r"AUC 0.72 at home; \ in a new trial", rf"{d['new_trial']:.2f} in Psyche", AUTH),
                (r"4", r"patients to show a choice rule works", rf"about {num(round(pai['inter'][1], -2))}", GOOD)):
            rows.add(VGroup(label(n_, font_size=30, color=col), wrapped_label(q, 6.4, 22, WHITE),
                            label(ans, font_size=24, color=col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"real group effects; \ individual measurement and generalization are the work left",
                             12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> To go from a reliability of zero point five at two hundred "
            "trials to zero point nine takes eighteen hundred. Clusters in data with no types differed in symptoms in "
            "nine studies out of ten. A model with an AUC of zero point seven two at home scored zero point five seven "
            "in a new trial, in Psyche. And showing that a choice rule works takes about fourteen hundred patients, "
            "four times the trial for the treatment itself. <bookmark mark='b'/> The group effects are real. "
            "Measuring individuals, and generalizing, are the work that's left."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=12.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"robust group effects can be unreliable individual measures", WHITE),
            (r"theory-driven and data-driven routes need the same discipline", MODEL),
            (r"compulsivity goes with less model-based control", MODEL),
            (r"anxiety and volatility: \ an idea with mixed evidence", MODEL),
            (r"mood as an integral of prediction errors", MODEL),
            (r"more trials, \ hierarchical models, \ many sessions", GOOD),
            (r"circular clusters always differ in symptoms; \ check stability", AUTH),
            (r"in-sample accuracy does not travel", AUTH),
            (r"choice rules need four times the sample", PERSON),
            (r"stimulation and psychedelics: \ sham, \ blinding, \ size", PERSON),
            (r"phones: \ small samples' strong correlations shrink", SYMP),
            (r"five tests for a target; \ none passed yet", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 59, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part fifty-nine in twelve lines. <bookmark mark='a'/> Robust group effects can be unreliable measures of "
            "individuals. The theory-driven and data-driven routes need the same discipline. Compulsivity goes with "
            "less model-based control. Anxiety and volatility is an idea with mixed evidence. Mood may be an integral "
            "of prediction errors. More trials, hierarchical models and many sessions fix measurement. Circular "
            "clusters always differ in symptoms, so check their stability. In-sample accuracy doesn't travel. Choice "
            "rules need four times the sample. Stimulation and psychedelics are judged by sham, blinding and size. "
            "Phones' strong correlations from small samples shrink. And there are five tests for a target, and none "
            "has been passed yet."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=34.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"models of minds, \ artificial and human", [60]),
            (r"the next psychology: \ big teams, \ registered models", [61]),
            (r"a dissertation that measures individuals", [62]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Models of minds, artificial and human, are Part 60. The next "
            "psychology, with big teams and registered models, is Part 61. And Part 62's dissertation can take on the "
            "measurement of individuals."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One buys reliability with "
            "trials. One attenuates a correlation. One repairs a leaky pipeline. One reads a stability check. One "
            "sizes a trial for a choice rule. One puts an interval on a small study's correlation. And the last, with "
            "the star, asks you to design a test of a computational treatment target. Pause here if you'd like to try "
            "them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"P. Seri\`es (ed.), \ \emph{Computational Psychiatry: A Primer}",
             r"A. D. Redish \& J. A. Gordon (eds.), \ \emph{Computational Psychiatry}",
             r"Q. J. M. Huys, \ T. V. Maia \& M. J. Frank (2016)"],
            [r"C. Hedge, \ G. Powell \& P. Sumner (2018); \ J. N. Rouder \& J. M. Haaf (2019)",
             r"C. M. Gillan et al.\ (2016); \ M. Browning et al.\ (2015); \ R. B. Rutledge et al.\ (2014)",
             r"A. T. Drysdale et al.\ (2017); \ R. Dinga et al.\ (2019)",
             r"A. M. Chekroud et al.\ (2016, \ 2024); \ R. J. DeRubeis et al.\ (2014)",
             r"E. J. Cole et al.\ (2022); \ G. M. Goodwin et al.\ (2022); \ T. R. Insel (2017)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Peggy Series's primer is the "
            "best introduction to the models; Redish and Gordon's volume surveys the field; and Huys, Maia and Frank's "
            "review sets out the two routes."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act XIII: \ the frontier, \ two of five", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 60", font_size=32, color=GREY_B),
                     label(r"Minds and Machines", font_size=34),
                     wrapped_label(r"what large language models can and cannot tell psychology", 6.0, 24, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Two parts of the frontier are done. <bookmark mark='a'/> This one asked whether models of the mind can "
            "reach the clinic, and found the road runs through measurement. <bookmark mark='b'/> The next asks about "
            "a different kind of model: machines that talk. What can large language models tell psychology, and what "
            "can psychology tell us about them? Part 60: Minds and Machines."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
