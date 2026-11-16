from __future__ import annotations

from videos.psychology.psych50.common import *  # noqa: F403

PROBLEMS = [
    r"Three studies: \ $d$ = 0.2, \ 0.5, \ 0.3 with variances 0.01, \ 0.04, \ 0.02. \ Find the fixed-effect estimate.",
    r"$Q$ = 30 on 14 degrees of freedom. \ Find $I^2$.",
    r"A random-effects mean of 0.4 with SE 0.05 and $\tau$ = 0.2: \ give a rough 95\% prediction interval.",
    r"$n$ = 17 answers on a 1-to-5 scale, \ reported mean 3.48. \ Apply GRIM.",
    r"Reported: \ $t(24) = 1.90$, \ $p = .03$ (two-sided). \ Recompute $p$; \ is the error gross?",
    r"PET's intercept is 0.05 (SE 0.06) and the naive estimate 0.38. \ What do you report?",
    r"$\star$ \ Plan a meta-analysis of a literature you suspect is filtered: \ search, \ registries, \ models, \ "
    r"corrections and how you will present their disagreement.",
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
        g, f, s, a = load("grim"), load("funnel"), load("specs"), load("audit")
        tot = np.asarray(a["total"])
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for k, q, ans, col in (
                (r"1", r"a mean of 5.19 from 28 whole-number answers", r"impossible", PERSON),
                (r"2", r"a filtered literature's pooled estimate (truth 0.2)", rf"{f['naive']:.2f}", AUTH),
                (r"3", r"significant analyses among 96", rf"{100 * s['share_sig']:.0f}\%", MODEL),
                (r"4", r"Ledger rows failed or retracted", rf"{100 * (tot[4] + tot[5]) / a['n']:.0f}\%", GOOD)):
            rows.add(VGroup(label(k, font_size=30, color=col), wrapped_label(q, 6.4, 22, WHITE),
                            label(ans, font_size=26, color=col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"a literature is evidence in proportion to how much of it would have been seen whatever "
                             r"it found", 12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> A mean of five point one nine from twenty-eight "
            "whole-number answers is impossible. A filtered literature with a true effect of zero point two pooled to "
            "about zero point four. About half of ninety-six defensible analyses came out significant. And about one "
            "in seven of the Ledger's rows failed or were retracted. <bookmark mark='b'/> A literature is evidence in "
            "proportion to how much of it would have been seen whatever it found."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=9.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"the published pile is not the pile of studies run", WHITE),
            (r"fixed effects: \ one truth; \ random effects: \ a distribution", SYMP),
            (r"the prediction interval answers the practitioner's question", SYMP),
            (r"moderators hide: \ meta-regression has few cases and no randomization", MODEL),
            (r"a funnel with a bite: \ Egger, \ PET and PEESE", MODEL),
            (r"every correction method fails somewhere", PERSON),
            (r"filtered meta-analyses run about three times the replications", PERSON),
            (r"registered reports remove the filter", GOOD),
            (r"GRIM, \ SPRITE and statcheck test numbers without data", AUTH),
            (r"open data is what makes fabrication findable", AUTH),
            (r"many analysts, \ one dataset: \ show the whole curve", GOOD),
            (r"large samples cure noise, \ not weak theory", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 50, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part fifty in twelve lines. <bookmark mark='a'/> The published pile isn't the pile of studies run. Fixed "
            "effects assume one truth, random effects a distribution, and the prediction interval answers the "
            "practitioner's question. Moderators hide, because meta-regression has few cases and no randomization. A "
            "filtered funnel has a bite taken out, read by Egger, PET and PEESE. Every correction method fails "
            "somewhere, and filtered meta-analyses run about three times the replications. Registered reports remove "
            "the filter. GRIM, SPRITE and statcheck test numbers without the data, and open data makes fabrication "
            "findable. With many analysts and one dataset, show the whole curve. And large samples cure noise, not "
            "weak theory."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=38.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"pooling, \ correction and forensics, \ each tested on literatures with a known truth",
             STATUS_COLOR["replicated"]),
            (r"registered and multi-site designs: \ experiments on the way science itself is done",
             STATUS_COLOR["replicated"]),
            (r"the audit counts outcomes, \ not reports; \ but a field's beliefs still steer what it tests",
             STATUS_COLOR["contested"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection met pooling, correction and forensics, each tested "
            "on literatures where the truth was known. Green. <bookmark mark='b'/> The second met registered and "
            "multi-site designs: experiments on the way science itself is done. Green. <bookmark mark='c'/> And the "
            "third. The audit counts outcomes, not reports, but a field's beliefs still steer what it chooses to "
            "test. Amber."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"psychology at work, \ judged by evidence", [51, 52, 53, 54, 55, 56, 57]),
            (r"incentives and the science of science", [61]),
            (r"a dissertation that meets this standard", [62]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Every part of Act Twelve, psychology at work, judges its "
            "practices by this standard. Incentives and the science of science are Part 61. And the series ends with "
            "a dissertation that has to meet it, in Part 62."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One pools three studies. "
            "One finds I squared. One draws a prediction interval. One applies GRIM. One recomputes a p-value. One "
            "decides what to report when PET and the naive estimate disagree. And the last, with the star, asks you to "
            "plan a meta-analysis of a literature you suspect is filtered. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"M. Borenstein, \ L. V. Hedges, \ J. P. T. Higgins \& H. R. Rothstein, \ \emph{Introduction to "
             r"Meta-Analysis} (2009)",
             r"E. H. Turner et al.\ (2008)",
             r"P. E. Meehl, \ Theoretical risks and tabular asterisks (1978)"],
            [r"E. C. Carter et al.\ (2019); \ T. D. Stanley \& H. Doucouliagos (2014); \ J. L. Vevea \& L. V. Hedges (1995)",
             r"A. Kvarven et al.\ (2020); \ A. M. Scheel et al.\ (2021)",
             r"N. J. L. Brown \& J. A. J. Heathers (2017); \ M. B. Nuijten et al.\ (2016)",
             r"R. Silberzahn et al.\ (2018); \ S. Steegen et al.\ (2016); \ U. Simonsohn et al.\ (2020)",
             r"K. Oberauer \& S. Lewandowsky (2019); \ T. Yarkoni (2022)",
             r"P. E. Smaldino \& R. McElreath (2016)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Borenstein and colleagues teach "
            "meta-analysis; Turner's paper is the clearest picture of a filter; and Meehl's essay of 1978 is still the "
            "sharpest argument about what a significant result can show."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act XI: \ the graduate toolkit, \ complete", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 51", font_size=32, color=GREY_B),
                     label(r"Human Factors", font_size=36),
                     wrapped_label(r"Act XII: \ psychology at work", 6.0, 26, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "The graduate toolkit is complete. <bookmark mark='a'/> Seven parts built the methods a researcher uses "
            "after the degree, and this one turned them on the literature itself. <bookmark mark='b'/> Act Twelve "
            "takes psychology to work: to cockpits and control rooms, products and offices, classrooms, courts and "
            "clinics. It begins where design meets the human limits of Acts Three to Six. Part 51: human factors."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
