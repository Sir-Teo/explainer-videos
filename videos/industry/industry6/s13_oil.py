from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry6.common import *  # noqa: F403


def derrick(h=1.4, color="#C9D3E0"):
    legs = VGroup(Line([-0.3 * h, 0, 0], [0, h, 0]), Line([0.3 * h, 0, 0], [0, h, 0])).set_stroke(color, 3)
    bars = VGroup(*[Line([-0.3 * h * (1 - f), f * h, 0], [0.3 * h * (1 - f), f * h, 0]).set_stroke(color, 2)
                    for f in (0.25, 0.5, 0.75)])
    cross = VGroup(Line([-0.3 * h, 0, 0], [0.15 * h, 0.5 * h, 0]), Line([0.3 * h, 0, 0], [-0.15 * h, 0.5 * h, 0])
                   ).set_stroke(color, 1.5)
    base = Rectangle(width=0.8 * h, height=0.06 * h, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
        [0, -0.03 * h, 0])
    return VGroup(legs, bars, cross, base)


def _x(month: str) -> float:
    return int(month[:4]) + (int(month[5:7]) - 0.5) / 12


class Oil(VoiceoverScene):
    def construct(self):
        card(self, 12, "Oil", "What does a company do when the price halves?",
             "Chapter twelve. Oil.", lit=("change", "make"))
        O = R["oil"]
        pa = viz.plot_axes([2005, 2026.9], [0, 150], x_length=10.2, y_length=2.6, yticks=[50, 100],
                           yfmt=lambda v: f"${v:g}", size=15)
        pa.move_to([0.6, 1.25, 0])
        pts = [(x, v) for x, v in ((_x(k), v) for k, v in zip(O["months"], O["wti"])) if x >= 2005]
        line = VMobject(stroke_color=PRICE, stroke_width=3).set_points_as_corners([pa.ax.c2p(x, v) for x, v in pts])
        lt = tx("price of a barrel of West Texas crude, each month", 16, PRICE).next_to(pa, UP, buff=0.08).align_to(
            pa, LEFT)
        pb = viz.plot_axes([2005, 2026.9], [0, 40], x_length=10.2, y_length=2.1, xticks=[2006, 2010, 2014, 2018, 2022, 2026],
                           yticks=[20, 40], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}bn", size=15)
        pb.move_to([0.6, -2.15, 0])
        bars = viz.year_bars(pb, [y + 0.5 for y in O["xom_years"]], O["xom_capex"], ORDER, width=0.42)
        bt = tx("Exxon Mobil's spending on new wells, plants and equipment, each year", 16, ORDER).next_to(
            pb, UP, buff=0.08).align_to(pb, LEFT)
        rigs = VGroup(*[derrick(0.6) for _ in range(5)]).arrange(RIGHT, buff=0.22).move_to([4.6, 3.3, 0])
        hi = glow_dot(pa.ax.c2p(_x("2014-06"), O["wti_2014_06"]), color=PRICE, radius=0.09)
        lo = glow_dot(pa.ax.c2p(_x("2016-02"), O["wti_2016_02"]), color=BUST, radius=0.09)
        hl = tx(f"${O['wti_2014_06']:.0f}, June 2014", 15, PRICE).next_to(hi, UP, buff=0.08)
        ll = tx(f"${O['wti_2016_02']:.0f}, February 2016", 15, BUST).next_to(lo, DOWN, buff=0.08)
        cap = dict(zip(O["xom_years"], O["xom_capex"]))
        src = source("EIA via FRED (WTI, monthly average); EIA (US crude output); Exxon Mobil Forms 10-K", size=13)
        with self.voiceover(
            "Oil runs on the same loop, with one more twist: the price is set for the whole world at once. "
            "<bookmark mark='a'/> For most of 2011 to 2014, a barrel of American crude sold for around a hundred "
            "dollars. <bookmark mark='b'/> The oil companies did what high prices tell them to do. Exxon Mobil, the "
            f"largest American one, spent {cap[2012]:.0f} billion dollars in 2012 on new wells, platforms and "
            "plants. Drillers opened up America's shale fields, and the country's output of crude rose from "
            f"{get('eia.crude.2010'):.1f} million barrels a day in 2010 to {get('eia.crude.2015'):.1f} million in "
            "2015. <bookmark mark='c'/> The new oil arrived. In June 2014 a barrel cost "
            f"{O['wti_2014_06']:.0f} dollars; by February 2016, {O['wti_2016_02']:.0f}. <bookmark mark='d'/> Exxon "
            f"cut its spending to {cap[2016]:.0f} billion, less than half. Then came the pandemic: in April 2020, "
            f"with the world's roads emptied, a barrel averaged {O['wti_2020_04']:.0f} dollars for the month, and "
            f"Exxon's spending fell to {cap[2021]:.0f} billion the year after. <bookmark mark='e'/> Spending stayed low, and when Russia invaded Ukraine in 2022, "
            "the price shot back above a hundred dollars. The spending has been climbing ever since. Each turn of "
            "the wheel is set up by the one before."
        ) as vo:
            self.play(FadeIn(src), LaggedStart(*[FadeIn(r_, shift=UP * 0.2) for r_ in rigs], lag_ratio=0.15),
                      FadeIn(pa), FadeIn(lt), run_time=1.8)
            vo.wait_until("a")
            self.play(Create(line), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(pb), FadeIn(bt), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[:6]],
                                                          lag_ratio=0.15), run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(hi, scale=2), FadeIn(hl))
            self.play(FadeIn(lo, scale=2), FadeIn(ll), rigs[2:].animate.set_opacity(0.25))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[6:13]], lag_ratio=0.15), run_time=1.8)
            c19 = glow_dot(pa.ax.c2p(_x("2020-04"), O["wti_2020_04"]), color=BUST, radius=0.09)
            self.play(FadeIn(c19, scale=2), FadeIn(tx(f"${O['wti_2020_04']:.0f}, April 2020", 15, BUST).next_to(
                c19, DOWN, buff=0.08)))
            vo.wait_until("e")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[13:]], lag_ratio=0.2),
                      rigs.animate.set_opacity(1), run_time=1.8)
        self.clear_scene()
