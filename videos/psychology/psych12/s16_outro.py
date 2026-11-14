from __future__ import annotations

from videos.psychology.psych12.common import *  # noqa: F403

PROBLEMS = [
    r"One observer has a hit rate of 0.84 and a false-alarm rate of 0.16; \ another, \ 0.69 and 0.07. \ Find $d'$ and $c$ "
    r"for each. \ Do they see differently, \ or decide differently?",
    r"For the equal-variance model, \ show that the likelihood ratio is $\exp(d'x - d'^2/2)$, \ and that the ideal "
    r"criterion is $x^* = d'/2 + \ln\beta/d'$. \ Find it for $d' = 2$, \ signals on a quarter of trials, \ all outcomes "
    r"worth the same.",
    r"Show that the area under an equal-variance ROC is $\Phi(d'/\sqrt2)$, \ and under an unequal-variance one "
    r"$\Phi\!\left(d'/\sqrt{1 + \sigma_s^2}\right)$.",
    r"With the mammogram's hit and false-alarm rates (0.8 and 0.096), \ at what prevalence is a positive test right "
    r"half the time?",
    r"A high-threshold observer detects with $p = 0.5$ and otherwise guesses yes at rate $g$. \ Compute $d'$ from its "
    r"rates for $g = 0.1$ and $g = 0.4$. \ What does the difference say about using $d'$ when that model is true?",
    r"With \texttt{explainer.psychology.psyche.sdt}: \ simulate rating studies from an observer with $\sigma_s = 1.25$ "
    r"at 50 and at 500 trials of each kind, \ and find how often \texttt{fit\_rating} rejects equal variances.",
    r"$\star$ \ Chapter 11's two watchers have the same hit rates. \ Design a single session that tells them apart, \ "
    r"and say what each predicts.",
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
        p, i, b, pv = (load(k) for k in ("payoffs", "ideal", "baserates", "prevalence"))
        items = [
            (r"radar observers missed contacts: \ but did they see less, \ or say less?", WHITE),
            (r"four outcomes; \ two numbers carry them: \ hits and false alarms", HIT),
            (r"two distributions and a line: \ $d' = z(H) - z(F)$, \ $c = -\tfrac12\,(z(H) + z(F))$", MODEL),
            (r"the ROC traces every criterion; \ its area is the two-choice score", ROCC),
            (r"the ideal line: \ likelihood ratio against base rate and payoffs; \ accuracy rewards silence", CRIT),
            (r"zROC slopes test equal spreads; \ recognition's is about 0.8", SIGNALC),
            (r"forced choice: \ $\Phi(d'/\sqrt2)$, \ no criterion", HIT),
            (r"curved ROCs retired the gate-like threshold; \ mixtures remain rivals", RIVAL),
            (rf"base rates: \ a positive mammogram is cancer {pct(b['nf_ppv'])} of the time; \ rare targets are missed",
             FA),
            (r"the watch: \ false alarms tell caution from fatigue", THRESH),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=31, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 12, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        del p, i, pv
        with self.voiceover(
            "Part twelve in ten lines. <bookmark mark='a'/> Radar observers missed contacts, and the question was "
            "whether they saw less or said less. Every detection has four outcomes, and two numbers carry them: hits "
            "and false alarms. Two distributions and a line turn those into d prime, for seeing, and c, for saying. "
            "The ROC traces every possible line, and its area is the score in a two-choice task. The ideal line "
            "weighs the likelihood ratio against base rates and payoffs, and when signals are rare, accuracy rewards "
            "silence. The slope of a z ROC tests whether the two spreads are equal, and in recognition memory it's "
            "about point eight. Forced choice gives d prime over root two, with no criterion at all. Curved ROCs "
            "retired the old gate-like threshold, though mixtures remain as rivals. Base rates decide what a yes "
            "means: a positive mammogram is cancer about eight percent of the time, and rare targets are missed. "
            "And on the long watch, the false alarms tell caution from fatigue."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=44.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"a law of the mind with a constant in it; \ thresholds fitted with intervals. \ Whether a sensation has a "
             r"size: \ still argued", STATUS_COLOR["replicated, smaller"]),
            (r"experiments by the dozen: \ assignment by lot, \ lesions, \ twins, \ a cave", STATUS_COLOR["replicated"]),
            (r"the report mixes seeing with saying, \ and detection theory measures the two apart", STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> Today was the third objection's day: that observing the mind disturbs "
            "it, so every report is coloured by the reporting. Detection theory concedes the first half. A yes does "
            "mix seeing with saying. <bookmark mark='b'/> But it denies the conclusion. The mixture has a structure, "
            "two numbers can be read off it, and the second one, the criterion, turns out to be something worth "
            "measuring in its own right. That's a strong reply. Not every report can be taken apart this way, and "
            "the hardest, reports of experience itself, wait for Part 27."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows], FadeIn(board.rows[0].reply),
                      FadeIn(board.rows[1].reply))
            vo.wait_until("a")
            self.play(Indicate(board.rows[2].objection, color=KANT))
            vo.wait_until("b")
            self.play(FadeIn(board.rows[2].reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"single photons and the eye's own noise", [13]),
            (r"recognition, \ line-ups and false memories", [21]),
            (r"confidence and evidence over time", [25]),
            (r"base rates and judgment", [26]),
            (r"seeing without knowing: \ awareness measured with $d'$", [27]),
            (r"alarms, \ watches and rare targets", [51]),
            (r"hiring as a detection problem", [53]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> The eye's response to single photons, and its own noise, are "
            "Part 13. Recognition memory, line-ups and false memories are Part 21. Confidence and evidence building "
            "up over time are Part 25. Base rates and judgment are Part 26. Whether you can see without knowing it, "
            "measured with d prime, is Part 27. Alarms, long watches and rare targets are Part 51. And hiring as a "
            "detection problem is Part 53."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=13.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One asks whether two "
            "observers see or decide differently. One derives the ideal criterion. One proves what the area under "
            "the ROC is. One finds where a positive test becomes a coin flip. One shows what d prime does when the "
            "threshold model is true. One uses Psyche's detection module to test for unequal variances. And the "
            "last, with the star, is the frontier's problem. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"D. M. Green \& J. A. Swets, \emph{Signal Detection Theory and Psychophysics} (1966)",
             r"N. A. Macmillan \& C. D. Creelman, \emph{Detection Theory: A User's Guide} (2nd ed., 2005)",
             r"T. D. Wickens, \emph{Elementary Signal Detection Theory} (2002)"],
            [r"N. H. Mackworth (1948); \ W. W. Peterson, T. G. Birdsall \& W. C. Fox (1954)",
             r"W. P. Tanner \& J. A. Swets (1954); \ J. A. Swets, W. P. Tanner \& T. G. Birdsall (1961)",
             r"R. Ratcliff, C.-F. Sheu \& S. D. Gronlund (1992); \ A. P. Yonelinas (1994)",
             r"G. Gigerenzer \& U. Hoffrage (1995); \ J. E. See et al.\ (1995)",
             r"J. A. Swets, R. M. Dawes \& J. Monahan (2000)",
             r"J. M. Wolfe, T. S. Horowitz \& N. M. Kenner (2005); \ M. S. Fleck \& S. R. Mitroff (2007)",
             r"B. Maniscalco \& H. Lau (2012); \ L. Mickes, H. D. Flowe \& J. T. Wixted (2012)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Macmillan and Creelman's user's "
            "guide is the place to start for doing it yourself."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act III: \ the senses", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 13", font_size=32, color=GREY_B), label(r"The Eye and the Code", font_size=50),
                     wrapped_label(r"How few quanta of light can a person see? \ Fewer than you would think, \ and the eye "
                                   r"sends the brain differences, \ not pictures.", 6.0, 28, GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "So a report can be taken apart into seeing and saying, and the seeing has a number. "
            "<bookmark mark='a'/> Which raises the next question: what is the seeing made of? <bookmark mark='b'/> In "
            "1942 three researchers sat in a dark room and asked how few quanta of light a person can see. The answer "
            "was a handful, close to the limit physics allows. And it turned out that the eye doesn't send the brain "
            "pictures. It sends differences, across space, time and colour, and each step can be written down as a "
            "filter. It's Part 13: the eye and the code."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
