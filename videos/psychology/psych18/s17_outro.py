from __future__ import annotations

from videos.psychology.psych18.common import *  # noqa: F403

PROBLEMS = [
    r"Under Treisman's attenuator with noise s.d. 0.25, \ find the attenuation at which your name, \ threshold 0.55, \ "
    r"is heard on a third of trials.",
    r"A serial, \ self-terminating search checks items at 50 ms each. \ Derive the target-present and target-absent "
    r"slopes, \ and their ratio.",
    r"Show that a central bottleneck makes the second response time fall with slope $-1$ at short SOAs, \ and find "
    r"the SOA at which the slope becomes 0.",
    r"In a diffusion with bound $a$ and drift $v$, \ the mean decision time is $\frac{a}{v}\tanh(av)$. \ Show why "
    r"subtracting drift costs more time than adding it saves.",
    r"Write the normalization model with an attention field, \ and show that a uniform attention gain cancels at high "
    r"contrast.",
    r"With \texttt{explainer.psychology.psyche.attention}: \ vary the quitting threshold in guided search, \ and plot "
    r"misses against the absent slope.",
    r"$\star$ \ Design an experiment that tells a capacity limit from a strategic choice in the attentional blink.",
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
            (r"much reaches the senses, \ little reaches report: \ the gorilla, \ the flicker", ATT),
            (r"Broadbent's filter, \ the first information-flow diagram of a mind", CUE),
            (r"your name gets through: \ attenuation, \ late selection, \ and load", ATT),
            (r"a spotlight moves without the eyes, \ and avoids where it has been", CUE),
            (r"pop-out and conjunction search: \ features, \ binding, \ guidance, \ saliency", TARGET),
            (r"what we attend decides what else we see, \ for experts too", ATT),
            (r"limits in time: \ the blink and the central bottleneck", CONTROL),
            (r"conflict and control: \ Stroop, \ flankers, \ switching", CONFLICT),
            (r"attention multiplies a neuron's drive before normalization", CONTROL),
            (r"capacity, \ vigilance and rare targets; \ phones, \ alarms and screens", BAD),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=30, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 18, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part eighteen in ten lines. <bookmark mark='a'/> Far more reaches the senses than reaches report: half of "
            "the observers miss a gorilla, and a flicker hides a large change for many seconds. Broadbent drew the "
            "first diagram of information flowing through a mind, with a filter. Your own name gets through it, "
            "which led to attenuation, late selection, and Lavie's load. A spotlight moves without the eyes, and "
            "avoids returning to where it has just been. A single feature pops out; a conjunction needs search, "
            "guided by features and saliency. What we attend decides what else we see, for experts too. In time, "
            "there is a blink, and a bottleneck where responses are chosen one at a time. Conflict between pathways "
            "slows us, and control fights back. In a neuron, attention multiplies the drive before normalization. "
            "And capacity is limited, vigilance decays, rare targets are missed, and phones, alarms and screens all "
            "compete for the same limited resource."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=50.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"a neuron that computes $\delta$; \ attention as a multiplication before a division",
             STATUS_COLOR["replicated"]),
            (r"experiments by the dozen: \ lots, \ lesions, \ twins, \ a cave, \ a gorilla",
             STATUS_COLOR["replicated"]),
            (r"cue weights read from choices, \ never from reports; \ and illusions that knowing does not undo",
             STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met a "
            "model in which attention is one multiplication placed before one division, and which settled a dispute "
            "about neurons. <bookmark mark='b'/> And the second, that the mind can't be experimented on, met an "
            "experiment anyone can run with a video and a question: did you see the gorilla?"
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows], FadeIn(board.rows[2].reply))
            vo.wait_until("a")
            self.play(Indicate(board.rows[0].objection, color=KANT), FadeIn(board.rows[0].reply, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(Indicate(board.rows[1].objection, color=KANT), FadeIn(board.rows[1].reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"working memory: \ what attention selects, \ and holds", [19]),
            (r"self-control and effort", [28]),
            (r"perceptual decisions as evidence accumulation", [25]),
            (r"attention in development, \ ADHD", [31, 41]),
            (r"human factors: \ vigilance, \ driving, \ cockpits", [51]),
            (r"designing for attention, \ and against it", [52]),
            (r"attention in brains and in machines", [60]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Working memory, what attention selects and then holds, is "
            "next, Part 19. Self-control and the feeling of effort are Part 28. Perceptual decisions as evidence accumulating "
            "to a bound are Part 25. Attention in development, and ADHD, appear in Parts 31 and 41. Vigilance, driving "
            "and cockpits are human factors, Part 51. Designing for attention, and against it, is Part 52. And "
            "attention in brains and in machines is Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=12.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One sets Treisman's "
            "attenuator to match Moray. One derives the two-to-one ratio of serial search. One derives the slope of "
            "minus one under a bottleneck. One explains why interference outweighs facilitation in a diffusion. One "
            "shows where the normalization model's contrast gain comes from. One uses Psyche to trade misses against "
            "search time. And the last, with the star, asks how to tell a limit from a choice. Pause here if you'd "
            "like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"H. Pashler, \emph{The Psychology of Attention} (1998)",
             r"J. M. Wolfe, \ Guided Search 6.0 (2021); \ M. Carrasco, \ Visual attention: the past 25 years (2011)",
             r"D. J. Simons \& C. F. Chabris, \emph{The Invisible Gorilla} (2010)"],
            [r"E. C. Cherry (1953); \ D. E. Broadbent (1958); \ N. Moray (1959); \ A. M. Treisman (1960)",
             r"J. A. Deutsch \& D. Deutsch (1963); \ N. Lavie (1995); \ M. I. Posner (1980); \ Posner \& Cohen (1984)",
             r"A. M. Treisman \& G. Gelade (1980); \ J. M. Wolfe et al.\ (1989); \ L. Itti et al.\ (1998)",
             r"R. A. Rensink et al.\ (1997); \ D. J. Simons \& C. F. Chabris (1999); \ T. Drew et al.\ (2013)",
             r"J. E. Raymond et al.\ (1992); \ H. Pashler (1994); \ J. R. Stroop (1935); \ C. M. MacLeod (1991)",
             r"M. M. Botvinick et al.\ (2001); \ R. D. Rogers \& S. Monsell (1995); \ J. Moran \& R. Desimone (1985)",
             r"J. H. Reynolds \& D. J. Heeger (2009); \ C. Bundesen (1990); \ N. H. Mackworth (1948)",
             r"J. M. Wolfe et al.\ (2005); \ D. L. Strayer \& W. A. Johnston (2001); \ E. Ophir et al.\ (2009)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Harold Pashler's The "
            "Psychology of Attention is the classic text; Simons and Chabris's The Invisible Gorilla is the "
            "readable one."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act V: \ thinking", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 19", font_size=32, color=GREY_B), label(r"Working Memory", font_size=50),
                     wrapped_label(r"George Miller was persecuted by an integer. \ It was the wrong integer.",
                                   6.0, 28, GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Attention decides what gets in. <bookmark mark='a'/> The next question is how much can be held once it "
            "is in, and for how long. <bookmark mark='b'/> In 1956 George Miller said he had been persecuted by an "
            "integer, the magical number seven. It was the wrong integer, and possibly not an integer at all. It's "
            "Part 19: working memory."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
