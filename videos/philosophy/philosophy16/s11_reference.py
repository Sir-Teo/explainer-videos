from __future__ import annotations

from videos.philosophy.philosophy16.common import *  # noqa: F403


class Reference(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"The reference class", r"Probability of what, \ among whom?", lit=(1866, 2007),
                            part=PART)
        with self.voiceover("Chapter ten. The reference class."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.bob()
        self.everyone()
        self.machines()

    def bob(self):
        head = label(r"Will Bob be alive in ten years?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sub = label(r"Bob: \ 60, \ smokes, \ runs every day \ (illustrative numbers)", font_size=21,
                    color=GREY_A).next_to(head, DOWN, buff=0.2)
        a = Circle(radius=1.9, color=NULLC, stroke_width=3, fill_opacity=0.06).move_to([-3.6, -0.8, 0])
        b = Circle(radius=1.4, color=SICK, stroke_width=3, fill_opacity=0.08).move_to([-4.3, -1.1, 0])
        c = Circle(radius=1.4, color=ALTC, stroke_width=3, fill_opacity=0.08).move_to([-2.9, -1.1, 0])
        la = label(r"60-year-olds", font_size=18, color=NULLC).next_to(a, UP, buff=0.05)
        lb = label(r"smokers", font_size=18, color=SICK).move_to([-5.0, -1.7, 0])
        lc = label(r"runners", font_size=18, color=ALTC).move_to([-2.2, -1.7, 0])
        bob = Dot([-3.6, -1.0, 0], radius=0.09, color=GOAL)
        bl = label(r"Bob", font_size=18, color=GOAL).next_to(bob, UP, buff=0.08)
        rows = stack([(r"60-year-olds: \ 90\% alive in ten years", NULLC),
                      (r"60-year-old smokers: \ 80\%", SICK),
                      (r"60-year-old runners: \ 95\%", ALTC),
                      (r"60-year-old smoking runners: \ 12 people on record", GREY_B),
                      (r"which number is \textit{Bob's} probability?", GOAL)], font_size=22, aligned_edge=LEFT).move_to(
            [3.4, -0.6, 0])
        src = label(r"Venn \ (1866); \ Reichenbach: \ `the narrowest class with reliable statistics'", font_size=19,
                    color=HIST).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Frequencies belong to classes, but decisions are about individuals. <bookmark mark='a'/>Bob is sixty, "
            "smokes, and runs every day. Will he be alive in ten years? <bookmark mark='b'/>Among sixty-year-olds, "
            "say ninety percent are. <bookmark mark='c'/>Among sixty-year-old smokers, eighty. "
            "<bookmark mark='d'/>Among sixty-year-old runners, ninety-five. <bookmark mark='e'/>And the class that "
            "fits him best, smoking runners of sixty, has twelve people on record: too few to trust. "
            "<bookmark mark='f'/>Which number is Bob's probability? John Venn saw the problem in 1866. Reichenbach "
            "advised using the narrowest class for which reliable statistics exist, which is a rule of thumb, not "
            "an answer."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sub), FadeIn(bob), FadeIn(bl))
            vo.wait_until("b")
            self.play(Create(a), FadeIn(la), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(b), FadeIn(lb), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(Create(c), FadeIn(lc), FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(Indicate(bob, color=GOAL, scale_factor=2), FadeIn(rows[3]))
            vo.wait_until("f")
            self.play(FadeIn(rows[4]), FadeIn(src))
        self.clear_scene()

    def everyone(self):
        hc = history_card(2007, r"Alan Hájek", r"`The Reference Class Problem is Your Problem Too'", width=7.0,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = [
            (r"frequentism", r"a frequency is relative to a class: \ which class?", NULLC),
            (r"propensities", r"a chance is relative to a set-up: \ which description of the set-up?", ALTC),
            (r"the classical view", r"equal possibilities are relative to a partition: \ Bertrand, \ Part 13", FISH),
            (r"subjective Bayes", r"$P(\text{dies} \mid E)$ for \textit{which} $E$? \ `all your evidence' is itself a "
                                  r"class, \ and often unusable", BAYC),
            (r"Hájek", r"probability is fundamentally conditional: \ the reference class is part of the question",
             GOAL),
        ]
        g = rows_table(rows, top=1.0, gap=0.42, width=8.4, x_text=-2.4)
        with self.voiceover(
            "Alan Hájek argued in 2007 that the reference class problem is everyone's problem. "
            "<bookmark mark='a'/>For a frequentist, a frequency is relative to a class, and the question is which "
            "class. <bookmark mark='b'/>For a propensity theorist, a chance is relative to a chance set-up, and the "
            "question is which description of the set-up. <bookmark mark='c'/>For the classical view, equal "
            "possibilities are relative to a partition, as Bertrand's paradox showed in Part 13. "
            "<bookmark mark='d'/>And a subjective Bayesian must say which evidence to condition on. All of your "
            "evidence is the official answer, but it is itself a reference class, and usually too fine to use. "
            "<bookmark mark='e'/>Hájek's conclusion: probability is fundamentally conditional, and the reference "
            "class is part of the question, not a defect in the answer."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def machines(self):
        head = label(r"Reference classes in machines", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"insurance", r"the premium is the reference class: \ age, \ postcode, \ car, \ credit score", WHITE),
            (r"medicine", r"`patients like you': \ every feature added narrows the class and thins the data", ALTC),
            (r"risk scores", r"a recidivism score is a frequency in a class someone chose \ (COMPAS, \ 2016)", BAD),
            (r"machine learning", r"a model's features \textit{are} its reference class; \ choosing them is a "
                                  r"normative act", GOAL),
            (r"Part 41", r"when calibrated scores for different groups cannot all be fair at once", FISH),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.6, x_text=-2.6)
        with self.voiceover(
            "The problem is now built into machines. <bookmark mark='a'/>An insurance premium is a frequency in a "
            "reference class: drivers of your age, postcode and car. <bookmark mark='b'/>Personalized medicine "
            "asks what happens to patients like you, and every feature that makes the class more like you also "
            "makes it smaller. <bookmark mark='c'/>A recidivism risk score is a frequency in a class that someone "
            "chose, and the 2016 controversy over the COMPAS score was partly about which class. "
            "<bookmark mark='d'/>In machine learning, a model's features are its reference class, and choosing "
            "them is not only a statistical act but a normative one. <bookmark mark='e'/>Part 41 shows that "
            "calibrated scores for different groups cannot, in general, be fair in every sense at once."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
