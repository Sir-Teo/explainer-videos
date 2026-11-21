from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ63.common import *  # noqa: F403

EVENTS = ((2008.7, 2009.25, r"Lehman, \ world trade collapses"), (2011.2, 2011.6, r"11 March 2011"),
          (2020.25, 2020.5, r"the pandemic"))


class Intermission(SoundScene):
    """Japan's industrial production, monthly since 2000 (index 2015 = 100), drawn month by month with the financial
    crisis, the earthquake and the pandemic marked; under it, each quarter's growth as a tune; then the story so
    far."""

    def construct(self):
        film = load("film")
        P, Gr, Q, O, R = (load(x) for x in ("playit", "granular", "quake", "oring", "response"))
        clip = ClipStore("econ63").load("intermission.melody")
        idx = np.array(film["index"], float)
        ax = plane([1999.5, 2024.8], [70, 125], center=DOWN * 0.25 + LEFT * 0.3, x_length=11.6, y_length=5.2,
                   xticks=[2000, 2005, 2010, 2015, 2020], yticks=[80, 90, 100, 110, 120],
                   ylabel=r"industrial production, \ Japan, \ 2015 = 100", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=15)
        yrs, ts = np.array(film["years"], float), np.array(film["t"], float)
        pts = [ax.ax.c2p(x, y) for x, y in zip(yrs, idx)]

        def grower(m, tt):
            k = int(np.searchsorted(ts, tt, side="right"))
            ps = pts[:max(k, 1)]
            if len(ps) < 2:
                ps = [pts[0], pts[0]]
            m.set_points_as_corners(ps)

        line = VMobject(stroke_color=PROD, stroke_width=3.2)
        line.set_points_as_corners([pts[0], pts[0]])
        marks = VGroup()
        for a, b, txt in EVENTS:
            r = shade(ax, [(a, b)], 70, 125, SHOCK if "March" in txt else RECESS, 0.35)
            tx = label(txt, font_size=15, color=SHOCK if "March" in txt else GREY_A).next_to(
                ax.ax.c2p((a + b) / 2, 125), DOWN, buff=0.12)
            m = VGroup(r, tx)
            m.ft = film_time(a)
            m.set_opacity(0.0)
            marks.add(m)
        drop = label(rf"{film['march_2011']:.1f}\% in one month".replace("-", "{-}"), font_size=18,
                     color=SHOCK).next_to(ax.ax.c2p(2011.25, film["mar_2011"]), DOWN + RIGHT, buff=0.1)
        drop.ft = film_time(2011.3)
        drop.set_opacity(0.0)
        yr = Integer(2000, font_size=48, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2004, 78))

        def set_year(m, tt):
            a, b = FILM_YEARS
            m.set_value(int(np.clip(a + (tt - 2.0) / (FILM_SECONDS - 4.0) * (b - a), a, 2024)))

        src = data_tag(r"OECD via FRED: \ JPNPROINDMISMEI", corner=DL, font_size=13).to_edge(UP, buff=0.12).to_edge(
            LEFT, buff=0.3)
        stag = note(r"sound: \ each quarter's growth, \ 2000--2024 \ (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"Japan's industrial production, \ monthly since 2000, \ with the financial crisis, \ the "
                        r"earthquake and the pandemic marked; \ each quarter's growth as a tune")
            snd.show(src, stag)
            snd.drive(line, grower)
            snd.drive(yr, set_year)
            for m in [*marks, drop]:
                snd.drive(m, lambda mm, tt: mm.set_opacity(1.0 if tt >= mm.ft else 0.0))
            snd.show(ax, marks, drop, line, yr)
            self.play(FadeIn(ax), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            for m in [*marks, drop, line, yr]:
                m.clear_updaters()
            self.play(*[FadeOut(m) for m in (ax, line, yr, marks, drop, src, stag)], run_time=1.0)
            Rw = {r["sector"]: r for r in P["rows"]}
            story = point_cards([
                (r"Leontief's paths", r"sales per dollar of GDP add to 1.9; \ energy sells mostly to other "
                 r"sectors", NODE),
                (r"Hulten", r"a small shock matters by the sector's sales, \ and nothing else", GDP),
                (r"Play it", rf"services cost {100 * (1 - np.exp(Rw['services']['loss'])):.0f}\%; \ energy a third "
                 r"more than its sales say", LINK),
                (r"granular", rf"Zipf-sized firms: \ {100 * Gr['rows'][-1]['zipf']:.1f}\% swings that do not "
                 r"cancel", SHOCK),
                (r"supply chains", rf"{100 * Q['direct_only']:.0f}\% lost at the hit firms, \ "
                 rf"{100 * Q['total_loss']:.1f}\% with the links", SEED),
                (r"the O-ring", rf"one weak link costs two fifths; \ sorting adds {100 * O['gain']:.0f}\%",
                 PEOPLE),
            ], width=12.6, cols=3, font_size=19).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
