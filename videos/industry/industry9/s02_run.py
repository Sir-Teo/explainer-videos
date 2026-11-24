from __future__ import annotations

from videos.industry.industry9.common import *  # noqa: F403

BUILD, WAIT, SELL = COPPER, "#7EC8F5", GREY_A


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: build, wait or sell", "You own one copper deposit. What do you do with it?",
             "Chapter one. Run it: build, wait, or sell.", lit=("make", "change"))
        self.deposit()
        self.cash()
        self.futures()

    def deposit(self):
        RR = R["run"]
        pit = draw.open_pit(4.6, 1.5, benches=4)
        pit.ore.set_fill(opacity=0.0)
        body = VGroup(*[Square(0.16, stroke_width=0, fill_color=COPPER if (i * 7 + j * 3) % 11 == 0 else ROCK,
                               fill_opacity=0.95) for i in range(6) for j in range(22)]).arrange_in_grid(
            rows=6, cols=22, buff=0.025)
        body.move_to(pit.get_bottom() + DOWN * 0.7)
        dep = VGroup(pit, body).scale(0.9).move_to([-3.7, 0.9, 0])
        facts = VGroup(
            tx("The model deposit", 24, COPPER, bold=True),
            tx(f"{RR['ore']:.0f} million tonnes of ore at {RR['grade']:.1f}% copper", 18, WHITE),
            tx("mill 40 million tonnes a year, for 15 years", 18, WHITE),
            tx(f"{RR['copper']:.0f} thousand tonnes of copper in year one, falling", 18, WHITE),
            tx(f"costs ${RR['cost0']:.2f} a pound to produce at first, ${RR['cost_end']:.2f} at the end", 18, WHITE),
            tx(f"${RR['capex'] / 1000:.0f} billion and {RR['build']} years to build", 18, WHITE),
            tx(f"pays its way at ${RR['breakeven']:.2f} a pound", 20, PRICE, bold=True),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-3.5, -2.2, 0])
        price = VGroup(tx("Copper today:", 22, GREY_A), tx(f"${RR['p0']:.2f} a pound", 30, PRICE, bold=True)
                       ).arrange(DOWN, buff=0.08).move_to([3.6, 3.1, 0])
        opts = VGroup()
        icons = [draw.haul_truck(1.0, color=BUILD), VGroup(Circle(0.42, stroke_color=WAIT, stroke_width=4),
                                                          Line(ORIGIN, UP * 0.3, stroke_color=WAIT, stroke_width=4),
                                                          Line(ORIGIN, RIGHT * 0.22, stroke_color=WAIT, stroke_width=4)),
                 draw.coin_stack(4, r=0.22)]
        texts = [("Build it now", f"spend ${RR['capex'] / 1000:.0f}bn, first copper in {RR['build']} years"),
                 ("Wait a year", "then build only if the price still pays"),
                 ("Sell it", f"a bigger miner offers ${RR['sell']:,.0f}m today")]
        for ic, (h, d), col in zip(icons, texts, [BUILD, WAIT, SELL]):
            ic.scale_to_fit_height(0.6)
            row = VGroup(ic, VGroup(tx(h, 22, col, bold=True), tx(d, 16, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                           buff=0.05)).arrange(
                RIGHT, buff=0.3)
            box = RoundedRectangle(corner_radius=0.12, width=5.6, height=1.05, stroke_color=col, stroke_width=1.6,
                                   fill_color="#141A24", fill_opacity=1)
            row.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.3)
            opts.add(VGroup(box, row))
        opts.arrange(DOWN, buff=0.25).move_to([3.6, -0.6, 0])
        tag = estimate_tag("a model deposit from the Works (mine.py), not any company's", corner=DR, size=14)
        tonne = Square(2.4, stroke_width=0, fill_color=ROCK, fill_opacity=0.95)
        grain = Square(2.4 * np.sqrt(0.005), stroke_width=0, fill_color=COPPER, fill_opacity=1).move_to(tonne)
        ton = VGroup(tonne, grain, tx("one tonne of ore", 20, WHITE, bold=True).next_to(tonne, UP, buff=0.15),
                     tx("holds 5 kilograms of copper", 20, COPPER, bold=True).next_to(tonne, DOWN, buff=0.15)
                     ).move_to([3.4, 0.2, 0])
        with self.voiceover(
            "Play it yourself. You own one copper deposit, found by your own geologists. <bookmark mark='a'/> It holds "
            f"{RR['ore']:.0f} million tonnes of ore, and each tonne holds half a percent of copper: five kilograms in a "
            "tonne of rock. A mill could process forty million tonnes a year for fifteen years, making about "
            f"{RR['copper']:.0f} thousand tonnes of copper in the first year, and less after that, because the best "
            "rock is mined first. <bookmark mark='b'/> It would cost three billion dollars and three years to build. "
            f"Producing a pound of copper would cost about {RR['cost0']:.2f} dollars at first, rising to "
            f"{RR['cost_end']:.2f}. Add the building cost, the royalty and the tax, and the mine pays its way, at an "
            f"eight percent return, if copper sells for {RR['breakeven']:.2f} a pound over its whole life. "
            f"<bookmark mark='c'/> Copper sells for {RR['p0']:.2f} today. You have three choices. <bookmark mark='d'/> "
            "Build now. <bookmark mark='e'/> Wait a year and see where the price goes, then build only if it still "
            "pays. <bookmark mark='f'/> Or sell the deposit to a bigger miner, which offers "
            f"{RR['sell']:,.0f} million dollars in cash today. Pause, and choose."
        ) as vo:
            self.play(FadeIn(pit), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, scale=0.5) for b_ in body], lag_ratio=0.004), run_time=1.6)
            self.play(FadeIn(ton[0]), FadeIn(ton[2]))
            self.play(GrowFromCenter(ton[1]), FadeIn(ton[3]), Flash(ton[1], color=COPPER))
            self.play(LaggedStart(*[FadeIn(f) for f in facts[:4]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(f) for f in facts[4:]], lag_ratio=0.3), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeOut(ton), FadeIn(price, shift=DOWN * 0.1))
            for k, m in enumerate("def"):
                vo.wait_until(m)
                self.play(FadeIn(opts[k], shift=LEFT * 0.2))
        self.clear_scene()

    def cash(self):
        RR = R["run"]
        cf = RR["cash"]
        n = len(cf)
        pa = viz.plot_axes([-0.7, n - 0.3], [-1100, 800], x_length=11.0, y_length=4.4, xticks=[0, 3, 10, 17],
                           yticks=[-1000, -500, 0, 500], xfmt=lambda v: f"year {int(v)}", yfmt=lambda v: f"${v:,.0f}m",
                           size=14).move_to([0.2, -0.3, 0])
        zero = Line(pa.ax.c2p(-0.7, 0), pa.ax.c2p(n - 0.3, 0), stroke_color=GREY_B, stroke_width=1.5)
        bars = VGroup()
        for k, v in enumerate(cf):
            p0, p1 = pa.ax.c2p(k, 0), pa.ax.c2p(k, v)
            h = abs(p1[1] - p0[1])
            bars.add(Rectangle(width=0.42, height=max(h, 0.01), stroke_width=0, fill_color=COPPER if v > 0 else STATE,
                               fill_opacity=0.9).move_to([p0[0], (p0[1] + p1[1]) / 2, 0]))
        cum = np.cumsum(cf)
        line = VMobject(stroke_color=PRICE, stroke_width=3).set_points_as_corners(
            [pa.ax.c2p(k, max(min(c / 8, 800), -1100)) for k, c in enumerate(cum)])
        payk = int(np.argmax(cum > 0))
        head = tx(f"The model mine's cash, year by year, if copper stays at ${RR['p0']:.2f}", 22, WHITE, bold=True
                  ).to_edge(UP, buff=0.45)
        labs = VGroup(tx("building: $1bn a year", 17, STATE).next_to(bars[2], RIGHT, buff=0.2).shift(DOWN * 0.9),
                      tx("selling copper: less each year, as the grade falls", 17, COPPER).move_to(
                          pa.ax.c2p(10, 760)),
                      tx("closing and cleaning up", 17, STATE).next_to(bars[-1], DOWN, buff=0.15).shift(LEFT * 0.6))
        cl = VGroup(tx("running total (drawn at 1:8)", 15, PRICE), tx(f"in the black in year {payk}", 17, PRICE, bold=True)
                    ).arrange(DOWN, buff=0.04).next_to(pa.ax.c2p(payk, 0), DR, buff=0.2)
        src = source("computed: the Works' model mine (mine.py), before discounting", size=13)
        with self.voiceover(
            "Before you choose, look at what a mine is, in cash. <bookmark mark='a'/> For three years it is only a cost: "
            "a billion dollars a year, and no copper. <bookmark mark='b'/> Then it pays, year after year, but a little "
            "less each year, because the grade falls and the mill makes less copper from the same rock. "
            "<bookmark mark='c'/> At the end, someone has to close it, fill the holes and treat the water, and that "
            f"costs money too. <bookmark mark='d'/> At {RR['p0']:.2f} a pound, the running total turns positive only in "
            f"year {payk}. Everything is paid up front, and the reward comes over a decade and a half, at prices nobody "
            "knows yet. That is the shape of every mine on Earth."
        ) as vo:
            self.play(FadeIn(pa), Create(zero), FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, UP) for b_ in bars[:3]], lag_ratio=0.3), FadeIn(labs[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[3:-1]], lag_ratio=0.15), FadeIn(labs[1]),
                      run_time=3.0)
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[-1], UP), FadeIn(labs[2]))
            vo.wait_until("d")
            self.play(Create(line), run_time=2.5)
            self.play(FadeIn(cl), Flash(pa.ax.c2p(payk, cum[payk] / 8), color=PRICE))
        self.clear_scene()

    def futures(self):
        RR = R["run"]
        paths = np.array(RR["paths"])
        years = paths.shape[1]
        pa = viz.plot_axes([0, years - 1], [0, 9], x_length=4.3, y_length=3.0, xticks=[0, 6, 12, 18],
                           yticks=[2, 4, 6, 8], xfmt=lambda v: f"year {int(v)}", yfmt=lambda v: f"${v:g}", size=13)
        pa.move_to([-4.55, 1.35, 0])
        lines = VGroup(*[VMobject(stroke_color=PRICE, stroke_width=1.3, stroke_opacity=0.45).set_points_as_corners(
            [pa.ax.c2p(t, min(v, 9)) for t, v in enumerate(p)]) for p in paths])
        be = DashedLine(pa.ax.c2p(0, RR["breakeven"]), pa.ax.c2p(years - 1, RR["breakeven"]), stroke_color=COPPER,
                        stroke_width=2)
        bel = tx(f"break-even ${RR['breakeven']:.2f}", 14, COPPER).next_to(be, DOWN, buff=0.06).align_to(be, RIGHT)
        head = tx("Forty of four hundred futures for the price of copper", 17, GREY_A).next_to(pa, UP, buff=0.12)
        # three outcome strips: each future's value, sorted
        lo, hi = -3000, 5000
        strips = VGroup()
        axis = NumberLine(x_range=[lo, hi, 1000], length=5.7, include_numbers=False, stroke_color="#5B6372")
        ticks = VGroup(*[tx(f"{v / 1000:+.0f}bn" if v else "0", 12, GREY_B).next_to(axis.n2p(v), DOWN, buff=0.08)
                         for v in range(lo, hi + 1, 2000)])
        axis_g = VGroup(axis, ticks).move_to([4.05, -3.15, 0])

        def dots(vals, y, col):
            g = VGroup()
            counts: dict = {}
            for v in vals:
                if v == 0:
                    continue
                b_ = int(np.clip((v - lo) // 200, 0, 39))
                counts[b_] = counts.get(b_, 0) + 1
                x = axis.n2p(lo + 200 * b_ + 100)[0]
                g.add(Dot([x, y + 0.035 * counts[b_], 0], radius=0.022,
                          color=STATE if v < 0 else col))
            return g

        now = RR["now_all"]
        wait = RR["wait_all"]
        rows = [("Build now", BUILD, now, f"average ${RR['now_mean']:,.0f}m; loses in {100 * RR['now_loss']:.0f}%"),
                ("Wait a year", WAIT, wait, f"average ${RR['wait_mean']:,.0f}m; loses in {100 * RR['wait_loss']:.0f}%"),
                ("Sell", SELL, None, f"${RR['sell']:,.0f}m, certain")]
        ys = [1.55, -0.2, -1.75]
        for (name, col, vals, note), y in zip(rows, ys):
            lab = VGroup(tx(name, 19, col, bold=True), tx(note, 14, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04
                                                                                     ).move_to([0.95, y + 0.25, 0],
                                                                                               aligned_edge=LEFT)
            if vals is None:
                mark = Line([axis.n2p(RR["sell"])[0], y - 0.05, 0], [axis.n2p(RR["sell"])[0], y + 0.9, 0],
                            stroke_color=SELL, stroke_width=5)
                strips.add(VGroup(lab, mark))
            else:
                strips.add(VGroup(lab, dots(vals, y - 0.05, col)))
                if name == "Wait a year":
                    never = sum(1 for v in vals if v == 0) / len(vals)
                    strips[-1][0].add(tx(f"never built in {100 * never:.0f}%:", 13, GREY_B),
                                      tx("worth nothing, lost nothing", 13, GREY_B))
                    strips[-1][0].arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        for s_ in strips:
            s_[0].shift(LEFT * 0.0)
        zero = DashedLine([axis.n2p(0)[0], -2.95, 0], [axis.n2p(0)[0], 2.6, 0], stroke_color=GREY_B, stroke_width=1.2)
        zl = tx("value today: below zero loses", 13, GREY_B).next_to(zero, UP, buff=0.05)
        for s_, y in zip(strips, ys):
            s_[0].next_to([axis.n2p(lo)[0] - 0.25, y + 0.3, 0], LEFT, buff=0)
        tag = estimate_tag("400 price paths starting at $4.50, drifting back towards $3.80; values discounted at 8%",
                           corner=DR, size=13)
        verdict = VGroup(tx("Rich and diversified: build.", 19, BUILD, bold=True),
                         tx("One deposit and a bank loan: sell.", 19, SELL, bold=True)).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.08).move_to(
            [-4.4, -1.9, 0])
        with self.voiceover(
            "Now let the price move, as it does. <bookmark mark='a'/> Here are forty of four hundred futures, each "
            "starting at four fifty and wandering, with shocks every year, back towards three eighty, roughly where "
            "copper has spent the last few years. <bookmark mark='b'/> Run the mine through all four hundred. If you "
            f"build now, the mine is worth {RR['now_mean']:,.0f} million dollars on average, in today's money. But each "
            f"dot is one future, and in {100 * RR['now_loss']:.0f} percent of them, the red ones, the mine loses money. "
            "<bookmark mark='c'/> If you wait a year, you avoid some of the bad futures, but you give up a year of high "
            f"prices, and here that costs more than it saves: {RR['wait_mean']:,.0f} million on average. "
            f"<bookmark mark='d'/> If you sell, you get {RR['sell']:,.0f} million, whatever happens. "
            "<bookmark mark='e'/> So the answer depends on who you are. A giant with twenty mines can take the "
            "average, because its bad futures and good futures cancel out across the mines. A small company with one "
            "deposit and a bank loan cannot survive the one future in three that goes wrong, so it should sell. That is "
            "how the industry is built: small explorers find deposits, and the majors buy them and build them."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(tag), Create(be), FadeIn(bel))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.04), run_time=3.5)
            vo.wait_until("b")
            self.play(FadeIn(axis_g), Create(zero), FadeIn(zl), FadeIn(strips[0][0]))
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.2) for d in strips[0][1]], lag_ratio=0.004), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(strips[1][0]))
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.2) for d in strips[1][1]], lag_ratio=0.004), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(strips[2][0]), Create(strips[2][1]))
            vo.wait_until("e")
            self.play(FadeIn(verdict, shift=UP * 0.1))
        self.clear_scene()
