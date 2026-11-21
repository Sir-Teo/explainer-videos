from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ65.common import *  # noqa: F403

SHORT = {"USA": "United States", "GBR": "Britain", "DEU": "Germany", "FRA": "France", "JPN": "Japan",
         "KOR": "South Korea"}


class Intermission(SoundScene):
    """Average annual hours worked per worker in six countries since 1950 (Penn World Table 11.0), drawn year by year
    against Keynes's fifteen-hour week; under it, the six countries' average as a falling tune; then the story so
    far."""

    def construct(self):
        film = load("film")
        T, J, D, H, G = (load(x) for x in ("tasks", "jcurve", "desk", "hulten", "growth"))
        clip = ClipStore("econ65").load("intermission.melody")
        ax = plane([1948, 2026], [500, 3200], center=DOWN * 0.25 + LEFT * 0.8, x_length=10.8, y_length=5.2,
                   xticks=[1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020],
                   yticks=[780, 1000, 1500, 2000, 2500, 3000],
                   ylabel=r"hours worked a year, \ per worker", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:,.0f}".replace(",", "{,}"), font_size=15)
        kline = seg(ax, 1948, film["keynes"], 2026, film["keynes"], E.ACCENT, 2.6, dashed=True)
        klab = label(r"Keynes's fifteen-hour week", font_size=17, color=E.ACCENT).next_to(
            ax.ax.c2p(1952, film["keynes"]), UP, buff=0.1).align_to(ax.ax.c2p(1952, 0), LEFT)
        lines, ends = VGroup(), VGroup()
        for c, S in film["series"].items():
            pts = [ax.ax.c2p(y, h) for y, h in zip(S["year"], S["hours"])]
            ts = np.array(S["t"], float)
            m = VMobject(stroke_color=NATION[c], stroke_width=3.0)
            m.set_points_as_corners([pts[0], pts[0]])
            m.pts, m.ts = pts, ts
            lines.add(m)
            e = label(SHORT[c], font_size=15, color=NATION[c]).next_to(pts[-1], RIGHT, buff=0.1)
            e.ft = float(ts[-1])
            e.y0 = float(pts[-1][1])
            ends.add(e)
        # spread the end labels so that none overlaps: at least 0.3 apart, in the order of their lines
        order = sorted(range(len(ends)), key=lambda i: ends[i].y0)
        ys = [ends[i].y0 for i in order]
        for j in range(1, len(ys)):
            ys[j] = max(ys[j], ys[j - 1] + 0.3)
        shift = (sum(ys) - sum(ends[i].y0 for i in order)) / len(ys)
        for i, y in zip(order, ys):
            ends[i].set_y(y - shift)
            ends[i].set_opacity(0.0)

        def grower(m, tt):
            k = int(np.searchsorted(m.ts, tt, side="right"))
            ps = m.pts[:max(k, 1)]
            if len(ps) < 2:
                ps = [m.pts[0], m.pts[0]]
            m.set_points_as_corners(ps)

        yr = Integer(1950, font_size=48, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2014, 3000))

        def set_year(m, tt):
            a, b = FILM_YEARS
            m.set_value(int(np.clip(a + (tt - 2.0) / (FILM_SECONDS - 4.0) * (b - a), a, film["last"])))

        src = data_tag(r"Penn World Table 11.0: \ avh", corner=DL, font_size=13).to_edge(UP, buff=0.12).to_edge(
            LEFT, buff=0.3)
        stag = note(r"sound: \ the six countries' average hours, \ 1950--2023 \ (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"hours worked a year per worker in six countries, \ 1950--2023, \ against Keynes's "
                        r"fifteen-hour week; \ their average as a tune")
            snd.show(src, stag)
            for m in lines:
                snd.drive(m, grower)
            for e in ends:
                snd.drive(e, lambda mm, tt: mm.set_opacity(1.0 if tt >= mm.ft else 0.0))
            snd.drive(yr, set_year)
            snd.show(ax, kline, klab, lines, ends, yr)
            self.play(FadeIn(ax), FadeIn(kline), FadeIn(klab), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            for m in [*lines, *ends, yr]:
                m.clear_updaters()
            self.play(*[FadeOut(m) for m in (ax, lines, ends, yr, kline, klab, src, stag)], run_time=1.0)
            P = G["paths"]
            story = point_cards([
                (r"Keynes", r"four to eight times richer: \ right; \ fifteen hours a week: \ not close", GDP),
                (r"Play it", rf"automate 90\% of research: \ a boom to {100 * P['0.90']['peak']:.0f}\% growth, "
                 r"\ then back; \ automate all: \ explosion", IDEA),
                (r"the task model", rf"automation: \ displacement against productivity; \ new tasks restore "
                 rf"labour's share to {100 * T['new_tasks']['labour_share'][-1]:.0f}\%", WORK),
                (r"the J-curve", rf"measured productivity falls {100 * (1 - J['low']):.0f}\% before it rises: "
                 r"\ the intangible investment is unseen", NEWT),
                (r"the experiments", rf"+{100 * D['est']:.0f}\% on the support desk, \ +"
                 rf"{100 * D['fifths'][0]['est']:.0f}\% for the least skilled", TEXT),
                (r"the aggregates", rf"Acemoglu's arithmetic: \ {100 * H['rows'][0]['tfp']:.2f}\% more TFP in "
                 r"ten years", MACH),
            ], width=12.6, cols=3, font_size=19).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
