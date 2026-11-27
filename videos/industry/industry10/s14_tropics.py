from __future__ import annotations

from videos.industry.industry10.common import *  # noqa: F403


class Tropics(VoiceoverScene):
    def construct(self):
        card(self, 12, "Cocoa, and the world's plate", "What happens when one crop comes from one corner of the world?",
             "Chapter twelve. Cocoa, and the world's plate.", lit=("change", "unit"))
        self.cocoa()
        self.squeeze()
        self.plate()

    def cocoa(self):
        C = R["cocoa"]
        wm = draw.world_map(9.0, lon=(-25, 60), lat=(-30, 40)).move_to([-2.6, 0.1, 0])
        civ, gha = wm.p(-5.5, 7.5), wm.p(-1.2, 7.8)
        bub = VGroup(Circle(0.035 * np.sqrt(C["civ"]), stroke_color=COCOA, stroke_width=2, fill_color=COCOA, fill_opacity=0.6
                            ).move_to(civ),
                     Circle(0.035 * np.sqrt(C["gha"]), stroke_color=COCOA, stroke_width=2, fill_color=COCOA, fill_opacity=0.6
                            ).move_to(gha))
        labs = VGroup(VGroup(tx("Côte d'Ivoire", 15, WHITE, bold=True), tx(f"{C['civ']:,.0f} kt", 14, COCOA)).arrange(
            DOWN, buff=0.02).next_to(bub[0], LEFT, buff=0.1),
                      VGroup(tx("Ghana", 15, WHITE, bold=True), tx(f"{C['gha']:,.0f} kt", 14, COCOA)).arrange(
            DOWN, buff=0.02).next_to(bub[1], RIGHT, buff=0.1))
        pods = VGroup(*[draw.cocoa_pod(0.5) for _ in range(5)]).arrange(RIGHT, buff=0.15).move_to([-2.6, -2.6, 0])
        share = VGroup(tx(f"{100 * C['share']:.0f}% of the world's cocoa beans, 2022/23", 18, COCOA, bold=True),
                       tx(f"next season: world crop -{100 * (1 - C['world24'] / C['world']):.0f}%", 16, STATE)).arrange(
            DOWN, buff=0.05).next_to(pods, UP, buff=0.15)
        ms = C["months"]
        sel = [(m, v) for m, v in zip(ms, C["price"]) if m >= "2015-01"]
        pa = viz.plot_axes([2015, 2027], [0, 12000], x_length=4.6, y_length=3.4, xticks=[2015, 2020, 2025],
                           yticks=[3000, 6000, 9000, 12000], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v / 1000:g}k",
                           size=12).move_to([4.4, 0.0, 0])
        ln = VMobject(stroke_color=COCOA, stroke_width=3).set_points_as_corners([pa.ax.c2p(mx(m), v) for m, v in sel])
        pk = VGroup(Dot(pa.ax.c2p(mx(C["peak"]), C["peak_val"]), color=WHITE, radius=0.06),
                    tx(f"{mlabel(C['peak'])}: ${C['peak_val']:,.0f}", 13, WHITE, bold=True))
        pk[1].next_to(pk[0], LEFT, buff=0.1)
        pt = tx("cocoa, dollars a tonne", 15, COCOA, bold=True).next_to(pa, UP, buff=0.1)
        src = source("ICCO, Quarterly Bulletin of Cocoa Statistics (February 2025); IMF cocoa price via FRED; map: Natural "
                     "Earth", size=13)
        with self.voiceover(
            "Some crops come from almost everywhere. Cocoa comes from one corner of one continent. "
            "<bookmark mark='a'/> In the 2022 to 2023 season, two neighbouring countries in West Africa, Côte d'Ivoire "
            f"and Ghana, grew about {100 * C['share']:.0f} percent of the world's cocoa beans, almost all of it on "
            "small family farms of a few hectares each. <bookmark mark='b'/> The next season, bad weather and a "
            "spreading tree virus cut the crop, and the world's harvest fell by about "
            f"{100 * (1 - C['world24'] / C['world']):.0f} percent. <bookmark mark='c'/> Because chocolate eaters do not "
            "stop eating chocolate, the price did the rationing. Cocoa had cost about "
            f"{C['y2022']:,.0f} dollars a tonne in 2022. By {mlabel(C['peak'])} it cost {C['peak_val']:,.0f}, more than "
            f"four times as much. It has since fallen back to about {C['last']:,.0f}."
        ) as vo:
            self.play(FadeIn(wm), FadeIn(src), FadeIn(pods))
            vo.wait_until("a")
            self.play(GrowFromCenter(bub[0]), GrowFromCenter(bub[1]), FadeIn(labs), FadeIn(share[0]))
            vo.wait_until("b")
            self.play(FadeIn(share[1]), *[p.animate.set_opacity(0.3) for p in pods[3:]])
            vo.wait_until("c")
            self.play(FadeIn(pa), FadeIn(pt))
            self.play(Create(ln), run_time=3.0)
            self.play(FadeIn(pk))
        self.clear_scene()

    def squeeze(self):
        C = R["cocoa"]
        ys = sorted(C["hsy"])
        pa = viz.plot_axes([2018.4, 2025.6], [0, 22], x_length=6.0, y_length=3.6, xticks=ys, yticks=[5, 10, 15, 20],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}%", size=13).move_to([-2.2, -0.4, 0])
        hb = VGroup()
        mb = VGroup()
        for y in ys:
            for g, d, dx, col in ((hb, C["hsy"], -0.17, BRAND), (mb, C["mdlz"], 0.17, COCOA)):
                m = 100 * d[y][1] / d[y][0]
                p0, p1 = pa.ax.c2p(y + dx, 0), pa.ax.c2p(y + dx, m)
                g.add(Rectangle(width=0.3, height=p1[1] - p0[1], stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(
                    [p0[0], (p0[1] + p1[1]) / 2, 0]))
        key = VGroup(VGroup(Square(0.18, stroke_width=0, fill_color=BRAND, fill_opacity=1), tx("Hershey", 15, WHITE)).arrange(
            RIGHT, buff=0.08), VGroup(Square(0.18, stroke_width=0, fill_color=COCOA, fill_opacity=1),
                                     tx("Mondelez (Cadbury, Milka, Oreo)", 15, WHITE)).arrange(RIGHT, buff=0.08)).arrange(
            RIGHT, buff=0.4).next_to(pa, UP, buff=0.12)
        pt = tx("profit as a share of sales", 15, GREY_A).next_to(key, UP, buff=0.06)
        side = VGroup(tx("Where the farmer stands:", 19, WHITE, bold=True),
                      tx("in both countries a state board sets", 16, GREY_A),
                      tx("the price paid to farmers each season,", 16, GREY_A),
                      tx("and sells much of the crop ahead.", 16, GREY_A),
                      tx("When the world price leapt, the price", 16, WHITE),
                      tx("at the farm gate rose far less.", 16, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to(
            [4.4, -0.3, 0])
        src = source("SEC EDGAR, Hershey and Mondelez Forms 10-K", size=13)
        with self.voiceover(
            "Who paid? <bookmark mark='a'/> The chocolate makers, at first. Hershey kept about sixteen cents of each "
            "dollar for years; in 2025, about "
            f"{100 * C['hsy'][2025][1] / C['hsy'][2025][0]:.0f}. Mondelez, the owner of Cadbury and Milka, fell to about "
            f"{100 * C['mdlz'][2025][1] / C['mdlz'][2025][0]:.0f}. Then shoppers paid, as chocolate prices rose. <bookmark mark='b'/> And the farmers? In Côte d'Ivoire and Ghana, a state board sets the price "
            "paid to cocoa farmers for each season and sells much of the crop a year or more ahead. That protects "
            "farmers from crashes, but when the world price leapt, the price at the farm gate rose far more slowly. The "
            "boards' answer to a volatile price "
            "was the farmer's forward sale, made by the state."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(key), FadeIn(pt), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(a, DOWN), GrowFromEdge(b, DOWN)) for a, b in zip(hb, mb)],
                                  lag_ratio=0.2), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.25), run_time=2.0)
        self.clear_scene()

    def plate(self):
        cal = R["calories"]
        cols = {"United States": GREY_B, "China": STATE, "World": WHITE, "India": FARM, "Africa": COCOA}
        pa = viz.plot_axes([1961, 2025], [1300, 4100], x_length=10.0, y_length=4.6, xticks=[1961, 1980, 2000, 2024],
                           yticks=[1500, 2000, 2500, 3000, 3500, 4000], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:,.0f}",
                           ylabel="food supply per person per day, kilocalories", size=14).move_to([-0.6, -0.4, 0])
        t = ValueTracker(1961)

        def line(e):
            pts = sorted(cal[e].items())

            def f():
                q = [pa.ax.c2p(y, v) for y, v in pts if y <= t.get_value()]
                return VMobject(stroke_color=cols[e], stroke_width=3.5 if e == "World" else 2.5).set_points_as_corners(
                    q) if len(q) > 1 else VMobject()
            return always_redraw(f)
        lines = VGroup(*[line(e) for e in cols])
        labs = VGroup(*[tx(f"{e}: {cal[e][1961]:,.0f} → {cal[e][2024]:,.0f}", 15, cols[e], bold=True).next_to(
            pa.ax.c2p(2024, cal[e][2024]), RIGHT, buff=0.12) for e in cols])
        labs[2].shift(UP * 0.05)
        head = tx("How much food there is for each person on Earth", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("FAO food balance sheets via Our World in Data", size=13)
        with self.voiceover(
            "Step back and look at the whole world's plate. <bookmark mark='a'/> The Food and Agriculture "
            "Organization adds up all the food each country produces and imports, less exports, waste and animal feed, "
            f"and divides by its people. In 1961 the world had about {cal['World'][1961]:,.0f} kilocalories of food a "
            f"day for each person. In 2024, about {cal['World'][2024]:,.0f}, for a population more than two and a half "
            f"times as large. <bookmark mark='b'/> China went from about {cal['China'][1961]:,.0f}, the years of the "
            f"great famine, to {cal['China'][2024]:,.0f}. India from {cal['India'][1961]:,.0f} to "
            f"{cal['India'][2024]:,.0f}. <bookmark mark='c'/> Africa has gained least, and still has the least: that is "
            "where the next green revolution is needed. But the treadmill that made farming such a hard business made "
            "the world fed."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(src))
            self.add(lines)
            vo.wait_until("a")
            self.play(t.animate.set_value(2024), run_time=6.0, rate_func=linear)
            self.play(FadeIn(labs[2]))
            vo.wait_until("b")
            self.play(FadeIn(labs[1]), FadeIn(labs[3]))
            vo.wait_until("c")
            self.play(FadeIn(labs[4]), FadeIn(labs[0]))
        for l_ in lines:
            l_.clear_updaters()
        self.clear_scene()
