from __future__ import annotations

from videos.psychology.psych58.common import *  # noqa: F403

PROBLEMS = [
    r"Laughlin's rule: \ contrasts are uniform on $[-1, 1]$. \ The best response curve? \ And if they are normal?",
    r"Image power falls as $1/f^2$. \ How must a whitening filter's gain grow with $f$, \ and what does that do to "
    r"noise?",
    r"Normalization with $n = 2$, \ $\sigma = 0.15$: \ the response to $c = 0.15$ alone, \ and with a mask of 0.15?",
    r"Prior N(0, 1), \ reading $x = 2$ with noise SD 0.5. \ The posterior mean and variance, \ and the surprise?",
    r"Each sample is right with probability 0.65. \ The accuracy of a majority of three?",
    r"``The brain minimizes free energy.'' \ What observation would count against it?",
    r"$\star$ \ Design an experiment that separates predictive coding from adaptation as the cause of a mismatch "
    r"response.",
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
        t = load("tilt")
        b = load("bias")
        i20 = int(np.argmin(abs(np.asarray(t["tests"]) - 20)))
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for n_, q, ans, col in (
                (r"1", r"vertical after 20 degrees clockwise", rf"tilted counterclockwise, \ about "
                                                               rf"{t['shift'][i20]:.0f} degrees in Psyche", PERSON),
                (r"2", r"near-cardinal lines", rf"pushed away, \ about {np.max(np.abs(b['bias'])):.1f} degrees", MODEL),
                (r"3", r"which contrasts get the most levels", r"the commonest, \ near zero", AUTH),
                (r"4", r"samples, \ when each costs time", r"one", GOOD)):
            rows.add(VGroup(label(n_, font_size=30, color=col), wrapped_label(q, 5.0, 22, WHITE),
                            wrapped_label(ans, 5.6, 22, col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"each answer follows from a code doing its best with limited resources", 12.0, 22,
                             YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> After lines tilted twenty degrees clockwise, a vertical "
            "line looks tilted counterclockwise, by about four degrees in Psyche and a few in people. Lines near "
            "vertical are pushed away from it, by about two and a half degrees. The commonest contrasts, near zero, "
            "get the most levels. And when each sample costs time, the best number is one. <bookmark mark='b'/> Each "
            "answer follows from a code doing its best with limited resources."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=12.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"sparse codes for images grow edge detectors", WHITE),
            (r"efficient codes match the world's statistics (Laughlin)", MODEL),
            (r"whitening derives centre-surround", MODEL),
            (r"adaptation re-centres the code; \ after-effects are the price", PERSON),
            (r"efficient encoding makes biases repulsive", PERSON),
            (r"rate-distortion derives generalization gradients", MODEL),
            (r"normalization: \ one equation, \ many places", GOOD),
            (r"predictive coding: \ errors up, \ predictions down; \ contested", AUTH),
            (r"free energy: \ a theorem, \ a framework, \ untested as a principle", AUTH),
            (r"Bayesian models predict when priors are measured", SYMP),
            (r"heuristics can be rational when thinking costs", SYMP),
            (r"a principle is judged by what it risks", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 58, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part fifty-eight in twelve lines. <bookmark mark='a'/> Sparse codes for images grow edge detectors. "
            "Efficient codes match the world's statistics, as Laughlin's fly showed. Whitening derives centre-surround "
            "cells. Adaptation re-centres the code, and after-effects are the price. Efficient encoding makes biases "
            "repulsive. Rate-distortion theory derives generalization gradients. Normalization is one equation in "
            "many places. Predictive coding sends errors up and predictions down, and is contested. The free energy "
            "is a theorem and a framework, untested as a principle. Bayesian models predict when priors are measured. "
            "Heuristics can be rational when thinking costs. And a principle is judged by what it risks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=34.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"priors and precision in psychiatry", [59]),
            (r"machines that learn from examples in context", [60]),
            (r"a dissertation that tests a principle", [62]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Priors and precision in psychiatry are Part 59. Machines "
            "that learn from examples in context are Part 60. And Part 62's dissertation can test a principle."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One applies Laughlin's "
            "rule. One designs a whitening filter. One computes a normalized response. One does variational inference "
            "by hand. One counts a majority of samples. One asks what would count against the free-energy principle. "
            "And the last, with the star, asks you to separate predictive coding from adaptation. Pause here if "
            "you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"A. Hyv\"arinen, \ J. Hurri \& P. O. Hoyer, \ \emph{Natural Image Statistics}",
             r"P. Dayan \& L. F. Abbott, \ \emph{Theoretical Neuroscience}",
             r"T. Parr, \ G. Pezzulo \& K. J. Friston, \ \emph{Active Inference}"],
            [r"H. B. Barlow (1961); \ S. Laughlin (1981); \ E. P. Simoncelli \& B. A. Olshausen (2001)",
             r"B. A. Olshausen \& D. J. Field (1996); \ A. J. Bell \& T. J. Sejnowski (1997)",
             r"X.-X. Wei \& A. A. Stocker (2015, \ 2017); \ C. R. Sims (2018); \ M. Carandini \& D. J. Heeger (2012)",
             r"R. P. N. Rao \& D. H. Ballard (1999); \ K. Friston (2010)",
             r"J. S. Bowers \& C. J. Davis (2012); \ F. Lieder \& T. L. Griffiths (2020)",
             r"T. P. Lillicrap et al.\ (2020); \ A. Newell (1973)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Hyvarinen, Hurri and Hoyer's "
            "book is the best introduction to natural image statistics; Dayan and Abbott's is the standard text on "
            "theoretical neuroscience; and Parr, Pezzulo and Friston's sets out active inference from its authors' "
            "side."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act XIII: \ the frontier, \ one of five", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 59", font_size=32, color=GREY_B),
                     label(r"Computational Psychiatry", font_size=34),
                     wrapped_label(r"can a model of the mind help a clinician?", 6.0, 24, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "The first part of the frontier is done. <bookmark mark='a'/> It asked whether one principle explains "
            "the mind, and found several that explain a great deal of perception. <bookmark mark='b'/> The next part "
            "takes those models to the clinic: learning rates, priors and precision as places where illness might "
            "live. Part 59: computational psychiatry."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
