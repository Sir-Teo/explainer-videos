from __future__ import annotations

from videos.economics.econ41.common import *  # noqa: F403


class Schedule(VoiceoverScene):
    def construct(self):
        card(self, 7, r"The whole schedule", r"What should marginal rates look like from the bottom to the top?",
             "Chapter seven. The whole schedule.", lit={1998: r"Diamond", 2002: r"Saez"},
             scale=("person", "nation"), horizon=("a year",))
        self.ushape()
        self.bottom()

    def ushape(self):
        M = load("mirrlees")
        lz = np.log10(np.array(M["z_rel"]))
        tp = np.array(M["Tp"])
        ax = plane([-0.7, 1.7], [0.4, 0.8], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.4, y_length=4.6,
                   xticks=[-0.5, 0, 0.5, 1.0, 1.5], yticks=[0.4, 0.5, 0.6, 0.7, 0.8],
                   xlabel=r"income, \ median = 1 \ (log scale)", ylabel=r"optimal marginal tax rate",
                   xfmt=lambda v: f"{10 ** v:.2g}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        m = (lz >= -0.7) & (lz <= 1.7)
        ln = path(ax, lz[m], tp[m], RATE, 3.6)
        top = seg(ax, -0.7, M["top"], 1.7, M["top"], GREY_B, 1.8, dashed=True)
        mn = M["min"]
        low = dot(ax, np.log10(mn["z_rel"]), mn["Tp"], WHITE, 0.09)
        side = VGroup(
            label(rf"at the bottom: \ {100 * M['bottom']:.0f}\%: \\ taking back benefits \\ as income rises",
                  font_size=18, color=RATE),
            label(rf"lowest, \ {100 * mn['Tp']:.0f}\%, \ near the \\ {100 * mn['F']:.0f}th percentile", font_size=18,
                  color=WHITE),
            label(rf"rising towards \\ $1/(1 + a e)$ = {100 * M['top']:.0f}\% \\ at the top, \ incomes' \\ "
                  rf"$a = \alpha/(1 + e)$ = {M['a_income']:.1f}", font_size=18,
                  color=GREY_B),
            label(r"a U-shape \\ (Diamond 1998)", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Multiply Diamond's three factors at every income, and the Island's optimal schedule appears. "
            f"<bookmark mark='a'/> At the bottom the marginal rate is high, {100 * M['bottom']:.0f} percent. That "
            "sounds harsh, but it is the rate at which support for the poorest is withdrawn as they earn more, and "
            "few people are affected while everyone above shares the benefit. <bookmark mark='b'/> Through the "
            f"middle the rate falls, to {100 * mn['Tp']:.0f} percent near the {100 * mn['F']:.0f}th percentile. "
            "<bookmark mark='c'/> Then it rises again, towards the top rate of chapter six, here "
            f"{100 * M['top']:.0f} percent: incomes grow faster than skills, because the more able also work "
            f"more, so the Island's incomes have a Pareto parameter of {M['a_income']:.1f}, and one over one plus a "
            "times e gives the limit. <bookmark mark='d'/> Diamond's U-shape. These levels are high because the "
            "Island's government cares a lot about equality and the elasticity is modest; the shape is what carries "
            "over."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(low, scale=1.5), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(top), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def bottom(self):
        cards = point_cards([
            (r"the intensive margin", r"people adjust hours: \\ high withdrawal rates \\ at the bottom \\ make sense",
             RATE),
            (r"the extensive margin", r"people decide whether \\ to work at all: \\ the bottom's rate \\ matters "
                                      r"most", WORKER),
            (r"Saez (2002)", r"if entry responds most, \\ pay more to those \\ who work than to \\ those who do not",
             TOP),
            (r"the EITC", r"a credit that rises \\ with earnings at first: \\ a negative marginal \\ rate", GAIN),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"the bottom of the schedule: \ work or no work", font_size=28, color=E.ACCENT).to_edge(UP,
                                                                                                    buff=0.6)
        tag = published_tag(tables.MIRRLEES_1971.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The bottom of the schedule is where the model's assumption about behaviour matters most. "
            "<bookmark mark='a'/> If people respond by adjusting their hours a little, the high withdrawal rates of "
            "the U make sense. <bookmark mark='b'/> But many low earners face a different choice: whether to work at "
            "all. <bookmark mark='c'/> In 2002 Saez showed that when that decision is what responds most, the best "
            "schedule pays more to low earners who work than to those who do not. <bookmark mark='d'/> America's "
            "Earned Income Tax Credit does just that: it rises with earnings at first, a negative marginal tax rate, "
            "before it is phased out. Part forty-two returns to it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
