from __future__ import annotations

from videos.economics.econ33.common import *  # noqa: F403


class Fighting(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Fighting a crisis", r"What stops a panic once it has started?",
             "Chapter eleven. Fighting a crisis.", lit={1873: r"Bagehot", 2009: r"stress tests", 2020: r"the "
                                                                                                    r"pandemic"},
             scale=("nation", "world"), horizon=("a day", "a year"))
        self.toolkit()
        self.swaps()

    def toolkit(self):
        F = load("fight")
        cards = point_cards([
            (r"lend freely", r"against good collateral, \\ at a penalty rate: \\ Bagehot's rule (Part 26)", CB),
            (r"guarantee", r"deposits, \ money funds, \\ banks' new debt: \\ stop the run itself", CALM),
            (r"recapitalize", r"put capital into banks \\ so they can lend again: \\ TARP, \ October 2008", HOUSE),
            (r"test, \ and show", rf"May 2009: \ {F['scap_banks']} banks, \\ {F['scap_short']} short by \\ "
                                  rf"\${F['scap_gap']} billion; \ results public", RATE),
        ], width=12.6, cols=2, font_size=22).move_to(DOWN * 0.2)
        head = label(r"the toolkit", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.45)
        foot = label(r"every rescue teaches lenders to expect the next one: \ the case for preventing booms",
                     font_size=21, color=HOLD).to_edge(DOWN, buff=0.3)
        tag = published_tag(r"Bagehot, \ \emph{Lombard Street} (1873); \ Board of Governors, \ SCAP results, \ 7 May "
                            r"2009", corner=DR, font_size=12)
        with self.voiceover(
            "Once a panic has started, what stops it? The answers of 2008 are older than they looked. "
            "<bookmark mark='a'/> Lend freely, against good collateral, at a penalty rate: Walter Bagehot's rule of "
            "1873, from Part twenty-six, applied to dealers, money funds and the commercial paper market as well as "
            "banks. <bookmark mark='b'/> Guarantee the liabilities that are running, as the Treasury did for money "
            "funds on the nineteenth of September and governments across Europe did for bank deposits and debt. "
            "<bookmark mark='c'/> Put capital into the banks, so that they can absorb losses and lend again: the "
            "Troubled Asset Relief Program, first meant to buy bad assets, was used instead in October to buy "
            "shares in banks. <bookmark mark='d'/> And find out how big the hole is, and say so. In May 2009 the "
            f"Federal Reserve published stress tests of the {F['scap_banks']} largest banks: {F['scap_short']} "
            f"needed more capital, {F['scap_gap']} billion dollars in all, to be raised within six months. Markets "
            "had feared worse; once the number was public, banks could raise it. <bookmark mark='e'/> The cost of "
            "all this is not only money. Every rescue teaches lenders to expect the next one, which is the case for "
            "stopping booms before they start: chapter twelve."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def swaps(self):
        F = load("fight")
        ax = plane([2007.5, 2022], [0, 620], center=LEFT * 1.8 + DOWN * 0.4, x_length=9.0, y_length=4.4,
                   xticks=[2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022], yticks=[0, 200, 400, 600],
                   ylabel=r"the Fed's dollar swap lines with other central banks, \ \$ billion",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        ln = path(ax, F["t"], F["swaps"], CB, 3.2, xr=(2007.5, 2022), smooth=False)
        side = VGroup(
            label(rf"December 2008: \\ \${F['peak08']:.0f} billion", font_size=20, color=CB),
            label(rf"May 2020: \\ \${F['peak20']:.0f} billion", font_size=20, color=CB),
            label(rf"the Fed's assets in 2020: \\ \${F['wal20_before']:.1f} $\to$ \${F['wal20_after']:.1f} "
                  r"trillion \\ in fourteen weeks", font_size=19, color=WHITE),
            label(r"the 2008 playbook, \\ run in weeks, \ not months", font_size=19, color=HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Board of Governors (H.4.1), \ via FRED: \ SWPT, \ WALCL", corner=DR, font_size=12)
        with self.voiceover(
            "The world's banks borrow in dollars, so a dollar panic is a global one. <bookmark mark='a'/> The "
            "Federal Reserve lent dollars to other central banks, which lent them on to their own banks: at the "
            f"peak, in December 2008, {F['peak08']:.0f} billion dollars. <bookmark mark='b'/> In March 2020, as "
            "the pandemic closed economies, the same lines were opened again and reached "
            f"{F['peak20']:.0f} billion dollars by May. <bookmark mark='c'/> The Fed's balance sheet went from "
            f"{F['wal20_before']:.1f} to {F['wal20_after']:.1f} trillion dollars in fourteen weeks, and most of the "
            "facilities of 2008 were reopened, some within days. <bookmark mark='d'/> The playbook had been "
            "written; this time it was run in weeks. Whether its being known in advance makes the next boom bigger "
            "is the question that opens the next chapter."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
