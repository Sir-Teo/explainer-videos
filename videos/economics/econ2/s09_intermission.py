from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ2.common import *  # noqa: F403

LO, HI = np.log10(0.18), np.log10(16.0)


def month_x(m: str) -> float:
    return int(m[:4]) + (int(m[5:7]) - 0.5) / 12


class Intermission(SoundScene):
    """Sixty-six years in thirty-four seconds, without narration: the real prices of eight commodities, month by
    month, each starting at one in 1960, under the real price of Arabica coffee played as a tune; then the story so
    far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ2").load("intermission.melody")
        months = film["months"]
        xs = np.array([month_x(m) for m in months])
        x0, x1 = -5.6, 4.3
        y0, y1 = -2.6, 2.2

        def X(x):
            return x0 + (x1 - x0) * (x - 1960) / (2026.9 - 1960)

        def Y(v):
            return y0 + (y1 - y0) * (np.log10(v) - LO) / (HI - LO)

        frame = VGroup()
        for v in (0.25, 0.5, 1, 2, 5, 10):
            y = Y(v)
            frame.add(Line([x0, y, 0], [x1, y, 0], color=GREY_D, stroke_width=1 if v != 1 else 2,
                           stroke_opacity=0.6 if v != 1 else 1))
            frame.add(MathTex(rf"\times {v:g}", font_size=20, color=GREY_B if v != 1 else WHITE).next_to([x0, y, 0], LEFT,
                                                                                                    buff=0.15))
        for yr in range(1960, 2030, 10):
            frame.add(MathTex(str(yr), font_size=20, color=GREY_B).move_to([X(yr), y0 - 0.3, 0]))
        axis_name = label(r"real price, \ each commodity's 1960 price $= 1$, \ log scale", font_size=20,
                          color=GREY_A).move_to([(x0 + x1) / 2, y0 - 0.75, 0])
        legend = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.32, color=FILM_COLOR[k], stroke_width=5),
                                 label(FILM_NAME[k], font_size=19, color=FILM_COLOR[k])).arrange(RIGHT, buff=0.1)
                          for k in FILM]).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.35)
        if legend.width > 13.2:
            legend.width = 13.2
        series = {k: np.array(film[k]) for k in FILM}
        lines = VGroup(*[VMobject(stroke_color=FILM_COLOR[k], stroke_width=2.6) for k in FILM])
        tips = VGroup(*[Dot(radius=0.055, color=FILM_COLOR[k]) for k in FILM])
        year_t = Integer(1960, font_size=80, color=GREY_C, group_with_commas=False).move_to([5.75, 1.7, 0])
        year_t.set_z_index(-2)
        events = [("1974-02", r"the oil embargo; \ sugar at eleven times its 1960 price", 4.2),
                  ("1977-04", r"the black frost: \ coffee and cocoa", 3.2),
                  ("1998-06", r"two decades of falling prices", 0.36),
                  ("2008-07", r"oil at eleven times 1960", 9.0),
                  ("2026-02", r"gold at thirteen times", 13.5)]
        # one caption above the chart, changed at each event, and a faint tick where the event falls
        ev_mobs = VGroup()
        ticks = VGroup()
        for m, text, at in events:
            t = label(rf"{m[:4]}: \ {text}", font_size=24, color=WHITE).move_to([(x0 + x1) / 2, y1 + 0.42, 0])
            t.set_opacity(0)
            ev_mobs.add(t)
            ticks.add(DashedLine([X(month_x(m)), y0, 0], [X(month_x(m)), y1, 0], color=GREY_B, stroke_width=1.2,
                                 stroke_opacity=0.0))
        tag = data_tag(r"World Bank Pink Sheet (Nov 2026), deflated by the US consumer price index (BLS via FRED)",
                       corner=DL, font_size=15)
        stag = note(r"sound: the real price of Arabica coffee, \ as a tune (computed)", font_size=15, color=E.ACCENT)
        stag.to_corner(DR, buff=0.3)
        t_end = film_time(months[-1])

        def idx_at(t):
            return int(np.clip(np.floor((t - film_time(months[0])) / (t_end - film_time(months[0])) * (len(months) - 1)),
                               0, len(months) - 1))

        def draw(m, t):
            i = max(idx_at(t), 1)
            for line, tip, k in zip(m, tips, FILM):
                v = series[k][: i + 1]
                ok = np.isfinite(v)
                pts = [np.array([X(x), Y(max(y, 0.19)), 0]) for x, y in zip(xs[: i + 1][ok], v[ok])]
                if len(pts) >= 2:
                    line.set_points_as_corners(pts)
                    tip.move_to(pts[-1])

        def counter(m, t):
            m.set_value(int(months[idx_at(t)][:4]))

        def show_events(m, t):
            i = idx_at(t)
            reached = [k for k, (mon, _, _) in enumerate(events) if i >= months.index(mon)]
            last = reached[-1] if reached else -1
            for k, ev in enumerate(m):
                ev.set_opacity(1.0 if k == last else 0.0)

        def show_ticks(m, t):
            i = idx_at(t)
            for (mon, _, _), tk in zip(events, m):
                tk.set_stroke(opacity=0.45 if i >= months.index(mon) else 0.0)

        with self.listen(clip) as snd:
            snd.caption(r"real prices of eight commodities, 1960 to 2026, \ under the price of coffee as a tune")
            snd.show(tag, stag)
            snd.drive(lines, draw)
            snd.drive(year_t, counter)
            snd.drive(ev_mobs, show_events)
            snd.drive(ticks, show_ticks)
            snd.show(ticks, lines, tips, year_t, ev_mobs, frame, axis_name, legend)
            self.play(LaggedStart(*[Create(m) if isinstance(m, Line) else FadeIn(m) for m in frame], lag_ratio=0.03),
                      FadeIn(axis_name), FadeIn(legend), run_time=1.4)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (frame, axis_name, tag, lines, tips, ev_mobs, ticks, stag, legend)],
                      year_t.animate.set_opacity(0.0), run_time=1.0)
            story = point_cards([
                (r"the margin", r"a price is the value of the last unit, \ not of the whole", WATER),
                (r"two blades", r"demand from buyers' values, \ supply from sellers' costs", E.ACCENT),
                (r"the marginal pair", r"four cards fix the band; \ the rest could change", E.DEMAND),
                (r"zero is not enough", r"the rules give the efficiency, \ learning gives the price", E.AGORA),
                (r"elasticity", r"small at first, \ larger given time", E.SUPPLY),
                (r"shifts", r"a frost moved supply, \ and coffee slid along demand", COFFEE),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            nxt = label(r"next: \ surplus, \ who pays a tax, \ and what a price control costs", font_size=22,
                        color=GREY_B).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 1.6))
            self.play(FadeIn(nxt))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
