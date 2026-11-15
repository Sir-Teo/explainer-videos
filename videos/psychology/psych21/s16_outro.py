from __future__ import annotations

from videos.psychology.psych21.common import *  # noqa: F403

PROBLEMS = [
    r"Fit $S = a t^{-b}$ to Ebbinghaus's savings by least squares on $\log S$ against $\log t$, \ and show that its "
    r"hazard $-d \ln S / dt$ is $b/t$.",
    r"Prove that if $\lambda \sim \mathrm{Gamma}(k, \theta)$, \ then $E\,e^{-\lambda t} = (1 + \theta t)^{-k}$, \ "
    r"and say why this warns against reading a single trace's law off an average.",
    r"Solve $\dot h = -a h$, \ $\dot c = k h - b c$ from $h(0) = 1$, \ $c(0) = 0$, \ and find the age at which "
    r"$c$ peaks.",
    r"In the bifurcation model, \ give feedback after the initial test so that failed items gain $g_f$. \ How "
    r"does the crossover delay move as $g_f$ grows?",
    r"Show that $\hat{x} = \lambda y + (1 - \lambda) \rho$ with $\lambda = \sigma_c^2 / (\sigma_c^2 + \sigma_y^2)$ "
    r"minimises $E(\hat{x} - x)^2$, \ and that the minimum is $\lambda \sigma_y^2$.",
    r"With \texttt{explainer.psychology.opendata}: \ pool the second overshadowing replication yourself, \ fixed "
    r"and random effects, \ and test whether the original's effect lies in the pooled interval.",
    r"$\star$ \ Design a line-up study that could tell whether confidence inflation after feedback changes the "
    r"memory itself, \ or only the report.",
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
            (r"forgetting is fast, \ then slow, \ in every replication; \ a power law, \ with a caution about "
             r"averages", LOST),
            (r"much forgetting is interference, \ from what came before and after, \ and even from remembering", CUE),
            (r"memories consolidate from hippocampus to cortex, \ in sleep, \ and reopen when recalled", CTX),
            (r"a fast and a slow learner, \ joined by replay, \ learn the penguin without losing the robin", MODEL),
            (r"space your study, \ with the gap set by how long you need it", TRACE),
            (r"test yourself: \ retrieval strengthens, \ and the feeling of fluency misleads", TRACE),
            (r"recall blends the trace with the schema: \ biased, \ and more accurate on average", CTX),
            (r"a memory that sums similar experiences remembers the word that was never there", FALSE),
            (r"suggestion becomes memory; \ verbal overshadowing is real, \ and smaller than first reported", FALSE),
            (r"initial confidence, \ under good procedures, \ tells you a lot; \ later confidence, \ little", MODEL),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=30, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 21, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part twenty-one in ten lines. <bookmark mark='a'/> Forgetting is fast and then slow, in every attempt "
            "to repeat Ebbinghaus, and a power law describes it, with a caution about what averages can hide. Much "
            "forgetting is interference: from what you learnt before, what you learnt after, and even from "
            "remembering itself. Memories consolidate, moving from the hippocampus toward the cortex, with sleep's "
            "help, and become fragile again when they're recalled. A fast learner and a slow one, joined by replay, "
            "can learn about penguins without forgetting about robins. Space your study, with the gap set by how "
            "long you'll need it. Test yourself, because retrieval strengthens, and the fluent feeling of "
            "re-reading misleads. Recall blends a trace with a schema: biased, and on average more accurate. A "
            "memory that sums similar experiences will remember a word that was never there. Suggestion becomes "
            "memory, and verbal overshadowing is real, and smaller than first reported. And a witness's first "
            "confidence, under good procedures, tells you a lot; their later confidence, very little."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=45.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"attention as a multiplication; \ memory search fitted recall by recall; \ forgetting laws, \ spacing "
             r"and testing fitted",
             STATUS_COLOR["replicated"]),
            (r"experiments by the dozen, \ and one replicated by 53 sets of labs, \ with every lab's data open",
             STATUS_COLOR["replicated"]),
            (r"cue weights read from choices, \ never from reports; \ and illusions that knowing does not undo",
             STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "laws of forgetting compared by their likelihood, a model of spacing that predicts the best gap, and a "
            "model of testing that predicts the crossover. <bookmark mark='b'/> And the second, that the mind can't "
            "be experimented on, met an experiment repeated in fifty-three sets of laboratories at once, with every "
            "lab's data open for anyone to pool."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows], FadeIn(board.rows[2].reply))
            vo.wait_until("a")
            self.play(Indicate(board.rows[0].objection, color=KANT), FadeIn(board.rows[0].reply, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(Indicate(board.rows[1].objection, color=KANT), FadeIn(board.rows[1].reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"concepts, \ categories, \ and the penguin again", [22]),
            (r"memory across the lifespan", [31]),
            (r"fear, \ trauma and their treatment", [40]),
            (r"model fitting and model comparison", [48]),
            (r"learning: \ spacing, \ testing, \ the classroom", [54]),
            (r"witnesses, \ line-ups, \ the courtroom", [56]),
            (r"memory in machines", [60]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Concepts and categories, and the penguin again, are the next "
            "part. Memory across the lifespan is Part 31. Fear, trauma and their treatment come in Part 40. Fitting and "
            "comparing models is Part 48. Spacing, testing and the classroom are Part 54. Witnesses, line-ups and "
            "the courtroom are Part 56. And memory in machines is Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=12.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One fits the power law "
            "and derives its hazard. One proves the averaging result. One solves the two-store model. One adds "
            "feedback to the bifurcation model. One derives the category adjustment model's optimal weight. One "
            "pools the overshadowing replication from the open data. And the last, with the star, asks you to design "
            "a line-up study that could tell whether feedback changes the memory, or only the words. Pause here if "
            "you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"D. L. Schacter, \emph{The Seven Sins of Memory} (2001; 2nd ed., \ 2021)",
             r"A. Baddeley, \ M. W. Eysenck \& M. C. Anderson, \emph{Memory} (3rd ed., \ 2020)",
             r"P. C. Brown, \ H. L. Roediger \& M. A. McDaniel, \emph{Make It Stick} (2014)"],
            [r"J. M. J. Murre \& J. Dros (2015); \ J. T. Wixted \& E. B. Ebbesen (1991); \ B. J. Underwood (1957)",
             r"M. C. Anderson, \ R. A. Bjork \& E. L. Bjork (1994); \ K. Nader et al.\ (2000); \ T. E. Hardwicke et "
             r"al.\ (2016)",
             r"J. L. McClelland, \ B. L. McNaughton \& R. C. O'Reilly (1995); \ M. McCloskey \& N. J. Cohen (1989)",
             r"N. J. Cepeda et al.\ (2008); \ P. I. Pavlik \& J. R. Anderson (2005); \ H. L. Roediger \& J. D. "
             r"Karpicke (2006)",
             r"F. C. Bartlett (1932); \ J. Huttenlocher, \ L. V. Hedges \& S. Duncan (1991); \ H. L. Roediger \& "
             r"K. B. McDermott (1995)",
             r"E. F. Loftus \& J. E. Pickrell (1995); \ A. Scoboria et al.\ (2017); \ V. K. Alogna et al.\ (2014)",
             r"J. M. Talarico \& D. C. Rubin (2003); \ J. T. Wixted \& G. L. Wells (2017); \ B. Settles \& B. "
             r"Meeder (2016)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Daniel Schacter's The Seven "
            "Sins of Memory is the best short tour of how memory fails, and Make It Stick, by Peter Brown, Henry "
            "Roediger and Mark McDaniel, turns chapters five and six into advice."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act V: \ thinking", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 22", font_size=32, color=GREY_B), label(r"Concepts and Categories", font_size=40),
                     wrapped_label(r"Is a penguin a bird? \ Is a tomato a fruit? \ How fast do you say yes, \ and "
                                   r"what does the speed tell us about what a concept is?", 6.0, 28, GREY_A)
                     ).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Today the penguin taught a network to forget about robins. <bookmark mark='a'/> Next time it raises a "
            "deeper question. <bookmark mark='b'/> Is a penguin a bird? Is a tomato a fruit? You'll answer faster "
            "for some birds than for others, and that difference is the key to what a concept is: a definition, an "
            "average, or a memory of every example you've met. It's Part 22: concepts and categories."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
