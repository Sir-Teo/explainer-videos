from __future__ import annotations

from videos.industry.industry8.common import *  # noqa: F403

CUTS = [("heavy fuel and asphalt", "#3A2A1E"), ("diesel and heating oil", "#C08040"), ("jet fuel and kerosene", "#E0B060"),
        ("gasoline", "#F2D27A"), ("naphtha for chemicals", "#C9D3E0"), ("propane and butane", "#E8EAED")]


class Refining(VoiceoverScene):
    def construct(self):
        card(self, 12, "Refining: a business of spreads", "What does a refinery sell, and why do its profits lurch?",
             "Chapter twelve. Refining: a business of spreads.", lit=("make", "dollar"))
        self.column()
        self.crack()

    def column(self):
        col = draw.column(4.6).move_to([-2.8, -0.6, 0])
        cuts = VGroup()
        for k, (name, c) in enumerate(CUTS):
            ln = col.cuts[k]
            end = ln.get_end()
            dot = Circle(radius=0.16, stroke_width=0, fill_color=c, fill_opacity=1).move_to(end + RIGHT * 0.2)
            t = tx(name, 17, WHITE).next_to(dot, RIGHT, buff=0.15)
            cuts.add(VGroup(ln.copy().set_stroke(c, 4), dot, t))
        heat = VGroup(*[Triangle(stroke_width=0, fill_color="#F2A65A", fill_opacity=0.9).scale(0.12).move_to(
            col[0].get_bottom() + UP * 0.05 + RIGHT * (k - 1) * 0.18) for k in range(3)])
        crude_in = Arrow(col[0].get_left() + LEFT * 1.0, col[0].get_left(), buff=0.05, stroke_width=4, color=CRUDE,
                         max_tip_length_to_length_ratio=0.25)
        cl = tx("crude, heated", 16, CRUDE).next_to(crude_in, UP, buff=0.05)
        # vapour rising inside the tower
        rng = np.random.default_rng(2)
        t = ValueTracker(0)
        tw = col.tower
        bubbles = VGroup(*[Dot(radius=0.04, color="#F2D27A") for _ in range(18)])

        def rise(m):
            tt = t.get_value()
            for k, d_ in enumerate(m):
                ph = (tt * 0.5 + k / len(m)) % 1.0
                x = tw.get_x() + (rng.random() - 0.5) * 0.4 if False else tw.get_x() + ((k * 37) % 9 - 4) * 0.05
                d_.move_to([x, tw.get_bottom()[1] + 0.2 + ph * (tw.height - 0.4), 0]).set_opacity(0.8 - 0.5 * ph)
        bubbles.add_updater(rise)
        note = VGroup(tx("light molecules rise highest;", 17, GREY_A), tx("each cut is drawn off at its height", 17, GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.04).to_corner(UR, buff=0.6)
        tag = estimate_tag("illustrative tower; real refineries also crack and reform the cuts", corner=DR, size=14)
        with self.voiceover(
            "Crude oil is no use as it comes out of the ground. A refinery turns it into things people buy. "
            "<bookmark mark='a'/> The first step is a tall column. Crude is heated until most of it boils, and the "
            "vapour rises up the tower, cooling as it goes. <bookmark mark='b'/> Heavy molecules condense low down: "
            "fuel oil and asphalt at the bottom, then diesel, then jet fuel, then gasoline, and the lightest gases at "
            "the top. <bookmark mark='c'/> Then other units break the heavy cuts into lighter, more valuable ones. "
            "The result is that a refinery's whole business is a spread: what its products sell for, minus what the "
            "crude cost."
        ) as vo:
            self.play(FadeIn(col), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowArrow(crude_in), FadeIn(cl), FadeIn(heat))
            self.add(bubbles)
            self.play(t.animate.set_value(3), run_time=3, rate_func=linear)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(Create(c_[0]), FadeIn(c_[1], scale=1.5), FadeIn(c_[2], shift=RIGHT * 0.1))
                                    for c_ in cuts], lag_ratio=0.35), t.animate.set_value(8), FadeIn(note), run_time=4.0)
            vo.wait_until("c")
            self.play(t.animate.set_value(11), run_time=3, rate_func=linear)
        bubbles.clear_updaters()
        self.clear_scene()

    def crack(self):
        C = R["crack"]
        ms, cr = C["months"], C["crack"]
        pts = [(mx(m), c) for m, c in zip(ms, cr) if c is not None]
        pa = viz.plot_axes([1987, 2027], [-10, 60], x_length=7.4, y_length=3.6, xticks=[1990, 2000, 2010, 2020],
                           yticks=[0, 20, 40, 60], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}", size=13)
        pa.move_to([-2.5, -0.5, 0])
        ln = VMobject(stroke_color=COST, stroke_width=2.5).set_points_as_corners([pa.ax.c2p(x, v) for x, v in pts])
        zero = DashedLine(pa.ax.c2p(1987, 0), pa.ax.c2p(2027, 0), stroke_color=GREY_C, stroke_width=1)
        head = tx("3-2-1 crack spread: 2 gasoline + 1 diesel - 3 crude, per barrel", 16, COST).next_to(pa, UP, buff=0.15)
        eq = MathTex(r"\text{crack} = \tfrac{2\,p_{\text{gasoline}} + p_{\text{diesel}} - 3\,p_{\text{crude}}}{3}",
                     font_size=28).next_to(pa, DOWN, buff=0.45)
        vlo = R["companies"]["VLO"]["net"]
        ys = sorted(y for y in vlo if y >= 2012)
        pb = viz.plot_axes([2011.4, 2025.6], [-3, 13], x_length=4.2, y_length=3.0, xticks=[2012, 2016, 2020, 2024],
                           yticks=[0, 5, 10], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}bn", size=12)
        pb.move_to([4.4, -0.3, 0])
        bars = VGroup()
        for y in ys:
            v = vlo[y]
            p0, p1 = pb.ax.c2p(y - 0.35, 0), pb.ax.c2p(y + 0.35, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=max(abs(p1[1] - p0[1]), 0.01), stroke_width=0,
                               fill_color=GAS if v >= 0 else STATE, fill_opacity=0.9).move_to((p0 + p1) / 2))
        hb = tx("Valero, net income", 16, GAS, bold=True).next_to(pb, UP, buff=0.12)
        a20, a22, a26 = C["annual"][2020], C["annual"][2022], C["annual"][2026]
        lab = VGroup(tx(f"2020: ${a20:.0f}", 15, WHITE), tx(f"2022: ${a22:.0f}", 15, WHITE),
                     tx(f"2026 so far: ${a26:.0f}", 15, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to(
            pa.ax.c2p(2008, 50))
        src = source("EIA spot prices: New York Harbor gasoline and heating oil, Brent (monthly); Valero, Forms 10-K "
                     "(SEC company facts); this film's crack spread", size=13)
        with self.voiceover(
            "Traders measure that spread with a rule of thumb, the three-two-one crack: three barrels of crude make "
            "roughly two of gasoline and one of diesel. <bookmark mark='a'/> Here it is, month by month since 1987, "
            "from New York Harbor's fuel prices and Brent. Through the 1990s it was usually under ten dollars a "
            "barrel. <bookmark mark='b'/> In 2020, with nobody driving or flying, the spread fell to "
            f"{a20:.0f} dollars a barrel on average; in 2022, after Russia's invasion of Ukraine cut supplies of diesel, "
            f"it averaged {a22:.0f}. In 2026, with the Gulf's exports of diesel and jet fuel cut off, it has averaged "
            f"{a26:.0f} so far. <bookmark mark='c'/> A refiner's profit follows the spread, not the price of oil. "
            "Valero, one of America's largest refiners, lost money in 2020 and made eleven and a half billion "
            "dollars in 2022. <bookmark mark='d'/> Pipelines are the opposite: in America the rates on oil pipelines "
            "between states are regulated, so they earn a toll on every barrel, whatever it is worth."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(head), Create(zero), Write(eq))
            vo.wait_until("a")
            self.play(Create(ln), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(lab))
            vo.wait_until("c")
            self.play(FadeIn(pb), FadeIn(hb), LaggedStart(*[GrowFromEdge(b_, DOWN if vlo[y] >= 0 else UP)
                                                             for b_, y in zip(bars, ys)], lag_ratio=0.08), run_time=2.0)
            vo.wait_until("d")
            self.play(Indicate(bars, color=WHITE, scale_factor=1.02))
        self.clear_scene()
