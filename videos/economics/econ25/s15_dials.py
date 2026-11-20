from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ25.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dial: \ the interest semi-elasticity of money demand", r"How much less money do people "
             r"hold when interest rates rise?", "Chapter thirteen. The Dial: the interest semi-elasticity of money "
             "demand.", lit={2001: r"Ball", 2009: r"Ireland"}, scale=("nation",), horizon=("decades",))
        self.dial()

    def dial(self):
        dial = dials.DIALS["money_demand"]
        head = status_head(dial, r"the interest semi-elasticity of money demand \ (new)")
        frame, rows = dial_rows(dial, -0.08, 0.0, [-0.08, -0.06, -0.04, -0.02, 0.0], r"per point of the interest "
                                r"rate", top=1.7, step=0.8, fmt="{:.3f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 17, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"Ball, JME 47(1) (2001); \ Ireland, AER 99(3) (2009); \ this film", corner=DR,
                            font_size=12)
        ball, ireland, pre, post = dial.estimates
        with self.voiceover(
            "One dial, new in this part: the interest semi-elasticity of money demand, how much less money, "
            "relative to income, people hold for each point on the interest rate. <bookmark mark='a'/> Laurence "
            f"Ball's estimate for American M1 after the Second World War was about {ball.value:.2f}: five percent "
            "less money per point. <bookmark mark='b'/> Peter Ireland, using the years after 1980 and Cagan's form, "
            "found it below two percent per point. <bookmark mark='c'/> This film's regressions, from chapter nine, "
            f"give {pre.value:.3f} before 1981 <bookmark mark='d'/> and {post.value:.3f} after 1994. "
            "<bookmark mark='e'/> The status: contested. The number decides how costly inflation is, and it depends "
            "on which accounts you call money."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
