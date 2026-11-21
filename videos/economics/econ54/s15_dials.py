from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ54.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ how averse to risk?", r"Why do careful methods disagree about one number?",
             "Chapter thirteen. The Dials: how averse to risk?",
             lit={2002: r"Holt and Laury", 2006: r"Chetty", 2025: r"Elminejad, Havranek and Irsova"},
             scale=("person", "household"), horizon=("a year", "a century"))
        self.risk()
        self.why()
        self.patience()

    def risk(self):
        dial = dials.DIALS["risk_aversion"]
        head = status_head(dial, r"relative risk aversion \ (from Parts 7, 22 and 23)")
        frame, rows = dial_rows(dial, -1, np.log10(20), [0.1, 0.3, 1, 3, 10], r"$\gamma$ \ (log scale)", top=2.45,
                                step=0.41, log=True, fmt="{:.1f}")
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        with self.voiceover(
            "Chapter nine borrowed a number from the Dial of relative risk aversion. Here is the Dial. <bookmark "
            "mark='a'/> Laboratory gambles over a few dollars give a fraction of one. Consumption and labour supply "
            "give about one. Finance's Euler equations give two to seven. Surveys of gambles over lifetime income "
            "give four. The calibrations that fit asset prices need ten or more. <bookmark mark='b'/> The status is "
            "contested, and after this part we can say why."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2), run_time=3.5)
            vo.wait_until("b")
            self.play(Indicate(head[1], color=WHITE))
        self.clear_scene()

    def why(self):
        rows = VGroup(
            label(r"each method leans on different facts:", font_size=24, color=E.ACCENT),
            label(r"the laboratory: \ small gambles, \ where any smooth utility should be nearly neutral",
                  font_size=21, color=WHITE),
            label(r"labour supply and consumption: \ how hours and spending respond to wages and windfalls",
                  font_size=21, color=PATIENCE),
            label(r"finance: \ how returns move with consumption, \ the Euler equation of Chapter 4", font_size=21,
                  color=EST),
            label(r"surveys: \ hypothetical gambles over a whole lifetime's income", font_size=21, color=DATA),
            label(r"one $\gamma$ in a model that is not quite right: \ each set of facts asks for its own value",
                  font_size=22, color=ERR),
            label(r"the $J$-test's lesson, \ at the scale of a whole field", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).move_to(UP * 0.1)
        with self.voiceover(
            "Each method leans on different facts, exactly as the sensitivity matrix showed for one estimate. "
            "<bookmark mark='a'/> The laboratory uses small gambles, where any smooth utility function should be "
            "nearly indifferent to risk, so whatever aversion people show there cannot be the curvature of "
            "utility over wealth, which is Matthew Rabin's point from Part seven. <bookmark mark='b'/> Labour "
            "supply and consumption use how hours and spending respond to wages and windfalls. <bookmark mark='c'/> "
            "Finance uses how returns move with consumption. <bookmark mark='d'/> Surveys use gambles over a "
            "lifetime's income that nobody is actually offered. <bookmark mark='e'/> Put one parameter, gamma, "
            "into a model that is not quite right, and each set of facts asks for its own value. <bookmark "
            "mark='f'/> It is the J-test's rejection from Chapter four, at the scale of a whole field: the "
            "conditions cannot all hold with a single number."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def patience(self):
        dial = dials.DIALS["dynamic_beta"]
        head = status_head(dial, r"the discount factor of a dynamic decision maker \ (from Part 44)")
        frame, rows = dial_rows(dial, 0.9, 1.0, [0.9, 0.925, 0.95, 0.975, 1.0], r"monthly discount factor", top=1.2,
                                step=0.9, fmt="{:.4f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 12.0, 18, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The other dial this part speaks to has a status of its own. <bookmark mark='a'/> When Part forty-four "
            "estimated Rust's buses, the likelihood barely moved among patient discount factors: it could rule out "
            "myopia, and little else. <bookmark mark='b'/> Not identified is a status a dial can have, and an honest "
            "one. The usual practice is to fix the discount factor by assumption and say so, which is calibration, "
            "chosen because estimation could not do better."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(rows))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
