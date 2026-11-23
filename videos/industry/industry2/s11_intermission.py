from __future__ import annotations

from videos.industry.industry2.common import *  # noqa: F403

LINES = [("Manufacturing", "#F2A65A"), ("Finance, insurance and real estate", "#F2C14E"),
         ("Professional and business services", "#4FD1C5"), ("Government", "#8B95A7"),
         ("Health care and social assistance", "#7BD88F"), ("Information", "#B58CFF"),
         ("Farms, forestry, fishing", "#C8B79A")]


class Intermission(VoiceoverScene):
    def construct(self):
        H = R["history"]
        years = H["years"]
        pa = viz.plot_axes((1947, 2025), (0, 27), x_length=10.6, y_length=5.0, xticks=[1947, 1965, 1985, 2005, 2025],
                           yticks=[0, 5, 10, 15, 20, 25], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}%",
                           size=16, ylabel="share of GDP").shift(LEFT * 1.0 + DOWN * 0.3)
        tracker = ValueTracker(1947)
        curves = VGroup()
        for name, c in LINES:
            ys = H["series"][name]

            def make(ys=ys, c=c):
                end = tracker.get_value()
                pts = [pa.ax.c2p(y, v) for y, v in zip(years, ys) if y <= end and v is not None]
                m = VMobject(stroke_color=c, stroke_width=3.5)
                if len(pts) > 1:
                    m.set_points_as_corners(pts)
                else:
                    m.set_points_as_corners([pts[0], pts[0] + RIGHT * 0.001])
                return m
            curves.add(always_redraw(make))
        labels = VGroup()
        for name, c in LINES:
            v = H["series"][name][-1]
            short_n = {"Finance, insurance and real estate": "Finance and real estate",
                       "Professional and business services": "Business services",
                       "Health care and social assistance": "Health care", "Farms, forestry, fishing": "Farms"}.get(
                name, name)
            labels.add(T(f"{short_n} {v:.1f}%", 16, c).move_to(pa.ax.c2p(2025, v) + RIGHT * 1.45))
        # spread labels that would overlap
        ys_sorted = sorted(range(len(labels)), key=lambda i: labels[i].get_y())
        for a, b in zip(ys_sorted, ys_sorted[1:]):
            if labels[b].get_y() - labels[a].get_y() < 0.26:
                labels[b].set_y(labels[a].get_y() + 0.26)
        yr = TB("1947", 36, I.ACCENT).to_corner(UR, buff=0.5)
        head = T("Intermission: eighty years of the American economy", 24, I.DIM).to_edge(UP, buff=0.35)
        src = source("BEA, GDP by Industry: historical tables (1947-1997) and TVA110 (1998-2025)")
        yr.add_updater(lambda m: m.become(TB(f"{int(tracker.get_value())}", 36, I.ACCENT).to_corner(UR, buff=0.5)))
        with self.voiceover(
            "An intermission: eighty years of the American economy, by share of GDP. <bookmark mark='a'/> In 1947 "
            "manufacturing was a quarter of everything the country produced and farms were eight percent. Watch the "
            "lines cross. <bookmark mark='b'/> By 2025 manufacturing is under ten percent, farms under one, and "
            "finance and real estate, business services and health care have taken their place."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(src), FadeIn(yr))
            self.add(*curves)
            vo.wait_until("a")
            self.play(tracker.animate.set_value(2025), run_time=14, rate_func=linear)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.15))
        yr.clear_updaters()
        self.wait(1.0)
        self.clear_scene()
        so = VGroup(TB("The story so far", 34, I.ACCENT),
                    T("Measured by sales, the biggest businesses are shops, insurers and wholesalers.", 26, I.TEXT),
                    T("Measured by what each adds, real estate, government and manufacturing lead.", 26, I.TEXT),
                    T("Measured by jobs, government, health care and business services.", 26, I.TEXT),
                    T("Leontief's table shows how each industry feeds the others.", 26, I.TEXT),
                    T("Next: who buys, where a household's dollar ends up, and why the economy moved to services.", 22, I.DIM)
                    ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "The story so far. Measured by sales, the biggest businesses are shops, insurers and wholesalers. "
            "Measured by what each adds, real estate, government and manufacturing lead. Measured by jobs, "
            "government, health care and business services. And Leontief's table shows how they all feed one "
            "another. Next: who does the final buying, where a household's dollar ends up, and why the economy moved from factories to services."
        ):
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in so], lag_ratio=0.5), run_time=5)
        self.clear_scene()
