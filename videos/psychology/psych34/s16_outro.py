from __future__ import annotations

from videos.psychology.psych34.common import *  # noqa: F403

PROBLEMS = [
    r"A crowd of $n$ has thresholds $0, 1, \dots, n - 1$. \ Show that everyone joins, \ and that raising one threshold "
    r"from 1 to 2 stops the cascade at one person. \ In general, \ show the cascade ends at the first $k$ with "
    r"$F(k) = k$, \ where $F(k)$ counts thresholds $\le k$.",
    r"In DeGroot's model $x_{t+1} = W x_t$ with $W$ row-stochastic and primitive. \ Show that everyone converges to "
    r"$\pi^{\top} x_0$, \ where $\pi^{\top} W = \pi^{\top}$, \ and that a doubly stochastic $W$ gives the plain mean.",
    r"Prove the diversity prediction identity: \ $(\bar x - \theta)^2 = \overline{(x_i - \theta)^2} - "
    r"\overline{(x_i - \bar x)^2}$.",
    r"Each of $N$ bystanders helps with probability $p/N$. \ Show that the chance someone helps tends to "
    r"$1 - e^{-p}$, \ and compare it with one person alone.",
    r"In a group of four, \ each member mentions what they know with probability 0.3. \ Compare the chance that a "
    r"fact known to all four comes up with one known to only one member.",
    r"In bounded confidence, \ show that the order of opinions never changes, \ and explain why roughly "
    r"$1/(2\varepsilon)$ camps remain from opinions spread evenly on $[0, 1]$.",
    r"$\star$ \ Design a study that could separate social influence from homophily in a network of friends, \ and "
    r"say what each part of your design rules out.",
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
                (r"1", r"Milgram's men who went to 450 volts", r"65\%, \ 26 of 40", AUTH),
                (r"2", r"critical answers with the wrong majority, \ 2023", r"33\%", CROWD),
                (r"3", r"filmed public fights where someone stepped in", r"about 9 in 10", GOOD),
                (r"4", r"how far off the middle guess of the ox was", r"under 1\%", MODEL)):
            rows.add(VGroup(label(n, font_size=30, color=c), wrapped_label(q, 7.0, 23, WHITE),
                            label(ans, font_size=28, color=c)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"the same species that obeys and conforms also steps in, \ and guesses well together",
                             12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> Milgram's men who went to four hundred and fifty volts: "
            "sixty-five percent, twenty-six of forty. Critical answers that went with the wrong majority in 2023: "
            "thirty-three percent. Filmed public fights in which someone stepped in: about nine in ten. And the "
            "middle guess of the ox: less than one percent off. <bookmark mark='b'/> The same species that obeys and "
            "conforms also steps in, and guesses well together."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=8.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"groups make norms, \ and people keep them alone: \ Sherif's light", CROWD),
            (r"a unanimous majority sways about a third of answers; \ one ally removes most of it", AUTH),
            (r"obedience is a dose-response curve, \ from 0\% to 92.5\%, \ set by the situation", AUTH),
            (r"the archives show doubt, \ coaching and improvised prods behind the famous numbers", P.ACCENT),
            (r"the prison study was coached, \ and the 38 witnesses were a parable", P.ACCENT),
            (r"each bystander helps less; \ a crowd still helps more often than not", GOOD),
            (r"audiences inhibit; \ groups loaf, \ polarize and under-share", CROWD),
            (r"persuasion runs through arguments or cues; \ norm messages depend on the place", PERSON),
            (r"thresholds and networks: \ one person can flip a crowd, \ and clustering spreads costly habits", MODEL),
            (r"crowds are wise when independent, \ and influence can destroy or improve that", GOOD),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        head = label(r"Part 34, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part thirty-four in ten lines. <bookmark mark='a'/> Groups make norms, and people keep them when they're "
            "alone again. A unanimous majority sways about a third of answers, and one ally removes most of that. "
            "Obedience is a dose-response curve, from none to ninety-two and a half percent, set by the situation. "
            "The archives show doubt, coaching and improvised prods behind the famous numbers. The prison study was "
            "coached, and the thirty-eight witnesses were a parable. Each bystander helps less, but a crowd still "
            "helps more often than not. Audiences inhibit, and groups loaf, polarize and under-share. Persuasion "
            "runs through arguments or through cues, and norm messages depend on the place. One person can flip a "
            "crowd, and clustered networks spread costly habits. And crowds are wise when they're independent; "
            "influence can destroy that, or, in the right network, improve it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=42.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"thresholds, \ averaging, \ contagion and the diversity identity: \ crowds written as mathematics",
             STATUS_COLOR["replicated"]),
            (r"randomized field experiments on bystanders, \ ratings and voting, \ some on millions", STATUS_COLOR["replicated"]),
            (r"Milgram's and Perry's questionnaires: \ what participants believed changed what they did", STATUS_COLOR["replicated, smaller"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "thresholds, averaging, contagion and the diversity identity: crowds written as mathematics. "
            "<bookmark mark='b'/> The second, that the mind can't be experimented on, met randomized field "
            "experiments on bystanders, ratings and voting, some of them on millions of people. "
            "<bookmark mark='c'/> And the third, about introspection. Milgram's own questionnaires, and Perry's "
            "reanalysis of them, showed that what people believed about the situation changed what they did. Asking "
            "them mattered: a lighter green."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"reading minds, \ your own included", [35]),
            (r"us and them: \ groups against groups", [36]),
            (r"cooperation, \ trust and punishment", [37]),
            (r"culture as social learning", [38]),
            (r"field experiments and nudges", [55]),
            (r"minds and machines", [60]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Reading minds, your own included, is next, in Part 35. "
            "Groups against groups are Part 36; cooperation, trust and punishment Part 37; and culture as social "
            "learning Part 38. Field experiments and nudges are Part 55, and minds and machines Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=8.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One solves Granovetter's "
            "cascade. One finds DeGroot's consensus. One proves the diversity identity. One asks whether a crowd of "
            "bystanders helps less than one person. One computes the hidden profile's arithmetic. One explains the "
            "camps of bounded confidence. And the last, with the star, asks you to design a study that could "
            "separate influence from homophily. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"S. Milgram, \emph{Obedience to Authority} (1974)",
             r"G. Perry, \emph{Behind the Shock Machine} (2012)",
             r"R. B. Cialdini, \emph{Influence} (1984)"],
            [r"S. E. Asch (1956); \ R. Bond \& P. B. Smith (1996); \ A. Franzen \& S. Mader (2023)",
             r"J. M. Burger (2009); \ N. Haslam, \ S. Loughnan \& G. Perry (2014); \ S. A. Haslam \& S. D. Reicher (2012)",
             r"S. Reicher \& S. A. Haslam (2006); \ T. Le Texier (2019)",
             r"J. M. Darley \& B. Latan\'e (1968); \ R. Manning, \ M. Levine \& A. Collins (2007); \ R. Philpot et al.\ (2020)",
             r"M. Granovetter (1978); \ M. H. DeGroot (1974); \ R. Hegselmann \& U. Krause (2002); \ D. Centola (2010)",
             r"F. Galton (1907); \ J. Lorenz et al.\ (2011); \ M. J. Salganik, \ P. S. Dodds \& D. J. Watts (2006)",
             r"C. R. Shalizi \& A. C. Thomas (2011); \ R. M. Bond et al.\ (2012); \ L. Muchnik et al.\ (2013)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Milgram's book is the study in "
            "his own words; Gina Perry's Behind the Shock Machine is what the archives show; and Cialdini's "
            "Influence is the field guide."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act IX \ begun: \ other people", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 35", font_size=32, color=GREY_B), label(r"Social Cognition", font_size=40),
                     wrapped_label(r"How do you read a mind, \ including your own?", 6.0, 28, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "That begins Act Nine, on other people. <bookmark mark='a'/> This part watched what people do around "
            "others. <bookmark mark='b'/> The next asks what they think about each other, and about themselves. "
            "Students paid one dollar to tell a lie came to believe it more than students paid twenty. Part 35: "
            "social cognition."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
