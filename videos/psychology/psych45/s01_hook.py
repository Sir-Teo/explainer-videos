from __future__ import annotations

from videos.psychology.psych45.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.two_forms()
        self.rasch()
        self.question()
        self.objectives()

    def two_forms(self):
        d = load("classical")
        head = heading(r"Different questions, \ one scale?")
        A = axes([0.3, 2.7], [0, 10], x_length=4.4, y_length=3.2, xticks=None, yticks=[0, 5, 10],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"expected score out of 10", center=[-3.9, 0.3, 0], font_size=14)
        b = bars(A.ax, [1, 2], [d["exp_easy"], d["exp_hard"]], [GOOD, AUTH], width=0.6)
        names = VGroup(label(r"easy form", font_size=17, color=GOOD).next_to(A.ax.c2p(1, 0), DOWN, buff=0.15),
                       label(r"hard form", font_size=17, color=AUTH).next_to(A.ax.c2p(2, 0), DOWN, buff=0.15))
        vals = VGroup(*[label(f"{v:.1f}", font_size=20, color=c).next_to(bb, UP, buff=0.08)
                        for v, c, bb in zip((d["exp_easy"], d["exp_hard"]), (GOOD, AUTH), b)])
        rows = rows_of([
            (r"two pupils of exactly the same ability; \ one takes an easy form of a reading test, \ the other a hard "
             r"one, \ with no items in common", WHITE),
            (rf"expected scores: \ {d['exp_easy']:.1f} and {d['exp_hard']:.1f} out of 10", PERSON),
            (r"a score says how a person did on these items; \ it cannot say how they would do on others", AUTH),
            (r"the question for this part: \ can people who took different questions be put on one scale?", YOU),
        ], 6.0, 21, 0.42).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{irt.prob}, \ two simulated forms")
        with self.voiceover(
            "Two pupils of exactly the same ability take a reading test. <bookmark mark='a'/> One gets an easy form, "
            "the other a hard one, with no items in common. <bookmark mark='b'/> Their expected scores are about eight "
            "out of ten, and about three. <bookmark mark='c'/> A score says how a person did on these items. It "
            "can't say how they'd do on others. <bookmark mark='d'/> So the question for this part: can people who "
            "took different questions be put on one scale?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b), FadeIn(vals))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def rasch(self):
        head = heading(r"One person, \ one item")
        steps = VGroup()
        for yr, txt, c in (
                (r"1950s", r"in Copenhagen, \ the mathematician Georg Rasch is asked to compare children's reading "
                           r"across tests that share no items", PERSON),
                (r"1960", r"his book models the single encounter of one person with one item: \ the odds of success "
                          r"depend only on ability minus difficulty", MODEL),
                (r"then", r"the person and the item separate: \ abilities compared without the items, \ items "
                          r"compared without the people", GOOD),
                (r"since", r"adaptive tests, \ a statistical definition of an unfair item, \ national surveys, \ and "
                           r"tracking what a learner knows", YOU)):
            steps.add(VGroup(word_chip(yr, color=c, font_size=18, width=1.6), wrapped_label(txt, 10.0, 21, WHITE))
                      .arrange(RIGHT, buff=0.4))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.2, 0])
        tag = historical_tag(r"Rasch (1960)")
        with self.voiceover(
            "The answer came from Denmark. <bookmark mark='a'/> In the 1950s the mathematician Georg Rasch was asked to "
            "compare children's reading across tests that shared no items. <bookmark mark='b'/> In his 1960 book he "
            "modelled the single encounter of one person with one item. The odds of success depend only on ability "
            "minus difficulty. <bookmark mark='c'/> And then the person and the item separate. Abilities can be "
            "compared without the items, and items without the people. <bookmark mark='d'/> From that idea came "
            "adaptive tests, a statistical definition of an unfair item, national surveys of what students know, and "
            "ways to track what a learner knows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", steps):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ how do you measure with questions that differ?")
        rows = rows_of([
            (r"what classical scores cannot do, \ and the Rasch model that can", SYMP),
            (r"discrimination, \ guessing, \ and information", MODEL),
            (r"estimation, \ adaptive tests, \ and rating scales", PERSON),
            (r"fair items, \ linked forms, \ national surveys, \ and learning", GOOD),
        ], 12.4, 27, 0.48).move_to([0, -0.2, 0])
        with self.voiceover(
            "So this part asks how to measure with questions that differ from person to person. "
            "<bookmark mark='a'/> What classical scores can't do, and the Rasch model that can. <bookmark mark='b'/> "
            "Discrimination, guessing, and how much an item tells you. <bookmark mark='c'/> Estimation, adaptive "
            "tests, and rating scales. <bookmark mark='d'/> And fair items, linked forms, national surveys, and "
            "learning."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 45", font_size=34, color=GREY_B), label(r"Item Response Theory", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the Rasch model, \ and why the sum score is sufficient",
            r"two and three parameters, \ and item information",
            r"marginal maximum likelihood, \ and ability estimates",
            r"an adaptive test, \ built and compared with fixed forms",
            r"rating scales, \ unfair items and linked forms",
            r"plausible values, \ and tracking what a learner knows",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 45 of Psychology, Built: item response theory. <bookmark mark='a'/> We'll build the Rasch "
            "model and derive why the sum score is all you need. We'll add discrimination and guessing, and measure "
            "how much each item tells you. We'll estimate items by marginal maximum likelihood, on real test data. "
            "We'll build an adaptive test and compare it with fixed forms. We'll fit rating scales, find unfair items "
            "and link two forms. And we'll see how national surveys report a population, and how software tracks "
            "what a learner knows."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
