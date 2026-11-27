from __future__ import annotations

from videos.industry.industry14.common import *  # noqa: F403

ORDER = ["SEHG01", "SEHG02", "SEHF02", "SEHA", "SEHF01"]
LABEL = {"SEHG01": "water and sewerage", "SEHG02": "rubbish collection", "SEHF02": "piped gas", "SEHA": "rent",
         "SEHF01": "electricity"}


def interp(d, x):
    k = sorted(d)
    if x <= k[0]:
        return d[k[0]]
    for a, b in zip(k, k[1:]):
        if a <= x <= b:
            return d[a] + (d[b] - d[a]) * (x - a) / (b - a)
    return d[k[-1]]


class Intermission(VoiceoverScene):
    def construct(self):
        self.film()
        self.bill()

    def film(self):
        H = R["history"]
        real = H["real"]
        pa = viz.plot_axes([1953, 2026], [0.4, 4.0], x_length=10.6, y_length=4.8, xticks=[1955, 1965, 1975, 1985, 1995, 2005, 2015, 2025],
                           yticks=[0.5, 1, 2, 3, 4], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"x{v:g}",
                           ylabel="price after inflation (first year = 1)", size=14).move_to([-0.6, -0.4, 0])
        one = DashedLine(pa.ax.c2p(1953, 1), pa.ax.c2p(2026, 1), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        t = ValueTracker(1953)
        lines, tips = VGroup(), VGroup()
        for k in ORDER:
            S = real[k]
            ys = sorted(S)

            def mk(S=S, ys=ys, k=k):
                xs = [y for y in ys if y <= t.get_value()]
                if xs and xs[-1] < t.get_value():
                    xs = xs + [t.get_value()]
                q = [pa.ax.c2p(x, interp(S, x)) for x in xs]
                return VMobject(stroke_color=SERIES_COL[k], stroke_width=4).set_points_as_corners(q) if len(q) > 1 else VMobject()
            lines.add(always_redraw(mk))
        yr = draw.number(lambda: t.get_value(), 0, commas=False, size=36, color=GREY_A)
        yr.add_updater(lambda m: m.to_corner(UR, buff=0.5))
        yr.update()
        ends = VGroup(*[tx(f"{LABEL[k]}: x{real[k][2025]:.2f}", 15, SERIES_COL[k], bold=True).next_to(pa.ax.c2p(2025, real[k][2025]), RIGHT, buff=0.1)
                        for k in ORDER])
        ends[3].shift(UP * 0.12)
        ends[4].shift(DOWN * 0.12)
        head = tx("Seventy-two years of American bills, after inflation", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("BLS, consumer price indexes (US city average, annual averages), each divided by all items; "
                     "rubbish collection from 1984", size=13)
        with self.voiceover(
            "An intermission: seventy-two years of American household bills, each divided by prices in general, so "
            "that a flat line means the bill kept pace with everything else. <bookmark mark='a'/> Watch them "
            "together. <bookmark mark='b'/> Electricity ends about where it started, a little below. Rent barely moves. Piped gas rises and falls with the gas market. "
            f"<bookmark mark='c'/> Rubbish collection, since its index began in 1984, has doubled. <bookmark mark='d'/> And "
            f"water and sewerage has risen almost every year for seven decades: {real['SEHG01'][2025]:.1f} times as "
            "expensive, after inflation, as in 1953. Nothing else on this chart comes close."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(one), FadeIn(head), FadeIn(src))
            self.add(lines, yr)
            vo.wait_until("a")
            self.play(t.animate.set_value(2025), run_time=12.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(ends[4]), FadeIn(ends[3]), FadeIn(ends[2]))
            vo.wait_until("c")
            self.play(FadeIn(ends[1]), Indicate(ends[1], color=RECYCLE))
            vo.wait_until("d")
            self.play(FadeIn(ends[0]), Indicate(ends[0], color=WATER, scale_factor=1.15))
        yr.clear_updaters()
        self.clear_scene()

    def bill(self):
        H = R["history"]
        a = VGroup(tx("1953 to 2025", 24, WHITE, bold=True),
                   tx(f"all prices: x{H['all_x']:.1f}", 28, GREY_A, bold=True),
                   tx(f"water and sewerage: x{H['water_x']:.1f}", 34, WATER, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([1.8, 0.6, 0])
        sc = 4.0 / H["water_x"]
        b1 = Rectangle(width=1.0, height=H["all_x"] * sc, stroke_width=0, fill_color=GREY_B, fill_opacity=0.85).move_to([-4.6, -1.0, 0], aligned_edge=DOWN)
        b2 = Rectangle(width=1.0, height=H["water_x"] * sc, stroke_width=0, fill_color=WATER, fill_opacity=0.9).move_to([-3.2, -1.0, 0], aligned_edge=DOWN)
        bl = VGroup(tx("all prices", 13, GREY_A).next_to(b1, DOWN, buff=0.08), tx("water", 13, WATER).next_to(b2, DOWN, buff=0.08))
        why = VGroup(tx("the pipes, the sewage works and the rules they must meet", 18, GREY_A),
                     tx("are paid for in the bill, and they keep being replaced and raised", 18, GREY_A)).arrange(DOWN, buff=0.06).move_to([1.8, -1.8, 0])
        src = source("BLS, consumer price indexes: water and sewerage maintenance; all items (US city average, annual averages)", size=13)
        with self.voiceover(
            f"In plain numbers: since 1953, prices in general have risen about {H['all_x']:.0f} times. <bookmark mark='a'/> "
            f"The price of water and sewerage has risen about {H['water_x']:.0f} times. <bookmark mark='b'/> The reason, as "
            "the rest of this film argues: a bill built on pipes and works that keep being replaced, and standards that keep "
            "being raised. Back to the rubbish, and what happens to the part we try to recycle."
        ) as vo:
            self.play(FadeIn(a[0]), FadeIn(a[1]), FadeIn(src), GrowFromEdge(b1, DOWN), FadeIn(bl[0]))
            vo.wait_until("a")
            self.play(FadeIn(a[2], scale=1.2), GrowFromEdge(b2, DOWN), FadeIn(bl[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(why, shift=UP * 0.1))
        self.clear_scene()
