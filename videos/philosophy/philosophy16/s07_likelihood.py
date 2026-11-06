from __future__ import annotations

from math import comb

from videos.philosophy.philosophy16.common import *  # noqa: F403


class Likelihood(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"The likelihood principle", r"Is all the evidence in the likelihood?",
                            lit=(1962,), part=PART)
        with self.voiceover("Chapter six. The likelihood principle."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.principle()
        self.coins()
        self.proof()
        self.price()
        self.brick()

    def principle(self):
        head = label(r"Three questions \ (Royall, \ 1997)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"what should I believe?", r"posterior probability: \ Bayes", BAYC),
                (r"what should I do?", r"decisions with controlled errors: \ Neyman and Pearson", NEYP),
                (r"what do the data say?", r"the likelihood", ALTC)]
        g = rows_table(rows, top=1.8, gap=0.4, width=7.0, x_text=-1.6, label_size=24, text_size=22)
        law = VGroup(label(r"the law of likelihood \ (Hacking, \ 1965):", font_size=22, color=GOAL),
                     MathTex(r"E \text{ favours } H_1 \text{ over } H_2 \iff P(E \mid H_1) > P(E \mid H_2),\quad "
                             r"\text{by the ratio}", font_size=30, color=GOAL)).arrange(DOWN, buff=0.15).next_to(
            g, DOWN, buff=0.5).set_x(0)
        lp = VGroup(label(r"the likelihood principle:", font_size=22, color=ALTC),
                    label(r"all the evidence an outcome gives about $\theta$ is in its likelihood function $\theta "
                          r"\mapsto P(x \mid \theta)$, \ up to a constant", font_size=21)).arrange(
            DOWN, buff=0.12).next_to(law, DOWN, buff=0.4)
        with self.voiceover(
            "Richard Royall separated three questions that statistics runs together. <bookmark mark='a'/>What "
            "should I believe? That needs prior probabilities: Bayes. <bookmark mark='b'/>What should I do? That "
            "needs decisions with controlled error rates: Neyman and Pearson. <bookmark mark='c'/>And what do the "
            "data say? For that, Royall argued, only the likelihood matters. <bookmark mark='d'/>Ian Hacking's law "
            "of likelihood: evidence favours one hypothesis over another if it was more probable under the first, "
            "and the ratio measures how strongly. <bookmark mark='e'/>The likelihood principle goes further: all "
            "the evidence that an outcome provides about a parameter is contained in its likelihood function, up to "
            "a constant factor. What else might have happened does not matter."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(law))
            vo.wait_until("e")
            self.play(FadeIn(lp))
        self.clear_scene()

    def coins(self):
        d = load("birnbaum")
        head = label(r"Nine heads and three tails, \ two ways", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 1.05, 0.5], x_length=5.6, y_length=3.0, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 16}).move_to([-3.5, -0.9, 0])
        peak = 0.75 ** 9 * 0.25 ** 3
        f1 = ax.plot(lambda t: t ** 9 * (1 - t) ** 3 / peak, x_range=[0, 1], color=FISH, stroke_width=6)
        f2 = ax.plot(lambda t: t ** 9 * (1 - t) ** 3 / peak, x_range=[0, 1], color=NEYP, stroke_width=3)
        xl = label(r"$\theta$ \ (chance of heads)", font_size=18, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.3)
        tl = label(r"both likelihoods $\propto \theta^9 (1 - \theta)^3$", font_size=20, color=ALTC).next_to(
            ax, UP, buff=0.15)
        a = stack([(r"Ann planned 12 tosses \ (binomial)", FISH),
                   (r"$L(0.75)/L(0.5) = " + f"{d['ratio_E1']:.2f}" + r"$", WHITE),
                   (r"$P(\ge 9 \text{ heads} \mid \theta = \tfrac12) = " + f"{d['p_binomial']:.3f}" + r"$: \ not "
                    r"significant", FISH)], font_size=21, aligned_edge=LEFT)
        b = stack([(r"Bo tossed until the 3rd tail \ (negative binomial)", NEYP),
                   (r"$L(0.75)/L(0.5) = " + f"{d['ratio_E2']:.2f}" + r"$", WHITE),
                   (r"$P(\ge 12 \text{ tosses} \mid \theta = \tfrac12) = " + f"{d['p_negative_binomial']:.3f}" +
                    r"$: \ significant", NEYP)], font_size=21, aligned_edge=LEFT)
        VGroup(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([3.3, -0.6, 0])
        foot = label(r"identical likelihoods, \ different $p$-values: \ the sampling plan changes the frequentist "
                     r"verdict", font_size=21, color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here is the classic illustration, due to Dennis Lindley and Lawrence Phillips. "
            "<bookmark mark='a'/>Ann planned to toss a coin twelve times, and got nine heads. "
            "<bookmark mark='b'/>Bo planned to toss until the third tail, which came on the twelfth toss: also nine "
            "heads and three tails. <bookmark mark='c'/>Their likelihood functions are identical in shape: both "
            "proportional to theta to the ninth times one minus theta cubed. The likelihood ratio of a biased coin, "
            "point seven five, against a fair one is four point eight for both. <bookmark mark='d'/>But their "
            "p-values for the fair coin differ. For Ann, the chance of nine or more heads in twelve is point zero "
            "seven three: not significant. For Bo, the chance of needing twelve or more tosses is point zero three "
            "three: significant. <bookmark mark='e'/>Same data, same likelihood, different verdicts, because the "
            "experiments they did not do differ."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a[0]), FadeIn(ax), FadeIn(xl), Create(f1))
            vo.wait_until("b")
            self.play(FadeIn(b[0]), Create(f2))
            vo.wait_until("c")
            self.play(FadeIn(tl), FadeIn(a[1]), FadeIn(b[1]))
            vo.wait_until("d")
            self.play(FadeIn(a[2]), FadeIn(b[2]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def proof(self):
        hc = history_card(1962, r"Allan Birnbaum", r"`On the Foundations of Statistical Inference'", width=6.6,
                          color=HIST).to_corner(UL, buff=0.3)
        coin = label(r"$E^*$: \ flip a fair coin; \ heads, \ do Ann's experiment; \ tails, \ do Bo's", font_size=21,
                     color=WHITE).next_to(hc, DOWN, buff=0.3).set_x(0)
        steps = VGroup(
            MathTex(r"\mathrm{Ev}\big(E^*, (E_1, x_1)\big) = \mathrm{Ev}\big(E^*, (E_2, x_2)\big)", font_size=30,
                    color=ALTC),
            MathTex(r"\mathrm{Ev}\big(E^*, (E_i, x_i)\big) = \mathrm{Ev}(E_i, x_i)", font_size=30, color=FISH),
            MathTex(r"\therefore\ \ \mathrm{Ev}(E_1, x_1) = \mathrm{Ev}(E_2, x_2)", font_size=34, color=GOAL),
        ).arrange(DOWN, buff=0.55).next_to(coin, DOWN, buff=0.45)
        whys = VGroup(
            label(r"sufficiency: \ in $E^*$, \ a statistic that merges the two outcomes is sufficient, \ since their "
                  r"likelihoods are proportional", font_size=19, color=ALTC),
            label(r"conditionality: \ which experiment the coin chose is known, \ and carries no information about "
                  r"$\theta$", font_size=19, color=FISH),
            label(r"the likelihood principle, \ for any two outcomes with proportional likelihoods", font_size=19,
                  color=GOAL))
        for w, st in zip(whys, steps):
            w.next_to(st, DOWN, buff=0.1)
        with self.voiceover(
            "In 1962 Allan Birnbaum proved that the likelihood principle follows from two principles almost every "
            "statistician accepts. <bookmark mark='a'/>Imagine a mixed experiment: flip a fair coin, and do Ann's "
            "experiment on heads, Bo's on tails. <bookmark mark='b'/>Within this mixture, Ann's outcome and Bo's "
            "outcome have proportional likelihoods, so a statistic that merges them is sufficient. The principle "
            "of sufficiency says the two outcomes of the mixture carry the same evidence. "
            "<bookmark mark='c'/>The principle of conditionality says that once you know which experiment the coin "
            "chose, the evidence is just the evidence of that experiment; the coin flip tells you nothing about "
            "theta. <bookmark mark='d'/>Chain the equalities: Ann's outcome and Bo's carry the same evidence. That "
            "is the likelihood principle. Accept sufficiency and conditionality, and p-values, which differ between "
            "Ann and Bo, cannot measure evidence."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(coin))
            vo.wait_until("b")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(Write(steps[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(Write(steps[2]), FadeIn(whys[2]))
        self.clear_scene()

    def price(self):
        d = load("birnbaum")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mcs"] == [["B1"], ["B2"], ["B3"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.9, width=3.9, font_size=21,
                       center=[0, -0.5, 0], title=r"The Price List: \ Birnbaum's theorem")
        positions = [(("B3",), r"the likelihoodists", r"Savage; \ Royall; \ Berger and Wolpert: \ accept the "
                                                       r"likelihood principle: \ $p$-values are not evidence"),
                     (("B2",), r"Durbin \ (1970)", r"restrict conditionality to ancillaries that are functions of the "
                                                   r"sufficient statistic"),
                     (("B1",), r"Kalbfleisch \ (1975)", r"restrict sufficiency to within a single experiment"),
                     ((), r"Mayo \ (2014)", r"the proof equivocates between two readings of the principles: \ "
                                            r"no price is owed")]
        with self.voiceover(
            "Birnbaum's theorem is a Price List. <bookmark mark='a'/>Sufficiency; conditionality; and the conviction "
            "that the sampling plan matters, that Ann's data and Bo's are different evidence. "
            "<bookmark mark='b'/>Together they are inconsistent, and giving up any one restores consistency. "
            "<bookmark mark='c'/>Leonard Savage, Richard Royall, and James Berger and Robert Wolpert give up the "
            "third. They accept the likelihood principle, and with it the conclusion that p-values are not "
            "evidence. Savage called Birnbaum's paper a really historic occasion. <bookmark mark='d'/>James Durbin "
            "restricted conditionality, so that the mixture's coin flip no longer qualifies. "
            "<bookmark mark='e'/>John Kalbfleisch restricted sufficiency instead. <bookmark mark='f'/>And Deborah "
            "Mayo argued in 2014 that the proof itself equivocates, using the principles in two different senses, "
            "so that no price is owed at all. The debate is still open."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cdef", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def brick(self):
        w = wall(upto=16, current=16).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(16, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        rows = card[1][1]
        with self.voiceover(
            "This is the sixteenth brick in the Wall. <bookmark mark='a'/>The dream: one account of statistical "
            "evidence that controls long-run error rates and also tells us what this particular data set means. "
            "<bookmark mark='b'/>The wall: Birnbaum's theorem. Respect sufficiency and conditionality, and the "
            "evidential meaning of data is fixed by the likelihood alone, which ignores error rates. "
            "<bookmark mark='c'/>What it forces: choose your principle. Keep error control and give up a principle "
            "that seems obvious, or keep the principles and give up error rates as evidence. Lindley's paradox, in "
            "the next chapter, shows how far apart the two sides can land."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(Indicate(w.brick[16], color=P.CONCL, scale_factor=1.08), FadeIn(card[0]), FadeIn(card[1][0]),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            self.play(Indicate(card, color=P.WALL, scale_factor=1.02))
        self.clear_scene()
