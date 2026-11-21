from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ59.common import *  # noqa: F403


class Intermission(SoundScene):
    """Airline fares in the consumer price index, deflated by the index for everything, 1964-2025, drawn year by
    year with deregulation and the big mergers marked; under it, the fares as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        T, P, U, Fm = (load(x) for x in ("towns", "playit", "upp", "forms"))
        clip = ClipStore("econ59").load("intermission.melody")
        ax = plane([1962, 2027], [60, 220], center=DOWN * 0.25 + LEFT * 0.3, x_length=11.6, y_length=5.2,
                   xticks=[1965, 1975, 1985, 1995, 2005, 2015, 2025], yticks=[75, 100, 125, 150, 175, 200],
                   ylabel=r"airline fares in the CPI \ $\div$ \ the CPI, \ 1978 = 100", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=15)
        base = DashedLine(ax.ax.c2p(1962, 100), ax.ax.c2p(2027, 100), color=GREY_C, stroke_width=1.2)
        ys, vs, ts = np.array(film["years"], float) + 0.5, np.array(film["real"], float), np.array(film["t"], float)
        pts = [ax.ax.c2p(x, y) for x, y in zip(ys, vs)]
        grow = VMobject(stroke_color=FARE, stroke_width=3.4)
        grow.set_points_as_corners([pts[0], pts[0]])

        def grower(m, tt):
            k = int(np.searchsorted(ts, tt, side="right"))
            ps = pts[:max(k, 1)]
            if 0 < k < len(pts):
                f = float(np.clip((tt - ts[k - 1]) / (ts[k] - ts[k - 1]), 0, 1))
                ps = ps + [pts[k - 1] + f * (pts[k] - pts[k - 1])]
            if len(ps) < 2:
                ps = [ps[0], ps[0]]
            m.set_points_as_corners(ps)

        marks = VGroup()
        for i, e in enumerate(film["events"]):
            x = e["year"] + 0.5
            ln = DashedLine(ax.ax.c2p(x, 62), ax.ax.c2p(x, 212), color=GOV if "and" in e["what"] else GREY_B,
                            stroke_width=1.4)
            tx = label(tex_safe(e["what"]), font_size=13, color=GOV if "and" in e["what"] else GREY_A)
            tx.rotate(PI / 2).next_to(ax.ax.c2p(x, 62), UP, buff=0.1).shift(RIGHT * 0.12)
            m = VGroup(ln, tx)
            m.ft = e["t"]
            m.set_opacity(0.0)
            marks.add(m)
        year = Integer(1964, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1972, 200))

        def set_year(m, tt):
            a, b = 1964.0, 2026.0
            m.set_value(int(np.clip(a + (tt - 2.0) / (FILM_SECONDS - 4.0) * (b - a), a, 2025)))

        src = data_tag(r"BLS via FRED: \ CUUR0000SETG01, \ CPIAUCNS", corner=DL, font_size=13).to_edge(
            UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ real airline fares, \ 1964--2025 \ (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"airline fares in the consumer price index, \ relative to all prices, \ 1964--2025, \ "
                        r"with deregulation and the big mergers marked; \ the fares as a tune")
            snd.show(src, stag)
            snd.drive(grow, grower)
            snd.drive(year, set_year)
            for m in marks:
                snd.drive(m, lambda mm, tt: mm.set_opacity(0.9 if tt >= mm.ft else 0.0))
            snd.show(ax, base, grow, year, marks)
            self.play(FadeIn(ax), FadeIn(base), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            caveat = label(r"an index is a method: \ from late 1998 to mid-2003 the CPI's fares rose 15.4\%, \ "
                           r"the BLS's index of fares actually paid 6.8\%", font_size=19, color=HOLD).to_edge(
                DOWN, buff=0.35)
            self.play(FadeIn(caveat), run_time=0.8)
            self.wait(2.5)
            self.play(*[FadeOut(m) for m in (ax, base, grow, year, marks, src, stag, caveat)], run_time=1.0)
            pairs = P["pairs"]
            story = point_cards([
                (r"the law", r"`may be substantially to lessen competition': \ a prediction, \ argued in court",
                 GOV),
                (r"the map", rf"Alder alone charges {T['lone_premium']:.0f}\% more \ than with both rivals; \ "
                 r"but rents differ too", ALDER),
                (r"Play it", rf"diversion above $X/(X + M)$: \ Alder and Birch ({100 * pairs[0]['D']:.0f}\% $>$ "
                 rf"{100 * pairs[0]['critical']:.0f}\%), \ and the kilns", BIRCH),
                (r"the market", r"the smallest set a monopolist could raise prices in; \ beware cellophane", CEDAR),
                (r"pricing pressure", rf"Alder's GUPPI {100 * U['products']['Alder']['guppi']:.1f}\%; \ simulated "
                 rf"+{100 * U['simulation']['dp'][0]:.1f}\%", SIM),
                (r"the curve decides", rf"the same data: \ +{Fm['rise'][0]:.1f}\% \ to \ +{Fm['rise'][3]:.1f}\%",
                 CARTEL),
            ], width=12.6, cols=3, font_size=19).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
