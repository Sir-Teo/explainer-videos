from __future__ import annotations

from videos.economics.econ61.common import *  # noqa: F403


def design_grid(kind: str, rows: int = 8, cols: int = 24, w: float = 0.2, h: float = 0.3, seed: int = 61):
    """City-periods as cells: rows are cities, columns hours; filled by design (user, switchback, city)."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    city_t = rng.permutation(rows) < rows // 2
    for r in range(rows):
        for c in range(cols):
            x, y = c * (w + 0.03), -r * (h + 0.05)
            if kind == "user":
                a = Rectangle(width=w / 2, height=h, stroke_width=0, fill_color=TEST, fill_opacity=0.9)
                b = Rectangle(width=w / 2, height=h, stroke_width=0, fill_color=GREY_C, fill_opacity=0.9)
                g.add(VGroup(a.move_to([x - w / 4, y, 0]), b.move_to([x + w / 4, y, 0])))
            else:
                on = (rng.random() < 0.5) if kind == "switchback" else city_t[r]
                g.add(Rectangle(width=w, height=h, stroke_width=0, fill_color=TEST if on else GREY_C,
                                fill_opacity=0.9).move_to([x, y, 0]))
    return g


class Interference(VoiceoverScene):
    def construct(self):
        card(self, 9, r"When units interfere", r"If treated riders take the drivers control riders would have had, "
             r"\ what does an A/B test measure?", "Chapter nine. When units interfere.",
             lit={2014: r"Blake and Coey", 2023: r"two-sided randomization"}, scale=("market",),
             horizon=("a day",))
        self.designs()
        self.results()

    def designs(self):
        S = load("switchback")
        grids = [design_grid(k) for k in ("user", "switchback", "city")]
        names = (r"by user: \ half the riders in every city and hour", r"switchback: \ whole city-hours, \ at "
                 r"random", r"by city: \ whole cities, \ for the whole test")
        for g in grids:
            g.move_to(DOWN * 0.6 + LEFT * 2.0)
        heads = [label(n, font_size=21, color=TEST).next_to(grids[0], UP, buff=0.3) for n in names]
        axl = VGroup(label(r"cities", font_size=16, color=GREY_A).rotate(PI / 2).next_to(grids[0], LEFT, buff=0.15),
                     label(r"hours $\to$", font_size=16, color=GREY_A).next_to(grids[0], DOWN, buff=0.15))
        key = VGroup(label(r"pink: \ discount", font_size=17, color=TEST), label(r"grey: \ no discount",
                                                                                 font_size=17, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(grids[0], RIGHT, buff=0.4)
        facts = VGroup(
            label(rf"drivers are shared: \ about {S['drivers']:.0f} an hour in a city, \ for "
                  rf"{S['demand_off']:.0f} riders who want a ride", font_size=19, color=DRIVER),
            label(rf"a 20\% discount raises that to {S['demand_on']:.0f}: \ more riders than drivers", font_size=19,
                  color=TEST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(UP, buff=0.45)
        tag = island_tag(r"the Island: \ 20 cities, \ 48 hours, \ 300 riders a city-hour; \ "
                         r"agora.platform.switchback", corner=DL, font_size=12)
        with self.voiceover(
            "Part sixty's hotel rooms come back as drivers. The Island tests a twenty percent discount for "
            f"riders. <bookmark mark='a'/> In each city, about {S['drivers']:.0f} drivers an hour serve riders of "
            f"whom {S['demand_off']:.0f} want a ride at the normal fare; the discount raises that to "
            f"{S['demand_on']:.0f}, more than there are drivers. <bookmark mark='b'/> Design one, the ordinary A/B "
            "test: in every city and every hour, half the riders get the discount. But the discounted riders "
            "request more, and the drivers they take are drivers the other riders would have had. The control "
            "group is not what the world would look like without the discount; it is worse. <bookmark mark='c'/> "
            "Design two, the switchback: whole city-hours get the discount or not, at random, so within any hour "
            "everyone shares the same treatment. <bookmark mark='d'/> Design three: whole cities, for the whole "
            "test."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(facts))
            vo.wait_until("b")
            self.play(FadeIn(heads[0]), FadeIn(grids[0]), FadeIn(axl), FadeIn(key))
            vo.wait_until("c")
            self.play(ReplacementTransform(grids[0], grids[1]), ReplacementTransform(heads[0], heads[1]))
            vo.wait_until("d")
            self.play(ReplacementTransform(grids[1], grids[2]), ReplacementTransform(heads[1], heads[2]))
        self.clear_scene()

    def results(self):
        S = load("switchback")
        keys = ("user", "switchback", "city")
        names = (r"by user", r"switchback", r"by city")
        vals = [100 * S[k] for k in keys]
        sds = [100 * S[k + "_sd"] for k in keys]
        truth = 100 * S["truth"]
        ax = plane([-0.6, 2.6], [0, 22], center=LEFT * 3.0 + DOWN * 0.4, x_length=6.0, y_length=4.6, xticks=[],
                   yticks=[0, 5, 10, 15, 20], ylabel=r"rides per 100 riders, \ effect of the discount",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        cols = (SURGE, TEST, TEST)
        b = bars(ax, range(3), vals, cols, width=0.5)
        errs = VGroup(*[Line(ax.ax.c2p(k, v - 2 * s), ax.ax.c2p(k, v + 2 * s), color=WHITE, stroke_width=2.4)
                        for k, (v, s) in enumerate(zip(vals, sds))])
        labs = VGroup(*[label(n, font_size=16, color=c).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.12)
                        for k, (n, c) in enumerate(zip(names, cols))])
        tl = DashedLine(ax.ax.c2p(-0.5, truth), ax.ax.c2p(2.5, truth), color=TRUE, stroke_width=2.4)
        tll = label(rf"the truth: \ +{truth:.1f}", font_size=16, color=TRUE).next_to(ax.ax.c2p(2.5, truth), UP,
                                                                                     buff=0.08).shift(LEFT * 0.6)
        side = VGroup(
            label(rf"by user: \ +{vals[0]:.1f}, \ {S['naive_ratio']:.1f} times the truth", font_size=20, color=SURGE),
            label(rf"switchback: \ +{vals[1]:.1f}, \ give or take {2 * sds[1]:.1f}", font_size=20, color=TEST),
            label(rf"by city: \ +{vals[2]:.1f}, \ give or take {2 * sds[2]:.1f}", font_size=20, color=TEST),
            label(r"the price of a clean comparison: \ fewer, \ noisier units", font_size=19, color=WHITE),
            label(r"switchbacks need hours long enough for drivers to settle, \\ or one hour's treatment leaks into "
                  r"the next", font_size=18, color=GREY_A),
            label(r"two-sided randomization: \ treat riders and drivers \\ separately, \ and compare the cells",
                  font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ 400 runs of each design; \ bars: \ mean, \ lines: \ $\pm$2 sd", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Here is what each design reports, averaged over four hundred runs, against the truth: the extra "
            "rides per hundred riders if everyone got the discount. <bookmark mark='a'/> The A/B test by user "
            f"says {vals[0]:.1f} more rides per hundred riders, {S['naive_ratio']:.1f} times the truth, because "
            "most of the discounted riders' extra rides were taken from the control riders, not created. "
            f"<bookmark mark='b'/> The switchback finds {vals[1]:.1f}, give or take {2 * sds[1]:.1f}, <bookmark "
            f"mark='c'/> and the city test {vals[2]:.1f}, give or take {2 * sds[2]:.1f}: centred on the truth, "
            f"{truth:.1f}, but noisier, since twenty cities are only twenty units. <bookmark mark='d'/> That is the "
            "trade: a clean comparison costs units. <bookmark mark='e'/> Switchbacks have their own catch: hours "
            "must be long enough for drivers to settle, or one hour's discount leaks into the next through "
            "where the drivers are. <bookmark mark='f'/> Platforms now also randomize both sides at once, "
            "riders and drivers or buyers and listings separately, and compare the four cells to see the "
            "interference itself: two-sided randomization, studied by Ramesh Johari and colleagues and by "
            "Patrick Bajari and colleagues at Amazon."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(tag), Create(tl), FadeIn(tll))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[k], DOWN), Create(errs[k]), FadeIn(side[k]))
            for k, mk in enumerate("def"):
                vo.wait_until(mk)
                self.play(FadeIn(side[3 + k]))
        self.clear_scene()
