from __future__ import annotations

from videos.industry.industry13.common import *  # noqa: F403


class Physics(VoiceoverScene):
    def construct(self):
        card(self, 2, "A product that cannot be stored", "What does it mean to sell something that must be made the instant it is used?",
             "Chapter two. A product that cannot be stored.", lit=("unit", "make"))
        self.balance()
        self.days()
        self.sorted_hours()

    def balance(self):
        P = R["physics"]
        f = ValueTracker(60.0)
        g = draw.gauge(f, 58.0, 62.0, r=1.5, bands=((BAD, 0.3), (PRICE, 0.45), (GOOD, 0.55), (PRICE, 0.7), (BAD, 1.0)))
        g.move_to([-3.6, 0.2, 0])
        fl = draw.number(lambda: f.get_value(), 2, suffix=" Hz", size=34, color=WHITE)
        fl.add_updater(lambda m: m.next_to(g, DOWN, buff=0.25))
        lab = tx("the grid's frequency", 17, GREY_A).next_to(g, UP, buff=0.15)
        sup = draw.gas_plant(1.2).move_to([2.0, 1.4, 0])
        dem = draw.skyline(2.6).move_to([5.0, 1.4, 0]) if hasattr(draw, "skyline") else draw.house(1.0).move_to([5.0, 1.4, 0])
        sl = tx("supply", 18, GAS, bold=True).next_to(sup, DOWN, buff=0.12)
        dl = tx("demand", 18, DEMAND, bold=True).next_to(dem, DOWN, buff=0.12)
        rules = VGroup(tx("demand above supply: generators slow, frequency falls", 15, BAD),
                       tx("supply above demand: generators speed up, frequency rises", 15, PRICE),
                       tx("fall too far, and protective relays trip plants off the grid", 15, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.3, -1.6, 0])
        nine = VGroup(tx("Texas, 15 February 2021:", 18, WHITE, bold=True),
                      tx(f"operators had {P['nine']:.0f} minutes to stop about 17,000 MW", 16, BAD),
                      tx("of plants tripping, which could have blacked out the whole grid", 16, BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.05).move_to([3.3, -1.6, 0])
        src = source("FERC-NERC staff report on the February 2021 cold weather outages (November 2021)", size=13)
        with self.voiceover(
            "Electricity is almost impossible to store in bulk, so it is made at the very instant it is used. "
            "<bookmark mark='a'/> The whole grid is one machine: thousands of generators spinning in step, at sixty turns "
            "a second in America. <bookmark mark='b'/> When demand runs ahead of supply, the generators slow down, and "
            "the frequency falls. <bookmark mark='c'/> When supply runs ahead, it rises. Fall too far, and relays trip "
            "plants off the grid to protect them, which makes the shortage worse. <bookmark mark='d'/> In the early hours "
            "of the fifteenth of February 2021, the federal report found, Texas's operators had nine minutes to stop "
            "about seventeen thousand megawatts of plants from tripping, enough to black out the whole state's grid."
        ) as vo:
            self.play(FadeIn(g), FadeIn(fl), FadeIn(lab), FadeIn(sup), FadeIn(dem), FadeIn(sl), FadeIn(dl), FadeIn(src))
            vo.wait_until("a")
            self.play(f.animate.set_value(60.02), run_time=1.0)
            self.play(f.animate.set_value(59.99), run_time=1.0)
            vo.wait_until("b")
            self.play(dem.animate.scale(1.2), f.animate.set_value(59.5), FadeIn(rules[0]), run_time=2.0)
            vo.wait_until("c")
            self.play(dem.animate.scale(1 / 1.2), f.animate.set_value(60.3), FadeIn(rules[1]), run_time=1.5)
            self.play(f.animate.set_value(60.0), FadeIn(rules[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeOut(rules), FadeIn(nine), f.animate.set_value(59.3), sup.animate.set_opacity(0.4), run_time=2.0)
        fl.clear_updaters()
        self.clear_scene()

    def days(self):
        P = R["physics"]
        pk, lw = P["peak_curve"], P["low_curve"]
        pa = viz.plot_axes([1, 24], [0, 90000], x_length=9.0, y_length=4.4, xticks=[1, 6, 12, 18, 24],
                           yticks=[20000, 40000, 60000, 80000], xfmt=lambda v: f"{int(v)}:00", yfmt=lambda v: f"{v / 1000:.0f} GW",
                           ylabel="ERCOT's demand, hour by hour", size=14).move_to([-1.4, -0.4, 0])
        hrs = list(range(1, len(pk) + 1))
        lp = poly(pa, list(zip(hrs, pk)), BAD, 4)
        ll = poly(pa, list(zip(range(1, len(lw) + 1), lw)), WIND, 4)
        import datetime as _dt

        def nice(d):
            x = _dt.date.fromisoformat(d)
            return f"{x.day} {x.strftime('%B')} {x.year}"
        key = VGroup(tx(f"{nice(P['peak_day'])}: the year's peak, {max(pk) / 1000:.1f} GW", 16, BAD, bold=True),
                     tx(f"{nice(P['low_day'])}: a mild spring day, peak {max(lw) / 1000:.1f} GW", 16, WIND, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.9, 2.4, 0])
        note = VGroup(tx("the grid must be built for", 16, GREY_A), tx("the red line's highest hour", 16, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.03).move_to([4.8, 0.4, 0])
        head = tx("Texas's grid, two days of 2025", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("EIA, Hourly Electric Grid Monitor (Form EIA-930), ERCOT, demand", size=13)
        with self.voiceover(
            "So demand has a shape, and the grid has to follow it. Here is Texas's grid, run by ERCOT, on two days of "
            f"2025. <bookmark mark='a'/> On {nice(P['peak_day'])}, the hottest stretch of the summer, demand climbed "
            f"through the afternoon to {max(pk) / 1000:.1f} gigawatts at about six in the evening. <bookmark mark='b'/> "
            f"On a mild spring day, {nice(P['low_day'])}, it never passed {max(lw) / 1000:.0f}. <bookmark mark='c'/> "
            "Every power plant, every wire, has to be there for the red line's highest hour, even though most of the "
            "year it is not needed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(lp), FadeIn(key[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(ll), FadeIn(key[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(note), Flash(pa.ax.c2p(int(np.argmax(pk)) + 1, max(pk)), color=BAD))
        self.clear_scene()

    def sorted_hours(self):
        P = R["physics"]
        dur = P["duration"]
        n = len(dur)
        xs = [8 * i for i in range(n)]
        pa = viz.plot_axes([0, P["hours"]], [0, 90000], x_length=9.0, y_length=4.4, xticks=[0, 2000, 4000, 6000, 8000],
                           yticks=[20000, 40000, 60000, 80000], xfmt=lambda v: f"{int(v):,}", yfmt=lambda v: f"{v / 1000:.0f} GW",
                           ylabel="demand, every hour of 2025 sorted from highest to lowest", size=14).move_to([-1.4, -0.4, 0])
        xl = tx("hours of the year", 14, GREY_B).next_to(pa, DOWN, buff=0.05)
        area = Polygon(*[pa.ax.c2p(x, y) for x, y in zip(xs, dur)], pa.ax.c2p(xs[-1], 0), pa.ax.c2p(0, 0), stroke_width=0,
                       fill_color=WIND, fill_opacity=0.35)
        line = poly(pa, list(zip(xs, dur)), WIND, 3)
        cap = Rectangle(width=pa.ax.c2p(P["hours"], 0)[0] - pa.ax.c2p(0, 0)[0], height=pa.ax.c2p(0, P["peak"])[1] - pa.ax.c2p(0, 0)[1],
                        stroke_color=BAD, stroke_width=2, fill_opacity=0).move_to(pa.ax.c2p(0, 0), aligned_edge=DL)
        top10 = P["top"][0.1]
        band = Rectangle(width=pa.ax.c2p(top10, 0)[0] - pa.ax.c2p(0, 0)[0], height=pa.ax.c2p(0, P["peak"])[1] - pa.ax.c2p(0, 0.9 * P["peak"])[1],
                         stroke_width=0, fill_color=BAD, fill_opacity=0.5).move_to(pa.ax.c2p(0, P["peak"]), aligned_edge=UL)
        notes = VGroup(tx(f"load factor: {100 * P['load_factor']:.0f}%", 24, WHITE, bold=True),
                       tx("the blue area over the red box", 14, GREY_A),
                       tx(f"the top tenth of the peak, {0.1 * P['peak'] / 1000:.1f} GW,", 16, BAD),
                       tx(f"was needed in only {top10:,} hours", 16, BAD),
                       tx(f"(Insull's block alone: {100 * R['hook']['lf_alone']:.1f}%)", 14, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([5.25, 0.6, 0])
        src = source("EIA, Hourly Electric Grid Monitor (Form EIA-930), ERCOT, 2025", size=13)
        with self.voiceover(
            f"Now take all {P['hours']:,} hours of 2025 and sort them from the busiest to the quietest. "
            "<bookmark mark='a'/> This is the load duration curve, the shape every power system is built around. "
            f"<bookmark mark='b'/> The red box is the capacity Texas needed for its peak, {P['peak'] / 1000:.1f} gigawatts, "
            "all year. The blue area is what it actually used. <bookmark mark='c'/> The ratio is Insull's load factor: "
            f"about {100 * P['load_factor']:.0f} per cent for the whole of Texas, a world away from his single block, "
            f"because millions of customers smooth each other out. <bookmark mark='d'/> But look at the top: the last "
            f"tenth of the peak, about {0.1 * P['peak'] / 1000:.0f} gigawatts of plants, was needed for only "
            f"{top10:,} hours of the year. Somebody has to build those plants, and get paid for standing ready."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(area), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(cap))
            vo.wait_until("c")
            self.play(FadeIn(notes[:2]), FadeIn(notes[4]))
            vo.wait_until("d")
            self.play(FadeIn(band), FadeIn(notes[2:4]))
        self.clear_scene()
