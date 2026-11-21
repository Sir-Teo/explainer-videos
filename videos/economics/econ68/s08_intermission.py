from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ68.common import *  # noqa: F403


class Intermission(SoundScene):
    """Vehicles entering New York's Congestion Relief Zone, a seven-day average, day by day from January 2025 (MTA
    open data), with the holidays marked; under it, the entries as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        D, Bu, V, C = (load(x) for x in ("did", "buses", "vmt", "clock"))
        clip = ClipStore("econ68").load("intermission.melody")
        last = film["last"]
        ax = plane([0, last + 10], [300, 600], center=DOWN * 0.25 + LEFT * 0.4, x_length=11.4, y_length=5.2,
                   xticks=[0, 180, 360, 545, 680], yticks=[300, 400, 500, 600],
                   ylabel=r"vehicles entering the zone, \ thousands a day \ (seven-day average)",
                   xfmt=lambda v: {0: "Jan 2025", 180: "Jul 2025", 360: "Jan 2026", 545: "Jul 2026",
                                   680: "Nov 2026"}.get(int(v), ""), yfmt=lambda v: f"{v:.0f}", font_size=15)
        days, ts = np.array(film["days"], float), np.array(film["t"], float)
        pts = [ax.ax.c2p(x, y) for x, y in zip(days, film["avg"])]

        def grower(m, tt):
            k = int(np.searchsorted(ts, tt, side="right"))
            ps = pts[:max(k, 1)]
            if len(ps) < 2:
                ps = [pts[0], pts[0]]
            m.set_points_as_corners(ps)

        line = VMobject(stroke_color=PROD, stroke_width=2.8)
        line.set_points_as_corners([pts[0], pts[0]])
        marks = VGroup()
        avg = np.array(film["avg"], float)
        for when, txt in ((180, r"July 4th"), (354, r"Christmas"), (545, r"July 4th")):
            win = np.nonzero(np.abs(days - when) <= 8)[0]
            k = int(win[np.argmin(avg[win])])
            lab = label(txt, font_size=14, color=GREY_A).next_to(ax.ax.c2p(days[k], film["avg"][k]), DOWN, buff=0.12)
            lab.ft = float(ts[k])
            lab.set_opacity(0.0)
            marks.add(lab)
        src = data_tag(r"MTA, \ Congestion Relief Zone vehicle entries \ (data.ny.gov, \ t6yz-b64h)", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ entries, \ week by week \ (computed)", font_size=13, color=E.ACCENT).to_corner(
            UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"vehicles entering New York's congestion zone, \ a seven-day average, \ from January 2025; "
                        r"\ the entries as a tune")
            snd.show(src, stag)
            snd.drive(line, grower)
            for m in marks:
                snd.drive(m, lambda mm, tt: mm.set_opacity(1.0 if tt >= mm.ft else 0.0))
            snd.show(ax, line, marks)
            self.play(FadeIn(ax), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            line.clear_updaters()
            for m in marks:
                m.clear_updaters()
            self.play(*[FadeOut(m) for m in (ax, line, marks, src, stag)], run_time=1.0)
            n, f = C["nine"], C["five"]
            story = point_cards([
                (r"the question", r"what did New York's charge do, \ and how would an economist find out?", TOLL),
                (r"the data", r"crossings since 2019, \ entries since 2025, \ miles since 2024, \ bus speeds since "
                 r"2023", DATA),
                (r"the design", r"year-on-year comparisons with placebo years; \ a discontinuity in time", TRUE),
                (r"the tunnels", rf"{100 * D['effect']:.1f}\%; \ net of their earlier drift "
                 rf"{100 * D['adjusted']:.1f}\%".replace("-", "{-}"), CTRL),
                (r"buses and miles", rf"buses {100 * Bu['effect']:+.1f}\% against outside; \ miles in the zone "
                 rf"{100 * V['crz_change']:+.1f}\%".replace("-", "{-}"), BUS),
                (r"the clock", rf"+{100 * (np.exp(n['jump']) - 1):.0f}\% at 9 pm, \ "
                 rf"{100 * (np.exp(f['jump']) - 1):.0f}\% at 5 am".replace("-", "{-}"), MODEL),
            ], width=12.6, cols=3, font_size=19).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
