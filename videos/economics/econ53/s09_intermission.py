from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ53.common import *  # noqa: F403


class Intermission(SoundScene):
    """What American households expected inflation to be over the next year (the University of Michigan's survey
    median), against what it was, month by month since 1978; under it, the expectations as a tune; then the story
    so far."""

    def construct(self):
        film = load("film")
        Pr, Ct, D = (load(x) for x in ("prosecutor", "cheap", "design"))
        clip = ClipStore("econ53").load("intermission.melody")
        t = np.array(film["t"], float)
        ex = np.array(film["expected"], float)
        ac = np.array(film["actual"], float)
        ax = plane([1977, 2027], [-3, 15], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1980, 1990, 2000, 2010, 2020], yticks=[0, 5, 10, 15], ylabel=r"inflation, \ \%",
                   xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.0f}", font_size=15)
        zero = DashedLine(ax.ax.c2p(1977, 0), ax.ax.c2p(2027, 0), color=GREY_D, stroke_width=1.2)
        year = Integer(int(t[0]), font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2004, 13))
        t0, t1 = film_time(t[0]), film_time(t[-1])
        pts_e = [ax.ax.c2p(x, y) for x, y in zip(t, ex)]
        pts_a = [ax.ax.c2p(x, y) for x, y in zip(t, ac)]
        grow_e = VMobject(stroke_color=BELIEF, stroke_width=3.2)
        grow_a = VMobject(stroke_color=GREY_B, stroke_width=2.0)
        grow_e.set_points_as_corners([pts_e[0], pts_e[0]])
        grow_a.set_points_as_corners([pts_a[0], pts_a[0]])

        def make(pts):
            def grower(m, tt):
                yr = float(np.clip(t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0]), t[0], t[-1]))
                k = int(np.searchsorted(t, yr, side="right"))
                ps = pts[:max(k, 1)]
                if k < len(t):
                    f = (yr - t[k - 1]) / (t[k] - t[k - 1])
                    ps = ps + [pts[k - 1] + f * (pts[k] - pts[k - 1])]
                if len(ps) < 2:
                    ps = [ps[0], ps[0]]
                m.set_points_as_corners(ps)
            return grower

        def set_year(m, tt):
            m.set_value(int(np.clip(t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0]), t[0], t[-1])))

        key = VGroup(label(r"purple: \ what households expected for the year ahead", font_size=17, color=BELIEF),
                     label(r"grey: \ inflation over the past year", font_size=17, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to(ax.ax.c2p(2013, 10.5))
        pk = ax.ax.c2p(film["peak_expected_t"], film["peak_expected"])
        pk_lab = label(rf"{film['peak_expected_t']:.0f}: \ expected {film['peak_expected']:.1f}\%", font_size=17,
                       color=BELIEF)
        pk_lab.next_to(ax.ax.c2p(film["peak_expected_t"] + 5.5, film["peak_expected"] + 1.6), RIGHT, buff=0)
        marks = VGroup(VGroup(pk_lab, Line(pk + RIGHT * 0.08, pk_lab.get_left() + LEFT * 0.06, color=BELIEF,
                                           stroke_width=1.2)))
        marks[0].ft = film_time(film["peak_expected_t"])
        src = data_tag(r"University of Michigan, \ Surveys of Consumers; \ BLS CPI; \ via FRED", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the expectations \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the median household's expected inflation for the next twelve months, \ and inflation over "
                        r"the past twelve, \ 1978--2026; \ the expectations as a tune")
            snd.show(src, stag)
            snd.drive(grow_e, make(pts_e))
            snd.drive(grow_a, make(pts_a))
            snd.drive(year, set_year)
            for m in marks:
                snd.drive(m, lambda mm, tt: mm.set_opacity(1.0 if tt >= mm.ft else 0.0))
            snd.show(ax, zero, grow_a, grow_e, year, marks, key)
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(key), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            self.play(*[FadeOut(m) for m in (ax, zero, grow_a, grow_e, year, marks, key, src, stag)], run_time=1.0)
            r05 = next(r for r in Ct["rows"] if abs(r["b"] - 0.05) < 1e-9)
            story = point_cards([
                (r"the prosecutor", rf"flag 3 in 7 innocent: \ {100 * Pr['optimal']:.0f}\% convicted, \ nobody fooled",
                 SENDER),
                (r"Bayesian games", r"play each type's best response, \ on average over the others", RECEIVER),
                (r"beliefs off the path", r"beer or quiche: \ the intuitive criterion keeps only beer", BELIEF),
                (r"cheap talk", rf"a bias of 0.05: \ {r05['N']} messages; \ a quarter: \ babble", SIGNAL),
                (r"persuasion", r"the concave closure of the sender's value, \ at the prior", SENDER),
                (r"many receivers", rf"obedient recommendations: \ {D['best']:.1f} investors, \ not {D['full']:.1f}",
                 THEORY),
            ], width=12.6, cols=3, font_size=21).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
