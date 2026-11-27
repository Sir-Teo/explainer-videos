from __future__ import annotations

from videos.industry.industry24.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.empire()
        self.railway()
        self.output()
        self.title()

    def empire(self):
        H = R["hook"]
        frame = draw.skyscraper_frame(floors=34, w=1.5, floor_h=0.14).move_to([-3.8, -0.2, 0])
        frame.align_to([0, -3.0, 0], DOWN)
        crane = draw.tower_crane(1.6).scale(0.9)
        crane.next_to(frame.floors[16], RIGHT, buff=-0.6).align_to(frame.floors[16], DOWN)
        c = stat_cards([("17 March 1930", "ground broken", BUILD), ("1 May 1931", f"opened: {H['days']} days later", BUILD)],
                       y=1.6, size=34, span=7.0)
        c.shift(RIGHT * 2.6)
        c2 = stat_cards([(f"{H['floors']} floors", f"{get('esb.height'):,.0f} feet to the tip of its antenna", ALL),
                         (f"{H['stories']} a week", "storeys of steel frame at the peak", PRICE)], y=-1.0, size=34, span=7.0)
        c2.shift(RIGHT * 2.6)
        src = source("Empire State Building, fact sheet", size=12)
        beat(self,
             "In March 1930, on Fifth Avenue in New York, builders broke ground for the Empire State Building. "
             "<bookmark mark='a'/> On the first of May 1931, President Hoover pressed a button in Washington and the "
             f"building opened: {H['days']} days after the ground was broken. <bookmark mark='b'/> It has {H['floors']} "
             f"floors. <bookmark mark='c'/> At its fastest, its steel frame rose {H['stories']} storeys a week, and the "
             f"whole thing took more than {H['hours']} million hours of work.",
             base=[frame.floors[0], VGroup(frame[0]), src],
             steps=[[c[0], *frame.floors[1:12]], [c[1], *frame.floors[12:24], crane], [c2[0], *frame.floors[24:]], c2[1]])

    def railway(self):
        H = R["hook"]
        items = [("2008: the whole line, Los Angeles to San Francisco", H["hsr08"], GOOD, f"${H['hsr08']:.0f}bn"),
                 ("2026: Phase 1, by a cheaper route, finished 2039", H["phase1"], PRICE, f"${H['phase1']:.1f}bn"),
                 ("2026: Phase 1 as first designed", H["full"], BAD, f"${H['full']:.1f}bn")]
        rows = hbars(items, max_value=240, x0=-1.0, top=1.3, row=1.0, length=6.0, size=16, bar_h=0.5)
        lab = tx("California's high-speed railway: the estimated cost", 17, GREY_A).to_edge(UP, buff=0.8)
        note = tx(f"first stretch, Merced to Bakersfield: ${H['mb']:.1f}bn, finished {H['mb_done']}", 18, WHITE, bold=True).move_to([0, -2.2, 0])
        src = source("California High-Speed Rail Authority, Business Plans of November 2008 and 2026", size=12)
        beat(self,
             "Now a project of our own century. <bookmark mark='a'/> In November 2008 California's high-speed rail "
             f"authority said its line from Los Angeles to San Francisco would cost about {H['hsr08']} billion dollars. "
             f"<bookmark mark='b'/> Its 2026 plan puts the first phase at {H['phase1']:.1f} billion, using existing tracks "
             f"for part of the way, with completion in {H['p1_done']}. <bookmark mark='c'/> Built as first designed, "
             f"{H['full']:.1f} billion. <bookmark mark='d'/> The first stretch, in the Central Valley, between Merced and "
             f"Bakersfield, is now due in {H['mb_done']}. Some of those numbers are in dollars of different years; none of "
             "the difference is small.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1], rows[2], note])

    def output(self):
        P = R["productivity"]
        ch = line_chart({"manufacturing": (P["per"]["manufacturing"], MAKE), "whole economy": (P["per"]["all"], ALL),
                         "construction": (P["per"]["construction"], BUILD)},
                        x=(1970, 2025), y=(0, 6), xticks=[1970, 1980, 1990, 2000, 2010, 2020, 2025], yticks=[0, 1, 2, 3, 4, 5, 6],
                        yfmt=lambda v: f"x{v:.0f}", ylabel="real output per worker, 1970 = 1", width=9.4, height=4.4,
                        center=(-0.9, -0.45))
        one = DashedLine(ch.ax.c2p(1970, 1), ch.ax.c2p(2025, 1), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        src = source("BEA, real value added by industry (chain-type quantity indexes, 1947-2025, linked at 1997); BLS "
                     "employment via FRED; whole economy: real GDP per nonfarm job", size=12)
        beat(self,
             "And the strangest picture in this series. <bookmark mark='a'/> Since 1970, what an American factory worker "
             f"produces, measured in real terms, has grown {P['per']['manufacturing'][2025]:.1f} times. "
             f"<bookmark mark='b'/> Across the whole economy, about {P['per']['all'][2025]:.0f} times. "
             "<bookmark mark='c'/> In construction it has fallen: by this measure, a construction worker in 2025 "
             f"produced {P['per']['construction'][2025]:.2f} of what one produced in 1970. By this measure construction "
             "has gone backwards while most of the economy moved forward, and this film is about why.",
             base=[ch.frame, one, src], steps=[[ch.lines["manufacturing"], ch.labels["manufacturing"]],
                                               [ch.lines["whole economy"], ch.labels["whole economy"]],
                                               [ch.lines["construction"], ch.labels["construction"]]])

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part twenty-four: construction. Why has almost everything become cheaper to "
                            "make, except a building?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
