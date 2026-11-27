from __future__ import annotations

from videos.industry.industry12.common import *  # noqa: F403


class Fertilizer(VoiceoverScene):
    def construct(self):
        card(self, 6, "Fertilizer: gas into food", "Why does the price of bread depend on the price of gas?",
             "Chapter six. Fertilizer: gas into food.", lit=("unit", "make", "dollar"))
        self.nutrients()
        self.haber()
        self.costs()
        self.producers()
        self.profits()

    def nutrients(self):
        fld = draw.field(6.0, rows=3, n=12, kind="corn", h=0.7).move_to([0, -2.7, 0])
        sacks = VGroup(*[draw.sack(0.9, c, label_=l_) for l_, c in (("N", NITRO), ("P", "#E0B07A"), ("K", "#E88A8A"))])
        for s_, x in zip(sacks, (-4.0, 0.0, 4.0)):
            s_.move_to([x, -0.6, 0])
        srcs = VGroup(
            VGroup(VGroup(draw.molecule("N2", bond=0.5), tx("+", 24, WHITE), draw.molecule("CH4", bond=0.4)).arrange(RIGHT, buff=0.2),
                   tx("nitrogen: from the air,", 15, NITRO, bold=True), tx("with natural gas, as ammonia", 14, GREY_A)),
            VGroup(draw.quarry(1.8, 0.55, "#C8A57A"), tx("phosphorus: phosphate", 15, "#E0B07A", bold=True),
                   tx("rock, mined", 14, GREY_A)),
            VGroup(draw.open_pit(1.8, 0.55, 3, "#C97B7B"), tx("potassium: potash,", 15, "#E88A8A", bold=True),
                   tx("mined from old sea beds", 14, GREY_A)))
        for s_, x in zip(srcs, (-4.0, 0.0, 4.0)):
            s_.arrange(DOWN, buff=0.08).move_to([x, 2.3, 0])
        arr1 = VGroup(*[Arrow(s_.get_bottom(), k_.get_top(), buff=0.12, stroke_width=2.5, color=GREY_B,
                              max_tip_length_to_length_ratio=0.25) for s_, k_ in zip(srcs, sacks)])
        arr2 = VGroup(*[Arrow(k_.get_bottom(), fld.get_top() + RIGHT * 0.4 * (i - 1), buff=0.1, stroke_width=2.5, color=GREY_B,
                              max_tip_length_to_length_ratio=0.25) for i, k_ in enumerate(sacks)])
        who = VGroup(tx("CF Industries", 14, WHITE), tx("Mosaic", 14, WHITE), tx("Mosaic, ICL", 14, WHITE))
        for w_, k_ in zip(who, sacks):
            w_.next_to(k_, RIGHT, buff=0.2)
        with self.voiceover(
            "Plants need three things from fertilizer above all. <bookmark mark='a'/> Nitrogen, which the air is full "
            "of, but in a form no crop can use until it is made into ammonia, and that takes natural gas. "
            "<bookmark mark='b'/> Phosphorus, which comes from phosphate rock, dug out of mines. <bookmark mark='c'/> "
            "And potassium, from potash, mined from the beds of ancient seas. <bookmark mark='d'/> So fertilizer is "
            "really two industries: a chemical one, which turns gas into nitrogen, and a mining one, which digs up "
            "the other two. American companies cover both: CF Industries makes nitrogen; Mosaic mines phosphate and "
            "potash; Israel's ICL mines potash too. <bookmark mark='e'/> Nitrogen is the one used in the largest "
            "amounts, and the one with the most interesting economics, because its main raw material is gas."
        ) as vo:
            self.play(FadeIn(fld))
            for m_, s_, k_, a_ in zip("abc", srcs, sacks, arr1):
                vo.wait_until(m_)
                self.play(FadeIn(s_, shift=DOWN * 0.2), GrowArrow(a_), FadeIn(k_, shift=DOWN * 0.1), run_time=1.2)
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in arr2], lag_ratio=0.2), *[p_.animate.scale(1.12, about_edge=DOWN)
                                                                                    for p_ in fld[1]], run_time=1.5)
            self.play(LaggedStart(*[FadeIn(w_, shift=LEFT * 0.1) for w_ in who], lag_ratio=0.3), run_time=1.2)
            vo.wait_until("e")
            self.play(Indicate(sacks[0], color=NITRO, scale_factor=1.15), Indicate(srcs[0], color=NITRO))
        self.clear_scene()

    def haber(self):
        F_ = R["fertilizer"]
        n2 = draw.molecule("N2", bond=0.45).move_to([-4.6, 1.4, 0])
        h2s = VGroup(*[draw.molecule("H2", bond=0.4) for _ in range(3)]).arrange(DOWN, buff=0.35).move_to([-2.4, 1.4, 0])
        nh3 = VGroup(*[draw.molecule("NH3", bond=0.45) for _ in range(2)]).arrange(RIGHT, buff=0.6).move_to([2.6, 1.4, 0])
        plus = tx("+", 30, WHITE).move_to([-3.5, 1.4, 0])
        arr = Arrow([-1.4, 1.4, 0], [0.9, 1.4, 0], buff=0, stroke_width=4, color=GOLD)
        cond = VGroup(tx("an iron catalyst,", 14, GREY_A), tx("hundreds of degrees,", 14, GREY_A),
                      tx("hundreds of atmospheres", 14, GREY_A)).arrange(DOWN, buff=0.04).next_to(arr, DOWN, buff=0.15)
        eq = tx("N2  +  3 H2  →  2 NH3", 26, WHITE, bold=True).move_to([0, 3.1, 0])
        hsrc = tx("the hydrogen: in plants like CF's, stripped from methane, CH4, with steam", 15, GAS).move_to([-3.2, -0.2, 0])
        per = F_["per_ton"]
        gas = R["fertilizer"]["cf_gascost"]
        rows = VGroup(tx(f"CF Industries, 2025: {get('cf.gas.2025'):,.0f} million MMBtu of gas", 18, WHITE),
                      tx(f"for {get('cf.ammonia.2025') / 1000:.1f} million short tons of ammonia", 18, WHITE),
                      tx(f"= about {per:.1f} MMBtu of gas in every ton", 24, GAS, bold=True),
                      tx(f"at CF's ${gas:.2f} gas: about ${per * gas:,.0f} a ton", 20, TEXAS, bold=True),
                      tx(f"at Europe's $12 gas: about ${per * 12:,.0f} a ton", 20, EUROPE, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([0.6, -2.0, 0])
        src = source("CF Industries, Form 10-K 2025 (gas consumed, gross ammonia production, cost of gas)", size=13)
        with self.voiceover(
            "Here is the chemistry Fritz Haber found and Carl Bosch scaled up. <bookmark mark='a'/> One molecule of "
            "nitrogen, from the air, and three of hydrogen, <bookmark mark='b'/> pressed together over an iron catalyst "
            "at hundreds of degrees and hundreds of atmospheres, make two molecules of ammonia. <bookmark mark='c'/> "
            "The hard part is the hydrogen. In plants like CF Industries', it is stripped from methane, natural gas, "
            "with steam, and more gas is burned to heat and squeeze the whole process. <bookmark mark='d'/> How much? "
            f"CF's filing gives the numbers: it used {get('cf.gas.2025'):,.0f} million million-Btu of gas in 2025 "
            f"and made {get('cf.ammonia.2025') / 1000:.1f} million tons of ammonia: about {per:.0f} million Btu in "
            f"every ton. <bookmark mark='e'/> At the {gas:.2f} dollars CF paid for its gas, that is about "
            f"{per * gas:,.0f} dollars a ton. At twelve dollars, about what Europe paid in 2025, it is about "
            f"{per * 12:,.0f}. Ammonia is, in effect, natural gas in a different form."
        ) as vo:
            self.play(FadeIn(eq), FadeIn(src), FadeIn(n2, scale=0.6), FadeIn(plus),
                      LaggedStart(*[FadeIn(h_, scale=0.6) for h_ in h2s], lag_ratio=0.2), run_time=1.2)
            vo.wait_until("a")
            self.play(Indicate(n2, color=NITRO, scale_factor=1.2), *[Indicate(h_, scale_factor=1.2) for h_ in h2s], run_time=1.0)
            vo.wait_until("b")
            self.play(GrowArrow(arr), FadeIn(cond))
            self.play(TransformFromCopy(VGroup(n2, h2s), nh3), VGroup(n2, h2s, plus).animate.set_opacity(0.4), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(hsrc, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeOut(hsrc), FadeIn(rows[:3], shift=UP * 0.1), run_time=1.2)
            vo.wait_until("e")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
            self.play(FadeIn(rows[4], shift=UP * 0.1))
        self.clear_scene()

    def costs(self):
        F_ = R["fertilizer"]
        us, eu = F_["cost"]["US"], F_["cost"]["EU"]
        ys = sorted(us)
        pa = viz.plot_axes([ys[0] - 0.5, ys[-1] + 0.5], [0, 1400], x_length=9.0, y_length=4.5,
                           xticks=[2000, 2005, 2010, 2015, 2020, 2025], yticks=[300, 600, 900, 1200], xfmt=lambda v: f"{int(v)}",
                           yfmt=lambda v: f"${v:,.0f}", ylabel="dollars a short ton of ammonia", size=14).move_to([-1.6, -0.4, 0])
        lu = VMobject(stroke_color=TEXAS, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(y, us[y]) for y in ys])
        le = VMobject(stroke_color=EUROPE, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(y, eu[y]) for y in ys])
        pr = F_["price"]
        dots = VGroup(*[Dot(pa.ax.c2p(y, v), radius=0.08, color=WHITE) for y, v in sorted(pr.items())])
        pline = VMobject(stroke_color=WHITE, stroke_width=2).set_points_as_corners([pa.ax.c2p(y, v) for y, v in sorted(pr.items())])
        key = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=c, stroke_width=4), tx(t_, 15, c)).arrange(RIGHT, buff=0.1)
                       for c, t_ in ((EUROPE, "gas for a ton, at European prices"), (TEXAS, "gas for a ton, at American prices"),
                                     (WHITE, "what ammonia sold for, US Gulf"))]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(
            [4.4, 2.5, 0])
        y = 2022
        note = VGroup(tx(f"{y}", 18, WHITE, bold=True), tx(f"European gas: ${eu[y]:,.0f} a ton", 16, EUROPE),
                      tx(f"ammonia sold for: ${pr[y]:,.0f}", 16, WHITE), tx(f"American gas: ${us[y]:,.0f}", 16, TEXAS)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([5.0, 0.0, 0])
        uk = VGroup(tx("CF closed its Ince plant in England in 2022,", 15, GREY_A),
                    tx("and stopped making ammonia at Billingham in 2023,", 15, GREY_A),
                    tx("'due to the substantial increase in the", 15, WHITE),
                    tx("cost of natural gas in the United Kingdom'", 15, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to(
            [4.6, -2.0, 0])
        tag = estimate_tag(f"gas cost: {F_['per_ton']:.1f} MMBtu a ton (CF, 2025) x the IMF's gas prices; price: USGS", corner=DR, size=12)
        src = source("IMF via FRED; USGS Mineral Commodity Summaries 2026, nitrogen; CF Industries, 10-K 2023", size=13)
        with self.voiceover(
            "So the cost of ammonia rises and falls with gas. <bookmark mark='a'/> This is the gas in a ton of "
            "ammonia, at American prices and at European prices, year by year. Before shale they were close. After it, "
            f"Europe's was often two to five times America's. <bookmark mark='b'/> In {y}, the gas alone for a ton "
            f"cost a European plant about {eu[y]:,.0f} dollars. <bookmark mark='c'/> Ammonia itself sold on America's "
            f"Gulf Coast for about {pr[y]:,.0f}, by the Geological Survey's figures. <bookmark mark='d'/> So European "
            "plants that bought gas at market prices lost money on every ton, and some stopped. CF closed one British "
            "plant in 2022 and stopped making ammonia at the other in 2023, because of the cost of gas, its filing says. "
            f"<bookmark mark='e'/> An American plant paid about {us[y]:,.0f} dollars for the gas in the same ton."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(key), FadeIn(tag), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(lu), Create(le), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(note[:2]), Flash(pa.ax.c2p(y, eu[y]), color=EUROPE))
            vo.wait_until("c")
            self.play(Create(pline), LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.15), FadeIn(note[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(uk, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(note[3]), Indicate(lu, color=TEXAS))
        self.clear_scene()

    def producers(self):
        F_ = R["fertilizer"]
        p = F_["producers"]
        world = F_["world"]
        rows = [("China", p["china"]), ("India", p["india"]), ("Russia", p["russia"]), ("United States", p["us"]),
                ("everyone else", world - sum(p.values()))]
        sc = 5.0 / 70000
        nbar = VGroup()
        for i, (n_, v) in enumerate(rows):
            yy = 1.9 - 0.62 * i
            b = Rectangle(width=max(v * sc, 0.02), height=0.42, stroke_width=0, fill_color=NITRO if i < 4 else GREY_D,
                          fill_opacity=0.9).move_to([-4.6, yy, 0], aligned_edge=LEFT)
            nbar.add(VGroup(tx(n_, 15, WHITE).next_to(b, LEFT, buff=0.15).set_x(-4.75, direction=RIGHT),
                            b, tx(f"{v / 1000:.0f} Mt", 15, NITRO if i < 4 else GREY_B, bold=True).next_to(b, RIGHT, buff=0.1)))
        nh = tx(f"Ammonia, 2025: {world / 1000:.0f} million tonnes of nitrogen", 18, NITRO, bold=True).move_to([-2.4, 2.75, 0])
        pk = F_["potash"]
        prow = [("Canada", pk["canada"]), ("Russia", pk["russia"]), ("China", pk["china"]), ("Belarus", pk["belarus"])]
        pbar = VGroup()
        for i, (n_, v) in enumerate(prow):
            yy = 1.9 - 0.62 * i
            b = Rectangle(width=v * 2.0 / 15000, height=0.42, stroke_width=0, fill_color="#E88A8A", fill_opacity=0.9).move_to(
                [4.0, yy, 0], aligned_edge=LEFT)
            pbar.add(VGroup(tx(n_, 15, WHITE).next_to(b, LEFT, buff=0.15), b,
                            tx(f"{v / 1000:.1f} Mt", 15, "#E88A8A", bold=True).next_to(b, RIGHT, buff=0.1)))
        ph = tx(f"Potash, 2025: {F_['potash_world'] / 1000:.0f} Mt of K2O; the four largest", 18, "#E88A8A", bold=True).move_to([4.4, 2.75, 0])
        pu = VGroup(tx(f"America mines {F_['potash_us'] / 1000:.1f} Mt", 14, GREY_A),
                    tx(f"and imports {F_['potash_imports'] / 1000:.1f} Mt,", 14, GREY_A),
                    tx(f"{F_['potash_canada']:.0f}% of it from Canada (2021-24)", 14, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                    buff=0.04).move_to([4.6, -0.6, 0])
        facts = VGroup(tx(f"America: {F_['us_plants']:.0f} ammonia plants", 17, WHITE, bold=True),
                       tx(f"{F_['gulf']:.0f}% of the capacity in Louisiana, Oklahoma and Texas, near the gas", 15, GREY_A),
                       tx(f"{F_['fert']:.0f}% of the ammonia goes into fertilizer", 15, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([-1.6, -2.2, 0])
        src = source("USGS, Mineral Commodity Summaries 2026: nitrogen (fixed), ammonia; potash (K2O equivalent)", size=13)
        with self.voiceover(
            "Who makes it? <bookmark mark='a'/> The world made about "
            f"{world / 1000:.0f} million tonnes of nitrogen as ammonia in 2025, the Geological Survey estimates. "
            f"China, about {p['china'] / 1000:.0f} million. India and Russia, about {p['india'] / 1000:.0f} each. "
            f"America, about {p['us'] / 1000:.0f}. <bookmark mark='b'/> America has {F_['us_plants']:.0f} ammonia "
            f"plants, with {F_['gulf']:.0f} per cent of the capacity in Louisiana, Oklahoma and Texas, next to the gas, "
            f"and {F_['fert']:.0f} per cent of what they make goes into fertilizer. <bookmark mark='c'/> Potash is a "
            "different map, because you can only mine it where the old seas left it. Canada is far ahead, with about "
            f"{pk['canada'] / 1000:.0f} million tonnes, then Russia, China and Belarus. America mines only about "
            f"{F_['potash_us'] / 1000:.1f} million tonnes, and imports about {F_['potash_imports'] / 1000:.1f} million, "
            f"{F_['potash_canada']:.0f} per cent of it from Canada."
        ) as vo:
            self.play(FadeIn(src), FadeIn(nh))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2])) for r_ in nbar],
                                  lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(facts, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(ph), LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2]))
                                                for r_ in pbar], lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(pu))
        self.clear_scene()

    def profits(self):
        from explainer.industry.data.fetch import read
        d = {r["ticker"]: {} for r in read("sec_annual") if r["ticker"] in ("CF", "MOS")}
        for r in read("sec_annual"):
            if r["ticker"] in d and str(r["year_end"]).endswith("12-31") and r["net_income"] is not None:
                d[r["ticker"]][int(str(r["year_end"])[:4])] = r["net_income"]
        ys = list(range(2015, 2026))
        pa = viz.plot_axes([2014.4, 2025.6], [-1.5, 4.0], x_length=9.0, y_length=4.2, xticks=[2015, 2018, 2021, 2024],
                           yticks=[-1, 0, 1, 2, 3, 4], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}bn",
                           ylabel="net income", size=14).move_to([-1.4, -0.4, 0])
        zero = Line(pa.ax.c2p(2014.4, 0), pa.ax.c2p(2025.6, 0), stroke_color=GREY_B, stroke_width=1.2)
        bars = {}
        for t, col, dx in (("CF", NITRO, -0.18), ("MOS", "#E88A8A", 0.18)):
            g = VGroup()
            for y in ys:
                v = d[t].get(y)
                if v is None:
                    continue
                p0, p1 = pa.ax.c2p(y + dx, 0), pa.ax.c2p(y + dx, v)
                g.add(Rectangle(width=0.3, height=max(abs(p1[1] - p0[1]), 0.01), stroke_width=0, fill_color=col,
                                fill_opacity=0.9).move_to([p0[0], (p0[1] + p1[1]) / 2, 0]))
            bars[t] = g
        key = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.9), tx(t_, 15, c)).arrange(RIGHT, buff=0.1)
                       for c, t_ in ((NITRO, "CF Industries (nitrogen)"), ("#E88A8A", "Mosaic (phosphate and potash)"))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.6, 2.3, 0])
        cf = next(c for c in R["landscape"]["companies"] if c["ticker"] == "CF")
        note = VGroup(tx(f"CF, 2022: ${d['CF'][2022]:.1f}bn", 18, NITRO, bold=True),
                      tx("in the year Europe's plants", 15, GREY_A), tx("could not cover their gas", 15, GREY_A),
                      tx(f"CF's net margin, {cf['year'] - 4}-{cf['year']}:", 15, GREY_A),
                      tx(f"{100 * cf['margin5']:.0f}% of sales", 22, GOOD, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to(
            [4.7, -0.6, 0])
        src = source("Form 10-K filings via SEC XBRL (net income attributable to the company)", size=13)
        with self.voiceover(
            "And the money. <bookmark mark='a'/> These are the profits of CF Industries, which makes nitrogen, and of "
            "Mosaic, which mines phosphate and potash, since 2015. <bookmark mark='b'/> In 2022, with European "
            f"producers priced out by their gas, CF earned about {d['CF'][2022]:.1f} billion dollars, on cheap American "
            "gas and a world price set by the expensive plants. It is the cracker story again, with a different "
            f"molecule. <bookmark mark='c'/> Over the last five years, CF kept about {100 * cf['margin5']:.0f} cents of "
            "every dollar of sales as profit, more than any other company in this part. Fertilizer is cyclical, but "
            "the cheapest producer in a world priced by the dearest does very well."
        ) as vo:
            self.play(FadeIn(pa), Create(zero), FadeIn(key), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars["CF"]], lag_ratio=0.1),
                      LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars["MOS"]], lag_ratio=0.1), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(note[:3]), Indicate(bars["CF"][ys.index(2022)], color=NITRO))
            vo.wait_until("c")
            self.play(FadeIn(note[3:], shift=UP * 0.1))
        self.clear_scene()
