from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ58.common import *  # noqa: F403


class Intermission(SoundScene):
    """Every baseline the Congressional Budget Office has published since 1984, each a thin line of its projected
    deficits drawn as its date arrives, against the deficits that happened; under it, the outcomes as a tune; then
    the story so far."""

    def construct(self):
        film = load("film")
        B, P, D, V = (load(x) for x in ("bridge", "playit", "discount", "vsl"))
        clip = ClipStore("econ58").load("intermission.melody")
        ax = plane([1983, 2036], [-16, 6], center=DOWN * 0.25 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1985, 1995, 2005, 2015, 2025, 2035], yticks=[-15, -10, -5, 0, 5],
                   ylabel=r"federal surplus or deficit, \ \% of GDP", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:+.0f}".replace("-", "{-}") if y else "0", font_size=15)
        z = DashedLine(ax.ax.c2p(1983, 0), ax.ax.c2p(2036, 0), color=GREY_C, stroke_width=1.2)
        lines = VGroup()
        for b in film["baselines"]:
            m = path(ax, b["fy"], np.clip(b["v"], -16, 6), CBO, 1.4, smooth=False)
            m.ft = b["t"]
            m.set_stroke(opacity=0.0)
            lines.add(m)
        at = np.array(film["actual_fy"], float)
        av = np.array(film["actual"], float)
        ats = np.array(film["actual_t"], float)
        pts = [ax.ax.c2p(x, max(y, -16)) for x, y in zip(at, av)]
        grow = VMobject(stroke_color=WHITE, stroke_width=3.2)
        grow.set_points_as_corners([pts[0], pts[0]])

        def grower(m, tt):
            k = int(np.searchsorted(ats, tt, side="right"))
            ps = pts[:max(k, 1)]
            if 0 < k < len(pts):
                f = float(np.clip((tt - ats[k - 1]) / (ats[k] - ats[k - 1]), 0, 1))
                ps = ps + [pts[k - 1] + f * (pts[k] - pts[k - 1])]
            if len(ps) < 2:
                ps = [ps[0], ps[0]]
            m.set_points_as_corners(ps)

        year = Integer(1984, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2030, 3.6))

        def set_year(m, tt):
            a, b = 1984.0, 2026.0
            m.set_value(int(np.clip(a + (tt - 2.0) / (FILM_SECONDS - 4.0) * (b - a), a, 2025)))

        key = VGroup(label(r"blue: \ each CBO baseline, \ as published", font_size=17, color=CBO),
                     label(r"white: \ what happened", font_size=17, color=WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.ax.c2p(1992, 4.2))
        src = data_tag(r"CBO, \ eval-projections", corner=DL, font_size=13).to_edge(UP, buff=0.12).to_edge(
            LEFT, buff=0.3)
        stag = note(r"sound: \ the deficit, \ 1984--2025 \ (computed)", font_size=13, color=E.ACCENT).to_corner(
            UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"every baseline the Congressional Budget Office published, \ "
                        rf"{film['first'][:4]}--{film['last'][:4]}, \ against the deficits that happened; \ "
                        r"the deficit as a tune")
            snd.show(src, stag)
            snd.drive(grow, grower)
            snd.drive(year, set_year)
            for m in lines:
                snd.drive(m, lambda mm, tt: mm.set_stroke(opacity=0.55 if tt >= mm.ft else 0.0))
            snd.show(ax, z, lines, grow, year, key)
            self.play(FadeIn(ax), FadeIn(z), FadeIn(key), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            for m in lines:
                m.clear_updaters()
            self.play(*[FadeOut(m) for m in (ax, z, lines, grow, year, key, src, stag)], run_time=1.0)
            b35 = B["by_rate"]["0.035"]["npv"]
            story = point_cards([
                (r"the sentence", r"benefits `to whomsoever they may accrue' \ must exceed the costs", E.ACCENT),
                (r"surplus", rf"the bridge: \ time, \ new trips, \ lives; \ Bo's fares net out; \ NPV {b35:+.0f}"
                 .replace("-", "{-}"), TRAV),
                (r"no prices", r"noise from houses, \ a beach from trips, \ birds from surveys", NOISE),
                (r"a statistical life", rf"\$9 million on the Island; \ without ability held fixed, \ "
                 rf"{V['naive']:.1f}", SAFE),
                (r"Play it", rf"the higher rate raises {P['behavioural']:.0f}, \ not {P['static']:.0f}", BEHAV),
                (r"the rate decides", rf"the bridge: \ {D['bridge']['0.030']:+.0f} at 3\%, \ "
                 rf"{D['bridge']['0.070']:+.0f} at 7\%".replace("-", "{-}"), RATE),
            ], width=12.6, cols=3, font_size=20).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
