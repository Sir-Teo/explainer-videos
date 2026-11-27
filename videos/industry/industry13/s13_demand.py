from __future__ import annotations

from videos.industry.industry13.common import *  # noqa: F403

UNAMES = {"DUK": "Duke", "SO": "Southern", "EXC": "Exelon", "XEL": "Xcel", "PCG": "PG&E", "SRE": "Sempra"}


class Demand(VoiceoverScene):
    def construct(self):
        card(self, 11, "The new load", "After fifteen flat years, why is America using more electricity?",
             "Chapter eleven. The new load.", lit=("change", "dollar"))
        self.growth()
        self.datacentres()
        self.build()

    def growth(self):
        D = R["demand"]
        g = D["growth"]
        ys = sorted(g)
        pa = viz.plot_axes([1999.3, 2026.7], [-4.5, 5], x_length=10.0, y_length=4.4, xticks=[2000, 2005, 2010, 2015, 2020, 2025],
                           yticks=[-4, -2, 0, 2, 4], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:+.0f}%" if v else "0",
                           ylabel="change in US electricity sales on the year before", size=14).move_to([-0.3, -0.5, 0])
        zero = Line(pa.ax.c2p(1999.3, 0), pa.ax.c2p(2026.7, 0), stroke_color=GREY_B, stroke_width=1.2)
        bars = VGroup()
        for y in ys:
            v = g[y]
            p0, p1 = pa.ax.c2p(y, 0), pa.ax.c2p(y, v)
            bars.add(Rectangle(width=0.26, height=max(abs(p1[1] - p0[1]), 0.01), stroke_width=0, fill_color=GOOD if v >= 0 else BAD,
                               fill_opacity=0.85).move_to([p0[0], (p0[1] + p1[1]) / 2, 0]))
        p0, p1 = pa.ax.c2p(D["ytd_year"], 0), pa.ax.c2p(D["ytd_year"], D["ytd"])
        ytd = Rectangle(width=0.26, height=p1[1] - p0[1], stroke_color=GOOD, stroke_width=2, fill_opacity=0).move_to([p0[0], (p0[1] + p1[1]) / 2, 0])
        yl = tx(f"{D['ytd_year']}, January-{['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November'][D['ytd_months']]}: {D['ytd']:+.1f}%",
                13, GOOD).move_to(pa.ax.c2p(2022.5, 4.6))
        flat = Rectangle(width=pa.ax.c2p(2021, 0)[0] - pa.ax.c2p(2007, 0)[0], height=4.4, stroke_width=0, fill_color=WHITE,
                         fill_opacity=0.05).move_to([(pa.ax.c2p(2021, 0)[0] + pa.ax.c2p(2007, 0)[0]) / 2, pa.ax.c2p(0, 0.25)[1], 0])
        fl = tx("2007-2021: no growth, on average", 14, GREY_B).next_to(flat, UP, buff=0.04)
        src = source("EIA, Monthly Energy Review, Table 7.6 (retail sales of electricity)", size=13)
        with self.voiceover(
            "Remember the flat line in the intermission. <bookmark mark='a'/> Year by year, American electricity sales "
            "rose a little and fell a little, and from 2007 to 2021 they went nowhere at all. <bookmark mark='b'/> Then "
            f"2022, up {g[2022]:.0f} per cent; 2024, up {g[2024]:.1f}; 2025, up {g[2025]:.1f}. <bookmark mark='c'/> And "
            f"in the first {D['ytd_months']} months of {D['ytd_year']}, about {D['ytd']:.0f} per cent more than a year "
            "before. For an industry that had spent fifteen years selling the same amount, that is a new world."
        ) as vo:
            self.play(FadeIn(pa), Create(zero), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN if g[y] >= 0 else UP) for b_, y in zip(bars, ys) if y <= 2021], lag_ratio=0.05),
                      FadeIn(flat), FadeIn(fl), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN if g[y] >= 0 else UP) for b_, y in zip(bars, ys) if y > 2021], lag_ratio=0.2),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(Create(ytd), FadeIn(yl))
        self.clear_scene()

    def datacentres(self):
        D = R["demand"]
        rack = VGroup(*[draw.server_rack(0.9) for _ in range(5)]).arrange(RIGHT, buff=0.15).move_to([-4.2, 2.2, 0]) if hasattr(draw, "server_rack") else VGroup()
        vals = [("2014", D["dc14"], None), ("2023", D["dc23"], None), ("2028?", D["dc28"], (D["dc28_lo"], D["dc28_hi"]))]
        bars = VGroup()
        for i, (lab, v, rng) in enumerate(vals):
            x = -3.0 + 2.2 * i
            if rng:
                lo = Rectangle(width=1.2, height=rng[0] / 600 * 4.2, stroke_width=0, fill_color=SUN, fill_opacity=0.7).move_to([x, -2.6, 0], aligned_edge=DOWN)
                hi = Rectangle(width=1.2, height=(rng[1] - rng[0]) / 600 * 4.2, stroke_color=SUN, stroke_width=2, fill_color=SUN,
                               fill_opacity=0.2).next_to(lo, UP, buff=0)
                b = VGroup(lo, hi)
                txt = tx(f"{rng[0]:.0f}-{rng[1]:.0f} TWh", 17, SUN, bold=True).next_to(hi, UP, buff=0.08)
            else:
                b = Rectangle(width=1.2, height=v / 600 * 4.2, stroke_width=0, fill_color=SUN, fill_opacity=0.85).move_to([x, -2.6, 0], aligned_edge=DOWN)
                txt = tx(f"{v:.0f} TWh", 17, SUN, bold=True).next_to(b, UP, buff=0.08)
            bars.add(VGroup(b, txt, tx(lab, 16, GREY_A).next_to([x, -2.6, 0], DOWN, buff=0.12)))
        notes = VGroup(tx("US data centres' electricity", 18, WHITE, bold=True),
                       tx(f"2023: about {D['dc_share']:.1f}% of all US electricity", 16, GREY_A),
                       tx("2028, the projection: 6.7% to 12%", 16, SUN, bold=True),
                       tx(f"for scale: electric vehicles, 2025: {D['ev']:.0f} TWh", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to(
            [4.9, 0.6, 0])
        src = source("US Department of Energy on LBNL's 2024 United States Data Center Energy Usage Report; EIA MER Table 7.6 (EVs)", size=12)
        with self.voiceover(
            "What changed? Part of the answer is data centres. <bookmark mark='a'/> In 2014, "
            f"America's data centres used about {D['dc14']:.0f} terawatt-hours. <bookmark mark='b'/> By 2023, about "
            f"{D['dc23']:.0f}, some {D['dc_share']:.1f} per cent of all the country's electricity, by the estimate of a "
            "national laboratory for the Department of Energy. <bookmark mark='c'/> And by 2028, it projected, between "
            f"{D['dc28_lo']:.0f} and {D['dc28_hi']:.0f} terawatt-hours: up to twelve per cent of the nation's power, "
            f"driven, the Department said, by investment in artificial intelligence. Electric vehicles, for comparison, used about {D['ev']:.0f} in 2025."
        ) as vo:
            self.play(FadeIn(rack), FadeIn(src), FadeIn(notes[0]))
            for m_, b_ in zip("abc", bars):
                vo.wait_until(m_)
                self.play(FadeIn(b_[0], shift=UP * 0.2), FadeIn(b_[1]), FadeIn(b_[2]))
                if m_ == "b":
                    self.play(FadeIn(notes[1]))
            self.play(FadeIn(notes[2:]))
        self.clear_scene()

    def build(self):
        D = R["demand"]
        cx = D["capex"]
        ys = sorted(cx)
        pa = viz.plot_axes([ys[0] - 0.6, ys[-1] + 0.6], [0, 75], x_length=8.0, y_length=4.4, xticks=ys, yticks=[20, 40, 60],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}bn", ylabel="capital spending, six utilities", size=13).move_to(
            [-1.8, -0.4, 0])
        bars = viz.year_bars(pa, ys, [cx[y] for y in ys], GOOD, width=0.55)
        labs = VGroup(*[tx(f"${cx[y]:.0f}bn", 13, GOOD).next_to(b_, UP, buff=0.05) for y, b_ in zip(ys, bars) if y in (ys[0], ys[-1])])
        who = tx(", ".join(UNAMES.get(t, t) for t in D["capex_who"]), 13, GREY_B).next_to(pa, DOWN, buff=0.15)
        notes = VGroup(tx(f"{ys[0]} to {ys[-1]}: +{100 * (cx[ys[-1]] / cx[ys[0]] - 1):.0f}%", 20, GOOD, bold=True),
                       tx("every dollar enters the rate base,", 16, GREY_A), tx("and earns the allowed return", 16, GREY_A),
                       tx("until customers have paid it back", 16, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.07).move_to([4.5, 0.6, 0])
        src = source("Forms 10-K via SEC XBRL (payments to acquire property, plant and equipment)", size=13)
        with self.voiceover(
            "And the utilities are building for it. <bookmark mark='a'/> Six big American utilities that report their "
            f"capital spending the same way spent about {cx[ys[0]]:.0f} billion dollars on plants and wires in {ys[0]}. "
            f"<bookmark mark='b'/> In {ys[-1]}, about {cx[ys[-1]]:.0f} billion. <bookmark mark='c'/> Remember chapter five: "
            "every dollar of that goes into the rate base and earns the allowed return, paid by customers for decades. "
            "New load is the best news a regulated utility has had in a generation, and the question for regulators is "
            "who pays: the data centres that cause it, or everyone."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(who))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[:-1]], lag_ratio=0.1), FadeIn(labs[0]), run_time=1.8)
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[-1], DOWN), FadeIn(labs[1]), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1:]))
        self.clear_scene()
