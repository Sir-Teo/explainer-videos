from __future__ import annotations

from videos.industry.industry6.common import *  # noqa: F403


def _x(month: str) -> float:
    return int(month[:4]) + (int(month[5:7]) - 0.5) / 12


class Intermission(VoiceoverScene):
    def construct(self):
        H, M, K, S = R["hogs"], R["micron"], R["maersk"], R["housing"]["series"]
        head = tx("Intermission: four cycles", 26, GREY_A).to_edge(UP, buff=0.35)
        # four small panels, each a different industry and a different century, all the same shape
        specs = [
            ("hogs, Chicago, 1885-1935", HOG, [(1885 + i / 12, v) for i, v in enumerate(H["dev_price"])][::3],
             draw.pig(0.7, color=HOG)),
            ("houses started, US, 2000-2026", ORDER, [(_x(k), v / 1000) for k, v in zip(S["HOUST"]["months"],
                                                                                    S["HOUST"]["values"])],
             draw.house(0.6, color=STONE)),
            ("Maersk's operating profit, 2019-2025", CAP, list(zip(K["years"], K["ebit"])), draw.ship(0.9)),
            ("Micron's sales a quarter, 2009-2025", "#B58CFF",
             [(int(q[:4]) + int(q[5:7]) / 12, v) for q, v in zip(M["quarters"], M["q_revenue"]) if q < "2025-09"],
             draw.chip(0.55)),
        ]
        panels = VGroup()
        for name, col, pts, pic in specs:
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            lo, hi = min(ys), max(ys)
            pad = 0.08 * (hi - lo)
            pa = viz.plot_axes([min(xs), max(xs)], [lo - pad, hi + pad], x_length=5.0, y_length=1.9, size=12,
                               grid=False)
            ln = VMobject(stroke_color=col, stroke_width=3).set_points_smoothly([pa.ax.c2p(x, y) for x, y in pts]) \
                if len(pts) < 40 else VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(
                    [pa.ax.c2p(x, y) for x, y in pts])
            t_ = tx(name, 16, col).next_to(pa, UP, buff=0.08).align_to(pa, LEFT)
            pic.scale_to_fit_height(0.5).next_to(t_, RIGHT, buff=0.25)
            panels.add(VGroup(pa, ln, t_, pic))
        panels.arrange_in_grid(rows=2, cols=2, buff=(1.1, 0.8)).move_to([0, -0.35, 0])
        src = source("NBER via FRED; Census via FRED; Maersk and Micron filings", size=13)
        with self.voiceover(
            "Four industries, a century apart, drawing the same shape. <bookmark mark='a'/> Hogs in Chicago before "
            "the Second World War. <bookmark mark='b'/> Houses across America in the 2000s. <bookmark mark='c'/> "
            "Container ships after the pandemic. <bookmark mark='d'/> And memory chips, cycle after cycle. Different "
            "products, different people, different centuries. The same wait between deciding and delivering, and the "
            "same habit of deciding by today's price."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                pa, ln, t_, pic = panels[k]
                self.play(FadeIn(pa), FadeIn(t_), FadeIn(pic, scale=0.7), run_time=0.6)
                self.play(Create(ln), run_time=2.2, rate_func=linear)
        self.clear_scene()
        self.story()

    def story(self):
        head = tx("The story so far", 36, GOLD, bold=True).to_edge(UP, buff=0.6)
        lines = ["When capacity takes years to build, and firms order by today's price, prices swing.",
                 "The longer the wait, the bigger the swings, even when demand grows smoothly.",
                 "Ships, chips and houses have all been round the loop in the last twenty years.",
                 "Everyone knows about the cycle: lumpy plants, hidden orders, eager lenders keep it going.",
                 "Next: what the swings do to the companies caught in them."]
        pics = [VGroup(draw.crane(0.6), Text("→", font_size=30, color=GREY_A), draw.ship(0.8)).arrange(RIGHT, buff=0.1),
                VGroup(*[draw.crane(0.4) for _ in range(3)]).arrange(RIGHT, buff=0.04),
                VGroup(draw.ship(0.5), draw.chip(0.35), draw.house(0.35, color=STONE)).arrange(RIGHT, buff=0.1),
                VGroup(Rectangle(width=0.5, height=0.4, stroke_width=0, fill_color="#2A3140", fill_opacity=1),
                       tx("?", 20, GREY_B, bold=True)),
                VGroup(draw.factory(0.6, color=GREY_B), Arrow(UP * 0.2, DOWN * 0.25, color=BUST, buff=0,
                                                             stroke_width=4)).arrange(RIGHT, buff=0.1)]
        rows = VGroup()
        for k, (pic, ln) in enumerate(zip(pics, lines)):
            pic.scale_to_fit_height(0.6)
            if pic.width > 1.4:
                pic.scale_to_fit_width(1.4)
            rows.add(VGroup(pic, tx(ln, 23 if k < 4 else 21, WHITE if k < 4 else GREY_B)))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(head, DOWN, buff=0.6)
        for r_ in rows:
            r_[0].move_to([rows.get_left()[0] + 0.7, r_.get_y(), 0])
            r_[1].next_to(r_[0], RIGHT, buff=0.4).align_to(rows[0][1], LEFT)
        if rows.width > 13.2:
            rows.scale_to_fit_width(13.2)
        rows.set_x(0)
        with self.voiceover(
            "The story so far. <bookmark mark='a'/> When capacity takes years to build, and firms order it by "
            "looking at today's price, prices swing. <bookmark mark='b'/> The longer the wait, the bigger the "
            "swings, even when demand grows smoothly. <bookmark mark='c'/> Ships, chips and houses have all been "
            "round the loop in the last twenty years. <bookmark mark='d'/> Everyone knows about the cycle, and it "
            "keeps turning anyway: plants come in lumps, orders are hidden, lenders lend at the top. "
            "<bookmark mark='e'/> Next: what the swings do to the companies caught in them."
        ) as vo:
            self.play(FadeIn(head))
            for k, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k][0], scale=0.6), FadeIn(rows[k][1], shift=RIGHT * 0.15), run_time=0.9)
        self.clear_scene()
