from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ48.common import *  # noqa: F403


def stripe_color(v: float, lo: float = -0.5, hi: float = 1.6):
    """Blue for cool years, red for warm, white near the 1850-1900 average."""
    x = float(np.clip((v - lo) / (hi - lo), 0, 1))
    z = (0 - lo) / (hi - lo)
    if x < z:
        return interpolate_color(ManimColor("#2B6CB0"), ManimColor("#F5F5F5"), x / z)
    return interpolate_color(ManimColor("#F5F5F5"), ManimColor("#C53030"), (x - z) / (1 - z))


class Intermission(SoundScene):
    """The world's warming since 1850-1900, year by year, drawn as a stripe for each year as the years pass, with the
    line over it; under it, the warming as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        M = load("metals")
        B = load("bet")
        Fi = load("fishery")
        C = load("climate")
        D = load("dice")
        S = load("scc")
        clip = ClipStore("econ48").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["v"], float)
        x0, x1, y0, y1 = -6.2, 6.2, -2.6, 1.9
        w = (x1 - x0) / len(t)
        stripes = VGroup(*[Rectangle(width=w * 1.02, height=y1 - y0, stroke_width=0, fill_color=stripe_color(val),
                                     fill_opacity=1.0).move_to([x0 + w * (i + 0.5), (y0 + y1) / 2, 0])
                           for i, val in enumerate(v)])
        for i, s_ in enumerate(stripes):
            s_.ft = film_time(t[i])
            s_.set_opacity(0.0)
        ys = lambda val: y0 + 0.3 + (val + 0.5) / 2.2 * (y1 - y0 - 0.6)  # noqa: E731
        pts = [np.array([x0 + w * (i + 0.5), ys(val), 0]) for i, val in enumerate(v)]
        grow = VMobject(stroke_color=BLACK, stroke_width=3.4)
        grow.set_points_as_corners([pts[0], pts[0]])
        t0, t1 = film_time(t[0]), film_time(t[-1])

        def grower(m, tt):
            yr = float(np.clip(t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0]), t[0], t[-1]))
            k = int(np.searchsorted(t, yr, side="right"))
            ps = pts[:max(k, 1)]
            if len(ps) < 2:
                ps = [ps[0], ps[0]]
            m.set_points_as_corners(ps)

        year = Integer(1850, font_size=52, color=E.ACCENT, group_with_commas=False).move_to([-4.6, 2.75, 0])

        def set_year(m, tt):
            m.set_value(int(np.clip(t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0]), t[0], t[-1])))

        marks = VGroup()
        for yr_, txt in ((1850.0, rf"1850: \ {film['first']:+.2f}\textdegree".replace("-", "{-}")),
                         (1950.0, rf"1950: \ {film['v1950']:+.2f}\textdegree"),
                         (2000.0, rf"2000: \ {film['v2000']:+.2f}\textdegree"),
                         (float(t[-1]), rf"{int(t[-1])}: \ {film['last']:+.2f}\textdegree")):
            i = int(np.argmin(np.abs(t - yr_)))
            m = label(txt, font_size=18, color=WHITE).next_to(np.array([x0 + w * (i + 0.5), y0, 0]), DOWN, buff=0.15)
            m.ft = film_time(yr_)
            marks.add(m)
        src = data_tag(r"Met Office Hadley Centre and CRU, \ HadCRUT5; \ stripes after Ed Hawkins", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the warming \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the world's warming since 1850--1900, \ 1850--2025; \ each stripe a year, \ the warming "
                        r"as a tune")
            snd.show(src, stag)
            for s_ in stripes:
                snd.drive(s_, lambda mm, tt: mm.set_fill(opacity=1.0 if tt >= mm.ft else 0.0))
            snd.drive(grow, grower)
            snd.drive(year, set_year)
            for m in marks:
                snd.drive(m, lambda mm, tt: mm.set_opacity(1.0 if tt >= mm.ft else 0.0))
            snd.show(stripes, grow, year, marks)
            snd.wait_until("film_end")
            self.wait(1.0)
            self.play(*[FadeOut(m) for m in (stripes, grow, year, marks, src, stag)], run_time=1.0)
            O = D["opt"]
            story = point_cards([
                (r"the bet", rf"Simon won 1980--90: \ {100 * M['bundle_8090']:+.0f}\%; \ Ehrlich wins \ "
                             rf"{100 * B['ehrlich_share']:.0f}\% of decades".replace("-", "{-}"), METAL),
                (r"Hotelling", r"the scarcity rent \ rises at the rate \ of interest; \ prices need not", METAL),
                (r"the fishery", rf"open access: \ stock {Fi['open_end']:.1f}; \ a quota: \ {Fi['quota_end']:.1f}",
                 FISH),
                (r"the climate", rf"four equations \ fitted: \ {C['decade_model']:.2f}\textdegree \ against "
                                 rf"{C['decade_obs']:.2f}\textdegree", HEAT),
                (r"the model", rf"optimal: \ {O['T2100']:.1f}\textdegree \ in 2100; \ \${O['price2050']:.0f} \ "
                               r"a tonne in 2050", OPT),
                (r"the discount rate", rf"\${S['by_rate'][2]:.0f} \ at 2\%, \ \${S['by_rate'][8]:.0f} \ at 5\%",
                 STERN),
            ], width=12.6, cols=3, font_size=21).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
