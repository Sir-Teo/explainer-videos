from __future__ import annotations

from videos.economics.econ32.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ budget offices and debt managers", r"Who does this for a living?",
             "Chapter fourteen. In practice: budget offices and debt managers.", lit={2013: r"Blanchard and Leigh"},
             scale=("nation",), horizon=("a year", "decades"))
        self.jobs()
        self.called()

    def jobs(self):
        rows = VGroup(
            label(r"the people who do this", font_size=27, color=E.ACCENT),
            label(r"budget offices: \ the cost of every bill, \ and its effect on the economy \ (Part 58)",
                  font_size=21, color=TAX),
            label(r"debt managers: \ how much to borrow, \ at what maturities, \ in which instruments", font_size=21,
                  color=DEBT),
            label(r"finance-ministry and IMF economists: \ forecasts with the budget in them, \ debt sustainability",
                  font_size=21, color=SPEND),
            label(r"the tools: \ the budget constraint, \ r minus g, \ multipliers, \ and their uncertainty",
                  font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Part 58: \ scoring the bill", corner=DR, font_size=12)
        with self.voiceover(
            "Who does this for a living? <bookmark mark='a'/> Budget offices, such as America's Congressional "
            "Budget Office, estimate what every bill costs and how it moves the economy; Part 58 takes one apart. "
            "<bookmark mark='b'/> Debt managers in finance ministries decide how much to borrow, at what "
            "maturities and in which instruments, which matters more when rates rise. <bookmark mark='c'/> "
            "Economists at finance ministries and the IMF forecast with the budget built in, and judge whether "
            "debts are sustainable. <bookmark mark='d'/> Their tools are this part's: the budget constraint, r "
            "minus g, and multipliers, with honest bands around each."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["imf_2010"]
        L = load("bl")
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.4,
                       font_size=17).to_edge(UP, buff=0.3)
        ax = plane([-3, 6], [-9, 6], center=DOWN * 1.55 + LEFT * 1.6, x_length=7.0, y_length=2.6,
                   xticks=[-2, 0, 2, 4, 6], yticks=[-8, -4, 0, 4], xlabel=r"planned consolidation, \ \% of GDP",
                   ylabel=r"growth minus forecast", xfmt=lambda v: f"{v:+.0f}" if v else "0",
                   yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=13)
        zero = seg(ax, -3, 0, 6, 0, GREY_C, 1.2)
        pts = VGroup(*[Dot(ax.ax.c2p(r["x"], r["err"]), radius=0.05, color=TAX) for r in L["rows"]])
        fit = seg(ax, -3, L["a"] - 3 * L["b"], 6, L["a"] + 6 * L["b"], INFL, 3)
        names = VGroup(*[label(r["code"], font_size=11, color=GREY_B).next_to(ax.ax.c2p(r["x"], r["err"]), UR,
                                                                              buff=0.02)
                         for r in L["rows"] if r["code"] in ("GRC", "DEU", "IRL", "PRT", "ESP", "GBR")])
        key = VGroup(label(rf"slope: \ {L['b']:.2f} \ (s.e. {L['se']:.2f}), \ {L['n']} economies", font_size=15,
                           color=INFL),
                     label(r"a correct forecast would show \\ no slope at all", font_size=15, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).next_to(ax, RIGHT, buff=0.4)
        tag = published_tag(r"Blanchard and Leigh, \ \emph{AER} 103(3) (2013), \ replication data", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In April 2010 the IMF forecast growth for 2010 and 2011 in each "
            "European economy, knowing each government's plans to cut its deficit. If the forecasters had used the "
            "right multiplier, the errors should have had nothing to do with the size of the plans. "
            "<bookmark mark='b'/> Here are the errors against the planned consolidation, recomputed from Olivier "
            "Blanchard and Daniel Leigh's data. <bookmark mark='c'/> The slope is "
            f"{L['b']:.2f}: each extra point of GDP of austerity came with growth about one point below forecast. "
            "Greece, on the right, missed by the most. <bookmark mark='d'/> The forecasts had underestimated the "
            "multiplier by about one. Wrong, and the IMF's own chief economist said so."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag), FadeIn(ax), FadeIn(zero))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromCenter(p) for p in pts], lag_ratio=0.05), FadeIn(names), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(fit), FadeIn(key), Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("d")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
