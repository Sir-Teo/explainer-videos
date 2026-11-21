from __future__ import annotations

import datetime as dt

from videos.economics.econ68.common import *  # noqa: F403


def month_x(m: str) -> float:
    return int(m[:4]) + (int(m[5:7]) - 0.5) / 12


class Data(VoiceoverScene):
    def construct(self):
        card(self, 2, r"The data", r"What does the transit authority publish, \ and what do the numbers look like "
             r"before any estimate?", "Chapter two. The data.", scale=("city",), horizon=("a day", "a year"))
        self.sources()
        self.entries()
        self.crossings()

    def sources(self):
        cards = point_cards([
            (r"crossings, \ 2019--", r"vehicles on the authority's ten bridges and tunnels, \ every hour, \ by "
             r"direction: \ two tunnels lead into the zone", CTRL),
            (r"entries, \ 2025--", r"vehicles entering the zone, \ every ten minutes, \ by class and entry point: \ "
             r"only after the charge began", TOLL),
            (r"miles driven, \ 2024--", r"daily vehicle-miles inside the zone and on its two free highways, \ by "
             r"month", DATA),
            (r"bus speeds, \ 2023--", r"miles and hours of every route inside and outside the business district, \ "
             r"by month and hour", BUS),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"four public datasets", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = data_tag(r"MTA open data on data.ny.gov: \ ebfx-2m7v, \ t6yz-b64h, \ jbxx-kxff, \ r6db-kkzj \ (retrieved "
                       r"21 November 2026)", corner=DL, font_size=12)
        with self.voiceover(
            "The data come first, and they are public. <bookmark mark='a'/> Hourly crossings of the transit "
            "authority's ten bridges and tunnels since 2019; two of the tunnels lead straight into the zone. "
            "<bookmark mark='b'/> Entries into the zone every ten minutes, by type of vehicle and entry point, which "
            "exist only since the charge began. <bookmark mark='c'/> Miles driven each day in the zone and on its "
            "two free highways, since 2024. <bookmark mark='d'/> And bus speeds, route by route, inside and outside "
            "the business district, since 2023. Each file was reduced by a query written down in the Data Room, so "
            "anyone can rebuild it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def entries(self):
        E = load("entries")
        days = [(dt.date.fromisoformat(d) - dt.date(2025, 1, 5)).days for d in E["date"]]
        last = max(days)
        ax = plane([0, last + 5], [0, 700], center=LEFT * 0.9 + DOWN * 0.3, x_length=10.4, y_length=4.6,
                   xticks=[0, 180, 360, 540, 680], yticks=[0, 200, 400, 600],
                   ylabel=r"vehicles entering the zone, \ thousands a day",
                   xfmt=lambda v: {0: "Jan 2025", 180: "Jul 2025", 360: "Jan 2026", 540: "Jun 2026",
                                   680: "Nov 2026"}.get(int(v), ""), yfmt=lambda v: f"{v:.0f}", font_size=14)
        pts = VGroup(*[Dot(ax.ax.c2p(x, a / 1000), radius=0.022,
                           color=DATA if dt.date.fromisoformat(d).weekday() < 5 else GREY_B)
                       for x, a, d in zip(days, E["all"], E["date"])])
        key = legend_rows([(DATA, "weekdays"), (GREY_B, "weekends and holidays")], font_size=15).next_to(
            ax.ax.c2p(last, 690), DL, buff=0.1)
        side = label(rf"weekday average: \ {E['weekday_all'] / 1000:.0f},000 \ ({100 * E['car_share']:.0f}\% cars, "
                     r"pickups and vans)", font_size=18, color=DATA).to_edge(DOWN, buff=0.35)
        tag = data_tag(r"MTA, \ Congestion Relief Zone vehicle entries", corner=UL, font_size=12)
        with self.voiceover(
            "Describe before estimating. <bookmark mark='a'/> Here is every day since the charge began: the "
            "vehicles entering the zone. Weekdays, in gold, sit in a band near half a million; weekends and holidays "
            "fall below. <bookmark mark='b'/> On an average weekday "
            f"{E['weekday_all'] / 1000:.0f} thousand vehicles enter, and {100 * E['car_share']:.0f} percent of all "
            "entries are cars, pickups and vans. <bookmark mark='c'/> Notice what this chart cannot show: there is "
            "no before. Entries were first counted when the cameras started charging, so this file alone can never "
            "say what the charge did."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.002), FadeIn(key), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side))
            vo.wait_until("c")
            self.play(Indicate(ax.ax.get_y_axis() if hasattr(ax.ax, "get_y_axis") else ax.ax, color=TOLL))
        self.clear_scene()

    def crossings(self):
        X = load("crossings")
        xs = [month_x(m) for m in X["months"]]
        ax = plane([2019, 2027], [0, 125], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.6, y_length=4.8,
                   xticks=[2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027], yticks=[0, 25, 50, 75, 100, 125],
                   ylabel=r"weekday traffic, \ 2019 = 100", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        start = vline(ax, 2025.01, 0, 125, TOLL, 2.2)
        sl = label(r"the charge", font_size=15, color=TOLL).next_to(ax.ax.c2p(2025.01, 125), UP, buff=0.05)
        lt = path(ax, xs, X["treated"], TOLL, 3.0, smooth=False)
        lc = path(ax, xs, X["control"], CTRL, 3.0, smooth=False)
        key = legend_rows([(TOLL, r"the two tunnels into the zone, \\ toward Manhattan"),
                           (CTRL, f"{X['n_controls']} directions of \\ other crossings")], font_size=15).next_to(
            ax.ax, RIGHT, buff=0.3).shift(UP * 1.2)
        if key.get_right()[0] > 6.9:
            key.scale_to_fit_width(6.9 - key.get_left()[0])
        side = VGroup(
            label(r"the pandemic's hole, \\ and a recovery", font_size=17, color=GREY_A),
            label(r"the tunnels recover more, \\ then slip back from 2023: \\ before the charge", font_size=17,
                  color=TOLL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(key, DOWN, buff=0.5).align_to(key, LEFT)
        tag = data_tag(r"MTA, \ Bridges and Tunnels hourly crossings, \ weekday averages by month", corner=DL,
                       font_size=12)
        with self.voiceover(
            "The crossings have a before. <bookmark mark='a'/> Weekday traffic by month since 2019, each group "
            "indexed to its 2019 level: in red, the two tunnels whose Manhattan-bound lanes lead into the zone; in "
            f"blue, {X['n_controls']} directions of crossings elsewhere in the city. <bookmark mark='b'/> First the "
            "pandemic's hole in 2020, and a recovery, stronger in the tunnels. <bookmark mark='c'/> Then something to "
            "write down before estimating anything: from 2023 the tunnels' traffic slips back relative to the other "
            "crossings, two years before the charge. Whatever design we use will have to deal with it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(start), FadeIn(sl))
            vo.wait_until("a")
            self.play(Create(lc), Create(lt), FadeIn(key), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
        self.clear_scene()
