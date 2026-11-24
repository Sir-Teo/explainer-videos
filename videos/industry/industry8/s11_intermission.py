from __future__ import annotations

from videos.industry.industry8.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.film()
        self.story()

    def film(self):
        L = R["long"]
        ms, real = L["months"], L["real"]
        pts = [(mx(m), v) for m, v in zip(ms, real) if v is not None]
        xs = [p[0] for p in pts]
        pa = viz.plot_axes([1946, 2027], [0, 220], x_length=11.6, y_length=5.0,
                           xticks=[1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020], yticks=[50, 100, 150, 200],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}", size=14)
        pa.move_to([0, -0.4, 0])
        t = ValueTracker(xs[0])

        def line():
            x = t.get_value()
            q = [pa.ax.c2p(a, b) for a, b in pts if a <= x]
            return VMobject(stroke_color=PRICE, stroke_width=3).set_points_as_corners(q) if len(q) > 1 else VMobject()
        ln = always_redraw(line)
        yr = draw.number(lambda: t.get_value(), 0, commas=False, size=36, color=GREY_A)
        yr.add_updater(lambda m: m.to_corner(UR, buff=0.5))
        head = tx(f"A barrel of WTI in dollars of {mlabel(L['cpi_month'])}, month by month", 22, WHITE, bold=True).to_edge(
            UP, buff=0.35)
        d = {round(a, 3): b for a, b in pts}
        eps = []
        for x, name in L["episodes"]:
            near = min(pts, key=lambda p: abs(p[0] - x))
            eps.append((near[0], max(b for a, b in pts if abs(a - x) < 0.6), name))
        marks = VGroup()
        for k, (x, y, name) in enumerate(eps):
            p = pa.ax.c2p(x, y)
            lab = tx(name, 14, WHITE).next_to(p, UP, buff=0.12 + 0.28 * (k % 2))
            marks.add(VGroup(Dot(p, radius=0.05, color=WHITE), lab))
        del d
        src = source("WTI (FRED, WTISPLC; EIA since 1986) deflated by the US consumer price index (BLS)", size=13)
        with self.voiceover(
            "An intermission: eighty years of a barrel of American crude, in today's dollars. "
            "<bookmark mark='a'/> For a quarter of a century after the war, it barely moved, at around twenty-five "
            "to thirty of today's dollars. <bookmark mark='b'/> Then the embargo of 1973, and the revolution in Iran "
            "in 1979. <bookmark mark='c'/> The long fall of the 1980s, when Saudi Arabia gave up holding the price "
            "up. <bookmark mark='d'/> The climb to 2008, when a barrel cost more than two hundred of today's dollars, "
            "and the crash after it. <bookmark mark='e'/> The shale glut of 2014, the lockdowns of 2020, Ukraine in "
            "2022, and now the Strait of Hormuz. Look at the shape rather than the dates: long calm stretches, and "
            "then cliffs, in both directions."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(head))
            self.add(ln, yr)
            prev = 0.0
            for m, x1 in zip("abcde", (1972.5, 1981.0, 1999.0, 2009.5, 2026.8)):
                vo.wait_until(m)
                new = [marks[i] for i in range(len(marks)) if prev < eps[i][0] <= x1]
                self.play(t.animate.set_value(x1), run_time=3.5, rate_func=linear)
                if new:
                    self.play(*[FadeIn(g, shift=DOWN * 0.1) for g in new], run_time=0.6)
                prev = x1
        for m in (ln, yr):
            m.clear_updaters()
        self.clear_scene()

    def story(self):
        head = tx("The story so far", 36, GOLD, bold=True).to_edge(UP, buff=0.6)
        lines = ["Oil forms in source rock and gathers in traps; shale is drilled in the source rock itself.",
                 "Every well fades, shale wells fastest: a shale basin must keep drilling to stand still.",
                 "Reserves are a forecast at a price, not a quantity of rock.",
                 "A barrel costs $3.51 to lift in Saudi Arabia, $66 to drill anew in Texas; the last barrel sets the price.",
                 "The owner of the rock, usually a state, keeps most of the difference.",
                 "Neither buyers nor sellers can move fast, so small shortages make huge price swings.",
                 "Next: the cartel, shale, refining, gas, and the companies that do the drilling."]
        pics = [VGroup(Rectangle(width=0.6, height=0.2, stroke_width=0, fill_color="#2A2520", fill_opacity=1),
                       Rectangle(width=0.6, height=0.2, stroke_width=0, fill_color="#B79A6A", fill_opacity=1)).arrange(UP, buff=0),
                draw.derrick(0.6, color=SHALE), draw.barrel(0.5), draw.pumpjack(0.8), draw.coin_stack(3, r=0.15),
                VGroup(Line(LEFT * 0.2 + DOWN * 0.25, RIGHT * 0.05 + UP * 0.25), Line(LEFT * 0.05 + UP * 0.25,
                                                                                     RIGHT * 0.2 + DOWN * 0.25)).set_stroke(PRICE, 3),
                draw.tanker(0.9)]
        rows = VGroup()
        for k, (pic, ln) in enumerate(zip(pics, lines)):
            pic.scale_to_fit_height(min(max(pic.height, 0.35), 0.55))
            if pic.width > 0.9:
                pic.scale_to_fit_width(0.9)
            rows.add(VGroup(pic, tx(ln, 19 if k < 6 else 18, WHITE if k < 6 else GREY_B)))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.5)
        for r_ in rows:
            r_[0].move_to([rows.get_left()[0] + 0.5, r_.get_y(), 0])
            r_[1].next_to(r_[0], RIGHT, buff=0.35).align_to(rows[0][1], LEFT)
        if rows.width > 13.4:
            rows.scale_to_fit_width(13.4)
        rows.set_x(0)
        with self.voiceover(
            "The story so far. <bookmark mark='a'/> Oil forms in a source rock and gathers in traps; shale wells are "
            "drilled into the source rock itself. <bookmark mark='b'/> Every well fades, shale wells fastest, so a "
            "shale basin must keep drilling just to stand still. <bookmark mark='c'/> Reserves are a forecast at a "
            "price. <bookmark mark='d'/> A barrel costs a few dollars to lift in Saudi Arabia and sixty-six to drill "
            "anew in Texas, and the last barrel the world needs sets the price. <bookmark mark='e'/> The owner of the "
            "rock, usually a state, keeps most of the difference. <bookmark mark='f'/> And since neither buyers nor "
            "sellers can move fast, small shortages make huge swings. <bookmark mark='g'/> Next: the cartel that tried "
            "to tame those swings, the shale drillers who undid it, and the businesses between the well and the pump."
        ) as vo:
            self.play(FadeIn(head))
            for k, m in enumerate("abcdefg"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k][0], scale=0.6), FadeIn(rows[k][1], shift=RIGHT * 0.15), run_time=0.9)
        self.clear_scene()
