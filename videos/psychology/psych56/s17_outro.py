from __future__ import annotations

from videos.psychology.psych56.common import *  # noqa: F403

PROBLEMS = [
    r"A line-up: \ correct-ID rate 0.60, \ innocent-suspect rate 0.05. \ The diagnosticity ratio, \ and the posterior "
    r"odds from prior odds 1:4?",
    r"Six faces, \ culprit absent, \ a fair line-up and a witness who picks someone 60\% of the time: \ how often "
    r"is the innocent suspect picked?",
    r"Why can a higher diagnosticity ratio come with a worse ROC? \ Draw two curves.",
    r"Lie judgements: \ 61\% of truths and 47\% of lies judged correctly. \ Overall accuracy with equal numbers?",
    r"IQ 69, \ reliability 0.95, \ SD 15: \ the SEM and the 95\% interval.",
    r"Base rates 0.2 and 0.4, \ one calibrated score: \ explain why the false-positive rates must differ.",
    r"$\star$ \ Write the line-up protocol for a police force, \ with the reason for each rule.",
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
        d, iq = load("onyou"), load("iq")
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for n_, q, ans, col in (
                (r"1", r"culprit absent: \ someone picked", rf"{100 * d['absent_any']:.0f}\% in Psyche", PERSON),
                (r"2", r"lie judgements correct", r"54\%", MODEL),
                (r"3", r"students who signed a false confession", r"about two thirds", AUTH),
                (r"4", r"IQ 71, \ reliability 0.97", rf"{iq['lo']:.0f} to {iq['hi']:.0f}", GOOD)):
            rows.add(VGroup(label(n_, font_size=30, color=col), wrapped_label(q, 5.6, 22, WHITE),
                            label(ans, font_size=24, color=col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"evidence is as good as the procedure that produced it", 12.0, 22,
                             YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> When the culprit was absent, sixty-four percent of "
            "Psyche's witnesses still picked someone. Lie judgements are right fifty-four percent of the time. About "
            "two thirds of falsely accused students signed a confession. And an IQ of seventy-one, from a test with "
            "reliability zero point nine seven, has an interval from sixty-six to seventy-six. <bookmark mark='b'/> "
            "Evidence is as good as the procedure that produced it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=9.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"most early DNA exonerations involved a mistaken witness", WHITE),
            (r"a line-up is signal detection: \ judge it by its ROC", SYMP),
            (r"sequential line-ups shift the criterion", SYMP),
            (r"initial high confidence is diagnostic; \ later confidence is not", MODEL),
            (r"double-blind, \ fair fillers, \ confidence recorded", MODEL),
            (r"false evidence produces false confessions", AUTH),
            (r"lie detection: \ 54\%", AUTH),
            (r"context bends experts on ambiguous evidence", PERSON),
            (r"suggestion can create detailed false memories", PERSON),
            (r"hungry judges, \ or the order of cases", PERSON),
            (r"calibration and equal errors cannot both hold", GOOD),
            (r"a score in court has an error and a date", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 56, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part fifty-six in twelve lines. <bookmark mark='a'/> Most early DNA exonerations involved a mistaken "
            "witness. A line-up is signal detection, so judge it by its ROC. Sequential line-ups shift the criterion. "
            "Initial high confidence is diagnostic, and later confidence isn't. Run line-ups double-blind, with fair "
            "fillers and confidence recorded. False evidence produces false confessions. Lie detection runs at "
            "fifty-four percent. Context bends experts on ambiguous evidence. Suggestion can create detailed false "
            "memories. Hungry judges may be the order of cases. Calibration and equal error rates can't both hold. "
            "And a score in court has an error and a date."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=34.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"assessment and care in health", [57]),
            (r"computational psychiatry and risk", [59]),
            (r"fairness in machines", [60]),
            (r"incentives in science", [61]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Assessment and care in health are Part 57. Prediction and "
            "risk in psychiatry are Part 59. Fairness in machines is Part 60. And the incentives that shape science "
            "itself are Part 61."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One weighs an "
            "identification by Bayes's rule. One finds how often a fair line-up catches an innocent suspect. One "
            "explains why a better ratio can mean a worse curve. One computes lie-detection accuracy. One puts an "
            "interval on an IQ score. One explains the impossibility result. And the last, with the star, asks you to "
            "write a line-up protocol for a police force. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"B. L. Garrett, \ \emph{Convicting the Innocent} (2011)",
             r"J. T. Wixted \& G. L. Wells (2017)",
             r"G. L. Wells et al.\ (2020)"],
            [r"R. C. L. Lindsay \& G. L. Wells (1985); \ J. T. Wixted \& L. Mickes (2014)",
             r"S. M. Kassin \& K. L. Kiechel (1996); \ S. M. Kassin et al.\ (2010)",
             r"C. F. Bond \& B. M. DePaulo (2006); \ National Research Council (2003, \ 2009)",
             r"I. E. Dror, \ D. Charlton \& A. E. P\'eron (2006); \ S. J. Ceci \& M. Bruck (1995)",
             r"S. Danziger et al.\ (2011); \ A. Gl\"ockner (2016)",
             r"A. Chouldechova (2017); \ J. Kleinberg et al.\ (2016)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Garrett's book tells the "
            "exoneration cases; Wixted and Wells's review is the modern account of confidence; and the 2020 "
            "recommendations are the procedure."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act XII: \ psychology at work, \ 6 of 7", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 57", font_size=32, color=GREY_B),
                     label(r"Health and Care", font_size=36),
                     wrapped_label(r"how can psychology reach everyone who needs help?", 6.0, 26, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Six parts of Act Twelve are done. <bookmark mark='a'/> This one weighed memories, confessions and experts "
            "by the procedures that produced them. <bookmark mark='b'/> The last part of the act goes to health and "
            "care. How can psychology reach everyone who needs help? Part 57: health and care."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
