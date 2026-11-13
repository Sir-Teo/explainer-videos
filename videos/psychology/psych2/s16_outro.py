from __future__ import annotations

from videos.psychology.psych2.common import *  # noqa: F403

PROBLEMS = [
    r"Pfungst ran 42 tests in which the questioner knew the number on the card and 49 in which he did not; Hans "
    r"was right in 98\% and 8\%. \ How many answers is that in each? \ If Hans stopped at a number from 1 to 12 "
    r"chosen blindly, what share would he get right?",
    r"A supplement is tested on 60 volunteers: their memory score rises 4 points over eight weeks. \ Name four "
    r"threats to the conclusion that the supplement works, and the change of design that removes each.",
    r"$n$ people are dealt at random into two equal groups. \ A trait has standard deviation $\sigma$. \ Show that "
    r"the difference between the group means has standard deviation $2\sigma/\sqrt{n}$, and find $n$ for which "
    r"it is $\sigma/20$.",
    r"An effect of 8 ms; people differ with SD 24 ms; a person's two sessions correlate 0.89. \ For 80\% power at "
    r"the 5\% level ($z_{0.975} + z_{0.80} = 2.80$), how many people does a two-group design need, and a "
    r"within-person one? \ Why does a simulation ask for a few more than the second number?",
    r"Cell means: quick people 200 ms without the game and 180 with it; slow people 240 and 216. \ Compute the "
    r"interaction contrast in milliseconds and in log milliseconds. \ What would you report?",
    r"With \texttt{explainer.psychology.lab}: run the \texttt{regression} design with screening tests of 5, 20 "
    r"and 80 trials (\texttt{Lab(pool, n\_trials=...)}). \ How does the spurious effect change, and why?",
    r"$\star$ \ A trial's participants can tell which arm they are in. \ Design a study, acceptable to an ethics "
    r"board, that separates the treatment's effect from the effect of knowing.",
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
        w, h = load("within"), load("hans")
        num = h["numerals"]
        items = [
            (r"Berlin, 1904: \ thirteen experts look for the trick, and find none", KANT),
            (rf"Pfungst: \ {100 * num['with_knowledge']['correct']:.0f}\% right when the questioner knows, "
             rf"\ {100 * num['without_knowledge']['correct']:.0f}\% when he does not", HORSE),
            (r"the cue is a movement of a millimetre; \ the remedy is a blind", BLIND),
            (r"compared with what? \ the control group", CTRL),
            (r"six unsound designs, six effects, \ and the truth was zero", BIAS),
            (r"Peirce and Jastrow, 1884: \ the shuffle balances what nobody measured", P.ARCHIVE),
            (rf"each person as their own control: \ about {w['n_within_sim']} people do the work of "
             rf"{w['n_between_total']}, \ if the order is balanced", P.ACCENT),
            (r"expectations leak both ways: \ rats, classrooms, dogs, and the willing subject", "#F2A65A"),
            (r"interactions depend on the scale; \ four kinds of validity; \ who was studied", "#B48EF0"),
            (r"the subject is a person: \ respect, benefit, justice", "#7BD88F"),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=32, color=c) for i, (t, c) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        head = label(r"Part 2, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part two in ten lines. <bookmark mark='a'/> Thirteen experts looked for the trick in a horse that "
            "did arithmetic, and found none. One student varied who knew the answer, and the ability vanished. "
            "The horse had been reading a movement of a millimetre, and the remedy was a questioner who "
            "doesn't know. An experiment is a comparison, and the control group says what would have happened "
            "anyway. Six tempting designs each found an effect where the truth was zero. Peirce and Jastrow "
            "let a shuffled deck decide, and the shuffle balances even what nobody measured. Using each person "
            "as their own control buys a great deal of precision, provided the order is balanced. Expectations "
            "leak, from experimenter to subject and back. Interactions can depend on the scale, a study can be "
            "wrong in four separate ways, and it matters who was in the room. And the subject is a person."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.75), run_time=40.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"a division, a subtraction, a logarithm, a forgetting curve", STATUS_COLOR["replicated"]),
            (r"tasks can be taken apart; \ and now minds can be compared fairly: \ a control, a shuffle, a "
             r"balanced order", STATUS_COLOR["replicated"]),
            (r"the observer can be designed out, with a blind, \ where a blind can be kept", P.ACCENT),
        ))
        with self.voiceover(
            "So how does Kant's wager stand now? <bookmark mark='a'/> His first objection was lost in Part 1. "
            "<bookmark mark='b'/> His second, that there can be no experiment on the mind, is lost today. You "
            "can't take a mind apart like a compound. But you can deal minds into groups by shuffle, treat the "
            "groups differently, and compare. That is an experiment in the full sense. <bookmark mark='c'/> And "
            "the third, the observer who disturbs, has its first real reply. The disturbance can be designed "
            "out: by a questioner who doesn't know, a subject who doesn't know, an order nobody chose. Where "
            "that's possible. Kant keeps a piece of this one, and the frontier chapter showed you which piece. "
            "And there's an observer we haven't dealt with at all: the one who analyses the data, and wants a "
            "result. That is Part 4."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r.objection) for r in board.rows])
            for mark, r in zip("abc", board.rows):
                vo.wait_until(mark)
                self.play(FadeIn(r.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"what a test measures; \ construct validity", [3]),
            (r"the randomization test; \ the analyst as observer", [4]),
            (r"the psychometric function of a horse", [11]),
            (r"false alarms and where the criterion sits", [12]),
            (r"obedience, and its record", [34]),
            (r"which findings travel", [38]),
            (r"placebos and the trials of therapy", [42]),
            (r"one study, many laboratories", [43]),
        ], font_size=30)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> What a measurement measures is the next part, and the "
            "analyst as the last observer is the one after. The curve that described Hans's eyesight is "
            "Part 11, and the dogs' false alarms are Part 12. Milgram's study and its record are in Part 34, "
            "the question of which findings travel in Part 38, placebos and the trials of therapy in Part 42. "
            "And in Part 43 the series runs one experiment across many laboratories at once."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.4), run_time=9.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=25)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One checks "
            "Pfungst's arithmetic. One asks you to find the threats in a study and design them out. Two are "
            "short derivations: how well a shuffle balances, and how many people a design needs. One is an "
            "interaction that depends on its scale. One uses the laboratory's code. And the last, with the "
            "star, is the open problem from the frontier. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=6.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"O. Pfungst, \emph{Clever Hans} (1907; transl.\ 1911); \ R. Rosenthal, \emph{Experimenter Effects in "
             r"Behavioral Research} (1966)",
             r"D. T. Campbell \& J. C. Stanley, \emph{Experimental and Quasi-Experimental Designs for Research} "
             r"(1963)",
             r"W. R. Shadish, T. D. Cook \& D. T. Campbell, \emph{Experimental and Quasi-Experimental Designs for "
             r"Generalized Causal Inference} (2002)",
             r"R. A. Fisher, \emph{The Design of Experiments} (1935); \ \emph{The Belmont Report} (1979)"],
            [r"C. S. Peirce \& J. Jastrow (1884); \ S. Milgram (1963); \ M. T. Orne (1962); \ R. Rosenthal \& "
             r"K. L. Fode (1963)",
             r"R. Rosenthal \& L. Jacobson (1968); \ S. W. Raudenbush (1984); \ W. A. Wagenaar (1972); \ R. Falk \& "
             r"C. Konold (1997)",
             r"J. J. Arnett (2008); \ J. Henrich, S. J. Heine \& A. Norenzayan (2010); \ L. Lit, J. B. Schweitzer \& "
             r"A. M. Oberbauer (2011)",
             r"J. de Quidt, J. Haushofer \& C. Roth (2018); \ J. M. Mitchell et al.\ (2021)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Pfungst's own account of "
            "the horse is in the public domain, and it's still one of the best descriptions there is of how to "
            "investigate something."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=1, height=6.2).move_to([-3.9, 0.1, 0])
        tally = label(r"the laboratory is open; \ one faculty begun", font_size=26, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        nxt = VGroup(label(r"Part 3", font_size=32, color=GREY_B), label(r"The Measure", font_size=54),
                     wrapped_label(r"1940. \ A committee of physicists and psychologists reports, after eight "
                                   r"years, that it cannot agree whether a sensation can be measured at all.", 6.0,
                                   28, GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "That's the laboratory. <bookmark mark='a'/> We can now compare minds fairly. But every comparison "
            "today came down to a number, a reaction time in milliseconds, and we took the number on trust. "
            "<bookmark mark='b'/> In 1940 a committee of British physicists and psychologists, appointed to "
            "decide whether sensation can be measured, reported after eight years that it could not agree. Some "
            "of its members held that nothing in psychology had ever been measured, in the sense that a length "
            "is measured. What a number attached to a mind means, how much of it is error, and whether it "
            "measures what its name says: that's Part 3, the measure."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
