from __future__ import annotations

from videos.psychology.psych60.common import *  # noqa: F403

PROBLEMS = [
    r"A model scores 85\% on published items and 26\% on reworded twins with four options each. \ What do you "
    r"conclude?",
    r"Twelve models, \ each tested with 100 phrasings. \ What is the sample size for a claim about models?",
    r"Two models at 70\% and 73\%, \ 1,000 shared items, \ item scores correlated 0.5. \ Can you tell them apart?",
    r"An aid is right 80\% of the time, \ you 70\%. \ Your accuracy if you follow it half the time, \ at random?",
    r"Silicon respondents match a survey's mean but have half its SD. \ Which conclusions survive?",
    r"Screen time explains 0.4\% of the variance in well-being. \ Could it still matter? \ For whom?",
    r"$\star$ \ Design a randomized trial of a mental-health chatbot that would meet Part 42's standards.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.your_numbers()
        self.recap()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def your_numbers(self):
        c = load("contam")
        s = load("silicon")
        sp = load("spec")
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for n_, q, ans, col in (
                (r"1", r"the memorizer on reworded items", rf"{100 * c['memorizer'][1]:.0f}\%, \ chance", PERSON),
                (r"2", r"100 phrasings to one model", r"an interval for one model only", MODEL),
                (r"3", r"silicon spread against people's", rf"SD {s['silicon_sd']:.1f} against {s['human_sd']:.1f}",
                 AUTH),
                (r"4", r"variance explained by screen time", rf"about {100 * sp['median_r2']:.0f}\% in Psyche; \ at "
                                                             rf"most 0.4\% in real data", GOOD)):
            rows.add(VGroup(label(n_, font_size=30, color=col), wrapped_label(q, 5.6, 22, WHITE),
                            wrapped_label(ans, 5.4, 22, col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"each answer is one of psychology's old lessons, \ applied to a new kind of subject",
                             12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> The memorizer scored twenty-five percent on reworded "
            "items, which is chance. A hundred phrasings to one model give an interval for that one model only. "
            "Silicon respondents had a spread of zero point seven, against one point seven for people. And screen "
            "time explained about one percent of the variance in well-being in Psyche, and at most zero point four "
            "percent in real data. <bookmark mark='b'/> Each answer is one of psychology's old lessons, applied to a "
            "new kind of subject."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=12.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"AI began in psychology; \ now the debt runs both ways", WHITE),
            (r"networks predict brains; \ errors and controls test mechanism", MODEL),
            (r"classic items are contaminated; \ use new and perturbed ones", AUTH),
            (r"one model is a sample of one", AUTH),
            (r"machine theory of mind: \ contested", PERSON),
            (r"benchmarks are tests: \ validity, \ IRT, \ size", MODEL),
            (r"aversion and appreciation, \ by task", PERSON),
            (r"a dialogue durably moved beliefs; \ awaiting replication", GOOD),
            (r"chatbot care needs active controls and counted harms", CARE),
            (r"silicon samples shrink spread and erase minorities", AUTH),
            (r"screens: \ tiny associations, \ few experiments", SYMP),
            (r"machine behaviour needs psychology's methods", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 60, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part sixty in twelve lines. <bookmark mark='a'/> AI began in psychology, and now the debt runs both "
            "ways. Networks predict brains, and errors and controls test mechanism. Classic items are contaminated, "
            "so use new and perturbed ones. One model is a sample of one. Machine theory of mind is contested. "
            "Benchmarks are tests, with validity, item response theory and sample size. Aversion and appreciation "
            "depend on the task. A dialogue durably moved beliefs, and awaits replication. Chatbot care needs active "
            "controls and counted harms. Silicon samples shrink the spread and erase minorities. Screens show tiny "
            "associations, with few experiments. And machine behaviour needs psychology's methods."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=34.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"language models as research assistants and simulated participants", [61]),
            (r"theories written as code, \ and models of whole fields", [61]),
            (r"a dissertation with a registered analysis", [62]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Language models as research assistants and simulated "
            "participants, and theories written as code, are Part 61. And Part 62's dissertation has a registered "
            "analysis."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One reads a "
            "contamination test. One finds the sample size. One separates two models. One computes accuracy with an "
            "aid. One asks which conclusions survive a silicon sample. One asks whether a tiny association can "
            "matter. And the last, with the star, asks you to design a trial of a mental-health chatbot. Pause here "
            "if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"M. Mitchell, \ \emph{Artificial Intelligence: A Guide for Thinking Humans}",
             r"B. M. Lake et al.\ (2017)",
             r"I. Rahwan et al.\ (2019)"],
            [r"F. Rosenblatt (1958); \ J. Weizenbaum (1966); \ D. L. K. Yamins \& J. J. DiCarlo (2016)",
             r"M. Binz \& E. Schulz (2023); \ M. Kosinski (2023); \ T. Ullman (2023); \ J. W. A. Strachan et al.\ "
             r"(2024)",
             r"B. J. Dietvorst et al.\ (2015); \ J. M. Logg et al.\ (2019); \ H. M. Gray et al.\ (2007)",
             r"T. H. Costello et al.\ (2024); \ M. V. Heinz et al.\ (2025); \ L. P. Argyle et al.\ (2023)",
             r"A. Orben \& A. K. Przybylski (2019); \ H. Allcott et al.\ (2020); \ J. M. Twenge et al.\ (2018)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Melanie Mitchell's book is a "
            "clear introduction to what AI can and can't do; Lake and colleagues' paper sets out what human-like "
            "learning needs; and Rahwan and colleagues' paper proposes the science of machine behaviour."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act XIII: \ the frontier, \ three of five", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 61", font_size=32, color=GREY_B),
                     label(r"The Next Psychology", font_size=34),
                     wrapped_label(r"what would psychology look like if it were designed today?", 6.0, 24, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Three parts of the frontier are done. <bookmark mark='a'/> This one turned psychology's methods on "
            "machines, and on people living with them. <bookmark mark='b'/> The next turns them on psychology itself. "
            "If the field were designed today, with big teams, huge samples and theories written as code, what would "
            "it look like? Part 61: the next psychology."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
