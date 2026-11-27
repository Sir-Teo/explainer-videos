from __future__ import annotations

from videos.industry.industry13.common import *  # noqa: F403


class Sun(VoiceoverScene):
    def construct(self):
        card(self, 7, "Wind and sun", "What happens to a market when the cheapest power is free and arrives all at once?",
             "Chapter seven. Wind and sun.", lit=("make", "change"))
        self.duck()
        self.capacity()
        self.price()

    def duck(self):
        S = R["sun"]["days"]
        hrs = list(range(1, 25))
        pa = viz.plot_axes([1, 24], [0, 28000], x_length=9.4, y_length=4.6, xticks=[1, 6, 12, 18, 24],
                           yticks=[5000, 10000, 15000, 20000, 25000], xfmt=lambda v: f"{int(v)}:00", yfmt=lambda v: f"{v / 1000:.0f} GW",
                           ylabel="California ISO, an average April day", size=14).move_to([-1.4, -0.4, 0])
        d26 = S[2026]
        dem = poly(pa, list(zip(hrs, d26["demand"])), WHITE, 3)
        sol = Polygon(*[pa.ax.c2p(h, d - max(s, 0)) for h, d, s in zip(hrs, d26["demand"], d26["solar"])],
                      *[pa.ax.c2p(h, d) for h, d in zip(reversed(hrs), reversed(d26["demand"]))], stroke_width=0, fill_color=SUN,
                      fill_opacity=0.45)
        n19 = poly(pa, list(zip(hrs, S[2019]["net"])), GREY_B, 3)
        n26 = poly(pa, list(zip(hrs, d26["net"])), PRICE, 4)
        lo19, lo26 = min(S[2019]["net"]), min(d26["net"])
        i0 = 15
        ramp = max(d26["net"][16:21]) - min(d26["net"][14:18])
        key = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=WHITE, stroke_width=3), tx("demand, April 2026", 14, WHITE)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.22, stroke_width=0, fill_color=SUN, fill_opacity=0.5), tx("met by solar", 14, SUN)).arrange(RIGHT, buff=0.1),
                     VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=GREY_B, stroke_width=3), tx("left for other plants, April 2019", 14, GREY_B)).arrange(RIGHT, buff=0.1),
                     VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=PRICE, stroke_width=4), tx("left for other plants, April 2026", 14, PRICE)).arrange(RIGHT, buff=0.1)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.9, 2.3, 0])
        notes = VGroup(tx(f"midday: {lo19 / 1000:.1f} GW in 2019,", 15, GREY_A), tx(f"{lo26 / 1000:.1f} GW in 2026", 15, PRICE, bold=True),
                       tx(f"sunset: about {ramp / 1000:.0f} GW more", 15, GREY_A), tx("needed within three hours", 15, PRICE, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.05).move_to([4.9, -1.0, 0])
        del i0
        src = source("EIA, Hourly Electric Grid Monitor (EIA-930), California ISO: demand, solar and wind, April 2019 and 2026", size=13)
        with self.voiceover(
            "Wind and solar have no fuel, so once built they cost almost nothing to run. That changes everything about "
            "the day. <bookmark mark='a'/> Here is California's grid on an average April day in 2026. Demand, the white "
            "line, barely moves. <bookmark mark='b'/> But from mid-morning, solar meets a huge share of it. "
            "<bookmark mark='c'/> What is left for every other plant is the demand minus the wind and sun. In 2019 it "
            "sagged at midday. <bookmark mark='d'/> By 2026 the sag is far deeper, and then, as the sun sets, the other "
            f"plants must find about {ramp / 1000:.0f} gigawatts within about three hours. Engineers call this shape the "
            "duck curve: the belly at noon, the neck at dusk."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(dem), FadeIn(key[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(sol), FadeIn(key[1]))
            vo.wait_until("c")
            self.play(Create(n19), FadeIn(key[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(n26), FadeIn(key[3]), run_time=2.0)
            self.play(FadeIn(notes))
        self.clear_scene()

    def capacity(self):
        S = R["sun"]
        caps = [("solar", S["solar_cap"], SUN, draw.solar_panel(1.0)), ("batteries", S["battery_cap"], STORE, draw.battery(0.7)
                                                                        if hasattr(draw, "battery") else draw.cylinder(0.8, STORE)),
                ("natural gas", S["gas_cap"], GAS, draw.gas_plant(0.9))]
        bars = VGroup()
        for i, (n, v, col, ic) in enumerate(caps):
            x = -4.6 + 2.6 * i
            b = Rectangle(width=1.4, height=v / 30 * 3.6, stroke_width=0, fill_color=col, fill_opacity=0.88).move_to([x, -2.4, 0], aligned_edge=DOWN)
            ic.scale_to_fit_height(min(ic.height, 0.8)).next_to(b, UP, buff=0.5)
            bars.add(VGroup(b, ic, tx(f"{v:.0f} GW", 20, col, bold=True).next_to(b, UP, buff=0.08), tx(n, 16, GREY_A).next_to(b, DOWN, buff=0.12)))
        head = tx("California ISO, April 2026: capacity", 21, WHITE, bold=True).move_to([-2.0, 3.0, 0])
        facts = VGroup(tx("April 2024 to April 2026:", 16, GREY_A), tx("solar capacity +19%", 17, SUN, bold=True),
                       tx("battery capacity +79%", 17, STORE, bold=True), tx("gas capacity about the same", 17, GAS, bold=True),
                       tx("January-May 2026:", 16, GREY_A),
                       tx(f"solar out-generated gas on {S['solar_days']:.0f}% of days", 17, SUN, bold=True),
                       tx("(21% in 2024 and in 2025)", 15, GREY_A),
                       tx(f"battery discharge: {S['battery_x']:.0f} times 2024's", 17, STORE, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.2, 0.2, 0])
        src = source("EIA, Today in Energy, 'Solar generation in CAISO surpassed natural gas in the first five months of 2026' "
                     "(16 June 2026)", size=13)
        with self.voiceover(
            "California is where this has gone furthest. <bookmark mark='a'/> By April 2026, the state's grid operator had "
            f"about {S['solar_cap']:.0f} gigawatts of utility-scale solar, {S['battery_cap']:.0f} of batteries, and "
            f"{S['gas_cap']:.0f} of gas, the government's energy agency reports. <bookmark mark='b'/> In two years solar grew "
            "by about a fifth and batteries by almost four-fifths, while gas stood still. <bookmark mark='c'/> In the first "
            f"five months of 2026, solar made more electricity than gas on {S['solar_days']:.0f} per cent of days, up "
            "from about a fifth in the two years before."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), *[FadeIn(b_[3]) for b_ in bars])
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_[0], DOWN), FadeIn(b_[1]), FadeIn(b_[2])) for b_ in bars], lag_ratio=0.3),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(facts[:4]))
            vo.wait_until("c")
            self.play(FadeIn(facts[4:]))
        self.clear_scene()

    def price(self):
        W = R["sun"]["works"]
        hours, p0, p1 = W["hours"], W["p_lo"], W["p_hi"]
        cap0, cap1 = W["cap_lo"], W["cap_hi"]
        pa = viz.plot_axes([0, 23], [0, 70], x_length=8.4, y_length=4.2, xticks=[0, 6, 12, 18, 23], yticks=[20, 40, 60],
                           xfmt=lambda v: f"{int(v)}:00", yfmt=lambda v: f"${v:.0f}", ylabel="price, $ a MWh", size=14).move_to([-1.8, -0.4, 0])
        l0 = poly(pa, list(zip(hours, p0)), GREY_B, 3)
        l1 = poly(pa, list(zip(hours, p1)), SUN, 4)
        notes = VGroup(tx("what a MWh of solar earns:", 16, GREY_A), tx(f"few solar plants: ${cap0:.0f}", 18, GREY_B, bold=True),
                       tx(f"many solar plants: ${cap1:.0f}", 18, SUN, bold=True), tx("solar's success lowers", 15, GREY_A),
                       tx("the price solar is paid", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([4.6, 0.4, 0])
        key = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=GREY_B, stroke_width=3), tx("a day with little solar", 14, GREY_B)).arrange(RIGHT, buff=0.1),
                     VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=SUN, stroke_width=4), tx("the same day with 60 GW of solar", 14, SUN)).arrange(RIGHT, buff=0.1)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([-3.4, 2.5, 0])
        tag = estimate_tag("the Works (power.py): Chapter 4's illustrative fleet, an illustrative day", corner=DR, size=12)
        with self.voiceover(
            "And free fuel does something strange to the price. <bookmark mark='a'/> Take chapter four's merit order, on "
            "a day with little solar: through the day the price is set by gas, and it rises for the evening peak. "
            "<bookmark mark='b'/> Now add a lot of solar. At midday it pushes every gas and coal plant out of the merit "
            "order, and the price falls to nothing; in the evening, when the sun has gone, it is exactly as high as "
            "before. <bookmark mark='c'/> So the more solar there "
            f"is, the less each megawatt-hour of it earns: here, from about {cap0:.0f} dollars to about {cap1:.0f}. The "
            "cheapest power undercuts itself, and the money moves to whoever can deliver in the evening."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(l0), FadeIn(key[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(l1), FadeIn(key[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(notes, shift=LEFT * 0.1))
        self.clear_scene()
