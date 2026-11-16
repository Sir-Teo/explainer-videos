from __future__ import annotations

from videos.psychology.psych49.common import *  # noqa: F403

PROBLEMS = [
    r"A pipeline has 5 binary choices and 3 thresholds. \ How many paths? \ If each were an independent test at "
    r"5\%, \ how likely is at least one false positive?",
    r"20 people, \ a contrast with mean 0.3 and SD 1.0 across people. \ Find the random-effects $t$.",
    r"A map has 50,000 voxels. \ Find the Bonferroni threshold for a familywise rate of 5\%.",
    r"A 2-target interface is right 80\% of the time, \ one choice every 2 s. \ Find bits per minute.",
    r"A true correlation of 0.25; \ the brain measure's reliability is 0.5 and the behaviour's 0.9. \ Find the "
    r"expected observed correlation.",
    r"Why does selecting voxels on all the data before cross-validation inflate accuracy? \ Give the fix.",
    r"$\star$ \ Plan a brain-behaviour study of working memory and a fronto-parietal measure: \ sample size, \ "
    r"reliability, \ pipeline, \ and a held-out test.",
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
        m, dc, b, t = load("multiverse"), load("decoding"), load("bwas"), load("thresholds")
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for k, q, ans, col in (
                (r"1", r"different maps from 72 pipelines", rf"{m['distinct']}", PERSON),
                (r"2", r"leaky decoding of pure noise", rf"{100 * dc['null_leaky']:.0f}\%", MODEL),
                (r"3", r"average reported $|r|$ at $n = 25$ (truth 0.1)", rf"{b['reported'][0]:.2f}", AUTH),
                (r"4", r"people for 80\% power at $r = 0.1$", rf"{num(t['n_r01'])}", GOOD)):
            rows.add(VGroup(label(k, font_size=30, color=col), wrapped_label(q, 6.4, 22, WHITE),
                            label(ans, font_size=26, color=col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"a brain map is a measurement made by a pipeline: \ fix the pipeline, \ match the "
                             r"threshold to the noise and the sample to the effect", 12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> Seventy-two pipelines gave forty-four different maps. A "
            "decoder that chose its voxels with all the data read pure noise at ninety-four percent. With twenty-five "
            "people, the significant correlations averaged about zero point four seven, when the truth was zero "
            "point one. And eighty percent power for that truth takes about seven hundred and eighty people. "
            "<bookmark mark='b'/> A brain map is a measurement made by a pipeline. Fix the pipeline, match the "
            "threshold to the noise, and match the sample to the effect."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=9.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"one dataset, \ many pipelines, \ different answers", WHITE),
            (r"preprocessing choices are forks; \ motion makes connections", SYMP),
            (r"the second level treats people as the sample", SYMP),
            (r"lenient clusters fail; \ permutation lets the noise set the bar", MODEL),
            (r"the threshold is a decision about errors", MODEL),
            (r"decoders leak when any choice sees the test data", PERSON),
            (r"geometry compares tables of distances, \ up to a noise ceiling", PERSON),
            (r"encoding models are judged by prediction", AUTH),
            (r"global-signal regression makes anticorrelations", AUTH),
            (r"windows chosen from the answer give false positives", GOOD),
            (r"populations code what single cells cannot", GOOD),
            (r"brain-behaviour claims need thousands of people and reliable measures", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 49, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part forty-nine in twelve lines. <bookmark mark='a'/> One dataset, many pipelines, different answers. "
            "Preprocessing choices are forks, and head motion makes connections. The second level treats people as "
            "the sample. Lenient clusters fail, and permutation lets the noise set the bar. The threshold is a "
            "decision about errors. Decoders leak when any choice sees the test data. Geometry compares tables of "
            "distances, up to a noise ceiling. Encoding models are judged by prediction. Global-signal regression "
            "makes anticorrelations. Windows chosen from the answer give false positives. Populations code what "
            "single cells cannot. And brain-behaviour claims need thousands of people, and reliable measures."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=38.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"group models, \ permutation tests, \ decoders and encoding models, \ all run on a brain whose truth "
             r"was known", STATUS_COLOR["replicated"]),
            (r"experiments with brains: \ designed tasks, \ and devices that act on the decoded intention",
             STATUS_COLOR["replicated"]),
            (r"brain data are not reports: \ but what a region ``represents'' is still read through a model",
             STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection met group models, permutation tests, decoders and "
            "encoding models, all run on a brain whose truth was known. Green. <bookmark mark='b'/> The second met "
            "designed experiments with brains, and devices that act on a decoded intention. Green. "
            "<bookmark mark='c'/> And the third, about introspection. Brain data aren't reports, though what a region "
            "represents is still read through a model. Green."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the weight of evidence across studies", [50]),
            (r"the predictive brain", [58]),
            (r"computational psychiatry and its biomarkers", [59]),
            (r"brains and machines compared", [60]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> The weight of evidence across studies is next, in Part 50. "
            "The predictive brain is Part 58. Computational psychiatry, and its search for biomarkers, is Part 59. "
            "And brains and machines compared are Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=7.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One counts pipelines. One "
            "computes a group t. One finds a Bonferroni threshold. One computes bits per minute. One attenuates a "
            "correlation. One explains a leak. And the last, with the star, asks you to plan a brain-behaviour study "
            "that would deserve to be believed. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"R. A. Poldrack, \ J. A. Mumford \& T. E. Nichols, \ \emph{Handbook of Functional MRI Data Analysis} "
             r"(2011)",
             r"S. J. Luck, \ \emph{An Introduction to the Event-Related Potential Technique} (2nd ed., \ 2014)",
             r"R. Botvinik-Nezer et al., \ Variability in the analysis of a single neuroimaging dataset by many teams "
             r"(2020)"],
            [r"J. Carp (2012); \ T. E. Nichols \& A. P. Holmes (2002); \ A. Eklund et al.\ (2016)",
             r"J. V. Haxby et al.\ (2001); \ N. Kriegeskorte et al.\ (2008)",
             r"T. Naselaris et al.\ (2011); \ A. G. Huth et al.\ (2016)",
             r"M. E. Raichle et al.\ (2001); \ J. D. Power et al.\ (2012); \ K. Murphy et al.\ (2009)",
             r"A. P. Georgopoulos et al.\ (1982); \ J. R. Wolpaw et al.\ (2002)",
             r"S. Marek et al.\ (2022); \ M. L. Elliott et al.\ (2020); \ E. Jonas \& K. P. Kording (2017)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Poldrack, Mumford and Nichols "
            "teach the fMRI pipeline; Steven Luck's book is the standard for ERPs; and the seventy-team paper is the "
            "best single argument for registering an analysis."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act XI: \ the graduate toolkit, \ 6 of 7", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 50", font_size=32, color=GREY_B),
                     label(r"The Weight of Evidence", font_size=36),
                     wrapped_label(r"What does a whole literature say, \ and can it be trusted to say it?", 6.0, 26,
                                   GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Six parts of the graduate toolkit done. <bookmark mark='a'/> This one followed the brain's data from the "
            "scanner to the claim. <bookmark mark='b'/> Next, whole literatures. A regulator holds the registered "
            "results of seventy-four antidepressant trials, and the journals tell a different story. What does a "
            "literature say, and can it be trusted to say it? Part 50: the weight of evidence."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
