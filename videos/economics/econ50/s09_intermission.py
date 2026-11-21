from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ50.common import *  # noqa: F403


class Intermission(SoundScene):
    """The official poverty rate of American children, year by year since 1989, drawn as the years pass; under it,
    the series as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        R = load("record")
        S = load("schedules")
        I = load("island")
        B = load("budget")
        A = tables.ALLOWANCE_50.data
        clip = ClipStore("econ50").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["v"], float)
        events = ((float(t[0]), rf"{int(t[0])}: \ {film['first']:.1f}\%", DR),
                  (float(film["peak_t"]), rf"{int(film['peak_t'])}: \ {film['peak']:.1f}\%", UP),
                  (2000.0, rf"2000: \ {float(np.interp(2000, t, v)):.1f}\%", DOWN),
                  (2010.0, rf"2010: \ {float(np.interp(2010, t, v)):.1f}\%", UP),
                  (2021.0, rf"2021: \ {film['v2021']:.1f}\%", UP),
                  (float(t[-1]), rf"{int(t[-1])}: \ {film['last']:.1f}\%", DOWN))
        ax = plane([1988, 2026], [0, 25], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025], yticks=[0, 5, 10, 15, 20, 25],
                   ylabel=r"American children below the official poverty line, \ \%", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=15)
        year = Integer(int(t[0]), font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2018, 23))
        t0, t1 = film_time(t[0]), film_time(t[-1])
        grow = VMobject(stroke_color=POOR, stroke_width=3.4)
        pts = [ax.ax.c2p(x, y) for x, y in zip(t, v)]
        grow.set_points_as_corners([pts[0], pts[0]])

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

        def set_year(m, tt):
            m.set_value(int(np.clip(t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0]), t[0], t[-1])))

        marks = VGroup()
        for x, n, d in events:
            y = float(np.interp(x, t, v))
            m = label(n, font_size=16, color=GREY_A).next_to(ax.ax.c2p(x, y), d, buff=0.2)
            m.ft = film_time(x)
            marks.add(m)
        spm = VGroup(*[Dot(ax.ax.c2p(int(k), val), radius=0.07, color=SPM) for k, val in R["spm"].items()])
        spm.ft = film_time(2021)
        spm_l = label(r"green: \ the SPM, \ which counts tax credits", font_size=15, color=SPM).next_to(
            ax.ax.c2p(2012, 4), DOWN, buff=0.1)
        spm_l.ft = film_time(2021)
        src = data_tag(r"Census SAIPE, \ via FRED (PPU18US00000A156NCEN); \ SPM: \ Census (2022, 2023)", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the series \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"American children below the official line, \ 1989--2024, \ estimated from the American "
                        r"Community Survey; \ the value as a tune")
            snd.show(src, stag)
            snd.drive(grow, grower)
            snd.drive(year, set_year)
            for m in (*marks, spm, spm_l):
                snd.drive(m, lambda mm, tt: mm.set_opacity(1.0 if tt >= mm.ft else 0.0))
            snd.show(ax, grow, year, marks, spm, spm_l)
            self.play(FadeIn(ax), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            self.play(*[FadeOut(m) for m in (ax, grow, year, marks, spm, spm_l, src, stag)], run_time=1.0)
            story = point_cards([
                (r"the question", r"the 2021 design, \ permanent, \ against the old credit", NEW),
                (r"one family", rf"\${S['at0_new']:,.0f} more at no earnings; \ a tenth less reward for work"
                 .replace(",", "{,}"), CHILD),
                (r"the dials", r"participation 0.25 \ (0 to 0.5); \ the cost of funds; \ the MVPF", WORK),
                (r"take-up", r"the poorest file least: \ incomplete claims save money by missing them", HOLD),
                (r"the budget", rf"\${I['per_child']:,.0f} a child; \ responses add {100 * B['fe_share']:.1f}\%"
                 .replace(",", "{,}"), BUDGET),
                (r"the evidence", rf"no fall in work in 2021 or in Canada; \ a model says {A['exit_share']}\% leave",
                 EVIDENCE),
            ], width=12.6, cols=3, font_size=21).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
