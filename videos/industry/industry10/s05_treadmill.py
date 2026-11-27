from __future__ import annotations

from videos.industry.industry10.common import *  # noqa: F403


class Treadmill(VoiceoverScene):
    def construct(self):
        card(self, 4, "The treadmill", "Why does growing more not make farmers richer?",
             "Chapter four. The treadmill.", lit=("change", "moat"))
        self.model()
        self.evidence()

    def model(self):
        T = R["treadmill"]["model"]
        years = len(T["share"])
        cells = VGroup(*[Square(0.34, stroke_color=BACKGROUND, stroke_width=2, fill_color="#5E6B4A", fill_opacity=1)
                         for _ in range(100)]).arrange_in_grid(rows=10, cols=10, buff=0.0).move_to([-4.2, -0.1, 0])
        order = list(np.random.default_rng(3).permutation(100))
        t = ValueTracker(0)

        def paint(g):
            k = int(round(np.interp(t.get_value(), range(years), T["share"]) * 100))
            on = set(order[:k])
            for i, c in enumerate(g):
                c.set_fill(FARM if i in on else "#5E6B4A")
        cells.add_updater(paint)
        grid_l = VGroup(tx("100 farms", 18, WHITE, bold=True),
                        VGroup(Square(0.18, stroke_width=0, fill_color=FARM, fill_opacity=1), tx("using the new method", 14, GREY_A)
                               ).arrange(RIGHT, buff=0.08)).arrange(DOWN, buff=0.08).next_to(cells, UP, buff=0.2)
        pa = viz.plot_axes([0, years - 1], [0.7, 1.25], x_length=5.6, y_length=2.1, xticks=[0, 10, 20, 29],
                           yticks=[0.8, 1.0, 1.2], xfmt=lambda v: f"year {int(v)}", yfmt=lambda v: f"{v:.1f}", size=12).move_to(
            [2.9, 1.85, 0])
        pb = viz.plot_axes([0, years - 1], [-0.2, 0.32], x_length=5.6, y_length=2.1, xticks=[0, 10, 20, 29],
                           yticks=[-0.1, 0, 0.1, 0.2, 0.3], xfmt=lambda v: f"year {int(v)}", yfmt=lambda v: f"{100 * v:+.0f}%",
                           size=12).move_to([2.9, -1.55, 0])
        z = Line(pb.ax.c2p(0, 0), pb.ax.c2p(years - 1, 0), stroke_color=GREY_B, stroke_width=1.2)

        def curve(ax, ys, col):
            def f():
                n = int(t.get_value()) + 1
                q = [ax.ax.c2p(i, ys[i]) for i in range(min(n, years))]
                return VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(q) if len(q) > 1 else VMobject()
            return always_redraw(f)
        price = curve(pa, T["price"], PRICE)
        out = curve(pa, T["output"], WHITE)
        adopt = curve(pb, T["adopter"], FARM)
        lag = curve(pb, T["laggard"], STATE)
        la = VGroup(tx("output", 14, WHITE), tx("price", 14, PRICE)).arrange(RIGHT, buff=0.3).next_to(pa, UP, buff=0.08)
        lb = VGroup(tx("profit of an early adopter", 14, FARM), tx("of a farmer who never adopts", 14, STATE)).arrange(
            RIGHT, buff=0.3).next_to(pb, UP, buff=0.08)
        yr = draw.number(lambda: t.get_value(), 0, prefix="year ", size=26, color=GREY_A)
        yr.add_updater(lambda m: m.next_to(cells, DOWN, buff=0.25))
        yr.update()
        tag = estimate_tag("the Works (farm.py): a method that grows 12% more on the same costs; demand elasticity -0.4",
                           corner=DR, size=13)
        src = source("after Willard Cochrane, Farm Prices: Myth and Reality (1958)", size=13)
        with self.voiceover(
            "In 1958, the agricultural economist Willard Cochrane described what he called the treadmill. Here it is as "
            "a model. <bookmark mark='a'/> A hundred farms grow the same crop. A new method arrives, a better seed, "
            "say, that grows twelve percent more on the same costs. <bookmark mark='b'/> The first farmers to adopt it "
            "do very well. They grow more, and the price has not moved yet, because they are only a few. "
            "<bookmark mark='c'/> So their neighbours copy them, and output rises across the whole market. But people "
            "do not eat much more bread or corn because there is more of it, so to sell the extra, the price must fall, "
            "and fall a long way. <bookmark mark='d'/> By the time everyone has adopted, the price has fallen so far "
            "that the early adopters' extra profit is gone. And the farmers who never adopted are now losing money on "
            "every acre. They sell out to their neighbours, and farms get bigger and fewer. "
            "<bookmark mark='e'/> Then another new method arrives, and the treadmill turns again. The gains from all "
            "that ingenuity do not stay with farmers. They pass, through lower prices, to everyone who eats."
        ) as vo:
            self.play(FadeIn(cells), FadeIn(grid_l), FadeIn(src), FadeIn(tag), FadeIn(yr))
            vo.wait_until("a")
            self.play(FadeIn(pa), FadeIn(pb), Create(z), FadeIn(la), FadeIn(lb))
            self.add(price, out, adopt, lag)
            vo.wait_until("b")
            self.play(t.animate.set_value(6), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            self.play(t.animate.set_value(14), run_time=5.0, rate_func=linear)
            vo.wait_until("d")
            self.play(t.animate.set_value(years - 1), run_time=5.0, rate_func=linear)
            vo.wait_until("e")
            self.play(Indicate(lb[1], color=STATE))
        for m in (cells, price, out, adopt, lag, yr):
            m.clear_updaters()
        self.clear_scene()

    def evidence(self):
        Tr = R["treadmill"]
        um = Tr["us_maize"]
        pa = viz.plot_axes([1866, 2025], [0, 12.5], x_length=5.6, y_length=3.0, xticks=[1866, 1900, 1950, 2000, 2025],
                           yticks=[4, 8, 12], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g} t", size=13).move_to(
            [-3.4, 1.1, 0])
        yl = VMobject(stroke_color=CORN, stroke_width=3).set_points_as_corners([pa.ax.c2p(y, v) for y, v in um.items()])
        yt = tx("US corn harvested per hectare, since 1866", 16, CORN, bold=True).next_to(pa, UP, buff=0.1)
        ann = VGroup(tx("70 years flat", 13, GREY_A).move_to(pa.ax.c2p(1900, 3.2)),
                     tx("hybrid seed", 13, GREY_A).next_to(pa.ax.c2p(1945, 2.4), UP, buff=0.35),
                     tx(f"x{Tr['maize_x30']:.0f}", 20, CORN, bold=True).next_to(pa.ax.c2p(2025, um[2024]), LEFT, buff=0.15).shift(
                         UP * 0.3))
        rp = Tr["real_maize"]
        pb = viz.plot_axes([1992, 2025], [0, 9], x_length=5.4, y_length=3.0, xticks=[1995, 2005, 2015, 2025],
                           yticks=[3, 6, 9], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}", size=13).move_to([3.6, 1.1, 0])
        pl = VMobject(stroke_color=PRICE, stroke_width=3).set_points_as_corners([pb.ax.c2p(y, v) for y, v in rp.items()])
        pt = tx(f"a bushel of corn, in dollars of {mlabel(Tr['cpi_month'])}", 16, PRICE, bold=True).next_to(pb, UP, buff=0.1)
        f35 = VGroup(*[Square(0.11, stroke_width=0, fill_color=FARM, fill_opacity=1) for _ in range(68)]).arrange_in_grid(
            rows=4, cols=17, buff=0.04)
        f25 = VGroup(*[Square(0.11 * np.sqrt(Tr["acres_2025"] / Tr["acres_1935"]), stroke_width=0, fill_color=FARM,
                              fill_opacity=1) for _ in range(19)]).arrange_in_grid(rows=2, cols=10, buff=0.04)
        g35 = VGroup(tx("1935", 18, WHITE, bold=True), f35, tx(f"{Tr['farms_1935']:.2f} million farms,", 15, GREY_A),
                     tx(f"{Tr['acres_1935']:.0f} acres each", 15, GREY_A)).arrange(DOWN, buff=0.08).move_to([-3.2, -2.2, 0])
        g25 = VGroup(tx("2025", 18, WHITE, bold=True), f25, tx(f"{Tr['farms_2025']:.2f} million farms,", 15, GREY_A),
                     tx(f"{Tr['acres_2025']:.0f} acres each", 15, GREY_A)).arrange(DOWN, buff=0.08).move_to([3.4, -2.2, 0])
        each = tx("each square: 100,000 farms, drawn to their average size", 13, GREY_B).move_to([0.1, -2.2, 0])
        src = source("FAO via Our World in Data (maize yields); IMF maize via FRED, deflated by the CPI; USDA ERS and NASS "
                     "(farms)", size=13)
        with self.voiceover(
            "And here is the treadmill in America's records. <bookmark mark='a'/> For seventy years after the Civil "
            "War, an acre of American corn yielded about the same. Then, from the 1930s, came hybrid seed, then "
            "nitrogen fertilizer, bigger machines, genetically engineered seed and precision planting. Each hectare now "
            f"yields about {Tr['maize_x30']:.0f} times what it did before. <bookmark mark='b'/> But the price of a bushel, "
            "after inflation, has not risen in thirty years of booming demand, including the rise of corn ethanol; "
            "it has fallen. <bookmark mark='c'/> And the farms. In 1935 the United States had "
            f"{Tr['farms_1935']:.1f} million farms, averaging {Tr['acres_1935']:.0f} acres. In 2025 it had "
            f"{Tr['farms_2025']:.2f} million, averaging {Tr['acres_2025']:.0f}. About the same land, worked by a "
            "fraction of the farms. Every new method made the survivors bigger and let everyone else go."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(yt))
            vo.wait_until("a")
            self.play(Create(yl), run_time=3.5)
            self.play(FadeIn(ann))
            vo.wait_until("b")
            self.play(FadeIn(pb), FadeIn(pt))
            self.play(Create(pl), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(g35[0]), LaggedStart(*[FadeIn(sq, scale=0.5) for sq in f35], lag_ratio=0.01), FadeIn(g35[2:]),
                      run_time=1.6)
            self.play(FadeIn(each))
            self.play(FadeIn(g25[0]), LaggedStart(*[FadeIn(sq, scale=0.5) for sq in f25], lag_ratio=0.03), FadeIn(g25[2:]),
                      run_time=1.6)
        self.clear_scene()
