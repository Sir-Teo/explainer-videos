from __future__ import annotations

from videos.psychology.psych15.common import *  # noqa: F403

PROBLEMS = [
    r"Show that 20 dB is ten times the pressure and 10 dB ten times the intensity. \ Two equal, \ unrelated sources "
    r"of 60 dB play together: \ what is the level?",
    r"Using $\mathrm{ERB}(f) = 24.7\,(4.37 f/1000 + 1)$, \ find the auditory filter's width at 500 Hz and 4 kHz, "
    r"\ and the number of ERBs between 100 Hz and 8 kHz.",
    r"With Woodworth's $\mathrm{ITD} = (r/c)(\theta + \sin\theta)$, \ $r$ = 8.75 cm, \ $c$ = 343 m/s, \ find the "
    r"delay at 90$^\circ$, \ and the direction a 10 $\mu$s difference corresponds to.",
    r"Show that a sum of harmonics $n f_0$ repeats with period $1/f_0$ whichever harmonics are present, \ and so that "
    r"its autocorrelation peaks at a lag of $1/f_0$.",
    r"Derive the label model of ABX discrimination: \ if listeners compare only covert labels, \ "
    r"$P(\text{correct}) = \tfrac12[1 + (p_A - p_B)^2]$.",
    r"With \texttt{explainer.psychology.psyche.hearing.gate}: \ for an injury signal of 1, \ find the touch input "
    r"that halves T, \ and how it changes if $g$ is doubled.",
    r"$\star$ \ The McGurk effect could change what people hear, \ or only what they report. \ Design a test, \ using "
    r"Part 12's detection theory, \ that tells the two apart.",
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
        items = [
            (r"a pitch you hear that is not in the sound: \ the missing fundamental", YOU),
            (r"sound in physics' units; \ the decibel is Fechner's law in engineering", SOUND),
            (r"the cochlea: \ a travelling wave, \ a place map, \ an amplifier, \ a bank of filters", PLACE),
            (r"masking and critical bands; \ pitch from the timing of spikes, \ by autocorrelation", TIMING),
            (r"where: \ microsecond delays, \ Jeffress's circuit, \ and what mammals do instead", WHITE),
            (r"scenes are grouped by sound's own Gestalt rules", PRIOR),
            (r"speech: \ no invariant, \ categories that do not erase, \ a voice changed by a face", TIMING),
            (r"music: \ roughness is shared; \ the taste for consonance is learned", SOUND),
            (r"touch, \ position and pain: \ four channels, \ a rubber hand, \ a gate", TOUCH),
            (r"smell is a code of hundreds of dimensions; \ the tongue map and the trillion, \ corrected", SMELL),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=30, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 15, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part fifteen in ten lines. <bookmark mark='a'/> You heard a pitch that wasn't in the sound. Sound is "
            "pressure, and the decibel is Fechner's law turned into engineering. The cochlea carries a travelling "
            "wave, maps frequency onto place, amplifies itself, and acts as a bank of filters. Masking shows the "
            "filters' widths, and pitch comes from the timing of spikes, found by autocorrelation. Where a sound is "
            "comes from microsecond delays, read by Jeffress's circuit in owls and by something else in mammals. "
            "Scenes are grouped by sound's own Gestalt rules. Speech has no invariant sounds, its categories don't "
            "erase detail, and a face can change what a voice says. In music, roughness is shared and the taste for "
            "consonance is learned. Touch has four channels, the body can adopt a rubber hand, and pain passes "
            "through a gate. And smell is a code of hundreds of dimensions, where the tongue map and the trillion "
            "smells needed correcting."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=46.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"a threshold counted in quanta; \ colour a matrix; \ a missing note found by a computation",
             STATUS_COLOR["replicated"]),
            (r"experiments by the dozen: \ assignment by lot, \ lesions, \ twins, \ a cave",
             STATUS_COLOR["replicated"]),
            (r"cue weights read from choices, \ never from reports; \ and illusions that knowing does not undo",
             STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> Today the first objection, that mathematics can't apply to the inner "
            "sense, lost a little more ground: an autocorrelation predicts a note that isn't in the sound, and the "
            "decibel made Fechner's logarithm an industrial unit. <bookmark mark='b'/> But the rubber hand is a "
            "warning about the third objection. If people's reports follow what they expect an experiment to produce, "
            "then asking them changes what they tell us, and perhaps what they feel. The Ledger keeps that one open."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows], FadeIn(board.rows[1].reply),
                      FadeIn(board.rows[2].reply))
            vo.wait_until("a")
            self.play(Indicate(board.rows[0].objection, color=KANT), FadeIn(board.rows[0].reply, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(Indicate(board.rows[2].objection, color=KANT))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"learning from the senses: \ conditioning", [16]),
            (r"prediction errors", [17]),
            (r"attention, \ and the cocktail party", [18]),
            (r"speech and language", [23]),
            (r"hearing aids, \ alarms and the human in the loop", [51]),
            (r"pain and placebo in the clinic", [57]),
            (r"the predictive brain", [58]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Learning what the senses report, in conditioning, is Part 16, "
            "and prediction errors are Part 17. Attention, and the cocktail party, is Part 18. Speech and language are Part 23. "
            "Hearing aids, alarms and the human in the loop are Part 51. Pain and placebo in the clinic are Part 57. "
            "And the predictive brain is Part 58."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=12.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One works with decibels. "
            "One measures the ear's filters. One finds the largest time difference between the ears, and the "
            "smallest direction it can resolve. One proves why a missing fundamental can still be found. One derives "
            "the label model of categorical perception. One uses Psyche's gate. And the last, with the star, asks how "
            "to tell whether the McGurk effect changes hearing or only reporting. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"B. C. J. Moore, \emph{An Introduction to the Psychology of Hearing} (6th ed., 2012)",
             r"A. S. Bregman, \emph{Auditory Scene Analysis} (1990)",
             r"J. M. Wolfe et al., \emph{Sensation \& Perception}; \ G. von Békésy, \emph{Experiments in Hearing} (1960)"],
            [r"H. Fletcher (1940); \ D. T. Kemp (1978); \ D. D. Greenwood (1990); \ E. Terhardt (1979)",
             r"J. F. Schouten (1940); \ J. C. R. Licklider (1951); \ R. Meddis \& M. J. Hewitt (1991)",
             r"L. A. Jeffress (1948); \ A. Brand et al.\ (2002); \ L. P. A. S. van Noorden (1975)",
             r"A. M. Liberman et al.\ (1957); \ B. McMurray et al.\ (2002); \ H. McGurk \& J. MacDonald (1976)",
             r"D. B. Mallick et al.\ (2015); \ R. Plomp \& W. J. M. Levelt (1965); \ J. H. McDermott et al.\ (2016)",
             r"M. Botvinick \& J. Cohen (1998); \ P. Lush et al.\ (2020); \ R. Melzack \& P. D. Wall (1965)",
             r"J. D. Levine et al.\ (1978); \ L. Buck \& R. Axel (1991); \ C. Bushdid et al.\ (2014)",
             r"R. C. Gerkin \& J. B. Castro (2015); \ M. Meister (2015); \ S. G. Kujawa \& M. C. Liberman (2009)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Brian Moore's Introduction to the "
            "Psychology of Hearing is the place to start."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act III complete: \ the senses", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 16", font_size=32, color=GREY_B), label(r"Conditioning", font_size=50),
                     wrapped_label(r"A dog, \ a bell, \ and the discovery that learning is prediction.", 6.0, 28,
                                   GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "That completes Act Three: how the senses measure the world, and how the brain bets on what's out there. "
            "<bookmark mark='a'/> But every sense we've met can be changed by experience: the light-from-above prior "
            "retrained in an hour, a consonance learned from a culture, pain that is learned. <bookmark mark='b'/> Next "
            "time, Act Four begins with learning itself: a dog, a bell, and the discovery that what animals learn is "
            "not an association but a prediction. It's Part 16: conditioning."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
