from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ61.common import *  # noqa: F403


class Intermission(SoundScene):
    """E-commerce's share of American retail sales, quarterly since 1999, drawn quarter by quarter with the
    financial crisis and the pandemic marked; under it, the yearly share as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        N, C, S, A = (load(x) for x in ("night", "commission", "surplus", "ads"))
        R, Rk = load("reputation"), load("ranking")
        clip = ClipStore("econ61").load("intermission.melody")
        top = float(max(film["share"])) * 1.15
        ax = plane([1999, 2027], [0, top], center=DOWN * 0.25 + LEFT * 0.3, x_length=11.6, y_length=5.2,
                   xticks=[2000, 2005, 2010, 2015, 2020, 2025], yticks=[0, 5, 10, 15, 20],
                   ylabel=r"online sales, \ \% of all retail sales", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=15)
        yrs, ts = np.array(film["years"], float), np.array(film["t"], float)
        pts = [ax.ax.c2p(x, y) for x, y in zip(yrs, film["share"])]

        def grower(m, tt):
            k = int(np.searchsorted(ts, tt, side="right"))
            ps = pts[:max(k, 1)]
            if len(ps) < 2:
                ps = [pts[0], pts[0]]
            m.set_points_as_corners(ps)

        line = VMobject(stroke_color=ECOM, stroke_width=3.4)
        line.set_points_as_corners([pts[0], pts[0]])
        marks = VGroup()
        for e in film["events"]:
            ln = DashedLine(ax.ax.c2p(e["year"], 0.3), ax.ax.c2p(e["year"], top * 0.97), color=GREY_B,
                            stroke_width=1.3)
            tx = label(tex_safe(e["what"]), font_size=14, color=GREY_A).rotate(PI / 2).next_to(
                ax.ax.c2p(e["year"], top * 0.97), DOWN, buff=0.1).shift(LEFT * 0.14)
            m = VGroup(ln, tx)
            m.ft = e["t"]
            m.set_opacity(0.0)
            marks.add(m)
        key = label(r"the share of American retail \\ sold online, \ quarterly, \\ seasonally adjusted", font_size=17,
                    color=ECOM).move_to(ax.ax.c2p(2003.3, top * 0.78))
        val = DecimalNumber(float(film["share"][0]), num_decimal_places=1, font_size=48, color=E.ACCENT,
                            unit=r"\%").move_to(ax.ax.c2p(2023, top * 0.3))

        def set_val(m, tt):
            k = int(np.clip(np.searchsorted(ts, tt, side="right") - 1, 0, len(ts) - 1))
            m.set_value(float(film["share"][k]))

        src = data_tag(r"Census Bureau via FRED: \ ECOMPCTSA", corner=DL, font_size=13).to_edge(
            UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the yearly share, \ 2000--2025 \ (computed)", font_size=13, color=E.ACCENT).to_corner(
            UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the share of American retail sales made online, \ quarterly since the end of 1999, \ with "
                        r"the financial crisis and the pandemic marked; \ the yearly share as a tune")
            snd.show(src, stag)
            snd.drive(line, grower)
            snd.drive(val, set_val)
            for m in marks:
                snd.drive(m, lambda mm, tt: mm.set_opacity(0.9 if tt >= mm.ft else 0.0))
            snd.show(ax, line, val, marks, key)
            self.play(FadeIn(ax), FadeIn(key), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            for m in marks:
                m.clear_updaters()
            line.clear_updaters()
            val.clear_updaters()
            self.play(*[FadeOut(m) for m in (ax, line, val, marks, key, src, stag)], run_time=1.0)
            O = C["options"]
            story = point_cards([
                (r"twenty-six minutes", rf"surge off: \ about {100 * N['off']['rate_peak']:.0f}\% of requests "
                 r"filled at the peak; \ surge on: \ all of them", SURGE),
                (r"Play it", rf"the platform's best commission: \ {100 * C['best_c']:.0f}\%, \ "
                 rf"\${O['0.3']['platform']:.0f} an hour at 30\%; \ riders and drivers lose far more", PLAT),
                (r"surge's surplus", rf"\${S['cs_per_dollar']:.2f} of consumer surplus per dollar on the Island; \ "
                 r"about \$1.60 for UberX", RIDER),
                (r"ranking", rf"position alone: \ the top slot gets {Rk['top_vs_fifth']:.1f} times the fifth's "
                 r"attention; \ a sponsored top slot costs clicks", SELL),
                (r"reputation", rf"percent positive, \ median {100 * R['pp_median']:.0f}\%; \ counting silence "
                 r"tracks quality better", DRIVER),
                (r"advertising", rf"the dashboard: \ +{100 * A['attributed_roi']:,.0f}\%; \ the truth: \ "
                 rf"{100 * A['true_roi']:.0f}\%".replace(",", "{,}").replace("-", "{-}"), AD),
            ], width=12.6, cols=3, font_size=19).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
