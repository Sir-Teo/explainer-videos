from __future__ import annotations

from videos.psychology.psych46.common import *  # noqa: F403


class Utility(VoiceoverScene):
    def construct(self):
        self.card()
        self.gumbel()
        self.mcfadden()

    def card(self):
        card = chapter_card(4, r"Random utility", r"Where does the logit come from?", lit={1974: r"McFadden"},
                            part=PART, scale=("person", "society"), marr=("what", "how"))
        with self.voiceover("Chapter four. Random utility."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def gumbel(self):
        d = load("gumbel")
        head = heading(r"Gumbel noise gives the logit")
        eqs = VGroup(
            MathTex(r"U_j = V_j + \varepsilon_j, \qquad \varepsilon_j \sim \text{Gumbel, independent}", font_size=34,
                    color=WHITE),
            MathTex(r"P(j \text{ chosen}) = P(U_j > U_k \ \forall k) = \frac{e^{V_j}}{\sum_k e^{V_k}}", font_size=36,
                    color=MODEL),
        ).arrange(DOWN, buff=0.4).move_to([-3.1, 1.4, 0])
        A = axes([0.3, 3.7], [0, 0.6], x_length=4.6, y_length=2.4, xticks=None, yticks=[0, 0.25, 0.5],
                 yfmt=lambda v: f"{v:g}", ylabel=r"share chosen", center=[-3.4, -1.6, 0], font_size=13)
        xs = np.array([1, 2, 3])
        b1 = bars(A.ax, xs - 0.17, d["sim"], [PERSON] * 3, width=0.3)
        b2 = bars(A.ax, xs + 0.17, d["logit"], [MODEL] * 3, width=0.3)
        names = VGroup(*[label(rf"$V = {v:g}$", font_size=13, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.1)
                         for i, v in enumerate(d["V"])])
        key = VGroup(label(r"400{,}000 simulated choices", font_size=12, color=PERSON),
                     label(r"logit formula", font_size=12, color=MODEL)).arrange(RIGHT, buff=0.3).next_to(A, UP, buff=0.05)
        rows = rows_of([
            (r"each option's utility is a systematic part, \ from its attributes, \ plus a random part", WHITE),
            (r"if the random parts are independent Gumbel (the law of the largest of many shocks), \ the chance of "
             r"being best is exactly the logit", MODEL),
            (rf"Psyche checks it: \ shares {d['sim'][0]:.3f}, \ {d['sim'][1]:.3f}, \ {d['sim'][2]:.3f} against "
             rf"{d['logit'][0]:.3f}, \ {d['logit'][1]:.3f}, \ {d['logit'][2]:.3f}", PERSON),
            (r"so Luce's axiom and random utility meet: \ the same formula from a mechanism", GOOD),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{scaling.gumbel\_choice\_shares}")
        with self.voiceover(
            "Economists reached the same formula by another road. <bookmark mark='a'/> Each option's utility is a "
            "systematic part, from its attributes, plus a random part. <bookmark mark='b'/> If the random parts are "
            "independent and follow the Gumbel distribution, the law of the largest of many shocks, then the chance "
            "that an option is best is exactly the logit. <bookmark mark='c'/> Psyche checks it with four hundred "
            "thousand simulated choices. The shares match the formula to the third decimal. <bookmark mark='d'/> So "
            "Luce's axiom and random utility meet. The same formula, from a mechanism."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eqs[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(eqs[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(A), FadeIn(names), FadeIn(key), FadeIn(b1), FadeIn(b2))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def mcfadden(self):
        head = heading(r"McFadden's forecast")
        steps = VGroup()
        for yr, txt, c in (
                (r"model", r"the conditional logit: \ utility as a weighted sum of an option's attributes, \ such as "
                           r"time, \ cost and walking; \ weights fitted from observed choices", MODEL),
                (r"forecast", r"before the San Francisco Bay Area's BART rail system opened, \ McFadden's model of "
                              r"commuters predicted its share of commuting trips", PERSON),
                (r"outcome", r"the forecast came close to the share actually observed; \ the engineering forecasts "
                             r"were far too high", GOOD),
                (r"since", r"transport planning, \ marketing, \ energy and health economics; \ the Nobel Prize in "
                           r"economics in 2000", YOU)):
            steps.add(VGroup(word_chip(yr, color=c, font_size=18, width=2.2), wrapped_label(txt, 9.6, 21, WHITE))
                      .arrange(RIGHT, buff=0.4))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.2, 0])
        tag = published_tag(r"McFadden (1974)")
        with self.voiceover(
            "Daniel McFadden made the model a tool. <bookmark mark='a'/> In the conditional logit, utility is a "
            "weighted sum of an option's attributes, such as travel time, cost and walking, with the weights fitted "
            "from people's observed choices. <bookmark mark='b'/> Before the Bay Area's BART rail system opened, his "
            "model of commuters predicted its share of trips. <bookmark mark='c'/> The forecast came close to the "
            "share actually observed, while the engineering forecasts were far too high. <bookmark mark='d'/> The "
            "method spread to transport planning, marketing, energy and health economics, and won him the Nobel "
            "Prize in 2000."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", steps):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
