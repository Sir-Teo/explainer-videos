from __future__ import annotations

import math

from videos.philosophy.philosophy16.common import *  # noqa: F403


def cup(milk_first: bool, size=0.32) -> VGroup:
    body = RoundedRectangle(width=size * 1.6, height=size * 1.4, corner_radius=0.06, stroke_color=GREY_B,
                            stroke_width=2, fill_color="#C9A27A" if milk_first else "#7A4E2D", fill_opacity=0.9)
    handle = Arc(radius=size * 0.35, start_angle=-PI / 2, angle=PI, color=GREY_B, stroke_width=2).next_to(
        body, RIGHT, buff=-0.02)
    return VGroup(body, handle)


class Schools(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Three schools", r"What does a statistical test tell us?", lit=(1925, 1933, 1939),
                            part=PART)
        with self.voiceover("Chapter one. Three schools."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.fisher()
        self.neyman()
        self.bayes()
        self.fiducial()
        self.coin()
        self.feud()

    def fisher(self):
        hc = history_card(1935, r"Ronald Fisher", r"\textit{The Design of Experiments}: \ the lady tasting tea",
                          width=7.0, color=HIST).to_corner(UL, buff=0.35)
        cups = VGroup(*[cup(m) for m in (1, 0, 0, 1, 0, 1, 1, 0)]).arrange(RIGHT, buff=0.35).next_to(
            hc, DOWN, buff=0.45).set_x(0)
        cl = label(r"8 cups: \ 4 milk first, \ 4 tea first; \ she must pick the 4 milk-first", font_size=21,
                   color=GREY_A).next_to(cups, DOWN, buff=0.2)
        eq = MathTex(r"P(\text{all 4 right} \mid \text{she is guessing}) = \frac{1}{\binom{8}{4}} = \frac{1}{70} "
                     r"\approx 0.014", font_size=34, color=FISH).next_to(cl, DOWN, buff=0.35)
        rows = stack([(r"the $p$-value: \ the chance, \ if the null is true, \ of a result at least this extreme", WHITE),
                      (r"small $p$: \ `either an exceptionally rare chance has occurred, \ or the theory is not true'",
                       FISH),
                      (r"a measure of evidence against \textit{one} hypothesis; \ no alternative needed", GREY_A)],
                     font_size=21).next_to(eq, DOWN, buff=0.35)
        with self.voiceover(
            "Ronald Fisher's founding example. <bookmark mark='a'/>A lady claims she can tell whether the milk or "
            "the tea was poured first. Fisher gives her eight cups, four of each, in random order, and she must pick "
            "the four with milk first. <bookmark mark='b'/>If she is merely guessing, the chance that she picks all "
            "four correctly is one in seventy, about point zero one four. <bookmark mark='c'/>That number is the "
            "p-value: the probability, if the null hypothesis is true, of a result at least as extreme as the one "
            "observed. <bookmark mark='d'/>When it is small, Fisher said, either an exceptionally rare chance has "
            "occurred, or the theory is not true. <bookmark mark='e'/>It measures evidence against a single "
            "hypothesis, and it needs no alternative."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cups], lag_ratio=0.1), FadeIn(cl))
            vo.wait_until("b")
            self.play(Write(eq))
            for mk, r in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def neyman(self):
        hc = history_card(1933, r"Jerzy Neyman \ and Egon Pearson", r"`On the Problem of the Most Efficient Tests'",
                          width=7.0, color=HIST).to_corner(UL, buff=0.35)
        ax = Axes(x_range=[-3.5, 6, 1], y_range=[0, 0.45, 0.1], x_length=9.0, y_length=2.8, tips=False,
                  axis_config={"color": GREY_C, "include_ticks": False}).move_to([-0.6, -1.7, 0])
        mu1, crit = 2.5, 1.645
        f0 = ax.plot(lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi), x_range=[-3.5, 6], color=NULLC)
        f1 = ax.plot(lambda x: math.exp(-(x - mu1) ** 2 / 2) / math.sqrt(2 * math.pi), x_range=[-3.5, 6], color=ALTC)
        a_area = ax.get_area(f0, x_range=[crit, 6], color=BAD, opacity=0.5)
        b_area = ax.get_area(f1, x_range=[-3.5, crit], color=NEYP, opacity=0.35)
        cl = DashedLine(ax.c2p(crit, 0), ax.c2p(crit, 0.44), color=WHITE, stroke_width=2)
        h0 = label(r"$H_0$", font_size=24, color=NULLC).move_to(ax.c2p(-1.6, 0.36))
        h1 = label(r"$H_1$", font_size=24, color=ALTC).move_to(ax.c2p(4.1, 0.36))
        rej = label(r"reject $H_0$", font_size=20, color=WHITE).next_to(cl, UP, buff=0.05).shift(RIGHT * 0.7)
        beta = 1 - (1 - (0.5 * (1 + math.erf((crit - mu1) / math.sqrt(2)))))
        side = stack([(r"$\alpha = 0.05$: \ wrongly rejecting $H_0$", BAD),
                      (rf"$\beta = {beta:.2f}$: \ wrongly keeping it; \ power $1 - \beta = {1 - beta:.2f}$", NEYP),
                      (r"the lemma: \ reject when $\dfrac{P(x \mid H_1)}{P(x \mid H_0)} > k$ \ is most powerful", GOAL),
                      (r"not evidence about \textit{this} case: \ a rule with known long-run error rates", GREY_A)],
                     font_size=20, aligned_edge=LEFT, width=6.0).move_to([3.8, 1.5, 0])
        with self.voiceover(
            "Jerzy Neyman and Egon Pearson rebuilt testing around decisions. <bookmark mark='a'/>There are two "
            "hypotheses, the null and an alternative, <bookmark mark='b'/>and a rule that rejects the null when the "
            "data fall beyond a cutoff. <bookmark mark='c'/>Two errors are possible. Rejecting a true null happens "
            "with probability alpha, fixed in advance at five percent. <bookmark mark='d'/>Keeping a false null "
            "happens with probability beta; one minus beta is the power. <bookmark mark='e'/>Their lemma of 1933 "
            "says which rule is best: reject when the likelihood ratio of the alternative to the null exceeds a "
            "constant. <bookmark mark='f'/>The guarantee is about the rule, in the long run: not about how strong "
            "the evidence is in this particular case."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(ax), Create(f0), Create(f1), FadeIn(h0), FadeIn(h1))
            vo.wait_until("b")
            self.play(Create(cl), FadeIn(rej))
            vo.wait_until("c")
            self.play(FadeIn(a_area), FadeIn(side[0]))
            vo.wait_until("d")
            self.play(FadeIn(b_area), FadeIn(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
            vo.wait_until("f")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def bayes(self):
        hc = history_card(1939, r"Harold Jeffreys", r"\textit{Theory of Probability}", width=5.6,
                          color=HIST).to_corner(UL, buff=0.35)
        eq = MathTex(r"\frac{P(H_0 \mid x)}{P(H_1 \mid x)} = \underbrace{\frac{P(x \mid H_0)}{P(x \mid H_1)}}_{"
                     r"\text{Bayes factor } B_{01}} \times \frac{P(H_0)}{P(H_1)}", font_size=36,
                     color=BAYC).next_to(hc, DOWN, buff=0.5).set_x(0)
        marg = MathTex(r"P(x \mid H_1) = \int P(x \mid \theta)\, \pi(\theta \mid H_1)\, d\theta", font_size=30,
                       color=GREY_A).next_to(eq, DOWN, buff=0.35)
        scale = stack([(r"Jeffreys's scale: \ $B_{10}$ of 3, \ 10, \ 30, \ 100: \ substantial, \ strong, \ very strong, "
                        r"\ decisive", WHITE),
                       (r"evidence \textit{for} the null is possible; \ the alternative must be spelled out as a prior",
                        GOAL)], font_size=21).next_to(marg, DOWN, buff=0.45)
        with self.voiceover(
            "The third school is older and newer at once. Harold Jeffreys, in his Theory of Probability of 1939, "
            "made Bayes's theorem a method for testing. <bookmark mark='a'/>The posterior odds of the null against "
            "the alternative equal the prior odds times the Bayes factor: the ratio of how well each hypothesis "
            "predicted the data. <bookmark mark='b'/>For a composite alternative, its prediction is an average over "
            "a prior on its parameter. <bookmark mark='c'/>Jeffreys gave a scale for reading Bayes factors: three is "
            "substantial, ten strong, a hundred decisive. <bookmark mark='d'/>Two differences from Fisher stand out. "
            "Data can be evidence for the null, not just fail to be evidence against it. And the alternative has to "
            "be spelled out."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(marg))
            vo.wait_until("c")
            self.play(FadeIn(scale[0]))
            vo.wait_until("d")
            self.play(FadeIn(scale[1]))
        self.clear_scene()

    def fiducial(self):
        hc = history_card(1930, r"Fisher's fiducial argument", r"`Inverse Probability'", width=6.0,
                          color=HIST).to_corner(UL, buff=0.35)
        steps = VGroup(
            MathTex(r"P\big(\bar X - \mu \le 1.645\,\sigma/\sqrt n \ \big|\ \mu\big) = 0.95", font_size=32,
                    color=WHITE),
            MathTex(r"\text{observe } \bar x:\quad \text{`} P\big(\mu \ge \bar x - 1.645\,\sigma/\sqrt n\big) = "
                    r"0.95\text{'}", font_size=32, color=FISH),
        ).arrange(DOWN, buff=0.45).next_to(hc, DOWN, buff=0.5).set_x(0)
        rows = stack([
            (r"a probability for $\mu$ \ without any prior: \ Fisher's hope", FISH),
            (r"Neyman: \ the same numbers as a \textit{confidence} statement about the procedure", NEYP),
            (r"with several parameters the argument broke down: \ `Fisher's biggest blunder' \ (Efron)", BAD),
            (r"revived as confidence distributions \ and generalized fiducial inference", GREY_A),
        ], font_size=21, aligned_edge=LEFT, buff=0.3).next_to(steps, DOWN, buff=0.45)
        with self.voiceover(
            "Fisher also wanted what the Bayesians had, a probability for the parameter itself, without a prior. "
            "<bookmark mark='a'/>He started from a statement about the data: the sample mean exceeds the true mean "
            "by more than one point six four five standard errors only five percent of the time. "
            "<bookmark mark='b'/>Then, once the mean is observed, he read the statement the other way round, as a "
            "probability distribution for the unknown mean. He called it fiducial probability. "
            "<bookmark mark='c'/>Neyman took the same numbers and read them as a confidence statement about the "
            "procedure, not about the parameter. <bookmark mark='d'/>For problems with several parameters, Fisher's "
            "argument gave inconsistent answers, and Bradley Efron called it Fisher's biggest blunder. "
            "<bookmark mark='e'/>It has recently been revived, in confidence distributions and generalized "
            "fiducial inference."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(steps[0]))
            vo.wait_until("b")
            self.play(Write(steps[1]), FadeIn(rows[0]))
            for mk, r in zip("cde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def coin(self):
        d = load("schools")
        head = label(r"One coin, \ three verdicts: \ " + str(d["heads"]) + r" heads in " + str(d["n"]) + r" tosses",
                     font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Fisher", r"$p = " + f"{d['p_fisher']:.3f}" + r"$: \ not quite significant; \ some evidence against "
                        r"fairness", FISH),
            (r"Neyman--Pearson", r"reject if heads $\le " + str(d["reject_below"]) + r"$ or $\ge " +
             str(d["reject_above"]) + r"$ \ (size " + f"{d['size']:.3f}" + r"): \ do not reject; \ power against "
             r"0.6 only " + f"{d['power']:.2f}", NEYP),
            (r"Jeffreys", r"$B_{01} = " + f"{d['bf01']:.2f}" + r"$: \ the data slightly \textit{favour} fairness; "
                          r"\ $P(H_0 \mid x) = " + f"{d['post_null']:.2f}" + r"$", BAYC),
        ]
        g = rows_table(rows, x_label=-6.4, x_text=-2.6, top=1.6, gap=0.6, label_size=24, text_size=22, width=9.0)
        foot = label(r"the same numbers: \ evidence against, \ no decision, \ evidence for", font_size=24,
                     color=GOAL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Give the three schools the same data: sixty heads in a hundred tosses. Is the coin fair? "
            "<bookmark mark='a'/>Fisher's p-value is point zero five seven. Not quite significant; some evidence "
            "against fairness. <bookmark mark='b'/>Neyman and Pearson fix the rule in advance: reject if heads are "
            "at most thirty-nine or at least sixty-one. Sixty falls short, so the null is not rejected, and the "
            "test had less than even power against a coin biased to point six. <bookmark mark='c'/>Jeffreys, with a "
            "uniform prior on the bias, finds a Bayes factor of one point one in favour of the fair coin: the data "
            "very slightly support fairness. <bookmark mark='d'/>Evidence against, no decision, evidence for: the "
            "same numbers, three readings."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r[0]), FadeIn(r[1], shift=LEFT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def feud(self):
        head = label(r"The feud, \ and the hybrid", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Fisher \ (1955)", r"Neyman--Pearson tests are acceptance procedures for factories, \ not reasoning in "
                                 r"science", FISH),
            (r"Neyman \ (1957)", r"there is no `inductive inference', \ only `inductive behaviour': \ rules with good "
                                 r"error rates", NEYP),
            (r"the textbooks", r"Fisher's $p$, \ Neyman's $\alpha = 0.05$, \ read as a Bayesian probability: \ "
                               r"the `null ritual'", BAD),
            (r"Gigerenzer \ (2004)", r"a hybrid that neither founder would have recognized", GREY_A),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=9.2)
        with self.voiceover(
            "The founders fought bitterly. <bookmark mark='a'/>Fisher wrote in 1955 that Neyman and Pearson's tests "
            "were acceptance procedures, fit for quality control in a factory, not for reasoning in science. "
            "<bookmark mark='b'/>Neyman replied that there is no such thing as inductive inference, only inductive "
            "behaviour: following rules whose error rates are known. <bookmark mark='c'/>What reached the textbooks "
            "was a hybrid: Fisher's p-value, compared with Neyman's fixed five percent, and then read as if it were "
            "the Bayesian probability that the null is true. <bookmark mark='d'/>Gerd Gigerenzer called it the null "
            "ritual, a procedure neither founder would have recognized. Much of the replication crisis begins here."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
