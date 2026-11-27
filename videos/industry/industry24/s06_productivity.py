from __future__ import annotations

from videos.industry.industry24.common import *  # noqa: F403


class Productivity(VoiceoverScene):
    def construct(self):
        card(self, 5, "Why building has not got cheaper", "Why does construction not get more productive?",
             "Chapter five. Why building has not got cheaper. The opening showed construction's output per worker "
             "falling since 1970. Here is the evidence in more detail, and the reasons people give.", lit=("make", "change"))
        self.workers()
        self.prices()
        self.materials()
        self.why()

    def workers(self):
        P = R["productivity"]
        j = P["jobs"]
        items = [("construction jobs, 1970", j["construction"][0] / 1e3, GREY_B, f"{j['construction'][0] / 1e3:.1f}m"),
                 ("construction jobs, 2025", j["construction"][1] / 1e3, BUILD, f"{j['construction'][1] / 1e3:.1f}m"),
                 ("manufacturing jobs, 1970", j["manufacturing"][0] / 1e3, GREY_B, f"{j['manufacturing'][0] / 1e3:.1f}m"),
                 ("manufacturing jobs, 2025", j["manufacturing"][1] / 1e3, MAKE, f"{j['manufacturing'][1] / 1e3:.1f}m")]
        rows = hbars(items, max_value=20, x0=-0.2, top=1.8, row=0.72, length=6.0, size=17, bar_h=0.42)
        out = VGroup(tx(f"real output: construction x{P['real']['construction']:.1f}", 20, BUILD, bold=True),
                     tx(f"real output: manufacturing x{P['real']['manufacturing']:.1f}", 20, MAKE, bold=True)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -1.7, 0])
        src = source("BLS employment via FRED; BEA real value added by industry, 1970 to 2025", size=12)
        beat(self,
             "Two numbers make the picture. <bookmark mark='a'/> Since 1970 the number of people working in American "
             f"construction has grown from {j['construction'][0] / 1e3:.1f} million to {j['construction'][1] / 1e3:.1f} "
             f"million, <bookmark mark='b'/> while manufacturing jobs fell from {j['manufacturing'][0] / 1e3:.1f} million "
             f"to {j['manufacturing'][1] / 1e3:.1f}. <bookmark mark='c'/> Over the same years construction's real output, "
             f"its value added after allowing for prices, grew {P['real']['construction']:.1f} times, and manufacturing's "
             f"{P['real']['manufacturing']:.1f} times. More than twice the workers, for less than one and a half times the "
             "output.",
             base=[rows.axis, src], steps=[rows[:2], rows[2:], out])

    def prices(self):
        P = R["productivity"]
        ch = line_chart({"construction": (P["price"]["construction"], BUILD), "whole economy": (P["price"]["all"], ALL),
                         "manufacturing": (P["price"]["manufacturing"], MAKE)},
                        x=(1970, 2025), y=(0, 20), xticks=[1970, 1980, 1990, 2000, 2010, 2020, 2025], yticks=[0, 5, 10, 15, 20],
                        yfmt=lambda v: f"x{v:.0f}", ylabel="price of each industry's output, 1970 = 1", width=9.4, height=4.4,
                        center=(-0.9, -0.45))
        src = source("BEA, chain-type price indexes for value added by industry, 1947-2025 linked at 1997", size=12)
        beat(self,
             "And the other side of the same coin is the price. <bookmark mark='a'/> The price of what manufacturing "
             f"produces has risen {P['price']['manufacturing'][2025]:.1f} times since 1970; prices across the whole "
             f"economy {P['price']['all'][2025]:.1f} times. <bookmark mark='b'/> The price of what construction produces "
             f"has risen {P['price']['construction'][2025]:.0f} times. When an industry's output per worker does not grow, "
             "while everyone else's pay does, what it makes gets dearer, year after year. That is the answer to this film's "
             "question, in one chart: what factories make has risen in price far less than prices in general, and what "
             "builders make far more.",
             base=[ch.frame, src], steps=[[ch.lines["manufacturing"], ch.labels["manufacturing"], ch.lines["whole economy"],
                                           ch.labels["whole economy"]], [ch.lines["construction"], ch.labels["construction"]]])

    def materials(self):
        M = R["materials"]
        ch = line_chart({"construction materials": (M["ppi"], BAD), "consumer prices": (M["cpi"], ALL)}, x=(2015, 2025),
                        y=(0.8, 1.6), xticks=[2015, 2017, 2019, 2021, 2023, 2025], yticks=[0.8, 1.0, 1.2, 1.4, 1.6],
                        yfmt=lambda v: f"x{v:.1f}", ylabel="prices, 2019 = 1", width=9.0, height=4.2, center=(-0.8, -0.45))
        src = source("BLS, producer price index for materials and components for construction, and CPI-U, via FRED", size=12)
        beat(self,
             "Part of it lately is materials. <bookmark mark='a'/> The prices builders pay for materials and components "
             f"rose {100 * (M['ppi'][2022] - 1):.0f} per cent between 2019 and 2022, <bookmark mark='b'/> against "
             f"{100 * (M['cpi'][2022] - 1):.0f} per cent for consumer prices, and they have not come back down. But "
             "materials only explain the last few years. The long fall in output per worker began decades earlier.",
             base=[ch.frame, src], steps=[[ch.lines["construction materials"], ch.labels["construction materials"]],
                                          [ch.lines["consumer prices"], ch.labels["consumer prices"]]])

    def why(self):
        g = VGroup(tx("Why? The usual explanations, none settled", 22, WHITE, bold=True),
                   tx("every site is a prototype: built once, on a different plot, to a different design", 18, BUILD),
                   tx("the work is split among many small firms, each with its own slice of the job", 18, PRICE),
                   tx("land-use rules, permits and codes vary from town to town", 18, MAKE),
                   tx("and the measurement itself: a better building is hard to count as more output", 18, GREY_A)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.2, 0])
        frame = draw.skyscraper_frame(floors=10, w=1.0, floor_h=0.14).move_to([5.4, -2.2, 0])
        tag = estimate_tag("this series' summary of the explanations economists give", size=12)
        beat(self,
             "Why has construction not improved? Economists argue about it, and the honest answer is that nobody has "
             "settled it. <bookmark mark='a'/> One explanation is that every site is a prototype: each building is "
             "made once, on a different plot, to a different design, so the lessons of the last one only partly carry "
             "over. <bookmark mark='b'/> Another is fragmentation: the work is split among many small firms, each doing "
             "its slice, with no one firm able to redesign the whole. <bookmark mark='c'/> A third is the rules: every "
             "town has its own permits and codes. <bookmark mark='d'/> And a fourth is the measurement: if buildings "
             "today are safer, quieter and better insulated, some of the improvement may be missing from the "
             "statistics. The Empire State Building's frame rose four and a half storeys a week in 1930; whatever the "
             "answer is, it is not that builders forgot how.",
             base=[frame, tag], steps=[g[0:2], g[2], g[3], g[4]])
