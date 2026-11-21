from __future__ import annotations

from videos.economics.econ64.common import *  # noqa: F403


class Prediction(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Prediction policy problems", r"Which decisions need a forecast, \ and which need a cause?",
             "Chapter one. Prediction policy problems.", lit={1954: r"Meehl", 2015: r"Kleinberg et al."},
             scale=("person", "nation"), horizon=("a year",))
        self.umbrella()
        self.island()
        self.called()

    def umbrella(self):
        left = point_cards([(r"the rain dance", r"does dancing cause rain? \ only a causal effect answers this: \ "
                             r"$\hat\beta$", CAUSE)], width=5.8, font_size=21)
        right = point_cards([(r"the umbrella", r"will it rain? \ if so, \ take one: \ the umbrella does not change "
                              r"the weather, \ so a forecast is enough: \ $\hat y$", ALGO)], width=5.8, font_size=21)
        pair = VGroup(left, right).arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.9)
        ex = VGroup(
            label(r"bail: \ will this person come back to court?", font_size=22, color=WHITE),
            label(r"a hip replacement pays off over years: \ will this patient live that long?", font_size=22,
                  color=WHITE),
            label(r"inspections: \ which restaurant, \ which building, \ which tax return?", font_size=22,
                  color=WHITE),
            label(r"each is a decision whose value turns on a prediction", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(pair, DOWN, buff=0.6)
        tag = published_tag(r"Kleinberg, \ Ludwig, \ Mullainathan and Obermeyer, \ AER 105(5) (2015); \ Mullainathan "
                            r"and Spiess, \ JEP 31(2) (2017)", corner=DL, font_size=12)
        with self.voiceover(
            "Most of economics asks causal questions. Jon Kleinberg, Jens Ludwig, Sendhil Mullainathan and Ziad "
            "Obermeyer pointed out that many policy decisions do not. <bookmark mark='a'/> A farmer wondering "
            "whether a rain dance brings rain needs a causal effect. <bookmark mark='b'/> A person deciding whether "
            "to take an umbrella needs only a forecast: the umbrella does not change the weather. Mullainathan and "
            "Jann Spiess put it as y-hat problems against beta-hat problems. <bookmark mark='c'/> Bail is an "
            "umbrella problem: the judge needs to know whether this person will come back. <bookmark mark='d'/> So "
            "is a hip replacement, whose benefit comes over years, for a patient who may not live that long. "
            "<bookmark mark='e'/> So are inspections: which restaurant, which building, which tax return. <bookmark "
            "mark='f'/> Each is a decision whose value turns on a prediction, and prediction is what machine "
            "learning does best."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            for k, mk in enumerate("cdef"):
                vo.wait_until(mk)
                self.play(FadeIn(ex[k], shift=RIGHT * 0.1))
        self.clear_scene()

    def island(self):
        Cc = load("courts")
        cal = Cc["calibration"]
        ax = plane([0, 0.5], [0, 0.5], center=LEFT * 2.6 + DOWN * 0.3, x_length=5.2, y_length=4.6,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5],
                   xlabel=r"the algorithm's predicted risk", ylabel=r"actual chance of failing to appear",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        diag = seg(ax, 0, 0, 0.5, 0.5, GREY_C, 1.5, dashed=True)
        tr = VGroup(*[dot(ax, c["predicted"], c["truth"], TRUTHC, 0.07) for c in cal])
        side = VGroup(
            label(rf"{Cc['n']:,} defendants: \ half to train, \ half to test".replace(",", "{,}"), font_size=20,
                  color=WHITE),
            label(r"trained only on the released \\ (their outcomes are the only ones seen)", font_size=20,
                  color=GAIN),
            label(r"a random forest: \ age, \ prior arrests, \\ missed court dates, \ the charge, \ a job",
                  font_size=20, color=ALGO),
            label(r"gold: \ each tenth of predicted risk \\ against the truth the Island knows", font_size=20,
                  color=TRUTHC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"the Island: \ risks planted; \ agora.learn.courts", corner=DL, font_size=12)
        with self.voiceover(
            f"The Island has bail courts too: {Cc['n']:,} defendants, fifty judges, each case assigned at random. "
            "<bookmark mark='a'/> Split them in half: one half to learn from, the other to test on. <bookmark "
            "mark='b'/> The algorithm can learn only from the defendants the judges released, because only their "
            "outcomes are seen. <bookmark mark='c'/> It is a random forest: many decision trees, each grown on a "
            "resample, each split chosen to separate those who came back from those who did not, using age, prior "
            "arrests, missed court dates, the charge and whether the person has a job. <bookmark mark='d'/> On the "
            "test half, group defendants by their predicted risk, in tenths, and compare with the truth the "
            "simulation knows. The forest ranks them well, but it underestimates the riskiest tenth: it learned "
            "from the released, who were the less risky of their kind. Remember that for chapter three."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(diag), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(side[k], shift=LEFT * 0.1))
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in tr], lag_ratio=0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["meehl_1954"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=17)
        cc.move_to(UP * 0.6)
        lesson = label(r"seventy years on: \ the formula usually wins, \ unless the expert sees what it cannot",
                       font_size=21, color=E.ACCENT).next_to(cc, DOWN, buff=0.55)
        tag = published_tag(r"Meehl (1954); \ Grove, \ Zald, \ Lebow, \ Snitz and Nelson, \ Psychological Assessment "
                            r"12(1) (2000)", corner=DR, font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In 1954 the psychologist Paul Meehl reviewed every study he could find "
            "that pitted clinicians against simple statistical rules applied to the same facts, and concluded that "
            "the rules did as well or better. Experts are inconsistent, and they give weight to vivid details. "
            "<bookmark mark='b'/> In 2000 William Grove and colleagues pooled 136 such studies. The mechanical rule "
            "was about ten percent more accurate on average, much better in a third to nearly half of the studies, "
            "and much worse in a few. <bookmark mark='c'/> The verdict: right. <bookmark mark='d'/> With one caveat "
            "this part keeps returning to: the expert sometimes sees what the records do not."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(cc.left), FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(cc.left, color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(cc.right))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
            vo.wait_until("d")
            self.play(FadeIn(lesson))
        self.clear_scene()
