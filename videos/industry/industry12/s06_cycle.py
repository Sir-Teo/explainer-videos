from __future__ import annotations

from videos.industry.industry12.common import *  # noqa: F403


class Cycle(VoiceoverScene):
    def construct(self):
        card(self, 5, "The commodity cycle", "If everyone sees the same fat margins, what happens four years later?",
             "Chapter five. The commodity cycle.", lit=("change", "dollar"))
        self.wave()
        self.utilization()
        self.resins()
        self.profits()

    def wave(self):
        u = ValueTracker(93.0)
        m = ValueTracker(600.0)
        yr = ValueTracker(1)
        xs = [-6.0, -4.6, -3.2, -1.8, -0.4, 1.0]
        old = VGroup(*[draw.cracker_unit(1.25).move_to([x, -1.9, 0]) for x in xs[:3]])
        plots = VGroup(*[DashedVMobject(Rectangle(width=1.2, height=0.6, stroke_color=GREY_C, stroke_width=1.5), num_dashes=24
                                        ).move_to([x, -2.3, 0]) for x in xs[3:]])
        firms = VGroup(*[tx(n_, 13, GREY_A).move_to([x, -2.95, 0]) for n_, x in zip("ABCDEF", xs)])
        cranes = VGroup(*[draw.crane(1.2, "#F2C14E").move_to([x, -1.9, 0]) for x in xs[3:]])
        new = VGroup(*[draw.cracker_unit(1.25).move_to([x, -1.9, 0]) for x in xs[3:]])
        ground = Line([-6.9, -2.62, 0], [1.8, -2.62, 0], stroke_color=GREY_D, stroke_width=2)
        g = draw.gauge(u, 70, 100, r=1.1, bands=((BAD, 0.34), (PRICE, 0.67), (GOOD, 1.0))).move_to([4.6, 1.5, 0])
        gl = draw.number(lambda: u.get_value(), 0, suffix="% full", size=26, color=WHITE).next_to(g, DOWN, buff=0.15)
        gt = tx("how full the plants run", 15, GREY_A).next_to(g, UP, buff=0.1)
        base = -2.6

        def bar():
            h = max(m.get_value(), 0) / 700 * 2.0
            col = GOOD if m.get_value() > 300 else BAD
            return Rectangle(width=1.0, height=max(h, 0.01), stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                [4.6, base, 0], aligned_edge=DOWN)
        mb = always_redraw(bar)
        ml = draw.number(lambda: m.get_value(), 0, prefix="$", size=24, color=WHITE)
        ml.add_updater(lambda x_: x_.next_to(mb, UP, buff=0.1))
        mt = tx("margin a tonne", 15, GREY_A).move_to([4.6, base - 0.3, 0])
        ycount = draw.memo_redraw(lambda: int(round(yr.get_value())), lambda k: tx(f"year {k}", 28, GOLD, bold=True),
                                  lambda mob: mob.move_to([-2.5, 2.9, 0]))
        tag = estimate_tag("illustration: stylised numbers, the pattern and not any real market", corner=DR, size=12)
        with self.voiceover(
            "Part 6 of this series showed how an industry that builds slowly, and orders by today's price, swings. "
            "Petrochemicals are the purest case. <bookmark mark='a'/> Picture six companies, three with crackers "
            "running, in a year when the plants are full and margins are fat. <bookmark mark='b'/> Every one of them "
            "sees the same numbers, and three decide to build. <bookmark mark='c'/> A cracker takes years. While they "
            "are being built, demand keeps growing, the plants stay full, and the margins stay fat, which only seems "
            "to prove the decision right. <bookmark mark='d'/> Then they all start up within a year or two of each "
            "other. Capacity jumps far ahead of demand, the plants run part-empty, and the margin collapses. "
            "<bookmark mark='e'/> Now nobody builds. Demand grows into the new capacity, year by year, until the "
            "plants are full again, the margins are fat again, and everyone sees the same numbers."
        ) as vo:
            self.play(FadeIn(ground), FadeIn(firms), FadeIn(plots), FadeIn(g), FadeIn(gl), FadeIn(gt), FadeIn(mb), FadeIn(ml),
                      FadeIn(mt), FadeIn(tag), FadeIn(ycount), FadeIn(old))
            vo.wait_until("a")
            self.play(LaggedStart(*[Indicate(o_, color=GOOD, scale_factor=1.08) for o_ in old], lag_ratio=0.2), run_time=1.2)
            vo.wait_until("b")
            ann = tx("D, E and F announce new crackers", 18, PRICE, bold=True).move_to([-2.5, 2.2, 0])
            self.play(LaggedStart(*[FadeIn(c_, shift=DOWN * 0.3) for c_ in cranes], lag_ratio=0.3), FadeIn(ann), run_time=1.5)
            vo.wait_until("c")
            self.play(yr.animate.set_value(4), u.animate.set_value(96), m.animate.set_value(650),
                      *[Wiggle(c_, scale_value=1.03, rotation_angle=0.01 * TAU) for c_ in cranes], run_time=4.0, rate_func=linear)
            vo.wait_until("d")
            ann2 = tx("all three start up at once", 18, BAD, bold=True).move_to(ann)
            self.play(FadeOut(cranes), FadeIn(new, shift=UP * 0.2), FadeTransform(ann, ann2), yr.animate.set_value(5), run_time=1.2)
            self.play(u.animate.set_value(78), m.animate.set_value(60), run_time=2.0)
            ann = ann2
            vo.wait_until("e")
            ann3 = tx("nobody builds; demand catches up", 18, GOOD, bold=True).move_to(ann)
            self.play(FadeTransform(ann, ann3), run_time=0.8)
            self.play(yr.animate.set_value(10), u.animate.set_value(93), m.animate.set_value(600), run_time=5.0, rate_func=linear)
        for mob in (gl, ml):
            mob.clear_updaters()
        self.clear_scene()

    def utilization(self):
        cu = R["cycle"]["cap_util"]
        ys = sorted(cu)
        pa = viz.plot_axes([ys[0] - 0.5, ys[-1] + 0.5], [60, 92], x_length=10.4, y_length=4.4,
                           xticks=[1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020], yticks=[65, 70, 75, 80, 85, 90],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}%", ylabel="capacity in use, annual average",
                           size=14).move_to([0, -0.5, 0])
        line = VMobject(stroke_color=ETHYL, stroke_width=3).set_points_as_corners([pa.ax.c2p(y, cu[y]) for y in ys])
        lows = [y for y in ys[1:-1] if cu[y] < cu[y - 1] and cu[y] < cu[y + 1] and cu[y] < 72.5]
        marks = VGroup()
        for y in lows:
            d_ = Dot(pa.ax.c2p(y, cu[y]), radius=0.06, color=BAD)
            marks.add(VGroup(d_, tx(f"{y}: {cu[y]:.0f}%", 13, BAD).next_to(d_, DOWN, buff=0.08)))
        hi_y = max((y for y in ys if y >= 2015), key=lambda y: cu[y])
        hd = Dot(pa.ax.c2p(hi_y, cu[hi_y]), radius=0.06, color=GOOD)
        hl = tx(f"{hi_y}: {cu[hi_y]:.0f}%", 13, GOOD).next_to(hd, UP, buff=0.08)
        head = tx(f"America's chemical plants: how full, {ys[0]}-{ys[-1]}", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("Federal Reserve Board, G.17: capacity utilization, chemicals (NAICS 325), via FRED", size=13)
        with self.voiceover(
            "Here is the real thing, as far back as the Federal Reserve's figures go. This is how much of America's "
            "chemical capacity was in use each year, from 1948. <bookmark mark='a'/> It covers medicines and soaps "
            "as well as petrochemicals, so it averages a lot out. Even so, it swings. <bookmark mark='b'/> The deepest "
            "troughs: " + ", ".join(f"{y}" for y in lows[:-1]) + f" and {lows[-1]}. The worst was {min(lows, key=lambda y: cu[y])}, "
            f"when only {min(cu[y] for y in lows):.0f} per cent of the capacity was used. <bookmark mark='c'/> And {hi_y}, when demand came back from the pandemic "
            f"faster than plants could follow, at {cu[hi_y]:.0f} per cent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(pa))
            self.play(Create(line), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(k_, scale=0.6) for k_ in marks], lag_ratio=0.25), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(hd, scale=0.6), FadeIn(hl))
        self.clear_scene()

    def resins(self):
        rs = R["cycle"]["resins"]
        ys = sorted(rs)
        pa = viz.plot_axes([ys[0] - 0.5, ys[-1] + 0.5], [0, 400], x_length=10.0, y_length=4.4,
                           xticks=[1980, 1990, 2000, 2010, 2020], yticks=[100, 200, 300, 400], xfmt=lambda v: f"{int(v)}",
                           yfmt=lambda v: f"{v:.0f}", ylabel="producer price index, 1982 = 100", size=14).move_to([-0.3, -0.5, 0])
        line = VMobject(stroke_color=PLASTIC, stroke_width=3).set_points_as_corners([pa.ax.c2p(y, rs[y]) for y in ys])
        jumps = sorted(((rs[y] / rs[y - 1] - 1, y) for y in ys[1:]), reverse=True)[:3]
        falls = sorted((rs[y] / rs[y - 1] - 1, y) for y in ys[1:])[:3]
        marks = VGroup()
        for ch, y in jumps + falls:
            col = BAD if ch > 0 else GOOD
            d_ = Dot(pa.ax.c2p(y, rs[y]), radius=0.06, color=col)
            lab = tx(f"{y}: {100 * ch:+.0f}%", 13, col).next_to(d_, UP if ch > 0 else DOWN, buff=0.08)
            marks.add(VGroup(d_, lab))
        j1, y1 = jumps[0]
        head = tx("What American makers charged for plastic resins", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("US Bureau of Labor Statistics, PPI: plastics material and resin manufacturing, via FRED", size=13)
        with self.voiceover(
            "The swings show up in prices. <bookmark mark='a'/> This is what American plants charged for plastic resins, "
            "polyethylene and the rest, since 1977. <bookmark mark='b'/> Year to year it jumps and falls by ten, "
            "twenty, even thirty per cent. The biggest rise in this record was "
            f"{y1}: {100 * j1:.0f} per cent in a single year. For a business that runs on margins of a few hundred "
            "dollars a tonne, those swings decide whether the year is a bonanza or a loss."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(pa))
            vo.wait_until("a")
            self.play(Create(line), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(k_, scale=0.6) for k_ in marks], lag_ratio=0.2), run_time=2.0)
        self.clear_scene()

    def profits(self):
        nets = R["cycle"]["nets"]
        names = {"DOW": "Dow", "LYB": "LyondellBasell", "WLK": "Westlake", "OLN": "Olin", "LIN": "Linde", "SHW": "Sherwin-Williams"}
        ys = list(range(2014, 2026))
        panels = VGroup()
        for i, t in enumerate(("DOW", "LYB", "WLK", "OLN")):
            d = nets[t]
            top = max(max(d.values()), 1.0)
            bot = min(min(d.values()), -0.5)
            h = 2.0
            sc = h / (top - bot)
            x0 = -6.4 + 3.2 * i
            zero_y = 0.6 + (-bot) * sc - h / 2
            bars = VGroup()
            bars.years = []
            for k, y in enumerate(ys):
                v = d.get(y)
                if v is None:
                    continue
                r_ = Rectangle(width=0.17, height=max(abs(v) * sc, 0.01), stroke_width=0, fill_color=GOOD if v >= 0 else BAD,
                               fill_opacity=0.9)
                r_.move_to([x0 + 0.2 + 0.22 * k, zero_y, 0], aligned_edge=DOWN if v >= 0 else UP)
                bars.add(r_)
                bars.years.append(y)
            axis = Line([x0, zero_y, 0], [x0 + 2.85, zero_y, 0], stroke_color=GREY_C, stroke_width=1.2)
            nm = tx(names[t], 17, WHITE, bold=True).move_to([x0 + 1.45, 2.3, 0])
            y21 = tx(f"2021: ${d[2021]:.1f}bn", 13, GOOD).move_to([x0 + 1.45, -0.85, 0])
            y25 = tx(f"2025: {'−' if d[2025] < 0 else ''}${abs(d[2025]):.1f}bn", 13, BAD if d[2025] < 0 else GOOD).next_to(
                y21, DOWN, buff=0.06)
            panels.add(VGroup(axis, bars, nm, y21, y25))
        yrs = tx(f"each bar a year, {ys[0]}-{ys[-1]}: net income, each company on its own scale", 14, GREY_A).move_to([0, 2.85, 0])
        t21 = sum(nets[t][2021] for t in ("DOW", "LYB", "WLK", "OLN"))
        t25 = sum(nets[t][2025] for t in ("DOW", "LYB", "WLK", "OLN"))
        tot = VGroup(tx(f"Together: ${t21:.1f}bn of profit in 2021", 20, GOOD, bold=True),
                     tx(f"{'a loss of' if t25 < 0 else ''} ${abs(t25):.1f}bn in 2025", 20, BAD, bold=True)).arrange(
            RIGHT, buff=0.5).move_to([0, -2.4, 0])
        head = tx("Four commodity chemical makers", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Form 10-K filings via SEC XBRL (net income attributable to the company)", size=13)
        with self.voiceover(
            "And they decide the profits. <bookmark mark='a'/> Here are four American makers of commodity chemicals, "
            "each bar a year of net income: Dow, LyondellBasell, Westlake and Olin. <bookmark mark='b'/> In 2021, with "
            f"the plants full, the four made about {t21:.0f} billion dollars between them. <bookmark mark='c'/> In 2025, "
            f"with the plants less full and margins thin, they lost about {abs(t25):.0f} billion between them, "
            "counting the write-downs that come with bad years. Same plants, same people, four years apart. "
            "<bookmark mark='d'/> Not every chemical business lives like this. The next chapters go down other "
            "branches of the tree: fertilizer, which rides the price of gas; the gas companies, which almost never "
            "lose; and the paint makers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(yrs))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(p_[0]), FadeIn(p_[2]),
                                                   LaggedStart(*[GrowFromEdge(b_, DOWN if b_.get_center()[1] > p_[0].get_center()[1] else UP)
                                                                 for b_ in p_[1]], lag_ratio=0.08))
                                    for p_ in panels], lag_ratio=0.3), run_time=4.0)
            vo.wait_until("b")
            self.play(*[FadeIn(p_[3]) for p_ in panels], *[Indicate(p_[1][p_[1].years.index(2021)], color=GOOD) for p_ in panels], FadeIn(tot[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(p_[4]) for p_ in panels], *[Indicate(p_[1][p_[1].years.index(2025)], color=BAD) for p_ in panels], FadeIn(tot[1]))
        self.clear_scene()
