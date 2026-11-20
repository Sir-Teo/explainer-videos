from __future__ import annotations

from videos.economics.econ28.common import *  # noqa: F403


class Critique(VoiceoverScene):
    def construct(self):
        card(self, 8, r"The Lucas critique", r"Can you estimate a trade-off and then exploit it?", "Chapter eight. "
             "The Lucas critique.", lit={1976: r"Lucas"}, scale=("nation",), horizon=("decades",))
        self.island()
        self.meaning()

    def island(self):
        C = load("critique")
        ax = plane([-2, 10], [92, 110], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.6, y_length=4.8,
                   xticks=[0, 2, 4, 6, 8, 10], yticks=[92, 96, 100, 104, 108], xlabel=r"inflation, \ \%",
                   ylabel=r"output", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        old = VGroup(*[dot(ax, x, y, color=CB, r=0.05) for x, y in zip(C["pi_old"], C["y_old"])])
        new = VGroup(*[dot(ax, x, y, color=INFL, r=0.05) for x, y in zip(C["pi_new"], C["y_new"]) if x <= 10])
        fit = seg(ax, -2, C["intercept"] - 2 * C["slope"], 7.5, C["intercept"] + 7.5 * C["slope"], color=EXPECT,
                  width=3)
        pred = dot(ax, C["pibar_new"], C["predicted"], color=EXPECT, r=0.1)
        act = dot(ax, C["pibar_new"], C["actual"], color=INFL, r=0.1)
        side = VGroup(
            label(rf"the old rule: \ inflation around {C['pibar_old']:.0f}\%; \\ people expect "
                  rf"{C['pibar_old']:.0f}\%", font_size=19, color=CB),
            label(rf"fitted: \ output rises {C['slope']:.1f} \\ per point of inflation", font_size=19, color=EXPECT),
            label(rf"the council moves to {C['pibar_new']:.0f}\%: \\ the fit predicts output {C['predicted']:.1f}",
                  font_size=19, color=EXPECT),
            label(rf"people now expect {C['pibar_new']:.0f}\%: \\ output averages {C['actual']:.1f}", font_size=19,
                  color=INFL),
            label(r"the slope was a fact about \\ the old rule, \ not about the economy", font_size=20,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Part four showed the Lucas critique with slowly adapting expectations. Here it is with rational ones. "
            f"<bookmark mark='a'/> For forty years the council has aimed at {C['pibar_old']:.0f} percent inflation, "
            "with random misses, and people expect two percent. Output rises whenever inflation is a surprise. "
            f"<bookmark mark='b'/> An economist fits a line through the blue years: output rises {C['slope']:.1f} "
            "for every point of inflation. A clean, stable relationship. <bookmark mark='c'/> So the council moves "
            f"its target to {C['pibar_new']:.0f} percent, and the line predicts output of {C['predicted']:.0f}. "
            f"<bookmark mark='d'/> But people now expect {C['pibar_new']:.0f} percent, and output averages "
            f"{C['actual']:.0f}, exactly where it always was. <bookmark mark='e'/> The slope was a fact about the "
            "old rule, not about the economy. Change the rule and the relationship changes with it. That was Lucas's "
            "critique, in 1976, of every policy model of the day."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), LaggedStart(*[FadeIn(d) for d in old], lag_ratio=0.02),
                      FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromCenter(pred), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(d) for d in new], lag_ratio=0.02), GrowFromCenter(act), FadeIn(side[3]),
                      run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def meaning(self):
        rows = VGroup(
            label(r"Lucas, \ 1976: \ ``Econometric policy evaluation: \ a critique''", font_size=25,
                  color=E.ACCENT),
            label(r"a model's coefficients summarize how people behaved under the old policy", font_size=23,
                  color=CB),
            label(r"people's decisions depend on what they expect policy to do", font_size=23, color=EXPECT),
            label(r"so to evaluate a new policy, \ model what people want and know, \ not past correlations",
                  font_size=23, color=OUTPUT),
            label(r"the reason macroeconomics rebuilt itself on tastes, \ technology and expectations \ (Part 29)",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Lucas, \ Carnegie-Rochester Conference Series 1 (1976): \ 19--46", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Lucas's paper was called Econometric policy evaluation: a critique. <bookmark mark='a'/> A model's "
            "coefficients summarize how people behaved under the old policy. <bookmark mark='b'/> But their "
            "decisions depend on what they expect policy to do. <bookmark mark='c'/> So to judge a new policy, you "
            "need a model of what people want and what they know, not a table of past correlations. "
            "<bookmark mark='d'/> That argument is the reason macroeconomics rebuilt itself, from the late 1970s, on "
            "people's tastes, firms' technology and everyone's expectations. Part twenty-nine is the first result."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
