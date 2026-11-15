from __future__ import annotations

from videos.psychology.psych33.common import *  # noqa: F403

PROBLEMS = [
    r"Behaviour in situation $s$ is $T + u_s + e$, \ with variances $\sigma_T^2$ and $\sigma_e^2$ for the trait and "
    r"everything else. \ Show that averages over $k$ situations correlate $k\rho/(1 + (k - 1)\rho)$, \ with $\rho = "
    r"\sigma_T^2/(\sigma_T^2 + \sigma_e^2)$.",
    r"Two normal scores correlate $r$. \ Show that both fall on the same side of their medians with probability "
    r"$\tfrac12 + \arcsin(r)/\pi$, \ and give the chance of keeping all four letters of a type at $r = 0.8$.",
    r"Show that the correlation of a normal variable with its own median split is $\sqrt{2/\pi}$.",
    r"Two groups differ by $d$ on each of $p$ independent traits. \ Show that $D = d\sqrt{p}$, \ and find the overlap "
    r"$2\Phi(-D/2)$ for $d = 0.2$ and $p = 25$.",
    r"Reverse-key an item on a 1 to 6 scale. \ Why $7 - x$, \ and what happens to Cronbach's alpha if you forget?",
    r"In the binomial effect-size display, \ show that a correlation $r$ between two median splits gives success "
    r"rates $50 \pm 50r$ percent.",
    r"$\star$ \ Design a study that could tell whether conscientiousness causes longer life or merely marks it, \ and "
    r"say which confounders each part of your design removes.",
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
        a = load("acts")
        t = load("types")
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for n, q, ans, c in (
            (r"1", r"one situation predicting another", rf"about {a['single']:.2f}", PERSON),
            (r"2", r"sixteen situations predicting sixteen others", rf"about {a['observed'][-1]:.2f}", PERSON),
            (r"3", r"the same four-letter type on retest", rf"about {pct(t['all4'][1])}", O_),
            (r"4", r"the share of trait differences that come with genes", r"about 40\%", A_)):
            rows.add(VGroup(label(n, font_size=30, color=c), wrapped_label(q, 7.0, 23, WHITE),
                            label(ans, font_size=28, color=c)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"the gap between the first two numbers is the whole person-situation debate", 12.0, 22,
                             YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> One situation predicting another: about point three. "
            "Sixteen situations predicting sixteen others: close to point nine. The same four-letter type on "
            f"retest: about {spct(t['all4'][1])}. And the share of trait differences that come with genes: about "
            "forty percent. <bookmark mark='b'/> The gap between the first two numbers is the whole person-situation "
            "debate."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=8.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"17{,}953 words, \ reduced to five factors: \ and a sixth, \ honesty-humility, \ in many languages", YOU),
            (r"in 2{,}800 people's answers, \ parallel analysis keeps five, \ and every item finds its factor", E_),
            (r"types cut a single hump in two: \ unstable at the cut, \ and poorer predictors", O_),
            (r"one act predicts another at about .3, \ as Hartshorne, \ May and Mischel found", LOST),
            (r"many acts predict many others well: \ Spearman-Brown, \ Epstein, \ Fleeson", PERSON),
            (r"stability rises with age; \ on average we grow more agreeable, \ conscientious and calm", C_),
            (r"about 40\% of trait differences come with genes, \ little with the shared family", A_),
            (r"traits predict health, \ love and work modestly, \ and 87\% of 78 links replicated", GOOD),
            (r"Freud's themes survived; \ his specific theory and the inkblots did not", N_),
            (r"small sex differences that add up in many dimensions; \ and traits read from likes", MODEL),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        head = label(r"Part 33, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part thirty-three in ten lines. <bookmark mark='a'/> Seventeen thousand nine hundred and fifty-three "
            "words were reduced to five factors, with a sixth, honesty-humility, in many languages. In two thousand "
            "eight hundred people's answers, parallel analysis keeps five, and every item finds its factor. Types cut "
            "a single hump in two, and are unstable at the cut and poorer predictors. One act predicts another at "
            "about point three, as Hartshorne, May and Mischel found. Many acts predict many others well, by "
            "Spearman-Brown, as Epstein and Fleeson showed. Stability rises with age, and on average we grow more "
            "agreeable, conscientious and calm. About forty percent of trait differences come with genes, and little "
            "with the shared family. Traits predict health, love and work modestly, and eighty-seven percent of "
            "seventy-eight links replicated. Freud's broad themes survived; his specific theory and the inkblots "
            "didn't. And small sex differences add up across many dimensions, while traits can be read from likes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=42.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"factor analysis, \ Spearman-Brown, \ the arcsine law and Mahalanobis's $D$: \ personality written as "
             r"mathematics", STATUS_COLOR["replicated"]),
            (r"randomized coaching that changed traits, \ and preregistered tests of 78 predictions", STATUS_COLOR["replicated"]),
            (r"self-reports agree with friends, \ with behaviour and with footprints: \ introspection, \ checked from "
             r"outside", STATUS_COLOR["replicated, smaller"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "factor analysis, the Spearman-Brown formula, the arcsine law and Mahalanobis's distance: personality "
            "written as mathematics. <bookmark mark='b'/> The second, that the mind can't be experimented on, met "
            "randomized coaching that changed traits, and preregistered tests of seventy-eight predictions. "
            "<bookmark mark='c'/> And the third, about introspection. Personality is mostly measured by asking "
            "people about themselves, but those answers agree with friends, with behaviour and with digital "
            "footprints. Introspection, checked from outside: a lighter green."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"situations that move people", [34]),
            (r"disorders as continua, \ like traits", [39]),
            (r"latent variables against networks", [44]),
            (r"items, \ responses and faking, \ modelled", [45]),
            (r"personality at work", [53]),
            (r"minds and machines", [60]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Situations that move people are next, in Part 34. "
            "Disorders as continua, like traits, are Part 39. Latent variables against networks are Part 44, and item response "
            "theory, which models items, responses and faking, Part 45. Personality at work is Part 53, and minds "
            "and machines Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=8.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=22)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One derives the "
            "aggregation curve. One derives the arcsine law for types. One finds what a median split keeps. One "
            "shows how Mahalanobis's distance grows with the number of traits. One asks why reverse-keying matters. "
            "One derives the binomial effect-size display. And the last, with the star, asks you to design a study "
            "that could tell whether conscientiousness causes a longer life or merely marks it. Pause here if you'd "
            "like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"D. C. Funder, \emph{The Personality Puzzle}",
             r"W. Mischel, \emph{Personality and Assessment} (1968)",
             r"G. W. Allport \& H. S. Odbert, \emph{Trait-Names: A Psycho-Lexical Study} (1936)"],
            [r"E. C. Tupes \& R. E. Christal (1961); \ L. R. Goldberg (1990); \ R. R. McCrae \& P. T. Costa (1997)",
             r"S. Epstein (1979); \ D. C. Funder \& D. J. Ozer (1983); \ W. Fleeson (2001)",
             r"B. W. Roberts \& W. F. DelVecchio (2000); \ B. W. Roberts et al.\ (2006, \ 2007)",
             r"C. J. Soto (2019); \ M. Stieger et al.\ (2021)",
             r"J. S. Hyde (2005); \ M. Del Giudice et al.\ (2012)",
             r"M. Kosinski et al.\ (2013); \ W. Youyou et al.\ (2015); \ S. C. Matz et al.\ (2017)",
             r"S. O. Lilienfeld, \ J. M. Wood \& H. N. Garb (2000)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. David Funder's textbook, The "
            "Personality Puzzle, is the clearest guide to the field and to the person-situation debate; Mischel's "
            "1968 book is the challenge itself; and Allport and Odbert's monograph is where the words came from."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act VIII \ complete: \ how people differ", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 34", font_size=32, color=GREY_B), label(r"Social Influence", font_size=40),
                     wrapped_label(r"How much of what you do is decided by who is in the room?", 6.0, 28, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "That completes Act Eight, on how people differ. <bookmark mark='a'/> Act Nine is about other people. "
            "<bookmark mark='b'/> In the early 1960s, at Yale, Stanley Milgram had an experimenter tell ordinary "
            "people to give another person electric shocks. Chapter six measured how large situations are. Part 34 "
            "tells that study as it was run, as it was retold, and as the archives now show it: social influence."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
