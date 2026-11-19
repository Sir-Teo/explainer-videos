from __future__ import annotations

from videos.economics.econ2.common import *  # noqa: F403


def month_x(m: str) -> float:
    return int(m[:4]) + (int(m[5:7]) - 0.5) / 12


class Frost(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Shifts: a frost in Brazil", r"When a price jumps, which curve moved?",
             "Chapter seven. Shifts: a frost in Brazil.", lit={1975: r"the black frost"},
             scale=("market", "world"), horizon=("a year", "a decade"))
        self.storms()
        self.rules()
        self.frost()
        self.reading()
        self.later()

    # ------------------------------------------------------------------
    def storms(self):
        f = load("fish")
        L, S = Linear(**f["line"]), Linear(**f["storm_line"])
        ax = price_axes(320, (1.5, 4.5), x_length=7.2, y_length=4.8, qticks=[0, 80, 160, 240, 320],
                        pticks=[1.5, 2, 2.5, 3, 3.5, 4, 4.5], qlabel=r"fish sold in a day", plabel=r"price",
                        center=LEFT * 2.4 + DOWN * 0.35)
        a = ax.ax

        def seg(lin, demand, color, dash=False):
            ps = np.linspace(1.5, 4.5, 2)
            qs = [float(lin.qd(x) if demand else lin.qs(x)) for x in ps]
            mob = (DashedLine if dash else Line)(a.c2p(qs[0], ps[0]), a.c2p(qs[1], ps[1]), color=color,
                                                 stroke_width=3 if dash else 4)
            return mob

        dem = seg(L, True, E.TRUTH, dash=True)
        sup = seg(L, False, E.SUPPLY)
        sup_s = seg(S, False, STORM)
        calm = VGroup(*[Dot(a.c2p(x["q"], x["p"]), radius=0.045, color=E.FISH) for x in f["days"] if not x["storm"]])
        storm = VGroup(*[Dot(a.c2p(x["q"], x["p"]), radius=0.06, color=STORM) for x in f["days"] if x["storm"]])
        leg = VGroup(
            label(r"calm days", font_size=22, color=E.FISH),
            label(r"stormy days: \ a third of the boats ashore", font_size=22, color=STORM),
            label(r"dashed: \ the planted demand line", font_size=22, color=E.TRUTH),
            label(r"supply, \ calm and stormy", font_size=22, color=E.SUPPLY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.45).shift(UP * 1.2)
        moved = VGroup(label(r"supply moved;", font_size=26, color=E.ACCENT),
                       label(r"the price slid along demand", font_size=26, color=E.ACCENT)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1)
        moved.next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        e0, e1 = f["eq"], f["storm_eq"]
        arrow = Arrow(a.c2p(e0["q"], e0["p"]), a.c2p(e1["q"], e1["p"]), buff=0.1, color=E.ACCENT, stroke_width=4)
        tag = island_tag(rf"simulated: the Island, {len(f['days'])} market days", corner=DR, font_size=16)
        with self.voiceover(
            "Prices move because one of the blades moves. Start where we know the truth: the Island's fish "
            f"market, over {len(f['days'])} market days. <bookmark mark='a'/> On calm days the boats go out, and the "
            "price and the catch settle near the same spot, scattered a little because the villagers' appetites "
            "vary from day to day. <bookmark mark='b'/> On stormy days a third of the boats stay ashore. "
            "<bookmark mark='c'/> The supply curve swings to the left, and the price rises and the catch falls. "
            "<bookmark mark='d'/> The stormy days lie along the planted demand line, because nothing about the "
            "buyers changed: the price moved along their curve."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(sup), FadeIn(leg[3]))
            self.play(LaggedStart(*[FadeIn(dd, scale=0.5) for dd in calm], lag_ratio=0.01), FadeIn(leg[0]), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(dd, scale=0.5) for dd in storm], lag_ratio=0.05), FadeIn(leg[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(TransformFromCopy(sup, sup_s), run_time=1.5)
            self.play(GrowArrow(arrow))
            vo.wait_until("d")
            self.play(Create(dem), FadeIn(leg[2]))
            self.play(FadeIn(moved, shift=UP * 0.1))
        self.clear_scene()

    def rules(self):
        head = heading(r"Which blade moved?")
        rows = [
            (r"price up, \ quantity down", r"supply fell", r"a frost, \ a storm, \ a tax", E.SUPPLY),
            (r"price down, \ quantity up", r"supply rose", r"a new machine, \ a bumper crop", E.SUPPLY),
            (r"price up, \ quantity up", r"demand rose", r"a fashion, \ a richer town", E.DEMAND),
            (r"price down, \ quantity down", r"demand fell", r"a substitute, \ a recession", E.DEMAND),
        ]
        table = VGroup()
        for see, means, eg, col in rows:
            table.add(VGroup(label(see, font_size=26, color=WHITE), label(means, font_size=26, color=col),
                             label(eg, font_size=22, color=GREY_B)))
        for r in table:
            r[0].move_to([-4.0, 0, 0])
            r[1].move_to([0.4, 0, 0])
            r[2].move_to([4.3, 0, 0])
        table.arrange(DOWN, buff=0.45).move_to(DOWN * 0.2)
        heads = VGroup(label(r"you see", font_size=22, color=GREY_A).move_to([-4.0, 0, 0]),
                       label(r"it means", font_size=22, color=GREY_A).move_to([0.4, 0, 0]),
                       label(r"for instance", font_size=22, color=GREY_A).move_to([4.3, 0, 0]))
        heads.next_to(table, UP, buff=0.4)
        for h, x in zip(heads, (-4.0, 0.4, 4.3)):
            h.set_x(x)
        foot = label(r"comparative statics: \ move one blade, \ hold the other still, \ compare", font_size=24,
                     color=E.ACCENT).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "That gives a habit of thought economists use every day. <bookmark mark='a'/> When the price rises and "
            "the quantity falls, supply has fallen: a frost, a storm, a new tax on sellers. When the price falls "
            "and the quantity rises, supply has risen. <bookmark mark='b'/> When both rise together, demand has "
            "risen; when both fall, demand has fallen. <bookmark mark='c'/> It's called comparative statics: move "
            "one blade, hold the other still, and compare where the market settles. When both blades move at once, "
            "you need more than two points, and that is the subject of Part four."
        ) as vo:
            self.play(FadeIn(head), FadeIn(heads))
            vo.wait_until("a")
            self.play(FadeIn(table[0], shift=UP * 0.1))
            self.play(FadeIn(table[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(table[2], shift=UP * 0.1))
            self.play(FadeIn(table[3], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()

    def frost(self):
        d = load("frost")
        hc = history_card(r"18 July 1975", r"the black frost, \ Paran\'a, \ southern Brazil",
                          r"a hard frost kills coffee trees across the state that grew most of Brazil's coffee",
                          color=STORM, width=6.6, font_size=24).to_corner(UL, buff=0.45)
        crop = price_axes(2, (0, 80), x_length=4.4, y_length=2.6, qticks=None, pticks=[0, 20, 40, 60, 80],
                          qlabel="", plabel=r"million 60 kg bags", money=False, font_size=18)
        crop.to_corner(UR, buff=0.5).shift(DOWN * 0.2)
        ca = crop.ax
        groups = VGroup()
        for k, (name, v0, v1) in enumerate(((r"Brazil", d["brazil_1975"], d["brazil_1976"]),
                                            (r"the world", d["world_1975"], d["world_1976"]))):
            b0 = Rectangle(width=0.5, height=ca.c2p(0, v0 / 1000)[1] - ca.c2p(0, 0)[1], stroke_width=0,
                           fill_color=COFFEE, fill_opacity=0.85).move_to((ca.c2p(k + 0.3, 0) + ca.c2p(k + 0.3, v0 / 1000)) / 2)
            b1 = Rectangle(width=0.5, height=ca.c2p(0, v1 / 1000)[1] - ca.c2p(0, 0)[1], stroke_width=0,
                           fill_color=STORM, fill_opacity=0.85).move_to((ca.c2p(k + 0.7, 0) + ca.c2p(k + 0.7, v1 / 1000)) / 2)
            n = label(name, font_size=19, color=GREY_A).next_to(ca.c2p(k + 0.5, 0), DOWN, buff=0.15)
            ch = label(pct(v1 / v0 - 1, 0), font_size=20, color=WHITE).next_to(b1, UP, buff=0.08)
            groups.add(VGroup(b0, b1, n, ch))
        crop_leg = label(r"brown: \ 1975/76 crop; \ grey: \ 1976/77", font_size=17, color=GREY_B).next_to(crop, DOWN,
                                                                                                          buff=0.45)
        months = d["months"]
        ara = np.array(d["arabica"])
        ax = year_axis((1970, 1981), (0, 8), x_length=8.6, y_length=2.7, xticks=list(range(1970, 1982, 2)),
                       yticks=[0, 2, 4, 6, 8], ylabel=r"Arabica coffee, \ dollars a kilo (as quoted then)",
                       yfmt=lambda v: rf"\${v:.0f}", center=DOWN * 1.75 + LEFT * 1.9, font_size=18)
        a = ax.ax
        xs = [month_x(m) for m in months]
        t = ValueTracker(1)
        line = always_redraw(lambda: VMobject(stroke_color=COFFEE, stroke_width=3).set_points_as_corners(
            [a.c2p(x, y) for x, y in zip(xs[:max(int(t.get_value()), 2)], ara[:max(int(t.get_value()), 2)])]))
        i75 = months.index("1975-06")
        ipk = months.index(d["peak_month"])
        n75 = VGroup(Dot(a.c2p(xs[i75], ara[i75]), radius=0.06, color=WHITE),
                     label(rf"June 1975: \ {dollars(d['june75'])}", font_size=19, color=WHITE))
        n75[1].next_to(n75[0], UL, buff=0.08)
        npk = VGroup(Dot(a.c2p(xs[ipk], ara[ipk]), radius=0.07, color=E.ACCENT),
                     label(rf"April 1977: \ {dollars(d['peak'])}", font_size=20, color=E.ACCENT))
        npk[1].next_to(npk[0], RIGHT, buff=0.12)
        frost_line = DashedLine(a.c2p(1975.54, 0), a.c2p(1975.54, 8), color=STORM, stroke_width=2)
        src = data_tag(r"World Bank Pink Sheet (Nov 2026); \ USDA FAS, PSD Online; \ retrieved 18 Nov 2026",
                       corner=DR, font_size=15).shift(UP * 0.1)
        with self.voiceover(
            "Now the real world, where nothing is planted. <bookmark mark='a'/> On the night of the eighteenth of "
            "July 1975, a black frost, so called because it blackens the leaves, swept across Paraná, in southern "
            "Brazil, the state that grew much of Brazil's coffee. <bookmark mark='b'/> According to the United "
            "States Department of Agriculture, Brazil's next crop was "
            f"{abs(100 * d['brazil_change']):.0f} percent smaller than the one before: from "
            f"{d['brazil_1975'] / 1000:.1f} million sacks to {d['brazil_1976'] / 1000:.1f} million. Brazil grew "
            f"about {100 * d['brazil_share_1975']:.0f} percent of the world's coffee, so the world's crop fell "
            f"{abs(100 * d['world_change']):.0f} percent. <bookmark mark='c'/> Here is the price of Arabica coffee, "
            "month by month, as it was quoted at the time. <bookmark mark='d'/> In June 1975 it was "
            f"{money_words(d['june75'])} a kilo. <bookmark mark='e'/> The frost hit, and the price climbed for "
            f"nearly two years, to {money_words(d['peak'])} in April 1977: "
            f"{d['ratio_peak_june75']:.1f} times as much."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(crop))
            for g in groups:
                self.play(GrowFromEdge(g[0], DOWN), FadeIn(g[2]), run_time=0.6)
                self.play(GrowFromEdge(g[1], DOWN), FadeIn(g[3]), run_time=0.6)
            self.play(FadeIn(crop_leg))
            vo.wait_until("c")
            self.play(FadeIn(ax))
            self.add(line)
            self.play(t.animate.set_value(i75 + 1), run_time=2.5, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(n75), Create(frost_line))
            vo.wait_until("e")
            self.play(t.animate.set_value(len(xs)), run_time=4, rate_func=linear)
            self.play(FadeIn(npk))
        line.clear_updaters()
        self.clear_scene()

    def reading(self):
        d = load("frost")
        eq = MathTex(r"\varepsilon \approx \frac{\%\,\Delta Q}{\%\,\Delta P} = "
                     rf"\frac{{{100 * (d['world_1976'] - d['world_1975']) / ((d['world_1976'] + d['world_1975']) / 2):.0f}\%}}"
                     rf"{{+{100 * (d['p1977'] - d['p1975']) / ((d['p1977'] + d['p1975']) / 2):.0f}\%}} \approx {d['arc']:.2f}",
                     font_size=46).to_edge(UP, buff=0.7)
        sub = label(r"midpoint changes: \ the world's crop, \ 1975/76 to 1976/77; \ the average Arabica price, \ 1975 "
                    r"to 1977", font_size=21, color=GREY_B).next_to(eq, DOWN, buff=0.3)
        caveats = point_cards([
            (r"stocks", r"warehouses sold coffee picked in earlier years, \ so less was drunk than the crop alone "
             r"suggests", COFFEE),
            (r"expectations", r"traders bid for the next harvests too, \ which were also damaged", STORM),
            (r"the long run", r"supply came back: \ the world's crop recovered by 1978, \ and the price fell", E.SUPPLY),
        ], width=12.8, cols=3, font_size=22).move_to(DOWN * 1.3)
        with self.voiceover(
            "What does that tell us? <bookmark mark='a'/> If supply moved and demand stayed put, the price slid "
            "along the demand curve, and the two changes give its elasticity. The world's crop fell by about "
            f"{abs(100 * (d['world_1976'] - d['world_1975']) / ((d['world_1976'] + d['world_1975']) / 2)):.0f} percent, "
            f"measured from the midpoint, and the average price rose by about "
            f"{100 * (d['p1977'] - d['p1975']) / ((d['p1977'] + d['p1975']) / 2):.0f} percent. That's an elasticity "
            f"of about {say_num(d['arc'])}: in the short run, coffee drinkers hardly respond at all. "
            "<bookmark mark='b'/> Treat that number gently. Warehouses sold coffee picked in earlier years, so "
            "less was drunk than the crop alone suggests. Traders bid for the next harvests too. And the long run "
            "came: the world's crop recovered by 1978, and the price fell back. That's elasticity growing with "
            "time, on the supply side."
        ) as vo:
            self.play(Write(eq))
            self.play(FadeIn(sub))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in caveats.cards], lag_ratio=0.6), run_time=4)
        self.clear_scene()

    def later(self):
        d = load("frost")
        m21, a21r = d["m21"], np.array(d["a21_real"])
        ax = year_axis((1960, 2027), (0, 42), x_length=11.0, y_length=4.2, xticks=list(range(1960, 2030, 10)),
                       yticks=[0, 10, 20, 30, 40], ylabel=r"Arabica, \ dollars a kilo in October 2026 prices",
                       yfmt=lambda v: rf"\${v:.0f}", center=DOWN * 0.4, font_size=18)
        a = ax.ax
        film = load("film")
        months = film["months"]
        real = np.array(film["arabica"])
        # film stores an index of the real price (first year = 1); rebuild dollars from the frost item's base
        base = d["peak_real"] / real[months.index(d["peak_month"])]
        xs = [month_x(m) for m in months]
        pts = [a.c2p(x, y * base) for x, y in zip(xs, real) if np.isfinite(y)]
        line = VMobject(stroke_color=COFFEE, stroke_width=2.5).set_points_as_corners(pts)
        pk = Dot(a.c2p(month_x(d["peak_month"]), d["peak_real"]), radius=0.08, color=E.ACCENT)
        pkl = label(rf"1977: \ {dollars(d['peak_real'], 0)}", font_size=22, color=E.ACCENT).next_to(pk, RIGHT, buff=0.15)
        i25 = months.index(d["max21_month"])
        p25 = Dot(a.c2p(xs[i25], real[i25] * base), radius=0.08, color=WHITE)
        p25l = label(rf"2025: \ {dollars(d['max21_real'], 0)}, \ a record in the dollars of the day", font_size=22,
                     color=WHITE).next_to(p25, UP, buff=0.25).shift(LEFT * 1.2)
        i94 = months.index("1994-07")
        p94 = Dot(a.c2p(xs[i94], real[i94] * base), radius=0.06, color=STORM)
        p94l = label(r"1994: \ two frosts", font_size=20, color=STORM).next_to(p94, UP, buff=0.15)
        src = data_tag(r"World Bank Pink Sheet (Nov 2026), deflated by the US CPI (BLS via FRED); "
                       r"October 2025 filled from its neighbours", corner=DL, font_size=15)
        with self.voiceover(
            "Coffee has been through this again and again. <bookmark mark='a'/> Here is the whole history since "
            "1960, in today's dollars. <bookmark mark='b'/> Frosts in the Brazilian winter of 1994 sent the price "
            f"up by half in a single month, from {money_words(d['june94'])} a kilo in June to "
            f"{money_words(d['july94'])} in July. <bookmark mark='c'/> In February 2025, after poor Brazilian "
            f"harvests, Arabica averaged {money_words(d['max21'])} a kilo, the highest monthly price in the World "
            f"Bank's records, in dollars of the day. <bookmark mark='d'/> But a dollar of 1977 bought far more. In today's money the peak after "
            f"the black frost was about {d['peak_real']:.0f} dollars a kilo, four times the record of 2025. "
            "Whenever you compare prices across decades, divide by the price of everything else first."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(line), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(p94, scale=0.5), FadeIn(p94l))
            vo.wait_until("c")
            self.play(FadeIn(p25, scale=0.5), FadeIn(p25l))
            vo.wait_until("d")
            self.play(FadeIn(pk, scale=0.5), FadeIn(pkl))
            self.play(Indicate(pk, color=E.ACCENT, scale_factor=1.6))
        self.clear_scene()
