from __future__ import annotations

from videos.economics.econ3.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.report()
        self.totals()
        self.types()
        self.warning()
        self.question()
        self.title()
        self.pipes()
        self.objectives()

    # ------------------------------------------------------------------
    def report(self):
        when = history_card(r"1932", r"Robert La Follette, senator for Wisconsin",
                            r"Senate Resolution 220 asks the Department of Commerce for the national income of "
                            r"1929, 1930 and 1931", color=KUZ, width=6.4, font_size=25)
        who = history_card(r"1933", r"Simon Kuznets, of the National Bureau of Economic Research",
                           r"leads a small team at the Bureau of Foreign and Domestic Commerce", color=E.ACCENT,
                           width=6.4, font_size=25)
        VGroup(when, who).arrange(DOWN, buff=0.4, aligned_edge=LEFT).to_edge(LEFT, buff=0.6).shift(UP * 0.2)
        cover = report_cover(3.3).to_edge(RIGHT, buff=1.2).shift(UP * 0.1)
        # what there was: the Federal Reserve's index of industrial production, month by month
        ip = data.fred("INDPRO")
        pts = [(int(d[:4]) + (int(d[5:7]) - 0.5) / 12, v) for d, v in zip(ip["date"], ip["value"])
               if "1927-01" <= d <= "1933-12-31"]
        base = next(v for d, v in zip(ip["date"], ip["value"]) if d.startswith("1929-07"))
        ipax = axes([1927, 1934], [0, 120], x_length=8.6, y_length=4.2, xticks=list(range(1927, 1935)),
                    yticks=[0, 50, 100], xfmt=lambda v: f"{v:.0f}", ylabel=r"industrial production, \ July 1929 $= 100$",
                    font_size=20, center=DOWN * 0.3)
        line = VMobject(stroke_color=E.FIRMS, stroke_width=4).set_points_as_corners(
            [ipax.ax.c2p(x, 100 * v / base) for x, v in pts])
        low = min(pts, key=lambda t: t[1])
        lowlab = label(rf"July 1932: \ {100 * low[1] / base:.0f}", font_size=24, color=E.FIRMS)
        lowlab.next_to(ipax.ax.c2p(low[0], 100 * low[1] / base), DOWN, buff=0.2)
        iptag = data_tag(rf"Federal Reserve Board, industrial production (INDPRO), {data.fred_cite('INDPRO')}",
                         corner=DL, font_size=16)
        what = label(r"what Washington had: \ indexes of output, prices, freight loadings", font_size=24,
                     color=GREY_A).to_edge(UP, buff=0.5)
        src = published_tag(r"BEA, Survey of Current Business, September 2020 (the report reprinted)", corner=DR,
                            font_size=16)
        with self.voiceover(
            "In 1932 the United States was three years into the Great Depression, and nobody could say how much "
            "the country's income had fallen. There were indexes: industrial production had halved since 1929. "
            "There were prices of shares, freight loadings, scattered surveys. But there was no total. <bookmark mark='a'/> In 1932 a senator from Wisconsin, Robert La Follette, pushed "
            "through a resolution asking the Department of Commerce for the national income of the last three "
            "years. <bookmark mark='b'/> The work went to a young economist at the National Bureau of Economic "
            "Research, Simon Kuznets, who had been born in Pinsk, in what is now Belarus, and had come to America "
            "in 1922. <bookmark mark='c'/> On the fourth of January 1934, the report went to the Senate. It ran to "
            "nearly two hundred and seventy pages, and it was the first official estimate of the national income "
            "of the United States."
        ) as vo:
            self.play(FadeIn(ipax), FadeIn(what), FadeIn(iptag), Create(line, rate_func=linear), run_time=4.0)
            self.play(FadeIn(lowlab))
            vo.wait_until("a")
            self.play(*[FadeOut(m) for m in (ipax, what, iptag, line, lowlab)], run_time=0.6)
            self.play(FadeIn(when, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(who, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cover, shift=LEFT * 0.3), FadeIn(src))
        self.clear_scene()

    def totals(self):
        k = load("kuznets")
        years = k["years"]
        ax = axes([1928.4, 1932.6], [0, 90], x_length=6.4, y_length=4.4, xticks=years, yticks=[0, 20, 40, 60, 80],
                  xfmt=lambda v: f"{v:.0f}", ylabel=r"billions of dollars", font_size=20,
                  center=LEFT * 2.6 + DOWN * 0.3)
        a = ax.ax
        bars = VGroup()
        for i, y in enumerate(years):
            for j, (key, col) in enumerate((("produced", E.FIRMS), ("paid_out", E.HOUSEHOLDS))):
                v = k[key][i] / 1000
                x = y - 0.17 + 0.34 * j
                lo, hi = a.c2p(x, 0), a.c2p(x, v)
                bars.add(Rectangle(width=0.5, height=max(hi[1] - lo[1], 0.01), stroke_width=0, fill_color=col,
                                   fill_opacity=0.9).move_to((lo + hi) / 2))
        key = VGroup(
            VGroup(Square(0.22, stroke_width=0, fill_color=E.FIRMS, fill_opacity=0.9),
                   label(r"income produced", font_size=22, color=E.FIRMS)).arrange(RIGHT, buff=0.12),
            VGroup(Square(0.22, stroke_width=0, fill_color=E.HOUSEHOLDS, fill_opacity=0.9),
                   label(r"income paid out to people", font_size=22, color=E.HOUSEHOLDS)).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(ax, UP, buff=0.25).align_to(ax, LEFT).shift(RIGHT * 1.2)
        rows = VGroup(
            label(rf"produced: \ {bn(k['produced'][0])} $\to$ {bn(k['produced'][-1])}", font_size=26, color=E.FIRMS),
            label(rf"down {pct(k['fall_produced'], 0)}", font_size=26, color=E.FIRMS),
            label(rf"paid out: \ {bn(k['paid_out'][0])} $\to$ {bn(k['paid_out'][-1])}", font_size=26,
                  color=E.HOUSEHOLDS),
            label(rf"down {pct(k['fall_paid'], 0)}", font_size=26, color=E.HOUSEHOLDS),
            label(rf"the difference: \ businesses paid out \\ {bn(-k['business_savings'][-1])} more than they made "
                  r"in 1932", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.5).shift(UP * 0.3)
        tag = published_tag(r"National Income, 1929--32 (Senate Document 124, 1934), table 1", corner=DL, font_size=16)
        with self.voiceover(
            "Its first table answered the senator's question. <bookmark mark='a'/> In 1929 the American economy "
            f"produced an income of {k['produced'][0] / 1000:.0f} billion dollars. By 1932 it produced "
            f"{k['produced'][-1] / 1000:.0f} billion: <bookmark mark='b'/> a fall of more than half in three "
            "years. <bookmark mark='c'/> The income actually paid out to people, in wages, salaries, dividends, "
            f"interest and rent, fell less, by {k['fall_paid'] * 100:.0f} percent. <bookmark mark='d'/> The gap was "
            "business as a whole making a loss. In 1932, firms paid out nine and a half billion dollars more than "
            "they earned."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[0::2]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[1::2]], lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def types(self):
        k = load("kuznets")
        names = {"interest": r"interest", "salaries_wages_other": r"pay in all other industries",
                 "salaries_selected": r"salaries (mines, factories, building, railways)",
                 "withdrawals": r"owners' withdrawals", "rents_royalties": r"rents and royalties",
                 "dividends": r"dividends", "wages_selected": r"wages (mines, factories, building, railways)"}
        order = ["interest", "salaries_wages_other", "salaries_selected", "withdrawals", "rents_royalties",
                 "dividends", "wages_selected"]
        color = {"interest": E.BANKS, "dividends": E.BANKS, "rents_royalties": E.BANKS,
                 "salaries_wages_other": E.HOUSEHOLDS, "salaries_selected": E.HOUSEHOLDS,
                 "wages_selected": E.HOUSEHOLDS, "withdrawals": E.FIRMS}
        x0, x1 = -0.6, 5.2
        head = label(r"income paid out in 1932, \ as a share of 1929", font_size=30).to_edge(UP, buff=0.45)
        rows = VGroup()
        bars = VGroup()
        full = VGroup()
        for i, key in enumerate(order):
            y = 2.1 - i * 0.68
            nm = label(names[key], font_size=21, color=color[key])
            nm.move_to([x0 - 0.25, y, 0], aligned_edge=RIGHT)
            ref = Rectangle(width=x1 - x0, height=0.4, stroke_color=GREY_D, stroke_width=1, fill_opacity=0)
            ref.move_to([(x0 + x1) / 2, y, 0])
            v = k["type_rel"][key][-1] / 100
            bar = Rectangle(width=(x1 - x0) * v, height=0.4, stroke_width=0, fill_color=color[key],
                            fill_opacity=0.85).move_to([x0 + (x1 - x0) * v / 2, y, 0])
            val = label(rf"{100 * v:.1f}\%", font_size=22).move_to([x1 + 0.55, y, 0])
            rows.add(VGroup(nm, val))
            bars.add(bar)
            full.add(ref)
        hundred = DashedLine([x1, 2.45, 0], [x1, 2.1 - 6 * 0.68 - 0.35, 0], color=GREY_B, stroke_width=1.5)
        hl = label(r"1929 $= 100\%$", font_size=18, color=GREY_B).next_to(hundred, UP, buff=0.08)
        legend = VGroup(
            label(r"to lenders and owners of property", font_size=20, color=E.BANKS),
            label(r"to people who work for pay", font_size=20, color=E.HOUSEHOLDS),
            label(r"to people who run their own business", font_size=20, color=E.FIRMS),
        ).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.75)
        tag = published_tag(r"National Income, 1929--32, table 2 (millions of current dollars)", corner=DL,
                            font_size=16)
        with self.voiceover(
            "The second table showed who had lost it. <bookmark mark='a'/> Set each kind of income in 1929 at one "
            "hundred percent, and look at 1932. <bookmark mark='b'/> Interest was still being paid almost in full: "
            f"{k['type_rel']['interest'][-1]:.1f} percent of what it had been. People who had lent money, to "
            "companies and to governments, were still collecting. <bookmark mark='c'/> Dividends had fallen to "
            f"{k['type_rel']['dividends'][-1]:.0f} percent. <bookmark mark='d'/> And the wages paid in mining, "
            "manufacturing, construction and the railways, the industries where the report could count wage "
            f"earners separately, had fallen to {k['type_rel']['wages_selected'][-1]:.0f} percent: down by six "
            "tenths, as factories closed and the people still working took cuts. Before 1934, nobody could have "
            "drawn this picture."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(full), *[FadeIn(r[0]) for r in rows], Create(hundred),
                      FadeIn(hl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.15), run_time=2.0)
            self.play(LaggedStart(*[FadeIn(r[1]) for r in rows], lag_ratio=0.1), FadeIn(legend))
            vo.wait_until("b")
            self.play(Indicate(rows[0], color=E.BANKS), bars[0].animate.set_fill(opacity=1.0))
            vo.wait_until("c")
            self.play(Indicate(rows[5], color=E.BANKS))
            vo.wait_until("d")
            self.play(Indicate(rows[6], color=E.HOUSEHOLDS), bars[6].animate.set_fill(opacity=1.0))
        self.clear_scene()

    def warning(self):
        t = tables.KUZNETS_1934.data
        q = quote_card(t["welfare"], r"National Income, 1929--32 (1934), chapter 1, p.\ 7", width=10.4,
                       font_size=32, color=KUZ).to_edge(UP, buff=0.6)
        why = VGroup(
            label(r"it leaves out work that is not sold: \ ``housewives' services''", font_size=25, color=UNPAID),
            label(r"it says nothing of who gets the income", font_size=25, color=E.HOUSEHOLDS),
            label(r"it ignores the ``intensity and unpleasantness of effort''", font_size=25, color=E.MISS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(q, DOWN, buff=0.55)
        with self.voiceover(
            "And on page seven, before any of the numbers, the report warned its readers what they could not do "
            "with them. <bookmark mark='a'/> The welfare of a nation, it said, can scarcely be inferred from a "
            "measurement of national income. <bookmark mark='b'/> The measure left out work that is never sold, "
            "and the report's example was the work of housewives. <bookmark mark='c'/> It said nothing about who "
            "received the income. <bookmark mark='d'/> And it counted the pay for a job, but not how hard or how "
            "unpleasant the job was. The number became the most watched statistic in the world, and the warning "
            "is still worth reading."
        ) as vo:
            self.wait(0.3)
            vo.wait_until("a")
            self.play(FadeIn(q, shift=UP * 0.2))
            for m, r in zip("bcd", why):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def question(self):
        q = label(ASK, font_size=60, color=E.ACCENT).to_edge(UP, buff=0.9)
        subs = VGroup(
            label(r"add up what? \ \ sales, spending, or incomes?", font_size=30, color=E.FIRMS),
            label(r"compare years, \ when prices change?", font_size=30, color=FISHER),
            label(r"compare countries, \ when a dollar buys different things?", font_size=30, color=E.WORLD),
            label(r"and what does the number leave out?", font_size=30, color=UNPAID),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "This part is about one question: how do you put a number on an economy? <bookmark mark='a'/> What "
            "exactly do you add up, when every sale is also somebody's purchase? <bookmark mark='b'/> How do you "
            "compare one year with the next, when prices have changed? <bookmark mark='c'/> How do you compare "
            "two countries, when a dollar buys different things in each? <bookmark mark='d'/> And what does the "
            "number leave out?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for m, r in zip("abcd", subs):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        logo = meter_glyph(0.85, 0.15)
        t = label(SERIES_EN, font_size=72)
        sub = label(r"Part 3 \ \textperiodcentered\ \ The Measure", font_size=40, color=E.ACCENT)
        g = VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        a = PI * 0.95 - PI * 0.9 * 0.72
        target = Line(ORIGIN, np.array([np.cos(a), np.sin(a), 0]) * 0.85 * 0.82, stroke_color=WHITE,
                      stroke_width=3.6).shift(logo.hub.get_center())
        with self.voiceover("Economics, Built. Part three: the measure."):
            self.play(Create(logo.arc), FadeIn(logo.ticks), FadeIn(logo.hub), Create(logo.needle), run_time=1.0)
            self.play(Transform(logo.needle, target), Write(t), run_time=1.4)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(0.8)
        self.clear_scene()

    def pipes(self):
        tab = tableau_map(open_pipes=("spending", "goods"), lit=(), width=12.6, font_size=21).move_to(DOWN * 0.2)
        head = heading(r"The Tableau: \ a meter on every pipe")
        meters = VGroup()
        for key, pp in tab.pipe.items():
            m = meter_glyph(0.2, 0.5 + 0.3 * np.sin(len(key)), color=E.ACCENT, stroke_width=2.4)
            m.move_to(pp.path.point_from_proportion(0.5 if key not in ("spending", "goods") else 0.3))
            bg = Circle(radius=0.24, stroke_width=0, fill_color=BACKGROUND, fill_opacity=0.9).move_to(m)
            meters.add(VGroup(bg, m))
        flows = VGroup(*[flowing(tab.paths[k], c, n=6, period=3.0) for k, c in (("spending", E.HOUSEHOLDS),
                                                                                 ("goods", E.FIRMS))])
        with self.voiceover(
            "Part two opened the first two pipes of the Tableau, spending and goods, and found the price where they "
            "meet. <bookmark mark='a'/> This part opens no new pipes. It puts a meter on every one. The national "
            "accounts are the meter readings of a whole economy: what flows from households to firms, from firms "
            "to the government, to the rest of the world, in a year. <bookmark mark='b'/> Kuznets read the first "
            "meters by hand. We'll build the meters for the Island, read them for the United States, and ask, at "
            "every step, what they cannot see."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            self.add(flows)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in meters], lag_ratio=0.12), run_time=2.2)
            vo.wait_until("b")
            self.play(*[Rotate(m[1].needle, angle=-0.6, about_point=m[1].hub.get_center()) for m in meters],
                      run_time=1.5)
        for f in flows:
            f.clear_updaters()
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 3", font_size=34, color=GREY_B), label(r"The Measure", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"GDP three ways on the Island: \ output, spending and income, \ and why they must agree",
            r"what the number leaves out: \ housework, the informal economy, free goods",
            r"real and nominal: \ whose basket? \ Play it, \ and the consumer price index's bias",
            r"across countries, \ in a survey of jobs, \ and across people",
            r"Leontief's table, \ the revisions nobody saw, \ and measures beyond GDP",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Part three: the measure. <bookmark mark='a'/> We'll keep the Island's accounts three ways, by what it "
            "produces, by what it spends and by what it earns, and see why the three must agree. <bookmark mark='b'/> "
            "We'll ask what the number leaves out. <bookmark mark='c'/> We'll compare one year with the next, which "
            "turns out to depend on whose basket of goods you price, and you'll play with two baskets yourself. "
            "<bookmark mark='d'/> We'll compare countries, measure unemployment with a survey, and ask who gets "
            "the income. <bookmark mark='e'/> And we'll finish with Leontief's table of who buys from whom, the "
            "revisions that rewrite history, and the attempts to measure what GDP does not."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
