from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ60.common import *  # noqa: F403


class Intermission(SoundScene):
    """Producer prices of processed food and consumer prices of food at home, monthly since 1990 (1990 = 100), drawn
    month by month with the 2008 spike, the pandemic and the war in Ukraine marked; under it, food inflation as a
    tune; then the story so far."""

    def construct(self):
        film = load("film")
        C, X, P, L = (load(x) for x in ("costplus", "experiment", "playit", "rm"))
        clip = ClipStore("econ60").load("intermission.melody")
        top = float(max(max(film["cpi"]), max(film["ppi"]))) * 1.08
        ax = plane([1989, 2027], [80, top], center=DOWN * 0.25 + LEFT * 0.3, x_length=11.6, y_length=5.2,
                   xticks=[1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025], yticks=[100, 150, 200, 250],
                   ylabel=r"index, \ January 1990 = 100", xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.0f}",
                   font_size=15)
        yrs, ts = np.array(film["years"], float), np.array(film["t"], float)

        def grower_for(vals):
            pts = [ax.ax.c2p(x, y) for x, y in zip(yrs, vals)]

            def grower(m, tt):
                k = int(np.searchsorted(ts, tt, side="right"))
                ps = pts[:max(k, 1)]
                if len(ps) < 2:
                    ps = [pts[0], pts[0]]
                m.set_points_as_corners(ps)
            return pts, grower

        pc, gc = grower_for(film["cpi"])
        pp, gp = grower_for(film["ppi"])
        cpi = VMobject(stroke_color=FOOD, stroke_width=3.2)
        cpi.set_points_as_corners([pc[0], pc[0]])
        ppi = VMobject(stroke_color=PPI, stroke_width=2.6)
        ppi.set_points_as_corners([pp[0], pp[0]])
        marks = VGroup()
        for e in film["events"]:
            ln = DashedLine(ax.ax.c2p(e["year"], 82), ax.ax.c2p(e["year"], top * 0.97), color=GREY_B,
                            stroke_width=1.3)
            tx = label(tex_safe(e["what"]), font_size=14, color=GREY_A).rotate(PI / 2).next_to(
                ax.ax.c2p(e["year"], top * 0.97), DOWN, buff=0.1).shift(LEFT * 0.14)
            m = VGroup(ln, tx)
            m.ft = e["t"]
            m.set_opacity(0.0)
            marks.add(m)
        key = VGroup(label(r"green: \ food at the grocer's \ (CPI)", font_size=17, color=FOOD),
                     label(r"orange: \ processed food at the factory gate \ (PPI)", font_size=17, color=PPI)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.ax.c2p(1999, top * 0.9))
        year = Integer(1990, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2023,
                                                                                                    top * 0.25 + 60))

        def set_year(m, tt):
            a, b = 1990.0, 2027.0
            m.set_value(int(np.clip(a + (tt - 2.0) / (FILM_SECONDS - 4.0) * (b - a), a, 2026)))

        src = data_tag(r"BLS via FRED: \ CUSR0000SAF11, \ WPU02", corner=DL, font_size=13).to_edge(
            UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ food inflation, \ 1991--2025 \ (computed)", font_size=13, color=E.ACCENT).to_corner(
            UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the price of processed food at the factory gate and of food at the grocer's, \ monthly "
                        r"since 1990, \ with the 2008 spike, \ the pandemic and the war in Ukraine marked; \ food "
                        r"inflation as a tune")
            snd.show(src, stag)
            snd.drive(cpi, gc)
            snd.drive(ppi, gp)
            snd.drive(year, set_year)
            for m in marks:
                snd.drive(m, lambda mm, tt: mm.set_opacity(0.9 if tt >= mm.ft else 0.0))
            snd.show(ax, ppi, cpi, year, marks, key)
            self.play(FadeIn(ax), FadeIn(key), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            for m in marks:
                m.clear_updaters()
            self.play(*[FadeOut(m) for m in (ax, cpi, ppi, year, marks, key, src, stag)], run_time=1.0)
            Rr = P["rules"]
            story = point_cards([
                (r"cost-plus", rf"the top of the profit curve is flat; \ a fixed markup earned "
                 rf"{100 * C['fixed']:.1f}\% of the best", FIRM),
                (r"willingness to pay", r"stated values run high; \ conjoint choices and BDM's lottery do better",
                 TEST),
                (r"experiments", rf"scarce rooms doubled the A/B test: \ +{100 * X['naive']:.1f} points against "
                 rf"+{100 * X['global']:.1f}", COST),
                (r"Play it", rf"start low and raise: \ \${Rr['start low, raise']['mean']:,.0f} a flight; \ start high "
                 rf"and cut: \ \${Rr['start high, cut']['mean']:,.0f}".replace(",", "{,}"), LEIS),
                (r"Littlewood", rf"protect a seat while P(it sells high) $>$ $p_L/p_H$: \ "
                 rf"{L['littlewood']['y_star']} seats", BUS),
                (r"the optimum", r"a fare for every day and every seat left, \ by dynamic programming", OPT),
            ], width=12.6, cols=3, font_size=19).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
