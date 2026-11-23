from __future__ import annotations

from videos.industry.industry4.common import *  # noqa: F403
from videos.industry.industry4.compute import avail, demand, sun

X0, Y0, XL, YL = -0.55, -2.75, 7.1, 4.9   # the stack chart: origin and size
GW_MAX, P_MAX = 1200.0, 60.0


def gx(gw: float) -> float:
    return X0 + XL * gw / GW_MAX


def gy(p: float) -> float:
    return Y0 + YL * min(p, P_MAX) / P_MAX


def clock(h: float) -> str:
    h = round(h * 4) / 4  # quarter hours, so each label is typeset once and cached
    hh = int(h) % 24
    mm = int(round((h - int(h)) * 60)) % 60
    ap = "am" if hh < 12 else "pm"
    h12 = hh % 12 or 12
    return f"{h12}:{mm:02d} {ap}"


class Stack(VoiceoverScene):
    def construct(self):
        card(self, 8, "The Stack", "Who sets the price of electricity, hour by hour?",
             "Chapter eight. The Stack: a day on America's power grid.", lit=("make", "dollar"))
        self.build()

    def build(self):
        B = R["fleet"]["blocks"]
        hour = ValueTracker(4.0)

        # --- the chart ----------------------------------------------------------------------------------------
        xa = Line([X0, Y0, 0], [X0 + XL + 0.15, Y0, 0], stroke_color=GREY_B, stroke_width=2)
        ya = Line([X0, Y0, 0], [X0, Y0 + YL + 0.2, 0], stroke_color=GREY_B, stroke_width=2)
        yt = VGroup(*[VGroup(Line([X0 - 0.06, gy(p), 0], [X0, gy(p), 0], stroke_color=GREY_B),
                             tx(f"${p}", 16, GREY_B).next_to([X0 - 0.06, gy(p), 0], LEFT, buff=0.06))
                      for p in (0, 20, 40, 60)])
        xt = VGroup(*[tx(f"{g:,}", 16, GREY_B).next_to([gx(g), Y0, 0], DOWN, buff=0.08) for g in (0, 400, 800, 1200)])
        xl = tx("gigawatts available", 17, GREY_B).next_to([gx(600), Y0, 0], DOWN, buff=0.38)
        yl = tx("cost of one more MWh", 17, GREY_B).rotate(PI / 2).next_to([X0, gy(30), 0], LEFT, buff=0.55)
        axes = VGroup(xa, ya, yt, xt, xl, yl)

        # --- phase 1: the whole fleet, installed capacity ---------------------------------------------------------
        def rect(b, width_gw, left_gw):
            hgt = max(gy(b["mc"]) - Y0, 0.07)
            return Rectangle(width=max(XL * width_gw / GW_MAX, 0.004), height=hgt, stroke_width=0,
                             fill_color=TECH[b["key"]], fill_opacity=0.9).move_to(
                [gx(left_gw) + XL * width_gw / GW_MAX / 2, Y0 + hgt / 2, 0])
        installed, left = VGroup(), 0.0
        lefts = []
        for b in B:
            installed.add(rect(b, b["gw"], left))
            lefts.append(left)
            left += b["gw"]
        icons = VGroup(*[icon(b["key"], 0.5) for b in B])
        for ic, r in zip(icons, installed):
            ic.next_to(r, UP, buff=0.08)
        oil_tag = tx(f"${B[-1]['mc']:.0f}", 16, TECH["oil"]).next_to(installed[-1], UP, buff=0.62)
        names = VGroup(*[tx(f"{b['name']}\n${b['mc']:.0f}", 14, TECH[b["key"]]) for b in B])
        head = tx("Every US power plant, cheapest to run on the left", 24).to_edge(UP, buff=0.25)
        src = source("EIA, Electric Power Annual 2025: capacity, fuel costs, heat rates; fuel and running cost per MWh",
                     size=12)
        with self.voiceover(
            "Here is how an industry's costs become its price, in the plainest case there is: electricity. "
            "<bookmark mark='a'/> Line up every power station in America by what it costs to make one more "
            "megawatt-hour, cheapest on the left. The width of each block is how much it can produce; its height, "
            "what one more unit costs it. <bookmark mark='b'/> Wind and solar come first: once they are built, the "
            "wind and the sun are free. <bookmark mark='c'/> Then hydro, and the nuclear plants, at about nine "
            "dollars a megawatt-hour, mostly fuel. <bookmark mark='d'/> Then coal at about twenty-six, the big "
            "combined-cycle gas plants at thirty-three, older gas boilers at forty, <bookmark mark='e'/> the gas "
            "turbines that only run at the peaks, forty-six, and at the very end, oil, at a hundred and fifty-five, "
            "off the top of the chart. <bookmark mark='f'/> This staircase is the industry's supply curve. "
            "Economists call it the merit order; this series calls it the Stack."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(axes), run_time=1.5)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(*[AnimationGroup(GrowFromEdge(installed[i], DOWN), FadeIn(icons[i], shift=DOWN * 0.1))
                        for i in (0, 1)], run_time=1.2)
            vo.wait_until("c")
            self.play(*[AnimationGroup(GrowFromEdge(installed[i], DOWN), FadeIn(icons[i], shift=DOWN * 0.1))
                        for i in (2, 3)], run_time=1.2)
            vo.wait_until("d")
            self.play(*[AnimationGroup(GrowFromEdge(installed[i], DOWN), FadeIn(icons[i], shift=DOWN * 0.1))
                        for i in (4, 5, 6)], run_time=1.4)
            vo.wait_until("e")
            self.play(*[AnimationGroup(GrowFromEdge(installed[i], DOWN), FadeIn(icons[i], shift=DOWN * 0.1))
                        for i in (7, 8)], FadeIn(oil_tag), run_time=1.2)
            vo.wait_until("f")
            stair = VMobject(stroke_color=WHITE, stroke_width=3).set_points_as_corners(
                [[X0, Y0, 0]] + [p for r in installed for p in (r.get_corner(UL), r.get_corner(UR))])
            self.play(Create(stair), run_time=1.8)
            self.play(FadeOut(stair))

        # --- phase 2: a day ---------------------------------------------------------------------------------------
        sky = Rectangle(width=6.0, height=3.7, stroke_width=0, fill_color=draw.sky_color(4),
                        fill_opacity=1).move_to([-3.95, 1.55, 0])
        city = draw.skyline(5.8, seed=7).scale_to_fit_width(5.8)
        city.move_to(sky.get_bottom(), aligned_edge=DOWN)
        sun_g = draw.sun(0.3)
        moon_g = draw.moon(0.24).move_to([-1.6, 2.9, 0])
        clock_t = always_redraw(lambda: tx(clock(hour.get_value()), 26, bold=True).move_to([-6.15, 3.1, 0]))
        dem_t = always_redraw(lambda: tx(f"demand {5 * round(demand(hour.get_value()) / 5):,.0f} GW", 20, "#E8EAED").move_to(
            [-6.0, 2.62, 0], aligned_edge=LEFT).shift(LEFT * 0.75))

        def avail_widths(h):
            return [avail(b["key"], b["gw"], h) for b in B]

        def state(h):
            w = avail_widths(h)
            d = demand(h)
            acc, marg = 0.0, 0
            for i, wi in enumerate(w):
                if acc < d:
                    marg = i
                acc += wi
            return w, d, marg

        def upd_blocks(g):
            w, d, marg = state(hour.get_value())
            left_ = 0.0
            for i, (r, b) in enumerate(zip(g, B)):
                hgt = max(gy(b["mc"]) - Y0, 0.07)
                r.become(rect(b, w[i], left_))
                running = left_ < d
                r.set_fill(opacity=0.95 if running else 0.25)
                if i == marg:
                    r.set_stroke(WHITE, width=3)
                left_ += w[i]
                del hgt
        blocks = VGroup(*[rect(b, wi, sum(avail_widths(4.0)[:i])) for i, (b, wi) in enumerate(zip(B, avail_widths(4.0)))])

        def upd_icons(g):
            w, d, marg = state(hour.get_value())
            for i, (ic, r) in enumerate(zip(g, blocks)):
                ic.next_to(r, UP, buff=0.08)
                op = 1.0 if w[i] > 8 else 0.0
                ic.set_opacity(op)
            icons_marg[0] = marg

        icons_marg = [0]
        dline = always_redraw(lambda: DashedLine([gx(demand(hour.get_value())), Y0, 0],
                                                 [gx(demand(hour.get_value())), Y0 + YL + 0.1, 0],
                                                 stroke_color=WHITE, stroke_width=2.5))
        dlab = always_redraw(lambda: tx("demand", 16).next_to([gx(demand(hour.get_value())), Y0 + YL + 0.1, 0], UP,
                                                               buff=0.04))

        def price_now():
            w, d, marg = state(hour.get_value())
            return B[marg]["mc"], marg
        pline = always_redraw(lambda: DashedLine([X0, gy(price_now()[0]), 0],
                                                 [gx(demand(hour.get_value())), gy(price_now()[0]), 0],
                                                 stroke_color=PRICE, stroke_width=2.5))
        price_t = always_redraw(lambda: VGroup(
            tx("price for everyone", 18, GREY_B),
            tx(f"${price_now()[0]:.0f} per MWh", 34, PRICE, bold=True),
            tx(f"set by: {B[price_now()[1]]['name'].lower()}", 18, TECH[B[price_now()[1]]['key']]),
        ).arrange(DOWN, buff=0.06).move_to([-3.95, -1.55, 0]))

        def upd_sky(m):
            h = hour.get_value()
            m.set_fill(draw.sky_color(h))
            s_ = sun(h)
            x = -6.6 + 5.3 * min(max((h - 6) / 14, 0), 1)
            sun_g.move_to([x, 0.3 + 2.5 * s_, 0]).set_opacity(1.0 if s_ > 0.02 else 0.0)
            moon_g.set_opacity(0.0 if 6.5 < h < 19.5 else 1.0)
            draw.light(city.windows, (demand(h) - 460) / 300)

        def show_day():
            sky.add_updater(upd_sky)
            blocks.add_updater(upd_blocks)
            icons.add_updater(upd_icons)
            draw.spin(icons[0], 1.8)

        with self.voiceover(
            "Now run a day, a hot summer weekday. <bookmark mark='a'/> On the left, the country; on the right, only "
            "what can run at this hour: the wind is light today, and the dams save their water for the evening. "
            "<bookmark mark='b'/> At four in the morning America needs about four hundred and seventy gigawatts. "
            "Fill the stack from the left until demand is met. The last plant needed, the marginal plant, sets the "
            "price, and every plant running is paid that same price: about thirty-three dollars, set by a "
            "combined-cycle gas plant. <bookmark mark='c'/> The sun comes up. Solar slides in at the bottom of the "
            "stack, at zero cost, and pushes every other block to the right. Demand rises through the morning, "
            "but the sun keeps pace, and gas still sets the price."
        ) as vo:
            self.play(FadeOut(oil_tag), FadeOut(head), ReplacementTransform(installed, blocks),
                      FadeIn(sky), FadeIn(city), FadeIn(moon_g), FadeIn(sun_g.set_opacity(0)), run_time=1.6)
            self.add(blocks, icons)
            show_day()
            self.play(FadeIn(clock_t), FadeIn(dem_t))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(dline), FadeIn(dlab))
            self.play(Create(pline), FadeIn(price_t))
            vo.wait_until("c")
            self.play(hour.animate.set_value(12.5), run_time=max(4.0, vo.duration * 0.35), rate_func=linear)
        with self.voiceover(
            "Late in the afternoon, the air conditioners are all on and demand climbs past seven hundred "
            "gigawatts. <bookmark mark='a'/> And the sun is setting: the solar block shrinks just as demand peaks. "
            "<bookmark mark='b'/> The stack has to reach further right, past the gas boilers, into the peakers, the "
            "gas turbines that run one hour in seven. The price jumps to forty-six dollars, for every megawatt-hour "
            "sold in that hour, from every plant. <bookmark mark='c'/> Then night falls, demand ebbs, and the big "
            "gas plants set the price again."
        ) as vo:
            self.play(hour.animate.set_value(17.0), run_time=4.0, rate_func=linear)
            vo.wait_until("a")
            self.play(hour.animate.set_value(19.0), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(Indicate(price_t, color=PRICE, scale_factor=1.08))
            vo.wait_until("c")
            self.play(hour.animate.set_value(24.0), run_time=4.0, rate_func=linear)
        rents = Rectangle(width=gx(demand(24)) - X0, height=gy(B[5]["mc"]) - Y0, stroke_width=0, fill_color=PROFIT,
                          fill_opacity=0.18).move_to([X0, Y0, 0], aligned_edge=DL)
        rent_t = tx("the gap between the price and each plant's own cost:\nwhat the cheaper plants keep", 18,
                    PROFIT).move_to([gx(300), gy(52), 0])
        tag = estimate_tag("the day is illustrative; the plants and their costs are the 2025 fleet", corner=DR)
        with self.voiceover(
            "Two lessons. <bookmark mark='a'/> First, the price is set by the cost of one more unit from the last "
            "plant needed, not by the average cost of all of them. <bookmark mark='b'/> Second, everyone to the left "
            "of the marginal plant earns the gap between that price and their own cost. A nuclear plant that can "
            "make power for nine dollars is paid thirty-three. That gap is what pays for the plant itself, which is "
            "the subject of this whole part: the cost of one more is not the whole cost. The day is illustrative; "
            "the plants, their sizes and their costs are America's fleet in 2025."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(pline, color=PRICE))
            vo.wait_until("b")
            self.play(FadeIn(rents), FadeIn(rent_t))
        for m in (sky, blocks, icons, icons[0].rotor):
            m.clear_updaters()
        self.clear_scene()
