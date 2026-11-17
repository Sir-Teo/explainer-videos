from __future__ import annotations

from videos.psychology.psych36.common import *  # noqa: F403

PROBLEMS = [
    r"In Tajfel's matrix (top row $7 + j$, \ bottom row $1 + 2j$, \ $j = 0, \dots, 12$), \ find the columns that "
    r"maximize the joint total, \ the ingroup's points, \ and the ingroup's lead, \ and the column that is fair.",
    r"Hamilton and Gifford's groups have 18 and 9 desirable acts and 8 and 4 undesirable ones. \ If the smaller "
    r"group's undesirable acts are remembered with weight $1 + b$, \ find the remembered undesirable share for each "
    r"group as a function of $b$.",
    r"In a list experiment with $J$ control items, \ each held independently with probability $p_j$, \ and a "
    r"sensitive item with prevalence $\pi$, \ show that the difference in mean counts is unbiased for $\pi$, \ and "
    r"find its variance with $n$ people per arm.",
    r"A measure has test-retest reliability $\rho_{xx}$, \ and the trait it measures correlates $r$ with a "
    r"behaviour measured without error. \ Show that the observed correlation is at most $r\sqrt{\rho_{xx}}$.",
    r"Callback rates are 9.6\% and 6.4\%. \ Find the number of applications per group that detects the gap with "
    r"80\% power at the two-sided 5\% level.",
    r"At each level of a ladder the top half of a pool is promoted; \ one group's scores are $N(\delta, 1)$, \ the "
    r"other's $N(0, 1)$. \ Write the equation for the cut-off, \ and show that the disadvantaged share falls at every "
    r"level.",
    r"$\star$ \ Design a field experiment that tests whether a diversity training changes hiring decisions, \ and say "
    r"what you would measure, \ for how long, \ and how many teams you need.",
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
                (r"1", r"extra callbacks for white-sounding names", r"50\%", CROWD),
                (r"2", r"correlation between two IAT sessions", r"about .5", MODEL),
                (r"3", r"fall in hiring discrimination against Black applicants, \ 1989 to 2015", r"none", AUTH),
                (r"4", r"effect of the stereotype on the Dutch girls' maths scores", r"none found", PERSON)):
            rows.add(VGroup(label(n, font_size=30, color=c), wrapped_label(q, 6.8, 23, WHITE),
                            label(ans, font_size=28, color=c)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"the reaction-time measure is noisy and the famous threat effect shrank; \ the "
                             r"behaviour, \ measured directly, \ has not moved", 12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> Extra callbacks for white-sounding names: fifty "
            "percent. The correlation between two IAT sessions: about point five. The fall in hiring "
            "discrimination against Black applicants from 1989 to 2015: none. And the effect of the stereotype on "
            "the Dutch girls' maths scores: none found. <bookmark mark='b'/> The reaction-time measure is noisy, "
            "and the famous threat effect shrank. The behaviour, measured directly, hasn't moved."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=8.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"a meaningless label is enough for favouritism", IN),
            (r"part of who we are is our groups; \ favouritism is mostly warmth for us", CROWD),
            (r"Robbers Cave was a demonstration, \ after a first run that failed", P.ACCENT),
            (r"stereotypes are categories with consequences; \ a minority can earn a bad name from memory alone", PERSON),
            (r"a list experiment buys privacy with precision", MODEL),
            (r"the IAT: \ clear for a crowd, \ noisy for a person, \ and changing it does not change behaviour", MODEL),
            (r"identical r\'esum\'es: \ 50\% more callbacks, \ and no change in 25 years", AUTH),
            (r"stereotype threat: \ a misread adjustment and a null registered test", AUTH),
            (r"contact helps on average; \ randomized tests are few", GOOD),
            (r"norms moved in Rwanda; \ a real conversation moved attitudes for months", GOOD),
            (r"small biases compound on a ladder", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 36, \ in eleven lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part thirty-six in eleven lines. <bookmark mark='a'/> A meaningless label is enough for favouritism. "
            "Part of who we are is our groups, and favouritism is mostly warmth for us. Robbers Cave was a "
            "demonstration, after a first run that failed. Stereotypes are categories with consequences, and a "
            "minority can earn a bad name from memory alone. A list experiment buys privacy with precision. The "
            "IAT is clear for a crowd, noisy for a person, and changing it doesn't change behaviour. Identical "
            "résumés get fifty percent more callbacks with a white-sounding name, with no change in twenty-five "
            "years. Stereotype threat rests on a misread adjustment, and a registered test found nothing. Contact helps "
            "on average, but randomized tests are few. Norms moved in Rwanda, and a real conversation moved "
            "attitudes for months. And small biases compound on a ladder."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=42.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"allocation matrices, \ a diffusion model of the IAT, \ attenuation and a ladder of normal tails",
             STATUS_COLOR["replicated"]),
            (r"r\'esum\'es with random names, \ randomized radio and randomized conversations", STATUS_COLOR["replicated"]),
            (r"asking fails where answers are unacceptable; \ the list experiment and the audit route around "
             r"it", STATUS_COLOR["replicated, smaller"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "allocation matrices, a diffusion model of the IAT, attenuation, and a ladder of normal tails. "
            "<bookmark mark='b'/> The second, that the mind can't be experimented on, met résumés with random "
            "names, a randomized radio drama, and randomized conversations at the door. <bookmark mark='c'/> And "
            "the third, about introspection. Asking fails where some answers are unacceptable, and the list "
            "experiment and the audit study are ways around it. A lighter green."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"cooperation, \ trust and punishment", [37]),
            (r"culture, \ and which findings travel", [38]),
            (r"structured selection and fair hiring", [53]),
            (r"field experiments and nudges", [55]),
            (r"bias in machines", [60]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Cooperation, trust and punishment are next, in Part 37. "
            "Culture, and which findings travel, is Part 38. Structured selection and fair hiring are Part 53, "
            "field experiments and nudges Part 55, and bias in machines Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=8.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One reads Tajfel's "
            "matrix. One models the illusory correlation. One derives the list experiment's estimator and its "
            "variance. One proves the attenuation bound. One sizes an audit study. One writes down the ladder. And "
            "the last, with the star, asks you to design a field test of a diversity training. Pause here if you'd "
            "like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"G. W. Allport, \emph{The Nature of Prejudice} (1954)",
             r"G. Perry, \emph{The Lost Boys} (2018)",
             r"M. R. Banaji \& A. G. Greenwald, \emph{Blindspot} (2013)"],
            [r"H. Tajfel, \ M. G. Billig, \ R. P. Bundy \& C. Flament (1971); \ H. Tajfel \& J. C. Turner (1979)",
             r"D. Balliet, \ J. Wu \& C. K. W. De Dreu (2014); \ M. Sherif et al.\ (1961)",
             r"D. L. Hamilton \& R. K. Gifford (1976); \ S. T. Fiske, \ A. J. C. Cuddy, \ P. Glick \& J. Xu (2002)",
             r"A. G. Greenwald, \ D. E. McGhee \& J. L. K. Schwartz (1998); \ F. L. Oswald et al.\ (2013); \ "
             r"P. S. Forscher et al.\ (2019)",
             r"M. Bertrand \& S. Mullainathan (2004); \ L. Quillian et al.\ (2017)",
             r"C. M. Steele \& J. Aronson (1995); \ P. R. Sackett et al.\ (2004); \ P. C. Flore et al.\ (2018)",
             r"T. F. Pettigrew \& L. R. Tropp (2006); \ E. L. Paluck et al.\ (2019, \ 2021); \ E. L. Paluck (2009)",
             r"D. Broockman \& J. Kalla (2016); \ E. H. Chang et al.\ (2019); \ B. K. Payne et al.\ (2017)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Allport's book is where the "
            "modern study of prejudice began; Perry's The Lost Boys is Robbers Cave from the archives; and "
            "Blindspot is the case for implicit bias, by two of the IAT's creators, to read alongside its critics."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act IX: \ other people", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 37", font_size=32, color=GREY_B), label(r"Bonds and Bargains", font_size=40),
                     wrapped_label(r"Why do people cooperate with strangers?", 6.0, 28, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Act Nine goes on. <bookmark mark='a'/> This part asked how groups divide people. "
            "<bookmark mark='b'/> The next asks how people cooperate anyway: with strangers, in games with real "
            "money, and in the bonds that hold them together. Part 37: bonds and bargains."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
