from __future__ import annotations

from videos.industry.industry12.common import *  # noqa: F403


class Shale(VoiceoverScene):
    def construct(self):
        card(self, 4, "The shale advantage", "Why did a gas field in Pennsylvania change the price of plastic bags?",
             "Chapter four. The shale advantage.", lit=("make", "change"))
        self.well()
        self.ethane()
        self.gas()
        self.gap()

    def well(self):
        ground = Line([-7.2, 0.6, 0], [7.2, 0.6, 0], stroke_color="#6B5A45", stroke_width=3)
        earth = Rectangle(width=14.4, height=4.6, stroke_width=0, fill_color="#2A2420", fill_opacity=0.9).move_to([0, -1.7, 0])
        layer = Rectangle(width=14.4, height=0.7, stroke_width=0, fill_color="#3D3530", fill_opacity=1).move_to([0, -2.9, 0])
        ll = tx("a layer of shale, kilometres down", 14, GREY_B).move_to([-4.6, -3.45, 0])
        rig = draw.derrick(1.6).move_to([-4.5, 1.45, 0])
        bore = VMobject(stroke_color="#C9D3E0", stroke_width=3).set_points_smoothly(
            [[-4.5, 0.6, 0], [-4.5, -1.6, 0], [-4.2, -2.6, 0], [-3.4, -2.9, 0], [2.6, -2.9, 0]])
        fracs = VGroup(*[VGroup(Line([x, -2.9, 0], [x + 0.15, -2.6, 0]), Line([x, -2.9, 0], [x - 0.12, -3.2, 0]),
                                Line([x, -2.9, 0], [x + 0.2, -3.15, 0])).set_stroke("#F6C453", 1.5) for x in np.arange(-2.8, 2.7, 0.7)])
        mols = VGroup()
        rng = np.random.default_rng(12)
        kinds = ["CH4"] * 7 + ["C2H6"] * 3
        for k, kind in enumerate(kinds):
            m = draw.molecule(kind, bond=0.18 if kind == "CH4" else 0.17).move_to([-2.6 + 0.55 * k, -2.9 + 0.05 * rng.normal(), 0])
            mols.add(m)
        bub = Circle(1.15, stroke_color=GAS, stroke_width=2, fill_color=GAS, fill_opacity=0.06).move_to([3.6, -1.15, 0])
        inside = VGroup(*[draw.molecule(k_, bond=0.16 if k_ == "CH4" else 0.15) for k_ in ["CH4"] * 6 + ["C2H6"] * 2])
        inside.arrange_in_grid(rows=3, cols=3, buff=0.18)
        inside.scale_to_fit_width(min(inside.width, 1.55)).move_to(bub)
        blab = VGroup(tx("wet gas", 18, GAS, bold=True), tx("mostly methane, with ethane,", 14, GREY_A),
                      tx("propane and butane", 14, GREY_A)).arrange(DOWN, buff=0.04).next_to(bub, RIGHT, buff=0.2)
        if blab.get_right()[0] > 7.0:
            blab.next_to(bub, DOWN, buff=0.1)
        plant = draw.column(1.3).move_to([0.6, 1.4, 0])
        pl_lab = tx("gas processing plant", 15, GREY_A).next_to(plant, DOWN, buff=0.08)
        pipe_in = Line([-4.5, 0.75, 0], [plant.get_left()[0] - 0.05, 0.75, 0], stroke_color="#6C7686", stroke_width=4)
        out_m = VGroup(draw.molecule("CH4", bond=0.2), tx("methane: the pipeline,", 15, GAS, bold=True),
                       tx("homes and power plants", 15, GREY_A)).arrange(RIGHT, buff=0.15).move_to([4.6, 2.6, 0])
        out_e = VGroup(draw.molecule("C2H6", bond=0.2), tx("ethane:", 15, ETHYL, bold=True), tx("the cracker", 15, GREY_A)).arrange(
            RIGHT, buff=0.15).move_to([4.6, 1.2, 0])
        arr_m = Arrow(plant.get_right(), out_m.get_left(), buff=0.1, stroke_width=2.5, color=GAS, max_tip_length_to_length_ratio=0.15)
        arr_e = Arrow(plant.get_right(), out_e.get_left(), buff=0.1, stroke_width=2.5, color=ETHYL, max_tip_length_to_length_ratio=0.15)
        with self.voiceover(
            "To see why America's crackers are so cheap to run, go underground. <bookmark mark='a'/> In the 2000s, "
            "drillers learned to turn a well sideways inside a layer of shale and crack the rock open with water and "
            "sand under pressure, freeing gas that had been locked in it. <bookmark mark='b'/> Much of that gas is "
            "what the industry calls wet: mostly methane, but carrying ethane, propane and butane with it. "
            "<bookmark mark='c'/> At a gas processing plant the heavier molecules are separated out. The methane goes "
            "into the pipeline, to homes and power stations. <bookmark mark='d'/> The ethane can go to a cracker. And "
            "when ethane is too cheap to bother, producers simply leave it in the gas and sell it as fuel, which ties "
            "its price to the price of natural gas."
        ) as vo:
            self.play(FadeIn(earth), FadeIn(layer), Create(ground), FadeIn(rig), FadeIn(ll))
            vo.wait_until("a")
            self.play(Create(bore), run_time=2.0)
            self.play(LaggedStart(*[Create(f_) for f_ in fracs], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in mols], lag_ratio=0.08), FadeIn(bub), FadeIn(inside), FadeIn(blab),
                      run_time=1.5)
            self.play(LaggedStart(*[m.animate.move_to([-4.5, -0.6 + 0.12 * k, 0]).set_opacity(0.0) for k, m in enumerate(mols)],
                                  lag_ratio=0.08), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(plant), FadeIn(pl_lab), Create(pipe_in))
            self.play(GrowArrow(arr_m), FadeIn(out_m, shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(GrowArrow(arr_e), FadeIn(out_e, shift=RIGHT * 0.2))
        self.clear_scene()

    def ethane(self):
        f = R["feedstock"]
        eth_m = read_monthly("PET.M_EPLLEA_FPF_NUS_MBBLD.M")
        exp_m = read_monthly("PET.M_EPLLEA_EEX_NUS-Z00_2.M")
        x1 = mx(f["ethane_last_m"]) + 0.5
        pa = viz.plot_axes([1980.5, x1], [0, 3600], x_length=10.0, y_length=4.6, xticks=[1985, 1995, 2005, 2015, 2025],
                           yticks=[1000, 2000, 3000], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:,.0f}",
                           ylabel="thousand barrels a day", size=14).move_to([-0.3, -0.4, 0])
        xs = sorted(exp_m.items())
        ex = Polygon(*[pa.ax.c2p(mx(m), v) for m, v in xs], pa.ax.c2p(mx(xs[-1][0]), 0), pa.ax.c2p(mx(xs[0][0]), 0),
                     stroke_width=0, fill_color=GAS, fill_opacity=0.55)
        shale = Rectangle(width=pa.ax.c2p(x1, 0)[0] - pa.ax.c2p(2008, 0)[0], height=4.6, stroke_width=0, fill_color=WHITE,
                          fill_opacity=0.05).move_to(pa.ax.c2p(2008, 0), aligned_edge=DL)
        sl = tx("the shale era", 14, GREY_B).next_to(shale, UP, buff=0.05).align_to(shale, LEFT)
        d0 = Dot(pa.ax.c2p(mx(f["ethane_first_m"]), f["ethane_first"]), radius=0.06, color=ETHYL)
        l0 = tx(f"{f['ethane_first']:,.0f} ({mlabel(f['ethane_first_m'])})", 15, ETHYL).next_to(d0, UP, buff=0.1)
        d1 = Dot(pa.ax.c2p(mx(f["ethane_last_m"]), f["ethane_last"]), radius=0.06, color=ETHYL)
        l1 = tx(f"{f['ethane_last']:,.0f} ({mlabel(f['ethane_last_m'])})", 15, ETHYL, bold=True).next_to(d1, LEFT, buff=0.12)
        xl = tx(f"exports: {f['exports_last']:,.0f}", 15, GAS, bold=True).next_to(pa.ax.c2p(mx(f["exports_last_m"]),
                                                                                         f["exports_last"]), UP + LEFT, buff=0.1)
        head = tx("American ethane, produced and exported", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("EIA, natural gas plant field production of ethane and exports of ethane (monthly)", size=13)
        e15 = f["ethane"][2015]
        with self.voiceover(
            "Here is what shale did to the supply of ethane. <bookmark mark='a'/> For a quarter of a century, America "
            f"produced around half a million barrels a day, {f['ethane_first']:,.0f} thousand in "
            f"{mlabel(f['ethane_first_m']).split()[1]}, by the Energy Information Administration's count. "
            "<bookmark mark='b'/> Then the shale gas came, and the ethane came with it. <bookmark mark='c'/> By "
            f"{mlabel(f['ethane_last_m'])}, about {f['ethane_last']:,.0f} thousand barrels a day, about "
            f"{f['ethane_last'] / e15:.0f} times the average as recently as 2015. <bookmark mark='d'/> So much that "
            f"America now sells it abroad, by pipeline and in specially built ships: exports started in "
            f"{f['exports_first_m'][:4]} and reached about {f['exports_last']:,.0f} thousand barrels a day."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(pa))
            vo.wait_until("a")
            em = sorted(eth_m.items())
            part1 = poly(pa, [(mx(m), v) for m, v in em if m <= "2008-01"], ETHYL, 3)
            part2 = poly(pa, [(mx(m), v) for m, v in em if m >= "2008-01"], ETHYL, 3)
            self.play(Create(part1), FadeIn(d0), FadeIn(l0), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(shale), FadeIn(sl))
            self.play(Create(part2), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(d1), FadeIn(l1, shift=LEFT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(ex), FadeIn(xl), run_time=1.5)
        self.clear_scene()

    def gas(self):
        P = R["prices"]
        ys = P["years"]
        pa = viz.plot_axes([1999.5, ys[-1] + 0.5], [0, 40], x_length=9.4, y_length=4.6, xticks=[2000, 2005, 2010, 2015, 2020, 2025],
                           yticks=[10, 20, 30, 40], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}",
                           ylabel="dollars per million Btu, annual average", size=14).move_to([-1.0, -0.4, 0])
        cols = {"us": TEXAS, "eu": EUROPE, "asia": ASIA}
        segs = [{k: poly(pa, [(y, P[k][y]) for y in ys if lo <= y <= hi], c, 3.5) for k, c in cols.items()}
                for lo, hi in ((2000, 2008), (2008, 2021), (2021, ys[-1]))]
        names = {"us": "America (Henry Hub)", "eu": "Europe (Dutch TTF)", "asia": "Asia (Japan's imported LNG)"}
        key = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=c, stroke_width=4), tx(names[k], 15, c)).arrange(RIGHT, buff=0.1)
                       for k, c in (("asia", ASIA), ("eu", EUROPE), ("us", TEXAS))]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(
            [4.6, 2.2, 0])
        y13 = 2013
        c13 = VGroup(tx(f"{y13}", 16, WHITE, bold=True), tx(f"America ${P['us'][y13]:.2f}", 15, TEXAS),
                     tx(f"Europe ${P['eu'][y13]:.2f}", 15, EUROPE), tx(f"Asia ${P['asia'][y13]:.2f}", 15, ASIA)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04).move_to([4.6, 0.2, 0])
        c22 = VGroup(tx("2022", 16, WHITE, bold=True), tx(f"America ${P['us'][2022]:.2f}", 15, TEXAS),
                     tx(f"Europe ${P['eu'][2022]:.2f}", 15, EUROPE), tx(f"Asia ${P['asia'][2022]:.2f}", 15, ASIA)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04).move_to([4.6, -1.6, 0])
        head = tx("Natural gas in three markets", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("IMF Primary Commodity Prices via FRED (annual averages of monthly prices; 2026 to date)", size=13)
        with self.voiceover(
            "Gas, unlike oil, is expensive to move across oceans: it has to be chilled into a liquid and shipped. So "
            "it has no single world price. <bookmark mark='a'/> Until about 2008, America, Europe and Asia paid roughly "
            "the same. <bookmark mark='b'/> Then shale flooded the American market, and its price fell away from the "
            f"rest. In {y13}, gas cost {P['us'][y13]:.2f} dollars per million British thermal units in America, "
            f"{P['eu'][y13]:.2f} in Europe and {P['asia'][y13]:.2f} in Asia. <bookmark mark='c'/> And in 2022, when "
            f"Russia cut off most of its gas to Europe, Europe paid {P['eu'][2022]:.0f} dollars, about "
            f"{P['eu'][2022] / P['us'][2022]:.0f} times America's {P['us'][2022]:.2f}. Every cracker and every ammonia plant in Europe paid it too."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(pa), FadeIn(key))
            vo.wait_until("a")
            self.play(*[Create(v) for v in segs[0].values()], run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(*[Create(v) for v in segs[1].values()], run_time=3.0, rate_func=linear)
            self.play(FadeIn(c13, shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(*[Create(v) for v in segs[2].values()], run_time=2.0, rate_func=linear)
            self.play(FadeIn(c22, shift=LEFT * 0.1), Flash(pa.ax.c2p(2022, P["eu"][2022]), color=EUROPE))
        self.clear_scene()

    def gap(self):
        f = R["feedstock"]
        ys = R["prices"]["years"]
        ct, ce = f["cost"]["Texas, ethane"], f["cost"]["Europe, naphtha"]
        pa = viz.plot_axes([1999.5, ys[-1] + 0.5], [0, 1600], x_length=8.8, y_length=4.6, xticks=[2000, 2005, 2010, 2015, 2020, 2025],
                           yticks=[400, 800, 1200, 1600], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:,.0f}",
                           ylabel="cash cost of a tonne of ethylene", size=14).move_to([-1.6, -0.4, 0])
        lt1, lt2 = (poly(pa, [(y, ct[y]) for y in ys if lo <= y <= hi], TEXAS, 3.5) for lo, hi in ((2000, 2006), (2006, ys[-1])))
        le1, le2 = (poly(pa, [(y, ce[y]) for y in ys if lo <= y <= hi], EUROPE, 3.5) for lo, hi in ((2000, 2006), (2006, ys[-1])))
        band = Polygon(*[pa.ax.c2p(y, ce[y]) for y in ys], *[pa.ax.c2p(y, ct[y]) for y in reversed(ys)], stroke_width=0,
                       fill_color=TEXAS, fill_opacity=0.16)
        key = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=c, stroke_width=4), tx(t_, 15, c)).arrange(RIGHT, buff=0.1)
                       for c, t_ in ((EUROPE, "Europe, naphtha"), (TEXAS, "Texas, ethane"))]).arrange(DOWN, aligned_edge=LEFT,
                                                                                                     buff=0.1).move_to([4.7, 2.2, 0])
        g = f["gap"]
        early = [y for y in ys if y <= 2005]
        late = [y for y in ys if y >= 2010]
        e_avg = float(np.mean([g[y] for y in early]))
        l_avg = float(np.mean([g[y] for y in late]))
        notes = VGroup(tx(f"{early[0]}-{early[-1]}: on average", 15, GREY_A),
                       tx(f"within ${abs(e_avg):,.0f} a tonne", 18, WHITE, bold=True),
                       tx(f"{late[0]}-{late[-1]}: Texas cheaper by", 15, GREY_A), tx(f"${l_avg:,.0f} a tonne", 24, TEXAS, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.05)
        notes[2].shift(DOWN * 0.3)
        notes[3].shift(DOWN * 0.3)
        notes.move_to([5.4, -0.4, 0])
        head = tx("The same plant, on two feedstocks", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        tag = estimate_tag("the Works (cracker.py), with the IMF's gas and Brent prices", corner=DR, size=12)
        with self.voiceover(
            "Put those prices through the Works' cracker, and you see the shale advantage open up. <bookmark mark='a'/> "
            "In the early 2000s, ethane in Texas and naphtha in Europe made ethylene for about the same cost: on "
            f"average, the two were within {abs(e_avg):.0f} dollars a tonne of each other. <bookmark mark='b'/> From 2010, the gap "
            f"averaged about {l_avg:,.0f} dollars a tonne, in a product that sells for around a thousand. "
            "<bookmark mark='c'/> It is not a better machine. It is the same machine with cheaper molecules, and an "
            "advantage that lasts as long as American gas stays cheap and stranded on its own continent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(pa), FadeIn(key))
            vo.wait_until("a")
            self.play(Create(le1), Create(lt1), run_time=2.5, rate_func=linear)
            self.play(FadeIn(notes[:2]))
            vo.wait_until("b")
            self.play(Create(le2), Create(lt2), run_time=3.0, rate_func=linear)
            self.play(FadeIn(band), FadeIn(notes[2:]))
            vo.wait_until("c")
            self.play(Indicate(notes[3], color=TEXAS))
        self.clear_scene()


def poly(pa, pts, color, width) -> VMobject:
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners([pa.ax.c2p(x, y) for x, y in pts])


def read_monthly(series: str) -> dict:
    from explainer.industry.data.fetch import read
    return {str(r["month"]): r["value"] for r in read("eia_ngl") if r["series"] == series and r["value"] is not None}
