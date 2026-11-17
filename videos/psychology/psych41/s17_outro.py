from __future__ import annotations

from videos.psychology.psych41.common import *  # noqa: F403

PROBLEMS = [
    r"The hollow mask: \ a prior at $+1$ with precision 6 meets a stereo signal at $-1$ with precision 4. \ Find the "
    r"posterior mean. \ Is a face seen? \ At what prior precision is the posterior exactly 0?",
    r"The expected error of a prior with weight $w$ is $(1 - w)^2/\pi_e + (1 - p)(2w)^2$. \ Find the best $w$, \ and "
    r"the best prior precision, \ for $\pi_e = 4$ and $p = 0.95$, \ then $p = 0.6$.",
    r"In Redish's model, \ $\delta = \max(r - V + D, D)$. \ Show that $V$ grows by at least $\alpha D$ per use, \ and "
    r"bound $V$ after 300 uses with $\alpha = 0.1$, \ $D = 0.2$.",
    r"With $V = A/(1 + kD)$ and $k = 0.05$ per day, \ compare 50 now with 100 in 30 days, \ then 50 in 60 days with "
    r"100 in 90 days. \ What happens, \ and why does it matter for relapse?",
    r"A Rescorla-Wagner cue gets bursts of size $b$ on a share $q$ of trials and no reward. \ Find its average learned "
    r"value. \ Evaluate it for $q = 0.2$, \ $b = 1$.",
    r"Children born in August are diagnosed with ADHD at 85.1 per 10{,}000, \ those born in September at 63.6. \ If "
    r"the whole difference is due to relative age, \ what share of the August-born diagnoses does it account for?",
    r"$\star$ \ Design a study that could tell whether a tendency to conditioned hallucinations is a stable trait "
    r"or tracks a person's current state.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.your_numbers()
        self.recap()
        self.score()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def your_numbers(self):
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for n, q, ans, c in (
                (r"1", r"heritability of schizophrenia in twin studies", r"about 80\%", PERSON),
                (r"2", r"Vietnam veterans addicted again within a year of home", r"about 5\%", MODEL),
                (r"3", r"children in the Danish vaccine study", r"657{,}461", SYMP),
                (r"4", r"medication's advantage left at three years in the MTA trial", r"none", GOOD)):
            rows.add(VGroup(label(n, font_size=30, color=c), wrapped_label(q, 6.8, 23, WHITE),
                            label(ans, font_size=28, color=c)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"strong genes and strong settings; \ myths ended by plain tests; \ effects that fade", 12.0,
                             22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> The heritability of schizophrenia in twin studies: about "
            "eighty percent. Vietnam veterans addicted again within a year of coming home: about five percent. "
            "Children in the Danish vaccine study: six hundred and fifty-seven thousand, four hundred and sixty-one. "
            "And medication's advantage left at three years in the largest ADHD trial: none. "
            "<bookmark mark='b'/> Strong genes, and strong settings. Myths ended by plain tests. And effects that fade."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=8.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"the hollow mask needs a strong prior, \ and many people with schizophrenia are not fooled", SYMP),
            (r"schizophrenia: \ positive, \ negative and cognitive symptoms, \ and a course that varies widely", WHITE),
            (r"antipsychotics block dopamine D2 receptors, \ and work on positive symptoms, \ at a cost", AUTH),
            (r"aberrant salience: \ dopamine out of step makes the irrelevant feel meant", MODEL),
            (r"hallucinations as strong priors: \ influential, \ contested", SYMP),
            (r"heritability near 0.8, \ from hundreds of variants; \ and blaming mothers did harm", PERSON),
            (r"addiction: \ reward, \ tolerance, \ wanting without liking, \ habit and steep discounting", AUTH),
            (r"a drug's surge that cannot be learned away, \ computed, \ and a prediction that failed", MODEL),
            (r"setting matters; \ vouchers for clean samples work while they last", GOOD),
            (r"autism: \ a fraud retracted, \ a method failed, \ priors as a trade-off, \ more diagnoses", SYMP),
            (r"ADHD: \ age within a class, \ and stimulants that help in the short term", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 41, \ in eleven lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part forty-one in eleven lines. <bookmark mark='a'/> The hollow mask needs a strong prior, and many "
            "people with schizophrenia aren't fooled. Schizophrenia has positive, negative and cognitive symptoms, "
            "and a course that varies widely. Antipsychotics block dopamine D2 receptors, and work on positive "
            "symptoms, at a cost. Aberrant salience: dopamine out of step makes the irrelevant feel meant. "
            "Hallucinations as strong priors: influential, and contested. Heritability near eighty percent, from "
            "hundreds of variants, and blaming mothers did harm. Addiction draws on reward, tolerance, wanting "
            "without liking, habit and steep discounting. A drug's surge that can't be learned away, computed, and a "
            "prediction that failed. Setting matters, and vouchers for clean samples work while they last. Autism: a "
            "fraud retracted, a method failed, priors as a trade-off, and more diagnoses. And ADHD: age within a "
            "class, and stimulants that help in the short term."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=40.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"Gaussian priors on a hollow face, \ salience, \ conditioned tones and a drug's endless prediction error",
             STATUS_COLOR["replicated"]),
            (r"drug trials, \ vouchers, \ blind tests of facilitated typing, \ and a cohort of 657{,}461",
             STATUS_COLOR["replicated"]),
            (r"hallucinations are reports, \ and the models of them are fitted to what people say they heard",
             STATUS_COLOR["contested"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "Gaussian priors on a hollow face, salience, conditioned tones, and a drug's endless prediction error. "
            "<bookmark mark='b'/> The second, that the mind can't be experimented on, met drug trials, vouchers, blind "
            "tests of facilitated typing, and a cohort of more than six hundred and fifty thousand children. "
            "<bookmark mark='c'/> And the third, about introspection: hallucinations are reports, and the models of "
            "them are fitted to what people say they heard. Amber."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"does therapy work, \ and which?", [42]),
            (r"the efficient, \ predictive brain: \ precision properly", [58]),
            (r"computational psychiatry: \ the dials in one person", [59]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Whether therapy works, and which, is next, in Part 42. "
            "Precision, properly, is Part 58's efficient, predictive brain. And measuring the dials in one person is "
            "Part 59's computational psychiatry."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One computes the hollow "
            "mask. One finds the best strength for a prior. One bounds the value of a drug in Redish's model. One "
            "finds a preference reversal. One computes aberrant salience. One works out how much of an ADHD "
            "diagnosis rate is relative age. And the last, with the star, asks you to design a study that could tell "
            "a trait from a state. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"U. Frith, \ \emph{Autism: Explaining the Enigma} (2nd edition, \ 2003)",
             r"R. L. Gregory, \ \emph{Eye and Brain} (5th edition, \ 1997)",
             r"D. H. Barlow, \ V. M. Durand \& S. G. Hofmann, \ \emph{Abnormal Psychology} (textbook)"],
            [r"H. M. Emrich (1989); \ D. Dima et al.\ (2009); \ P. Sterzer et al.\ (2018)",
             r"S. Kapur (2003); \ O. D. Howes \& S. Kapur (2009); \ A. R. Powers et al.\ (2017)",
             r"P. F. Sullivan et al.\ (2003); \ A. Sekar et al.\ (2016); \ V. Trubetskoy et al.\ (2022)",
             r"T. E. Robinson \& K. C. Berridge (1993); \ A. D. Redish (2004); \ L. N. Robins (1974)",
             r"S. T. Higgins et al.\ (1991); \ A. Hviid et al.\ (2019); \ E. Pellicano \& D. Burr (2012)",
             r"MTA Cooperative Group (1999); \ T. J. Layton et al.\ (2018)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Uta Frith's Autism: Explaining "
            "the Enigma is a clear account of the science; Richard Gregory's Eye and Brain is the classic on "
            "perception as hypothesis; and Barlow, Durand and Hofmann's textbook covers the conditions."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act X: \ when minds suffer", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 42", font_size=32, color=GREY_B),
                     label(r"Does Therapy Work?", font_size=36),
                     wrapped_label(r"How would anyone know whether talking helps?", 6.0, 26, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Act Ten closes with a question about the treatments themselves. <bookmark mark='a'/> This part used the "
            "series' models as a language for psychosis, addiction and development. <bookmark mark='b'/> The next "
            "asks how anyone could know whether talking helps: Eysenck's challenge, the method invented to answer "
            "it, and what works for whom. Part 42: does therapy work?"
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
