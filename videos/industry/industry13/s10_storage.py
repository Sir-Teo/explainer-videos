from __future__ import annotations

from videos.industry.industry13.common import *  # noqa: F403


class Storage(VoiceoverScene):
    def construct(self):
        card(self, 8, "Storing the sun", "Can a battery make money moving power from noon to night?",
             "Chapter eight. Storing the sun.", lit=("make", "dollar", "change"))
        self.day()
        self.arbitrage()

    def day(self):
        St = R["storage"]
        d = St["day"]
        hrs = [r["hour"] for r in d]
        pa = viz.plot_axes([1, 24], [-9000, 16000], x_length=8.8, y_length=4.8, xticks=[1, 6, 12, 18, 24],
                           yticks=[-8000, -4000, 0, 4000, 8000, 12000, 16000], xfmt=lambda v: f"{int(v)}:00",
                           yfmt=lambda v: f"{v / 1000:+.0f} GW" if v else "0", ylabel="California ISO, 15 April 2026", size=14).move_to([-1.9, -0.4, 0])
        zero = Line(pa.ax.c2p(1, 0), pa.ax.c2p(24, 0), stroke_color=GREY_B, stroke_width=1.2)
        sol = Polygon(*[pa.ax.c2p(h, max(r["solar"], 0)) for h, r in zip(hrs, d)], pa.ax.c2p(24, 0), pa.ax.c2p(1, 0), stroke_width=0,
                      fill_color=SUN, fill_opacity=0.4)
        bars = VGroup()
        for h, r in zip(hrs, d):
            v = r["other"]
            p0, p1 = pa.ax.c2p(h, 0), pa.ax.c2p(h, v)
            bars.add(Rectangle(width=0.28, height=max(abs(p1[1] - p0[1]), 0.01), stroke_width=0, fill_color=STORE if v > 0 else BAD,
                               fill_opacity=0.9).move_to([p0[0], (p0[1] + p1[1]) / 2, 0]))
        key = VGroup(VGroup(Square(0.22, stroke_width=0, fill_color=SUN, fill_opacity=0.5), tx("solar", 14, SUN)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.22, stroke_width=0, fill_color=BAD, fill_opacity=0.9), tx("'other', taking power in: charging", 14, BAD)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.22, stroke_width=0, fill_color=STORE, fill_opacity=0.9), tx("'other', giving it back: discharging", 14, STORE)).arrange(RIGHT, buff=0.1)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.9, 2.3, 0])
        notes = VGroup(tx(f"noon: about {abs(St['min_other']) / 1000:.1f} GW going in", 16, BAD, bold=True),
                       tx(f"night: up to {St['max_other'] / 1000:.1f} GW coming out", 16, STORE, bold=True),
                       tx("no power plant consumes power;", 14, GREY_A), tx("this is storage", 14, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([5.3, -0.9, 0])
        src = source("EIA, Hourly Electric Grid Monitor (EIA-930), California ISO, 15 April 2026: solar and 'other fuel sources'", size=13)
        with self.voiceover(
            "The answer to the duck is storage. Here is one spring day in California, the fifteenth of April 2026, from "
            "the same federal data. <bookmark mark='a'/> The solar, rising to a peak at noon. <bookmark mark='b'/> And a "
            "category the grid operator reports as other. At midday it goes negative: something is taking about "
            f"{abs(St['min_other']) / 1000:.0f} gigawatts out of the grid. No power plant does that. Those are batteries, "
            "charging on cheap midday sun. <bookmark mark='c'/> And after sunset they give it back, up to about "
            f"{St['max_other'] / 1000:.0f} gigawatts, just as demand peaks and the solar disappears. California had "
            f"about {R['sun']['battery_cap']:.0f} gigawatts of batteries by April 2026, the agency reports, and their "
            "discharge tripled in two years."
        ) as vo:
            self.play(FadeIn(pa), Create(zero), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(sol), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, UP) for b_, r in zip(bars, d) if r["other"] < 0], lag_ratio=0.1), FadeIn(key[1]),
                      FadeIn(notes[0]), FadeIn(notes[2:]), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_, r in zip(bars, d) if r["other"] >= 0], lag_ratio=0.05), FadeIn(key[2]),
                      FadeIn(notes[1]), run_time=2.0)
        self.clear_scene()

    def arbitrage(self):
        W = R["storage"]["works"]
        p = W["prices"]
        hours = list(range(24))
        pa = viz.plot_axes([0, 23], [0, 70], x_length=7.4, y_length=3.8, xticks=[0, 6, 12, 18, 23], yticks=[20, 40, 60],
                           xfmt=lambda v: f"{int(v)}:00", yfmt=lambda v: f"${v:.0f}", ylabel="chapter 7's sunny day, $ a MWh", size=13).move_to([-2.6, 0.6, 0])
        ln = poly(pa, list(zip(hours, p)), SUN, 3.5)
        ch = VGroup(*[Rectangle(width=0.24, height=0.25, stroke_width=0, fill_color=BAD, fill_opacity=0.9).move_to(pa.ax.c2p(h, 4)) for h in W["charge"]])
        dc = VGroup(*[Rectangle(width=0.24, height=0.25, stroke_width=0, fill_color=STORE, fill_opacity=0.9).move_to(pa.ax.c2p(h, p[h] + 5))
                      for h in W["discharge"]])
        bat = draw.battery(1.2) if hasattr(draw, "battery") else draw.cylinder(1.2, STORE)
        bat.move_to([-6.2, -2.3, 0])
        rows = VGroup(tx("a 100 MW, four-hour battery:", 17, WHITE, bold=True),
                      tx(f"buys at midday, sells at night: ${W['profit'] / 1000:,.0f}k a day", 16, GREY_A),
                      tx(f"= ${W['year']:.1f}m a year", 18, STORE, bold=True),
                      tx(f"it costs about ${W['capex']:.0f}m to build: ${W['fixed']:.1f}m a year", 16, GREY_A),
                      tx("with interest and upkeep", 16, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.07).move_to([-1.4, -2.3, 0])
        side = VGroup(tx("so it needs the bad evenings:", 17, PRICE, bold=True),
                      tx(f"about {W['days_even']:.0f} evenings a year at $1,000", 16, GREY_A),
                      tx("to pay its way on trading alone", 16, GREY_A),
                      tx("or payments for standing ready", 16, GREY_A),
                      tx(f"America's older storage: {W['pumped']:.0f} GW", 15, HYDRO, bold=True),
                      tx("of pumped hydro, water pumped uphill", 14, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.07).move_to([4.6, 0.2, 0])
        tag = estimate_tag("the Works (power.py): an illustrative battery; costs EIA AEO2026, capital 7% over 15 years", corner=DR, size=11)
        src = source("EIA, AEO2026 Electricity Market Module (battery costs); Electric Power Annual 2025, Table 4.3 (pumped storage)", size=12)
        with self.voiceover(
            "Does it pay? Play it with the Works. <bookmark mark='a'/> Take chapter seven's sunny day, with power free at "
            "noon and dear at night. <bookmark mark='b'/> A battery charges in the four cheapest hours and sells in the "
            "four dearest, losing some energy on the way. <bookmark mark='c'/> That earns about "
            f"{W['profit'] / 1000:.0f} thousand dollars a day for a hundred-megawatt battery, about {W['year']:.0f} million "
            f"a year. But the battery costs about {W['capex']:.0f} million dollars to build, which with interest and upkeep "
            f"is about {W['fixed']:.0f} million a year. <bookmark mark='d'/> Ordinary days do not pay for it. It needs the "
            f"bad evenings: about {W['days_even']:.0f} a year when the price hits a thousand dollars, or payments from the "
            "grid for standing ready. Storage, like the peaker, is paid for scarcity. <bookmark mark='e'/> And it is not "
            f"new: America has had about {W['pumped']:.0f} gigawatts of pumped hydro for decades, pumping water uphill when "
            "power is cheap and letting it run down through turbines when it is dear."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(tag), FadeIn(src), FadeIn(bat))
            vo.wait_until("a")
            self.play(Create(ln), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c_, scale=0.5) for c_ in ch], lag_ratio=0.2), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(c_, scale=0.5) for c_ in dc], lag_ratio=0.2), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(rows[:3]))
            self.play(FadeIn(rows[3:]))
            vo.wait_until("d")
            self.play(FadeIn(side[:4], shift=LEFT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(side[4:]))
        self.clear_scene()
