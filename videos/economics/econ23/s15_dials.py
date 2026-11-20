from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ23.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ risk aversion, \ and investment's response to its cost", r"How much do people "
             r"fear risk, \ and how much does cheaper capital raise investment?",
             "Chapter thirteen. The Dials: risk aversion, and investment's response to its cost.",
             scale=("household", "firm"), lit={1999: r"Chirinko et al.", 2017: r"Zwick and Mahon"},
             horizon=("a year", "a century"))
        self.risk()
        self.invest()

    def risk(self):
        dial = dials.DIALS["risk_aversion"]
        head = status_head(dial, r"relative risk aversion \ (from Part 7; \ three rows added)")
        frame, rows = dial_rows(dial, -1, np.log10(20), [0.1, 0.3, 1, 3, 10], r"$\gamma$ \ (log scale)", top=2.45,
                                step=0.41, log=True, fmt="{:.1f}")
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        new = rows[-3:]
        with self.voiceover(
            "Two dials. The first was opened in Part seven: relative risk aversion. <bookmark mark='a'/> Laboratory "
            "gambles over a few dollars give a fraction of one; consumption and labour supply about one; finance's "
            "estimates two to seven; survey gambles over lifetime income about four; the calibrations that fit asset "
            "prices, ten. <bookmark mark='b'/> This part adds three rows of its own. The Hansen-Jagannathan bound on "
            "Shiller's century needs at least eight. The consumption CAPM's premium over its covariance gives about "
            "twelve. And the Island with rare disasters fits the premium with three and a half. "
            "<bookmark mark='c'/> The status stays contested: the number you need depends on what you believe "
            "people fear."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:-3]], lag_ratio=0.2), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in new], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("c")
            self.play(Indicate(head[1], color=WHITE))
        self.clear_scene()

    def invest(self):
        dial = dials.DIALS["investment_user_cost"]
        head = status_head(dial, r"investment's response to the user cost \ (new)")
        frame, rows = dial_rows(dial, -2.0, 0.0, [-2.0, -1.5, -1.0, -0.5, 0.0], r"elasticity", top=1.4, step=0.95,
                                fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 17, GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"Chirinko, Fazzari and Meyer (1999); \ Hassett and Hubbard (2002); \ Zwick and Mahon "
                            r"(2017)", corner=DR, font_size=12)
        cfm, hh_, zm = dial.estimates
        with self.voiceover(
            "The second dial is new: how much investment responds when the user cost of capital falls. "
            "<bookmark mark='a'/> Robert Chirinko, Steven Fazzari and Andrew Meyer used American firms in the 1980s, "
            f"whose user costs differed, and found a small elasticity: about {cfm.value:.2f}. "
            "<bookmark mark='b'/> Kevin Hassett and Glenn Hubbard's review in 2002 put the range of then-recent "
            "studies at minus a half to minus one. <bookmark mark='c'/> Eric Zwick and James Mahon studied bonus "
            "depreciation, temporary tax breaks for equipment, across a hundred and twenty thousand firms: "
            "eligible investment rose about ten percent in 2001 to 2004 and seventeen in 2008 to 2010, with small "
            f"firms responding most, an elasticity of about {zm.value:.1f}. <bookmark mark='d'/> The status: "
            "contested. Whether a tax break or a rate cut builds factories depends on which of these is right, "
            "and on who is short of cash: the same lesson as Part twenty-two's households."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
