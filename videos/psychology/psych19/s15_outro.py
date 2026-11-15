from __future__ import annotations

from videos.psychology.psych19.common import *  # noqa: F403

PROBLEMS = [
    r"Smith recoded binary digits in groups of five. \ With a span of 8 chunks, \ how many binary digits could he "
    r"hold, \ and how many bits is that per chunk?",
    r"Derive Cowan's $K = N(H - F)$ from a slot model with guessing, \ and Pashler's $K = N(H - F)/(1 - F)$ for a "
    r"whole-display test.",
    r"Show that $j$ exponential comparisons each at rate $1/(jc)$ finish first after an exponential time of mean "
    r"$c$, \ and hence that limited-capacity parallel search mimics serial search.",
    r"In SIMPLE with $c = 1$, \ find the discriminability of an item 3 s old among items 30 and 60 s old, \ and of the "
    r"same item at 18 s.",
    r"Compute the Fisher information $J$ of a von Mises with $\kappa = 5$, \ and the circular s.d. of the same "
    r"distribution.",
    r"With \texttt{explainer.psychology.psyche.wm}: \ simulate a slots observer, \ fit the variable-precision "
    r"model, \ and report which model AIC prefers as the number of trials grows.",
    r"$\star$ \ Design a training study whose far-transfer result could convince a sceptic, \ and say what its "
    r"control group must believe.",
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
            (r"span counts chunks, \ not bits: \ recode, \ and the span grows", EXEC),
            (r"a large icon fades in a second; \ report, \ not seeing, \ is the bottleneck", MODEL),
            (r"forgetting in seconds is crowding, \ not decay: \ the first trial forgets nothing", LOST),
            (r"a system, \ not a store: \ the loop holds about two seconds of speech", LOOP),
            (r"memory scanning is linear, \ and a parallel model can draw the same line", MEM),
            (r"without rehearsal, \ about four: \ $K = N(H - F)$", MEM),
            (r"precision falls continuously with load; \ variable precision fits the open data best", MODEL),
            (r"a ring of neurons holds a bump, \ which diffuses: \ memory blurs with time", MEM),
            (r"working memory tracks reasoning, \ but training it does not raise reasoning", LOST),
            (r"a small workspace may be a budget spent well, \ not a defect", EXEC),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=30, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 19, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part nineteen in ten lines. <bookmark mark='a'/> Span counts chunks, not bits, so recoding makes it grow. "
            "A large visual icon fades within a second, and reporting, not seeing, is the bottleneck. Forgetting in "
            "seconds is mostly crowding by similar memories, which is why the first trial forgets almost nothing. "
            "Working memory is a system, and its phonological loop holds about two seconds of speech. Scanning it "
            "takes time in a straight line, which a parallel model can draw just as well. Without rehearsal, people "
            "hold about four items, counted by a formula that assumes slots. Precision falls continuously with load, "
            "and variable precision fits the open data best. A ring of neurons can hold a bump of activity, which "
            "diffuses, so memories blur with time. Working memory tracks reasoning across people, but training it "
            "does not raise reasoning. And the small size of the workspace may be a budget well spent, rather than a "
            "defect."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=45.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"a neuron that computes $\delta$; \ attention as a multiplication; \ a limit fitted trial by trial",
             STATUS_COLOR["replicated"]),
            (r"experiments by the dozen: \ lots, \ lesions, \ twins, \ a gorilla, \ a tone that picks a row",
             STATUS_COLOR["replicated"]),
            (r"cue weights read from choices, \ never from reports; \ and illusions that knowing does not undo",
             STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met a "
            "contest between four likelihoods, each fitted to seven thousand judgments of colour, with a winner. "
            "<bookmark mark='b'/> And the second, that the mind can't be experimented on, met Sperling's tone: a "
            "way to sample what someone saw without asking them to report it all."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows], FadeIn(board.rows[2].reply))
            vo.wait_until("a")
            self.play(Indicate(board.rows[0].objection, color=KANT), FadeIn(board.rows[0].reply, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(Indicate(board.rows[1].objection, color=KANT), FadeIn(board.rows[1].reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"long-term memory, \ and memory as activation", [20, 21]),
            (r"working memory across the lifespan; \ in ADHD", [31, 41]),
            (r"working memory and intelligence", [32]),
            (r"model recovery, \ and models that mimic each other", [48]),
            (r"read-backs, \ checklists, \ cognitive load", [51, 54]),
            (r"the limit as an efficient code", [58]),
            (r"small workspaces and large contexts", [60]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Long-term memory, and the idea that working memory is its "
            "active part, are Parts 20 and 21. Working memory across the lifespan and in ADHD are Parts 31 and 41. "
            "Its relation to intelligence is Part 32. Models that mimic each other, and how to tell them apart, are "
            "Part 48. Read-backs, checklists and cognitive load are Parts 51 and 54. The limit as an efficient code "
            "is Part 58. And small workspaces against large contexts is Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=12.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One does Smith's "
            "arithmetic. One derives both K formulas. One proves Townsend's mimicry. One computes SIMPLE's "
            "discriminability by hand. One computes the precision of a von Mises. One uses Psyche to see when a "
            "model comparison can be trusted. And the last, with the star, asks you to design the training study "
            "that would convince a sceptic. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"A. Baddeley, \emph{Working Memory, \ Thought, \ and Action} (2007)",
             r"N. Cowan, \emph{Working Memory Capacity} (2005); \ W. J. Ma, \ M. Husain \& P. M. Bays, \ Changing "
             r"concepts of working memory (2014)",
             r"K. Oberauer et al., \ Benchmarks for models of short-term and working memory (2018)"],
            [r"G. A. Miller (1956); \ G. Sperling (1960); \ L. R. \& M. J. Peterson (1959); \ G. Keppel \& B. J. "
             r"Underwood (1962)",
             r"R. C. Atkinson \& R. M. Shiffrin (1968); \ T. Shallice \& E. K. Warrington (1970); \ A. D. Baddeley \& "
             r"G. Hitch (1974)",
             r"A. D. Baddeley et al.\ (1975); \ S. Sternberg (1966); \ J. T. Townsend (1972); \ G. D. A. Brown et al.\ "
             r"(2007)",
             r"S. J. Luck \& E. K. Vogel (1997); \ N. Cowan (2001); \ W. Zhang \& S. J. Luck (2008)",
             r"P. M. Bays et al.\ (2009); \ R. van den Berg et al.\ (2012, 2014); \ S. Funahashi et al.\ (1989)",
             r"K. Wimmer et al.\ (2014); \ G. Mongillo et al.\ (2008); \ M. Daneman \& P. A. Carpenter (1980)",
             r"M. J. Kane et al.\ (2005); \ S. M. Jaeggi et al.\ (2008); \ T. S. Redick et al.\ (2013)",
             r"M. Melby-Lerv\aa{}g et al.\ (2016); \ D. J. Simons et al.\ (2016); \ C. R. Sims et al.\ (2012)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Alan Baddeley's Working "
            "Memory, Thought, and Action is the classic account by the model's author; Ma, Husain and Bays's review "
            "is the clearest introduction to precision and resources."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act V: \ thinking", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 20", font_size=32, color=GREY_B), label(r"Memory I: \ Storing and Finding",
                                                                           font_size=40),
                     wrapped_label(r"1885: \ Hermann Ebbinghaus, \ alone, \ learns 2,300 nonsense syllables.",
                                   6.0, 28, GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Working memory holds a few things for a few seconds. <bookmark mark='a'/> Everything else you know is "
            "somewhere else. <bookmark mark='b'/> In 1885 Hermann Ebbinghaus, working alone, made up two thousand "
            "three hundred nonsense syllables and spent years learning and relearning them, to measure how memory "
            "is stored and lost. It's Part 20: memory, storing and finding."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
