from __future__ import annotations

from videos.psychology.psych1.common import *  # noqa: F403

PROBLEMS = [
    r"A nerve is stimulated at two points 55 mm apart, and the twitch from the farther point begins 1.7 ms later. "
    r"\ What speed does that give, and how long would such a signal take to travel one metre?",
    r"Donders' means were 201 ms (a), 237 ms (c) and 284 ms (b). \ Compute his two differences. \ Now suppose "
    r"go/no-go contains a 30 ms decision, and the choice task a 25 ms stage that programs the response. \ What are "
    r"the durations of discrimination and of choice?",
    r"Show that if $\text{RT}_c = \text{RT}_a + D$ with $D$ independent of $\text{RT}_a$, then "
    r"$\operatorname{Var}[\text{RT}_c] = \operatorname{Var}[\text{RT}_a] + \operatorname{Var}[D]$. \ A subject's "
    r"variances are 900 ms$^2$ in task a and 700 ms$^2$ in task c. \ What follows?",
    r"Two factors multiply the mean duration of the \emph{same} 50 ms stage by 1.4 and by 1.6. \ Write the "
    r"$2 \times 2$ table of mean reaction times (the other stages total 250 ms) and its interaction contrast. \ "
    r"Repeat with the factors acting on two \emph{different} 50 ms stages.",
    r"A website reports that phone users have slower reaction times than laptop users. \ Give three explanations "
    r"other than ``phone users are slower'', and a design that would separate them.",
    r"With \texttt{explainer.psychology.psyche.chronometry}: simulate 2,000 choice reaction times, fit an "
    r"ex-Gaussian, then double the mean of the choice stage and fit again. \ Which of $\mu$, $\sigma$, $\tau$ move?",
    r"$\star$ \ Design an experiment on Battery task 1 whose reaction-time distributions would separate discrete "
    r"stages from a cascade.",
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
            (r"Kant, 1786: \ three objections to a science of the mind", KANT),
            (r"Helmholtz, 1850: \ $v = \Delta x / \Delta t$, \ 25 to 43 m/s in a frog's nerve", NERVE),
            (r"Donders, 1868: \ $c - a = 36$ ms, \ $b - c = 47$ ms", CHOOSE),
            (r"pure insertion: \ means cannot test it; \ variances can", DISC),
            (r"additive factors: \ different stages add, \ the same stage interacts", P.ACCENT),
            (r"Fechner, 1860: \ $S = \frac{1}{k}\ln(I / I_0)$", "#C9A227"),
            (r"Ebbinghaus, 1885: \ memory, measured by the time saved", P.ARCHIVE),
            (r"the mind banned in 1913, \ and back by 1956: \ maps, plans, bits", "#7EC8F5"),
            (r"Marr: \ what is computed, \ by what algorithm, \ in what tissue", "#7BD88F"),
            (r"explain a faculty by building it: \ Psyche, the Pool, the Battery, the Ledger", P.PSYCHE),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=34, color=c) for i, (t, c) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        head = label(r"Part 1, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7  # Chinese lines are taller: keep the tenth inside the frame
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part one in ten lines. <bookmark mark='a'/> Kant gave three reasons why the mind could never be a "
            "subject for science. Helmholtz showed that a signal in a nerve takes time, and measured its speed "
            "by dividing a distance by a delay. Donders subtracted one task from another, and gave a choice a "
            "duration. His subtraction assumes pure insertion, which three averages can't test, and whole "
            "distributions can. Sternberg's additive factors read the stages off a pattern instead. Fechner "
            "defined sensation by counting noticeable steps, and got a logarithm. Ebbinghaus measured memory by "
            "the time saved in relearning. The behaviourists banned the mind in 1913, and by 1956 maps, plans "
            "and bits had brought it back. Marr separated what is computed, by what algorithm, and in what "
            "tissue. And the way to explain a faculty without a little person inside is to build it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.75), run_time=38.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"numbers apply: \ a division, a subtraction, a logarithm, a forgetting curve",
             STATUS_COLOR["replicated"]),
            (r"tasks can be taken apart and recombined; \ whether the mind's stages can is a question the data "
             r"answer, case by case", STATUS_COLOR["contested"]),
            (r"still open: \ introspection failed on exactly this. \ Part 2 begins here", P.ERR),
        ))
        with self.voiceover(
            "So how does Kant's wager stand? <bookmark mark='a'/> On the first objection he has lost. Numbers "
            "apply: a division, a subtraction, a logarithm, a forgetting curve. <bookmark mark='b'/> On the "
            "second he has half a point. Tasks can be taken apart and put together again. But whether the mind's "
            "own stages can be, without changing them, is exactly the question of pure insertion, and the "
            "answer depends on the case. <bookmark mark='c'/> And on the third, that the observer disturbs what "
            "is observed, he is still ahead. Introspection failed on precisely this. And the next part begins "
            "with the most famous case of an observer disturbing the observed, without knowing it."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r.objection) for r in board.rows])
            for mark, r in zip("abc", board.rows):
                vo.wait_until(mark)
                self.play(FadeIn(r.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"thresholds and Fechner's law", [11]),
            (r"subtraction, in the brain scanner", [8]),
            (r"additive factors and memory search", [19]),
            (r"Ebbinghaus's curve", [20, 21]),
            (r"the shape of reaction times; \ Hick's law", [25, 52]),
            (r"the average describes no one", [47, 48]),
            (r"the observer disturbs", [2, 4]),
            (r"the Homunculus's last drawing", [62]),
        ], font_size=31)
        with self.voiceover(
            "Almost everything here comes back. <bookmark mark='a'/> Fechner's law and your own threshold, in "
            "Part 11. Donders' subtraction, as the logic of brain imaging, in Part 8. Additive factors in "
            "Part 19, Ebbinghaus's curve in Parts 20 and 21. The shape of reaction times, and Hick's law, in "
            "Part 25, and in interface design in Part 52. The group average that describes no one, in the "
            "graduate toolkit. And Kant's third objection, in the very next part."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.4), run_time=9.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=25)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One is Helmholtz's "
            "arithmetic. Two are about Donders' subtraction and what it assumes. One works out an additive-factor "
            "table by hand. One asks you to find the confounds in a claim about phones and laptops. One uses "
            "Psyche's own code. And the last, marked with a star, is the research problem. Pause here if you'd "
            "like to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"E. G. Boring, \emph{A History of Experimental Psychology} (2nd ed., 1950); \ K. Danziger, "
             r"\emph{Constructing the Subject} (1990)",
             r"R. D. Luce, \emph{Response Times} (1986); \ R. S. Woodworth, \emph{Experimental Psychology} (1938)",
             r"D. Marr, \emph{Vision} (1982), ch.~1; \ D. C. Dennett, \emph{Brainstorms} (1978)",
             r"H. Gardner, \emph{The Mind's New Science} (1985)"],
            [r"I. Kant, \emph{Metaphysical Foundations of Natural Science} (1786), Preface; \ H. Helmholtz (1850); \ "
             r"G. T. Fechner, \emph{Elemente der Psychophysik} (1860)",
             r"F. C. Donders (1868; transl.\ 1969); \ H. Ebbinghaus, \emph{\"Uber das Ged\"achtnis} (1885); \ "
             r"J. B. Watson (1913)",
             r"E. C. Tolman (1948); \ K. S. Lashley (1951); \ W. E. Hick (1952); \ S. Sternberg (1969); \ "
             r"J. L. McClelland (1979)",
             r"H. Schmidgen, \emph{Endeavour} 26 (2002); \ G. A. Miller, \emph{Trends in Cognitive Sciences} 7 (2003)",
             r"D. L. Woods et al., \emph{Front.\ Hum.\ Neurosci.}\ 9 (2015); \ A. Roelofs, \emph{Acta Psychologica} "
             r"191 (2018); \ R. W. Proctor \& D. W. Schneider (2018)"])
        with self.voiceover(
            "The books and papers this part follows are listed here and in the README: Boring's and Danziger's "
            "histories, Luce on response times, Marr and Dennett, and the original papers, from Kant's preface "
            "to the 2018 reanalysis of Donders' notebook."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=1, height=6.2).move_to([-3.9, 0.1, 0])
        tally = label(r"one faculty begun, \ nineteen to go", font_size=26, color=P.MECH).next_to(hm, DOWN, buff=0.15)
        nxt = VGroup(label(r"Part 2", font_size=32, color=GREY_B), label(r"The Experiment", font_size=54),
                     wrapped_label(r"Berlin, 1904. \ A horse named Hans is doing arithmetic, and a commission of "
                                   r"experts can find no trick.", 6.0, 28, GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "That's the first gear in the head: one faculty begun, and nineteen to go. <bookmark mark='a'/> We "
            "ended on the objection Kant is still winning: the observer disturbs what is observed. "
            "<bookmark mark='b'/> In Berlin in 1904, a horse named Hans was doing arithmetic, tapping out the "
            "answers with his hoof, and a commission of thirteen experts could find no trick. There was no "
            "trick. What there was, and how one young psychologist found it, gave psychology its rules for "
            "asking a mind a question. That's Part 2: the experiment."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            self.play(Circumscribe(VGroup(hm.token["reacts"], hm.name["reacts"]), color=P.MECH, buff=0.08))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
