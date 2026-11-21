from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ66.common import *  # noqa: F403


class Intermission(SoundScene):
    """The US trade balance in goods and services, monthly since 1992 (Census and BEA via FRED), drawn month by month,
    with the rush to import before the 2025 tariffs marked; under it, the balance as a tune that falls as the deficit
    deepens; then the story so far."""

    def construct(self):
        film = load("film")
        F, E_, B, S = (load(x) for x in ("formula", "effective", "bloc", "scenarios"))
        clip = ClipStore("econ66").load("intermission.melody")
        ax = plane([1991, 2027.5], [-145, 10], center=DOWN * 0.25 + LEFT * 0.4, x_length=11.4, y_length=5.2,
                   xticks=[1995, 2000, 2005, 2010, 2015, 2020, 2025], yticks=[-140, -120, -100, -80, -60, -40, -20, 0],
                   ylabel=r"trade balance, \ goods and services, \ billions of dollars a month",
                   xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.0f}".replace("-", "{-}"), font_size=15)
        zero = seg(ax, 1991, 0, 2027.5, 0, GREY_C, 1.5)
        yrs, ts = np.array(film["years"], float), np.array(film["t"], float)
        pts = [ax.ax.c2p(x, y) for x, y in zip(yrs, film["balance"])]

        def grower(m, tt):
            k = int(np.searchsorted(ts, tt, side="right"))
            ps = pts[:max(k, 1)]
            if len(ps) < 2:
                ps = [pts[0], pts[0]]
            m.set_points_as_corners(ps)

        line = VMobject(stroke_color=PROD, stroke_width=2.6)
        line.set_points_as_corners([pts[0], pts[0]])
        marks = VGroup()
        for when, txt, y_off in ((2006.5, r"2006: \ the housing boom", 14), (2020.3, r"2020: \ the pandemic", 22),
                                 (2025.17, r"March 2025: \ the rush \\ before the tariffs", 18)):
            k = int(np.argmin(np.abs(yrs - when)))
            lab = label(txt, font_size=14, color=GREY_A).next_to(ax.ax.c2p(yrs[k], film["balance"][k] - y_off),
                                                                 DOWN, buff=0.02)
            lab.ft = film_time(float(yrs[k]))
            lab.set_opacity(0.0)
            marks.add(lab)
        yr = Integer(1992, font_size=48, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1999, -110))

        def set_year(m, tt):
            a, b = FILM_YEARS
            m.set_value(int(np.clip(a + (tt - 2.0) / (FILM_SECONDS - 4.0) * (b - a), a, 2026)))

        src = data_tag(r"Census and BEA via FRED: \ BOPGSTB", corner=DL, font_size=13).to_edge(UP, buff=0.12).to_edge(
            LEFT, buff=0.3)
        stag = note(r"sound: \ the balance, \ quarter by quarter, \ 1992--2026 \ (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the US trade balance in goods and services, \ monthly since 1992, \ with the rush to import "
                        r"before the 2025 tariffs; \ the balance as a tune")
            snd.show(src, stag)
            snd.drive(line, grower)
            snd.drive(yr, set_year)
            for m in marks:
                snd.drive(m, lambda mm, tt: mm.set_opacity(1.0 if tt >= mm.ft else 0.0))
            snd.show(ax, zero, line, yr, marks)
            self.play(FadeIn(ax), FadeIn(zero), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            for m in [line, yr, *marks]:
                m.clear_updaters()
            self.play(*[FadeOut(m) for m in (ax, zero, line, yr, marks, src, stag)], run_time=1.0)
            n4 = [x for x in S["rows"] if x["theta"] == 4.0]
            story = point_cards([
                (r"the formula", rf"Vietnam: \ {100 * F['raw']:.0f}\% halved to {100 * F['rate']:.0f}\%; \ with "
                 rf"realistic pass-through, \ {100 * F['rate_945']:.0f}\%", TARIFF),
                (r"who paid", rf"importers and buyers at home, \ in 2018 and in 2025; \ the effective rate peaked "
                 rf"at {100 * E_['peak']:.1f}\%", PRICE),
                (r"Play it", r"a tariff pays only against a partner who never answers; \ free trade wins on "
                 r"average", US),
                (r"the war", rf"optimal tariff {100 * B['optimal']:.0f}\%; \ at the Nash tariffs both lose: \ US "
                 rf"{100 * B['nash_us']:.2f}\%".replace("-", "{-}"), STATE),
                (r"the model", rf"15\% for everyone: \ US {100 * n4[0]['us']:+.2f}\% alone, \ "
                 rf"{100 * n4[1]['us']:+.2f}\% with retaliation".replace("-", "{-}"), ROW),
                (r"deficits", r"saving minus investment; \ bilateral balances measure nothing a tariff should fix",
                 FREE),
            ], width=12.6, cols=3, font_size=19).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
