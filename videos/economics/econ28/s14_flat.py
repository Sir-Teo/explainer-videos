from __future__ import annotations

from videos.economics.econ28.common import *  # noqa: F403


class Flat(VoiceoverScene):
    def construct(self):
        card(self, 12, r"The flat Phillips curve", r"Where did the trade-off go after 2000?", "Chapter twelve. The "
             "flat Phillips curve.", lit={2022: r"Hazell, Herre\~no, Nakamura and Steinsson"}, scale=("nation",),
             horizon=("decades",))
        self.slopes()
        self.anchors()

    def slopes(self):
        F = load("flat")
        e, m, l_ = F["early"], F["middle"], F["late"]
        ax = plane([-3, 5], [-4, 4], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.4, y_length=4.8,
                   xticks=[-2, 0, 2, 4], yticks=[-4, -2, 0, 2, 4], xlabel=r"unemployment less the natural rate, \ "
                   r"points", ylabel=r"change in core inflation, \ points", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=15)

        def cloud(d, c):
            return VGroup(*[dot(ax, x, y, color=c, r=0.06) for x, y in zip(d["gap"], d["dpi"]) if -4 <= y <= 4])

        def fit(d, c):
            g = np.array(d["gap"])
            b, a = np.polyfit(g, d["dpi"], 1)
            return seg(ax, g.min(), a + b * g.min(), g.max(), a + b * g.max(), color=c, width=4)
        ce, cl = cloud(e, INFL), cloud(l_, CB)
        fe, fm, fl = fit(e, INFL), fit(m, EXPECT), fit(l_, CB)
        side = VGroup(
            label(rf"1960--1983: \ slope {e['slope']:.2f}", font_size=21, color=INFL),
            label(rf"1984--1999: \ {m['slope']:.2f}", font_size=21, color=EXPECT),
            label(rf"2000--2019: \ {l_['slope']:.2f}", font_size=21, color=CB),
            label(r"a point of slack once moved \\ inflation half a point a year; \\ now a tenth or less",
                  font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"BLS: \ core CPI and unemployment; \ CBO: \ the natural rate; \ annual, \ via FRED", corner=DR,
                       font_size=12)
        with self.voiceover(
            "After Volcker, the curve flattened. Across the bottom, how far unemployment was from the Budget "
            "Office's estimate of its natural rate; up the side, how much core inflation changed that year. "
            f"<bookmark mark='a'/> From 1960 to 1983, the slope was about {e['slope']:.2f}: each point of extra "
            "unemployment took about two thirds of a point off inflation in a year. "
            f"<bookmark mark='b'/> From 1984 to 1999, {m['slope']:.2f}. <bookmark mark='c'/> From 2000 to 2019, "
            f"{l_['slope']:.2f}: almost flat. <bookmark mark='d'/> In the Great Recession, unemployment rose five "
            "points above its natural rate, and inflation barely moved. Economists talked of the missing "
            "disinflation."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in ce], lag_ratio=0.05), Create(fe), FadeIn(side[0]),
                      run_time=1.5)
            vo.wait_until("b")
            self.play(Create(fm), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in cl], lag_ratio=0.05), Create(fl), FadeIn(side[2]),
                      run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def anchors(self):
        rows = VGroup(
            label(r"why flat?", font_size=28, color=E.ACCENT),
            label(r"1. \ \ anchored expectations: \ if everyone expects 2\%, \ prices are set as if inflation will "
                  r"be 2\%, \ whatever the slack", font_size=21, color=EXPECT),
            label(r"2. \ \ good policy hides the curve: \ a bank that offsets every demand shock leaves no trade-off "
                  r"to see", font_size=21, color=CB),
            label(r"3. \ \ the curve itself is flatter: \ global competition, \ fewer price changes \ (Part 30)",
                  font_size=21, color=WAGE),
            label(r"Hazell, \ Herre\~no, \ Nakamura and Steinsson, \ 2022: \ across states, \ which share one "
                  r"central bank, \ the slope is small, \ and was small even in the early 1980s", font_size=20,
                  color=OUTPUT),
            label(r"so the disinflation of the 1980s came mostly from expectations, \ not from slack", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Hazell, \ Herre\~no, \ Nakamura and Steinsson, \ QJE 137(3) (2022): \ 1299--1344",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Why so flat? Three answers, all partly true. <bookmark mark='a'/> First, anchored expectations: once "
            "everyone expects two percent, prices and wages are set as if inflation will be two percent, whatever "
            "the slack. <bookmark mark='b'/> Second, good policy hides the curve: a central bank that offsets every "
            "shift in demand leaves no trade-off in the data to see. <bookmark mark='c'/> Third, the curve itself "
            "may be flatter, with global competition and fewer price changes. <bookmark mark='d'/> Jonathon Hazell, "
            "Juan Herreño, Emi Nakamura and Jón Steinsson got around the second problem by comparing American "
            "states, "
            "which share one central bank. They found the slope small, and small even in the early 1980s. "
            "<bookmark mark='e'/> If so, the great disinflation came mostly from Volcker changing what people "
            "expected, not from the slack he created."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
