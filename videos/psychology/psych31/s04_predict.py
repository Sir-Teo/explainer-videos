from __future__ import annotations

from videos.psychology.psych31.common import *  # noqa: F403

ORDER = ("cohort", "period", "age")  # the order the graphs are shown in
YEARS = ((0, r"1960", GREY_B), (3, r"1990", AGE), (6, r"2020", YOU))


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.quiz()
        self.answers()

    def card(self):
        card = chapter_card(3, r"On you: \ age, \ period or cohort?", r"Which clock drew each graph?", lit=(),
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter three. On you: age, period or cohort?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _panel(self, kind, i, d):
        A = axes([20, 80], [-1.1, 1.1], x_length=3.6, y_length=3.0, xticks=[20, 50, 80], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"age", center=[-4.4 + 4.4 * i, -0.3, 0], font_size=14)
        tab = d[f"lexis_{kind}"]
        lines = VGroup()
        for j, _, col in YEARS:
            y = tab[:, j] - (0.5 if kind == "period" else 0.0)
            lines.add(curve(A.ax, d["lexis_ages"], y, col, stroke_width=4))
        name = label(rf"Graph {i + 1}", font_size=26, color=WHITE).next_to(A, UP, buff=0.2)
        return VGroup(A, lines, name)

    def quiz(self):
        d = load("apc")
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        panels = VGroup(*[self._panel(k, i, d) for i, k in enumerate(ORDER)])
        key = legend([(col, rf"tested in {yr}") for _, yr, col in YEARS], font_size=18).arrange(RIGHT, buff=0.5)
        key.move_to([0, -2.75, 0])
        with self.voiceover(
            "Your turn. Each graph shows average scores by age, from cross-sections taken in three different "
            "years: 1960 in grey, 1990 in blue, 2020 in yellow. In each, only one clock is at work. "
            "<bookmark mark='a'/> Graph one: in every year, older people score lower, and every line is higher than "
            "the one before. <bookmark mark='b'/> Graph two: within a year, age makes no difference, but later "
            "years are higher. <bookmark mark='c'/> Graph three: the three years fall on one curve, flat until "
            "fifty, then down. <bookmark mark='d'/> Which clock drew each graph: age, period, or cohort? This part's "
            "interactive gives you nine more, and a world whose three effects you set yourself. Pause and decide."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(key))
            for m, p_ in zip("abc", panels):
                vo.wait_until(m)
                self.play(FadeIn(p_[0]), FadeIn(p_[2]), LaggedStart(*[Create(l_) for l_ in p_[1]], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(Indicate(stage, color=YOU))
        self.wait(3.0)
        self.clear_scene()

    def answers(self):
        d = load("apc")
        head = heading(r"The answers")
        panels = VGroup(*[self._panel(k, i, d) for i, k in enumerate(ORDER)]).shift(UP * 0.5)
        names = VGroup()
        for p_, kind, col in zip(panels, ORDER, (COHORT, PERIOD, AGE)):
            names.add(label(kind, font_size=30, color=col).next_to(p_[0], DOWN, buff=0.55))
        foot = wrapped_label(r"graph 1 is the trap: \ each cross-section shows a decline with age, \ yet nobody "
                             r"ages at all; \ the giveaway is that the lines move up between years", 12.4, 23, LOST)
        foot.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The answers. <bookmark mark='a'/> Graph one is cohort: each generation keeps its level for life, and "
            "later generations start higher. <bookmark mark='b'/> Graph two is period: whatever the year does, it "
            "does to everyone. <bookmark mark='c'/> Graph three is age: every year shows the same curve. "
            "<bookmark mark='d'/> Graph one is the trap. Every cross-section in it shows a decline with age, and "
            "yet nobody in that world ages at all. The giveaway is that the lines move up between the years. A "
            "single cross-section can't show you that, which is why chapter two's first design misleads."
        ) as vo:
            self.play(FadeIn(head), FadeIn(panels))
            for m, n_ in zip("abc", names):
                vo.wait_until(m)
                self.play(FadeIn(n_, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
