from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ62.common import *  # noqa: F403


class Intermission(SoundScene):
    """Output per hour in the American nonfarm business sector, quarterly since 1947 (log scale), drawn quarter by
    quarter with the eras of fast and slow growth marked; under it, each year's growth as a tune; then the story so
    far."""

    def construct(self):
        film = load("film")
        D, X, Pr, Pc, C, T = (load(x) for x in ("dispersion", "experiment", "practices", "piece", "ceo", "tradeoff"))
        clip = ClipStore("econ62").load("intermission.melody")
        idx = np.array(film["index"], float)
        lo, hi = np.log10(idx.min() * 0.9), np.log10(idx.max() * 1.15)
        ax = plane([1946, 2027], [lo, hi], center=DOWN * 0.25 + LEFT * 0.3, x_length=11.6, y_length=5.2,
                   xticks=[1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020], yticks=[np.log10(v) for v in (25, 50, 100)],
                   ylabel=r"output per hour, \ 2017 = 100 \ (log scale)", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{10 ** y:.0f}", font_size=15)
        yrs, ts = np.array(film["years"], float), np.array(film["t"], float)
        pts = [ax.ax.c2p(x, np.log10(y)) for x, y in zip(yrs, idx)]

        def grower(m, tt):
            k = int(np.searchsorted(ts, tt, side="right"))
            ps = pts[:max(k, 1)]
            if len(ps) < 2:
                ps = [pts[0], pts[0]]
            m.set_points_as_corners(ps)

        line = VMobject(stroke_color=PROD, stroke_width=3.4)
        line.set_points_as_corners([pts[0], pts[0]])
        eras = VGroup()
        for e in film["eras"]:
            a, b = e["from"], e["to"]
            r = shade(ax, [(a - 0.5, b + 0.5)], lo, hi, GREY_E if e["growth"] < 2 else RECESS, 0.35)
            tx = label(rf"{e['growth']:.1f}\% a year", font_size=15, color=GAIN if e["growth"] >= 2 else COST).move_to(
                ax.ax.c2p((a + b) / 2, hi - 0.06))
            m = VGroup(r, tx)
            m.ft = film_time(b + 0.5)
            m.set_opacity(0.0)
            eras.add(m)
        key = label(r"output per hour of work, \ American business", font_size=17, color=PROD).move_to(
            ax.ax.c2p(1960, lo + 0.75 * (hi - lo)))
        yr = Integer(1947, font_size=48, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2014,
                                                                                                lo + 0.2 * (hi - lo)))

        def set_year(m, tt):
            a, b = 1947.0, 2027.0
            m.set_value(int(np.clip(a + (tt - 2.0) / (FILM_SECONDS - 4.0) * (b - a), a, 2026)))

        src = data_tag(r"BLS via FRED: \ OPHNFB", corner=DL, font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT,
                                                                                                        buff=0.3)
        stag = note(r"sound: \ each year's growth, \ 1948--2025 \ (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"output per hour in American business, \ quarterly since 1947, \ with the eras of fast and "
                        r"slow growth marked; \ each year's growth as a tune")
            snd.show(src, stag)
            snd.drive(line, grower)
            snd.drive(yr, set_year)
            for m in eras:
                snd.drive(m, lambda mm, tt: mm.set_opacity(1.0 if tt >= mm.ft else 0.0))
            snd.show(ax, eras, line, yr, key)
            self.play(FadeIn(ax), FadeIn(key), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            for m in eras:
                m.clear_updaters()
            line.clear_updaters()
            yr.clear_updaters()
            self.play(*[FadeOut(m) for m in (ax, line, yr, eras, key, src, stag)], run_time=1.0)
            r3 = [r for r in D["rows"] if r["sigma"] == 3.0][0]
            story = point_cards([
                (r"dispersion", rf"survivors' 90/10 productivity ratio {r3['ratio_90_10']:.2f}; \ less where buyers "
                 r"switch easily", PLANT),
                (r"Play it", rf"recording defects returns {Pr['rows']['record and act on defects']['per_dollar']:.1f} "
                 r"per dollar; \ the loom loses money", MGR),
                (r"the experiment", rf"+{100 * X['first_est']:.0f}\% on the Island, \ +17\% in Mumbai: \ the owners "
                 r"did not know", TREAT),
                (r"piece rates", rf"+{100 * Pc['gain_total']:.0f}\% output per worker, \ about half from who "
                 r"joins", WORK),
                (r"executive pay", rf"pay $\propto$ size$^{{1/3}}$ across firms; \ all firms six times larger, \ pay "
                 rf"{C['ratio_after_sixfold']:.0f} times", CEO),
                (r"capital structure", rf"the trade-off's best about {100 * T['best']:.0f}\% debt; \ firms borrow "
                 r"less, \ the pecking order", FIN),
            ], width=12.6, cols=3, font_size=19).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
