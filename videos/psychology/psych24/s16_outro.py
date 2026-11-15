from __future__ import annotations

from videos.psychology.psych24.common import *  # noqa: F403

PROBLEMS = [
    r"Use the eight kinds of thing to show that \emph{No $A$ are $B$; \ all $B$ are $C$} \ has exactly one valid "
    r"conclusion, \ and say which.",
    r"Without existential presupposition, \ which of the 27 valid syllogisms lose their conclusion? \ Explain why "
    r"\emph{all $A$ are $B$; \ all $B$ are $C$} \ still implies \emph{some $A$ are $C$} only if $A$ is nonempty.",
    r"For optimal data selection with an even prior, \ show that the not-$q$ card's information gain does not "
    r"depend on $P(q)$, \ and find where the $q$ card falls below it when $P(p) = 0.1$.",
    r"Show that the Tower of Hanoi with $n$ discs has $3^n$ states and needs $2^n - 1$ moves, \ and that the goal "
    r"stack's longest pause comes before the first move.",
    r"Derive causal power $q = \Delta P / (1 - P(e \mid \neg c))$ from the noisy-OR model, \ and find the "
    r"corresponding power for a cause that prevents the effect.",
    r"With \texttt{explainer.psychology.opendata}: \ fit each person's rotation rate separately for same and mirror "
    r"pairs. \ Are mirror pairs rotated at the same speed?",
    r"$\star$ \ Design an experiment that separates a power-law prior from an Erlang prior in people's everyday "
    r"predictions, \ person by person.",
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
            (r"four cards: \ abstract rules defeat most people; \ a drinking rule almost none", CONTENT),
            (r"twenty-seven valid syllogisms, \ and 139 people right on 41\% of answers", LOGIC),
            (r"mental models, \ rules and shortcuts: \ no single account fits", LOGIC),
            (r"rarity makes the ``wrong'' cards informative: \ optimal data selection", MODEL),
            (r"problems are spaces of states; \ searching them well needs subgoals", SEARCH),
            (r"insight is hard to see coming: \ the nine dots need the outside of the box", INSIGHT),
            (r"experts see chunks; \ practice matters, \ but ten thousand hours is a story", CONTENT),
            (r"analogy maps relations, \ not looks: \ the fortress and the tumour", INSIGHT),
            (r"mental rotation, \ about 93 degrees a second, \ in 54 people's open data", SEARCH),
            (r"causal power, \ everyday priors, \ and a mind that satisfices", MODEL),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=30, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 24, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part twenty-four in ten lines. <bookmark mark='a'/> Abstract rules defeat most people on four cards; a "
            "drinking rule defeats almost no one. Twenty-seven syllogisms have a valid conclusion, and a hundred and "
            "thirty-nine people were right on forty-one percent of their answers. Mental models, rules and shortcuts "
            "each explain part of what people do, and no single account fits. Under rarity, the wrong cards are the "
            "informative ones. Problems are spaces of states, and searching them well needs subgoals. Insight is hard "
            "to see coming, and the nine dots really do need the outside of the box. Experts see chunks; practice "
            "matters, but ten thousand hours is a story. Analogy maps relations, not looks. Mental rotation runs at "
            "about ninety-three degrees a second in fifty-four people's open data. And causes, everyday priors, and "
            "a mind that settles for good enough."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=45.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"validity computed for every syllogism; \ information gain, \ search spaces and rotation fitted",
             STATUS_COLOR["replicated"]),
            (r"four cards, \ two contents, \ one logical form: \ an experiment that isolates content",
             STATUS_COLOR["replicated"]),
            (r"answers, \ move times and rotation times, \ measured; \ thinking aloud, \ checked against a model",
             STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "validity computed for every syllogism, and information, search spaces and rotation fitted to data. "
            "<bookmark mark='b'/> The second, that the mind can't be experimented on, met four cards with one "
            "logical form and two contents: an experiment that isolates what content does. "
            "<bookmark mark='c'/> And the third, that looking inward disturbs what you look at, met answers, move "
            "times and rotation times, measured, and thinking aloud, used only where it could be checked against a "
            "model."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"deciding in time: \ evidence accumulates to a bound", [25]),
            (r"judgement and decision: \ heuristics and biases", [26]),
            (r"modelling behaviour: \ fitting and comparing reasoning models", [48]),
            (r"designing for minds: \ usability testing", [52]),
            (r"work and organizations: \ selecting people", [53]),
            (r"the science of learning: \ worked examples and practice", [54]),
            (r"minds and machines: \ reasoning in language models", [60]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> How long a decision takes is the next part. Judgement and "
            "its biases are Part 26. Fitting and comparing reasoning models is Part 48. Usability testing is Part "
            "52, selecting people for jobs is Part 53, worked examples and practice are Part 54, and reasoning in "
            "language models is Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=12.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One finds the only valid "
            "conclusion of the hardest syllogism. One asks what happens without assuming the terms name anything. "
            "One finds when the not-Q card becomes worth turning. One counts the tower's states and moves. One "
            "derives causal power and its preventive twin. One fits rotation separately for mirror pairs, on the open "
            "data. And the last, with the star, asks you to tell two priors apart in a single person. Pause here if "
            "you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"A. Newell \& H. A. Simon, \emph{Human Problem Solving} (1972)",
             r"P. N. Johnson-Laird, \emph{How We Reason} (2006)",
             r"K. J. Holyoak \& R. G. Morrison (eds.), \emph{The Oxford Handbook of Thinking and Reasoning} (2012)"],
            [r"P. C. Wason (1966, \ 1968); \ R. A. Griggs \& J. R. Cox (1982); \ L. Cosmides (1989)",
             r"J. St B. T. Evans et al.\ (1983); \ S. Khemlani \& P. N. Johnson-Laird (2012)",
             r"M. Oaksford \& N. Chater (1994); \ P. W. Cheng \& K. J. Holyoak (1985)",
             r"K. Duncker (1945); \ J. Metcalfe \& D. Wiebe (1987); \ J. N. MacGregor et al.\ (2001)",
             r"W. G. Chase \& H. A. Simon (1973); \ K. A. Ericsson et al.\ (1993); \ B. N. Macnamara et al.\ (2014)",
             r"M. L. Gick \& K. J. Holyoak (1980); \ D. Gentner (1983); \ R. N. Shepard \& J. Metzler (1971)",
             r"P. W. Cheng (1997); \ T. L. Griffiths \& J. B. Tenenbaum (2006); \ H. A. Simon (1955)",
             r"G. Ganis \& R. Kievit (2015); \ T. Webb et al.\ (2023); \ S. LeGris et al.\ (2024)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Newell and Simon's Human "
            "Problem Solving is where the field's methods began, and Phil Johnson-Laird's How We Reason is the best "
            "single book on deduction by people rather than by logicians."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act V: \ thinking", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 25", font_size=32, color=GREY_B), label(r"Deciding in Time", font_size=40),
                     wrapped_label(r"Why does a decision take the time it takes? \ A wartime test for "
                                   r"ammunition, \ and a mind that adds up evidence until it crosses a line.",
                                   6.0, 28, GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Today the mind reasoned, searched, and guessed well enough. <bookmark mark='a'/> Next time, it decides, "
            "against the clock. <bookmark mark='b'/> During the Second World War a statistician worked out the "
            "fastest reliable way to decide between two hypotheses: keep adding up evidence until it crosses a line. "
            "Thirty years later, psychologists found that people seem to do the same, in half a second. It's Part "
            "25: deciding in time."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
