from __future__ import annotations

from videos.philosophy.philosophy15.common import *  # noqa: F403


class Merging(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"When opinions merge", r"Do priors wash out?", lit=(1962,), part=PART)
        with self.voiceover("Chapter nine. When opinions merge."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.merge()
        self.theorem()
        self.limits()

    def merge(self):
        d = load("merging")
        head = label(r"Two Bayesians, \ one coin", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, d["n"], 100], y_range=[0, 1, 0.25], x_length=8.4, y_length=4.2, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 18}).move_to([-1.6, -0.7, 0])
        xl = label(r"tosses", font_size=19, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"P(next is heads)", font_size=19, color=GREY_B).next_to(ax.y_axis, UP, buff=0.1)
        truth = DashedLine(ax.c2p(0, d["truth"]), ax.c2p(d["n"], d["truth"]), color=OK, stroke_width=2)
        ca = series_plot(ax, d["a"], A_C, xs=d["idx"])
        cb = series_plot(ax, d["b"], B_C, xs=d["idx"])
        leg = stack([(r"Ann: \ prior Beta(1, 9): \ `heads is rare'", A_C),
                     (r"Bo: \ prior Beta(9, 1): \ `heads is common'", B_C),
                     (r"dashed: \ the true chance, \ 0.7", OK)], font_size=20,
                    aligned_edge=LEFT).move_to([4.6, 1.3, 0])
        gap0, gapN = d["gap"][0], d["gap"][-1]
        gaps = stack([(r"gap at the start: \ " + f"{gap0:.2f}", WHITE),
                      (r"after " + str(d["n"]) + r" tosses: \ " + f"{gapN:.3f}", GOAL)], font_size=21,
                     aligned_edge=LEFT).next_to(leg, DOWN, buff=0.5)
        with self.voiceover(
            "Bayesians have their own answer to the worry that priors are arbitrary: in the long run, they wash out. "
            "<bookmark mark='a'/>Ann thinks heads is rare; her prior on the coin's chance is a Beta one, nine. Bo "
            "thinks heads is common: Beta nine, one. At the start their predictions differ by point eight. "
            "<bookmark mark='b'/>The coin's true chance is point seven. <bookmark mark='c'/>They watch the same "
            "tosses and conditionalize. <bookmark mark='d'/>Both predictions move toward the truth, and toward each "
            "other. After four hundred tosses they differ by two hundredths."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(yl), FadeIn(leg[:2]), FadeIn(gaps[0]))
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(leg[2]))
            vo.wait_until("c")
            self.play(Create(ca), Create(cb), run_time=4)
            vo.wait_until("d")
            self.play(FadeIn(gaps[1]))
        self.clear_scene()

    def theorem(self):
        d = load("merging")
        hc = history_card(1962, r"David Blackwell \ and Lester Dubins", r"`Merging of Opinions with Increasing "
                          r"Information'", width=7.0, color=HIST).to_corner(UL, buff=0.35)
        thm = VGroup(label(r"if $P \ll Q$ \ and \ $Q \ll P$ \ \ (each gives positive probability where the other "
                           r"does)", font_size=21, color=WHITE),
                     MathTex(r"\sup_{A}\ \big| P(A \mid x_1, \dots, x_n) - Q(A \mid x_1, \dots, x_n) \big| \ "
                             r"\xrightarrow{\ n \to \infty\ }\ 0 \quad \text{almost surely}", font_size=32,
                             color=FUT)).arrange(DOWN, buff=0.25).next_to(hc, DOWN, buff=0.4).set_x(0)
        ax = Axes(x_range=[0, d["n"], 100], y_range=[0, 1, 0.5], x_length=5.4, y_length=2.6, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 16}).move_to([-3.5, -2.0, 0])
        truth = DashedLine(ax.c2p(0, d["truth"]), ax.c2p(d["n"], d["truth"]), color=OK, stroke_width=2)
        cc = series_plot(ax, d["c"], BAD, xs=d["idx"])
        side = stack([(r"Cy: \ prior gives \textit{zero} to every chance above $\tfrac12$", BAD),
                      (r"stuck below 0.5 \ forever: \ " + f"{d['c'][-1]:.3f}" + r" after " + str(d["n"]), BAD),
                      (r"the condition fails: \ no merging, \ no learning", GREY_A),
                      (r"Cromwell's rule \ (Lindley): \ never give probability 0 \ to what might be true",
                       GOAL)], font_size=20, aligned_edge=LEFT, width=6.2).move_to([3.4, -1.9, 0])
        with self.voiceover(
            "This is a theorem, due to David Blackwell and Lester Dubins in 1962. <bookmark mark='a'/>If two "
            "priors agree about what is possible, each giving positive probability wherever the other does, then "
            "with probability one their conditional probabilities, for every event at once, converge as the data "
            "grow. <bookmark mark='b'/>The condition matters. Cy's prior gives probability zero to every chance above "
            "one half. <bookmark mark='c'/>The data cannot revive what the prior has killed: Cy's prediction creeps "
            "up toward one half and stops, forever wrong. <bookmark mark='d'/>Dennis Lindley called the moral "
            "Cromwell's rule, after Cromwell's plea to the Church of Scotland: I beseech you, think it possible you "
            "may be mistaken. Never give probability zero to anything that might be true."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(thm[0]), Write(thm[1]))
            vo.wait_until("b")
            self.play(FadeIn(ax), Create(truth), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Create(cc), run_time=3)
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def limits(self):
        head = label(r"What merging does not give", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([
            (r"agreement, \ not truth: \ two priors can merge on a falsehood \ (if both rule out the truth)", WHITE),
            (r"the long run: \ no bound on how long \ unless the priors are close", WHITE),
            (r"infinitely many hypotheses: \ consistency can fail \ (Diaconis and Freedman, \ 1986)", WHITE),
            (r"and it assumes the data come from one fixed process", WHITE),
            (r"Doob \ (1949): \ each Bayesian is \textit{sure} it will converge to the truth", GOAL),
            (r"Belot \ (2013): \ that certainty is a kind of arrogance about the world", BAD),
        ], font_size=23, buff=0.35, aligned_edge=LEFT).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Merging is a real comfort, but a limited one. <bookmark mark='a'/>It gives agreement, not truth: two "
            "people who rule out the same truth can merge on the same mistake. <bookmark mark='b'/>It is about the "
            "long run, with no bound on how long unless the priors were close to begin with. "
            "<bookmark mark='c'/>With infinitely many hypotheses, Persi Diaconis and David Freedman showed in 1986 "
            "that a Bayesian can fail to converge at all. <bookmark mark='d'/>And it assumes one fixed process "
            "producing the data. <bookmark mark='e'/>Joseph Doob proved that every Bayesian is certain, by her own "
            "lights, to converge on the truth. <bookmark mark='f'/>Gordon Belot argued in 2013 that this certainty "
            "is a defect: a prior that is sure it will learn has decided in advance that the world is learnable."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()
