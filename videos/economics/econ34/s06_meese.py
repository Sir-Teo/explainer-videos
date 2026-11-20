from __future__ import annotations

from videos.economics.econ34.common import *  # noqa: F403


class Meese(VoiceoverScene):
    def construct(self):
        card(self, 5, r"The random walk", r"Can any model forecast exchange rates?", "Chapter five. The random walk.",
             lit={1983: r"Meese and Rogoff"}, scale=("market", "world"), horizon=("a month", "a year"))
        self.race()

    def race(self):
        M = load("meese")
        groups = (("h1", "1 month"), ("h3", "3 months"), ("h12", "12 months"))
        models = (("random walk", GREY_B), ("interest parity", USD), ("AR(1)", DEM))
        ax = plane([0.3, 3.7], [0.9, 1.1], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.6, y_length=4.4, xticks=[],
                   yticks=[0.9, 0.95, 1.0, 1.05, 1.1], ylabel=r"forecast error, \ relative to the random walk",
                   yfmt=lambda v: f"{v:.2f}", font_size=14)
        one = seg(ax, 0.3, 1.0, 3.7, 1.0, GREY_C, 1.2, dashed=True)
        bars, labs, nms = VGroup(), VGroup(), VGroup()
        for g, (key, nm) in enumerate(groups):
            for j, (mname, col) in enumerate(models):
                x = g + 1 + (j - 1) * 0.25
                v = M[key]["ratio"][mname]
                p0, p1 = ax.ax.c2p(x - 0.1, 0.9), ax.ax.c2p(x + 0.1, v)
                bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=col, fill_opacity=0.85,
                                   stroke_width=0).move_to((p0 + p1) / 2))
                labs.add(label(rf"{v:.3f}", font_size=13, color=col).next_to(bars[-1], UP, buff=0.04))
            nms.add(label(nm, font_size=16, color=GREY_A).next_to(ax.ax.c2p(g + 1, 0.9), DOWN, buff=0.12))
        key = VGroup(*[label(m, font_size=16, color=c) for m, c in models]).arrange(RIGHT, buff=0.4).next_to(
            ax, UP, buff=0.15)
        side = VGroup(
            label(r"forecasts made each month \\ from the data of the day, \\ 1990--2026, \\ pound, \ yen, \\ Canadian "
                  r"dollar, \ franc", font_size=17, color=GREY_A),
            label(rf"random walk: \ {M['h1']['rmse']['random walk']:.1f}\% \\ error at a month, \\ "
                  rf"{M['h12']['rmse']['random walk']:.1f}\% at a year", font_size=17, color=WHITE),
            label(r"no model gains \\ more than a fraction \\ of a percent", font_size=18, color=CRISIS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        head = label(r"Meese and Rogoff's horse race, \ rerun", font_size=24, color=E.ACCENT).to_edge(UP, buff=0.3)
        intro = VGroup(
            label(r"1983: \ the leading models, \ given the true values of everything they said mattered", font_size=24,
                  color=WHITE),
            label(r"against: \ `no change'", font_size=30, color=GREY_A),
            label(r"none won, \ at one to twelve months", font_size=26, color=CRISIS),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.2)
        tag = data_tag(r"FRED: \ end-of-month H.10 rates, \ OECD 3-month rates; \ this film", corner=DR, font_size=12)
        with self.voiceover(
            "If parity conditions explain so little, can anything forecast exchange rates? In 1983 Richard Meese "
            "and Kenneth Rogoff ran a horse race. They took the leading models of the day, gave them the actual "
            "values of everything the models said should matter, and asked them to forecast exchange rates one to "
            "twelve months ahead. None beat the simplest forecast of all: no change, the random walk. "
            "<bookmark mark='a'/> Here is the race rerun. Each month since 1990, for the pound, the yen, the "
            "Canadian dollar and the Swiss franc, three forecasts are made using only data available then: no "
            "change; <bookmark mark='p'/> the change interest parity predicts; <bookmark mark='r'/> and a statistical "
            "model fitted to the last ten years of monthly moves. <bookmark mark='b'/> The bars are each forecast's "
            "error relative to the random walk's. "
            "At one month, three months and a year, they are all within a fraction of a percent of one. "
            f"<bookmark mark='c'/> The random walk's own errors are {M['h1']['rmse']['random walk']:.1f} percent at "
            f"a month and {M['h12']['rmse']['random walk']:.1f} at a year. Forty years after Meese and Rogoff, their "
            "result still mostly stands: at short horizons, exchange rates behave like a random walk."
        ) as vo:
            self.play(FadeIn(head), FadeIn(intro, shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeOut(intro), FadeIn(ax), FadeIn(one), FadeIn(nms), FadeIn(key), FadeIn(side[0]))
            for mk, j in (("a", 0), ("p", 1), ("r", 2)):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[j::3]], lag_ratio=0.2), run_time=1.2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(lb) for lb in labs], lag_ratio=0.08), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.clear_scene()
