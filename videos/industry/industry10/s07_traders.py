from __future__ import annotations

from videos.industry.industry10.common import *  # noqa: F403


class Traders(VoiceoverScene):
    def construct(self):
        card(self, 6, "The grain traders", "Who moves the world's grain, and how do they make money?",
             "Chapter six. The grain traders.", lit=("make", "dollar"))
        self.journey()
        self.size()
        self.crush()

    def journey(self):
        wm = draw.world_map(12.8, lon=(-128, 150), lat=(-12, 58)).move_to([0, 0.2, 0])
        iowa, stl, nola = wm.p(-93.5, 42.0), wm.p(-90.2, 38.6), wm.p(-90.0, 29.5)
        pan, asia = wm.p(-79.6, 9.0), wm.p(121.0, 31.0)
        river = VMobject(stroke_color="#5DA9E9", stroke_width=3).set_points_smoothly([wm.p(-91.2, 44.5), wm.p(-91.0, 41.5), stl,
                                                                                       wm.p(-89.6, 35.0), wm.p(-91.2, 31.5), nola])
        sea = VMobject().set_points_smoothly([nola, wm.p(-86, 24), wm.p(-81, 17), pan, wm.p(-100, 10), wm.p(-150, 20),
                                              wm.p(170, 30), wm.p(140, 33), asia])
        sea.set_stroke(GREY_B, 1.5, opacity=0.6)
        sea_r = VMobject().set_points_smoothly([nola, wm.p(-86, 24), wm.p(-81, 17), pan])
        sea_r.set_stroke(GREY_B, 1.5, opacity=0.6)
        sea_p = VMobject().set_points_smoothly([pan, wm.p(-110, 12), wm.p(-127, 16)])
        sea_p.set_stroke(GREY_B, 1.5, opacity=0.6)
        sea_a = VMobject().set_points_smoothly([wm.p(150, 25), wm.p(132, 28), asia])
        sea_a.set_stroke(GREY_B, 1.5, opacity=0.6)
        elev = draw.grain_elevator(0.8).move_to(iowa + UP * 0.45)
        ship = draw.ship(0.6, boxes=0).move_to(nola)
        grain = Dot(iowa, radius=0.09, color=CORN)
        labs = VGroup(tx("an Iowa farm and elevator", 14, WHITE).next_to(elev, UP, buff=0.06),
                      tx("barges down the Mississippi", 14, "#5DA9E9").next_to(stl, RIGHT, buff=0.15),
                      tx("export elevators near New Orleans", 14, WHITE).next_to(nola, DOWN, buff=0.15),
                      tx("through the Panama Canal", 14, GREY_A).next_to(pan, DOWN, buff=0.12),
                      tx("to feed mills in Asia", 14, WHITE).next_to(asia, DOWN, buff=0.12),
                      tx("across the Pacific", 13, GREY_A).next_to(wm.p(-125, 16), UP, buff=0.08),
                      tx("across the Pacific", 13, GREY_A).next_to(wm.p(146, 25), DOWN, buff=0.08))
        src = source("the standard export route for US corn and soybeans; map: Natural Earth", size=13)
        with self.voiceover(
            "Follow a bushel of corn or soybeans after it leaves the farm. <bookmark mark='a'/> A truck takes it to a "
            "country elevator, a tall concrete store beside a railway or a river. <bookmark mark='b'/> From there it goes "
            "by train, or by barge, a few hundred thousand bushels to a string of barges, down the Mississippi. "
            "<bookmark mark='c'/> At export elevators on the river near New Orleans it is loaded onto ships, "
            "<bookmark mark='d'/> which carry it through the Panama Canal and across the Pacific, to feed mills that turn "
            "it into feed for pigs and chickens in China, Japan and Mexico. <bookmark mark='e'/> Almost every step of "
            "that journey, the elevators, the barges, the terminals and the contracts with the buyers abroad, belongs to "
            "a handful of trading companies."
        ) as vo:
            self.play(FadeIn(wm), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(elev), FadeIn(labs[0]), FadeIn(grain, scale=2))
            vo.wait_until("b")
            self.play(Create(river), FadeIn(labs[1]))
            self.play(MoveAlongPath(grain, VMobject().set_points_smoothly([iowa, wm.p(-91.0, 41.5), stl, wm.p(-89.6, 35.0),
                                                                           wm.p(-91.2, 31.5), nola])), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(ship), FadeIn(labs[2]), FadeOut(grain))
            vo.wait_until("d")
            self.play(Create(sea_r), FadeIn(labs[3]))
            self.play(MoveAlongPath(ship, sea_r), run_time=2.0)
            self.play(Create(sea_p), Create(sea_a), FadeIn(labs[4]), FadeIn(labs[5:]))
            vo.wait_until("e")
            self.play(Indicate(elev, color=TRADE), Indicate(labs[2], color=TRADE))
        self.clear_scene()

    def size(self):
        T = R["traders"]
        adm = T["adm"]
        ys = [y for y in sorted(adm) if y >= 2012]
        pa = viz.plot_axes([2011.4, 2025.6], [0, 110], x_length=6.0, y_length=3.8, xticks=[2012, 2016, 2020, 2025],
                           yticks=[25, 50, 75, 100], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}bn", size=13).move_to(
            [-3.2, -0.5, 0])
        rev = viz.year_bars(pa, ys, [adm[y][0] for y in ys], TRADE, width=0.3)
        prof = viz.year_bars(pa, ys, [adm[y][1] for y in ys], GREEN_C, width=0.3)
        pk = VGroup(tx("ADM: revenue (blue) and profit (green)", 16, WHITE, bold=True),
                    tx(f"profit was {100 * T['adm_margin']:.1f} cents per dollar of sales, on average, 2016-2025", 14, GREY_A)
                    ).arrange(DOWN, buff=0.04).next_to(pa, UP, buff=0.12)
        big = VGroup()
        bg = T["bg"]
        entries = [("Cargill", T["cargill"], "private; year to May 2025", TRADE), ("ADM", adm[2025][0], "2025", TRADE),
                   ("Bunge", bg[2025][0], "2025, after buying Viterra", TRADE), ("Louis Dreyfus", None, "private", TRADE)]
        for name, v, note, col in entries:
            if v:
                b = Rectangle(width=v / 160 * 3.3, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.85)
                txt = tx(f"${v:.0f}bn", 16, WHITE, bold=True)
            else:
                b = Rectangle(width=0.05, height=0.42, stroke_width=0, fill_opacity=0)
                txt = tx("(publishes no US filing)", 13, GREY_B)
            big.add(VGroup(tx(name, 17, WHITE, bold=True), b, txt, tx(note, 12, GREY_B)))
        for i, row in enumerate(big):
            y = 1.3 - 0.85 * i
            row[0].move_to([1.2, y, 0], aligned_edge=LEFT)
            row[1].move_to([2.8, y, 0], aligned_edge=LEFT)
            row[2].next_to(row[1], RIGHT, buff=0.1)
            row[3].next_to(row[0], DOWN, buff=0.04).align_to(row[0], LEFT)
        bt = tx("Revenue of the big grain traders", 18, WHITE, bold=True).move_to([3.6, 2.2, 0])
        pr_arrow = Arrow(pa.ax.c2p(2018.5, 30), pa.ax.c2p(2021, 4.5), buff=0.05, stroke_width=3, color=GREEN_C, tip_length=0.15)
        pr_lab = tx("the profit", 16, GREEN_C, bold=True).next_to(pr_arrow.get_start(), UP, buff=0.05)
        src = source("SEC EDGAR, ADM and Bunge Forms 10-K; Cargill, 2025 Annual Report", size=13)
        with self.voiceover(
            "Four companies dominate the world's grain trade, known in the business as the ABCD: ADM, Bunge, Cargill "
            "and Louis Dreyfus. <bookmark mark='a'/> They are among the largest companies on Earth by revenue. Cargill, "
            f"privately owned by its founding families, took in about {T['cargill']:.0f} billion dollars in the year to "
            f"May 2025. ADM, about {adm[2025][0]:.0f} billion in 2025. Bunge, about {bg[2025][0]:.0f} billion, after "
            "it bought the Canadian trader Viterra. <bookmark mark='b'/> But look at what they keep. ADM's profit has "
            f"averaged about {100 * T['adm_margin']:.0f} cents for every dollar of sales over the last ten years. "
            "<bookmark mark='c'/> A trader buys a bushel and sells it a few weeks later for almost the same price. It "
            "lives on volume, on the logistics it owns, and on the small differences in price between places, months "
            "and products."
        ) as vo:
            self.play(FadeIn(src), FadeIn(bt))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2:])) for r_ in big],
                                  lag_ratio=0.4), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(pa), FadeIn(pk))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in rev], lag_ratio=0.05), run_time=1.5)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in prof], lag_ratio=0.05), run_time=1.5)
            self.play(GrowArrow(pr_arrow), FadeIn(pr_lab))
            vo.wait_until("c")
            self.play(Indicate(pk[1], color=GREEN_C))
        self.clear_scene()

    def crush(self):
        C = R["traders"]["crush"]
        beans = VGroup(*[Circle(0.12, stroke_width=0, fill_color="#D9C27A", fill_opacity=1) for _ in range(30)]
                       ).arrange_in_grid(rows=5, cols=6, buff=0.04).move_to([-5.0, 1.6, 0])
        meal = VGroup(Rectangle(width=1.2, height=0.9, stroke_width=0, fill_color="#B5915A", fill_opacity=1),
                      tx(f"{C['meal'] * 60:.0f} lb meal", 14, WHITE)).arrange(DOWN, buff=0.06).move_to([-1.6, 2.1, 0])
        oil = VGroup(draw.bottle(0.9, color="#F2C14E", water=0.9), tx(f"{C['oil'] * 60:.0f} lb oil", 14, WHITE)).arrange(
            DOWN, buff=0.06).move_to([-1.6, 0.6, 0])
        arr = VGroup(Arrow(beans.get_right(), meal.get_left(), buff=0.15, stroke_width=2.5, color=GREY_B, tip_length=0.12),
                     Arrow(beans.get_right(), oil.get_left(), buff=0.15, stroke_width=2.5, color=GREY_B, tip_length=0.12))
        bl = tx("a 60-lb bushel of soybeans", 14, WHITE).next_to(beans, DOWN, buff=0.1)
        ms = C["months"]
        xs = [mx(m) for m in ms]
        pa = viz.plot_axes([1992, 2027], [0, 180], x_length=6.2, y_length=3.4, xticks=[1995, 2005, 2015, 2025],
                           yticks=[50, 100, 150], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}", size=13).move_to(
            [3.3, -0.6, 0])
        ln = VMobject(stroke_color=SOY, stroke_width=2.5).set_points_as_corners([pa.ax.c2p(x, v) for x, v in zip(xs, C["margin"])])
        pt = tx("meal + oil - beans, per tonne of beans (world prices)", 15, SOY, bold=True).next_to(pa, UP, buff=0.1)
        last = VGroup(Dot(pa.ax.c2p(xs[-1], C["last"]), color=WHITE, radius=0.06),
                      tx(f"{mlabel(C['last_month'])}: ${C['last']:.0f}", 15, WHITE, bold=True)).arrange(LEFT, buff=0.1)
        last.move_to(pa.ax.c2p(xs[-1], C["last"]), aligned_edge=RIGHT).shift(LEFT * 0.12 + DOWN * 0.05)
        avg = DashedLine(pa.ax.c2p(1992, C["avg"]), pa.ax.c2p(2027, C["avg"]), stroke_color=GREY_B, stroke_width=1.2)
        al = tx(f"average ${C['avg']:.0f}", 13, GREY_A).next_to(avg, UP, buff=0.04).align_to(avg, LEFT)
        tag = estimate_tag("illustrative: the IMF's world prices of beans, meal and oil, with CME's standard crush yields",
                           corner=DR, size=12)
        src = source("IMF primary commodity prices via FRED; CME Group, Soybean Crush Reference Guide", size=13)
        with self.voiceover(
            "Here is one of those differences. <bookmark mark='a'/> A soybean crusher, a business all four traders run, "
            "buys soybeans and presses them. By the exchange's standard reckoning, a sixty-pound bushel gives about "
            "forty-four pounds of meal, which feeds animals, <bookmark mark='b'/> and eleven pounds of oil, which goes "
            "into cooking and, increasingly, into diesel made from plants. <bookmark mark='c'/> The crusher's margin is "
            "what the meal and the oil sell for, less what the beans cost. On world prices, it has averaged about "
            f"{C['avg']:.0f} dollars a tonne of beans since 1992, a few percent of the price. <bookmark mark='d'/> In "
            f"2026 it jumped to about {C['last']:.0f} dollars, as American policies on biofuels pulled soybean oil into "
            "fuel tanks. Notice that the crusher does not care whether soybeans are dear or cheap. It cares about the "
            "gap. That is how a trader thinks, and why its margin is thin and steady while the farmer's swings."
        ) as vo:
            self.play(FadeIn(src), FadeIn(tag), FadeIn(beans), FadeIn(bl))
            vo.wait_until("a")
            self.play(GrowArrow(arr[0]), FadeIn(meal))
            vo.wait_until("b")
            self.play(GrowArrow(arr[1]), FadeIn(oil))
            vo.wait_until("c")
            self.play(FadeIn(pa), FadeIn(pt), Create(avg), FadeIn(al))
            self.play(Create(ln), run_time=4.0, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(last))
        self.clear_scene()
