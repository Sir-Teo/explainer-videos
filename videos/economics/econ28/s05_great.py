from __future__ import annotations

from videos.economics.econ28.common import *  # noqa: F403


class Great(VoiceoverScene):
    def construct(self):
        card(self, 4, r"The Great Inflation", r"How did the curve dissolve?", "Chapter four. The Great Inflation.",
             lit={1973: r"the first oil shock", 1979: r"the second"}, scale=("nation", "world"),
             horizon=("a decade",))
        self.loops()
        self.causes()

    def loops(self):
        u = load("us")
        ys = np.array(u["years"])
        k = (ys >= 1966) & (ys <= 1983)
        U, P = np.array(u["unemployment"])[k], np.array(u["inflation"])[k]
        ax = plane([3, 11], [0, 15], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.0, y_length=4.8,
                   xticks=[3, 5, 7, 9, 11], yticks=[0, 5, 10, 15], xlabel=r"unemployment, \ \%",
                   ylabel=r"inflation, \ \%", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        full = VMobject(stroke_color=INFL, stroke_width=3).set_points_as_corners(
            [ax.ax.c2p(x, y) for x, y in zip(U, P)])
        dots_ = VGroup(*[dot(ax, x, y, color=INFL, r=0.06) for x, y in zip(U, P)])
        names = VGroup(*[label(f"{yy}", font_size=13, color=GREY_B).next_to(ax.ax.c2p(x, y), UR, buff=0.04)
                         for x, y, yy in zip(U, P, ys[k]) if yy in (1966, 1970, 1973, 1974, 1975, 1979, 1980, 1983)])
        side = VGroup(
            label(r"each loop: \ a boom pushes inflation up; \\ a recession brings it partly down", font_size=19,
                  color=INFL),
            label(r"but each loop starts higher: \\ expected inflation ratchets up", font_size=19, color=EXPECT),
            label(r"1973 and 1979: \\ oil prices quadruple, \\ then more than double", font_size=19, color=WAGE),
            label(r"the short-run curves \\ shift up and right", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"BLS: \ the CPI and the unemployment rate, \ annual averages, \ via FRED", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Here are the years from 1966 to 1983, joined in order. <bookmark mark='a'/> They move in loops. A boom "
            "pushes inflation up; a recession brings it partly down; then the next boom starts. "
            "<bookmark mark='b'/> But each loop starts higher than the last, because each burst of inflation raised "
            "what people expected. Exactly Friedman's mechanism. <bookmark mark='c'/> On top came two oil shocks: "
            "in 1973 and 1974 the price of oil roughly quadrupled, and in 1979 and 1980 it more than doubled again. "
            "<bookmark mark='d'/> In the language of the last chapter, the short-run curves shifted up and to the "
            "right, and the menu of the 1960s was gone."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(full), LaggedStart(*[GrowFromCenter(d) for d in dots_], lag_ratio=0.1), FadeIn(names),
                      FadeIn(side[0]), run_time=4)
            for mk, r_ in zip("bcd", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()

    def causes(self):
        rows = VGroup(
            label(r"why did it happen?", font_size=28, color=E.ACCENT),
            label(r"policy chased an unemployment target that was too low: \ the natural rate had risen", font_size=22,
                  color=CB),
            label(r"economists blamed oil, \ unions and monopolies, \ and tried price controls (1971--74)",
                  font_size=22, color=WAGE),
            label(r"the Federal Reserve let money grow fast, \ and tightened only briefly", font_size=22, color=INFL),
            label(r"the deeper cause: \ a model without expectations, \ and a central bank under pressure",
                  font_size=22, color=EXPECT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Romer and Romer, \ ``The evolution of economic understanding and postwar "
                            r"stabilization policy'' (2002)", corner=DR, font_size=12)
        with self.voiceover(
            "Why did it happen? <bookmark mark='a'/> Policymakers chased an unemployment target that was too low. "
            "They believed full employment meant four percent or less, while the natural rate had risen, as the "
            "workforce grew younger and more varied. <bookmark mark='b'/> Many blamed oil, unions and big "
            "companies, and America tried wage and price controls from 1971 to 1974. They held prices down for a "
            "while, and then let them go. <bookmark mark='c'/> And the Federal Reserve let money grow quickly, "
            "tightening only briefly whenever inflation alarmed it. <bookmark mark='d'/> Christina and David Romer "
            "have argued that the deeper cause was the model policymakers used: one that left out expectations, "
            "and promised a trade-off that was not there."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
