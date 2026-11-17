from __future__ import annotations

from videos.psychology.psych10.common import *  # noqa: F403

PROBLEMS = [
    r"A clock left in the dark has a period of 24.18 hours. \ How many minutes a day does it drift, and which way? \ After "
    r"how many days is it twelve hours out? \ What must morning light do each day to hold it at 24 hours?",
    r"In the two-process model the pressure rises as $1 - (1 - S_0)\,e^{-t/18.18}$ and falls as $S_0\,e^{-t/4.2}$ ($t$ in "
    r"hours). \ From $S = 0.17$ on waking, find $S$ after 16 hours and after 40 hours awake. \ From each, how long must "
    r"sleep last to return to 0.17? \ Why is recovery sleep not proportional to the time awake?",
    r"Lapses grow each day by 0.15 for every hour awake beyond 15.84. \ Compare fourteen days on 6 hours in bed with "
    r"fourteen days on 7. \ How much sleep keeps the count level?",
    r"A drug has $K = 2$ mg/L. \ What concentration occupies 80\% of its receptors? \ With a blocker present at four "
    r"times its own $K_B$, what concentration gives the same 80\%? \ With three sites that must all be filled, "
    r"$p = D^3 / (D^3 + K^3)$: \ what is the ratio of the doses that give 90\% and 10\%?",
    r"Caffeine's half-life is 5 hours. \ You take 100 mg at 8:00 and 100 mg at 14:00 (absorbed at once). \ How much is "
    r"left at 23:00? \ When would a single 200 mg dose have to be taken to leave the same? \ Alcohol leaves at a constant "
    r"rate $r$: \ what doubles when the dose doubles?",
    r"With \texttt{explainer.psychology.psyche.body}: use \texttt{entrain} to find the day lengths the clock locks to at "
    r"300 lux and at 3{,}000 lux. \ Then use \texttt{two\_process} with \texttt{keep\_awake} to plot recovery sleep "
    r"against hours awake.",
    r"$\star$ \ Short sleepers die sooner, and so do long sleepers. \ Design the study that could tell sleep as a cause "
    r"from sleep as a symptom, \ and say what result would count against a causal effect.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.score()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def recap(self):
        c, s, st, d, tol = (load(k) for k in ("clock", "sleep", "stress", "dose", "tolerance"))
        a = archive.ASERINSKY_1953.data
        r = archive.RASCH_2007.data
        items = [
            (r"a month in a cave: \ one man's rhythm followed a 28-hour day, \ the other's kept to 24", CLOCKC),
            (rf"the clock: \ ${c['published_period']:.2f}$ hours in people, \ ${c['free_period']:.2f}$ in the model; \ it "
             r"locks to days of 23 to 25 hours, \ not 28", CLOCKC),
            (r"light sets it: \ later before the low point, \ earlier after; \ a flight leaves it behind for days", LIGHTC),
            (rf"sleep has stages, in ninety-minute cycles; \ REM: \ {a['dreams_rem']} dreams in {a['awakenings_rem']} "
             r"awakenings", REMC),
            (rf"two processes, a pressure and a gate: \ ${s['usual']:.1f}$ hours of sleep, \ ${s['recovery']:.1f}$ after a "
             r"lost night", SLEEPC),
            (r"six hours a night for two weeks: \ as impaired as two nights awake, \ and unaware of it", BAD),
            (rf"a memory cued in deep sleep: \ $g = {r['g']:.2f}$; \ what dreams and sleep are for: \ open", SLEEPC),
            (rf"the stress loop switches itself off within ${st['gone_hours']:.1f}$ hours; \ a worn brake does not", HORM),
            (rf"a drug mimics, blocks, holds or amplifies; \ occupancy $D/(D+K)$; \ ${d['caf_at_23']:.2f}$ of a cup at "
             r"23:00", DRUG),
            (rf"the body answers back: \ the effect felt falls from ${tol['felt_first']:.2f}$ to ${tol['felt_last']:.2f}$; "
             r"\ in a new room, deaths double", OPP),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=32, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        head = label(r"Part 10, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part ten in ten lines. <bookmark mark='a'/> Two men spent a month in a cave. One man's "
            "rhythm followed a twenty-eight-hour day, and the other's kept to twenty-four. The body has "
            "a clock. It runs about ten minutes slow, and it locks to days near twenty-four hours and to "
            "no others. Light sets it: later if it falls before the low point, earlier if after, and a "
            "flight leaves it behind for days. Sleep has stages, in cycles of ninety minutes, and one of "
            "them comes with dreams. Two processes decide when you sleep: a pressure that builds, and a "
            "gate that the clock opens and closes. Six hours a night for two weeks impairs you as much "
            "as two nights awake, and you won't know it. A memory cued in deep sleep is strengthened, a "
            "little, and what dreams and sleep are for is open. The stress loop switches itself off, "
            "unless its brake is worn. A drug mimics, blocks, holds or amplifies, by one formula for "
            "occupancy. And the body answers back, which is tolerance while the drug is there, and "
            "withdrawal when it's gone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=46.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"an oscillator with a curve for what light does to it; \ two exponentials that predict a recovery night; "
             r"\ one formula for receptors and enzymes", STATUS_COLOR["replicated"]),
            (r"a cave, \ a day of 28 hours, \ sleep assigned by lot, \ an odour delivered to a sleeping brain",
             STATUS_COLOR["replicated"]),
            (r"sleep loss degrades the observer: \ the ratings level off while the lapses climb. \ A stopwatch is not "
             r"fooled", STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> Today spoke most directly to the third objection: that "
            "observing a mental state disturbs it. Chapter six showed something worse. Sleep loss "
            "degrades the observer. People's ratings of their own sleepiness levelled off, while their "
            "lapses kept climbing. The reply is the same as in Part 1: don't ask the instrument to "
            "inspect itself. Time it. <bookmark mark='b'/> On the second objection, that the mind can't "
            "be experimented on: a cave, a day of twenty-eight hours, sleep handed out by lot, and an "
            "odour delivered to a sleeping brain. <bookmark mark='c'/> And on the first, that the mind "
            "admits no mathematics: an oscillator, with a curve for what light does to it. Two "
            "exponentials that predict the night after a lost night. And one formula that covers a "
            "receptor and an enzyme."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            vo.wait_until("a")
            self.play(FadeIn(board.rows[2].reply, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(board.rows[1].reply, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(board.rows[0].reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the retina, \ and the cells that see without pictures", [13]),
            (r"conditioning: \ the room that switches on tolerance", [16]),
            (r"reward, dopamine, and what drugs take over", [17]),
            (r"what it is to consolidate a memory", [20]),
            (r"motivation, arousal and the opponent process", [28]),
            (r"adolescence, and the late clock", [31]),
            (r"depression, the stress loop, and addiction", [40, 41]),
            (r"do drugs and therapies work?", [42]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> The retina, and the cells that see without "
            "making pictures, are Part 13. Conditioning, and the room that switches on tolerance, is "
            "Part 16. Reward, dopamine and what drugs take over are Part 17. What it means to "
            "consolidate a memory is Part 20. Motivation, arousal and the opponent process are Part 28. "
            "Adolescence, and the late clock, are in Part 31. Depression, the stress loop and addiction "
            "are Parts 40 and 41. And whether drugs and therapies work is Part 42."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=13.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One does "
            "the clock's arithmetic. One works the two-process model by hand, and finds out why a lost "
            "night isn't repaid hour for hour. One compares two weeks on six hours with two weeks on "
            "seven. One fills receptors, with a blocker and without. One does the arithmetic of coffee "
            "and of alcohol. One uses Psyche's body module to find what the clock can follow. And the "
            "last, with the star, is the frontier's problem. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"N. Kleitman, \emph{Sleep and Wakefulness} (revised ed., 1963)",
             r"K. Miller, \emph{Mapping the Darkness} (2023)",
             r"T. Roenneberg, \emph{Internal Time} (2012)",
             r"J. S. Meyer \& L. F. Quenzer, \emph{Psychopharmacology: Drugs, the Brain, and Behavior} (2nd ed., 2013)"],
            [r"N. Kleitman (1939); \ C. A. Czeisler et al.\ (1999); \ E. Aserinsky \& N. Kleitman (1953)",
             r"A. A. Borb\'ely (1982); \ S. Daan, D. G. M. Beersma \& A. A. Borb\'ely (1984)",
             r"H. P. A. Van Dongen et al.\ (2003); \ G. Belenky et al.\ (2003); \ T. Roenneberg et al.\ (2004)",
             r"B. Rasch et al.\ (2007); \ X. Hu et al.\ (2020); \ J. A. Hobson \& R. W. McCarley (1977); \ M. Solms (2000)",
             r"F. P. Cappuccio et al.\ (2010); \ G. P. Dunster et al.\ (2018); \ J. M. Trauer et al.\ (2015)",
             r"C. H. Phoenix et al.\ (1959); \ K. H. Teigen (1994); \ R. L. Solomon \& J. D. Corbit (1974); \ S. Siegel et "
             r"al.\ (1982)",
             r"L. Xie et al.\ (2013); \ A. Miao et al.\ (2024)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Kleitman's own "
            "book is still worth opening, and Aserinsky's paper is two pages long."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act II is complete: \ the wet machine", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 11", font_size=32, color=GREY_B), label(r"The Threshold", font_size=50),
                     wrapped_label(r"Leipzig, the morning of 22 October 1850. \ A physicist lying in bed sees how a "
                                   r"sensation could be measured.", 6.0, 28, GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "That finishes the second act. Six parts on the wet machine: the neuron, the synapse and "
            "the circuit, the brain, the instruments that read it, the genes that vary it, and now the "
            "body that it lives in. <bookmark mark='a'/> From here the series goes back to where "
            "psychology began: to the mind itself, starting at its edge, with the senses. And it begins "
            "with Kant's first objection, that nothing in the mind can be measured. "
            "<bookmark mark='b'/> On the morning of the twenty-second of October, 1850, a physicist in "
            "Leipzig called Gustav Fechner was lying in bed, when he saw how it could be done. You "
            "can't put a ruler to a sensation. But you can count the smallest differences a person is "
            "able to notice, and build a scale from those. What he built, and how well it has lasted, "
            "is Part 11: the threshold."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
