from __future__ import annotations

from videos.psychology.psych26.common import *  # noqa: F403

PROBLEMS = [
    r"Show that every expected-utility indifference line in the probability triangle has slope "
    r"$(u_2 - u_1)/(u_3 - u_2)$, \ and so that B over A forces D over C in Allais's problems.",
    r"With $v(x) = x^{0.88}$ and no probability weighting, \ which programme does the disease problem's gain frame "
    r"choose? \ What does the weighting function add?",
    r"Show that the 1979 form $\sum w(p_i)\,v(x_i)$ can prefer a lottery to one that dominates it, \ and that the "
    r"cumulative weights cannot.",
    r"For four fair flips, \ list the fourteen sequences with a flip after a head and verify that the average share "
    r"of heads after a head is $17/42$.",
    r"A hyperbolic discounter with $k = 0.05$ a week prefers 110 at week $t + 4$ to 100 at week $t$ for which $t$? "
    r"\ Derive the reversal point.",
    r"With \texttt{explainer.psychology.opendata.choices13k}: \ fit prospect theory with Prelec's weighting "
    r"function instead. \ Does it predict held-out problems better?",
    r"$\star$ \ Design an experiment that would tell the description--experience gap from the effect of small "
    r"samples alone, \ and say what each account predicts.",
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
        d = load("c13k")
        items = [
            (r"the disease problem: \ the same outcomes, \ framed as lives or deaths, \ reverse the choice", RISKY),
            (r"expected value, \ Bernoulli's utility, \ and four axioms; \ independence is the one people break", NORM),
            (r"Allais in the triangle: \ parallel lines, \ parallel steps, \ and people who choose B and C", LOSS),
            (r"prospect theory: \ a kinked value curve and an inverse-S weighting of probabilities", MODEL),
            (r"the fourfold pattern: \ lottery tickets and insurance from one pair of curves", GAIN),
            (rf"choices13k: \ prospect theory explains {100 * d['r2']['cpt']:.0f}\% out of sample; \ loss aversion "
             rf"only {d['params']['cpt']['lam']:.2f} at small stakes", DATA),
            (r"heuristics err systematically; \ frequencies and simple rules often do well", HEUR),
            (r"the hot hand: \ the fallacy was in the statistic", RISKY),
            (r"hyperbolic discounting reverses plans; \ beta--delta names present bias", TIME),
            (r"experience underweights rare events; \ values come partly from what we have sampled", SURE),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=30, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 26, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part twenty-six in ten lines. <bookmark mark='a'/> In the disease problem, the same outcomes framed as "
            "lives or as deaths reverse the choice. The standard is expected value, Bernoulli's utility and four "
            "axioms, and independence is the one people break. In the probability triangle, Allais's choices cross "
            "parallel lines in opposite directions. Prospect theory replaces the standard with a kinked value curve "
            "and an inverse-S weighting of probabilities, and from that one pair of curves comes the fourfold "
            "pattern: lottery tickets and insurance. On almost two thousand open problems, prospect theory "
            f"explains about {100 * d['r2']['cpt']:.0f} percent out of sample, with loss aversion of only "
            f"{d['params']['cpt']['lam']:.2f} at small stakes. Heuristics err systematically, while frequencies and "
            "simple rules often do well. The hot-hand fallacy was in the statistic. Hyperbolic discounting reverses "
            "plans, and beta and delta give present bias a name. And experience underweights rare events, while "
            "values come partly from what we've sampled."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=45.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"prospect theory's curves, \ derived, \ computed, \ and fitted to 1{,}928 open problems out of sample",
             STATUS_COLOR["replicated"]),
            (r"the same outcomes, \ two descriptions: \ framing is an experiment on the mind's reference point",
             STATUS_COLOR["replicated"]),
            (r"choices, \ not introspection: \ and where people explain themselves, \ as with Linda, \ the words "
             r"themselves became the question", STATUS_COLOR["contested"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met a "
            "theory of choice with two curves, derived, computed, and fitted out of sample to almost two thousand "
            "open problems. <bookmark mark='b'/> The second, that the mind can't be experimented on, met the purest "
            "experiment in this part: the same outcomes in two descriptions, which moves the mind's reference "
            "point and nothing else. <bookmark mark='c'/> And the third, that looking inward disturbs what you look "
            "at, met choices rather than reports. Where words mattered, as with Linda, the meaning of the words "
            "became the question, and that point is still argued, so it gets amber."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"consciousness: \ what you experience, \ and what only guides you", [27]),
            (r"personality: \ is risk preference a trait?", [33]),
            (r"social influence: \ framing and persuasion between people", [34]),
            (r"modelling behaviour: \ fitting choice models properly", [48]),
            (r"choice architecture: \ defaults, \ nudges and their evaluation", [55]),
            (r"value as efficient code", [58]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> What you experience, as against what only guides you, is "
            "the next part, on consciousness. Whether risk preference is a trait belongs to personality, Part 33. "
            "Framing and persuasion between people are Part 34. Fitting choice models properly is Part 48. "
            "Defaults and nudges, and how to evaluate them, are Part 55. And value as an efficient code is Part 58."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=11.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One proves that "
            "expected utility's lines in the triangle are parallel. One asks what the value curve alone does with "
            "the disease problem. One shows why the 1979 theory needed its cumulative fix. One counts the coin "
            "flips of the hot-hand bias by hand. One derives the hyperbolic reversal point. One refits the open "
            "data with Prelec's weighting function. And the last, with the star, asks you to design an experiment "
            "that separates the description-experience gap from small samples. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"D. Kahneman, \emph{Thinking, \ Fast and Slow} (2011)",
             r"G. Gigerenzer, \ P. M. Todd \& the ABC Research Group, \emph{Simple Heuristics That Make Us Smart} "
             r"(1999)",
             r"P. P. Wakker, \emph{Prospect Theory for Risk and Ambiguity} (2010)"],
            [r"D. Bernoulli (1738); \ M. Allais (1953); \ J. von Neumann \& O. Morgenstern (1944)",
             r"D. Kahneman \& A. Tversky (1979); \ A. Tversky \& D. Kahneman (1974, \ 1981, \ 1983, \ 1992)",
             r"S. Lichtenstein \& P. Slovic (1971); \ J. Quiggin (1982); \ D. Prelec (1998)",
             r"G. Gigerenzer \& U. Hoffrage (1995); \ G. Gigerenzer \& D. G. Goldstein (1996)",
             r"T. Gilovich, \ R. Vallone \& A. Tversky (1985); \ J. B. Miller \& A. Sanjurjo (2018)",
             r"D. Laibson (1997); \ K. N. Kirby \& R. J. Herrnstein (1995)",
             r"R. Hertwig et al.\ (2004); \ N. Stewart, \ N. Chater \& G. D. A. Brown (2006)",
             r"J. C. Peterson et al.\ (2021); \ K. Ruggeri et al.\ (2020); \ F. Lieder \& T. L. Griffiths (2020)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Kahneman's Thinking, Fast "
            "and Slow is the classic account from one side, to be read with its own published errata, and "
            "Gigerenzer's Simple Heuristics That Make Us Smart from the other. Peter Wakker's book is the "
            "mathematics of prospect theory in full."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act V: \ thinking", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 27", font_size=32, color=GREY_B), label(r"Consciousness", font_size=40),
                     wrapped_label(r"A man who says he sees nothing, \ and points to it anyway.", 6.0, 28, GREY_A)
                     ).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Today the mind chose between risks, and between now and later. <bookmark mark='a'/> Next time, it "
            "notices, or fails to. <bookmark mark='b'/> In 1974 Lawrence Weiskrantz tested a man whose visual cortex "
            "had been damaged on one side. He insisted he saw nothing there. Asked to guess anyway, he pointed to "
            "objects in that blind half almost perfectly. What is the difference between information the brain "
            "uses and information you experience? It's Part 27: consciousness."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
