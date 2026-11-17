from __future__ import annotations

from videos.psychology.psych42.common import *  # noqa: F403

PROBLEMS = [
    r"Each person's mean symptom score is $N(14, 5^2)$ and each occasion adds $N(0, 5^2)$. \ Someone enrols with a "
    r"score of 24. \ What is their expected score next time, \ with no treatment?",
    r"At the end of a trial the waiting list averages 18.85, \ placebo therapy 15.85 and active therapy 13.85, \ with "
    r"SD 6.7 in each arm. \ Find the active therapy's $d$ against each control.",
    r"Three trials find $d$ = 0.4, \ 0.6 and 0.2, \ with variances 0.04, \ 0.02 and 0.05. \ Find the fixed-effect "
    r"estimate, \ its SE, \ $Q$ and the DerSimonian-Laird $\hat\tau^2$.",
    r"A scale has SD 7 and reliability 0.85. \ Find the change needed for reliable change, \ and say whether a "
    r"client who goes from 26 to 20 has changed reliably.",
    r"The clinical group averages 28 (SD 6) and the well group 7 (SD 5). \ Find Jacobson and Truax's cut-off $c$.",
    r"A therapy's true effect is $d = 0.3$, \ trials have 20 people per arm, \ and only significant results are "
    r"published. \ Find the power, \ and the average published effect.",
    r"$\star$ \ Design a trial that could separate a therapy's specific ingredient from its common factors, \ and "
    r"show which comes first, \ the change in the mechanism or the improvement.",
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
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for n, q, ans, c in (
                (r"1", r"Smith and Glass's average effect size", r"0.68", PERSON),
                (r"2", r"published antidepressant trials that looked positive", r"94\%", MODEL),
                (r"3", r"the alliance-outcome correlation", r"about 0.28", SYMP),
                (r"4", r"sessions by which half of clients have improved", r"about 8", GOOD)):
            rows.add(VGroup(label(n, font_size=30, color=c), wrapped_label(q, 6.8, 23, WHITE),
                            label(ans, font_size=28, color=c)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"therapy works; \ the published effect is too big; \ the control sets the size", 12.0,
                             22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> Smith and Glass's average effect size: zero point six "
            "eight. Published antidepressant trials that looked positive: ninety-four percent, against about half at "
            "the regulator. The alliance-outcome correlation: about zero point two eight. And the sessions by which "
            "half of clients have improved: about eight. <bookmark mark='b'/> Therapy works. The published effect is "
            "too big. And the control sets the size."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=8.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"Eysenck, \ 1952: \ people improve anyway; \ only a control can say how much therapy adds", WHITE),
            (r"regression to the mean: \ people enrol at their worst, \ so every arm improves", MODEL),
            (r"the control sets the effect: \ waiting list, \ no treatment, \ placebo therapy", SYMP),
            (r"meta-analysis: \ standardized effects, \ weighted; \ Smith and Glass found 0.68", PERSON),
            (r"the dodo bird: \ bona fide therapies near-equal on average, \ with exceptions", SYMP),
            (r"the alliance correlates 0.28 with outcome; \ its direction is argued", MODEL),
            (r"therapy and medication do about equally well; \ therapy's effect outlasts it", GOOD),
            (r"publication bias inflates the effect; \ the real one is smaller, \ and real", AUTH),
            (r"reliable change and a cut-off say whether one person got better", PERSON),
            (r"some treatments harm: \ debriefing, \ Scared Straight, \ recovered memories", AUTH),
            (r"half improve by about 8 sessions; \ most people get no therapy at all", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 42, \ in eleven lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part forty-two in eleven lines. <bookmark mark='a'/> Eysenck, in 1952: people improve anyway, and only a "
            "control can say how much therapy adds. Regression to the mean: people enrol at their worst, so every arm "
            "improves. The control sets the effect: waiting list, no treatment, placebo therapy. Meta-analysis puts "
            "studies on one scale and weighs them; Smith and Glass found zero point six eight. The dodo bird: bona "
            "fide therapies are near-equal on average, with exceptions. The alliance correlates about zero point two "
            "eight with outcome, and its direction is argued. Therapy and medication do about equally well, and "
            "therapy's effect outlasts it. Publication bias inflates the effect; the real one is smaller, and real. "
            "Reliable change and a cut-off say whether one person got better. Some treatments harm: debriefing, "
            "Scared Straight, recovered memories. And half of clients improve by about eight sessions, while most "
            "people get no therapy at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=40.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"regression to the mean, \ random effects, \ reliable change and a filter, \ computed",
             STATUS_COLOR["replicated"]),
            (r"randomized trials of talking, \ with controls chosen to answer different questions",
             STATUS_COLOR["replicated"]),
            (r"outcomes are mostly self-reports, \ and patients cannot be blind to therapy",
             STATUS_COLOR["contested"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "regression to the mean, random effects, reliable change and a publication filter, all computed. "
            "<bookmark mark='b'/> The second, that the mind can't be experimented on, met randomized trials of "
            "talking, with controls chosen to answer different questions. <bookmark mark='c'/> And the third, about "
            "introspection: outcomes are mostly self-reports, and patients can't be blind to therapy. Amber."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"one study replicated from start to finish", [43]),
            (r"the weight of evidence: \ meta-analysis and bias, \ properly", [50]),
            (r"health and care: \ closing the treatment gap", [57]),
            (r"computational psychiatry: \ matching treatments to people", [59]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> One study replicated from start to finish is next, in Part "
            "43, the capstone. Meta-analysis and its biases, properly, are Part 50. Closing the treatment gap is Part "
            "57. And matching treatments to people is Part 59."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=7.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One computes regression to "
            "the mean. One turns end scores into effect sizes against three controls. One does a small meta-analysis "
            "by hand. One finds reliable change. One finds the cut-off. One works out what a significance filter does "
            "to the published effect. And the last, with the star, asks you to design a trial that separates a "
            "specific ingredient from the common factors. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"B. E. Wampold \& Z. E. Imel, \ \emph{The Great Psychotherapy Debate} (2nd edition, \ 2015)",
             r"E. S. Valenstein, \ \emph{Great and Desperate Cures} (1986)",
             r"M. L. Smith, \ G. V. Glass \& T. I. Miller, \ \emph{The Benefits of Psychotherapy} (1980)"],
            [r"H. J. Eysenck (1952); \ M. L. Smith \& G. V. Glass (1977); \ L. Luborsky et al.\ (1975)",
             r"B. E. Wampold et al.\ (1997); \ D. F. Tolin (2010); \ C. Flückiger et al.\ (2018)",
             r"M. M. Linehan et al.\ (1991, \ 2006); \ S. D. Hollon et al.\ (2005)",
             r"E. H. Turner et al.\ (2008); \ E. Driessen et al.\ (2015); \ P. Cuijpers et al.\ (2019)",
             r"N. S. Jacobson \& P. Truax (1991); \ K. I. Howard et al.\ (1986)",
             r"S. O. Lilienfeld (2007); \ R. A. Mayou et al.\ (2000); \ A. Petrosino et al.\ (2013)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Wampold and Imel's The Great "
            "Psychotherapy Debate makes the case for common factors; Valenstein's Great and Desperate Cures tells the "
            "history of lobotomy; and Smith, Glass and Miller's book is the full meta-analysis that answered Eysenck."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act X: \ when minds suffer, \ complete", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 43", font_size=32, color=GREY_B),
                     label(r"The Replication", font_size=36),
                     wrapped_label(r"Can you run a study that deserves to be believed?", 6.0, 26,
                                   GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Act Ten is complete. <bookmark mark='a'/> It asked what a disorder is, built fear and sadness, psychosis "
            "and addiction from the series' own models, and weighed the evidence for therapy. "
            "<bookmark mark='b'/> The next part is the capstone of the degree. One classic effect from the Ledger, "
            "replicated properly on screen, from the choice of target to the report, with the viewer as a "
            "participant. Part 43: the replication."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
