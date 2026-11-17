from __future__ import annotations

from videos.psychology.psych35.common import *  # noqa: F403

PROBLEMS = [
    r"Kelley's cube: \ a person reacts (1) or not (0) to an entity on an occasion, \ with 2 people, \ 2 entities and "
    r"2 occasions. \ If only person 1 ever reacts, \ show that the person main effect carries all the variance, \ and "
    r"say which of consensus, \ distinctiveness and consistency are high and which low.",
    r"An observer thinks a writer's attitude is pro with probability $1/2$. \ A pro writer writes a pro essay; \ an "
    r"anti writer does too if assigned, \ which the observer thinks happened with probability $\pi$. \ Show "
    r"$P(\text{pro} \mid \text{pro essay}) = 1/(1 + \pi)$, \ and explain why it exceeds $1/2$ unless $\pi = 1$.",
    r"Skill $X$ and self-estimate $Y$ are on a scale with mean 50 and equal spreads, \ with "
    r"$E[Y \mid X] = 50 + s + \rho\,(X - 50)$. \ Show that the bottom quarter's mean estimate is "
    r"$50 + s + \rho\,(E[X \mid \text{bottom}] - 50)$, \ and draw the graph for $\rho = 0$.",
    r"Dawes's false consensus: \ the share $p$ who agree is uniform on $[0, 1]$, \ and you agree. \ Show your posterior "
    r"mean for $p$ is $2/3$, \ and compare it with Ross, \ Greene and House's estimates.",
    r"A study estimates $d$ with standard error $\sigma$ and reports it only if $\hat d / \sigma > 1.96$. \ For a true "
    r"$d = 0.2$ and $\sigma = 0.31$, \ show that the expected reported $\hat d$ is about four times $d$.",
    r"In a gridworld, \ an agent's step is equally likely under goals A and C, \ and impossible under B. \ Show "
    r"that the posterior ratio of A to C does not change, \ and that B drops to zero.",
    r"$\star$ \ Design an experiment that separates dissonance from self-perception, \ and say which result would "
    r"favour each.",
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
                (r"1", r"places that refused the couple in person", r"1 of 251", GOOD),
                (r"2", r"letter replies that said they would refuse", r"92\%", AUTH),
                (r"3", r"where the bottom quarter placed themselves", r"about the 62nd percentile", PERSON),
                (r"4", r"US students above the median driver, \ by their own rating", r"93\%", CROWD)):
            rows.add(VGroup(label(n, font_size=30, color=c), wrapped_label(q, 6.6, 23, WHITE),
                            label(ans, font_size=28, color=c)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"what people say about others, \ and about themselves, \ is a guess built from a theory",
                             12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> Places that refused the Chinese couple in person: one, of "
            "two hundred and fifty-one. Letter replies that said they would refuse: ninety-two percent. Where the "
            "bottom quarter placed themselves: about the sixty-second percentile. And American students who rated "
            "themselves above the median driver: ninety-three percent. <bookmark mark='b'/> What people say about "
            "others, and about themselves, is a guess built from a theory."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=8.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"we see minds in moving shapes, \ automatically", PERSON),
            (r"Kelley's cube: \ attribution is an analysis of variance", MODEL),
            (r"the correspondence bias replicates, \ and may be a rational bet", CROWD),
            (r"self-perception rivals dissonance; \ the 39-lab test found no effect of choice", AUTH),
            (r"attitudes predict acts that match them in kind", GOOD),
            (r"almost everyone is above average; \ much of Dunning-Kruger's graph is regression", PERSON),
            (r"faces are judged in a tenth of a second, \ and thin slices carry information", CROWD),
            (r"behavioural priming and power posing's hormones failed; \ semantic priming holds", AUTH),
            (r"a small significant study has overestimated: \ the winner's curse", MODEL),
            (r"mind reading is inverse planning: \ Bayes with a rational planner inside", MODEL),
            (r"we often explain ourselves as observers would", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 35, \ in eleven lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part thirty-five in eleven lines. <bookmark mark='a'/> We see minds in moving shapes, automatically. "
            "Kelley's cube makes attribution an analysis of variance. The correspondence bias replicates, and may be "
            "a rational bet. Self-perception rivals dissonance, and the test in thirty-nine laboratories found no "
            "effect of choice. Attitudes predict the acts that match them in kind. Almost everyone is above "
            "average, and much of the Dunning-Kruger graph is regression to the mean. Faces are judged in a tenth "
            "of a second, and thin slices of behaviour carry real information. Behavioural priming and power "
            "posing's hormones failed, while semantic priming holds. A small study that reaches significance has "
            "overestimated: the winner's curse. Mind reading is inverse planning, Bayes' rule with a rational "
            "planner inside. And we often explain ourselves the way an observer would."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=42.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"Kelley's analysis of variance, \ a Bayesian observer and an inverse planner: \ social inference "
             r"written as mathematics", STATUS_COLOR["replicated"]),
            (r"one dissonance study rerun in 39 laboratories, \ and two famous effects tested and failed",
             STATUS_COLOR["replicated"]),
            (r"Kant's doubt in a new form: \ people's accounts of why they acted are often theories, \ not "
             r"observations", STATUS_COLOR["contested"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "Kelley's analysis of variance, a Bayesian observer and an inverse planner: social inference written as "
            "mathematics. <bookmark mark='b'/> The second, that the mind can't be experimented on, met one "
            "dissonance study rerun in thirty-nine laboratories, and two famous effects tested until they failed. "
            "<bookmark mark='c'/> And the third, about introspection. Here Kant's doubt returns in a new form. "
            "People's accounts of why they acted are often theories, not observations. Amber."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"us and them: \ groups, \ stereotypes and bias scores", [36]),
            (r"cooperation and trust", [37]),
            (r"attribution across cultures", [38]),
            (r"interviews and performance reviews", [53]),
            (r"theory of mind in machines", [60]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Groups, stereotypes and bias scores are next, in Part 36. "
            "Cooperation and trust are Part 37, and attribution across cultures Part 38. Interviews and performance "
            "reviews are measured in Part 53, and theory of mind in machines is Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=8.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One runs Kelley's cube. "
            "One builds the rational observer of the essays. One derives the Dunning-Kruger graph from regression. "
            "One finds Dawes's two thirds in false consensus. One computes the winner's curse. One updates an "
            "inverse planner by hand. And the last, with the star, asks you to design the experiment that separates "
            "dissonance from self-perception. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"S. T. Fiske \& S. E. Taylor, \emph{Social Cognition}",
             r"L. Festinger, \emph{A Theory of Cognitive Dissonance} (1957)",
             r"T. D. Wilson, \emph{Strangers to Ourselves} (2002)"],
            [r"F. Heider \& M. Simmel (1944); \ H. H. Kelley (1973); \ E. E. Jones \& V. A. Harris (1967)",
             r"L. Festinger \& J. M. Carlsmith (1959); \ D. J. Bem (1967); \ D. C. Vaidis et al.\ (2024)",
             r"R. T. LaPiere (1934); \ I. Ajzen (1991); \ O. Svenson (1981); \ J. Kruger \& D. Dunning (1999)",
             r"J. Willis \& A. Todorov (2006); \ N. Ambady \& R. Rosenthal (1993)",
             r"J. A. Bargh, \ M. Chen \& L. Burrows (1996); \ S. Doyen et al.\ (2012); \ E. Ranehill et al.\ (2015)",
             r"R. Saxe \& N. Kanwisher (2003); \ C. L. Baker, \ R. Saxe \& J. B. Tenenbaum (2009)",
             r"R. E. Nisbett \& T. D. Wilson (1977); \ P. Johansson et al.\ (2005); \ M. Kosinski (2024)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Fiske and Taylor's Social "
            "Cognition is the field's textbook; Festinger's book is where dissonance began; and Timothy Wilson's "
            "Strangers to Ourselves is chapter eleven at book length."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act IX: \ other people", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 36", font_size=32, color=GREY_B), label(r"Us and Them", font_size=40),
                     wrapped_label(r"How little does it take to make a group?", 6.0, 28, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Act Nine goes on. <bookmark mark='a'/> This part asked how we read single minds. "
            "<bookmark mark='b'/> The next asks what happens when we read people as members of groups. Schoolboys "
            "divided by a meaningless preference between two painters favoured their own group at once. Part 36: "
            "us and them."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
