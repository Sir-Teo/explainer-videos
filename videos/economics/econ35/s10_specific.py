from __future__ import annotations

from videos.economics.econ35.common import *  # noqa: F403


class Specific(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Specific factors: \ who loses first", r"Who is hurt when a price changes tomorrow, not in "
             r"ten years?", "Chapter eight. Specific factors: who loses first.",
             lit={1971: r"Jones; \ Samuelson", 1965: r"Olson"}, scale=("household", "nation"),
             horizon=("a year",))
        self.diagram()
        self.politics()

    def diagram(self):
        S = load("specific")
        Lt = S["L"]
        ax = plane([0, Lt], [0, 1.6], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=4.6,
                   xticks=[0, 25, 50, 75, 100], yticks=[0, 0.4, 0.8, 1.2, 1.6],
                   xlabel=r"workers in manufacturing $\rightarrow$ \qquad $\leftarrow$ workers in farming",
                   ylabel=r"the value of a worker's marginal product", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        vM = path(ax, S["curve_L"], S["vM"], CAPITAL, 3.4, yr=(0, 1.6))
        vA0 = path(ax, S["curve_L"], S["vA0"], LAND, 3.4, yr=(0, 1.6))
        vA1 = path(ax, S["curve_L"], S["vA1"], LAND, 3.4, yr=(0, 1.6)).set_stroke(opacity=1.0)
        vA0d = path(ax, S["curve_L"], S["vA0"], LAND, 1.6, yr=(0, 1.6)).set_stroke(opacity=0.45)
        e0 = dot(ax, S["LM0"], S["w0"], WHITE, 0.08)
        e1 = dot(ax, S["LM1"], S["w1"], GAIN, 0.09)
        side = VGroup(
            label(r"gold: \ in factories, \\ working with capital", font_size=18, color=CAPITAL),
            label(r"brown: \ on farms, \\ working with land", font_size=18, color=LAND),
            label(r"the wage is where \\ they cross", font_size=18, color=WHITE),
            label(rf"food +{100 * S['dpA']:.0f}\%: \\ wage {100 * S['dw']:+.1f}\%, \\ land {100 * S['drT']:+.0f}\%, \\ "
                  rf"capital {100 * S['drK']:+.1f}\%", font_size=19, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Jones, \ in \emph{Trade, \ Balance of Payments and Growth} (1971); \ Samuelson (1971); \ "
                            r"the Island", corner=DR, font_size=12)
        setup = VGroup(
            label(r"labour moves \\ between sectors", font_size=20, color=LABOUR),
            label(r"capital is stuck \\ in manufacturing", font_size=20, color=CAPITAL),
            label(r"land is stuck \\ in farming", font_size=20, color=LAND),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Heckscher and Ohlin's world is a long run, in which capital moves freely between industries. "
            "Tomorrow, a loom cannot plough a field. The specific-factors model, set out by Ronald Jones and Paul "
            "Samuelson in 1971, takes that seriously: labour moves, but capital is stuck in manufacturing and land "
            "in farming. <bookmark mark='a'/> The gold curve is what a worker adds in the factories, with "
            "workers counted from the left; <bookmark mark='b'/> the brown curve what a worker adds on the farms, "
            "counted from the right. <bookmark mark='c'/> Workers move until the two are equal, and that sets the "
            f"wage. <bookmark mark='d'/> Now the price of food rises {100 * S['dpA']:.0f} percent. The farm curve "
            f"shifts up, workers move to the farms, and the wage rises, but only {100 * S['dw']:.0f} percent, less "
            f"than the price of food. Landowners gain {100 * S['drT']:.0f} percent; the owners of factories lose "
            f"{abs(100 * S['drK']):.0f}. And workers? Better off in manufactures, worse off in food: it depends on "
            "what they eat."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(x, shift=LEFT * 0.1) for x in setup], lag_ratio=0.6), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeOut(setup), Create(vM), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(vA0), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(e0, scale=1.4), FadeIn(side[2]))
            vo.wait_until("d")
            self.add(vA0d)
            self.play(Transform(vA0, vA1), FadeIn(e1, scale=1.4), FadeIn(side[3]), run_time=1.5)
        self.clear_scene()

    def politics(self):
        rows = VGroup(
            label(r"losers are few and concentrated; \ winners many and diffuse", font_size=26, color=E.ACCENT),
            label(r"a tariff on cloth: \ each weaver and mill owner gains a lot", font_size=23, color=CAPITAL),
            label(r"each shopper loses a little, \ and may never notice", font_size=23, color=GREY_A),
            label(r"Olson (1965): \ small groups with large stakes organize; \ large groups with small stakes do not",
                  font_size=22, color=WHITE),
            label(r"so trade policy is made by the specific factors", font_size=24, color=TARIFF),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Olson, \ \emph{The Logic of Collective Action} (1965)", corner=DR, font_size=12)
        with self.voiceover(
            "This is why trade politics looks the way it does. <bookmark mark='a'/> The losers from imports are "
            "few and concentrated: the owners and workers of one industry, often in one region. "
            "<bookmark mark='b'/> A tariff on cloth is worth a great deal to each weaver and each mill owner. "
            "<bookmark mark='c'/> It costs each shopper a little, perhaps too little to notice. "
            "<bookmark mark='d'/> Mancur Olson explained in 1965 why that matters: small groups with large stakes "
            "organize, lobby and vote on the issue; large groups with small stakes do not. "
            "<bookmark mark='e'/> So trade policy tends to be made by and for the specific factors, which is the "
            "starting point of chapter ten."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
