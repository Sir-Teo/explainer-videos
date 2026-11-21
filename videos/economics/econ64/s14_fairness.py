from __future__ import annotations

from videos.economics.econ64.common import *  # noqa: F403


class Fairness(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Fairness", r"Can a risk score be fair to two groups in every sense at once?",
             "Chapter twelve. Fairness.", lit={2016: r"ProPublica", 2017: r"Kleinberg et al."},
             scale=("person", "nation"), horizon=("a year",))
        self.compas()
        self.island()
        self.identity()

    def compas(self):
        cards = VGroup(
            history_card(2016, r"Broward County, \ Florida", r"ProPublica studies a commercial risk score for more "
                         r"than 10,000 defendants: \ Black defendants who did not reoffend were labelled higher risk "
                         r"45\% of the time, \ white defendants 23\%", color=GROUPB, width=11.2, font_size=21),
            history_card(r"the reply", r"the same score, \ read another way", r"at each score, \ Black and white "
                         r"defendants reoffended at about the same rate: \ the score was calibrated for both",
                         color=GROUPA, width=11.2, font_size=21),
            history_card(r"both true", r"and both cannot be fixed at once", r"when two groups reoffend at different "
                         r"rates, \ a calibrated score must make different kinds of error for each", color=E.ACCENT,
                         width=11.2, font_size=21),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.2)
        tag = published_tag(r"Angwin, \ Larson, \ Mattu and Kirchner, \ ProPublica (2016)", corner=DL, font_size=12)
        with self.voiceover(
            "In 2016 the newsroom ProPublica studied a commercial risk score used for more than ten thousand "
            "defendants in Broward County, Florida. <bookmark mark='a'/> Among defendants who did not go on to "
            "reoffend, Black defendants had been labelled higher risk forty-five percent of the time, white "
            "defendants twenty-three percent. <bookmark mark='b'/> The company replied that at each score, Black "
            "and white defendants reoffended at about the same rate: the score meant the same thing for both. "
            "<bookmark mark='c'/> Both were true. When two groups have different rates of the outcome, no score "
            "can satisfy both definitions of fairness at once."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(cards[2], shift=UP * 0.1))
        self.clear_scene()

    def island(self):
        F = load("fairness")
        A, B = F["A"], F["B"]
        mids = (np.arange(10) + 0.5) / 10
        axc = plane([0, 1], [0, 1], center=LEFT * 3.6 + DOWN * 0.3, x_length=4.4, y_length=4.4,
                    xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], xlabel=r"score", ylabel=r"share who fail to appear",
                    xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", font_size=13)
        diag = seg(axc, 0, 0, 1, 1, GREY_C, 1.5, dashed=True)
        ca = VGroup(*[dot(axc, m - 0.012, v, GROUPA, 0.06) for m, v in zip(mids, A["calibration"]) if v is not None])
        cb = VGroup(*[dot(axc, m + 0.012, v, GROUPB, 0.06) for m, v in zip(mids, B["calibration"]) if v is not None])
        axe = plane([-0.6, 1.6], [0, 0.6], center=RIGHT * 1.2 + DOWN * 0.3, x_length=4.2, y_length=4.4, xticks=[],
                    yticks=[0, 0.2, 0.4, 0.6], ylabel=r"error rate", yfmt=lambda v: rf"{100 * v:.0f}\%",
                    font_size=13)
        eb = VGroup(bars(axe, [-0.17, 0.17], [A["fpr"], B["fpr"]], [GROUPA, GROUPB], width=0.3),
                    bars(axe, [0.83, 1.17], [A["fnr"], B["fnr"]], [GROUPA, GROUPB], width=0.3))
        el = VGroup(label(r"wrongly detained \\ (of those who \\ would come back)", font_size=13, color=GREY_A).next_to(
            axe.ax.c2p(0, 0), DOWN, buff=0.12),
            label(r"wrongly released \\ (of those who \\ would not)", font_size=13, color=GREY_A).next_to(
                axe.ax.c2p(1, 0), DOWN, buff=0.12))
        side = VGroup(
            label(rf"group A: \ {100 * A['base']:.0f}\% would fail", font_size=18, color=GROUPA),
            label(rf"group B: \ {100 * B['base']:.0f}\% would fail", font_size=18, color=GROUPB),
            label(rf"detain if the score \\ is above {F['threshold']:.1f}", font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ the score is each person's true risk; \ agora.learn.fairness", corner=DL,
                         font_size=12)
        with self.voiceover(
            "The Island shows why with the best score possible: each defendant's true risk. <bookmark mark='a'/> "
            f"Two groups: in A, {100 * A['base']:.0f} percent would fail to appear; in B, {100 * B['base']:.0f} "
            "percent, perhaps because B's neighbourhoods are policed more heavily, so its records are longer. "
            "Detain anyone whose score is above 0.3. <bookmark mark='b'/> The score is perfectly calibrated: at "
            "every level, the share who fail is the same in both groups. <bookmark mark='c'/> Now the errors. Of "
            f"those who would have come back, {100 * A['fpr']:.0f} percent of group A are detained, and "
            f"{100 * B['fpr']:.0f} percent of group B. <bookmark mark='d'/> Of those who would not, "
            f"{100 * A['fnr']:.0f} percent of A are released, and {100 * B['fnr']:.0f} percent of B. A perfectly "
            "accurate, perfectly calibrated score, and the errors still fall differently on the two groups."
        ) as vo:
            self.play(FadeIn(axc), FadeIn(diag), FadeIn(axe), FadeIn(el), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in ca], lag_ratio=0.05),
                      LaggedStart(*[FadeIn(d) for d in cb], lag_ratio=0.05), run_time=1.5)
            vo.wait_until("c")
            self.play(*[GrowFromEdge(b, DOWN) for b in eb[0]])
            vo.wait_until("d")
            self.play(*[GrowFromEdge(b, DOWN) for b in eb[1]])
        self.clear_scene()

    def identity(self):
        eq = label(r"$\text{FPR} = \dfrac{p}{1 - p}\cdot\dfrac{1 - \text{PPV}}{\text{PPV}}\cdot(1 - \text{FNR})$",
                   font_size=36).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"$p$: \ the group's base rate; \ PPV: \ the share of the detained who would fail", font_size=22,
                  color=GREY_A),
            label(r"different base rates, \ the same PPV: \ the error rates must differ", font_size=22, color=WHITE),
            label(r"calibration, \ equal false positives, \ equal false negatives: \ pick two at most", font_size=22,
                  color=E.ACCENT),
            label(r"which errors matter more is a value judgement; \ economics prices the trade-off, \ it does not "
                  r"settle it", font_size=22, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(eq, DOWN, buff=0.6)
        tag = published_tag(r"Chouldechova, \ Big Data 5(2) (2017); \ Kleinberg, \ Mullainathan and Raghavan, \ "
                            r"ITCS (2017)", corner=DL, font_size=12)
        with self.voiceover(
            "Alexandra Chouldechova wrote the reason in one line. <bookmark mark='a'/> The false positive rate "
            "equals the odds of the outcome in the group, times a term in the positive predictive value, times one "
            "minus the false negative rate. <bookmark mark='b'/> If two groups differ in their base rates and the "
            "score means the same thing in both, the error rates must differ. <bookmark mark='c'/> Jon Kleinberg, "
            "Sendhil Mullainathan and Manish Raghavan proved the general version: calibration and equal error "
            "rates for both kinds of error cannot hold together, except with equal base rates or perfect "
            "prediction. <bookmark mark='d'/> Which errors matter more, a wrongful detention or a missed court date, "
            "is a value judgement. Economics can price the trade-off and show who bears it; it cannot settle it. "
            "And the base rates themselves may carry the history of how each group was policed."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(eq), FadeIn(rows[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k + 1], shift=RIGHT * 0.1))
        self.clear_scene()
