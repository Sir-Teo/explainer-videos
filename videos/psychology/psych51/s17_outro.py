from __future__ import annotations

from videos.psychology.psych51.common import *  # noqa: F403

PROBLEMS = [
    r"Fitts's law with $a$ = 0.1 s and $b$ = 0.15 s per bit: \ predict the time to reach a 2 cm target 16 cm away "
    r"($ID = \log_2(2D/W)$).",
    r"A watch: \ 40 signals, \ 28 hits; \ 2,000 non-signals, \ 30 false alarms. \ Find $d'$ and $c$.",
    r"Targets in 1 bag in 200; \ hit rate 0.9, \ false-alarm rate 0.05. \ What share of alarms are real?",
    r"Four independent layers, \ each failing one time in 20: \ the chance of an accident?",
    r"NASA-TLX ratings 70, \ 40, \ 60, \ 50, \ 30, \ 80 with weights 5, \ 1, \ 3, \ 2, \ 0, \ 4: \ the weighted "
    r"score?",
    r"A level-3 car hands over with a 7 s budget; \ takeover times are lognormal with median 5 s and log-SD 0.45. \ "
    r"What share finish in time?",
    r"$\star$ \ Write the human-factors section of a safety case for a medication pump's dose entry: \ tasks, \ "
    r"likely slips, \ lapses and mistakes, \ the tests, \ and the residual risk.",
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
        v, p, t = load("vigilance"), load("prevalence"), load("takeover")
        f = load("fatigue")
        h17 = int(np.asarray(f["hours"])[np.argmin(np.abs(np.asarray(f["bac"]) - 0.05))])
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for k, q, ans, col in (
                (r"1", r"detected in the last half hour of a two-hour watch", rf"{100 * v['hit'][-1]:.0f}\%", PERSON),
                (r"2", r"misses at 1 in 2, \ and at 1 in 100", rf"{100 * p['miss_partial'][0]:.0f}\% $\to$ "
                                                              rf"{100 * p['miss_partial'][-1]:.0f}\%", AUTH),
                (r"3", r"takeovers within 7 s, \ failures 1 in 10 against 1 in 10,000",
                 rf"{100 * t['within'][0]:.0f}\% $\to$ {100 * t['within'][-1]:.0f}\%", MODEL),
                (r"4", r"hours awake like 0.05\% alcohol", rf"about {h17}", GOOD)):
            rows.add(VGroup(label(k, font_size=30, color=col), wrapped_label(q, 6.4, 22, WHITE),
                            label(ans, font_size=26, color=col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"each is a human limit a designer can plan for: \ none is a reason to blame the person "
                             r"who meets it", 12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> In the last half hour of a two-hour watch, Psyche's "
            "watchers caught about half the signals. When targets fell from one bag in two to one in a hundred, misses "
            "went from sixteen percent to forty-two. With automation failing once in ten thousand demands instead of "
            "once in ten, takeovers within seven seconds fell from ninety-five percent to sixty-two. And about "
            "seventeen hours awake impair performance like a blood alcohol of zero point zero five. "
            "<bookmark mark='b'/> Each is a human limit a designer can plan for. None is a reason to blame the person "
            "who meets it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=9.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"error is designed in: \ shape, \ position and compatibility", WHITE),
            (r"Fitts's and Hick's laws predict movement and choice time", SYMP),
            (r"slips, \ lapses, \ mistakes and violations need different fixes", SYMP),
            (r"show the state, \ not the command", MODEL),
            (r"workload is several resources, \ measured several ways", MODEL),
            (r"vigilance falls within the first half hour", PERSON),
            (r"rare targets raise the criterion", PERSON),
            (r"awareness fails most often at perception", PERSON),
            (r"reliable automation leaves an unready human", AUTH),
            (r"an alarm is a criterion; \ trust is a second one", AUTH),
            (r"defences fail together through shared causes", GOOD),
            (r"fatigue is a measured, \ manageable risk", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 51, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part fifty-one in twelve lines. <bookmark mark='a'/> Error is designed in, through shape, position and "
            "compatibility. Fitts's and Hick's laws predict movement and choice time. Slips, lapses, mistakes and "
            "violations need different fixes. Show the state, not the command. Workload is several resources, measured "
            "several ways. Vigilance falls within the first half hour. Rare targets raise the criterion. Awareness "
            "fails most often at perception. Reliable automation leaves an unready human. An alarm is a criterion, and "
            "trust is a second one. Defences fail together through shared causes. And fatigue is a measured, "
            "manageable risk."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=34.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"Fitts, \ Hick and the keystroke-level model", [52]),
            (r"selection and training at work", [53]),
            (r"line-ups as a detection task", [56]),
            (r"humans supervising learning machines", [60]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Fitts's and Hick's laws become an engineering model of the "
            "interface in Part 52. Selection and training at work are Part 53. Part 56 treats an eyewitness line-up as "
            "a detection task. And humans supervising learning machines return in Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One applies Fitts's law. "
            "One finds a watcher's d prime and criterion. One asks what share of alarms are real. One stacks four "
            "layers of cheese. One scores the task load index. One finds the share of takeovers that finish in time. "
            "And the last, with the star, asks you to write the human-factors section of a safety case for a "
            "medication pump. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"C. D. Wickens et al., \ \emph{Engineering Psychology and Human Performance}",
             r"J. Reason, \ \emph{Human Error} (1990)",
             r"S. Dekker, \ \emph{The Field Guide to Understanding Human Error}"],
            [r"P. M. Fitts \& R. E. Jones (1947); \ A. Chapanis, \ W. R. Garner \& C. T. Morgan (1949); \ P. M. Fitts (1954)",
             r"N. H. Mackworth (1948); \ J. E. See et al.\ (1995); \ J. M. Wolfe et al.\ (2005)",
             r"L. Bainbridge (1983); \ R. Parasuraman, \ T. B. Sheridan \& C. D. Wickens (2000)",
             r"M. R. Endsley (1995); \ J. D. Lee \& K. A. See (2004)",
             r"A. B. Haynes et al.\ (2009); \ D. R. Urbach et al.\ (2014)",
             r"D. Dawson \& K. Reid (1997)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Wickens and colleagues' textbook "
            "is the field's reference; Reason's Human Error gives it its vocabulary; and Dekker's field guide is the "
            "best short argument for asking why an action made sense at the time."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act XII: \ psychology at work, \ begun", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 52", font_size=32, color=GREY_B),
                     label(r"Designing for Minds", font_size=36),
                     wrapped_label(r"predicting a design's time before it is built", 6.0, 26, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Act Twelve has begun. <bookmark mark='a'/> This part put a person into a system and asked where the "
            "system should bend. <bookmark mark='b'/> The next one asks whether psychology is quantitative enough to "
            "engineer with. In the late nineteen eighties a telephone company was about to buy workstations that would "
            "save seconds a call. A model of the operator, built on paper, said they'd be slower. Part 52: designing "
            "for minds."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
