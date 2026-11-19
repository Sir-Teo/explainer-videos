from __future__ import annotations

from videos.economics.econ13.common import *  # noqa: F403


class Testing(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Testing for private information", r"If you can't see what people know, \ how can you tell "
             r"whether they are using it?", "Chapter nine. Testing for private information.",
             lit={2000: r"Chiappori and Salanié"}, scale=("person", "market"), horizon=("a year",))
        self.test()
        self.simulate()
        self.advantageous()

    def test(self):
        rows = VGroup(
            label(r"the trace private information leaves: \ those who buy more cover \ should claim more often",
                  font_size=24),
            label(r"among people the insurer prices the same: \ same age, \ same car, \ same town", font_size=23,
                  color=GREY_A),
            label(r"Pierre-Andr\'e Chiappori and Bernard Salani\'e (2000): \ young French drivers, \ licensed less "
                  r"than three years", font_size=23, color=SIGNAL),
            label(r"no correlation between full cover and accidents: \ no sign of private information", font_size=24,
                  color=GOOD),
            label(r"but the test also catches moral hazard: \ insured drivers who take less care \ (Part 14)",
                  font_size=23, color=HOLD),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Chiappori and Salani\'e, JPE 108(1) (2000)", corner=DR, font_size=13)
        with self.voiceover(
            "How would we know whether buyers really do know more? Private information leaves a trace. "
            "<bookmark mark='a'/> If the riskier people buy more cover, then those with more cover should claim more "
            "often, <bookmark mark='b'/> even among people the insurer treats alike: the same age, the same car, the "
            "same town. <bookmark mark='c'/> In 2000 Pierre-Andre Chiappori and Bernard Salanie looked for that "
            "correlation among young French drivers, licensed for less than three years. "
            "<bookmark mark='d'/> They found none: drivers with comprehensive cover had no more accidents than "
            "otherwise similar drivers with basic cover. <bookmark mark='e'/> The test has a second reading, too: a "
            "positive correlation could also come from insured drivers taking less care, which is moral hazard, the "
            "subject of Part fourteen."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def simulate(self):
        t = load("tests")
        res = t["results"]
        names = (("adverse", r"the risky buy more", LOSS), ("none", r"cover unrelated to risk", GREY_A),
                 ("advantageous", r"the cautious buy more", GOOD))
        ax = plane([0.4, 3.6], [0, 0.14], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.2, y_length=4.6, xticks=[],
                   yticks=[0, 0.05, 0.1], ylabel=r"share of drivers who claim", font_size=16,
                   yfmt=lambda v: f"{100 * v:.0f}\\%")
        a = ax.ax
        bars = VGroup()
        for k, (key, name, col) in enumerate(names):
            r = res[key]
            x = k + 1
            for dx, v, op in ((-0.17, r["claim_rate_basic"], 0.45), (0.17, r["claim_rate_full"], 0.95)):
                bars.add(Rectangle(width=0.3, height=a.c2p(0, v)[1] - a.c2p(0, 0)[1], stroke_width=0, fill_color=col,
                                   fill_opacity=op).move_to(a.c2p(x + dx, 0), aligned_edge=DOWN))
            bars.add(label(name, font_size=15, color=col).next_to(a.c2p(x, 0), DOWN, buff=0.2))
        key = label(r"each pair: \ basic cover (faint), \ full cover (solid)", font_size=15, color=GREY_B).next_to(
            ax, UP, buff=0.05)
        side = VGroup(
            label(rf"Agora's drivers: \ {t['n']:,} of them, \\ each with a private accident risk".replace(",", "{,}"),
                  font_size=21),
            label(rf"if the risky buy more, \ correlation {res['adverse']['corr']:.3f}: \\ the test sees it",
                  font_size=21, color=LOSS),
            label(rf"if cover is unrelated to risk: \\ {res['none']['corr']:.3f}, \ indistinguishable from 0",
                  font_size=21, color=GREY_A),
            label(rf"if a hidden trait, \ caution, \ makes people \\ both safer and keener to insure: \\ "
                  rf"{res['advantageous']['corr']:.3f}, \ negative", font_size=21, color=GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Agora can show what the test can and cannot see. <bookmark mark='a'/> Simulate twenty thousand drivers, "
            "each with a private accident risk. <bookmark mark='b'/> If the riskier ones are more likely to buy full "
            "cover, the full-cover drivers claim more often, and the correlation is positive: the test sees it. "
            "<bookmark mark='c'/> If cover has nothing to do with risk, the correlation is indistinguishable from "
            "zero. <bookmark mark='d'/> But suppose a hidden trait, caution, makes people both safer drivers and keener "
            "to insure. Then the full-cover drivers claim less often, and the correlation turns negative, though "
            "everyone is using what they know about themselves."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(key), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[0:3]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars[3:6]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(bars[6:9]), FadeIn(side[3]))
        self.clear_scene()

    def advantageous(self):
        rows = VGroup(
            label(r"Amy Finkelstein and Kathleen McGarry (2006): \ long-term care insurance in America", font_size=23),
            label(r"people's own forecasts of entering a nursing home \ predicted both buying cover and using care: \ "
                  r"private information", font_size=22, color=LOSS),
            label(r"yet the insured were no more likely to use care: \ the cautious buy more insurance and need less "
                  r"care", font_size=22, color=GOOD),
            label(r"two kinds of private information, \ pulling opposite ways, \ cancel in the correlation",
                  font_size=23, color=GREY_A),
            label(r"so a zero correlation doesn't prove that buyers know nothing", font_size=25, color=E.ACCENT),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Finkelstein and McGarry, AER 96(4) (2006)", corner=DR, font_size=13)
        with self.voiceover(
            "This is not just a simulation. <bookmark mark='a'/> In 2006 Amy Finkelstein and Kathleen McGarry studied "
            "long-term care insurance in America. <bookmark mark='b'/> People's own forecasts of how likely they were "
            "to enter a nursing home predicted both whether they bought cover and whether they later used care: clear "
            "private information. <bookmark mark='c'/> Yet the insured were no more likely to use care than the "
            "uninsured, because more cautious people both buy more insurance and need less care. "
            "<bookmark mark='d'/> Two kinds of private information, pulling in opposite directions, cancelled out in "
            "the correlation. <bookmark mark='e'/> So a correlation of zero doesn't prove that buyers know nothing the "
            "insurer doesn't."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
