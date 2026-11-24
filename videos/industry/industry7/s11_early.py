from __future__ import annotations

from explainer.industry.works.diffusion import predict
from videos.industry.industry7.common import *  # noqa: F403


class Early(VoiceoverScene):
    def construct(self):
        card(self, 11, "Calling the curve early", "Could you have seen the ceiling from the first years?",
             "Chapter eleven. Calling the curve early.", lit=("change",))
        self.colour_tv()
        self.fan()
        self.all_of_them()

    def colour_tv(self):
        E = R["early"]
        row = next(d for d in E["rows"] if d["name"] == "Colour TV")
        ys, ss, cut = row["years"], row["shares"], row["cut"]
        pa = viz.plot_axes([1964, 2006], [0, 100], x_length=9.0, y_length=4.4, xticks=[1965, 1975, 1985, 1995, 2005],
                           yticks=[25, 50, 75, 100], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}%", size=15)
        pa.move_to([0.8, -0.5, 0])
        early_d = VGroup(*[Dot(pa.ax.c2p(y, s), radius=0.06, color=WHITE) for y, s in zip(ys, ss) if y <= cut])
        later_d = VGroup(*[Dot(pa.ax.c2p(y, s), radius=0.06, color=FACTORY) for y, s in zip(ys, ss) if y > cut])
        xs = np.linspace(1964, 2006, 90)
        fit = VMobject(stroke_color=GUESS, stroke_width=4).set_points_smoothly(
            [pa.ax.c2p(x, float(predict(row["early"], [x])[0])) for x in xs])
        cutl = DashedLine(pa.ax.c2p(cut, 0), pa.ax.c2p(cut, 100), stroke_color=GREY_C, stroke_width=1.5)
        cutt = tx(f"what you could see in {cut:.0f}", 15, GREY_B).next_to(pa.ax.c2p(cut, 100), UP, buff=0.05)
        fl = tx(f"the curve fitted to those years: tops out at {row['ceiling']:.0f}%", 17, GUESS).next_to(
            pa.ax.c2p(1990, row["ceiling"]), UP, buff=0.12)
        al = tx(f"what happened: {row['last']:.0f}% by {row['last_year']:.0f}", 17, FACTORY).next_to(
            pa.ax.c2p(1990, 96), DOWN, buff=0.3)
        tv = VGroup(RoundedRectangle(corner_radius=0.1, width=1.3, height=1.0, stroke_width=0, fill_color="#3A2F2A",
                                     fill_opacity=1),
                    RoundedRectangle(corner_radius=0.08, width=0.95, height=0.7, stroke_width=0, fill_color="#5DA9E9",
                                     fill_opacity=0.8).shift(LEFT * 0.1),
                    *[Rectangle(width=0.32, height=0.23, stroke_width=0, fill_color=c, fill_opacity=0.9).shift(
                        LEFT * (0.1 + 0.32 * (k - 1)) + UP * 0.1) for k, c in enumerate(("#E8554E", "#7BD88F", "#F6C453"))]
                    ).move_to([-5.6, 2.2, 0])
        src = source("Our World in Data (Comin and Hobijn); this film's Bass fit to the years up to 25% of households",
                     size=13)
        with self.voiceover(
            "Put yourself in 1969. Colour television has been on sale for some years. <bookmark mark='a'/> These "
            f"dots are all you can see: the share of American households with a colour set, rising to about a "
            "quarter. <bookmark mark='b'/> Fit Bass's curve to those years, and it says colour television is levelling "
            f"off, at about {row['ceiling']:.0f} percent of homes: a luxury for a third of the country. "
            "<bookmark mark='c'/> Here is what happened. It kept climbing, to almost every home in America. The "
            "model was not wrong about the shape. It simply could not tell, from the bottom of the S, where the top "
            "would be. Nothing in the first quarter of a curve tells you whether you are looking at the start of a "
            "steep climb or most of a gentle one."
        ) as vo:
            self.play(FadeIn(src), FadeIn(tv, shift=RIGHT * 0.2), FadeIn(pa))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=2) for d_ in early_d], lag_ratio=0.15), Create(cutl), FadeIn(cutt))
            vo.wait_until("b")
            self.play(Create(fit), run_time=2.4)
            self.play(FadeIn(fl))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d_, scale=2) for d_ in later_d], lag_ratio=0.05), run_time=2.6)
            self.play(FadeIn(al))
        self.clear_scene()

    def fan(self):
        """Four ceilings, one set of early points: each curve passes within a fraction of a point of every dot."""
        F = R["fan"]
        row = next(d for d in R["early"]["rows"] if d["name"] == "Colour TV")
        ys, ss, cut = row["years"], row["shares"], F["cut"]
        pa = viz.plot_axes([1964, 1990], [0, 100], x_length=8.0, y_length=4.4, xticks=[1965, 1970, 1975, 1980, 1985, 1990],
                           yticks=[25, 50, 75, 100], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}%", size=15)
        pa.move_to([-0.6, -0.5, 0])
        dots = VGroup(*[Dot(pa.ax.c2p(y, s_), radius=0.065, color=WHITE) for y, s_ in zip(ys, ss) if y <= cut])
        cols = [GUESS, UNITS, RETAIL, FACTORY]
        xs = np.linspace(1964, 1990, 80)
        curves, labs = VGroup(), VGroup()
        for f, col in zip(F["fits"], cols):
            c_ = VMobject(stroke_color=col, stroke_width=3.5).set_points_smoothly(
                [pa.ax.c2p(x, float(predict(f, [x])[0])) for x in xs])
            curves.add(c_)
            labs.add(VGroup(tx(f"ceiling {f['m']:.0f}%", 18, col, bold=True),
                            tx(f"misses the dots by {f['rmse']:.2f} points", 15, GREY_B)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                buff=0.03))
        VGroup(*reversed(labs)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([5.0, -0.3, 0])
        zoom = Rectangle(width=pa.ax.c2p(cut + 0.6, 0)[0] - pa.ax.c2p(1965.4, 0)[0],
                         height=pa.ax.c2p(0, 30)[1] - pa.ax.c2p(0, 4)[1], stroke_color=WHITE,
                         stroke_width=1.5).move_to(pa.ax.c2p((1965.4 + cut + 0.6) / 2, 17))
        cutl = DashedLine(pa.ax.c2p(cut, 0), pa.ax.c2p(cut, 100), stroke_color=GREY_C, stroke_width=1.5)
        head = tx(f"Colour TV, the years up to {cut:.0f}: four ceilings, one set of dots", 22, WHITE, bold=True).to_edge(
            UP, buff=0.5)
        src = source("Our World in Data (Comin and Hobijn); this film's Bass fits with the ceiling held fixed", size=13)
        with self.voiceover(
            "Why does it miss so badly? Look closely at what the first years contain. <bookmark mark='a'/> Here are "
            f"colour television's four dots, up to {cut:.0f}: none above a quarter of households. "
            "<bookmark mark='b'/> Now force the curve to stop at forty percent, and fit it. "
            "<bookmark mark='c'/> At sixty. At eighty. At a hundred. <bookmark mark='d'/> Every one of the four passes "
            f"within about a third of a percentage point of every dot. The early years cannot tell these curves "
            "apart, because in the early years every S-curve looks the same: a slow start bending upward. The "
            "ceiling is simply not in the data yet. <bookmark mark='e'/> So a forecast of the ceiling has to come "
            "from somewhere else: from who could possibly buy, at what price, and from products that came before. "
            "The curve can tell you the shape. It cannot tell you the size."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(head), Create(cutl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=2) for d_ in dots], lag_ratio=0.12), Create(zoom))
            vo.wait_until("b")
            self.play(Create(curves[0]), FadeIn(labs[0]), run_time=1.4)
            vo.wait_until("c")
            for k in (1, 2, 3):
                self.play(Create(curves[k]), FadeIn(labs[k]), run_time=1.0)
            vo.wait_until("d")
            self.play(Indicate(zoom, color=WHITE), *[Indicate(l_[1], color=WHITE) for l_ in labs])
            vo.wait_until("e")
            self.play(*[c_.animate.set_stroke(opacity=0.4) for c_ in curves], dots.animate.set_color(GOLD))
        self.clear_scene()

    def all_of_them(self):
        E = R["early"]
        rows = sorted(E["rows"], key=lambda d: d["miss"])
        n = len(rows)
        x0, w = -6.2, 12.0 / n
        base = 0.2
        u = 0.035
        bars = VGroup()
        for i, d in enumerate(rows):
            h = d["miss"] * u
            col = RETAIL if abs(d["miss"]) <= 10 else ("#E8554E" if abs(d["miss"]) > 30 else GUESS)
            bars.add(Rectangle(width=w * 0.8, height=max(abs(h), 0.02), stroke_width=0, fill_color=col,
                               fill_opacity=0.9).move_to([x0 + w * (i + 0.5), base, 0],
                                                         aligned_edge=DOWN if h >= 0 else UP))
        zero = Line([x0, base, 0], [x0 + 12.0, base, 0], stroke_color=GREY_B, stroke_width=1.5)
        names = VGroup()
        for i in (0, 1, 2, n - 3, n - 2, n - 1):
            d = rows[i]
            t_ = tx(d["name"].replace(" infrastructure", "").replace("Household ", ""), 13, GREY_A).rotate(PI / 2)
            t_.next_to(bars[i], UP if d["miss"] < 0 else DOWN, buff=0.08)
            names.add(t_)
        yl = VGroup(tx("forecast too low", 16, "#E8554E").move_to([x0 + 1.6, base - 2.4, 0]),
                    tx("forecast too high", 16, GUESS).move_to([x0 + 10.4, base + 1.4, 0]))
        head = tx(f"{n} technologies: the S-curve fitted at 25% adoption, against the last year observed "
                  "(percentage points)", 18, GREY_A).to_edge(UP, buff=0.5)
        stats = VGroup(tx(f"median miss: {E['median']:.0f} points", 22, WHITE, bold=True),
                       tx(f"{E['within10']} of {n} within 10 points; {E['over30']} off by more than 30", 18, GREY_A)
                       ).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.5)
        src = source("Our World in Data (Comin and Hobijn and others); this film's fits", size=13)
        with self.voiceover(
            "Was colour television unlucky? Run the same test on every technology in the data with enough years "
            f"to try it: {n} of them. <bookmark mark='a'/> For each, fit the curve to the years up to a quarter of "
            "households, and compare its forecast with the last year observed. <bookmark mark='b'/> About half "
            f"land within ten percentage points. <bookmark mark='c'/> {E['over30']} miss by more than thirty, "
            "almost all of them on the low side: colour television, power steering, the refrigerator, the washing "
            f"machine. The median miss is {E['median']:.0f} points. <bookmark mark='d'/> So an honest forecast of a "
            "young market is a range, and a wide one, which is why careful forecasters publish scenarios and update "
            "them as the years come in. A single confident number for a market "
            "ten years out is a guess with decimals."
        ) as vo:
            self.play(FadeIn(src), FadeIn(head), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN if rows[i]["miss"] >= 0 else UP) for i, b_ in enumerate(bars)],
                                  lag_ratio=0.05), run_time=2.4)
            vo.wait_until("b")
            self.play(*[Indicate(b_, color=WHITE, scale_factor=1.0) for i, b_ in enumerate(bars)
                        if abs(rows[i]["miss"]) <= 10], FadeIn(stats[1]))
            vo.wait_until("c")
            self.play(FadeIn(names), FadeIn(yl))
            self.play(FadeIn(stats[0]))
        self.clear_scene()
