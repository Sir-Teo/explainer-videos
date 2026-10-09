from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.trading.common import FACTS, GeoMap, label, load, note, server_box, source, tagged


def tower(color=C.MICROWAVE, h=0.32) -> VGroup:
    mast = Polygon(UP * h, DOWN * 0 + LEFT * h * 0.22, RIGHT * h * 0.22, stroke_color=color, stroke_width=1.5,
                   fill_opacity=0)
    dish = Dot(UP * h, radius=0.035, color=color)
    return VGroup(mast, dish)


class SpeedOfLight(VoiceoverScene):
    def construct(self):
        self.geography()
        self.race()
        self.colocation()

    # ------------------------------------------------------------------
    def geography(self):
        g = load("geo")
        r = g["routes"]["carteret"]
        km, vac_ms, fib_ms = r["km"], r["vacuum_ms"], r["fiber_straight_ms"]
        assert 1170 < km < 1185 and abs(vac_ms - 3.93) < 0.01 and abs(fib_ms - 5.77) < 0.01
        m = GeoMap(width=12.6).shift(DOWN * 0.62)
        self.m = m
        pts = {k: m.site(k) for k in ("aurora", "carteret", "mahwah", "secaucus")}
        dots = VGroup(*[Dot(p, radius=0.08, color=C.LIGHT if k == "aurora" else WHITE) for k, p in pts.items()])
        cme = tagged(r"CME Group, Aurora, IL\\{\small S\&P 500 futures}", font_size=26, color=C.LIGHT)
        cme.next_to(pts["aurora"], DOWN, buff=0.2)
        nj = VGroup(
            tagged(r"NYSE, Mahwah", font_size=22).next_to(pts["mahwah"], UL, buff=0.08),
            tagged(r"Equinix NY4, Secaucus", font_size=22).next_to(pts["secaucus"], LEFT, buff=0.15),
            tagged(r"Nasdaq, Carteret", font_size=22).next_to(pts["carteret"], DOWN, buff=0.12).shift(LEFT * 0.3),
        )
        src = source(r"OpenStreetMap (addresses), Natural Earth (outlines)", font_size=18)
        head = label(r"the speed of light", font_size=40).to_edge(UP, buff=0.5)
        self.play(FadeIn(head), run_time=0.6)
        with self.voiceover(
            "Every race in this market is limited by one fact about the universe: information cannot travel faster "
            "than light. <bookmark mark='map'/> Here is the most valuable stretch of geography in American finance. "
            "<bookmark mark='cme'/> In Aurora, Illinois, outside Chicago, sits the matching engine of the CME, where "
            "S&P 500 futures trade. <bookmark mark='nj'/> And about seven hundred miles east, in New Jersey, sit the "
            "stock exchanges: Nasdaq in Carteret, the New York Stock Exchange in Mahwah, and many other venues "
            "around Secaucus."
        ) as vo:
            vo.wait_until("map")
            self.play(FadeIn(m), FadeIn(src), FadeOut(head), run_time=1.5)
            vo.wait_until("cme")
            self.play(GrowFromCenter(dots[0]), FadeIn(cme, shift=UP * 0.1))
            vo.wait_until("nj")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots[1:]], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(t) for t in nj], lag_ratio=0.3), run_time=2)

        gc = m.route("carteret", color=C.LIGHT, stroke_width=3)
        dist = tagged(rf"{km:,.0f} km".replace(",", "{,}") + r" in a straight line", font_size=28, color=C.LIGHT)
        dist.move_to(gc.point_from_proportion(0.42) + UP * 0.45)
        vac = VGroup(
            label(r"light in a vacuum:", font_size=30, color=C.LIGHT),
            MathTex(rf"\frac{{{km:,.0f}\ \text{{km}}}}{{299{{,}}792\ \text{{km/s}}}} = {vac_ms:.2f}\ \text{{ms}}".replace(",", "{,}", 1),
                    font_size=34, color=C.LIGHT),
        ).arrange(RIGHT, buff=0.25).to_edge(UP, buff=0.35)
        with self.voiceover(
            "When futures move in Chicago, every quote on a related stock or ETF in New Jersey is suddenly out of date, "
            "so there's a race to carry the news east. <bookmark mark='gc'/> The shortest path along the Earth's "
            "surface is about 1,178 kilometers. <bookmark mark='v'/> Light in a vacuum covers that in 3.93 "
            "milliseconds. That's the floor. No network, no algorithm, no amount of money will ever beat it."
        ) as vo:
            vo.wait_until("gc")
            self.play(FadeOut(cme), Create(gc), FadeIn(dist), run_time=2)
            vo.wait_until("v")
            self.play(FadeIn(vac, shift=DOWN * 0.15))
        self.gc, self.dist, self.vac, self.dots, self.nj = gc, dist, vac, dots, nj

        # fiber: slower glass, longer routes
        n = load("geo")["n_fiber"]
        glass = VGroup(
            label(r"light in glass fiber:", font_size=30, color=C.FIBER),
            MathTex(rf"{vac_ms:.2f}\ \text{{ms}} \times {n:.2f} = {fib_ms:.2f}\ \text{{ms}}", font_size=34, color=C.FIBER),
            label(r"(if the fiber were perfectly straight)", font_size=24, color=GREY_B),
        ).arrange(RIGHT, buff=0.25).next_to(vac, DOWN, buff=0.25)
        spread = VGroup(
            label(r"Spread Networks, 2010", font_size=28, color=C.FIBER),
            label(rf"{FACTS['spread_miles']} miles of new fiber; {FACTS['spread_rtt_ms']} ms round trip", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        spread.to_corner(DL, buff=0.45).shift(UP * 0.4)
        spread.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.12)
        with self.voiceover(
            "<bookmark mark='g'/> Light in optical fiber is slower. Glass has a refractive index of about 1.47, so "
            "even a perfectly straight fiber would take 5.77 milliseconds. And real fiber follows railways and "
            "highways. <bookmark mark='s'/> In 2010, a company called Spread Networks dug a new, straighter route "
            "through the Allegheny Mountains, 825 miles of cable, just to bring the round trip down to 13.33 "
            "milliseconds. Trading firms paid a fortune to lease it."
        ) as vo:
            vo.wait_until("g")
            self.play(FadeIn(glass, shift=DOWN * 0.15))
            vo.wait_until("s")
            self.play(FadeIn(spread, shift=UP * 0.15))
        self.glass, self.spread = glass, spread

    # ------------------------------------------------------------------
    def route_variant(self, wiggle: float, n_waves: float, color, phase=0.0) -> VMobject:
        """The great circle with a smooth sideways wiggle (a schematic route)."""
        m = self.m
        g = load("geo")["routes"]["carteret"]["path"]
        pts = np.array([m.p(lat, lon) for lon, lat in g])
        d = np.gradient(pts, axis=0)
        nrm = np.stack([-d[:, 1], d[:, 0], np.zeros(len(d))], 1)
        nrm /= np.linalg.norm(nrm, axis=1, keepdims=True)
        t = np.linspace(0, 1, len(pts))
        env = np.sin(np.pi * t) ** 0.7
        off = wiggle * env * np.sin(2 * np.pi * n_waves * t + phase)
        return VMobject().set_points_smoothly(pts + nrm * off[:, None]).set_stroke(color, 3)

    def race(self):
        m = self.m
        r = load("geo")["routes"]["carteret"]
        vac_ms, fib_ms = r["vacuum_ms"], r["fiber_straight_ms"]
        mw_ms = FACTS["quincy_carteret_ms"]
        extra_us = (mw_ms - vac_ms) * 1000
        assert abs(extra_us - 53) < 1.5
        mw_route = self.route_variant(0.05, 9, C.MICROWAVE)
        towers = VGroup()
        for s in np.linspace(0.04, 0.96, 19):
            towers.add(tower().move_to(mw_route.point_from_proportion(s), aligned_edge=DOWN))
        mw_tag = VGroup(
            label(r"microwave towers, in sight of each other", font_size=26, color=C.MICROWAVE),
            label(rf"Aurora $\to$ Carteret: {mw_ms:.3f} ms ({FACTS['quincy_year']})", font_size=26, color=C.MICROWAVE),
            label(rf"just {extra_us:.0f} $\mu$s ({100 * extra_us / 1000 / vac_ms:.1f}\%) slower than light in a vacuum",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        mw_tag.to_corner(DR, buff=0.4).shift(UP * 0.35)
        mw_tag.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.12)
        sch = note(r"tower positions schematic").next_to(mw_tag, UP, buff=0.12).align_to(mw_tag, RIGHT)
        with self.voiceover(
            "<bookmark mark='mw'/> Then the industry did something that sounds backwards: it went back to radio. "
            "Microwaves travel through air at almost exactly the speed of light, so firms built chains of towers, "
            "each able to see the next, as close to the great circle as the landscape allows. <bookmark mark='q'/> "
            "By 2016, one network was delivering data from Aurora to Carteret in 3.982 milliseconds, just 53 "
            "microseconds, or 1.3 percent, slower than light in a vacuum."
        ) as vo:
            vo.wait_until("mw")
            self.play(FadeOut(self.spread), FadeOut(self.dist), LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in towers],
                                                                         lag_ratio=0.08), run_time=2.5)
            vo.wait_until("q")
            self.play(FadeIn(mw_tag), FadeIn(sch))

        # the race: three signals leave Aurora together; 1 ms of real time = 1.6 s on screen
        fiber_route = self.route_variant(0.42, 2.3, C.FIBER, phase=0.6)
        spread_ms = FACTS["spread_rtt_ms"] / 2
        clock_t = ValueTracker(0.0)
        clock = always_redraw(lambda: VGroup(
            label(r"elapsed:", font_size=30, color=GREY_A),
            MathTex(rf"{clock_t.get_value():.3f}\ \text{{ms}}", font_size=40, color=C.LATENCY),
        ).arrange(RIGHT, buff=0.2).to_corner(UL, buff=0.4))
        legend = VGroup(
            VGroup(Dot(color=C.MICROWAVE), label(rf"microwave, {mw_ms:.2f} ms", font_size=24, color=C.MICROWAVE)),
            VGroup(Dot(color=C.LIGHT), label(rf"straight fiber, {fib_ms:.2f} ms", font_size=24, color=C.LIGHT)),
            VGroup(Dot(color=C.FIBER), label(rf"a real fiber route, $\approx${spread_ms:.1f} ms", font_size=24,
                                             color=C.FIBER)),
        )
        for row in legend:
            row.arrange(RIGHT, buff=0.15)
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.4)
        legend.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.1)
        slow = 1.6
        p_mw, p_st, p_fi = (Dot(radius=0.1, color=c) for c in (C.MICROWAVE, C.LIGHT, C.FIBER))
        for p in (p_mw, p_st, p_fi):
            p.move_to(m.site("aurora"))
        straight = self.gc.copy().set_stroke(C.LIGHT, 2.5, opacity=0.5)
        with self.voiceover(
            "<bookmark mark='race'/> Let's race them, slowed down about sixteen hundred times. The same news leaves "
            "Aurora at the same instant. <bookmark mark='a1'/> The microwave signal arrives first. <bookmark "
            "mark='a2'/> A perfectly straight fiber would arrive 1.8 milliseconds later, <bookmark mark='a3'/> and a "
            "real fiber route later still. In a market where races are decided by microseconds, that is an eternity. "
            "Microwave links carry very little data, and heavy rain can knock them out, so firms keep fiber as a "
            "backup and send only the most valuable bits through the air."
        ) as vo:
            vo.wait_until("race")
            self.play(FadeOut(self.vac), FadeOut(self.glass), FadeOut(mw_tag), FadeOut(sch), FadeIn(clock),
                      FadeIn(legend), Create(fiber_route), FadeIn(straight), run_time=1.2)
            self.add(p_mw, p_st, p_fi)
            T = spread_ms * slow
            # each dot moves at constant speed along its own route, arriving at its own time
            def mover(dot, route, arrive):
                def upd(d, dt):
                    s = min(clock_t.get_value() / arrive, 1.0)
                    d.move_to(route.point_from_proportion(s))
                return upd
            p_mw.add_updater(mover(p_mw, mw_route, mw_ms))
            p_st.add_updater(mover(p_st, straight, fib_ms))
            p_fi.add_updater(mover(p_fi, fiber_route, spread_ms))
            self.play(clock_t.animate.set_value(mw_ms), run_time=mw_ms * slow, rate_func=linear)
            flash1 = Flash(m.site("carteret"), color=C.MICROWAVE, line_length=0.3, num_lines=10)
            self.play(flash1, clock_t.animate.set_value(mw_ms + 0.25), run_time=0.25 * slow, rate_func=linear)
            self.play(clock_t.animate.set_value(fib_ms), run_time=(fib_ms - mw_ms - 0.25) * slow, rate_func=linear)
            self.play(Flash(m.site("carteret"), color=C.LIGHT, line_length=0.3, num_lines=10),
                      clock_t.animate.set_value(fib_ms + 0.25), run_time=0.25 * slow, rate_func=linear)
            self.play(clock_t.animate.set_value(spread_ms), run_time=(spread_ms - fib_ms - 0.25) * slow, rate_func=linear)
            self.play(Flash(m.site("carteret"), color=C.FIBER, line_length=0.3, num_lines=10))
            for p in (p_mw, p_st, p_fi):
                p.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def colocation(self):
        # a data hall: the exchange's cage on the left, customer racks at different distances, equal cable
        cage = RoundedRectangle(width=2.4, height=3.6, corner_radius=0.1, stroke_color=C.TRADE, stroke_width=3,
                                fill_color=C.TRADE, fill_opacity=0.08).move_to(LEFT * 4.8 + DOWN * 0.3)
        engine = server_box("matching\\\\engine", color=C.TRADE, width=1.8, height=1.5, font_size=22).move_to(cage)
        cage_l = label(r"the exchange's cage", font_size=24, color=C.TRADE).next_to(cage, UP, buff=0.15)
        racks = VGroup(*[server_box(color=GREY_B, width=1.1, height=0.75) for _ in range(4)])
        xs = [-1.2, 0.8, 2.8, 4.8]
        for rk, x, y in zip(racks, xs, [1.6, 0.5, -0.6, -1.7]):
            rk.move_to([x, y, 0])
        rack_l = label(r"trading firms' servers, a few meters away", font_size=24, color=GREY_A).to_edge(UP, buff=0.5)
        cables = VGroup()
        coils = VGroup()
        port = cage.get_right()
        for i, rk in enumerate(racks):
            a = port + UP * (0.9 - 0.6 * i)
            b = rk.get_left()
            loops = 3 - i  # the nearest rack gets the most slack
            mid = (a + b) / 2
            path = VMobject()
            pts = [a, a + RIGHT * 0.3]
            if loops > 0:
                c = a + RIGHT * 0.9
                for k in range(24 * loops + 1):
                    ang = k / 24 * TAU
                    pts.append(c + 0.22 * np.array([np.sin(ang), -np.cos(ang) + 1, 0]) + RIGHT * 0.04 * k / 24)
                pass
            pts += [b + LEFT * 0.3, b]
            path.set_points_smoothly(pts)
            path.set_stroke(C.FIBER, 2.5)
            cables.add(path)
        equal = VGroup(
            label(r"every customer gets the same length of fiber", font_size=30, color=C.FIBER),
            label(r"1 meter of fiber $\approx$ 4.9 ns", font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.45)
        tag = note(r"schematic").to_corner(UR, buff=0.3)
        with self.voiceover(
            "The same logic plays out at the scale of meters. <bookmark mark='c'/> Exchanges rent space inside their own "
            "data centers, so trading servers can sit a few meters from the matching engine. That's called "
            "colocation. <bookmark mark='e'/> To keep it fair, exchanges give every colocated customer the same length "
            "of cable: one meter of fiber costs about five nanoseconds, so the customers closest to the exchange get "
            "extra fiber, coiled up. <bookmark mark='f'/> And yes, firms argue about this. In a 2024 letter to the "
            "SEC, a group of trading firms pressed Nasdaq to equalize latency across its whole Carteret campus, in a "
            "dispute where Nasdaq itself put one of the differences at 50 to 200 nanoseconds."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeIn(cage), FadeIn(engine), FadeIn(cage_l), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in racks], lag_ratio=0.15), FadeIn(rack_l))
            vo.wait_until("e")
            self.play(LaggedStart(*[Create(c) for c in cables], lag_ratio=0.2), run_time=2.5)
            coil_l = label(r"nearer racks: extra fiber, coiled up", font_size=22, color=C.FIBER).next_to(
                cage, DOWN, buff=0.2).align_to(cage, LEFT)
            self.play(FadeIn(coil_l), FadeIn(equal))
            vo.wait_until("f")
            pulses = VGroup(*[Dot(radius=0.07, color=C.LIGHT).move_to(c.get_start()) for c in cables])
            self.add(pulses)
            self.play(*[MoveAlongPath(p, c, rate_func=linear) for p, c in zip(pulses, cables)], run_time=2.2)
            self.play(*[Flash(r, color=C.LIGHT, line_length=0.15) for r in racks], FadeOut(pulses))
        self.clear_scene()
