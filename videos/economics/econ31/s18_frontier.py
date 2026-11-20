from __future__ import annotations

from videos.economics.econ31.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ after the surge", r"What did 2021--26 teach central banks?",
             "Chapter sixteen. Frontier: after the surge.", lit={2022: r"the fastest rises since the 1980s"},
             scale=("nation", "world"), horizon=("a month", "years"))
        self.cycle()
        self.losses()
        self.open_()

    def cycle(self):
        F = load("frontier")
        ax = plane([2019, 2027], [0, 10], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[2019, 2021, 2023, 2025, 2027], yticks=[0, 2, 4, 6, 8, 10], ylabel=r"percent",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        cpi = path(ax, F["cpi_t"], F["cpi"], INFL, 3, xr=(2019, 2027), smooth=False)
        ff = path(ax, F["ff_t"], F["ff"], RATE, 3.5, smooth=False)
        target = seg(ax, 2019, 2, 2027, 2, CB, 1.6, dashed=True)
        side = VGroup(
            label(rf"red: \ consumer prices over 12 months, \\ peaking at {F['cpi_peak']:.1f}\% in "
                  rf"{F['cpi_peak_date'][:4]}", font_size=18, color=INFL),
            label(rf"pink: \ the funds rate's ceiling, \\ zero to {F['ff_peak']:.1f}\% in sixteen months", font_size=18,
                  color=RATE),
            label(r"late: \ the rate began to rise \\ a year after inflation did", font_size=18, color=HOLD),
            label(r"inflation came down \\ without the recession \\ many forecast", font_size=18, color=OUTPUT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"BLS CPI and the Federal Reserve's target range, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "The newest test of everything in this part began in 2021. <bookmark mark='a'/> Consumer price "
            f"inflation rose to {F['cpi_peak']:.1f} percent by mid-2022. <bookmark mark='b'/> The Federal Reserve "
            f"raised its rate from zero to {F['ff_peak']:.1f} percent in sixteen months, the fastest rise since "
            "the early 1980s. <bookmark mark='c'/> It started late, about a year after inflation took off, partly "
            "because a new framework had promised to let inflation run a little above target after years below "
            "it, and partly because the surge was first read as passing. <bookmark mark='d'/> Inflation then fell "
            "a long way without the recession many forecasters expected, which the anchored expectations of Part "
            "28 and the supply shocks of Part 30 help explain, and which the profession is still arguing about."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(target), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(cpi), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(ff), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def losses(self):
        F = load("frontier")
        ax = plane([2019, 2027], [-260, 120], center=LEFT * 3.3 + DOWN * 0.4, x_length=5.6, y_length=4.4,
                   xticks=[2019, 2021, 2023, 2025, 2027], yticks=[-250, -200, -150, -100, -50, 0, 50, 100],
                   ylabel=r"owed to the Treasury, \ \$ billions", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=13)
        ax2 = plane([2019, 2027], [0, 10], center=RIGHT * 3.3 + DOWN * 0.4, x_length=5.6, y_length=4.4,
                    xticks=[2019, 2021, 2023, 2025, 2027], yticks=[0, 2, 4, 6, 8, 10],
                    ylabel=r"the Fed's assets, \ \$ trillions", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                    font_size=13)
        zero = seg(ax, 2019, 0, 2027, 0, GREY_C, 1.5)
        rem = path(ax, F["rem_t"], F["rem"], INFL, 2.8, smooth=False)
        assets = path(ax2, F["a_t"], F["assets"], CB, 3, smooth=False)
        n1 = label(rf"the deferred asset: \ \${F['deferred_max']:.0f} billion \\ at its deepest, \ "
                   rf"{F['deferred_max_date'][:4]}", font_size=16, color=INFL).next_to(ax, UP, buff=0.15)
        n2 = label(rf"runoff: \ \${F['peak']:.1f} trillion in {F['peak_date'][:4]}, \\ \${F['last']:.1f} trillion "
                   rf"now", font_size=16, color=CB).next_to(ax2, UP, buff=0.15)
        foot = label(r"a central bank paying more on reserves than it earns on its bonds \ loses money, \ but cannot "
                     r"run out of it", font_size=20, color=E.ACCENT).to_edge(DOWN, buff=0.25)
        tag = data_tag(r"Federal Reserve Board: \ H.4.1 (remittances; \ total assets), \ via FRED", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Two consequences are still unwinding. <bookmark mark='a'/> A floor system means paying interest on "
            "trillions of reserves. When the Fed raised its rate, it paid more on reserves than it earned on the "
            "bonds it had bought at low yields, and from September 2022 it ran losses. It records them as a "
            "deferred asset, an amount it will keep back from future payments to the Treasury; at its deepest, in "
            f"{F['deferred_max_date'][:4]}, {F['deferred_max']:.0f} billion dollars. <bookmark mark='b'/> And it "
            f"shrank its balance sheet, from {F['peak']:.1f} trillion dollars to {F['last']:.1f}. "
            "<bookmark mark='c'/> A central bank can lose money without running out of it, since it creates the "
            "money it pays with. Whether losses threaten its independence, and how small the balance sheet can "
            "get while reserves stay ample, are open questions."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(ax2), FadeIn(zero), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(rem), FadeIn(n1), run_time=2)
            vo.wait_until("b")
            self.play(Create(assets), FadeIn(n2), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def open_(self):
        rows = VGroup(
            label(r"open questions", font_size=27, color=E.ACCENT),
            label(r"how to separate a central bank's choices from what its choices reveal \ (the information effect)",
                  font_size=21, color=METHOD["hf_info"]),
            label(r"why the neutral rate fell, \ and whether it is rising again", font_size=21, color=CB),
            label(r"how large a balance sheet a floor system needs", font_size=21, color=RES),
            label(r"how much of 2021--23 was policy, \ and how much the supply shocks undoing themselves",
                  font_size=21, color=INFL),
            label(r"how monetary policy reaches households that differ \ (Part 52)", font_size=21, color=OUTPUT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Nakamura and Steinsson (2018); \ Holston, \ Laubach and Williams (2023); \ "
                            r"Kaplan, \ Moll "
                            r"and Violante, \ \emph{AER} 108(3) (2018)", corner=DR, font_size=12)
        with self.voiceover(
            "The open questions. <bookmark mark='a'/> How to separate what a central bank chooses from what its "
            "choices reveal. <bookmark mark='b'/> Why the neutral rate fell, and whether it is rising again. "
            "<bookmark mark='c'/> How large a balance sheet a floor system needs. <bookmark mark='d'/> How much "
            "of the fall in inflation after 2022 was policy, and how much was supply shocks undoing themselves. "
            "<bookmark mark='e'/> And how monetary policy reaches households that differ in wealth and debts, "
            "which Part 52 takes up."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
