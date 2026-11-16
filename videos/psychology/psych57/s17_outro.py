from __future__ import annotations

from videos.psychology.psych57.common import *  # noqa: F403

PROBLEMS = [
    r"Placebo against no treatment: \ 40\% and 30\% improve. \ Placebo against baseline: \ 40\%. \ Which number is the "
    r"placebo effect?",
    r"Pain as inference: \ stimulus 7, \ expectation 5, \ sensory SD 1, \ prior SD 2. \ The felt intensity?",
    r"Diabetes: \ 11 cases per 100 person-years on placebo, \ 58\% fewer on lifestyle. \ Cases prevented per 100 "
    r"person-years?",
    r"A service gets 80 referrals a week; \ therapy lasts 10 weeks. \ How many therapy places must be open at once?",
    r"Adherence 50\%; \ a drug halves risk in those who take it. \ The effect in everyone prescribed it?",
    r"An open-label placebo trial: \ why can it not be blinded, \ and what outcome would persuade a sceptic?",
    r"$\star$ \ Plan an evaluation of a mental health app for a health system: \ trial, \ engagement, \ outcomes, \ "
    r"and privacy.",
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
        d = load("care")
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for n_, q, ans, col in (
                (r"1", r"open-label placebo against nothing", r"59\% against 35\% (contested)", PERSON),
                (r"2", r"new diabetes cases with lifestyle", r"58\% fewer", MODEL),
                (r"3", r"long-term medicines taken as prescribed", r"about half", AUTH),
                (r"4", r"recovered in six months, \ therapy only", rf"{100 * d['recovered_26'][0]:.0f}\% in Psyche",
                 GOOD)):
            rows.add(VGroup(label(n_, font_size=30, color=col), wrapped_label(q, 5.6, 22, WHITE),
                            label(ans, font_size=24, color=col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"modest effects in the body; \ large effects from systems that deliver what works",
                             12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> Open-label placebo patients reported relief more often "
            "than untreated ones, fifty-nine percent against thirty-five, though it's contested. Lifestyle cut new "
            "diabetes cases by fifty-eight percent. About half of long-term medicines are taken as prescribed. And in "
            "Psyche's service where everyone waits for therapy, about three in ten recover within six months. "
            "<bookmark mark='b'/> Modest effects in the body, and large effects from systems that deliver what "
            "works."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=9.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"stress raises susceptibility to infection", WHITE),
            (r"observational stress research cannot separate causes", SYMP),
            (r"placebo: \ small, \ subjective, \ partly opioid", SYMP),
            (r"open-label placebo: \ promising, \ contested", MODEL),
            (r"expectation is a prior on bodily signals; \ nocebo too", MODEL),
            (r"chronic pain is learned and maintained", PERSON),
            (r"behaviour is the treatment: \ adherence and diabetes", PERSON),
            (r"CBT for insomnia before pills", GOOD),
            (r"mindfulness: \ real for some, \ null in schools", AUTH),
            (r"capacity must match the flow", GOOD),
            (r"measure every session; \ flag the off-track", GOOD),
            (r"lay counsellors and apps, \ with their limits", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 57, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part fifty-seven in twelve lines. <bookmark mark='a'/> Stress raises susceptibility to infection. "
            "Observational stress research can't separate causes. The placebo effect is small, subjective, and partly "
            "opioid. Open-label placebo is promising and contested. Expectation is a prior on bodily signals, and so "
            "is the nocebo. Chronic pain is learned and maintained. Behaviour is the treatment, for adherence and for "
            "diabetes. CBT for insomnia comes before pills. Mindfulness is real for some, and null in schools. "
            "Capacity must match the flow. Measure every session, and flag the off-track. And lay counsellors and apps "
            "help, with their limits."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=34.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the predictive brain and interoception", [58]),
            (r"computational psychiatry", [59]),
            (r"chatbots and minds", [60]),
            (r"a dissertation on a health intervention", [62]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> The predictive brain, and the body's signals, are Part 58. "
            "Computational psychiatry is Part 59. Chatbots and minds are Part 60. And Part 62's dissertation can test a "
            "health intervention."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One finds the placebo "
            "effect. One computes a felt pain. One counts diabetes cases prevented. One sizes a service. One dilutes a "
            "drug's effect by adherence. One asks what would persuade a sceptic of open-label placebo. And the last, "
            "with the star, asks you to plan the evaluation of a mental health app. Pause here if you'd like to try "
            "them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"R. M. Sapolsky, \ \emph{Why Zebras Don't Get Ulcers}",
             r"F. Benedetti, \ \emph{Placebo Effects}",
             r"D. M. Clark (2018)"],
            [r"S. Cohen, \ D. A. J. Tyrrell \& A. P. Smith (1991); \ V. J. Felitti et al.\ (1998)",
             r"H. K. Beecher (1955); \ A. Hr\'objartsson \& P. C. G\o tzsche (2001); \ J. D. Levine et al.\ (1978)",
             r"T. J. Kaptchuk et al.\ (2010); \ Diabetes Prevention Program (2002)",
             r"W. Kuyken et al.\ (2022); \ M. Goyal et al.\ (2014)",
             r"M. J. Lambert et al.\ (2018); \ D. Chibanda et al.\ (2016)",
             r"A. J. Crum \& E. J. Langer (2007); \ R. H. Rosenman et al.\ (1975)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Sapolsky's book is the best "
            "introduction to stress and the body; Benedetti's is the reference on placebo; and Clark's paper describes "
            "a national service that counts its outcomes."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act XII: \ psychology at work, \ complete", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 58", font_size=32, color=GREY_B),
                     label(r"The Efficient, \ Predictive Brain", font_size=34),
                     wrapped_label(r"Act XIII: \ the frontier", 6.0, 26, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Psychology at work is complete. <bookmark mark='a'/> Seven parts took the science into cockpits, "
            "interfaces, offices, classrooms, governments, courts and clinics. <bookmark mark='b'/> Act Thirteen goes "
            "to the frontier, where the questions are open. It begins with the idea that the brain is a prediction "
            "machine. Part 58: the efficient, predictive brain."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
