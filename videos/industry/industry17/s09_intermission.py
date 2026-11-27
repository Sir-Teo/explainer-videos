from __future__ import annotations

from videos.industry.industry17.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.prices()
        self.sales()

    def prices(self):
        H = R["history"]
        rel = H["rel"]
        pa = viz.plot_axes([1948, 2026], [0, 2.0], x_length=10.2, y_length=4.5, xticks=[1950, 1970, 1990, 2010, 2025],
                           yticks=[0, 0.5, 1.0, 1.5, 2.0], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"x{v:g}",
                           ylabel="price against all consumer prices, 1948 = 1 (used cars: 1953 = 1)", size=13).move_to([-0.5, -0.6, 0])
        one = DashedLine(pa.ax.c2p(1948, 1), pa.ax.c2p(2026, 1), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        ln = poly(pa, sorted((y, v) for y, v in rel["new"].items() if y <= 2025), MAKER, 4)
        lr = poly(pa, sorted((y, v) for y, v in rel["repair"].items() if y <= 2025), SUPPLIER, 4)
        lu = poly(pa, sorted((y, v) for y, v in rel["used"].items() if y <= 2025), DEALER, 3)
        l1 = tx(f"a new car: x{rel['new'][2025]:.2f}", 17, MAKER, bold=True).next_to(pa.ax.c2p(2025, rel["new"][2025]), LEFT, buff=0.2).shift(DOWN * 0.3)
        l2 = tx(f"repairs: x{rel['repair'][2025]:.2f}", 17, SUPPLIER, bold=True).next_to(pa.ax.c2p(2025, rel["repair"][2025]), LEFT, buff=0.2).shift(UP * 0.3)
        l3 = tx("used cars", 15, DEALER, bold=True).next_to(pa.ax.c2p(2021, rel["used"][2022]), UP, buff=0.15)
        head = tx("Intermission: what a car has cost since 1948", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("BLS, CPI-U: new vehicles, used cars and trucks, motor vehicle maintenance and repair, all items; US city "
                     "average, annual averages (via FRED); the index adjusts for quality", size=12)
        with self.voiceover(
            "An intermission, and three lines from America's consumer price index, each set against all prices. "
            f"<bookmark mark='a'/> Since 1948 prices in general have risen about {H['all_x']:.0f} times. The price index for "
            f"new vehicles has risen {H['new_x']:.1f} times. Against everything else, a new car costs "
            f"{rel['new'][2025]:.2f} of what it did, about a third, because the index counts the better car each year "
            "buys: the safety, the reliability, the electronics. <bookmark mark='b'/> Repairs went the other way. The price "
            f"of having a car maintained and fixed rose {H['rep_x']:.0f} times, faster than prices in general. "
            "<bookmark mark='c'/> And used cars, after decades of drifting down, jumped "
            f"{100 * H['used_2021']:.0f} per cent between 2020 and 2022, when the chip shortage left the new car lots empty. "
            "Making cars is a business of falling prices. Fixing them is not."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(one), FadeIn(head), FadeIn(src), FadeIn(ghost(ln, lr, opacity=0.3)))
            vo.wait_until("a")
            self.play(Create(ln), run_time=3.0)
            self.play(FadeIn(l1))
            vo.wait_until("b")
            self.play(Create(lr), run_time=2.5)
            self.play(FadeIn(l2))
            vo.wait_until("c")
            self.play(Create(lu), run_time=2.0)
            self.play(FadeIn(l3))
        self.clear_scene()

    def sales(self):
        H = R["history"]
        ms = {m: v for m, v in H["monthly_sales"].items()}
        months = sorted(ms)
        t = lambda m: int(m[:4]) + (int(m[5:7]) - 0.5) / 12  # noqa: E731
        pa = viz.plot_axes([1976, 2027], [0, 24], x_length=10.4, y_length=4.4, xticks=[1980, 1990, 2000, 2010, 2020],
                           yticks=[0, 5, 10, 15, 20], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}m",
                           ylabel="US light vehicle sales, millions a year (seasonally adjusted rate)", size=13).move_to([-0.3, -0.5, 0])
        line = poly(pa, [(t(m), ms[m]) for m in months], PRICE, 2)
        marks = VGroup()
        for y, lab in ((1982, "1982"), (2009, "2009")):
            v = H["sales"][y]
            d = Dot(pa.ax.c2p(y + 0.5, v), radius=0.08, color=BAD)
            marks.add(VGroup(d, tx(f"{lab}: {v:.1f}m", 14, BAD, bold=True).next_to(d, DOWN, buff=0.1)))
        lo20 = min((m for m in months if m.startswith("2020")), key=lambda m: ms[m])
        d20 = Dot(pa.ax.c2p(t(lo20), ms[lo20]), radius=0.08, color=BAD)
        l20 = tx(f"April 2020: {ms[lo20]:.1f}m", 14, BAD, bold=True).next_to(d20, RIGHT, buff=0.1)
        pk = H["sales_peak"]
        dpk = Dot(pa.ax.c2p(pk + 0.5, H["sales"][pk]), radius=0.08, color=GOOD)
        lpk = tx(f"{pk}: {H['sales'][pk]:.1f}m", 14, GOOD, bold=True).next_to(dpk, UP, buff=0.1)
        src = source("US Bureau of Economic Analysis, total vehicle sales (via FRED, TOTALSA)", size=12)
        with self.voiceover(
            "And here is how many vehicles Americans bought each year since 1976, month by month. <bookmark mark='a'/> The "
            "line breathes with the economy. In a good year Americans buy around seventeen million. <bookmark mark='b'/> In "
            f"the bad years they put off the purchase: {H['sales'][1982]:.1f} million a year in 1982, "
            f"{H['sales'][2009]:.1f} million in 2009, and for one month in the spring of 2020, a rate of "
            f"{ms[lo20]:.1f} million. <bookmark mark='c'/> A car is the easiest big purchase to postpone, because the old "
            "one still runs. Between 2007 and 2009 American sales fell by more than a third. So the business that needs its "
            "plants full sells a product whose demand can collapse in two years."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(ghost(line, opacity=0.3)))
            vo.wait_until("a")
            self.play(Create(line), run_time=3.5)
            self.play(GrowFromCenter(dpk), FadeIn(lpk))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m_) for m_ in marks], lag_ratio=0.4), GrowFromCenter(d20), FadeIn(l20))
            vo.wait_until("c")
            self.play(Indicate(marks[1], color=BAD))
        self.clear_scene()
