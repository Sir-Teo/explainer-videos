from __future__ import annotations

from videos.industry.industry28.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.buffett()
        self.fares()
        self.profits()
        self.title()

    def buffett(self):
        q = quote(["'Indeed, if a farsighted capitalist had been present at Kitty Hawk, he would have done his successors",
                   "a huge favor by shooting Orville down.'"], "Warren Buffett, Berkshire Hathaway's letter to shareholders for 2007",
                  size=20).move_to([0, 1.6, 0])
        plane = draw.plane(4.0).move_to([0, -1.2, 0])
        src = source("Berkshire Hathaway, letter to shareholders for 2007", size=12)
        beat(self,
             "In 2008 the investor Warren Buffett wrote that airlines were the worst sort of business: "
             "one that grows fast, needs huge amounts of capital, and earns little or nothing. <bookmark mark='a'/> 'If a "
             "farsighted capitalist had been present at Kitty Hawk,' he wrote, 'he would have done his successors a huge "
             "favor by shooting Orville down.' <bookmark mark='b'/> He knew from experience: Berkshire had bought into US "
             "Air in 1989, and watched it stop paying.",
             base=[src], steps=[q, plane])

    def fares(self):
        H = R["hook"]["real"]
        ch = line_chart({"airline fares after inflation": (H, SKY)}, x=(2000, 2025), y=(0.4, 1.1),
                        xticks=[2000, 2005, 2010, 2015, 2020, 2025], yticks=[0.4, 0.6, 0.8, 1.0], yfmt=lambda v: f"x{v:.1f}",
                        ylabel="American airline fares divided by all consumer prices, 2000 = 1", width=9.4, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        m = marker(ch.ax, 2025, H[2025], f"2025: x{H[2025]:.2f}", GOOD, side=LEFT)
        src = source("BLS, CPI-U for airline fares and all items (annual averages), via FRED", size=12)
        beat(self,
             "Yet for its customers the industry has been a gift. <bookmark mark='a'/> Since 2000, the fares Americans pay, "
             f"measured by the consumer price index, have fallen {100 * (1 - H[2025]):.0f} per cent after inflation. "
             "<bookmark mark='b'/> A ticket that cost a hundred dollars in 2000 would, if it had risen with prices in "
             f"general, cost a hundred dollars of 2000's money today; instead it costs about {100 * H[2025]:.0f}. Flying has "
             "become an ordinary thing that ordinary people do.",
             base=[ch.frame, src], steps=[ch.lines["airline fares after inflation"], m])

    def profits(self):
        P = R["hook"]["profit"]
        items = [(str(y)[2:], abs(P[y][0]), GOOD if P[y][0] > 0 else BAD, f"{P[y][0]:+.0f}") for y in range(2009, 2026)]
        cols = vbars(items, base_y=-1.6, height=3.2, width=0.5, gap=0.22, size=12, max_value=36)
        lab = tx("nine listed American airlines together: net income, $bn a year, 2009-2025", 16, GREY_A).to_edge(UP, buff=0.7)
        tot = tx(f"in all: ${R['hook']['total']:.0f}bn on ${R['hook']['total_rev'] / 1e3:.2f} trillion of revenue: "
                 f"{100 * R['hook']['total'] / R['hook']['total_rev']:.1f} cents a dollar", 18, CASH, bold=True).to_edge(DOWN, buff=0.9)
        src = source("Delta, United, American, Southwest, JetBlue, Alaska, Frontier, Allegiant and Hawaiian; Forms 10-K via SEC company facts", size=12)
        beat(self,
             "And for its owners? <bookmark mark='a'/> Add up nine of America's listed airlines. From 2009 to 2019 they "
             f"made money, as much as {P[2015][0]:.0f} billion dollars in 2015. <bookmark mark='b'/> In 2020 they lost "
             f"{abs(P[2020][0]):.0f} billion. <bookmark mark='c'/> Over seventeen years they earned {R['hook']['total']:.0f} "
             f"billion dollars on {R['hook']['total_rev'] / 1e3:.1f} trillion of revenue: about three cents in every dollar "
             "a passenger paid.",
             base=[lab, src], steps=[VGroup(*cols[:11]), VGroup(*cols[11:12]), [VGroup(*cols[12:]), tot]])

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part twenty-eight: airlines. Why has an industry that changed the world lost "
                            "money over most of its history?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
