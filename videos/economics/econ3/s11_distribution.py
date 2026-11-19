from __future__ import annotations

from videos.economics.econ3.common import *  # noqa: F403

LORENZ = "#F2B84B"
BOTTOM = E.HOUSEHOLDS
TOP = "#F26D6D"


class Distribution(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Who gets the income?", r"What does the average hide?",
             "Chapter nine. Who gets the income?", lit=("households",), scale=("household", "nation", "world"),
             horizon=("a year", "decades"))
        self.island()
        self.lorenz()
        self.countries()
        self.accounts()

    # ------------------------------------------------------------------
    def island(self):
        d = load("distribution")
        inc = np.array(d["incomes"])
        names = d["names"]
        order = np.argsort(inc)
        ax = axes([0, 40], [0, 110], x_length=10.6, y_length=4.4, yticks=[0, 25, 50, 75, 100],
                  yfmt=lambda v: rf"\${v:.0f}", xlabel=r"the Island's 40 households, \ poorest to richest",
                  ylabel=r"income in the year", font_size=20, center=DOWN * 0.4)
        a = ax.ax
        bars = VGroup()
        for k, i in enumerate(order):
            v = inc[i]
            lo, hi = a.c2p(k + 0.5, 0), a.c2p(k + 0.5, v)
            col = TOP if names[i] in ("Friday", "Crusoe") else BOTTOM
            bars.add(Rectangle(width=0.2, height=max(hi[1] - lo[1], 0.01), stroke_width=0, fill_color=col,
                               fill_opacity=0.85).move_to((lo + hi) / 2))
        mean = d["total"] / len(inc)
        ml = DashedLine(a.c2p(0, mean), a.c2p(40, mean), color=E.ACCENT, stroke_width=2)
        mt = label(rf"average: \ \${mean:.2f}", font_size=24, color=E.ACCENT).next_to(a.c2p(1, mean), UP, buff=0.1)
        mt.align_to(a.c2p(1, mean), LEFT)
        fc = VGroup(label(r"Friday \ (the grove)", font_size=21, color=TOP),
                    label(r"Crusoe \ (the boatyard)", font_size=21, color=TOP)).arrange(DOWN, aligned_edge=RIGHT,
                                                                                       buff=0.1)
        fc.next_to(bars[-2], LEFT, buff=0.25).shift(UP * 0.6)
        tag = island_tag(r"simulated: the Island's households, year 3: wages, profits and shares", corner=DR,
                         font_size=16)
        with self.voiceover(
            "GDP per head is an average, and an average says nothing about how the income is shared. Kuznets "
            "warned about that too. <bookmark mark='a'/> Here are the Island's forty households, from poorest to "
            "richest, with what each received in the year: wages, profits and shares in the businesses. "
            f"<bookmark mark='b'/> The average is {money_words(mean)}. <bookmark mark='c'/> But two households "
            "stand far above it: Friday's, which owns the coconut grove, and Crusoe's, which owns the boatyard and "
            "half the fishing company. Between them they receive a quarter of all the income."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.04), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(ml), FadeIn(mt))
            vo.wait_until("c")
            self.play(FadeIn(fc), Indicate(bars[-1], color=TOP), Indicate(bars[-2], color=TOP))
        self.clear_scene()

    def lorenz(self):
        d = load("distribution")
        ax = axes([0, 1], [0, 1], x_length=5.2, y_length=5.2, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                  xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%",
                  xlabel=r"share of households, \ poorest first", ylabel=r"share of income", font_size=20,
                  center=LEFT * 3.0 + DOWN * 0.3)
        a = ax.ax
        diag = DashedLine(a.c2p(0, 0), a.c2p(1, 1), color=GREY_B, stroke_width=2)
        dl = label(r"perfect equality", font_size=20, color=GREY_B).next_to(a.c2p(0.55, 0.6), UL, buff=0.05)
        pts = [a.c2p(x, y) for x, y in zip(d["lorenz_x"], d["lorenz_y"])]
        curve = VMobject(stroke_color=LORENZ, stroke_width=4).set_points_as_corners(pts)
        area = Polygon(*pts, a.c2p(1, 1), stroke_width=0, fill_color=LORENZ, fill_opacity=0.25)
        area = VMobject(stroke_width=0, fill_color=LORENZ, fill_opacity=0.25).set_points_as_corners(
            pts + [a.c2p(0, 0)])
        half = DashedLine(a.c2p(0.5, 0), a.c2p(0.5, d["bottom50"]), color=BOTTOM, stroke_width=2)
        hl = label(rf"the poorer half: \ {pct(d['bottom50'], 0)}", font_size=21, color=BOTTOM)
        hl.next_to(a.c2p(0.5, d["bottom50"]), RIGHT, buff=0.15)
        rows = VGroup(
            label(r"Max Lorenz, 1905: \ the curve", font_size=26, color=LORENZ),
            label(r"Corrado Gini, 1912: \ the coefficient", font_size=26, color=E.ACCENT),
            MathTex(r"G = \frac{\text{area between the diagonal and the curve}}{\text{area under the diagonal}}",
                    font_size=30),
            label(rf"the Island: \ $G = {d['gini']:.2f}$", font_size=32, color=E.ACCENT),
            label(rf"wages alone: \ $G = {d['gini_wages']:.2f}$", font_size=24, color=GREY_A),
            label(r"0: \ everyone the same \qquad 1: \ one household has it all", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.45)
        tag = island_tag(r"simulated: the Island's households, year 3", corner=DR, font_size=16)
        with self.voiceover(
            "In 1905 an American student, Max Lorenz, found a picture for this. <bookmark mark='a'/> Line the "
            "households up from poorest to richest, and plot the share of all income received by the poorest "
            "ten percent, the poorest twenty, and so on. <bookmark mark='b'/> If everyone had the same income, "
            "the curve would be the diagonal. <bookmark mark='c'/> On the Island the poorer half of households "
            f"receive {say_pct(d['bottom50'], 0)} of the income, so the curve sags below it. <bookmark mark='d'/> "
            "In 1912 the Italian statistician Corrado Gini turned the sag into a number: the area between the "
            "diagonal and the curve, as a share of the whole triangle. <bookmark mark='e'/> Zero means everyone "
            f"has the same; one means a single household has everything. The Island's Gini is {d['gini']:.2f}; "
            f"for wages alone, without the profits, it would be {d['gini_wages']:.2f}."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(rows[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(curve, rate_func=linear), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(diag), FadeIn(dl))
            vo.wait_until("c")
            self.play(Create(half), FadeIn(hl))
            vo.wait_until("d")
            self.play(FadeIn(area), FadeIn(rows[1]), Write(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[5]), FadeIn(rows[3]))
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def countries(self):
        d = load("distribution")["wdi"]
        g = np.array(d["gini"])
        x0, x1 = -6.0, 6.0

        def X(v):
            return x0 + (x1 - x0) * (v - 20) / 45

        axis = Line([x0, -0.4, 0], [x1, -0.4, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(v), -0.48, 0], [X(v), -0.32, 0], color=GREY_C),
                                MathTex(f"{v}", font_size=22, color=GREY_B).move_to([X(v), -0.8, 0]))
                         for v in (20, 30, 40, 50, 60)])
        name = label(r"Gini index, \ latest survey 2015--2024 \ (0 to 100)", font_size=22, color=GREY_A)
        name.move_to([0, -1.3, 0])
        rng = np.random.default_rng(7)
        dots = VGroup(*[Dot([X(v), -0.4 + 0.15 + rng.uniform(0, 1.6), 0], radius=0.05, color=GREY_A,
                            fill_opacity=0.7) for v in g])
        picks = VGroup()
        for i, (code, nm, side) in enumerate((("SVK", r"Slovakia", UP), ("SWE", r"Sweden", DOWN),
                                              ("DEU", r"Germany", UP), ("CHN", r"China", DOWN),
                                              ("USA", r"United States", UP), ("BRA", r"Brazil", DOWN),
                                              ("ZAF", r"South Africa", UP))):
            k = d["codes"].index(code)
            v = d["gini"][k]
            y = 2.2 if side is UP else -2.1
            stem = Line([X(v), -0.32, 0], [X(v), y - 0.2 * (1 if side is UP else -1), 0], color=E.ACCENT,
                        stroke_width=1.5, stroke_opacity=0.7)
            t = label(rf"{nm} \ {v:.1f}", font_size=21, color=E.ACCENT).move_to([X(v), y, 0])
            picks.add(VGroup(stem, t))
        note_ = label(r"some countries survey incomes, \ others what households consume: \ compare with care",
                      font_size=21, color=GREY_B).to_edge(DOWN, buff=0.75)
        head = label(rf"{len(g)} countries", font_size=28).to_edge(UP, buff=0.4)
        tag = data_tag(r"World Bank, WDI (Nov 2026), SI.POV.GINI", corner=DR, font_size=15)
        with self.voiceover(
            f"Here is the Gini index for {len(g)} countries, each from its latest household survey, on a scale "
            "of nought to a hundred. <bookmark mark='a'/> The most equal, like Slovakia and Sweden, are in the "
            "twenties. <bookmark mark='b'/> Germany is in the thirties, China a little higher, <bookmark mark='c'/> "
            f"the United States at {d['gini'][d['codes'].index('USA')]:.0f}, and the most unequal, Brazil, South "
            "Africa and their neighbours, in the fifties. <bookmark mark='d'/> A warning before comparing them: "
            "some countries survey income and others survey what households consume, which is more equal than "
            "income, because people borrow and save."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(ticks), FadeIn(name), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(dd, scale=0.5) for dd in dots], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(picks[0]), FadeIn(picks[1]))
            vo.wait_until("b")
            self.play(FadeIn(picks[2]), FadeIn(picks[3]))
            vo.wait_until("c")
            self.play(FadeIn(picks[4]), FadeIn(picks[5]), FadeIn(picks[6]))
            vo.wait_until("d")
            self.play(FadeIn(note_))
        self.clear_scene()

    def accounts(self):
        p = load("distribution")["psz"]
        ax = axes([0, 1], [0, 25], x_length=4.6, y_length=4.6, yticks=[0, 25],
                  yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"share of pre-tax national income", font_size=20,
                  center=LEFT * 3.6 + DOWN * 0.3)
        a = ax.ax
        y0, y1 = p["years"]
        yl = VGroup(label(str(y0), font_size=22, color=GREY_B).next_to(a.c2p(0.08, 0), DOWN, buff=0.15),
                    label(str(y1), font_size=22, color=GREY_B).next_to(a.c2p(0.92, 0), DOWN, buff=0.15))
        b = Line(a.c2p(0.08, p["bottom50_share"][0]), a.c2p(0.92, p["bottom50_share"][1]), color=BOTTOM,
                 stroke_width=5)
        t = Line(a.c2p(0.08, p["top1_share"][0]), a.c2p(0.92, p["top1_share"][1]), color=TOP, stroke_width=5)
        bl = label(r"the bottom half of adults", font_size=21, color=BOTTOM).next_to(b.get_start(), UR, buff=0.12)
        tl = label(r"the top 1\%", font_size=21, color=TOP).next_to(t.get_start(), DR, buff=0.12)
        dots = VGroup(*[Dot(pt, radius=0.08, color=c) for pt, c in ((b.get_start(), BOTTOM), (b.get_end(), BOTTOM),
                                                                  (t.get_start(), TOP), (t.get_end(), TOP))])
        vals = VGroup(label(f"{p['bottom50_share'][0]:.0f}\\%", font_size=22, color=BOTTOM).next_to(dots[0], LEFT),
                      label(f"{p['bottom50_share'][1]:.0f}\\%", font_size=22, color=BOTTOM).next_to(dots[1], RIGHT),
                      label(f"{p['top1_share'][0]:.0f}\\%", font_size=22, color=TOP).next_to(dots[2], LEFT),
                      label(f"{p['top1_share'][1]:.0f}\\%", font_size=22, color=TOP).next_to(dots[3], RIGHT))
        psz = study_card(r"Distributional national accounts", r"Piketty, Saez and Zucman (2018)",
                         [(r"what", r"all of national income, split among adults using tax records and surveys"),
                          (r"result", rf"the bottom half's average stagnated at about \${p['bottom50_income']:,} "
                                      rf"(2014 dollars) while the average rose {p['average_growth']}\%".replace(",",
                                                                                                          "{,}")),
                          (r"ratio", rf"a top-1\% adult earned {p['ratio'][0]} times a bottom-half adult in "
                                     rf"{y0}, {p['ratio'][1]} times in {y1}")],
                         design="survey", width=7.6, font_size=21).to_edge(RIGHT, buff=0.35).shift(UP * 1.2)
        aus = study_card(r"The same accounts, other assumptions", r"Auten and Splinter (2024)",
                         [(r"result", rf"the top 1\%'s pre-tax share rose {p['as_top1_pretax_rise']} points, "
                                      rf"{p['as_years'][0]}--{p['as_years'][1]}; after tax and transfers, "
                                      rf"{p['as_top1_aftertax_rise']}"),
                          (r"why", r"different guesses about whose income never reaches a tax return")],
                         design="survey", width=7.6, font_size=21, color=E.MISS)
        aus.next_to(psz, DOWN, buff=0.25)
        tag = published_tag(r"Piketty, Saez and Zucman, QJE (2018), introduction; Auten and Splinter, JPE (2024)",
                            corner=DL, font_size=15)
        with self.voiceover(
            "Surveys miss the very rich, who rarely answer them. So in the 2010s Thomas Piketty, Emmanuel Saez and "
            "Gabriel Zucman tried something new: take all of national income, the same total as the accounts, "
            "and split it among adults, using tax records for the top. <bookmark mark='a'/> In their estimates for "
            f"the United States, the bottom half of adults received about {p['bottom50_share'][0]:.0f} percent of "
            f"pre-tax income in {y0} and {p['bottom50_share'][1]:.0f} percent in {y1}. <bookmark mark='b'/> The "
            f"top one percent went the other way, from about {p['top1_share'][0]:.0f} percent to "
            f"{p['top1_share'][1]:.0f}. The two groups had swapped their shares. <bookmark mark='c'/> Their numbers "
            "were challenged. Gerald Auten and David Splinter, economists at the Treasury and at Congress's Joint "
            "Committee on Taxation, built the same kind of accounts with different assumptions about income that "
            f"never shows up on tax returns, and found the top one percent's pre-tax share rising "
            f"{p['as_top1_pretax_rise']} points, about half as much, and only {p['as_top1_aftertax_rise']} after "
            "taxes and transfers. <bookmark mark='d'/> Both teams used the same national accounts. They disagree "
            "about the parts no record shows. Part 40 takes up the argument."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(yl), FadeIn(tag), FadeIn(psz))
            vo.wait_until("a")
            self.play(FadeIn(dots[0]), FadeIn(vals[0]), FadeIn(bl))
            self.play(Create(b), FadeIn(dots[1]), FadeIn(vals[1]))
            vo.wait_until("b")
            self.play(FadeIn(dots[2]), FadeIn(vals[2]), FadeIn(tl))
            self.play(Create(t), FadeIn(dots[3]), FadeIn(vals[3]))
            vo.wait_until("c")
            self.play(FadeIn(aus, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(Indicate(aus.card, color=E.MISS, scale_factor=1.02))
        self.clear_scene()
