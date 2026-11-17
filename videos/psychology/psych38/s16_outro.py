from __future__ import annotations

from videos.psychology.psych38.common import *  # noqa: F403

PROBLEMS = [
    r"Conformist transmission: \ show that $p + D p (1-p)(2p-1)$ is the expected share after one generation when "
    r"learners sample three models and adopt a variant held by two of them with chance $2/3 + D/3$ and by one with "
    r"chance $1/3 - D/3$. \ Find the fixed points and their stability.",
    r"Henrich's model: \ the best of $N$ independent Gumbel$(\mu, \beta)$ draws has mean $\mu + \beta(\gamma + \ln N)$. "
    r"\ Find the critical $N^*$ for $\alpha = 4.5$ and $\beta = 1$.",
    r"Two cultures differ by $0.8$ SD on a trait, \ and everyone rates themselves relative to their own culture's "
    r"mean. \ What is the expected difference in mean ratings? \ Name two designs that recover the true difference.",
    r"In Psyche's trolley model, \ $\Pr(\text{accept}) = \sigma(c_k + \ell_j)$. \ Show that if $c_1 > c_2 > c_3$, "
    r"\ every country has the same order of acceptance, \ whatever its level $\ell_j$.",
    r"A replication tests 567 infants; \ the original effect was 26 of 28. \ If the true preference were 0.6, \ "
    r"what is the chance of observing 49\% or fewer? \ Use the normal approximation.",
    r"Arnett's numbers: \ 96\% of samples come from countries with 12\% of the world's population. \ How many times "
    r"over-represented is a person in those countries, \ relative to everyone else?",
    r"$\star$ \ Write a constraints-on-generality statement for one finding in this series, \ and design the "
    r"smallest study that could test it.",
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
                (r"1", r"share who would push the man, \ average of 42 countries", r"51\%", PERSON),
                (r"2", r"countries where Switch $>$ Loop $>$ Footbridge", r"all 42", WEST),
                (r"3", r"babies who chose the helper in ManyBabies 4", r"49\%", GOOD),
                (r"4", r"how often effects differed between WEIRD and less WEIRD samples", r"rarely", WORLD)):
            rows.add(VGroup(label(n, font_size=30, color=c), wrapped_label(q, 6.8, 23, WHITE),
                            label(ans, font_size=28, color=c)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"the structure travels more often than the level, \ and the questionnaires less often "
                             r"than either", 12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> The share who would push the man, averaged over forty-"
            "two countries: fifty-one percent. The countries where Switch beat Loop and Loop beat Footbridge: all "
            "forty-two. The babies who chose the helper in the largest replication: forty-nine percent, chance. And "
            "how often effects differed between WEIRD and less WEIRD samples: rarely. <bookmark mark='b'/> The "
            "structure of a judgment travels more often than its level, and the questionnaires less often than "
            "either."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=8.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"psychology's samples are mostly WEIRD, \ and still are", PERSON),
            (r"even the Müller-Lyer illusion varies; \ why is argued", WEST),
            (r"independent and interdependent selves: \ the idea is strong, \ the scales are weak", WORLD),
            (r"rice, \ mobility and kinship: \ theories of where differences come from", GOOD),
            (r"rating yourself against your neighbours can hide a real difference", MODEL),
            (r"conformity makes groups uniform inside and different from each other", MODEL),
            (r"prestige spreads useless traits along with useful ones; \ children copy faithfully", WORLD),
            (r"intuition comes first in moral judgment, \ more often than reasoning", PERSON),
            (r"Switch, \ Loop, \ Footbridge: \ the same order in 42 countries, \ different levels", WEST),
            (r"babies' preference for helpers did not replicate at scale", AUTH),
            (r"findings travel or fail mostly by the finding, \ not by the place: \ say where yours should hold",
             YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 38, \ in eleven lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part thirty-eight in eleven lines. <bookmark mark='a'/> Psychology's samples are mostly WEIRD, and "
            "still are. Even the Müller-Lyer illusion varies, and why is argued. Independent and interdependent "
            "selves: the idea is strong, and the scales are weak. Rice, mobility and kinship are theories of where "
            "differences come from. Rating yourself against your neighbours can hide a real difference. Conformity "
            "makes groups uniform inside and different from each other. Prestige spreads useless traits along with "
            "useful ones, and children copy faithfully. Intuition comes first in moral judgment, more often than "
            "reasoning. Switch, Loop and Footbridge keep the same order in forty-two countries, at different levels. "
            "Babies' preference for helpers didn't replicate at scale. And findings travel or fail mostly by the "
            "finding, not by the place, so say where yours should hold."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=40.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"the mathematics of conformity, \ prestige and population size, \ and a model of moral judgment",
             STATUS_COLOR["replicated"]),
            (r"one protocol run in dozens of countries at once", STATUS_COLOR["replicated"]),
            (r"self-reports compared across cultures can hide what they claim to measure",
             STATUS_COLOR["contested"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "the mathematics of conformity, prestige and population size, and a model of moral judgment. "
            "<bookmark mark='b'/> The second, that the mind can't be experimented on, met one protocol run in dozens "
            "of countries at once. <bookmark mark='c'/> And the third, about introspection: self-reports compared "
            "across cultures can hide the very thing they claim to measure. Amber."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"culture in diagnosis: \ idioms of distress", [39]),
            (r"measurement invariance, \ tested", [44]),
            (r"surveys and scaling across countries", [46]),
            (r"machines' values, \ and whose they are", [60]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Culture in diagnosis, and idioms of distress, open Act Ten "
            "in Part 39. Measurement invariance is tested properly in Part 44. Surveys and scaling across countries "
            "are Part 46. And machines' values, and whose they are, return in Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=7.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One derives the "
            "conformist step and its fixed points. One finds Henrich's critical population. One works the "
            "reference-group effect. One proves that the trolley model keeps the order everywhere. One asks how "
            "surprising the infant replication would be if the effect were real. One turns Arnett's numbers into "
            "over-representation. And the last, with the star, asks you to write a constraints-on-generality "
            "statement, and design the study to test it. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"J. Henrich, \ \emph{The WEIRDest People in the World} (2020)",
             r"R. Boyd \& P. J. Richerson, \ \emph{Culture and the Evolutionary Process} (1985)",
             r"R. E. Nisbett, \ \emph{The Geography of Thought} (2003)"],
            [r"J. J. Arnett (2008); \ J. Henrich, \ S. J. Heine \& A. Norenzayan (2010); \ A. G. Thalmayer et al.\ "
             r"(2021)",
             r"M. H. Segall, \ D. T. Campbell \& M. J. Herskovits (1966); \ T. Gandhi et al.\ (2015)",
             r"H. R. Markus \& S. Kitayama (1991); \ T. Masuda \& R. E. Nisbett (2001); \ D. Oyserman et al.\ (2002)",
             r"T. Talhelm et al.\ (2014); \ R. Thomson et al.\ (2018); \ J. F. Schulz et al.\ (2019); \ S. J. Heine "
             r"et al.\ (2002)",
             r"J. Henrich (2004); \ V. Horner \& A. Whiten (2005); \ K. Vaesen et al.\ (2016)",
             r"J. Haidt (2001); \ J. D. Greene et al.\ (2001); \ J. Graham, \ J. Haidt \& B. A. Nosek (2009)",
             r"E. Awad et al.\ (2018, \ 2020); \ B. Bago et al.\ (2022); \ J. K. Hamlin et al.\ (2007); \ K. Lucca "
             r"et al.\ (2025)",
             r"R. A. Klein et al.\ (2018); \ D. J. Simons, \ Y. Shoda \& D. S. Lindsay (2017); \ M. Muthukrishna et "
             r"al.\ (2020)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Henrich's The WEIRDest People "
            "in the World is the long version of the historical argument; Boyd and Richerson's book is the "
            "mathematics of cultural evolution; and Nisbett's The Geography of Thought is the case for analytic and "
            "holistic thinking, to be read alongside this part's cautions."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act IX: \ other people, \ complete", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Act X \ \textperiodcentered\ \ Part 39", font_size=32, color=GREY_B),
                     label(r"What Is a Disorder?", font_size=40),
                     wrapped_label(r"Where is the line between suffering and illness, \ and who draws it?", 6.0, 26,
                                   GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "That completes Act Nine, other people. <bookmark mark='a'/> We've seen minds shaped by crowds, by "
            "groups, by bargains and by whole cultures. <bookmark mark='b'/> Act Ten turns to minds that suffer. It "
            "begins with a question that sounds simple: where is the line between suffering and illness, and who "
            "draws it? Part 39: what is a disorder?"
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
