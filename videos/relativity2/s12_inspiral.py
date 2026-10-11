from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity2.common import (boxed, clamp_x, label, ladder, load, mtex, note, polyline, redraw, sci, under)

WAVE, MAT = C.WAVE, C.MATTER


class Inspiral(VoiceoverScene):
    def construct(self):
        self.d = load("inspiral")
        self.balance()
        self.chirp()
        self.animate_inspiral()
        self.pulsar()
        self.pulsar_numbers()

    # ------------------------------------------------------------------
    def balance(self):
        rows = [
            mtex(r"E", r"=", r"-\frac{\mu M}{2a}", font_size=42),
            mtex(r"\frac{dE}{dt}", r"=", r"-L = -\frac{32}{5}\frac{\mu^2M^3}{a^5}", font_size=42),
            mtex(r"\frac{da}{dt}", r"=", r"-\frac{64}{5}\,\frac{\mu M^2}{a^3}", font_size=42),
            mtex(r"T_{\rm merge}", r"=", r"\frac{5}{256}\,\frac{a_0^4}{\mu M^2}", font_size=42),
        ]
        whys = [
            note(r"a circular orbit's energy (Newtonian: we're far from merger)"),
            note(r"the waves carry it away"),
            note(r"so the orbit shrinks (checked symbolically)"),
            note(r"integrate $a^3\,da$: the time to reach $a = 0$ (Peters, 1964)"),
        ]
        rows[0][0].set_color(MAT)
        rows[1][2].set_color(WAVE)
        rows[3][0].set_color(WAVE)
        under(rows, whys, -0.8)
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.8, buff=0.62)
        with self.voiceover(
            "The energy radiated has to come from somewhere: the orbit. <bookmark mark='a'/> The orbital energy of the "
            "pair is minus mu M over two a. <bookmark mark='b'/> It decreases at the rate the waves carry energy "
            "away. <bookmark mark='c'/> Solve for the separation: the orbit shrinks, slowly at first, and faster and "
            "faster as a gets smaller. <bookmark mark='d'/> Integrating, two bodies starting a distance a naught apart "
            "merge after five two-hundred-fifty-sixths of a naught to the fourth, over mu M squared. That fourth power "
            "is brutal: halve the distance, and the time to merge drops sixteen-fold."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chirp(self):
        rows = [
            mtex(r"f_{\rm GW}", r"=", r"\frac{\omega}{\pi} = \frac{1}{\pi}\sqrt{\frac{M}{a^3}}", font_size=40),
            mtex(r"\frac{df}{dt}", r"=", r"\frac{96}{5}\,\pi^{8/3}\,\mathcal{M}^{5/3}\,f^{11/3},\qquad \mathcal{M} \equiv \mu^{3/5}M^{2/5}",
                 font_size=40),
            mtex(r"f(\tau)", r"=", r"\frac{1}{\pi}\Big(\frac{5}{256\,\tau}\Big)^{3/8}\mathcal{M}^{-5/8}", font_size=44),
        ]
        whys = [
            note(r"twice the orbital frequency (Kepler)"),
            note(r"differentiate, use $da/dt$, eliminate $a$: \ only one combination of the masses survives, the chirp mass"),
            note(r"integrate, with $\tau = t_c - t$ the time left before coalescence (checked symbolically)"),
        ]
        rows[0][0].set_color(WAVE)
        rows[2][0].set_color(WAVE)
        under(rows, whys, -0.8)
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.8, buff=0.75)
        p1 = label(r"Part 1 quoted this formula to match LIGO's data. \ Now it's derived.", font_size=28, color=WAVE)
        p1.to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "What a detector hears is the frequency. <bookmark mark='a'/> The gravitational-wave frequency is twice the "
            "orbital frequency, which Kepler's law ties to the separation. <bookmark mark='b'/> Differentiate it, "
            "substitute the shrinking rate, and eliminate a. Something remarkable happens: the two masses only appear "
            "in one combination, mu to the three fifths times M to the two fifths, called the chirp mass. "
            "<bookmark mark='c'/> Integrating gives the frequency as a function of the time left before coalescence. "
            "It rises without limit, a chirp. <bookmark mark='d'/> This is exactly the formula part one quoted, and "
            "laid over LIGO's data. Now we've derived it, five over two hundred fifty-six and all."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(p1))
        self.clear_scene()

    # ------------------------------------------------------------------
    def animate_inspiral(self):
        d = self.d
        tau, f, phase, amp, sep = d["tau"], d["f"], d["phase"], d["amp"], d["sep_km"]
        m1, m2 = float(d["m1"]), float(d["m2"])
        assert abs(f[0] - 32.1) < 0.2 and abs(f[-1] - 180.5) < 0.5 and abs(sep[0] - 980) < 2 and abs(sep[-1] - 310) < 2
        t = -tau  # seconds, coalescence at 0
        cen = np.array([-4.3, 0.6, 0])
        sc = 2.0 / sep[0]
        k = ValueTracker(0.0)
        n = len(t)

        def binary():
            j = int(k.get_value() * (n - 1))
            orb = phase[j] / 2
            u = np.array([math.cos(orb), math.sin(orb), 0])
            a = sep[j] * sc
            g = VGroup(Circle(radius=a * m2 / (m1 + m2), color=GREY_D, stroke_width=1).move_to(cen),
                       Circle(radius=a * m1 / (m1 + m2), color=GREY_D, stroke_width=1).move_to(cen))
            g.add(Dot(cen + a * m2 / (m1 + m2) * u, radius=0.16, color=MAT), Dot(cen - a * m1 / (m1 + m2) * u, radius=0.15, color=MAT))
            return g

        B = redraw(binary)
        ax = Axes(x_range=[-0.2, 0, 0.05], y_range=[-1.2, 1.2, 1], x_length=8.2, y_length=2.4, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to([2.4, 1.3, 0])
        h = amp / amp.max() * np.cos(phase)

        def wave():
            j = max(2, int(k.get_value() * (n - 1)))
            return polyline(ax, t[:j], h[:j], color=WAVE, stroke_width=2.5)

        Wv = redraw(wave)
        ax2 = Axes(x_range=[-0.2, 0, 0.05], y_range=[0, 200, 50], x_length=8.2, y_length=2.4, tips=False,
                   axis_config={"stroke_color": GREY_B, "font_size": 20},
                   y_axis_config={"numbers_to_include": [50, 100, 150, 200]}).move_to([2.4, -1.85, 0])
        ff = polyline(ax2, t, f, color=WAVE, stroke_width=3)
        dot2 = redraw(lambda: Dot(ax2.c2p(t[int(k.get_value() * (n - 1))], f[int(k.get_value() * (n - 1))]),
                                  radius=0.07, color=WHITE))
        l1 = label(r"$h(t)$, leading order", font_size=22, color=WAVE).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        l2 = label(r"$f_{\rm GW}$ (Hz) vs time before coalescence (s)", font_size=22).next_to(ax2, UP, buff=0.05).align_to(ax2, LEFT)
        sep_rd = redraw(lambda: label(rf"separation: {sep[int(k.get_value() * (n - 1))]:.0f} km", font_size=24)
                        .move_to(cen + DOWN * 2.6))
        cap = note(r"computed: $36 + 31\,M_\odot$ (GW150914's masses, as seen at Earth), from $32$ to $180$ Hz; the formula fails "
                   r"near merger").to_edge(DOWN, buff=0.15)
        clamp_x(cap)
        with self.voiceover(
            "<bookmark mark='a'/> Here it is for two black holes with the masses of LIGO's first detection. Two tenths "
            "of a second before they merge, they're a thousand kilometers apart and the wave is at thirty hertz. "
            "<bookmark mark='b'/> As they spiral together, the frequency and the amplitude both climb, faster and "
            "faster: the chirp. In the last instants, a few hundred kilometers apart, our leading-order formula breaks "
            "down, and only a full numerical solution of Einstein's equation can follow the merger itself."
        ) as vo:
            vo.wait_until("a")
            self.add(B, sep_rd)
            self.play(Create(ax), Create(ax2), FadeIn(l1), FadeIn(l2), FadeIn(cap))
            self.add(Wv, dot2)
            self.play(Create(ff), run_time=1)
            vo.wait_until("b")
            self.play(k.animate.set_value(1.0), run_time=max(vo.remaining() - 0.5, 4), rate_func=lambda x: x)
        for m in (B, Wv, dot2, sep_rd):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def pulsar(self):
        d = self.d
        fe, Pdot = float(d["ht_fe"]), float(d["ht_Pdot"])
        assert abs(fe - 11.857) < 0.001 and abs(Pdot / 1e-12 + 2.4021) < 0.001
        hdr = VGroup(label(r"PSR B1913+16: the Hulse--Taylor binary pulsar", font_size=36),
                     label(r"found at Arecibo, 1974; Nobel Prize 1993", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.12)
        hdr.to_edge(UP, buff=0.35)
        facts = VGroup(
            label(r"two neutron stars, $1.438$ and $1.390\,M_\odot$", font_size=28, color=MAT),
            label(r"orbit: 7.75 hours, eccentricity $e = 0.617$", font_size=28),
            label(r"one is a pulsar: a clock ticking 17 times a second", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-3.2, 0.6, 0])
        eqs = VGroup(
            mtex(r"\dot P_b", r"=", r"-\frac{192\pi}{5}\Big(\frac{2\pi}{P_b}\Big)^{5/3}\frac{m_1m_2}{M^{1/3}}\,f(e)", font_size=36),
            mtex(r"f(e) = \frac{1 + \tfrac{73}{24}e^2 + \tfrac{37}{96}e^4}{(1 - e^2)^{7/2}} = 11.86", font_size=34),
            label(r"(Peters \& Mathews 1963: eccentric orbits radiate much more, mostly at closest approach)",
                  font_size=22, color=GREY_A),
            mtex(r"\dot P_b^{\rm GR} = " + sci(Pdot, 4).replace("{-}", "-"), font_size=40, color=WAVE),
        ).arrange(DOWN, buff=0.22).move_to([2.9, 0.2, 0])
        eqs[0][0].set_color(WAVE)
        with self.voiceover(
            "The first evidence that gravitational waves carry energy came from a pair of neutron stars. "
            "<bookmark mark='a'/> In 1974, Russell Hulse and Joseph Taylor found a pulsar in a binary orbit: two neutron "
            "stars, each about one point four solar masses, orbiting every seven and three quarter hours, one of them a "
            "spinning beacon that ticks seventeen times a second, a superb clock. <bookmark mark='b'/> The orbit is "
            "eccentric, so the quadrupole formula needs a correction, worked out by Peters and Mathews: it radiates "
            "almost twelve times more than a circular orbit would. <bookmark mark='c'/> The prediction: the orbital "
            "period should shrink by two point four trillionths of a second, every second."
        ) as vo:
            self.play(FadeIn(hdr))
            vo.wait_until("a")
            self.play(FadeIn(facts, lag_ratio=0.3), run_time=2)
            vo.wait_until("b")
            self.play(Write(eqs[0]), FadeIn(eqs[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[3]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def pulsar_numbers(self):
        d = self.d
        years, shift = d["ht_years"], d["ht_shift"]
        merge, wdot = float(d["ht_merge"]), float(d["ht_wdot"])
        assert abs(merge - 301) < 2 and abs(wdot - 4.2266) < 0.001
        ax = Axes(x_range=[1974, 2026, 10], y_range=[-120, 0, 20], x_length=6.2, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_B, "font_size": 20},
                  x_axis_config={"numbers_to_include": [1980, 1990, 2000, 2010, 2020], "decimal_number_config": {"group_with_commas": False, "num_decimal_places": 0}},
                  y_axis_config={"numbers_to_include": [-100, -80, -60, -40, -20]}).move_to([-3.1, -0.8, 0])
        cur = polyline(ax, 1974 + years, shift, color=WAVE, stroke_width=4)
        yl = label(r"shift of periastron time (s)", font_size=22).next_to(ax, UP, buff=0.12)
        cl = note(r"curve: GR's prediction, $\tfrac12(\dot P_b/P_b)\,t^2$, computed").next_to(ax, DOWN, buff=0.45)
        res = VGroup(
            label(r"measured, corrected for the Galaxy's pull:", font_size=26),
            mtex(r"\frac{\dot P_b^{\rm obs}}{\dot P_b^{\rm GR}} = 0.9983 \pm 0.0016", font_size=38, color=WAVE),
            label(r"(Weisberg \& Huang 2016, 35 years of timing)", font_size=22, color=GREY_A),
            label(r"periastron advance: $4.2266^\circ$/yr (Mercury: $43''$/century)", font_size=24),
            label(r"the Double Pulsar (Kramer et al.\ 2021): $0.999963 \pm 0.000063$", font_size=24, color=WAVE),
            label(rf"time until the two stars merge: \ {merge:.0f} million years", font_size=26, color=MAT),
        ).arrange(DOWN, buff=0.22).move_to([3.4, -0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A shrinking period shows up as a drift in the time of closest approach, growing like "
            "the square of the elapsed time. Here's general relativity's prediction since 1974: by now, more than a "
            "hundred seconds. <bookmark mark='b'/> The measured decay, after correcting for the acceleration of the "
            "pulsar in our galaxy, agrees with the prediction to two parts in a thousand. "
            "<bookmark mark='c'/> The orbit's ellipse also turns, by four degrees a year: Mercury's effect, in a far "
            "stronger field. And a second system, the Double Pulsar, now agrees with the quadrupole formula to a few "
            "parts in a hundred thousand. <bookmark mark='d'/> In about three hundred million years, these two stars "
            "will merge, ending with a chirp like the ones LIGO hears."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(yl), FadeIn(cl))
            self.play(Create(cur), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(res[:3], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(res[3:5], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(res[5]))
        self.clear_scene()
