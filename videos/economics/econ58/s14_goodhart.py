from __future__ import annotations

from videos.economics.econ58.common import *  # noqa: F403


class Goodhart(VoiceoverScene):
    def construct(self):
        card(self, 12, r"What targets do to numbers", r"What happens to a number once a decision depends on it?",
             "Chapter twelve. What targets do to numbers.", lit={1975: r"Goodhart", 1979: r"Campbell",
                                                                 2005: r"the four-hour target"},
             scale=("person", "nation"), horizon=("a day", "a year"))
        self.laws()
        self.waits()

    def laws(self):
        g = history_card(1975, r"Charles Goodhart", r"`Any observed statistical regularity will tend to collapse "
                         r"once pressure is placed upon it for control purposes.'", color=CBO, width=11.4,
                         font_size=23)
        c = history_card(1979, r"Donald Campbell", r"`The more any quantitative social indicator is used for social "
                         r"decision-making, \ the more subject it will be to corruption pressures \ and the more apt "
                         r"it will be to distort and corrupt the social processes it was intended to monitor.'",
                         color=COST, width=11.4, font_size=23)
        VGroup(g, c).arrange(DOWN, buff=0.5).move_to(DOWN * 0.4)
        top = label(r"once a decision depends on a number, \ people act on the number", font_size=28,
                    color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.TARGETS_58.tag, corner=DL, font_size=12)
        with self.voiceover(
            "Every number in this part is meant to inform a decision, and once a decision depends on a number, "
            "people act on the number. <bookmark mark='a'/> Charles Goodhart, an economist at the Bank of England, "
            "put it for monetary policy in 1975: any observed statistical regularity will tend to collapse once "
            "pressure is placed upon it for control purposes. <bookmark mark='b'/> Donald Campbell, a psychologist, "
            "put it for social policy: the more any quantitative social indicator is used for social decision-making, "
            "the more subject it will be to corruption pressures, and the more apt it will be to distort and "
            "corrupt the social processes it was intended to monitor."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(top, shift=DOWN * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(g, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def waits(self):
        G = load("target")
        T = tables.TARGETS_58.data
        edges, h0, h1 = np.array(G["edges"]), np.array(G["h0"]), np.array(G["h1"])
        top = float(max(h0.max(), h1.max())) * 1.12
        ax = plane([0, 480], [0, top], center=LEFT * 2.6 + DOWN * 0.5, x_length=7.4, y_length=4.6,
                   xticks=[0, 120, 240, 360, 480], yticks=[], xlabel=r"minutes from arrival to admission or "
                   r"discharge", ylabel=r"share of patients", xfmt=lambda v: f"{v:.0f}", font_size=14)

        def hist(h, col, op):
            g = VGroup()
            for a, b, v in zip(edges[:-1], edges[1:], h):
                p0, p1 = ax.ax.c2p(a, 0), ax.ax.c2p(b, v)
                g.add(Rectangle(width=(p1[0] - p0[0]) * 0.9, height=max(p1[1] - p0[1], 0.001), fill_color=col,
                                fill_opacity=op, stroke_width=0).move_to((p0 + p1) / 2))
            return g

        before = hist(h0, GREY_B, 0.7)
        after = hist(h1, COST, 0.8)
        line = DashedLine(ax.ax.c2p(240, 0), ax.ax.c2p(240, top), color=E.ACCENT, stroke_width=2)
        ll = label(r"four hours", font_size=17, color=E.ACCENT).next_to(ax.ax.c2p(240, top), UP, buff=0.05)
        side = VGroup(
            label(rf"within four hours: \ {100 * G['within_before']:.0f}\% $\to$ {100 * G['within_after']:.0f}\%",
                  font_size=21, color=WHITE),
            label(rf"in the last quarter-hour: \ {100 * G['spike_before']:.0f}\% $\to$ {100 * G['spike_after']:.0f}\%",
                  font_size=21, color=COST),
            label(rf"the median wait: \ {G['median_before']:.0f} minutes, \ unchanged", font_size=21,
                  color=GREY_A),
            label(rf"England, \ 2002 to 2004: \ waits over four hours {T['before']}\% $\to$ {T['after']}\%",
                  font_size=19, color=CBO),
            label(r"with reports of patients admitted, \ or moved, \ just before the deadline", font_size=17,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.3)
        tag = island_tag(r"the Island: \ an emergency department, \ simulated", corner=DR, font_size=12)
        eng = history_card(2005, r"England's emergency departments", rf"{T['target']}\% of patients admitted, "
                           r"transferred or discharged within four hours", color=CBO, width=5.6,
                           font_size=19).move_to(ax.get_center())
        with self.voiceover(
            "England gave its hospitals a target: patients in emergency departments should be admitted, transferred "
            "or discharged within four hours, for ninety-eight percent of them from 2005. <bookmark mark='a'/> Here "
            "is an Island emergency department before any target: the time each patient spends, with a long tail "
            "past four hours. <bookmark mark='b'/> Now set the target, and suppose staff move on most patients who "
            "would have breached it by less than two hours, in the last fifteen minutes before the deadline. "
            f"<bookmark mark='c'/> The share seen within four hours jumps from {100 * G['within_before']:.0f} to "
            f"{100 * G['within_after']:.0f} percent, and a spike grows just under the line. <bookmark mark='d'/> The "
            "typical patient's wait has not changed at all. <bookmark mark='e'/> In England the share waiting over "
            f"four hours fell from {T['before']} percent in 2002 to {T['after']} in 2004. Much of that was real "
            "improvement; Gwyn Bevan and Christopher Hood also collected reports of patients moved to wards, or "
            "ambulances kept waiting outside, to beat the clock. Every appraisal target, a benefit-cost ratio "
            "above one included, invites the same, which is the best argument for scoring forecasts against "
            "outcomes."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(eng, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeOut(eng), run_time=0.5)
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in before], lag_ratio=0.02), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(line), FadeIn(ll))
            vo.wait_until("c")
            self.play(FadeOut(before), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in after], lag_ratio=0.02),
                      FadeIn(side[0]), FadeIn(side[1]), run_time=1.8)
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()
