from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ9.common import *  # noqa: F403

BRENT = "#7EC8F5"
WTI = "#F2A65A"


class Intermission(SoundScene):
    """One price for oil?  Brent and West Texas Intermediate crude, month by month, 1987-2026, drawn without
    narration as a month counter runs, with the gap between them below; under them, Brent's premium year by year as
    a tune; three notes on the way; then the story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ9").load("intermission.melody")
        months = film["months"]
        t_of = np.array(film["times"])
        n = len(months)
        xs = np.array([int(m[:4]) + (int(m[5:7]) - 1) / 12 for m in months])
        brent, wti = np.array(film["brent"]), np.array(film["wti"])
        gap = brent - wti
        top = plane([1986, 2027], [0, 150], center=UP * 0.85 + LEFT * 0.4, x_length=11.4, y_length=3.7,
                    xticks=[1990, 2000, 2010, 2020], yticks=[0, 50, 100, 150], ylabel=r"\$ a barrel", font_size=16,
                    xfmt=lambda v: f"{v:.0f}")
        bot = plane([1986, 2027], [-10, 30], center=DOWN * 2.55 + LEFT * 0.4, x_length=11.4, y_length=1.5,
                    xticks=[1990, 2000, 2010, 2020], yticks=[-10, 0, 10, 20, 30], ylabel=r"Brent $-$ WTI",
                    font_size=15, xfmt=lambda v: f"{v:.0f}")
        zero = DashedLine(bot.ax.c2p(1986, 0), bot.ax.c2p(2027, 0), color=GREY_C, stroke_width=1.5)
        full = {
            "brent": VMobject(stroke_color=BRENT, stroke_width=2.5).set_points_as_corners(
                [top.ax.c2p(x, v) for x, v in zip(xs, brent)]),
            "wti": VMobject(stroke_color=WTI, stroke_width=2.5).set_points_as_corners(
                [top.ax.c2p(x, v) for x, v in zip(xs, wti)]),
            "gap": VMobject(stroke_color=E.ACCENT, stroke_width=2.5).set_points_as_corners(
                [bot.ax.c2p(x, max(min(v, 30), -10)) for x, v in zip(xs, gap)]),
        }
        grown = {k: m.copy() for k, m in full.items()}
        for k, m in grown.items():
            m.full_ = full[k]

        def grow(m, t):
            k = float(np.interp(t, t_of, np.arange(n)))
            m.pointwise_become_partial(m.full_, 0, max(k / (n - 1), 1e-3))

        year = Integer(int(months[0][:4]), font_size=50, color=E.ACCENT, group_with_commas=False).to_corner(
            UR, buff=0.45).shift(DOWN * 0.35)

        def set_year(m, t):
            k = int(np.clip(np.floor(float(np.interp(t, t_of, np.arange(n)))), 0, n - 1))
            m.set_value(int(months[k][:4]))

        legend = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, color=c, stroke_width=4), label(t_, font_size=17,
                                                                                         color=GREY_A)).arrange(
            RIGHT, buff=0.1) for t_, c in ((r"Brent (North Sea)", BRENT), (r"WTI (Cushing, Oklahoma)", WTI))]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(bot.ax.c2p(1994, 20))

        def at(month):
            return float(np.interp(months.index(month), np.arange(n), t_of))

        notes = [
            (label(r"for 24 years, \ usually within a dollar or two", font_size=19, color=WHITE).move_to(
                top.ax.c2p(1996, 112)), 2.0, at("2010-06-01")),
            (label(r"2011--13: \ oil floods into Cushing \\ faster than pipelines can carry it out", font_size=19,
                   color=E.ACCENT).move_to(top.ax.c2p(1996, 112)), at("2011-03-01"), at("2015-06-01")),
            (label(r"new pipelines, \ and from December 2015 \\ American crude may be exported again", font_size=19,
                   color=WHITE).move_to(top.ax.c2p(1996, 112)), at("2015-09-01"), at("2025-06-01")),
            (label(r"2026: \ a new spike, \\ too recent for this film to explain", font_size=19,
                   color=GREY_A).move_to(top.ax.c2p(1996, 112)), at("2025-10-01"), t_of[-1] + 6.0),
        ]

        def window(t0, t1):
            def f(m, t):
                m.set_opacity(float(np.clip((t - t0) / 0.8, 0, 1) * np.clip((t1 - t) / 0.8, 0, 1)))
            return f

        src = data_tag(r"U.S.\ Energy Information Administration via FRED (MCOILBRENTEU, MCOILWTICO), monthly",
                       corner=DL, font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: Brent's premium over WTI, \ year by year (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"one price for oil? \ Brent and WTI, \ 1987--2026, \ under the gap as a tune")
            snd.show(src, stag)
            for m in grown.values():
                snd.drive(m, grow)
            snd.drive(year, set_year)
            for m, t0, t1 in notes:
                m.set_opacity(0)
                snd.drive(m, window(t0, t1))
            snd.show(top, bot, zero, *grown.values(), year, legend, *[m for m, _, _ in notes])
            self.play(FadeIn(top), FadeIn(bot), FadeIn(zero), FadeIn(legend), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (top, bot, zero, *grown.values(), year, legend, src, stag,
                                             *[m for m, _, _ in notes])], run_time=1.0)
            story = point_cards([
                (r"the box", r"every way to share; \\ the lens of gains", LENS),
                (r"the contract curve", r"equal rates of substitution: \\ Pareto efficient", CC),
                (r"prices", r"offer curves cross; \\ Walras's law", PRICE),
                (r"the core", r"shrinks to the price outcome \\ as traders multiply", CORE),
                (r"the first theorem", r"equilibrium is efficient, \\ if its assumptions hold", E.ACCENT),
                (r"the second", r"any efficient point, \\ by a lump-sum transfer", ANA),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
