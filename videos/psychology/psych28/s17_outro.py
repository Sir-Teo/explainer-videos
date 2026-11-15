from __future__ import annotations

from videos.psychology.psych28.common import *  # noqa: F403

PROBLEMS = [
    r"Solve $dx/dt = -k(x - s) + D$ from $x(0) = x_0$, \ and show that the error at rest is $D/k$. \ Why does adding "
    r"$-k_i \int (x - s)\,d\tau$ remove it?",
    r"In the energy-balance loop, \ show that a lasting cut of $c$ kcal a day lowers weight by $c/a$ at rest, \ and "
    r"find how long it takes to lose half of that.",
    r"For Atkinson's $T = (M_s - M_{af}) P (1 - P)$, \ find the preferred $P$ for each sign of $M_s - M_{af}$.",
    r"In the self-perception model, \ show that the inferred interest after drawing falls as the reward's pull "
    r"$\beta_R$ rises. \ What happens when $\beta_R \to \infty$?",
    r"With the RRR table \ (\texttt{opendata.ego\_depletion\_rrr}), \ recompute the pooled $d$ with a fixed-effect "
    r"model and compare. \ Why are they so close?",
    r"Show that the expected remaining wait $\mathbb{E}[T - t \mid T > t]$ falls with $t$ for a normal $T$ and rises "
    r"for a Pareto $T$.",
    r"$\star$ \ Design a test of the opportunity-cost account of effort that the resource account would fail, "
    r"\ and say what each predicts.",
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
            (r"a rat at a lever: \ reward reached directly, \ without the body's needs", WANT),
            (r"homeostasis: \ negative feedback, \ with an error unless the loop remembers", BODY),
            (r"weight: \ a settling point, \ defended against loss", BODY),
            (r"curiosity is rewarding; \ the Yerkes--Dodson law was a story about mice", INTR),
            (r"wanting is not liking: \ value recomputed from the body's state", WANT),
            (r"expected rewards can undermine interest; \ specific, \ hard goals work", EXTR),
            (r"your discount curve, \ by six questions per delay", YOU),
            (r"ego depletion: \ hundreds of studies, \ and 23 laboratories found $d = 0.04$", LOST),
            (r"the marshmallow test and grit: \ real, \ smaller, \ and mostly something else", CTRL),
            (r"effort is a cost, \ chosen: \ try when it pays, \ stop when it does not", MODEL),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=30, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 28, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part twenty-eight in ten lines. <bookmark mark='a'/> A rat at a lever showed reward reached directly, "
            "without passing through the body's needs. Homeostasis is negative feedback, with a steady error unless "
            "the loop remembers. Body weight has a settling point, defended more against loss than gain. Curiosity "
            "is rewarding in itself, and the Yerkes-Dodson law was mostly a story told about some mice. Wanting is "
            "not liking, and a cue's value can be recomputed from the body's state with no new learning. Expected "
            "rewards can undermine interest, and specific, difficult goals work. You measured your own discount "
            "curve with six questions per delay. Ego depletion grew from hundreds of studies, and twenty-three "
            "laboratories found almost nothing. The marshmallow test and grit are real effects, smaller than their "
            "stories, and mostly something else. And effort is a cost the brain chooses to pay: try when it pays, "
            "stop when it doesn't."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=45.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"control loops, \ Bayes, \ expected value of control: \ motives written as equations and solved",
             STATUS_COLOR["replicated"]),
            (r"brain stimulation, \ dopamine lesions, \ a registered test in 23 laboratories", STATUS_COLOR["replicated"]),
            (r"self-reported grit and mindset: \ a trait by questionnaire, \ and most of it was an old one",
             STATUS_COLOR["contested"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "control loops, Bayes's rule and the expected value of control: motives written as equations and solved. "
            "<bookmark mark='b'/> The second, that the mind can't be experimented on, met brain stimulation, "
            "dopamine lesions, and a registered test run by twenty-three laboratories at once. "
            "<bookmark mark='c'/> The third, that introspection disturbs what it observes, hit hardest where the "
            "measure was a questionnaire about oneself: grit and mindset, where most of what was measured turned "
            "out to be an old trait. Amber."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"emotion: \ the feelings that motives come with", [29]),
            (r"wanting without liking: \ addiction", [41]),
            (r"incentives and goals at work", [53]),
            (r"mindset and grit in schools", [54]),
            (r"what machines should want", [60]),
        ], font_size=28)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Emotion is next, in Part 29. Wanting without liking is "
            "the centre of addiction in Part 41. Incentives and goals at work are Part 53, mindset and grit in "
            "schools are Part 54, and what machines should want is Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=8.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One solves the "
            "thermostat and its integral term. One finds the settling point and its half-life. One works through "
            "Atkinson's model. One takes the self-perception model to its limit. One recomputes the replication's "
            "pooled effect a second way, from the open data. One proves the waiting result. And the last, with the "
            "star, asks you to design an experiment that the opportunity-cost account of effort would pass and the "
            "resource account would fail. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"W. B. Cannon, \emph{The Wisdom of the Body} (1932)",
             r"K. C. Berridge \& M. L. Kringelbach, \emph{Pleasure systems in the brain}, \ Neuron (2015)",
             r"W. Mischel, \emph{The Marshmallow Test} (2014)"],
            [r"J. Olds \& P. Milner (1954); \ A. Routtenberg \& J. Lindy (1965)",
             r"K. D. Hall et al.\ (2011); \ R. L. Leibel, \ M. Rosenbaum \& J. Hirsch (1995)",
             r"K. C. Berridge \& T. E. Robinson (1998); \ J. Zhang et al.\ (2009); \ M. J. F. Robinson \& K. C. "
             r"Berridge (2013)",
             r"M. R. Lepper, \ D. Greene \& R. E. Nisbett (1973); \ E. L. Deci, \ R. Koestner \& R. M. Ryan (1999)",
             r"E. A. Locke \& G. P. Latham (2002); \ J. W. Atkinson (1957)",
             r"R. F. Baumeister et al.\ (1998); \ M. S. Hagger et al.\ (2010, \ 2016); \ K. D. Vohs et al.\ (2021)",
             r"T. W. Watts, \ G. J. Duncan \& H. Quan (2018); \ J. T. McGuire \& J. W. Kable (2013)",
             r"A. Shenhav, \ M. M. Botvinick \& J. D. Cohen (2013); \ R. Kurzban et al.\ (2013)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Cannon's The Wisdom of the "
            "Body is still a pleasure to read; Berridge and Morten Kringelbach's review is the best short account of "
            "wanting and liking; and Mischel's own book on the marshmallow test is worth reading alongside the 2018 "
            "replication."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act VI \ begun: \ feeling and wanting", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 29", font_size=32, color=GREY_B), label(r"Emotion", font_size=40),
                     wrapped_label(r"Do we run because we are afraid, \ or are we afraid because we run?",
                                   6.0, 28, GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "That's the first part of Act Six, on feeling and wanting. <bookmark mark='a'/> Motives come with "
            "feelings, and the next part is about them. <bookmark mark='b'/> In 1884 William James asked whether we "
            "run from a bear because we are afraid, or are afraid because we run, and answered: the second. "
            "Psychology has argued about the order of events ever since, through a pen held in the teeth, a "
            "rickety bridge, and faces photographed around the world. It's Part 29: emotion."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
