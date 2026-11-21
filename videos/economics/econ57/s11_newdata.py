from __future__ import annotations

from videos.economics.econ57.common import *  # noqa: F403


class NewData(VoiceoverScene):
    def construct(self):
        card(self, 9, r"New data", r"What can scraped prices, \ card payments and satellites see that surveys "
             r"cannot?", "Chapter nine. New data.", lit={2012: r"Henderson, \ Storeygard and Weil",
                                                         2016: r"Cavallo and Rigobon", 2024: r"Chetty et al."},
             scale=("person", "firm", "nation", "world"), horizon=("a day", "a year"))
        self.speed()
        self.studies()

    def speed(self):
        rows = [(r"GDP, \ first estimate", 0.92, FIRST), (r"payrolls", 0.62, FIRST),
                (r"jobless claims", 0.42, SPF), (r"card payments", 0.22, LATEST),
                (r"prices scraped online", 0.08, LATEST)]
        ax = plane([0, 1], [-0.5, len(rows) - 0.5], center=RIGHT * 0.6 + DOWN * 0.2, x_length=8.2,
                   y_length=4.6, xticks=[], yticks=[], xlabel=r"how long after the fact it arrives", ylabel=r"",
                   font_size=14)
        ends = VGroup(label(r"days", font_size=18, color=GREY_B).next_to(ax.ax.c2p(0, -0.5), DOWN, buff=0.15),
                      label(r"weeks", font_size=18, color=GREY_B).next_to(ax.ax.c2p(0.5, -0.5), DOWN, buff=0.15),
                      label(r"months", font_size=18, color=GREY_B).next_to(ax.ax.c2p(1, -0.5), DOWN, buff=0.15))
        bars = VGroup()
        names = VGroup()
        for k, (n_, v, c) in enumerate(rows):
            y = len(rows) - 1 - k
            p0, p1 = ax.ax.c2p(0, y - 0.28), ax.ax.c2p(v, y + 0.28)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=c,
                               fill_opacity=0.8).move_to((p0 + p1) / 2))
            names.add(label(n_, font_size=19, color=c).next_to(ax.ax.c2p(0, y), LEFT, buff=0.25))
        tag = note(r"schematic: \ the order of the typical delays, \ not their exact lengths", font_size=14,
                   color=E.SOURCE).to_corner(DL, buff=0.3)
        with self.voiceover(
            "Official statistics are careful and slow. <bookmark mark='a'/> A quarter's GDP arrives a month after "
            "it ends; payrolls a week after the month; claims for unemployment insurance a few days after the week. "
            "<bookmark mark='b'/> In the last fifteen years economists have added sources that arrive within days: "
            "card payments, and prices read off retailers' websites. They are not designed to be representative, "
            "and that is their price: they are fast, and they have to be checked against the slow numbers."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(ends), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(n_), GrowFromEdge(b_, LEFT)) for n_, b_ in
                                    zip(names[:3], bars[:3])], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(n_), GrowFromEdge(b_, LEFT)) for n_, b_ in
                                    zip(names[3:], bars[3:])], lag_ratio=0.4), run_time=2.0)
        self.clear_scene()

    def studies(self):
        cards = point_cards([
            (r"prices scraped online", r"Alberto Cavallo and Roberto Rigobon's Billion Prices Project: \ daily "
             r"prices from retailers' websites tracked official inflation in most countries, \ and showed "
             r"Argentina's official index understating inflation", LATEST),
            (r"card payments", r"Raj Chetty and coauthors built a public tracker from card and payroll data in "
             r"2020: \ spending by the richest fell most, \ in the places they lived, \ and low-wage jobs there "
             r"with it", SPF),
            (r"night lights", r"Vernon Henderson, \ Adam Storeygard and David Weil used the brightness of lights "
             r"seen from satellites to estimate growth where national accounts are weak", GB),
            (r"job postings", r"online vacancy ads, \ counted and read, \ give a daily view of labour demand by "
             r"occupation and skill", NOW),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.15)
        head = label(r"four new windows", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Cavallo and Rigobon, \ JEP 30(2) (2016); \ Chetty et al., \ QJE 139(2) (2024); \ "
                            r"Henderson, \ Storeygard and Weil, \ AER 102(2) (2012)", corner=DR, font_size=11)
        with self.voiceover(
            "Four of the new windows. <bookmark mark='a'/> Alberto Cavallo and Roberto Rigobon collected daily "
            "prices from retailers' websites across many countries. In most, online inflation tracked the official "
            "index closely; in Argentina it showed the official index understating inflation for years. <bookmark "
            "mark='b'/> In 2020 Raj Chetty and his coauthors built a public tracker from card payments and payroll "
            "records. It showed spending falling most among the richest, in the places they lived, and low-wage "
            "jobs disappearing there first. <bookmark mark='c'/> Vernon Henderson, Adam Storeygard and David Weil "
            "used the lights seen from satellites at night to measure growth where national accounts are weak. "
            "<bookmark mark='d'/> And online job postings, counted and read, show labour demand day by day. Each "
            "answers a question the official statistics answer late, or not at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
