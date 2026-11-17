from __future__ import annotations

from videos.psychology.psych62.common import *  # noqa: F403

PROBLEMS = [
    r"Halves correlate 0.58. \ The Spearman-Brown reliability of the full test?",
    r"A reliability of 0.74 from 40 people. \ Roughly how many people to make the 95\% interval half as wide?",
    r"The registered minimum excluded everyone. \ List two things a Stage 1 reviewer could have asked to catch it.",
    r"Of 322 Ledger rows, \ 203 held. \ Why is that number not ``the replication rate of psychology''?",
    r"Psyche's search slopes: \ 10 ms per item present, \ 35 absent. \ What would a serial self-terminating search "
    r"predict?",
    r"Write Kant's fourth objection in one sentence, \ and the evidence that it is being answered.",
    r"$\star$ \ Choose an open problem from any part's Frontier and write its Stage 1 registered report.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.your_numbers()
        self.recap()
        self.problems()
        self.references()
        self.end()

    def your_numbers(self):
        s = load("stage2")
        b = load("board")
        sc = load("scorecard")
        c = b["counts"]
        held = c["replicated"] + c["replicated, smaller"] + c["story and record"]
        npass = sum(1 for ok in sc["pass"] if ok == "yes")
        nrun = sum(1 for ok in sc["pass"] if ok != "n/a")
        head = heading(r"Your last four numbers, \ checked")
        rows = VGroup()
        for n_, q, ans, col in (
                (r"1", r"a person's rotation slope: \ reliable?", rf"{s['slope_rel']:.2f} ({s['slope_ci'][0]:.2f} "
                                                                rf"to {s['slope_ci'][1]:.2f}): \ inconclusive", PERSON),
                (r"2", r"the share of Ledger rows that held", rf"{held} of {b['total']}, \ "
                                                              rf"{100 * held / b['total']:.0f}\%", MODEL),
                (r"3", r"Battery tasks matched by one Psyche", rf"{npass} of {nrun}", AUTH),
                (r"4", r"Kant's objections that survive", r"none as stated; \ the third was right, \ and answered",
                 KANT)):
            rows.add(VGroup(label(n_, font_size=30, color=col), wrapped_label(q, 5.6, 22, WHITE),
                            wrapped_label(ans, 5.4, 22, col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        with self.voiceover(
            f"First, your last four numbers. <bookmark mark='a'/> A person's rotation slope had a reliability of "
            f"zero point seven four, with an interval from zero point five one to zero point eight seven: "
            f"inconclusive. {held} of the Ledger's {b['total']} rows held, about "
            f"{round(100 * held / b['total'])} percent. One Psyche matched {npass} of the {nrun} Battery tasks it can "
            f"sit. And none of Kant's objections survives as he stated it. The third was right, and answered."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=12.0)
        self.clear_scene()

    def recap(self):
        items = [
            (r"a question from a collision of two results", WHITE),
            (r"ethics is a practice, \ checked by others", CARE),
            (r"the plan as code, \ hashed before analysis", MODEL),
            (r"a design check says what the design can decide", MODEL),
            (r"reviews before results", PERSON),
            (r"a deviation, \ reported with the original rule", AUTH),
            (r"inconclusive, \ and leaning against the paradox", PERSON),
            (r"exploratory analyses, \ labelled", MODEL),
            (r"one Psyche: \ five of seven tasks", AUTH),
            (r"the Ledger: \ about three in five held", GOOD),
            (r"Kant answered, \ and a fourth objection named", KANT),
            (r"the next row is yours", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 62, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part sixty-two in twelve lines. <bookmark mark='a'/> A question came from a collision of two results. "
            "Ethics is a practice, checked by others. The plan was written as code, and hashed before the analysis. "
            "A design check says what the design can decide. Reviews come before results. A deviation was reported "
            "with the original rule beside it. The answer was inconclusive, leaning against the paradox. Exploratory "
            "analyses were labelled. One Psyche did five of seven tasks. In the Ledger, about three rows in five "
            "held. Kant was answered, and a fourth objection named. And the next row is yours."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=34.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "The last seven problems, with full solutions in this part's README. <bookmark mark='a'/> One corrects a "
            "split half. One sizes a replication. One asks what a reviewer could have caught. One asks why the "
            "Ledger's share isn't a replication rate. One tests Psyche's search. One states Kant's fourth objection. "
            "And the last, with the star, asks you to write your own Stage 1 report. Pause here if you'd like to "
            "try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"C. D. Chambers, \ \emph{The Seven Deadly Sins of Psychology}",
             r"The Belmont Report (1979)",
             r"I. Kant, \ \emph{Metaphysical Foundations of Natural Science} (1786)"],
            [r"C. D. Chambers \& L. Tzavella, \ The past, \ present and future of Registered Reports (2022)",
             r"G. Ganis \& R. Kievit (2015); \ C. Hedge et al.\ (2018); \ J. N. Rouder \& J. M. Haaf (2019)",
             r"D. H. Hoffman et al., \ the independent review for the American Psychological Association (2015)",
             r"A. M. Scheel et al.\ (2021); \ C. K. Soderberg et al.\ (2021)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Chambers's book is the best "
            "account of what went wrong and of registered reports; the Belmont Report is short and still the "
            "foundation of research ethics; and Kant's preface is where this series began."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def end(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Sixty-two parts, \ complete", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        last = VGroup(label(r"Psychology, \ Built", font_size=40),
                      wrapped_label(r"from Kant's ``never'' to a Ledger with dates", 6.0, 24, GREY_A),
                      wrapped_label(r"the open problems are on the course site, \ with every lab, \ every "
                                    r"experiment, \ and the code", 6.0, 20, GREY_B))
        last.arrange(DOWN, buff=0.35).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "That's the end of the series. <bookmark mark='a'/> It began with Kant's never: no mathematics, no "
            "experiment, no observation that doesn't disturb. Sixty-two parts later there are equations that predict "
            "measurements, experiments run every day, a field that measures its own disturbances, and a Ledger of "
            "what held, with a date on every row. <bookmark mark='b'/> The open problems are on the course site, "
            "with every lab, every experiment, and the code. The next row is yours. Thank you for watching."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("a")
            self.play(FadeIn(last[0], shift=UP * 0.2), FadeIn(last[1]))
            vo.wait_until("b")
            self.play(FadeIn(last[2]))
        self.wait(3.0)
        self.clear_scene()
