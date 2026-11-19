from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ3.common import *  # noqa: F403

U3 = "#F2B84B"


def month_x(m: str) -> float:
    return int(m[:4]) + (int(m[5:7]) - 0.5) / 12


class Intermission(SoundScene):
    """Seventy-eight years in thirty-six seconds, without narration: the US unemployment rate month by month since
    January 1948, under the same numbers played as a tune (a year a note, then a month a note from 2025); the last
    stretch magnified, where one month has no number and the tune rests; then the story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ3").load("intermission.melody")
        months = film["months"]
        u = np.array(film["u3"], float)
        times = np.array(film["times"])
        xs = np.array([month_x(m) for m in months])
        x0, x1 = -6.0, 3.0
        y0, y1 = -2.5, 2.2

        def X(x):
            return x0 + (x1 - x0) * (x - 1948) / (2027 - 1948)

        def Y(v):
            return y0 + (y1 - y0) * v / 16.0

        frame = VGroup()
        for v in (0, 4, 8, 12, 16):
            frame.add(Line([x0, Y(v), 0], [x1, Y(v), 0], color=GREY_D, stroke_width=1, stroke_opacity=0.6))
            frame.add(MathTex(f"{v}\\%", font_size=20, color=GREY_B).next_to([x0, Y(v), 0], LEFT, buff=0.15))
        for yr in range(1950, 2030, 10):
            frame.add(MathTex(str(yr), font_size=20, color=GREY_B).move_to([X(yr), y0 - 0.3, 0]))
        axis_name = label(r"US unemployment rate, \ monthly, \ seasonally adjusted", font_size=20, color=GREY_A)
        axis_name.move_to([(x0 + x1) / 2, y0 - 0.75, 0])
        # the magnifier: January 2025 to October 2026, a month a dot
        zm = [i for i, m in enumerate(months) if m >= "2025-01"]
        zx0, zx1 = 3.7, 6.7
        zy0, zy1 = -1.2, 1.6

        def ZX(i):
            return zx0 + (zx1 - zx0) * (i - zm[0]) / (len(zm) - 1)

        def ZY(v):
            return zy0 + (zy1 - zy0) * (v - 3.5) / 1.5

        zbox = RoundedRectangle(width=zx1 - zx0 + 0.6, height=zy1 - zy0 + 1.3, corner_radius=0.12, stroke_color=GREY_C,
                                stroke_width=1.5, fill_color=BACKGROUND, fill_opacity=0.9)
        zbox.move_to([(zx0 + zx1) / 2, (zy0 + zy1) / 2 + 0.1, 0])
        zhead = label(r"2025--26, \ a month a dot", font_size=19, color=GREY_A).next_to(zbox, UP, buff=0.1)
        zlabels = VGroup(*[MathTex(t, font_size=18, color=GREY_B).move_to([ZX(zm[k]), zy0 - 0.35, 0])
                           for k, t in ((0, "J"), (9, "O"), (12, "J"), (21, "O"))])
        zyl = VGroup(*[MathTex(f"{v:g}\\%", font_size=17, color=GREY_B).next_to([zx0, ZY(v), 0], LEFT, buff=0.08)
                       for v in (4.0, 4.5)])
        zdots = VGroup()
        for i in zm:
            if np.isfinite(u[i]):
                zdots.add(Dot([ZX(i), ZY(u[i]), 0], radius=0.06, color=U3).set_opacity(0))
            else:
                ring = Circle(radius=0.09, stroke_color=E.MISS, stroke_width=2.5).move_to([ZX(i), ZY(4.35), 0])
                zdots.add(ring.set_stroke(opacity=0))
        miss_i = next(i for i in zm if not np.isfinite(u[i]))
        miss_k = zm.index(miss_i)
        mlab = label(r"October 2025: \ no number. \\ The survey was not taken \\ during the shutdown", font_size=19,
                     color=E.MISS).next_to(zbox, DOWN, buff=0.15)
        mlab.set_opacity(0)
        line = VMobject(stroke_color=U3, stroke_width=2.6)
        tip = Dot(radius=0.055, color=U3)
        year_t = Integer(1948, font_size=72, color=GREY_C, group_with_commas=False).move_to([-4.6, 1.75, 0])
        year_t.set_z_index(-2)
        events = [("1949-10", r"1949: \ 7.9\%, \ a postwar recession"),
                  ("1953-05", r"1953: \ 2.5\%, \ the lowest on record"),
                  ("1982-11", r"1982: \ 10.8\%, \ the Fed breaks inflation \ (Part 28)"),
                  ("2009-10", r"2009: \ 10.0\%, \ the financial crisis \ (Part 33)"),
                  ("2020-04", r"April 2020: \ 14.8\%, \ the pandemic")]
        ev_mobs = VGroup()
        ticks = VGroup()
        for m, text in events:
            t = label(text, font_size=24, color=WHITE).move_to([(x0 + x1) / 2, y1 + 0.5, 0])
            ev_mobs.add(t.set_opacity(0))
            k = months.index(m)
            ticks.add(Dot([X(xs[k]), Y(u[k]), 0], radius=0.08, color=WHITE).set_opacity(0))
        tag = data_tag(rf"BLS, Current Population Survey (UNRATE), {data.fred_cite('UNRATE')}", corner=DL,
                       font_size=15)
        stag = note(r"sound: the same numbers, \ as a tune (computed)", font_size=15, color=E.ACCENT)
        stag.to_corner(DR, buff=0.3)
        t_start, t_last = times[0], times[-1]

        def idx_at(t):
            return int(np.clip(np.searchsorted(times, t, side="right") - 1, 0, len(months) - 1))

        def draw(m, t):
            i = max(idx_at(t), 1)
            ok = np.isfinite(u[: i + 1])
            pts = [np.array([X(x), Y(v), 0]) for x, v in zip(xs[: i + 1][ok], u[: i + 1][ok])]
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
                tip.move_to(pts[-1])

        def counter(m, t):
            m.set_value(int(months[idx_at(t)][:4]))

        def show_events(m, t):
            i = idx_at(t)
            reached = [k for k, (mon, _) in enumerate(events) if i >= months.index(mon)]
            last = reached[-1] if reached else -1
            for k, ev in enumerate(m):
                ev.set_opacity(1.0 if k == last and i < zm[0] else 0.0)

        def show_ticks(m, t):
            i = idx_at(t)
            for (mon, _), tk in zip(events, m):
                tk.set_opacity(0.9 if i >= months.index(mon) else 0.0)

        def zoom(m, t):
            i = idx_at(t)
            on = 1.0 if t >= times[zm[0]] - 0.6 else 0.0
            for g in (zbox, zhead, zlabels, zyl):
                g.set_opacity(on) if g is not zbox else g.set_stroke(opacity=on).set_fill(opacity=0.9 * on)
            for k, dd in enumerate(zdots):
                shown = on and i >= zm[k]
                if zm[k] == miss_i:
                    dd.set_stroke(opacity=1.0 if (on and t >= film_time("2025-10")) else 0.0)
                else:
                    dd.set_opacity(1.0 if shown else 0.0)
            mlab.set_opacity(1.0 if t >= film_time("2025-10") else 0.0)

        with self.listen(clip) as snd:
            snd.caption(r"the US unemployment rate, 1948 to 2026, \ under the same numbers as a tune")
            snd.show(tag, stag)
            snd.drive(line, draw)
            snd.drive(year_t, counter)
            snd.drive(ev_mobs, show_events)
            snd.drive(ticks, show_ticks)
            zoom_group = VGroup(zbox, zhead, zlabels, zyl, zdots, mlab)
            snd.drive(zoom_group, zoom)
            snd.show(ticks, line, tip, year_t, ev_mobs, frame, axis_name, zoom_group)
            self.play(LaggedStart(*[Create(m) if isinstance(m, Line) else FadeIn(m) for m in frame], lag_ratio=0.03),
                      FadeIn(axis_name), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (frame, axis_name, tag, line, tip, ev_mobs, ticks, stag, zoom_group)],
                      year_t.animate.set_opacity(0.0), run_time=1.0)
            story = point_cards([
                (r"three ways, one number", r"output, spending and income \\ must agree: \ it's bookkeeping",
                 E.ACCENT),
                (r"value added", r"count what each firm adds, \\ not what it sells", E.FIRMS),
                (r"the boundary", r"housework, informal work and free \\ goods sit outside it", UNPAID),
                (r"whose basket?", r"Laspeyres overstates, Paasche \\ understates; Fisher is close", FISHER),
                (r"chain drift", r"chain often, \ with a superlative index", PAAS),
                (r"quality", r"a longer boat is not inflation: \\ hedonics", E.FISH),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            nxt = label(r"next: \ countries, \ jobs, \ who gets the income, \ and the revisions", font_size=22,
                        color=GREY_B).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 1.6))
            self.play(FadeIn(nxt))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
