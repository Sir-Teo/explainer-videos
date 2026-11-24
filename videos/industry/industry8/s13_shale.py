from __future__ import annotations

from videos.industry.industry8.common import *  # noqa: F403

REG = [("texas", "Texas", SHALE), ("dakota", "North Dakota", "#E8C26A"), ("gulf", "Gulf of Mexico, offshore", BRENT),
       ("rest", "everywhere else", "#5B6372")]


class Shale(VoiceoverScene):
    def construct(self):
        card(self, 11, "Shale: oil from a factory", "How did the United States become the largest producer again?",
             "Chapter eleven. Shale: oil from a factory.", lit=("make", "change"))
        self.output()
        self.rigs()
        self.trade()

    def output(self):
        U = R["us"]
        ms = U["months"]
        keep = [k for k, m in enumerate(ms) if U["monthly"][k] is not None]
        xs = [mx(ms[k]) for k in keep]
        tot = np.array([U["monthly"][k] for k in keep]) / 1000
        tex = np.array([U["texas"][k] or 0 for k in keep]) / 1000
        dak = np.array([U["dakota"][k] or 0 for k in keep]) / 1000
        gul = np.array([U["gulf"][k] or 0 for k in keep]) / 1000
        rest = tot - tex - dak - gul
        pa = viz.plot_axes([2000, 2027], [0, 15], x_length=9.4, y_length=4.4, xticks=[2000, 2005, 2010, 2015, 2020, 2025],
                           yticks=[5, 10, 15], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}m", size=14)
        pa.move_to([0.3, -0.5, 0])
        series = {"texas": tex, "dakota": dak, "gulf": gul, "rest": rest}
        base = np.zeros(len(xs))
        areas = VGroup()
        for key, name, col in [REG[3], REG[2], REG[1], REG[0]]:
            top = base + series[key]
            pts = [pa.ax.c2p(x, v) for x, v in zip(xs, top)] + [pa.ax.c2p(x, v) for x, v in zip(xs[::-1], base[::-1])]
            areas.add(Polygon(*pts, stroke_width=0, fill_color=col, fill_opacity=0.9))
            base = top
        key_ = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=c, fill_opacity=1), tx(n, 14, c)).arrange(RIGHT, buff=0.08)
                        for _, n, c in REG]).arrange(RIGHT, buff=0.35).next_to(pa, UP, buff=0.15)
        peak = DashedLine(pa.ax.c2p(2000, U["peak1970"] / 1000), pa.ax.c2p(2027, U["peak1970"] / 1000), stroke_color=WHITE,
                          stroke_width=2)
        pl = tx(f"the 1970 peak: {U['peak1970'] / 1000:.1f}m barrels a day", 16, WHITE).next_to(pa.ax.c2p(2001, U["peak1970"] / 1000),
                                                                                         UP, buff=0.08).align_to(pa.ax.c2p(2001, 0), LEFT)
        passed = tx(f"passed in {U['pass1970']}", 17, PRICE, bold=True).next_to(pa.ax.c2p(U["pass1970"], U["peak1970"] / 1000),
                                                                             UP, buff=0.35)
        kb = dict(zip(U["years"], U["kbd"]))
        low = tx(f"{kb[2008] / 1000:.1f}m in 2008", 16, GREY_A).next_to(pa.ax.c2p(2008.5, kb[2008] / 1000), DOWN, buff=0.15)

        def avg(series, y):
            v = [series[k] for k, m in enumerate(ms) if m.startswith(str(y)) and series[k] is not None]
            return sum(v) / len(v)
        g_nd = avg(U["dakota"], 2025) / avg(U["dakota"], 2008)
        g_tx = avg(U["texas"], 2025) / avg(U["texas"], 2008)
        src = source("US Energy Information Administration, field production of crude oil, monthly (US, Texas, North "
                     "Dakota, federal Gulf of Mexico)", size=13)
        with self.voiceover(
            "In 2008 the United States produced about five million barrels of crude a day, half its peak of 1970, "
            "and everyone expected the decline to go on. <bookmark mark='a'/> Then drillers in Texas and North "
            "Dakota combined two old techniques, drilling sideways and cracking the rock with water and sand under "
            "pressure, and turned them on the source rock itself. <bookmark mark='b'/> Between 2008 and 2025, North "
            f"Dakota's output rose about {g_nd:.0f}-fold and Texas's about {g_tx:.0f}-fold. <bookmark mark='c'/> In "
            f"{U['pass1970']} American production passed its 1970 peak, and by 2026 it was close to fourteen million "
            "barrels a day. No country has ever produced more crude oil, as the Energy Information Administration "
            "has noted every year since 2018."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(key_), Create(peak), FadeIn(pl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(a_) for a_ in areas], lag_ratio=0.25), run_time=3.0)
            self.play(FadeIn(low))
            vo.wait_until("b")
            self.play(Indicate(areas[3], color=WHITE), Indicate(areas[2], color=WHITE))
            vo.wait_until("c")
            self.play(FadeIn(passed))
        self.clear_scene()

    def rigs(self):
        U = R["us"]
        b = U["bust"]
        ms = U["months"]
        k0, k1 = ms.index("2013-01"), ms.index("2018-12")
        sel = range(k0, k1 + 1)
        xs = [mx(ms[k]) for k in sel]
        rig = [U["rigs"][k] for k in sel]
        prod = [U["monthly"][k] / 1000 for k in sel]
        pa = viz.plot_axes([2013, 2019], [0, 1800], x_length=5.4, y_length=3.4, xticks=[2014, 2016, 2018],
                           yticks=[500, 1000, 1500], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{int(v)}", size=13)
        pb = viz.plot_axes([2013, 2019], [0, 12], x_length=5.4, y_length=3.4, xticks=[2014, 2016, 2018],
                           yticks=[4, 8, 12], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}m", size=13)
        VGroup(pa, pb).arrange(RIGHT, buff=1.2).move_to([0, -0.6, 0])
        lr = VMobject(stroke_color=STATE, stroke_width=4).set_points_as_corners([pa.ax.c2p(x, v) for x, v in zip(xs, rig)])
        lp = VMobject(stroke_color=SHALE, stroke_width=4).set_points_as_corners([pb.ax.c2p(x, v) for x, v in zip(xs, prod)])
        ha = tx("oil rigs drilling in the US", 18, STATE, bold=True).next_to(pa, UP, buff=0.15)
        hb = tx("US crude output, barrels a day", 18, SHALE, bold=True).next_to(pb, UP, buff=0.15)
        ra = tx(f"{b['rig_hi'][1]:,.0f} ({mlabel(b['rig_hi'][0])}) to {b['rig_lo'][1]:.0f} ({mlabel(b['rig_lo'][0])}): "
                f"{100 * b['rig_fall']:.0f}%", 16, WHITE).next_to(pa, DOWN, buff=0.35)
        rb = tx(f"{b['prod_hi'][1] / 1000:.2f}m ({mlabel(b['prod_hi'][0])}) to {b['prod_lo'][1] / 1000:.2f}m "
                f"({mlabel(b['prod_lo'][0])}): {100 * b['prod_fall']:.0f}%", 16, WHITE).next_to(pb, DOWN, buff=0.35)
        src = source("EIA: crude oil rotary rigs in operation (Baker Hughes) and field production, monthly", size=13)
        with self.voiceover(
            "The price collapse of 2014 was the test. <bookmark mark='a'/> Drillers cut fast. The number of rigs "
            f"drilling for oil in America fell by {abs(100 * b['rig_fall']):.0f} percent in nineteen months. "
            "<bookmark mark='b'/> Output fell by only about a tenth, and not for long. The wells drilled were "
            "better, the rigs that stayed were the best, and the companies drilled their best rock first. "
            "<bookmark mark='c'/> By 2018, output was setting records with half the rigs of 2014. Shale is a factory "
            "process: thousands of nearly identical wells, each a few months from decision to oil, getting cheaper "
            "and more productive each year."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(pb), FadeIn(ha), FadeIn(hb))
            vo.wait_until("a")
            self.play(Create(lr), run_time=2.5)
            self.play(FadeIn(ra))
            vo.wait_until("b")
            self.play(Create(lp), run_time=2.5)
            self.play(FadeIn(rb))
            vo.wait_until("c")
            self.play(Indicate(lp, color=WHITE))
        self.clear_scene()

    def trade(self):
        U = R["us"]
        ni = U["net_imports"]
        ys = [y for y in range(1990, 2026) if y in ni]
        pa = viz.plot_axes([1989.4, 2025.6], [-4, 14], x_length=9.6, y_length=4.2, xticks=[1990, 2000, 2010, 2020],
                           yticks=[-4, 0, 4, 8, 12], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}m", size=14)
        pa.move_to([0.3, -0.5, 0])
        bars = VGroup()
        for y in ys:
            v = ni[y] / 1000
            p0, p1 = pa.ax.c2p(y - 0.35, 0), pa.ax.c2p(y + 0.35, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]), stroke_width=0,
                               fill_color=STATE if v > 0 else GAS, fill_opacity=0.9).move_to((p0 + p1) / 2))
        head = tx("US net imports of crude oil and products, barrels a day", 18, GREY_A).next_to(pa, UP, buff=0.15)
        pk = max(ys, key=lambda y: ni[y])
        lab = tx(f"{pk}: {ni[pk] / 1000:.1f}m a day imported, net", 17, STATE, bold=True).next_to(
            pa.ax.c2p(pk, ni[pk] / 1000), UP, buff=0.1)
        lab2 = tx(f"since {U['first_net_export']}: a net exporter ({ni[2025] / 1000:.1f}m in 2025)", 17, GAS, bold=True).next_to(
            pa.ax.c2p(2018, -3.5), LEFT, buff=0.1)
        src = source("US Energy Information Administration, net imports of crude oil and petroleum products, annual",
                     size=13)
        with self.voiceover(
            "And it changed the country's place in the world. <bookmark mark='a'/> In "
            f"{pk}, America imported, net, {ni[pk] / 1000:.1f} million barrels a day of crude and fuels. "
            f"<bookmark mark='b'/> Since {U['first_net_export']} it has exported more than it imports. "
            "<bookmark mark='c'/> And shale changed the price, too. A deepwater project decided today produces in "
            "the 2030s. A shale well decided today produces next spring. When prices rise, American drillers can "
            "add supply within months, which puts a soft ceiling on the price; when they fall, they stop just as "
            "fast. The swing producer of the 1980s was a government. Today a large part of the swing is thousands "
            "of private drillers, each looking at the price."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.04), run_time=3.0)
            self.play(FadeIn(lab))
            vo.wait_until("b")
            self.play(FadeIn(lab2))
            vo.wait_until("c")
            self.play(Indicate(bars[-6:], color=WHITE))
        self.clear_scene()
