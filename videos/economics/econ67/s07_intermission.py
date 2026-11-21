from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ67.common import *  # noqa: F403


class Intermission(SoundScene):
    """Britain's public debt as a share of GDP, 1870-2020 (the Jordà-Schularick-Taylor Macrohistory Database), drawn
    year by year with the wars marked and the 90% line of Reinhart and Rogoff; under it, the debt as a tune that
    rises with it; then the story so far."""

    def construct(self):
        film = load("film")
        C, R, Dd, M = (load(x) for x in ("camel", "replication", "designs", "meta"))
        clip = ClipStore("econ67").load("intermission.melody")
        ax = plane([1865, 2025], [0, 300], center=DOWN * 0.25 + LEFT * 0.4, x_length=11.4, y_length=5.2,
                   xticks=[1880, 1900, 1920, 1940, 1960, 1980, 2000, 2020], yticks=[0, 50, 90, 150, 200, 250, 300],
                   ylabel=r"public debt, \ percent of GDP", xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.0f}",
                   font_size=15)
        ninety = seg(ax, 1865, 90, 2025, 90, FAIL, 1.6, dashed=True)
        nl = label(r"90\%", font_size=14, color=FAIL).next_to(ax.ax.c2p(2025, 90), RIGHT, buff=0.08)
        yrs, ts = np.array(film["years"], float), np.array(film["t"], float)
        pts = [ax.ax.c2p(x, y) for x, y in zip(yrs, film["debt"])]

        def grower(m, tt):
            k = int(np.searchsorted(ts, tt, side="right"))
            ps = pts[:max(k, 1)]
            if len(ps) < 2:
                ps = [pts[0], pts[0]]
            m.set_points_as_corners(ps)

        line = VMobject(stroke_color=PROD, stroke_width=3.0)
        line.set_points_as_corners([pts[0], pts[0]])
        marks = VGroup()
        for when, txt, dx, dy in ((1916, r"the First World War", -8, 70), (1946, r"1946: \ the peak", 3, 22),
                                  (1975, r"growth through the debt's long fall", 14, 115),
                                  (2009, r"2008: \ the financial crisis", -12, 55)):
            k = int(np.argmin(np.abs(yrs - when)))
            lab = label(txt, font_size=14, color=GREY_A).move_to(ax.ax.c2p(yrs[k] + dx, film["debt"][k] + dy))
            lab.ft = film_time(float(yrs[k]))
            lab.set_opacity(0.0)
            marks.add(lab)
        yr = Integer(1870, font_size=48, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1895, 240))

        def set_year(m, tt):
            a, b = FILM_YEARS
            m.set_value(int(np.clip(a + (tt - 2.0) / (FILM_SECONDS - 4.0) * (b - a), a, b)))

        src = data_tag(r"Jord\`a, \ Schularick and Taylor, \ Macrohistory Database: \ United Kingdom, \ debtgdp",
                       corner=DL, font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the debt, \ year by year, \ 1870--2020 \ (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"Britain's public debt as a share of GDP, \ 1870--2020, \ with Reinhart and Rogoff's 90\% "
                        r"line; \ the debt as a tune")
            snd.show(src, stag)
            snd.drive(line, grower)
            snd.drive(yr, set_year)
            for m in marks:
                snd.drive(m, lambda mm, tt: mm.set_opacity(1.0 if tt >= mm.ft else 0.0))
            snd.show(ax, ninety, nl, line, yr, marks)
            self.play(FadeIn(ax), FadeIn(ninety), FadeIn(nl), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            for m in [line, yr, *marks]:
                m.clear_updaters()
            stat = label(rf"years above 90\%: \ {film['n_hi']}, \ growth {film['g_hi']:.1f}\% a year \\ below 90\%: "
                         rf"\ {film['g_lo']:.1f}\% \\ peacetime years above 90\%: \ {film['g_hi_peace']:.1f}\%",
                         font_size=16, color=PROD).next_to(ax.ax.c2p(2025, 300), DL, buff=0.1)
            self.play(FadeIn(stat), run_time=0.8)
            self.wait(2.5)
            self.play(*[FadeOut(m) for m in (ax, ninety, nl, line, yr, marks, src, stag, stat)], run_time=1.0)
            b = Dd["designs"]
            story = point_cards([
                (r"the camel", rf"published results: \ {C['caliper']['ratio']:.1f} just above 1.96 per one just "
                 rf"below; \ first tries: \ {C['caliper_first']['ratio']:.1f}", PUB),
                (r"Play it", r"results just past the line replicate about half the time", TRUE),
                (r"the laboratories", rf"11 of 18 replicated, \ effects two thirds as large; \ the simulated field: "
                 rf"{100 * R['rate']:.0f}\%", FIRST),
                (r"reproduction", r"from the files alone, \ fewer than half of papers in 2015; \ now checked before "
                 r"publication", STATE),
                (r"designs", rf"missing insignificant results: \ trials {100 * (1 - b['RCT']['beta']):.0f}\%, \ "
                 rf"instruments {100 * (1 - b['IV']['beta']):.0f}\%", FAIL),
                (r"correction", rf"the selection model recovers {M['ak']['theta']:.3f} against a truth of "
                 rf"{M['theta']:.3f}".replace("-", "{-}"), ROW),
            ], width=12.6, cols=3, font_size=19).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
