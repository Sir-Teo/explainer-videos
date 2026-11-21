from __future__ import annotations

from videos.economics.econ53.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ robust design, \ learning receivers", r"What if the designer does not know the "
                                                                              r"audience?",
             "Chapter sixteen. Frontier: robust design and learning receivers.",
             lit={2005: r"Bergemann and Morris", 2021: r"algorithmic information design"}, scale=("person", "world"),
             horizon=("a decade",))
        self.robust()
        self.open_questions()

    def robust(self):
        C = load("concav")
        Pr = load("prosecutor")
        mu = np.array(C["mu"])
        ax = plane([0, 1], [0, 1.1], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.4, y_length=4.6,
                   xticks=[0, 0.3, 0.5, 1.0], yticks=[0, 0.5, 1.0], xlabel=r"the judge's belief in guilt",
                   ylabel=r"chance of a conviction", xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        cv = path(ax, mu, C["cv"], BELIEF, 3.0, smooth=False)
        thresholds = (0.45, 0.5, 0.55)
        posts = VGroup()
        for t in thresholds:
            posts.add(DashedLine(ax.ax.c2p(t, 0), ax.ax.c2p(t, 1.05), color=GREY_B, stroke_width=1.2))
        # design for 0.5; a judge who needs 0.55 convicts no one; a safer design aims at 0.55
        p_safe = Pr["prior"] * (1 - 0.55) / (0.55 * (1 - Pr["prior"]))
        safe = Pr["prior"] + (1 - Pr["prior"]) * p_safe
        side = VGroup(
            label(r"designed for a judge \\ who convicts at 0.5", font_size=19, color=SENDER),
            label(r"a judge who needs 0.55 \\ ignores the flag: \ 0 convicted", font_size=19, color=ERR),
            label(rf"aim at 0.55 instead: \\ {100 * safe:.0f}\% for sure, \ whichever \\ of the judges it is",
                  font_size=19, color=GAIN),
            label(r"robust design gives up a \\ little to lose nothing badly", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Bergemann and Morris, \ Econometrica 73(6) (2005): \ robust mechanism design",
                            corner=DR, font_size=12)
        with self.voiceover(
            "The optimal investigation sat exactly on the edge of the judge's standard. That is its weakness. "
            "<bookmark mark='a'/> It was designed for a judge who convicts at a belief of one half. <bookmark "
            "mark='b'/> A slightly stricter judge, who needs 0.55, would see that a flag means only one half, and "
            "convict nobody. <bookmark mark='c'/> A designer unsure which judge she faces can aim at the stricter "
            f"standard instead: {100 * safe:.0f} percent convicted, whichever judge it is. <bookmark mark='d'/> "
            "Robust design, which Dirk Bergemann and Stephen Morris began for mechanisms in 2005, gives up a little "
            "of the best case to avoid the worst. How much to give up, against audiences whose beliefs and "
            "standards are unknown, is an active field."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(cv), FadeIn(posts))
            for mk, s_ in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(s_, shift=RIGHT * 0.1))
        self.clear_scene()

    def open_questions(self):
        head = label(r"what remains open", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        cards = point_cards([
            (r"learning receivers", r"audiences who learn the designer's habits over time, \ or are algorithms",
             RECEIVER),
            (r"robustness", r"designs that work for audiences whose priors and standards are unknown", SENDER),
            (r"attention", r"receivers who cannot or will not read everything they are shown", BELIEF),
            (r"measurement", r"how much real people update: \ persuasion rates, \ beliefs elicited in surveys",
             SIGNAL),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.3)
        with self.voiceover(
            "What remains open? <bookmark mark='a'/> Receivers who learn: an audience that watches a designer over "
            "many rounds learns her habits, and the receiver may itself be an algorithm. <bookmark mark='b'/> "
            "Robustness to audiences whose priors and standards the designer does not know. <bookmark mark='c'/> "
            "Attention: real receivers cannot read everything, and what they skip changes what a design can do; "
            "Part forty-five's rational inattention returns here. <bookmark mark='d'/> And measurement: how much "
            "people actually update, from persuasion rates in the field to beliefs elicited directly in surveys."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c_ in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.1))
        self.clear_scene()
